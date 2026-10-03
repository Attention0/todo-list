"""Execute only the revision manifest. No respondent-level exports."""
from pathlib import Path
import sys, json, hashlib, argparse, time
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
import grid_models as gm
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parent/'mpc_size_curve'))
import size_curve as prior

def write(frame,name):frame.to_csv(OUT/name,index=False)
def data(path):
    d=prior.prepare(path)
    assert [len(d)]+[int(d['sample_'+s].sum()) for s in gm.SAMPLES[1:]]==[5497,5480,5171,2715,1208]
    return d

def main(path):
    t=time.time();manifest=OUT/'revision_spec_manifest.json'
    freeze=hashlib.sha256(manifest.read_bytes()).hexdigest();d=data(path);g=gm.groups(d)
    grid,blocks,focal,diag=gm.run_grid(g)
    assert len(grid)==1500
    write(grid,'specification_grid.csv');write(diag,'model_diagnostics.csv')
    maxes,matrix,sizes=gm.multiplier(g,blocks,5000,20261003)
    grid['global_maxT_p']=[(1+np.sum(maxes>=r.statistic))/5001 if r.status=='ok' else np.nan for r in grid.itertuples()]
    grid['holm_p']=np.nan;ok=grid.status.eq('ok');grid.loc[ok,'holm_p']=multipletests(grid.loc[ok,'p'],method='holm')[1]
    write(grid,'specification_grid.csv')
    focus=grid[(grid['sample']=='R') & (grid.representation=='trend') & (grid.outcome=='top75') & (grid.model=='OLS_HC3')].copy()
    assert len(focus)==5
    write(focus,'maxT_results.csv');write(pd.DataFrame({'draw':range(1,5001),'maximum_statistic':maxes}),'maxT_draw_summary.csv')
    f=focus.rename(columns={'estimand':'estimand_definition','contrast':'estimand'})
    f['role']='form-specific interaction';f['scale']='probability per fivefold'
    focal['holm_p']=multipletests(focal.p,method='holm')[1]
    write(pd.concat([focal,f],ignore_index=True),'table_A1_focal_estimand.csv')
    write(grid[grid.model.str.startswith('ordered')],'ordered_model_sensitivity.csv')
    print('GLOBAL FOCAL',focus[['contrast','estimate','p','global_maxT_p']].to_string(index=False),flush=True)
    # Null simulation with exact multinomial outcomes, common fixed design/membership.
    pooled=d.ordinal.value_counts().reindex(range(1,7),fill_value=0).to_numpy()/len(d)
    ng=g.copy();ng['count']=ng.block_N.to_numpy()*pooled[ng.category.to_numpy()-1]
    _,nb,_,nd=gm.run_grid(ng,verbose=False)
    nm,nmatrix,nsizes=gm.multiplier(ng,nb,5000,20261004)
    critical=np.quantile(nm,.95);rng=np.random.default_rng(20261005)
    noises=[]
    for _ in range(200):
        draws=np.concatenate([rng.multinomial(int(block.block_N.iloc[0]),pooled) for _,block in ng.groupby(['cell','bits'],sort=False)])
        noises.append(draws-ng['count'].to_numpy())
    simmax=gm.max_statistics(nmatrix,nsizes,np.array(noises))
    rejected=simmax>critical;rate=rejected.mean();k=int(rejected.sum());ci=stats.beta.ppf([.025,.975],[k if k else .5,k+1],[200-k+1,200-k if k<200 else .5])
    write(pd.DataFrame(dict(simulation=range(1,201),maximum_statistic=simmax,reject_05=rejected,critical_05=critical)),'maxT_simulation_draws.csv')
    write(pd.DataFrame([dict(simulations=200,rejections=k,empirical_size=rate,lo=ci[0],hi=ci[1],draws_per_calibration=5000,scope='multinomial six-category null, fixed design, score-level family; not repeated optimizer refits',null_models_failed=int(nd.status.ne('ok').sum()))]),'maxT_simulation_check.csv')
    print('NULL SIM',rate,ci,flush=True)
    metadata=dict(freeze_sha256=freeze,raw_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),samples={s:len(d) if s=='R' else int(d['sample_'+s].sum()) for s in gm.SAMPLES},planned_tests=1500,estimable_tests=int(ok.sum()),failed_tests=int((~ok).sum()),planned_models=300,failed_models=int(diag.status.ne('ok').sum()),bootstrap_draws=5000,bootstrap_model_refits=0,bootstrap_nonestimable_fits='not applicable; no draw-level fits; model-level failures in diagnostics',null_simulation_size=float(rate),elapsed_seconds=time.time()-t)
    (OUT/'execution_manifest.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    assert hashlib.sha256(manifest.read_bytes()).hexdigest()==freeze
    print('A complete',metadata,flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);main(ap.parse_args().data)
