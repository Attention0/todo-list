# NHB final verification — locked requirements

## Scope

This is a closed verification round following `NHB_REVIEW_REANALYSIS.md`. It must not reopen exploratory searches, alter the manuscript, or change the core outcome and treatment definitions. All new analysis outputs remain aggregate and must be written to `消费调查/results/nhb_reanalysis/`.

## Required checks

1. Formally estimate the pooled Food−Cash effect in the strictly inframarginal food-spending sample. Strict inframarginality is defined from the lower bound of the reported monthly food-spending interval multiplied by the six-month voucher validity period. Report the original ordinal outcome as primary and midpoint coding as sensitivity, with heteroskedasticity-robust uncertainty and amount adjustment.
2. Increase the model-refit respondent bootstrap for Cash→Food and Cash→Medical target-normalized portability gaps from 100 to 1,000 draws. Resample source training, target training and target evaluation respondents within randomized amount strata; refit models in every draw.
3. Add amount-adjusted portability and separate portability matrices for RMB 200, 1,000 and 5,000. Diagonal cells must remain genuinely out of sample, and all comparisons must use common folds/seeds.
4. Add a held-out person-score × transfer-form invariance test. Construct the person score without using the held-out respondent’s outcome, then test whether its response slope differs across transfer forms. Report separate Food×score and Medical×score terms and their joint test.
5. Add ordinal-outcome robustness plus a descriptive audit of subjective-item correlations, PCA and Cronbach’s alpha. Treat alpha and PCA as measurement diagnostics, not evidence of a unidimensional latent trait.

## Stopping rule

After completing these five checks, update the audit/results/RESULT summaries, commit and push. Do not add further moderators, mechanisms, policy exercises or manuscript edits.

## Reproducibility and privacy

- Use fixed seeds and common folds.
- Record model settings and package versions.
- Do not commit raw data, respondent identifiers, respondent-level predictions or bootstrap resamples.
- Report nulls and specification sensitivity directly.
