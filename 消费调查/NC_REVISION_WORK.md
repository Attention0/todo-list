# NC Revision Work Plan — evidence first, story second

Project: 消费调查  
Target: Nature Communications revision audit  
Purpose: respond to the second simulated NC review using existing data plus transparent external benchmarks.

## 0. Non-negotiable rules

1. Do not rewrite the manuscript yet. This task is an analysis/revision audit. Final deliverables are results, figures/tables, literature verification, and a decision memo. Chat will rewrite the manuscript after reviewing the returned evidence.
2. The study was not preregistered. Never use “pre-specified”, “confirmatory”, “approved”, “locked” or similar wording to imply otherwise.
3. Before running any new analysis, save revision_spec_manifest.json listing outcomes, contrasts, samples, amount parameterizations, model families, moderator variables, multiplicity families, and decision rules. Do not add specifications after seeing results unless a bug is found; log any bug-driven change.
4. Do not chase significance. Report point estimate, 95% CI, raw P, adjusted P, N, and exact estimand.
5. Distinguish Fact / Inference / Elimination / Interpretation / Speculation in all result notes.
6. Restricted = exactly 0.5 Food + 0.5 Medical and is a derived summary, never a fourth randomized arm.
7. Food and Medical must be shown separately before any pooled Restricted summary.
8. Outcomes are hypothetical stated spending responses, not realized spending.
9. If a proposed analysis is impossible because the data lack a variable, return NOT FEASIBLE with the exact reason. Do not invent proxies.
10. Preserve existing raw data and historical results. Put all new work under 消费调查/results/nc_revision_audit/.

## 1. Existing material to reuse

Reuse existing scripts/results first:
- 消费调查/results/mpc_size_curve/
- 消费调查/results/mpc_final_strengthening/
- 消费调查/results/mpc_allx_screen/
- 消费调查/results/nature_main_figures/
- 消费调查/results/mpc_hero_figure/

Relevant branches if needed:
- feature/mpc-size-curve
- feature/mpc-final-strengthening
- feature/mpc-allx-screen
- feature/nature-main-figures
- feature/mpc-hero-figure

Do not count old analyses as independent replications.

# PHASE A — M1: lock the focal estimand and quantify researcher degrees of freedom

## A1. Focal estimand

Use the original >75% category (Top75) as the focal outcome and test a 3-form × log(amount) / centered trend interaction.

Amount coding:
- z = -1, 0, 1 for RMB 200, 1000, 5000;
- one unit = a fivefold amount increase.

Focal omnibus null:
- Cash, Food, Medical amount slopes are equal.

Then decompose:
- Cash vs Food slope difference;
- Cash vs Medical slope difference.

Do not make equal-weight Restricted the sole focal test. Restricted is secondary.

Required output: table_A1_focal_estimand.csv with Cash/Food/Medical slopes, omnibus 2-df interaction, Cash–Food and Cash–Medical slope differences, optional Restricted–Cash secondary summary, 95% CI, raw P and adjusted P.

## A2. Frozen finite specification family

Freeze and run the following grid.

Outcomes:
1. ordinal 1–6;
2. midpoint-coded stated MPC;
3. any spending;
4. >=10%;
5. >=25%;
6. >=50%;
7. >75%.

Contrasts:
1. 3-form omnibus form × amount interaction;
2. Cash vs Food slope;
3. Cash vs Medical slope;
4. Food vs Medical slope;
5. secondary equal-weight Restricted vs Cash.

Samples:
- R / full;
- A / adult;
- C / clean;
- Q1;
- Q2.

Amount representations:
- centered log trend;
- saturated amount indicators;
- endpoint RMB 5000 vs RMB 200.

Models, only where appropriate:
- OLS / LPM with HC3;
- logit and probit for binary thresholds;
- ordered logit and ordered probit for ordinal;
- location-scale / heterogeneous-choice ordered model if implementable.

Outputs:
- specification_grid.csv, one row per frozen specification;
- specification/forest plot with all estimates, never selected by significance;
- planned / estimable / failed counts.

## A3. Global max-T correction

This is the highest-priority new robustness analysis.

Correct for the fact that outcome, threshold, contrast, model form and sample were analysis choices.

