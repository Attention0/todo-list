# NHB reviewer re-analysis protocol — 2026-09-25

## Why this round exists

The current NHB manuscript makes a strong claim about **cross-context portability of individual behavioural prediction**. Reviewer comments identify several points that could materially change the paper rather than merely polish it.

This round is therefore a **claim-validation and re-analysis round**, not a manuscript-writing round.

Do **not** begin by rewriting the abstract, Introduction, Discussion, or figure captions. First establish what the data actually support.

The key question is:

> Is predictive mapping genuinely less portable across transfer forms, relative to an appropriate within-context benchmark, or is the main structure instead that cash and food are approximately invariant while the medical-account condition changes the behavioural construct/mapping more substantially?

The reviewer supplied some numerical claims in comments. Treat every such number as a **hypothesis to independently reproduce**, never as an input to the analysis or as ground truth.

---

# A. Non-negotiable principles

1. Use the existing raw survey data, questionnaire/codebook, and current analysis code as the source of truth.
2. Preserve the original randomized 3×3 design:
   - form: cash / food voucher / medical account;
   - amount: RMB 200 / 1,000 / 5,000.
3. Do not change the primary sample or variable coding silently.
4. Every deviation from the current manuscript pipeline must be documented.
5. Do not select models, transformations, exclusions, or seeds because they produce a preferred result.
6. Report effect sizes and uncertainty, not only significance labels.
7. Distinguish clearly:
   - randomized mean effects;
   - predictive performance;
   - cross-context transport/portability;
   - HTE ranking;
   - exploratory moderators;
   - mechanism speculation.
8. The outcome is hypothetical/stated additional consumption, not realized spending or welfare.
9. Never upload respondent-level raw data or sensitive personal information to GitHub.
10. Commit code, aggregate tables, figures, diagnostics, and reports only.

---

# B. First task: reproduce the current manuscript exactly

Before changing anything, reproduce all current headline quantities from the manuscript with the existing pipeline.

At minimum verify:

- N = 5,497 and all nine cell sizes;
- pooled food-minus-cash and medical-minus-cash effects;
- full-model out-of-sample R² around the value reported in the manuscript;
- cash→food, cash→medical, food→medical rank-transfer statistics;
- domain-drop results;
- food-vs-cash and medical-vs-cash HTE calibration/separation results;
- pooled policy-value result.

Create a machine-readable table:

`消费调查/results/nhb_reanalysis/00_current_manuscript_reproduction.csv`

and a short report:

`消费调查/results/nhb_reanalysis/00_REPRODUCTION.md`

For every headline result mark:
- reproduced exactly;
- reproduced within numerical tolerance;
- not reproduced;
- impossible to verify, with reason.

If a current headline result cannot be reproduced, stop treating the manuscript number as authoritative and explain the discrepancy before proceeding.

---

# C. Study-design and measurement audit

This is essential because the manuscript currently describes the three conditions as closely aligned contexts.

## C1. Exact vignette wording

Extract the exact Chinese wording shown to respondents in all 9 scenarios, including the outcome question and all response options.

Create:

`消费调查/results/nhb_reanalysis/01_VIGNETTE_WORDING_AUDIT.md`

For each condition record:
- transfer label;
- permitted uses;
- cash convertibility;
- validity horizon;
- any account/voucher restrictions;
- whether household/family use is explicit;
- whether future use is possible;
- exact outcome-question wording;
- exact six response categories;
- any condition-specific wording differences.

Do not paraphrase away wording differences.

Explicitly answer:

> Are respondents truly answering the same measurement question across cash, food, and medical arms, or are there wording/construct differences that could themselves generate mapping differences?

## C2. Question order / priming

Map the questionnaire order around the treatment vignette.

Record which baseline variables occur:
- clearly before randomization/treatment;
- immediately before the vignette;
- after the vignette.

Pay special attention to medical expenditure, subsidy experience, social protection, liquidity, expectations, and any question that may make a treatment domain salient.

