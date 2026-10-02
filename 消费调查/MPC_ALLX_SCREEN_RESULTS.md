# MPC all-X / multi-outcome slope screen results

## 1. Bottom line

Judgment: **rich observables still explain little**. Rich observed subjective and objective characteristics do not yield a stable explanatory signature for the form-by-size pattern in this corrected exploratory screen. No BH q<.10 in any of the six families; no Tier A or Tier B candidate. This is a failure to find a stable observed signature, NOT proof of zero heterogeneity, a measurement-error-free null, or a quantified upper bound on joint explanatory power. Reduced-form PR9–11 story is preserved; no new headline.

## 2. Variable inventory

221 inventoried fields/representations: all 67 .dta fields, 150 eligible (53 raw, 97 previously constructed), 71 excluded. Eligible breakdown: 35 raw subjective, 18 raw objective, 60 constructed subjective, 37 constructed objective. Q1–31 precede randomized scenario; Q41–49 platform background fields. Raw labels win over questionnaire option-order conflicts. Personal income harmonization is not household income. Exclude ID, assignment/form/amount, outcome and transforms, assigned-amount bindingness, outcome-trained CATE/person scores, quality/style indicators, invalid nominal-code numerical trends and unbounded Food upper-expenditure proxy. Main raw ordered fields use factors and prior rank versions remain separate. Four factors unsupported for full-model HC3: q44_industry, q46_income, q47_province, q48_city. No ad hoc category pooling or generalized-inverse discoveries. Complete-case R=5497, Cash=1798; each Cash model reports actual Cash N. All other-form diagnostics use full R. Existing saved 3 domain-PC directions and 27 prior diagnostic global-PC directions are reconstructed with frozen prior centers/scales; no new PCA axes fit/selected. Residual diagnostic PCs are not validated psychological scales. Inventory/mapping/frozen metadata and raw SHA are supplied.

## 3. Cash slope screen — ordinal

150 planned X representations; 146 estimable. Nominal p<.05: 4; minimum nominal p=0.0126; minimum BH q=1.0000; BH q<.10=0, q<.05=0, Holm p<.05=0. Nominal minima are audit statistics, not selected explanatory stories. Full coefficients, CIs, original-unit scalar coefficients, omnibus profiles and model N: `results/mpc_allx_screen/allx_cash_ordinal.csv`.

## 4. Cash slope screen — midpoint

150 planned X representations; 146 estimable. Nominal p<.05: 1; minimum nominal p=0.02986; minimum BH q=0.8695; BH q<.10=0, q<.05=0, Holm p<.05=0. Nominal minima are audit statistics, not selected explanatory stories. Full coefficients, CIs, original-unit scalar coefficients, omnibus profiles and model N: `results/mpc_allx_screen/allx_cash_midpoint.csv`.

## 5. Cash slope screen — Top75

150 planned X representations; 146 estimable. Nominal p<.05: 1; minimum nominal p=0.04934; minimum BH q=0.9771; BH q<.10=0, q<.05=0, Holm p<.05=0. Nominal minima are audit statistics, not selected explanatory stories. Full coefficients, CIs, original-unit scalar coefficients, omnibus profiles and model N: `results/mpc_allx_screen/allx_cash_top75.csv`.

## 6. Restricted-vs-Cash screen — ordinal

150 planned X representations; 146 estimable. Nominal p<.05: 3; minimum nominal p=0.01773; minimum BH q=0.9446; BH q<.10=0, q<.05=0, Holm p<.05=0. Nominal minima are audit statistics, not selected explanatory stories. Full coefficients, CIs, original-unit scalar coefficients, omnibus profiles and model N: `results/mpc_allx_screen/allx_rc_ordinal.csv`.

## 7. Restricted-vs-Cash screen — midpoint

150 planned X representations; 146 estimable. Nominal p<.05: 3; minimum nominal p=0.02972; minimum BH q=0.9498; BH q<.10=0, q<.05=0, Holm p<.05=0. Nominal minima are audit statistics, not selected explanatory stories. Full coefficients, CIs, original-unit scalar coefficients, omnibus profiles and model N: `results/mpc_allx_screen/allx_rc_midpoint.csv`.

## 8. Restricted-vs-Cash screen — Top75

150 planned X representations; 146 estimable. Nominal p<.05: 3; minimum nominal p=0.01377; minimum BH q=1.0000; BH q<.10=0, q<.05=0, Holm p<.05=0. Nominal minima are audit statistics, not selected explanatory stories. Full coefficients, CIs, original-unit scalar coefficients, omnibus profiles and model N: `results/mpc_allx_screen/allx_rc_top75.csv`.

