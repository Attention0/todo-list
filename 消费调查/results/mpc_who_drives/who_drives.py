"""Bounded observable moderation; direct PR9 preparation reuse, aggregate exports only."""
from pathlib import Path
import sys, argparse, json, hashlib
from importlib.metadata import version
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint
from sklearn.model_selection import StratifiedKFold
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'mpc_size_curve'))
import size_curve as prior
SEED=20261004
B=499
TIER1=['liquidity','income','food','medical','subsidy']
TIER2=['age','education','household_size','minor_child','housing','work']
LABELS={'liquidity':'Emergency liquidity','income':'Personal income rank','food':'Baseline food expenditure','medical':'Baseline medical expenditure','subsidy':'Prior subsidy experience','age':'Age','education':'Education','household_size':'Household size','minor_child':'Minor child present','housing':'Housing tenure','work':'Work status'}
RAW={'liquidity':'q07_emergfund','income':'income','food':'q29_foodexp','medical':'q30_medexp','age':'q42_age','education':'q43_edu','household_size':'q28_hhsize'}
CATEGORIES={'subsidy':('q31_gotsubsidy',2,{1:'yes',3:'unknown'}),'housing':('q26_housing',1,{2:'rent',3:'other'}),'work':('q24_workstat',1,{2:'retired',3:'student',4:'not_working',5:'other'})}
FORMS=prior.FORMS
FW={'cash':[1,0,0],'restricted':[0,.5,.5],'restricted-cash':[-1,.5,.5],'food-cash':[-1,1,0],'medical-cash':[-1,0,1]}

def covariates(d):
    X=pd.DataFrame(index=d.index);groups={};meta=[]
    for var in TIER1+TIER2:
        vals={}
        if var in RAW: vals[var]=d[RAW[var]].astype(float)
        elif var=='minor_child': vals[var]=d.q27_minorchild.eq(1).astype(float)
        else:
            raw,ref,codes=CATEGORIES[var]
            for code,label in codes.items():vals[var+'_'+label]=d[raw].eq(code).astype(float)
        groups[var]=list(vals)
        for col,x in vals.items():
            sd=x.std();assert sd>0 and x.notna().all()
            X[col]=(x-x.mean())/sd
            meta.append(dict(moderator=var,column=col,mean=x.mean(),sd=sd,coding='category_dummy' if var in CATEGORIES else 'binary_yes' if var=='minor_child' else 'rank_or_age',reference=CATEGORIES[var][1] if var in CATEGORIES else np.nan))
    return X,groups,pd.DataFrame(meta)

def design(d,X,interaction=True):
    # Form-specific blocks avoid accidental sample-size pooled Restricted arm.
    out={}
    for f in FORMS:
        mask=d.form.eq(f).to_numpy().astype(float)
        out[f+':intercept']=mask;out[f+':z']=mask*d.z.to_numpy()
        for col in X:
            out[f+':'+col]=mask*X[col].to_numpy()
            if interaction:out[f+':z:'+col]=mask*d.z.to_numpy()*X[col].to_numpy()
    return pd.DataFrame(out,index=d.index)

def fit(d,X,y='top75',interaction=True):
    M=design(d,X,interaction);m=sm.OLS(d[y].to_numpy(),M).fit(cov_type='HC3');assert np.linalg.matrix_rank(M)==len(M.columns)
    return m

def vec(m,est,col=None,profile=None):
    v=pd.Series(0.,index=m.params.index)
    for f,w in zip(FORMS,FW[est]):
        if col is not None:v[f+':z:'+col]=w
        else:
            v[f+':z']=w
            if profile is not None:
                for c,value in profile.items():v[f+':z:'+c]=w*value
    return v.to_numpy()

def contrast(m,v):
    eff=float(v@m.params);se=float(np.sqrt(max(0,v@m.cov_params()@v)))
    return dict(estimate=eff,se=se,lo=eff-1.95996398454*se,hi=eff+1.95996398454*se,p=float(2*stats.norm.sf(abs(eff/se))))

def omnibus(m,V):
    V=np.atleast_2d(V);b=V@m.params.to_numpy();cov=V@m.cov_params().to_numpy()@V.T;df=np.linalg.matrix_rank(cov);stat=float(b@np.linalg.pinv(cov)@b)
    return dict(wald=stat,df=int(df),p=float(stats.chi2.sf(stat,df)))

