# Nature-series figure legends (draft)

All panels use the Raw R sample (N=5,497) unless a smaller N is stated. Responses are hypothetical stated additional consumption, not realized spending. No figure implies welfare or actual cash-equivalent value.

**Fig. 1 | Transfer form changes stated additional-consumption responses.** a, Randomized 3×3 transfer-form-by-amount design with cell N. b, Six-category response distribution by transfer form, pooled across amounts; bar segments are category shares. c, Cell mean of the original ordinal 1–6 response with 95% normal-approximation confidence intervals, plus pooled randomized contrasts estimated by a saturated form×amount linear model with HC1 intervals. N=5,497; no multiplicity correction is used for the prespecified average contrasts.

**Fig. 2 | Rich baseline information explains little stated-MPC variation.** a, Repeated five-fold out-of-sample R² for a prespecified random forest on midpoint-coded stated MPC, using identical stratified folds for the seven locked feature sets; intervals are 95% bootstrap intervals over ten held-out fold scores. b, Paired fold differences relative to objective/needs variables with 95% fold-bootstrap intervals; vertical lines at +0.01 and +0.02 are predeclared practical-gain benchmarks. c, Held-out R² from discovery-half PCA domain scores, with factor alpha values listed. N=5,497 for a,b; c uses the held-out half. These are predictive, not causal comparisons.

**Fig. 3 | Observed response rankings have limited cross-form portability.** a, Spearman correlations between source-form model predictions and observed target-form midpoint stated MPC; each target contains a distinct randomized respondent sample. b, Ridge coefficient-vector correlations for objective/needs and ALL blocks with 95% stratified respondent-bootstrap intervals; the displayed difference is also bootstrap-tested. c, Classical attenuation sensitivity at assumed equal reliabilities 0.4, 0.6, and 0.8; reliability is not observed or estimated. N=5,497; cross-form source models use the full source arm and never refit on target outcomes. Panel a is descriptive, not a treatment-effect estimand.

**Fig. 4 | Predictable fungibility heterogeneity differs by transfer context.** a,b, Within-quintile observed randomized midpoint stated-MPC contrast across quintiles of out-of-fold DR predicted treatment effects, using identical five-fold cell-stratified partitions and held-out outcomes. Error bars are 95% normal-approximation intervals. Food−Cash N=3,634; Medical−Cash N=3,661. c, Medical-minus-Food difference in calibration slopes and top-minus-bottom observed-effect separation, with 95% stratified respondent-bootstrap intervals that resample Cash observations jointly. Calibration models use HC1 errors. The contrast difference is exploratory but fixed by the roadmap; learner comparisons appear in Extended Data.

**Fig. 5 | Medical-context heterogeneity varies with amount and economic exposure.** a, Out-of-fold Medical−Cash calibration slopes by randomized transfer amount for T and cross-fitted DR learners, with HC1 95% confidence intervals. b,c, Raw within-band randomized Medical−Food contrasts in the original ordinal 1–6 response for household income and past-year medical-spending bands; normal-approximation 95% intervals. Medical−Food is a secondary contrast used because the transparent moderation signal is stronger there. Past medical spending is a proxy for prior exposure/need, not a causal treatment or strict bindingness measure. N=5,497 overall; amount-specific and band Ns are in panel source CSVs.

**Fig. 6 | Personalized form assignment does not improve the stated-consumption objective.** a, Cross-fitted doubly robust policy values for three uniform forms, a depth-2 tree, and ML argmax, with 95% respondent-bootstrap intervals; annotations give gains versus uniform Cash and paired bootstrap intervals. b, Out-of-fold policy allocation shares. Known one-third assignment propensities and held-out outcome-model predictions are used. N=5,497; IPW values and seed-stability checks are provided in supplementary tables. These values concern stated midpoint MPC, not welfare or realized spending.

**Extended Data Fig. 1 | Full nine-cell outcome distributions.** Each panel is a randomized form×amount cell; bars show six-category response shares, and titles give exact cell N. Raw R; N=5,497.

**Extended Data Fig. 2 | Form-effect robustness across outcome codings.** Pooled Food−Cash and Medical−Cash contrasts under ordinal, midpoint, alternative-top, and binary-threshold outcomes. Points and bars are HC1 estimates and 95% intervals. Scales differ across rows; N=5,497.

**Extended Data Fig. 3 | Prediction-model family comparison.** Mean repeated-CV R² across locked information sets for ridge, elastic net, random forest, and histogram gradient boosting on identical folds. N=5,497; full fold distributions and error metrics are in source tables.

**Extended Data Fig. 4 | Outcome-representation predictability.** Ridge repeated-CV R² across ordinal, midpoint, alternative-top, and threshold outcomes; intervals depict 95% normal intervals over ten fold scores. N=5,497.

**Extended Data Fig. 5 | Subjective-factor diagnostics.** First-component explained variance and internal-consistency alpha for three preassigned subjective domains. Loadings come from the discovery half and are scored in the held-out half.

**Extended Data Fig. 6 | Cross-form level and slope transfer.** Mean-recentered target-form R² and calibration slope for all six directed source→target predictions. N=5,497 across randomized arms; no target-form mapping is refitted.

**Extended Data Fig. 7 | Predictor-map similarity diagnostics.** ALL-feature ridge coefficient cosine similarity and sign agreement with 95% respondent-bootstrap intervals. N=5,497; the measures are descriptive.

**Extended Data Fig. 8 | HTE learner comparison.** T, cross-fitted DR, and Robinson R learner calibration and top–bottom separation for Food−Cash and Medical−Cash; points and bars show HC1 or normal-approximation 95% intervals. Pairwise Ns: 3,634 and 3,661.

**Extended Data Fig. 9 | HTE stability over ten fixed seeds.** Each dot is a complete five-fold OOF re-estimation of calibration or top–bottom separation under one seed. Seed grid 20260921–20260930; pairwise Ns: 3,634 and 3,661.

**Extended Data Fig. 10 | Response-quality sensitivity.** Rows show Raw R, Clean C, Q1 and Q2 screens with exact N; columns show pooled ordinal Food−Cash and Medical−Cash effects and Medical−Food income and prior-medical-spending moderation. Points and bars are HC1 estimates and 95% intervals. Quality screens use only baseline response-style diagnostics and are sensitivity checks, not primary exclusions.
