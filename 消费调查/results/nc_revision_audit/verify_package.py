"""Independent estimator and package consistency checks; no new specification."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from scipy import stats
from scipy.optimize._numdiff import approx_derivative
from PIL import Image
from pypdf import PdfReader
import grid_models as gm
from run_revision import data,OUT
from secondary import covariates

def main(path):
    results={};d=covariates(data(path));grid=pd.read_csv(OUT/'specification_grid.csv');g=gm.groups(d)
    def check(name,condition,details=''):
        results[name]={'passed':bool(condition),'details':details}
        if not condition:raise AssertionError(name+': '+str(details))
    freeze=hashlib.sha256((OUT/'revision_spec_manifest.json').read_bytes()).hexdigest()
    check('manifest_unchanged',freeze=='6b1e95952886d4cc0a245579d03fe72b40e79f7c925669cd1f5ba40c9cc87375',freeze)
    check('grid1500_unique_estimable',len(grid)==1500 and grid.spec_id.nunique()==1500 and grid.status.eq('ok').all())
    diag=pd.read_csv(OUT/'model_diagnostics.csv');check('all300_models_converged',len(diag)==300 and diag.status.eq('ok').all() and (diag.full_gradient<1e-5).all() and (diag.null_gradient<1e-5).all() and (diag.full_hessian_min>0).all() and (diag.null_hessian_min>0).all())
    counts={s:len(d) if s=='R' else int(d['sample_'+s].sum()) for s in gm.SAMPLES}
    check('sample_counts',list(counts.values())==[5497,5480,5171,2715,1208],counts)
    # Original individuals, independent statsmodels formula-free OLS/GLM engine.
    errs=[]
    for rep in gm.REPS:
        dd=d[d.amount.ne(1000)] if rep=='endpoint' else d
        X,ix=gm.design(dd.cell,rep)
        for y in gm.OUTCOMES:
            m=sm.OLS(dd[y].to_numpy(),X).fit(cov_type='HC3')
            part=grid[(grid['sample']=='R')&(grid.representation==rep)&(grid.outcome==y)&(grid.model=='OLS_HC3')]
            C=gm.matrices(X.shape[1],ix,rep,len(m.params))
            for r in part.itertuples():
                e=C[r.contrast]@m.params;v=C[r.contrast]@m.cov_params()@C[r.contrast].T
                errs.extend(np.abs(e-np.array(json.loads(r.profile))))
                errs.extend(np.abs((e-1.96*np.sqrt(np.diag(v)))-np.array(json.loads(r.profile_lo))))
    check('independent_OLS_all7Y_3dose_5contrasts',max(errs)<1e-8,{'max_abs_estimate_CI_error':float(max(errs)),'comparison_count':len(errs)})
    X,ix=gm.design(d.cell,'trend');groupX,gix=gm.design(g.cell,'trend')
    for link in ['logit','probit']:
        m=sm.GLM(d.top75,X,family=sm.families.Binomial(link=sm.families.links.Logit() if link=='logit' else sm.families.links.Probit())).fit(cov_type='HC1')
        grouped=gm.fit(groupX,gm.yvals(g.category,'top75'),g['count'].to_numpy(),link,gix)
        # statsmodels GLM HC1 does not always apply N/(N-k); compare MLE parameters only.
        check('independent_'+link+'_MLE',np.max(np.abs(m.params-grouped['params']))<1e-5,{'max_abs_param_error':float(np.max(np.abs(m.params-grouped['params'])))})
    X,ix=gm.design(d.cell,'trend',True);gx,gix=gm.design(g.cell,'trend',True)
    for link in ['logit','probit']:
        m=OrderedModel(d.ordinal.to_numpy(),X,distr=link).fit(method='bfgs',disp=False,gtol=1e-8,maxiter=600)
        grouped=gm.fit(gx,g.category.to_numpy(),g['count'].to_numpy(),'ordered_'+link,gix)
        error=float(np.max(np.abs(m.params-grouped['params'])))
        check('independent_ordered_'+link+'_MLE',error<1e-5,{'max_abs_param_error':error})
    # Analytic category log-probability scores compared to finite differences including scale.
    grad_errors={}
    for link,scale in [('logit',False),('probit',False),('probit',True)]:
        name='ordered_location_scale' if scale else 'ordered_'+link
        fit=gm.fit(gx,g.category.to_numpy(),g['count'].to_numpy(),name,gix)
        pr,score=gm.ordered_score(fit['params'],gx,g.category.to_numpy(),link,scale)
        num=approx_derivative(lambda p:np.log(gm.ordered_score(p,gx,g.category.to_numpy(),link,scale)[0]),fit['params'],method='3-point')
        grad_errors[name]=float(np.max(np.abs(num-score)))
    check('ordered_analytic_scores',max(grad_errors.values())<1e-5,grad_errors)
    draws=pd.read_csv(OUT/'maxT_draw_summary.csv');check('5000_finite_shared_draws',len(draws)==5000 and np.isfinite(draws.maximum_statistic).all())
    p=np.array([(1+(draws.maximum_statistic>=r.statistic).sum())/5001 for r in grid.itertuples()])
    check('globalP_recomputed_from_draws',np.max(np.abs(p-grid.global_maxT_p))<1e-12)
    sim=pd.read_csv(OUT/'maxT_simulation_check.csv').iloc[0];check('null_simulation_score_size',sim.simulations==200 and sim.rejections==7 and sim.lo<.05<sim.hi,'Score-level only; does not test model-refit size.')
    fixed=d[d.form.isin(['cash','food']) & (d.food_lower6>5000)]
    check('fixed_inframarginal_baseline_only',len(fixed)==2815,{'N':len(fixed)})
    bt=pd.read_csv(OUT/'bindingness_ratio_tests.csv');check('finite_binding_family75',len(bt)==75 and bt.p.notna().all())
    cv=pd.read_csv(OUT/'relative_scale_cv.csv');fold=pd.read_csv(OUT/'relative_scale_cv_folds.csv')
    check('relative_grid45_and450_model_fold_rows',len(cv)==45 and len(fold)==450,{'CV_rows':len(cv),'fold_rows':len(fold)})
    check('no_material_loss_improvement',cv.relative_improvement.max()<.01,{'maximum':float(cv.relative_improvement.max())})
    theory=pd.read_csv(OUT/'theory_moderators.csv');power=pd.read_csv(OUT/'moderator_power_mde.csv');control=pd.read_csv(OUT/'positive_controls.csv')
    check('moderator36_power36_control9',len(theory)==36 and len(power)==36 and len(control)==9)
    check('MDE_formula',np.allclose(power.MDE_80,(stats.norm.ppf(.975)+stats.norm.ppf(.8))*power.se_actual_HC3))
    check('controls_sign_not_redefined',control.expected_sign.eq('negative').all() and control[control.control=='income_rank_z'].estimate.gt(0).all())
    ref=pd.read_csv(OUT/'reference_audit.csv');check('reference30_verified_metadata',len(ref)==30 and ref.verified.str.startswith('YES').all(),'Metadata/title identity only; bounded scientific claims remain qualified.')
    qq=pd.read_csv(OUT/'allx_supplemental_counts.csv');check('allx_reused6_primary_families',len(qq)==6 and qq.q_10.eq(0).all() and qq.q_05.eq(0).all())
    images={}
    for pdf in sorted(OUT.glob('fig_*.pdf')):
        p=PdfReader(pdf);im=Image.open(pdf.with_suffix('.png'));dpi=im.info.get('dpi');svg=pdf.with_suffix('.svg').read_text(encoding='utf-8')
        text=p.pages[0].extract_text();images[pdf.name]={'pages':len(p.pages),'png_pixels':im.size,'dpi':dpi,'text_chars':len(text)}
        check(pdf.stem+'_formats',len(p.pages)==1 and '<text' in svg and len(text)>30 and dpi and min(dpi)>599)
    check('seven_pdf_figures',len(images)==7,images)
    expected=json.loads((OUT/'input_checksums.json').read_text(encoding='utf-8'))
    check('raw_docs_history_unmodified_since_inventory',all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in expected.items()))
    rawhash=hashlib.sha256(Path(path).read_bytes()).hexdigest();execution=json.loads((OUT/'execution_manifest.json').read_text())
    check('raw_unchanged_since_analysis',rawhash==execution['raw_sha256'],rawhash)
    # Never export identifiers/person fold assignments/raw scenario answers.
    forbidden={'id','respondent_id','person_id','scen_mpc','q32_cash200','q33_cash1k','q34_cash5k','q35_vouch200'}
    check('aggregate_csv_no_person_identifiers',all(not(forbidden&set(pd.read_csv(p,nrows=0).columns)) for p in OUT.glob('*.csv')))
    payload={'date':'2026-10-03','all_assertions_passed':all(x['passed'] for x in results.values()),'checks':results,'limitations':['No raking or response-time/process test: NOT FEASIBLE','Missing ethics/minor/recruitment documentation: not passed','Score-level null simulation, not full model-refit validation','Paired CV intervals ignore training dependence'],'visual_QA':'See figure_audit.md; separately rendered and visually inspected, not inferred from assertions.'}
    (OUT/'verification_results.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Verified',len(results),'assertions; see explicit limitations.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);main(p.parse_args().data)
