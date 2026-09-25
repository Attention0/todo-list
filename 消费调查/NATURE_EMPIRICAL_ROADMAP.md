# 消费调查项目 — Nature-Series Empirical Roadmap

## 0. Purpose

This document is a **paper-development empirical roadmap**, not another open-ended heterogeneity fishing exercise.

The target is a paper that could plausibly be framed for **Nature Human Behaviour** or **Nature Communications**, while retaining a credible economics fallback. The empirical standard must be higher than “many regressions are significant.” The paper needs a small number of broad claims, each supported by multiple complementary forms of evidence, honest out-of-sample validation, transparent limitations, and a reproducible analysis pipeline.

Current evidence is already suggestive of a broad question:

> **Are individual differences in marginal spending responses stable across transfer contexts, or does the form in which money is delivered reshape who responds?**

A second linked question is:

> **Do rich subjective economic and psychological states meaningfully improve our ability to predict these responses?**

The paper should not be built around a narrow “cash vs voucher vs medical account” comparison alone. The three randomized forms are the experimental contexts used to study a more general issue: **stable individual differences versus context-specific behavioural response mappings**.

---

# 1. Editorial bar to design around

## Nature Human Behaviour

Nature Human Behaviour explicitly evaluates:

- whether the question is broad or narrow;
- whether the research question is important within and beyond one discipline;
- whether the work is substantive rather than preliminary;
- conceptual novelty;
- methodological novelty;
- societal / policy advance;
- advance in evidence;
- sample size and sampling design;
- preregistration.

Therefore the manuscript cannot rely on “we have N=5,497 and many covariates.” It needs a conceptually broad result and an evidence package that makes the result difficult to dismiss as:
- one survey artefact;
- one coding choice;
- one ML model;
- one subgroup;
- one noisy stated outcome.

## Nature Communications

Nature Communications asks for an important advance for the relevant research community and emphasizes:
- transparent reporting;
- statistical reporting including null results;
- code reproducibility;
- disclosure of preregistration / lack thereof;
- behavioural and social sciences reporting standards.

The project is exploratory/post hoc. Do not conceal this. Instead, lock the analysis pipeline now and sharply distinguish:
- analyses already explored;
- confirmatory-style locked re-estimation / robustness;
- genuinely exploratory extensions.

---

# 2. Central paper architecture

The Nature-style paper should ideally have **four empirical pillars**.

## Pillar 1 — Low predictability of stated MPC despite unusually rich information

Question:

> How much of individual heterogeneity in stated marginal spending responses can be predicted from observable characteristics?

Current benchmark evidence:
- treatment-only OOS R² is near zero;
- objective/needs variables raise OOS R² to roughly 4–5%;
- subjective economic states add only a few tenths of a percentage point to a few thousandths in R²;
- the full feature set achieves only about 5% OOS R².

The broad claim is **not**:
> 95% of MPC heterogeneity is preferences.

Allowed claim:

> Even with rich objective and subjective baseline information, most variation in stated marginal spending responses remains unexplained / latent-or-noise.

This is the direct bridge to Lewis, Melcangi & Pilossoph (ReStud 2026), but our measurement object differs.

---

## Pillar 2 — Observable “high-responder” rankings generalize poorly across transfer forms

Question:

> If a person is predicted to have a high spending response under Cash, are they also predicted to respond highly under Food or Medical?

Current evidence:
- cross-form rank correlations are low;
- Cash–Food is more aligned than Cash–Medical;
- coefficient-vector similarity is materially higher for Cash–Food than Cash–Medical.

This is potentially the broad human-behaviour contribution.

The broad claim must remain careful:

> Observable response rankings have limited portability across resource-delivery contexts.

Do **not** write:
> human preferences are unstable.

Why:
- one outcome per person;
- coarse six-category stated response;
- measurement error attenuates cross-form stability;
- no repeated-measures reliability estimate.

---

## Pillar 3 — Context-specific heterogeneity is asymmetric

Question:

> Is all transfer-form non-fungibility equally predictable?

Current evidence:
- Food−Cash has an average gap but flexible HTE does not validate;
- Medical−Cash shows reproducible OOF calibration in several cross-fitted learners;
- Medical−Cash HTE is especially visible at RMB 1,000;
- subjective-only information contributes little; objective/needs variables contain more predictive structure.

