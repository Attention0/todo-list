# MPC curve heterogeneity: who drives the size effect?

## 0. Purpose

This is a bounded mechanism-oriented heterogeneity pass for the consumer-survey project.

The main reduced-form story is already fixed by PR #9 and PR #10:

> Small cash transfers generate a disproportionately large high-MPC response. As transfer size rises, this upper tail compresses sharply. Food and Medical show much weaker compression, so transfer form changes how stated MPC scales with transfer size.

The purpose of this round is NOT to search for a new headline. It is to answer a narrower question:

> **Who drives the Cash size gradient, and which observable household characteristics are associated with the Cash-vs-Restricted difference in that gradient?**

This round should distinguish three objects:

1. **Who has the steepest Cash amount curve?**
2. **Which groups account for most of the aggregate decline in the high-MPC tail?**
3. **Do standard observables explain the Restricted-vs-Cash difference in size sensitivity, or does that difference remain largely unexplained?**

Do not modify the manuscript in this pass.

---

# PART I. IDENTIFICATION AND CLAIM BOUNDARIES

## 1. What is identified

Form and amount are randomized.

Therefore, for any pre-treatment observable X, it is valid to estimate:
- subgroup-specific Cash amount effects;
- subgroup-specific Restricted-vs-Cash differential amount effects;
- form × amount × X moderation.

However, X itself is not randomized.

So the analysis may say:

> "The size gradient is concentrated among households with low emergency liquidity."

It may NOT say:

> "Low liquidity causes the size gradient."

Use terms such as:
- moderation;
- concentration;
- heterogeneity;
- association with treatment sensitivity;
- where the experimental effect is strongest.

Do not make causal claims about income, liquidity, education, medical need, or other baseline observables.

Each respondent still provides exactly one randomized scenario response. Do not construct within-person MPC curves or individual slopes.

---

# PART II. PRIMARY OUTCOME AND CONTRASTS

## 2. Primary outcome

The primary heterogeneity outcome should be:

> **Top-MPC indicator: response category >75%.**

Reason:
- PR #9 and PR #10 show that this is where the Cash amount pattern is most visible;
- it does not depend on midpoint coding;
- both Food and Medical show weaker amount compression in this margin.

Secondary outcomes:
1. ordinal score;
2. midpoint MPC;
3. MPC >=50%;
4. any additional spending.

Do not expand to all outcomes unless needed for a predefined robustness table.

---

## 3. Primary treatment contrasts

Preserve z = (-1, 0, 1) for RMB 200 / 1,000 / 5,000.

For each moderator X estimate two primary quantities:

### A. Cash size-gradient moderation

Within Cash:

TopMPC = a + b z + c X + d (z × X) + error

Key estimand:
- d = how the Cash amount slope varies with X.

### B. Restricted-vs-Cash size-gradient moderation

Define Restricted as the equal-weight average of Food and Medical, exactly as in PR #10.

Estimate the full model with:
- form;
- z;
- X;
- form × z;
- form × X;
- z × X;
- form × z × X.

Key estimand:
- Restricted × z × X.

This asks whether the difference between Cash and Restricted amount sensitivity itself varies with X.

Also report Food-vs-Cash and Medical-vs-Cash three-way terms as secondary diagnostics.

---

# PART III. PRESPECIFIED OBSERVABLES

## 4. Tier 1: core economic moderators

These are the main mechanism-oriented variables and should receive the most attention.

### 4.1 Emergency liquidity / fundraising capacity
Use the existing Q7 coding already used in PR #9.

Economic hypothesis:
- households with lower liquidity may be especially likely to treat a small Cash transfer as immediately spendable;
- their Cash high-MPC tail may therefore be especially large at RMB 200 and compress more as amount rises.

Report:
- standardized continuous/rank specification if appropriate;
- a coarse low / middle / high visualization using fixed categories.

### 4.2 Household income
Use the existing harmonized income coding.

Economic hypothesis:
- lower-income households may show higher small-transfer Cash MPC and a steeper amount gradient.

Use:
- standardized rank/continuous coding;
- pre-specified terciles or economically interpretable categories for plots.

### 4.3 Baseline food expenditure
Use the existing Q29 category-rank coding.

