"""Final trait-vs-context exploration. Writes aggregate outputs only."""
from argparse import ArgumentParser
from pathlib import Path
import sys,json,math,warnings
import numpy as np,pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold,RepeatedKFold,GridSearchCV
from sklearn.linear_model import Ridge,ElasticNet
from sklearn.ensemble import RandomForestRegressor,HistGradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier,export_text
from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error,silhouette_score
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.inspection import permutation_importance
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0,str(Path(__file__).resolve().parent)); import heterogeneity_formal as hf
warnings.filterwarnings("ignore"); SEED=20260921
FORMS=["cash","food","medical"]
SUBJ_DOMAINS={
 "subjective_economic":["q06_socsec","q07_emergfund","q09_gain","q10_effort","q11_mobility","q13_pressure","q15_fut_self","q17a_fut_econ","q17b_fut_job","q17c_fut_price","q17e_fut_welfare","q18_ses_now","q19_ses_past5","q20_ses_next1"],
 "social_confidence":["q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q08_support","q12_voice","q17d_fut_fair","q21_order","q22_vitality"],
 "wellbeing_optimism":["q01_lifesat","q15_fut_self","q16_fut_society","q17a_fut_econ","q20_ses_next1"]}

def pre(cols):
    cats=[x for x in cols if x in hf.NOMINAL+hf.ORDERED]; nums=[x for x in cols if x not in cats]
    return ColumnTransformer([("num",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),nums),("cat",Pipeline([("imp",SimpleImputer(strategy="most_frequent")),("oh",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cats)])
def model(kind):
    if kind=="ridge": return Ridge(alpha=10)
    if kind=="elastic_net": return ElasticNet(alpha=.01,l1_ratio=.1,max_iter=10000)
    if kind=="rf": return RandomForestRegressor(n_estimators=180,min_samples_leaf=20,max_features=.5,n_jobs=-1,random_state=SEED)
    return HistGradientBoostingRegressor(max_iter=120,max_leaf_nodes=15,l2_regularization=3,random_state=SEED)
def design(df,cols):
    x=df[cols].copy(); x["amount_cat"]=df.amount.astype(str); return x,cols+["amount_cat"]
def pipe_for(cols,kind):
    # amount is categorical and appended to the formal feature list locally.
    cats=[x for x in cols if x in hf.NOMINAL+hf.ORDERED or x=="amount_cat"]; nums=[x for x in cols if x not in cats]
    pp=ColumnTransformer([("num",Pipeline([("imp",SimpleImputer(strategy="median")),("sc",StandardScaler())]),nums),("cat",Pipeline([("imp",SimpleImputer(strategy="most_frequent")),("oh",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cats)])
    return Pipeline([("pre",pp),("model",model(kind))])

def form_predictions(d,out):
    rows=[]; pred=np.full((len(d),3),np.nan); fold=np.full(len(d),-1); cv=StratifiedKFold(5,shuffle=True,random_state=SEED)
    # Common global folds preserve all nine cells. Each form model predicts every held-out respondent.
    for k,(tr,te) in enumerate(cv.split(d,d.cell)):
      fold[te]=k
      for j,t in enumerate(FORMS):
        train=d.iloc[tr]; train=train[train.transfer_type.eq(t)]; Xtr,cols=design(train,hf.FEATURES); Xte,_=design(d.iloc[te],hf.FEATURES)
        p=pipe_for(cols,"rf").fit(Xtr,train.mpc_midpoint); pred[te,j]=p.predict(Xte)
    d2=d.copy();
    for j,t in enumerate(FORMS):d2["mu_"+t]=pred[:,j]
    d2["shared"]=pred.mean(1)
    for t in FORMS:d2["dev_"+t]=d2["mu_"+t]-d2.shared
    dec=[["actual_outcome",d2.mpc_midpoint.var()],["shared_prediction",d2.shared.var()]]+[["deviation_"+t,d2["dev_"+t].var()] for t in FORMS]
    pd.DataFrame(dec,columns=["component","variance"]).to_csv(out/"final_shared_specific_decomposition.csv",index=False)
    # Form-specific observed predictive performance, identical folds and model families.
    for t in FORMS:
      dd=d[d.transfer_type.eq(t)].copy(); cvf=RepeatedKFold(n_splits=5,n_repeats=2,random_state=SEED)
      for kind in ["ridge","elastic_net","rf","hgb"]:
       X,cols=design(dd,hf.FEATURES)
       for k,(tr,te) in enumerate(cvf.split(dd)):
        p=pipe_for(cols,kind).fit(X.iloc[tr],dd.mpc_midpoint.iloc[tr]); yhat=p.predict(X.iloc[te]); y=dd.mpc_midpoint.iloc[te]
        rows.append([t,kind,k,r2_score(y,yhat),math.sqrt(mean_squared_error(y,yhat)),mean_absolute_error(y,yhat)])
    pd.DataFrame(rows,columns=["form","model","fold","r2","rmse","mae"]).to_csv(out/"final_form_specific_prediction.csv",index=False)
    return d2,fold

def cross_form_transfer(d,out):
    rows=[]
    for source in FORMS:
      a=d[d.transfer_type.eq(source)]; Xa,cols=design(a,hf.FEATURES); p=pipe_for(cols,"rf").fit(Xa,a.mpc_midpoint)
      for target in FORMS:
       if source==target:continue
       b=d[d.transfer_type.eq(target)]; Xb,_=design(b,hf.FEATURES); raw=p.predict(Xb); rec=raw-raw.mean()+b.mpc_midpoint.mean(); slope=smf.ols("y~p",pd.DataFrame({"y":b.mpc_midpoint,"p":raw})).fit().params["p"]
       rows.append([source,target,stats.spearmanr(raw,b.mpc_midpoint).statistic,r2_score(b.mpc_midpoint,rec),slope,len(b)])
    pd.DataFrame(rows,columns=["train_form","test_form","spearman","recentered_r2","calibration_slope","N_test"]).to_csv(out/"final_cross_form_transfer.csv",index=False)

def coefficient_alignment(d,out,B=300):
    sets={"O_needs":hf.OBJECTIVE+hf.NEEDS,"S":hf.SUBJECTIVE,"A":hf.ATTITUDES,"ALL":hf.FEATURES}; rows=[]; rng=np.random.default_rng(SEED)
    for sn,cols0 in sets.items():
      # Fixed full-sample encoding makes coefficient vectors comparable across forms.
      Xraw=d[cols0].copy(); cats=[x for x in cols0 if x in hf.NOMINAL+hf.ORDERED]; X=pd.get_dummies(Xraw,columns=cats,drop_first=False,dtype=float); X=(X-X.mean())/X.std().replace(0,1); X=X.fillna(0); names=list(X.columns)
      def coefs(ix,t):
       z=ix[d.transfer_type.iloc[ix].eq(t).to_numpy()]; m=Ridge(alpha=10).fit(X.iloc[z],d.mpc_midpoint.iloc[z]); return m.coef_
      base={t:coefs(np.arange(len(d)),t) for t in FORMS}
      for a,b in [("cash","food"),("cash","medical"),("food","medical")]:
       x,y=base[a],base[b]; cor=np.corrcoef(x,y)[0,1]; cos=np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)); sign=(np.sign(x)==np.sign(y)).mean(); boots=[]
       for _ in range(B):
        ix=rng.integers(0,len(d),len(d)); xx,yy=coefs(ix,a),coefs(ix,b); boots.append([np.corrcoef(xx,yy)[0,1],np.dot(xx,yy)/(np.linalg.norm(xx)*np.linalg.norm(yy))])
       q=np.quantile(boots,[.025,.975],axis=0); rows.append([sn,a,b,cor,q[0,0],q[1,0],cos,q[0,1],q[1,1],sign,len(names)])
    pd.DataFrame(rows,columns=["feature_set","form1","form2","coef_correlation","corr_lo","corr_hi","cosine","cos_lo","cos_hi","sign_agreement","coefficients"]).to_csv(out/"final_predictor_alignment.csv",index=False)

def known_propensity(dd):
    # Pairwise treatment probability conditional on randomized amount.
    return dd.amount.map(dd.groupby("amount").W.mean()).to_numpy()
def encode_fold(train,test,cols):
    pp=pre(cols); a=pp.fit_transform(train[cols]); b=pp.transform(test[cols]); return np.asarray(a),np.asarray(b)
def standard_hte(d,treated,control,cols,method):
    dd=d[d.transfer_type.isin([treated,control])].reset_index(drop=True).copy(); dd["W"]=dd.transfer_type.eq(treated).astype(int); Y=dd.mpc_midpoint.to_numpy(); W=dd.W.to_numpy(); e=known_propensity(dd); tau=np.zeros(len(dd)); outer=StratifiedKFold(5,shuffle=True,random_state=SEED)
    for k,(tr,te) in enumerate(outer.split(dd,dd.cell)):
      Xtr,Xte=encode_fold(dd.iloc[tr],dd.iloc[te],cols); atr=pd.get_dummies(dd.amount.iloc[tr],drop_first=False,dtype=float).to_numpy(); ate=pd.get_dummies(dd.amount.iloc[te],drop_first=False,dtype=float).to_numpy(); Xtr=np.c_[Xtr,atr]; Xte=np.c_[Xte,ate]; wt=W[tr]; yt=Y[tr]; et=e[tr]
      if method=="t":
       kw=dict(n_estimators=180,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=SEED+k); m1=RandomForestRegressor(**kw).fit(Xtr[wt==1],yt[wt==1]); m0=RandomForestRegressor(**kw).fit(Xtr[wt==0],yt[wt==0]); tau[te]=m1.predict(Xte)-m0.predict(Xte); continue
      inn=StratifiedKFold(3,shuffle=True,random_state=SEED+k); mu=np.zeros(len(tr)); mu1=np.zeros(len(tr)); mu0=np.zeros(len(tr))
      for a,b in inn.split(Xtr,dd.cell.iloc[tr]):
       if method=="dr":
        q1=HistGradientBoostingRegressor(max_iter=100,min_samples_leaf=25,l2_regularization=3,random_state=k).fit(Xtr[a][wt[a]==1],yt[a][wt[a]==1]); q0=HistGradientBoostingRegressor(max_iter=100,min_samples_leaf=25,l2_regularization=3,random_state=k).fit(Xtr[a][wt[a]==0],yt[a][wt[a]==0]); mu1[b]=q1.predict(Xtr[b]); mu0[b]=q0.predict(Xtr[b])
       else:
        q=HistGradientBoostingRegressor(max_iter=100,min_samples_leaf=25,l2_regularization=3,random_state=k).fit(Xtr[a],yt[a]); mu[b]=q.predict(Xtr[b])
      if method=="dr": pseudo=mu1-mu0+wt*(yt-mu1)/et-(1-wt)*(yt-mu0)/(1-et); learner=RandomForestRegressor(n_estimators=180,min_samples_leaf=30,max_features=.5,n_jobs=-1,random_state=SEED+k).fit(Xtr,pseudo)
      else:
       wy=wt-et; pseudo=(yt-mu)/wy; learner=RandomForestRegressor(n_estimators=180,min_samples_leaf=30,max_features=.5,n_jobs=-1,random_state=SEED+k).fit(Xtr,pseudo,sample_weight=wy**2)
      tau[te]=learner.predict(Xte)
    dd["tau"]=tau; dd["tc"]=tau-tau.mean(); dd["q"]=pd.qcut(tau,5,labels=False,duplicates="drop")+1; blp=smf.ols("mpc_midpoint~W+tc+W:tc+C(amount)",dd).fit(cov_type="HC1"); b=blp.params["W:tc"]; se=blp.bse["W:tc"]
    gs=[]
    for q,g in dd.groupby("q"):
     a=g[g.W.eq(1)].mpc_midpoint; c=g[g.W.eq(0)].mpc_midpoint; eff=a.mean()-c.mean(); s=math.sqrt(a.var()/len(a)+c.var()/len(c)); gs.append([q,len(g),len(a),len(c),eff,s,eff-1.96*s,eff+1.96*s,g.tau.mean()])
    g=pd.DataFrame(gs,columns=["quintile","N","treated_N","control_N","effect","se","lo","hi","predicted"]); sep=g.iloc[-1].effect-g.iloc[0].effect; ss=math.sqrt(g.iloc[-1].se**2+g.iloc[0].se**2)
    return dd,[b,se,b-1.96*se,b+1.96*se,blp.pvalues["W:tc"]],[sep,ss,sep-1.96*ss,sep+1.96*ss],g

def hte_suite(d,out):
    summary=[]; groups=[]; feature_sets={"O":hf.OBJECTIVE,"O_needs":hf.OBJECTIVE+hf.NEEDS,"S":hf.SUBJECTIVE,"A":hf.ATTITUDES,"ALL":hf.FEATURES}
    for cname,t,c in [("food-cash","food","cash"),("medical-cash","medical","cash"),("medical-food","medical","food")]:
      for fs,cols in feature_sets.items():
       for method in (["t","dr","r"] if fs=="ALL" else ["dr"]):
        dd,cal,sep,g=standard_hte(d,t,c,cols,method); summary.append([cname,fs,method,*cal,*sep]); g.insert(0,"method",method); g.insert(0,"feature_set",fs); g.insert(0,"contrast",cname); groups.append(g)
    pd.DataFrame(summary,columns=["contrast","feature_set","learner","calibration","cal_se","cal_lo","cal_hi","cal_p","top_bottom","tb_se","tb_lo","tb_hi"]).to_csv(out/"final_standard_hte.csv",index=False)
    pd.concat(groups).to_csv(out/"final_standard_hte_quintiles.csv",index=False)

def paired_increment(d,out):
    f=Path(__file__).resolve().parents[1]/"tables"/"formal_level_ml_cv.csv"; f=f if f.exists() else None
    tab=pd.read_csv(f) if f else pd.DataFrame(); z=tab[tab.model.eq("random_forest")].pivot(index="fold",columns="feature_set",values="r2"); rng=np.random.default_rng(SEED); rows=[]
    for a,b in [("O","O+S"),("O","O+A"),("O","ALL")]:
      v=(z[b]-z[a]).to_numpy(); boots=[rng.choice(v,len(v),replace=True).mean() for _ in range(10000)]; lo,hi=np.quantile(boots,[.025,.975]); rows.append([a,b,v.mean(),lo,hi,hi<.01,hi<.02])
    pd.DataFrame(rows,columns=["base","expanded","mean_delta_r2","lo","hi","rules_out_plus_001","rules_out_plus_002"]).to_csv(out/"final_subjective_increment.csv",index=False)
def outcome_sensitivity(d,out):
    rows=[]; cv=RepeatedKFold(n_splits=5,n_repeats=2,random_state=SEED); X=d[hf.FEATURES].copy(); p=Pipeline([("pre",pre(hf.FEATURES)),("model",Ridge(alpha=10))])
    for y in ["outcome_ord","mpc_midpoint","mpc_alt","any_spend","mpc_10plus","mpc_25plus","mpc_50plus"]:
     for k,(tr,te) in enumerate(cv.split(d)):
      m=clone(p).fit(X.iloc[tr],d[y].iloc[tr]); pr=m.predict(X.iloc[te]); rows.append([y,k,r2_score(d[y].iloc[te],pr),math.sqrt(mean_squared_error(d[y].iloc[te],pr))])
    pd.DataFrame(rows,columns=["outcome","fold","r2","rmse"]).to_csv(out/"final_outcome_sensitivity.csv",index=False)

def cronbach(x):
    k=x.shape[1]; return k/(k-1)*(1-x.var(axis=0,ddof=1).sum()/x.sum(axis=1).var(ddof=1))
def latent_dimensions(d,out):
    rng=np.random.default_rng(SEED); train=rng.random(len(d))<.5; loads=[]; scores=pd.DataFrame(index=d.index); diag=[]
    for domain,items in SUBJ_DOMAINS.items():
      sc=StandardScaler().fit(d.loc[train,items]); a=sc.transform(d.loc[train,items]); allx=sc.transform(d[items]); pca=PCA().fit(a); # retain by parallel-analysis-inspired eigenvalue>1, capped 3
      k=max(1,min(3,int((pca.explained_variance_>1).sum()))); diag.append([domain,len(items),k,pca.explained_variance_ratio_[:k].sum(),cronbach(pd.DataFrame(a))])
      for j in range(k):
       scores[f"{domain}_pc{j+1}"]=allx@pca.components_[j]
       for item,val in zip(items,pca.components_[j]):loads.append([domain,j+1,item,val,pca.explained_variance_ratio_[j]])
    pd.DataFrame(loads,columns=["domain","factor","item","loading","variance_share"]).to_csv(out/"final_latent_loadings.csv",index=False); pd.DataFrame(diag,columns=["domain","items","retained_components","variance_explained","cronbach_alpha"]).to_csv(out/"final_latent_diagnostics.csv",index=False)
    # Discovery-half loadings, heldout predictive increment over O.
    base=d[hf.OBJECTIVE+hf.NEEDS].copy(); base=pd.get_dummies(base,columns=[x for x in hf.OBJECTIVE+hf.NEEDS if x in hf.NOMINAL+hf.ORDERED],dtype=float); Z=pd.concat([base,scores],axis=1).fillna(0); B=base.fillna(0); m0=Ridge(alpha=10).fit(B.loc[train],d.mpc_midpoint.loc[train]); m1=Ridge(alpha=10).fit(Z.loc[train],d.mpc_midpoint.loc[train]); r0=r2_score(d.mpc_midpoint.loc[~train],m0.predict(B.loc[~train])); r1=r2_score(d.mpc_midpoint.loc[~train],m1.predict(Z.loc[~train])); pd.DataFrame([[r0,r1,r1-r0,int((~train).sum())]],columns=["O_r2","O_plus_latent_r2","increment","N_test"]).to_csv(out/"final_latent_increment.csv",index=False)
    dd=pd.concat([d,scores],axis=1); latent=list(scores.columns); hr=[]
    for cname,t,c in [("food-cash","food","cash"),("medical-cash","medical","cash")]:
      _,cal,sep,_=standard_hte(dd,t,c,hf.OBJECTIVE+hf.NEEDS+latent,"dr"); hr.append([cname,*cal,*sep])
    pd.DataFrame(hr,columns=["contrast","calibration","cal_se","cal_lo","cal_hi","cal_p","top_bottom","tb_se","tb_lo","tb_hi"]).to_csv(out/"final_latent_hte.csv",index=False)
    return scores

def policy_value(d,preds,out,fold):
    # OOF ML policy. Uniform and simple depth-2 tree are evaluated by IPW with known 1/3 form propensity.
    mu=preds[["mu_cash","mu_food","mu_medical"]].to_numpy(); ml=np.argmax(mu,axis=1); simple=np.zeros(len(d),int); rules=[]
    X=pd.DataFrame({"income":d.income_h,"medical_spending":d.q30_medexp,"food_spending":d.q29_foodexp,"age":d.q42_age})
    for k in range(5):
      tr=fold!=k; te=fold==k; labels=np.argmax(mu[tr],axis=1); tree=DecisionTreeClassifier(max_depth=2,min_samples_leaf=200,random_state=SEED+k).fit(X.loc[tr],labels); simple[te]=tree.predict(X.loc[te]); rules.append(export_text(tree,feature_names=list(X.columns)))
    actual=d.transfer_type.map({"cash":0,"food":1,"medical":2}).to_numpy(); y=d.mpc_midpoint.to_numpy(); rng=np.random.default_rng(SEED)
    policies={"all_cash":np.zeros(len(d),int),"all_food":np.ones(len(d),int),"all_medical":np.full(len(d),2),"depth2_tree":simple,"ml_argmax":ml}; rows=[]; scoremap={}
    for name,a in policies.items():
      score=(actual==a)*y*3; scoremap[name]=score; v=score.mean(); boots=[rng.choice(score,len(score),replace=True).mean() for _ in range(3000)]; lo,hi=np.quantile(boots,[.025,.975]); rows.append([name,v,score.std(ddof=1)/math.sqrt(len(score)),lo,hi,*[(a==j).mean() for j in range(3)]])
    z=pd.DataFrame(rows,columns=["policy","ipw_value","se","lo","hi","share_cash","share_food","share_medical"]); best=z[z.policy.str.startswith("all_")].sort_values("ipw_value").iloc[-1]; bn=best.policy; z["gain_vs_best_uniform"]=z.ipw_value-best.ipw_value; glo=[]; ghi=[]
    for n in z.policy:
      dif=scoremap[n]-scoremap[bn]; boots=[rng.choice(dif,len(dif),replace=True).mean() for _ in range(3000)]; q=np.quantile(boots,[.025,.975]); glo.append(q[0]); ghi.append(q[1])
    z["gain_lo"]=glo; z["gain_hi"]=ghi; z.to_csv(out/"final_policy_value.csv",index=False); (out/"final_policy_tree_rules.txt").write_text("\n\n".join(rules),encoding="utf-8")

def amount_context(d,out):
    rows=[]
    for amount in [200,1000,5000]:
      da=d[d.amount.eq(amount)].copy()
      for cname,t,c in [("food-cash","food","cash"),("medical-cash","medical","cash")]:
       for method in ["t","dr"]:
        _,cal,sep,_=standard_hte(da,t,c,hf.FEATURES,method); rows.append([amount,cname,method,*cal,*sep])
    pd.DataFrame(rows,columns=["amount","contrast","learner","calibration","cal_se","cal_lo","cal_hi","cal_p","top_bottom","tb_se","tb_lo","tb_hi"]).to_csv(out/"final_amount_hte.csv",index=False)

def response_quality(d,out):
    items=["q01_lifesat","q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q06_socsec","q07_emergfund","q08_support","q09_gain","q10_effort","q11_mobility","q12_voice","q13_pressure"]
    x=d[items]; d=d.copy(); d["scale_sd"]=x.std(1); d["extreme_share"]=x.isin([0,10]).mean(1); d["mid_share"]=(x==5).mean(1); d["unique_n"]=x.nunique(1); d["entropy"]=x.apply(lambda r:stats.entropy(r.value_counts(normalize=True)),axis=1)
    screens={"R":np.ones(len(d),bool),"C":d.sample_C,"Q1":d.sample_A&(d.scale_sd>=1)&(d.unique_n>=4),"Q2":d.sample_A&(d.scale_sd>=1.5)&(d.unique_n>=5)&(d.extreme_share<=.8)}; comp=[]; res=[]
    for name,mask in screens.items():
      z=d[mask]; comp.append([name,len(z),z.q42_age.mean(),z.q43_edu.mean(),z.income_h.mean(),z.scale_sd.mean(),z.extreme_share.mean(),z.mid_share.mean(),z.unique_n.mean(),z.entropy.mean()])
      m=smf.ols("outcome_ord~C(transfer_type)*C(amount)",z).fit(cov_type="HC1")
      for est,w in [("food-cash",{"C(transfer_type)[T.food]":1,"C(transfer_type)[T.food]:C(amount)[T.1000]":1/3,"C(transfer_type)[T.food]:C(amount)[T.5000]":1/3}),("medical-cash",{"C(transfer_type)[T.medical]":1,"C(transfer_type)[T.medical]:C(amount)[T.1000]":1/3,"C(transfer_type)[T.medical]:C(amount)[T.5000]":1/3})]:
       # Correct equal-weight pooled main term: main is repeated across three amounts.
       w={k:v for k,v in w.items()}; res.append([name,est,*hf.ctest(m,w),len(z)])
      for v in ["income_h","q30_medexp"]:
       zz=v+"_z"; mm=smf.ols(f"outcome_ord~C(transfer_type)*C(amount)+{zz}+C(transfer_type):{zz}+C(amount):{zz}",z).fit(cov_type="HC1"); res.append([name,"medical-food_"+v,*hf.ctest(mm,{f"C(transfer_type)[T.medical]:{zz}":1,f"C(transfer_type)[T.food]:{zz}":-1}),len(z)])
    pd.DataFrame(comp,columns=["screen","N","age_mean","education_mean","income_mean","scale_sd","extreme_share","mid_share","unique_n","entropy"]).to_csv(out/"final_quality_composition.csv",index=False); pd.DataFrame(res,columns=["screen","estimand","effect","se","lo","hi","p","N"]).to_csv(out/"final_quality_robustness.csv",index=False)

def composition(d,out):
    rows=[]
    for v in ["q41_gender","q43_edu","q23_hukou","q24_workstat","q49_citytier","q47_province","income_h"]:
      for k,n in d[v].value_counts(dropna=False).sort_index().items():rows.append([v,k,n,n/len(d)])
    pd.DataFrame(rows,columns=["variable","category","N","share"]).to_csv(out/"final_sample_composition.csv",index=False)
    pd.DataFrame([["age",len(d),d.q42_age.mean(),d.q42_age.std(),d.q42_age.quantile(.25),d.q42_age.median(),d.q42_age.quantile(.75)]],columns=["variable","N","mean","sd","p25","p50","p75"]).to_csv(out/"final_age_summary.csv",index=False)

def external_benchmarks(d,out):
    """Descriptive comparisons only; incompatible population frames are not raked."""
    rows=[]
    def add(label,sample,official,year,compat,note,url): rows.append([label,sample,official,sample-official,year,compat,note,url])
    sex_url="https://www.stats.gov.cn/zt_18555/zdtjgz/zgrkpc/dqcrkpc/ggl/202302/t20230215_1904000.html"
    edu_url="https://www.stats.gov.cn/zt_18555/zdtjgz/zgrkpc/dqcrkpc/ggl/202302/t20230215_1903999.html"
    age_url="https://www.stats.gov.cn/zt_18555/zdtjgz/zgrkpc/dqcrkpc/ggl/202302/t20230215_1903996.html"
    add("male_share",(d.q41_gender==1).mean(),.5124,2020,"partial","Adult online survey versus total-population census.",sex_url)
    add("female_share",(d.q41_gender==2).mean(),.4876,2020,"partial","Adult online survey versus total-population census.",sex_url)
    add("junior_college_or_more_share",(d.q43_edu>=3).mean(),.15467,2020,"low","Large age and sampling-frame mismatch; not a weighting target.",edu_url)
    add("age_60plus_share",(d.q42_age>=60).mean(),.1870,2020,"low","Adult online survey versus census including children.",age_url)
    pd.DataFrame(rows,columns=["benchmark","sample_share","official_share","gap","official_year","comparability","note","source_url"]).to_csv(out/"final_external_benchmarks.csv",index=False)

def figures(out,figs):
    sns.set_theme(style="whitegrid")
    f=pd.read_csv(out/"final_form_specific_prediction.csv"); a=f.groupby(["form","model"]).r2.agg(["mean","std"]).reset_index(); fig,ax=plt.subplots(figsize=(8,5)); sns.barplot(a,x="form",y="mean",hue="model",ax=ax); ax.errorbar([],[],label="fold uncertainty"); ax.set(ylabel="Repeated-CV R²",title="Form-specific stated-MPC predictability"); fig.tight_layout(); fig.savefig(figs/"final_form_predictability.png",dpi=180); plt.close(fig)
    x=pd.read_csv(out/"final_cross_form_transfer.csv"); mat=x.pivot(index="train_form",columns="test_form",values="spearman"); fig,ax=plt.subplots(figsize=(6,5)); sns.heatmap(mat,annot=True,cmap="vlag",center=0,ax=ax); ax.set(title="Cross-form prediction rank transferability"); fig.tight_layout(); fig.savefig(figs/"final_cross_form_stability.png",dpi=180); plt.close(fig)
    dec=pd.read_csv(out/"final_shared_specific_decomposition.csv"); fig,ax=plt.subplots(figsize=(8,4)); sns.barplot(dec,x="component",y="variance",ax=ax); ax.tick_params(axis="x",rotation=20); ax.set(title="Shared versus form-specific predictable variance"); fig.tight_layout(); fig.savefig(figs/"final_shared_specific.png",dpi=180); plt.close(fig)
    h=pd.read_csv(out/"final_standard_hte_quintiles.csv"); z=h[(h.feature_set=="ALL")&(h.method=="dr")&h.contrast.isin(["food-cash","medical-cash"])]; fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
    for ax,(c,g) in zip(axes,z.groupby("contrast")):ax.errorbar(g.quintile,g.effect,yerr=1.96*g.se,marker="o",capsize=3); ax.axhline(0,color="black",lw=.8); ax.set(title=c,xlabel="OOF CATE quintile",ylabel="Observed midpoint contrast")
    fig.tight_layout(); fig.savefig(figs/"final_honest_hte.png",dpi=180); plt.close(fig)
    p=pd.read_csv(out/"final_policy_value.csv"); fig,ax=plt.subplots(figsize=(8,4)); ax.errorbar(p.policy,p.ipw_value,yerr=1.96*p.se,fmt="o",capsize=4); ax.tick_params(axis="x",rotation=20); ax.set(title="Honest IPW policy value",ylabel="Mean midpoint stated MPC"); fig.tight_layout(); fig.savefig(figs/"final_policy_value.png",dpi=180); plt.close(fig)
    formal=Path(__file__).resolve().parents[1]/"tables"/"formal_level_ml_cv.csv"
    if formal.exists():
      q=pd.read_csv(formal); q=q[q.model.eq("random_forest")]; fig,ax=plt.subplots(figsize=(8,4)); sns.pointplot(q,x="feature_set",y="r2",errorbar=("pi",95),ax=ax); ax.axhline(0,color="black",lw=.8); ax.set(title="Stated-MPC OOS predictability with fold uncertainty",ylabel="Random-forest CV R²"); fig.tight_layout(); fig.savefig(figs/"final_level_predictability.png",dpi=180); plt.close(fig)
    moderation=Path(__file__).resolve().parents[1]/"tables"/"formal_medical_food_robustness.csv"
    if moderation.exists():
      q=pd.read_csv(moderation); q=q[(q["sample"]=="R")&(q.specification=="primary")&(q.se_type=="HC1")&q.variable.isin(["income_h","q30_medexp"])&q.amount.astype(str).isin(["200","1000","5000"])].copy(); q["amount"]=q.amount.astype(int)
      fig,ax=plt.subplots(figsize=(8,4))
      for variable,g in q.groupby("variable"):
       label={"income_h":"Household income","q30_medexp":"Medical spending"}[variable]; ax.errorbar(g.amount,g.effect_or_wald,yerr=1.96*g.se,marker="o",capsize=3,label=label)
      ax.axhline(0,color="black",lw=.8); ax.set(xscale="log",xticks=[200,1000,5000],xticklabels=["200","1,000","5,000"],xlabel="Transfer amount (RMB)",ylabel="Medical minus food interaction",title="Medical-versus-food moderation by transfer amount"); ax.legend(); fig.tight_layout(); fig.savefig(figs/"final_medical_moderation.png",dpi=180); plt.close(fig)

def main(data,outdir):
    out=Path(outdir); figs=out/"figures"; out.mkdir(parents=True,exist_ok=True); figs.mkdir(exist_ok=True); d=hf.prep(pd.read_stata(data,convert_categoricals=False)); preds,fold=form_predictions(d,out); cross_form_transfer(d,out); coefficient_alignment(d,out); hte_suite(d,out); paired_increment(d,out); outcome_sensitivity(d,out); latent_dimensions(d,out); amount_context(d,out); policy_value(d,preds,out,fold); response_quality(d,out); composition(d,out); external_benchmarks(d,out); figures(out,figs); summary={"N_R":len(d),"N_A":int(d.sample_A.sum()),"N_C":int(d.sample_C.sum()),"standard_hte_contrasts":3,"policy_evaluation":"OOF IPW","causal_forest":False}; (out/"final_run_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); print(json.dumps(summary,indent=2))
if __name__=="__main__":
    p=ArgumentParser(); p.add_argument("data"); p.add_argument("--out",default="final-output"); a=p.parse_args(); main(a.data,a.out)
