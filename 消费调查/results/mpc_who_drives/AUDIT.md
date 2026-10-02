# Who-drives audit and reproducibility

## Authority and provenance

2026-10-02. Read project SPEC and WORK plus complete MPC_CURVE_WHO_DRIVES_WORK.md; user's explicitly named task overrides obsolete NHB routing in WORK. This is a new, explicitly authorized bounded pass after the prior stopping decision, not reopening headline discovery. Synced latest main `757fe14`; branch starts from PR #10 `cb6910f1141943c1a6649ed77d0134f95b43770b`, inheriting PR #9 `d749f5c0eab3938038882d948bc6370e78835249`. Merged main's new immutable workplan only. New stacked PR targets `feature/mpc-final-strengthening` to avoid duplicating #9/#10 packages; no automatic merge. Original PR files and manuscript unchanged. Old untracked files/cache preserved/excluded.

Directly import PR #9 preparation and assertions; do not run its discovery pipeline or repeat basic audit. Original local .dta SHA256 `16996c88fdd20f5084b62a8503a8eec1d4c6ec7caff489eff109500f629694fe`; R/A/C/Q1/Q2 counts 5497/5480/5171/2715/1208 unchanged. Exactly one original scenario per unique ID, same outcome/amount/form mappings and quality screens. No raw copy or respondent/fold/OOF/bootstrap records exported.

## Predetermined choices

ANALYSIS_PLAN fixed before treatment-moderation results. Primary outcome ordinal=6, z=-1/0/1. Five Tier 1 conceptual variables only; six Tier 2 only. No psychology, attitude, forest, SHAP, cluster, latent, new cutpoints or data-driven control selection. Subsidy, housing and work are categorical: standardized dummy columns and multi-df omnibus tests, not a meaningless nominal category trend. Per-SD coefficients stored separately from omnibus test statistics. Full-R scaling retained across samples; unsupervised full-X scaling cannot cause outcome leakage and is specified by task. Missingness in these eleven variables is zero.

Stata coding/labels and frequencies inspected: Q7 perceived emergency fundraising capacity (0–10); Q29 monthly household food category, Q30 prior-year household self-paid medical category; Q31 yes/no/don't-remember, Q26 own/rent/other, Q24 working/retired/student/not-working/other. Existing income legacy harmonization retained (30 entries codes11–16 minus10). Actual available income is PERSONAL income rank, not household total; flags retained in report. No precision-yuan recode invented. Household-size top category is 6+, rank only; education rank, child yes binary, age actual years.

## Regression and inference

Three independent form blocks, each containing intercept,z,X,z×X; exactly equivalent to full form*z*X lower-order specification. Cash-only fit independently matches the Cash interaction and HC3 SE from the three-form block; table N is full model N, effective Cash arm N is separately in manifest. Restricted is .5F+.5M, never observation pooling. Contrasts and SEs use full covariance. All component CIs normal 1.959964×HC3; omnibus Wald chi-square, rank(df) determined from contrast covariance. No ad hoc clustering.

Holm separately: five Tier1 Cash omnibus tests; five Tier1 RC omnibus tests; six Tier2 Cash tests; six Tier2 RC tests. One categorical variable contributes one multi-df p, irrespective of column count. Scalar component p is equivalent to its one-df omnibus; categorical component p and all Food/Medical diagnoses nominal outside families. Joint six-column Cash and RC omnibus tests additionally Holm two. No pooling of all outcomes/specifications into one family, and no confirmatory claim from nominal tests.

Fixed group definitions in plan; subsidy original unordered categories, not artificial low/mid/high. Cash cell means Wilson CI. Restricted .5 arm mean, variance .25(varF/nF+varM/nM); delta-normal CI, not Wilson on combined observations. Raw form-cell file shows component counts. Decompositions use ALL R subgroup proportions; exhaustive weights sum to1 within each variable. Contribution CI treats empirical X shares as fixed, shares-of-total descriptive without CI. Standardized totals need not equal raw Cash total due treatment sample composition; all totals and raw endpoint value exported. Correlated variable partitions non-additive. Main slope estimates use all three amount cells, not half of an endpoint difference; shape can differ within noisy groups.