def moderation(d,X,groups,variables,y='top75',sample='R'):
    rows=[]
    for var in variables:
        cols=groups[var];m=fit(d,X[cols],y)
        # Explicit Cash-only regression, verify identical block from full form model.
        ix=d.form.eq('cash');cash_X=sm.add_constant(pd.DataFrame({'z':d.loc[ix,'z'],**{c:X.loc[ix,c] for c in cols},**{'z_'+c:d.loc[ix,'z']*X.loc[ix,c] for c in cols}}));cm=sm.OLS(d.loc[ix,y],cash_X).fit(cov_type='HC3')
        for c in cols:
            assert np.allclose(m.params['cash:z:'+c],cm.params['z_'+c])
            assert np.allclose(m.bse['cash:z:'+c],cm.bse['z_'+c])
        for est in ['cash','restricted-cash','food-cash','medical-cash']:
            primary=est in ['cash','restricted-cash']
            for c in cols:
                rows.append(dict(moderator=var,label=LABELS[var],column=c,record_type='component',estimand=est,outcome=y,sample=sample,N=int(m.nobs),tier=1 if var in TIER1 else 2,primary=primary,**contrast(m,vec(m,est,c))))
            rows.append(dict(moderator=var,label=LABELS[var],column='all',record_type='omnibus',estimand=est,outcome=y,sample=sample,N=int(m.nobs),tier=1 if var in TIER1 else 2,primary=primary,**omnibus(m,[vec(m,est,c) for c in cols])))
    t=pd.DataFrame(rows);t['holm_p']=np.nan
    for est in ['cash','restricted-cash']:
        ix=t.index[t.estimand.eq(est)&t.record_type.eq('omnibus')];t.loc[ix,'holm_p']=multipletests(t.loc[ix,'p'],method='holm')[1]
        for var in variables:
            if len(groups[var])==1:
                mask=t.estimand.eq(est)&t.moderator.eq(var);t.loc[mask,'holm_p']=t.loc[mask&t.record_type.eq('omnibus'),'holm_p'].iloc[0]
    return t

def bins(d):
    return {'liquidity':pd.cut(d.q07_emergfund,[-1,5,8,10],labels=['low_0_5','middle_6_8','high_9_10']),
            'income':pd.cut(d.income,[0,3,4,6],labels=['low_rank1_3','middle_rank4','high_rank5_6']),
            'food':pd.cut(d.q29_foodexp,[0,2,4,6],labels=['low_rank1_2','middle_rank3_4','high_rank5_6']),
            'medical':pd.cut(d.q30_medexp,[0,2,4,6],labels=['low_0_500','middle_501_5000','high_above5000']),
            'subsidy':d.q31_gotsubsidy.map({1:'yes',2:'no',3:'unknown'})}

