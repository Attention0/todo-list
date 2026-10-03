# JEBO reviewer-driven revision specification — logic, estimands, and evidential repair

## 0. Scope and priority

This revision responds to the latest external-style JEBO review of the manuscript currently in PR #17 (`feature/jebo-repositioning`).

**Primary purpose:** repair substantive logic, estimand definition, measurement interpretation, and claims that are not supported by the existing design.

**Not the purpose:** make the prose artificially more conservative or more aggressive, rescue significance, invent new mechanisms, or continue exploratory mining.

The revision should treat the review as a set of testable scientific criticisms. Where the reviewer is correct, correct the manuscript plainly. Where a criticism depends on an invalid assumption or unavailable measurement, document that precisely rather than forcing an analysis.

The current PR #17 head is:

- branch: `feature/jebo-repositioning`
- head: `926b05022189661bdfe4dc41d24ad900c77bbd12`

Create a stacked reviewer-revision branch from that head. Do not merge PR #17 or any older PR.

---

## 1. Issues that must be treated as substantive, not stylistic

The following points are considered high-priority scientific issues:

1. **Share decline versus implied-yuan response.**  
   The manuscript currently emphasizes declining midpoint-coded spending shares. The reviewer correctly notes that implied additional yuan rises nearly proportionally with transfer size. The paper must distinguish:
   - average spending share (Y/T);
   - additional yuan (Y);
   - incremental spending response over each amount interval;
   - endpoint elasticity;
   - form-specific level/intercept versus slope differences.

2. **The fixed-yuan benchmark is too weak.**  
   A constant-yuan model is only a straw benchmark. The relevant parsimonious benchmark is an affine spending function:
   [
   Y^*_{if}=a_f+b_fT_i+arepsilon_i.
   ]
   Equivalently, on the share scale:
   [
   S^*_{if}=rac{a_f}{T_i}+b_f+arepsilon_i/T_i.
   ]
   This must be evaluated carefully, without treating it as a structural consumption model.

3. **“Spendability” is not measured.**  
   The questionnaire contains no direct measure of perceived spendability, mental-account assignment, intended allocation, planning horizon, saving intention, or self-control. “Spendability” must not be presented as an empirically identified construct or as the title-level finding unless new direct measurement exists (it does not). It can remain only as a candidate interpretation / future hypothesis.

4. **Food bindingness sign logic must be corrected.**  
   Under the simple increasing-bindingness story, if larger Food vouchers become more difficult to absorb, the Food spending-share or high-response slope should become **more negative relative to Cash** as bindingness rises. With the current sign convention (slope_{Food}-slope_{Cash}), the simple prediction is negative. The existing likely-binding subgroup estimate is positive, so the previous phrase “exactly in the direction predicted” is incorrect and must be withdrawn.

5. **The “participation/extensive margin” terminology is too strong.**  
   The lowest response category means “essentially no additional spending,” not an observed exact zero, and category 2 is “<10%.” Therefore categories 2–6 versus category 1 are not a clean (P(spend>0)) margin. Rename this object:
   - “above-bottom-category probability”;
   - “bottom-category margin”;
   - “conditional-above-bottom component.”
   The product decomposition remains a valid arithmetic decomposition of the coded outcome but is **not** an extensive/intensive causal decomposition.

6. **Null moderator results cannot be mechanism exclusions.**  
   Income, liquidity, need, Q1/Q2, and all-X non-rejections must not be used as evidence that those mechanisms are absent. The revision must report precision / MDE and distinguish:
   - contradiction of a sharp prediction;
   - absence of affirmative evidence;
   - inability to rule out economically meaningful moderation.

7. **Pre-specified / post hoc language must be internally consistent.**  
   The study was not preregistered. Some follow-up analyses were frozen before being run but only after earlier results from the same data had been observed. The manuscript must never use “pre-specified” or “confirmatory” without stating the stage relative to which it was fixed.

8. **Methods and study metadata must be complete.**  
   Recruitment platform, field dates, incentives, completion/response information if available, exact randomization procedure, sample characteristics, exact scenario/question wording, ethics/consent, data availability, funding, conflicts, CRediT contributions, and any journal-required AI disclosure must be audited and supplied where records exist. Missing author facts must be listed, not invented.

---

## 2. Core empirical reframing to test — do not assume it is true

The reviewer proposes that the data may be better summarized as:

