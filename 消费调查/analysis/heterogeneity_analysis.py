"""Systematic stated-MPC and randomized treatment-effect heterogeneity audit.

Usage:
  python heterogeneity_analysis.py delivery.dta --out ../heterogeneity-output

The script never writes respondent-level records. Outputs are aggregate tables and figures.
"""
from argparse import ArgumentParser
from pathlib import Path
import json, math, warnings
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RepeatedKFold, StratifiedKFold, cross_validate
from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
SEED=20260921
SCEN=["q32_cash200","q33_cash1k","q34_cash5k","q35_vouch200","q36_vouch1k","q37_vouch5k","q38_med200","q39_med1k","q40_med5k"]
TYPES=["cash"]*3+["food"]*3+["medical"]*3; AMOUNTS=[200,1000,5000]*3
MID={1:0,2:.05,3:.175,4:.375,5:.625,6:.875}; ALT={**MID,6:1.0}

FEATURES={
"q42_age":("Q42","age","objective","continuous",True),
"q41_gender":("Q41","gender","objective","binary",True),
"q43_edu":("Q43","education","objective","ordinal",True),
"income_h":("Q46","monthly income harmonized 1-6","objective","ordinal",True),
"q23_hukou":("Q23","hukou","objective","categorical",True),
"q24_workstat":("Q24","employment status","objective","categorical",True),
"q25_unittype":("Q25","work-unit type","objective","categorical",True),
"q26_housing":("Q26","housing tenure","objective","categorical",True),
"q27_minorchild":("Q27","minor child","needs","binary",True),
"q28_hhsize":("Q28","household size","needs","ordinal",True),
"q29_foodexp":("Q29","monthly food spending","needs","ordinal",True),
"q30_medexp":("Q30","annual OOP medical spending","needs","ordinal",True),
"q31_gotsubsidy":("Q31","prior subsidy","objective","categorical",True),
"q49_citytier":("Q49","city tier","objective","ordinal",True),
"q06_socsec":("Q6","perceived social protection","subjective_economic","continuous",True),
"q07_emergfund":("Q7","emergency liquidity","subjective_economic","continuous",True),
"q09_gain":("Q9","sense of gain","subjective_economic","continuous",True),
"q10_effort":("Q10","returns to effort","subjective_economic","continuous",True),
"q11_mobility":("Q11","upward mobility","subjective_economic","continuous",True),
"q13_pressure":("Q13","pressure affordability","subjective_economic","continuous",True),
"q15_fut_self":("Q15","future self","subjective_economic","continuous",True),
"q17a_fut_econ":("Q17-1","economic outlook","subjective_economic","continuous",True),
"q17b_fut_job":("Q17-2","employment/income outlook","subjective_economic","continuous",True),
"q17c_fut_price":("Q17-3","price/affordability outlook","subjective_economic","continuous",True),
"q17e_fut_welfare":("Q17-5","welfare outlook","subjective_economic","continuous",True),
"q18_ses_now":("Q18","subjective SES","subjective_economic","ordinal",True),
"q19_ses_past5":("Q19","past mobility","subjective_economic","continuous",True),
"q20_ses_next1":("Q20","expected mobility","subjective_economic","continuous",True),
"q01_lifesat":("Q1","life satisfaction","attitudes","continuous",False),
"q02_safety":("Q2","safety","attitudes","continuous",False),
"q03a_fair_dist":("Q3-1","distribution fairness","attitudes","continuous",False),
"q03b_fair_opp":("Q3-2","opportunity fairness","attitudes","continuous",False),
"q03c_fair_rule":("Q3-3","rule fairness","attitudes","continuous",False),
"q04_trust_gov":("Q4","institutional trust","attitudes","continuous",False),
"q05_trust_soc":("Q5","generalized trust","attitudes","continuous",False),
"q08_support":("Q8","social support","attitudes","continuous",False),
"q12_voice":("Q12","voice/response","attitudes","continuous",False),
"q16_fut_society":("Q16","national outlook","attitudes","continuous",False),
"q17d_fut_fair":("Q17-4","fairness outlook","attitudes","continuous",False),
"q21_order":("Q21","social order","attitudes","continuous",False),
"q22_vitality":("Q22","social vitality","attitudes","continuous",False),
}
SETS={"O":[k for k,v in FEATURES.items() if v[2] in ["objective","needs"]],"S":[k for k,v in FEATURES.items() if v[2]=="subjective_economic"],"A":[k for k,v in FEATURES.items() if v[2]=="attitudes"]}
SETS["ALL"]=SETS["O"]+SETS["S"]+SETS["A"]