Use a constrained null that:
- preserves form main effects;
- preserves amount main effects;
- imposes no form × amount interaction / equal form-specific amount slopes.

Construct the null distribution of the maximum absolute t-statistic across the frozen specification family using a suitable bootstrap/resampling procedure.

Requirements:
- at least 5,000 bootstrap draws if feasible, otherwise >=2,000 with explanation;
- same frozen specification grid in every draw;
- output global max-T adjusted P for focal omnibus and focal pairwise contrasts;
- log non-estimable bootstrap fits;
- validate with a small null simulation showing approximate size control.

Files:
- maxT_results.csv
- maxT_diagnostics.md
- maxT_simulation_check.csv
- code.

Decision:
- survives global correction -> may call evidence strong;
- does not survive -> manuscript must use suggests / evidence for, not a strong causal-sounding title;
- do not rescue a weak result by switching outcomes/models.

## A4. Ordered-outcome robustness

Use all six categories:
- ordered logit;
- ordered probit;
- location-scale / heterogeneous-choice ordered model.

Question:
could latent scale/variance differences across form/amount mimic a location interaction?

Output ordered_model_sensitivity.csv with coefficients/contrasts, convergence diagnostics and a short interpretation.

## A5. Bayesian model — optional secondary

If straightforward, fit a hierarchical ordered model using the same frozen form × amount structure. Report posterior probability Cash slope < Food slope and Cash slope < Medical slope.

Do not use Bayesian output to replace A3.

## A6. Analysis history

Create analysis_history.md:
- outcome families and contrasts inspected before this revision;
- current story is post hoc;
- timestamp/specification freeze point;
- any post-freeze deviation and reason.

# PHASE B — M2: Food and Medical must be separated

## B1. Primary display

All primary tables/figures show Cash, Food, Medical separately.

Required:
- form-specific Top75 amount profiles;
- midpoint and ordinal profiles in Extended Data.

Only after this may equal-weight Restricted be shown as a compact secondary summary.

## B2. “Convergence” and equivalence

Do not claim convergence merely because a difference is non-significant.

Preferred wording:
- gap narrows / attenuates.

Run TOST at RMB 5000 only if a defensible SESOI can be justified independently of observed estimates.
If no defensible single SESOI exists:
- do not invent one;
- report ±2pp, ±3pp, ±5pp sensitivity only as revision-stage descriptive analysis;
- state margins were not preregistered.

Output equivalence_sensitivity_5000.csv.

## B3. Thresholds and relative scales

Reproduce:
- Any spending;
- >=10%;
- >=25%;
- >=50%;
- >75%;
- risk ratios;
- odds ratios;
- logit/probit AMEs where appropriate.

Allowed wording:
- “most visible in the upper tail” if supported.

Not allowed:
- “tail-specific” unless direct cross-threshold tests establish it after correction.

## B4. Wording robustness

Document:
- wording differs across form;
- wording is fixed across amount within each form.

Explain:
- form-level gaps can be affected by fixed wording differences;
- within-form amount gradients and differences in gradients are relatively robust to fixed form wording, assuming wording does not interact with amount;
- cross-form no-spending comparisons are more vulnerable than the within-Cash RMB200→RMB5000 comparison.

Create wording_identification_note.md.

# PHASE C — M3: rewrite and test the bindingness benchmark

## C1. Prediction table

Create mechanism_prediction_table.md and .csv with four rows:

1. Full fungibility / inframarginal benchmark
   - expected level gap when fully inframarginal;
   - expected slope difference.

2. Mechanical binding constraint
   - prediction as transfer approaches/exceeds normal eligible spending;
   - prediction for Cash–Food gap versus bindingness.

3. Label / mental-accounting effect
   - may create level gaps even when inframarginal;
   - no unique monotone slope prediction without extra assumptions.

4. Scale-induced categorization / endogenous earmarking
   - small unrestricted Cash unusually spendable;
   - larger Cash may become self-categorized;
   - predicts attenuation of Cash advantage with scale;
   - explicitly labelled an untested interpretation unless Phase D supports it.

