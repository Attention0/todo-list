# Figure legends

All data are aggregate. Probability units, original category 6 (>75%) outcome; z=-1,0,1 for 200/1000/5000. All R scaling; equal-form Restricted=.5 Food+.5 Medical. Pointwise CIs are not simultaneous family-wise intervals. Single scenario per person; lines do not show individual transitions.

## Figure 1 — Who has the steepest Cash curve?

`fig1_moderation.png`, `fig1_source.csv`. Single-variable Cash z×X HC3 estimates with 95% normal CIs. Q7 and expenditure/income category ranks are standardized, not actual yuan/wealth; subsidy uses separately standardized yes/no and unknown/no dummy contrasts. One SD of a dummy is not the raw between-category difference. Subsidy contributes one two-df omnibus test, not two tests, to the primary five-moderator Cash Holm family. See primary table for corrected p; no variable survives. Full form model's Cash block numerically equals the explicit Cash-only regression.

## Figure 2 — Who has the largest Restricted-vs-Cash slope difference?

`fig2_moderation.png`, `fig2_source.csv`. Exactly .5 Food z×X+.5 Medical z×X−Cash z×X; full lower orders included. HC3 normal 95% CI; independent five-variable Holm family in primary table. Form-specific diagnostic coefficients are not confirmatory. Nothing survives correction.

## Figure 3 — Fixed subgroup top-MPC curves

`fig3_subgroup_curves.png`, `fig3_source.csv`. Five rows: liquidity/income first, food/medical need next, subsidy last. Each row's three columns exhaust the R sample and are fixed before outcomes. Q7 0–5/6–8/9–10; harmonized income 1–3/4/5–6; food rank1–2/3–4/5–6; annual medical 0–500/501–5000/>5000; subsidy yes/no/unknown (not ordered). Title displays subgroup R N; near each mean is the relevant randomized cell N (Restricted is summed Food+Medical N but mean still equal-weight). Cash Wilson intervals; Restricted independent-cell delta-normal intervals. All pointwise. `subgroup_form_cells.csv` additionally gives Food/Medical separately and their component N. No moderator is defined using assigned amount or observed MPC. No household-income measure is available: income is personal-income proxy.

## Figure 4 — Where the Cash top-tail decline occurs

`fig4_contributions.png`, `fig4_source.csv`. R subgroup share times within-group Cash probability change 5000−200. Conditional on empirical R shares, error bars use independent-cell mean variance. Negative bars mean decline. Within each moderator, bars sum to the common-composition standardized endpoint change; they need not sum exactly to the raw unstandardized endpoint difference. Contributions from different partitions MUST NOT be added. No causal attribution to X or population representativeness asserted; share-of-decline ratios in table descriptive.

## Figure 5 — Joint-model / calibration diagnostic

`fig5_calibration.png`, `fig5_source.csv`, `fig5_metrics_source.csv`. Only five core variables/six design columns, no model search. Predictions and training-cut quintiles use five cell-stratified holdout folds, seed20261004. First two panels: dashed held-out forecast, solid AIPW randomized-endpoint score means, crosses raw randomized subgroup estimates. Cash positive sensitivity means p200−p5000; RC positive sensitivity means Restricted (p5000−p200) minus Cash (p5000−p200). Error bars: 499 exponential-weight bootstrap refits, fixed folds, training re-fit and quintile re-sorting; weights shared across overlapping training sets. No individual score exports, no observed individual treatment effects. Right panel: OOF Brier/MSE baseline form*z; level reference form*z+form*X; full form*z*X, same folds. No reliable honest sensitivity ordering and no interaction-only prediction gain. LPM out-of-range prediction rate and clipped-MSE robustness disclosed separately. This secondary diagnostic is neither exact finite-sample RI nor a new causal HTE discovery pipeline.

## Supplementary compact subgroup forest

`subgroup_differential_forest.png`, `subgroup_forest_source.csv`. All fifteen fixed subgroup Restricted−Cash slopes and nominal HC3 95% CIs. Significant within-group contrasts do not prove between-group moderation. Upper/lower expenditure subgroup point estimates are retained but cannot rescue null primary rank/omnibus tests.