def bh(p):
    p=np.asarray(p,float); order=np.argsort(p); q=np.empty(len(p)); ranked=p[order]*len(p)/np.arange(1,len(p)+1); ranked=np.minimum.accumulate(ranked[::-1])[::-1]; q[order]=np.minimum(ranked,1); return q
def contrast(res, weights):
    names=list(res.params.index); v=np.zeros(len(names))
    for k,w in weights.items():
        if k in names: v[names.index(k)]=w
    z=res.t_test(v); return np.asarray(z.effect).item(),np.asarray(z.sd).item(),np.asarray(z.conf_int())[0,0],np.asarray(z.conf_int())[0,1],np.asarray(z.pvalue).item()
def prep(d):
    hit=d[SCEN].notna(); d=d.copy(); d["scenario_n"]=hit.sum(1); d["treatment_cell"]=np.where(d.scenario_n.eq(1),hit.values.argmax(1)+1,np.nan)
    d["transfer_type"]=d.treatment_cell.map(dict(enumerate(TYPES,1))); d["amount"]=d.treatment_cell.map(dict(enumerate(AMOUNTS,1)))
    d["outcome_ord"]=d[SCEN].bfill(axis=1).iloc[:,0]; d["mpc_midpoint"]=d.outcome_ord.map(MID); d["mpc_alt"]=d.outcome_ord.map(ALT)
    d["any_spend"]=(d.outcome_ord>1).astype(int); d["mpc_10plus"]=(d.outcome_ord>=3).astype(int); d["mpc_25plus"]=(d.outcome_ord>=4).astype(int); d["high_mpc"]=(d.outcome_ord>=5).astype(int)
    d["income_h"]=np.where(d.q46_income.between(11,16),d.q46_income-10,d.q46_income)
    scales=["q01_lifesat","q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q06_socsec","q07_emergfund","q08_support","q09_gain","q10_effort","q11_mobility","q12_voice","q13_pressure"]
    straight=d[scales].nunique(1).eq(1); d["clean_candidate"]=~(straight|~d.q42_age.between(18,100)|d.id.duplicated(False))
    for x in FEATURES:
        d[x+"_z"]=(d[x]-d[x].mean())/d[x].std()
    return d
def variable_map(d):
    rows=[]
    for x,(item,concept,domain,kind,main) in FEATURES.items():
        tr="legacy Q46 11-16 -> 1-6; z-score for interactions" if x=="income_h" else "raw coding; z-score for interactions"
        rows.append([x,item,concept,domain,kind,int(d[x].isna().sum()),str(sorted(d[x].dropna().unique())[:10]),tr,main,not main])
    return pd.DataFrame(rows,columns=["variable","item","concept","domain","type","missing_N","coding_abridged","transformation","main_theory","exploratory_ML"])

def descriptive(d,out):
    key=["income_h","q07_emergfund","q06_socsec","q15_fut_self","q17b_fut_job","q18_ses_now","q29_foodexp","q30_medexp","q42_age","q43_edu"]
    rows=[]; gaps=[]
    for x in key:
        try: bins=pd.qcut(d[x],3,duplicates="drop")
        except Exception: bins=d[x]
        for b,g in d.groupby(bins,observed=True):
            for t,h in g.groupby("transfer_type"):
                y=h.outcome_ord; se=y.std()/math.sqrt(len(y)); rows.append([x,str(b),t,len(y),y.mean(),se,y.mean()-1.96*se,y.mean()+1.96*se])
            for t in ["food","medical"]:
                a=g[g.transfer_type.eq(t)].outcome_ord; c=g[g.transfer_type.eq('cash')].outcome_ord
                diff=a.mean()-c.mean(); se=math.sqrt(a.var()/len(a)+c.var()/len(c)); gaps.append([x,str(b),f"{t}-cash",len(a),len(c),diff,se,diff-1.96*se,diff+1.96*se])
    pd.DataFrame(rows,columns=["variable","group","type","N","mean","se","lo","hi"]).to_csv(out/"heterogeneity_descriptive_levels.csv",index=False)
    gap=pd.DataFrame(gaps,columns=["variable","group","contrast","N_treated","N_cash","effect","se","lo","hi"]); gap.to_csv(out/"heterogeneity_descriptive_gaps.csv",index=False)
    return gap

