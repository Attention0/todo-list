# Data reconciliation — 2026-10-04 work order

Audit executed 2026-10-06. Scope: Stages A/B of the appended WORK instructions, before mechanisms. Verdicts use **Confirmed**, **Partially confirmed**, **Incorrect**, **Unknown**. Evidence labels distinguish **Observed fact**, **Reconstruction**, **Assumption**, and **Unknown**. Counts below are unweighted; a nonmissing field is not necessarily a valid value or a complete lifetime history.

## Evidence and reproducibility

Source project: `/home/liuze/project-cmds_fertility` (P below). Current data: `P/output/data_revision_20260914/cmds_2012_2018_mother_base_variables_FIXED.csv`; legacy export: `P/output/data_revision_20260914/final_analysis/fertility_main_women.csv`. Both were reread, not inferred from prior reports. Aggregate results and input SHA-256 hashes: [reconciliation_evidence.json](audit/reconciliation_evidence.json). Diagnostic code: [reconcile_20261004.py](audit/reconcile_20261004.py); frozen published sample rule: [sample_definition_20260920.py](audit/sample_definition_20260920.py).

Evidence index:

- E1: `P/code/rebuild_main_base_fixed.py`, `build_2012`–`build_2018`, `finalize`, `add_spouse_fields`; lines 392–975 and variable notes 1153–1375.
- E2: `P/code/build_main_panel_40cols.py`, `build_panel`, lines 125–255: calendar range, child-date cleaning, parity and location construction.
- E3: `P/code/marriage_fertility_geography.py`, `load_external`, `pcode`, `mean_gap`, `attach_treatments`, lines 59–188.
- E4: `P/work/audit_20260914/*metadata.json` and `2017_pandas_labels.json`; saved raw-file row counts and labels.
- E5: `P/work/audit_20260914/cmds2017技术文件.pdf.txt`, lines 57–62, 171–172; A questionnaire text, question 100 and questions 412–418.
- E6: actual `/mnt/g/桌面/科研/数据-CMDS流动人口/cmds2017a卷.dta`, column inventory and selected raw intention fields, joined to master IDs.
- E7: prior branch `feature/fertility-audit` at `b2458db`, sample script and reports; preserved as historical evidence, not overwritten.
- E8: `P/work/revision_20260914/sample_profile_export.py`, `P/output/data_revision_20260914/main_sample_sensitivity.csv`, legacy sample exports.

Run under WSL with pandas, NumPy and openpyxl: `python3 fertility/audit/reconcile_20261004.py`. Source microdata are read only. The real-ID 51-row diagnostic history stays outside the repository; only aggregates are published.

## A. Main sample and survey structure

| Checklist row | Verdict | Verified evidence and interpretation |
|---|---|---|
| A1 Survey structure | Confirmed | E1 constructs `mother_id = wave + respondent ID`; 507,225 distinct IDs, no duplicates. This is not evidence that persons never recur: no verified persistent cross-wave linkage exists. Repeated cross-section plus retrospective reconstruction, not observed longitudinal residence. |
| A2 Survey years | Partially confirmed | Current female base covers 2012–2018. Broad published population covers 2012–2017; see wave table. Saved metadata also show 2009 N=87,084; 2010 migrant/local comparison files each N=8,200; 2011 N=128,000. These older/special samples are not interchangeable with the national female base. |
| A3 Broad main sample | Partially confirmed | Reproduced N=362,245 exactly. It retains all reasons/scopes and does not require CBR match or balance. It nevertheless requires arrival at age 15+, an origin proxy and complete dated child counts. The age-at-arrival rule excludes childhood arrivals; completeness can select on current marriage/module routing. These are substantive restrictions, not automatically indispensable for every outcome. |
| A4 Sex/age and outcome risk sets | Partially confirmed | E1 selects female respondents, not all migrants. Person-years in E2 use ages 15–45, from max(1990,birth year+15) to min(survey year,birth year+45). The 362,245 population contains 22,612 women arriving after 45 and 53,638 surveyed after 45. Keep them in a population inventory, but do not include out-of-risk person-years in annual fertility hazards. Marriage eligibility must not require a birth-history module. |
| A5 Current migrant selection | Confirmed for main A sample; blanket absence of locals is Incorrect | E5 samples nonlocal-hukou residents present at least one month, aged 15+ in 2017. Returnees no longer at the sampled destination are not observed there. However, 2017 D and 2010 local comparison files exist; “CMDS has no nonmigrants anywhere” is false. Their comparability/history suitability has not been established. |

