# Existing all-X cross-fit diagnostics (not rerun)

| target | outcome | representations | five_valid_train | five_valid_holdout | five_train_same_direction | five_holdout_positive |
| --- | --- | --- | --- | --- | --- | --- |
| cash | ordinal | 150 | 146 | 143 | 67 | 5 |
| cash | midpoint | 150 | 146 | 143 | 77 | 3 |
| cash | top75 | 150 | 146 | 143 | 67 | 8 |
| rc | ordinal | 150 | 146 | 141 | 68 | 1 |
| rc | midpoint | 150 | 146 | 141 | 78 | 5 |
| rc | top75 | 150 | 146 | 141 | 65 | 2 |

Source: results/mpc_allx_screen/crossfit_family_summary.csv and crossfit_stability.csv; five cell-stratified folds, seed20261005. Every eligible X×three outcomes×Cash/RC was directionally projected from training coefficients into held-out coefficients. Factor vectors use training unit direction. Training sign comparisons to overlapping full sample are optimistic; heldout same-sign counts are descriptive and dependent. Sparse factor/zero-variance failures are retained. This is not a joint BLP/GATES heterogeneity test and does not establish universality. No valid already-completed joint BLP/GATES test for this specific size-curve estimand was found in the cited all-X package; older HTE analyses address different estimands and are not recycled as validation. No new black-box/global heterogeneity search was launched. Reuse is supplemental, not independent replication.
