"""Finite B-F analyses, using original raw labels and existing quality definitions."""
from pathlib import Path
import json,sys,argparse,hashlib
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import log_loss
import grid_models as gm
from run_revision import data,write,OUT

def inf(e,se):return dict(estimate=float(e),se=float(se),lo=float(e-1.96*se),hi=float(e+1.96*se),p=float(2*stats.norm.sf(abs(e/se))))
def contrast(m,weights):
    v=np.zeros(len(m.params))
    for name,val in weights.items():v[list(m.params.index).index(name)]=val
    return inf(v@m.params,np.sqrt(v@m.cov_params()@v))
def holm(t):
    t['holm_p']=np.nan;valid=t.p.notna();t.loc[valid,'holm_p']=multipletests(t.loc[valid,'p'],method='holm')[1];return t

def covariates(d):
    raw=d.q46_income
    scheme=np.where(raw>=11,'legacy','current')
    pos=np.where(raw>=11,raw-10,raw)
    # Rank normalized by scheme; not a claim that the currency bands coincide.
    rank=pd.Series(pos,index=d.index).groupby(scheme).rank(method='average',pct=True)
    d['income_rank']=rank
    for name,var in [('fundraising','q07_emergfund'),('food_need','q29_foodexp'),('medical_need','q30_medexp')]:
        d[name]=(d[var]-d[var].mean())/d[var].std(ddof=1)
    d['income_rank_z']=(rank-rank.mean())/rank.std(ddof=1)
    common={2:750.,3:2000.5,4:5500.5,5:11500.5,12:2000.5,13:4000.5,14:6500.5,15:10000.5,16:16000.5}
    for mapping,edges in [('M1',{1:250.,6:20000.,11:500.}),('M2',{1:125.,6:30000.,11:250.})]:
        d['income_'+mapping]=raw.map(common|edges)
        assert d['income_'+mapping].notna().all()
    d['income_rank_scale']=rank
    d['food_lower6']=d.q29_foodexp.map({1:0,2:501,3:1001,4:2001,5:3001,6:5001})*6
    return d

def profiles(d):
    rows=[]
    for (form,amount),part in d.groupby(['form','amount']):
        for outcome in gm.OUTCOMES:
            y=part[outcome];e=y.mean();se=y.std(ddof=1)/np.sqrt(len(y))
            rows.append(dict(form=form,amount=amount,outcome=outcome,N=len(y),**inf(e,se),ci='95% normal cell mean interval; binary sample variance',estimand='unconditional stated response'))
    write(pd.DataFrame(rows),'form_amount_profiles.csv')
    ratios=[]
    for outcome in ['any_spending','ge10','ge25','ge50','top75']:
        for form in ['cash','food','medical']:
            lo=d[(d.form==form)&(d.amount==200)][outcome];hi=d[(d.form==form)&(d.amount==5000)][outcome]
            p0,p1=lo.mean(),hi.mean();v0,v1=lo.var(ddof=1)/len(lo),hi.var(ddof=1)/len(hi)
            for scale in ['difference','risk_ratio','odds_ratio']:
                if scale=='difference':r=inf(p1-p0,np.sqrt(v0+v1))
                else:
                    e=np.log(p1/p0) if scale=='risk_ratio' else np.log(p1/(1-p1))-np.log(p0/(1-p0))
                    se=np.sqrt(v1/p1**2+v0/p0**2) if scale=='risk_ratio' else np.sqrt(v1/(p1*(1-p1))**2+v0/(p0*(1-p0))**2)
                    r=inf(e,se);r.update(estimate=np.exp(e),lo=np.exp(r['lo']),hi=np.exp(r['hi']),se_scale='log ratio')
                ratios.append(dict(outcome=outcome,form=form,scale=scale,N_200=len(lo),N_5000=len(hi),estimand='5000 versus200 within form',**r))
    write(holm(pd.DataFrame(ratios)),'threshold_relative_scales.csv')
    ames=[]
    sys.path.insert(0,str(OUT.parent/'mpc_final_strengthening'))
    import strengthening as old
    for outcome in ['any_spending','ge10','ge25','ge50','top75']:
        for link in ['logit','probit']:
            m=old.fit_glm(outcome,d,link=link)
            for c,r in old.marginal_contrasts(m,link,'trend').items():ames.append(dict(outcome=outcome,model=link,contrast=c,N=len(d),estimand='balanced-dose probability derivative per-fivefold; not link coefficient',**r))
    write(holm(pd.DataFrame(ames)),'threshold_probability_AME.csv')