### Wave reconciliation

Raw N is the local file's saved metadata count (not a claim about every national release). Date counts refer to the female base, not the master.

| Wave | Raw file N | Female base | Published broad master | Marriage year observed | Arrival month observed |
|---|---:|---:|---:|---:|---:|
| 2012 | 158,556 | 74,380 | 59,632 | 59,914 | 0 |
| 2013 | 198,795 | 92,067 | 72,757 | 74,805 | 92,067 |
| 2014 | 16,024 | 7,200 | 5,467 | 5,484 | 7,200 |
| 2015 | 206,000 | 96,692 | 76,743 | 77,242 | 96,692 |
| 2016 | 169,000 | 80,912 | 67,483 | 68,064 | 80,912 |
| 2017 | 169,989 | 82,118 | 80,163 | 0 | 82,118 |
| 2018 | 152,000 | 73,856 | 0 | 63,413 | 73,856 |

2012 stays in the broad population despite unavailable comparable current-move reason. 2018 has marriage/cohabitation dates for 63,413 women but no origin in the current extraction, so it is unavailable for the current OD design, not universally unusable for marriage research. 2014 is a small local file; national representativeness of this supplied subset is Unknown.

### Published hard funnel and what it actually excludes

Selected missing shares in the female base (structural routing included, not interpreted as nonresponse):

| Wave | Marriage year missing | First-leave year missing | Arrival month missing | Child total missing |
|---|---:|---:|---:|---:|
| 2012 | 19.45% | 0.00% | 100.00% | 19.39% |
| 2013 | 18.75% | 0.36% | 0.00% | 18.75% |
| 2014 | 23.83% | 0.00% | 0.00% | 23.83% |
| 2015 | 20.12% | 0.00% | 0.00% | 20.12% |
| 2016 | 15.88% | 100.00% | 0.00% | 15.88% |
| 2017 | 100.00% | 0.00% | 0.00% | 0.00% |
| 2018 | 14.14% | 100.00% | 0.00% | 14.14% |

433,369 women (2012–2017) → valid arrival at age 15+ and no later than interview: 423,070 → first-leave/arrival coherence: 420,825 → dated child-count completeness: 362,323 → mover scope 1–3: 362,245. ID, birth year, destination and some origin remove zero additional records in the published sequence. Timing coherence removes 2,245 at its stage; 1,715 of those would otherwise survive the later birth/scope filters. Thus the previous 363,960-to-362,245 change and the funnel's 2,245 are different denominators, not contradictory counts.

The master is retained as the audit starting population. No exclusions below redefine it. A future marriage master should start from the female base with valid marriage-risk information, rather than conditioning on having complete births.

**Observed selection:** all **63,336 currently unmarried women in the 2012–2016 female base are absent from the published master** (by wave: 14,071 /17,096 /1,716 /17,605 /12,848). Its 10,325 currently unmarried women all come from 2017. This is not a balanced representation of marriage/first-birth risk: conditioning on future marriage/fertility-module availability can select retrospective childless person-years too. Complete-date construction alone does not solve it. Do not code excluded women as zero births without checking survey routing and their outcomes.

## B. Geography and migration history

### B1 Origin definitions

