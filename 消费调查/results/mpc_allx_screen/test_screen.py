"""Independent numerical/statistical checks; reads local raw data, exports test metadata only."""
import sys,json,hashlib,subprocess
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.model_selection import StratifiedKFold
from inventory import ROOT,make_inventory,prior
from screen import fit,extract,encode,TARGETS,Y_NAMES,SEED,direction

def bh(p):
    order=np.argsort(p);q=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1];out=np.empty(len(p));out[order]=np.minimum(q,1);return out

def holm(p):
    order=np.argsort(p);q=np.maximum.accumulate(p[order]*(len(p)-np.arange(len(p))));out=np.empty(len(p));out[order]=np.minimum(q,1);return out

def run(data,repeat=False):
    checks=[]
    def check(name,cond):
        if not cond:raise AssertionError(name)
        checks.append(name);print('PASS',name,flush=True)
    before=json.loads((ROOT/'inventory_manifest.json').read_text());d,X,inv,defs=make_inventory(data,ROOT);t=pd.read_csv(ROOT/'all_screen_results.csv');c=pd.read_csv(ROOT/'cross_outcome_concordance.csv')
    check('inventory fingerprint unchanged after regressions',before['inventory_sha256']==hashlib.sha256((ROOT/'all_x_variable_inventory.csv').read_bytes()).hexdigest())
    raw=pd.read_stata(data,convert_categoricals=False)
    check('all 67 original fields inventoried once',set(raw.columns)==set(inv[inv.origin.eq('raw')].variable) and len(inv[inv.origin.eq('raw')])==67)
    check('150 legal substantive baseline X',len(defs)==150 and inv[inv.eligible].timing.eq('pre-treatment').all() and not inv[inv.eligible].domain.eq('metadata').any())
    check('no outcomes treatment IDs or quality fields eligible',not set(defs)&{'id','scen_mpc','scen_amount','scen_type','amount','form','z','top75','person_score','cate','scale_sd','extreme_share','strict_assigned','sample_Q1','sample_Q2'})
    check('three outcome encodings independently verified',np.array_equal(d.ordinal,raw.scen_mpc) and np.array_equal(d.top75,(raw.scen_mpc==6).astype(int)) and np.allclose(d.midpoint,raw.scen_mpc.map({1:0,2:.05,3:.175,4:.375,5:.625,6:.875})))
    check('samples R A C Q1 Q2 match prior audit',[len(d),int(d.sample_A.sum()),int(d.sample_C.sum()),int(d.sample_Q1.sum()),int(d.sample_Q2.sum())]==[5497,5480,5171,2715,1208])
    # Independent statsmodels estimator and a separately assembled block design.
    for var in ['q07_emergfund','q26_housing','q43_edu','subjective_economic_pc1']:
        a,lev,sd=encode(X[var],defs[var]['kind']);k=a.shape[1];z=d.z.to_numpy();block=np.c_[np.ones(len(d)),z,a,z[:,None]*a];B=np.column_stack([block*(d.form.to_numpy()==f)[:,None] for f in ['cash','food','medical']]);pdim=block.shape[1]
        for y in Y_NAMES:
            model=sm.OLS(d[y],B).fit(cov_type='HC3');m=fit(d,a,d[y],lev)
            check(f'{var}/{y} independently fitted full HC3 beta',np.allclose(m[0].reshape(-1),model.params,rtol=1e-7,atol=2e-10))
            for target in ['cash','rc']:
                V=np.zeros((k,3*pdim))
                for f,w in enumerate(TARGETS[target]):
                    for j in range(k):V[j,f*pdim+2+k+j]=w
                b=V@model.params;cov=V@model.cov_params()@V.T;p=stats.chi2.sf(b@np.linalg.solve(cov,b),k);r,bs,se=extract(m,TARGETS[target],k);rr=t[(t.variable==var)&(t.target==target)&(t.outcome==y)].iloc[0]
                check(f'{var}/{y}/{target} independent estimates covariance omnibus',np.allclose(bs,b,atol=2e-10) and np.allclose(se,np.sqrt(np.diag(cov)),atol=2e-10) and np.allclose([r['p'],rr.p],[p,p],atol=2e-8))
            ix=d.form.eq('cash');cm=sm.OLS(d.loc[ix,y],block[ix]).fit(cov_type='HC3');cash=fit(d,a,d[y],lev,arms=['cash']);check(f'{var}/{y} actual Cash-only HC3 equality',np.allclose(cm.params,cash[0][0],atol=2e-10) and np.allclose(cm.cov_params(),cash[1][0],atol=2e-10))
    for target in ['cash','rc']:
        for y in Y_NAMES:
            g=t[(t.target==target)&(t.outcome==y)];p=g.p.fillna(1).to_numpy();ok=g.status.eq('ok').to_numpy();check(f'{target}/{y} BH and Holm independent formulas with all150',len(g)==150 and np.allclose(g.q.to_numpy()[ok],bh(p)[ok]) and np.allclose(g.holm_p.to_numpy()[ok],holm(p)[ok]) and g.loc[~ok,['q','holm_p']].isna().all().all());check(f'{target}/{y} no FDR or Holm discoveries',not g.q.lt(.1).any() and not g.holm_p.lt(.05).any());check(f'{target}/{y} per-X actual N',g.N.eq(1798 if target=='cash' else 5497).all())
    check('empty shortlist derived not manually selected',not c.shortlisted.any() and not c.tier.isin(['A','B']).any())
    check('all raw/constructed aliases preserved in family',{'q07_emergfund','q07_emergfund_z','liquidity','who::liquidity'}<=set(defs))
    aa=t[t.variable.eq('q07_emergfund')].sort_values(['target','outcome']).estimate.to_numpy()
    for v in ['q07_emergfund_z','liquidity','who::liquidity']:check(v+' affine alias numerical equality',np.allclose(aa,t[t.variable.eq(v)].sort_values(['target','outcome']).estimate.to_numpy(),atol=1e-12))
    cf=pd.read_csv(ROOT/'crossfit_stability.csv');details=pd.read_csv(ROOT/'crossfit_fold_diagnostics.csv');check('all X x3Y x2target x5fold outputs',len(cf)==900 and len(details)==4500 and not cf.duplicated(['variable','outcome','target']).any() and not details.duplicated(['variable','outcome','target','fold']).any())
    unordered=cf[cf.variable.eq('q26_housing')];check('unordered factors have vector median not arbitrary rank trend',unordered.median_training_estimate.isna().all() and unordered.median_training_profile.notna().all())
    slopes=pd.read_csv(ROOT/'categorical_form_slopes.csv');check('factor form slopes have unique keys and suppressed small groups',not slopes.duplicated(['variable','outcome','category','form']).any() and slopes.N.ge(10).all())
    folds=np.zeros(len(d),int)
    for k,(_,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=SEED).split(d,d.cell)):folds[te]=k
    counts=pd.crosstab(folds,d.cell);check('nine-cell five-fold stratification',counts.shape==(5,9) and ((counts.max()-counts.min())<=1).all())
    a,lev,_=encode(X.q07_emergfund,'numeric');te=folds==0;tr=~te;mt=fit(d.loc[tr],a[tr],d.loc[tr,'top75'],arms=['cash']);mh=fit(d.loc[te],a[te],d.loc[te,'top75'],arms=['cash']);_,b,_=extract(mt,TARGETS['cash'],1,False);_,h,_=extract(mh,TARGETS['cash'],1,False);rr=details[(details.variable=='q07_emergfund')&(details.outcome=='top75')&(details.target=='cash')&(details.fold==1)].iloc[0];check('heldout scalar projection sign and magnitude',np.allclose(rr.holdout_direction_score,np.sign(b[0])*h[0]))
    check('direction gates reject major reversals',not direction(['[1.0]','[-0.2]','[0.3]'])[0] and not direction(['[1,0]','[-1,0]','[0.5,0]'])[0])
    r=pd.read_csv(ROOT/'shortlisted_robustness.csv');j=pd.read_csv(ROOT/'joint_candidate_models.csv');check('conditional analyses honestly N/A, not passed',r.status.str.startswith('not_applicable').all() and j.status.str.startswith('not_applicable').all() and r.estimate.isna().all() and j.estimate.isna().all())
    check('six figure families and source CSVs',len(list((ROOT/'figures').glob('fig*.png')))==6 and len(list((ROOT/'figures').glob('fig*.pdf')))==6 and len(list(ROOT.glob('fig*_source.csv')))==6)
    report=(ROOT.parents[1]/'MPC_ALLX_SCREEN_RESULTS.md').read_text(encoding='utf-8');check('report exactly17 mandated sections',sum(line.startswith('## ') for line in report.splitlines())==17)
    # Export allowlist is aggregate-schema based, not a meaningless file row-count rule.
    for path in ROOT.glob('*.csv'):
        df=pd.read_csv(path);check(path.name+' no respondent raw/prediction schema',not set(df.columns)&{'id','respondent_id','person_id','fold_id','cate_oof','individual_prediction','scen_mpc','scen_amount','scen_type'})
    if repeat:
        snapshot={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.csv')}
        for script in ['screen.py','deliver.py']:subprocess.run([sys.executable,str(ROOT/script),data,'--out',str(ROOT)],check=True)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.csv')};check('complete repeated run all27 aggregate CSV SHA256 identical',snapshot==after and len(snapshot)==27)
    result=dict(status='passed',assertions=len(checks),checks=checks,raw_sha256=before['data_sha256'],inventory_sha256=before['inventory_sha256'],test='independent statsmodels HC3, manual multiplicity formulas, design/crossfit/protocol/privacy assertions')
    (ROOT/'test_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('ALL',len(checks),'ASSERTIONS PASSED',flush=True)
    artifacts={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='artifact_manifest.json'}
    (ROOT/'artifact_manifest.json').write_text(json.dumps(dict(artifacts=artifacts,aggregate_only=True),indent=2),encoding='utf-8')

if __name__=='__main__':run(sys.argv[1],repeat='--repeat' in sys.argv[2:])
