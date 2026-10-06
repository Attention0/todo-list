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


