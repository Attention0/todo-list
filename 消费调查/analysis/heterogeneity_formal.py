"""Formal second-pass stated-MPC predictability and transfer-form HTE analysis.

Only aggregate tables/figures are written. Respondent records and OOF predictions
remain in memory. Usage: python heterogeneity_formal.py delivery.dta --out DIR
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
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, RepeatedKFold, StratifiedKFold, GridSearchCV
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
SEED=20260921
SCEN=["q32_cash200","q33_cash1k","q34_cash5k","q35_vouch200","q36_vouch1k","q37_vouch5k","q38_med200","q39_med1k","q40_med5k"]
TYPES=["cash"]*3+["food"]*3+["medical"]*3; AMOUNTS=[200,1000,5000]*3
MID={1:0,2:.05,3:.175,4:.375,5:.625,6:.875}; ALT={**MID,6:1.0}

CONT=["q42_age","q06_socsec","q07_emergfund","q09_gain","q10_effort","q11_mobility","q13_pressure","q15_fut_self","q17a_fut_econ","q17b_fut_job","q17c_fut_price","q17e_fut_welfare","q18_ses_now","q19_ses_past5","q20_ses_next1","q01_lifesat","q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q08_support","q12_voice","q16_fut_society","q17d_fut_fair","q21_order","q22_vitality"]
ORDERED=["q43_edu","income_h","q28_hhsize","q29_foodexp","q30_medexp","q49_citytier"]
NOMINAL=["q41_gender","q23_hukou","q24_workstat","q25_unittype","q26_housing","q27_minorchild","q31_gotsubsidy"]
FEATURES=CONT+ORDERED+NOMINAL
NEEDS=["q27_minorchild","q28_hhsize","q29_foodexp","q30_medexp"]
OBJECTIVE=["q42_age","q41_gender","q43_edu","income_h","q23_hukou","q24_workstat","q25_unittype","q26_housing","q31_gotsubsidy","q49_citytier"]
SUBJECTIVE=[x for x in CONT if x.startswith(("q06","q07","q09","q10","q11","q13","q15","q17a","q17b","q17c","q17e","q18","q19","q20"))]
ATTITUDES=[x for x in CONT if x not in SUBJECTIVE and x!="q42_age"]
SETS={"T":[],"O":OBJECTIVE+NEEDS,"S":SUBJECTIVE,"A":ATTITUDES,"O+S":OBJECTIVE+NEEDS+SUBJECTIVE,"O+A":OBJECTIVE+NEEDS+ATTITUDES,"ALL":FEATURES}
FAMILY={x:("objective" if x in OBJECTIVE else "needs" if x in NEEDS else "subjective" if x in SUBJECTIVE else "attitudes") for x in FEATURES}

def bh(p):
    p=np.asarray(p,float); o=np.argsort(p); q=np.empty(len(p)); r=p[o]*len(p)/np.arange(1,len(p)+1); r=np.minimum.accumulate(r[::-1])[::-1]; q[o]=np.minimum(r,1); return q
def ctest(m,w):
    names=list(m.params.index); v=np.zeros(len(names))
    for k,a in w.items():
        if k in names:v[names.index(k)]=a
    z=m.t_test(v); ci=np.asarray(z.conf_int())[0]
    return float(np.asarray(z.effect).item()),float(np.asarray(z.sd).item()),float(ci[0]),float(ci[1]),float(np.asarray(z.pvalue).item())
def prep(d):
    hit=d[SCEN].notna(); assert hit.sum(1).eq(1).all(),"invalid treatment assignment"
    d=d.copy(); d["cell"]=hit.values.argmax(1)+1; d["transfer_type"]=d.cell.map(dict(enumerate(TYPES,1))); d["amount"]=d.cell.map(dict(enumerate(AMOUNTS,1)))
    d["outcome_ord"]=d[SCEN].bfill(axis=1).iloc[:,0].astype(int); assert d.outcome_ord.between(1,6).all()
    assert (d.scen_amount.astype(int)==d.amount).all() and (d.scen_mpc.astype(int)==d.outcome_ord).all()
    smap={1:"cash",2:"food",3:"medical","cash":"cash","food":"food","medical":"medical"}; assert d.scen_type.map(smap).eq(d.transfer_type).all()
    d["mpc_midpoint"]=d.outcome_ord.map(MID); d["mpc_alt"]=d.outcome_ord.map(ALT)
    d["any_spend"]=(d.outcome_ord>1).astype(int); d["mpc_10plus"]=(d.outcome_ord>=3).astype(int); d["mpc_25plus"]=(d.outcome_ord>=4).astype(int); d["mpc_50plus"]=(d.outcome_ord>=5).astype(int)
    d["income_h"]=np.where(d.q46_income.between(11,16),d.q46_income-10,d.q46_income)
    straight=d[["q01_lifesat","q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q06_socsec","q07_emergfund","q08_support","q09_gain","q10_effort","q11_mobility","q12_voice","q13_pressure"]].nunique(1).eq(1)
    d["sample_A"]=d.q42_age.between(18,100); d["sample_C"]=d.sample_A&~straight&~d.id.duplicated(False)
    for x in CONT+ORDERED:d[x+"_z"]=(d[x]-d[x].mean())/d[x].std()
    return d

def variable_map(d,out):
    rows=[]
    for x in FEATURES:
        typ="continuous" if x in CONT else "ordered" if x in ORDERED else "nominal"
        formal="z trend; bins/spline for top findings" if typ=="continuous" else "z trend plus factor robustness" if typ=="ordered" else "factor only; joint omnibus"
        rows.append([x,typ,FAMILY[x],int(d[x].nunique()),int(d[x].isna().sum()),formal])
    pd.DataFrame(rows,columns=["variable","formal_type","family","levels","missing_N","formal_coding"]).to_csv(out/"formal_variable_map.csv",index=False)

def average_effects(d,out):
    rows=[]
    for sn,dd in [("R",d),("A",d[d.sample_A]),("C",d[d.sample_C])]:
      for y in ["outcome_ord","mpc_midpoint"]:
       m=smf.ols(f"{y}~C(transfer_type)*C(amount)",dd).fit(cov_type="HC1")
       for a in [200,1000,5000]:
        for t,b in [("food","cash"),("medical","cash"),("medical","food")]:
         w={f"C(transfer_type)[T.{t}]":1 if t!="cash" else 0,f"C(transfer_type)[T.{b}]":-1 if b!="cash" else 0}
         if a!=200:
          w[f"C(transfer_type)[T.{t}]:C(amount)[T.{a}]"]=1 if t!="cash" else 0; w[f"C(transfer_type)[T.{b}]:C(amount)[T.{a}]"]=-1 if b!="cash" else 0
         rows.append([sn,y,a,f"{t}-{b}",*ctest(m,w),int(m.nobs)])
       for t,b in [("food","cash"),("medical","cash"),("medical","food")]:
        vals=[]
        for a in [200,1000,5000]:
         w={f"C(transfer_type)[T.{t}]":1/3 if t!="cash" else 0,f"C(transfer_type)[T.{b}]":-1/3 if b!="cash" else 0}
         if a!=200:
          w[f"C(transfer_type)[T.{t}]:C(amount)[T.{a}]"]=1/3 if t!="cash" else 0; w[f"C(transfer_type)[T.{b}]:C(amount)[T.{a}]"]=-1/3 if b!="cash" else 0
         vals.append(w)
        W={}; [W.update({k:W.get(k,0)+v for k,v in z.items()}) for z in vals]
        rows.append([sn,y,"pooled",f"{t}-{b}",*ctest(m,W),int(m.nobs)])
    pd.DataFrame(rows,columns=["sample","outcome","amount","contrast","effect","se","lo","hi","p","N"]).to_csv(out/"formal_average_effects.csv",index=False)

def hte_scan(d,out):
    rows=[]; cats=[]
    for sn,dd in [("R",d),("A",d[d.sample_A]),("C",d[d.sample_C])]:
      for x in CONT+ORDERED:
        z=x+"_z"; f=f"outcome_ord~C(transfer_type)*C(amount)+{z}+C(transfer_type):{z}+C(amount):{z}"
        for cov in ["HC1","HC3"]:
          m=smf.ols(f,dd).fit(cov_type=cov)
          ws={"food-cash":{f"C(transfer_type)[T.food]:{z}":1},"medical-cash":{f"C(transfer_type)[T.medical]:{z}":1},"medical-food":{f"C(transfer_type)[T.medical]:{z}":1,f"C(transfer_type)[T.food]:{z}":-1}}
          for est,w in ws.items():rows.append([sn,x,FAMILY[x],"trend",est,cov,*ctest(m,w),int(m.nobs)])
        if x in ORDERED and sn in ["R","C"]:
          m=smf.ols(f"outcome_ord~C(transfer_type)*C(amount)+C({x})+C(transfer_type):C({x})+C(amount):C({x})",dd).fit(cov_type="HC1")
          terms=[t for t in m.params.index if "C(transfer_type)" in t and f"C({x})" in t]
          R=np.zeros((len(terms),len(m.params))); [R.__setitem__((i,list(m.params.index).index(t)),1) for i,t in enumerate(terms)]
          w=m.wald_test(R,scalar=True); cats.append([sn,x,FAMILY[x],"ordered_factor",float(w.statistic),len(terms),float(w.pvalue),int(m.nobs)])
      for x in NOMINAL:
        m=smf.ols(f"outcome_ord~C(transfer_type)*C(amount)+C({x})+C(transfer_type):C({x})+C(amount):C({x})",dd).fit(cov_type="HC1")
        terms=[t for t in m.params.index if "C(transfer_type)" in t and f"C({x})" in t]
        R=np.zeros((len(terms),len(m.params))); [R.__setitem__((i,list(m.params.index).index(t)),1) for i,t in enumerate(terms)]
        w=m.wald_test(R,scalar=True); cats.append([sn,x,FAMILY[x],"nominal_factor",float(w.statistic),len(terms),float(w.pvalue),int(m.nobs)])
    z=pd.DataFrame(rows,columns=["sample","variable","family","coding","estimand","se_type","effect","se","lo","hi","p","N"]); z["q"]=np.nan
    for (fam,est),ix in z[(z['sample']=='R')&(z.se_type=='HC1')].groupby(["family","estimand"]).groups.items():z.loc[ix,"q"]=bh(z.loc[ix,"p"])
    z.to_csv(out/"formal_hte_scan.csv",index=False); pd.DataFrame(cats,columns=["sample","variable","family","coding","wald","df","omnibus_p","N"]).to_csv(out/"formal_categorical_omnibus.csv",index=False)
    return z

def top_robustness(d,out):
    rows=[]; top=["income_h","q43_edu","q30_medexp"]
    controls=[x for x in OBJECTIVE+NEEDS if x not in top]
    ctrl="+".join([f"C({x})" if x in NOMINAL+ORDERED else x for x in controls])
    for sn,dd in [("R",d),("A",d[d.sample_A]),("C",d[d.sample_C])]:
      for x in top:
       z=x+"_z"; base=f"outcome_ord~C(transfer_type)*C(amount)*{z}"
       specs={"primary":base,"controls":base+"+"+ctrl,"province_FE":base+"+C(q47_province)","citytier_FE":base+"+C(q49_citytier)"}
       for sp,f in specs.items():
        for cov,kw in [("HC1",{}),("HC3",{}),("province_cluster",{"groups":dd.q47_province}),("city_cluster",{"groups":dd.q48_city})]:
         try:
          m=smf.ols(f,dd).fit(cov_type=("cluster" if "cluster" in cov else cov),cov_kwds=kw)
          for a in [200,1000,5000]:
           w={f"C(transfer_type)[T.medical]:{z}":1,f"C(transfer_type)[T.food]:{z}":-1}
           if a!=200:w.update({f"C(transfer_type)[T.medical]:C(amount)[T.{a}]:{z}":1,f"C(transfer_type)[T.food]:C(amount)[T.{a}]:{z}":-1})
           rows.append([sn,x,sp,cov,a,*ctest(m,w),int(m.nobs)])
          terms=[t for t in m.params.index if z in t and "C(transfer_type)" in t]
          R=np.zeros((len(terms),len(m.params))); [R.__setitem__((i,list(m.params.index).index(t)),1) for i,t in enumerate(terms)]
          w=m.wald_test(R,scalar=True); rows.append([sn,x,sp,cov,"joint",float(w.statistic),np.nan,np.nan,np.nan,float(w.pvalue),int(m.nobs)])
         except Exception: pass
    pd.DataFrame(rows,columns=["sample","variable","specification","se_type","amount","effect_or_wald","se","lo","hi","p","N"]).to_csv(out/"formal_medical_food_robustness.csv",index=False)

def geography(d,out):
    rows=[]
    for level,col in [("province","q47_province"),("city","q48_city")]:
     for key,g in d.groupby(col):rows.append([level,key,len(g),g.transfer_type.nunique(),g.cell.nunique()])
    pd.DataFrame(rows,columns=["level","cluster","N","treatment_forms","treatment_cells"]).to_csv(out/"formal_geography_diagnostics.csv",index=False)
    d.groupby(["q47_province","transfer_type"]).size().rename("N").reset_index().to_csv(out/"formal_treatment_balance_province.csv",index=False)
    d.groupby(["q49_citytier","transfer_type"]).size().rename("N").reset_index().to_csv(out/"formal_treatment_balance_citytier.csv",index=False)

def design_matrix(df,cols):
    cats=[x for x in cols if x in NOMINAL+ORDERED]; nums=[x for x in cols if x not in cats]
    return ColumnTransformer([("num",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),nums),("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cats)],remainder="drop")
def add_design(d,cols):
    x=d[cols].copy(); x["type"]=d.transfer_type; x["amount_cat"]=d.amount.astype(str); return x
def level_predictability(d,out,figdir):
    rows=[]; rng=RepeatedKFold(n_splits=5,n_repeats=2,random_state=SEED); folds=list(rng.split(d)); base=["type","amount_cat"]
    for s,cols in SETS.items():
      X=add_design(d,cols); allcols=cols+base; cats=[x for x in allcols if x in NOMINAL+ORDERED+base]; nums=[x for x in allcols if x not in cats]
      pre=ColumnTransformer([("num",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),nums),("cat",Pipeline([("imp",SimpleImputer(strategy="most_frequent")),("oh",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cats)])
      for model,est,grid in [("ridge",Ridge(),{"model__alpha":[.1,1,10,100]}),("elastic_net",ElasticNet(max_iter=10000),{"model__alpha":[.001,.01],"model__l1_ratio":[.1,.7]}),("random_forest",RandomForestRegressor(n_estimators=100,min_samples_leaf=20,n_jobs=-1,random_state=SEED),{"model__max_features":[.5,1.0]}),("hist_gradient_boosting",HistGradientBoostingRegressor(max_iter=100,random_state=SEED),{"model__max_leaf_nodes":[15,31],"model__l2_regularization":[3]})]:
       for k,(tr,te) in enumerate(folds):
        pipe=Pipeline([("pre",pre),("model",est)]); fit=GridSearchCV(pipe,grid,cv=5,scoring="r2",n_jobs=1).fit(X.iloc[tr],d.mpc_midpoint.iloc[tr]); p=fit.predict(X.iloc[te]); rows.append([s,model,k,r2_score(d.mpc_midpoint.iloc[te],p),math.sqrt(mean_squared_error(d.mpc_midpoint.iloc[te],p)),mean_absolute_error(d.mpc_midpoint.iloc[te],p)])
    tab=pd.DataFrame(rows,columns=["feature_set","model","fold","r2","rmse","mae"]); tab.to_csv(out/"formal_level_ml_cv.csv",index=False)
    avg=tab.groupby(["feature_set","model"],as_index=False).agg(r2=("r2","mean"),rmse=("rmse","mean"),mae=("mae","mean")); sns.set_theme(style="whitegrid"); fig,ax=plt.subplots(figsize=(10,5)); sns.barplot(avg,x="feature_set",y="r2",hue="model",ax=ax); ax.axhline(0,color="black",lw=.8); ax.set(title="Formal OOS stated-MPC predictability",ylabel="Repeated 5-fold CV R²"); fig.tight_layout(); fig.savefig(figdir/"formal_level_predictability.png",dpi=180); plt.close(fig)
    # Classical in-sample and fixed-fold OLS CV.
    joint=[]
    for s,cols in SETS.items():
      terms=["C(transfer_type)*C(amount)"]+[f"C({x})" if x in NOMINAL+ORDERED else x for x in cols]+(["I(q42_age**2)"] if "q42_age" in cols else [])
      f="mpc_midpoint~"+"+".join(terms); m=smf.ols(f,d).fit()
      preds=np.zeros(len(d)); kf=KFold(10,shuffle=True,random_state=SEED)
      for tr,te in kf.split(d):preds[te]=smf.ols(f,d.iloc[tr]).fit().predict(d.iloc[te])
      joint.append([s,m.rsquared,m.rsquared_adj,r2_score(d.mpc_midpoint,preds),math.sqrt(mean_squared_error(d.mpc_midpoint,preds)),d.mpc_midpoint.var(),len(d)])
    pd.DataFrame(joint,columns=["feature_set","in_sample_r2","adjusted_r2","cv10_r2","cv10_rmse","outcome_variance","N"]).to_csv(out/"formal_level_joint_models.csv",index=False)
    return tab

def encode(train,test,cols):
    pre=design_matrix(train,cols); a=pre.fit_transform(train[cols]); b=pre.transform(test[cols]); return np.asarray(a.todense() if hasattr(a,"todense") else a),np.asarray(b.todense() if hasattr(b,"todense") else b)
def honest_hte(d,treated,control,cols,method):
    dd=d[d.transfer_type.isin([treated,control])].reset_index(drop=True).copy(); W=dd.transfer_type.eq(treated).astype(int).to_numpy(); Y=dd.mpc_midpoint.to_numpy(); pred=np.zeros(len(dd)); strata=dd.cell.astype(str)
    cv=StratifiedKFold(5,shuffle=True,random_state=SEED)
    for k,(tr,te) in enumerate(cv.split(dd,strata)):
      Xtr,Xte=encode(dd.iloc[tr],dd.iloc[te],cols+[]) ; atr=pd.get_dummies(dd.amount.iloc[tr],prefix="a",drop_first=True).to_numpy(); ate=pd.get_dummies(dd.amount.iloc[te],prefix="a",drop_first=True).reindex(columns=pd.get_dummies(dd.amount.iloc[tr],prefix="a",drop_first=True).columns,fill_value=0).to_numpy(); Xtr=np.c_[Xtr,atr]; Xte=np.c_[Xte,ate]
      wt=W[tr]; yt=Y[tr]; p=wt.mean()
      if method=="t_rf":
       kw=dict(n_estimators=220,min_samples_leaf=25,max_features=.7,n_jobs=-1,random_state=SEED+k); m1=RandomForestRegressor(**kw).fit(Xtr[wt==1],yt[wt==1]); m0=RandomForestRegressor(**kw).fit(Xtr[wt==0],yt[wt==0]); pred[te]=m1.predict(Xte)-m0.predict(Xte)
      else:
       mu=HistGradientBoostingRegressor(max_iter=150,min_samples_leaf=25,l2_regularization=3,random_state=SEED+k).fit(np.c_[Xtr,wt],yt); mu1=mu.predict(np.c_[Xtr,np.ones(len(tr))]); mu0=mu.predict(np.c_[Xtr,np.zeros(len(tr))])
       if method=="dr": target=mu1-mu0+wt*(yt-mu1)/p-(1-wt)*(yt-mu0)/(1-p); weight=None
       else: target=(yt-mu.predict(np.c_[Xtr,wt]))/(wt-p); weight=(wt-p)**2
       learner=RandomForestRegressor(n_estimators=220,min_samples_leaf=30,max_features=.7,n_jobs=-1,random_state=SEED+k).fit(Xtr,target,sample_weight=weight); pred[te]=learner.predict(Xte)
    dd["W"]=W; dd["cate"]=pred; dd["cate_c"]=pred-pred.mean(); dd["quintile"]=pd.qcut(pred,5,labels=False,duplicates="drop")+1
    m=smf.ols("mpc_midpoint~W+cate_c+W:cate_c+C(amount)",dd).fit(cov_type="HC1"); cal=ctest(m,{"W:cate_c":1})
    gs=[]
    for q,g in dd.groupby("quintile"):
      a=g[g.W.eq(1)].mpc_midpoint; b=g[g.W.eq(0)].mpc_midpoint; e=a.mean()-b.mean(); se=math.sqrt(a.var()/len(a)+b.var()/len(b)); gs.append([q,len(g),len(a),len(b),g.cate.mean(),e,se,e-1.96*se,e+1.96*se])
    g=pd.DataFrame(gs,columns=["quintile","N","N_treated","N_control","predicted_cate","effect","se","lo","hi"]); sep=g.iloc[-1].effect-g.iloc[0].effect; ses=math.sqrt(g.iloc[-1].se**2+g.iloc[0].se**2)
    return cal,g,[sep,ses,sep-1.96*ses,sep+1.96*ses]
def hte_ml(d,out,figdir):
    rows=[]; groups=[]
    for name,t,c in [("food-cash","food","cash"),("medical-cash","medical","cash"),("medical-food","medical","food")]:
      for method in ["t_rf","dr","r"]:
       cal,g,sep=honest_hte(d,t,c,FEATURES,method); rows.append([name,method,*cal,*sep]); g.insert(0,"method",method); g.insert(0,"contrast",name); groups.append(g)
    pd.DataFrame(rows,columns=["contrast","learner","calibration","cal_se","cal_lo","cal_hi","cal_p","top_bottom","tb_se","tb_lo","tb_hi"]).to_csv(out/"formal_hte_calibration.csv",index=False)
    G=pd.concat(groups); G.to_csv(out/"formal_hte_quintiles.csv",index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    for ax,c in zip(axes,["food-cash","medical-cash"]):
      for method,g in G[G.contrast.eq(c)].groupby("method"):ax.plot(g.quintile,g.effect,marker="o",label=method)
      ax.axhline(0,color="black",lw=.8); ax.set(title=c,xlabel="OOF predicted CATE quintile",ylabel="Observed midpoint contrast"); ax.legend()
    fig.tight_layout(); fig.savefig(figdir/"formal_hte_validation.png",dpi=180); plt.close(fig)

def food_nulls(d,out):
    bounds={1:(0,500),2:(501,1000),3:(1001,2000),4:(2001,3000),5:(3001,5000),6:(5000,np.inf)}; x=d[d.transfer_type.isin(["cash","food"])].copy()
    lo=x.q29_foodexp.map(lambda v:bounds[int(v)][0]*6); x["strict"]=x.amount<lo; x["very_strict"]=x.amount<=.5*lo
    rows=[]
    for sm,dd in [("strict",x[x.strict]),("very_strict",x[x.very_strict])]:
      for v in ["income_h","q29_foodexp","q28_hhsize","q27_minorchild","q07_emergfund","q18_ses_now","q15_fut_self","q17b_fut_job"]:
       if v in NOMINAL:
        m=smf.ols(f"outcome_ord~C(transfer_type)*C(amount)+C({v})+C(transfer_type):C({v})+C(amount):C({v})",dd).fit(cov_type="HC1"); terms=[t for t in m.params.index if "C(transfer_type)" in t and f"C({v})" in t]; R=np.zeros((len(terms),len(m.params))); [R.__setitem__((i,list(m.params.index).index(t)),1) for i,t in enumerate(terms)]; w=m.wald_test(R,scalar=True); rows.append([sm,v,"factor_omnibus",float(w.statistic),np.nan,np.nan,np.nan,float(w.pvalue),int(m.nobs),np.nan])
       else:
        z=v+"_z"; m=smf.ols(f"outcome_ord~C(transfer_type)*C(amount)+{z}+C(transfer_type):{z}+C(amount):{z}",dd).fit(cov_type="HC1"); r=ctest(m,{f"C(transfer_type)[T.food]:{z}":1}); rows.append([sm,v,"trend",*r,int(m.nobs),1.96*r[1]])
    z=pd.DataFrame(rows,columns=["sample","variable","coding","effect_or_wald","se","lo","hi","p","N","ci_halfwidth"]); z["q"]=np.nan
    for sm,ix in z.groupby("sample").groups.items():z.loc[ix,"q"]=bh(z.loc[ix,"p"])
    z.to_csv(out/"formal_food_null_precision.csv",index=False)

def randomization(d,out,B=2000):
    rng=np.random.default_rng(SEED); rows=[]
    targets=[("income_h","medical-food"),("q43_edu","medical-food"),("q30_medexp","medical-food")]
    for x,est in targets:
      z=x+"_z"; formula=f"outcome_ord~C(transfer_type)*C(amount)+{z}+C(transfer_type):{z}+C(amount):{z}"; m=smf.ols(formula,d).fit(cov_type="HC1"); w={f"C(transfer_type)[T.medical]:{z}":1,f"C(transfer_type)[T.food]:{z}":-1}; obs=ctest(m,w)[0]; vals=[]; cells=d.cell.to_numpy().copy()
      for b in range(B):
       dd=d.copy(); pcell=rng.permutation(cells); dd["transfer_type"]=pd.Series(pcell).map(dict(enumerate(TYPES,1))).to_numpy(); dd["amount"]=pd.Series(pcell).map(dict(enumerate(AMOUNTS,1))).to_numpy(); mm=smf.ols(formula,dd).fit(); vals.append(ctest(mm,w)[0])
      pv=(1+np.sum(np.abs(vals)>=abs(obs)))/(B+1); rows.append([x,est,obs,pv,B])
    pd.DataFrame(rows,columns=["variable","estimand","observed_effect","randomization_p","permutations"]).to_csv(out/"formal_randomization_inference.csv",index=False)

def ordered_top(d,out):
    rows=[]
    for x in ["income_h","q43_edu","q30_medexp"]:
      z=x+"_z"; X=pd.DataFrame({"food":d.transfer_type.eq("food").astype(int),"medical":d.transfer_type.eq("medical").astype(int),"a1":d.amount.eq(1000).astype(int),"a5":d.amount.eq(5000).astype(int),"x":d[z]});
      for c in ["food","medical","a1","a5"]:X[c+"_x"]=X[c]*X.x
      for dist in ["logit","probit"]:
       m=OrderedModel(d.outcome_ord,X,distr=dist).fit(method="bfgs",disp=False,maxiter=250); v=np.zeros(len(m.params)); v[list(m.params.index).index("medical_x")]=1; v[list(m.params.index).index("food_x")]=-1; q=m.t_test(v); ci=np.asarray(q.conf_int())[0]; rows.append([x,dist,float(np.asarray(q.effect).item()),float(np.asarray(q.sd).item()),ci[0],ci[1],float(np.asarray(q.pvalue).item())])
      for y in ["any_spend","mpc_10plus","mpc_25plus","mpc_50plus"]:
       m=smf.ols(f"{y}~C(transfer_type)*C(amount)+{z}+C(transfer_type):{z}+C(amount):{z}",d).fit(cov_type="HC1"); rows.append([x,y,*ctest(m,{f"C(transfer_type)[T.medical]:{z}":1,f"C(transfer_type)[T.food]:{z}":-1})[:5]])
    pd.DataFrame(rows,columns=["variable","model","effect","se","lo","hi","p"]).to_csv(out/"formal_ordered_threshold_checks.csv",index=False)

def individual_level_associations(d,out):
    rows=[]; base=smf.ols("mpc_midpoint~C(transfer_type)*C(amount)",d).fit(); r0=base.rsquared_adj
    for x in FEATURES:
      if x in NOMINAL+ORDERED:
        m=smf.ols(f"mpc_midpoint~C(transfer_type)*C(amount)+C({x})",d).fit(cov_type="HC1")
        terms=[t for t in m.params.index if f"C({x})" in t]; R=np.zeros((len(terms),len(m.params))); [R.__setitem__((i,list(m.params.index).index(t)),1) for i,t in enumerate(terms)]; w=m.wald_test(R,scalar=True)
        rows.append([x,FAMILY[x],"factor_omnibus",float(w.statistic),np.nan,np.nan,np.nan,float(w.pvalue),m.rsquared_adj-r0])
      else:
        z=x+"_z"; m=smf.ols(f"mpc_midpoint~C(transfer_type)*C(amount)+{z}",d).fit(cov_type="HC1"); b,se,lo,hi,p=ctest(m,{z:1}); rows.append([x,FAMILY[x],"per_SD",b,se,lo,hi,p,m.rsquared_adj-r0])
    pd.DataFrame(rows,columns=["variable","family","coding","effect_or_wald","se","lo","hi","p","incremental_adjusted_r2"]).to_csv(out/"formal_level_individual_associations.csv",index=False)

def focused_joint_medical(d,out):
    xs=["income_h","q43_edu","q30_medexp"]; zs=[x+"_z" for x in xs]
    focal="+".join(zs)+"+"+"+".join([f"C(transfer_type):{z}+C(amount):{z}" for z in zs])
    omit=set(xs); controls=[x for x in OBJECTIVE+NEEDS if x not in omit]
    ctrl="+".join([f"C({x})" if x in NOMINAL+ORDERED else x for x in controls])
    rows=[]
    for sn,dd in [("R",d),("A",d[d.sample_A]),("C",d[d.sample_C])]:
      for sp,extra in [("joint_unadjusted",""),("joint_prespecified","+"+ctrl),("joint_province_FE","+C(q47_province)")]:
       m=smf.ols("outcome_ord~C(transfer_type)*C(amount)+"+focal+extra,dd).fit(cov_type="HC1")
       for x,z in zip(xs,zs):rows.append([sn,sp,x,*ctest(m,{f"C(transfer_type)[T.medical]:{z}":1,f"C(transfer_type)[T.food]:{z}":-1}),int(m.nobs)])
    pd.DataFrame(rows,columns=["sample","specification","variable","effect","se","lo","hi","p","N"]).to_csv(out/"formal_medical_food_joint.csv",index=False)

def level_explainability(d,out,figdir):
    cols=FEATURES; X=add_design(d,cols); allcols=cols+["type","amount_cat"]; cats=[x for x in allcols if x in NOMINAL+ORDERED+["type","amount_cat"]]; nums=[x for x in allcols if x not in cats]
    pre=ColumnTransformer([("num",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),nums),("cat",Pipeline([("imp",SimpleImputer(strategy="most_frequent")),("oh",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cats)])
    pipe=Pipeline([("pre",pre),("model",RandomForestRegressor(n_estimators=300,min_samples_leaf=20,max_features=.5,n_jobs=-1,random_state=SEED))])
    rng=np.random.default_rng(SEED); test=rng.random(len(d))<.3; pipe.fit(X.loc[~test],d.mpc_midpoint.loc[~test]); pi=permutation_importance(pipe,X.loc[test],d.mpc_midpoint.loc[test],scoring="r2",n_repeats=10,random_state=SEED)
    imp=pd.DataFrame({"variable":allcols,"importance_mean":pi.importances_mean,"importance_sd":pi.importances_std}).sort_values("importance_mean",ascending=False); imp.to_csv(out/"formal_level_ml_importance.csv",index=False)
    top=[x for x in imp.variable if x in CONT][:3]
    if top:
      fig,axes=plt.subplots(1,len(top),figsize=(5*len(top),4)); PartialDependenceDisplay.from_estimator(pipe,X.loc[test],features=top,ax=np.atleast_1d(axes)); fig.tight_layout(); fig.savefig(figdir/"formal_level_partial_dependence.png",dpi=180); plt.close(fig)

def main(data,outdir):
    out=Path(outdir); figs=out/"figures"; out.mkdir(parents=True,exist_ok=True); figs.mkdir(exist_ok=True)
    d=prep(pd.read_stata(data,convert_categoricals=False)); variable_map(d,out); average_effects(d,out); hte=hte_scan(d,out); top_robustness(d,out); geography(d,out); individual_level_associations(d,out); focused_joint_medical(d,out); level=level_predictability(d,out,figs); level_explainability(d,out,figs); hte_ml(d,out,figs); food_nulls(d,out); ordered_top(d,out); randomization(d,out,2000)
    summary={"raw_N":len(d),"adult_N":int(d.sample_A.sum()),"clean_N":int(d.sample_C.sum()),"features":len(FEATURES),"formal_hte_rows":len(hte),"level_cv_rows":len(level),"ri_permutations":2000}
    (out/"formal_run_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); print(json.dumps(summary,indent=2))
if __name__=="__main__":
    p=ArgumentParser(); p.add_argument("data"); p.add_argument("--out",default="formal-output"); a=p.parse_args(); main(a.data,a.out)