Potential general statement:

> Context dependence itself differs across contexts: some resource labels/restrictions generate broadly shared shifts, while others interact more strongly with recipient characteristics.

This is more general than “medical accounts are different.”

But the paper must show the asymmetry formally, not by comparing “significant” vs “not significant.”

---

## Pillar 4 — Predictable heterogeneity is not necessarily actionable

Question:

> Does predictable HTE allow useful personalization of transfer form?

Current evidence:
- all-Cash has the highest stated-MPC policy value;
- depth-2 policy tree assigns Cash to everyone;
- ML argmax personalization does not beat all-Cash.

Potential general point:

> Predictable treatment-effect heterogeneity need not imply useful individualized policy assignment when one treatment broadly dominates the outcome objective.

This is a valuable null and should be reported, not hidden.

---

# 3. Required empirical modules

The final paper should contain the following modules. Each module must be implemented in a locked, reproducible script and produce both main-text and supplement-ready outputs.

---

# Module A. Experimental design and measurement integrity

## A1. Randomization integrity

Reproduce:
- N=5,497;
- exact one-of-nine treatment assignment;
- cell counts;
- omnibus treatment-cell balance;
- key baseline balance table;
- assignment reconstruction cross-check.

Main text should show a compact design diagram:
[
3 transfer forms 	imes 3 amounts
]

Forms:
- Cash;
- Food/daily-needs voucher;
- Medical account.

Amounts:
- RMB 200;
- RMB 1,000;
- RMB 5,000.

## A2. Outcome measurement

Show the six stated incremental-consumption response categories clearly.

Explicitly distinguish:
- ordinal stated outcome;
- midpoint approximation;
- threshold outcomes.

Primary:
- original 1–6 category.

Secondary:
- midpoint stated MPC;
- alternative top coding;
- any-spend / 10%+ / 25%+ / 50%+.

Do not let the paper depend on midpoint mapping.

## A3. Distributional treatment effects

Before any ML, report full outcome distributions by:
- transfer form pooled across amount;
- amount;
- 3×3 cells.

Use:
- cumulative probability plots;
- category-share plots;
- stochastic-dominance style comparisons if appropriate;
- ordered-logit/probit as summaries.

The paper needs to show that mean effects are not driven by one arbitrary coding.

---

# Module B. “How predictable is stated MPC?”

This should be the cleanest bridge to the ReStud latent-MPC literature.

## B1. Feature blocks

Lock feature sets:

### T
Treatment design only.

### O
Objective / quasi-objective economics:
- age;
- sex;
- education;
- income;
- hukou;
- work status;
- work-unit type;
- housing;
- children;
- household size;
- food spending;
- medical spending;
- prior subsidy;
- city tier.

### S
Subjective economic states:
- emergency liquidity;
- perceived social protection;
- pressure;
- subjective SES;
- expected mobility;
- personal future;
- economy / employment / prices / welfare expectations;
- effort / mobility beliefs.

### A
Broader attitudes:
- trust;
- fairness;
- safety;
- social support;
- voice;
- order;
- vitality;
- life satisfaction / societal outlook where not already allocated.

### O+S
### O+A
### ALL

Do not redefine these blocks after seeing results.

## B2. Prediction models

Use:
- OLS / ridge;
- elastic net;
- random forest;
- histogram gradient boosting;
- optionally one additional well-supported boosting implementation if environment is stable.

Same repeated folds across all feature sets.

All preprocessing inside training folds.

Report:
- OOS R²;
- RMSE;
- MAE;
- fold distribution;
- paired differences between feature sets.

## B3. Practical-equivalence tests

For:
[
R^2(O+S)-R^2(O)
]

and:
[
R^2(ALL)-R^2(O)
]

report paired bootstrap / permutation CI across identical folds.

Predeclare practical improvement thresholds:
- +0.01 OOS R²;
- +0.02 OOS R².

If upper CI < .01, explicitly state:
> Rich subjective information does not improve predictive accuracy by even one percentage point of outcome variance under this design.

This is stronger than “not significant.”

## B4. Outcome-representation robustness

Repeat the predictability result using:
- ordinal score;
- midpoint MPC;
- alternative top coding;
- binary thresholds.

