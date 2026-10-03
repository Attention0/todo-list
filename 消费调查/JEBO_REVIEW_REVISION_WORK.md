# JEBO reviewer-driven revision — Work execution plan

## Mission

Use the scientific specification in:

`消费调查/JEBO_REVIEW_REVISION_SPEC.md`

to produce a new reviewer-response revision based on PR #17.

This task is specifically about correcting logic, estimands, measurement interpretation, and unsupported mechanism claims. It is **not** a generic polishing pass and **not** a request for new exploratory discoveries.

---

## 1. Branching and dependency

Create:

`feature/jebo-review-revision`

from the exact PR #17 head:

`feature/jebo-repositioning@926b05022189661bdfe4dc41d24ad900c77bbd12`

Open a stacked PR against `feature/jebo-repositioning`.

Do not merge PR #17 or older PRs.

Do not modify historical PR #9–#17 result files.

---

## 2. First commit: reviewer analysis protocol

Before any new calculation, create and commit:

- `消费调查/results/jebo_review_revision/REVIEWER_REANALYSIS_MANIFEST.md`
- `消费调查/results/jebo_review_revision/REVIEW_ISSUE_MATRIX.md`

The issue matrix must classify every reviewer point as:
- factual/logical correction accepted;
- analysis required;
- wording/positioning issue;
- author metadata required;
- reviewer claim to verify.

For each point record:
- old manuscript statement;
- why it is problematic;
- exact empirical or textual fix;
- source/result needed;
- status.

This commit must precede all new reviewer-driven result commits.

---

## 3. Questionnaire-boundary audit

Read the original questionnaire, not only codebook summaries.

Deliver:

`QUESTION_INTERVAL_AUDIT.md`

Do not run interval regression until this exists.

Key decision:
- Is there a defensible numerical interval for category 1?
- Is the top bin bounded or open?
- Can categories 1+2 be merged into <10% without inventing a boundary?

Record the decision and its implications.

---

## 4. Reproduce canonical adult 3×3 data

Independently rebuild the adult cell table from canonical PR #16/#17 sources.

Deliver:
- `adult_cell_distribution.csv`
- `adult_share_yuan_table.csv`
- `CELL_REPRODUCTION_CHECK.md`

For each cell include:
- N;
- six counts and shares;
- ordinal mean;
- midpoint share;
- midpoint-implied yuan;
- Top75;
- above-bottom-category probability.

All manuscript numbers must come from this adult source.

---

## 5. Yuan-scale and affine analysis

Implement every authorized item in Section 4 of the spec.

Deliver at minimum:

- `incremental_yuan_response.csv`
- `endpoint_elasticity.csv`
- `affine_midpoint_parameters.csv`
- `affine_model_comparison.csv`
- `interval_affine_parameters.csv` if defensible
- `interval_affine_fit.csv` if defensible
- `AFFINE_RESPONSE_RESULT.md`

Bootstrap:
- adult sample;
- nine-cell stratified;
- fixed seed;
- at least 4,000 draws;
- preserve cell Ns.

### Mandatory estimates

For Cash, Food, Medical:
- 200→1,000 incremental midpoint-implied response;
- 1,000→5,000 incremental midpoint-implied response;
- endpoint elasticity 200→5,000;
- form-specific affine intercept;
- form-specific affine slope.

### Pairwise comparisons

For each amount interval:
- Cash−Food;
- Cash−Medical;
- Food−Medical.

Use a frozen six-test family for these pairwise interval comparisons.

### Model comparison

Compare:
1. common intercept/common slope;
2. form intercepts/common slope;
3. form intercepts/form slopes.

Report both fit and parameter uncertainty. Avoid “same slope” language unless the interval is actually informative.

### Interval regression

If questionnaire bounds are defensible, fit the interval-censored model and inspect predicted category probabilities in all nine cells.

If bounds are not defensible:
- do not force interval MLE;
- write a short technical memo explaining why;
- implement the closest valid ordered / merged-category sensitivity.

---

## 6. Multiplicity family 42

Extend the existing 21-test inference machinery without changing outcome definitions.

Create the 42-test family exactly as specified.

Deliver:
- `scientific_family42.csv`
- `family42_simultaneous_intervals.csv` if available
- `FAMILY42_RESULT.md`

Report:
- nominal;
- Holm42;
- joint min-P42 if validly implemented.

Highlight:
- Cash ordinal;
- Cash midpoint;
- Cash Top75;
- cross-form Top75 omnibus;
- Cash−Food;
- Cash−Medical.

Do not hide outcomes that lose adjustment significance.

---

## 7. Food bindingness reanalysis

First independently reproduce the historical +8.00 / +1.33 estimates and sign convention.

Deliver:
- `FOOD_BINDINGNESS_SIGN_AUDIT.md`

Then build raw subgroup tables:
- `food_bindingness_raw_cells.csv`

For both subgroup categories and each Cash/Food amount report:
- N;
- all six response shares;
- midpoint;
- ordinal;
- Top75;
- above-bottom category.

Run the bounded continuous / ratio reanalysis specified in the spec.

Deliver:
- `food_bindingness_continuous.csv`
- `food_bindingness_adjusted.csv`
- `food_bindingness_ratio.csv`
- `FOOD_BINDINGNESS_RESULT.md`

Primary outcome is Top75 because that is the historical focal result.

Secondary only:
- midpoint;
- ordinal.

Controls/moderation:
- income;
- household size.

No additional covariate search.

The final note must state whether the simple increasing-bindingness prediction is:
- supported;
- contradicted;
- or unresolved.

---

