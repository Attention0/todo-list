# 消费调查项目 — Final Exploration: Stable Traits, Context-Specific Fungibility, and Nature-Style Positioning

## 0. Purpose

This is the **last open-ended exploration round** before choosing a paper story.

Read first:

- `SPEC.md`
- `DATA_AUDIT.md`
- `FIRST_LOOK.md`
- `HETEROGENEITY_AUDIT.md`
- `HETEROGENEITY_RESULTS.md`
- `HETEROGENEITY_FORMAL_AUDIT.md`
- `HETEROGENEITY_FORMAL_RESULTS.md`

Treat the formal second-pass results as the current source of truth.

This round should not repeat all previous regressions. It should answer a smaller set of higher-level questions that matter for either:

1. an economics paper extending the “MPC heterogeneity is hard to explain” literature toward transfer-form fungibility; or
2. a broader human-behaviour paper suitable in spirit for journals such as Nature Human Behaviour / Nature Communications.

The central conceptual question is:

> Are differences in consumption responses to windfalls mainly stable individual propensities, or does the *form in which money is delivered* create context-specific reordering of people?

The final round must investigate whether the data support any of the following, without assuming them in advance:

- rich observable traits still explain little of stated-MPC variation;
- subjective economic states add little beyond objective household conditions;
- Food-vs-Cash non-fungibility is broadly present but not systematically structured by observed traits;
- Medical-vs-Cash non-fungibility is more context-specific and partly predictable;
- transfer form changes not only the mean response but the *mapping from person characteristics to response*;
- predictable treatment-effect heterogeneity does or does not translate into useful transfer-form targeting.

Do not force a Nature-style story if the data do not support a sufficiently general behavioural result.

---

# 1. Important interpretation constraints

Always use:

- “stated MPC”;
- “hypothetical incremental-consumption response”;
- “randomized transfer-form effect”;
- “conditional / predictable heterogeneity”;
- “transfer-form fungibility” as behavioral equivalence in stated consumption response.

Never claim:

- realized spending;
- welfare or utility;
- cash-equivalent value;
- actual preference for cash vs in-kind;
- causal effects of baseline income, attitudes, trust, expectations, etc.;
- true individual-level MPC potential outcomes;
- a validated psychological mechanism;
- “latent preference” when the unexplained component also includes measurement noise.

The remaining unexplained component may contain:

- latent preference heterogeneity;
- unobserved constraints;
- coarse outcome measurement;
- hypothetical-bias / survey response error;
- random response noise.

Use “unexplained / latent-or-noise component” unless specifically decomposed.

---

# 2. Do not reopen settled first-pass issues

Retain the formal second-pass rules:

- Raw R / Adult A / Clean C samples;
- correct nominal / ordered / continuous coding;
- HC1 primary, HC3 robustness;
- province / city-tier FE only as robustness;
- no city FE because of sparse city cells unless diagnostics materially change;
- family-wise BH-FDR;
- ordered outcome primary;
- midpoint MPC auxiliary;
- no respondent-level data or OOF predictions committed to GitHub.

Do not rerun broad one-variable fishing unless needed for a specifically defined new object below.

---

# 3. Repair the HTE machine-learning implementation first

The previous formal round provides useful OOF evidence, but the DR and “R learner” implementations should be made more standard before they are used for a final claim.

Create a new script:

- `analysis/final_exploration.py`

Keep old scripts unchanged.

## 3.1 Cross-fitted DR learner

For each binary contrast:

- Food vs Cash;
- Medical vs Cash;
- Medical vs Food.

Use outer folds stratified by original type × amount cell.

Inside each outer training fold:

1. construct nuisance folds;
2. estimate (hat m_1(X,A)) and (hat m_0(X,A)) out-of-fold within the outer training sample;
3. use known/randomized treatment propensity (e(A)), preferably conditional on amount or design-cell probabilities;
4. build DR pseudo-outcomes only from nuisance predictions that did not use the observation’s own outcome;
5. train the CATE learner on those cross-fitted pseudo-outcomes;
6. predict only into the outer held-out fold.