Do not write “standard theory predicts the gap must widen.” The correct claim is narrower: a simple mechanical bindingness account makes a directional prediction that can be tested.

## C2. Continuous bindingness ratio

For Cash and Food respondents construct:

r_i = assigned transfer amount / conservative lower bound of six-month food spending.

Rules:
- reuse the already audited lower-bound mapping;
- no arbitrary exact values for open-ended expenditure categories;
- document undefined/zero-denominator cases;
- do not call r-based associations causal because r also contains baseline food spending.

Freeze meaningful bins before outcomes are inspected, suggested:
- r <= 0.10
- 0.10 < r <= 0.25
- 0.25 < r <= 0.50
- 0.50 < r <= 1
- r > 1

Merge only if sparse and log the merge.

Within Cash/Food:
- plot Cash–Food gap by r bin;
- test whether Food effect/gap grows with r;
- Top75 focal; ordinal/midpoint secondary;
- optionally one frozen continuous log-r or monotone trend test.

Core question:
Does the Cash–Food gap increase with actual mechanical bindingness?

Outputs:
- bindingness_ratio_source.csv
- bindingness_ratio_tests.csv
- fig_bindingness_ratio.*

## C3. Fixed inframarginal sample: slope, not only level

Use the existing fixed common sample with conservative six-month food-spending lower bound > RMB5000.

Report:
- pooled Food–Cash level difference;
- Cash amount slope;
- Food amount slope;
- Food–Cash slope difference;
- CI and P.

Do not use the level result to claim the slope mechanism is established.

# PHASE D — M4: test only what can be tested about scale-induced categorization

## D1. Relative-size collapse test

Highest-priority mechanism-oriented analysis.

Construct:

s_i = assigned transfer amount / income scale_i.

Income is banded:
- document midpoint mapping for bounded bands;
- use at least two sensitivity mappings for open-ended bands;
- also run an ordinal/rank-based alternative that does not pretend exact income;
- never call midpoint income observed exact income.

Compare:

ABS model: Outcome ~ form × ln(amount)

REL model: Outcome ~ form × ln(relative amount / income scale)

Use:
- Top75 focal;
- ordinal/midpoint secondary;
- same sample restrictions;
- cross-validated log-loss/MSE or held-out predictive score;
- AIC/BIC secondary only.

Pre-written interpretation:
- REL materially outperforms ABS and predicts earlier compression for lower-income respondents -> supports a relative-scale budgeting/categorization account;
- no improvement -> does not support that specific mechanism;
- mixed -> mechanism unresolved.

Outputs:
- relative_scale_models.csv
- relative_scale_cv.csv
- fig_relative_scale.*
- falsification memo.

## D2. Response-time audit

Search raw survey export/metadata for page timing, item timing, total duration, Qualtrics timing fields.

If absent, write:
NOT FEASIBLE: no response-time metadata in delivered data/export.

Do not create unrelated timing proxies.

## D3. Questionnaire mechanism audit

Audit the full original questionnaire/codebook for:
- intended use;
- saving/debt/housing/education/health allocation;
- planning horizon;
- perceived spendability;
- mental account / earmarking;
- open text;
- reasons;
- other transfer forms;
- other amount arms.

Create questionnaire_mechanism_audit.md with:
- variable;
- exact wording;
- pre/post treatment;
- usable process measure?;
- why/why not.

If usable mechanism variables exist, propose a tiny fixed test set before running. If none exist, stop; do not mine substitutes.

## D4. Mechanism wording rule

Unless D1/D3 produces direct evidence:
- scale-induced categorization is Discussion hypothesis only;
- remove it from title;
- Abstract ending should be:
“A scale-dependent earmarking account is one candidate explanation, but the present design does not directly test this mechanism.”

# PHASE E — M5: heterogeneity and power

## E1. 150-variable screen is supplemental only

Do not infer “broadly shared human tendency” from 150 null moderators.

Move the all-X screen to Supplement/Extended Data.

## E2. Theory-driven moderators

Use only 3–5 theory-driven variables, never chosen by P value.

Priority:
1. relative transfer size / income;
2. emergency liquidity / fundraising capacity;
3. saving or planning tendency, only if directly measured;
4. category-specific baseline need;
5. numeracy / financial sophistication, only if directly measured.

