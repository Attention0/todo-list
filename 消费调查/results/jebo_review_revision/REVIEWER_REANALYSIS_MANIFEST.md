# Reviewer-response analysis plan

Base: PR17 `926b05022189661bdfe4dc41d24ad900c77bbd12`. Branch:
`feature/jebo-review-revision`. Fixed before the calculations below. The study
was not preregistered. This reviewer-driven plan is fixed after earlier results
from the same dataset, including PR17, were observed. It provides no retroactive
confirmatory status. No specification search follows the results.

## Inputs, samples and protection

Canonical adult sample A: recorded age 18–100, N=5,480. Forms Cash/Food/Medical;
amounts 200/1,000/5,000. Six original responses, ordinal scores 1–6, midpoint
scores 0/.05/.175/.375/.625/.875, and seven existing representations remain fixed.
Raw SHA256: 16996c88fdd20f5084b62a8503a8eec1d4c6ec7caff489eff109500f629694fe.
Read the original integrated Chinese questionnaire and authorized Stata file;
export only aggregate data, public questionnaire text and fit summaries. Historical
PR9–17 files and local v2 manuscripts remain read-only; record their hashes.

## A. Yuan scale and affine description

4,000 independent categorical-record bootstrap draws in the nine fixed-size adult
cells, seed 2026100417, NumPy default_rng, fixed Cash/Food/Medical then ascending
amount order. The multinomial implementation is exactly equivalent to respondent
resampling for models depending only on randomized cell and response category.

Report nine-cell counts/shares, ordinal means, midpoint shares and implied yuan,
with percentile intervals. Incremental responses are differences in midpoint-implied
yuan divided by 800 or 4,000. Report six pairwise contrasts, normal HC3 p values
and Holm6, plus bootstrap percentile intervals. Endpoint log elasticities and three
pairwise differences have percentile intervals, no additional significance family.

Fit midpoint-implied yuan on form intercepts and T/1,000 slopes. Fit common intercept/
common slope, form intercepts/common slope, and form intercepts/form slopes. Use
individual-observation-equivalent HC3 and cell-stratified bootstrap. Report parameters,
pairwise differences, predicted cell means, residuals, RMSE and saturated-cell
lack-of-fit Wald diagnostics. Three nested robust Wald comparisons (intercepts,
slopes, both) use Holm3; bootstrap confidence intervals describe parameter uncertainty.
An intercept extrapolates to zero transfer outside the observed design and is not a
causal effect of a zero transfer or a mechanism.

### Interval audit gate

Publish QUESTION_INTERVAL_AUDIT.md before any interval fit. Do not assign a numeric
cutoff to category 1. If wording permits, merge categories 1+2 as below 10%; retain
10–25, 25–50, 50–75, and right-censored above 75%. Verbal top bounds and parenthetical
75–100% examples must be disclosed; no unannounced 100% cap. Below 10% is left-censored
at .10T, with no invented exact zero threshold. This is a latent-normal sensitivity,
not a nonnegative structural spending model. If merging is not defensible, skip MLE
and explain using exact wording; retain the original ordered results instead.

If the gate passes: primary normal latent-yuan affine model with a common constant
sigma; one sensitivity with sigma separately estimated at each of the three amounts
(common across forms within amount). Fit form intercepts/form slopes and form
intercepts/common slope in each scale model. Bootstrap 4,000 independent nine-cell
draws, seed 2026100418, for each unrestricted scale model, using grouped likelihood
counts equivalent to resampled respondent intervals. Report percentile intervals,
robust score/Hessian covariance, slope-equality Wald diagnostics, constrained model
fit, all 45 merged category probabilities and calibration discrepancies. Bootstrap
failures remain disclosed, not silently removed or redrawn. Optimize from fixed
observed-fit starts; one deterministic retry from a fixed neutral start is allowed
for numerical convergence, without changing the model. No model tuning or alternative
censoring search. Record gradient and convergence diagnostics.

## B. Scientific sensitivity family 42

