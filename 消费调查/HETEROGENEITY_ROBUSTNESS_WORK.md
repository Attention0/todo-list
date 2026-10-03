# 消费调查项目 — Formal Heterogeneity Robustness & Predictability Exploration

## 0. Purpose

This is the **second-pass formal exploration** after:

- `SPEC.md`
- `DATA_AUDIT.md`
- `FIRST_LOOK.md`
- `HETEROGENEITY_AUDIT.md`
- `HETEROGENEITY_RESULTS.md`

The first heterogeneity pass was intentionally broad and useful for discovery, but several specifications are not yet suitable for a paper-quality economics analysis. This round must:

1. correct the treatment of categorical variables;
2. make the regression estimands explicit;
3. separate identification from precision controls / fixed effects;
4. provide principled inference for an individual-level randomized survey experiment;
5. distinguish MPC-level predictability from treatment-effect / fungibility predictability;
6. improve ML HTE estimation and honest validation;
7. quantify how much of stated-MPC heterogeneity is explainable by observables;
8. explicitly benchmark the empirical question against Lewis, Melcangi & Pilossoph (2026, ReStud), **without mechanically copying their estimator**, because our data structure is different;
9. determine whether the strongest findings from the first exploration survive a stricter specification.

The goal remains **exploration and diagnosis**, not writing a paper story and not maximizing significance.

---

# 1. Key correction from the first pass

The first-pass script standardized all baseline variables numerically for the one-variable scan, including nominal categorical variables such as employment status and work-unit type. This is not acceptable for the formal second pass.

### Required correction

Variables must be classified into:

### A. Continuous / approximately continuous scales

Examples:

- age;
- Q1–Q22 0–10 scales;
- subjective SES where a linear trend is substantively defensible.

Use:

- centered and standardized linear term as the main parsimonious specification;
- spline / bins as robustness for top variables.

### B. Ordered categories

Examples:

- education;
- harmonized income category;
- household size;
- food-spending category;
- medical-spending category;
- city tier.

For these variables, estimate **both**:

1. a standardized linear-trend specification, for a one-number summary;
2. a categorical-dummy specification, as the formal robustness check.

Do not interpret the linear trend as the only model.

### C. Nominal categorical variables

Examples:

- hukou type;
- work status;
- work-unit type;
- housing tenure;
- prior subsidy status;
- gender if coded as categories.

These must enter as factor/dummy variables. Never z-score numeric labels and interpret the resulting coefficient as an economic slope.

For treatment-effect heterogeneity, interact the full set of category dummies with treatment and test them jointly.

---

# 2. Data construction and reproducibility

## 2.1 Raw data

Continue to use the original delivery Stata file only as read-only input.

Do not upload respondent-level data to GitHub.

All transformations must be generated in code from raw variables.

## 2.2 Treatment reconstruction

Reconstruct treatment from Q32–Q40 exactly as previously verified:

- cash × 200 / 1000 / 5000;
- food × 200 / 1000 / 5000;
- medical × 200 / 1000 / 5000.

Cross-check against `scen_*` metadata on every run.

Abort the script if:

- any respondent has zero or multiple treatment outcomes;
- reconstructed treatment differs from metadata;
- outcome is outside 1–6.

## 2.3 Sample definitions

Keep three explicitly named samples:

### Sample R — Raw
N = 5,497, subject only to valid treatment assignment.

### Sample C — Clean candidate
Use the existing transparent rule:
- remove Q1–Q13 complete straight-liners;
- remove age outside 18–100;
- remove duplicate IDs / assignment anomalies if any.

Do not change this rule after looking at results.

### Sample A — Adult-only minimal
Only age 18–100 restriction, no straight-line exclusion.

This separates the effect of age eligibility from the stronger quality screen.

Every headline result should report R and at least one of C/A.

---

# 3. Outcome definitions

## 3.1 Primary outcome

`outcome_ord` = original 1–6 stated incremental-consumption category.

This is the primary measurement object.

Do not describe it as realized MPC.

## 3.2 Auxiliary numerical MPC

`mpc_midpoint`:

- 1 → 0
- 2 → .05
- 3 → .175
- 4 → .375
- 5 → .625
- 6 → .875

Alternative:
- category 6 → 1.0.

This is useful for:
- intuitive effect sizes;
- prediction;
- ML;
- variance-explanation exercises.