If some are absent, use fewer variables. Do not replace them by searching 150 variables.

For each:
- moderation of Cash amount slope;
- Cash–Food and Cash–Medical slope differences where interpretable;
- Top75 focal; ordinal/midpoint secondary;
- estimate, CI, raw P.

## E3. Power / MDE

For each theory moderator calculate 80% MDE using actual sample sizes and outcome variance/probability, preferably by simulation.

Compare MDE with:
- average Cash slope;
- Cash–Food slope difference;
- Cash–Medical slope difference.

If MDE is larger than the effect of interest, explicitly write:
“the design cannot rule out moderation on the scale of the average interaction.”

Output moderator_power_mde.csv.

## E4. All-X supplemental diagnostic

Keep:
- QQ plots of raw P by family;
- BH q distributions;
- q<0.10/q<0.05 counts;
- no highlighted nominal “winner”.

Reuse a valid existing cross-fitted BLP/GATES/global heterogeneity test if already available. Do not open a new black-box search.

Main-text conclusion later:
- “no stable observed moderator was identified”;
- not “the effect is universal”;
- not “hard to locate across people” unless immediately paired with the power limitation.

# PHASE F — M6: measurement validity, sample quality, external validity, transparency

## F1. Positive controls for stated MPC

Predefine and test only well-established expectations:
1. Cash stated MPC decreases with transfer size.
2. Emergency-liquidity constraints predict higher stated MPC / spending response.
3. Income predicts stated MPC in the expected literature direction, if the existing measure supports a clean test.

Verify the expected direction in the external literature before interpreting results. Do not redefine the expected sign after seeing the data.

Output:
- positive_controls.csv
- positive_control_literature.md

Goal:
assess whether the hypothetical unincentivized measure reproduces established MPC patterns.

## F2. Quality-gradient sensitivity

For the same focal estimand display side-by-side:
- R;
- A;
- C;
- Q1;
- Q2.

Do not hide attenuation.

Explain:
- Q1/Q2 change sample composition;
- they are not pure exogenous quality improvements.

Outputs:
- fig_quality_gradient.*
- source CSV.

## F3. Calibration/raking sensitivity

If a reliable official China benchmark can be obtained:
- use defensible age × education margins;
- document source/year;
- calibrate/rake sample;
- rerun focal form × amount estimand.

Rules:
- do not call weighted sample nationally representative;
- describe as calibration sensitivity;
- if no defensible official benchmark, mark NOT FEASIBLE.

Outputs:
- raking_method.md
- raking_weights_summary.csv
- raking_focal_results.csv

## F4. Missing Methods information

Create author_information_needed.md listing items that cannot be inferred:
- recruitment platform/provider;
- field dates;
- sampling frame;
- quotas;
- respondent incentives;
- invitations/completions/completion rate;
- deduplication;
- sample-size determination/stopping rule;
- arm-specific attrition if applicable;
- consent procedure.

Do not guess.

## F5. Ethics / minors

Check project files for:
- ethics committee / IRB;
- approval/exemption ID;
- consent;
- coverage for 17 respondents age <18.

If minors are not clearly covered:
- flag SUBMISSION BLOCKER;
- recommend adult-only primary sample n=5480 unless authors provide documentation.

## F6. Open-science package

Prepare release checklist only; do not publish sensitive data without author approval.

Package:
- scripts;
- aggregate source data;
- codebook;
- environment/requirements;
- README with reproduction steps;
- de-identified respondent-level data if permissible, otherwise controlled-access statement.

OSF is optional; Zenodo or other stable DOI repository is acceptable.

Create NC_submission_requirements.md with current Nature Communications requirements.

# PHASE G — literature audit and manuscript implications

## G1. Verify every current reference

For every 2025–2026 citation and working paper verify:
- exact title;
- authors;
- journal/status;
- volume/pages/DOI if available;
- exact claim supported.

Create reference_audit.csv:
ref_number, citation, verified, source_url_or_doi, claim_supported, action.

Flag/delete unverified references.

## G2. Add directly relevant literature

