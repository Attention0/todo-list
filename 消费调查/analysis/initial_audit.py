"""Reproduce the first-round audit without writing respondent-level data.

Usage:
  python initial_audit.py "path/to/delivery.dta" --out "path/to/summary-output"
"""
from argparse import ArgumentParser
from pathlib import Path
import json, math
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

SCEN = ["q32_cash200","q33_cash1k","q34_cash5k","q35_vouch200","q36_vouch1k","q37_vouch5k","q38_med200","q39_med1k","q40_med5k"]
TYPES = ["cash"]*3+["food"]*3+["medical"]*3
AMOUNTS = [200,1000,5000]*3
MID = {1:0,2:.05,3:.175,4:.375,5:.625,6:.875}

def diff_ci(a,b):
    a,b=pd.Series(a).dropna(),pd.Series(b).dropna()
    d=a.mean()-b.mean(); se=math.sqrt(a.var()/len(a)+b.var()/len(b))
    return d,se,d-1.96*se,d+1.96*se,len(a),len(b)

def main(data_path, out_path):
    out=Path(out_path); figs=out/"figures"; figs.mkdir(parents=True,exist_ok=True)
    d=pd.read_stata(data_path,convert_categoricals=False); n=len(d)
    hit=d[SCEN].notna(); d["scenario_n"]=hit.sum(axis=1)
    d["cell"]=np.where(d.scenario_n.eq(1),hit.values.argmax(1)+1,np.nan)
    d["type"]=d.cell.map(dict(enumerate(TYPES,1))); d["amount"]=d.cell.map(dict(enumerate(AMOUNTS,1)))
    d["outcome"]=d[SCEN].bfill(axis=1).iloc[:,0].where(d.scenario_n.eq(1)); d["mpc"]=d.outcome.map(MID)
    d["income_h"]=np.where(d.q46_income.between(11,16),d.q46_income-10,d.q46_income)
    scales=["q01_lifesat","q02_safety","q03a_fair_dist","q03b_fair_opp","q03c_fair_rule","q04_trust_gov","q05_trust_soc","q06_socsec","q07_emergfund","q08_support","q09_gain","q10_effort","q11_mobility","q12_voice","q13_pressure"]
    straight=d[scales].notna().all(1)&d[scales].nunique(1).eq(1)
    bad_age=~d.q42_age.between(18,100)|d.q42_age.isna()
    mismatch=d.scenario_n.eq(1)&((d.cell!=d.scen_version)|(d.outcome!=d.scen_mpc)|(d.amount!=d.scen_amount)|(d.type.map({'cash':1,'food':2,'medical':3})!=d.scen_type))
    d["clean"]=~(straight|bad_age|mismatch|d.id.isna()|d.id.duplicated(False))
    cells=d.groupby(["cell","type","amount"]).agg(N=("outcome","size"),mean_ord=("outcome","mean"),sd=("outcome","std"),mean_mpc=("mpc","mean")).reset_index()
    cells["se"]=cells.sd/np.sqrt(cells.N); cells.to_csv(out/"cell_means.csv",index=False)
    d[d.clean].groupby(["cell","type","amount"]).agg(N=("outcome","size"),mean_ord=("outcome","mean"),mean_mpc=("mpc","mean")).reset_index().to_csv(out/"clean_cell_means.csv",index=False)
    counts=d.groupby(["cell","type","amount"]).size().reset_index(name="N"); counts["share"]=counts.N/n; counts.to_csv(out/"cell_counts.csv",index=False)
    chi,p=stats.chisquare(counts.N,np.repeat(n/9,9))
    model=smf.ols("outcome~C(type)*C(amount)",d).fit(cov_type="HC1")
    controls="q42_age+C(q41_gender)+C(q43_edu)+C(income_h)+C(q23_hukou)+C(q24_workstat)+C(q26_housing)+C(q27_minorchild)+C(q28_hhsize)+C(q29_foodexp)+C(q30_medexp)+C(q31_gotsubsidy)+q06_socsec+q07_emergfund+q13_pressure+q15_fut_self+q17a_fut_econ+q17b_fut_job+C(q49_citytier)"
    controlled=smf.ols("outcome~C(type)*C(amount)+"+controls,d).fit(cov_type="HC1")
    for name,m in [("uncontrolled",model),("controlled",controlled)]:
        ci=m.conf_int(); pd.DataFrame({"term":m.params.index,"b":m.params,"se":m.bse,"lo":ci[0],"hi":ci[1],"p":m.pvalues}).to_csv(out/f"{name}_ols.csv",index=False)
    bounds={1:(0,500),2:(501,1000),3:(1001,2000),4:(2001,3000),5:(3001,5000),6:(5000,np.inf)}
    cf=d[d.type.isin(["cash","food"])].copy()
    def cls(r):
        lo,hi=bounds[int(r.q29_foodexp)]; lo*=6; hi*=6
        return "definitely inframarginal" if r.amount<lo else ("likely binding" if r.amount>hi else "ambiguous")
    cf["food_binding"]=cf.apply(cls,axis=1); rows=[]
    for label,g in cf.groupby("food_binding"):
        z=diff_ci(g[g.type.eq('food')].outcome,g[g.type.eq('cash')].outcome); rows.append([label,*z])
    pd.DataFrame(rows,columns=["class","food_minus_cash","se","lo","hi","N_food","N_cash"]).to_csv(out/"food_binding.csv",index=False)
    base=["q42_age","q06_socsec","q07_emergfund","q13_pressure","q15_fut_self","q17a_fut_econ","q17b_fut_job","q41_gender","q43_edu","income_h","q23_hukou","q24_workstat","q26_housing","q27_minorchild","q28_hhsize","q29_foodexp","q30_medexp","q31_gotsubsidy","q49_citytier"]
    z=d[["cell"]+base].dropna(); X=pd.get_dummies(z[base],columns=[x for x in base if x not in ["q42_age","q06_socsec","q07_emergfund","q13_pressure","q15_fut_self","q17a_fut_econ","q17b_fut_job"]],drop_first=True,dtype=float); X=sm.add_constant(X)
    full=sm.MNLogit((z.cell-1).astype(int),X).fit(disp=False); null=sm.MNLogit((z.cell-1).astype(int),np.ones((len(z),1))).fit(disp=False); lr=2*(full.llf-null.llf); df_lr=int(full.df_model-null.df_model)
    summary={"N":n,"columns":len(d.columns)-8,"exactly_one_scenario":int(d.scenario_n.eq(1).sum()),"zero_scenario":int(d.scenario_n.eq(0).sum()),"multiple_scenario":int(d.scenario_n.gt(1).sum()),"duplicate_id_rows":int(d.id.duplicated(False).sum()),"full_duplicates":int(d.duplicated().sum()),"straightliners":int(straight.sum()),"age_under_18_or_over_100_or_missing":int(bad_age.sum()),"metadata_mismatch":int(mismatch.sum()),"clean_N":int(d.clean.sum()),"assignment_chi2":chi,"assignment_p":p,"balance_LR":lr,"balance_df":df_lr,"balance_p":stats.chi2.sf(lr,df_lr),"floor_pct":100*d.outcome.eq(1).mean(),"ceiling_pct":100*d.outcome.eq(6).mean()}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    fig,ax=plt.subplots(figsize=(8,5))
    for t,g in cells.groupby("type"): ax.errorbar(g.amount,g.mean_ord,yerr=1.96*g.se,marker='o',capsize=4,label=t)
    ax.set_xscale('log'); ax.set_xticks([200,1000,5000],labels=['200','1000','5000']); ax.set(xlabel='Transfer amount (RMB)',ylabel='Mean ordered outcome',title='Mean stated response by treatment'); ax.legend(); fig.tight_layout(); fig.savefig(figs/"treatment_lines.png",dpi=180)

if __name__=="__main__":
    p=ArgumentParser(); p.add_argument("data"); p.add_argument("--out",default="audit-output"); a=p.parse_args(); main(a.data,a.out)