If any supposed “baseline predictor” was measured after treatment, it must not be used as a baseline predictor.

---

# D. Sample-quality and ethics audit

The reviewer comments raise concerns that cannot be left implicit.

Create:

`消费调查/results/nhb_reanalysis/02_SAMPLE_QUALITY_ETHICS.md`

## D1. Age and minors

Independently count:
- respondents <18;
- respondents =18;
- respondents >18.

Do not assume the reviewer’s claimed number is correct.

Produce headline results under:
1. full valid randomized sample;
2. adults-only sample.

Flag the ethics/consent issue for author input. Do not invent IRB/ethics approval information.

## D2. Internal consistency and platform variables

Audit:
- age;
- education;
- income;
- occupation;
- employment/student status;
- household composition;
- platform-profile variables versus survey-reported variables;
- duplicate or conflicting demographic fields;
- impossible or contradictory combinations;
- straight-lining / patterned response if detectable;
- timing, IP, device, attention checks, quality flags, if actually available.

Do not delete observations solely because they look unusual.

Define:
- `raw_valid_sample`;
- `adult_sample`;
- `clean_candidate_sample`;

with a transparent flow chart/table of exclusions/flags.

The clean-candidate rule must be deterministic and documented before rerunning the substantive models.

---

# E. Core analysis 1 — the missing within-context benchmark

This is the most important task of this round.

The current manuscript reports cross-form prediction statistics without an adequate within-form reference. Build the full benchmark.

## E1. Full 3×3 source-target matrix

For each transfer form source (s ∈ {cash, food, medical}):

1. train the exact same prediction pipeline on source-form respondents;
2. obtain out-of-sample prediction performance on:
   - the same form (within-context diagonal);
   - each of the two other forms (cross-context off-diagonal).

The diagonal must be genuinely out-of-sample. Never evaluate a model on observations used to fit it.

Use common, reproducible folds/seeds.

Primary predictive ranking metric:
- Spearman rank correlation between OOF/source-model prediction and observed target outcome.

Also report:
- Pearson correlation;
- target-centered R² / another defensible scale metric if already used;
- uncertainty.

## E2. Sample-size matching

Cross-context source training sets and within-context diagonal training sets must be comparable.

Implement at least one matched-training-size benchmark so a diagonal advantage is not mechanically driven by more training data.

Document the matching procedure.

## E3. Target-normalized portability

Raw cash→food versus cash→medical correlations are not enough because food and medical outcomes may differ in inherent predictability.

For each target form (t), calculate metrics such as:

- `absolute_cross_perf(s→t)`;
- `within_target_perf(t→t)`;
- `portability_gap = cross - within_target`;
- `relative_portability = cross / within_target` when denominator is safely away from zero;
- rank-based difference with respondent-level uncertainty.

The most interpretable comparison should ask:

> How much predictive performance is lost by transporting a model into target t, relative to a model trained within target t?

Do not compare different targets without accounting for their within-target predictability.

## E4. Uncertainty

Do not bootstrap the small set of fold scores as if they were independent observations.

Primary uncertainty should use respondent-level resampling with model refitting where computationally feasible.

At minimum, bootstrap both:
- the source training respondents;
- the target evaluation respondents.

Preserve randomized-arm structure.

If full refit bootstrap is computationally expensive, document a staged solution:
- headline refit bootstrap for the key comparisons;
- cheaper conditional-on-fit diagnostics as secondary only.

## E5. Deliverables

Create:
- `03_portability_matrix.csv`;
- `03_portability_normalized.csv`;
- `03_PORTABILITY_REPORT.md`;
- a new heatmap including the diagonal;
- a figure of target-normalized portability gaps with 95% CIs.

The report must explicitly answer:
1. Is cash→food meaningfully worse than food→food?
2. Is cash→medical meaningfully worse than medical→medical?
3. Is the portability loss larger for medical than food?
4. Does the answer survive matched training sizes?
5. Does it survive adult-only and clean-candidate samples?