If predictability remains low across representations, the low R² result is not purely a midpoint-coding artefact.

## B5. Psychometric subjective factors

Retain the current latent-domain approach but formalize it.

Domains:
- subjective economic state;
- social confidence;
- wellbeing / optimism.

Use:
- discovery-half or fold-specific loadings;
- PCA / factor solution fixed before outcome prediction;
- alpha / internal-consistency diagnostics;
- held-out scoring.

Key test:
[
O ightarrow O + latent subjective dimensions
]

If held-out gain remains approximately zero, this is a substantive result:

> Coherent self-reported subjective states provide little incremental prediction of stated marginal spending responses.

Do not interpret this as “psychology does not matter.”

---

# Module C. Stable trait versus context-specific response

This module should be the conceptual center of the Nature-style paper.

## C1. Form-specific outcome prediction

Fit identical models separately for:
- Cash;
- Food;
- Medical.

Report OOS R² with uncertainty for each.

Question:
> Is one context intrinsically more predictable than another?

## C2. Cross-form prediction transfer

For each source→target pair:
- train on source form;
- evaluate prediction ranking in target form;
- do not refit the X→Y mapping;
- allow only transparent mean recentering for R² comparison.

Report:
- Spearman rank correlation;
- recentered R²;
- calibration slope.

Pairs:
- Cash→Food;
- Cash→Medical;
- Food→Cash;
- Food→Medical;
- Medical→Cash;
- Medical→Food.

## C3. Formal comparison of cross-form portability

Do not merely report that .19 > .11.

Bootstrap the **difference**:

[
ho(Cash,Food)-ho(Cash,Medical)
]

and:
[
ho(Cash,Food)-ho(Food,Medical).
]

Also compare:
- coefficient-vector correlation;
- cosine similarity;
- sign agreement.

If Cash–Food is consistently more aligned than Cash–Medical across methods, this supports a “Medical reshapes mapping more strongly” interpretation.

## C4. Noise-aware interpretation

Because low reliability can attenuate cross-form correlation, add a quantitative sensitivity exercise.

We do not have test–retest reliability, so do not “correct” correlations as fact.

Instead:
- assume plausible outcome reliabilities, e.g. 0.4, 0.6, 0.8;
- show the implied attenuation-corrected correlation under classical independent measurement error;
- label the exercise explicitly as sensitivity, not an estimate.

Goal:
> determine whether even generous reliability assumptions would still imply only moderate cross-context stability.

If corrected correlations could easily become high, the Nature-style trait-vs-context claim must be weakened.

This sensitivity is important.

## C5. Shared versus form-specific predictable signal

Using cross-fitted:
[
hatmu_C(X),hatmu_F(X),hatmu_M(X)
]

decompose:
- shared predicted component;
- form-specific predicted deviations.

Report variance ratios relative to observed outcome variance.

Interpretation:
- predictable variation itself is small;
- within that small predictable part, how much is shared versus context-specific?

---

# Module D. Fungibility heterogeneity

## D1. Average randomized contrasts

Report:
- Food−Cash;
- Medical−Cash;
- Medical−Food;
- pooled and by amount.

Primary on ordinal outcome; midpoint for interpretation.

## D2. Correct conceptual definition

Fungibility heterogeneity is:

[
	au_F(X)=E[Y(Food)-Y(Cash)|X]
]

[
	au_M(X)=E[Y(Medical)-Y(Cash)|X]
]

not an observed individual-level gap.

## D3. Transparent HTE

Run theory-guided interaction models for:
- income;
- education;
- food spending;
- medical spending;
- emergency liquidity;
- subjective SES;
- household size;
- children;
- age;
- social protection.

Use:
- continuous trend where defensible;
- categorical omnibus;
- amount-saturated interactions;
- family FDR;
- randomization inference for final highlighted variables.

## D4. Cross-fitted HTE

Use:
- T-learner;
- fully cross-fitted DR learner;
- standard R-learner;
- causal forest only if stable package available.

Evaluation:
- calibration slope;
- CATE quintiles;
- top−bottom contrast;
- confidence intervals;
- learner agreement.

Main evidence is held-out treatment-effect gradient, not feature importance.

## D5. Formal Food-vs-Medical asymmetry test

This is essential for a Nature-style claim.

