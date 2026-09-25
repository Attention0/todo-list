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

## Formal heterogeneity robustness update

- Added `HETEROGENEITY_FORMAL_AUDIT.md` and `HETEROGENEITY_FORMAL_RESULTS.md`.
- Added `analysis/heterogeneity_formal.py`, 18 aggregate `formal_*.csv` tables, and three reproducible figures.
- Corrected nominal/ordered categorical handling; added saturated Type×Amount×X checks, HC3, FE/cluster robustness, 2,000-permutation randomization inference, unified nested CV, and treatment-cell-stratified OOF HTE validation.
- Preserved all first-pass outputs for comparison and did not commit respondent-level data or predictions.

## Final exploration update

### Summary

Completed `FINAL_EXPLORATION_WORK.md` without selecting a paper story. The final pass tests stable observable traits against transfer-form-specific response mappings, repairs DR/R cross-fitting, evaluates latent subjective dimensions, amount context, policy value, response quality, and generalizability, and separates strongest facts from strongest nulls.

### Files changed

- `FINAL_EXPLORATION_AUDIT.md`: estimands, transformations, cross-fitting, psychometrics, policy evaluation, quality screens, external benchmarks, limitations, and deviations.
- `FINAL_EXPLORATION_RESULTS.md`: Q1–Q8 results plus the required A–G synthesis and positioning audit.
- `analysis/final_exploration.py`: reproducible final pipeline.
- `tables/final_*.csv`: aggregate-only results.
- `figures/final_*.png`: seven candidate main-text figures.

### Key implementation decisions

- Used outer cell-stratified folds and inner nuisance folds for standard DR; used Robinson residualization without treatment in the marginal outcome nuisance for R learning.
- Evaluated treatment-effect rankings only on untouched outer folds and treated calibration/top-bottom agreement across learners as primary ML evidence.
- Estimated domain PCA loadings in a discovery half and evaluated scores in held-out observations.
- Used OOF policy assignments and randomized-design IPW; no respondent-level predictions were exported.
- Used official census margins descriptively but did not rake incompatible online-adult and total-population frames.

### Testing performed

- Executed all final analysis modules against the specified Stata delivery and generated the aggregate tables and seven figures.
- Confirmed N_R=5,497, N_A=5,480, and N_C=5,171 in the reproducible output.
- Syntax-compiled the final script after compatibility fixes.
- Visually inspected a contact sheet containing all seven final figures.
- Verified aggregate output schemas and excluded respondent-level scores, OOF predictions, and fold assignments.

### Acceptance Criteria

- Stable-trait versus form-specific prediction, cross-form transfer, and decomposition: met.
- Standard cross-fitted T/DR/R HTE for all three contrasts: met; causal forest unavailable and documented.
- Subjective incremental prediction, practical-equivalence bounds, and outcome sensitivity: met.
- Held-out latent dimensions and HTE: met.
- Amount, Medical-vs-Food, policy-value, response-quality, and generalizability analyses: met with documented limits.
- Required final audit/results and exact A–G synthesis: met.
- No premature paper story and no respondent-level data committed: met.

### Known issues

- No reliable causal-forest dependency was available, and no fragile package was installed.
- Policy value is evaluated with honest IPW but not a second DR policy estimator.
- The delivery lacks timing, IP/device, attention checks, realized expenditure, or independent replication.
- Population benchmarks are not sufficiently compatible for defensible raking.

### Git

- Branch: `feature/consumer-survey-initial-audit`
- Final exploration commit: this section is part of the final exploration commit.
- PR: https://github.com/Attention0/todo-list/pull/3
- Merge status: not merged.

## Nature-series locked empirical package update

### Summary

Implemented the fixed `NATURE_EMPIRICAL_ROADMAP.md` and `NATURE_FIGURE_BLUEPRINT.md` against the existing survey delivery. This is a locked post-hoc re-estimation, not a new open-ended story search or prospective confirmation. The package adds formal portability and HTE-asymmetry tests, reliability sensitivity, common global folds, quality-screen HTE/prediction, cross-fitted DR policy value, amount and policy seed stability, and publication-scale candidate figures. The results explicitly downgrade Nature-style claims that fail quality or measurement checks.

### Files changed

- `NATURE_EMPIRICAL_AUDIT.md` and `NATURE_EMPIRICAL_RESULTS.md`.
- `analysis/nature_empirical.py` and `analysis/nature_figures.py`.
- 67 aggregate `tables/nature_*.csv` files, including 27 figure-panel source CSVs.
- Six main and ten Extended Data figures, each in vector PDF and 600-dpi PNG, plus `figures/nature_figure_legends.md`.

### Key implementation decisions

- All headline ML comparisons inherit a single global five-fold assignment stratified by the nine randomized cells; level prediction uses the same two repeated partitions for all feature sets and models.
- The Food-versus-Medical HTE predictability contrast directly bootstraps calibration and top–bottom differences, with shared Cash respondents resampled jointly.
- Reliability adjustment is explicitly a scenario calculation, not an estimate.
- DR policy evaluation uses OOF form-specific nuisance predictions and known randomized assignment propensity.
- Quality screens remain sensitivity checks and are never used to silently redefine the primary estimand.

### Testing performed

- Ran the full empirical pipeline end to end on the specified external Stata file; completed with R=5,497, A=5,480, C=5,171 and ten fixed HTE seeds.
- Executed the ten-seed amount-specific stability extension and generated all 16 figure pairs from aggregate tables.
- Re-rendered figure PDFs and visually inspected the six-figure portfolio and selected Extended Data panels after correcting crowded labels and direct-comparison scales.
- Verified 16 single-page vector PDFs, 16 600-dpi PNGs, panel source data, and no exported respondent-level observations or OOF predictions.

### Acceptance Criteria

- Formal portability, reliability, Food-versus-Medical HTE asymmetry, common folds, quality-screen predictability/HTE, DR policy, and repeated-seed stability: met.
- Roadmap theory-guided/amount/inframarginal/RI/FE checks and generalizability diagnostics: met, with explicit no-raking limitation.
- Six main figures, ten Extended Data figures, panel CSVs, legends, audit/results: met.
- No changed core estimand, no new paper story, no respondent-level data committed: met.

### Known issues

- Outcome reliability is not observed; under plausible assumed reliability, the true cross-form correlation could be materially higher than the observed one.
- Medical−Cash HTE is formally more predictable than Food−Cash but Q1/Q2 quality-screen validation is inconclusive; it is not yet an unqualified Nature-style main claim.
- The study remains hypothetical, post hoc, single-sample, and without realized-spending validation.

### Git

- Branch: `feature/consumer-survey-initial-audit`
- Nature empirical package commit SHA: `098ceb84d3a0479bdd6a14176400d9fb31bd9539`
- PR: https://github.com/Attention0/todo-list/pull/3
- Merge status: not merged.
