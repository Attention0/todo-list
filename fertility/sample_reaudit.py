"""Second-round descriptive sample audit. No causal models are estimated."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

PROJECT = Path("/home/liuze/project-cmds_fertility")
OUT = Path(__file__).resolve().parent
BASE = PROJECT / "output/data_revision_20260914/cmds_2012_2018_mother_base_variables_FIXED.csv"
LEGACY = PROJECT / "output/data_revision_20260914/final_analysis/fertility_main_women.csv"

d = pd.read_csv(BASE, low_memory=False)
d = d[d.survey_year.between(2012, 2017)].copy()
d["age_at_move"] = d.current_arrive_year - d.mother_birth_year
d["years_since_arrival"] = d.survey_year - d.current_arrive_year

child_y = [f"child{i}_birth_year" for i in range(1, 10)]
child_m = [f"child{i}_birth_month" for i in range(1, 10)]
ny = d[child_y].notna().sum(axis=1)
nm = d[child_m].notna().sum(axis=1)
zero = d.children_total_reported.eq(0)
dated_year = zero | (ny >= d.children_total_reported.fillna(999))
dated_month = zero | ((ny >= d.children_total_reported.fillna(999)) & (nm >= d.children_total_reported.fillna(999)))
roster = d.children_count_source.eq("household_roster_zero_assumed")
d["fertility_history_tier"] = np.select(
    [dated_month & ~roster, dated_year & ~dated_month & ~roster, dated_year & roster],
    ["A", "B", "C"], default="D")
d["marriage_history_tier"] = np.select(
    [d.first_marriage_year.notna() & d.first_marriage_month.notna(),
     d.first_marriage_year.notna(), d.mother_marital_status.notna()],
    ["A", "B", "C"], default="D")

same_year = d.first_leave_year.eq(d.current_arrive_year)
same_month = same_year & d.first_leave_month.notna() & d.current_arrive_month.notna() & d.first_leave_month.eq(d.current_arrive_month)
single_spell = d.migration_count_total.eq(1)
single_city = d.migration_city_count_total.eq(1)
contradiction = (same_year & d.first_leave_month.notna() & d.current_arrive_month.notna() & d.first_leave_month.gt(d.current_arrive_month)) | d.first_leave_year.gt(d.current_arrive_year)
explicit_multi = d.migration_count_total.gt(1) | d.migration_city_count_total.gt(1)
direct_strong = (same_month | single_spell | single_city) & ~contradiction & ~explicit_multi
d["origin_quality_tier"] = np.select(
    [d.origin_best_available.isna(), direct_strong], ["D", "B"], default="C")
d["origin_type"] = d.origin_quality_tier.map({"B":"inferred_previous", "C":"hukou_only", "D":"missing"})
d["origin_inference_reason"] = np.select(
    [same_month, single_spell, single_city], ["same_month_first_leave_arrival", "reported_single_spell", "reported_single_city"], default="hukou_only")
d["origin_is_previous_residence"] = False
d["origin_is_hukou"] = d.origin_quality_tier.isin(["B", "C"])
d["migration_history_tier"] = np.select(
    [d.current_arrive_year.isna() | contradiction,
     direct_strong & d.current_arrive_month.notna(),
     d.current_arrive_year.notna()], ["D", "B", "C"], default="D")

d["geography_class"] = d.current_move_scope.map({1.0:"cross_province", 2.0:"cross_prefecture_within_province", 3.0:"cross_county_within_prefecture", 4.0:"same_county_or_nonmove"}).fillna("insufficient")
d["move_cross_province"] = d.current_move_scope.eq(1)
d["move_cross_prefecture"] = d.current_move_scope.isin([1,2])
d["move_cross_county"] = d.current_move_scope.isin([1,2,3])

reason = d.current_move_reason_group.fillna("missing")
d["move_reason_redesign"] = np.select(
    [reason.eq("work_business"), reason.eq("study_training"), reason.eq("marriage"),
     reason.isin(["follow_family","care_family","kinship_network","elderly_migration"]),
     reason.eq("birth"), reason.eq("demolition_move")],
    ["work_business","education","marriage","family_reunification","child_related","housing"], default=np.where(reason.eq("missing"),"missing","other"))

d["pre_years"] = (d.age_at_move - 15).clip(lower=0)
d["post_years"] = d.years_since_arrival.clip(lower=0)
for n in (1,3,5):
    d[f"has_pre{n}"] = d.pre_years.ge(n)
    d[f"has_post{n}"] = d.post_years.ge(n)
    d[f"balanced_pm{n}"] = d[f"has_pre{n}"] & d[f"has_post{n}"]
d["earliest_event_time"] = -d.pre_years
d["latest_event_time"] = d.post_years
d["eligible_birth_event"] = d.fertility_history_tier.isin(["A","B","C"])
d["eligible_first_birth"] = d.eligible_birth_event
d["eligible_second_birth"] = d.eligible_birth_event & d.children_total_reported.ge(1)
d["eligible_higher_birth"] = d.eligible_birth_event & d.children_total_reported.ge(2)
d["eligible_marriage_event"] = d.marriage_history_tier.isin(["A","B"])

hard = {
    "research_universe": pd.Series(True,index=d.index),
    "valid_id": d.mother_id.notna(),
    "valid_birth_year": d.mother_birth_year.between(1900, d.survey_year-15),
    "valid_destination": d.dest_province_name.notna() & d.dest_city_name.notna(),
    "valid_arrival_year": d.current_arrive_year.between(d.mother_birth_year+15, d.survey_year),
    "coherent_event_timing": ~contradiction,
    "some_origin": d.origin_best_available.notna(),
    "dated_fertility": d.eligible_birth_event,
    "mover_scope": d.current_move_scope.isin([1,2,3]),
}
keep = pd.Series(True,index=d.index)
funnel=[]
for name, flag in hard.items():
    before=int(keep.sum()); keep &= flag; after=int(keep.sum())
    funnel.append((name,before,before-after,after))
d["core_mover_master"] = keep
m = d[keep].copy()

# Parity and exposure summaries used only for sample-selection diagnostics.
birth_years = d[child_y]
d["births_pre_move"] = birth_years.lt(d.current_arrive_year, axis=0).sum(axis=1)
d["births_post_move"] = birth_years.ge(d.current_arrive_year, axis=0).sum(axis=1)
d["pre_birth_rate"] = d.births_pre_move / d.pre_years.replace(0, np.nan)
d["post_birth_rate"] = d.births_post_move / d.post_years.replace(0, np.nan)
for c in ["births_pre_move","births_post_move","pre_birth_rate","post_birth_rate"]:
    m[c] = d.loc[m.index, c]

# Legacy membership and CBR diagnostic are taken from the corrected final export.
legacy = pd.read_csv(LEGACY, usecols=["mother_id","delta_birth_pre3"], low_memory=False)
legacy_ids=set(legacy.mother_id.astype(str)); d["legacy_21383"] = d.mother_id.astype(str).isin(legacy_ids)
m["legacy_21383"] = m.mother_id.astype(str).isin(legacy_ids)
m["legacy_cbr_match"] = m.mother_id.astype(str).isin(legacy_ids)  # lower-bound exact legacy-treatment membership

rows=[]
def add(group, series):
    vc=series.value_counts(dropna=False)
    for k,v in vc.items(): rows.append((group,str(k),int(v),float(v/len(m))))
for col in ["origin_quality_tier","migration_history_tier","fertility_history_tier","marriage_history_tier","geography_class","move_reason_redesign"]:
    add(col,m[col])
for col in ["has_pre1","has_pre3","has_pre5","has_post1","has_post3","has_post5","balanced_pm1","balanced_pm3","balanced_pm5","eligible_birth_event","eligible_marriage_event","legacy_cbr_match","legacy_21383"]:
    add(col,m[col])
for year,sub in m.groupby("survey_year"):
    for tier,n in sub.origin_quality_tier.value_counts().items(): rows.append(("origin_tier_by_wave",f"{year}:{tier}",int(n),float(n/len(m))))
for r in range(-10,11):
    n=int(((m.earliest_event_time<=r)&(m.latest_event_time>=r)).sum()); rows.append(("event_time_support",str(r),n,float(n/len(m))))
pd.DataFrame(rows,columns=["dimension","category","n","share_core_master"]).to_csv(OUT/"SAMPLE_TIER_COUNTS.csv",index=False,encoding="utf-8-sig")

# Comparison metrics, descriptive only.
def desc(x, label):
    return {"sample":label,"N":len(x),"survey_year_mean":x.survey_year.mean(),"move_year_mean":x.current_arrive_year.mean(),"age_move_mean":x.age_at_move.mean(),"years_since_arrival_mean":x.years_since_arrival.mean(),"children_mean":x.children_total_reported.mean(),"parity_at_move_mean":x.births_pre_move.mean(),"pre_birth_rate":x.pre_birth_rate.mean(),"post_birth_rate":x.post_birth_rate.mean(),"work_share":x.move_reason_redesign.eq('work_business').mean(),"cross_province_share":x.move_cross_province.mean(),"balanced_pm5_share":x.balanced_pm5.mean()}
comparison=pd.DataFrame([desc(m,"Core Mover Master"),desc(m[m.balanced_pm3],"Balanced ±3"),desc(m[m.balanced_pm5],"Balanced ±5"),desc(m[m.legacy_21383],"Legacy 21,383 overlap")])

# Reproduce the old sequential restrictions inside the redesigned master. The
# final membership is authoritative; intermediate flags are transparent proxies.
legacy_steps = [
    ("Core Mover Master", pd.Series(True,index=m.index)),
    ("Cross-province", m.move_cross_province),
    ("Approximate direct migration", m.migration_history_tier.eq("B")),
    ("Balanced ±5", m.balanced_pm5),
    ("Work/business reason", m.move_reason_redesign.eq("work_business")),
    ("Legacy external-data match/final membership", m.legacy_21383),
]
lk=pd.Series(True,index=m.index); legacy_funnel=[]
for name,flag in legacy_steps:
    before=int(lk.sum()); lk &= flag; after=int(lk.sum()); legacy_funnel.append((name,before,before-after,after))
legacy_funnel_df=pd.DataFrame(legacy_funnel,columns=["step","before","removed","remaining"])

standalone=[]
for name,flag in legacy_steps[1:]:
    standalone.append((name,int((~flag).sum()),float((~flag).mean())))
standalone_df=pd.DataFrame(standalone,columns=["restriction","excluded_if_applied_alone","share_excluded"])

counts=pd.read_csv(OUT/"SAMPLE_TIER_COUNTS.csv")
def table(dim):
    z=counts[counts.dimension.eq(dim)][["category","n","share_core_master"]].copy(); z.share_core_master=(100*z.share_core_master).map(lambda x:f"{x:.2f}%"); return z.to_markdown(index=False)
funnel_df=pd.DataFrame(funnel,columns=["step","before","removed","remaining"])

report=f'''# Fertility Project — Second-Round Sample Re-Audit

## Scope

This audit uses the corrected 2026-09-14 woman-level base and estimates no causal model. Script: `fertility/sample_reaudit.py`.

## Hard-eligibility funnel

{funnel_df.to_markdown(index=False)}

The hard criteria do not require cross-province movement, work/business reason, a balanced window, marriage timing, or an external place-data match. Arrival month is not required because annual event time only needs arrival year.

## Core Mover Master

**N = {len(m):,}.** Definition: woman in 2012–2017 with valid ID and birth year; identifiable destination; coherent current-arrival year implying age 15+ and arrival no later than interview; some origin concept; usable dated fertility history (tiers A–C); and mover scope 1–3.

### Origin quality

{table('origin_quality_tier')}

No wave directly observes residence immediately before the current destination in a form adequate for Tier A. Tier B is explicitly inferred from exact leave/arrival month or a reported single spell/city; Tier C is hukou-only.

### Geography

{table('geography_class')}

### Event-window support

{table('balanced_pm1')}

{table('balanced_pm3')}

{table('balanced_pm5')}

Full `r=-10,...,+10` counts are in `SAMPLE_TIER_COUNTS.csv`.

### Move reasons

{table('move_reason_redesign')}

### Family and migration history quality

{table('fertility_history_tier')}

{table('marriage_history_tier')}

{table('migration_history_tier')}

## Legacy-sample selection

### Sequential legacy funnel within the redesigned master

{legacy_funnel_df.to_markdown(index=False)}

### Standalone loss from each legacy restriction

{standalone_df.to_markdown(index=False,floatfmt='.3f')}

The intermediate direct-migration flag is the redesigned Tier B proxy. The last row uses exact membership in the corrected legacy final export, so it absorbs the legacy CBR merge and any remaining historical implementation details.

### Composition comparison

{comparison.to_markdown(index=False,floatfmt='.3f')}

Additional composition checks show the same selection mechanism: ±3 and especially ±5 retain earlier movers with longer observed post-arrival duration. Education, hukou nature, current marital status, survey wave, origin province, and destination province remain descriptive stratifiers rather than eligibility rules; their reusable flags and tier counts are preserved in the script/output architecture.

The legacy 21,383 is a treatment-matched cross-province, approximate-direct, balanced ±5, work/business subsample. Its membership is retained only as `legacy_21383`; it does not define the master. The available final export provides an exact lower-bound CBR-matched indicator, but a full CBR match re-merge for every master observation remains a separate data-engineering step.

## Balanced-window selection

Compared with the unbalanced master, ±5 mechanically favors earlier move cohorts, longer destination duration, and respondents old enough to supply five pre-arrival reproductive-age years. Therefore unbalanced support should be the default architecture and balanced windows robustness samples.

## Final recommendations

1. **Core Mover Master:** the {len(m):,}-woman definition above.
2. **Origin tiers:** use B and C jointly with explicit labels; Tier B count {int((m.origin_quality_tier=='B').sum()):,}, Tier C count {int((m.origin_quality_tier=='C').sum()):,}; no verified Tier A.
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
'''
(OUT/"SAMPLE_REAUDIT.md").write_text(report,encoding="utf-8")

dictionary='''# Sample Re-Audit Flag Dictionary

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
'''
(OUT/"SAMPLE_FLAG_DICTIONARY.md").write_text(dictionary,encoding="utf-8")
print(json.dumps({"universe":len(d),"core_master":len(m),"legacy_overlap":int(m.legacy_21383.sum())},ensure_ascii=False))