It is not a precisely observed continuous MPC.

## 3.3 Threshold outcomes

Retain:
- any_spend;
- 10%+;
- 25%+;
- 50%+.

Use only for robustness / interpretation of where in the distribution the effect arises.

## 3.4 Ordered-outcome model

For top findings estimate:
- ordered logit;
- ordered probit.

Check proportional-odds sensitivity by comparing threshold-specific binary models. If signs / conclusions vary sharply across thresholds, flag the result rather than forcing a single latent-index interpretation.

---

# 4. Treatment estimands

Predefine:

## 4.1 Average form effects

At each amount:
- Food − Cash;
- Medical − Cash;
- Medical − Food.

Pooled across amount:
- Food − Cash;
- Medical − Cash;
- Medical − Food;
- Restricted (Food + Medical) − Cash.

## 4.2 Fungibility heterogeneity

For baseline trait X:

[
	au_F(x)=E[Y(Food)-Y(Cash)mid X=x]
]

[
	au_M(x)=E[Y(Medical)-Y(Cash)mid X=x]
]

These are conditional randomized treatment contrasts.

Do **not** create an observed individual-level “fungibility gap.”

## 4.3 Medical-vs-food heterogeneity

This is not a cash-fungibility estimand, but it is substantively useful:

[
	au_{MF}(x)=E[Y(Medical)-Y(Food)mid X=x].
]

Keep this as a separate object throughout.

---

# 5. Main regression specifications

## 5.1 Reduced-form benchmark

For outcome Y:

[
Y_i=alpha+lambda_{type(i)}+mu_{amount(i)}
+(lambda	imesmu)_{type(i),amount(i)}+arepsilon_i.
]

Estimate:
- no controls;
- HC1 robust SE as direct replication of the first pass;
- HC3 as robustness.

Report raw cell means alongside regression contrasts.

---

## 5.2 One-variable HTE — continuous / ordered trend

For standardized X:

[
Y_i =
alpha
+ Type_i	imes Amount_i
+ gamma X_i
+ Type_i	imes X_i
+ Amount_i	imes X_i
+arepsilon_i.
]

This is the **pooled form-HTE model**.

Interpret:
- Food×X = change in Food−Cash contrast per 1 SD X;
- Medical×X = change in Medical−Cash contrast per 1 SD X;
- Medical×X − Food×X = change in Medical−Food contrast.

### Important restriction

This model assumes the type-by-X HTE is pooled across the three amounts, conditional on amount×X.

Therefore, for every candidate top finding also estimate the fully saturated model:

[
Y_i =
Type_i	imes Amount_i	imes X_i
]

plus all lower-order terms.

Test:
1. joint significance of the type×X / type×amount×X terms;
2. whether the HTE differs across 200 / 1000 / 5000.

Do not headline an amount-specific interaction unless the relevant joint/saturated evidence is shown.

---

## 5.3 One-variable HTE — categorical X

For nominal or formal categorical treatment of ordered X:

[
Y_i =
Type_i	imes Amount_i
+ C(X_i)
+ Type_i	imes C(X_i)
+ Amount_i	imes C(X_i)
+arepsilon_i.
]

Report:
- category-specific adjusted treatment contrasts;
- joint Wald test for all Type×C(X) terms;
- omnibus test before discussing any one category.

For top results also use:
[
Type	imes Amount	imes C(X).
]

Do not report a meaningless “one unit increase” for nominal codes.

---

# 6. Controls and fixed effects

## 6.1 Identification principle

Treatment was individually randomized.

Therefore:

- controls are **not required for identification** of treatment effects;
- geographic fixed effects are **not required for identification**;
- controls / FE are precision and robustness devices.

This must be stated explicitly in the report.

## 6.2 Primary HTE specification

Primary:
- no post-treatment variables;
- no geography FE;
- treatment design terms + focal X.

This preserves transparent experimental interpretation.

## 6.3 Prespecified precision-adjusted model

Define one fixed set of pre-treatment covariates before estimating:

- age + age²;
- gender;
- education;
- harmonized income;
- hukou;
- employment status;
- housing tenure;
- minor child;
- household size;
- food spending;
- medical spending;
- prior subsidy;
- city tier.

For nominal variables use dummies.

For each focal X, omit duplicate versions of X from the adjustment set to avoid mechanical collinearity.

