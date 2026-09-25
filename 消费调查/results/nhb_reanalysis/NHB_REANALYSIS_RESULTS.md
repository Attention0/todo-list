# NHB reviewer re-analysis results and decision memo

## Decision

The corrected evidence most closely supports **Pattern C: mostly low predictability, little direct evidence of contextual remapping**, with one narrower descriptive asymmetry: Cash-to-Medical loses more rank portability relative to the Medical within-context benchmark than Cash-to-Food does relative to Food. This is not Pattern A. It does not cleanly reach Pattern B because the model-refit interval for the medical portability loss includes zero and direct invariance models fail to improve held-out fit when form-specific mappings are added.

## Strongest independently reproduced facts

1. Randomized average effects reproduce. Food-Cash is -0.121 ordinal categories (95% CI -0.223, -0.019); Medical-Cash is -0.311 (-0.410, -0.211).
2. Within-context prediction is weak: mean OOF Spearman is 0.178 for cash, 0.164 for food and 0.160 for medical; corresponding target-centered R2 values are 0.043, 0.028, and 0.032.
3. Target-normalized Cash-to-Food rank loss is 0.016; Cash-to-Medical loss is -0.052. The secondary paired target bootstrap gives Cash-to-Food 95% CI [-0.038, 0.049] and Cash-to-Medical [-0.105, -0.002]. The refit-bootstrap table is the primary uncertainty record.
   In the primary model-refit bootstrap, Cash-to-Food is 0.009 (95% interval -0.075, 0.086) and Cash-to-Medical is -0.041 (-0.129, 0.017); both intervals include zero.
4. Direct invariance is an important null. Mean ridge X-by-form incremental OOS R2 is -0.0163 and form-specific RF incremental OOS R2 is -0.0089. Neither flexible representation improves on its common-map comparator.
5. Food inframarginality is an important null: the ordinal form-by-bound-class joint test has p=0.307 (midpoint p=0.236). The data do not show that Food-Cash differences are systematically organized by bindingness bounds.
6. Corrected HTE validation separates the two contrasts in R/A/C/Q1. Across five seeds, Food-Cash standardized DR-BLP slopes range -0.012 to 0.005; Medical-Cash slopes are positive in all seeds, 0.027 to 0.039. In the shared-cash bootstrap, the R-sample Medical-minus-Food difference is 0.034 for BLP and 0.087 for GATES, with intervals excluding zero. However, both differences reverse sign and include zero in Q2. Amount-interaction p-values vary materially by seed, so HTE contrast and amount localization are not fully quality-screen-stable.

## Robustness interpretation

Adult and clean-sample results track the raw-sample conclusions. The stricter Q1/Q2 screens reduce precision but do not overturn the hierarchy: average Medical-Cash is more negative than Food-Cash; absolute predictability is weak; form-specific mapping flexibility does not deliver a stable held-out gain. The Q screens are composition-changing sensitivity checks and should not be described as recovering a cleaner population estimand.

## What the current manuscript can and cannot say

- Supported: form shifts average stated consumption; measured covariates have weak individual-level predictive power; the point estimate of Cash-to-Medical target-normalized portability is worse than Cash-to-Food; Medical-Cash HTE ranking validates more consistently than Food-Cash in R/A/C/Q1.
- Not supported as a headline: broad non-portability, a general failure of invariance, a simple feature-switch mechanism, stable RMB-1,000 localization, or a bindingness mechanism for food vouchers.
- The empirical center should therefore be low predictability plus a bounded medical-versus-food asymmetry, with direct invariance and food bindingness presented as important nulls. The manuscript itself was not edited.

## Required next editorial step

Do not retain claims that raw cross-form correlations alone establish remapping. Any revision should lead with the fully OOS target-normalized benchmark and explicitly reconcile the medical portability loss with the null direct-invariance increments. This memo settles the empirical pattern; it does not rewrite the paper.
