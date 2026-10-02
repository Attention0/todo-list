# MPC slope all-X screen: multi-outcome exploratory mechanism mapping

## 0. Purpose

This is a deliberately broad but disciplined exploratory pass.

The reduced-form paper story is already established from PR #9–#11:
- Cash stated MPC declines with transfer size.
- Restricted forms show weaker high-MPC-tail compression.
- Standard economic observables explain little in the bounded mechanism pass.

The user now wants to ask a broader question:

> Across all available pre-treatment variables — subjective and objective, raw and previously constructed — which characteristics are associated with steeper or flatter MPC size curves, and which are associated with the Restricted-vs-Cash slope difference?

This pass should NOT be presented as a confirmatory mechanism test. It is an exploratory screen whose purpose is to identify a small set of reproducible candidate explanatory dimensions.

Do not modify the manuscript.

---

# PART I. VARIABLE INVENTORY AND ELIGIBILITY

## 1. Build a complete X inventory before estimating anything

Create a machine-readable variable inventory that covers all available fields in the survey data and all existing constructed variables already used in prior analyses.

For every variable record:
- variable name;
- label / questionnaire meaning;
- raw vs constructed;
- subjective vs objective;
- numeric / ordinal / categorical / binary;
- pre-treatment / treatment / post-treatment / outcome / identifier / unclear;
- source question;
- missingness;
- number of unique values;
- whether it is eligible for the all-X screen;
- if excluded, exact reason.

Create:
- all_x_variable_inventory.csv
- raw_constructed_mapping.csv

Do not begin the regression screen until this inventory is complete.

## 2. Inclusion rule

Include all variables that are clearly pre-treatment and substantively interpretable as respondent characteristics, including:
- subjective economic assessments;
- psychological / social-attitude variables;
- objective demographics;
- household composition;
- employment;
- housing;
- baseline expenditure / needs;
- prior subsidy experience;
- location / city-tier style baseline descriptors if they are not treatment-derived;
- all existing constructed indices, ranks, harmonized measures, and scale summaries created in prior analysis.

## 3. Exclusion rule

Exclude:
- respondent IDs;
- treatment assignment variables;
- transfer form;
- transfer amount;
- any variable mechanically derived from treatment;
- the MPC outcome and all transformations of the MPC outcome;
- post-treatment responses;
- variables that encode the same scenario answer being explained;
- survey metadata with no behavioral interpretation unless explicitly part of prior quality screening;
- quality-screen indicators as substantive X variables;
- variables with effectively no variation;
- variables whose timing relative to treatment is unclear.

If timing is unclear, mark "unclear" and exclude from the main screen.

## 4. Raw and constructed variables

The user explicitly wants both raw and constructed variables screened.

Therefore:
- keep original raw items;
- keep existing constructed indices / ranks / harmonized variables;
- do not silently replace raw with constructed;
- do not drop a raw variable merely because a constructed version exists.

But record raw/constructed relationships so that later interpretation can distinguish:
- a genuine construct-level pattern;
- one raw item driving an index;
- multiple redundant representations of the same information.

Do NOT treat raw and constructed versions as independent replications.

---

# PART II. THREE PRIMARY OUTCOMES

## 5. Outcome 1: ordinal score

Use the original six-category ordered MPC response coded 1–6.

For the broad screening stage, estimate it using OLS with HC3 SE for transparent slope interactions.

This is a pragmatic summary model, not a claim that the categories are cardinal.

For shortlisted variables, run ordered logit and ordered probit robustness.

## 6. Outcome 2: midpoint-coded MPC

Use the existing midpoint mapping:

- category 1 -> 0
- category 2 -> 0.05
- category 3 -> 0.175
- category 4 -> 0.375
- category 5 -> 0.625
- category 6 -> 0.875

Primary screen: OLS + HC3.

For shortlisted variables repeat with alternative top-bin coding:
- category 6 -> 1.0.

This outcome is an approximate stated MPC measure and must be labeled as such.

## 7. Outcome 3: top-MPC indicator

Define:
- Top75 = 1 if category 6 (>75%);
- 0 otherwise.

Primary screen: linear probability model with HC3.

For shortlisted variables:
- logit;
- probit;
- average marginal effects.

The point of using all three outcomes is:
- ordinal = overall rank shift;
- midpoint = approximate average MPC shift;
- Top75 = high-MPC-tail compression.

---

# PART III. TWO TARGET SLOPE QUESTIONS

## 8. Target A: Cash amount-slope moderation

