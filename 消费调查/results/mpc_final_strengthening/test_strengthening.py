"""Acceptance checks plus optional independent numerical delta-gradient verification."""
from pathlib import Path
import argparse,json
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests
import strengthening as s

root=Path(__file__).resolve().parent
def table(name):return pd.read_csv(root/(name+'.csv'))

def check_outputs():
    pooled=table('restricted_vs_cash_slopes');assert len(pooled)==64
    old=pd.concat([pd.read_csv(root.parents[0]/'mpc_size_curve'/'primary_amount_slopes.csv'),pd.read_csv(root.parents[0]/'mpc_size_curve'/'differential_slopes.csv')])
    for y,g in pooled.groupby('outcome'):
        e=g.set_index('estimand').estimate
        assert np.isclose(e.restricted,.5*(e.food+e.medical))
        assert np.isclose(e['restricted-cash'],e.restricted-e.cash)
        h=g[g.estimand.isin(s.FAMILY)]
        assert np.allclose(h.holm_p,multipletests(h.p,method='holm')[1])
        for f in s.FORMS:
            ref=old[(old.outcome==y)&(old['sample']=='R')&(old.specification=='unadjusted')&(old.estimand==f)]
            assert np.isclose(e[f],ref.slope.item())
    binary=table('threshold_logit_probit');assert len(binary)==160
    for _,g in binary.groupby(['outcome','model','scale']):
        h=g[g.estimand.isin(s.FAMILY)];assert np.allclose(h.holm_p,multipletests(h.p,method='holm')[1])
        e=g.set_index('estimand').estimate;assert np.isclose(e['restricted-cash'],.5*(e['food-cash']+e['medical-cash']))
    profile=table('threshold_joint_profile');tails=table('threshold_tail_specificity');assert len(profile)==15 and len(tails)==12
    for name,g in tails.groupby('contrast'):
        assert np.allclose(g.holm_p,multipletests(g.p,method='holm')[1])
        p=profile[profile.contrast.eq(name)].set_index('threshold').estimate
        for _,row in g.iterrows():assert np.isclose(row.estimate,p.top75-p[row.comparison.replace('top75-minus-','')])
        cov=pd.read_csv(root/(name+'_threshold_covariance.csv'),index_col=0).to_numpy()
        assert np.allclose(cov,cov.T) and np.linalg.eigvalsh(cov).min()>0
    relative=table('top_tail_relative_change');assert len(relative)==21 and relative.B.eq(5000).all()
    for scale in ['risk_ratio','odds_ratio']:
        q=relative[relative.scale.eq(scale)].set_index('estimand').estimate
        for f in ['food','medical','restricted']:
            observed=relative[(relative.estimand==f+'-cash')&(relative.scale=='ratio_of_'+scale+'s')].estimate.item()
            assert np.isclose(observed,q[f]/q.cash)
    h=relative[relative.role.eq('between_form_comparison')];assert np.allclose(h.holm_p,multipletests(h.p,method='holm')[1])
    multi=table('multinomial_probability_checks');assert len(multi)==54
    assert np.allclose(multi.groupby(['form','amount']).predicted_probability.sum(),1)
    assert np.allclose(multi.groupby(['form','amount']).raw_probability.sum(),1)
    grid=table('specification_curve');assert len(grid)==420
    keys=['sample','adjustment','amount_representation','coding','estimand'];assert not grid.duplicated(keys).any()
    assert all(grid.groupby('sample').size()==84)
    assert np.isfinite(grid[['estimate','se','lo','hi','p','comparable_estimate']].to_numpy()).all()
    ratio=np.where(grid.amount_representation.eq('trend'),1,2)
    assert np.allclose(grid.estimate/ratio,grid.comparable_estimate)
    assert len(table('model_diagnostics'))==140 and table('model_diagnostics').converged.all()
    cells=table('implied_yuan_cells');assert len(cells)==12
    assert np.allclose(cells.midpoint*cells.amount,cells.implied_yuan)
    assert np.allclose(cells.midpoint_lo*cells.amount,cells.yuan_lo)
    scaling=table('implied_yuan_scaling');assert len(scaling)==7
    for f in s.FORMS+['restricted']:
        x=cells[cells.form.eq(f)].set_index('amount');eta=np.log(x.loc[5000,'implied_yuan']/x.loc[200,'implied_yuan'])/np.log(25)
        assert np.isclose(eta,scaling[scaling.estimand.eq(f)].eta.item())
    assert len(table('constant_dollar_benchmark'))==3 and len(table('restricted_form_heterogeneity'))==4
    for fig in ['A','B','C','D','E']:
        assert len(table('fig'+fig+'_source'))>0
        assert len(list((root/'figures').glob('fig'+fig+'*.png')))==1
    manifest=json.loads((root/'manifest.json').read_text());assert manifest['B']==5000 and manifest['specifications']==420 and manifest['individual_exports'] is False
    for file in root.glob('*.csv'):
        assert not {'id','respondent_id','fold_id','oof_prediction'}.intersection(pd.read_csv(file,nrows=0).columns)
    report=(root.parents[1]/'MPC_FINAL_STRENGTHENING_RESULTS.md').read_text(encoding='utf-8')
    assert len([line for line in report.splitlines() if line.startswith('## ')])==10
    assert 'plausible main story but must be written as suggestive' in report
    print('PASS: PR9 replication/algebra, Holm families, joint covariance, ratios, 420-grid completeness, finite/converged models, scaling, figures/source CSVs, aggregate-only schemas.')

def numerical_check(data):
    d=s.prior.prepare(data)
    for link in ['logit','probit']:
        for representation in ['trend','endpoint']:
            m=s.fit_glm('top75',d,representation=representation,link=link)
            for f in s.FORMS:
                _,grad=s.probability_function(m,link,f,representation);numeric=[]
                for j in range(len(m.params)):
                    plus=np.asarray(m.params).copy();minus=plus.copy();step=1e-6/(1+np.abs(m.model.exog[:,j]).max())
                    plus[j]+=step;minus[j]-=step
                    vp=s.probability_function(m,link,f,representation,params=plus)[0]
                    vm=s.probability_function(m,link,f,representation,params=minus)[0]
                    numeric.append((vp-vm)/(2*step))
                assert np.allclose(grad,numeric,rtol=2e-4,atol=1e-7),(link,representation,f)
    point,draws,sizes=s.cell_bootstrap(d)
    z=np.array([-1,0,1]);zbar=(sizes*z).sum(1)/sizes.sum(1);weights=sizes*(z-zbar[:,None]);weights/=(sizes*(z-zbar[:,None])**2).sum(1)[:,None]
    pp=1-np.cumsum(point,axis=-1)[...,:5];analytic=np.zeros((5,5));w=np.array([-1,.5,.5])
    for f in range(3):
        for a in range(3):
            p=pp[f,a];cellcov=np.minimum.outer(p,p)-np.outer(p,p);analytic+=w[f]**2*weights[f,a]**2*cellcov/sizes[f,a]
    empirical=pd.read_csv(root/'restricted-cash_threshold_covariance.csv',index_col=0).to_numpy()
    assert np.linalg.norm(empirical-analytic)/np.linalg.norm(analytic)<.08
    print('PASS: logit/probit trend/endpoint analytic gradients versus numerical derivatives; joint-bootstrap covariance versus analytic nested-indicator covariance.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--data');args=parser.parse_args();check_outputs()
    if args.data:numerical_check(args.data)
