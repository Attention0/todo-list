# Fertility Project — Second-Round Sample Re-Audit

## Scope

This audit uses the corrected 2026-09-14 woman-level base and estimates no causal model. Script: `fertility/sample_reaudit.py`.

## Hard-eligibility funnel

| step                  |   before |   removed |   remaining |
|:----------------------|---------:|----------:|------------:|
| research_universe     |   433369 |         0 |      433369 |
| valid_id              |   433369 |         0 |      433369 |
| valid_birth_year      |   433369 |         0 |      433369 |
| valid_destination     |   433369 |         0 |      433369 |
| valid_arrival_year    |   433369 |     10299 |      423070 |
| coherent_event_timing |   423070 |      2245 |      420825 |
| some_origin           |   420825 |         0 |      420825 |
| dated_fertility       |   420825 |     58502 |      362323 |
| mover_scope           |   362323 |        78 |      362245 |

The hard criteria do not require cross-province movement, work/business reason, a balanced window, marriage timing, or an external place-data match. Arrival month is not required because annual event time only needs arrival year.

## Core Mover Master

**N = 362,245.** Definition: woman in 2012–2017 with valid ID and birth year; identifiable destination; coherent current-arrival year implying age 15+ and arrival no later than interview; some origin concept; usable dated fertility history (tiers A–C); and mover scope 1–3.

### Origin quality

| category   |      n | share_core_master   |
|:-----------|-------:|:--------------------|
| C          | 193709 | 53.47%              |
| B          | 168536 | 46.53%              |

No wave directly observes residence immediately before the current destination in a form adequate for Tier A. Tier B is explicitly inferred from exact leave/arrival month or a reported single spell/city; Tier C is hukou-only.

### Geography

| category                         |      n | share_core_master   |
|:---------------------------------|-------:|:--------------------|
| cross_province                   | 183840 | 50.75%              |
| cross_prefecture_within_province | 112487 | 31.05%              |
| cross_county_within_prefecture   |  65918 | 18.20%              |

### Event-window support

| category   |      n | share_core_master   |
|:-----------|-------:|:--------------------|
| True       | 331779 | 91.59%              |
| False      |  30466 | 8.41%               |

| category   |      n | share_core_master   |
|:-----------|-------:|:--------------------|
| True       | 220049 | 60.75%              |
| False      | 142196 | 39.25%              |

| category   |      n | share_core_master   |
|:-----------|-------:|:--------------------|
| False      | 223061 | 61.58%              |
| True       | 139184 | 38.42%              |

Full `r=-10,...,+10` counts are in `SAMPLE_TIER_COUNTS.csv`.

### Move reasons

| category             |      n | share_core_master   |
|:---------------------|-------:|:--------------------|
| work_business        | 231814 | 63.99%              |
| missing              |  59632 | 16.46%              |
| family_reunification |  57359 | 15.83%              |
| marriage             |   8875 | 2.45%               |
| other                |   2870 | 0.79%               |
| housing              |   1438 | 0.40%               |
| education            |    257 | 0.07%               |

### Family and migration history quality

| category   |      n | share_core_master   |
|:-----------|-------:|:--------------------|
| A          | 282082 | 77.87%              |
| C          |  80163 | 22.13%              |

| category   |      n | share_core_master   |
|:-----------|-------:|:--------------------|
| A          | 281858 | 77.81%              |
| C          |  80387 | 22.19%              |

| category   |      n | share_core_master   |
|:-----------|-------:|:--------------------|
| C          | 193709 | 53.47%              |
| B          | 168536 | 46.53%              |

## Legacy-sample selection

### Sequential legacy funnel within the redesigned master

| step                                        |   before |   removed |   remaining |
|:--------------------------------------------|---------:|----------:|------------:|
| Core Mover Master                           |   362245 |         0 |      362245 |
| Cross-province                              |   362245 |    178405 |      183840 |
| Approximate direct migration                |   183840 |    102491 |       81349 |
| Balanced ±5                                 |    81349 |     41445 |       39904 |
| Work/business reason                        |    39904 |      7919 |       31985 |
| Legacy external-data match/final membership |    31985 |     11422 |       20563 |

