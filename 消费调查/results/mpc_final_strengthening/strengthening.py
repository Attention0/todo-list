"""Final bounded strengthening pass, directly extending PR #9. Aggregate exports only."""
from pathlib import Path
import sys, argparse, json, hashlib, warnings
from importlib.metadata import version
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit
import patsy
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'mpc_size_curve'))
import size_curve as prior
warnings.filterwarnings('ignore',category=FutureWarning)
FORMS=prior.FORMS
AMOUNTS=prior.AMT
THRESHOLDS=['any_spending','ge10','ge25','ge50','top75']
OUTCOMES=['ordinal','midpoint','alt_top']+THRESHOLDS
FAMILY=['cash','food','medical','restricted','restricted-cash','food-medical']
CONTRASTS=['medical-cash','food-cash','restricted-cash']
SEED=20261003
B=5000
ROOT=Path(__file__).resolve().parent

def vectors(names,representation):
    """Per-form link/linear slopes or full endpoint changes, with named design columns."""
    result={}
    for form in FORMS:
        w=np.zeros(len(names))
        term='z' if representation=='trend' else 'C(amount)[T.5000]'
        w[names.index(term)]=1
        if form!='cash':
            w[names.index(f'C(form)[T.{form}]:'+term)]=1
        result[form]=w
    result['restricted']=.5*(result['food']+result['medical'])
    for k in ['restricted-cash','food-cash','medical-cash','food-medical']:
        a,b=k.split('-');result[k]=result[a]-result[b]
    return result

def inference(effect,se,null=0):
    p=2*stats.norm.sf(abs((effect-null)/se)) if se>0 else float(effect==null)
    return dict(estimate=float(effect),se=float(se),lo=float(effect-1.96*se),hi=float(effect+1.96*se),p=float(p))

def linear_contrast(model,w):
    return inference(w@model.params,np.sqrt(max(0,w@model.cov_params()@w)))

def corrected_sandwich(model):
    """Generic likelihood HC1 labels can silently fall back to HC0; correct explicitly."""
    model._results.cov_params_default *= model.nobs/(model.nobs-len(model.params))
    return model

def add_holm(frame,keys,estimand='estimand'):
    frame['holm_p']=np.nan
    for _,g in frame.groupby(keys,dropna=False):
        h=g[g[estimand].isin(FAMILY)]
        frame.loc[h.index,'holm_p']=multipletests(h.p,method='holm')[1]
    return frame

def modified_design(model,form,amount):
    """Hold the same empirical covariates for every counterfactual form/dose."""
    x=np.asarray(model.model.exog).copy()
    names=list(model.model.exog_names)
    z={200:-1,1000:0,5000:1}[amount]
    for j,name in enumerate(names):
        if name=='z' or 'C(form)' in name or 'C(amount)' in name:
            val=1.
            for part in name.split(':'):
                if part=='z':val*=z
                elif part.startswith('C(form)'):val*=float(part==f'C(form)[T.{form}]')
                elif part.startswith('C(amount)'):val*=float(part==f'C(amount)[T.{amount}]')
                else:raise ValueError(name)
            x[:,j]=val
    return x

def probability_function(model,link,form,representation,params=None):
    """Value and analytic gradient for balanced-dose AME or endpoint change."""
    params=np.asarray(model.params) if params is None else np.asarray(params);names=list(model.model.exog_names)
    def densities(eta):
        if link=='logit':
            p=expit(eta);return p,p*(1-p),p*(1-p)*(1-2*p)
        return stats.norm.cdf(eta),stats.norm.pdf(eta),-eta*stats.norm.pdf(eta)
    if representation=='endpoint':
        value=0.;grad=np.zeros(len(params))
        for a,sign in [(5000,1),(200,-1)]:
            x=modified_design(model,form,a);p,den,_=densities(x@params)
            value+=sign*p.mean();grad+=sign*(den@x)/len(x)
        return value,grad
    dw=vectors(names,'trend')[form];slope=dw@params
    value=0.;grad=np.zeros(len(params))
    for a in AMOUNTS:
        x=modified_design(model,form,a);_,den,der= densities(x@params)
        value+=slope*den.mean()/3
        grad+=((slope*der)@x/len(x)+den.mean()*dw)/3
    return value,grad