def theory_scan(d,out):
    outcomes=["outcome_ord","mpc_midpoint","mpc_alt","any_spend","mpc_10plus","mpc_25plus","high_mpc"]
    rows=[]
    for sample,dd in [("raw",d),("clean",d[d.clean_candidate])]:
      for y in outcomes:
       for x,meta in FEATURES.items():
        z=x+"_z"
        lvl=smf.ols(f"{y}~C(transfer_type)*C(amount)+{z}",dd).fit(cov_type="HC1")
        m=smf.ols(f"{y}~C(transfer_type)*C(amount)+{z}+C(transfer_type):{z}+C(amount):{z}",dd).fit(cov_type="HC1")
        terms={"level":{z:1},"food-cash":{f"C(transfer_type)[T.food]:{z}":1},"medical-cash":{f"C(transfer_type)[T.medical]:{z}":1},"restricted-cash":{f"C(transfer_type)[T.food]:{z}":.5,f"C(transfer_type)[T.medical]:{z}":.5},"medical-food":{f"C(transfer_type)[T.medical]:{z}":1,f"C(transfer_type)[T.food]:{z}":-1}}
        for estimand,w in terms.items():
            r=contrast(lvl if estimand=="level" else m,w); rows.append([sample,y,x,meta[1],meta[2],estimand,*r,int(m.nobs)])
    z=pd.DataFrame(rows,columns=["sample","outcome","variable","concept","family","estimand","effect","se","lo","hi","p","N"])
    z["q"]=np.nan
    primary=z[(z['sample']=='raw')&(z.outcome=='outcome_ord')].copy()
    for (fam,est),ix in primary.groupby(["family","estimand"]).groups.items(): z.loc[ix,"q"]=bh(z.loc[ix,"p"])
    # Robustness score for primary treatment HTE.
    keys=z[(z.estimand!='level')].groupby(["variable","estimand"])
    robust=[]
    for k,g in keys:
        base=g[(g['sample']=='raw')&(g.outcome=='outcome_ord')]
        if base.empty: continue
        s=np.sign(base.effect.iloc[0]); stable=((np.sign(g.effect)==s)&(g.effect.abs()>.00001)).mean()
        robust.append([*k,float(base.effect.iloc[0]),float(base.p.iloc[0]),float(base.q.iloc[0]) if pd.notna(base.q.iloc[0]) else np.nan,stable,int((g.p<.05).sum()),len(g)])
    rb=pd.DataFrame(robust,columns=["variable","estimand","primary_effect","primary_p","primary_q","sign_stability","specs_p_lt_05","specs_total"])
    z.to_csv(out/"heterogeneity_theory_scan.csv",index=False); rb.to_csv(out/"heterogeneity_robustness_grid.csv",index=False)
    return z,rb

def amount_specific_scan(d,out):
    rows=[]
    for sample,dd in [('raw',d),('clean',d[d.clean_candidate])]:
      for amount in [200,1000,5000]:
       da=dd[dd.amount.eq(amount)]
       for y in ['outcome_ord','mpc_midpoint','mpc_alt','any_spend','mpc_25plus']:
        for x,meta in FEATURES.items():
          z=x+'_z'; m=smf.ols(f"{y}~C(transfer_type)+{z}+C(transfer_type):{z}",da).fit(cov_type='HC1')
          for est,w in [('food-cash',{f"C(transfer_type)[T.food]:{z}":1}),('medical-cash',{f"C(transfer_type)[T.medical]:{z}":1}),('medical-food',{f"C(transfer_type)[T.medical]:{z}":1,f"C(transfer_type)[T.food]:{z}":-1})]:
            r=contrast(m,w); rows.append([sample,amount,y,x,meta[1],meta[2],est,*r,int(m.nobs)])
    tab=pd.DataFrame(rows,columns=['sample','amount','outcome','variable','concept','family','estimand','effect','se','lo','hi','p','N']); tab['q']=np.nan
    prim=tab[(tab['sample']=='raw')&(tab.outcome=='outcome_ord')]
    for (fam,est,amt),ix in prim.groupby(['family','estimand','amount']).groups.items(): tab.loc[ix,'q']=bh(tab.loc[ix,'p'])
    tab.to_csv(out/'heterogeneity_amount_specific.csv',index=False)