def equivalence(d):
    x=d[d.amount==5000];m=smf.ols('top75~C(form)',x).fit(cov_type='HC3');rows=[]
    for c,w in [('cash-food',{'C(form)[T.food]':-1}),('cash-medical',{'C(form)[T.medical]':-1}),('food-medical',{'C(form)[T.food]':1,'C(form)[T.medical]':-1}),('restricted-cash',{'C(form)[T.food]':.5,'C(form)[T.medical]':.5})]:
        r=contrast(m,w)
        for margin in [.02,.03,.05]:
            p=max(stats.norm.sf((r['estimate']+margin)/r['se']),stats.norm.cdf((r['estimate']-margin)/r['se']))
            rows.append(dict(contrast=c,margin_pp=100*margin,**{k:v for k,v in r.items() if k!='p'},raw_difference_p=r['p'],p=p,N=len(x),TOST_90lo=r['estimate']-1.644854*r['se'],TOST_90hi=r['estimate']+1.644854*r['se'],interpretation='non-preregistered sensitivity, no independently justified single SESOI'))
    write(holm(pd.DataFrame(rows)),'equivalence_sensitivity_5000.csv')

def binding(d):
    allrows=[];tests=[];counts=[]
    for sample in gm.SAMPLES:
        dd=d if sample=='R' else d[d['sample_'+sample]]
        x=dd[dd.form.isin(['cash','food'])].copy();undefined=x.food_lower6<=0
        counts.append(dict(sample=sample,N_candidate=len(x),zero_denominator=int(undefined.sum()),defined=int((~undefined).sum()),merged_bins='none'))
        x=x[~undefined].copy();x['ratio']=x.amount/x.food_lower6
        x['ratio_bin']=pd.cut(x.ratio,[0,.1,.25,.5,1,np.inf],right=True,include_lowest=True,labels=['<=.10','(.10,.25]','(.25,.50]','(.50,1]','>1'])
        x['logr']=np.log(x.ratio)
        for outcome in ['top75','ordinal','midpoint']:
            for rb in ['<=.10','(.10,.25]','(.25,.50]','(.50,1]','>1']:
                xx=x[x.ratio_bin==rb];nc=int(xx.form.eq('cash').sum());nf=int(xx.form.eq('food').sum())
                if min(nc,nf)<2:allrows.append(dict(sample=sample,outcome=outcome,ratio_bin=rb,N=len(xx),cash_N=nc,food_N=nf,status='not estimable',failure='fewer than2 in a form'));continue
                m=smf.ols(outcome+'~C(form)',xx).fit(cov_type='HC3')
                allrows.append(dict(sample=sample,outcome=outcome,ratio_bin=rb,N=len(xx),cash_N=nc,food_N=nf,cash_mean=xx[xx.form=='cash'][outcome].mean(),food_mean=xx[xx.form=='food'][outcome].mean(),status='ok',estimand='Cash-Food unadjusted within-r-bin association',**contrast(m,{'C(form)[T.food]':-1})))
            m=smf.ols(outcome+'~C(form)*logr+C(amount)',x).fit(cov_type='HC3')
            tests.append(dict(sample=sample,outcome=outcome,analysis='continuous_ratio',estimand='Food-Cash log-r gradient, conditional amount indicators; baseline association',N=len(x),**contrast(m,{'C(form)[T.food]:logr':1})))
            fixed=dd[(dd.food_lower6>5000)&dd.form.isin(['cash','food'])]
            m=smf.ols(outcome+'~C(form)*z',fixed).fit(cov_type='HC3')
            for est,w in [('cash_slope',{'z':1}),('food_slope',{'z':1,'C(form)[T.food]:z':1}),('food-cash_slope',{'C(form)[T.food]:z':1})]:
                tests.append(dict(sample=sample,outcome=outcome,analysis='fixed_inframarginal',estimand=est,N=len(fixed),**contrast(m,w)))
            m=smf.ols(outcome+'~C(form)*C(amount)',fixed).fit(cov_type='HC3')
            tests.append(dict(sample=sample,outcome=outcome,analysis='fixed_inframarginal',estimand='pooled_equal_amount_food-cash_level',N=len(fixed),**contrast(m,{'C(form)[T.food]':1,'C(form)[T.food]:C(amount)[T.1000]':1/3,'C(form)[T.food]:C(amount)[T.5000]':1/3})))
    write(holm(pd.DataFrame(allrows)),'bindingness_ratio_source.csv');write(holm(pd.DataFrame(tests)),'bindingness_ratio_tests.csv');write(pd.DataFrame(counts),'bindingness_ratio_counts.csv')