| Origin concept | Verdict | Exact fields/source | Years and level | Observed/inferred; missingness | Interpretation |
|---|---|---|---|---|---|
| Hukou origin | Confirmed | `origin_province_code` from `resi_place_1` (2012–13), `Q101J1` (2016); `origin_raw` from `resi_place_1` (2014); `origin_province_name` (2015); `origin_county_code/name` from `q101j1a/b` (2017) | Province common in 2012–17, county in 2017 | Observed registered location; nonmissing in those waves. Province harmonization still fails for 1,650 master women | Preserve raw field and source; `origin_best_available` mixes names/codes and is not itself a merge key |
| Residence immediately before current destination | Unknown in raw material; unavailable in harmonized base | No verified previous-residence field; `origin_quality_tier=B` uses leave/arrival equality or single move/city reports | Proxy across waves; no verified Tier A | 168,536 inferred B; 193,709 hukou-only C; actual previous residence missing for the full master | Same-month departure/arrival and one-city reports do not establish continuous direct residence |
| Birthplace/upbringing | Unknown | No verified harmonized field in 215-column base | Not established | Do not report a measured missing percentage for a nonexistent field | Hukou cannot silently substitute |
| First place left / first destination | Partially confirmed | `first_leave_year/month` dates departure from hukou; 2017 `first_move_city_code/name` from `Q304A/B` is first migration destination, not previous residence | 2017 first destination nonmissing for all 82,118 base women; first departure years 2012–15,2017 | Observed reports with incomplete trajectory | Do not relabel first destination as last origin |

### B2 Destination

Confirmed: `dest_province_name/dest_city_name/dest_county_name` are derived from residence/survey geography (`C1/C2/C3` in later waves); all are nonmissing in the current base. These are current-location fields, not annual addresses. Province is the common **coded and harmonizable** OD level; 2017 alone supplies 80,163 broad-master county-origin codes. Extracting the first four county-code digits is a provisional prefecture key, not a validated historical boundary crosswalk. Municipality, county-to-district and suppressed/invalid codes require validation. External keys: province×year now; city/county×year after crosswalk. Current city strings must not be equated across waves without harmonization.

### B3 Timing

| Event | Verdict | Exact source | Coverage in base | Interpretation |
|---|---|---|---|---|
| Current arrival | Confirmed | 2012 `flo_time_1`; 2013–14 `floyear_1/flomon_1`; 2015 `q101k1y/m`; 2016 `Q101M1Y/M`; 2017 `q101m1y/m`; 2018 `Q101MY1/MM1` → `current_arrive_year/month` | Year all seven waves; month absent 2012, available later | Reported current-destination arrival, not necessarily latest uninterrupted spell |
| First departure from hukou | Confirmed, partial waves | `fir_away`, `fir_away_Y/M`, `Q201Y/M`, `Q302Y/M` → `first_leave_year/month` | 2012–15,2017; 294,707/362,245 master years present (18.644% missing) | Distinct from arrival |
| First migration | Partially confirmed | 2016 `Q202B` → `first_move_start_year` | 14,311/80,912 base nonmissing (82.31% missing/routed) | Builder deliberately does not place it in `first_leave_year` |
| Latest move / every spell | Unknown/unavailable | No verified complete sequence | No usable full-history count | Cannot prove arrival is latest spell or uninterrupted exposure |
| Duration | Confirmed as reconstruction | `survey_year-current_arrive_year` | All master | Integer-year approximation, not person-month exposure |

### B4 Multiple moves

Partially confirmed. `migration_count_total` (2016) and `migration_city_count_total` (2017) are different objects, not a common move counter. Explicit multi-move/city reports occur for 47,759 women (13.18% of master); others are not proven single movers. The one-move report subset has 54,703 women, the one-city subset 45,183; equal first-leave/current-arrival year gives 147,388; inferred B gives 168,536. These are alternative diagnostic sets, not additive counts. Previous/intermediate residence spells are unavailable. Recent arrival ≤2 years retains 135,208, but cannot rule out earlier moves or return visits.

### B5 Migration motives

Additional partial trajectory fields in 2016 are observed: `Q201` → `migration_count_total`; `Q202A` → `this_move_start_year`; `Q202B/Q203B` → first migration start/end; `Q204AX/Q204BX` → this/first migration province; `Q207` → cumulative out-migration duration. These are first/current endpoints, not every intermediate residence. Their wording and discrepancies with roster arrival need a separate spell-level reconciliation before interpreting duration as continuous exposure. In 2017 `Q307` counts cities. Neither field is a common-wave complete move count.

Partially confirmed. Harmonized reason combines work and business; it does not identify random assignment or distinguish all job transfers. `classify_move_reason` in E1 maps wave-specific codes; 2012 has no comparable current reason. No verified separate hukou-motive category exists in the master. Child education cannot automatically be equated with respondent study/training.