## 9. Cross-outcome concordance

Zero X crosses q<.10 in even one Y, hence zero cross-outcome FDR candidates. Tier counts per target: 0 A, 0 B, 5 C, 145 D. These C counts include redundant representations, not five independent constructs. Scalar sign agreement: Cash 103 /150; RC 110/150 including estimable factor-profile agreement. Same direction across correlated Y is not independent replication and cannot rescue uncorrected findings. `cross_outcome_concordance.csv` retains all signs/q, profile cosines and gates.

## 10. Subjective vs objective

All four subjective/objective × raw/constructed groups yield zero BH q<.10 and zero Holm survivors in every Y/target. Subjective fields do not show a corrected discovery advantage. Counts are descriptive, not a formal comparison of explanatory capacity; subjective scales may carry response-style noise and shared measurement. Correlated aliases inflate representation counts but are not independent discoveries. See `subjective_objective_summary.csv` and Figure6.

## 11. Raw vs constructed

Component and frozen loading-oriented comparisons are fully exported. No constructed index has corrected evidence; no raw item can be promoted into an established construct. Standardized/dummy aliases are affine reuse, not replication; raw factor/rank encodings test distinct specifications of the same information. Three fixed prior domain PCs are displayed against all their raw items as a null diagnostic rather than "candidate constructs". Nominal alignment, cancellation and one-item labels are descriptive only; the table records the actual component count and q per Y.

## 12. Stability and robustness

Protocol21–23 applies sample/adjustment/functional reruns ONLY to Tier A/strongest Tier B. The corrected shortlist is empty: R/A/C/Q1/Q2, fixed-PR9 precision adjustment, ordered logit/probit, alternative top=1, Top75 logit/probit AME are explicitly **not applicable**, not "passed" or "stable". `shortlisted_robustness.csv` records each planned gate and available sample size (R5497/A5480/C5171/Q1 2715/Q2 1208; Cash sizes separately); no estimated effects are fabricated. We do not substitute raw-only variables to obtain apparent robustness.

## 13. Cross-fit stability

Every eligible X, all three Y, both targets: 5 cell-stratified folds, seed20261005; 900 summaries and 4500 fold diagnostics. Cash fits are genuinely Cash-only; RC fits preserve equal-weight form contrast. Training coefficient/profile direction is projected into heldout coefficients. Scalar heldout score=sign(train coefficient)×holdout coefficient; factor score=train unit-profile·holdout profile. Same-sign train counts reference the overlapping full-R estimate, so are optimistic descriptive stability, not independent validation. Sparse-factor fold failures retained. Zero outcome variation may leave heldout covariance singular; coefficient direction is still reported without an invalid Wald/calibration p, and zero-norm cosine is missing. No FDR candidate exists to promote even if nominal direction is stable. Aggregate valid-fold and sign counts in `crossfit_family_summary.csv`; no person fold IDs/predictions exported.

## 14. Joint explanatory power

Joint A and representative-per-construct B require Tier A. None qualifies, so joint Wald, slope-before/after and OOF full-vs-level gain are recorded **not applicable** in `joint_candidate_models.csv`. This round does NOT estimate the joint explanatory share of all150 variables and does NOT claim a saturated joint null. Prior bounded PR11 joint result remains background, not re-estimated evidence here. Optional regularized interaction diagnostic omitted: optional, and not needed to rescue an empty corrected shortlist.

## 15. Candidate mechanism interpretation

No coherent subjective/behavioral mechanism candidate emerges; nor does a corrected set of several explanatory correlates. Numerical nominal associations remain exploratory audit records. Randomized amount/form moderation can establish differential response associations conditional on baseline X, but cannot establish that X causes a mechanism. Hypothetical coarse outcomes, correlated Y/aliases, subjective response error, uneven category support, conservative correction, and limited interaction power remain limitations. Failure to reject is not equivalence. No raw-p-value story selection.

## 16. Paper implication

**rich observables still explain little** (third prescribed category). More precisely: no stable corrected observable signature is identified by this screen; joint explanatory fraction is unestimated because the candidate gate is empty. Preserve the Cash-size / restricted-tail reduced-form puzzle without attaching a newly discovered psychological mechanism. No manuscript change.

## 17. Final stop decision

STOP. Inventory, six corrected screens, raw/constructed and cross-outcome comparisons, all-X five-fold diagnostics, conditional N/A robustness/joint artifacts, six figure families/source CSVs, audit and reproducibility tests delivered. Do not launch further variable search, new moderator definitions, PCA/latent-trait discovery, SHAP/black-box HTE, or manuscript edits. Publish a new stacked PR; do not merge.