> form differences are concentrated at small transfer amounts, while the incremental yuan response at larger amounts is more similar across forms.

This is a hypothesis to test, not a conclusion to hard-code.

Using current adult midpoint means, the rough descriptive quantities are:

### Cash
- RMB 200: share ~0.253, implied yuan ~50.6
- RMB 1,000: share ~0.227, implied yuan ~226.7
- RMB 5,000: share ~0.202, implied yuan ~1,008

Approximate incremental yuan response:
- 200→1,000: ~0.220
- 1,000→5,000: ~0.195

### Food
- ~0.193 and ~0.194

### Medical
- ~0.179 and ~0.179

These are midpoint-derived descriptive quantities. They require adult-sample bootstrap uncertainty and a coding-robust interval-censored analysis before they can become a manuscript result.

The revision should explicitly ask whether the data are better described by:
- form-specific intercepts with similar slopes;
- form-specific intercepts and slopes;
- piecewise incremental slopes;
- or no useful affine summary.

---

## 3. Exact questionnaire audit before interval regression

Before fitting any interval regression, Work must re-read the original questionnaire and document the exact response options for all three forms and all amounts.

Create:

`消费调查/results/jebo_review_revision/QUESTION_INTERVAL_AUDIT.md`

Record for every response category:
- original Chinese wording;
- English translation used in manuscript;
- whether the category has an exact numerical lower bound;
- whether it has an exact numerical upper bound;
- whether the top category is open-ended;
- whether the bottom category is an exact zero or only verbal “essentially no increase”;
- whether wording differs by form.

### Critical rule

Do **not** invent a numerical boundary between:
- “essentially no additional spending”; and
- “less than 10%”
if the questionnaire does not define one.

If the bottom category is not numerically bounded, the primary interval-censored sensitivity should merge the first two categories into a single **<10%** category if that is logically valid from the exact wording. The resulting intervals would then be:
- <10%;
- 10–25%;
- 25–50%;
- 50–75%;
- >75%.

For the top category, use right censoring if it is truly open-ended. Do not silently cap at 100% unless the questionnaire explicitly does so.

If even the merged five-category mapping is not defensible from the actual wording, state that the reviewer’s proposed interval regression cannot be implemented without imposing unsupported bounds. In that case, do not fake the analysis; rely on the ordered outcome and midpoint sensitivity, and explain the measurement limitation in the response letter.

---

## 4. New reviewer-driven analysis A — yuan-scale response and affine benchmark

This is the highest-priority new analysis.

Before running it, create and commit a frozen manifest:

`消费调查/results/jebo_review_revision/REVIEWER_REANALYSIS_MANIFEST.md`

State explicitly:
- the study is not preregistered;
- this analysis is reviewer-driven and fixed before execution after PR #17 results were already known;
- no additional specification search is allowed after seeing results.

### A1. Adult 3×3 cell table

For each adult randomized cell report:
- N;
- full six-bin distribution;
- ordinal mean;
- midpoint share;
- midpoint-implied yuan;
- pointwise bootstrap CI for midpoint share and implied yuan.

Use the existing adult cell counts as the canonical source and verify all values independently.

### A2. Incremental yuan response by interval

For each form calculate:

[
m^{low}_f = rac{E[Y|1000,f]-E[Y|200,f]}{800}
]

[
m^{high}_f = rac{E[Y|5000,f]-E[Y|1000,f]}{4000}
]

where (Y) is midpoint-implied additional yuan.

Use cell-stratified adult bootstrap with a fixed seed.

Report:
- estimate;
- 95% CI;
- Cash–Food, Cash–Medical, Food–Medical differences in each interval;
- a finite six-contrast Holm family (2 intervals × 3 pairwise form differences) or a clearly justified equivalent finite family.

Do not call these structural MPCs. Call them **incremental midpoint-implied spending responses**.

### A3. Endpoint elasticity

For each form estimate:

[
eta_f =
rac{log(E[Y|5000,f]/E[Y|200,f])}{log(25)}.
]

Use adult-sample cell-stratified bootstrap.

Report:
- form-specific estimates and CIs;
- pairwise differences and CIs;
- no “equal” claim based on overlapping CIs.

The old PR #10 full-sample endpoint elasticities can be used as a reproducibility check, not substituted for adult estimates.

### A4. Midpoint affine companion model