No observation’s outcome may be used both to fit its nuisance prediction and to construct its pseudo-outcome.

## 3.2 Standard R-learner / Robinson residualization

Implement the R-learner objective more faithfully.

For each pairwise contrast:

1. cross-fit
   [
   hat m(X,A)=E[Y|X,A]
   ]
   without using treatment W as a direct regressor in the definition of the marginal outcome nuisance;
2. use known randomized propensity
   [
   e(A)=P(W=1|A);
   ]
3. create residuals
   [
   	ilde Y=Y-hat m(X,A),qquad
   	ilde W=W-e(A);
   ]
4. learn (	au(X)) by minimizing approximately
   [
   sum_i(	ilde Y_i-	ilde W_i	au(X_i))^2
   ]
   with a forest / boosted learner or penalized interaction model;
5. use OOF CATE prediction.

Document the exact implementation.

## 3.3 Causal forest if feasible

If a reliable package is available (`econml`, `causalml`, or equivalent), add one honest causal-forest estimator.

If not available, do not install fragile dependencies solely for this task. Record the limitation.

## 3.4 ML evidence hierarchy

Treat evidence strength in this order:

1. OOF / held-out observed treatment-effect gradient;
2. BLP calibration;
3. top-minus-bottom contrast;
4. agreement across T / DR / R / causal-forest learners;
5. feature importance only last.

Never infer a mechanism from feature importance.

---

# 4. General behavioural question: stable trait or context-specific response?

This is the most important new analysis.

We observe randomized samples from three potential response functions:

[
mu_C(X)=E[Y(Cash)|X],
]

[
mu_F(X)=E[Y(Food)|X],
]

[
mu_M(X)=E[Y(Medical)|X].
]

The question is whether the same baseline characteristics rank people similarly across transfer forms, or whether form changes the mapping from X to Y.

## 4.1 Form-specific outcome models

Using identical feature sets and CV folds, estimate separate OOF response models for:

- Cash;
- Food;
- Medical.

Models:
- ridge / elastic net;
- random forest;
- gradient boosting.

Amount must enter each model.

Report OOS:
- R²;
- RMSE;
- MAE.

This tells us whether one form is more individually predictable than another.

## 4.2 Predictor alignment across forms

Using transparent standardized linear / regularized models, estimate form-specific coefficient vectors for baseline predictors.

Compare across forms using:

- coefficient-vector correlation;
- cosine similarity;
- bootstrap CI;
- sign agreement.

Do this separately for:
- objective / needs variables;
- subjective economic variables;
- broader attitudes;
- ALL.

Question:

> Do the same traits predict spending under Cash, Food, and Medical?

If Medical has a meaningfully different predictor profile while Cash and Food are similar, that is potentially important.

## 4.3 Cross-form prediction transferability

Train a model within one transfer form and evaluate it on another form **without refitting the mapping from X to Y**, after allowing only a mean-level recentering if necessary.

Examples:
- train on Cash, test rank prediction on Food;
- train on Cash, test on Medical;
- train on Food, test on Medical.

Report:
- OOS rank correlation;
- R² where meaningful;
- calibration slope;
- whether adding form-specific refitting materially improves prediction.

This is not a causal estimand. It is a test of whether “who is a high spender out of a windfall” generalizes across money forms.

## 4.4 Shared vs form-specific predictability decomposition

Construct cross-fitted predictions:

[
hatmu_C(X),hatmu_F(X),hatmu_M(X).
]

Define a shared predicted propensity:

[
G(X)=rac{hatmu_C(X)+hatmu_F(X)+hatmu_M(X)}{3}
]

and form-specific deviations:

[
D_t(X)=hatmu_t(X)-G(X).
]

Report variance of:
- shared prediction (G(X));
- each form-specific deviation;
- actual outcome.

Use cross-fitting so this is not an in-sample decomposition.

Interpret only descriptively:

> how much predictable variation looks general across forms versus form-specific.

---

