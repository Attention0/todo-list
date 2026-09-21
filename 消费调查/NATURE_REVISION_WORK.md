# NATURE_REVISION_WORK.md

## Purpose

This is a **targeted revision package**, not a new exploration round.

The locked Nature-series package already establishes the core story:

1. randomized transfer context changes **stated** marginal-consumption responses;
2. unusually rich person-level information predicts little of individual response variation out of sample;
3. subjective economic states add very little incremental predictive power beyond objective/needs information;
4. observed predictive mappings have limited portability across Cash, Food and Medical contexts;
5. Medical−Cash HTE is more predictably structured than Food−Cash HTE, but the Medical HTE result is quality-sensitive and amount-specific;
6. personalized transfer-form assignment does not beat uniform Cash for the stated-consumption objective.

The revision should answer three concrete reviewer-style questions without reopening the search for new stories:

- **Where does the predictive structure move across contexts?**
- **Could the low R² simply be an artifact of outcome measurement noise?**
- **Why does predictable HTE fail to generate personalization gains?**

Do not alter the core estimands or the locked results in `NATURE_EMPIRICAL_RESULTS.md`.

Primary inputs:
- `NATURE_EMPIRICAL_RESULTS.md`
- `NATURE_EMPIRICAL_AUDIT.md`
- `NATURE_EMPIRICAL_ROADMAP.md`
- `NATURE_FIGURE_BLUEPRINT.md`
- `analysis/nature_empirical.py`
- `analysis/final_exploration.py`
- `analysis/heterogeneity_formal.py`

Use the same cleaned variable definitions, outcome codings and respondent-level data preparation already frozen in the existing pipeline.

---

# A. Context-specific predictor map: where does the limited signal move?

## A1. Goal

The manuscript currently shows that predictive mappings differ across forms, but it does not show clearly **which observable domains account for those differences**.

The goal is descriptive/predictive, not causal. We want to learn whether the limited predictive signal is carried by different observable domains in Cash, Food and Medical contexts.

Do **not** interpret feature importance as a mechanism, attention weight or causal determinant.

## A2. Primary analysis: domain-level held-out importance

Construct a small, theory-guided set of predictor domains from the already locked variables. Prefer broad interpretable domains over dozens of single variables. At minimum include:

1. **Resources / socioeconomic position**
   - income
   - education
   - employment/work status
   - housing
   - subjective SES only if it belongs in a separately labelled subjective block; do not mix objective and subjective silently

2. **Liquidity / financial capacity**
   - Q7 emergency-liquidity measure and closely related prespecified variables

3. **Household needs / exposure**
   - household size
   - children
   - food expenditure
   - prior medical expenditure

4. **Expectations / future economic outlook**
   - own next-year condition
   - economy/jobs/prices/fairness/welfare expectations
   - expected SES change

5. **Subjective security / pressure**
   - social protection sufficiency
   - pressure and related economic vulnerability states

6. **Broader social attitudes / wellbeing**
   - trust
   - fairness
   - social support
   - life satisfaction
   - social order/vitality and related broad attitudes

If an exact variable belongs ambiguously to two domains, document the choice in the audit and keep the mapping fixed before estimation.

For each form separately (Cash, Food, Medical):

- fit the headline RF using the same common outcome and fold logic as the locked analysis;
- estimate **leave-one-domain-out held-out ΔR²**:
  [
  I_{d,c}=R^2_{ALL,c}-R^2_{ALL\setminus d,c}.
  ]
- use repeated common folds and repeated seeds so comparisons are not driven by one partition;
- report point estimates and uncertainty/stability summaries;
- negative ΔR² is allowed and should be shown, not truncated.

Primary figure:
- rows = predictor domains;
- columns = Cash / Food / Medical;
- cell or point estimate = held-out ΔR² from dropping that domain;
- same scale across forms.

Also compute pairwise context differences:
[
I_{d,Cash}-I_{d,Food},quad
I_{d,Cash}-I_{d,Medical},quad
I_{d,Food}-I_{d,Medical}.
]

Use a respondent/bootstrap or repeated-split procedure that reflects disjoint treatment arms. Do not rely on significance-vs-nonsignificance logic.

## A3. Secondary analysis: standardized ridge predictor maps

Using the existing common standardized encoding:

- fit form-specific ridge models on the same outcome;
- export standardized coefficient vectors for Cash, Food, Medical;
- report bootstrap distributions of coefficient differences across contexts;
- create an Extended Data heatmap / coefficient plot.

For visualization, do **not** select variables separately within each form. Use either:
- all interpretable raw predictors grouped by the fixed domains; or
- a fixed display subset chosen by pooled, treatment-blind criteria and documented before looking at form-specific signs.

The figure should make clear that coefficients are predictive associations, not causal mechanisms.

## A4. Optional secondary diagnostic: permutation importance

If computationally stable, add out-of-fold permutation importance for RF within each form.