Test whether predictability of Medical−Cash HTE exceeds Food−Cash HTE.

Possible statistics:
- difference in calibration slopes;
- difference in top−bottom treatment-effect separation;
- difference in cross-validated HTE loss / RATE-like metric.

Use:
- bootstrap preserving randomized treatment structure;
- permutation where feasible.

Do not infer asymmetry simply because one CI excludes zero and another does not.

## D6. Amount moderation

Current evidence suggests strongest Medical−Cash HTE around RMB 1,000.

Formally report:
- amount-specific calibration;
- uncertainty;
- interaction / heterogeneity test across amounts.

Treat this as a key qualifier.

Do not claim general Medical heterogeneity if 200 and 5,000 are null.

---

# Module E. Food as a falsification / null case

Food is scientifically valuable even if its HTE is null.

## E1. Average Food−Cash effect

Reproduce across:
- Raw R;
- Adult A;
- Clean C;
- response-quality screens.

## E2. Inframarginal subsamples

Keep:
- strict inframarginal;
- very-strict inframarginal.

Show:
- average Food−Cash gap;
- confidence interval;
- power / precision for HTE.

## E3. HTE null precision

For prespecified predictors report:
- effect;
- CI;
- BH q;
- minimum heterogeneity magnitude ruled out by CI.

This allows a disciplined statement:

> We find little evidence that the Food−Cash gap is structured by observed household characteristics, although smaller heterogeneity remains possible.

## E4. Response-quality sensitivity

Because the Food average gap weakens under the strict Q2 response-style screen, do not headline Food as equally robust to Medical.

Report this transparently.

---

# Module F. Medical as the context-specific case

## F1. Average Medical−Cash effect

Show robustness across:
- R/A/C;
- response-quality screens;
- outcome codings;
- FE / SE variants.

## F2. Strongest moderators

Current candidates:
- income;
- education;
- prior medical spending.

For each:
- raw binned plot;
- linear trend;
- categorical specification;
- amount-specific pattern;
- prespecified controls;
- province FE;
- HC1 / HC3;
- geography-cluster sensitivity;
- randomization inference;
- Raw / Adult / Clean / quality-screen robustness.

Do not call past medical spending “bindingness.”

Use:
> prior medical need / exposure proxy.

## F3. Joint model

Estimate a focused joint moderation model containing:
- income;
- education;
- medical spending.

Report whether each remains informative conditional on the others.

## F4. Interpretation boundary

Data may be consistent with:
- category relevance;
- usability;
- perceived liquidity;
- state-contingent need.

Data do not identify which mechanism is causal.

---

# Module G. Policy-learning null

This should be a compact but important section.

## G1. Uniform policies

Evaluate:
- all Cash;
- all Food;
- all Medical.

## G2. Personalized policies

Evaluate honestly:
- shallow policy tree;
- ML argmax policy from OOF (hatmu_t(X)).

## G3. Policy value

Use:
- known randomization probabilities;
- IPW;
- DR policy value if correctly cross-fitted.

Primary statistic:
[
V(hat d)-V(Cash)
]

if Cash is best uniform policy.

Report:
- CI;
- allocation shares;
- whether personalized rule meaningfully differs from all Cash.

If personalization fails:
> predictable HTE does not imply actionable personalization.

Do not spin a negative policy value into a positive story.

---

# Module H. Survey-response validity

This is mandatory for a Nature-family submission.

## H1. Response-style diagnostics

Report:
- complete straightlining;
- near-straightlining;
- within-person scale variance;
- number of unique responses;
- extreme response share;
- midpoint share;
- entropy.

## H2. Sensitivity screens

Use:
- R;
- C;
- Q1;
- Q2.

Report composition changes.

Re-estimate:
- average Food−Cash;
- Medical−Cash;
- main Medical HTE;
- predictability.

Do not define the screen after looking at treatment effects.

## H3. Common-method concern

Both subjective predictors and stated MPC are self-reports.

If subjective variables still add little predictive value, common-method covariance cannot explain a positive result—but it may complicate null interpretation.

Discuss explicitly.

## H4. Hypothetical-bias limitation

The paper must say clearly:
- outcome is stated;
- no actual expenditure;
- no incentive-compatible consumption decision;
- no transaction verification.

Do not imply behavioral realization.