def ordered_checks(d,theory,out):
    top=theory[(theory['sample']=='raw')&(theory.outcome=='outcome_ord')&(theory.estimand.isin(['food-cash','medical-cash']))].sort_values('p').head(16).variable.unique()
    rows=[]
    for x in top:
      dd=d.copy(); z=dd[x+"_z"]
      X=pd.DataFrame({"food":dd.transfer_type.eq('food').astype(int),"medical":dd.transfer_type.eq('medical').astype(int),"a1000":dd.amount.eq(1000).astype(int),"a5000":dd.amount.eq(5000).astype(int),"x":z})
      X["food_x"]=X.food*X.x; X["medical_x"]=X.medical*X.x; X["a1000_x"]=X.a1000*X.x; X["a5000_x"]=X.a5000*X.x
      try:
        m=OrderedModel(dd.outcome_ord.astype(int),X,distr='logit').fit(method='bfgs',disp=False,maxiter=250)
        for est,term in [("food-cash","food_x"),("medical-cash","medical_x")]:
            b=m.params[term]; se=m.bse[term]; rows.append([x,est,b,se,b-1.96*se,b+1.96*se,m.pvalues[term],m.mle_retvals.get('converged',False)])
        v=np.zeros(len(m.params)); v[list(m.params.index).index('medical_x')]=1; v[list(m.params.index).index('food_x')]=-1; z=m.t_test(v); b=np.asarray(z.effect).item(); se=np.asarray(z.sd).item(); ci=np.asarray(z.conf_int())[0]; rows.append([x,'medical-food',b,se,ci[0],ci[1],np.asarray(z.pvalue).item(),m.mle_retvals.get('converged',False)])
      except Exception: rows.append([x,"failed",np.nan,np.nan,np.nan,np.nan,np.nan,False])
    pd.DataFrame(rows,columns=["variable","estimand","ordered_logit_coef","se","lo","hi","p","converged"]).to_csv(out/"heterogeneity_ordered_checks.csv",index=False)

def domain_models(d,out):
    domains={
      "E1_objective_resources":["q42_age","q41_gender","q43_edu","income_h","q23_hukou","q24_workstat","q25_unittype","q26_housing","q31_gotsubsidy","q49_citytier"],
      "E2_liquidity_resilience":["q07_emergfund","income_h","q26_housing","q24_workstat"],
      "E3_expectations":["q15_fut_self","q17a_fut_econ","q17b_fut_job","q17c_fut_price","q17e_fut_welfare","q20_ses_next1"],
      "E4_protection_precaution":["q06_socsec","q13_pressure","q30_medexp","q24_workstat"],
      "E5_baseline_needs":["q27_minorchild","q28_hhsize","q29_foodexp","q30_medexp"],
      "S1_broader_attitudes":SETS["A"],
      "ALL":SETS["ALL"],
    }
    rows=[]
    for name,cols in domains.items():
        zs=[x+"_z" for x in cols]; mains="+".join(zs); inter="+".join([f"C(transfer_type):{z}" for z in zs]+[f"C(amount):{z}" for z in zs])
        m=smf.ols(f"mpc_midpoint~C(transfer_type)*C(amount)+{mains}+{inter}",d).fit(cov_type='HC1')
        terms=[t for t in m.params.index if 'C(transfer_type)' in t and ':' in t and any(z in t for z in zs)]
        R=np.zeros((len(terms),len(m.params)))
        for i,t in enumerate(terms): R[i,list(m.params.index).index(t)]=1
        w=m.wald_test(R,scalar=True) if terms else None
        rows.append([name,len(cols),m.rsquared,m.rsquared_adj,float(w.statistic) if w else np.nan,len(terms),float(w.pvalue) if w else np.nan,int(m.nobs)])
    pd.DataFrame(rows,columns=["domain_model","features","r2","adjusted_r2","type_interaction_wald","df","p","N"]).to_csv(out/"heterogeneity_domain_models.csv",index=False)

