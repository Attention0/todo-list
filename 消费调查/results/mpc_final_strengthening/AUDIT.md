# Final strengthening audit / reproducibility note

## Execution boundary

2026-10-02. Read `SPEC.md`, `WORK.md` and the complete current `MPC_SIZE_CURVE_STRENGTHENING_WORK.md`. The user's final-strengthening request governs this pass rather than WORK's obsolete NHB routing. Latest fetched main `ef0f174269de0dcf918b9c372e9b03067fd9322a` contains the strengthening workplan. Direct empirical foundation: open PR #9, branch `feature/mpc-size-curve`, head `d749f5c0eab3938038882d948bc6370e78835249`.

New branch `feature/mpc-final-strengthening` starts at PR #9 and merges latest main's task document. A **stacked PR targeting `feature/mpc-size-curve`** keeps the new analysis diff separate from the 40 inherited PR #9 files; it depends on PR #9. Neither PR is merged automatically. No old code/result/manuscript files are edited. Pre-existing untracked analysis/NHB cache files are preserved and excluded; Python import caches are excluded too.

`ANALYSIS_PLAN.md` fixed all computational choices/families before generating this pass's outputs. No new moderators/HTE/SHAP/cluster/latent variables, subgroup search, ML tuning, mechanism rescue or policy learning. After this package, current-data exploratory work stops.

## Data and direct reuse

User's local original `.dta`, SHA-256 `16996c88fdd20f5084b62a8503a8eec1d4c6ec7caff489eff109500f629694fe`, unchanged from PR #9. New script imports PR #9 `size_curve.py` and calls its preparation function; it never calls the prior discovery pipeline. Reuses scenario assertions, ordinal/midpoint/alternative-top maps, R/A/C/Q1/Q2 definitions and fixed objective+needs control formula. Counts R/A/C/Q1/Q2 = 5,497/5,480/5,171/2,715/1,208. All reconstructed raw form slopes match PR #9 outputs. No repeat of basic randomization audit, need matching, Food mechanism work or prediction pipelines.

One scenario per unique respondent. No individual slopes, potential-outcome differences, within-person curves or reliability inferred. All deliverables aggregate; no respondent IDs, raw records, bootstrap records or individual predictions.

## Estimands / inferential choices

- Equal-weight Restricted = .5 Food + .5 Medical. Keep three form intercepts/slopes; do not collapse observations into a pooled arm with sample-size weights. OLS HC3 reference. Six prespecified tests per outcome: Cash/Food/Medical/Restricted slopes, Restricted−Cash differential, Food−Medical slope difference. Supplemental Food−Cash/Medical−Cash retain raw p, outside this six-test family. PR #9's original five-family interpretation is not overwritten.
- Binary GLM logit/probit with full form×z. Explicit HC1 covariance: empirical score/Hessian HC0 sandwich times n/(n-k), avoiding generic statsmodels' silent HC1/HC3→HC0 fallback. Ordered grid fits use the same explicit HC1 correction (k includes cutpoints) and must converge. All 140 finite-grid model entries are successful; 40 ordered models are included.
- Link interactions are link effects only. Probability AMEs are mean derivatives across z=-1/0/1 with equal dose weights; adjusted probabilities/AMEs use the same empirical covariates for each counterfactual form/dose. Delta method gradients include intercept, form and slope estimation uncertainty. Covariate reference distribution is treated as fixed for conditional-model inference. Restricted AME is mean of form AMEs. Averages of link slopes are not logit/probit of mixed probabilities.
- Endpoint fits use unrestricted form×amount indicators. Probability effects are 5,000−200 changes; latent effects are index differences. Raw endpoint estimates are retained. Separate comparable columns divide endpoint change by two; this is a display normalization, not evidence of continuous linearity. AME average derivatives and endpoint half-changes are not the same exact nonlinear functional.
- All normal CIs are pointwise 1.96×SE, not multiplicity-adjusted simultaneous intervals. Multiverse p-values are raw/descriptive, not a new family of confirmatory tests. Primary priority remains R/unadjusted/ordinal; top-category evidence is a prespecified supporting strengthening result, not an outcome substitution.

## Joint bootstrap and relative scales

5,000 draws, seed 20261003. Within each of nine randomized cells, resample empirical six-category outcomes retaining exact N. Implemented as multinomial counts: **mathematically identical to respondent bootstrap within cell** for the statistics used, because there are no additional covariates in these bootstrap estimands. All five nested thresholds use the same sampled categories/draws; their correlations are retained. No covariates or treatment labels permuted, no independent threshold resampling, no row/draw exports.