---

# F. Core analysis 2 — direct invariance / additive-shift tests

The conceptual null in the paper is close to:

> transfer form changes only a common intercept/mean shift, while the mapping from individual covariates X to response remains invariant.

Test that null directly.

## F1. Linear / regularized interaction benchmark

Construct a transparent benchmark on the same locked predictor set.

Compare nested models conceptually equivalent to:

1. `Y ~ form + amount + X`
2. `Y ~ form + amount + X + X×form`
3. where useful, include amount interactions explicitly and separately.

Use held-out prediction to compare model 1 versus model 2.

Report:
- incremental OOS R² from X×form;
- joint tests / permutation or bootstrap tests appropriate to the chosen model;
- separate evidence for Food×X and Medical×X;
- pairwise mapping differences.

Do not use “one significant, one insignificant” as evidence that two contexts differ. Directly test the difference.

## F2. Flexible nonlinear benchmark

Repeat the invariance question with a flexible learner:

- common model with form as an additive feature;
- context-specific models / interactions.

Evaluate whether context-specific flexibility produces a real held-out gain.

The purpose is not to maximize prediction; it is to test whether allowing the X→Y mapping to vary by form improves generalization.

## F3. Amount heterogeneity

If RMB 1,000 looks different from RMB 200 or 5,000, test the **difference itself**.

Do not infer amount moderation from:
- significant at 1,000;
- insignificant at 200 and 5,000.

Run a formal contrast / interaction.

## F4. Interpretation discipline

Possible outcomes:

- **Food approximately additive/invariant, Medical non-invariant:** this supports a boundary-condition interpretation.
- **Both non-invariant:** stronger portability-breakdown evidence.
- **Neither clearly non-invariant:** current portability claim is unsupported and must be rewritten.
- **Results unstable to sample/metric/model:** report instability; do not choose the preferred specification.

Deliver:
- `04_invariance_tests.csv`;
- `04_INVARIANCE_REPORT.md`;
- one compact figure comparing additive versus context-specific predictive performance.

---

# G. Core analysis 3 — data-quality robustness for all headline analyses

The current manuscript only uses response-quality screens narrowly. That is not enough.

For each of the following, rerun the **entire core pipeline** under:
1. raw valid sample;
2. adults only;
3. clean candidate sample;
4. any previously used Q1/Q2 quality screen, clearly defined.

Core pipeline:
- randomized mean effects;
- pooled prediction;
- 3×3 portability benchmark;
- direct invariance test;
- HTE validation.

Create:
- `05_sample_robustness_summary.csv`;
- `05_SAMPLE_ROBUSTNESS.md`.

Do not make the clean sample the primary sample unless there is a defensible pre-specified/measurement reason. The point is robustness and diagnosis.

---

# H. Core analysis 4 — food-voucher inframarginality

This is theoretically important and is already alluded to in Methods but not integrated into the Results.

Use the actual survey food-spending intervals and the 6-month food-voucher validity horizon.

Construct a bounds-based classification, not a midpoint-only classification:

- definitely inframarginal;
- ambiguous / potentially binding;
- likely binding/extramarginal.

For open-ended intervals, document conservative bounds.

Then estimate Food − Cash by bindingness class.

Primary question:

> Among respondents for whom the food voucher is clearly inframarginal relative to baseline six-month food expenditure, is Food approximately equivalent to Cash, or does a robust difference remain?

Report:
- cell N;
- treatment contrasts + 95% CI;
- direct heterogeneity test;
- ordinal-outcome version;
- midpoint version as auxiliary.

Because baseline food expenditure is observational, do not call this a causal mechanism test.

Also check whether the result differs by transfer amount in a formally tested interaction.

Deliver:
- `06_food_inframarginality.csv`;
- `06_FOOD_INFRAMARGINALITY.md`;
- one figure with Food−Cash effects by bindingness class and amount if precision allows.

