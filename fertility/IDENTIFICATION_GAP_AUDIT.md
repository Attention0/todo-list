# Identification gap audit — 2026-10-04 work order

Executed 2026-10-06. This completes Stage B using [DATA_RECONCILIATION.md](DATA_RECONCILIATION.md), raw labels/questionnaire text, corrected data, existing code and new descriptive calculations. Mechanism estimation is deferred as requested.

**A = feasible now:** observed variables and an implementable diagnostic exist; not a claim of causal validity or that a regression was run.
**B = external merge or moderate reconstruction needed:** prerequisites identified but not validated.
**C = infeasible with current data:** the required history/control population/exclusion evidence is absent.
Split rows prevent a partly feasible proposal being given an unconditional A.

Counts use published broad starting population **M=362,245**. A treatment-matched province subset is **T=323,949**, loss 38,296 (10.572%); positive/negative/zero gaps 64,440/97,068/162,441. Direct birth-module waves 2012–16 retain **D=282,082**, loss 80,163 (22.129%). Dated marriage retains **J=281,858**, loss 80,387 (22.191%). City-origin-detail subset **C17=80,163**, loss 282,082 (77.871%). Restrictions are independent unless explicitly combined; final intersections, common support and regression row counts require estimation-stage checks. “0 fixed loss” means no extra person filter, not complete covariate/treatment coverage.

## Benchmark evidence boundary

“Benchmark” below describes what the supplied IDENTIFICATION_UPGRADE_PLAN §2 reports, not independent verification of published coefficients or all appendices. Its text attributes FE, event studies, motive balance, matched nonmovers, AKM, observables, disasters, IV, movers-only, no-job moves, balance, alternative fertility measures/clusters and parity heterogeneity to Wu–Zhu. Do not infer it performs every specific CMDS diagnostic proposed below.

Motivations are the plan's design mapping: mover pre-outcome defenses (FGW; Cantoni–Pons), group/exposure overidentification (Chetty–Hendren), independent other-mover prediction (Chyn–Shenhav), and connected-set/limited-mobility diagnostics (AKM). They guide tests; they do not transfer identifying assumptions to CMDS.

No new causal regressions, IV, place-effect estimation or mechanism models were run here. Existing 2026-09-14 short-run sensitivities are historical results from the restricted legacy sample; they cannot be reported as completed tests on M.

## Tier 0 — measurement