Fit the transparent descriptive midpoint model:

[
Y_i = a_f+b_fT_i+arepsilon_i
]

using adult respondents and midpoint-implied yuan.

Use heteroskedasticity-robust inference and a cell-stratified bootstrap.

Estimate:
- (a_f), (b_f) by form;
- pairwise intercept differences;
- pairwise slope differences;
- predicted cell means;
- fit errors.

Compare nested descriptive models:
1. common intercept + common slope;
2. form-specific intercepts + common slope;
3. form-specific intercepts + form-specific slopes.

Use appropriate Wald / bootstrap comparisons. Do not rely on three aggregated means alone for standard errors.

### A5. Interval-censored affine analysis

If and only if the questionnaire audit supports defensible intervals, estimate a latent yuan-spending model:

[
Y_i^* = a_f+b_fT_i+arepsilon_i
]

from the original response intervals in yuan.

Because interval widths scale with transfer size, the homoskedastic normal interval-regression assumption may be strong. Therefore:

- primary: interval-censored MLE with transparent assumptions;
- sensitivity: allow scale to vary with amount, or fit an equivalent share-scale interval model if technically defensible;
- uncertainty: respondent bootstrap stratified by the nine randomized cells.

Report:
- (a_f,b_f);
- common-slope versus form-specific-slope test;
- predicted probabilities for each observed category/cell;
- goodness-of-fit / calibration at all nine cells;
- whether the affine model materially misses any cell/distribution.

Do not present the affine model as structural. It is a parsimonious description of the response pattern.

### A6. Story decision from analysis A

Create:

`AFFINE_RESPONSE_RESULT.md`

It must answer:

1. Is the Cash share decline economically large once expressed as yuan elasticity?
2. Are incremental midpoint-implied responses similar across forms at 1,000→5,000?
3. Are form differences better characterized as intercept/level differences than slope differences?
4. Does interval-censored estimation support the midpoint-derived conclusion?
5. Does a common-slope model fit adequately?
6. What cannot be inferred because of the response bins?

Do not force the reviewer’s interpretation if the data reject it.

---

## 5. New reviewer-driven analysis B — multiplicity family including within-form trends

The current 21-test family includes seven outcomes × three interaction tests.

The reviewer asks why headline within-form trends are outside the correction family.

Create a **42-test reviewer sensitivity family**:

For each of seven existing outcome representations include:
- Cash within-form trend;
- Food within-form trend;
- Medical within-form trend;
- form×amount omnibus;
- Cash–Food trend difference;
- Cash–Medical trend difference.

Total = 7 × 6 = 42 tests.

Use:
- Holm correction across all 42;
- joint min-P across all 42 if the existing influence-function / resampling machinery can be validly extended without changing estimands.

Preserve the original 21-test family as historical analysis in the supplement.

Create:
- `scientific_family42.csv`
- `FAMILY42_RESULT.md`

The manuscript should use the 42-test sensitivity when discussing the robustness of the headline Cash trend.

Important:
- do not redefine outcomes;
- do not shrink the family after seeing results;
- do not add new thresholds.

---

## 6. New reviewer-driven analysis C — Food bindingness sign correction and bounded reanalysis

### C1. Prediction must be written before results

Write the sharp simple-mechanical prediction explicitly:

If increasing voucher size makes the Food restriction increasingly binding and thereby suppresses additional total spending, then in the group more likely to bind:

[
slope_{Food}-slope_{Cash}<0
]

for a spending-share / high-response outcome.

The current historical estimate in the likely-binding group is positive. Therefore the earlier statement “exactly in the direction predicted” is wrong.

### C2. Define the historical outcome and sign convention

Document exactly:
- which outcome produced +8.00 pp and +1.33 pp;
- whether the slope is per fivefold amount increase;
- whether the estimand is Food−Cash or Cash−Food;
- sample N;
- subgroup definition.

No manuscript text may discuss this result until the sign is independently reproduced.

### C3. Raw subgroup cells

For Cash and Food separately, and for both subgroup definitions, report all six randomized cells:
- N;
- all original response-bin shares;
- ordinal mean;
- midpoint mean;
- top75 probability;
- above-bottom probability.

Create a figure or table that makes the subgroup pattern inspectable without regression.

### C4. Continuous baseline-food-spending reanalysis

Use the pre-treatment food-expenditure variable as a continuous / ordered quantity.