Search/map:
- denomination effect;
- magnitude / windfall-size effects;
- stated MPC validity and realized/reported MPC;
- fungibility / inframarginality;
- Hastings–Shapiro fungibility/labeling;
- shopping-voucher/coupon evidence including Taiwan if verified;
- cash vs in-kind / earmarked transfers;
- mental accounting / behavioral life-cycle.

Nature-family papers stay only if directly relevant. Remove citations that look like journal-brand decoration.

Create NC_revision_literature_map.md:
paper | journal/year | exact result | manuscript paragraph supported | keep/add/remove.

## G3. Revised Intro outline only

Do not rewrite manuscript yet. Provide a revised Intro outline:
1. broad transfer-size/form question;
2. classic size/MPC evidence;
3. form/fungibility/labeling evidence;
4. competing predictions / unresolved form × size question;
5. design;
6. headline empirical pattern;
7. bounded contribution.

Literature discussion must be problem-driven, not journal-brand-driven.

# PHASE H — manuscript hygiene assets

Do not rewrite manuscript in this task, but prepare for later revision.

1. Use real figures, no placeholders.
2. Food and Medical shown separately where scientifically necessary.
3. Future manuscript must delete internal workflow language:
   - PR #13/#14;
   - approved;
   - reviewer-style critique;
   - revised narrative structure;
   - branch/commit names.
4. Reduce repeated numbers across Abstract/Intro/Results/Discussion.
5. Future title depends on Phase A3:
   - strong global evidence: “gaps attenuate with transfer size” may be acceptable;
   - weak global evidence: “evidence for…” / “suggests…”.
6. Do not use “reshapes” unless global correction clearly justifies it.
7. Broader implication to evaluate:
   “A transfer-form effect estimated at one amount need not extrapolate to another amount.”

# REQUIRED DELIVERABLES

Create under 消费调查/results/nc_revision_audit/:

1. NC_REVISION_RESULT.md
2. revision_spec_manifest.json
3. analysis_history.md
4. table_A1_focal_estimand.csv
5. specification_grid.csv
6. maxT_results.csv
7. maxT_diagnostics.md
8. maxT_simulation_check.csv
9. ordered_model_sensitivity.csv
10. equivalence_sensitivity_5000.csv or NOT_FEASIBLE note
11. bindingness_ratio_tests.csv
12. bindingness_ratio_source.csv
13. mechanism_prediction_table.md
14. relative_scale_models.csv
15. relative_scale_cv.csv
16. questionnaire_mechanism_audit.md
17. moderator_power_mde.csv
18. positive_controls.csv
19. positive_control_literature.md
20. fig_quality_gradient.* + source CSV
21. raking_method.md + results if feasible
22. author_information_needed.md
23. NC_submission_requirements.md
24. reference_audit.csv
25. NC_revision_literature_map.md
26. all scripts
27. verification_results.json

## Final decision memo

At the top of NC_REVISION_RESULT.md answer:

1. Does the focal form × size result survive global correction?
   - YES / MIXED / NO
   - estimate, CI, global adjusted P.

2. What do Food and Medical separately show?
   - mean pattern;
   - Top75 pattern;
   - which form drives which result.

3. Is simple bindingness supported?
   - continuous r test;
   - fixed-inframarginal slope;
   - supported / incomplete / unresolved.

4. Is relative-scale categorization supported?
   - ABS vs REL comparison;
   - supportive / mixed / unsupported / not testable.

5. Can observed heterogeneity support a “broadly shared human tendency” claim?
   - report MDE;
   - state exactly what can/cannot be ruled out.

6. Does stated MPC pass positive-control checks?
   - YES / MIXED / NO.

7. How stable is focal evidence across R/A/C/Q1/Q2 and weighting?
   - report all.

8. Recommended manuscript strength:
   - A — NC-level main story remains defensible
   - B — interesting but should be framed as suggestive
   - C — do not organize the paper around form × size

Give a 5–10 sentence rationale based only on frozen analyses.

# STOPPING RULE

After the frozen analyses:
- no additional moderator search;
- no new outcomes;
- no tuned thresholds;
- no focal-estimand changes;
- no manuscript rewrite.

Commit/push all results and report the commit or PR URL.