Purpose:
- tests whether baseline consumption needs or expenditure intensity predict Cash size sensitivity;
- also allows comparison with Food-form moderation.

### 4.4 Baseline medical expenditure
Use the existing Q30 category-rank coding.

Purpose:
- tests whether underlying expenditure needs predict Cash size sensitivity;
- also allows comparison with Medical-form moderation.

### 4.5 Prior subsidy experience
Use the existing pre-treatment subsidy-history variable.

Purpose:
- checks whether familiarity with transfers is associated with weaker or stronger size sensitivity.

These five variables form the PRIMARY moderator family.

---

## 5. Tier 2: descriptive household profile

Use only a small fixed set:

1. age;
2. education;
3. household size;
4. presence of minor child;
5. housing status / tenure;
6. work status.

These are secondary descriptive moderators.

Do NOT add:
- psychological scales;
- personality factors;
- attitudes;
- dozens of demographics;
- post-treatment variables.

The goal is to characterize "who" without reopening a broad fishing exercise.

---

# PART IV. SINGLE-MODERATOR ANALYSES

## 6. Standardized continuous/rank specifications

For each moderator:

- standardize using the full R sample;
- estimate the Cash z×X interaction;
- estimate the Restricted×z×X interaction;
- report HC3 SE, 95% CI, raw p-value;
- apply Holm correction separately to:
  - Tier 1 Cash-slope moderation family;
  - Tier 1 Restricted-vs-Cash family;
  - Tier 2 Cash-slope family;
  - Tier 2 Restricted-vs-Cash family.

Do not combine all tests in one huge multiplicity family, but do not report unadjusted significance as confirmatory evidence.

---

## 7. Subgroup curve plots

For each Tier 1 moderator, produce a simple visualization:

- low X;
- middle X;
- high X;

and plot the top-MPC probability across:
- 200;
- 1,000;
- 5,000;

for:
- Cash;
- Restricted;
- optionally Food and Medical in light lines.

The bins must be defined before looking at treatment effects.

Recommended:
- terciles for ranked/continuous variables where natural categories are unavailable;
- original categories when economically meaningful.

Each figure should display:
- subgroup N;
- cell means;
- 95% CIs.

Do not infer individual transitions.

---

# PART V. WHO DRIVES THE CASH TOP-TAIL DECLINE?

## 8. Variable-by-variable contribution decomposition

The aggregate Cash top-category probability falls substantially from RMB 200 to RMB 5,000.

For each moderator separately, decompose this endpoint decline across exhaustive subgroups.

For subgroup g:

Contribution_g = population_share_g × [P(top | Cash, 5000, g) - P(top | Cash, 200, g)]

The contributions within a given moderator partition should sum to the total standardized Cash endpoint decline, up to sampling / weighting differences.

Report for each moderator:
- subgroup share;
- Cash top probability at 200;
- Cash top probability at 1,000;
- Cash top probability at 5,000;
- subgroup endpoint decline;
- weighted contribution;
- share of total decline.

IMPORTANT:
This is a **where-the-decline-occurs decomposition**, not a causal attribution.

Because moderators are correlated, contributions from different variables CANNOT be added across variables.

Do not say:
- "income explains 40% and liquidity explains 30%, therefore together 70%."

Instead say:
- "Within the income partition, X% of the aggregate decline occurs among the lowest-income group."
- "Within the liquidity partition, Y% occurs among low-liquidity households."

---

# PART VI. WHO DRIVES THE RESTRICTED-vs-CASH DIFFERENCE?

## 9. Differential-slope decomposition by subgroup

For each Tier 1 moderator, estimate within each low/mid/high subgroup:

1. Cash amount slope;
2. Restricted amount slope;
3. Restricted−Cash differential slope.

Then ask:

> In which subgroup is the Cash-vs-Restricted difference largest?

Produce one compact forest table / figure for:
- liquidity;
- income;
- food spending;
- medical spending;
- prior subsidy.

This is likely the most useful "who drives the puzzle?" figure.

---

# PART VII. JOINT MODEL: DO OBSERVABLES EXPLAIN THE PATTERN?

## 10. Joint theory-driven interaction model

Fit a joint model using only the five Tier 1 moderators.

For the top-MPC outcome include:
- all lower-order terms;
- form;
- z;
- the five standardized X variables;
- form × z;
- z × X_j;
- form × X_j;
- form × z × X_j.

