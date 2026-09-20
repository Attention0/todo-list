# Fertility Geography Project — Sample Construction

## Source of truth and sample rule

Use `output/data_revision_20260914/final_analysis/`. This is a pooled repeated cross-section expanded retrospectively from birth histories; `mother_id` is not a cross-wave panel ID.

The final sample keeps women surveyed in 2013–2017 who report a cross-province current move with distinct valid provinces, have current-arrival timing and satisfy the approximate direct-move rule, meet the birth-history convention, have a balanced `-5...+5` window at ages 15–45, report work/business as current-move reason, and match province CBR inputs.

## Sample funnel

| Step | Before | Removed | Removed % | Remaining |
|---|---:|---:|---:|---:|
| Harmonized 2012–2018 female base | — | — | — | 507,225 |
| Keep 2012–2017 | 507,225 | 73,856 | 14.56% | 433,369 |
| Cross-province scope | 433,369 | 216,600 | 49.98% | 216,769 |
| Valid different provinces | 216,769 | 2,037 | 0.94% | 214,732 |
| Arrival + approximate direct move | 214,732 | 92,624 | 43.13% | 122,108 |
| Birth-history convention | 122,108 | 19,857 | 16.26% | 102,251 |
| Balanced ±5, ages 15–45 | 102,251 | 60,094 | 58.77% | 42,157 |
| Work/business move | 42,157 | 13,499 | 32.02% | 28,658 |
| Province CBR gap available | 28,658 | 7,275 | 25.39% | **21,383** |

Counts are from `final_analysis/sample_funnel.csv`.

## Final sample by wave

| Year | Base women | Final women | City-origin precision | Birth in +1…+5 |
|---:|---:|---:|---:|---:|
| 2012 | 74,380 | 0 | 0 | 0 |
| 2013 | 92,067 | 4,666 | 0 | 1,377 |
| 2014 | 7,200 | 363 | 0 | 109 |
| 2015 | 96,692 | 4,721 | 0 | 1,463 |
| 2016 | 80,912 | 6,814 | 0 | 2,213 |
| 2017 | 82,118 | 4,819 | 4,819 | 1,525 |
| 2018 | 73,856 | 0 | 0 | 0 |

## Final structure

- 21,383 respondents and 235,213 person-years; exactly 11 periods each.
- Base migration scopes: 252,798 cross-province, 161,734 province-internal cross-city, 92,602 city-internal cross-county, 20 coded nonmovers, 71 missing.
- Final sample has no stayers, 31 origin provinces, and 31 destination provinces. OD-pair quantiles were not saved and remain a follow-up diagnostic.
- Origin precision: 16,564 province-only (77.46%), 4,819 city/county-capable (22.54%; all 2017).
- Move cohorts 2003–2012; event years 1998–2017.
- Mean age at move 28.75 (P25 24, median 28, P75 34, range 20–40).
- Arrival family stage: unmarried 3,654; married/no child 1,780; married/one child 6,878; married/2+ 4,094; uncertain 4,977.
- 6,687 women (31.27%) have a birth in years +1…+5; 14,696 do not.

## Assumptions and validation

- Origin is mainly survey-time hukou province, not observed prior residence.
- Direct move means same-year first departure/current arrival or, for 2016, one reported migration.
- 2017 women with no roster child are assigned zero children.
- The balanced window selects moves far enough before interview to observe +5.
- Work movers are selected and do not supply exogenous destinations.

The final export verifies unique IDs and person-year keys, 11 periods per woman, birth/parity identities, CSV/DTA agreement, and reproduction of the revised short-run estimate.
