# Nature-series locked empirical package: audit

## Scope and claim lock

This package implements `NATURE_EMPIRICAL_ROADMAP.md` and `NATURE_FIGURE_BLUEPRINT.md` against the fixed survey delivery, using `FINAL_EXPLORATION_AUDIT.md` and `FINAL_EXPLORATION_RESULTS.md` as the prior benchmark. It does not reopen feature selection, invent a mechanism, or change the randomized transfer-form estimands. The eight locked claims concern: low stated-MPC predictability; small incremental value of subjective states; limited cross-form portability; a possible Cash–Food versus Cash–Medical portability difference; Medical−Cash versus Food−Cash HTE predictability; amount-specific Medical HTE; no personalized-policy gain; and response-quality sensitivity. Every result is exploratory/post hoc, including analyses now re-estimated under locked code.

The data are hypothetical stated incremental-consumption responses from a single Chinese online sample, not realized expenditure, welfare, or cash-equivalent value. Baseline characteristics are not randomized; their associations are predictive/descriptive. Transfer form and amount were randomized.

## Data, outcomes, and samples

The code reads the external Stata delivery and calls the frozen `heterogeneity_formal.prep` function. It checks exactly one of nine response variables per respondent, scenario metadata agreement, and valid 1–6 outcomes. Raw R has N=5,497; Adult A has N=5,480; Clean C has N=5,171. The primary mean-effect outcome is the original ordinal 1–6 category. Midpoint stated MPC is an auxiliary outcome for prediction, HTE ranking, and policy-value estimands. Alternative top coding and binary thresholds (any, ≥10%, ≥25%, ≥50%) are sensitivity outcomes. Full form, amount, and nine-cell distributions are exported.

Response-quality screens are fixed from pre-treatment 0–10 scale items: Q1 = Adult A, within-person SD≥1, at least four unique values; Q2 = Adult A, SD≥1.5, at least five unique values, extreme-response share≤0.8. R/C remain the primary samples. Outputs include complete/near straightlining, scale SD, uniqueness, extreme share, midpoint share, entropy, and composition changes. The delivery has no duration, IP/device, formal attention check, incentive-compatible decision, or transaction validation.

## Locked feature blocks and transformations

Feature definitions are imported unchanged from `heterogeneity_formal.py`: T = randomized form and amount only; O = objective/quasi-objective household and needs variables; S = subjective economic states; A = broader attitudes; O+S, O+A, and ALL are fixed unions. Ordered and nominal predictors use training-fold one-hot encoding; numeric predictors use training-fold median imputation and standardization. Model preprocessing is never fitted on a held-out outcome. Amount enters every form-specific model and HTE nuisance model.

The three preassigned subjective domains and discovery-half PCA loadings are retained from `final_exploration.py`. Their held-out incremental result and loadings are copied as validated aggregate baseline outputs; they are not refitted to the new common five-fold partition because their discovery/validation design is a separate, predeclared psychometric estimand. Outcome-representation and legacy HC/FE/RI tables are likewise retained as clearly identified supplementary baseline checks, not falsely presented as newly harmonized folds.

## Fold lock and ML models

Global respondent folds are five-way `StratifiedKFold` on the original 3×3 randomized cell, with `shuffle=True`. The headline seed is 20260921. Two repeated partitions, seeds 20260921 and 20260922, yield ten identically indexed held-out level-prediction scores for all seven feature blocks and four models. The same global fold IDs are inherited by each pairwise HTE contrast, so shared Cash respondents are in the same held-out fold for Food−Cash and Medical−Cash. Policy predictions and policy evaluation use the same headline global folds. Quality-screen and amount-specific analyses regenerate five cell-stratified folds within each explicitly changed sample. No fold IDs or respondent-level predictions are exported.

Level prediction uses ridge (alpha 10), elastic net (alpha .01, L1 ratio .1), RF (180 trees, minimum leaf 20, max features .5), and histogram gradient boosting (120 iterations, max leaf nodes 15, L2 regularization 3). Each reports fold-level and mean out-of-sample R², RMSE, and MAE. Paired feature-block R² differences use 4,000 fold bootstrap draws. Practical-gain benchmarks are +0.01 and +0.02 R². The ten folds are correlated through repeated respondents, so fold-bootstrap intervals are sensitivity summaries, not independent-sample frequentist coverage guarantees.

## Cross-form portability and reliability sensitivity

Each source-form RF is trained only on respondents randomized to that form. Predictions in the target form are evaluated without any target-form refitting; mean recentering is used only for R², not Spearman ranking. Six directed Spearman, R², and slope results are exported. Formal Spearman differences use 3,000 target-respondent bootstrap draws with source models fixed; these intervals are conditional on source-model training and do not include its uncertainty. Ridge predictor-vector correlation, cosine, and sign agreement use a fixed common standardized encoding; 600 stratified respondent bootstrap draws refit the source models and test Cash–Food minus Cash–Medical and Cash–Food minus Food–Medical. Some percentile intervals are biased relative to full-sample point estimates in high-dimensional regularized fits; both are shown, with no precision claim from an isolated metric.

The attenuation exercise divides observed cross-form Spearman by assumed equal reliabilities 0.4, 0.6, and 0.8, capped at 1. This applies a classical independent-error heuristic to a rank statistic. It is a **sensitivity calculation**, not a reliability estimate or factual correction. The survey has no repeated outcome measure with which to identify reliability.