# 5. “MPC heterogeneity remains latent even with subjective information” — sharpen this result

The second pass found ALL OOS R² about .05 and almost no incremental value from subjective variables.

Formalize this in a way that can support a general behavioural claim.

## 5.1 Fixed nested comparisons

Using identical folds:

- T only;
- T + Objective/Needs (O);
- T + Subjective Economic (S);
- T + Broader Attitudes (A);
- T + O + S;
- T + O + A;
- T + ALL.

For each, report distribution across repeated folds of:
- R²;
- RMSE;
- MAE.

Do not report only mean R².

Add:
- paired fold-by-fold differences O vs O+S;
- O vs O+A;
- O vs ALL;
- bootstrap or paired permutation CI for incremental OOS R².

Question:

> Can we statistically rule out a meaningful predictive contribution from subjective information?

## 5.2 Practical-equivalence benchmark

Predefine a small but meaningful incremental OOS R² benchmark, e.g.:

- +0.01;
- +0.02.

Report whether the CI for (R^2(O+S)-R^2(O)) excludes these thresholds.

This turns “not much improvement” into a more interpretable null.

## 5.3 Noise ceiling / outcome coarsening sensitivity

Because the outcome is six-category stated MPC, attempt to quantify how much low predictability could mechanically reflect coarse/noisy measurement.

Without inventing reliability, do:

- predict `outcome_ord` with ordinal models;
- predict threshold outcomes;
- predict midpoint and alternative-top coding;
- compare whether low predictability is robust across outcome representations.

If all are low, say low predictability is not solely an artifact of one midpoint mapping.

Do **not** claim measurement-error correction without repeated measurements.

---

# 6. Psychometric / latent-dimension exploration of subjective states

For a Nature Human Behaviour / Nature Communications framing, the subjective block should not be represented only as dozens of separate questionnaire items.

Explore whether interpretable latent psychological/economic dimensions add predictive information.

This must be done carefully and honestly.

## 6.1 Split domains before dimension reduction

Never run one giant PCA across all survey items.

Separate:

### Subjective economic state
- social protection;
- emergency liquidity;
- sense of gain;
- effort / mobility;
- pressure;
- personal future;
- macro/job/price/welfare expectations;
- subjective SES / mobility.

### Social confidence / institutional-social environment
- safety;
- fairness;
- government trust;
- generalized trust;
- voice;
- social order;
- vitality;
- social support.

### General well-being / optimism
- life satisfaction;
- personal / societal outlook variables if conceptually appropriate.

Document exact item membership before looking at outcome associations.

## 6.2 Factor extraction

Within each domain compare:

- simple standardized mean index;
- PCA;
- exploratory factor analysis if dependencies support it.

Use parallel analysis / scree plot where possible.

Report:
- factor loadings;
- variance explained;
- internal consistency where meaningful;
- interpretability.

Do not force a factor if items do not form one.

## 6.3 Validation discipline

To avoid full-sample psychometric overfitting:

- estimate loadings in training folds or a discovery half;
- score factors in held-out data using fixed loadings;
- evaluate incremental prediction / HTE in held-out data.

Test whether latent factors improve:
- MPC level prediction;
- Food−Cash HTE prediction;
- Medical−Cash HTE prediction.

If they do not, this strengthens the “rich subjective information adds little” conclusion.

---

# 7. Baseline-profile / behavioural-phenotype exploration

This is optional but potentially relevant for a broader human-behaviour paper.

Cluster respondents **only on pre-treatment variables**, never on the outcome or treatment response.

Use:
- k-means / Gaussian mixture on standardized low-dimensional objective + latent subjective factors;
- or hierarchical clustering if stable.

Choose small K (2–6), using:
- silhouette / BIC where appropriate;
- cluster stability under resampling;
- interpretability.

Then, in held-out data only, estimate randomized:
- Cash / Food / Medical means by profile;
- Food−Cash;
- Medical−Cash;
- Medical−Food.

The objective is not to discover “significant clusters.”

Question:

> Are there stable baseline behavioural/economic profiles whose response to money form differs meaningfully?

