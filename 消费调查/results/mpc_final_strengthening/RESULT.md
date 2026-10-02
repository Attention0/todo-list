# RESULT — final MPC size-curve strengthening

## Summary

Decision **2: plausible main story but must be written as suggestive**. Restricted−Cash top-category differential=.02954 per fivefold amount increase, CI [.01043,.04865], raw/Holm p=.00244/.01222. However, direct d75−dany=.01939, CI [−.01439,.05317], Holm=1; no tail-specificity. Relative/link robustness directionally supportive but multiplicity weaker. Primary pooled ordinal=.09121, CI [−.01650,.19892]. No manuscript changes; further current-data exploratory analysis stops.

## Files changed

New `消费调查/MPC_FINAL_STRENGTHENING_RESULTS.md` and `消费调查/results/mpc_final_strengthening/` scripts, prescribed aggregate tables, finite-grid summaries/diagnostics, five PNGs/source CSVs, plan/audit/legends/manifest/this result. Latest main's immutable strengthening task document inherited by merge. PR #9's code/results unchanged; raw data and all old untracked files excluded.

## Key implementation decisions

Direct PR #9 preparation/controls reuse; exact equal form weights; six-estimand Holm family; explicit HC1 nonlinear/ordered sandwich and analytic marginal delta; joint 5,000-cell bootstrap preserving threshold covariance; ratio mixture before ratios; full 420-spec grid; endpoint scale normalization explicit; latent scales separate. No new moderators or mining.

## Testing performed

Two full bounded executions; repeated core CSV hashes matched (specification metadata clarification documented). Aggregate acceptance and independent analytic-gradient/nested-threshold covariance checks passed. 140 grid configurations finite/converged. All five figures visually checked. Exactly ten report sections. No unexecuted test claimed.

## Acceptance Criteria

All nine named analysis tables, additional joint/source/diagnostic tables; figures A–E and source CSVs; no individual exports; report makes explicit one-of-three judgment and stop decision. No manuscript/HTE/SHAP/latent/subgroup expansion. New stacked PR dependent on #9, no automatic merge.

## Known issues

No directly established tail-specificity; unadjusted ordinal primary weak; ordered pooled differences unstable in quality screens; relative nine-family Holm weak; no equivalence between restricted forms; hypothetical/binned/top-coded response and bundled form attributes; conditional-model AME uncertainty; not representative or welfare/realized-MPC claims. These are scientific limits, not missing computational deliverables.

## Branch

`feature/mpc-final-strengthening`, direct base PR #9 (`d749f5c`) plus latest main `ef0f174` task document. PR base `feature/mpc-size-curve` to avoid duplicating inherited package changes.

## Commit SHA

Analysis commit: `4c1281569c083507d00abd463f007baada3baffb`. Publication metadata follow-up is separate to avoid a self-referential SHA. Native Git push succeeded using the existing Windows proxy configuration after direct connectivity failed.

## PR

https://github.com/Attention0/todo-list/pull/10 — stacked on PR #9. Do not merge #9 or this PR automatically. Further exploratory analysis of the current data stops here.