def regularized_interactions(d,out):
    base=pd.DataFrame({x:d[x+'_z'] for x in FEATURES}); td=pd.get_dummies(d.transfer_type,prefix='type',drop_first=True,dtype=float); ad=pd.get_dummies(d.amount,prefix='amount',drop_first=True,dtype=float)
    X=pd.concat([td,ad,base],axis=1)
    for t in td:
        for x in FEATURES: X[f'{t}__x__{x}']=td[t]*base[x]
    for a in ad:
        for x in FEATURES: X[f'{a}__x__{x}']=ad[a]*base[x]
    X=X.to_numpy(float); y=d.mpc_midpoint.to_numpy(float); names=list(pd.concat([td,ad,base],axis=1).columns)+[f'{t}__x__{x}' for t in td for x in FEATURES]+[f'{a}__x__{x}' for a in ad for x in FEATURES]
    outer=RepeatedKFold(n_splits=5,n_repeats=2,random_state=SEED); perf=[]; coefs=[]
    models={"ridge":lambda:RidgeCV(alphas=np.logspace(-3,3,25)),"lasso":lambda:LassoCV(alphas=np.logspace(-5,-1,35),cv=5,max_iter=10000,random_state=SEED),"elastic_net":lambda:ElasticNetCV(l1_ratio=[.1,.5,.9],alphas=np.logspace(-5,-1,30),cv=5,max_iter=10000,random_state=SEED)}
    for modelname,builder in models.items():
      for fold,(tr,te) in enumerate(outer.split(X)):
        sc=StandardScaler(); xt=sc.fit_transform(X[tr]); xe=sc.transform(X[te]); m=builder(); m.fit(xt,y[tr]); pr=m.predict(xe); perf.append([modelname,fold,r2_score(y[te],pr),math.sqrt(mean_squared_error(y[te],pr))]); coefs.append(pd.DataFrame({'model':modelname,'fold':fold,'term':names,'coefficient':m.coef_}))
    pd.DataFrame(perf,columns=['model','fold','r2','rmse']).to_csv(out/'heterogeneity_regularized_cv.csv',index=False)
    c=pd.concat(coefs,ignore_index=True); s=c.groupby(['model','term']).agg(mean_coefficient=('coefficient','mean'),mean_abs_coefficient=('coefficient',lambda x:np.abs(x).mean()),nonzero_frequency=('coefficient',lambda x:(np.abs(x)>1e-8).mean())).reset_index(); s.to_csv(out/'heterogeneity_regularized_coefficients.csv',index=False)

def transformer(cols):
    cats=[x for x in cols if FEATURES[x][3] in ["categorical","binary"]]
    nums=[x for x in cols if x not in cats]
    return ColumnTransformer([("num",Pipeline([("imp",SimpleImputer(strategy='median')),("sc",StandardScaler())]),nums),("cat",Pipeline([("imp",SimpleImputer(strategy='most_frequent')),("oh",OneHotEncoder(handle_unknown='ignore'))]),cats)])