| Harmonized current reason | N | Share of master |
|---|---:|---:|
| `work_business` | 231,814 | 63.99% |
| `missing` | 59,632 | 16.46% |
| `follow_family` | 47,636 | 13.15% |
| `marriage` | 8,875 | 2.45% |
| `care_family` | 6,290 | 1.74% |
| `kinship_network` | 2,959 | 0.82% |
| `other` | 2,869 | 0.79% |
| `demolition_move` | 1,438 | 0.40% |
| `elderly_migration` | 474 | 0.13% |
| `study_training` | 257 | 0.07% |
| `military` | 1 | 0.00% |

The absence of retained “birth” cases is not evidence that fertility never motivated migration. Missing reasons must not be coded as nonfamily/work.

## C. Marriage and fertility histories

| Checklist item | Verdict | Evidence, dates and research boundary |
|---|---|---|
| C1 Current marital status / ever married | Partially confirmed | `mother_marital_status` available in all waves; codes include unmarried, first marriage, remarriage, divorce, widowhood, and later cohabitation. Survey-time status permits a proxy for ever married, not complete transitions. |
| C1 First-marriage age/year/month | Partially confirmed | 2012 `firmarr_time` parsed YYYYMM; 2013–14 `firmarr_y/m`; 2015 `Q305Y/M`; 2016 `Q404Y/M`; 2018 `Q312Y/M`. Dates are reported/parsed, not survey-age algebra. 2016/2018 wording includes living together. Current master has 281,858 dated records, 80,387 missing (22.191%). |
| C1 Divorce/remarriage/widowhood histories | Incorrect if claimed reconstructable | Current states are not dated complete histories; `year>=first_marriage_year` means ever-married proxy, not necessarily currently married at every t. |
| C1 Spouse residence/origin/co-residence, education/job/income | Partially confirmed | E1 locates spouse by relation code 2 across slots 2–10; `spouse_education/hukou_nature/marital_status` are survey-time reports, not baseline covariates. Roster residence can support present-location reconstruction with raw extraction; geographic spouse origin, past co-residence, occupation/income histories are not verified in this base. |
| C2 Children ever born versus living/roster children | Partially confirmed | `children_total_reported`, `children_existing_reported` and child slots have different source semantics. 2017 is roster-derived, including zero when no child listed; it is not validated lifetime CEB. |
| C2 Child years/months, order, first/second/higher/last birth | Partially confirmed | `child1...child9_birth_year/month`; direct fertility modules in 2012–16 and 2018, household roster in 2017. Sort dated events and handle same-year multiples; “first listed” need not be lifetime first if roster omits children. No future child dates in master; 29 women have child dates before maternal age 10, removed from events by E2 but retained in the base. |
| C2 Pregnancy, intentions, ideal children, contraception/family planning | Partially confirmed/Unknown | 2015 pregnancy-location/history fields (`q307e1...5`) concern prior births, not a conception-date history. Health-education fields exist (2017 `Q404C`). Broad comparable intentions/ideal-child/contraception histories are not harmonized; absent data must not become zeros. |
| C3 Births ≥2–3 years before, year before, migration year, after | Confirmed as dated-event reconstruction; residence interpretation assumed | For r=-3,-2,-1,0,+1,+2,+3, women with a listed birth number 23,820;25,360;29,582;33,249;28,228;17,901;13,050. These are event counts, not hazard rates: age, censoring and risk-set denominators differ. |
| C3 Pregnancy immediately before migration | Partially confirmed | Birth month minus assumed gestation is an inferred conception proxy; gestational length/pregnancy loss are not observed histories. Annual dates alone cannot order move-year conception. |
| C3 Marriage near arrival / marriage-to-first-birth | Partially confirmed | Marriage counts at the same r values: 14,776;17,046;20,824;26,985;9,051;6,007;4,444. Dated subset only, annual ties need months, 2012 arrival month absent, 2017 marriage unavailable. |
| C3 Fertility conditional on already married | Partially confirmed | Define marriage dated before arrival using year/month and a separate estimand; do not condition total-effect regressions on post-move marriage. Prior first marriage does not rule out divorce before the move. |