Use Restricted vs Cash as the main form contrast.

Do not add Tier 2 variables to the primary joint model.

Report:

1. baseline Restricted−Cash differential slope without moderators;
2. average differential slope after allowing moderator interactions;
3. joint Wald test that all Restricted×z×X_j terms = 0;
4. joint Wald test that all Cash z×X_j terms = 0;
5. the estimated heterogeneity range across realistic X profiles;
6. out-of-sample predictive improvement from adding the five interaction blocks.

Interpretation:
- if joint interactions are weak and predictive gain is tiny, observables do not meaningfully explain who drives the curve;
- if one or two interactions dominate and are stable, they become candidate mechanism evidence.

Do not claim that interaction adjustment "explains away" the average randomized effect unless that statement is mathematically well-defined.

---

# PART VIII. HONEST PREDICTION OF TREATMENT SENSITIVITY

## 11. Optional cross-fitted low-dimensional model

Because the user specifically wants to know "who changes", it is useful to ask whether the pre-treatment observables can predict size sensitivity out of sample.

Use only the prespecified Tier 1 variables.

Preferred methods:
- linear / logistic interaction model;
- shallow tree as a diagnostic.

Do NOT use:
- causal forest;
- boosted HTE discovery;
- SHAP;
- high-dimensional black-box searches.

Use 5-fold cross-fitting.

Construct predictions of:
- Cash top-MPC probability at 200;
- Cash top-MPC probability at 5,000;
- predicted Cash endpoint decline;
- Restricted-vs-Cash differential decline.

Then report:
- distribution of predicted subgroup sensitivity;
- calibration by predicted-sensitivity quintile;
- out-of-sample calibration slope;
- whether the highest-predicted-sensitivity group actually shows a larger randomized Cash endpoint difference.

This is a secondary diagnostic.

Do not claim individual treatment effects are observed.

---

# PART IX. MECHANISM PATTERN TESTS

## 12. Liquidity mechanism signature

The cleanest candidate mechanism is liquidity / financial slack.

A liquidity-based explanation is more credible if we see the following joint pattern:

1. low-liquidity households have a higher top-MPC probability for RMB 200 Cash;
2. their Cash top-MPC probability declines more strongly as amount rises;
3. the Restricted-vs-Cash size differential is also larger for low-liquidity households;
4. the pattern appears in both continuous interaction and subgroup plots;
5. it survives the joint Tier 1 model.

If only condition 1 holds, that is merely a level effect, not an explanation of the amount curve.

---

## 13. Income mechanism signature

Similarly, a low-income explanation requires:

1. stronger small-Cash high-MPC response among lower-income households;
2. a steeper Cash amount decline;
3. evidence that the Cash-vs-Restricted differential slope varies with income.

Do not infer mechanism from "low-income households have higher MPC" alone.

---

## 14. Need-matching signature

For expenditure-need variables:

### Food spending
Ask whether higher food needs change:
- Food-vs-Cash slope;
- the general Restricted-vs-Cash slope.

### Medical spending
Ask whether higher medical needs change:
- Medical-vs-Cash slope;
- the general Restricted-vs-Cash slope.

PR #9 found weak level-matching evidence but little evidence that need explains the size differential.

Treat this as a confirmation / falsification exercise, not a new discovery opportunity.

---

# PART X. ROBUSTNESS

## 15. Outcome robustness

For any Tier 1 moderator that looks substantively important in the primary top-MPC outcome, repeat only:

1. ordinal score;
2. midpoint MPC;
3. >=50% threshold.

Do not run every moderator across every possible outcome.

The purpose is to distinguish:
- a genuine curve-moderation pattern;
from
- a one-threshold artifact.

---

## 16. Sample robustness

For the strongest one or two moderator patterns only, repeat in:
- R;
- A;
- C;
- Q1;
- Q2.

Do not require all quality-screen estimates to be significant.

Report:
- sign;
- effect size;
- CI;
- whether point estimates materially collapse or reverse.

Do not hide unfavorable Q1/Q2 results.

---

# PART XI. WHAT WOULD COUNT AS AN EXPLANATION?

## 17. Strong observable explanation

