"""Aggregate-output acceptance checks; requires no respondent data."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

root = Path(__file__).resolve().parent
cell = pd.read_csv(root / 'cell_summary.csv')
assert len(cell) == 9 and cell.N.sum() == 5497
assert cell.N.tolist() == [619,595,584,614,620,602,615,612,636]
p = cell[[f'p{k}' for k in range(1,7)]].to_numpy()
assert np.allclose(p.sum(axis=1),1)
assert np.allclose(p @ np.arange(1,7),cell.ordinal_mean)
assert np.allclose(p @ [0,.05,.175,.375,.625,.875],cell.midpoint_mean)
assert np.allclose(np.cumsum(p,axis=1),cell[[f'cdf{k}' for k in range(1,7)]])
threshold = pd.read_csv(root / 'threshold_curves.csv')
assert len(threshold) == 45
for i,name in enumerate(['any_spending','ge10','ge25','ge50','top75'],1):
    g = threshold[threshold.threshold.eq(name)].merge(cell,on=['form','amount'])
    assert np.allclose(g.probability,1-g[f'cdf{i}'])
decomp = pd.read_csv(root / 'distribution_decomposition.csv')
for form,g in decomp.groupby('form'):
    c = cell[cell.form.eq(form)].set_index('amount')
    assert np.isclose(g.mean_change_contribution.sum(),c.loc[5000,'midpoint_mean']-c.loc[200,'midpoint_mean'])
    assert np.isclose(g.probability_shift_5000_minus_200.sum(),0)
slopes = pd.concat([pd.read_csv(root/'primary_amount_slopes.csv'),pd.read_csv(root/'differential_slopes.csv')])
assert len(slopes) == 480
family = ['cash','food','medical','food-cash','medical-cash']
for _,g in slopes.groupby(['outcome','sample','specification']):
    h = g[g.estimand.isin(family)]
    assert len(h) == 5 and np.allclose(h.holm_p,multipletests(h.p,method='holm')[1])
    assert np.isfinite(g[['slope','se','lo','hi','p']].to_numpy()).all()
    t = g.set_index('estimand').slope
    assert np.isclose(t['medical-cash'],t.medical-t.cash)
    assert np.isclose(t['medical-food'],t.medical-t.food)
pair = pd.read_csv(root/'pairwise_amount_changes.csv')
for (outcome,form),g in pair.groupby(['outcome','form']):
    c = cell[cell.form.eq(form)].set_index('amount')
    if outcome in ['ordinal','midpoint']:
        for _,row in g.iterrows():
            assert np.isclose(row.change,c.loc[row.amount_high,outcome+'_mean']-c.loc[row.amount_low,outcome+'_mean'])
food = pd.read_csv(root/'food_inframarginal_curve.csv')
assert food[food.screen.eq('likely_binding')].outcome.eq('cell_N').all()
assert food[(food.screen=='likely_binding') & (food.estimand=='5000')].N.item() == 56
ordered = pd.read_csv(root/'ordered_slopes.csv')
assert len(ordered) == 12 and np.isfinite(ordered[['slope','se','lo','hi','p']].to_numpy()).all()
for _,g in ordered.groupby('model'):
    h=g[g.estimand.isin(family)]
    assert np.allclose(h.holm_p,multipletests(h.p,method='holm')[1])
ri = pd.read_csv(root/'randomization_inference.csv')
assert len(ri)==12 and ri.B.eq(5000).all() and ri.permutation_p.between(1/5001,1).all()
assert json.loads((root/'manifest.json').read_text())['sample_N']=={'R':5497,'A':5480,'C':5171,'Q1':2715,'Q2':1208}
for name in ['fig1_ordinal','fig1_midpoint','fig2_distribution','fig3_thresholds','fig4_slopes','fig5_mechanisms']:
    assert (root/'figures'/f'{name}.png').stat().st_size > 10000
for name in ['fig1_source','fig2_source','fig3_source','fig4_source','fig5_food_source','fig5_medical_source']:
    assert len(pd.read_csv(root/f'{name}.csv'))>0
for file in root.glob('*.csv'):
    assert not {'id','respondent_id','fold_id','oof_prediction'}.intersection(pd.read_csv(file,nrows=0).columns)
report=(root.parents[1]/'MPC_SIZE_CURVE_RESULTS.md').read_text(encoding='utf-8')
assert len([line for line in report.splitlines() if line.startswith('### ')]) == 14
print('PASS: design counts, category means/CDFs, thresholds, decomposition, contrasts, Holm, samples, binding nonidentification, figures/source CSVs, aggregate-only schemas.')
