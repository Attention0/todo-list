"""Frozen age x education sensitivity; no response-adaptive grouping."""
from analyze import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--data',required=True);args=p.parse_args()
d=covariates(prepare(args.data));a=d[d.sample_A].copy()
labels=['18-29','30-44','45-59','60+']
a['agegroup']=pd.cut(a.q42_age,[17,29,44,59,100],labels=labels).astype(str)
a['education']=a.q43_edu.map({1:'low',2:'high',3:'tertiary',4:'tertiary',5:'tertiary'})
c=pd.read_csv(OUT/'census_2020_transcription.csv');c['agegroup']=['18-29']*4+['30-44']*3+['45-59']*3+['60+']*6
c['tertiary']=c[['junior_college','bachelor','masters','doctor']].sum(axis=1);c['high']=c.high_school;c['low']=c.total-c.tertiary-c.high
target=c.groupby('agegroup')[['low','high','tertiary']].sum().stack().rename('target_count').reset_index().rename(columns={'level_1':'education'})
target['target_share']=target.target_count/target.target_count.sum()
n=a.groupby(['agegroup','education']).size().rename('sample_N').reset_index();target=target.merge(n,how='left');assert target.sample_N.notna().all() and target.sample_N.min()>0
target['sample_share']=target.sample_N/len(a);target['weight']=target.target_share/target.sample_share
a=a.merge(target[['agegroup','education','weight']],on=['agegroup','education'],validate='many_to_one')
out=[];diag=[]
from scipy.optimize import brentq
lam=brentq(lambda t:np.minimum(t*a.weight.to_numpy(),10).mean()-1,1,100)
capped=np.minimum(lam*a.weight.to_numpy(),10)
for scheme,w in [('unweighted',np.ones(len(a))),('uncapped',a.weight.to_numpy()),('cap10',capped)]:
    w=w/w.mean();a['w']=w
    m=smf.wls('top75~C(form)*z',a,weights=w).fit(cov_type='HC3')
    cm=np.array([unit(m,'C(form)[T.food]:z'),unit(m,'C(form)[T.medical]:z')]);rr=[Ctest(m,cm,'omnibus'),Ctest(m,-cm[0],'cash-food'),Ctest(m,-cm[1],'cash-medical')]
    for r,hp in zip(rr,holm([r['p'] for r in rr])):r.update(scheme=scheme,holm3=hp);out.append(r)
    sums=a.groupby(['agegroup','education']).w.sum()/w.sum()
    target[scheme+'_share']=[sums.loc[(r.agegroup,r.education)] for r in target.itertuples()]
    diag.append(dict(scheme=scheme,N=len(a),ESS=w.sum()**2/(w@w),min_weight=w.min(),max_weight=w.max(),normalized_cap=10 if scheme=='cap10' else np.nan,max_abs_target_discrepancy=float(abs(target[scheme+'_share']-target.target_share).max()),cap_fraction=float((w>=10-1e-9).mean()) if scheme=='cap10' else 0))
    if scheme=='cap10':assert w.max()<=10+1e-9 and abs(w.mean()-1)<1e-12
save(target,'calibration_cells.csv');save(pd.DataFrame(out),'calibration_effects.csv');save(pd.DataFrame(diag),'calibration_diagnostics.csv')
assert target.shape[0]==12 and abs(target.uncapped_share-target.target_share).max()<1e-12
# Complete adult descriptive endpoints; no new tests selected by their results.
rows=[]
for form,g in a.groupby('form'):
    low=g[g.amount==200].top75;high=g[g.amount==5000].top75;p0,p1=low.mean(),high.mean();v0,v1=low.var(ddof=1)/len(low),high.var(ddof=1)/len(high)
    for name,e,se in [('risk_ratio',np.log(p1/p0),np.sqrt(v1/p1**2+v0/p0**2)),('odds_ratio',np.log(p1/(1-p1)/(p0/(1-p0))),np.sqrt(v1/(p1*(1-p1))**2+v0/(p0*(1-p0))**2))]:
        r=interval(e,se);r.update(form=form,scale=name,estimate=np.exp(e),lo=np.exp(r['lo']),hi=np.exp(r['hi']),N200=len(low),N5000=len(high));r.pop('sim_lo');r.pop('sim_hi');rows.append(r)
save(pd.DataFrame(rows),'adult_endpoint_ratios.csv')
print(pd.DataFrame(diag).to_string(index=False));print(pd.DataFrame(out).to_string(index=False))
