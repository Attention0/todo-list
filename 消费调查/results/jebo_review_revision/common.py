from pathlib import Path
import sys, json, hashlib
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
O=Path(__file__).resolve().parent; ROOT=O.parents[1]; PRIOR=O.parent/'nc_evidence_revision'
FORMS=['cash','food','medical']; AMOUNTS=np.array([200,1000,5000])
SCORES=np.array([0,.05,.175,.375,.625,.875])
OUTCOMES=['ordinal','midpoint','any_spending','ge10','ge25','ge50','top75']
YS=np.column_stack([np.arange(1,7),SCORES]+[(np.arange(1,7)>=k).astype(float) for k in range(2,7)])
def save(rows,name):
    (rows if isinstance(rows,pd.DataFrame) else pd.DataFrame(rows)).to_csv(O/name,index=False)
def note(name,text): (O/name).write_text(text.rstrip()+'\n',encoding='utf8')
def mdtable(df):
    vals=df.fillna('').astype(str)
    return '| '+' | '.join(vals.columns)+' |\n| '+' | '.join(['---']*len(vals.columns))+' |\n'+'\n'.join('| '+' | '.join(row)+' |' for row in vals.values)
def holm(p):return multipletests(p,method='holm')[1]
def inf(e,se,k=1):
    q=stats.norm.ppf(1-.05/(2*k));return dict(estimate=float(e),se=float(se),lo=float(e-1.96*se),hi=float(e+1.96*se),p=float(2*stats.norm.sf(abs(e/se))),sim_lo=float(e-q*se),sim_hi=float(e+q*se))
def load(path):
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==json.loads((PRIOR/'freeze.json').read_text())['raw_sha256']
    sys.path.insert(0,str(O.parent/'mpc_size_curve'));from size_curve import prepare
    sys.path.insert(0,str(O.parent/'nc_revision_audit'));from secondary import covariates
    d=covariates(prepare(path));d=d[d.sample_A].copy();assert len(d)==5480
    return d
def counts():
    p=pd.read_csv(PRIOR/'distribution.csv');p=p[p['sample']=='A']
    return np.array([[int(p.loc[(p.form==f)&(p.amount==a)&(p.category==k),'count'].iloc[0]) for k in range(1,7)] for f in FORMS for a in AMOUNTS])
def grouped_fit(X,y,n):
    bread=np.linalg.inv(X.T@(n[:,None]*X));b=bread@X.T@(n*y)
    h=np.einsum('ij,jk,ik->i',X,bread,X);u=(y-X@b)/(1-h)
    v=bread@(X.T@((n*u*u)[:,None]*X))@bread
    return b,v,bread
def wald(b,v,C):
    e=C@b;vv=C@v@C.T;w=float(e@np.linalg.solve(vv,e));return dict(wald=w,df=len(C),p=float(stats.chi2.sf(w,len(C))))
