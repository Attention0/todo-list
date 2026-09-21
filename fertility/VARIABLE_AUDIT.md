# Fertility Geography Project — Variable Audit

## Research-variable matrix

| Need | Variable | Years | Quality | Main issue |
|---|---|---|---|---|
| Marriage timing | `first_marriage_year/month` | 2013–2016 | Medium | Missing for 2017; harmonized wording includes marriage/cohabitation |
| Current marriage | `mother_marital_status` | 2013–2017 | High | Survey-time only |
| First birth | `child1_birth_year/month`, `first_birth_exact` | 2013–2017 | Medium/high | 2017 zero histories are roster assumptions |
| Higher births | child 2–5 dates; parity outcomes | 2013–2017 | Medium/high | Sparse high parity; 2017 roster-derived |
| Annual fertility | `birth_t`, `birth_count_t` | reconstructed 1998–2017 | Medium/high | Retrospective, not annual interviews |
| Fertility intention | Wave-specific, not in final files | varies | Not harmonized | Not part of current design |
| Origin | `origin_prov`; 2017 county/city | 2013–2017 | Province high | Hukou origin, not prior residence |
| Destination | `dest_prov`, city/county names | 2013–2017 | Province high | City codes/names require standardization |
| Migration timing | current arrival; first leave | arrival all; leave partial | Arrival high | First leave only 14,569/21,383 |
| Migration reason | unified current-move group | 2013–2017 | Good | 2012 lacks comparable question |
| Multiple moves | move count (2016), city count (2017) | 2016–2017 | Partial | No full spell sequence |
| Spouse | education/hukou/status, roster slot | 2013–2017 | Corrected | Survey-time; no spouse residence history |
| Hukou | nature + registered origin | 2013–2017 | Good | Not public-service access history |
| Merge key | province all; 2017 origin county/city | 2013–2017 | Province ready | City harmonization required |

## Fertility histories

Among 21,383 women, dated births cover 19,553 first, 9,105 second, 931 third, 98 fourth, and 12 fifth children. Child 6–9 slots are empty. `birth_t` is reconstructed from child dates; `birth_count_t` retains multiples. `first_birth_exact`, `second_birth_exact`, and `higher_birth_exact` are mutually exclusive and sum to `birth_t`.

Births can be ordered before/after current arrival using year/month. Migration-year births should not be interpreted as post-move conceptions. Pregnancy location and birth place have limited coverage (7,705 and 13,057 person-years).

In 2017, fertility is reconstructed from the household roster and no listed child is treated as zero under an explicit assumption stored in `children_count_source`.

## Marriage histories

First-marriage year/month is present for 16,564 women (182,204 person-years), supporting timing and marriage-to-first-birth analysis for 2013–2016. It is absent for all 4,819 main-sample women in 2017. Remarriage/divorce/widowhood histories are not reconstructed; current marital status is not a substitute.

## Migration histories

The cleanest event is `current_arrive_year/month`, reported arrival in the current destination. `first_leave_year/month` dates first departure from hukou and is partial. The origin is the harmonized hukou province, not the immediately prior residence. No complete intermediate-location sequence exists.

The direct-move proxy uses same-year first leave/current arrival or 2016 migration count=1. In revised sensitivities, 128 women have leave month after arrival month and 258 are explicit multi-city movers.

## Retrospective person-year feasibility

| Column | Classification | Basis |
|---|---|---|
| ID | observed/harmonized | Survey-specific respondent ID, not cross-wave |
| Calendar year | deterministic | `move_year + r` |
| Age | deterministic | year minus birth year |
| Location | assumed | Origin pre-arrival, destination post-arrival |
| Event time | deterministic | year minus current arrival year |
| Married | reconstructed | First-marriage date; unavailable 2017 |
| Birth | reconstructed | Child birth dates; 2017 zeros assumption-dependent |

Thus the exported panel is credible as dated birth history around arrival, not as a directly observed annual residence panel.

## Geography and place treatment

Province is the only common level: 31 origins and 31 destinations. Only 4,819 final women, all 2017, have origin city/county precision. City analysis needs a frozen administrative crosswalk, municipality rules, standardized destination names/codes, and match-rate reporting.

The main treatment is external province crude birth rate (CBR, per thousand):

```text
delta_birth_pre3 = mean(destination CBR, t-3:t-1)
                 - mean(origin CBR,      t-3:t-1)
```

Alternatives use arrival year or `t-1`. This is not TFR/ASFR and is unadjusted for age, cohort, marriage, or migrant composition. Because it is external macro data, the respondent's own birth does not mechanically enter it. The treatment distribution and OD-cell quantiles should be added to the final diagnostics.