## 8. Mechanism precision audit

Using historical frozen estimates plus the bounded new Food analysis, create:

- `MECHANISM_PREDICTION_PRECISION_LEDGER.csv`
- `MECHANISM_PREDICTION_PRECISION_NOTE.md`

Compute 80% MDEs for the key moderator tests.

Where units permit, translate CIs into interpretable possible moderation ranges relative to the headline slope.

Do not report generic “percent explained” if the estimand is not commensurate.

The main-text conclusion should distinguish:
- sharp prediction contradicted;
- affirmative evidence;
- no affirmative evidence;
- insufficient precision.

---

## 9. Rewrite decomposition terminology

Update manuscript and supplement source language:

Replace:
- any spending;
- participation;
- extensive margin;
- positive spender

with measurement-faithful terms unless explicitly qualified.

Rename Table 3 / related decomposition:
- bottom-category component;
- conditional-above-bottom component.

Add the cross-amount threshold-comparability caveat.

Remove any claim that this decomposition establishes a Fuster-style extensive/intensive difference.

---

## 10. Methods completeness package

Build:

- `STUDY_METADATA_AUDIT.md`
- `sample_characteristics.csv`
- `randomization_balance.csv`
- `QUESTIONNAIRE_APPENDIX.md`
- `AUTHOR_INFORMATION_REQUIRED.md`

Search all project/repo files for metadata before declaring something missing.

If no record exists, ask the author rather than infer.

Q1/Q2:
- define exactly;
- call them response-style screens;
- put robustness in supplement;
- never call them attention checks without source evidence.

---

## 11. Literature verification

Perform current web verification of the priority literature and JEBO bibliographic details.

Deliver:
- `JEBO_V3_REFERENCE_AUDIT.csv`
- `LITERATURE_POSITION_REVISION.md`

Add / verify Shapiro–Slemrod.

Deepen discussion of:
- Fuster et al.;
- Andreolli–Surico;
- Crossley et al.;
- Bonomo et al.;
- Bernard;
- Parker–Souleles;
- Boehm et al.;
- Lee et al.;
- Pauls–Laudi.

Working papers must be labelled working papers.

---

## 12. Manuscript jebo_v3

Create:

`消费调查/manuscript/jebo_v3/`

Required:
- `JEBO_manuscript_v3.md`
- `JEBO_manuscript_v3.docx`
- `JEBO_supplement_v3.md`
- `JEBO_supplement_v3.docx`
- `RESPONSE_TO_JEBO_REVIEW.md`
- `JEBO_V3_CLAIM_LEDGER.csv`
- `JEBO_V3_REFERENCE_AUDIT.csv`
- `AUTHOR_INFORMATION_REQUIRED.md`
- figure package
- source-data CSVs

### Main narrative

Do not force the previous spendability story.

The new central question should be determined by the reviewer-driven results:

> Are the observed form differences mainly small-transfer level/intercept differences, differences in incremental spending response, or both?

If supported, emphasize:
- share decline versus near-proportional yuan growth;
- low-amount form differences;
- large-amount incremental-response convergence;
- uncertainty around true cross-form slope differences.

### Spendability

May appear only in Discussion as:
- a candidate interpretation;
- a future measurable construct.

Not title-level fact.

### Mechanisms

Use a **prediction and precision** structure, not a funnel claiming sequential exclusion.

---

## 13. Figures

Preferred main figures after results are known:

1. 3×3 response atlas.
2. Share versus amount + implied yuan versus amount.
3. Incremental midpoint-implied spending response by form and interval.
4. Food subgroup raw-cell figure with corrected prediction/sign.
5. Optional affine model fit / category calibration if it adds real information.

Remove the old mechanism-funnel figure if it implies excluded mechanisms.

All main figure source data must be adult aggregate data.

---

## 14. Response letter

The response letter must directly answer each reviewer point.

For the bindingness sign error:
- acknowledge the error without euphemism;
- give corrected prediction;
- show corrected result.

For the bottom-category/extensive-margin issue:
- acknowledge measurement overinterpretation;
- rename the estimand;
- revise Fuster comparison.

For spendability:
- state that it has been demoted from measured explanation to candidate interpretation.

For null moderators:
- report MDE/precision and stop using “rule out.”

For affine / marginal-response critique:
- present new results first, then explain how the manuscript’s core description changed.

---

## 15. Final audit

Before opening the PR, independently check:

- every sign in Food−Cash and Cash−Food statements;
- every form-specific incremental slope;
- every share-to-yuan calculation;
- every elasticity;
- all 42 adjusted p-values;
- all new table/figure numbers;
- all adult Ns;
- all questionnaire interval boundaries;
- no bottom-category variable is called actual “spending participation” without qualification;
- no unsupported ethics/recruitment fact is invented;
- no “pre-specified” language is unqualified;
- no “spendability is shown/proven” language remains;
- no null finding is described as equivalence.

Create:

`消费调查/results/jebo_review_revision/FINAL_AUDIT.md`

and a top-level:

`消费调查/results/jebo_review_revision/RESULT.md`

summarizing:
1. which reviewer criticisms were correct;
2. what the new affine / yuan-scale analysis found;
3. whether the paper’s core story changed;
4. which mechanism claims were withdrawn;
5. what metadata still require author input;
6. paths to final manuscript / supplement / response letter.

---

## 16. Pull request

Open a draft stacked PR:

- head: `feature/jebo-review-revision`
- base: `feature/jebo-repositioning`

Suggested title:

**JEBO reviewer revision: repair estimands, scale interpretation, and mechanism logic**

Do not merge automatically.