def curve_contribution(d,groupings,out):
    cells=[];contrib=[];slopes=[];raw=[]
    for var,b in groupings.items():
        assert b.notna().all()
        ordered=list(b.cat.categories) if isinstance(b.dtype,pd.CategoricalDtype) else ['yes','no','unknown']
        for group in ordered:
            g=d[b.eq(group)];share=len(g)/len(d);means={};variances={};counts={}
            for f in FORMS:
                for amount in prior.AMT:
                    yy=g[(g.form==f)&(g.amount==amount)].top75;n=len(yy);assert n>1
                    mean=yy.mean();se=np.sqrt(yy.var(ddof=1)/n);lo,hi=proportion_confint(int(yy.sum()),n,method='wilson')
                    means[f,amount]=mean;variances[f,amount]=se**2;counts[f,amount]=n
                    raw.append(dict(moderator=var,group=str(group),form=f,amount=amount,N=n,subgroup_N=len(g),population_share=share,probability=mean,se=se,lo=lo,hi=hi,interval='Wilson'))
                    if f=='cash':cells.append(raw[-1])
            for amount in prior.AMT:
                p=.5*(means['food',amount]+means['medical',amount]);se=.5*np.sqrt(variances['food',amount]+variances['medical',amount]);cells.append(dict(moderator=var,group=str(group),form='restricted',amount=amount,N=counts['food',amount]+counts['medical',amount],food_N=counts['food',amount],medical_N=counts['medical',amount],subgroup_N=len(g),population_share=share,probability=p,se=se,lo=p-1.96*se,hi=p+1.96*se,interval='independent-cell delta normal'))
            delta=means['cash',5000]-means['cash',200];se=np.sqrt(variances['cash',5000]+variances['cash',200])
            contrib.append(dict(moderator=var,group=str(group),subgroup_N=len(g),population_share=share,p200=means['cash',200],p1000=means['cash',1000],p5000=means['cash',5000],endpoint_change=delta,endpoint_se=se,endpoint_lo=delta-1.96*se,endpoint_hi=delta+1.96*se,contribution=share*delta,contribution_se=share*se,contribution_lo=share*(delta-1.96*se),contribution_hi=share*(delta+1.96*se)))
            m=fit(g,pd.DataFrame(index=g.index))
            for est in ['cash','restricted','restricted-cash','food-cash','medical-cash']:slopes.append(dict(moderator=var,group=str(group),N=len(g),estimand=est,**contrast(m,vec(m,est))))
    cc=pd.DataFrame(cells);cc[cc.form.eq('cash')].to_csv(out/'subgroup_cash_curves.csv',index=False);cc[cc.form.eq('restricted')].to_csv(out/'subgroup_restricted_curves.csv',index=False)
    pd.DataFrame(raw).to_csv(out/'subgroup_form_cells.csv',index=False)
    ct=pd.DataFrame(contrib);total=ct.groupby('moderator').contribution.transform('sum');ct['partition_standardized_total']=total;ct['share_of_total_decline']=ct.contribution/total;ct['raw_unstandardized_cash_change']=d[(d.form=='cash')&(d.amount==5000)].top75.mean()-d[(d.form=='cash')&(d.amount==200)].top75.mean();ct.to_csv(out/'cash_decline_contributions.csv',index=False)
    sl=pd.DataFrame(slopes);sl.to_csv(out/'subgroup_differential_slopes.csv',index=False)
    return cc,ct,sl

def joint(d,X,cols,out):
    m=fit(d,X[cols]);base=fit(d,pd.DataFrame(index=d.index));rows=[];tests=[]
    for name,model,profile in [('baseline',base,None),('joint_average',m,X[cols].mean())]:
        for est in ['cash','restricted','restricted-cash']:rows.append(dict(model=name,record_type='average_slope',column='empirical_R_mean',estimand=est,N=int(model.nobs),**contrast(model,vec(model,est,profile=profile))))
    for est in ['cash','restricted-cash']:
        V=[vec(m,est,c) for c in cols];tests.append(dict(test=est+'_all_moderation',N=len(d),**omnibus(m,V)))
        for c in cols:rows.append(dict(model='joint',record_type='moderation',column=c,estimand=est,N=len(d),**contrast(m,vec(m,est,c))))
    jt=pd.DataFrame(tests);jt['holm_two_p']=multipletests(jt.p,method='holm')[1];jt.to_csv(out/'joint_tests.csv',index=False)
    pd.DataFrame(rows).to_csv(out/'joint_tier1_model.csv',index=False)
    coefficients=[];signature=[]
    for term in m.params.index:
        vv=pd.Series(0.,index=m.params.index);vv[term]=1
        coefficients.append(dict(term=term,**contrast(m,vv.to_numpy())))
    pd.DataFrame(coefficients).to_csv(out/'joint_coefficients.csv',index=False)
    for var in TIER1:
        single=fit(d,X[[c for c in cols if c==var or c.startswith(var+'_')]])
        for c in [c for c in cols if c==var or c.startswith(var+'_')]:
            for name,model in [('single',single),('joint',m)]:
                v=pd.Series(0.,index=model.params.index);v['cash:'+c]=1;v['cash:z:'+c]=-1
                signature.append(dict(moderator=var,column=c,model=name,estimand='cash200_level_moderation',**contrast(model,v.to_numpy())))
    pd.DataFrame(signature).to_csv(out/'mechanism_signature_levels.csv',index=False)
    ranges=[]
    for est in ['cash','restricted-cash']:
        value=np.zeros(len(d))
        for f,w in zip(FORMS,FW[est]):value+=w*(m.params[f+':z']+X[cols].to_numpy()@np.array([m.params[f+':z:'+c] for c in cols]))
        for q,label in [(0,'min'),(.05,'p05'),(.25,'p25'),(.5,'p50'),(.75,'p75'),(.95,'p95'),(1,'max')]:ranges.append(dict(estimand=est,profile_quantile=label,predicted_slope=np.quantile(value,q)))
    pd.DataFrame(ranges).to_csv(out/'joint_profile_range.csv',index=False)
    return m

