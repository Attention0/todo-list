"""Independent algebra/inference, strict scope, crossfit leakage and artifact tests."""
import argparse,json,re,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import StratifiedKFold
import who_drives as w

def run(data,out):
    out=Path(out);d=w.prior.prepare(data).reset_index(drop=True);X,groups,meta=w.covariates(d);man=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    assert man['N']==5497 and man['samples']==dict(R=5497,A=5480,C=5171,Q1=2715,Q2=1208)
    assert man['raw_sha256']==hashlib.sha256(Path(data).read_bytes()).hexdigest() and not man['individual_exports']
    assert list(groups)==w.TIER1+w.TIER2;assert len([c for v in w.TIER1 for c in groups[v]])==6
    assert np.allclose(X.mean(),0) and np.allclose(X.std(),1)
    for name,variables,number in [('primary_moderator_interactions',w.TIER1,5),('secondary_profile_interactions',w.TIER2,6)]:
        t=pd.read_csv(out/(name+'.csv'));assert set(t.moderator)==set(variables)
        for est in ['cash','restricted-cash']:
            tt=t[t.estimand.eq(est)&t.record_type.eq('omnibus')];assert len(tt)==number;assert np.allclose(tt.holm_p,multipletests(tt.p,method='holm')[1])
        for var in variables:
            # Independent manual HC3 matrix calculation, not wrapper contrasts.
            M=w.design(d,X[groups[var]]);a=M.to_numpy();yy=d.top75.to_numpy();inv=np.linalg.inv(a.T@a);beta=inv@a.T@yy;resid=yy-a@beta;h=np.einsum('ij,jk,ik->i',a,inv,a);cov=inv@(a.T@(((resid/(1-h))**2)[:,None]*a))@inv
            for c in groups[var]:
                for est in ['cash','restricted-cash','food-cash','medical-cash']:
                    v=np.zeros(a.shape[1])
                    for f,ww in zip(w.FORMS,w.FW[est]):v[list(M.columns).index(f+':z:'+c)]=ww
                    r=t[t.moderator.eq(var)&t.column.eq(c)&t.estimand.eq(est)].iloc[0];value=v@beta;se=np.sqrt(v@cov@v)
                    assert np.allclose([r.estimate,r.se,r.p],[value,se,2*stats.norm.sf(abs(value/se))],atol=1e-10)
    cash=pd.read_csv(out/'subgroup_cash_curves.csv');restricted=pd.read_csv(out/'subgroup_restricted_curves.csv');raw=pd.read_csv(out/'subgroup_form_cells.csv');assert len(cash)==len(restricted)==45 and len(raw)==135
    for var,bins in w.bins(d).items():
        c=cash[cash.moderator.eq(var)];assert len(c)==9
        for amount in w.prior.AMT:assert c[c.amount.eq(amount)].N.sum()==len(d[d.form.eq('cash')&d.amount.eq(amount)])
        for group in pd.unique(bins):
            for amount in w.prior.AMT:
                x=raw[(raw.moderator==var)&(raw.group==str(group))&(raw.amount==amount)].set_index('form');r=restricted[(restricted.moderator==var)&(restricted.group==str(group))&(restricted.amount==amount)].iloc[0]
                assert np.allclose(r.probability,.5*(x.loc['food','probability']+x.loc['medical','probability']))
                assert np.allclose(r.se,.5*np.sqrt(x.loc['food','se']**2+x.loc['medical','se']**2))
    ct=pd.read_csv(out/'cash_decline_contributions.csv');assert len(ct)==15
    assert np.allclose(ct.endpoint_change,ct.p5000-ct.p200);assert np.allclose(ct.contribution,ct.population_share*ct.endpoint_change)
    for var,g in ct.groupby('moderator'):
        assert np.isclose(g.population_share.sum(),1);assert np.isclose(g.share_of_total_decline.sum(),1);assert np.allclose(g.partition_standardized_total,g.contribution.sum())
    sl=pd.read_csv(out/'subgroup_differential_slopes.csv')
    for _,g in sl.groupby(['moderator','group']):
        x=g.set_index('estimand');assert np.isclose(x.loc['restricted-cash','estimate'],x.loc['restricted','estimate']-x.loc['cash','estimate'])
        assert np.isclose(x.loc['restricted-cash','estimate'],.5*(x.loc['food-cash','estimate']+x.loc['medical-cash','estimate']))
    jt=pd.read_csv(out/'joint_tests.csv');assert len(jt)==2 and jt.df.eq(6).all();assert np.allclose(jt.holm_two_p,multipletests(jt.p,method='holm')[1])
    j=pd.read_csv(out/'joint_tier1_model.csv');baseline=j[j.model.eq('baseline')].set_index('estimand');old=pd.read_csv(out.parent/'mpc_size_curve/threshold_slope_contrasts.csv');old=old[(old.outcome=='top75')&(old['sample']=='R')&(old.specification=='unadjusted')].set_index('estimand');assert np.isclose(baseline.loc['restricted-cash','estimate'],.5*(old.loc['food-cash','slope']+old.loc['medical-cash','slope']))
    rob=pd.read_csv(out/'moderator_robustness.csv');assert len(rob)==320 and set(rob.moderator)==set(man['robustness_selected']);assert set(rob.outcome)=={'top75','ordinal','midpoint','ge50'};assert rob.holm_p.isna().all()
    for sn,g in rob.groupby('sample'):assert g.N.eq(man['samples'][sn]).all()
    # Independent reconstitution of honest diagnostic and explicit leakage test.
    cols=[c for v in w.TIER1 for c in groups[v]];folds=np.zeros(len(d),int)
    for k,(_,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=w.SEED).split(d,d.cell)):folds[te]=k
    s,cal,pred,q,obs,cf=w.crossfit(d,X[cols],folds,np.ones(len(d)))
    changed=d.copy();changed.loc[folds==0,'top75']=1-changed.loc[folds==0,'top75'];_,_,p2,q2,obs2,_=w.crossfit(changed,X[cols],folds,np.ones(len(d)))
    for target in pred:
        assert np.allclose(pred[target][folds==0],p2[target][folds==0]);assert np.array_equal(q[target][folds==0],q2[target][folds==0])
    for name in obs:assert np.allclose(obs[name][folds==0],obs2[name][folds==0])
    form=pd.Categorical(d.form,categories=w.FORMS).codes;resid=d.top75.to_numpy()-obs['full'];z=d.z.to_numpy()
    for target,weights in [('cash_decline',[-1,0,0]),('restricted_cash_delta',[-1,.5,.5])]:
        ww=np.array(weights);score=(cf[:,:,2]-cf[:,:,0])@ww+9*ww[form]*resid*(np.where(z==1,1,0)-np.where(z==-1,1,0))
        for quint in range(1,6):assert np.isclose(cal[(cal.target==target)&(cal.quintile==quint)].aipw_sensitivity.iloc[0],score[q[target]==quint].mean())
    summary=pd.read_csv(out/'prediction_summary.csv').set_index('statistic');assert np.allclose(summary.loc[list(s),'estimate'],list(s.values()));assert summary.B.eq(499).all();assert np.isclose(summary.loc['full_vs_level_mse_gain','estimate'],summary.loc['level_mse','estimate']-summary.loc['full_mse','estimate'])
    calibration=pd.read_csv(out/'prediction_calibration.csv');assert len(calibration)==10
    for target,g in calibration.groupby('target'):assert g.N.sum()==len(d) and g.predicted_sensitivity.is_monotonic_increasing
    required=['primary_moderator_interactions','secondary_profile_interactions','subgroup_cash_curves','subgroup_restricted_curves','cash_decline_contributions','subgroup_differential_slopes','joint_tier1_model','joint_tests','prediction_calibration','moderator_robustness']
    for name in required:assert (out/(name+'.csv')).exists()
    for f in out.glob('*.csv'):
        t=pd.read_csv(f);assert len(t)<2000;assert not {'id','respondent_id','fold','fold_id','scen_version'}.intersection(t.columns)
        if {'estimate','lo','hi'}.issubset(t):
            c=t[t.estimate.notna()];assert np.isfinite(c[['estimate','lo','hi']]).all().all();assert (c.lo<=c.hi).all()
    for n in range(1,6):assert (out/f'fig{n}_source.csv').exists() and list((out/'figures').glob(f'fig{n}_*.png'))
    report=out.parents[1]/'MPC_WHO_DRIVES_RESULTS.md';sections=re.findall(r'^## (\d+)\. ',report.read_text(encoding='utf-8'),re.M);assert sections==[str(i) for i in range(1,15)]
    print('PASS: scope, HC3 independent matrix, Holm, group/mixture/contribution algebra, baseline reuse, joint, robustness, crossfit leakage/AIPW, aggregate privacy and all artifacts.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('--out',default=str(w.ROOT));a=p.parse_args();run(a.data,a.out)