---

# Module I. External validity and sample composition

## I1. Internal composition

Report:
- age;
- gender;
- education;
- employment;
- hukou;
- income;
- city tier;
- province.

## I2. Official benchmark comparison

Use only official Chinese population benchmarks where definitions are compatible.

Current comparison suggests:
- sex difference modest;
- age difference large;
- education difference very large.

Do not rake when sampling frames / variable definitions are incompatible.

## I3. Heterogeneity of core findings by broad demographic strata

As descriptive robustness only:
- younger vs older;
- higher vs lower education;
- urban/non-agricultural vs agricultural hukou;
- high vs low city tier.

Do not create a new fishing exercise.

Question:
> Are headline randomized mean effects directionally similar across broad sample segments?

---

# Module J. Generality beyond economics terminology

The manuscript needs to translate the core result for a broad audience.

Economics object:
- stated MPC.

Broader behavioural object:
- marginal response to a windfall resource.

Economics object:
- fungibility.

Broader behavioural object:
- whether nominally equivalent resources elicit equivalent behavioural responses when delivered under different labels/restrictions.

Economics object:
- HTE.

Broader behavioural object:
- whether observable individual differences are stable across contexts.

The empirical paper should always retain precise economic estimands in Methods/Results, even if Introduction uses broader language.

---

# 4. Main-text result package

A Nature-style manuscript should aim for **5–6 main figures**, not dozens of coefficient tables.

## Figure 1 — Experimental design + outcome distribution

Panel A:
3×3 randomized design.

Panel B:
full six-category outcome distribution by form.

Panel C:
average form effects with CIs.

Purpose:
establish the experiment and the basic behavioural phenomenon.

---

## Figure 2 — Rich information predicts little stated MPC

Plot OOS R² for:
- T;
- O;
- S;
- A;
- O+S;
- O+A;
- ALL.

Show fold uncertainty.

Add inset:
paired incremental OOS R² of S/A beyond O.

Purpose:
connect to latent-MPC literature and establish the “rich information still explains little” result.

---

## Figure 3 — Response rankings transfer poorly across forms

Panel A:
cross-form prediction Spearman matrix.

Panel B:
predictor-vector similarity:
- Cash–Food;
- Cash–Medical;
- Food–Medical.

Panel C:
shared versus form-specific predictable variance.

Purpose:
establish stable-trait versus context-specific mapping.

---

## Figure 4 — Food and Medical differ in HTE predictability

Panel A:
Food−Cash OOF CATE quintiles.

Panel B:
Medical−Cash OOF CATE quintiles.

Panel C:
formal difference in calibration / top-bottom separation.

Purpose:
show that context-specific heterogeneity is asymmetric.

---

## Figure 5 — Medical context and transfer size

Panel A:
amount-specific Medical−Cash HTE calibration.

Panel B:
selected transparent moderators:
- income;
- medical spending;
- possibly education if robust.

Purpose:
show where the context-specific heterogeneity arises and qualify the result.

---

## Figure 6 — Predictable heterogeneity is not actionable personalization

Plot policy value for:
- all Cash;
- all Food;
- all Medical;
- policy tree;
- ML argmax.

Purpose:
show that HTE predictability does not automatically imply policy gain.

---

# 5. Supplementary / Extended Data package

The supplement should include:

1. full questionnaire variable map;
2. randomization balance;
3. all 3×3 cell distributions;
4. ordinal / midpoint / threshold robustness;
5. categorical coding and omnibus tests;
6. HC1 / HC3 / clustered SE;
7. province / city-tier FE robustness;
8. randomization inference;
9. all ML hyperparameters;
10. exact outer / inner CV scheme;
11. psychometric factor loadings;
12. response-quality screens;
13. inframarginal food definitions;
14. amount-specific HTE;
15. external sample benchmarks;
16. policy-value estimator details;
17. reproducibility checklist.

No respondent-level data should be committed if confidentiality prevents it, but code and aggregate outputs must reproduce every reported statistic.

---

# 6. Evidence hierarchy for claims

Use the following hierarchy.

## Tier 1 — Main claim eligible

Requires at least:
- transparent estimand;
- randomized or clearly predictive interpretation;
- OOF / held-out validation where ML is involved;
- robustness across outcome coding;
- Raw / Clean consistency;
- not dependent on one learner;
- uncertainty reported;
- no contradiction under quality screens.