| Test/design | Benchmark / motivation | Class | Exact variables; years; timing | Restrictions and sample cost | Identification value and residual gap | Result/status |
|---|---|:---:|---|---|---|---|
| 0.1 Arrival vs first departure | Mover timing prerequisite | A | current_arrive_year/month; first_leave_year/month, 2012–17; departure unavailable 2016, arrival month unavailable 2012 | M; equal-year subset 147,388 (loss 59.313%); inferred B 168,536 (loss 53.475%) | Detect compressed/mis-timed paths; equality does not prove actual prior residence | Counts executed |
| 0.1 Hukou-origin provenance | Measurement prerequisite | A | origin_province_code/name, origin_raw, origin_county_code/name, origin_best_available; 2012–17 | M; 1,650 fail valid province mapping | Prevent semantic substitution; registered location need not be exposure origin | Mapping audited |
| 0.1 Actual previous residence vs hukou estimates | Direct residence requires panel/spell evidence | C | No verified last-residence field or full prior sequence | No eligible verified previous-residence sample; inferred B is not a substitute | Would address origin error, but comparison cannot currently be identified | Not run |
| 0.2 External pre-move province measure | Benchmark alternative rates; independent treatment | A | external province×year CBR 2000–21; origin/dest codes, arrival; reported macro years, reconstructed pre3 mean | T; all six province-year values required; loss 10.572% | Removes own-CMDS-outcome mechanical construction; CBR demographic composition remains | Recomputed T and exact match on 21,255 legacy overlaps |
| 0.2 Age-standardized city×year / city pre-move measure | Preferred upgrade | B | births by maternal age and woman exposure, external city×year, crosswalk | At most C17 for observed common origin detail; further external loss Unknown | Better local exposure; origin error and selection remain | No validated ASFR/TFR merge |
| 0.2 Split sample / leave-one-out / leave-cohort-out / leave-survey-year-out CMDS measure | Independent prediction | B | child dates, age_t, survey_year, city code, parity_start_t, donor IDs; 2012–17 | D preferred, C17 for detailed origin; minimum donor cells/held-out-wave loss Unknown | Prevents own-record leakage, not survivor or migrant-composition bias | Requires reconstructed donor exposure and out-of-fold pipeline |
| 0.2 Minimum cells / reliability / shrinkage / ranking stability | Measurement-error defense | B | independent place estimates, donor N, variances, repeated rankings | Cell thresholds must be prespecified; loss Unknown | Noisy place ranks attenuate/mislead; shrinkage does not create independent treatment | Not executed |
| 0.3 Any annual birth | Benchmark fertility outcome | A | child1...9_birth_year/month, mother_birth_year, survey_year; 2012–17 | Age 15–45 person-years; date validation, 2017 flag; 29 women have impossible early child dates; do not blindly drop all their valid years | Defines denominators; recall/roster loss remain | Small diagnostic history executed; existing builder available |
| 0.3 First / second / higher-order hazards | Benchmark parity heterogeneity | B | parity_start_t from all valid earlier births; birth_count_t; 2012–17 | M → outcome/year-specific parity risk sets; at arrival N0=126,212, N1=149,096, N2+=86,937; annual loss not yet computed | Corrects survey-parity selection; incomplete lifetime births and twins need explicit treatment | Existing parity builder present; master hazard sample needs reconstruction |
| 0.3 Marriage among unmarried | Family-formation design | B | first_marriage_year/month; current marital status; base 2012–16 and 2018, origin-qualified 2012–16 | J is an upper bound for dated married-event histories, not marriage-risk population; rebuild from female base including verified never-married; final loss Unknown | Avoid conditioning marriage sample on observed fertility; cohabitation and dissolution histories incomplete | 2017 Q412 absent from actual release |
| 0.3 Conditional-on-marriage fertility | Separate estimand | B | first marriage before move, child dates, age; 2012–16 master | J ceiling; further valid sequencing loss Unknown | Separates a defined subgroup; conditioning on post-treatment marriage biases total-effect claim | Not estimated |

## Tier 1 — necessary selection defenses

