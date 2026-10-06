# Fertility Geography Audit — Result

## Summary

Completed the requested evidence-based audit using `/home/liuze/project-cmds_fertility`.

## Files changed

- `fertility/PROJECT_STATUS.md`
- `fertility/SAMPLE_CONSTRUCTION.md`
- `fertility/VARIABLE_AUDIT.md`
- `fertility/IDENTIFICATION_FEASIBILITY.md`
- `fertility/EXISTING_RESULTS.md`
- `RESULT.md`

`fertility/SPEC.md` and `fertility/WORK.md` were not modified.

## Key conclusions

- Current sample: 21,383 women and 235,213 retrospective woman-years, CMDS 2013–2017.
- Cleanest event: reported current-destination arrival year/month.
- Common geography: province; only 4,819 final women have city/county origin precision.
- Treatment: destination minus hukou-origin province pre-three-year mean CBR.
- The balanced birth history is not a true longitudinal panel.
- Marriage timing is usable only for 2013–2016.
- Actual prior residence and full multiple-move histories are unavailable.
- Revised short-run estimate: 2.86 pp per 10‰ CBR gap (SE 0.84 pp).

## Validation performed

Read the current README, revision notes, final sample/variable documentation, sample funnel, wave counts, geography precision, sample profile, quality diagnostics, sensitivity results, and historical key-result tables. Cross-checked 21,383 unique women × 11 periods = 235,213 person-years and distinguished revised from mixed-vintage outputs.

## Acceptance status

All five required audit documents exist and answer the core feasibility questions. The remaining missing diagnostics—OD-cell quantiles and a unified result manifest—are reported rather than invented.

## Known limitations

- Confidential microdata were not copied into Git.
- Historical models were inventoried, not all rerun.
- City treatment and a common-wave marriage hazard remain unfinished.

## Branch / commit / PR

To be filled after publication.
# Second-Round Sample Re-Audit

## Summary

Completed the descriptive second-round sample re-audit requested by `fertility/SAMPLE_REDESIGN.md` and `fertility/WORK_SAMPLE_REAUDIT.md`. The redesigned Core Mover Master contains **362,245** women after hard eligibility and internal timing-coherence checks. Cross-province movement, work/business reason, balanced event windows, marriage timing, and legacy external-data matching are retained as analysis flags or subsamples rather than master-sample restrictions. No causal regression was added.

## Files changed

- `fertility/SAMPLE_REAUDIT.md`
- `fertility/SAMPLE_TIER_COUNTS.csv`
- `fertility/SAMPLE_FLAG_DICTIONARY.md`
- `fertility/sample_reaudit.py`
- `RESULT.md`

## Key implementation decisions

- Defined auditable origin, migration, fertility, and marriage quality tiers.
- Excluded internally contradictory migration timing from hard eligibility.
- Kept all cross-county, cross-prefecture, and cross-province movers in the master.
- Reported unbalanced event-time support and balanced ±1/±3/±5 diagnostics.
- Reproduced the legacy restriction funnel and standalone sample losses.
- Preserved exact corrected legacy-final membership as a diagnostic flag, not as the master definition.

## Testing performed

- Executed `fertility/sample_reaudit.py` against the corrected 2026-09-14 woman-level base.
- Verified successful generation of all three required output files.
- Checked that tier counts sum to the 362,245-person Core Mover Master.
- Checked that no causal-model estimation is present in the audit script.

## Acceptance Criteria

- [x] Hard-eligibility funnel documented.
- [x] Quality tiers and flag dictionary produced.
- [x] Geographic and move-reason sample counts reported.
- [x] Event support for ±1/±3/±5 and r=-10 through +10 reported.
- [x] Legacy sequential funnel, standalone losses, and composition comparisons reported.
- [x] Final recommended samples stated.
- [x] No new causal regression added.

## Known issues

- The broad-master CBR match is not reconstructed from raw external place files; exact membership in the corrected legacy final export is used as a conservative diagnostic.
- The current base does not support a verified Tier A previous-residence origin; available origin observations are classified as inferred Tier B or hukou-only Tier C.

## Branch

`feature/fertility-audit`

## Commit SHA

`a782b001480b80533cecd79d72008127edebad0e` (sample re-audit implementation; this metadata line is finalized in the immediately following documentation commit)

## PR

https://github.com/Attention0/todo-list/pull/2

---
