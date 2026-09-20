# Consumer Survey Initial Audit Result

## Summary

Completed the first-round data audit and minimal first look required by `WORK.md`, using the specified Stata delivery file and questionnaire. No respondent-level data was added to the repository, and the research design was not expanded beyond the requested audit.

## Files changed

- `DATA_AUDIT.md`: data structure, sample quality, assignment integrity, randomization balance, outcome audit, sample composition, precision, and limitations.
- `FIRST_LOOK.md`: direct answers to the ten required research questions and the requested Strong/Weak/Fatal/Next summary.
- `analysis/initial_audit.py`: reproducible audit and first-look code accepting an external `.dta` path.
- `figures/`: five aggregate distribution and treatment-pattern figures.
- `tables/`: aggregate variable dictionary, balance, distribution, and precision tables.

## Key implementation decisions

- Reconstructed treatment only from the questionnaire-verified Q32–Q40 mapping and cross-checked it row by row against `scen_*` fields.
- Kept the six-category ordered outcome primary; midpoint MPC is auxiliary and includes an alternative top-category coding check.
- Reported raw N=5,497 and a transparent clean-candidate N=5,171 without modifying or deleting raw records.
- Used bounds, not a single midpoint, to classify food-voucher bindingness.
- Treated past medical spending as a proxy rather than a matched medical-account budget constraint.
- Harmonized the 30 legacy Q46 income codes 11–16 to their documented 1–6 equivalents.

## Testing performed

- Ran `analysis/initial_audit.py` against `社会心态小调研数据(1).dta`; completed successfully.
- Reproduced N=5,497, 67 fields, 5,497/5,497 exactly-one-scenario records, assignment p=0.931, joint balance p=0.454, floor=31.31%, ceiling=7.49%.
- Verified no duplicate IDs, full duplicate records, assignment metadata mismatches, or invalid outcome codes.
- Visually inspected Figure A and Figure B.
- Ran `git diff --check` successfully.
- Verified the committed variable dictionary suppresses respondent ID values.

## Acceptance Criteria

- Actual delivery data, questionnaire, and available analysis materials located and recorded: met.
- Data structure, missingness, duplicates, assignment integrity, cell size, balance, outcome distribution, sample quality, variable dictionary, and limitations: met.
- Raw and clean-candidate results, reduced-form treatment patterns, food bounds analysis, medical screening, external validity, and precision: met.
- Required figures and numeric results: met.
- `DATA_AUDIT.md` and `FIRST_LOOK.md` created: met.
- Raw respondent-level data excluded from GitHub: met.

## Known issues

- The delivery contains no timing, IP, device, channel, or platform quality flags.
- The DOCX renderer in the local artifact runtime lacked LibreOffice; questionnaire content was therefore checked through structured DOCX extraction and cross-validation with delivery variables rather than page-image rendering.
- Statistical environment dependencies (`scipy`, `statsmodels`, `matplotlib`) are required to rerun the script and are not vendored.

## Git

- Branch: `feature/consumer-survey-initial-audit`
- Implementation commit SHA: `485d8e23226e248f362117cfe9ab6414ad196606`
- PR: https://github.com/Attention0/todo-list/pull/3
- Merge status: not merged.

## Heterogeneity exploration update

Completed the full `HETEROGENEITY_WORK.md` scope on the same branch and PR:

- Added `HETEROGENEITY_AUDIT.md` and `HETEROGENEITY_RESULTS.md`.
- Added a reproducible theory-guided, ordered-outcome, regularized, prediction, and honest/cross-fitted HTE pipeline.
- Added aggregate heterogeneity tables and figures; no respondent-level records were committed.
- Distinguished stated-MPC level associations, randomized treatment-effect heterogeneity, and conditional fungibility contrasts throughout.
- Applied raw/clean and outcome-coding robustness, family-level BH-FDR, amount-specific scans, ordered-logit direction checks, repeated cross-validation, and held-out CATE-quintile calibration.
- Main synthesis: objective resources/needs weakly predict stated-MPC level; food-cash HTE is an important null; medical-related heterogeneity is stronger, with income, education, and past medical spending robustly differentiating medical from food responses.