def fit_blocks(d,X,y,train,weights,interaction):
    arr=X.to_numpy();z=d.z.to_numpy();b=np.column_stack([np.ones(len(d)),z,arr]+[z[:,None]*arr] if interaction else [np.ones(len(d)),z,arr]);betas=[]
    for f in FORMS:
        ix=train&d.form.eq(f).to_numpy();root=np.sqrt(weights[ix]);betas.append(np.linalg.lstsq(b[ix]*root[:,None],y[ix]*root,rcond=None)[0])
    return betas

def predict_blocks(beta,X,z,interaction=True):
    a=X.to_numpy();z=np.broadcast_to(z,len(X));b=np.column_stack([np.ones(len(X)),z,a]+[z[:,None]*a] if interaction else [np.ones(len(X)),z,a]);return np.stack([b@v for v in beta],axis=1)

def crossfit(d,X,fold,weights):
    n=len(d);y=d.top75.to_numpy();form=pd.Categorical(d.form,categories=FORMS).codes;obs=np.arange(n);z=d.z.to_numpy();preds={name:np.zeros(n) for name in ['baseline','level','full']};score={t:np.zeros(n) for t in ['cash_decline','restricted_cash_delta']};forecast={t:np.zeros(n) for t in score};quintile={t:np.zeros(n,int) for t in score};cf=np.zeros((n,3,3))
    for k in range(5):
        train=fold!=k;test=fold==k
        for name,xx,inter in [('baseline',X.iloc[:,:0],False),('level',X,False),('full',X,True)]:
            beta=fit_blocks(d,xx,y,train,weights,inter);pr=predict_blocks(beta,xx,z,inter);preds[name][test]=pr[obs[test],form[test]]
            if name=='full':
                pc=np.stack([predict_blocks(beta,X,t) for t in [-1,0,1]],axis=2);cf[test]=pc[test]
                cd=pc[:,0,0]-pc[:,0,2];rc=.5*(pc[:,1,2]-pc[:,1,0]+pc[:,2,2]-pc[:,2,0])+cd
                for target,val in [('cash_decline',cd),('restricted_cash_delta',rc)]:
                    cuts=weighted_quantile(val[train],weights[train],[.2,.4,.6,.8]);quintile[target][test]=np.searchsorted(cuts,val[test],side='right')+1;forecast[target][test]=val[test]
    resid=y-preds['full']
    for target,w in [('cash_decline',np.array([-1,0,0.])),('restricted_cash_delta',np.array([-1,.5,.5]))]:
        mu=(cf[:,:,2]-cf[:,:,0])@w
        aug=9*w[form]*resid*((z==1)-(z==-1).astype(int))
        score[target]=mu+aug
    metrics={}
    yybar=np.average(y,weights=weights);var=np.average((y-yybar)**2,weights=weights)
    for name,p in preds.items():
        mse=np.average((y-p)**2,weights=weights);metrics[name+'_mse']=mse;metrics[name+'_r2']=1-mse/var;metrics[name+'_clipped_mse']=np.average((y-np.clip(p,0,1))**2,weights=weights)
    metrics['full_vs_level_mse_gain']=metrics['level_mse']-metrics['full_mse'];metrics['full_vs_baseline_mse_gain']=metrics['baseline_mse']-metrics['full_mse'];metrics['full_vs_level_relative_mse_gain']=metrics['full_vs_level_mse_gain']/metrics['level_mse']
    stats_out={};cal=[]
    for target in score:
        # Fold FE calibrates out common fold-trained level variation.
        calX=np.column_stack([np.ones(n),forecast[target],pd.get_dummies(fold,dtype=float).to_numpy()[:,1:]])
        beta=np.linalg.lstsq(calX*np.sqrt(weights[:,None]),score[target]*np.sqrt(weights),rcond=None)[0];stats_out[target+':calibration_slope']=beta[1]
        for q in range(1,6):
            ix=quintile[target]==q;assert ix.sum()>0
            estimate=np.average(score[target][ix],weights=weights[ix]);stats_out[target+':q'+str(q)]=estimate
            cal.append(dict(target=target,quintile=q,N=int(ix.sum()),predicted_sensitivity=np.average(forecast[target][ix],weights=weights[ix]),aipw_sensitivity=estimate))
        stats_out[target+':highest_minus_lowest']=stats_out[target+':q5']-stats_out[target+':q1']
    stats_out.update(metrics)
    return stats_out,pd.DataFrame(cal),forecast,quintile,preds,cf

