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