Joint: six columns for five variables, 42 full parameters; 24 parameters in level-only comparator, 6 baseline. Full-R mean X contrast gives average Cash/Restricted/RC slope. Estimated profile ranges use empirically observed X vectors, not extreme synthetic corners. Their spread includes sampling/fit noise; no observed individual treatment sensitivities or true explained variance are inferred. Additional all-coefficient table and small-transfer Cash level contrasts support signature check; these level-only associations are nominal, not mechanism proof.

## Bounded honest diagnostic

Fixed 5-fold cell-stratified split, seed20261004, reused baseline/levels/full and every bootstrap. Linear interaction model only, no tuning/tree. Least-squares form blocks verified against full OLS. Quintile cutpoints obtained from TRAINING-X forecasts using trained coefficients, then applied to holdout X. Holdout person's outcome never used for own forecast or cutpoint fit. Other folds share training data, so a naive group CI conditional on fitted score is not the main inference.

Known randomized design probabilities 1/9. For endpoint contrast coefficients w_f: AIPW score = sum_f w_f(mu_f,5000−mu_f,200) + 9 w_observed_form (Y−mu_observed) [I5000−I200]. Cash decline uses w=(-1,0,0); RC differential endpoint uses (-1,.5,.5). OOF calibration score regressed on OOF sensitivity plus fold intercepts. Raw randomized quintile endpoints also exported; raw SE conditional on grouping is explicitly secondary. Scores refer to contrast averages, not observed person effects.

499 exponential-weight multiplier bootstrap replicates, seed fixed; all five training fits refit, quintile cutpoints recomputed, original folds fixed, same respondent weights used across overlapping folds. Full/level/baseline models and metrics refitted together. Percentile CI; Monte Carlo precision and nonsmooth quintile/weak-signal limitations acknowledged. Not exact RI, no causal learner validation headline. AIPW calibration weights 1/9 from design, not a changed estimand. Regression/OOF probability forecasts can leave [0,1]; rates and ranges reported, forecasts untrimmed for sorting and AIPW. Clipped Brier separately supplied; no silent fix chosen to improve result. OOF R2 is outcome prediction, not treatment heterogeneity explained fraction. Bootstraps never saved individually.

## Limited robustness

Before results, lock selection of at most two Tier1 variables with smallest min(Cash omnibus p,RC omnibus p). Selected Medical and Income, despite neither corrected discovery. Four outcomes top75/ordinal/midpoint/ge50 times five inherited samples: 320 component/omnibus rows. No more outcomes or moderators. Raw p/CI only, all Holm blank in this selection-sensitive table; no claim confirmatory replication. Unfavorable Q1/Q2/sign reversals retained. Original stopping boundary applies after delivery.

## Deliverable map and reproduce

Ten required CSVs present: primary_moderator_interactions; secondary_profile_interactions; subgroup_cash_curves; subgroup_restricted_curves; cash_decline_contributions; subgroup_differential_slopes; joint_tier1_model; joint_tests; prediction_calibration; moderator_robustness. Extras: coding, raw form cells, coefficients/signature levels, joint profile range, OOF distributions/probability diagnostics, refit calibration/model metrics, heldout quintile cells. Five required figure families plus compact subgroup forest, corresponding source CSVs and legends. Exact fourteen-section root report, plan/audit/RESULT/manifest/test script. Aggregate exports only.

```text
python 消费调查/results/mpc_who_drives/who_drives.py "LOCAL_RAW.dta"
python 消费调查/results/mpc_who_drives/test_who_drives.py "LOCAL_RAW.dta"
```

Use PR9 directory alongside this package and libraries recorded in manifest. Existing bundled Python + project libraries used, OPENBLAS_NUM_THREADS=1/OMP_NUM_THREADS=1; no new installations.

## Verification performed

Full pipeline executed; two final deterministic executions produced identical hashes for all **26 aggregate CSVs**, including all 499-refit diagnostic summaries (repeat draws are not independent replications). Acceptance tests: original sample/input hashes and scope; standardized coding; independent manual HC3 matrix/sandwich for every single-variable interaction; Holm reconstruction; Cash-only vs form-block equality; independent cell mixtures; exhaustive contribution sum/ratio identities; slope contrast algebra; baseline reproduces PR9/#10; joint df/family; selected robustness counts and all samples; independently reconstructed AIPW; explicit holdout-outcome perturbation leaves that fold's forecasts/quintile assignment unchanged; OOF metric reconstruction; finite intervals; aggregate/privacy schemas; all figures/source files; exact fourteen sections. Tests pass. All six plots visually inspected; no omitted/unrun test claimed.