Threshold trend estimator uses actual fixed cell counts and form-specific z centering, exactly matching unadjusted OLS despite slightly unequal cells. Joint bootstrap covariance supplies Wald SE/normal CI/p for each top-minus-other contrast; Holm four within each of three comparisons. Restricted−Cash primary, Food−Cash/Medical−Cash secondary. Optional profile Wald uses four contrasts/covariance rank=4; nonsignificance is not equivalence. Three exported aggregate covariance matrices allow verification of joint contrasts.

Endpoint probability changes/ratios use the same draws. Equal-weight Restricted risk/odds are functions of equal-weight mixed probabilities, **not averages of risk/odds ratios**. Ratio CIs percentile on original scale; p-values Wald on log-ratio scale using bootstrap log SD. Difference CIs percentile, p based on bootstrap SD. Nine comparative p-values (3 comparisons×3 scales) Holm; within-form changes descriptive only. These are scale robustness checks, not causal adjustment for an observed 200-yuan outcome.

## Finite specification grid

Exactly 420 rows: R/A/C/Q1/Q2 × unadjusted/fixed-control adjusted × trend/unrestricted endpoint × ordinal/midpoint/alt-top/ordered-logit/ordered-probit/top-probability/top-logit-marginal × Medical−Cash/Food−Cash/Restricted−Cash. Nothing outside this grid. Controls exactly PR #9, no interactions with new baseline characteristics. Q1/Q2 retained even when unfavorable. `model_diagnostics.csv` records 140 model configurations and convergence.

`specification_stability_summary.csv` is grouped by coding and contrast: sign, CI consistency, median/range, no mixing latent logit and probit with other outcomes. Score/share standardization uses the fixed R outcome SD; probability effects retain probability units; latent standardized columns deliberately blank. Shares of positive/significant-looking specs are descriptive because samples, outcomes and models are highly correlated. Do not count specs as independent replications.

## Multinomial / yuan diagnostics

Unadjusted multinomial logit uses six categories and form×z, no new controls or models. Predicted nine-cell probability vectors compared against original cell shares, no raw coefficient headline. Convergence asserted. Largest misfit is Medical/1,000/category-1 +.02930; raw nonparametric probabilities take precedence over smoothed fits.

Midpoint implied yuan = raw cell mean midpoint×amount; bootstrap uncertainty from the same category draws. Eta is log endpoint mean-yuan ratio/log(25), not individual elasticity. Comparisons output as Food−Cash, Medical−Cash, Restricted−Cash; complementary to, algebraically dependent on, share estimates. Constant-dollar K minimizes **unweighted** squared midpoint error across three amounts for K/T; reports K and fit errors only, no structural inference/test. Does not eliminate broader survey-scale/absolute-yuan interpretation concerns.

## Outputs and reproduction

Required nine named analysis CSVs are present, plus raw-yuan cells, joint threshold profiles/covariances/global tests, model diagnostics and stability summaries. Five PNG figure families A–E with five corresponding aggregate source CSVs and legends. Exactly ten report sections in `../../MPC_FINAL_STRENGTHENING_RESULTS.md`. `RESULT.md` records acceptance/publication.

```text
python 消费调查/results/mpc_final_strengthening/strengthening.py "LOCAL_RAW.dta"
python 消费调查/results/mpc_final_strengthening/test_strengthening.py --data "LOCAL_RAW.dta"
```

Versions and hashes in manifest.json. Existing bundled runtime/project libraries used; OPENBLAS_NUM_THREADS=1/OMP_NUM_THREADS=1 for efficient/reproducible ordered optimization. PR #9 directory must remain available for the direct import (already inherited on this branch). Only the local raw input path is supplied at run time.

## Actual verification

Full bounded script executed twice. All core scientific CSV SHA-256 hashes matched on repeat, including nonlinear, bootstrap and model-diagnostic outputs; three specification/source CSVs were intentionally updated only to clarify latent/probability scale metadata, not to change estimates. Aggregate acceptance tests passed: direct PR #9 slope reproduction, pooled algebra, all Holm families, joint contrasts/covariance, ratios, multinomial probability sums, complete unique 420-grid, finite CIs, 140 converged configurations, implied-yuan identities, eta, required figures/source schemas and privacy checks.

Analytic logit/probit gradients for both trend and endpoint were independently checked against finite-difference numerical derivatives; joint bootstrap nested-threshold covariance checked against its analytic empirical-bootstrap covariance. Both passed. An initial test-only parameter mutation failed under pandas copy-on-write; replaced with explicit parameter-vector evaluations, then tests passed—no analysis output changed. All five plots visually inspected. Report section count=10. No claim of unrun tests. No raw/individual data staged.