def relative(d):
    folds=np.zeros(len(d),int)
    for fold,(_,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=20261003).split(d,d.cell)):folds[te]=fold
    d['fold']=folds
    models=[];scores=[];foldrows=[];compression=[]
    for sample in gm.SAMPLES:
        x=(d if sample=='R' else d[d['sample_'+sample]]).copy()
        for mapping in ['M1','M2','rank']:
            scale=x['income_'+mapping] if mapping!='rank' else x.income_rank_scale
            loginc=np.log(scale)
            x['ABS']=np.log(x.amount);x['REL']=np.log(x.amount/scale)
            for outcome in ['top75','ordinal','midpoint']:
                losses={}
                for typ in ['ABS','REL']:
                    family='logit' if outcome=='top75' else 'OLS'
                    m=smf.glm(outcome+f'~C(form)*{typ}',x,family=sm.families.Binomial()).fit() if family=='logit' else smf.ols(outcome+f'~C(form)*{typ}',x).fit()
                    models.append(dict(sample=sample,mapping=mapping,outcome=outcome,model=typ,N=len(x),AIC=m.aic,BIC=-2*m.llf+len(m.params)*np.log(len(x)),R2=getattr(m,'rsquared',np.nan),converged=getattr(m,'converged',True),income='band mapping, not observed exact income'))
                    import patsy
                    X=np.asarray(patsy.dmatrix(f'C(form)*{typ}',x));y=x[outcome].to_numpy();loss=np.zeros(len(x))
                    for fold in range(5):
                        train=x.fold.to_numpy()!=fold;test=~train
                        reg=LogisticRegression(penalty=None,max_iter=2000,tol=1e-10,fit_intercept=False) if family=='logit' else LinearRegression(fit_intercept=False)
                        reg.fit(X[train],y[train]);pred=reg.predict_proba(X[test])[:,1] if family=='logit' else reg.predict(X[test])
                        pr=np.clip(pred,1e-12,1-1e-12)
                        loss[test]=-y[test]*np.log(pr)-(1-y[test])*np.log1p(-pr) if family=='logit' else (pred-y[test])**2
                        foldrows.append(dict(sample=sample,mapping=mapping,outcome=outcome,model=typ,fold=fold,N_train=int(train.sum()),N_test=int(test.sum()),loss=loss[test].mean()))
                    losses[typ]=loss
                diff=losses['ABS']-losses['REL'];se=diff.std(ddof=1)/np.sqrt(len(diff));improve=diff.mean()/losses['ABS'].mean()
                scores.append(dict(sample=sample,mapping=mapping,outcome=outcome,N=len(x),ABS_loss=losses['ABS'].mean(),REL_loss=losses['REL'].mean(),ABS_minus_REL=diff.mean(),lo=diff.mean()-1.96*se,hi=diff.mean()+1.96*se,relative_improvement=improve,material=bool(improve>=.01 and diff.mean()-1.96*se>0),score='logloss' if outcome=='top75' else 'MSE',CI='paired held-out loss descriptive normal interval, training dependence not accounted for'))
                xx=x[x.form=='cash'].copy();xx['log_income_z']=(loginc.loc[xx.index]-np.log((d['income_'+mapping] if mapping!='rank' else d.income_rank_scale)).mean())/np.log((d['income_'+mapping] if mapping!='rank' else d.income_rank_scale)).std(ddof=1)
                m=smf.ols(outcome+'~z*log_income_z',xx).fit(cov_type='HC3')
                compression.append(dict(sample=sample,mapping=mapping,outcome=outcome,N=len(xx),estimand='Cash amount slope moderation per1SD log income; positive = lower-income earlier/steeper compression',**contrast(m,{'z:log_income_z':1})))
    write(pd.DataFrame(models),'relative_scale_models.csv');write(pd.DataFrame(scores),'relative_scale_cv.csv');write(pd.DataFrame(foldrows),'relative_scale_cv_folds.csv');write(holm(pd.DataFrame(compression)),'relative_scale_compression.csv')
    write(d.groupby(['cell','fold']).size().rename('N').reset_index(),'unified_fold_counts.csv')
    (OUT/'fold_manifest.json').write_text(json.dumps(dict(seed=20261003,folds=5,assignment_sha256=hashlib.sha256(folds.tobytes()).hexdigest(),privacy='No individual IDs/folds exported; membership hash and aggregate counts only'),indent=2)+'\n',encoding='utf-8')

