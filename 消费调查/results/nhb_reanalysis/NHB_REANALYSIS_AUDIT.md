# NHB reviewer re-analysis audit

## Provenance and privacy

- Source data: local `社会心态小调研数据(1).dta`; SHA-256 `16996c88fdd20f5084b62a8503a8eec1d4c6ec7caff489eff109500f629694fe`.
- Questionnaire/codebook source: local integrated questionnaire DOCX plus Stata labels.
- Raw N=5497; adult N=5480; clean N=5171. Every record had exactly one non-missing randomized vignette response and reconstructed form/amount/outcome matched delivery metadata.
- No respondent rows, IDs, OOF predictions, or raw data are included in this directory. All CSVs are aggregate.
- Across 41 baseline balance tests, the minimum nominal p-value is 0.046; the minimum BH-adjusted q-value is 0.864. This provides no multiplicity-adjusted evidence of randomization failure.

## Vignette wording and order audit

The questionnaire presents baseline attitudes, household characteristics and prior subsidy receipt before the randomized vignette. The randomized module then presents exactly one of nine versions. Cash is unrestricted and may be spent, saved, or used to repay debt; the food/daily-needs voucher is restricted to eligible retailers, valid for six months, and non-cashable; the medical-account credit is long-lived, accumulable, usable for respondent/family medical expenses, and non-cashable. The common outcome asks how much total consumption would rise relative to the prior plan. Thus the outcome wording is aligned, but duration, liquidity, eligible spending category, institutional sender, and explicit saving/debt language are not held constant. These are treatment components and prevent interpreting form as a single pure mechanism.

Cell counts:
- cash, RMB 200: N=619
- cash, RMB 1000: N=595
- cash, RMB 5000: N=584
- food, RMB 200: N=614
- food, RMB 1000: N=620
- food, RMB 5000: N=602
- medical, RMB 200: N=615
- medical, RMB 1000: N=612
- medical, RMB 5000: N=636

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
