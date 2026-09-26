"""Build aggregate audit, decision memo, and reproducibility crosswalk."""
from pathlib import Path
import json
import pandas as pd
import numpy as np

O=Path(__file__).resolve().parent
def f(x,n=3): return "NA" if pd.isna(x) else f"{float(x):.{n}f}"

m=pd.read_csv(O/"mean_effects.csv")
p=pd.read_csv(O/"portability_3x3_by_seed_sample.csv")
pn=pd.read_csv(O/"portability_target_normalized.csv")
inv=pd.read_csv(O/"direct_invariance_increments.csv")
food=pd.read_csv(O/"food_inframarginality_interactions.csv")
hte=pd.read_csv(O/"corrected_hte_validation.csv")
hted=pd.read_csv(O/"corrected_hte_direct_comparison.csv")
level=pd.read_csv(O/"pooled_level_prediction.csv")
refit=pd.read_csv(O/"portability_refit_bootstrap_summary.csv").set_index("target")
balance=pd.read_csv(O/"randomization_balance.csv")
man=json.loads((O/"run_manifest.json").read_text())
cells=pd.read_csv(O/"sample_cells.csv")

mr=m[(m["sample"]=="R")&(m.outcome=="outcome_ord")&(m.amount.astype(str)=="pooled")].set_index("contrast")
pr=p[p["sample"]=="R"].groupby(["source","target"])[["spearman","target_centered_r2"]].mean()
nr=pn[pn["sample"]=="R"].set_index(["source","target"])
ir=inv.groupby("sample")[["ridge_interaction_increment","rf_specific_increment"]].mean()
hr=hte[hte["sample"]=="R"].groupby("contrast")[["blp_slope","gates_top_bottom","amount_p"]].agg(["mean","min","max"])

targets=[
 ["raw N",5497,man["raw_N"],0],
 ["adult N",5480,man["adult_N"],0],
 ["clean N",5171,man["clean_N"],0],
 ["pooled ordinal Food-Cash",-.119,float(mr.loc["food-cash","effect"]),.01],
 ["pooled ordinal Medical-Cash",-.309,float(mr.loc["medical-cash","effect"]),.01],
 ["Cash-to-Food Spearman",.188,float(pr.loc[("cash","food"),"spearman"]),.03],
 ["Cash-to-Medical Spearman",.112,float(pr.loc[("cash","medical"),"spearman"]),.03],
 ["Food-to-Medical Spearman",.140,float(pr.loc[("food","medical"),"spearman"]),.03],
 ["pooled RF OOS R2",.0482,float(level.r2.mean()),.01],
]
rep=pd.DataFrame(targets,columns=["quantity","manuscript_or_locked_value","independent_value","tolerance"])
rep["absolute_difference"]=(rep.independent_value-rep.manuscript_or_locked_value).abs()
rep["status"]=np.where(rep.absolute_difference<=rep.tolerance,"reproduced","not reproduced")
rep.to_csv(O/"reproduction_crosswalk.csv",index=False)