Requirements:
- repeat across at least 10 fixed seeds;
- report rank stability;
- aggregate correlated variables by domain when possible;
- use only as a secondary diagnostic / Extended Data table.

**Do not make SHAP a required or headline analysis.**
SHAP may be generated only if already available and stable, but it should not be treated as causal or as the primary evidence for context-specific structure.

## A5. Interpretation gate

Only strengthen the narrative if at least one broad domain shows a stable, substantively interpretable cross-context difference under more than one predictive representation (e.g. domain-drop RF plus ridge map).

If single-feature rankings are unstable or methods disagree, the manuscript should retain the aggregate portability result and say that the data do not localize the difference cleanly.

---

# B. Measurement-error sensitivity for low predictability

## B1. Goal

Address the concern that observed ALL-model R² ≈ 0.048 could be low simply because the six-category stated outcome is noisy/coarse.

The survey has **no repeated outcome**, so there is no identified empirical test-retest reliability.

Do not infer outcome reliability from Cronbach's alpha of subjective predictors. Predictor internal consistency and outcome reliability are different objects.

## B2. Classical-error sensitivity

Under a clearly labelled heuristic model:

[
Y=Y^*+\epsilon,qquad
Reliability(Y)=r_Y,
]

with classical outcome error independent of predictors and the latent response, use:

[
R^2_{latent}approx R^2_{observed}/r_Y.
]

Evaluate a continuous reliability grid, preferably (r_Yin[0.3,1.0]), highlighting 0.4, 0.6 and 0.8.

At minimum apply the sensitivity to:

1. ALL-model OOS R²;
2. O-model OOS R²;
3. incremental (O+S-O) R².

Report both point estimates and transformed interval endpoints, capped at logical bounds where necessary.

Important: this is **not an estimated upper bound** and should never be labelled a factual correction. Call it:
- "classical measurement-error sensitivity", or
- "reliability-conditional latent-response R² sensitivity."

## B3. Quality-screen comparison

Place R/C/Q1/Q2 OOS R² next to the reliability sensitivity as a separate empirical check.

Do not interpret the Q screens as estimates of reliability. They are sample restrictions only.

## B4. Interpretation gate

The intended manuscript statement is conditional:

> Even under severe assumed outcome unreliability, classical attenuation correction would leave a large majority of latent response variance unexplained by the rich baseline information.

Do not claim a theoretical ceiling on human predictability.

---

# C. Why personalization fails: decompose policy value

## C1. Goal

The current result that personalized assignment does not beat uniform Cash is important but under-explained.

We need to distinguish:

1. **average dominance / limited headroom**:
   Food and Medical are worse than Cash on average, and true treatment rankings may rarely cross;

2. **prediction / misallocation error**:
   some people may genuinely benefit from a non-Cash form, but the learned policy cannot identify them reliably.

We cannot identify individual true counterfactual rankings, so the decomposition must remain at the level of honest out-of-sample subgroup and policy value.

## C2. Exact value decomposition

For an OOF learned policy (d(X)), relative to uniform Cash:

[
V(d)-V(Cash)
=
E[
1\{d(X)=Food\}\tau_F(X)
+
1\{d(X)=Medical\}\tau_M(X)
].
]

Using cross-fitted DR scores, estimate the two additive contributions:

- Food-selected contribution;
- Medical-selected contribution.

Report:
- assignment share;
- DR mean incremental effect vs Cash among respondents selected for that non-Cash form;
- contribution to total policy value;
- paired-bootstrap intervals.

This directly answers whether the policy loses because the selected non-Cash subgroups still fail to outperform Cash.

## C3. Predicted headroom vs validated headroom

Using strictly OOF predictions:

- plot the distributions of
  [
  \hat\mu_F(X)-\hat\mu_C(X)
  ]
  and
  [
  \hat\mu_M(X)-\hat\mu_C(X);
  ]
- report the fraction of respondents with predicted positive Food-over-Cash or Medical-over-Cash advantage;
- for respondents with predicted positive advantage, estimate the **held-out DR realized average treatment contrast** relative to Cash.

Do not call the predicted-positive share the share who truly benefit.

Use language such as:
- "predicted crossing";
- "validated average effect among the predicted-crossing subgroup."

If the predicted-positive subgroup does not have a positive validated DR contrast, that is evidence of ranking/misallocation noise.
If it does have a positive contrast but is very small, that is evidence of limited headroom.

## C4. Best-case stress test at RMB 1,000

Because Medical−Cash HTE is strongest at RMB 1,000, run a clearly labelled exploratory best-case personalization test:

- sample restricted to randomized RMB 1,000 and Cash/Medical arms;
- OOF conditional response / CATE learning;
- policy = choose Medical only when predicted to exceed Cash;
- evaluate vs uniform Cash with cross-fitted DR and IPW.

This is a **sensitivity / stress test**, not a new headline estimand.

