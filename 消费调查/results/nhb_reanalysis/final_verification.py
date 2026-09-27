"""Locked five-part final verification for the NHB re-analysis.

Writes aggregate outputs only. No respondent rows or predictions are saved.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import nhb_reanalysis as core

SEED=20260927
SEEDS=[20260927,20260928,20260929,20260930,20261001]
FORMS=core.FORMS
SUBJECTIVE=[x for x in core.CONT if x!="q42_age"]

def strict_inframarginal(d,out):
    lower={1:0,2:501,3:1001,4:2001,5:3001,6:5001}
    z=d[d.transfer_type.isin(["cash","food"])].copy()
    z["lower6"]=z.q29_foodexp.map(lower)*6
    z=z[z.amount.lt(z.lower6)].copy(); z["food"]=z.transfer_type.eq("food").astype(int)
    rows=[]
    for sample,mask in core.samples(z).items():
      x=z[mask]
      for y in ["outcome_ord","mpc_midpoint"]:
        m=smf.ols(f"{y}~food+C(amount)",x).fit(cov_type="HC3")
        rows.append([sample,y,len(x),int(x.food.sum()),int((1-x.food).sum()),m.params.food,m.bse.food,*m.conf_int().loc["food"],m.pvalues.food])
    pd.DataFrame(rows,columns=["sample","outcome","N","N_food","N_cash","food_minus_cash","se","lo","hi","p"]).to_csv(out/"final_strict_inframarginal_pooled.csv",index=False)

def _rf(seed,trees=120):
    return core.rf(seed,trees=trees).set_params(model__n_jobs=1)

def refit_draw(d,split,b):
    rng=np.random.default_rng(SEED+b); vals={}
    ys={t:[] for t in ["food","medical"]}; pc={t:[] for t in ys}; pw={t:[] for t in ys}
    for k,(tr,te) in enumerate(split):
      def rs(ix):
        return np.concatenate([rng.choice(ix[d.amount.iloc[ix].eq(a).to_numpy()],sum(d.amount.iloc[ix].eq(a)),replace=True) for a in [200,1000,5000]])
      train={f:rs(tr[d.transfer_type.iloc[tr].eq(f).to_numpy()]) for f in FORMS}
      models={f:_rf(SEED+b+k).fit(d.loc[train[f],core.FEATURES],d.loc[train[f],"mpc_midpoint"]) for f in FORMS}
      for target in ["food","medical"]:
        ev=rs(te[d.transfer_type.iloc[te].eq(target).to_numpy()]); ys[target].extend(d.loc[ev,"mpc_midpoint"])
        pc[target].extend(models["cash"].predict(d.loc[ev,core.FEATURES])); pw[target].extend(models[target].predict(d.loc[ev,core.FEATURES]))
    for target in ys:
      vals[target]=stats.spearmanr(ys[target],pc[target]).statistic-stats.spearmanr(ys[target],pw[target]).statistic
    return b,vals["food"],vals["medical"]

def refit_bootstrap_1000(d,out,B=1000,jobs=-1):
    split=core.folds(d,SEED)
    draws=Parallel(n_jobs=jobs,verbose=10)(delayed(refit_draw)(d,split,b) for b in range(B))
    z=pd.DataFrame(draws,columns=["bootstrap","cash_to_food_gap","cash_to_medical_gap"])
    rows=[]
    for target,col in [("food","cash_to_food_gap"),("medical","cash_to_medical_gap")]:
      x=z[col]; rows.append(["cash",target,x.mean(),x.quantile(.025),x.quantile(.975),B,120,"full model refit; source training, target training and target evaluation resampled within amount"])
    pd.DataFrame(rows,columns=["source","target","point","lo","hi","B","trees","method"]).to_csv(out/"final_portability_refit_bootstrap_1000.csv",index=False)
    # Only aggregate quantiles are retained; respondent-level predictions and draw-level results are not written.

def prediction_matrix(d,seed,include_amount=False,outcome="mpc_midpoint"):
    pred={(s,t):np.full(len(d),np.nan) for s in FORMS for t in FORMS}
    for k,(tr,te) in enumerate(core.folds(d,seed)):
      for source in FORMS:
        a=tr[d.transfer_type.iloc[tr].eq(source).to_numpy()]
        if include_amount:
          pp=core.preprocessor(); xa=pp.fit_transform(d.loc[a,core.FEATURES]); amount_a=pd.get_dummies(d.loc[a,"amount"],dtype=float).reindex(columns=[200,1000,5000],fill_value=0).to_numpy()
          model=RandomForestRegressor(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=seed+k).fit(np.c_[xa,amount_a],d.loc[a,outcome])
        else: model=core.rf(seed+k).fit(d.loc[a,core.FEATURES],d.loc[a,outcome])
        for target in FORMS:
          b=te[d.transfer_type.iloc[te].eq(target).to_numpy()]
          if include_amount:
            xb=pp.transform(d.loc[b,core.FEATURES]); amount_b=pd.get_dummies(d.loc[b,"amount"],dtype=float).reindex(columns=[200,1000,5000],fill_value=0).to_numpy(); pred[(source,target)][b]=model.predict(np.c_[xb,amount_b])
          else: pred[(source,target)][b]=model.predict(d.loc[b,core.FEATURES])
    return pred

def portability_extensions(d,out):
    rows=[]
    for outcome,adjust in [("mpc_midpoint",True),("outcome_ord",False)]:
      for seed in SEEDS:
        pred=prediction_matrix(d,seed,adjust,outcome)
        for (s,t),p in pred.items():
          ix=d.transfer_type.eq(t).to_numpy(); y=d.loc[ix,outcome].to_numpy(); q=p[ix]
          if adjust:
            # Partial out target amount means from both outcome and prediction.
            amt=d.loc[ix,"amount"].to_numpy(); yr=y.copy(); qr=q.copy()
            for a in [200,1000,5000]:
              aa=amt==a; yr[aa]-=yr[aa].mean(); qr[aa]-=qr[aa].mean()
            met=core.metric(yr,qr)
          else: met=core.metric(y,q)
          rows.append(["amount_adjusted" if adjust else "ordinal",outcome,"all",seed,s,t,len(y),*met.values()])
    # By-amount matrices, with folds stratified by form and diagonal fully OOS.
    for amount in [200,1000,5000]:
      z=d[d.amount.eq(amount)].reset_index(drop=True)
      for seed in SEEDS:
        cv=list(StratifiedKFold(5,shuffle=True,random_state=seed).split(z,z.transfer_type))
        pred={(s,t):np.full(len(z),np.nan) for s in FORMS for t in FORMS}
        for k,(tr,te) in enumerate(cv):
          for s in FORMS:
            a=tr[z.transfer_type.iloc[tr].eq(s).to_numpy()]; model=core.rf(seed+k).fit(z.loc[a,core.FEATURES],z.loc[a,"mpc_midpoint"])
            for t in FORMS:
              b=te[z.transfer_type.iloc[te].eq(t).to_numpy()]; pred[(s,t)][b]=model.predict(z.loc[b,core.FEATURES])
        for (s,t),q in pred.items():
          ix=z.transfer_type.eq(t).to_numpy(); met=core.metric(z.loc[ix,"mpc_midpoint"].to_numpy(),q[ix]); rows.append(["by_amount","mpc_midpoint",amount,seed,s,t,int(ix.sum()),*met.values()])
    tab=pd.DataFrame(rows,columns=["specification","outcome","amount","seed","source","target","N_target","spearman","pearson","target_centered_r2","rmse"])
    tab.to_csv(out/"final_portability_amount_ordinal.csv",index=False)
    avg=tab.groupby(["specification","outcome","amount","source","target"],as_index=False)[["spearman","pearson","target_centered_r2","rmse"]].mean()
    gaps=[]
    for _,r in avg.iterrows():
      w=avg[(avg.specification==r.specification)&(avg.outcome==r.outcome)&(avg.amount.astype(str)==str(r.amount))&(avg.source==r.target)&(avg.target==r.target)].iloc[0]
      gaps.append([r.specification,r.outcome,r.amount,r.source,r.target,r.spearman-w.spearman,r.target_centered_r2-w.target_centered_r2])
    pd.DataFrame(gaps,columns=["specification","outcome","amount","source","target","spearman_gap_vs_target_within","r2_gap_vs_target_within"]).to_csv(out/"final_portability_amount_ordinal_gaps.csv",index=False)

def heldout_person_score(d,out):
    rows=[]
    for seed in SEEDS:
      for learner in ["ridge","random_forest"]:
        score=np.zeros(len(d)); y=d.mpc_midpoint.to_numpy()
        for k,(tr,te) in enumerate(core.folds(d,seed)):
          # Training-only cell means remove randomized form×amount levels before learning a person score.
          means=d.iloc[tr].groupby("cell").mpc_midpoint.mean(); residual=y[tr]-d.cell.iloc[tr].map(means).to_numpy()
          pp=core.preprocessor(); xt=pp.fit_transform(d.loc[tr,core.FEATURES]); xe=pp.transform(d.loc[te,core.FEATURES])
          model=Ridge(alpha=10) if learner=="ridge" else RandomForestRegressor(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=seed+k)
          score[te]=model.fit(xt,residual).predict(xe)
        s=(score-score.mean())/score.std(); z=d.copy(); z["person_score"]=s
        for outcome in ["mpc_midpoint","outcome_ord"]:
          m=smf.ols(f"{outcome}~person_score*C(transfer_type)+C(amount)+C(transfer_type):C(amount)",z).fit(cov_type="HC3")
          names=list(m.params.index); terms=["person_score:C(transfer_type)[T.food]","person_score:C(transfer_type)[T.medical]"]
          vals=[]
          for term in terms:
            vals += [m.params[term],m.bse[term],*m.conf_int().loc[term],m.pvalues[term]]
          R=np.zeros((2,len(names))); R[0,names.index(terms[0])]=1; R[1,names.index(terms[1])]=1; w=m.wald_test(R,scalar=True)
          rows.append([seed,learner,outcome,len(z),*vals,float(w.statistic),float(w.pvalue),r2_score_safe(z[outcome],m.fittedvalues)])
    cols=["seed","learner","outcome","N","food_score_interaction","food_se","food_lo","food_hi","food_p","medical_score_interaction","medical_se","medical_lo","medical_hi","medical_p","joint_wald","joint_p","in_sample_regression_r2"]
    pd.DataFrame(rows,columns=cols).to_csv(out/"final_heldout_person_score_invariance.csv",index=False)

def r2_score_safe(y,p): return 1-np.sum((np.asarray(y)-np.asarray(p))**2)/np.sum((np.asarray(y)-np.mean(y))**2)

def alpha(x):
    x=np.asarray(x,float); k=x.shape[1]; return k/(k-1)*(1-np.var(x,axis=0,ddof=1).sum()/np.var(x.sum(1),ddof=1))

def subjective_diagnostics(d,out):
    x=d[SUBJECTIVE].astype(float)
    x.corr().to_csv(out/"final_subjective_correlation.csv")
    z=StandardScaler().fit_transform(x); p=PCA().fit(z); load=p.components_.T*np.sqrt(p.explained_variance_)
    eig=pd.DataFrame({"component":np.arange(1,len(SUBJECTIVE)+1),"eigenvalue":p.explained_variance_,"variance_share":p.explained_variance_ratio_,"cumulative_variance":np.cumsum(p.explained_variance_ratio_)})
    eig.to_csv(out/"final_subjective_pca_eigenvalues.csv",index=False)
    pd.DataFrame(load,index=SUBJECTIVE,columns=[f"PC{i}" for i in range(1,len(SUBJECTIVE)+1)]).reset_index(names="item").to_csv(out/"final_subjective_pca_loadings.csv",index=False)
    # Overall alpha plus transparent content group diagnostics.
    domains={"all_subjective":SUBJECTIVE,"expectations":["q15_fut_self","q16_fut_society","q17a_fut_econ","q17b_fut_job","q17c_fut_price","q17d_fut_fair","q17e_fut_welfare","q20_ses_next1"],"fairness_trust":["q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q12_voice"],"security_resources":["q06_socsec","q07_emergfund","q08_support","q13_pressure"],"status_mobility":["q09_gain","q10_effort","q11_mobility","q18_ses_now","q19_ses_past5"]}
    pd.DataFrame([[k,len(v),alpha(d[v])] for k,v in domains.items()],columns=["scale","items","cronbach_alpha"]).to_csv(out/"final_subjective_cronbach_alpha.csv",index=False)

def final_figures(out):
    sns.set_theme(style="whitegrid"); figs=out/"figures"; figs.mkdir(exist_ok=True)
    b=pd.read_csv(out/"final_portability_refit_bootstrap_1000.csv"); fig,ax=plt.subplots(figsize=(6,4)); y=np.arange(len(b)); ax.errorbar(b.point,y,xerr=[b.point-b.lo,b.hi-b.point],fmt="o",capsize=4); ax.axvline(0,color="black",lw=.8); ax.set(yticks=y,yticklabels=[f"Cash→{x.title()}" for x in b.target],xlabel="Target-normalized Spearman gap",title="1,000-draw model-refit bootstrap"); fig.tight_layout(); fig.savefig(figs/"final_verification_refit_bootstrap.png",dpi=220); plt.close(fig)
    g=pd.read_csv(out/"final_portability_amount_ordinal_gaps.csv"); g=g[(g.specification=="by_amount")&(g.source=="cash")&g.target.isin(["food","medical"])]; fig,ax=plt.subplots(figsize=(7,4)); sns.pointplot(g,x="amount",y="spearman_gap_vs_target_within",hue="target",ax=ax); ax.axhline(0,color="black",lw=.8); ax.set(ylabel="Target-normalized Spearman gap",xlabel="Transfer amount (RMB)",title="Cash-model portability by amount"); fig.tight_layout(); fig.savefig(figs/"final_verification_by_amount.png",dpi=220); plt.close(fig)
    h=pd.read_csv(out/"final_heldout_person_score_invariance.csv"); h=h[(h.learner=="random_forest")&(h.outcome=="mpc_midpoint")]; fig,ax=plt.subplots(figsize=(7,4)); long=pd.concat([h[["seed","food_score_interaction"]].rename(columns={"food_score_interaction":"interaction"}).assign(form="Food"),h[["seed","medical_score_interaction"]].rename(columns={"medical_score_interaction":"interaction"}).assign(form="Medical")]); sns.pointplot(long,x="form",y="interaction",errorbar=("pi",100),ax=ax); ax.axhline(0,color="black",lw=.8); ax.set(ylabel="Held-out score × form coefficient",xlabel="",title="Person-score invariance across five folds/seeds"); fig.tight_layout(); fig.savefig(figs/"final_verification_person_score.png",dpi=220); plt.close(fig)
    e=pd.read_csv(out/"final_subjective_pca_eigenvalues.csv"); fig,ax=plt.subplots(figsize=(7,4)); ax.plot(e.component,e.eigenvalue,marker="o"); ax.axhline(1,color="black",ls="--",lw=.8); ax.set(xlabel="Principal component",ylabel="Eigenvalue",title="Subjective-item PCA scree plot"); fig.tight_layout(); fig.savefig(figs/"final_verification_subjective_pca.png",dpi=220); plt.close(fig)

def main(data,outdir,bootstrap=1000,jobs=-1):
    out=Path(outdir); out.mkdir(parents=True,exist_ok=True); d=core.prep(pd.read_stata(data,convert_categoricals=False))
    strict_inframarginal(d,out); refit_bootstrap_1000(d,out,bootstrap,jobs); portability_extensions(d,out); heldout_person_score(d,out); subjective_diagnostics(d,out); final_figures(out)
    (out/"final_verification_manifest.json").write_text(json.dumps({"seed":SEED,"seeds":SEEDS,"bootstrap":bootstrap,"folds":5,"rf_trees_primary":180,"rf_trees_bootstrap":120,"subjective_items":len(SUBJECTIVE)},indent=2),encoding="utf-8")

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("data"); ap.add_argument("--out",required=True); ap.add_argument("--bootstrap",type=int,default=1000); ap.add_argument("--jobs",type=int,default=-1); a=ap.parse_args(); main(a.data,a.out,a.bootstrap,a.jobs)