## Tier 2 — Supporting claim

May rely on:
- one robust interaction;
- one amount-specific pattern;
- suggestive factor / domain result;
- sample-sensitive effect.

Must be labeled supporting / exploratory.

## Tier 3 — Supplement only

Includes:
- isolated significance;
- feature importance;
- one learner only;
- one small subgroup;
- fragile attitude-only findings;
- poorly powered interactions.

Do not build Introduction claims from Tier 3.

---

# 7. “Go / No-go” conditions for the Nature-style framing

The Nature-style framing is strongest if all of the following survive locked re-analysis:

## Condition 1
ALL-feature OOS MPC prediction remains low, around current ~5% scale.

## Condition 2
Subjective information adds <1 percentage point OOS R² beyond objective/needs information, with CI ruling out +.01.

## Condition 3
Cross-form rank portability remains low.

## Condition 4
Cash–Food mapping is more similar than Cash–Medical under more than one metric.

## Condition 5
Medical−Cash HTE has positive OOF calibration under at least two principled learners.

## Condition 6
Food−Cash HTE does not positively validate.

## Condition 7
The Medical-vs-Food asymmetry is formally detectable rather than inferred from separate significance.

## Condition 8
Headline Medical findings survive reasonable response-quality screens.

If Conditions 3–7 fail, the broad “context reshapes individual differences” claim becomes weak and the paper should fall back toward economics.

---

# 8. Claims the current dataset probably cannot support

Do not attempt to make these central claims:

- “Preferences are unstable across contexts.”
- “Mental accounting causes the result.”
- “Medical need causally explains medical-account fungibility.”
- “The survey reveals true latent MPC types.”
- “Policy should assign different transfer forms to different people.”
- “Food vouchers reduce actual consumption.”
- “The findings represent the Chinese population.”
- “The results generalize cross-culturally.”
- “The results establish a universal law of human behaviour.”

These would require evidence not present in the current data.

---

# 9. Ideal additional evidence — unavailable with current fixed dataset

These should be discussed as what would most strengthen a Nature submission, but **do not treat them as required Work tasks if new data cannot be collected**.

Priority order:

## Ideal 1 — Independent replication
A second preregistered sample using the same 3×3 design.

## Ideal 2 — Behavioral validation
Actual transfer / incentivized spending choice or transaction-based outcome.

## Ideal 3 — Repeated measurement
Measure stated MPC or allocation choices more than once to estimate reliability and distinguish true instability from measurement noise.

## Ideal 4 — Direct mechanism measurement
Perceived liquidity, mental account assignment, perceived usefulness, willingness to exchange restricted funds for cash.

## Ideal 5 — Orthogonal manipulation
Separate:
- category restriction;
- expiration;
- liquidity;
- labeling.

The current Food treatment bundles category restriction and 6-month expiry.

If no new data are possible, these remain limitations and future-study proposals only.

---

# 10. Manuscript-result logic

The Results section should follow this logic:

### Result 1
Randomized transfer form changes stated marginal consumption response.

### Result 2
Rich observables predict only a small fraction of who responds strongly.

### Result 3
Adding coherent subjective economic/psychological information barely improves prediction.

### Result 4
Observable response rankings have limited portability across transfer forms.

### Result 5
Cash–Food mappings are more similar than Cash–Medical mappings.

### Result 6
Food−Cash HTE does not generalize out of sample, whereas Medical−Cash HTE partially does.

### Result 7
Medical HTE is context- and amount-specific, with strongest evidence at RMB 1,000.

### Result 8
Predictable Medical HTE does not create a profitable personalized-form policy relative to uniform Cash.

This sequence supports a broad conclusion:

> Observed individual differences in marginal spending are weakly predictable and only partly stable across resource-delivery contexts; rich subjective information does little to resolve this heterogeneity, and context-specific predictability does not automatically imply useful personalization.

Do not finalize this sentence until all formal comparisons are locked and reproduced.

---

# 11. Required next Work deliverable

Create a final locked analysis / manuscript-evidence package:

- `NATURE_EMPIRICAL_AUDIT.md`
- `NATURE_EMPIRICAL_RESULTS.md`
- `analysis/nature_empirical.py`
- `tables/nature_*.csv`
- `figures/nature_*.png`