Primary reviewer-driven model:
- adult Cash + Food sample;
- primary outcome: Top75, because that is the outcome behind the historical bindingness contrast;
- model includes form, amount trend, food-spending measure, and all lower-order terms plus the form×amount×food-spending interaction;
- include income and family-size moderation terms needed to prevent their known correlation with food spending from mechanically loading onto the focal interaction.

Report:
- focal three-way estimate and CI;
- income/family-size adjusted version;
- no causal language because food spending is observational.

Secondary outcomes:
- midpoint;
- ordinal.

Do not expand beyond these three.

### C5. Ratio representation

Where food-spending bands have valid positive monetary mappings, evaluate a continuous transfer-to-six-month-food-spending ratio.

Use the existing M1/M2/rank sensitivity logic where appropriate. Do not invent exact spending inside bands.

Compare:
- ratio-only restriction;
- unrestricted amount + food-spending terms.

### C6. Conclusion

The default interpretation, unless new evidence changes it, should be:

> baseline food spending moderates the observed Food–Cash gradient in the data, but the direction is inconsistent with the simplest prediction that increasing mechanical bindingness should make the Food slope more negative than the Cash slope. Because the moderator is observational and coarse, the source of this heterogeneity remains unresolved.

Do not call this “positive evidence for restrictions” unless a clearly specified prediction is actually supported.

---

## 7. Measurement repair — bottom category and decomposition

Rename all occurrences of:
- “any spending”;
- “participation”;
- “extensive margin”;
- “positive spender”;

unless the text explicitly says these are shorthand for a coded category.

Preferred language:
- “above-bottom-category response”;
- “probability of selecting a category above ‘essentially no additional spending’”;
- “bottom-category component”;
- “conditional-above-bottom component.”

The decomposition remains:

[
E[MPC_{coded}]
=
P(Y>bottom)
	imes E[MPC_{coded}|Y>bottom]
]

but this is only an arithmetic identity under the coding.

Add a measurement note:

> Because the first category is verbal and the remaining categories are shares of the assigned transfer, the above-bottom indicator is not a common yuan threshold across amounts. It should not be interpreted as a directly comparable extensive margin of actual spending.

Remove or substantially revise the comparison with Fuster et al. that treats the two extensive margins as the same object.

---

## 8. Mechanism evidence must become a prediction-and-precision table

Create:

`MECHANISM_PREDICTION_PRECISION_LEDGER.csv`

and:

`MECHANISM_PREDICTION_PRECISION_NOTE.md`

For each mechanism / alternative explanation include:

- mechanism;
- sharp prediction if one exists;
- outcome;
- estimand;
- sign prediction;
- point estimate;
- 95% CI;
- family-adjusted p where relevant;
- 80% MDE at two-sided alpha=.05;
- conservative family-adjusted MDE where meaningful;
- whether the data:
  - contradict a sharp prediction;
  - provide affirmative support;
  - are inconclusive;
  - cannot test the mechanism.

At minimum include:
- fixed-yuan arithmetic (measurement benchmark, not serious mechanism);
- affine yuan response;
- relative income;
- emergency liquidity;
- baseline category need;
- simple Food bindingness;
- observable-composition moderation;
- Q1/Q2 response-style screens.

### Explainable-share bounds

Where the units are directly comparable, translate the CI into a bound on how much of the relevant observed slope / slope difference could be explained.

Example:
- if a standardized moderator interaction changes the Cash slope by (g) per SD, translate the 10th-to-90th percentile span into an implied slope change and compare it with the headline Cash slope;
- if units are not comparable, explicitly mark “not interpretable as an explained-share bound.”

Do not manufacture a common “percent explained” across unrelated moderators.

### Main-text rule

All-X and broad observable screens belong in the supplement. The main text may say only:

> We did not identify a stable observable moderator signature at the available precision.

It must immediately add that economically meaningful moderation remains compatible with the intervals.

---

## 9. Study methods and metadata audit

Create:

`STUDY_METADATA_AUDIT.md`

Search the repository/project source material for:

- survey platform;
- recruitment channel;
- field dates;
- invitations / starts / completes if available;
- incentive / compensation;
- inclusion/exclusion rules;
- randomization code or platform randomization description;
- stopping rule, if any;
- ethics approval / exemption;
- informed consent wording;
- privacy/data handling;
- funding;
- conflict of interest;
- author contributions;
- data sharing permissions;
- code sharing;
- AI-assisted writing disclosure if required by current Elsevier/JEBO policy.