Use a Lin-style adjustment robustness:
- center continuous covariates;
- include main effects;
- where computationally manageable, allow treatment-form interactions with the prespecified covariate block.

The main purpose is precision; do not let control selection vary by result.

## 6.4 Geographic FE robustness

Estimate top results with:

### G1
province fixed effects.

### G2
city-tier fixed effects.

### G3
city fixed effects, only if:
- enough observations per city;
- treatment is sufficiently represented across cities;
- no severe sparsity / singularity.

Before using city FE, output:
- number of cities;
- median/min city N;
- treatment-form presence by city;
- proportion of cities with all three forms / all nine cells.

If city FE are too sparse, say so and do not force them.

Never include province FE and city FE simultaneously.

---

# 7. Standard errors and randomization inference

## 7.1 Baseline inference

Because assignment is individual-level and each person contributes one observation:

Primary:
- HC1 robust SE.

Robustness:
- HC3.

Do not cluster merely because economics papers often cluster.

## 7.2 Geography-cluster robustness

Diagnose:
- number of provinces;
- number of cities;
- cluster-size distribution.

For top results report:
- province-clustered SE;
- city-clustered SE if there are enough clusters and no extreme singleton structure.

If province clusters are about 30, use a small-cluster correction / wild-cluster bootstrap for top coefficients if feasible.

Clustering is a robustness exercise, not the primary design-based inference.

## 7.3 Randomization inference

For the strongest average effects and top HTE findings, implement randomization inference based on the actual 3×3 design:

- preserve the observed counts in each of the nine treatment cells;
- randomly permute treatment-cell labels across respondents;
- recompute the target statistic;
- at least 2,000 permutations; preferably 5,000 for final top results.

For HTE:
- keep X fixed;
- permute treatment assignment;
- use the same specification.

Report two-sided randomization p-values.

For a family of top HTE tests, additionally implement a max-|t| randomization correction if feasible.

This provides an inference check that relies directly on the randomized design.

---

# 8. Multiple testing

Keep BH-FDR but make families explicit and fixed.

Families:

1. objective socioeconomic conditions;
2. baseline needs;
3. subjective economic state;
4. broader attitudes.

Separate estimands:
- Food−Cash;
- Medical−Cash;
- Medical−Food;
- level association.

Do not mix secondary outcomes into the primary discovery family.

For headline claims require some combination of:
- primary raw p;
- FDR q;
- randomization-inference p;
- specification stability;
- honest ML support.

Do not require every metric to cross .05 mechanically, but report all.

---

# 9. “What explains stated MPC?” — ReStud-style observables exercise

Add a dedicated section inspired by Lewis, Melcangi & Pilossoph (2026).

Important: their MPCs are recovered from realized spending using Gaussian Mixture Linear Regression. Our MPC outcome is directly elicited and coarsened. Therefore **do not apply their GMLR mechanically and do not compare R² numbers as if they were the same estimand**.

Our corresponding question is:

> How much variation in stated MPC can be explained or predicted by observed baseline characteristics?

## 9.1 Individual associations

For each baseline variable:
- estimate univariate / minimally adjusted association with `mpc_midpoint`;
- report coefficient / group means;
- adjusted R² contribution where meaningful.

## 9.2 Joint regression

Build fixed models:

### T
Treatment design only:
- type × amount.

### O
T + objective conditions + baseline needs.

### S
T + subjective economic states.

### A
T + broader attitudes.

### O+S
T + objective + subjective economic.

### O+A
T + objective + attitudes.

### ALL
T + all pre-treatment observables.

Use:
- correctly dummy-coded categorical variables;
- age + age²;
- no interaction explosion in this particular **level-predictability** exercise unless explicitly comparing nonlinear ML.

Report:
- in-sample R²;
- adjusted R²;
- 10-fold CV R²;
- repeated 5-fold CV R²;
- RMSE.

The main object is the **incremental predictive value** relative to T.

Example:
[
Delta R^2_{O}=R^2(T+O)-R^2(T).
]

## 9.3 Block incremental value

Using nested CV, estimate:
- O → O+S;
- O → O+A;
- O → ALL.

Report whether subjective variables add material out-of-sample predictive power beyond objective information.

## 9.4 Variance decomposition description

Report:
- total variance of midpoint-stated-MPC;
- variance explained by treatment cell means;
- additional in-sample variance explained by O/S/A;
- out-of-sample explained variance.

