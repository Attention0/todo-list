# Sample Re-Audit Flag Dictionary

| Variable | Definition |
|---|---|
| `core_mover_master` | Meets only hard mover/fertility-history eligibility |
| `origin_quality_tier` | A observed previous; B inferred direct-from-hukou; C hukou only; D insufficient |
| `origin_type` | Provenance-preserving origin label |
| `origin_is_previous_residence` | True only for directly observed prior residence; false in current base |
| `origin_is_hukou` | Best origin derives from hukou |
| `origin_inference_reason` | Exact evidence used for B or hukou-only fallback |
| `migration_history_tier` | B strong inferred directness; C arrival observed/route uncertain; D invalid/contradictory |
| `fertility_history_tier` | A direct child year/month; B reliable year only; C roster/zero assumption; D unusable |
| `marriage_history_tier` | A year/month; B year only; C current status only; D insufficient |
| `geography_class` | Cross-county, cross-prefecture, cross-province, nonmove, or insufficient |
| `move_cross_county/prefecture/province` | Nested transition flags |
| `move_reason_redesign` | Mutually exclusive harmonized reason group |
| `pre_years`, `post_years` | Available reproductive-age pre years and interview-censored post years |
| `has_pre1/3/5`, `has_post1/3/5` | Event-side support flags |
| `balanced_pm1/3/5` | Both pre and post support at the stated horizon |
| `earliest_event_time`, `latest_event_time` | Individual unbalanced event-time range |
| `eligible_birth_event` | Fertility tier A–C |
| `eligible_first/second/higher_birth` | Outcome-specific birth eligibility/risk-set flags |
| `eligible_marriage_event` | Marriage tier A/B |
| `legacy_21383` | Exact membership in corrected legacy final sample |
| `legacy_cbr_match` | Exact legacy treatment-sample membership; conservative match diagnostic for the broad master |
