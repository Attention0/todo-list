# Result — 2026-10-04 reconciliation and identification-gap audit

Executed 2026-10-06 against main commit 52c28d735d857400de6fb2392616c9eab9f04e50.

## Summary

Completed DATA_RECONCILIATION.md and IDENTIFICATION_GAP_AUDIT.md under the latest WORK priorities. Preserved the published broad population for comparison. Executed descriptive counts, external province CBR remerge, questionnaire-versus-release checks, raw 2017 settlement-field coverage, province graph diagnostics, and a small local-only retrospective history. No causal or mechanism regressions were added.

## Files changed

- fertility/DATA_RECONCILIATION.md
- fertility/IDENTIFICATION_GAP_AUDIT.md
- fertility/audit/reconcile_20261004.py
- fertility/audit/sample_definition_20260920.py
- fertility/audit/reconciliation_evidence.json
- RESULT.md

## Key implementation decisions

Published population remains 362,245. Optional restrictions are measured independently rather than accumulated. Actual macro matching retains 323,949; legacy final membership is not a matching flag. All 63,336 currently unmarried base women in 2012–2016 are excluded from the published master; marriage/first-birth risk sets therefore require reconstruction. Questionnaires contain 2017 Q412–418 but the supplied raw release does not. Age-capped balanced ±5 support is 125,206, not the prior unrestricted-age 139,184. The 2017 roster flag was already correctly assigned to all that wave's master records.

## Testing performed

Executed the diagnostic script under WSL to successful completion. Assertions verified 362,245 master women, unique base IDs, complementary subsample counts, and equality of newly reconstructed versus saved CBR gaps for all 21,255 overlapping legacy IDs. Inspected aggregate missingness, province graphs, actual DTA labels and routed intention fields. Created 51 local-only person-year rows for 11 respondents and checked their field provenance. Source inputs are hashed in the evidence JSON. No regression test is claimed. Microdata and real-ID diagnostic rows are not included in Git.

## Acceptance Criteria

- Completed checklist A–H with verdicts, evidence, counts, contradictions and required concluding lists.
- Classified every upgrade-plan Tier 0–3 proposal and deferred §5 mechanism family using A/B/C, explicit requirements, timing, sample cost and residual identification issues.
- Unknown costs and unavailable histories are explicitly labeled rather than invented.
- Preserved SPEC.md, WORK.md, raw/clean datasets and historical audit outputs.
- Mechanisms deferred; no merge to main.

## Known issues

True previous-residence histories and realized exits are unavailable. Current broad population is selected by fertility-module availability. City-level standardized fertility, full risk sets and several donor/eligibility merges require further work. Benchmark methods are attributed to the supplied plan, not independently reverified against the paper's full appendices. Local GitHub transport failed; publication uses the authorized GitHub connector.

## Branch

feature/fertility-reconciliation-20261004 (based on latest main; earlier PR #2 remains separate).

## Commit SHA

Pending publication; to be replaced with the audit commit in the metadata follow-up.

## PR

Pending creation.