| Test/design | Benchmark / motivation | Class | Required variables, years, timing | Restrictions / estimated cost | Concern addressed; residual problem | Result/status |
|---|---|:---:|---|---|---|---|
| 1.1 Birth in -2,-1,0,+1,+2 | Event sequencing / reverse causality | A | child years/months and current arrival, 2012–17; reported dates, deterministic r | M; annual counts available, age/full-year denominators required for rates | Detects births concentrated around moves; intended conception/pregnancy losses unobserved | Counts 25,360 /29,582 /33,249 /28,228 /17,901, not causal estimates |
| 1.1 Conception shortly before move | Reverse causality | B | birth month minus assumed gestation, arrival month; 2013–17 | 2012 month unavailable; excludes 59,632 master persons plus any invalid dates | Distinguishes likely pre-move conception; no observed gestation history, not exact pregnancy onset | No conception proxy built |
| 1.1 Marriage immediately before/in move year | Benchmark family timing extension | A | first_marriage_year/month; 2012–16 | J; 22.191% lack dates; month ordering not available for 2012 arrival | Detects family-linked migration; dated married subset is selected | r=-1:20,824; r=0:26,985 |
| 1.1 Fertility hazard by gap before move | Mover pre-outcome balance | B | age_t, parity_start_t, birth_t, gap, arrival; 2012–17 | T intersect valid annual risk sets; no balanced filter by default; row loss Unknown | Reveals sorting/anticipation; cannot establish untreated residence or remove fertility plans | Requires corrected master person-years |
| 1.1 Marriage hazard by gap | Family timing balance | B | first-marriage hazard risk set, gap; 2012–16 | Reconstructed marriage universe, not just J; Unknown final N | Reveals marriage-driven sorting; no full marital spells | Not run |
| 1.1 ±1 birth donut | Reverse causality sensitivity | A | any child year within inclusive arrival±1; 2012–17 | Retains 273,440, loss 88,805 (24.515%); T intersection not yet counted | Removes near-birth moves; selects on realized outcomes, changes target population | Exact descriptive cost computed |
| 1.1 ±2 birth donut | Same | A | any child year within arrival±2 | Retains 236,884; loss 125,361 (34.607%) | Broader exclusion; still selects on post-move fertility and can remove true effects | Cost computed |
| 1.1 Combined marriage/birth donuts | Same | A | dated marriage and child years; 2012–16 | Known-marriage subset: ±1 retains 187,759 (loss 48.168% of M); ±2 159,048 (loss 56.094%) | Strict diagnostic only; excludes date-missing never-married too, so not a universal definition | Cost computed, no model |
| 1.1 Exclude marriage/family motives | Benchmark motives | A | current_move_reason_group, 2013–17 | Known nonfamily/nonmarriage 236,379, loss 34.746%; do not call 2012 unknown nonfamily | Tests self-reported motives; misreporting and fertility plans remain | Counts computed |
| 1.1 Work / education estimates | Motive sensitivity | A | current reason, 2013–17 | Work 231,814; education only 257 before treatment/risk-set intersections | Work is not exogenous; education subgroup is very small | Counts only |
| 1.1 Gap predicts migration timing | Selection diagnostic | A | arrival year, age at move, gap, survey_year; 2012–17 | T; no additional fixed person loss | Can measure association; gap itself uses move year, so mechanical calendar dependence must be separated from choice | No regression run |
| 1.2 Joint pre-trend, slope, magnitude, far bins, CIs | Benchmark event study; FGW/Cantoni–Pons | B | corrected unbalanced person-years, birth_t, gap×event bins, cohort/age/calendar controls | T plus valid person-years; conditional support r=-5:331,250 and r=+5:140,486 in M before macro/1990/full-year restrictions | Detects differential past outcomes; nonrejection is not equivalence, prior residence uncertain | Legacy event scripts exist; no new-master joint test |
| 1.3 Within-origin, origin×move cohort / survey-year | Comparable origin defense | A at province diagnostic level | origin_prov, dest_prov, arrival, survey_year, reason; 2012–17 | T; additional cell-variation/singleton losses Unknown | Controls common origin/cohort conditions; hukou origin may be wrong and within-cell choices endogenous | Province keys ready; full hazard model follows risk-set repair |
| 1.3 Origin×reason×cohort high-dimensional cells | Support-sensitive extension | B | same plus harmonized reason | Known-reason T intersection; sparse-cell loss Unknown | More comparable cells, but support/collinearity may destroy contrast | Must report cell support before fitting |
| 1.4 Pre-move age/parity/marriage balance | Benchmark observables | A for age/dated history | birth year; earlier child dates; first-marriage date; 2012–17, marriage 2012–16 | T; marriage J intersection; parity history conditional on completeness | Observed sorting, not unobserved plans | Variables audited |
| 1.4 Education/hukou/work/family background as baseline | Benchmark changes in observables | C for complete true baseline histories | mother_education(_unified), mother_hukou_nature, spouse traits are current; no verified schooling completion or pre-move job history | No verified common baseline-history sample | Current controls can be mediators; older movers’ education cannot be declared fixed without evidence | Current-covariate descriptives feasible, baseline claims not |
| 1.5 Up/down moves and symmetry | Sign/symmetry falsification | A at province-gap diagnostic level | origin_pre3, dest_pre3, gap, dated events | Up 64,440; down 97,068; omit/report 162,441 zero gaps from sign comparison | Different prehistories can explain asymmetry; same-province zero is aggregation | Sign counts computed; symmetry test not estimated |
| 1.6 Reported one move / one city | Benchmark movers sensitivity | A | migration_count_total (2016); migration_city_count_total (2017) | 54,703 /45,183 respectively, losses 84.899% /87.527% | Diagnoses compressed paths; one city not one spell | Costs computed |
| 1.6 Recent arrival / equal-year proxy / broad comparison | Mover robustness | A | years_since_arrival; first_leave_year; arrival | Recent≤2:135,208 (loss 62.675%); equal-year 147,388 | Restricts duration/path uncertainty; recent sample has no long post-period | Costs computed |
| 1.6 Fully correct intermediate moves | Complete spell design | C | All prior cities and start/end dates absent | No reconstructable population | Cannot identify actual cumulative exposure | Not run |
| 1.7 Duration/observable survival association | CMDS-specific stock selection | A | duration, parity, current marriage, births after arrival, reason, gap; 2012–17 | M/T; dated marriage subsets if needed | Diagnoses survivor composition; no exited migrants/denominator | Variables and recent subset available |
| 1.7 Settlement/return/onward intentions | CMDS-specific extension | A for 2017 raw diagnostic | Q314,Q315,Q317,Q318,Q321A; 2017, interview-time intentions | C17=80,163; Q314 complete; routed counts 66,403/1,941/1,352/179 | Directly documents intentions; post-treatment and not realized retention | Raw fields joined and counts checked |
| 1.7 Selection IPW to recover all arrivals | Selection correction | C with current stock alone | Need entrants, exits/retention outcomes and credible selection probabilities | No known arrival-cohort denominator | Intentions do not identify realized selection weights; observables-only reweighting has narrower purpose | No weights fit |
| 1.8 Origin/destination/two-way clustering | Benchmark alternate clustering | A for province sample | origin_prov,dest_prov,mother_id, model scores; 2012–17 | Legacy 31 origin/31 destination clusters; broad keys comparable; no intrinsic loss | Respondent SE ignores common treatment shocks; 31 clusters require caution | Existing two-way code; no new SE comparison |
| 1.8 Wild/bootstrap inference | Few-cluster defense | B | valid residual/score bootstrap for chosen estimator and crossed dependence | No fixed loss; effective clusters and support must be assessed | Better small-cluster inference under assumptions; wrong bootstrap cannot fix treatment endogeneity | Implementation/validation pending |