def weighted_quantile(values,w,qs):
    ix=np.argsort(values);cdf=(np.cumsum(w[ix])-.5*w[ix])/w.sum();return np.interp(qs,cdf,values[ix])

def prediction(d,X,out):
    folds=np.zeros(len(d),int)
    for k,(_,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=SEED).split(d,d.cell)):folds[te]=k
    point,cal,forecast,quint,preds,cf=crossfit(d,X,folds,np.ones(len(d)));rng=np.random.default_rng(SEED);boot={key:[] for key in point}
    for b in range(B):
        s,*_=crossfit(d,X,folds,rng.exponential(1,len(d)))
        for key,value in s.items():boot[key].append(value)
        if (b+1)%100==0:print('Calibration model-refit bootstrap',b+1,flush=True)
    summary=[]
    for key,value in point.items():
        lo,hi=np.quantile(boot[key],[.025,.975]);summary.append(dict(statistic=key,estimate=value,lo=lo,hi=hi,bootstrap_se=np.std(boot[key],ddof=1),B=B,interval='exponential-weight model-refit percentile; fixed folds'))
    st=pd.DataFrame(summary);st.to_csv(out/'prediction_summary.csv',index=False)
    for i,row in cal.iterrows():
        r=st[st.statistic.eq(row.target+':q'+str(row.quintile))].iloc[0];cal.loc[i,'lo']=r.lo;cal.loc[i,'hi']=r.hi
    # Also display raw randomized endpoint estimates for every heldout quintile.
    raw=[]
    for target in quint:
        w=np.array([-1.,0,0]) if target=='cash_decline' else np.array([-1.,.5,.5])
        for q in range(1,6):
            ix=quint[target]==q;est=0.;v=0.
            for j,f in enumerate(FORMS):
                for amount,sgn in [(200,-1),(5000,1)]:
                    g=d[ix&d.form.eq(f)&d.amount.eq(amount)].top75;assert len(g)>1
                    est+=w[j]*sgn*g.mean();v+=w[j]**2*g.var(ddof=1)/len(g)
            cal.loc[cal.target.eq(target)&cal.quintile.eq(q),'randomized_raw_sensitivity']=est
            cal.loc[cal.target.eq(target)&cal.quintile.eq(q),'raw_conditional_se']=np.sqrt(v)
            for f in FORMS:
                for amount in prior.AMT:
                    g=d[ix&d.form.eq(f)&d.amount.eq(amount)].top75;lo,hi=proportion_confint(int(g.sum()),len(g),method='wilson');raw.append(dict(target=target,quintile=q,form=f,amount=amount,N=len(g),probability=g.mean(),lo=lo,hi=hi))
    cal.to_csv(out/'prediction_calibration.csv',index=False);pd.DataFrame(raw).to_csv(out/'prediction_quintile_cells.csv',index=False)
    dist=[]
    for target,val in forecast.items():
        for q in [0,.05,.25,.5,.75,.95,1]:dist.append(dict(target=target,quantile=q,predicted_sensitivity=np.quantile(val,q)))
    pd.DataFrame(dist).to_csv(out/'prediction_sensitivity_distribution.csv',index=False)
    quality=[]
    for name,p in preds.items():quality.append(dict(model=name,observed_probability_outside01=np.mean((p<0)|(p>1)),min_prediction=p.min(),max_prediction=p.max()))
    quality.append(dict(model='full_all_counterfactuals',observed_probability_outside01=np.mean((cf<0)|(cf>1)),min_prediction=cf.min(),max_prediction=cf.max()))
    pd.DataFrame(quality).to_csv(out/'prediction_probability_diagnostics.csv',index=False)
    return cal,st