def level_ml(d,out,figs):
    cv=RepeatedKFold(n_splits=5,n_repeats=2,random_state=SEED); rows=[]
    level_sets={**SETS,"O+S":SETS["O"]+SETS["S"],"O+A":SETS["O"]+SETS["A"]}
    models={"ridge":RidgeCV(alphas=np.logspace(-3,3,13)),"random_forest":RandomForestRegressor(n_estimators=160,min_samples_leaf=20,max_features=.7,n_jobs=-1,random_state=SEED),"hist_gradient_boosting":HistGradientBoostingRegressor(max_iter=180,l2_regularization=1,min_samples_leaf=20,random_state=SEED)}
    for setname,cols in level_sets.items():
      for name,est in models.items():
        pipe=Pipeline([("pre",transformer(cols)),("model",est)])
        z=cross_validate(pipe,d[cols],d.mpc_midpoint,cv=cv,scoring={"r2":"r2","mse":"neg_mean_squared_error"},n_jobs=1)
        for fold,(r2,mse) in enumerate(zip(z['test_r2'],-z['test_mse'])): rows.append([setname,name,fold,r2,math.sqrt(mse)])
    cvtab=pd.DataFrame(rows,columns=["feature_set","model","fold","r2","rmse"]); cvtab.to_csv(out/"heterogeneity_level_ml_cv.csv",index=False)
    avg=cvtab.groupby(['feature_set','model']).agg(r2=('r2','mean'),rmse=('rmse','mean')).reset_index(); fig,ax=plt.subplots(figsize=(10,5)); sns.barplot(data=avg,x='feature_set',y='r2',hue='model',ax=ax); ax.axhline(0,color='black',lw=.8); ax.set(title='Out-of-sample prediction of stated MPC level',ylabel='Repeated 5-fold CV R-squared',xlabel='Feature set'); fig.tight_layout(); fig.savefig(figs/'heterogeneity_level_cv_comparison.png',dpi=180); plt.close(fig)
    # Honest holdout permutation importance and PDP for ALL HGB.
    rng=np.random.default_rng(SEED); test=rng.random(len(d))<.3; cols=SETS['ALL']; pipe=Pipeline([("pre",transformer(cols)),("model",HistGradientBoostingRegressor(max_iter=200,l2_regularization=1,min_samples_leaf=20,random_state=SEED))]); pipe.fit(d.loc[~test,cols],d.loc[~test,'mpc_midpoint'])
    pred=pipe.predict(d.loc[test,cols]); pi=permutation_importance(pipe,d.loc[test,cols],d.loc[test,'mpc_midpoint'],scoring='neg_mean_squared_error',n_repeats=10,random_state=SEED)
    imp=pd.DataFrame({"variable":cols,"importance_mean":pi.importances_mean,"importance_sd":pi.importances_std}).sort_values('importance_mean',ascending=False); imp.to_csv(out/"heterogeneity_level_ml_importance.csv",index=False)
    top=[x for x in imp.variable.head(3) if FEATURES[x][3] not in ['categorical']]
    if top:
        fig,axes=plt.subplots(1,len(top),figsize=(5*len(top),4)); axes=np.atleast_1d(axes); PartialDependenceDisplay.from_estimator(pipe,d.loc[test,cols],features=top,ax=axes); fig.tight_layout(); fig.savefig(figs/"heterogeneity_level_partial_dependence.png",dpi=180); plt.close(fig)
    return cvtab,imp

def encode_frame(train,test,cols):
    cats=[x for x in cols if FEATURES[x][3] in ['categorical','binary']]; nums=[x for x in cols if x not in cats]
    tr=train[cols].copy(); te=test[cols].copy(); both=pd.concat([tr,te]); both=pd.get_dummies(both,columns=cats,drop_first=False,dtype=float); both=both.fillna(both.median())
    return both.iloc[:len(tr)].to_numpy(float),both.iloc[len(tr):].to_numpy(float),list(both.columns)
def honest_cate(d,contrast,cols,method="t_rf"):
    treated,control=contrast
    dd=d[d.transfer_type.isin([treated,control])].reset_index(drop=True).copy(); W=dd.transfer_type.eq(treated).astype(int).to_numpy(); Y=dd.mpc_midpoint.to_numpy(); pred=np.zeros(len(dd)); foldid=np.zeros(len(dd),int); importances=[]
    cv=StratifiedKFold(5,shuffle=True,random_state=SEED)
    for k,(tr,te) in enumerate(cv.split(dd,W)):
        Xtr,Xte,names=encode_frame(dd.iloc[tr],dd.iloc[te],cols); wt=W[tr]; yt=Y[tr]
        if method=="t_rf":
            kw=dict(n_estimators=180,min_samples_leaf=25,max_features=.7,n_jobs=-1,random_state=SEED+k)
            m1=RandomForestRegressor(**kw).fit(Xtr[wt==1],yt[wt==1]); m0=RandomForestRegressor(**kw).fit(Xtr[wt==0],yt[wt==0]); pred[te]=m1.predict(Xte)-m0.predict(Xte); importances.append((m1.feature_importances_+m0.feature_importances_)/2)
        else:
            inner=StratifiedKFold(3,shuffle=True,random_state=SEED+k); mu1=np.zeros(len(tr)); mu0=np.zeros(len(tr))
            for a,b in inner.split(Xtr,wt):
                f1=HistGradientBoostingRegressor(max_iter=120,min_samples_leaf=20,l2_regularization=1,random_state=SEED).fit(Xtr[a][wt[a]==1],yt[a][wt[a]==1]); f0=HistGradientBoostingRegressor(max_iter=120,min_samples_leaf=20,l2_regularization=1,random_state=SEED).fit(Xtr[a][wt[a]==0],yt[a][wt[a]==0]); mu1[b]=f1.predict(Xtr[b]); mu0[b]=f0.predict(Xtr[b])
            p=wt.mean(); pseudo=mu1-mu0+wt*(yt-mu1)/p-(1-wt)*(yt-mu0)/(1-p); tau=RandomForestRegressor(n_estimators=180,min_samples_leaf=30,max_features=.7,n_jobs=-1,random_state=SEED+k).fit(Xtr,pseudo); pred[te]=tau.predict(Xte); importances.append(tau.feature_importances_)
        foldid[te]=k
    dd["cate_oof"]=pred; dd["quintile"]=pd.qcut(pred,5,labels=False,duplicates='drop')+1
    groups=[]
    for q,g in dd.groupby('quintile'):
        a=g[g.transfer_type.eq(treated)].outcome_ord; b=g[g.transfer_type.eq(control)].outcome_ord; eff=a.mean()-b.mean(); se=math.sqrt(a.var()/len(a)+b.var()/len(b)); groups.append([q,len(g),len(a),len(b),pred[g.index].mean(),eff,se,eff-1.96*se,eff+1.96*se])
    # BLP calibration: randomized effect variation along held-out CATE score.
    dd["W"]=W; dd["cate_c"]=dd.cate_oof-dd.cate_oof.mean(); blp=smf.ols("mpc_midpoint~W+cate_c+W:cate_c+C(amount)",dd).fit(cov_type='HC1'); b=blp.params['W:cate_c']; se=blp.bse['W:cate_c']
    im=np.mean(importances,axis=0); base_names=[]
    for n in names:
        matches=[x for x in cols if n==x or n.startswith(x+"_")]
        base_names.append(max(matches,key=len) if matches else n)
    agg={}
    for n,v in zip(base_names,im): agg[n]=agg.get(n,0)+v
    return dd,pd.DataFrame(groups,columns=["quintile","N","N_treated","N_control","predicted_cate","effect_ord","se","lo","hi"]),pd.DataFrame(sorted(agg.items(),key=lambda x:-x[1]),columns=['variable','model_importance']),[b,se,b-1.96*se,b+1.96*se,blp.pvalues['W:cate_c'],len(dd)]
