# NHB final verification audit

## Locked scope

This round executed only the five checks in `消费调查/NHB_FINAL_VERIFICATION.md`. No manuscript file was edited, no new moderator search was opened, and no respondent-level data or predictions were written.

## Methods verified

1. **Strict inframarginality.** Monthly food-spending band lower bounds were multiplied by the six-month voucher horizon. A respondent is strict only when transfer amount is below that lower bound. Food−Cash is estimated in the pooled strict sample with amount fixed effects and HC3 standard errors; ordinal outcome is primary.
2. **1,000-draw refit bootstrap.** Each draw resamples Cash source training, target-form training, and target evaluation respondents within amount strata. Cash, Food and Medical models are refit in every draw. Primary models use 120 trees, matching the previous 100-draw refit specification. Only aggregate quantiles are retained.
3. **Amount portability.** Amount-adjusted results include amount in source models and residualize target outcomes/predictions by target amount before evaluation. Separate RMB 200/1,000/5,000 matrices use common five-fold splits within each amount; diagonals are held out.
4. **Person-score invariance.** Within each outer training fold, randomized form×amount cell means are removed from midpoint MPC before learning a baseline person score. Ridge or random forest learns this residual score; the untouched fold receives the prediction. The final HC3 regression tests held-out score×Food and score×Medical interactions while controlling form×amount.
5. **Ordinal and subjective diagnostics.** The full portability matrix is rerun with the original 1–6 outcome. Subjective-item correlation, standardized PCA and Cronbach alpha use the 27 prespecified non-age 0–10 items. PCA/alpha are descriptive and do not establish a stable latent trait.

## Mechanical checks

- All five seeds completed; all portability cells have finite OOF predictions.
- Bootstrap B=1,000 with 120 trees and no failed draw.
- Strict pooled sample N=3262 (Food 1642, Cash 1620).
- PCA eigenvalues sum to 27.005, equal to the 27 standardized items up to finite-sample normalization.
- Correlation off-diagonal range: 0.399 to 0.850; median absolute correlation 0.703.
- No raw data, identifiers, respondent rows, fold assignments, OOF predictions or draw-level bootstrap results are included.

## Interpretation safeguards

- The strict-inframarginal effect is a randomized Food−Cash contrast within a baseline-defined subgroup, but its subgroup definition inherits interval-reporting and six-month extrapolation assumptions.
- Amount-specific portability has materially smaller cell sizes and is used for heterogeneity diagnosis, not independent discovery claims.
- Seed variation is a stability diagnostic, not five independent replications.
- The person-score midpoint/RF result is not robustly reproduced on the primary ordinal outcome; it is suggestive specification-dependent evidence.
- Very high alpha and a dominant PC1 can reflect overlapping wording or common response style; they do not prove a single substantive psychological trait.