**Questionnaire/data contradiction (Observed fact):** E5 includes Q412 (first marriage/cohabitation), Q413 (number of children), Q414 (birth plans), Q415–418 (contraception/current pregnancy reason). E6 actual DTA and labels contain **none of the Q412–Q418-prefixed columns**. It is incorrect to say the 2017 questionnaire did not ask these; the available release lacks them. Recovering another release is a data-acquisition task, not imputation from current status.

Question 100 includes spouse/children in the destination, hometown and elsewhere **but excludes children who have established a separate household**. Thus “roster equals co-resident children only” is also incorrect. Completeness as lifetime fertility still requires an assumption. All 80,163 master women in 2017 correctly carry fertility Tier C in the published code.

### Dynamic risk sets that must replace survey-parity eligibility flags

For each woman-year, calculate `parity_start_t = count(child birth year < t)` after date validity checks; first-birth risk set is parity=0, second-birth parity=1, higher-order parity≥2, all with defined reproductive ages and exposure time. At arrival, annual pre-move parity counts are 126,212 at zero, 149,096 at one, 86,937 at two or more. These are not complete annual risk-set sizes. Same-year twins can cross more than one parity; outcome definitions must say whether counting births, birth occasions or mutually exclusive categories. A woman without a marriage date must not be assumed unmarried throughout. Pregnancy and marital histories have separate routing/missingness.

## D. Place-fertility measure

Confirmed: current `delta_birth_pre3` is external **province CBR**, per thousand total population, not TFR, ASFR, CMDS own-sample fertility or a city effect. E3 reads the province workbook `全国各省份人口-人口出生率、死亡率和自然增长率（2000-2021年）.xlsx`, sheet `原始数据`, columns `行政区划代码/年份/人口出生率(‰)`. It requires all three years for **both** origin and destination:
`mean(CBR_dest,arrival-3...arrival-1)-mean(CBR_hukou,arrival-3...arrival-1)`.
Underlying data vary by province×year; the pre-move average is fixed within respondent. Source workbook has zero duplicate province-year keys. Preserve the two separate means before differencing. The older city-aggregated `province_cbr_proxy` in `province_aer_exploration.py` is a different measure.

**New reconstruction:** exact current mapping and three-year completeness yield **323,949** matched master women, loss **38,296 (10.572%)**; by wave 49,612 / 64,129 / 4,998 / 70,831 / 61,263 / 73,116. There are 1,650 invalid province mappings; other losses include pre-2000 external coverage. Gap is positive for 64,440, negative for 97,068 and zero for 162,441. Province-internal moves cannot identify a within-province gradient from this province measure. The 21,255 legacy/master overlapping IDs reproduce saved gaps numerically (`np.allclose` assertion).

Legacy N=21,383 gap: mean -0.761‰, SD 3.676‰, median -1.167‰, min -13.793‰, max 11.363‰; positive 8,345, negative 13,038. It is an estimation subset, not the external match universe.

| Internal-measure check requested | Verdict for current treatment |
|---|---|
| Respondent own outcome in measure | Confirmed absent at the CMDS-record level: independently sourced aggregate; this does not remove aggregate composition bias |
| Leave-one-out, split sample, cohort/year leave-out | Not required for current external CBR; Partially confirmed as feasible future reconstructed migrant measures, not implemented/validated here |
| Minimum city cell size / reliability | Unknown for a new city measure; no validated city ASFR/TFR currently attached |
| Age/cohort/parity standardization | Incorrect if claimed present: CBR has total-population denominator |
| Ranking stability / external validation | Unknown for the redesigned master; old alternate proxies do not establish this |
| Origin/destination components retained | Reconstructed separately in this diagnostic before gap; legacy export predominantly stores gaps |

## E. Small person-year reconstruction

Confirmed as a technical reconstruction: **51 rows for 11 respondents**, selected deterministically from up to two per wave; not a representative test sample. Years limited to ages 15–45, arrival ±3 and **before** survey year to avoid partial-year exposure. The local-only CSV is recorded in evidence JSON.