def figures(primary,cc,ct,sl,cal,st,out):
    folder=out/'figures';folder.mkdir(exist_ok=True)
    for num,est,title in [(1,'cash','Cash size-gradient moderation'),(2,'restricted-cash','Restricted minus Cash size-gradient moderation')]:
        g=primary[primary.record_type.eq('component')&primary.estimand.eq(est)].copy();g.to_csv(out/f'fig{num}_source.csv',index=False);fig,ax=plt.subplots(figsize=(9,5));pos=np.arange(len(g));ax.errorbar(g.estimate,pos,xerr=[g.estimate-g.lo,g.hi-g.estimate],fmt='o',capsize=3,color='#243746');labs=[LABELS[r.moderator]+(' ('+r.column.split('_',1)[1]+' vs no)' if r.moderator=='subsidy' else '') for r in g.itertuples()];ax.set(yticks=pos,yticklabels=labs,xlabel='Probability slope moderation per 1 R SD',title=title);ax.axvline(0,color='gray',lw=1);ax.invert_yaxis();fig.tight_layout();fig.savefig(folder/f'fig{num}_moderation.png',dpi=200);plt.close(fig)
    cc.to_csv(out/'fig3_source.csv',index=False);fig,axes=plt.subplots(5,3,figsize=(13,17));colors={'cash':'#243746','restricted':'#BC503F'}
    for i,var in enumerate(TIER1):
        groups=cc.loc[cc.moderator.eq(var),'group'].unique()
        for ax,group in zip(axes[i],groups):
            sub=cc[(cc.moderator==var)&(cc.group==group)]
            for f in ['cash','restricted']:
                g=sub[sub.form.eq(f)].sort_values('amount');ax.errorbar(g.amount,g.probability,yerr=[g.probability-g.lo,g.hi-g.probability],marker='o',capsize=2,label=f,color=colors[f]);
                for r in g.itertuples():ax.annotate(str(r.N),(r.amount,r.probability),xytext=(0,5 if f=='cash' else -12),textcoords='offset points',fontsize=7,color=colors[f])
            ax.set(xscale='log',xticks=prior.AMT,xticklabels=['200','1000','5000'],ylim=(-.03,max(.29,cc.hi.max()+.02)),title=LABELS[var]+'\n'+group+' | R N='+str(int(sub.subgroup_N.iloc[0])),ylabel='P(top category)');ax.xaxis.set_minor_locator(NullLocator());ax.legend(fontsize=7)
    fig.suptitle('Fixed observable groups; labels next to means are cell N',fontsize=13);fig.tight_layout(rect=(0,0,1,.97));fig.savefig(folder/'fig3_subgroup_curves.png',dpi=200);plt.close(fig)
    ct.to_csv(out/'fig4_source.csv',index=False);fig,axes=plt.subplots(1,5,figsize=(17,5))
    for ax,var in zip(axes,TIER1):
        g=ct[ct.moderator.eq(var)];pos=np.arange(len(g));ax.bar(pos,g.contribution,color='#243746');ax.errorbar(pos,g.contribution,yerr=1.96*g.contribution_se,fmt='none',ecolor='black',capsize=3);ax.set(xticks=pos,xticklabels=g.group,title=LABELS[var],ylabel='Population-share weighted endpoint change');ax.tick_params(axis='x',labelrotation=55);ax.axhline(0,color='gray',lw=.7)
    fig.suptitle('Separate partitions: contributions across variables must not be added');fig.tight_layout();fig.savefig(folder/'fig4_contributions.png',dpi=200);plt.close(fig)
    cal.to_csv(out/'fig5_source.csv',index=False);st.to_csv(out/'fig5_metrics_source.csv',index=False);fig,axes=plt.subplots(1,3,figsize=(15,4.7))
    for ax,target,title in [(axes[0],'cash_decline','Cash decline (200 minus 5000)'),(axes[1],'restricted_cash_delta','Restricted minus Cash endpoint difference')]:
        g=cal[cal.target.eq(target)];ax.plot(g.quintile,g.predicted_sensitivity,'o--',color='gray',label='OOF forecast');ax.errorbar(g.quintile,g.aipw_sensitivity,yerr=[g.aipw_sensitivity-g.lo,g.hi-g.aipw_sensitivity],fmt='o-',capsize=3,color='#243746',label='OOF AIPW / refit CI');ax.plot(g.quintile,g.randomized_raw_sensitivity,'x',color='#BC503F',label='Raw randomized estimate');ax.axhline(0,color='gray',lw=.7);ax.set(title=title,xticks=range(1,6),xlabel='Training-cut sensitivity quintile',ylabel='Probability difference');ax.legend(fontsize=7)
    g=st[st.statistic.isin(['baseline_mse','level_mse','full_mse'])];axes[2].errorbar(np.arange(len(g)),g.estimate,yerr=[g.estimate-g.lo,g.hi-g.estimate],fmt='o',capsize=3);axes[2].set(xticks=range(len(g)),xticklabels=['Baseline','Levels','Interactions'],title='5-fold OOF Brier (unclipped)',ylabel='Mean squared error');fig.tight_layout();fig.savefig(folder/'fig5_calibration.png',dpi=200);plt.close(fig)
    g=sl[sl.estimand.eq('restricted-cash')];g.to_csv(out/'subgroup_forest_source.csv',index=False);fig,ax=plt.subplots(figsize=(10,8));pos=np.arange(len(g));ax.errorbar(g.estimate,pos,xerr=1.96*g.se,fmt='o',capsize=3);ax.set(yticks=pos,yticklabels=g.moderator+' / '+g.group,xlabel='Restricted minus Cash probability slope',title='Within fixed groups (nominal pointwise 95% CI)');ax.axvline(0,color='gray');ax.invert_yaxis();fig.tight_layout();fig.savefig(folder/'subgroup_differential_forest.png',dpi=200);plt.close(fig)