If clusters are unstable or treatment contrasts do not validate, report the null and stop.

Do not call clusters psychological “types” unless strongly stable.

---

# 8. Amount as a behavioural context moderator

Previous results suggest Medical−Food HTE is strongest at 200 yuan.

Investigate whether amount changes:

1. mean stated-MPC ranking;
2. observable predictability;
3. fungibility predictability.

For each amount separately report:
- OOS MPC prediction;
- OOS Medical−Cash CATE calibration;
- OOS Food−Cash CATE calibration, if sample precision allows.

Then test whether prediction/calibration differs by amount.

Do not overfit nine-cell small samples.

Use simple models and broad uncertainty intervals.

Conceptual question:

> Does the *meaning* of transfer form become more or less important as the stake changes?

---

# 9. Formal food vs medical contrast: “generic labeling” versus “account relevance”

Do not assert mechanisms, but examine an empirical distinction.

Food voucher:
- spending category is common and recurring;
- many respondents are clearly inframarginal;
- average Food−Cash gap remains;
- observed subgroup heterogeneity appears weak.

Medical account:
- category is state-contingent / uncertain;
- account usability is more person-specific;
- Medical−Cash heterogeneity is more predictable;
- prior medical expenditure predicts relative response.

Test this contrast more directly.

## 9.1 Predictability comparison

Compare honest CATE-model calibration for:
- Food−Cash;
- Medical−Cash.

Use bootstrap/permutation to test whether Medical−Cash calibration / top-bottom separation exceeds Food−Cash.

Do not merely compare one significant and one insignificant result.

## 9.2 Observable-domain contribution to CATE

For each contrast run CATE models with:
- O only;
- O+needs;
- S only;
- A only;
- ALL.

Use identical folds.

Report:
- calibration;
- top-bottom separation;
- change when adding subjective information.

This directly asks whether Medical fungibility is structured by economic relevance rather than broad social mindset.

## 9.3 Medical-need gradient

For past medical spending:
- factor/dummy plot;
- trend plot;
- amount-specific plot;
- joint controls;
- raw/adult/clean.

If available in questionnaire/data, inspect any variables that proxy:
- age;
- household size;
- children;
- perceived protection;
- income.

Do not manufacture a “medical need index” unless justified.

---

# 10. Targeting transfer form: do the exercise, even if the answer is null

The previous evidence suggests Medical remains below Cash even in high predicted-CATE groups.

Do a formal policy-value exercise to establish whether predictable HTE creates useful treatment personalization.

## 10.1 Candidate policies

Compare:

### Uniform
- all Cash;
- all Food;
- all Medical.

### Simple interpretable policy
Depth-1 / depth-2 policy tree using baseline X.

### ML policy
Choose:
[
hat d(X)=argmax_t hatmu_t(X)
]
using cross-fitted outcome models.

## 10.2 Honest policy evaluation

Use only held-out / OOF policy assignments.

Estimate policy value with:
- inverse propensity weighting;
- doubly robust policy value if implemented correctly;
- known randomization probabilities.

Report:
- mean stated-MPC policy value;
- SE / bootstrap CI;
- difference from best uniform policy (likely all Cash);
- fraction assigned to each form.

The key estimand:

[
V(hat d)-max{V(Cash),V(Food),V(Medical)}.
]

If CI includes zero or policy assigns nearly everyone Cash, say:

> predictable HTE does not translate into meaningful targeting gains.

That is scientifically useful.

Do not optimize policy on the same outcomes used to evaluate it.

---

# 11. Survey-response quality and response-style robustness

This matters especially for a human-behaviour journal because the outcome is hypothetical and the sample is an online platform sample.

We lack duration, IP/device, and formal attention checks. State this clearly.

Still, construct transparent response-style diagnostics from pre-treatment 0–10 items:

- complete straightlining (already used);
- near-straightlining / very low within-person variance;
- extreme-response share (0 or 10);
- midpoint-response share (5);
- entropy / number of unique scale responses;
- internal inconsistency only where conceptually defensible (do not invent reverse-coded tests).