## Tier 2 — overidentification and validation

| Test/design | Benchmark / top-paper motivation | Class | Exact requirements and years | Sample cost | Concern addressed; remaining limitation | Status |
|---|---|:---:|---|---|---|---|
| 2.1 Own age/parity/marriage group vs unrelated group fertility | Chetty–Hendren-inspired overidentification, not asserted in benchmark | B | age_t, parity_start_t, marriage-risk status, independent group×place fertility; 2012–17, marriage 2012–16 | Donor splitting/min-cell and correct-risk losses Unknown; D preferred, C17 for city origins | Tests group specificity; correlated group measures/selected donors can produce apparent validation | No validated group measures |
| 2.1 Policy eligibility / stable hukou groups | Policy/access overidentification | B for externally reconstructed eligibility; C for unobserved complete hukou histories | historical eligibility rules, prior births, hukou transitions/local access dates | Unknown; current hukou available does not establish stable history | Avoid using post-treatment group labels; exclusion still not automatic | Deferred reconstruction |
| 2.2 Years since arrival / age at arrival | Exposure logic | A descriptively; B for corrected dynamic causal model | arrival,birth year,survey year, dated births; 2012–17 | M/T with age/full-year support; no forced balanced main sample | Checks coherent duration response; age/cohort/survival and spacing confound gradients | Duration counts available |
| 2.2 Duration under policy/institution | Exposure logic | B | destination policy rollout/access start dates and arrival | External merge and eligibility losses Unknown | Distinguishes effective exposure; continuous residence remains assumed | No policy-duration construction |
| 2.3 Other-mover / leave-one-origin prediction IV | Plan attributes benchmark IV; Chyn–Shenhav | B computationally | independent donor outcomes, origin/dest, cohorts, valid risk sets; leave-origin/destination folds | Fold/min-cell losses Unknown; city limit C17 | Removes own-record leakage; shared destination fertility shocks can violate exclusion | No instrument/first stage fitted |
| 2.3 Establish IV exclusion from sample splitting alone | Instrument validity | C | Exogenous assignment/exclusion argument not supplied | Not a sample-size issue | Independence of estimation samples is not independence of structural errors | Explicitly rejected as justification |
| 2.3 Required validation package | IV defense | B | first-stage strength, pre-move placebo, leave-origin/destination sensitivity, weak-IV robust inference | Same donor requirements; Unknown | Weak IV and residual selection; tests cannot prove exclusion | Must accompany any later IV |
| 2.4 Hukou reform timing/intensity | External shock hypothesis | B | city reform dates, rollout/intensity, migration timing, eligibility | City-origin geography C17 ceiling if two-sided city exposure; external loss Unknown | Reform may directly affect fertility through access, violating migration-IV exclusion | No reform merge; mechanism not executed |
| 2.4 Administrative/labor displacement/disaster assignment | Benchmark disasters; quasi-exogenous moves | C now | No verified exogenous displacement/assignment event in current files; job motive insufficient | No verified eligible sample | Requires independently documented shock and selection/exclusion evaluation | Future external event data could change verdict |
| 2.5 Fertility-policy as migration IV | Exclusion restriction | C | Policy directly changes fertility incentives | No legitimate sample fixes exclusion | Invalid naive instrument for place exposure | Do not implement |
| 2.5 Policy×eligibility×access validation | Later validation/mechanism | B, deferred | event calendar year, parity, historical eligibility, city policy/access | Unknown after eligibility merge; no three-child-era data | Can test constraints under DID assumptions; contemporaneous policy and composition remain | Classified only, no mechanism |
| 2.6 Mobility graph / connected component | Benchmark AKM; limited mobility | A at province proxy level | hukou origin/current destination; 2012–17 | Valid province keys; legacy 21,383, broad valid N in evidence JSON | Diagnoses disconnection/thin links; links are assumed paths | Legacy 707 directed links, component 31; 236 links <5 |
| 2.6 City connectedness / leave-out robustness | AKM graph requirements | B | harmonized city codes; edge multiplicities and incidence matrix | C17 maximum; crosswalk/weak-link losses Unknown | Ordinary connectedness insufficient for leave-one-out identification | Not established |
| 2.6 Raw vs bias-corrected variance/sorting covariance | Benchmark AKM; finite-sample correction | B computationally | valid person-place incidence, noise model, split/leave-out correction | Unknown after connected/support filters | Bias correction removes estimation noise, not endogenous migration or assumed location errors | Historical raw effects do not establish causal variance |