def moderators(d):
    rows=[];controls=[]
    for v in ['income_rank_z','fundraising','food_need','medical_need']:
        for outcome in ['top75','ordinal','midpoint']:
            m=smf.ols(outcome+f'~C(form)*z*{v}',d).fit(cov_type='HC3')
            for target,w in [('cash',{'z:'+v:1}),('cash-food',{'C(form)[T.food]:z:'+v:-1}),('cash-medical',{'C(form)[T.medical]:z:'+v:-1})]:
                rows.append(dict(variable=v,outcome=outcome,target=target,N=len(d),cash_N=int(d.form.eq('cash').sum()),estimand='amount slope moderation per1SD baseline X, fivefold amount step',**contrast(m,w)))
    table=holm(pd.DataFrame(rows));write(table,'theory_moderators.csv')
    grid=pd.read_csv(OUT/'table_A1_focal_estimand.csv')
    power=[]
    for r in table.itertuples():
        mde=(stats.norm.ppf(.975)+stats.norm.ppf(.8))*r.se
        ref=grid[grid.estimand==('cash_slope' if r.target=='cash' else r.target)]
        # Top75 average effect is the focal benchmark; secondary outcomes use own model.
        m=smf.ols(r.outcome+'~C(form)*z',d).fit(cov_type='HC3')
        w={'z':1} if r.target=='cash' else {f'C(form)[T.{r.target.split("-")[1]}]:z':-1}
        e=contrast(m,w)['estimate']
        power.append(dict(variable=r.variable,outcome=r.outcome,target=r.target,N=r.N,cash_N=r.cash_N,se_actual_HC3=r.se,MDE_80=mde,average_effect=e,MDE_over_absolute_effect=mde/abs(e),cannot_rule_out_average_scale=bool(mde>abs(e)),method='two-sided5%80% normal-design plug-in MDE per1SD; actual variance/design; not power simulation'))
    write(pd.DataFrame(power),'moderator_power_mde.csv')
    cash=d[d.form=='cash']
    for outcome in ['top75','ordinal','midpoint']:
        m=smf.ols(outcome+'~z+fundraising+income_rank_z',cash).fit(cov_type='HC3')
        for v in ['z','fundraising','income_rank_z']:
            r=contrast(m,{v:1});controls.append(dict(outcome=outcome,control=v,N=len(cash),expected_sign='negative',sign_matches=bool(r['estimate']<0),estimand='Cash within-form association adjusted jointly for size, income rank, emergency capacity',**r))
    write(holm(pd.DataFrame(controls)),'positive_controls.csv')

def main(path):
    d=covariates(data(path));profiles(d);equivalence(d);binding(d);relative(d);moderators(d)
    grid=pd.read_csv(OUT/'specification_grid.csv')
    quality=grid[(grid.outcome=='top75')&(grid.model=='OLS_HC3')&(grid.representation=='trend')]
    write(quality,'quality_gradient_source.csv')
    print('Finite secondary analyses complete.',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);main(ap.parse_args().data)