---

# I. Core analysis 5 — HTE validation and corrected inference

The current HTE section needs to be made more transparent and less seed/significance driven.

## I1. Separate contrasts

For:
- Food − Cash;
- Medical − Cash;

report separately:
- calibration slope + 95% CI;
- top-minus-bottom observed treatment-effect separation + 95% CI;
- quintile/bin plots using held-out predictions;
- exact N.

Do not make the main evidence “medical minus food is significant” while hiding the individual calibration estimates.

## I2. Direct comparison

Then directly compare Medical versus Food heterogeneity predictability using shared-cash-aware resampling.

## I3. One standard complementary validation

Add one defensible standard validation framework such as:
- BLP/GATES; or
- RATE/AUTOC.

Choose one and explain why. Do not add many methods just to search for significance.

## I4. Seeds

Multiple fold seeds are robustness checks only.

Do not treat “positive in all 10 seeds” as 10 independent replications.

## I5. Amount-specific HTE

If the RMB 1,000 signal remains interesting, test HTE predictability differences across amounts directly.

Unless a direct amount interaction is supported, keep RMB 1,000 subgroup results exploratory/SI-level.

Deliver:
- `07_hte_validation.csv`;
- `07_HTE_REPORT.md`;
- revised HTE figure.

---

# J. Analyses to downgrade or audit before keeping in the main paper

## J1. Ridge coefficient-vector similarity

Audit whether coefficient-vector correlations are stable to:
- encoding;
- standardization;
- collinearity;
- bootstrap.

If intervals/point estimates are internally inconsistent or the metric is unstable, remove it from the main paper rather than repairing cosmetically.

## J2. Classical attenuation panel

Do not mechanically “correct” cross-context prediction correlations using an assumed common outcome reliability.

Because reliability is not estimated and may differ by form, this should probably be removed from the main figure unless a clearly defensible interpretation can be written.

## J3. Domain-drop localization

Audit correlated predictors/domains.

Do not infer:

> no domain-level difference is significant ⇒ mapping shifts are distributed.

The only valid statement may be:

> we could not localize the difference to a single pre-defined domain with adequate precision.

If the method cannot support more, move the figure to SI/Extended Data.

## J4. Policy learning

Move pooled policy-learning analysis to SI unless it becomes directly necessary to the paper’s revised claim.

The current stated-consumption objective structurally gives unrestricted cash substantial headroom, and a policy tree that assigns everyone to cash adds little to the central scientific question.

Do not interpret policy value as welfare.

---

# K. Prediction feature audit

Create a complete table for the 41 predictors:

`08_predictor_dictionary.csv`

For each predictor include:
- raw question/field;
- exact wording;
- whether self-report or platform field;
- pre-treatment status;
- coding;
- missing handling;
- domain assignment;
- whether objective/subjective;
- any ambiguity.

For subjective items:
- report correlation matrix summary;
- PCA eigenvalues / explained variance;
- internal consistency where meaningful.

Do not claim “psychology is one-dimensional” unless the measurement structure truly warrants that statement.

---

# L. Mean effects and ordinal outcome robustness

For all headline mean-effect analyses:

1. report original 6-category distributions;
2. ordinal model / cumulative-threshold evidence;
3. ordinal-score OLS as descriptive;
4. midpoint MPC only as an auxiliary economic scale.

Report form × amount patterns directly.

Do not interpret midpoint coding as observed MPC.

Do not infer treatment-form differences from different significance labels.

---

# M. Decide the paper’s empirical story only after the above results

After completing Sections B–L, produce:

`消费调查/results/nhb_reanalysis/09_DECISION_MEMO.md`

This memo must choose among evidence patterns, not desired narratives.

It should answer:

## M1. What is the strongest defensible empirical statement?

Evaluate at least these possibilities:

### Pattern A — broad non-portability
Both food and medical produce material target-normalized portability loss and direct X×form evidence.

