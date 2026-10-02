# Current delivery - Nature figures

## Summary

Completed `NATURE_FIGURES_WORK.md`: four visually unified main figures, six Extended Data figures, editable vector PDF/SVG and600dpi PNG, combined four-page PDF and2×2 contact sheet. Main Figure1 is exactly1×3 ordinal/midpoint/Top75. Uses only existing approved PR9-12 aggregate results; no new empirical work or manuscript change.

## Files changed

`NATURE_FIGURES_RESULT.md`; `results/nature_main_figures/` contains ten figure families,13 source/audit CSVs, captions, style guide, figure audit, source manifest,231-check verification record and editable plotting/verification scripts. Existing analysis artifacts unchanged.

## Key implementation decisions

Same180mm page width, Arial, fixed treatment palette/markers, thin approved CIs. Restricted is dashed/hollow and explicitly derived=.5Food+.5Medical. Figure4 uses allowed compact six-family minimum BH q alternative plus full q rugs/count strip; detailed all-X in ED6. No commensurability claim for scalar versus factor coefficients. Original CI conventions retained and disclosed. No tail-specificity or equivalence upgrade.

## Testing performed

231 actual automated checks passed; source hashes/numeric values/CI/q/N/schema identities, no raw/estimator imports, vector PDFs/editable SVGs,600dpi/180mm, combined-page identity. Strict content bounds passed. All ten final PNGs, final PDFs/14 Poppler page proofs, contact sheet and grayscale inspected. Reduction caveat explicit; CVD simulator unavailable, not claimed tested.

## Acceptance Criteria

Four main layouts/figures, six ED diagnostics, all export formats/source CSVs/captions/style/audit/contact/combined file complete. No manuscript edit/new analysis/respondent export. New feature branch/stacked PR, no merge.

## Known issues

Full-width multi-panel figures should not be single-column thumbnails.89mm QA reductions are not a substitute for180mm typesetting. CVD simulation unavailable. Underlying suggestive/measurement/power limitations unchanged; lack of corrected discoveries is not equivalence.

## Branch

`feature/nature-main-figures`; stacked on PR12 `feature/mpc-allx-screen`, latest main6867cac merged.

## Commit SHA / PR

Pending publication; recorded after artifact commit. No automatic merge.

---

# Previous delivery record - all-X screen (PR12)

# Summary

Completed `MPC_SLOPE_ALLX_SCREEN_WORK.md` against PR9–11 and latest main44e2997. Inventory first: 67 raw fields /221 entries /150 eligible representations. Parallel ordinal/midpoint/Top75, Cash-only and equal-weight RC moderation; six BH/Holm families size150. No q<.10 / Holm survivors; zero Tier A/B. Final classification: **rich observables still explain little**, narrowly interpreted as no corrected stable signature, not zero heterogeneity or a measured joint explanatory-share bound. No manuscript change or additional search.

# Files changed

- `MPC_ALLX_SCREEN_RESULTS.md`: exactly17 mandated sections.
- `results/mpc_allx_screen/`: inventory/mapping, frozen prior direction metadata, six main tables and all diagnostic/concordance/stability/conditional joint tables, scripts, audit/locked plan/environment/manifest/test results.
- Six PNG/PDF figure families, six aggregate source CSVs, figure legends. Figures3/4 are explicit fixed-prior null displays; Figure5 is N/A, not invented candidate curves.

# Key implementation decisions

No new PCA fit; previously saved domain/global diagnostic directions reconstructed, residual global PCs unvalidated. Raw factors + prior ranks/aliases retained; aliases are not independent replications. Four sparse full factors nonestimable; no ad hoc category pooling. Cash-only fitting separately verified; RC weights exactly−1,+.5,+.5. HC3 fully interacted pooled OLS equals per-form blocks. Nonestimable correction placeholders p=1 keep planned family size, visible p/q missing. All150×3Y×2targets×5folds run; no respondent fold/prediction exports. Empty corrected shortlist means protocol-conditional sample/function/adjustment and joint layers explicitly not applicable, never claimed passed. Optional regularization omitted.

# Testing performed

Actual full script runs; independent statsmodels coefficient/covariance/omnibus and Cash-only equality checks; independent manual BH/Holm formulas; inventory/outcome/sample/fold/alias/gate/schema assertions. `test_results.json`: 114 assertions passed, including full repeated execution with all27 aggregate CSV SHA256 identical. All six figures visually reviewed; crowded ticks revised before final render. Initial coding and Cash-support issues corrected before final outputs. No tests claimed for unestimated N/A layers.

# Acceptance Criteria

Inventory complete before screen; six corrected families; cross-outcome/raw-constructed/subjective-objective summaries; every-X stratified five-fold stability; required tables/6 figures/source/legends; exact17-section report; no raw respondent exports; no manuscript changes; new feature branch/PR; no merge. Conditional required artifacts explicitly document absence of candidates. Stops further exploration.

# Known issues

Exploratory coarse hypothetical Y; correlated outcomes/representations; sparse factor support; limited moderation power; response error. No independent validation/equivalence claim. Joint explanatory share not estimated because candidate gate empty. Four raw factors unsupported; harmonized/rank representations remain separately screened where previously defined.

# Branch

`feature/mpc-allx-screen`; stacked on PR11 `feature/mpc-who-drives` (PR9/10 dependencies retained).

# Commit SHA

Analysis/artifact commit: `c2e3b71621f77b82766e70a3888c409b7256dd33`. Publication-record commit follows; this reference is intentionally not a self-referential commit hash.

# PR

https://github.com/Attention0/todo-list/pull/12 — stacked base `feature/mpc-who-drives` / PR11. No automatic merge.
