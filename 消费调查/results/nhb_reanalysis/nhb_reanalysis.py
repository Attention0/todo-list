"""Independent NHB reviewer re-analysis from respondent-level source data.

Only aggregate tables, figures, and reports are written. No respondent-level
records or out-of-fold predictions are saved.
"""
from __future__ import annotations

import argparse, hashlib, json, math, platform, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
SEED = 20260925
SEEDS = [20260925, 20260926, 20260927, 20260928, 20260929]
FORMS = ["cash", "food", "medical"]
SCEN = ["q32_cash200","q33_cash1k","q34_cash5k","q35_vouch200","q36_vouch1k","q37_vouch5k","q38_med200","q39_med1k","q40_med5k"]
TYPES = ["cash"]*3 + ["food"]*3 + ["medical"]*3
AMOUNTS = [200,1000,5000]*3
MID = {1:0,2:.05,3:.175,4:.375,5:.625,6:.875}
ALT = {**MID,6:1.0}
CONT = ["q42_age","q06_socsec","q07_emergfund","q09_gain","q10_effort","q11_mobility","q13_pressure","q15_fut_self","q17a_fut_econ","q17b_fut_job","q17c_fut_price","q17e_fut_welfare","q18_ses_now","q19_ses_past5","q20_ses_next1","q01_lifesat","q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q08_support","q12_voice","q16_fut_society","q17d_fut_fair","q21_order","q22_vitality"]
ORDERED = ["q43_edu","income_h","q28_hhsize","q29_foodexp","q30_medexp","q49_citytier"]
NOMINAL = ["q41_gender","q23_hukou","q24_workstat","q25_unittype","q26_housing","q27_minorchild","q31_gotsubsidy"]
FEATURES = CONT + ORDERED + NOMINAL

def prep(d):
    hit=d[SCEN].notna(); assert hit.sum(1).eq(1).all()
    d=d.copy(); d["cell"]=hit.values.argmax(1)+1
    d["transfer_type"]=d.cell.map(dict(enumerate(TYPES,1))); d["amount"]=d.cell.map(dict(enumerate(AMOUNTS,1)))
    d["outcome_ord"]=d[SCEN].bfill(axis=1).iloc[:,0].astype(int)
    assert d.outcome_ord.between(1,6).all() and (d.scen_amount.astype(int)==d.amount).all() and (d.scen_mpc.astype(int)==d.outcome_ord).all()
    d["mpc_midpoint"]=d.outcome_ord.map(MID); d["mpc_alt"]=d.outcome_ord.map(ALT)
    d["income_h"]=np.where(d.q46_income.between(11,16),d.q46_income-10,d.q46_income)
    items=["q01_lifesat","q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q06_socsec","q07_emergfund","q08_support","q09_gain","q10_effort","q11_mobility","q12_voice","q13_pressure"]
    x=d[items]; straight=x.nunique(1).eq(1)
    d["scale_sd"]=x.std(1); d["unique_n"]=x.nunique(1); d["extreme_share"]=x.isin([0,10]).mean(1)
    d["sample_A"]=d.q42_age.between(18,100)
    d["sample_C"]=d.sample_A & ~straight & ~d.id.duplicated(False)
    d["sample_Q1"]=d.sample_A & d.scale_sd.ge(1) & d.unique_n.ge(4)
    d["sample_Q2"]=d.sample_A & d.scale_sd.ge(1.5) & d.unique_n.ge(5) & d.extreme_share.le(.8)
    return d.reset_index(drop=True)