### Standalone loss from each legacy restriction

| restriction                                 |   excluded_if_applied_alone |   share_excluded |
|:--------------------------------------------|----------------------------:|-----------------:|
| Cross-province                              |                      178405 |            0.492 |
| Approximate direct migration                |                      193709 |            0.535 |
| Balanced ±5                                 |                      223061 |            0.616 |
| Work/business reason                        |                      130431 |            0.360 |
| Legacy external-data match/final membership |                      340990 |            0.941 |

The intermediate direct-migration flag is the redesigned Tier B proxy. The last row uses exact membership in the corrected legacy final export, so it absorbs the legacy CBR merge and any remaining historical implementation details.

### Composition comparison

| sample                |      N |   survey_year_mean |   move_year_mean |   age_move_mean |   years_since_arrival_mean |   children_mean |   parity_at_move_mean |   pre_birth_rate |   post_birth_rate |   work_share |   cross_province_share |   balanced_pm5_share |
|:----------------------|-------:|-------------------:|-----------------:|----------------:|---------------------------:|----------------:|----------------------:|-----------------:|------------------:|-------------:|-----------------------:|---------------------:|
| Core Mover Master     | 362245 |           2014.718 |         2009.547 |          30.540 |                      5.172 |           1.304 |                 0.931 |            0.057 |             0.095 |        0.640 |                  0.508 |                0.384 |
| Balanced ±3           | 220049 |           2014.757 |         2007.291 |          30.115 |                      7.465 |           1.386 |                 0.901 |            0.056 |             0.074 |        0.648 |                  0.514 |                0.633 |
| Balanced ±5           | 139184 |           2014.829 |         2005.524 |          30.226 |                      9.305 |           1.452 |                 0.922 |            0.057 |             0.062 |        0.660 |                  0.531 |                1.000 |
| Legacy 21,383 overlap |  21255 |           2015.330 |         2007.412 |          28.743 |                      7.918 |           1.389 |                 0.867 |            0.057 |             0.068 |        1.000 |                  1.000 |                1.000 |

Additional composition checks show the same selection mechanism: ±3 and especially ±5 retain earlier movers with longer observed post-arrival duration. Education, hukou nature, current marital status, survey wave, origin province, and destination province remain descriptive stratifiers rather than eligibility rules; their reusable flags and tier counts are preserved in the script/output architecture.

The legacy 21,383 is a treatment-matched cross-province, approximate-direct, balanced ±5, work/business subsample. Its membership is retained only as `legacy_21383`; it does not define the master. The available final export provides an exact lower-bound CBR-matched indicator, but a full CBR match re-merge for every master observation remains a separate data-engineering step.

## Balanced-window selection

Compared with the unbalanced master, ±5 mechanically favors earlier move cohorts, longer destination duration, and respondents old enough to supply five pre-arrival reproductive-age years. Therefore unbalanced support should be the default architecture and balanced windows robustness samples.

## Final recommendations

1. **Core Mover Master:** the 362,245-woman definition above.
2. **Origin tiers:** use B and C jointly with explicit labels; Tier B count 168,536, Tier C count 193,709; no verified Tier A.
3. **Geographic scope:** retain cross-county, cross-prefecture, and cross-province movers; use scope-specific estimands.
4. **Event support:** use unbalanced person-years; require only the event times a specification consumes; report ±3/±5 robustness.
5. **Move reason:** retain all categories in master; define work/business and non-marriage subsets at estimation.
6. **Fertility quality:** A/B for main birth events; C included with a 2017 exclusion sensitivity; D excluded.
7. **Marriage quality:** A/B only for marriage events; current-status-only Tier C stays in fertility master.
8. **Main birth event study:** origin B/C, migration B/C, fertility A/B plus separately flagged C, and event-time-specific support.
9. **Strict robustness:** origin B, migration B, fertility A, no contradiction or explicit multiple move.
10. **Marriage geography:** 2012–2016 marriage tiers A/B; do not force this restriction on fertility analyses.
11. **Future prefecture analysis:** primarily 2017 city/county-origin observations after administrative harmonization; origin B preferred.
12. **Legacy CBR sample:** treatment-matched estimation subsample only, never the research master.