### Pattern B — boundary condition
Cash–food is approximately stable/additive, while medical shows larger mapping change.

### Pattern C — mostly low predictability, little evidence of contextual remapping
Cross-context performance is low because within-context prediction is also low, and direct invariance tests provide little support for remapping.

### Pattern D — unresolved
Results depend strongly on metric, model, sample screen, or coding.

The memo must state which pattern the evidence most closely supports and why.

## M2. What must change in the manuscript?

Without rewriting the manuscript yet, list exact implications for:
- title;
- abstract;
- Introduction claim;
- definition of “context”;
- BGLS/cognitive-theory role;
- mental-accounting/fungibility literature;
- stated-MPC validity literature;
- Results structure;
- Discussion;
- Constraints on Generality;
- Methods;
- main versus SI figures.

## M3. Proposed main-figure set

Propose a parsimonious main-text set.

Default candidate:
1. design + randomized mean effects;
2. within-context predictability;
3. normalized portability + invariance;
4. HTE validation / contrast asymmetry.

Domain localization and policy learning should remain SI unless the new evidence makes them essential.

---

# N. Statistical and computational reproducibility requirements

1. Set and record random seeds.
2. Reuse common folds where comparisons require paired evaluation.
3. Never use target outcomes to tune/refit a transported source model.
4. For model selection/tuning, avoid leakage from held-out evaluation observations.
5. Store all model settings/hyperparameters in a readable config or report.
6. Record package versions and software environment.
7. Save intermediate aggregate results required to regenerate every figure.
8. Use scripts rather than notebook-only manual cells when possible.
9. Every final number in the report must be traceable to a script and aggregate output.

---

# O. Required GitHub deliverables

Create the directory:

`消费调查/results/nhb_reanalysis/`

At minimum commit:

- `00_REPRODUCTION.md`
- `00_current_manuscript_reproduction.csv`
- `01_VIGNETTE_WORDING_AUDIT.md`
- `02_SAMPLE_QUALITY_ETHICS.md`
- `03_PORTABILITY_REPORT.md`
- `03_portability_matrix.csv`
- `03_portability_normalized.csv`
- `04_INVARIANCE_REPORT.md`
- `04_invariance_tests.csv`
- `05_SAMPLE_ROBUSTNESS.md`
- `05_sample_robustness_summary.csv`
- `06_FOOD_INFRAMARGINALITY.md`
- `06_food_inframarginality.csv`
- `07_HTE_REPORT.md`
- `07_hte_validation.csv`
- `08_predictor_dictionary.csv`
- `09_DECISION_MEMO.md`
- figure files for the new benchmark/invariance/HTE results
- all new or modified analysis scripts needed to reproduce them.

Do not commit:
- raw respondent-level data;
- respondent identifiers;
- potentially identifying free text;
- credentials;
- private survey-platform exports containing sensitive individual records.

---

# P. Stop conditions / things that require human input

Do not invent or infer the following:

- ethics committee / IRB identity or approval number;
- informed-consent language;
- original prospective power calculation;
- original stopping rule;
- platform recruitment quotas not documented in source materials;
- whether minors were legally/ethically covered by consent;
- a public data-release permission that has not been granted.

Instead put them in a clearly titled **AUTHOR INPUT REQUIRED** section of the relevant report.

---

# Q. Final Work response

When this round is complete, do not merely say “done”.

Return a concise summary containing:

1. whether all current manuscript headline results reproduced;
2. the 3×3 portability matrix headline;
3. normalized portability loss for Food and Medical targets;
4. direct invariance-test conclusion;
5. adult-only / clean-sample robustness;
6. food inframarginality result;
7. separate Food−Cash and Medical−Cash HTE validation;
8. which empirical Pattern A/B/C/D is supported;
9. any fatal data/ethics/measurement concern;
10. exact Git commit / paths containing the reports and code.

Most importantly: **do not rewrite the NHB manuscript until the empirical pattern has been settled.**
