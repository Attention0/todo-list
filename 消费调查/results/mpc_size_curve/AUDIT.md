# Size-curve audit and reproduction note

## Scope and inputs

Execution date: 2026-10-02. Base: `main` `da1eec5`, including `消费调查/MPC_SIZE_CURVE_WORK.md`. `SPEC.md` and `WORK.md` were read; the user's explicit size-curve brief supersedes WORK's older NHB execution routing for this pass. No specifications, manuscript files or previous results were changed.

References read/reused, not merged wholesale:

- PR #3, `a7136537e551ff70c3aa5e94dbb9aea658721ce7`: DATA_AUDIT, formal analysis definitions, ordered outcome/midpoint/alternative-top, objective+needs controls, economic-variable coding, and Nature response-quality screens. Prior randomization auditing/predictive pipelines were not repeated.
- PR #8, `92695b79d8f3de1c01fbc4f5ca06da7012bf327c`: `results/nhb_reanalysis/fungibility_trait/FUNGIBILITY_TRAIT_RESULTS.md`, NHB sample definitions and food bounds. Exactly one original scenario per unique respondent; derived scen_mpc is not a repeated measurement.

Input: the user's existing local `社会心态小调研数据(1).dta`. SHA-256 `16996c88fdd20f5084b62a8503a8eec1d4c6ec7caff489eff109500f629694fe`. No raw-data copy is included. Assertions confirm exactly one answered scenario, ordinal range 1–6, 5,497 unique IDs and agreement with derived scen_type/scen_amount/scen_mpc. IDs are never exported.

## Locked analysis choices and limits

- Main outcome: original ordinal score; auxiliary midpoint `[0,.05,.175,.375,.625,.875]`, alt top=1, and five unconditional cumulative thresholds. Thresholds correspond to ordinal categories >=2,3,4,5,6; these are bin indicators, not continuous observed MPC cutoffs.
- Amount rank/log-five trend `z=(-1,0,1)`; Cash reference. Five primary tests specified by workplan; Medical−Food secondary. Primary priority is R/unadjusted/ordinal, not the strongest adjusted/subsample/coding result.
- OLS HC3, normal Wald CIs/p; no province/city clustering added ad hoc. Ordered likelihood models use score-Hessian sandwich **HC1 with explicit n/(n-k)** correction (including thresholds in k). Generic statsmodels OrderedResults otherwise silently treats HC3 as uncorrected HC0; the script avoids that fallback. Both ordered fits must converge. The proportional-index model is a sensitivity, not a claim of identical effects at every cutoff.
- Holm applies to the five estimands separately within outcome/sample/specification; ordered models within their own five-test family. This is not correction for all exploratory codings, threshold margins, screens and mechanisms combined. All mechanism p-values are secondary, nominal, exploratory.
- RI: 5,000 independent conditional amount-label permutations within each form, exact observed cell counts preserved; no covariate shuffle/refit. Two-sided Monte Carlo p uses `(1+extreme)/(B+1)`. A form slope tests no amount effect in that form; a differential statistic tests the stronger no-amount-effect sharp null in both forms, **not equality of possibly nonzero slopes**. Robust model contrasts are the main differential-equality tests. No post-hoc rescue by RI.
- Adjacent contrasts use saturated amount means. Form-specific pairwise differences use HC3; cross-form adjacent difference-in-differences use independent cell mean variances and normal CIs (unbiased sample variances). No individual response transitions inferred.

## Reused samples and covariates

R=5,497; A age 18–100=5,480; C=A excluding complete straightlining on the same 15 Q1–13 items and duplicate IDs=5,171. Q1=A with within-scale SD>=1 and >=4 distinct values=2,715; Q2=A with SD>=1.5, >=5 distinct values, extreme 0/10 share<=.8=1,208. Q1/Q2 and C are sensitivity populations, not better-identified causal populations.

Fixed precision controls: age/age², gender, education, harmonized income, hukou, work status, unit type, housing, minor child, household-size category, food expenditure, medical expenditure, prior subsidy and city-tier factors. This matches the prior objective+needs block; controls were not chosen by significance. Income 11–16 recoded by subtracting ten, preserving the prior convention for 30 legacy records; category labels remain an imperfect harmonization, not exact yuan income.