Seven existing outcomes: ordinal, midpoint, any_spending (displayed as above-bottom),
ge10, ge25, ge50, top75. Six tests each: three within-form trends, 2-df interaction
omnibus, Cash–Food and Cash–Medical trends. Same linear per-fivefold trend and HC3
as the existing 21-test family. Extend the joint influence vector to all 21 form
slopes; covariance includes outcome dependence. Gaussian centered unrestricted-error
min-P, 10,000 draws, seed 2026100419, uses normal scalar p values and chi-square2
omnibus p values. Holm42 and Bonferroni42 scalar intervals. Preserve the old21 family.
These are asymptotic sensitivity results, not sharp-null randomization inference.

## C. Food expenditure and sign

Before fitting: the sharp simple increasing-bindingness prediction is
Food−Cash size slope <0 in the group more likely to bind. Higher baseline eligible
food spending should weaken that disadvantage. The historical opposite sign cannot
be described as exactly predicted or as affirmative evidence for this simple story.

Independently reproduce Top75 Food−Cash +8.00/+1.33 pp per fivefold amount increase
in G=0/G=1, where G=1 iff six times the monthly food-band lower bound exceeds5,000.
Adult Cash/Food only. G=0 means failure of the proxy condition, not observed binding.
Report all12 subgroup×form×amount cells, six bins, ordinal, midpoint, Top75 and
above-bottom frequencies. No new subgroup definition.

Continuous primary moderator: Q29 ordered food-expenditure band, centered/scaled
within adult Cash/Food. Fit C(form)*z*food_band_z for Top75, midpoint and ordinal.
Adjusted: C(form)*z*(food_band_z+income_z+household_band_z), including every lower-order
term; income_z is standardized log of the existing M1 income mapping, household
size is standardized Q28 ordered response (top coding disclosed). Six focal
three-way tests (three outcomes × unadjusted/adjusted) have Holm6; robust HC3,
observational-moderator interpretation. No further covariates or moderator searches.

Ratio sensitivity: monthly Food M1=[250,750.5,1500.5,2500.5,4000.5,7500],
M2=[125,750.5,1500.5,2500.5,4000.5,10000] for bands1–6. These are proxies with
open-band endpoint sensitivity, never exact expenditure. Let lf=log(6*proxy),
la=log(amount). Compare unrestricted outcome~C(form)*(la+lf) with ratio-only
outcome~C(form)*(la-lf), for three outcomes and both mappings. Joint2-df restrictions
on common and form-dependent coefficients, Holm6. Also report coefficient pairs,
fit loss and the prior interaction-only1-df restriction as a labelled historical
comparison. Rank/ordered moderation is represented by the predeclared Q29 model;
no monetary ratio is manufactured from ranks.

## D. Prediction and precision, metadata and writing

Use frozen existing diagnostics plus the above results. For scalar tests, normal
80% MDE=(z_.975+z_.8)*SE; conservative family MDE replaces z_.975 with
z_(1-.05/(2K)). For joint tests no unique scalar MDE exists; supply coefficient
contrasts where already estimated or explicitly mark not scalar-interpretable.
Do not re-run broad screens. For commensurate standardized moderation, show the
observed10th–90th moderator span times coefficient CI relative to the matching
headline slope; this is a compatible moderation range, not causal percent explained.

Audit original documents for recruitment, dates, incentives, randomization, ethics,
consent and author declarations. Ask for unresolved author facts and list them.
Produce adult sample/missingness and balance tables using baseline age, gender,
education, income, household size, employment, hukou and defensible region labels.
No more than these eight balance tests; Holm8, descriptive diagnostic only. Use
Q1/Q2 as response-style screens. Record exact scenario/options in Chinese/English.

Verify the ten priority references with current primary sources, and official JEBO
abstract/AI-disclosure requirements where accessible. Rewrite only jebo_v3, select
title after results, produce response letter, source/claim audits, four main figures
and economical main tables. All timing language states the post hoc stage. Stop after
these analyses; weaker evidence changes the story, never the analysis list.