def marginal_contrasts(model,link,representation):
    values={f:probability_function(model,link,f,representation) for f in FORMS}
    values['restricted']=(.5*(values['food'][0]+values['medical'][0]),.5*(values['food'][1]+values['medical'][1]))
    for key in ['restricted-cash','food-cash','medical-cash','food-medical']:
        a,b=key.split('-');values[key]=(values[a][0]-values[b][0],values[a][1]-values[b][1])
    return {k:inference(v,np.sqrt(max(0,g@model.cov_params()@g))) for k,(v,g) in values.items()}

def formula(representation,adjustment):
    base='C(form)*z' if representation=='trend' else 'C(form)*C(amount)'
    return base+('+'+prior.CONTROLS if adjustment=='adjusted' else '')

def fit_glm(outcome,data,representation='trend',adjustment='unadjusted',link='logit'):
    family=sm.families.Binomial(link=sm.families.links.Logit() if link=='logit' else sm.families.links.Probit())
    m=smf.glm(outcome+'~'+formula(representation,adjustment),data,family=family).fit(cov_type='HC0',maxiter=200)
    assert m.converged
    return corrected_sandwich(m)

def pooled_and_binary(d,out,cache):
    rows=[];binary=[];hetero=[]
    for outcome in OUTCOMES:
        m=smf.ols(outcome+'~C(form)*z',d).fit(cov_type='HC3');cache[('ols','R','unadjusted','trend',outcome)]=m
        for estimand,w in vectors(list(m.params.index),'trend').items():
            rows.append(dict(outcome=outcome,sample='R',adjustment='unadjusted',estimand=estimand,N=len(d),**linear_contrast(m,w)))
        if outcome in ['ordinal','midpoint','top75']:
            hetero.append(dict(outcome=outcome,model='OLS',estimand='food-medical',**linear_contrast(m,vectors(list(m.params.index),'trend')['food-medical'])))
    pooled=add_holm(pd.DataFrame(rows),['outcome','sample','adjustment']);pooled.to_csv(out/'restricted_vs_cash_slopes.csv',index=False)
    for outcome in THRESHOLDS:
        for link in ['logit','probit']:
            m=fit_glm(outcome,d,link=link);cache[(link,'R','unadjusted','trend',outcome)]=m
            for k,w in vectors(list(m.params.index),'trend').items():
                binary.append(dict(outcome=outcome,model=link,scale='link_per_fivefold',estimand=k,**linear_contrast(m,w)))
            marginal=marginal_contrasts(m,link,'trend')
            for k,res in marginal.items():binary.append(dict(outcome=outcome,model=link,scale='probability_AME_per_fivefold',estimand=k,**res))
            if outcome=='top75' and link=='logit':hetero.append(dict(outcome=outcome,model='logit_AME',estimand='food-medical',**marginal['food-medical']))
    binary=add_holm(pd.DataFrame(binary),['outcome','model','scale']);binary.to_csv(out/'threshold_logit_probit.csv',index=False)
    pd.DataFrame(hetero).to_csv(out/'restricted_form_heterogeneity.csv',index=False)
    return pooled,binary

def cell_bootstrap(d):
    """Multinomial sampling is exactly cell-stratified respondent resampling for category means."""
    rng=np.random.default_rng(SEED);point=np.zeros((3,3,6));draws=np.zeros((B,3,3,6));sizes=np.zeros((3,3),int)
    for f,form in enumerate(FORMS):
        for a,amount in enumerate(AMOUNTS):
            g=d[(d.form==form)&(d.amount==amount)];n=len(g);p=g.ordinal.value_counts().reindex(range(1,7),fill_value=0).to_numpy()/n
            point[f,a]=p;draws[:,f,a]=rng.multinomial(n,p,size=B)/n;sizes[f,a]=n
    return point,draws,sizes