| Field | Classification | Meaning |
|---|---|---|
| id | Observed identifier, harmonized | Wave-prefixed, no longitudinal linkage |
| calendar_year | Deterministic reconstruction | Explicit annual grid |
| age | Deterministic reconstruction | Calendar year minus reported birth year, not exact birthday age |
| location | Explicit assumption | Hukou before/current destination after; must not be called observed residence |
| event_time | Deterministic reconstruction | Year minus arrival year |
| marital_status | Unavailable as complete state; proxy reconstruction | Saved as `ever_married_proxy`, missing with missing first date |
| parity | Deterministic conditional on complete birth history | Birth count strictly before t |
| birth | Deterministic conditional on dates | Any listed child date in year t |

At least the 47,759 explicit multiple-move/city reporters directly undermine a single-transition interpretation; 193,709 hukou-only Tier C records lack stronger directness evidence. These counts overlap and are not additive. Even Tier B does not prove no intermediate exposure. E2 correctly labels intervals between first leave and arrival as `Gap`; the earlier audit's universal two-location diagram overstated the existing builder.

## F. CMDS-specific selection threats

| Row | Verdict | Evidence and consequence |
|---|---|---|
| F1 Stay/return/onward selection | Confirmed concern, Partially confirmed diagnostics | Arrival duration is available throughout. Raw 2017 `Q314` (intend stay) available for all 80,163 master women; `Q315` intended duration for 66,403; routed `Q317` return/other destination for 1,941; `Q318` return timing for 1,352; nonblank `Q321A` intended city code only 179. Route-specific missingness is not refusal or zero propensity. Intentions are measured after migration and do not reveal realized exits. |
| F2 Retrospective censoring | Confirmed | Move years span 1956–2017 in broad population; post history ends at interview, age limits vary. Equal event times pool different ages, cohorts, survey waves and survivor durations. Survey-year annual birth exposure is partial. |
| F3 Policy-cohort composition | Partially confirmed | 2012–17 interviews can cover pre-relaxation, selective two-child and 2016 onward universal-two-child calendar periods; no post-2021 three-child outcomes exist. Individual eligibility/local implementation histories are not established. A calendar-era label is not treatment eligibility, and migration cohort is not event calendar year. |

### Optional restriction costs (not master exclusions)

Each loss below uses N=362,245 and applies the stated flag independently. Donuts are **person-level exclusion** of any listed birth within the inclusive ±k-year interval; not a person-year donut. Combined marriage/birth costs additionally require a known marriage date and therefore exclude never-married records with no date: these are conservative dated-subset diagnostics, not recommended population definitions.

| Flag | Retained N | Loss N | Loss % |
|---|---:|---:|---:|
| `birth_direct_waves_2012_2016` | 282,082 | 80,163 | 22.129% |
| `marriage_date` | 281,858 | 80,387 | 22.191% |
| `origin_county_code` | 80,163 | 282,082 | 77.871% |
| `first_leave_known` | 294,707 | 67,538 | 18.644% |
| `same_leave_arrival_year` | 147,388 | 214,857 | 59.313% |
| `reported_one_move` | 54,703 | 307,542 | 84.899% |
| `reported_one_city` | 45,183 | 317,062 | 87.527% |
| `inferred_B` | 168,536 | 193,709 | 53.475% |
| `recent_2years` | 135,208 | 227,037 | 62.675% |
| `work` | 231,814 | 130,431 | 36.006% |
| `education` | 257 | 361,988 | 99.929% |
| `cross_province` | 183,840 | 178,405 | 49.25% |
| `within_province` | 178,405 | 183,840 | 50.75% |
| `known_nonfamily_nonmarriage` | 236,379 | 125,866 | 34.746% |
| `birth_donut_pm1` | 273,440 | 88,805 | 24.515% |
| `marriage_birth_donut_pm1_known_marriage` | 187,759 | 174,486 | 48.168% |
| `balanced_pm1_published` | 331,779 | 30,466 | 8.41% |
| `balanced_pm1_age15_45` | 308,988 | 53,257 | 14.702% |
| `birth_donut_pm2` | 236,884 | 125,361 | 34.607% |
| `marriage_birth_donut_pm2_known_marriage` | 159,048 | 203,197 | 56.094% |
| `balanced_pm3_published` | 220,049 | 142,196 | 39.254% |
| `balanced_pm3_age15_45` | 202,191 | 160,054 | 44.184% |
| `balanced_pm5_published` | 139,184 | 223,061 | 61.577% |
| `balanced_pm5_age15_45` | 125,206 | 237,039 | 65.436% |