### Do not fabricate missing facts

If a fact cannot be verified, add it to:

`消费调查/manuscript/jebo_v3/AUTHOR_INFORMATION_REQUIRED.md`

with a concrete question for the authors.

### Sample table

Create a proper adult-sample descriptive table containing at least:
- age;
- sex/gender if recorded;
- education;
- income measure;
- household size;
- employment if recorded;
- geographic coverage if defensible.

Report missingness.

### Randomization balance

Reproduce a clean balance table across the nine randomized cells or across form/amount factors using pre-treatment variables.

Do not claim randomization “worked” solely because no adjusted imbalance is significant.

### Response-quality screens

Move clean/Q1/Q2 definitions and results into the supplement with exact definitions.

Do **not** call Q1/Q2 “attention checks” unless they were literally designed and administered as attention checks. They are response-style screens.

### Questionnaire appendix

Include:
- exact Chinese scenario text for all nine arms;
- exact response options;
- English translation;
- form-specific wording differences.

---

## 10. Analysis-timing language audit

Create a script or manual audit for all occurrences of:

- pre-specified;
- prespecified;
- preregistered;
- confirmatory;
- ex ante;
- planned;
- frozen;
- pre-existing;
- preceding audit.

Manuscript rule:

> The study was not preregistered. Some follow-up analyses were specified before execution but after prior results from the same dataset were observed.

Reviewer-driven analyses in this revision should be described as:

> specified in a reviewer-response analysis plan before the new calculations were run.

Do not mention PR numbers, Git workflow, “Work,” or internal audit stages in the scientific manuscript.

---

## 11. Literature and reference repair

Verify current publication status and bibliographic details using primary sources / Crossref / publisher pages.

The revised literature section must directly engage, not merely cite:

- Shapiro & Slemrod survey-MPC work;
- Fuster, Kaplan & Zafar (2021);
- Andreolli & Surico (2026);
- Crossley et al. (2026 or current status);
- Bernard (2023 working paper);
- Boehm, Fize & Jaravel (2025);
- Bonomo, Ruffini & Schanzenbach (current publication status);
- Parker & Souleles (2019);
- Lee et al. (JEBO 2024);
- Pauls & Laudi (JEBO 2025).

Specific checks:
- verify JEBO volume/page/article numbers for Lee and Pauls–Laudi;
- verify whether Crossley/Bonomo remain working papers at access date;
- verify how Parker–Souleles characterize correspondence and disagreement between reported and revealed-preference estimates;
- do not cite Parker–Souleles as generic validation without the qualifying result.

Create:

`JEBO_V3_REFERENCE_AUDIT.csv`

---

## 12. Manuscript reframing rules

Create a new directory:

`消费调查/manuscript/jebo_v3/`

Do not overwrite jebo_v1 or any local v2 file.

### Title

Do not use “Spendability” as an established construct in the title.

Work should propose 3–5 titles based on actual new results. Candidate directions:

- **Transfer size and stated spending across cash and earmarked resources**
- **Small-transfer differences and marginal spending responses across transfer forms**
- **How stated spending scales with transfer size across cash and earmarked resources**

Choose only after the affine / interval results are known.

### Abstract

Must include:
- randomized 3×3 design;
- adult N;
- share and implied-yuan distinction;
- main incremental/affine result if supported;
- interaction uncertainty;
- no claim of identified spendability mechanism.

Check the current official JEBO/Elsevier abstract requirement and comply with it.

### Introduction logic

Recommended sequence if supported by new analysis:

1. Finite-transfer spending shares can vary with transfer size.
2. The same data can look different on a share versus yuan scale.
3. The key empirical question is whether transfer forms differ mainly in:
   - small-transfer level/intercept;
   - incremental spending response;
   - both.
4. 3×3 randomized design.
5. Raw shares + implied-yuan responses.
6. Affine / piecewise incremental result.
7. Distributional description in original bins.
8. Cross-form interaction uncertainty.
9. Mechanism diagnostics as limited tests, not eliminations.
10. Contribution relative to Bernard, Fuster, Bonomo, Crossley, JEBO framing papers.

### Results order

Suggested:

1. 3×3 raw distributions and midpoint shares.
2. Share-to-yuan translation.
3. Incremental response / affine model.
4. Cross-form comparison and multiplicity family 42.
5. Distributional anatomy without extensive-margin terminology.
6. Food baseline-expenditure heterogeneity with corrected sign logic.
7. Other mechanism diagnostics with MDE/precision.
8. Robustness / response-style / population coverage in supplement.

### Discussion

“Spendability,” mental accounting, resource categorization, planning horizon, and salience may appear only as candidate mechanisms.

The Discussion should distinguish:
- what the data directly show;
- what is contradicted;
- what remains possible;
- what future experimental manipulation would identify.

---

## 13. Figures and tables

Main text should be visually economical.

Potential main items:

### Figure 1
Full 3×3 response atlas from adult sample.

### Figure 2
Two-panel scale view:
- Panel A: midpoint share versus transfer amount;
- Panel B: midpoint-implied yuan versus transfer amount, with affine fitted lines if justified.

This figure should make the reviewer’s central scale critique visually transparent.

### Figure 3
Incremental midpoint-implied spending responses:
- low interval 200→1,000;
- high interval 1,000→5,000;
- by form with bootstrap CIs.

### Figure 4
Corrected Food baseline-expenditure heterogeneity:
- raw Cash/Food cell outcomes by amount and subgroup;
- clearly label outcome (Top75 if primary);
- show N.

Do not use a “mechanism funnel” figure if it visually implies mechanisms have been ruled out.

### Main tables

1. Adult sample / randomized cell counts and treatment definitions.
2. Share, implied yuan, elasticity, incremental responses.
3. Affine / interval-censored model parameters.
4. 42-family key trend and interaction results.
5. Optional mechanism prediction/precision summary if compact.

Move broad screens to supplement.

---

## 14. Reviewer response letter

Create:

`消费调查/manuscript/jebo_v3/RESPONSE_TO_JEBO_REVIEW.md`

Respond point-by-point to the supplied review.

Tone:
- factual;
- non-defensive;
- explicit when the reviewer identified a real error.

For issue 4, state plainly that the previous bindingness interpretation had the sign logic wrong and has been corrected.

For issue 5, acknowledge that “participation/extensive margin” overstated what the bottom response category measures.

For issue 1, show the new yuan-scale / incremental / affine analysis.

For issue 3, replace “rule out” claims with precision/MDE statements.

For issue 7, state exactly how timing language has been standardized.

If any requested analysis cannot be validly implemented because the questionnaire does not define required interval boundaries, explain that limitation with the exact wording and provide the closest defensible analysis.

---

## 15. Stop rules

This revision authorizes only analyses directly motivated by the review:

- adult yuan-scale bootstrap;
- incremental responses;
- endpoint elasticity;
- affine midpoint model;
- interval-censored affine sensitivity if questionnaire boundaries permit;
- 42-test correction family;
- bounded Food bindingness reanalysis;
- MDE / precision summaries for already-existing mechanism tests;
- sample/balance/method metadata tables.

Do **not** run:
- new all-X screens;
- new thresholds;
- new subgroup mining;
- HTE / forest / SHAP;
- new latent classes;
- new psychological scales;
- outcome-driven sample rules;
- new mechanism variables not already in the questionnaire;
- alternative correction families after seeing results;
- specification searches intended to rescue a preferred story.

If the new affine / interval analysis weakens the current paper story, report that and rewrite accordingly.

---

## 16. Acceptance criteria

The revision is complete only if all of the following are true:

- no manuscript sentence treats spendability as measured;
- no null moderator is described as ruling out a mechanism;
- Food bindingness sign logic is correct everywhere;
- “any spending/extensive margin” has been replaced or explicitly qualified;
- adult-sample yuan and share quantities reconcile exactly;
- new incremental and elasticity estimates have bootstrap uncertainty;
- interval regression is used only if response boundaries are defensible;
- 42-test family is frozen and fully reported;
- pre/post analysis timing language is consistent;
- exact questionnaire text is available in supplement;
- sample characteristics and randomization balance are reported;
- missing ethics/recruitment facts are surfaced rather than invented;
- references and publication statuses are verified;
- manuscript, supplement, figures, tables, response letter, and claim ledger all use the same numbers and sign conventions.

The revision should improve **scientific coherence**, not merely rhetorical caution.