def bootstrap_analyses(d,out,point,draws,sizes):
    # Five jointly observed thresholds; no independent-threshold bootstrap.
    threshold_p=1-np.cumsum(point,axis=-1)[...,:5]
    threshold_b=1-np.cumsum(draws,axis=-1)[...,:5]
    z=np.array([-1,0,1]);zbar=(sizes*z).sum(axis=1)/sizes.sum(axis=1)
    weights=sizes*(z-zbar[:,None]);weights/= (sizes*(z-zbar[:,None])**2).sum(axis=1)[:,None]
    slopes=(threshold_p*weights[...,None]).sum(axis=1)
    slopes_b=(threshold_b*weights[None,...,None]).sum(axis=2)
    tail=[];profile=[];global_rows=[]
    for name,w in [('restricted-cash',np.array([-1,.5,.5])),('food-cash',np.array([-1,1,0])),('medical-cash',np.array([-1,0,1]))]:
        e=w@slopes;b=np.einsum('f,bft->bt',w,slopes_b);cov=np.cov(b,rowvar=False)
        for j,t in enumerate(THRESHOLDS):profile.append(dict(contrast=name,threshold=t,**inference(e[j],np.sqrt(cov[j,j]))))
        rr=[];D=np.zeros((4,5))
        for j,t in enumerate(THRESHOLDS[:-1]):
            D[j,4]=1;D[j,j]=-1;v=e[4]-e[j];se=np.std(b[:,4]-b[:,j],ddof=1)
            rr.append(dict(contrast=name,comparison='top75-minus-'+t,**inference(v,se),B=B))
        adj=multipletests([r['p'] for r in rr],method='holm')[1]
        for r,p in zip(rr,adj):r['holm_p']=p;tail.append(r)
        c=D@cov@D.T;effect=D@e;rank=np.linalg.matrix_rank(c);wald=effect@np.linalg.pinv(c)@effect
        global_rows.append(dict(contrast=name,wald=wald,df=rank,p=stats.chi2.sf(wald,rank)))
        pd.DataFrame(cov,index=THRESHOLDS,columns=THRESHOLDS).to_csv(out/(name+'_threshold_covariance.csv'),index_label='threshold')
    tail=pd.DataFrame(tail);tail.to_csv(out/'threshold_tail_specificity.csv',index=False)
    profile=pd.DataFrame(profile);profile.to_csv(out/'threshold_joint_profile.csv',index=False)
    pd.DataFrame(global_rows).to_csv(out/'threshold_global_profile.csv',index=False)
    # Top category endpoint scales, with pooled probabilities rather than pooled ratios.
    pp=point[:,:,-1];bb=draws[:,:,:,-1]
    pp=np.vstack([pp,.5*(pp[1]+pp[2])]);bb=np.concatenate([bb,.5*(bb[:,1:2]+bb[:,2:3])],axis=1)
    changes=pp[:,2]-pp[:,0];changes_b=bb[:,:,2]-bb[:,:,0]
    risks=pp[:,2]/pp[:,0];risks_b=bb[:,:,2]/bb[:,:,0]
    odds=(pp[:,2]/(1-pp[:,2]))/(pp[:,0]/(1-pp[:,0]));odds_b=(bb[:,:,2]/(1-bb[:,:,2]))/(bb[:,:,0]/(1-bb[:,:,0]))
    relative=[]
    def summary(value,boot,scale):
        lo,hi=np.quantile(boot,[.025,.975]);se=np.std(boot if scale=='probability_difference' else np.log(boot),ddof=1)
        effect=value if scale=='probability_difference' else np.log(value)
        return dict(estimate=value,lo=lo,hi=hi,se_on_inference_scale=se,p=2*stats.norm.sf(abs(effect/se)))
    for j,f in enumerate(FORMS+['restricted']):
        for scale,e,b in [('probability_difference',changes[j],changes_b[:,j]),('risk_ratio',risks[j],risks_b[:,j]),('odds_ratio',odds[j],odds_b[:,j])]:
            relative.append(dict(estimand=f,scale=scale,role='within_form_descriptive',**summary(e,b,scale)))
    for j,f in enumerate(['food','medical','restricted'],1):
        for scale,e,b in [('probability_difference',changes[j]-changes[0],changes_b[:,j]-changes_b[:,0]),('ratio_of_risk_ratios',risks[j]/risks[0],risks_b[:,j]/risks_b[:,0]),('ratio_of_odds_ratios',odds[j]/odds[0],odds_b[:,j]/odds_b[:,0])]:
            relative.append(dict(estimand=f+'-cash',scale=scale,role='between_form_comparison',**summary(e,b,scale)))
    relative=pd.DataFrame(relative);relative['holm_p']=np.nan;ix=relative.index[relative.role.eq('between_form_comparison')];relative.loc[ix,'holm_p']=multipletests(relative.loc[ix,'p'],method='holm')[1];relative['B']=B;relative.to_csv(out/'top_tail_relative_change.csv',index=False)
    # Midpoint translation and scaling; same draws, not independent confirmation.
    mp=point@np.array(prior.MID);mb=draws@np.array(prior.MID)
    mp=np.vstack([mp,.5*(mp[1]+mp[2])]);mb=np.concatenate([mb,.5*(mb[:,1:2]+mb[:,2:3])],axis=1)
    yuan=[];scaling=[];benchmark=[]
    for j,f in enumerate(FORMS+['restricted']):
        for a,amount in enumerate(AMOUNTS):
            lo,hi=np.quantile(mb[:,j,a],[.025,.975]);yuan.append(dict(form=f,amount=amount,midpoint=mp[j,a],midpoint_lo=lo,midpoint_hi=hi,implied_yuan=mp[j,a]*amount,yuan_lo=lo*amount,yuan_hi=hi*amount))
        eta=np.log(mp[j,2]*5000/(mp[j,0]*200))/np.log(25);eta_b=np.log(mb[:,j,2]*5000/(mb[:,j,0]*200))/np.log(25);lo,hi=np.quantile(eta_b,[.025,.975]);scaling.append(dict(estimand=f,eta=eta,lo=lo,hi=hi,se=np.std(eta_b,ddof=1)))
        if f!='restricted':
            inv=1/np.array(AMOUNTS);K=(mp[j]@inv)/(inv@inv);fit=K*inv
            benchmark.append(dict(form=f,K=K,RMSE=np.sqrt(np.mean((mp[j]-fit)**2)),SSE=np.sum((mp[j]-fit)**2),observed_midpoint_200=mp[j,0],observed_midpoint_1000=mp[j,1],observed_midpoint_5000=mp[j,2],fit_midpoint_200=fit[0],fit_midpoint_1000=fit[1],fit_midpoint_5000=fit[2]))
    ec=np.log(mp[:,2]*5000/(mp[:,0]*200))/np.log(25);eb=np.log(mb[:,:,2]*5000/(mb[:,:,0]*200))/np.log(25)
    for j,f in enumerate(['food','medical','restricted'],1):
        value=ec[j]-ec[0];boot=eb[:,j]-eb[:,0];lo,hi=np.quantile(boot,[.025,.975]);scaling.append(dict(estimand=f+'-cash',eta=value,lo=lo,hi=hi,se=np.std(boot,ddof=1)))
    yuan=pd.DataFrame(yuan);yuan.to_csv(out/'implied_yuan_cells.csv',index=False);pd.DataFrame(scaling).to_csv(out/'implied_yuan_scaling.csv',index=False);pd.DataFrame(benchmark).to_csv(out/'constant_dollar_benchmark.csv',index=False)
    return profile,relative,yuan

