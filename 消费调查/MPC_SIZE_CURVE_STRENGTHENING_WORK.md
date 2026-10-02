# MPC size-curve final evidence-strengthening workplan

## 0. Purpose and stopping rule

This is the final empirical pass for the current consumer-survey dataset.

It is NOT a new story-discovery round. Do not reopen unrestricted HTE, SHAP, latent-trait, psychological-moderator, subgroup, clustering, or machine-learning searches.

The goal is to stress-test and sharpen the single candidate story emerging from PR #9:

> Transfer form changes how stated MPC responds to transfer size. Cash shows a declining MPC-size gradient, driven mainly by compression of the highest-MPC tail; restricted resources show substantially weaker upper-tail compression.

PR #9 judged the Medical-vs-Cash average size-curve result suggestive rather than definitive. This final pass asks whether the evidence becomes materially clearer when we:
1. test a broader, theory-coherent Restricted-resources vs Cash contrast;
2. test whether the upper-tail result survives transformations that account for different baseline probabilities / headroom;
3. formally test whether the differential is concentrated in the upper tail;
4. summarize specification stability without cherry-picking;
5. distinguish falling MPC shares from rising absolute stated spending.

STOPPING RULE: after completing the prespecified analyses below, do not add new moderators, do not search for a replacement story, do not modify the manuscript, and write a final evidence judgment.

## 1. Inputs and identification limits

Use the original survey data already audited in PR #3, the one-observation-per-person identification constraint established in PR #8, and PR #9 branch feature/mpc-size-curve as the immediate empirical baseline.

Preserve all existing sample and coding conventions:
- R / A / C / Q1 / Q2 sample definitions;
- ordinal primary outcome;
- midpoint and alternative-top codings;
- z = (-1, 0, 1) amount trend;
- fixed objective+needs precision controls;
- existing response-quality definitions.

Do not reinterpret the outcome as realized MPC.

Each respondent observes only one form x amount cell. No within-person curve, individual remapping, individual slope, or stable trait is identified.

# PART I. GENERALIZE THE CORE RESULT: RESTRICTED RESOURCES VS CASH

## 2. Why this is the highest-value remaining test

PR #9 shows approximately:
- Cash top-category slope: -0.0405 per fivefold increase in amount.
- Food-vs-Cash top-category differential slope: +0.0282.
- Medical-vs-Cash top-category differential slope: +0.0309.

The Food and Medical top-tail differential slopes are strikingly similar even though their level effects differ.

This motivates a cleaner general hypothesis:

> The unusually large high-MPC response to small transfers is especially characteristic of unrestricted Cash; both restricted forms attenuate the amount-related compression of the high-MPC tail.

This potentially provides a more general and more powerful empirical statement than a Medical-only story.

## 3. Prespecified equal-weight Restricted-vs-Cash contrast

Define the restricted-resource estimand as the equal-weight average of Food and Medical:

Restricted = 0.5 x Food + 0.5 x Medical.

Use equal form weights, not sample-size weights, because the estimand should be the average of the two randomized restricted-form potential-outcome means.

For each outcome estimate:
1. Cash amount slope.
2. Food amount slope.
3. Medical amount slope.
4. Equal-weight Restricted amount slope.
5. Restricted-vs-Cash differential slope.
6. Food-vs-Medical slope difference.

Report estimate, robust SE, 95% CI, raw p-value, and a clearly defined multiplicity correction within the small prespecified family.

Do this for:
- ordinal score;
- midpoint;
- alternative-top midpoint;
- any additional spending;
- MPC >=10%;
- MPC >=25%;
- MPC >=50%;
- top category / >75%.

INTERPRETATION RULE: a pooled restricted-resources statement is defensible only if Food and Medical differential slopes are directionally similar, Food-vs-Medical slope heterogeneity is not large enough to contradict pooling, and the pooled result is not entirely driven by Medical.

If Food and Medical differ materially, report them separately and kill the pooled story.

# PART II. DOES THE TOP-TAIL RESULT SURVIVE HEADROOM / BASELINE-PROBABILITY CONCERNS?

