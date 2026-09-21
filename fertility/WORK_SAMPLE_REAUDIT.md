# Fertility Project — Work Instructions for Sample Re-Audit

## Objective

Rebuild the fertility project's sample architecture using the principles in:

`fertility/SAMPLE_REDESIGN.md`

The previous audit correctly documented the existing 21,383-woman sample, but that sample was shaped by the current province-CBR specification.

The new task is to construct and document a broader research master sample that is not prematurely restricted by treatment availability or by robustness-style filters.

Do not delete the previous audit outputs. This is a second-round sample audit.

---

## Required workflow

1. Read:
   - `fertility/SPEC.md`
   - `fertility/SAMPLE_REDESIGN.md`
   - existing audit files in `fertility/`.

2. Inspect the active empirical project and current sample-building code.

3. Reconstruct a **Research Universe** and a **Core Mover Master** according to the redesign.

4. Separate:
   - hard eligibility restrictions;
   - analysis flags / tiers.

5. Build explicit origin-quality, migration-history, fertility-history, marriage-history, geography, event-support and move-reason variables.

6. Do not require external CBR matching to enter the master sample.

7. Do not require cross-province movement to enter the master sample.

8. Do not require a balanced `±5` event window to enter the master sample.

9. Do not require work/business move reason to enter the master sample.

10. Keep respondents with high-confidence previous residence and respondents with hukou-only origin in the same master architecture, but mark them separately.

11. Quantify the selection induced by the old restrictions.

12. Write the required outputs and commit them to the current fertility-audit branch.

---

## Hard-eligibility audit

Explicitly evaluate whether each of the following should be required for the Core Mover Master:

- female respondent;
- usable survey wave;
- valid respondent ID;
- valid survey year;
- valid age / birth year;
- valid current destination;
- valid current-destination arrival year;
- valid current-destination arrival month;
- at least one usable origin concept;
- dated fertility history;
- internally coherent event timing.

Do not assume month-level timing is required if year-level timing is sufficient for a given design.

For every hard restriction report:

- reason;
- variable(s);
- number before;
- number removed;
- number remaining;
- whether the restriction is truly necessary for all fertility analyses.

---

## Origin reclassification

Search all usable waves again for any variable that could identify residence immediately before the current destination.

Do not stop at the previous conclusion that origin is "hukou" without checking wave-specific migration modules.

Create:

- `origin_type`;
- `origin_quality_tier`;
- `origin_province_best`;
- `origin_prefecture_best`;
- `origin_county_best`;
- `origin_is_previous_residence`;
- `origin_is_hukou`;
- `origin_inference_reason`.

Classify origin into:

- A = observed previous residence;
- B = high-confidence inferred previous residence / direct-from-hukou;
- C = hukou origin only;
- D = insufficient.

Document exact evidence for every A/B rule.

Never label B as directly observed.

Report counts by survey year and by tier.

---

## Geographic transition reclassification

Keep all usable movers, not only cross-province movers.

Classify each observation when possible as:

- same county / district;
- cross-county within prefecture;
- cross-prefecture within province;
- cross-province;
- insufficient geography.

Create corresponding flags.

Report sample size and survey-year coverage for each geography class.

---

## Event-window support

Use the unbalanced architecture as default.

For each respondent derive:

- number of usable pre-arrival years;
- number of usable post-arrival years;
- earliest event time;
- latest event time;
- `has_pre1`, `has_pre3`, `has_pre5`;
- `has_post1`, `has_post3`, `has_post5`;
- `balanced_pm1`, `balanced_pm3`, `balanced_pm5`.

Report how many women can contribute to each event time `r=-10,...,+10` if feasible, without requiring balance.

Produce an event-time support table.

Compare the characteristics of:

- all Core Mover Master respondents;
- balanced ±3;
- balanced ±5.

This comparison is required to diagnose duration / survivorship selection.

---

## Move-reason architecture

Keep all move reasons.

Create mutually exclusive categories and flags.

Report counts and shares for:

- work/business;
- education;
- marriage;
- family reunification;
- child-related;
- housing;
- hukou/institutional;
- other;
- missing.

Then report nested samples:

- all movers;
- exclude marriage movers;
- exclude marriage + family movers;
- work/business only.

Do not choose one as the final main sample in this task.

---

## Fertility-history quality

Create quality tiers based on how birth events are dated.

At minimum distinguish:

- A: child-specific year/month directly recorded;
- B: year reliable, month missing / derived;
- C: roster-derived / zero-parity assumption-dependent;
- D: not usable for dated event study.

Report tier counts by survey year.

Also report eligibility for:

- any birth event;
- first birth;
- second birth;
- higher-order birth.

---

## Marriage-history quality

Create quality tiers for:

- exact first-marriage year/month;
- year only / inferable;
- current marital status only;
- insufficient.

Report counts by survey year.

Define `eligible_marriage_event` separately from the fertility master sample.

Do not exclude women from the fertility master simply because marriage timing is unavailable.

---

## Migration-history quality

Create migration-history tiers based on:

- current-arrival timing;
- first-leave timing;
- number of migration spells;
- multiple-city evidence;
- timing contradictions;
- observed / inferred directness.

Report counts by survey year.

Do not compress these into a single direct-move flag.

---

## External match audit

Using the current legacy CBR file only as a diagnostic, not as a sample criterion:

1. Start from the redesigned Core Mover Master.
2. Report how many match the legacy CBR treatment.
3. Report how many do not.
4. Compare matched and unmatched observations by:
   - survey year;
   - move cohort;
   - geography class;
   - origin tier;
   - destination;
   - years since arrival.

The purpose is to quantify how the old CBR-merge requirement selected the sample.

Do not drop unmatched respondents from the master output.

---

## Legacy-sample decomposition

Recreate the old 21,383 sample by sequentially applying:

- cross-province;
- legacy direct-move restriction;
- legacy birth-history rule;
- balanced ±5;
- work/business;
- CBR match.

Then, starting from the new Core Mover Master, show the marginal effect of each old restriction.

Where order matters, report both:

- legacy sequential funnel;
- standalone loss from each restriction.

This is required.

---

## Required comparison table

Compare the new Core Mover Master with the legacy 21,383 sample on:

- N;
- survey year;
- move cohort;
- age at move;
- education;
- hukou type;
- marital status;
- parity at move;
- move reason;
- origin province;
- destination province;
- years since arrival;
- pre-move birth rate;
- post-move birth rate.

Use descriptive statistics only.

---

## Required outputs

Create:

```
fertility/SAMPLE_REAUDIT.md
fertility/SAMPLE_TIER_COUNTS.csv
fertility/SAMPLE_FLAG_DICTIONARY.md
```

If scripts are added, document them in `SAMPLE_REAUDIT.md`.

Do not overwrite the previous first-round audit files.

---

## Final recommendations section

End `SAMPLE_REAUDIT.md` with a concise recommendation for:

### Core Mover Master

Exact proposed definition and N.

### Main birth-event analysis sample

Which origin / migration / fertility tiers are acceptable.

### Strict identification robustness sample

Which tiers / exclusions define it.

### Marriage geography sample

Which marriage-history tiers and waves are usable.

### Future prefecture-level sample

Which waves and origin tiers support it.

### Legacy CBR sample

Treat this explicitly as a treatment-matched estimation subsample, not the research master sample.

---

## Definition of done

This task is complete only when the project has:

1. a broad Core Mover Master not defined by CBR matching;
2. no forced cross-province restriction in the master;
3. no forced balanced ±5 restriction in the master;
4. no forced work/business restriction in the master;
5. explicit origin-quality tiers;
6. explicit migration-history tiers;
7. explicit fertility-history tiers;
8. explicit marriage-history tiers;
9. geographic transition classes;
10. event-window support flags;
11. legacy-sample selection diagnostics;
12. documented recommendations for which sample tier belongs to which estimand.

Do not run new causal models in this task.