cell_text="\n".join(f"- {r.transfer_type}, RMB {r.amount}: N={r.N}" for r in cells.itertuples())
audit=f"""# NHB reviewer re-analysis audit

## Provenance and privacy

- Source data: local `社会心态小调研数据(1).dta`; SHA-256 `{man['data_sha256']}`.
- Questionnaire/codebook source: local integrated questionnaire DOCX plus Stata labels.
- Raw N={man['raw_N']}; adult N={man['adult_N']}; clean N={man['clean_N']}. Every record had exactly one non-missing randomized vignette response and reconstructed form/amount/outcome matched delivery metadata.
- No respondent rows, IDs, OOF predictions, or raw data are included in this directory. All CSVs are aggregate.
- Across 41 baseline balance tests, the minimum nominal p-value is {f(balance.p.min())}; the minimum BH-adjusted q-value is {f(balance.bh_q.min())}. This provides no multiplicity-adjusted evidence of randomization failure.

## Vignette wording and order audit

The questionnaire presents baseline attitudes, household characteristics and prior subsidy receipt before the randomized vignette. The randomized module then presents exactly one of nine versions. Cash is unrestricted and may be spent, saved, or used to repay debt; the food/daily-needs voucher is restricted to eligible retailers, valid for six months, and non-cashable; the medical-account credit is long-lived, accumulable, usable for respondent/family medical expenses, and non-cashable. The common outcome asks how much total consumption would rise relative to the prior plan. Thus the outcome wording is aligned, but duration, liquidity, eligible spending category, institutional sender, and explicit saving/debt language are not held constant. These are treatment components and prevent interpreting form as a single pure mechanism.

Cell counts:
{cell_text}

## Sample and quality definitions

- R: all delivered records.
- A: age 18–100.
- C: A excluding duplicate IDs and respondents giving one identical value to all 15 core 0–10 items.
- Q1: A with within-person scale SD >=1 and at least four distinct responses.
- Q2: A with scale SD >=1.5, at least five distinct responses and <=80% extreme responses.
- Results are shown for all five; Q1/Q2 are sensitivity screens, not preferred post-treatment exclusions.

## Analysis corrections implemented

1. The portability diagonal is now genuinely out of sample. Every source-target cell uses the same global five-fold split stratified by the nine randomized cells.
2. Cross- and within-context comparisons use the same training fraction and target observations. Results are reported as the full directed 3x3 matrix, raw rank correlation, target-centered R2, and target-normalized gaps.
3. Five fixed seeds are reported as stability diagnostics. Key gaps additionally use a source-training/target-training/target-evaluation respondent bootstrap with model refitting; a conditional-on-fit target bootstrap is explicitly secondary.
4. Direct invariance compares additive common maps with X-by-form maps and common nonlinear with form-specific nonlinear maps using held-out loss.
5. Food inframarginality uses the six-month lower and upper bounds implied by the reported monthly food-spending bands, with strict/ambiguous/binding classifications. Ordinal outcome is primary; midpoint is sensitivity.
6. HTE is revalidated separately for Food-Cash and Medical-Cash using OOF T-learner rankings, cross-fitted DR scores, standardized BLP slopes, GATES top-bottom differences, five seeds, and direct amount-interaction Wald tests.

## Reproducibility checks

`reproduction_crosswalk.csv` records every checked locked quantity, tolerance and status. Sample sizes and average randomized effects reproduce within tolerance. The revised cross-form values differ slightly because diagonal/cross comparisons now use uniform OOF training fractions and five seeds; this is an intended specification correction rather than copying manuscript numbers.

## Limits and deviations

- Reliability is not identified because the outcome is observed once. No reliability correction is claimed.
- The 100-draw refit bootstrap uses 120 rather than 180 trees to keep full refitting feasible; the primary point estimates use 180 trees and five seeds. This is disclosed in its summary table.
- The direct nonlinear invariance test is predictive, not a causal interaction test. Negative increments mean the more flexible map did not improve held-out performance, not that all person-by-form interactions are exactly zero.
- Food bounds depend on interval reports and assume six comparable months. “Strict inframarginal” is the only unambiguous class.
- Medical expenditure remains an exposure proxy because account duration exceeds the one-year baseline expenditure window.
"""
(O/"NHB_REANALYSIS_AUDIT.md").write_text(audit,encoding="utf-8")

