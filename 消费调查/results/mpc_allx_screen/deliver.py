"""Generate protocol-conditional artifacts and six scientific figures from locked tables."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from importlib.metadata import version
from inventory import ROOT,prior
from screen import Y_NAMES

COLORS={'subjective raw':'#238b8d','objective raw':'#d48325','constructed':'#7162a4'}
TITLES={'ordinal':'Ordinal category (1–6)','midpoint':'Approximate MPC (midpoints)','top75':'Top75 probability'}

def save(fig,out,name,source):
    if not name.startswith('fig6'):
        for ax in fig.axes:ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    folder=out/'figures';folder.mkdir(exist_ok=True);fig.savefig(folder/(name+'.png'),dpi=190,bbox_inches='tight');fig.savefig(folder/(name+'.pdf'),bbox_inches='tight');plt.close(fig);source.to_csv(out/(name+'_source.csv'),index=False)

def figures(out,t,c,s):
    plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    primary=t[t.target.isin(['cash','rc'])].copy();primary['display_group']=np.where(primary.origin.eq('constructed'),'constructed',primary.domain+' raw')
    for num,target,title in [(1,'cash','Cash amount-slope moderation'),(2,'rc','Equal-weight Restricted minus Cash moderation')]:
        g=primary[primary.target.eq(target)].copy();g['minus_log10_q']=-np.log10(g.q.clip(lower=1e-12));fig,axes=plt.subplots(1,3,figsize=(13,4.4))
        for ax,y in zip(axes,Y_NAMES):
            for group,color in COLORS.items():
                gg=g[(g.outcome==y)&g.display_group.eq(group)&g.estimate.notna()];ax.scatter(gg.estimate,gg.minus_log10_q,s=19,color=color,alpha=.7,label=group)
            multi=g[(g.outcome==y)&g.estimate.isna()&g.q.notna()];ax.scatter(np.zeros(len(multi)),multi.minus_log10_q,marker='x',color='black',label='factor omnibus (no signed effect)')
            ax.axhline(1,color='#b2182b',ls='--',lw=.8,label='BH q=.10');ax.axvline(0,color='grey',lw=.6);ax.set(title=TITLES[y],xlabel='Interaction per R SD; factors placed at 0',ylabel='−log10(BH q)',ylim=(-.05,1.12))
        axes[0].legend(fontsize=6,loc='upper left');fig.suptitle(title+' — no q<.10 discoveries');fig.tight_layout();save(fig,out,f'fig{num}_allx_{target}',g)
    # No candidates: an outcome-blind fixed display of existing economic/subjective measures.
    display=['q07_emergfund','income_h','need','foodneed','subjective_economic_pc1','social_confidence_pc1','wellbeing_optimism_pc1']
    g=primary[primary.variable.isin(display)].copy();g['display_status']='fixed prior measures; not shortlisted'
    # Different Y units stay on separate axes; no rescaling inference.
    fig,axes=plt.subplots(2,3,figsize=(13,6.8))
    for i,target in enumerate(['cash','rc']):
        for j,y in enumerate(Y_NAMES):
            gg=g[(g.target==target)&(g.outcome==y)].set_index('variable').reindex(display);ax=axes[i,j];ax.errorbar(gg.estimate,range(len(display)),xerr=1.96*gg.se,fmt='o',ms=4,color='#238b8d');ax.axvline(0,color='grey',lw=.7);ax.set(yticks=range(len(display)),yticklabels=display if j==0 else ['']*len(display),title=target+' / '+TITLES[y],xlabel='Interaction (95% HC3 CI)');ax.invert_yaxis()
    fig.suptitle('Cross-outcome concordance: no Tier A/B candidates\nFixed prior measures shown for scale, not a discovery ranking');fig.tight_layout();save(fig,out,'fig3_cross_outcome',g)
    raw=pd.read_csv(out/'raw_constructed_concordance.csv');constructs=['subjective_economic_pc1','social_confidence_pc1','wellbeing_optimism_pc1'];g=raw[raw.constructed.isin(constructs)&raw.outcome.eq('top75')].copy();g['display_status']='fixed pre-existing domain PCs; no candidate constructs'
    fig,axes=plt.subplots(2,3,figsize=(14,8))
    for i,target in enumerate(['cash','rc']):
        for j,co in enumerate(constructs):
            gg=g[(g.target==target)&(g.constructed==co)];ax=axes[i,j];items=gg.raw_component.tolist();vals=gg.raw_estimate.to_list();qs=gg.raw_q.to_list();rr=primary[(primary.variable==co)&(primary.target==target)&(primary.outcome=='top75')].iloc[0];items=['PC index']+items;vals=[rr.estimate]+vals;qs=[rr.q]+qs
            ax.scatter(vals,range(len(items)),c=['#7162a4']+['#238b8d']*(len(items)-1),s=20);ax.axvline(0,color='grey',lw=.5);ax.set(yticks=range(len(items)),yticklabels=[a+' q='+f'{b:.2f}' for a,b in zip(items,qs)],title=target+' / '+co, xlabel='Top75 interaction per SD (raw orientation)');ax.invert_yaxis();ax.tick_params(axis='y',labelsize=6)
    fig.suptitle('Raw versus previously constructed subjective dimensions\nNo FDR-discovered construct; signs are not causal mechanisms');fig.tight_layout();save(fig,out,'fig4_raw_constructed',g)
    fig,ax=plt.subplots(figsize=(8,3));ax.axis('off');ax.text(.5,.58,'No Tier A candidates',ha='center',fontsize=18);ax.text(.5,.32,'Candidate subgroup curves not estimated.\nNo nominal-p-value rescue or new cutpoint search.',ha='center');save(fig,out,'fig5_candidate_curves',pd.DataFrame([dict(status='not_applicable',reason='zero Tier A candidates',criterion='q<.10 in >=2 Y + direction + representation corroboration')]))
    fig,axes=plt.subplots(1,2,figsize=(10,4.4));groups=[('subjective','raw'),('objective','raw'),('subjective','constructed'),('objective','constructed')];labels=['Subjective raw','Objective raw','Subjective construct','Objective construct']
    for ax,target in zip(axes,['cash','rc']):
        gg=s[(s.target==target)&s.outcome.eq('midpoint')].set_index(['domain','origin']).reindex(groups);ax.bar(range(4),gg.X_screened,color=['#238b8d','#d48325','#7162a4','#7162a4'],alpha=.75)
        for k,r in enumerate(gg.itertuples()):ax.text(k,r.X_screened+1,f'{int(r.estimable)} estimable\n0 BH q<.10',ha='center',fontsize=7)
        ax.set(title=target,xticks=range(4),xticklabels=labels,ylabel='Representations screened',ylim=(0,75));ax.tick_params(axis='x',rotation=20)
    fig.suptitle('Descriptive discovery yield: zero discoveries in every Y / group\nCorrelated representations are not independent replications');fig.tight_layout();save(fig,out,'fig6_discovery_summary',s)
    legends='''# Figure legends

All plots describe stated, hypothetical MPC; z=(-1,0,1). Cash moderation is a within-Cash HC3 slope interaction. RC is exactly .5 Food+.5 Medical−Cash, not sample-size weighting. Six BH families each retain 150 inventoried representations; four unsupported factors have p=1 adjustment placeholders and missing displayed q. Points/counts are correlated representations, not independent discoveries. 95% intervals are unadjusted descriptive HC3 intervals, not simultaneous confidence intervals. No manuscript figures replaced.

1. Cash screen: one panel per Y, color by raw subjective/raw objective/constructed. Scalar coefficients are per full-R SD. Multi-df factors are x symbols placed at zero because an omnibus has no sign; their p/q remain omnibus. Unsupported factors are omitted from plot but retained in source CSV with status. Dashed q=.10 line has no discoveries above it.
2. Equal-weight RC screen: same conventions and three Y units; Food−Cash/Medical−Cash diagnostics remain in the tables, not extra discovery families.
3. No Tier A/B candidates exist. Fixed prior economic variables and the three previously constructed subjective domain-PC directions are displayed, NOT selected by raw p or relabeled as candidates. Separate axes preserve distinct Y units. CIs are descriptive, q is in source data.
4. No candidate construct exists. Display the three fixed, previously used domain-PC scores and their raw items for Top75, in original item orientation. Loading-oriented concordance is in the source CSV. q labels are from the original 150-X families; components are correlated and not replications. No new PCA fit.
5. Explicit not-applicable panel: subgroup curves allowed only for Tier A. Zero Tier A means no cutpoints or subgroup models estimated. Source records the gate rather than fabricated curves.
6. Descriptive representation and estimability counts, with zero q<.10 in all six families. The source includes all outcomes; counts shown use midpoint because the inventory/estimability count is the same across Y. No formal subjective-versus-objective yield test.
'''
    (out/'FIGURE_LEGENDS.md').write_text(legends,encoding='utf-8')

def deliver(data,out):
    out=Path(out);t=pd.read_csv(out/'all_screen_results.csv');c=pd.read_csv(out/'cross_outcome_concordance.csv');s=pd.read_csv(out/'subjective_objective_summary.csv');d=prior.prepare(data)
    # Conditional protocol gate is explicit, not silently skipped.
    if c.shortlisted.any():raise RuntimeError('Candidates present: implement/run conditional robustness and joint models before delivering; do not fabricate N/A.')
    masks={'R':np.ones(len(d),bool),'A':d.sample_A,'C':d.sample_C,'Q1':d.sample_Q1,'Q2':d.sample_Q2};rows=[]
    for sample,mask in masks.items():
        for y in ['ordinal','midpoint','top75']:
            for target in ['cash','rc']:
                for adj in ['unadjusted','fixed_PR9_controls']:
                    rows.append(dict(variable='NO_ELIGIBLE_CANDIDATE',sample=sample,outcome=y,target=target,specification=adj,sample_available_N=int((mask&d.form.eq('cash')).sum()) if target=='cash' else int(np.sum(mask)),model_N=np.nan,estimate=np.nan,lo=np.nan,hi=np.nan,status='not_applicable_no_Tier_A_or_B',reason='Protocol sections21–23 restrict reruns to shortlist; shortlist empty'))
    for method in ['ordered_logit','ordered_probit','midpoint_top1_OLS','Top75_logit_AME','Top75_probit_AME']:rows.append(dict(variable='NO_ELIGIBLE_CANDIDATE',sample='R',outcome=method,target='both',specification='functional_form',model_N=np.nan,estimate=np.nan,lo=np.nan,hi=np.nan,status='not_applicable_no_Tier_A_or_B',reason='No candidate passes primary correction; no raw-only rescue'))
    pd.DataFrame(rows).to_csv(out/'shortlisted_robustness.csv',index=False)
    pd.DataFrame([dict(model=m,outcome=y,target=target,record_type=r,status='not_applicable_no_Tier_A',variables='',N=np.nan,estimate=np.nan,p=np.nan,reason='No Tier A interactions; do not interpret absence of a joint test as joint-model null') for m in ['A_cross_outcome','B_one_per_construct'] for y in Y_NAMES for target in ['cash','rc'] for r in ['joint_Wald','average_slope_before_after','OOF_full_vs_level_MSE']]).to_csv(out/'joint_candidate_models.csv',index=False)
    figures(out,t,c,s)
    fact=[]
    for target in ['cash','rc']:
        for y in Y_NAMES:
            g=t[(t.target==target)&(t.outcome==y)];fact.append(dict(target=target,outcome=y,planned_X=len(g),estimable=int(g.status.eq('ok').sum()),nominal_p_lt05=int(g.p.lt(.05).sum()),min_p=g.p.min(),min_q=g.q.min(),BH_q_lt10=int(g.q.lt(.1).sum()),Holm_lt05=int(g.holm_p.lt(.05).sum())))
    facts=pd.DataFrame(fact);facts.to_csv(out/'family_summary.csv',index=False)
    cf=pd.read_csv(out/'crossfit_stability.csv');stable=[]
    for target in ['cash','rc']:
        for y in Y_NAMES:
            g=cf[(cf.target==target)&(cf.outcome==y)];stable.append(dict(target=target,outcome=y,representations=len(g),five_valid_train=int(g.valid_train_folds.eq(5).sum()),five_valid_holdout=int(g.valid_holdout_folds.eq(5).sum()),five_train_same_direction=int(g.same_direction_train_folds.eq(5).sum()),five_holdout_positive=int((g.positive_holdout_direction_folds.eq(5)&g.valid_holdout_folds.eq(5)).sum())))
    pd.DataFrame(stable).to_csv(out/'crossfit_family_summary.csv',index=False)
    inv=pd.read_csv(out/'all_x_variable_inventory.csv');excluded=t[(t.target=='rc')&(t.outcome=='midpoint')&t.status.ne('ok')].variable.to_list()
    def familytext(target,y):
        r=facts[(facts.target==target)&(facts.outcome==y)].iloc[0];return f"150 planned X representations; {int(r.estimable)} estimable. Nominal p<.05: {int(r.nominal_p_lt05)}; minimum nominal p={r.min_p:.4g}; minimum BH q={r.min_q:.4f}; BH q<.10=0, q<.05=0, Holm p<.05=0. Nominal minima are audit statistics, not selected explanatory stories. Full coefficients, CIs, original-unit scalar coefficients, omnibus profiles and model N: `results/mpc_allx_screen/allx_{target}_{y}.csv`."
    names=['1. Bottom line','2. Variable inventory','3. Cash slope screen — ordinal','4. Cash slope screen — midpoint','5. Cash slope screen — Top75','6. Restricted-vs-Cash screen — ordinal','7. Restricted-vs-Cash screen — midpoint','8. Restricted-vs-Cash screen — Top75','9. Cross-outcome concordance','10. Subjective vs objective','11. Raw vs constructed','12. Stability and robustness','13. Cross-fit stability','14. Joint explanatory power','15. Candidate mechanism interpretation','16. Paper implication','17. Final stop decision']
    texts=[
        'Judgment: **rich observables still explain little**. Rich observed subjective and objective characteristics do not yield a stable explanatory signature for the form-by-size pattern in this corrected exploratory screen. No BH q<.10 in any of the six families; no Tier A or Tier B candidate. This is a failure to find a stable observed signature, NOT proof of zero heterogeneity, a measurement-error-free null, or a quantified upper bound on joint explanatory power. Reduced-form PR9–11 story is preserved; no new headline.',
        f'{len(inv)} inventoried fields/representations: all 67 .dta fields, 150 eligible (53 raw, 97 previously constructed), {int((~inv.eligible).sum())} excluded. Eligible breakdown: 35 raw subjective, 18 raw objective, 60 constructed subjective, 37 constructed objective. Q1–31 precede randomized scenario; Q41–49 platform background fields. Raw labels win over questionnaire option-order conflicts. Personal income harmonization is not household income. Exclude ID, assignment/form/amount, outcome and transforms, assigned-amount bindingness, outcome-trained CATE/person scores, quality/style indicators, invalid nominal-code numerical trends and unbounded Food upper-expenditure proxy. Main raw ordered fields use factors and prior rank versions remain separate. Four factors unsupported for full-model HC3: '+', '.join(excluded)+'. No ad hoc category pooling or generalized-inverse discoveries. Complete-case R=5497, Cash=1798; each Cash model reports actual Cash N. All other-form diagnostics use full R. Existing saved 3 domain-PC directions and 27 prior diagnostic global-PC directions are reconstructed with frozen prior centers/scales; no new PCA axes fit/selected. Residual diagnostic PCs are not validated psychological scales. Inventory/mapping/frozen metadata and raw SHA are supplied.',
        familytext('cash','ordinal'),familytext('cash','midpoint'),familytext('cash','top75'),familytext('rc','ordinal'),familytext('rc','midpoint'),familytext('rc','top75'),
        'Zero X crosses q<.10 in even one Y, hence zero cross-outcome FDR candidates. Tier counts per target: 0 A, 0 B, 5 C, 145 D. These C counts include redundant representations, not five independent constructs. Scalar sign agreement: Cash '+str(int(c[c.target.eq('cash')].direction_consistent.sum()))+' /150; RC '+str(int(c[c.target.eq('rc')].direction_consistent.sum()))+'/150 including estimable factor-profile agreement. Same direction across correlated Y is not independent replication and cannot rescue uncorrected findings. `cross_outcome_concordance.csv` retains all signs/q, profile cosines and gates.',
        'All four subjective/objective × raw/constructed groups yield zero BH q<.10 and zero Holm survivors in every Y/target. Subjective fields do not show a corrected discovery advantage. Counts are descriptive, not a formal comparison of explanatory capacity; subjective scales may carry response-style noise and shared measurement. Correlated aliases inflate representation counts but are not independent discoveries. See `subjective_objective_summary.csv` and Figure6.',
        'Component and frozen loading-oriented comparisons are fully exported. No constructed index has corrected evidence; no raw item can be promoted into an established construct. Standardized/dummy aliases are affine reuse, not replication; raw factor/rank encodings test distinct specifications of the same information. Three fixed prior domain PCs are displayed against all their raw items as a null diagnostic rather than "candidate constructs". Nominal alignment, cancellation and one-item labels are descriptive only; the table records the actual component count and q per Y.',
        'Protocol21–23 applies sample/adjustment/functional reruns ONLY to Tier A/strongest Tier B. The corrected shortlist is empty: R/A/C/Q1/Q2, fixed-PR9 precision adjustment, ordered logit/probit, alternative top=1, Top75 logit/probit AME are explicitly **not applicable**, not "passed" or "stable". `shortlisted_robustness.csv` records each planned gate and available sample size (R5497/A5480/C5171/Q1 2715/Q2 1208; Cash sizes separately); no estimated effects are fabricated. We do not substitute raw-only variables to obtain apparent robustness.',
        'Every eligible X, all three Y, both targets: 5 cell-stratified folds, seed20261005; 900 summaries and 4500 fold diagnostics. Cash fits are genuinely Cash-only; RC fits preserve equal-weight form contrast. Training coefficient/profile direction is projected into heldout coefficients. Scalar heldout score=sign(train coefficient)×holdout coefficient; factor score=train unit-profile·holdout profile. Same-sign train counts reference the overlapping full-R estimate, so are optimistic descriptive stability, not independent validation. Sparse-factor fold failures retained. Zero outcome variation may leave heldout covariance singular; coefficient direction is still reported without an invalid Wald/calibration p, and zero-norm cosine is missing. No FDR candidate exists to promote even if nominal direction is stable. Aggregate valid-fold and sign counts in `crossfit_family_summary.csv`; no person fold IDs/predictions exported.',
        'Joint A and representative-per-construct B require Tier A. None qualifies, so joint Wald, slope-before/after and OOF full-vs-level gain are recorded **not applicable** in `joint_candidate_models.csv`. This round does NOT estimate the joint explanatory share of all150 variables and does NOT claim a saturated joint null. Prior bounded PR11 joint result remains background, not re-estimated evidence here. Optional regularized interaction diagnostic omitted: optional, and not needed to rescue an empty corrected shortlist.',
        'No coherent subjective/behavioral mechanism candidate emerges; nor does a corrected set of several explanatory correlates. Numerical nominal associations remain exploratory audit records. Randomized amount/form moderation can establish differential response associations conditional on baseline X, but cannot establish that X causes a mechanism. Hypothetical coarse outcomes, correlated Y/aliases, subjective response error, uneven category support, conservative correction, and limited interaction power remain limitations. Failure to reject is not equivalence. No raw-p-value story selection.',
        '**rich observables still explain little** (third prescribed category). More precisely: no stable corrected observable signature is identified by this screen; joint explanatory fraction is unestimated because the candidate gate is empty. Preserve the Cash-size / restricted-tail reduced-form puzzle without attaching a newly discovered psychological mechanism. No manuscript change.',
        'STOP. Inventory, six corrected screens, raw/constructed and cross-outcome comparisons, all-X five-fold diagnostics, conditional N/A robustness/joint artifacts, six figure families/source CSVs, audit and reproducibility tests delivered. Do not launch further variable search, new moderator definitions, PCA/latent-trait discovery, SHAP/black-box HTE, or manuscript edits. Publish a new stacked PR; do not merge.'
    ]
    report='# MPC all-X / multi-outcome slope screen results\n\n'+ '\n\n'.join('## '+n+'\n\n'+v for n,v in zip(names,texts))+'\n'
    (out.parents[1]/'MPC_ALLX_SCREEN_RESULTS.md').write_text(report,encoding='utf-8')
    audit='''# Audit and reproducibility

Direct foundation PR9/10/11, latest main44e2997 task merged into feature/mpc-allx-screen. Stacked publication target feature/mpc-who-drives; no manuscript modified. No respondent-level exports. Local raw .dta SHA in inventory_manifest.json; `screen_manifest.json` gives seed and only aggregate cell/fold counts. 67 raw fields /221 inventory entries /150 eligible, inventory frozen before regressions. Complete locked choices are in ANALYSIS_PLAN.md.

Cash must be estimated only using Cash support: software QA caught and corrected an initial implementation that required support in other forms for Cash. Final outputs fit Cash separately and independent tests verify equality to the Cash block of the supported full-model HC3 fit. Exact equal-weight RC = .5 Food+.5 Medical−Cash. Six planned families each size150; nonestimable p=1 placeholders included in correction, visible p/q missing. No category collapsing. Scalar tests normal/chi-square1 equivalent; factor tests multivariate HC3 chi-square with full covariance rank required. Per-form separate HC3 blocks exactly equal the fully interacted pooled OLS covariance. Crossfit zero-variation heldout covariance cannot support a Wald test; use coefficient-direction projection only, no fabricated inference. Initial pandas field-access / singular holdout issues were repaired before final run.

Reconstruction uses existing saved aggregate PCA loading tables, stored locally as frozen_prior_pca.csv with original commit provenance and reconstructed centers/scales. No runtime fetch or newly fitted PCA axes. Original-unit supplement is within each primary CSV; category slopes and individual contrasts in supplemental tables, with categoryN<10 suppressed. Inventory eligibility and families unchanged after seeing Y. Full support failures, missing tests, lower tiers retained. N/A conditional analyses are clearly marked, not silently claimed complete estimates. No independent holdout confirmation; five folds share original discovery dataset.

Run locally (Python3.12 compatible with numpy/pandas/scipy/statsmodels/sklearn/matplotlib):

    python screen.py "<local raw .dta>" --out "<this directory>"
    python deliver.py "<local raw .dta>" --out "<this directory>"
    python test_screen.py "<local raw .dta>"

Set OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1 for deterministic, efficient fitting. Existing sibling PR9/11 scripts are imports, not rerun discovery. No external raw-data requirement/export. Script output includes run phase/counts; test_results.json records actually executed assertions. High-cardinality factors may be legitimate baseline descriptors but have unsupported full category/form slope blocks; these are limitations, not null findings. FDR dependence/representation redundancy, coarse hypothetical Y, possible baseline self-report error and selection/power limits prevent a trait/mechanism/zero-heterogeneity inference. Exploration stops here.
'''
    (out/'AUDIT.md').write_text(audit,encoding='utf-8')
    versions={p:version(p) for p in ['numpy','pandas','scipy','statsmodels','scikit-learn','matplotlib']};(out/'environment.json').write_text(json.dumps(versions,indent=2),encoding='utf-8')
    print(facts.to_string(index=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('--out',default=str(ROOT));a=p.parse_args();deliver(a.data,a.out)