def hte_ml(d,out,figs):
    contrasts={"food-cash":("food","cash"),"medical-cash":("medical","cash")}
    # restricted-cash gets a binary pooled restricted treatment.
    dr=d.copy(); dr["transfer_type_orig"]=dr.transfer_type; dr["transfer_type"]=np.where(dr.transfer_type.eq('cash'),'cash','restricted')
    all_groups=[]; all_imp=[]; all_blp=[]
    for cname,pair in contrasts.items():
      for setname,cols in SETS.items():
        dd,g,imp,blp=honest_cate(d,pair,cols,'t_rf'); g.insert(0,'method','t_rf'); g.insert(0,'feature_set',setname); g.insert(0,'contrast',cname); all_groups.append(g); imp.insert(0,'feature_set',setname); imp.insert(0,'contrast',cname); imp.insert(0,'method','t_rf'); all_imp.append(imp); all_blp.append([cname,setname,'t_rf',*blp])
      dd,g,imp,blp=honest_cate(d,pair,SETS['ALL'],'dr_rf'); g.insert(0,'method','dr_rf'); g.insert(0,'feature_set','ALL'); g.insert(0,'contrast',cname); all_groups.append(g); imp.insert(0,'feature_set','ALL'); imp.insert(0,'contrast',cname); imp.insert(0,'method','dr_rf'); all_imp.append(imp); all_blp.append([cname,'ALL','dr_rf',*blp])
    for setname,cols in SETS.items():
        dd,g,imp,blp=honest_cate(dr,("restricted","cash"),cols,'t_rf'); g.insert(0,'method','t_rf'); g.insert(0,'feature_set',setname); g.insert(0,'contrast','restricted-cash'); all_groups.append(g); imp.insert(0,'feature_set',setname); imp.insert(0,'contrast','restricted-cash'); imp.insert(0,'method','t_rf'); all_imp.append(imp); all_blp.append(['restricted-cash',setname,'t_rf',*blp])
    G=pd.concat(all_groups,ignore_index=True); I=pd.concat(all_imp,ignore_index=True); B=pd.DataFrame(all_blp,columns=['contrast','feature_set','method','calibration_slope','se','lo','hi','p','N']); G.to_csv(out/"heterogeneity_honest_cate_quintiles.csv",index=False); I.to_csv(out/"heterogeneity_hte_ml_importance.csv",index=False); B.to_csv(out/"heterogeneity_hte_calibration.csv",index=False)
    fig,axes=plt.subplots(1,3,figsize=(15,4),sharey=True)
    for ax,c in zip(axes,['food-cash','medical-cash','restricted-cash']):
        z=G[(G.contrast==c)&(G.feature_set=='ALL')&(G.method=='t_rf')]; ax.errorbar(z.quintile,z.effect_ord,yerr=1.96*z.se,marker='o',capsize=4); ax.axhline(0,color='black',lw=.8); ax.set(title=c,xlabel='Held-out predicted CATE quintile',ylabel='Observed ordinal contrast')
    fig.tight_layout(); fig.savefig(figs/"heterogeneity_honest_cate_quintiles.png",dpi=180); plt.close(fig)
    return G,I,B