## Tier 3 — each proposed robustness item

These are later alternatives, not cumulative master restrictions. All “result” entries below are feasibility/cost audit only.

| Proposed item | Class | Variables / years / timing | Estimated cost and identification limitation |
|---|:---:|---|---|
| Province vs prefecture vs county | A province / B finer | province keys all 2012–17; origin_county_code 2017; current destination names/codes | C17 for common fine OD detail, 77.871% loss before crosswalk; boundary comparability and inferred origin remain |
| External vs internal fertility | B comparison | external CBR now; internal independent age/parity-adjusted donor rates need reconstruction | T external; internal donor loss Unknown; different estimands must be labeled |
| Alternative age standardization | B | external female age exposure/birth numerator or reconstructed independent donor hazards | Unknown; age adjustment cannot correct origin/selection errors |
| Alternative event windows | A support / B fitted dynamics | event_time, age_t, survey year; 2012–17 | Age-capped ±1/±3/±5 retains 308,988 /202,191 /125,206, before full-year/1990/treatment conditions; balance changes cohort composition |
| Recent movers only | A | arrival duration ≤2 | 135,208; 62.675% loss, short post history |
| Exclude marriage movers | A | current_move_reason_group | Known reasons 302,613 minus 8,875 marriage =293,738; loss 68,507 including 2012 unknown; motives incomplete |
| Exclude family-reunification movers | A | follow_family/care_family/kinship_network/elderly_migration | Known reasons 302,613 minus 57,359 =245,254; loss 116,991; definition stated, family labels are not causality |
| Work movers only | A | work_business | 231,814; loss 36.006%; no exogeneity implication |
| Cross-province movers | A | current_move_scope=1 | 183,840; loss 49.250%; province contrast improves but estimand narrows |
| Within-province movers | A population / B nonzero local treatment | scope 2/3 | 178,405; loss 50.750%; province gap cannot measure their local-place change |
| Stable hukou groups | C as stability claim | current nature is observed, transition dates absent | Current-group splits possible, stable historical status Unknown |
| Alternative cluster levels | A existing province / B bootstrap | origin,destination,respondent IDs | No fixed loss, effective clusters need estimator-specific audit |
| Placebo move dates | B | valid event histories, admissible date assignment respecting age/calendar/cohort | Unknown after placebo support; arbitrary shuffling may destroy dependence and give invalid null |
| Placebo destination measures | B | independent irrelevant group/place proxy, prespecified permutation strata | Unknown; correlated environments make null difficult to interpret |
| Reweight movers to broader CMDS composition | B | source population covariates, survey weights/design, overlap | Base contains 507,225 women; M-to-base support Unknown; cannot recover absent return migrants or fertility histories by weighting |