Preserve:
- z = (-1, 0, 1) for 200 / 1000 / 5000.

Within Cash, for each X estimate:

Y = a + b z + c X + d (z × X) + e

Main screening estimand:
- d = z × X.

Interpretation:
- how the Cash amount slope changes with X.

For standardized continuous/rank X:
- d is the slope change per 1 SD higher X.

For categorical X:
- use a full interaction block;
- report an omnibus moderation test;
- also report category-specific slopes for visualization.

## 9. Target B: Restricted-vs-Cash slope moderation

Use the exact equal-weight Restricted contrast from PR #10:
- Restricted = 0.5 Food + 0.5 Medical.

For each X estimate the full model containing:
- form;
- z;
- X;
- form × z;
- form × X;
- z × X;
- form × z × X.

Main screening estimand:
- Restricted × z × X.

Interpretation:
- how the Restricted-vs-Cash slope difference changes with X.

Also retain Food-vs-Cash and Medical-vs-Cash three-way interactions as diagnostics, but do not multiply the headline search space by promoting them all to co-primary outcomes.

---

# PART IV. STANDARDIZATION AND CODING

## 10. Continuous / ordinal variables

For numeric or ordered variables with enough support:
- preserve the raw variable;
- create a standardized version using the R sample mean/SD;
- use the standardized version in the main coefficient ranking.

Also keep:
- original-unit coefficient in a supplemental table.

Do not force strongly categorical variables into a linear numeric trend.

## 11. Categorical variables

For unordered categorical variables:
- use factor coding;
- estimate omnibus interaction tests;
- report category-specific predicted slopes.

For ordered categories:
- if prior analysis already has a justified rank coding, screen both:
  - the raw factor form;
  - the constructed rank form.

Record these as related representations.

## 12. Missing values

Use complete-case estimation per X for the univariate screen.

Report N for every model.

Do not impute missing X values solely to increase significance.

For joint exploratory models, use only variables with adequate coverage and document the resulting common sample.

---

# PART V. MULTIPLE TESTING

## 13. Why correction is essential

This pass intentionally scans many variables.

Therefore raw p-values alone are descriptive and must not be used to decide which variables "explain" the curve.

## 14. Main correction strategy: FDR

Use Benjamini-Hochberg FDR as the primary exploratory correction because the goal is discovery rather than a small confirmatory family.

Apply FDR separately within these six families:

1. Cash-slope moderation — ordinal Y.
2. Cash-slope moderation — midpoint Y.
3. Cash-slope moderation — Top75 Y.
4. Restricted-vs-Cash moderation — ordinal Y.
5. Restricted-vs-Cash moderation — midpoint Y.
6. Restricted-vs-Cash moderation — Top75 Y.

Report:
- raw p;
- BH q-value.

Primary discovery thresholds:
- q < .05 = strong exploratory signal;
- .05 <= q < .10 = suggestive exploratory signal.

## 15. Family-wise sensitivity

Also compute Holm-adjusted p-values within the same six families as a stricter sensitivity check.

Do not require Holm significance for exploratory ranking, but clearly distinguish:
- FDR discoveries;
- Holm-surviving findings;
- raw-only nominal findings.

## 16. Redundancy-aware interpretation

Because raw and constructed variables are correlated and sometimes near-duplicates:
- do not count multiple representations of one construct as multiple discoveries;
- cluster / group variables by raw_constructed_mapping and obvious survey-scale families for interpretation.

Do not alter p-value correction based on observed results.

---

# PART VI. CROSS-OUTCOME CONCORDANCE

## 17. Main ranking should reward replication across Y definitions

For each X create a cross-outcome summary:

For Cash moderation:
- ordinal interaction sign / q;
- midpoint interaction sign / q;
- Top75 interaction sign / q.

For Restricted-vs-Cash moderation:
- same three outcomes.

Create:
- cross_outcome_concordance.csv

## 18. Candidate classification

Classify variables into:

### Tier A — cross-outcome robust candidate
Must satisfy:
- same substantive direction in all 3 Y definitions;
- q < .10 in at least 2 outcomes;
- no major sign reversal;
- effect is not driven solely by one raw/constructed representation.

### Tier B — outcome-specific candidate
- q < .10 in one outcome only;
- other outcomes directionally compatible but weak.

### Tier C — nominal only
- raw p < .05 but q >= .10.

### Tier D — null / inconsistent
- no meaningful signal or sign reversals.

Do not call Tier B/C a mechanism result.

---