def food_inframarginal(d,out):
    bounds={1:(0,500),2:(501,1000),3:(1001,2000),4:(2001,3000),5:(3001,5000),6:(5000,np.inf)}
    cf=d[d.transfer_type.isin(['cash','food'])].copy()
    def cls(r):
        lo,hi=bounds[int(r.q29_foodexp)]; lo*=6; hi*=6
        return 'definitely_inframarginal' if r.amount<lo else ('likely_binding' if r.amount>hi else 'ambiguous')
    cf['food_binding']=cf.apply(cls,axis=1); inf=cf[cf.food_binding.eq('definitely_inframarginal')]
    rows=[]
    focus=['income_h','q07_emergfund','q18_ses_now','q28_hhsize','q27_minorchild','q29_foodexp','q15_fut_self','q17b_fut_job']
    for x in focus:
        z=x+'_z'; m=smf.ols(f"outcome_ord~C(transfer_type)*C(amount)+{z}+C(transfer_type):{z}+C(amount):{z}",inf).fit(cov_type='HC1'); r=contrast(m,{f"C(transfer_type)[T.food]:{z}":1}); rows.append([x,*r,int(m.nobs)])
    z=pd.DataFrame(rows,columns=['variable','effect','se','lo','hi','p','N']); z['q']=bh(z.p); z.to_csv(out/"heterogeneity_food_inframarginal.csv",index=False)
    return z

def figures(theory,gaps,out):
    sns.set_theme(style='whitegrid'); z=theory[(theory['sample']=='raw')&(theory.outcome=='outcome_ord')&(theory.estimand.isin(['food-cash','medical-cash']))].copy(); z['label']=z.concept
    for est in ['food-cash','medical-cash','medical-food','restricted-cash']:
        g=z[z.estimand.eq(est)].sort_values('effect'); fig,ax=plt.subplots(figsize=(8,10)); ax.errorbar(g.effect,range(len(g)),xerr=1.96*g.se,fmt='o',ms=4); ax.axvline(0,color='black',lw=.8); ax.set_yticks(range(len(g)),g.label); ax.set(title=f'Theory-guided HTE: {est}',xlabel='Interaction per 1 SD baseline X (ordinal categories)'); fig.tight_layout(); fig.savefig(out/f"heterogeneity_theory_{est}.png",dpi=180); plt.close(fig)

def main(data_path,out_path):
    out=Path(out_path); figs=out/"figures"; figs.mkdir(parents=True,exist_ok=True)
    d=prep(pd.read_stata(data_path,convert_categoricals=False)); variable_map(d).to_csv(out/"heterogeneity_variable_map.csv",index=False)
    gaps=descriptive(d,out); theory,robust=theory_scan(d,out); amount_specific_scan(d,out); ordered_checks(d,theory,out); domain_models(d,out); regularized_interactions(d,out); cvtab,levelimp=level_ml(d,out,figs); G,I,B=hte_ml(d,out,figs); inf=food_inframarginal(d,out); figures(theory,gaps,figs)
    summary={"raw_N":len(d),"clean_N":int(d.clean_candidate.sum()),"feature_count":len(FEATURES),"theory_specifications":len(theory),"level_cv_rows":len(cvtab),"honest_cate_group_rows":len(G)}
    (out/"heterogeneity_run_summary.json").write_text(json.dumps(summary,indent=2),encoding='utf-8'); print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=ArgumentParser(); p.add_argument('data'); p.add_argument('--out',default='heterogeneity-output'); a=p.parse_args(); main(a.data,a.out)
