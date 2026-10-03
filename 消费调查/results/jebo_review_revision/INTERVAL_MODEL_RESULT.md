# Censored-normal affine sensitivity

| model | loglik | parameters | converged | retry | max_gradient | hessian_min_eigenvalue | mean_abs_probability_error | max_probability_error | slope_equality_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| constant_full | -9254.694276994183 | 7 | True | False | 1.5766532685944205e-07 | 577.0849173631918 | 0.10150909276994315 | 0.2081111070606896 | 0.7802771005749272 |
| constant_common_slope | -9255.019578914884 | 5 | True | False | 6.360919862414203e-07 | 603.9751564894593 | 0.10148234414937427 | 0.20867211352284745 |  |
| amount_full | -7394.499518144744 | 9 | True | False | 5.972020889762014e-07 | 1048.8991859446144 | 0.03998683063098574 | 0.0878225713310502 | 0.07687099399493832 |
| amount_common_slope | -7397.017778769692 | 7 | True | False | 4.3974505300008397e-07 | 1054.4423916271132 | 0.04000346918366003 | 0.0898963737032577 |  |

Bounds are conditional on the questionnaire audit: merged below10%, 10–25%, 25–50%, 50–75%, and right-censored above75%. No zero/100% cap is imposed. The latent normal can be negative and has no structural spending interpretation. Constant residual scale is the frozen primary sensitivity; three amount-specific scales are the single frozen alternative. Sandwich covariance uses individual category scores and the observed likelihood Hessian. Bootstrap failures are retained in interval_bootstrap_status.csv and valid-draw denominators are attached to every percentile interval. Good numerical convergence does not establish measurement validity; calibration discrepancies must accompany all parameter interpretations.
