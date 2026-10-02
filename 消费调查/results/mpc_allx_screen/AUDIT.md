# Audit and reproducibility

Direct foundation PR9/10/11, latest main44e2997 task merged into feature/mpc-allx-screen. Stacked publication target feature/mpc-who-drives; no manuscript modified. No respondent-level exports. Local raw .dta SHA in inventory_manifest.json; `screen_manifest.json` gives seed and only aggregate cell/fold counts. 67 raw fields /221 inventory entries /150 eligible, inventory frozen before regressions. Complete locked choices are in ANALYSIS_PLAN.md.

Cash must be estimated only using Cash support: software QA caught and corrected an initial implementation that required support in other forms for Cash. Final outputs fit Cash separately and independent tests verify equality to the Cash block of the supported full-model HC3 fit. Exact equal-weight RC = .5 Food+.5 Medical−Cash. Six planned families each size150; nonestimable p=1 placeholders included in correction, visible p/q missing. No category collapsing. Scalar tests normal/chi-square1 equivalent; factor tests multivariate HC3 chi-square with full covariance rank required. Per-form separate HC3 blocks exactly equal the fully interacted pooled OLS covariance. Crossfit zero-variation heldout covariance cannot support a Wald test; use coefficient-direction projection only, no fabricated inference. Initial pandas field-access / singular holdout issues were repaired before final run.

Reconstruction uses existing saved aggregate PCA loading tables, stored locally as frozen_prior_pca.csv with original commit provenance and reconstructed centers/scales. No runtime fetch or newly fitted PCA axes. Original-unit supplement is within each primary CSV; category slopes and individual contrasts in supplemental tables, with categoryN<10 suppressed. Inventory eligibility and families unchanged after seeing Y. Full support failures, missing tests, lower tiers retained. N/A conditional analyses are clearly marked, not silently claimed complete estimates. No independent holdout confirmation; five folds share original discovery dataset.

Run locally (Python3.12 compatible with numpy/pandas/scipy/statsmodels/sklearn/matplotlib):

    python screen.py "<local raw .dta>" --out "<this directory>"
    python deliver.py "<local raw .dta>" --out "<this directory>"
    python test_screen.py "<local raw .dta>"

Set OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1 for deterministic, efficient fitting. Existing sibling PR9/11 scripts are imports, not rerun discovery. No external raw-data requirement/export. Script output includes run phase/counts; test_results.json records actually executed assertions. High-cardinality factors may be legitimate baseline descriptors but have unsupported full category/form slope blocks; these are limitations, not null findings. FDR dependence/representation redundancy, coarse hypothetical Y, possible baseline self-report error and selection/power limits prevent a trait/mechanism/zero-heterogeneity inference. Exploration stops here.