This should **reuse** validated code from the previous formal/final scripts wherever possible rather than rewriting everything.

The purpose is not another fishing round. It is to:

1. lock definitions;
2. formally test the asymmetries that are currently only descriptive;
3. add the noise/reliability sensitivity;
4. harmonize all prediction / HTE folds;
5. produce publication-grade main figures;
6. separate main-claim evidence from supplement-only evidence.

---

# 12. Specific new analyses that are still missing and should be added now

These are the highest-priority missing pieces.

## 12.1 Formal difference in cross-form stability

Bootstrap:
[
ho_{Cash,Food}-ho_{Cash,Medical}
]

and:
[
ho_{Cash,Food}-ho_{Food,Medical}.
]

Do this for:
- Spearman transferability;
- coefficient-vector correlation.

## 12.2 Reliability / attenuation sensitivity

For assumed reliability levels:
- 0.4;
- 0.6;
- 0.8;

calculate the classical attenuation-corrected cross-form correlations.

Report whether the conclusion remains “low/moderate portability” under plausible values.

Label as sensitivity only.

## 12.3 Formal Food-vs-Medical HTE predictability contrast

Compare:
- calibration slopes;
- top−bottom separation.

Use bootstrap or permutation with fixed folds.

Question:
> Is Medical−Cash genuinely more predictable than Food−Cash?

## 12.4 Fold harmonization

All main ML comparisons should use exactly the same predeclared outer folds wherever mathematically possible.

Store fold IDs internally in the script; do not commit respondent-level fold assignments if privacy rules prohibit it.

## 12.5 Response-quality predictability

Re-estimate the core OOS prediction and Medical−Cash HTE under:
- R;
- C;
- Q1;
- Q2.

The Nature claim cannot rely on average effects only being quality-robust; the *predictability structure* should also be checked.

## 12.6 DR policy evaluation

Add a correctly cross-fitted doubly robust policy-value estimator as robustness to IPW.

If it agrees that personalization does not beat Cash, the null becomes much stronger.

## 12.7 Repeated-seed ML stability

Repeat RF/DR/R analyses over a small fixed seed grid, e.g. 10 seeds.

Report distribution of:
- calibration;
- top-bottom separation;
- policy value.

The claim should not depend on one random forest seed.

---

# 13. Work reporting format

## NATURE_EMPIRICAL_AUDIT.md

Document:
- locked claims;
- exact feature blocks;
- exact folds;
- all estimands;
- model hyperparameters;
- bootstraps/permutations;
- reliability sensitivity assumptions;
- response-quality definitions;
- deviations from this roadmap.

## NATURE_EMPIRICAL_RESULTS.md

Organize by claim, not method:

### Claim 1 — Stated MPC is weakly predictable even with rich information
### Claim 2 — Subjective states add little incremental predictive value
### Claim 3 — Response rankings have limited cross-form portability
### Claim 4 — Cash–Food is more portable than Cash–Medical
### Claim 5 — Medical−Cash HTE is more predictable than Food−Cash HTE
### Claim 6 — Medical HTE is amount-specific
### Claim 7 — Personalization does not improve stated-MPC policy value
### Claim 8 — Which claims survive response-quality restrictions?

For each:
- headline statistic;
- CI;
- method;
- sample;
- robustness;
- interpretation;
- limitation.

End with:

## A. Main-text eligible results
Maximum 8.

## B. Extended-data only results

## C. Results that should be dropped

## D. Nature-style claim that is actually supported

## E. Strongest alternative economics framing

## F. Single biggest unresolved threat to interpretation

---

# 14. Final standard

The project should only be framed as a Nature-style human-behaviour paper if the empirical evidence supports a statement broader than:

> Cash, food vouchers and medical accounts have different stated MPCs.

The desired broad result is closer to:

> **Observable individual differences in marginal responses to resources are weakly predictable and only partially portable across contexts; changing the form of money can reshape the mapping between personal characteristics and behavioural response, while rich subjective information provides surprisingly little additional predictive power.**

The empirical work must make clear which parts of this statement are directly supported, which are sensitivity-dependent, and which remain speculative because the outcome is hypothetical and measured only once.