Published balance flags ignored age 45. Age-capped ±5 retains **125,206**, versus published **139,184** (difference 13,978). These updated age-only counts still allow the survey year and pre-1990 years, unlike a stricter full-year existing-panel definition; they are not a ready regression sample. No data are silently recoded here.

## G. Mobility network and AKM feasibility

Partially confirmed. A graph of hukou-to-current-location links is computable but is not a verified residence-move graph. Legacy province graph: 31 origins, 31 destinations, 707 directed OD pairs; largest undirected connected component covers all 31 provinces; degree 25–30. OD cell P25=3, median=9, P75=27, P90=68; **236/707 (33.38%)** links have fewer than five women. This is preliminary support, not proof of AKM rank, leave-out connectedness or causal variance identification. Broad-population graph, degree and destination counts are supplied in evidence JSON. Prefecture graph requires harmonized OD codes; only the 2017 origin-detail subset is available. Historical place-FE variance is not bias-corrected causal variance.

## Contradictions and instruction precedence

The broad province graph contains 360,595 valid-OD women, 922 directed links (including same-province links), one 31-province connected component, and non-self undirected degree 30 for every province. OD P25=11.25, median=54, P75=190, P90=663.9; 130/922 links have fewer than five women. Same-province links add no cross-province identification. Counts by destination and degree are in evidence JSON; they do not establish a city-level connected sample.

1. E7's “legacy CBR match” equals final-sample membership, not a match indicator. Replace that interpretation with the 323,949 fresh remerge; prior 20,563 proxy-funnel endpoint was not a reproduction of the legacy 21,383 sample.
2. E7's event support ignores upper reproductive age and full-year exposure; survey-total parity flags are not dynamic risk sets. Its mean post birth rate includes arrival-year events but uses duration excluding that year's exposure and may include out-of-age births. Do not cite those rates as hazards.
3. “Marriage dates only 2013–16” describes the restricted legacy sample, not the source base: 2012 and 2018 also have dates; 2016/2018 wording differs.
4. “2017 questionnaire lacks marriage module” is contradicted by Q412; the available raw release lacks the fields. No attempt was made to fill this from present status.
5. “No nonmigrants” applies to the current analytic sample; local comparison releases exist. A matched nonmover design is not ready merely because those files exist.
6. Broad does not mean population-unselected: fertility completeness and age-at-arrival≥15 exclude groups. Missing-module never-married women must not be treated as zero births.
7. E2 cleans 29 impossible child histories at event construction, while E7's completeness test only counts nonmissing dates. Coherence is not fully assured by nonmissingness.
8. Initial SPEC/WORK emphasized five older audit documents and mechanism ambition. The appended 2026-10-04 instructions and the user's current instruction prioritize these two audits and defer mechanisms. SPEC/WORK and historical results are preserved.

## Facts Chat can safely treat as established

- Corrected female base N=507,225; published broad starting population N=362,245; legacy estimation sample N=21,383. They answer different questions.
- Arrival and first departure are different variables. True previous residence and continuous spells are not established.
- Provincial external CBR is already independent of the focal CMDS record; age-standardized city fertility remains unavailable.
- Current macro matching supports 323,949 master women, including many zero province-gap movers.
- Births can be dated retrospectively, with distinct direct-module and 2017 roster provenance; an annual residence panel cannot be asserted.
- Current release lacks 2017 Q412–418 despite questionnaire presence. Raw stay/return intentions do exist.
- Numerical diagnostics and the small history were actually executed; no mechanism or causal regression was estimated in this audit.

## Assumptions Chat must not silently make

- Hukou equals previous residence; a single city equals a single spell; same-year dates prove direct travel.
- Roster completeness equals lifetime births; no listed child proves lifetime childlessness.
- Current education, hukou, labor status, spouse traits or settlement intentions are pre-move covariates.
- First-marriage date reveals divorce/remarriage dates or full marital state at t.
- CBR is ASFR/TFR, or a zero province gap means no local environmental change.
- Donut exclusions identify exogenous movers; lead insignificance proves no selection; intention weighting recovers unobserved returnees.
- Broad-person counts equal valid annual hazard denominators; a connected proxy graph establishes causal AKM variance.
