"""Only authorized new empirical calculation; aggregate categorical bootstrap."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
O=Path(__file__).resolve().parent
R=O.parent/'nc_evidence_revision'
B=4000;SEED=2026100316
scores=np.array([0,.05,.175,.375,.625,.875])
dist=pd.read_csv(R/'distribution.csv');dist=dist[dist['sample']=='A']
assert len(dist)==54 and dist.groupby(['form','amount']).N.first().sum()==5480
rng=np.random.default_rng(SEED);cells=[];draws={};point={};invalid=0
for form in ['cash','food','medical']:
    for amount in [200,1000,5000]:
        g=dist[(dist.form==form)&(dist.amount==amount)].sort_values('category')
        counts=g['count'].to_numpy(dtype=int);n=int(g.N.iloc[0]);assert sum(counts)==n
        prob=counts/n;p=1-prob[0];m=prob@scores;mp=m/p
        assert abs(m-p*mp)<1e-14
        boot=rng.multinomial(n,prob,size=B);bp=1-boot[:,0]/n;bm=boot@scores/n
        bad=(bp==0);invalid+=int(bad.sum());bplus=np.divide(bm,bp,out=np.full(B,np.nan),where=~bad)
        row=dict(sample='A',form=form,amount=amount,N=n,positive_N=n-counts[0],p_any=p,midpoint=m,conditional_midpoint=mp,top75=prob[-1])
        row.update({f'count{k+1}':int(v) for k,v in enumerate(counts)})
        for name,v in [('p_any',bp),('midpoint',bm),('conditional_midpoint',bplus)]:
            lo,hi=np.quantile(v,[.025,.975]) if np.isfinite(v).all() else [np.nan,np.nan]
            row[name+'_lo']=lo;row[name+'_hi']=hi
        cells.append(row);point[form,amount]=(p,mp,m);draws[form,amount]=(bp,bplus,bm)
decomp=[]
for form in ['cash','food','medical']:
    p0,m0,u0=point[form,200];p1,m1,u1=point[form,5000]
    ext=(p1-p0)*(m0+m1)/2;intensive=(m1-m0)*(p0+p1)/2
    bp0,bm0,bu0=draws[form,200];bp1,bm1,bu1=draws[form,5000]
    be=(bp1-bp0)*(bm0+bm1)/2;bi=(bm1-bm0)*(bp0+bp1)/2;bt=bu1-bu0
    assert abs(ext+intensive-(u1-u0))<1e-14 and np.nanmax(abs(be+bi-bt))<1e-14
    row=dict(sample='A',form=form,amount_low=200,amount_high=5000,p_any_change=p1-p0,conditional_midpoint_change=m1-m0,extensive=ext,intensive=intensive,total=u1-u0)
    for name,v in [('extensive',be),('intensive',bi),('total',bt)]:
        lo,hi=np.quantile(v,[.025,.975]) if np.isfinite(v).all() else [np.nan,np.nan]
        row[name+'_lo']=lo;row[name+'_hi']=hi
    decomp.append(row)
c=pd.DataFrame(cells);d=pd.DataFrame(decomp)
c.to_csv(O/'extensive_intensive_cells.csv',index=False);d.to_csv(O/'extensive_intensive_decomposition.csv',index=False)
meta=dict(seed=SEED,draws=B,method='independent cell-stratified empirical multinomial; exactly equivalent to categorical record bootstrap',invalid_zero_positive_draws=invalid,adult_N=5480,raw_data_access=False,source_sha256=hashlib.sha256((R/'distribution.csv').read_bytes()).hexdigest(),manifest_sha256=hashlib.sha256((O/'JEBO_ANALYSIS_MANIFEST.md').read_bytes()).hexdigest())
(O/'decomposition_verification.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
lines=['# Extensive and intensive accounting of stated spending','', 'Protocol commit: 950e90f. Adult sample only. No respondent-level data were read. The first response bin is coded zero; positive means categories2–6, not an independently observed purchase. Conditional-positive averages compare post-treatment selected groups and are descriptive. The Shapley components are an accounting identity, not causal mediation.','', '| Form | p(any) 200 / 5000 | Conditional midpoint 200 / 5000 | Total change pp | Extensive pp [95% interval] | Intensive pp [95% interval] |','|---|---|---|---|---|---|']
for r in decomp:
    f=r['form'];p0,m0,u0=point[f,200];p1,m1,u1=point[f,5000]
    lines.append(f"| {f.title()} | {p0:.4f} / {p1:.4f} | {m0:.4f} / {m1:.4f} | {100*r['total']:.3f} | {100*r['extensive']:.3f} [{100*r['extensive_lo']:.3f}, {100*r['extensive_hi']:.3f}] | {100*r['intensive']:.3f} [{100*r['intensive_lo']:.3f}, {100*r['intensive_hi']:.3f}] |")
lines+=['',f'Intervals use {B:,} draws, seed {SEED}, independent within all nine cells, fixed cell Ns. Zero-positive draws: {invalid}. All cell and bootstrap decomposition identities pass at1e-14. Intervals are pointwise percentile descriptions; no new hypothesis tests or component-significance selection.','', 'Cash arithmetic is dominated by the conditional-positive component, whereas a small increase in the probability of a positive response offsets part of the Food decline. Medical has opposing components and a near-zero total, making contribution percentages misleading. The result clarifies the observed margin pattern relative to size studies; it does not strengthen the statistical form-by-size interaction or identify a psychological account. No further empirical exploration follows.']
(O/'EXTENSIVE_INTENSIVE_NOTE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(d.to_string(index=False));print(meta)