Do **not** use these as primary exclusions.

Test whether:
- average transfer-form effects;
- Food−Cash inframarginal gap;
- Medical−Cash HTE calibration;
- Medical−Food income/medical-spending moderation

are robust across:
- raw;
- existing clean;
- progressively stricter response-style screens.

Report how sample composition changes under screens.

If stronger screens change results materially, flag response-quality sensitivity.

---

# 12. Representativeness / generalizability diagnostics

The sample is young and highly educated.

For a Nature-style paper this must be treated explicitly.

## 12.1 Internal sample composition

Provide:
- age;
- sex;
- education;
- hukou;
- employment;
- city tier;
- province;
- income category.

## 12.2 External benchmarks if authoritative margins are available

If the work environment can reliably obtain authoritative Chinese population margins from:
- National Bureau of Statistics;
- 2020 Population Census;
- another clearly documented official source,

compare sample margins for:
- sex;
- age bands;
- education;
- urban/rural or hukou where compatible;
- broad geography.

Do not use unofficial web summaries.

If authoritative margins cannot be obtained reliably, document that and do not improvise.

## 12.3 Reweighting sensitivity

If compatible population margins are available, construct transparent post-stratification / raking weights.

Re-estimate only:
- average Cash/Food/Medical effects;
- main pooled Food−Cash / Medical−Cash contrasts;
- core level-predictability facts if feasible.

Do not claim weighting makes the sample nationally representative.

Treat as sensitivity to observed demographic imbalance.

---

# 13. Nature-style generality check

Create a table that separates:

## Economics-specific objects
- stated MPC;
- cash / voucher / medical transfer;
- policy targeting.

## General human-behaviour objects
- context dependence of responses to nominally equivalent resources;
- stability versus context-specificity of individual differences;
- predictability of behavioural heterogeneity from objective versus subjective states;
- limits of self-reported psychological variables for predicting responses;
- whether “who responds” generalizes across contexts.

For each possible general claim, write:

- evidence supporting it;
- evidence against it;
- measurement limitation;
- whether it is truly broader than this transfer setting.

Do not simply rename “MPC” as “human behaviour.”

---

# 14. Nature Human Behaviour / Nature Communications positioning audit

Create a short evidence-based positioning section.

Evaluate, separately, whether the current dataset plausibly supports:

### Position A — Economics-style
“Rich observables explain little MPC heterogeneity; transfer form adds a fungibility dimension.”

### Position B — Human-behaviour style
“Individual behavioural responses to nominally equivalent resources are weakly trait-predictable and strongly context-dependent.”

### Position C — Policy-design style
“Observable traits provide limited value for targeting recipients, and only limited / form-specific value for tailoring the design of transfers.”

For each position give:

- strongest empirical fact;
- weakest link;
- whether evidence is causal / predictive / descriptive;
- whether stated outcome is fatal, serious, or manageable;
- whether single-study / single-country design is a serious barrier;
- what result would make the positioning substantially stronger.

Do not rank journals by prestige; assess fit and evidentiary demands.

---

# 15. Existing Nature-style evidence that should inform interpretation

Use these as conceptual checks in the final memo, not as data sources:

1. Nature Human Behaviour explicitly covers economic behaviour, decision-making, public policy, socioeconomic influences, interventions, and individual/group variation.
2. Nature Human Behaviour evaluates whether the question is broad enough to interest human-behaviour researchers beyond a narrow specialist audience.
3. Recent Nature Human Behaviour work shows that survey intentions/predictions may fail to transfer to real-world behaviour. This is directly relevant to stated MPC and must be discussed.
4. Nature Human Behaviour has published randomized cash-transfer work with realized expenditures and long-term outcomes; our stated single-survey outcome is therefore an evidentiary disadvantage, not something to hide.
5. Nature Communications explicitly welcomes important advances in human behaviour/social science and strongly encourages preregistration; this analysis is exploratory/post hoc, which must be transparently stated.

Do not claim these journals would accept the paper.