Do not label remaining variance as “preference heterogeneity.” It may include:
- latent preferences;
- unmeasured constraints;
- survey noise;
- coarsening;
- response error.

Use “unexplained / latent-or-noise component” unless stronger evidence is available.

---

# 10. ML for stated-MPC level prediction

Use the same train/test folds for fair model comparison.

## 10.1 Models

At minimum:

1. ridge;
2. elastic net;
3. random forest;
4. histogram gradient boosting.

If XGBoost / LightGBM / CatBoost are available without fragile environment changes, add **one** boosted-tree implementation, not all three.

## 10.2 Cross-validation

Use nested CV for penalized / tuned models:

Outer:
- repeated 5-fold, 2–5 repeats.

Inner:
- 5-fold tuning.

Do all preprocessing inside training folds:
- imputation;
- standardization;
- one-hot encoding.

No leakage.

## 10.3 Metrics

Report:
- OOS R²;
- RMSE;
- MAE.

For ordinal outcome also report:
- ordered-model log-likelihood / cross-entropy or an appropriate ordinal score if practical.

## 10.4 Explainability

For the best OOS model:
- permutation importance;
- ALE or partial dependence for top continuous variables.

Do not treat feature importance as a mechanism or causal effect.

---

# 11. ML for heterogeneous treatment effects / fungibility

The first pass used RF T-learners and a DR learner. Keep them as benchmarks but add more principled HTE learners if the environment permits.

## 11.1 Contrasts

Run separately:

- Food vs Cash;
- Medical vs Cash;
- Restricted vs Cash.

Keep Medical vs Food as a secondary contrast.

## 11.2 Target

Primary pooled CATE:
[
	au(x)=E_A[E(Y(1)-Y(0)mid X=x,A)]
]
averaged over the randomized amount distribution.

Amount is not the heterogeneity target here.

Use amount:
- in nuisance models;
- in stratification;
- or as an adjustment variable.

Do not let amount be a hidden source of apparent X heterogeneity.

Secondary:
- amount-specific CATEs if precision permits.

## 11.3 Cross-fitting folds

Stratify folds by:
- transfer form × amount cell

rather than transfer form alone.

This ensures each fold preserves the 3×3 design as closely as possible.

## 11.4 Learners

### H1 — Causal forest / generalized random forest
Preferred if available through `econml`, `grf` equivalent, or another reliable package.

Use:
- honest / subsampled forest;
- minimum leaf sizes appropriate for N≈3,600 pairwise samples;
- fixed random seeds;
- OOF predictions.

### H2 — R-learner
Residualize:
- outcome on X + amount;
- treatment on design probability / amount.

Then learn the residual-on-residual CATE with:
- random forest;
- gradient boosting;
- or penalized linear interactions.

### H3 — DR-learner
Retain a doubly robust learner with cross-fitted nuisance models.

### H4 — T-learner RF
Retain only as a benchmark to compare against the first pass.

Do not declare a heterogeneity result strong because only one learner finds it.

## 11.5 Known propensities

Because treatment is randomized:
- use design/sample assignment probabilities;
- do not fit an elaborate propensity model unless checking assignment balance.

For pairwise contrasts, compute treatment probabilities from the design / observed randomization proportions, potentially conditional on amount if needed.

## 11.6 Honest validation

Every CATE model must be evaluated with OOF predictions.

Report:

1. BLP calibration slope:
   [
   Ysim W+hat	au_c+W	imeshat	au_c+Amount
   ]

2. CATE quintiles:
   - form randomized contrast within each OOF-predicted quintile;
   - N treated/control;
   - CI.

3. Top-minus-bottom effect difference.

4. Rank / policy metrics if available:
   - RATE / AUTOC / Qini-type measure.

5. Treatment balance inside OOF CATE quintiles.

The headline is whether predicted heterogeneity **calibrates in held-out data**, not whether the forest has visually interesting feature importance.

---

# 12. Categorical-feature handling in ML

Use one-hot encoding for nominal variables.

For ordered categories:
- compare ordinal integer coding vs one-hot in ML;
- choose based on OOS performance, not in-sample fit.

For province/city:
- do not feed hundreds of sparse city dummies into the main ML model automatically;
- keep city tier in main feature set;
- province may be included as a low-dimensional categorical robustness if cell counts are adequate.