## Section 5 mechanisms — feasibility classification only; execution deferred

The supplied plan requests a matrix for §5. The user's “先不要做机制” controls execution: the following records prerequisites, not mechanism tests or estimates.

| Mechanism | Class | Required variables / years / timing | Cost / identification gap |
|---|:---:|---|---|
| Hukou/access to place | B | current mother_hukou_nature (all base waves), destination, historical eligibility/public-service access and reform dates | External loss Unknown; current hukou alone is not actual access or exogenous treatment |
| Fertility-policy regime | B | parity histories, calendar years, local/individual eligibility, access | D preferred for direct history; final loss Unknown; eligibility and parallel trends not established |
| Marriage markets | B | marriage hazard, external age/sex/education composition and city labor market | J is not sufficient marriage-risk sample; city detail C17 conflicts with missing 2017 marriage dates; source expansion needed |
| Family network/grandparental care | B for current proxies / C full historical care exposure | spouse/child current residence, raw family roster, origin distance, dated caregiver presence | Raw module extraction and coverage Unknown; spouse roster is not observed pre-move childcare |
| Economic constraints | B | city housing/wages/female work/childcare prices, historical individual employment | External losses Unknown; survey-time income/job can be post-treatment; causal mediation unavailable without additional assumptions |

## Reconciliation of previous results and readiness

The revised legacy sensitivity table reports about +2.86 pp per 10‰ gap (21,383 women), with exclusion of month contradictions and explicit multi-city reporters producing similar estimates. Those scripts/results are from the restricted 2013–17 work/cross-province/balanced sample and were not rerun here. They do not complete joint pre-trends, survivor diagnostics, independent city measures, risk-set corrections, IV or mechanisms for M. The provenance of the benchmark-method list is the supplied plan; no external article result is presented as newly verified.

**Corrections required before calling a Stage C model clean:**

1. Freeze a measurement-valid annual risk-set builder: upper age bound, survey-year partial exposure, impossible dates, lifetime-roster sensitivity, twins and pre-year parity.
2. Separate marriage universe from complete-birth-history eligibility; recover verified never-married risk exposure without coding unknown dates as never married.
   The current master excludes all 63,336 currently unmarried base women in 2012–2016. This also selects first-birth histories on later family status. Reconstructed hazards on the existing master alone therefore target a selected group, even when yearly parity is computed correctly.
3. Preserve source-specific origins and unknown intervals; do not manufacture previous residence.
4. Use the actual macro-match flag: 323,949, not legacy final membership. Report zero gaps and treatment variation within chosen cells.
5. Make split-sample or group measures genuinely independent with documented donor support; do not equate leave-out construction with an IV exclusion restriction.

## Recommended next execution order (not executed as regressions in this delivery)

1. Lock the independently sourced province treatment and publish its two components, match losses and zero-gap support (descriptive matching completed here).
2. Validate annual risk sets, then report near-move births/marriage and alternative donuts with consistent denominators and target-population labels.
3. Compare broad, reported one-move/city, inferred-origin and recent-arrival samples; retain broad starting population.
4. Estimate within-hukou-origin province comparisons and meaningful pre-outcome diagnostics with joint tests, slopes, effect-scaled magnitudes and confidence intervals.
5. Add 2017 intention and duration-specific stock-selection diagnostics; distinguish observed survivors from all arrival cohorts.
6. Audit clustering and few-cluster inference for the selected model.
7. Only after these, build independent fine-geography/group measures and evaluate stronger overidentification/IV prerequisites. Mechanisms remain deferred.

Audit completion is not identification success: the exact previous residence, unobserved migration/return selection, and incomplete lifetime histories remain material unresolved boundaries.