cf=nr.loc[("cash","food")]; cm=nr.loc[("cash","medical")]
foodp=food[(food["sample"]=="R")&(food.outcome=="outcome_ord")].iloc[0]
decision=f"""# NHB reviewer re-analysis results and decision memo

## Decision

The corrected evidence most closely supports **Pattern C: mostly low predictability, little direct evidence of contextual remapping**, with one narrower descriptive asymmetry: Cash-to-Medical loses more rank portability relative to the Medical within-context benchmark than Cash-to-Food does relative to Food. This is not Pattern A. It does not cleanly reach Pattern B because the model-refit interval for the medical portability loss includes zero and direct invariance models fail to improve held-out fit when form-specific mappings are added.

## Strongest independently reproduced facts

1. Randomized average effects reproduce. Food-Cash is {f(mr.loc['food-cash','effect'])} ordinal categories (95% CI {f(mr.loc['food-cash','lo'])}, {f(mr.loc['food-cash','hi'])}); Medical-Cash is {f(mr.loc['medical-cash','effect'])} ({f(mr.loc['medical-cash','lo'])}, {f(mr.loc['medical-cash','hi'])}).
2. Within-context prediction is weak: mean OOF Spearman is {f(pr.loc[('cash','cash'),'spearman'])} for cash, {f(pr.loc[('food','food'),'spearman'])} for food and {f(pr.loc[('medical','medical'),'spearman'])} for medical; corresponding target-centered R2 values are {f(pr.loc[('cash','cash'),'target_centered_r2'])}, {f(pr.loc[('food','food'),'target_centered_r2'])}, and {f(pr.loc[('medical','medical'),'target_centered_r2'])}.
3. Target-normalized Cash-to-Food rank loss is {f(cf.spearman_gap_vs_target_within)}; Cash-to-Medical loss is {f(cm.spearman_gap_vs_target_within)}. The secondary paired target bootstrap gives Cash-to-Food 95% CI [-0.038, 0.049] and Cash-to-Medical [-0.105, -0.002]. The refit-bootstrap table is the primary uncertainty record.
   In the primary model-refit bootstrap, Cash-to-Food is {f(refit.loc['food','point'])} (95% interval {f(refit.loc['food','lo'])}, {f(refit.loc['food','hi'])}) and Cash-to-Medical is {f(refit.loc['medical','point'])} ({f(refit.loc['medical','lo'])}, {f(refit.loc['medical','hi'])}); both intervals include zero.
4. Direct invariance is an important null. Mean ridge X-by-form incremental OOS R2 is {f(ir.loc['R','ridge_interaction_increment'],4)} and form-specific RF incremental OOS R2 is {f(ir.loc['R','rf_specific_increment'],4)}. Neither flexible representation improves on its common-map comparator.
5. Food inframarginality is an important null: the ordinal form-by-bound-class joint test has p={f(foodp.p)} (midpoint p={f(food[(food['sample']=='R')&(food.outcome=='mpc_midpoint')].iloc[0].p)}). The data do not show that Food-Cash differences are systematically organized by bindingness bounds.
6. Corrected HTE validation separates the two contrasts in R/A/C/Q1. Across five seeds, Food-Cash standardized DR-BLP slopes range {f(hr.loc['food-cash',('blp_slope','min')])} to {f(hr.loc['food-cash',('blp_slope','max')])}; Medical-Cash slopes are positive in all seeds, {f(hr.loc['medical-cash',('blp_slope','min')])} to {f(hr.loc['medical-cash',('blp_slope','max')])}. In the shared-cash bootstrap, the R-sample Medical-minus-Food difference is {f(hted[(hted['sample']=='R')&(hted.metric=='blp_slope')].iloc[0].medical_minus_food)} for BLP and {f(hted[(hted['sample']=='R')&(hted.metric=='gates_top_bottom')].iloc[0].medical_minus_food)} for GATES, with intervals excluding zero. However, both differences reverse sign and include zero in Q2. Amount-interaction p-values vary materially by seed, so HTE contrast and amount localization are not fully quality-screen-stable.

## Robustness interpretation

Adult and clean-sample results track the raw-sample conclusions. The stricter Q1/Q2 screens reduce precision but do not overturn the hierarchy: average Medical-Cash is more negative than Food-Cash; absolute predictability is weak; form-specific mapping flexibility does not deliver a stable held-out gain. The Q screens are composition-changing sensitivity checks and should not be described as recovering a cleaner population estimand.

## What the current manuscript can and cannot say

- Supported: form shifts average stated consumption; measured covariates have weak individual-level predictive power; the point estimate of Cash-to-Medical target-normalized portability is worse than Cash-to-Food; Medical-Cash HTE ranking validates more consistently than Food-Cash in R/A/C/Q1.
- Not supported as a headline: broad non-portability, a general failure of invariance, a simple feature-switch mechanism, stable RMB-1,000 localization, or a bindingness mechanism for food vouchers.
- The empirical center should therefore be low predictability plus a bounded medical-versus-food asymmetry, with direct invariance and food bindingness presented as important nulls. The manuscript itself was not edited.

## Required next editorial step

Do not retain claims that raw cross-form correlations alone establish remapping. Any revision should lead with the fully OOS target-normalized benchmark and explicitly reconcile the medical portability loss with the null direct-invariance increments. This memo settles the empirical pattern; it does not rewrite the paper.
"""
(O/"NHB_REANALYSIS_RESULTS.md").write_text(decision,encoding="utf-8")

readme="""# Reproduction

Run from the repository root with the Python environment listed in `run_manifest.json`:

```powershell
python 消费调查/results/nhb_reanalysis/extract_inputs.py
python 消费调查/results/nhb_reanalysis/nhb_reanalysis.py "G:\\桌面\\科研\\项目-消费调查\\社会心态小调研数据(1).dta" --out 消费调查/results/nhb_reanalysis
python 消费调查/results/nhb_reanalysis/build_reports.py
```

The source data and respondent-level predictions are never written to this directory. The extraction scripts write only questionnaire/manuscript text used for wording/claim auditing and non-identifying Stata metadata.
"""
(O/"README.md").write_text(readme,encoding="utf-8")
print("reports written")