def multinomial(d,out):
    X=patsy.dmatrix('C(form)*z',d,return_type='dataframe')
    m=sm.MNLogit(d.ordinal-1,X).fit(method='newton',maxiter=200,disp=False)
    assert m.mle_retvals['converged']
    rows=[]
    for f in FORMS:
        for a,z in zip(AMOUNTS,[-1,0,1]):
            x=patsy.build_design_matrices([X.design_info],pd.DataFrame({'form':[f],'z':[z]}))[0];pr=np.asarray(m.predict(x))[0];g=d[(d.form==f)&(d.amount==a)]
            for k in range(6):rows.append(dict(form=f,amount=a,category=k+1,N=len(g),raw_probability=g.ordinal.eq(k+1).mean(),predicted_probability=pr[k]))
    table=pd.DataFrame(rows);table['model_minus_raw']=table.predicted_probability-table.raw_probability;table.to_csv(out/'multinomial_probability_checks.csv',index=False)

def specification_grid(d,out,cache):
    samples={'R':d,**{k:d[d['sample_'+k]] for k in ['A','C','Q1','Q2']}}
    rows=[];diagnostics=[]
    sd={y:d[y].std() for y in ['ordinal','midpoint','alt_top']}
    for sn,x in samples.items():
        print('Finite grid sample',sn,flush=True)
        for adjustment in ['unadjusted','adjusted']:
            for representation in ['trend','endpoint']:
                for coding in ['ordinal','midpoint','alt_top','ordered_logit','ordered_probit','top75','top75_logit_AME']:
                    res=None;model_type='ols';outcome=coding
                    if coding=='top75_logit_AME':model_type='logit';outcome='top75'
                    key=(model_type,sn,adjustment,representation,outcome)
                    if coding.startswith('ordered_'):
                        link=coding.split('_')[1];X=patsy.dmatrix(formula(representation,adjustment),x,return_type='dataframe').drop(columns='Intercept')
                        m=OrderedModel(x.ordinal,X,distr=link).fit(method='bfgs',disp=False,cov_type='HC0',maxiter=600,gtol=1e-5)
                        assert m.mle_retvals['converged'],str((sn,adjustment,representation,coding))
                        corrected_sandwich(m);names=list(m.params.index);res={k:linear_contrast(m,w) for k,w in vectors(names,representation).items()}
                        scale='latent_'+link;standardizer=1
                    else:
                        m=cache.get(key)
                        if m is None:
                            m=fit_glm(outcome,x,representation,adjustment) if model_type=='logit' else smf.ols(outcome+'~'+formula(representation,adjustment),x).fit(cov_type='HC3')
                        if model_type=='logit':res=marginal_contrasts(m,'logit',representation);scale='probability';standardizer=1
                        else:res={k:linear_contrast(m,w) for k,w in vectors(list(m.params.index),representation).items()};scale='probability' if coding=='top75' else 'ordinal' if coding=='ordinal' else 'midpoint_proxy';standardizer=sd.get(coding,1)
                    diagnostics.append(dict(sample=sn,adjustment=adjustment,amount_representation=representation,coding=coding,N=int(m.nobs),parameters=len(m.params),converged=bool(getattr(m,'converged',True) if not coding.startswith('ordered_') else m.mle_retvals['converged'])))
                    divisor=1 if representation=='trend' else 2
                    for estimand in CONTRASTS:
                        r=res[estimand];rows.append(dict(sample=sn,adjustment=adjustment,amount_representation=representation,coding=coding,estimand=estimand,scale=scale,outcome_family='ordered_latent' if coding.startswith('ordered_') else 'binary_probability' if scale=='probability' else 'score_or_share',sign=int(np.sign(r['estimate'])),N=len(x),comparable_estimate=r['estimate']/divisor,comparable_lo=r['lo']/divisor,comparable_hi=r['hi']/divisor,standardized_comparable_effect=np.nan if coding.startswith('ordered_') else r['estimate']/divisor/standardizer,standardization='raw_R_outcome_SD' if coding in sd else 'separate_latent_scale' if coding.startswith('ordered_') else 'none_probability_unit',**r))
    grid=pd.DataFrame(rows);grid.to_csv(out/'specification_curve.csv',index=False);pd.DataFrame(diagnostics).to_csv(out/'model_diagnostics.csv',index=False)
    summary=[]
    for (family,coding,estimand),g in grid.groupby(['outcome_family','coding','estimand']):
        vals=g.standardized_comparable_effect.dropna()
        summary.append(dict(outcome_family=family,coding=coding,estimand=estimand,specifications=len(g),share_positive=g.estimate.gt(0).mean(),share_CI_positive=g.lo.gt(0).mean(),share_CI_excludes_zero=(g.lo.gt(0)|g.hi.lt(0)).mean(),comparable_median=g.comparable_estimate.median(),comparable_min=g.comparable_estimate.min(),comparable_max=g.comparable_estimate.max(),standardized_median=vals.median() if len(vals) else np.nan,standardized_min=vals.min() if len(vals) else np.nan,standardized_max=vals.max() if len(vals) else np.nan))
    pd.DataFrame(summary).to_csv(out/'specification_stability_summary.csv',index=False)
    return grid