# PART VII. RAW-VS-CONSTRUCTED CONCORDANCE

## 19. Compare raw items to constructed measures

For every constructed variable with identifiable raw components:
- report the constructed-variable slope interaction;
- report component-item interactions;
- report whether the construct-level signal is:
  - broad across components;
  - driven by one item;
  - canceled across components;
  - absent in raw items.

Create:
- raw_constructed_concordance.csv

This is especially important for subjective / psychological scales.

A constructed index should not be interpreted as a stable mechanism if only one component item generates the result.

---

# PART VIII. SUBJECTIVE VS OBJECTIVE COMPARISON

## 20. Compare discovery yield by variable type

Using the inventory tags, summarize separately:

- subjective variables;
- objective variables;
- constructed subjective indices;
- constructed objective measures.

For each group report:
- number of X variables screened;
- number with q < .10;
- number with q < .05;
- number with consistent sign across all 3 outcomes;
- number with Holm significance.

Do not use these counts as formal tests unless explicitly implemented.

Purpose:
- answer whether subjective variables appear more informative for slope heterogeneity than objective variables.

---

# PART IX. STABILITY AND VALIDATION

## 21. Sample stability for shortlisted variables

For Tier A and strongest Tier B candidates only, repeat in:
- R;
- A;
- C;
- Q1;
- Q2.

Report:
- interaction estimate;
- CI;
- sign;
- N.

Do not require significance in every screen.

Flag:
- sign reversals;
- large attenuation;
- Q1/Q2 collapse.

## 22. Adjustment robustness

For shortlisted variables compare:
- unadjusted;
- fixed objective+needs control block already used in PR #9/#10.

If X itself is part of the control block, do not double-include it improperly.

The randomized treatment interaction remains the estimand; adjustment is for precision and robustness.

## 23. Functional-form robustness

For shortlisted variables:
- ordinal OLS -> ordered logit/probit;
- midpoint -> alternative top=1;
- Top75 LPM -> logit/probit AME.

A candidate is stronger if the sign and substantive story survive these changes.

---

# PART X. DISCOVERY / VALIDATION SPLIT

## 24. Cross-fit stability ranking

Because the same dataset is being used for broad discovery, implement a simple cross-fit stability screen.

Use 5 folds stratified by the 9 randomized cells.

For each X and each primary outcome/target:
- estimate the interaction in 4/5 training data;
- apply the fitted interaction direction to the held-out fold;
- repeat across folds.

At minimum report:
- number of folds with same-sign interaction;
- median training estimate;
- held-out score / calibration diagnostic where feasible.

The purpose is NOT to claim independent validation.
It is to detect variables whose sign is extremely unstable.

Do not use the cross-fit result to tune the variable definition.

---

# PART XI. JOINT EXPLANATORY MODELS

## 25. Build small joint models from screened candidates only after ranking

Do not put all raw and constructed variables into one saturated interaction model.

Instead:

### Joint model A — top cross-outcome candidates
Include only Tier A variables, with:
- main effects;
- z × X;
- Restricted × z × X;
- appropriate lower-order terms.

### Joint model B — one representative per construct
If multiple raw/constructed variants represent the same construct, choose one representative using a rule defined before inspecting joint-model coefficients:
- prefer the previously constructed validated index;
- otherwise prefer the original survey variable with best interpretability.

Do not choose based on smallest p-value.

## 26. Joint model outputs

Report:
- whether candidate interactions remain directionally stable jointly;
- joint Wald test for Cash moderation;
- joint Wald test for Restricted-vs-Cash moderation;
- average randomized slope difference before / after interactions;
- 5-fold OOF MSE or log loss improvement relative to a level-only model.

Do not interpret prediction gain as causal mechanism proof.

---

# PART XII. OPTIONAL LOW-DIMENSIONAL REGULARIZATION

## 27. LASSO / elastic net as a diagnostic only

If implementation is straightforward, run one cross-validated regularized interaction model using:
- eligible standardized raw and constructed X;
- z × X terms;
- Restricted × z × X terms.

Purpose:
- check whether any coherent set of variables repeatedly enters.

Do not use:
- SHAP;
- random forest;
- boosted trees;
- causal forest;
- black-box HTE.

Report selection frequency across folds / resamples, not just one fitted model.

Do not let this replace the transparent univariate screen.

---

# PART XIII. WHAT COUNTS AS AN EXPLANATORY CANDIDATE?

## 28. Strong exploratory candidate

A variable / construct can be discussed as a serious candidate only if most of the following hold:

1. q < .10 in at least 2 of the 3 Y definitions;
2. same sign across all 3;
3. raw and constructed representations are coherent;
4. major sample screens do not reverse sign;
5. functional-form robustness is directionally consistent;
6. it survives or remains meaningful in a small joint model;
7. cross-fit sign stability is acceptable.

Even then use:
- "candidate explanatory correlate";
- "consistent with";
- "associated with treatment sensitivity".

Do not use:
- "mechanism established";
- "causes the slope".

## 29. If nothing survives

If no variable meets the above standard, report:

> Rich observed subjective and objective characteristics do not yield a stable explanatory signature for the form-by-size pattern.

This is a valid outcome.

Do NOT launch another variable search.

---

# PART XIV. REQUIRED OUTPUTS

Create:

消费调查/results/mpc_allx_screen/

Required files:

1. all_x_variable_inventory.csv
2. raw_constructed_mapping.csv
3. allx_cash_ordinal.csv
4. allx_cash_midpoint.csv
5. allx_cash_top75.csv
6. allx_rc_ordinal.csv
7. allx_rc_midpoint.csv
8. allx_rc_top75.csv
9. cross_outcome_concordance.csv
10. raw_constructed_concordance.csv
11. subjective_objective_summary.csv
12. shortlisted_robustness.csv
13. crossfit_stability.csv
14. joint_candidate_models.csv
15. optional_regularized_selection.csv if implemented
16. audit / reproducibility note

No respondent-level exports.

---

# PART XV. REQUIRED FIGURES

## Figure 1 — all-X Cash slope screen
Forest / volcano style summary for Cash amount-slope moderation, separated by:
- subjective;
- objective;
- constructed.

Use FDR labels.

## Figure 2 — all-X Restricted-vs-Cash screen
Same structure for the three-way interaction.

## Figure 3 — cross-outcome concordance
For top candidates, show interaction estimates for:
- ordinal;
- midpoint;
- Top75.

## Figure 4 — raw vs constructed
For candidate constructs, show raw items and constructed index side by side.

## Figure 5 — candidate subgroup curves
Only for Tier A candidates.

## Figure 6 — subjective vs objective discovery summary
Descriptive comparison only.

All figures need source-data CSVs.

---

# PART XVI. FINAL REPORT

Create:

消费调查/MPC_ALLX_SCREEN_RESULTS.md

with exactly these sections:

## 1. Bottom line
Do rich observables identify stable slope heterogeneity?

## 2. Variable inventory
What was included/excluded and why?

## 3. Cash slope screen — ordinal
Top findings and FDR.

## 4. Cash slope screen — midpoint
Top findings and FDR.

## 5. Cash slope screen — Top75
Top findings and FDR.

## 6. Restricted-vs-Cash screen — ordinal

## 7. Restricted-vs-Cash screen — midpoint

## 8. Restricted-vs-Cash screen — Top75

## 9. Cross-outcome concordance
Which variables survive more than one Y definition?

## 10. Subjective vs objective
Do subjective variables add more slope information?

## 11. Raw vs constructed
Are signals construct-level or item-specific?

## 12. Stability and robustness
R/A/C/Q1/Q2, functional form, adjustment.

## 13. Cross-fit stability
Which signals are stable enough to take seriously?

## 14. Joint explanatory power
Do top candidates jointly explain meaningful slope heterogeneity?

## 15. Candidate mechanism interpretation
What can and cannot be said?

## 16. Paper implication
Choose one:
- a coherent subjective/behavioral mechanism candidate emerges;
- several explanatory correlates emerge but no single mechanism;
- rich observables still explain little.

## 17. Final stop decision
No further variable exploration after this screen.

---

# PART XVII. IMPORTANT CLAIM DISCIPLINE

This is an exploratory screen.

Therefore:
- raw p < .05 is never enough by itself;
- FDR is the main discovery control;
- Holm is a stricter sensitivity;
- cross-outcome consistency matters;
- sample stability matters;
- raw/constructed coherence matters;
- cross-fit stability matters.

Do not promote a variable to the paper mechanism based on one favorable specification.

The ideal final result is not "we found many significant variables."

The ideal result is one of two clean outcomes:

A. A small, coherent set of subjective/behavioral constructs robustly predicts slope heterogeneity across multiple Y definitions.

or

B. Even rich subjective and objective observables fail to produce stable slope heterogeneity, strengthening the reduced-form puzzle.

Either is scientifically useful.
