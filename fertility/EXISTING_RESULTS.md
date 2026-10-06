# Fertility Geography Project — Existing Results

## Provenance warning

Many outputs exist, but not all were rebuilt after the 2026-09-14 spouse and 2017 fertility revisions. Only the revised final export and recorded sensitivity reruns should be treated as current without regeneration.

## Current revised result

The short-run model compares years +1/+2 with -5…-2 and scales the coefficient to a 10‰ higher destination-origin pre-three-year CBR gap. Existing controls and two-way origin/destination province clustering are retained.

| Sample | Women | Estimate (pp) | SE (pp) | p |
|---|---:|---:|---:|---:|
| Previous main sample | 20,559 | 2.98 | 0.82 | 0.0010 |
| Revised incl. 2017 | 21,383 | 2.86 | 0.84 | 0.0020 |
| Exclude month contradictions | 21,255 | 2.82 | 0.84 | 0.0021 |
| Also exclude explicit multi-city | 20,997 | 2.81 | 0.85 | 0.0025 |
| Require known month consistency | 20,436 | 2.86 | 0.89 | 0.0032 |

The association is stable under these filters; this does not solve destination selection, hukou-origin error, or retrospective measurement.

## Output inventory

| Output family | Producing code | Content | Status |
|---|---|---|---|
| `data_revision_20260914/final_analysis/` | revision + base/panel builders | Current women/panel files | Source of truth |
| `province_exact_year_exploration/` | `province_exact_year_exploration.py` | Events, parity, marriage-status heterogeneity, proxy checks | Verify run/input date before citation |
| `marriage_fertility_geography/` | marriage/fertility scripts | Marriage and birth events, gaps, mechanisms | Mixed vintage; 2017 cannot enter marriage timing |
| `.../aer_deepening/` | `marriage_fertility_aer_deepening.py` | Dose response, parity, robustness, placebos | Provisional until rebuilt |
| `phase_reports/phase1` | `phase1_exploratory.py` | Descriptives/binned scatter | Descriptive |
| `phase_reports/phase2–5` | event, ATE, margins, place-FE scripts | Event/DiD/parity/place effects | Historical specifications |
| `strict_aer/` | strict Python + Stata scripts | City marriage-gap analyses | Different 67,668-woman city estimand; not current province main sample |

For example, `strict_key_results.csv` reports negative post×marriage-gap and parity margins. These belong to the distinct city/marriage-gap construction and must not be presented as validation of the revised province-CBR estimate.

## Before paper use

1. Point retained scripts explicitly to final revised files.
2. Rebuild only agreed core tables/figures.
3. Archive or watermark superseded reports.
4. Save model metadata and input hashes in a result manifest.
5. Keep city/marriage analyses separate until samples and treatments are harmonized.