If personalization still fails where HTE is strongest, this substantially strengthens the distinction between predictable HTE and actionable policy value.
If it succeeds, report that honestly and narrow the global policy-null claim.

## C5. Required figure

Create a compact "Why personalization fails" figure with, ideally:

a. predicted Food−Cash and Medical−Cash advantage distributions;
b. DR validated average contrasts among respondents assigned to Food/Medical by the OOF policy;
c. decomposition of (V(policy)-V(Cash)) into Food-selected and Medical-selected contributions;
d. optional RMB 1,000 Cash-vs-Medical stress-test value.

Do not use welfare language.

---

# D. Sample composition robustness — limited, not pseudo-representative weighting

Do **not** construct a "nationally representative" sample by propensity-score weighting unless a defensible external joint target frame is supplied separately.

The current national census margins and online adult sample frame are not automatically exchangeable.

Instead, produce one supplementary composition-robustness table using broad prespecified strata where sample sizes permit:

- age bands;
- education bands;
- income bands;
- hukou;
- city tier.

Within each stratum, report only a small set of core descriptive/predictive quantities where estimable:
- average Medical−Cash and Food−Cash effect;
- ALL OOS R² if sample size supports cross-validation;
- optionally one portability metric if cells are large enough.

Do not over-interpret noisy subgroup estimates.
This module is supplementary and lower priority than A–C.

---

# E. Manuscript-writing changes to implement after the analyses

The empirical package should generate a short `NATURE_REVISION_MANUSCRIPT_NOTES.md` containing only results-supported language.

## E1. Introduction

Retain the current conceptual structure:

- latent heterogeneity is important;
- richer measurement should, in principle, reveal stable response types;
- observed heterogeneity remains difficult to predict;
- the alternative is not merely "context matters", but that context may change which individual differences become behaviourally relevant within a common decision domain;
- examples across money, health, education, energy and digital choice;
- theoretical motivation from problem recognition / representation, without claiming the mechanism is identified.

Do not turn Bordalo et al. (2026) into the paper's mechanism unless new evidence directly measures representations or attention (it does not).

## E2. Hypothetical-outcome framing

Do not claim that failure to predict hypothetical responses implies that real behaviour must be even harder to predict.

Preferred framing:

> The hypothetical design permits clean randomization of institutional context while holding the underlying response question fixed and collecting unusually rich baseline information. The results therefore speak directly to the predictability of stated behavioural responses under controlled scenarios. Whether realized spending exhibits the same predictive structure remains an open empirical question.

## E3. Abstract / conclusion punchline

The final punchline should be sharper than "context matters" but stay within identified evidence.

Preferred language:

> Rich measurement did little to solve the prediction problem, and the limited observable signal was only weakly portable across randomized contexts. The challenge is therefore not only how deeply we measure people, but whether what we learn about them retains predictive meaning when the context changes.

A shorter version:

> More information about people does not guarantee more portable predictions of behaviour.

Avoid:
- "the true determinants of behaviour are a function of context";
- "big-data personalization is an illusion";
- "preferences are unstable";
- "context causes recategorization";
- any claim that the hypothetical design is stronger evidence than realized behaviour.

---

# F. Outputs

Create:

- `analysis/nature_revision.py`
- `NATURE_REVISION_AUDIT.md`
- `NATURE_REVISION_RESULTS.md`
- `NATURE_REVISION_MANUSCRIPT_NOTES.md`

Tables:
- `tables/nature_revision_domain_importance.csv`
- `tables/nature_revision_domain_differences.csv`
- `tables/nature_revision_ridge_maps.csv`
- `tables/nature_revision_reliability_r2.csv`
- `tables/nature_revision_policy_decomposition.csv`
- `tables/nature_revision_predicted_crossing.csv`
- `tables/nature_revision_policy_1000.csv`
- optional composition table

Figures:
- `figures/nature_revision_predictor_map.pdf/png`
- `figures/nature_revision_reliability_r2.pdf/png`
- `figures/nature_revision_policy_decomposition.pdf/png`

All figures must have panel-source CSVs and legends.

Do not overwrite the existing six locked Nature figures yet. These are revision candidates. The main manuscript figure portfolio should be changed only after the results are reviewed.

---

# G. Reproducibility and no-fishing rules

- Use fixed seeds and report them.
- Reuse the locked sample definitions and fold logic whenever the estimand permits.
- No new broad moderator scan.
- No variable-by-variable significance hunting.
- No SHAP storytelling without stability checks.
- No census weighting presented as national representativeness.
- No Cronbach-alpha-based estimate of outcome reliability.
- No mechanism claims from feature importance.
- Re-run the complete revision script twice and verify deterministic/tolerance reproduction.
- In `NATURE_REVISION_RESULTS.md`, end with:
  1. what genuinely strengthens the Nature story;
  2. what remains Extended Data only;
  3. what reviewer request should be rejected on methodological grounds;
  4. whether the manuscript's core claim should be strengthened, unchanged or weakened.