---

# 13. Medical-specific investigation

The first pass found the most stable HTE in Medical−Food:

- income: negative;
- education: negative;
- past medical spending: positive.

These must receive a targeted formal re-test.

For each:

1. linear-trend HTE;
2. categorical/binned HTE;
3. saturated type×amount×X;
4. no controls;
5. prespecified controls;
6. province FE;
7. HC1 / HC3 / geographic cluster robustness;
8. ordered logit/probit;
9. raw / clean / adult-only samples;
10. randomization-inference p-value.

For past medical spending especially:
- show group-specific treatment means and CIs;
- do not call it bindingness;
- interpret as prior medical need/exposure proxy only.

For income / education:
- examine whether one is simply proxying for the other by estimating a joint model containing both and medical spending.

Then estimate a focused joint specification:
[
Y =
Type	imes Amount
+ Income
+ Education
+ MedicalSpending
+ Type	imes(Income+Education+MedicalSpending)
+ Amount	imes(Income+Education+MedicalSpending)
+	ext{prespecified controls}.
]

Report whether the three HTE patterns survive jointly.

---

# 14. Food-cash null investigation

The first pass found:

- a negative average Food−Cash gap among clearly inframarginal households;
- almost no stable observable HTE explaining that gap.

Treat this as an important empirical pattern and try to falsify it.

## 14.1 Reproduce binding classification

Use interval bounds, not only midpoints.

Check alternative conservative definitions:
- strict inframarginal;
- very-strict inframarginal: transfer <= 50% of lower-bound six-month food spending, if sample permits.

## 14.2 HTE

Within inframarginal samples test:
- income;
- food spending;
- household size;
- children;
- liquidity;
- subjective SES;
- expectations.

Use:
- correctly coded categories;
- joint tests;
- honest CATE ML.

## 14.3 Null evidence

Do not equate non-significance with homogeneity.

Report:
- CI widths;
- smallest heterogeneity magnitude that can be ruled out;
- equivalence-style intervals where practical.

For the strongest null variables, provide detectable-effect / CI-based interpretation.

---

# 15. Geographic and demographic structure diagnostics

Before FE/cluster use, create:

`tables/geography_diagnostics.csv`

with:
- province N;
- city N;
- mean / median / min observations per cluster;
- number of treatment forms per cluster;
- number of treatment cells per cluster.

Also create:
- treatment balance by province;
- treatment balance by city tier.

No individual-level output.

---

# 16. ReStud 2026 benchmark table

Create a short table in the report:

| Dimension | Lewis et al. (2026 ReStud) | Our survey |
|---|---|---|
| MPC source | realized spending response to 2008 rebate, MPC distribution estimated via GMLR | directly elicited, 6-category hypothetical stated MPC |
| transfer variation | tax rebate receipt/timing | randomized transfer form × amount |
| heterogeneity method | latent-group GMLR, then WLS projection on observables | direct outcome prediction + randomized HTE / CATE |
| observables | household financial/demographic characteristics; APC, income, housing, etc. | objective conditions + subjective economic states + broader attitudes |
| explained variation | ~6% adjusted R²; measurement-error correction ~8% | report our in-sample and OOS R², but do not claim numerical comparability |
| main interpretation | much MPC heterogeneity is not captured by standard observables | test whether richer subjective information materially improves prediction |

This comparison must be precise and cautious.

Do not write:
“we replicate their 8% result.”

Instead write:
“qualitatively, both exercises ask how much MPC heterogeneity is captured by observables; the measurement objects differ materially.”

---

# 17. Do NOT mechanically copy GMLR

Lewis et al. use Gaussian Mixture Linear Regression because household-specific MPCs are latent coefficients in realized spending regressions.

In our data:
- each respondent directly reports one coarsened stated MPC outcome;
- each respondent receives only one transfer scenario;
- there is no within-person panel of realized consumption responses.

Therefore:
- do not present GMLR as if it recovers true individual MPCs here;
- do not force a finite mixture of six response categories and call that latent MPC types.

If a latent-class model is explored, label it purely exploratory and justify identification separately. It is **not required** for this round.

---

# 18. Required modifications to existing code

Modify / replace `analysis/heterogeneity_analysis.py` so that:

1. categorical variables are no longer z-scored and treated as linear in formal HTE scans;
2. ordered variables have both trend and dummy versions;
3. saturated Type×Amount×X models are available;
4. fixed-effect robustness is implemented;
5. HC1 and HC3 are both supported;
6. geographic cluster diagnostics and clustered-SE robustness are implemented;
7. randomization inference is implemented for top findings;
8. model families and FDR corrections are fixed in code;
9. level-predictability models use the same CV folds for fair comparison;
10. HTE folds stratify on treatment-cell structure;
11. at least one causal-forest / R-learner style estimator is added if dependencies permit;
12. all preprocessing occurs inside training folds;
13. no respondent-level predictions / data are committed to GitHub;
14. every table has a machine-readable CSV and every headline figure is reproducible.

Keep the old first-pass outputs for comparison; do not silently overwrite them without versioning.

Suggested new script:
- `analysis/heterogeneity_formal.py`

---

# 19. Deliverables

Create:

- `HETEROGENEITY_FORMAL_AUDIT.md`
- `HETEROGENEITY_FORMAL_RESULTS.md`
- `analysis/heterogeneity_formal.py`
- `tables/formal_*.csv`
- `figures/formal_*.png`

## 19.1 HETEROGENEITY_FORMAL_AUDIT.md

Must document:
- data preprocessing;
- variable types and coding;
- exact equations;
- reference categories;
- covariate set;
- FE choices;
- SE / cluster choices;
- randomization inference;
- multiple testing;
- ML folds;
- hyperparameter grids;
- dependencies actually available;
- any deviations from this protocol.

## 19.2 HETEROGENEITY_FORMAL_RESULTS.md

Organize by substantive question:

### I. How much of stated-MPC variation is predictable?
- treatment-only;
- O;
- S;
- A;
- O+S;
- O+A;
- ALL;
- in-sample vs OOS.

### II. Which individual observables survive joint modeling?
- univariate;
- multivariate;
- regularized;
- ML importance.

### III. Is Food−Cash fungibility heterogeneity predictable?
- linear / categorical;
- inframarginal subsample;
- honest ML;
- power / CI of nulls.

### IV. Is Medical−Cash heterogeneity predictable?
- theory-guided;
- ML calibration;
- strongest subgroups.

### V. Why does Medical differ from Food?
- income;
- education;
- medical spending;
- joint specification;
- amount dependence.

### VI. Robustness
- raw / adult / clean;
- FE;
- HC1 / HC3 / clusters;
- randomization inference;
- ordinal models;
- outcome codings.

---

# 20. Final synthesis

At the end provide exactly:

## A. Facts that survived the formal re-analysis
Maximum 10.

For each:
- estimand;
- effect size;
- CI;
- p;
- q;
- randomization p if computed;
- sample;
- specification stability.

## B. Findings that disappeared after correct categorical coding / controls
List explicitly.

## C. Predictability facts
- treatment-only OOS R²;
- O incremental OOS R²;
- S incremental OOS R²;
- A incremental OOS R²;
- ALL OOS R²;
- best nonlinear ML OOS R².

## D. HTE predictability
For Food−Cash and Medical−Cash:
- best honest learner;
- calibration;
- top-bottom separation;
- whether multiple learners agree.

## E. Strong nulls
Include:
- variables / domains that clearly do not add predictive value;
- food-cash HTE nulls with precision.

## F. Candidate research interpretations
At most 3 clusters.

For each:
- what the data support;
- what the data do not identify;
- how it relates to the ReStud “observables explain little MPC heterogeneity” benchmark;
- whether it is specific to transfer form rather than general MPC level.

---

# 21. Interpretation discipline

Never claim:

- realized MPC;
- welfare;
- cash-equivalent valuation;
- causal effect of income / attitudes themselves;
- individual-level observed fungibility;
- latent preference heterogeneity as a proven mechanism.

Allowed language:

- stated MPC;
- randomized transfer-form effect;
- conditional treatment-effect heterogeneity;
- predictive content of observables;
- unexplained heterogeneity;
- consistency with latent/unmeasured traits, subject to survey measurement noise.

The core aim is to discover whether the data support a disciplined statement such as:

> Rich baseline observables explain only a small share of stated-MPC variation, while transfer-form responses—especially medical-account responses—display a distinct and partly predictable heterogeneity structure.

Do not adopt that sentence as a conclusion unless the formal analysis actually supports it.
