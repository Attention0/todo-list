# RESULT — MPC size-curve discovery

## Summary

Completed the prescribed size-curve package. Decision: **interesting but still underpowered / suggestive**, not a locked Nature Communications headline. Raw ordinal Medical−Cash slope=.1451, CI [.0234,.2668], raw/Holm p=.0195/.0778. Midpoint differential=.02705, Holm p=.03409. Cash gradient is chiefly unconditional upper-tail compression. Fixed-population Food and Medical-need layers remain limited. No manuscript changed or original HTE/SHAP story extended.

## Files changed

- `消费调查/MPC_SIZE_CURVE_RESULTS.md`: exactly 14 requested sections.
- `消费调查/results/mpc_size_curve/`: self-contained analysis and output-verification scripts, aggregate CSVs, six PNGs covering five figure families, six figure-source families, legends, manifest, audit and this result.
- No previous analysis/results/manuscript/raw delivery files changed or staged.

## Key implementation decisions

Ordinal R/unadjusted primary, fixed five-test Holm family; HC3 OLS and explicit HC1 ordered sandwich. RI preserves exact nine-cell counts but tests a sharper no-amount-effect null, not slope equality. Food pooled contrasts use saturated equal-amount means; a common strict subgroup separates eligibility composition from curves. Binding-group slope not identified. ML restricted to a small fixed shallow tree and theory features.

## Testing performed

Ran full pipeline on local original delivery. Ran `test_outputs.py`: all design/count/probability/CDF/threshold/decomposition/contrast/Holm/sample/RI/figure/source/privacy-schema and fourteen-section checks pass. Repeated final full execution: all aggregate CSV SHA-256 hashes identical. Ordered logit/probit convergence asserted. Visually inspected all six figures and fixed crowded log-axis minor ticks and distribution legend. Source/generated result correspondence checked. No unexecuted test claimed.

## Acceptance Criteria

All ten required table types, all five figure families, source CSVs and requested fourteen-section report delivered; raw/adult/clean/Q1/Q2 and adjusted robustness; ordinal/logit/probit/midpoint/alternative-top/threshold tests; adjacent/end contrasts; distribution anatomy; Food/Medical matching; limited economic benchmarks/model comparison/tree diagnostic. No raw data, IDs or individual OOF predictions. New branch/PR; no merge.

## Known issues

Outcome hypothetical/binned, scale and absolute-yuan interpretation unresolved; bundled transfer attributes; not representative-population or welfare inference; observational baseline moderators; weak ordered/multiplicity-adjusted primary evidence; Q2 point estimate near zero; low binding group support. See full audit/results. Old untracked local files preserved and excluded.

## Branch

`feature/mpc-size-curve`, based on latest fetched main `da1eec5`.

## Commit SHA

Analysis/data/figures/report commit: `5d2692658847657c6b46ded83242fa2725a0c0c6`. A separate metadata-only follow-up records publication; its SHA is available in the branch history (avoids a self-referential commit hash).

## PR

[PR #9](https://github.com/Attention0/todo-list/pull/9), targeting `main`, published and open. No automatic merge.