Mechanism trend variables are standardized Q30/Q29 expenditure **category ranks**, Q7 perceived emergency fundraising and harmonized income rank, standardized using R. Q30 grouping fixed at 0–500 / 501–5,000 / >5,000 yuan annual past self-paid expenditure. Medical account is long-lived: these cannot certify medical inframarginality. Baseline moderators are observational, not experimentally manipulated.

Food monthly bounds: lower `[0,501,1001,2001,3001,5001]`, upper `[500,1000,2000,3000,5000,infinity]`, multiplied by six. Strict-assigned lower6>assigned amount; very-strict lower6>=2*amount; possibly-inframarginal upper6>=amount. Additional fixed lower6>5,000 screen avoids amount-induced subgroup composition changes. Only 56 likely-binding Cash/Food observations, all at amount 5,000; slope estimation is deliberately skipped in that group. Pooled Food−Cash means are equal-weight average contrasts from saturated form×amount regressions, **not** a centered trend intercept or an unbalanced pooled raw difference. `food-cash_at_1000` is separately labelled model-implied level contrast; it is not the pooled estimator.

## Model comparison and ML boundary

M1=form+z; M2=form*z; M3=full form*z interactions with the four small economic covariates plus categorical prior subsidy main effects. All use the same five cell-stratified folds, seed 20261002. OOF R²/MSE are aggregate diagnostic quantities only; no OOF rows or fold IDs exported. Scaling uses unsupervised R means/SDs; linear rescaling does not change the fitted full-interaction model space, but this is not a clinical/deployment prediction benchmark.

Shallow tree only, max_depth=3/min_samples_leaf=150; same four covariates, subsidy factors, form/z; three predetermined split seeds (20261002–04), no tuning. Full-fit standardized surfaces explicitly remain descriptive diagnostics. No RF/SHAP, unrestricted predictor scan or CATE subgroup search.

## Deliverable map

| Workplan requirement | Deliverables |
|---|---|
| Nine-cell means, category probabilities, CDF | cell_summary.csv |
| Primary/differential slope families, coding/sample/control checks | primary_amount_slopes.csv, differential_slopes.csv, ordered_slopes.csv |
| Structured/unrestricted interaction and RI | joint_curve_tests.csv, randomization_inference.csv |
| Shape checks | pairwise_amount_changes.csv, adjacent_differential_changes.csv |
| Threshold probabilities and contrasts | threshold_curves.csv, threshold_slope_contrasts.csv (separate tidy cell/estimand tables) |
| Category mass contribution identity | distribution_decomposition.csv |
| Food bound/fixed-population/clean checks | food_inframarginal_curve.csv |
| Need matching/cross-domain/liquidity/income | medical_need_matching_curve.csv, medical_need_cell_summary.csv, theory_mechanism_tests.csv, liquidity_curve_heterogeneity.csv |
| Economic model comparison | model_comparison.csv, theory_adjusted_slopes_ordinal.csv, theory_adjusted_slopes_midpoint.csv |
| Limited tree diagnostic | ml_diagnostic.csv, ml_surface.csv |
| Five figure families, sources, legends | figures/*.png, fig*_source.csv, FIGURE_LEGENDS.md |
| Exactly 14 substantive sections | ../../MPC_SIZE_CURVE_RESULTS.md |
| Reproduction and acceptance | size_curve.py, test_outputs.py, manifest.json, RESULT.md |

## Reproduce

Use Python with the versions recorded in manifest.json. From repository root:

```text
python 消费调查/results/mpc_size_curve/size_curve.py "PATH_TO_LOCAL_RAW.dta" --out 消费调查/results/mpc_size_curve
python 消费调查/results/mpc_size_curve/test_outputs.py
```

The bundled Python runtime plus existing project library directory was used on this host; no new system installation required. Scientific tables contain aggregate estimates, group counts/proportions and model summaries only. Full individual arrays live only in memory. No raw data, respondent-level IDs, fold IDs or OOF predictions are deliverables.

Acceptance checks actually run: nine cell counts; p-vectors sum to one; category means/CDF reconstructed; thresholds match complements; decomposition identity; OLS/ordered Holm recomputed; finite coefficient CIs; contrast algebra; pairwise differences equal raw means; expected sample sizes; binding-group slope omitted; twelve RI rows with 5,000 draws; six plot files and six source families; aggregate-only CSV schemas; exactly fourteen report sections. All pass. Re-ran the final complete pipeline: every aggregate CSV SHA-256 matched the prior final run. All six final figures visually checked; corrected overlapping log minor ticks and distribution legend covering data. No pre-existing untracked files included.