## 4. Motivation

At RMB 200, Cash starts with a larger >75% response share than Food or Medical.

A reviewer can reasonably argue that Cash has more room to fall mechanically, so the larger probability decline may partly reflect different starting probabilities.

The probability-scale reduced-form difference is still valid, but the paper should show whether the result survives alternative link and relative-change scales.

## 5. Binary nonlinear models for each threshold

For each cumulative outcome:
- any spending;
- >=10%;
- >=25%;
- >=50%;
- >75%;

fit:

A. Logit:
logit(P(Y=1)) = form + z + form x z

B. Probit:
same structure.

For both models report:
- form-specific amount effects on the link scale;
- Food-vs-Cash;
- Medical-vs-Cash;
- equal-weight Restricted-vs-Cash;
- average marginal probability effects by form and differential marginal effects.

Do not interpret a nonlinear interaction coefficient as a probability-scale difference-in-differences without computing marginal contrasts.

Use bootstrap or delta-method inference and document the method.

KEY QUESTION:
Does Cash still show materially stronger top-tail compression than restricted forms after accounting for different baseline probabilities through nonlinear links?

## 6. Relative-change robustness for the top category

For the >75% category, report the 200-to-5000 change on:

1. probability difference;
2. risk ratio P5000 / P200;
3. odds ratio odds5000 / odds200;
4. ratio-of-risk-ratios and ratio-of-odds-ratios for:
   - Food vs Cash;
   - Medical vs Cash;
   - equal-weight Restricted vs Cash where mathematically well-defined.

Use stratified bootstrap over respondents / randomized cells.

This is a robustness exercise, not a search over scales.

If the result exists only in percentage points but vanishes on both relative scales, state that clearly.

# PART III. FORMALLY TEST UPPER-TAIL COMPRESSION

## 7. Joint threshold-vector bootstrap

PR #9 showed little differential at any-spending, increasingly larger point estimates at higher thresholds, and strongest evidence at >75%.

Do not infer tail-specificity merely because one p-value is smallest.

Use a stratified respondent bootstrap preserving the 3 x 3 structure.

For each bootstrap draw estimate the equal-weight Restricted-vs-Cash differential amount slope for the five cumulative thresholds:

d_any, d_10, d_25, d_50, d_75.

This yields their joint covariance.

Test these prespecified contrasts:
1. d_75 - d_any
2. d_75 - d_10
3. d_75 - d_25
4. d_75 - d_50

Apply Holm correction across these four contrasts.

Repeat Food-vs-Cash and Medical-vs-Cash as secondary analyses.

INTERPRETATION:
The statement "the form-by-size difference is concentrated in the high-MPC tail" is supported only if the upper-tail differential is demonstrably larger than at least the low / extensive margins.

If these direct cross-threshold differences are imprecise, write "most visible in the upper tail" rather than "tail-specific."

## 8. Optional global threshold-profile test

If straightforward to implement without fragile dependencies, construct one global Wald/bootstrap test:

H0: d_any = d_10 = d_25 = d_50 = d_75.

This is supportive, not primary.

Do not add a complex semiparametric distributional model merely to obtain a smaller p-value.

# PART IV. FULL DISTRIBUTION CHECK WITHOUT OVERMODELING

## 9. Multinomial category-probability robustness

Fit one transparent multinomial logit for the six outcome categories with:
- form;
- z;
- form x z.

Derive predicted category probabilities at z = -1, 0, 1 for Cash, Food, Medical.

Do not headline raw multinomial coefficients.

Use this only to check whether the parametric model reproduces the raw PR #9 pattern:
- Cash: large decline in category 6;
- redistribution toward middle categories;
- little change in category 1;
- Medical: offsetting category shifts.

If the multinomial model contradicts raw nonparametric cell shares, trust the cell shares and document model misfit.

# PART V. SPECIFICATION STABILITY / FINITE MULTIVERSE

## 10. Predefine the finite grid

Do not search beyond this grid.

