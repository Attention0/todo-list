# RESULT — NHB reviewer re-analysis

## Summary

Independently reran the NHB core empirical claims from the local raw Stata delivery and questionnaire/codebook. The corrected package adds the fully OOS 3×3 portability benchmark, target normalization, direct invariance comparisons, adult/clean/Q1/Q2 robustness, food-spending bound tests, and corrected HTE validation with a shared-cash direct comparison.

The evidence is closest to **Pattern C**: low within-context predictability explains much of the low cross-context performance, and form-specific mappings do not improve held-out fit. A medical-versus-food asymmetry remains in point estimates and HTE validation, but it is not sufficiently stable across model-refit uncertainty and the strictest Q2 screen to justify Pattern B as the headline.

## Files changed

All new files are under `消费调查/results/nhb_reanalysis/`:

- reproducible extraction and analysis scripts;
- aggregate CSV tables and run manifest;
- three PNG figures;
- `NHB_REANALYSIS_AUDIT.md`;
- `NHB_REANALYSIS_RESULTS.md`;
- reproduction instructions and this result summary.

No respondent-level raw data, IDs, or OOF prediction rows are included.

## Key implementation decisions

- Five common, nine-cell-stratified outer folds and five fixed seeds.
- All diagonal portability estimates are truly OOS and use the same training fraction as off-diagonal estimates.
- Primary portability uncertainty uses a 100-draw respondent bootstrap with model refitting in source and target arms; 5,000-draw conditional-on-fit intervals are secondary.
- Direct invariance is evaluated by held-out loss for additive versus X-by-form ridge and common versus form-specific random forests.
- Food inframarginality is based on both lower and upper six-month spending bounds.
- HTE validation uses OOF rankings, cross-fitted DR scores, BLP and GATES; the Medical-minus-Food comparison jointly resamples the shared cash arm.

## Testing performed

- Verified raw sample size (5,497), adult sample (5,480), clean sample (5,171), one-and-only-one vignette response, and exact agreement with delivered treatment metadata.
- Reproduced all locked quantities listed in `reproduction_crosswalk.csv` within declared tolerances.
- Ran 41 baseline balance tests; no BH-adjusted rejection.
- Ran the full script stages against the raw `.dta`, including 3×3 matrices, refit bootstrap, direct invariance, food bounds and HTE validation.
- Verified all committed CSVs are aggregate and scanned the output directory for respondent-level files.

## Acceptance Criteria

- [x] Latest `main` used as branch base.
- [x] `WORK.md`, `SPEC.md`, and `NHB_REVIEW_REANALYSIS.md` followed.
- [x] Manuscript not edited.
- [x] Required analyses and robustness samples completed.
- [x] Code, tables, figures and reports restricted to the required output directory.
- [x] No respondent-level raw data committed.

## Known issues

- Outcome reliability cannot be estimated from a single response; attenuation scenarios would be assumptions, not evidence.
- The refit bootstrap uses 120 trees per forest for computational feasibility, versus 180 trees for primary point estimates.
- Q2 is much smaller and changes the corrected HTE contrast; this is reported as fragility, not hidden.

## Branch / Commit / PR

- Branch: `feature/nhb-review-reanalysis`
- Commit SHA: recorded in the final handoff after commit
- PR: recorded in the final handoff after push