The cross-fitted shared signal `G=(mu_C+mu_F+mu_M)/3` and deviations `D_t=mu_t-G` reuse the validated final-exploration aggregate variance table. Each variance is scaled by observed outcome variance. These variances are non-additive and are not a partition of total outcome variance.

## Fungibility HTE and formal asymmetry

Pairwise contrasts remain Food−Cash and Medical−Cash in midpoint stated MPC for flexible HTE; Medical−Food is an explicit secondary transparent-moderation contrast. T learning fits form-specific RFs (110 trees, minimum leaf 25, max features .5). DR learning fits treatment-specific histogram-boosting nuisance models in three inner cell-stratified folds, builds each training pseudo-outcome only from its own out-of-fold nuisance predictions using randomized propensity conditional on amount, and fits an RF (110 trees, minimum leaf 30, max features .5). R learning cross-fits `m(X,A)` without treatment, constructs Robinson residuals and fits the RF objective using residual-treatment-squared weights. All CATE predictions are outer-fold held out. A reliable causal-forest package was unavailable and was not installed solely for this package.

Calibration is the HC1 coefficient on treatment×centered OOF CATE in a model adjusting for amount. Top–bottom separation is the randomized contrast in quintile 5 minus quintile 1, with normal-approximation intervals. Medical-minus-Food HTE predictability differences use 1,500 stratified respondent bootstrap draws, resampling the shared Cash observations jointly within each amount cell and holding OOF predictions fixed; this captures validation-sample uncertainty, not complete learner-training uncertainty. It is a formal contrast, not a comparison of separate p-values. T/DR/R are repeated over ten prespecified seeds 20260921–20260930, each with a full five-fold OOF re-estimation. Amount-specific T/DR calibration is supplemented by an HC1 two-df amount×treatment×within-amount-standardized-prediction omnibus test. This tests differences in standardized calibration, not an optimal transfer size.

Theory-guided moderator checks are restricted to income, education, and prior medical spending for highlighted Medical contrasts. Outputs include binned raw randomized contrasts, trend/factor specifications, a joint model, HC1/HC3, amount-saturated interactions, prespecified controls, province/city-tier FE, province-cluster sensitivity, R/A/C/Q1/Q2 screens, and 1,000 within-amount form-permutation randomization tests with three-variable BH q-values. Past medical spending is a proxy for prior exposure/need, not medical-account bindingness or a causal moderator. The frozen broader formal scan, categorical omnibus, Food null precision, and prior Medical−Food randomization tests remain available as supplementary evidence; the locked package does not rerun broad fishing.

Strict and very-strict Food inframarginal subsamples use the pre-existing six-month lower-bound food-spending rule; their pooled Food−Cash ordinal contrasts and prespecified HTE-null precision are reported. They do not prove unrestricted fungibility.

## Policy evaluation

Five policies are fixed: all Cash, all Food, all Medical, depth-2 tree, and ML argmax. Three form-specific RF response predictions are OOF. The shallow tree learns only from other folds' OOF predicted-best-form labels; its assignment is evaluated in the untouched fold. Known one-third randomized assignment probabilities are used for both IPW and cross-fitted DR policy values. The DR score is `mu_hat_d(X)+I(A=d)(Y-mu_hat_d(X))/p(A|amount)`, using an OOF nuisance prediction for every evaluated respondent. Paired respondent bootstrap intervals (3,000 draws) compare policy value to all Cash. Allocation shares are exported. The tree and argmax rules are rerun across the ten fixed fold seeds; seed stability reports point values and assignment shares, not ten independent experiments.

## Generalizability and export discipline

Internal composition and official census comparisons are carried from the final-exploration aggregate tables. The sample is online, young, and highly educated. Census totals and this adult platform frame are too incompatible for defensible raking; hukou is not interchangeable with residence. Broad age, education, hukou, and city-tier stratum estimates are descriptive robustness, not population transport estimates. No respondent-level data, OOF scores, fold IDs, or policy assignments are committed.

`analysis/nature_empirical.py` produces aggregate `tables/nature_*.csv`. `analysis/nature_figures.py` produces six main and ten Extended Data figures in PDF and 600-dpi PNG, panel source CSVs, and `figures/nature_figure_legends.md`. Cash, Food, and Medical colours are fixed throughout. Main randomized contrasts use HC1 or stated normal 95% intervals; bootstrap and fold-distribution intervals are explicitly distinguished. No significance stars are used.

## Protocol deviations and limitations

- The latent-factor discovery-half validation and previously validated outcome-coding checks are reused rather than forced into global five-fold splits; they answer different locked estimands.
- Cross-form Spearman bootstrap keeps source RF fits fixed; source-model uncertainty is partly addressed by separate ridge refit bootstrap and repeated HTE seeds, not by this Spearman interval.
- Causal forest and an additional boosting library were not installed. T, correctly cross-fitted DR, and Robinson R are the stable learner set.
- Model-feature permutation importance was not redone as a main figure; the ten-item Extended Data cap allocates ED Fig. 5 to latent-factor diagnostics as in the blueprint's final allocation. Legacy formal importance remains supplement-only and is never causal evidence.
- No raking was performed because authoritative margins are not measurement-frame compatible.
- The strict Q2 screen reduces N sharply; null HTE there is not evidence of equivalence.
- No new data, replication, preregistration, or realized-outcome validation exists. This is a locked re-analysis of previously explored data, not a prospective confirmatory study.