Sample:
- R
- A
- C
- Q1
- Q2

Adjustment:
- unadjusted
- fixed objective+needs controls

Amount representation:
- z = (-1,0,1)
- unrestricted amount indicators summarized by the full 200-to-5000 contrast

Outcome representation:
- ordinal linear score
- midpoint
- alternative-top midpoint
- ordered logit
- ordered probit
- top-category probability
- top-category logit marginal effect

Contrast:
- Medical-vs-Cash
- Food-vs-Cash
- equal-weight Restricted-vs-Cash

Focus the stability summary on the differential size effect.

## 11. Stability outputs

Create a specification-curve table with:
- estimate;
- scale;
- sign;
- CI;
- raw p-value;
- sample;
- coding;
- adjustment;
- outcome family.

Do not pool coefficients that live on incomparable latent scales.

For comparable probability / cardinal-like effects report:
- share of specifications with the predicted positive Restricted-vs-Cash differential;
- median and range of standardized comparable effects;
- how often CIs exclude zero.

For ordered latent-index models report sign and CI consistency separately.

This is descriptive robustness evidence. Do not treat "percentage significant" as a new hypothesis test.

Include unfavorable Q1 and Q2 results. Do not hide them.

# PART VI. MPC SHARE VS ABSOLUTE STATED SPENDING

## 12. Motivation

A lower MPC share at a larger transfer can coexist with much larger absolute stated spending.

The paper should make this visually obvious because otherwise "declining MPC" can be misread as "declining consumption."

## 13. Implied additional-yuan translation

Using the midpoint mapping only as an auxiliary descriptive translation:

ImpliedAdditionalYuan = midpoint MPC x transfer amount.

For all nine cells report:
- mean midpoint MPC;
- implied additional yuan;
- bootstrap CI.

Do not call this realized spending.

Then compute 200-to-5000 scaling:

eta = log(E[DeltaC]_5000 / E[DeltaC]_200) / log(5000/200)

for Cash, Food, Medical, with bootstrap uncertainty.

Interpretation:
- eta = 1: proportional absolute spending response / constant MPC;
- eta < 1: sub-proportional response / declining MPC;
- eta > 1: super-proportional response.

Compare:
- Cash vs Food;
- Cash vs Medical;
- Cash vs equal-weight Restricted.

This is algebraically related to the MPC-size pattern. Present it as an intuitive re-expression, not independent confirmation.

## 14. Constant-dollar-response benchmark

As a descriptive falsification benchmark, ask whether each form's three midpoint cell means are remotely consistent with:

MPC(T) = K / T,

where K is chosen to best fit the three form-specific means.

Report fit error only.

Purpose:
- check whether Cash's declining MPC can be reduced to "respondents plan a fixed yuan amount regardless of transfer size";
- if clearly inconsistent, show that absolute stated spending rises strongly with amount even though the share falls.

Do not promote this into a structural model.

# PART VII. CHECK WHETHER FOOD + MEDICAL REALLY SUPPORT A RESTRICTION STORY

## 15. Equal-weight pooled restricted curve

Produce one simple figure with:
- Cash;
- Food;
- Medical;
- equal-weight Restricted average;

for:
1. midpoint MPC;
2. >75% response probability.

The Restricted line is a derived randomized contrast, not a fourth treatment arm.

Report pooled slope and pooled differential with uncertainty.

## 16. Restricted-form heterogeneity

Formally test Food slope = Medical slope for:
- ordinal;
- midpoint;
- >75% probability;
- top-category logit marginal effect.

This is not an equivalence test.

The question is whether a pooled restricted-resource description is scientifically reasonable.

If Food and Medical differ materially on average-MPC slope but are similar on top-tail compression, the paper may make a distribution-specific pooled claim rather than a pooled average-MPC claim.

That distinction must be explicit.

# PART VIII. WHAT NOT TO DO

## 17. No further mechanism mining

Do not add:
- new psychological scales;
- more demographic interactions;
- SHAP;
- causal forest;
- policy learning;
- latent factors;
- new types;
- new clustering;
- new trait constructs;
- subgroup significance scans.