def preprocessor(cols=FEATURES):
    cats=[c for c in cols if c in NOMINAL+ORDERED]; nums=[c for c in cols if c not in cats]
    return ColumnTransformer([
        ("num",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),nums),
        ("cat",Pipeline([("imp",SimpleImputer(strategy="most_frequent")),("oh",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cats)])

def rf(seed, leaf=25, trees=180):
    return Pipeline([("pre",preprocessor()),("model",RandomForestRegressor(n_estimators=trees,min_samples_leaf=leaf,max_features=.5,n_jobs=-1,random_state=seed))])

def folds(d, seed):
    return list(StratifiedKFold(5,shuffle=True,random_state=seed).split(d,d.cell))

def samples(d):
    return {"R":np.ones(len(d),bool),"A":d.sample_A.to_numpy(),"C":d.sample_C.to_numpy(),"Q1":d.sample_Q1.to_numpy(),"Q2":d.sample_Q2.to_numpy()}

def metric(y,p):
    return {"spearman":stats.spearmanr(y,p).statistic,"pearson":stats.pearsonr(y,p).statistic,
            "target_centered_r2":1-np.sum((y-p)**2)/np.sum((y-y.mean())**2),"rmse":mean_squared_error(y,p)**.5}

def mean_effects(d,out):
    rows=[]
    for sn,mask in samples(d).items():
        z=d[mask]
        for y in ["outcome_ord","mpc_midpoint","mpc_alt"]:
            for amount in ["pooled",200,1000,5000]:
                a=z if amount=="pooled" else z[z.amount.eq(amount)]
                means=a.groupby("transfer_type")[y].mean()
                for t,c in [("food","cash"),("medical","cash"),("medical","food")]:
                    x=a[a.transfer_type.eq(t)][y]; q=a[a.transfer_type.eq(c)][y]
                    e=x.mean()-q.mean(); se=math.sqrt(x.var()/len(x)+q.var()/len(q)); p=2*stats.norm.sf(abs(e/se))
                    rows.append([sn,y,amount,f"{t}-{c}",e,se,e-1.96*se,e+1.96*se,p,len(a)])
    pd.DataFrame(rows,columns=["sample","outcome","amount","contrast","effect","se","lo","hi","p","N"]).to_csv(out/"mean_effects.csv",index=False)

def randomization_audit(d,out):
    rows=[]
    for v in FEATURES:
      x=d[[v,"cell"]].dropna()
      groups=[g[v].to_numpy() for _,g in x.groupby("cell")]
      if v in NOMINAL:
        tab=pd.crosstab(x[v],x.cell); stat,p,df,_=stats.chi2_contingency(tab); test="chi_square"
      else:
        stat,p=stats.f_oneway(*groups); df=8; test="anova"
      rows.append([v,test,len(x),d[v].isna().sum(),stat,df,p])
    z=pd.DataFrame(rows,columns=["variable","test","N","missing_N","statistic","df","p"])
    order=np.argsort(z.p.to_numpy()); q=np.empty(len(z)); vals=z.p.to_numpy()[order]*len(z)/np.arange(1,len(z)+1); vals=np.minimum.accumulate(vals[::-1])[::-1]; q[order]=np.minimum(vals,1); z["bh_q"]=q
    z.to_csv(out/"randomization_balance.csv",index=False)

def pooled_level_prediction(d,out):
    rows=[]; y=d.mpc_midpoint.to_numpy()
    for seed in SEEDS:
      pred=np.zeros(len(d))
      for k,(tr,te) in enumerate(folds(d,seed)):
        pp=preprocessor(); Xtr=pp.fit_transform(d.loc[tr,FEATURES]); Xte=pp.transform(d.loc[te,FEATURES])
        ftr=pd.get_dummies(d.loc[tr,"transfer_type"],dtype=float).reindex(columns=FORMS,fill_value=0).to_numpy()[:,1:]; fte=pd.get_dummies(d.loc[te,"transfer_type"],dtype=float).reindex(columns=FORMS,fill_value=0).to_numpy()[:,1:]
        atr=pd.get_dummies(d.loc[tr,"amount"],dtype=float).reindex(columns=[200,1000,5000],fill_value=0).to_numpy()[:,1:]; ate=pd.get_dummies(d.loc[te,"amount"],dtype=float).reindex(columns=[200,1000,5000],fill_value=0).to_numpy()[:,1:]
        model=RandomForestRegressor(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=seed+k).fit(np.c_[Xtr,ftr,atr],y[tr]); pred[te]=model.predict(np.c_[Xte,fte,ate])
      rows.append([seed,r2_score(y,pred),mean_squared_error(y,pred)**.5,stats.spearmanr(y,pred).statistic])
    pd.DataFrame(rows,columns=["seed","r2","rmse","spearman"]).to_csv(out/"pooled_level_prediction.csv",index=False)

def portability(d,out):
    rows=[]; saved={}
    for sn,mask in samples(d).items():
      dd=d[mask].reset_index(drop=True)
      for seed in SEEDS:
        pred={(s,t):np.full(len(dd),np.nan) for s in FORMS for t in FORMS}
        for k,(tr,te) in enumerate(folds(dd,seed)):
          for source in FORMS:
            tri=tr[dd.transfer_type.iloc[tr].eq(source).to_numpy()]
            model=rf(seed+k).fit(dd.loc[tri,FEATURES],dd.loc[tri,"mpc_midpoint"])
            for target in FORMS:
              ti=te[dd.transfer_type.iloc[te].eq(target).to_numpy()]
              pred[(source,target)][ti]=model.predict(dd.loc[ti,FEATURES])
        for (source,target),p in pred.items():
          ix=dd.transfer_type.eq(target).to_numpy(); assert np.isfinite(p[ix]).all()
          m=metric(dd.loc[ix,"mpc_midpoint"].to_numpy(),p[ix]); rows.append([sn,seed,source,target,len(dd.loc[ix]),*m.values()])
        if sn=="R" and seed==SEED: saved=(dd,pred)
    tab=pd.DataFrame(rows,columns=["sample","seed","source","target","N_target","spearman","pearson","target_centered_r2","rmse"])
    tab.to_csv(out/"portability_3x3_by_seed_sample.csv",index=False)
    av=tab.groupby(["sample","source","target"],as_index=False).agg(**{c:(c,"mean") for c in ["spearman","pearson","target_centered_r2","rmse"]})
    gaps=[]
    for _,r in av.iterrows():
        within=av[(av["sample"]==r["sample"])&(av.source==r.target)&(av.target==r.target)].iloc[0]
        gaps.append([r["sample"],r.source,r.target,r.spearman-within.spearman,
                     r.target_centered_r2-within.target_centered_r2,
                     r.spearman/within.spearman if abs(within.spearman)>.05 else np.nan])
    pd.DataFrame(gaps,columns=["sample","source","target","spearman_gap_vs_target_within","r2_gap_vs_target_within","spearman_ratio_vs_target_within"]).to_csv(out/"portability_target_normalized.csv",index=False)
    # Paired target-resampling CIs for key normalized gaps; predictions remain fully OOF.
    dd,pred=saved; rng=np.random.default_rng(SEED); br=[]
    for source,target in [("cash","food"),("cash","medical")]:
      ix=np.where(dd.transfer_type.eq(target))[0]; y=dd.mpc_midpoint.to_numpy(); vals=[]
      for _ in range(5000):
        b=rng.choice(ix,len(ix),replace=True)
        vals.append(stats.spearmanr(y[b],pred[(source,target)][b]).statistic-stats.spearmanr(y[b],pred[(target,target)][b]).statistic)
      obs=stats.spearmanr(y[ix],pred[(source,target)][ix]).statistic-stats.spearmanr(y[ix],pred[(target,target)][ix]).statistic
      lo,hi=np.quantile(vals,[.025,.975]); br.append([source,target,obs,lo,hi,5000,"paired target bootstrap; models fixed after OOF fitting"])
    pd.DataFrame(br,columns=["source","target","normalized_spearman_gap","lo","hi","B","method"]).to_csv(out/"portability_gap_uncertainty.csv",index=False)
    return tab

def portability_refit_bootstrap(d,out,B=100):
    """Headline source+target respondent bootstrap with full model refitting."""
    rng=np.random.default_rng(SEED); rows=[]; split=folds(d,SEED)
    for b in range(B):
      for target in ["food","medical"]:
        yc=[]; pc=[]; pw=[]
        for k,(tr,te) in enumerate(split):
          tr_cash=tr[d.transfer_type.iloc[tr].eq("cash").to_numpy()]
          tr_tar=tr[d.transfer_type.iloc[tr].eq(target).to_numpy()]
          te_tar=te[d.transfer_type.iloc[te].eq(target).to_numpy()]
          # Resample each randomized amount stratum in both training arms and target evaluation.
          def rs(ix):
            return np.concatenate([rng.choice(ix[d.amount.iloc[ix].eq(a).to_numpy()],sum(d.amount.iloc[ix].eq(a)),replace=True) for a in [200,1000,5000]])
          bc,bt,be=rs(tr_cash),rs(tr_tar),rs(te_tar)
          mc=rf(SEED+b+k,trees=120).fit(d.loc[bc,FEATURES],d.loc[bc,"mpc_midpoint"])
          mt=rf(SEED+b+k,trees=120).fit(d.loc[bt,FEATURES],d.loc[bt,"mpc_midpoint"])
          yc.extend(d.loc[be,"mpc_midpoint"]); pc.extend(mc.predict(d.loc[be,FEATURES])); pw.extend(mt.predict(d.loc[be,FEATURES]))
        gap=stats.spearmanr(yc,pc).statistic-stats.spearmanr(yc,pw).statistic
        rows.append([b,"cash",target,gap])
    z=pd.DataFrame(rows,columns=["bootstrap","source","target","normalized_spearman_gap"]); z.to_csv(out/"portability_refit_bootstrap_draws.csv",index=False)
    q=z.groupby(["source","target"]).normalized_spearman_gap.agg(point="mean",lo=lambda x:x.quantile(.025),hi=lambda x:x.quantile(.975)).reset_index(); q["B"]=B; q["trees"]=120; q["note"]="5-fold pipeline; source training and target training/evaluation resampled within amount; model refit each draw"
    q.to_csv(out/"portability_refit_bootstrap_summary.csv",index=False)

def invariance(d,out):
    rows=[]
    for sn,mask in samples(d).items():
      dd=d[mask].reset_index(drop=True); y=dd.mpc_midpoint.to_numpy()
      for seed in SEEDS:
        pa=np.zeros(len(dd)); pi=np.zeros(len(dd)); ps=np.zeros(len(dd)); pn=np.zeros(len(dd))
        for k,(tr,te) in enumerate(folds(dd,seed)):
          pp=preprocessor(); Xtr=pp.fit_transform(dd.loc[tr,FEATURES]); Xte=pp.transform(dd.loc[te,FEATURES])
          ftr=pd.get_dummies(dd.loc[tr,"transfer_type"],drop_first=True,dtype=float).reindex(columns=["food","medical"],fill_value=0).to_numpy()
          fte=pd.get_dummies(dd.loc[te,"transfer_type"],drop_first=True,dtype=float).reindex(columns=["food","medical"],fill_value=0).to_numpy()
          atr=pd.get_dummies(dd.loc[tr,"amount"],drop_first=True,dtype=float).reindex(columns=[1000,5000],fill_value=0).to_numpy()
          ate=pd.get_dummies(dd.loc[te,"amount"],drop_first=True,dtype=float).reindex(columns=[1000,5000],fill_value=0).to_numpy()
          base_tr=np.c_[Xtr,ftr,atr]; base_te=np.c_[Xte,fte,ate]
          int_tr=np.c_[base_tr,Xtr*ftr[:,[0]],Xtr*ftr[:,[1]]]; int_te=np.c_[base_te,Xte*fte[:,[0]],Xte*fte[:,[1]]]
          pa[te]=Ridge(alpha=10).fit(base_tr,y[tr]).predict(base_te)
          pi[te]=Ridge(alpha=10).fit(int_tr,y[tr]).predict(int_te)
          # Nonlinear common versus context-specific map.
          common=RandomForestRegressor(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=seed+k).fit(base_tr,y[tr]); pn[te]=common.predict(base_te)
          for form in FORMS:
            trf=tr[dd.transfer_type.iloc[tr].eq(form).to_numpy()]; tef=te[dd.transfer_type.iloc[te].eq(form).to_numpy()]
            loc_tr=np.isin(tr,trf); loc_te=np.isin(te,tef)
            xs_tr=np.c_[Xtr[loc_tr],atr[loc_tr]]; xs_te=np.c_[Xte[loc_te],ate[loc_te]]
            ps[tef]=RandomForestRegressor(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=seed+k).fit(xs_tr,y[trf]).predict(xs_te)
        for model,p in [("ridge_additive",pa),("ridge_form_interactions",pi),("rf_common",pn),("rf_form_specific",ps)]:
          rows.append([sn,seed,model,r2_score(y,p),mean_squared_error(y,p),len(dd)])
    z=pd.DataFrame(rows,columns=["sample","seed","model","r2","mse","N"]); z.to_csv(out/"direct_invariance_models.csv",index=False)
    wide=z.pivot(index=["sample","seed"],columns="model",values="r2").reset_index()
    wide["ridge_interaction_increment"]=wide.ridge_form_interactions-wide.ridge_additive
    wide["rf_specific_increment"]=wide.rf_form_specific-wide.rf_common
    wide.to_csv(out/"direct_invariance_increments.csv",index=False)

def invariance_paired_tests(d,out):
    """Paired respondent bootstrap of held-out loss increments, overall/by form."""
    y=d.mpc_midpoint.to_numpy(); pa=np.zeros(len(d)); pi=np.zeros(len(d)); pn=np.zeros(len(d)); ps=np.zeros(len(d))
    for k,(tr,te) in enumerate(folds(d,SEED)):
      pp=preprocessor(); Xtr=pp.fit_transform(d.loc[tr,FEATURES]); Xte=pp.transform(d.loc[te,FEATURES])
      ftr=pd.get_dummies(d.loc[tr,"transfer_type"],dtype=float).reindex(columns=FORMS,fill_value=0).to_numpy()[:,1:]
      fte=pd.get_dummies(d.loc[te,"transfer_type"],dtype=float).reindex(columns=FORMS,fill_value=0).to_numpy()[:,1:]
      atr=pd.get_dummies(d.loc[tr,"amount"],dtype=float).reindex(columns=[200,1000,5000],fill_value=0).to_numpy()[:,1:]
      ate=pd.get_dummies(d.loc[te,"amount"],dtype=float).reindex(columns=[200,1000,5000],fill_value=0).to_numpy()[:,1:]
      bt=np.c_[Xtr,ftr,atr]; be=np.c_[Xte,fte,ate]; it=np.c_[bt,Xtr*ftr[:,[0]],Xtr*ftr[:,[1]]]; ie=np.c_[be,Xte*fte[:,[0]],Xte*fte[:,[1]]]
      pa[te]=Ridge(alpha=10).fit(bt,y[tr]).predict(be); pi[te]=Ridge(alpha=10).fit(it,y[tr]).predict(ie)
      pn[te]=RandomForestRegressor(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=SEED+k).fit(bt,y[tr]).predict(be)
      for form in FORMS:
        a=tr[d.transfer_type.iloc[tr].eq(form).to_numpy()]; b=te[d.transfer_type.iloc[te].eq(form).to_numpy()]
        la=np.isin(tr,a); lb=np.isin(te,b); ps[b]=RandomForestRegressor(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=SEED+k).fit(np.c_[Xtr[la],atr[la]],y[a]).predict(np.c_[Xte[lb],ate[lb]])
    rng=np.random.default_rng(SEED); rows=[]
    for name,a,b in [("ridge_X_by_form",pa,pi),("rf_form_specific",pn,ps)]:
      loss=(y-a)**2-(y-b)**2
      for form in ["all"]+FORMS:
        ix=np.arange(len(d)) if form=="all" else np.where(d.transfer_type.eq(form))[0]
        vals=np.array([loss[rng.choice(ix,len(ix),replace=True)].mean() for _ in range(5000)])
        rows.append([name,form,loss[ix].mean(),*np.quantile(vals,[.025,.975]),(vals<=0).mean(),len(ix),5000])
    pd.DataFrame(rows,columns=["comparison","target","mse_reduction","lo","hi","bootstrap_p_one_sided","N","B"]).to_csv(out/"direct_invariance_paired_tests.csv",index=False)

def food_bounds(d,out):
    bounds={1:(0,500),2:(501,1000),3:(1001,2000),4:(2001,3000),5:(3001,5000),6:(5001,np.inf)}
    rows=[]; regs=[]
    for sn,mask in samples(d).items():
      x=d[mask & d.transfer_type.isin(["cash","food"]).to_numpy()].copy()
      x["lower6"]=x.q29_foodexp.map(lambda v:bounds[int(v)][0]*6); x["upper6"]=x.q29_foodexp.map(lambda v:bounds[int(v)][1]*6)
      x["strict_infra"]=x.amount.lt(x.lower6); x["possible_infra"]=x.amount.le(x.upper6)
      x["infra_class"]=np.select([x.strict_infra,~x.possible_infra],["strict_inframarginal","binding"],default="ambiguous")
      for amount in [200,1000,5000]:
        for cls,g in x[x.amount.eq(amount)].groupby("infra_class"):
          for y in ["outcome_ord","mpc_midpoint"]:
            a=g[g.transfer_type.eq("food")][y]; c=g[g.transfer_type.eq("cash")][y]
            if min(len(a),len(c))<2: continue
            e=a.mean()-c.mean(); se=math.sqrt(a.var()/len(a)+c.var()/len(c)); rows.append([sn,amount,cls,y,len(g),len(a),len(c),e,se,e-1.96*se,e+1.96*se])
      for y in ["outcome_ord","mpc_midpoint"]:
        m=smf.ols(f"{y}~C(transfer_type)*C(infra_class)+C(amount)",x).fit(cov_type="HC3")
        terms=[q for q in m.params.index if "C(transfer_type)" in q and "C(infra_class)" in q]
        if terms:
          test=m.wald_test_terms(skip_single=False).table
          key=[q for q in test.index if "C(transfer_type):C(infra_class)" in q][0]
          regs.append([sn,y,len(x),float(test.loc[key,"statistic"]),float(test.loc[key,"pvalue"]),len(terms)])
    pd.DataFrame(rows,columns=["sample","amount","classification","outcome","N","N_food","N_cash","food_minus_cash","se","lo","hi"]).to_csv(out/"food_inframarginality_cells.csv",index=False)
    pd.DataFrame(regs,columns=["sample","outcome","N","wald","p","df"]).to_csv(out/"food_inframarginality_interactions.csv",index=False)

def hte_one(dd,treated,seed):
    z=dd[dd.transfer_type.isin(["cash",treated])].reset_index(drop=True); y=z.mpc_midpoint.to_numpy(); w=z.transfer_type.eq(treated).astype(int).to_numpy()
    tau=np.zeros(len(z)); dr=np.zeros(len(z)); fold=np.zeros(len(z),int)
    for k,(tr,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=seed).split(z,z.cell)):
      fold[te]=k; pp=preprocessor(); Xtr=pp.fit_transform(z.loc[tr,FEATURES]); Xte=pp.transform(z.loc[te,FEATURES]); wt=w[tr]; yt=y[tr]
      kw=dict(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=seed+k)
      m1=RandomForestRegressor(**kw).fit(Xtr[wt==1],yt[wt==1]); m0=RandomForestRegressor(**kw).fit(Xtr[wt==0],yt[wt==0])
      mu1=m1.predict(Xte); mu0=m0.predict(Xte); tau[te]=mu1-mu0
      e=z.amount.iloc[te].map(z.iloc[tr].groupby("amount").apply(lambda g:(g.transfer_type==treated).mean())).to_numpy()
      dr[te]=mu1-mu0+w[te]*(y[te]-mu1)/e-(1-w[te])*(y[te]-mu0)/(1-e)
    tc=(tau-tau.mean())/tau.std(); X=pd.DataFrame({"dr":dr,"tc":tc,"amount":z.amount})
    blp=smf.ols("dr~tc+C(amount)",X).fit(cov_type="HC3")
    q=pd.qcut(tau,5,labels=False,duplicates="drop")+1; g=pd.DataFrame({"q":q,"dr":dr,"tau":tau,"amount":z.amount}).groupby("q").agg(N=("dr","size"),predicted=("tau","mean"),effect=("dr","mean"),se=("dr",lambda a:a.std()/len(a)**.5)).reset_index()
    top=g.iloc[-1].effect-g.iloc[0].effect; topse=math.sqrt(g.iloc[-1].se**2+g.iloc[0].se**2)
    am=smf.ols("dr~tc*C(amount)",X).fit(cov_type="HC3"); terms=[v for v in am.params.index if "tc:C(amount)" in v]
    R=np.zeros((len(terms),len(am.params))); names=list(am.params.index)
    for i,t in enumerate(terms): R[i,names.index(t)]=1
    aw=am.wald_test(R,scalar=True)
    ev=pd.DataFrame({"id":z.id.astype(str),"arm":z.transfer_type,"amount":z.amount,"dr":dr,"tc":tc,"q":q})
    return [blp.params.tc,blp.bse.tc,*blp.conf_int().loc["tc"],blp.pvalues.tc,top,topse,top-1.96*topse,top+1.96*topse,float(aw.statistic),float(aw.pvalue)],g,ev

def hte(d,out):
    rows=[]; gates=[]
    for sn,mask in samples(d).items():
      dd=d[mask].reset_index(drop=True)
      for seed in SEEDS:
        for t in ["food","medical"]:
          a,g,_=hte_one(dd,t,seed); rows.append([sn,seed,f"{t}-cash",*a]); g.insert(0,"contrast",f"{t}-cash"); g.insert(0,"seed",seed); g.insert(0,"sample",sn); gates.append(g)
    cols=["sample","seed","contrast","blp_slope","blp_se","blp_lo","blp_hi","blp_p","gates_top_bottom","gates_se","gates_lo","gates_hi","amount_wald","amount_p"]
    pd.DataFrame(rows,columns=cols).to_csv(out/"corrected_hte_validation.csv",index=False)
    pd.concat(gates).to_csv(out/"corrected_hte_gates.csv",index=False)

def hte_direct_comparison(d,out,B=2000):
    """Direct Medical-minus-Food validation difference; shared cash resampled jointly."""
    rng=np.random.default_rng(SEED); rows=[]
    for sn,mask in samples(d).items():
      dd=d[mask].reset_index(drop=True); _,_,ef=hte_one(dd,"food",SEED); _,_,em=hte_one(dd,"medical",SEED)
      def calc(e):
        X=pd.get_dummies(e[["tc","amount"]],columns=["amount"],drop_first=True,dtype=float); X=np.c_[np.ones(len(X)),X.to_numpy()]
        slope=np.linalg.lstsq(X,e.dr.to_numpy(),rcond=None)[0][1]
        gates=e.groupby("q").dr.mean(); return slope,gates.iloc[-1]-gates.iloc[0]
      obs=np.subtract(calc(em),calc(ef)); draws=[]
      cf=ef[ef.arm.eq("cash")]; tf=ef[ef.arm.eq("food")]; cm=em[em.arm.eq("cash")]; tm=em[em.arm.eq("medical")]; cfidx=cf.set_index("id",drop=False); cmidx=cm.set_index("id",drop=False); cash_ids=cf.id.to_numpy()
      # Shared cash IDs are drawn once and used in both contrast-specific score tables.
      for _ in range(B):
        ids=rng.choice(cash_ids,len(cash_ids),replace=True); bf=cfidx.loc[ids].reset_index(drop=True); bm=cmidx.loc[ids].reset_index(drop=True)
        ff=tf.iloc[rng.integers(0,len(tf),len(tf))]; mm=tm.iloc[rng.integers(0,len(tm),len(tm))]
        draws.append(np.subtract(calc(pd.concat([bm,mm])),calc(pd.concat([bf,ff]))))
      q=np.quantile(draws,[.025,.975],axis=0); draws=np.asarray(draws)
      rows += [[sn,"blp_slope",obs[0],q[0,0],q[1,0],2*min((draws[:,0]<=0).mean(),(draws[:,0]>=0).mean()),B],
               [sn,"gates_top_bottom",obs[1],q[0,1],q[1,1],2*min((draws[:,1]<=0).mean(),(draws[:,1]>=0).mean()),B]]
    pd.DataFrame(rows,columns=["sample","metric","medical_minus_food","lo","hi","bootstrap_p","B"]).to_csv(out/"corrected_hte_direct_comparison.csv",index=False)

def predictor_dictionary(out):
    meta=json.loads((out/"stata_metadata.json").read_text(encoding="utf-8"))["variable_labels"]
    fam={c:("continuous_scale" if c in CONT else "ordered" if c in ORDERED else "nominal") for c in FEATURES}
    pd.DataFrame([[c,meta.get(c,"derived household income band" if c=="income_h" else ""),fam[c]] for c in FEATURES],columns=["variable","exact_data_label","coding_family"]).to_csv(out/"predictor_dictionary.csv",index=False)

def figures(out):
    sns.set_theme(style="whitegrid"); figdir=out/"figures"; figdir.mkdir(exist_ok=True)
    p=pd.read_csv(out/"portability_3x3_by_seed_sample.csv"); p=p[p["sample"].eq("R")].groupby(["source","target"]).spearman.mean().unstack()
    fig,ax=plt.subplots(figsize=(6,5)); sns.heatmap(p.loc[FORMS,FORMS],annot=True,cmap="vlag",center=0,ax=ax); ax.set(title="Fully out-of-sample 3×3 rank portability"); fig.tight_layout(); fig.savefig(figdir/"fig_portability_3x3.png",dpi=220); plt.close(fig)
    h=pd.read_csv(out/"corrected_hte_validation.csv"); h=h[(h["sample"]=="R")].groupby("contrast").agg(est=("blp_slope","mean"),lo=("blp_lo","mean"),hi=("blp_hi","mean")).reset_index()
    fig,ax=plt.subplots(figsize=(6,4)); ax.errorbar(h.contrast,h.est,yerr=[h.est-h.lo,h.hi-h.est],fmt="o",capsize=4); ax.axhline(0,color="black",lw=.8); ax.set(ylabel="DR BLP slope",title="Corrected held-out HTE validation"); fig.tight_layout(); fig.savefig(figdir/"fig_corrected_hte.png",dpi=220); plt.close(fig)
    f=pd.read_csv(out/"food_inframarginality_cells.csv"); f=f[(f["sample"]=="R")&(f.outcome=="outcome_ord")]
    fig,ax=plt.subplots(figsize=(8,4)); sns.pointplot(f,x="amount",y="food_minus_cash",hue="classification",ax=ax); ax.axhline(0,color="black",lw=.8); ax.set(ylabel="Food minus cash (ordinal)",title="Food-voucher effect by spending-bound classification"); fig.tight_layout(); fig.savefig(figdir/"fig_food_inframarginality.png",dpi=220); plt.close(fig)

def main(data,outdir):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    d=prep(pd.read_stata(data,convert_categoricals=False))
    d.groupby(["transfer_type","amount"]).size().rename("N").reset_index().to_csv(out/"sample_cells.csv",index=False)
    pd.DataFrame([[k,int(v.sum())] for k,v in samples(d).items()],columns=["sample","N"]).to_csv(out/"sample_definitions.csv",index=False)
    mean_effects(d,out); randomization_audit(d,out); pooled_level_prediction(d,out); portability(d,out); portability_refit_bootstrap(d,out); invariance(d,out); invariance_paired_tests(d,out); food_bounds(d,out); hte(d,out); hte_direct_comparison(d,out); predictor_dictionary(out); figures(out)
    versions={"python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__}
    summary={"raw_N":len(d),"adult_N":int(d.sample_A.sum()),"clean_N":int(d.sample_C.sum()),"seeds":SEEDS,"folds":5,"data_sha256":hashlib.sha256(Path(data).read_bytes()).hexdigest(),"versions":versions}
    (out/"run_manifest.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("data"); ap.add_argument("--out",required=True); a=ap.parse_args(); main(a.data,a.out)
