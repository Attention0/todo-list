# Fungibility latent trait investigation plan

## Research question

The next stage should not continue optimizing MPC prediction. The key question is whether individual differences in how people treat different transfer forms as substitutes represent a stable economic trait.

The target concept:

> Individual resource fungibility: the extent to which a person treats different transfer forms as economically interchangeable.

The paper contribution is not that different transfer forms generate different MPCs (already known). The contribution would be showing whether cross-form MPC differences have a stable individual component beyond ordinary MPC heterogeneity.

---

## Priority 1: Audit data structure

Before further modeling, document exactly:

1. How many MPC observations does each respondent have?
2. Which transfer forms are observed for each respondent?
3. Which RMB amounts (200/1000/5000) are observed for each form?
4. Is cash observed repeatedly or only once?
5. Is assignment/order randomized?
6. Are there any repeated measures that can identify measurement reliability?

This determines whether a latent trait model is feasible.

---

## Priority 2: Test whether fungibility is a measurable latent trait

Do not start with simple differences:

F_i = MPC_cash - MPC_food

because this mixes true heterogeneity with measurement noise.

Estimate a latent factor model:

MPC_if = alpha_f + lambda_f * theta_i + error_if

where:

- alpha_f captures average form effects;
- theta_i captures individual fungibility tendency;
- lambda_f captures how each form loads on fungibility.

Report:

1. variance explained by latent fungibility;
2. reliability of theta_i;
3. form-specific residual variance.

Question:

Do people have a stable cross-form response pattern?

---

## Priority 3: Cross-form validation

Avoid mechanical correlations caused by shared cash terms.

Possible tests:

### A. Split-form prediction

Use some forms to estimate individual fungibility score and test whether it predicts response to another form.

Example:

Food/Cash information -> predict Medical response.

### B. Leave-one-form-out validation

Estimate latent fungibility excluding one transfer form, then test on the excluded form.

This directly tests portability.

---

## Priority 4: Compare with existing MPC heterogeneity literature

The relevant benchmark is not simply whether demographics predict MPC.

Compare:

1. Predicting MPC levels;
2. Predicting cross-form substitution/fungibility.

Question:

Does fungibility reveal a new dimension of heterogeneity beyond standard MPC heterogeneity?

Candidate predictors:

- income
- wealth proxy
- demographics
- psychological measures
- financial attitudes
- mental accounting related variables (if available)

---

## Priority 5: Examine external validity

Search existing questionnaire modules for validation outcomes:

- financial attitudes;
- saving behavior;
- consumption habits;
- psychological scales;
- mental accounting measures.

Test whether latent fungibility predicts independent outcomes.

---

## Priority 6: Reframe manuscript figures

Possible new structure:

Figure 1: Form effects

Different forms generate different MPCs (background, not main contribution).

Figure 2: Latent fungibility structure

Show whether a common individual component exists across forms.

Figure 3: Predictability of fungibility

Show how much standard observables explain latent fungibility.

Figure 4: Economic implications

Show whether fungibility changes optimal interpretation of transfers or resource allocation.

---

## Important caution

Do not claim:

"We discover heterogeneous MPC."

Existing literature already studies this.

The stronger claim, if supported, is:

"We identify a previously unmeasured dimension of economic heterogeneity: how individuals translate different forms of resources into consumption responses."

The immediate goal is therefore not more ML prediction, but identification and validation of the latent fungibility construct.