def run(data,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);d=prior.prepare(data).reset_index(drop=True);X,groups,meta=covariates(d);meta.to_csv(out/'moderator_coding.csv',index=False)
    primary=moderation(d,X,groups,TIER1);secondary=moderation(d,X,groups,TIER2);primary.to_csv(out/'primary_moderator_interactions.csv',index=False);secondary.to_csv(out/'secondary_profile_interactions.csv',index=False)
    print(primary[primary.record_type.eq('omnibus')&primary.primary].to_string(index=False),flush=True)
    cc,ct,sl=curve_contribution(d,bins(d),out);cols=[c for v in TIER1 for c in groups[v]];joint(d,X,cols,out)
    rank=primary[primary.record_type.eq('omnibus')&primary.primary].groupby('moderator').p.min().reindex(TIER1).sort_values(kind='stable');selected=list(rank.index[:2]);checks=[]
    for sn,x in {'R':d,**{s:d[d['sample_'+s]] for s in ['A','C','Q1','Q2']}}.items():
        for y in ['top75','ordinal','midpoint','ge50']:checks.append(moderation(x,X.loc[x.index],groups,selected,y,sn))
    robust=pd.concat(checks,ignore_index=True);robust['holm_p']=np.nan;robust['inference']='descriptive selected-pattern robustness; no new confirmatory family';robust.to_csv(out/'moderator_robustness.csv',index=False)
    cal,st=prediction(d,X[cols],out);figures(primary,cc,ct,sl,cal,st,out)
    manifest=dict(seed=SEED,bootstrap_B=B,N=len(d),form_N=d.form.value_counts().to_dict(),samples={'R':len(d),**{s:int(d['sample_'+s].sum()) for s in ['A','C','Q1','Q2']}},raw_sha256=hashlib.sha256(Path(data).read_bytes()).hexdigest(),prior_script_sha256=hashlib.sha256(Path(prior.__file__).read_bytes()).hexdigest(),tier1=TIER1,tier2=TIER2,robustness_selected=selected,folds=5,individual_exports=False,versions={p:version(p) for p in ['numpy','pandas','scipy','statsmodels','scikit-learn','matplotlib']},prior_pr9_head='d749f5c0eab3938038882d948bc6370e78835249',prior_pr10_head='cb6910f1141943c1a6649ed77d0134f95b43770b',stopping_rule='No further observable-variable exploration of current data')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print('Completed bounded pass; robustness selection:',selected,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('data');parser.add_argument('--out',default=str(ROOT));args=parser.parse_args();run(args.data,args.out)