def figures(out,point,draws,profile,relative,yuan,grid):
    folder=out/'figures';folder.mkdir(exist_ok=True)
    colors={'cash':'#243746','food':'#62A7A0','medical':'#B79A77','restricted':'#BB493D'}
    def amount_axis(ax):
        ax.set_xscale('log');ax.set_xticks(AMOUNTS,['200','1,000','5,000']);ax.xaxis.set_minor_locator(NullLocator());ax.set_xlabel('Transfer amount (RMB)')
    pooled_cells=[]
    for y,weight in [('midpoint',np.array(prior.MID)),('top75',np.array([0,0,0,0,0,1]))]:
        pp=point@weight;bb=draws@weight;pp=np.vstack([pp,.5*(pp[1]+pp[2])]);bb=np.concatenate([bb,.5*(bb[:,1:2]+bb[:,2:3])],axis=1)
        for f,form in enumerate(FORMS+['restricted']):
            for a,amount in enumerate(AMOUNTS):
                lo,hi=np.quantile(bb[:,f,a],[.025,.975]);pooled_cells.append(dict(outcome=y,form=form,amount=amount,estimate=pp[f,a],lo=lo,hi=hi))
    pc=pd.DataFrame(pooled_cells);pc.to_csv(out/'figA_source.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for ax,y,title in zip(axes,['midpoint','top75'],['Midpoint stated MPC','Probability of top-category response']):
        for f in FORMS+['restricted']:
            g=pc[(pc.outcome==y)&(pc.form==f)];ax.errorbar(g.amount,g.estimate,yerr=[g.estimate-g.lo,g.hi-g.estimate],marker='o',color=colors[f],alpha=.55 if f in ['food','medical'] else 1,lw=1 if f in ['food','medical'] else 2,label=f)
        amount_axis(ax);ax.set_ylabel(title);ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(folder/'figA_pooled_curves.png',dpi=220);plt.close(fig)
    g=profile[profile.contrast.eq('restricted-cash')];g.to_csv(out/'figB_source.csv',index=False);fig,ax=plt.subplots(figsize=(7,4.5));ax.errorbar(range(5),g.estimate,yerr=1.96*g.se,fmt='o-',capsize=3);ax.set_xticks(range(5),['Any','>=10%','>=25%','>=50%','>75%']);ax.axhline(0,color='black',lw=.7);ax.set_ylabel('Restricted minus Cash differential slope');ax.set_title('Joint-bootstrap threshold profile (pointwise 95% CI)');fig.tight_layout();fig.savefig(folder/'figB_threshold_profile.png',dpi=220);plt.close(fig)
    relative.to_csv(out/'figC_source.csv',index=False);fig,axes=plt.subplots(2,3,figsize=(12,8))
    for row,role,scales,titles in [(0,'within_form_descriptive',['probability_difference','risk_ratio','odds_ratio'],['Within-form probability change','Within-form risk ratio','Within-form odds ratio']),(1,'between_form_comparison',['probability_difference','ratio_of_risk_ratios','ratio_of_odds_ratios'],['Difference in probability changes','Ratio of risk ratios','Ratio of odds ratios'])]:
        g=relative[relative.role.eq(role)]
        for ax,scale,title in zip(axes[row],scales,titles):
            x=g[g.scale.eq(scale)];ix=np.arange(len(x));ax.errorbar(ix,x.estimate,yerr=[x.estimate-x.lo,x.hi-x.estimate],fmt='o',capsize=3);ax.set_xticks(ix,['Cash','Food','Medical','Restricted'] if row==0 else ['Food/Cash','Medical/Cash','Restricted/Cash'],rotation=25,ha='right');ax.axhline(0 if scale=='probability_difference' else 1,color='black',lw=.8);ax.set_title(title,fontsize=10)
    fig.suptitle('Top-category endpoint changes: 200 to 5,000');fig.tight_layout();fig.savefig(folder/'figC_relative_scales.png',dpi=220);plt.close(fig)
    # Separate probability effects from cardinal-like midpoint/ordinal comparisons.
    g=grid[grid.estimand.eq('restricted-cash')&grid.coding.isin(['midpoint','top75','top75_logit_AME'])];g.to_csv(out/'figD_source.csv',index=False);fig,axes=plt.subplots(3,1,figsize=(13,10))
    for ax,coding in zip(axes,['midpoint','top75','top75_logit_AME']):
        x=g[g.coding.eq(coding)].sort_values(['sample','adjustment','amount_representation'],key=lambda c:c.map({'R':0,'A':1,'C':2,'Q1':3,'Q2':4}) if c.name=='sample' else c);ix=np.arange(len(x));ax.errorbar(ix,x.comparable_estimate,yerr=[x.comparable_estimate-x.comparable_lo,x.comparable_hi-x.comparable_estimate],fmt='o',capsize=2);ax.set_xticks(ix,x['sample']+' '+x.adjustment.map({'unadjusted':'U','adjusted':'A'})+' '+x.amount_representation.map({'trend':'T','endpoint':'E'}),rotation=60,ha='right',fontsize=8);ax.axhline(0,color='black',lw=.8);ax.set_ylabel('Effect per fivefold step');ax.set_title(coding+' | endpoint changes / 2; fixed specification order')
    fig.tight_layout();fig.savefig(folder/'figD_specification_curve.png',dpi=220);plt.close(fig)
    yuan.to_csv(out/'figE_source.csv',index=False);fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for ax,y,lo,hi,title in [(axes[0],'midpoint','midpoint_lo','midpoint_hi','Midpoint stated MPC share'),(axes[1],'implied_yuan','yuan_lo','yuan_hi','Implied additional spending (yuan)')]:
        for f in FORMS+['restricted']:
            x=yuan[yuan.form.eq(f)];ax.errorbar(x.amount,x[y],yerr=[x[y]-x[lo],x[hi]-x[y]],marker='o',color=colors[f],label=f,alpha=.55 if f in ['food','medical'] else 1)
        amount_axis(ax);ax.set_ylabel(title);ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(folder/'figE_share_vs_yuan.png',dpi=220);plt.close(fig)

def run(data,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);d=prior.prepare(data);cache={}
    pooled,binary=pooled_and_binary(d,out,cache);print('Pooled and nonlinear threshold tests complete',flush=True)
    point,draws,sizes=cell_bootstrap(d);profile,relative,yuan=bootstrap_analyses(d,out,point,draws,sizes);print('Joint/relative/yuan bootstrap complete',flush=True)
    multinomial(d,out);grid=specification_grid(d,out,cache);assert len(grid)==420
    figures(out,point,draws,profile,relative,yuan,grid)
    manifest=dict(seed=SEED,B=B,N=len(d),sample_N={'R':len(d),**{k:int(d['sample_'+k].sum()) for k in ['A','C','Q1','Q2']}},raw_sha256=hashlib.sha256(Path(data).read_bytes()).hexdigest(),prior_script_sha256=hashlib.sha256(Path(prior.__file__).read_bytes()).hexdigest(),prior_pr=9,prior_commit='d749f5c0eab3938038882d948bc6370e78835249',versions={p:version(p) for p in ['numpy','pandas','scipy','statsmodels','matplotlib']},primary_family=FAMILY,specifications=len(grid),individual_exports=False,stopping_rule='No further current-data exploratory analysis after this package')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(pooled[pooled.estimand.eq('restricted-cash')].to_string(index=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('data');parser.add_argument('--out',default=str(ROOT));args=parser.parse_args();run(args.data,args.out)