A baseline observable can be described as an important explanatory correlate only if:

1. the three-way interaction is economically meaningful;
2. the interaction is reasonably precise after family-wise correction;
3. subgroup curves visually support the same pattern;
4. the pattern survives the joint Tier 1 model;
5. the result is not only a level difference;
6. the result is directionally stable in major sample/outcome checks.

Even then, use language such as:
- "consistent with";
- "concentrated among";
- "points to";
- "suggests a role for".

Do not say "proves the mechanism".

---

## 18. Weak or null explanation

If none of the five Tier 1 variables robustly moderate the Cash or Restricted-vs-Cash size slopes, this is itself informative.

The conclusion should then be:

> Standard observable markers of liquidity, income, category needs, and prior transfer experience do not explain much of the form-by-size pattern.

That would strengthen the idea that the phenomenon is not reducible to obvious compositional differences, while leaving the underlying mechanism unresolved.

Do not continue searching for new moderators to rescue a null result.

---

# PART XII. REQUIRED OUTPUTS

Create:

消费调查/results/mpc_who_drives/

with no respondent-level exports.

Required tables:

1. primary_moderator_interactions.csv
2. secondary_profile_interactions.csv
3. subgroup_cash_curves.csv
4. subgroup_restricted_curves.csv
5. cash_decline_contributions.csv
6. subgroup_differential_slopes.csv
7. joint_tier1_model.csv
8. joint_tests.csv
9. prediction_calibration.csv
10. moderator_robustness.csv

Required figures:

### Figure 1 — Who has the steepest Cash curve?
Forest plot of Tier 1 z×X interactions.

### Figure 2 — Who has the largest Restricted-vs-Cash slope difference?
Forest plot of Tier 1 Restricted×z×X interactions.

### Figure 3 — Subgroup curve panels
Liquidity and income first; food / medical need as secondary panels.

### Figure 4 — Contribution to Cash top-tail decline
For each Tier 1 moderator separately, show where the aggregate 200→5000 decline occurs.

### Figure 5 — Joint-model / calibration diagnostic
Show whether observable characteristics meaningfully sort households by predicted Cash size sensitivity.

All figures require source-data CSVs.

---

# PART XIII. FINAL REPORT

Create:

消费调查/MPC_WHO_DRIVES_RESULTS.md

with exactly these sections:

## 1. Bottom line
One paragraph: can observables explain who drives the size curve?

## 2. Who drives the Cash size gradient?
Focus on top-MPC outcome.

## 3. Who drives the Restricted-vs-Cash difference?
Focus on the three-way moderation.

## 4. Liquidity
Does it match the full mechanism signature?

## 5. Income
Does it match the full mechanism signature?

## 6. Consumption needs
Food and medical spending.

## 7. Prior subsidy experience

## 8. Contribution decomposition
Where does the aggregate Cash top-tail decline occur?

## 9. Joint explanatory power
Do the five core observables jointly explain meaningful heterogeneity?

## 10. Prediction / calibration
Can observables sort high-sensitivity households out of sample?

## 11. Robustness and negative evidence
Include unfavorable results.

## 12. Mechanism interpretation
Separate:
- what the experiment identifies;
- what observables suggest;
- what remains unknown.

## 13. Paper implication
Choose one:
- observables provide a coherent mechanism layer;
- observables identify who drives the pattern but not a single mechanism;
- observables explain little; retain the reduced-form puzzle.

## 14. Stop decision
State whether any further observable-variable exploration of the current dataset is scientifically justified.

Default expectation: no.

---

# PART XIV. PAPER-LEVEL DECISION STANDARD

The best possible outcome of this pass would support a story such as:

> The unusual small-transfer Cash response is concentrated among households with limited financial slack. Those households are especially likely to report spending most of a small cash transfer, but this response attenuates sharply as the transfer grows. The same size sensitivity is much weaker for restricted resources, consistent with liquidity and mental-budget mechanisms interacting with transfer form.

This sentence should be used only if the data support the full moderation pattern.

If instead the main observables do not robustly sort the curve, the paper should say:

> The form-by-size interaction is clear in the randomized treatment cells but is not readily explained by standard observable markers of liquidity, income, or category-specific need.

That is also a scientifically useful result.

Do not search beyond the prespecified variables after this report.