---

# 16. Required figures

Produce no more than 8 high-value candidate main-text figures.

At minimum:

### Figure 1 — Predictability of stated MPC
OOS R² by feature set:
- T;
- O;
- S;
- A;
- O+S;
- ALL.

Include uncertainty across folds.

### Figure 2 — Form-specific predictability
OOS R² separately for Cash / Food / Medical.

### Figure 3 — Cross-form stability
Matrix / plot of predictor-vector similarity or cross-form prediction transferability.

### Figure 4 — Honest fungibility heterogeneity
OOF CATE quintiles for:
- Food−Cash;
- Medical−Cash.

### Figure 5 — Medical need / socioeconomic moderation
Simple binned treatment-effect plots for the strongest robust variables.

### Figure 6 — Shared vs form-specific predictable variation
A clear decomposition or bar plot.

### Figure 7 — Policy value
Uniform policies vs simple policy tree vs ML personalized form, with CI.

### Figure 8 — Optional
Psychometric latent-factor incremental predictive value OR response-quality robustness, whichever is more informative.

Avoid coefficient forests with dozens of variables as main figures.

---

# 17. Deliverables

Create:

- `FINAL_EXPLORATION_AUDIT.md`
- `FINAL_EXPLORATION_RESULTS.md`
- `analysis/final_exploration.py`
- `tables/final_*.csv`
- `figures/final_*.png`

Do not overwrite earlier formal outputs.

## 17.1 FINAL_EXPLORATION_AUDIT.md

Must document:
- every new estimand;
- data transformations;
- psychometric factor construction;
- CV / cross-fitting;
- DR/R learner implementation;
- policy evaluation;
- response-quality screens;
- population benchmarks if used;
- any failed or unavailable dependency;
- protocol deviations.

## 17.2 FINAL_EXPLORATION_RESULTS.md

Organize by these questions:

### Q1. How predictable is stated MPC with rich objective and subjective information?

### Q2. Is predictability stable across Cash, Food, and Medical forms?

### Q3. Does transfer form reorder who is predicted to respond strongly?

### Q4. Is Food non-fungibility structurally different from Medical non-fungibility?

### Q5. Do latent subjective dimensions add anything beyond objective conditions?

### Q6. Does predictable HTE create useful transfer-form targeting gains?

### Q7. Are results robust to survey response-style concerns and sample composition?

### Q8. Which framing is best supported: economics, general human behaviour, or policy design?

---

# 18. Final synthesis — strict format

End with exactly these sections.

## A. Five strongest facts
Maximum five. Each must include:
- effect / predictive statistic;
- uncertainty;
- method;
- sample;
- robustness.

## B. Five strongest nulls
Especially:
- subjective incremental prediction;
- Food−Cash HTE predictability;
- targeting gains if null.

## C. Stable-trait vs context-specific verdict
Answer:
- Is there evidence for a general “high stated-MPC person” observable type?
- Are predictor rankings stable across forms?
- Does Medical create more reordering than Food?

## D. Economics-paper interpretation
One paragraph only.

## E. Nature-style interpretation
One paragraph only.

## F. Why the Nature-style interpretation may fail
Explicitly list:
- hypothetical stated outcome;
- single online Chinese sample;
- lack of independent replication;
- lack of preregistration;
- no actual expenditure validation;
- any weak/unstable ML result.

## G. Best single paper question supported by the data
One sentence.

Do not write an abstract or title yet.

---

# 19. Evidence threshold

A Nature-style claim should not be built from:
- one significant interaction;
- feature importance;
- a single ML learner;
- a post hoc subgroup;
- a weakly calibrated CATE.

Prefer claims supported by at least two of:
- randomized average contrast;
- transparent linear / categorical HTE;
- cross-fitted ML;
- held-out calibration;
- response-quality robustness;
- cross-form generalization;
- psychometric-factor replication;
- weighting / composition sensitivity.

The goal is to discover whether the existing data contain a **general behavioural fact**, not to cosmetically rebrand an economics survey paper.