PR #9 already showed Food inframarginality and Medical need matching are limited secondary layers. Do not try to rescue them.

## 18. No significance-driven model selection

Do not:
- switch primary outcome based on the smallest p-value;
- drop Q2 because it is unfavorable;
- select only adjusted models;
- redefine amount trend after seeing results;
- expand or shrink multiple-testing families after seeing results;
- call non-significance equivalence.

R / unadjusted / ordinal remains the primary reference result.

# PART IX. REQUIRED OUTPUTS

Create directory:

消费调查/results/mpc_final_strengthening/

with no respondent-level exports.

At minimum include:
1. restricted_vs_cash_slopes.csv
2. threshold_logit_probit.csv
3. top_tail_relative_change.csv
4. threshold_tail_specificity.csv
5. multinomial_probability_checks.csv
6. specification_curve.csv
7. implied_yuan_scaling.csv
8. constant_dollar_benchmark.csv
9. restricted_form_heterogeneity.csv
10. source-data CSVs for every new figure
11. analysis script(s)
12. reproducibility / audit note

## 19. Required figures

Figure A — pooled Restricted vs Cash amount curves
- Panel 1: midpoint MPC
- Panel 2: >75% response probability
Show Food and Medical separately/lightly so pooling is transparent.

Figure B — threshold-profile differential
Plot equal-weight Restricted-vs-Cash differential amount slope across:
- any
- >=10
- >=25
- >=50
- >75
with joint-bootstrap CIs.

Figure C — top-tail relative-scale robustness
Show probability, risk-ratio, and odds-ratio versions of the 200-to-5000 top-tail change.

Figure D — specification curve
Comparable differential effects only; annotate R/A/C/Q1/Q2 and adjusted/unadjusted.

Figure E — MPC share vs implied additional yuan
Make clear that declining MPC does not imply falling absolute stated spending.

# PART X. FINAL WRITTEN JUDGMENT

Create:

消费调查/MPC_FINAL_STRENGTHENING_RESULTS.md

with exactly these sections:

## 1. Bottom-line judgment
Choose exactly one:
- strong enough to organize the current paper;
- plausible main story but must be written as suggestive;
- not strong enough; revert to a more descriptive economics paper.

## 2. Restricted vs Cash
Does pooling Food and Medical reveal a coherent general pattern?

## 3. Is the effect genuinely upper-tail concentrated?
Use direct cross-threshold tests, not significance comparisons.

## 4. Does baseline headroom explain the result?
Use logit/probit and relative-scale robustness.

## 5. Specification stability
Include unfavorable Q1/Q2 results.

## 6. MPC share versus absolute stated spending
Clarify economic meaning.

## 7. What is supported
List only claims surviving this pass.

## 8. What is not supported
Explicitly state claims that should not appear in the main text.

## 9. Recommended paper architecture
Without editing the manuscript, state which 3-4 empirical results should form the main Results sequence.

## 10. Final stop decision
State whether any further analysis of the current dataset is scientifically necessary.

Default expectation: no further exploratory analysis after this pass.

# PART XI. DECISION STANDARD

The strongest possible current-data story would be:

> Small cash transfers generate a disproportionately large high-MPC response. As transfer size rises, this upper tail compresses sharply, producing the familiar decline in MPC. Two different restricted resource forms show substantially weaker upper-tail compression, implying that transfer design changes not only the level of stated MPC but the way consumption responses scale with transfer size.

Endorse this statement only if:

1. equal-weight Restricted-vs-Cash top-tail differential is precise;
2. it survives logit/probit and relative-scale checks;
3. direct cross-threshold tests show the effect is materially larger in the upper tail than at the extensive margin;
4. Food and Medical are sufficiently aligned for a distribution-specific pooled statement;
5. specification stability is acceptable and Q2 sensitivity is transparently reported;
6. the claim does not depend on one midpoint coding.

If these fail, the final report should say so clearly and stop searching.
