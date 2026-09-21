# Fertility Project — Main Sample Redesign

## 1. Purpose

The current 21,383-woman sample is useful for reproducing the existing province-CBR specification, but it should **not** automatically define the research master sample.

The next task is to rebuild the sampling logic from first principles.

The core principle is:

> **Define the economically meaningful research population first; attach identification-quality flags second; apply treatment-specific restrictions only at the estimation stage.**

Do not let the current province-level CBR specification determine who enters the master sample.

In particular, the redesigned master sample should not be mechanically restricted to:

- cross-province movers;
- a balanced `-5,...,+5` event window;
- work/business movers only;
- respondents matched to the current external CBR file;
- respondents whose hukou place is treated as if it were certainly the previous residence.

The project should instead keep the broadest credible mover/family-history sample and create explicit tiers for origin quality, migration-history quality, geography, event-window support, move reason, family-history quality, and external-data match status.

---

## 2. Sampling philosophy

Separate restrictions into two categories.

### A. Hard eligibility restrictions

These may legitimately define a research master sample because the observation cannot contribute to the central mover/family-history design without them.

Examples include:

- respondent is a woman in a CMDS wave with the required core modules;
- respondent identity / survey year is usable;
- current destination is identifiable at the minimum geographic level needed for the master file;
- arrival timing at the current destination is observed or credibly reconstructable;
- birth history is sufficient to date at least the fertility outcomes used in the master fertility design;
- age / birth-year information is sufficient to construct age at event;
- basic data are internally coherent enough to construct event time.

Even these should be justified empirically and documented.

### B. Analysis restrictions / flags

These should **not** define the broad master sample unless there is a specific estimand that requires them.

Examples:

- cross-province move;
- cross-prefecture move;
- balanced event window;
- work/business move reason;
- exact direct move;
- external fertility-data match;
- external marriage-data match;
- marriage timing observed;
- city-level origin available;
- strict migration-history consistency.

These should be stored as variables / tiers and invoked when needed.

---

## 3. Recommended sample architecture

Build a layered sample architecture rather than one final sample.

### Layer 0 — Research universe

All women in CMDS waves judged potentially usable for the project after basic harmonization.

Do not require:

- cross-province migration;
- balanced window;
- work/business reason;
- CBR/TFR/ASFR match;
- marriage timing;
- strict direct-move status.

This layer is for documenting the full observable research universe.

### Layer 1 — Core mover-history master

The preferred broad mover master should require only what is necessary to define a move to the current destination and to place fertility events around it.

Candidate requirements:

1. woman;
2. usable survey year;
3. valid birth year / age;
4. current destination identifiable;
5. current-destination arrival timing identifiable;
6. at least one usable origin concept:
   - observed previous residence, if available;
   - otherwise credible inferred previous residence;
   - otherwise hukou origin, clearly labeled as hukou origin;
7. fertility history sufficient to reconstruct dated birth events for the outcomes retained in the master file.

Do **not** require cross-province movement.

Do **not** require a balanced `±5` window.

Do **not** require work/business move reason.

Do **not** require any external fertility/place-data match.

### Layer 2 — Outcome-specific samples

Create separate analysis eligibility flags, for example:

- `eligible_birth_event`;
- `eligible_first_birth`;
- `eligible_second_birth`;
- `eligible_marriage_event`;
- `eligible_marriage_to_birth`;
- `eligible_fertility_intention`.

Outcome-specific missingness should not shrink the master sample unnecessarily.

### Layer 3 — Identification-quality samples

Create origin / migration-history tiers and strict-mover samples rather than dropping weaker observations from the outset.

### Layer 4 — Treatment-specific matched samples

Only when estimating a model with an external place measure should the analysis require that measure to be matched.

Examples:

- `match_cbr`;
- `match_tfr`;
- `match_asfr`;
- `match_marriage_rate`;
- `match_housing`;
- `match_childcare`.

The external-data file should never define the core research population.

---

## 4. Origin redesign

The current audit shows that the existing analysis mostly uses hukou origin. That is acceptable as one origin concept, but it should not be treated as identical to previous residence.

The redesigned data must distinguish origin concepts explicitly.

### Proposed origin-quality tiers

#### Origin Tier A — Observed previous residence

Use when CMDS directly identifies the place of residence immediately before arrival at the current destination.

This is the highest-quality origin for a mover design.

Store:

- prior province;
- prior prefecture;
- prior county if available;
- source variable;
- survey wave;
- whether timing is directly linked to current arrival.

#### Origin Tier B — High-confidence inferred previous residence

Use when previous residence is not directly observed, but the data strongly support a direct move from hukou origin to current destination.

Examples may include:

- first departure from hukou place and current-destination arrival occur in the same year / month;
- reported number of migration spells is one;
- no evidence of intermediate cities;
- other wave-specific evidence consistent with a direct move.

This should be labeled as **inferred previous residence**, not observed previous residence.

#### Origin Tier C — Hukou origin only

Use when hukou origin is observed but there is insufficient evidence that it equals the immediately prior residence.

Keep these observations in the broad master sample where appropriate.

Label treatment contrasts explicitly as:

`destination minus hukou-origin`

rather than:

`destination minus previous residence`.

#### Origin Tier D — Origin insufficient / missing

Retain in the research-universe file if useful for documentation, but flag as not eligible for origin-destination treatment estimands.

### Required origin variables

Create variables equivalent to:

- `origin_type` = observed_previous / inferred_previous / hukou_only / missing;
- `origin_quality_tier` = A / B / C / D;
- `origin_province_best`;
- `origin_prefecture_best`;
- `origin_county_best`;
- `origin_is_hukou`;
- `origin_is_previous_residence`;
- `origin_inference_reason`.

The "best origin" field must preserve provenance.

---

## 5. Geographic scope redesign

Do not require cross-province movement in the master sample.

Instead classify every mover into the finest identifiable geographic transition.

Suggested categories:

1. same county / district;
2. cross-county within same prefecture;
3. cross-prefecture within same province;
4. cross-province;
5. geography insufficient to classify.

Create flags such as:

- `move_cross_county`;
- `move_cross_prefecture`;
- `move_cross_province`.

If the underlying data support only province comparisons in some waves, keep those observations and record the available precision.

This allows later city-level work without rebuilding the sample from scratch.

---

## 6. Event-window redesign

The default master sample should be **unbalanced**.

Do not require every woman to contribute all event times from `-5` through `+5`.

Instead, for each respondent, record:

- earliest observable pre-arrival birth-history year;
- latest observable post-arrival year before survey;
- number of usable pre years;
- number of usable post years;
- maximum negative event time available;
- maximum positive event time available.

Create event-support flags such as:

- `has_pre1`, `has_pre3`, `has_pre5`;
- `has_post1`, `has_post3`, `has_post5`;
- `balanced_pm1`;
- `balanced_pm3`;
- `balanced_pm5`.

The preferred empirical architecture should be:

- unbalanced event-time sample as the broad main analysis;
- balanced `±3` / `±5` as robustness or comparability samples.

The re-audit must quantify how balanced-window requirements change:

- sample size;
- move cohort;
- survey-year composition;
- age at move;
- destination duration;
- origin/destination composition;
- observed fertility.

This is necessary to diagnose survivorship / duration selection.

---

## 7. Move reason redesign

Keep all move reasons in the broad master sample.

Create mutually exclusive reason groups such as:

- work/business;
- education;
- marriage;
- family reunification;
- child-related;
- housing;
- hukou/institutional;
- other;
- missing.

Do not automatically drop marriage/family movers from the master data.

Instead create:

- `reason_work_business`;
- `reason_marriage_family`;
- `reason_other`.

Possible later analysis samples may include:

- all movers;
- non-marriage movers;
- work/business movers;
- strict labor-market movers.

This allows us to distinguish sample definition from identification strategy.

---

## 8. Family-history quality redesign

Do not use one binary "usable fertility history" flag if quality differs across waves.

Create fertility-history tiers.

Suggested structure:

### Fertility Tier A

Child-specific birth year/month directly recorded with strong internal consistency.

### Fertility Tier B

Birth year recoverable, month missing or reconstructed.

### Fertility Tier C

Roster-derived fertility history or zero-parity assumption, such as the current 2017 convention.

### Fertility Tier D

Insufficient for dated birth-event analysis.

Similarly create marriage-history quality tiers:

- exact first-marriage year/month;
- first-marriage year only / inferable;
- current marital status only;
- insufficient.

Keep the broad master sample and allow outcome-specific estimands to invoke the relevant tier.

---

## 9. Migration-history quality redesign

Create explicit migration-history quality tiers.

At minimum distinguish:

### Migration Tier A

Current-arrival timing observed and prior location / single-spell structure directly observed.

### Migration Tier B

Current-arrival timing observed and direct-move structure strongly inferred.

### Migration Tier C

Current-arrival timing observed but intermediate migration cannot be ruled out.

### Migration Tier D

Arrival timing too weak for event-study use.

Create flags for:

- current-arrival year observed;
- current-arrival month observed;
- first-leave year observed;
- first-leave month observed;
- migration count observed;
- multiple-city indicator observed;
- timing contradictions;
- explicit multiple moves.

Do not collapse all of this into one `direct_move` variable.

---

## 10. External-data matching principle

The master sample must be created **before** any CBR / TFR / ASFR / marriage-place data are merged.

External matches should generate status variables, not sample-definition rules.

For every external dataset later used, report:

- number eligible before merge;
- number matched;
- number unmatched;
- match rate;
- unmatched distribution by survey year;
- origin;
- destination;
- geography precision;
- move cohort.

This prevents external-data availability from silently redefining the research population.

---

## 11. Recommended core sample families

The re-audit should produce counts for at least the following samples.

### Sample U — Research universe

Broad harmonized female sample.

### Sample M — Core mover master

Valid current-destination arrival + usable destination + some origin concept + dated fertility history.

No cross-province, no balanced-window, no move-reason, no external-data restrictions.

### Sample M-A/B — High-quality-origin movers

Origin tiers A or B.

### Sample M-C — Hukou-origin movers

Origin tier C.

These should coexist rather than one replacing the other.

### Sample BIRTH

Eligible for annual birth-event analysis.

### Sample MARRIAGE

Eligible for first-marriage timing analysis.

### Sample STRICT

High-quality origin + high-quality migration-history subset.

### Sample GEO-PREF

Origin and destination usable at prefecture level.

### Sample GEO-PROV

Origin and destination usable at province level.

### Matched treatment samples

Examples:

- Sample ASFR;
- Sample TFR;
- Sample marriage-rate;
- Sample CBR legacy.

These are estimation samples, not master samples.

---

## 12. What the new sample funnel should look like

Do **not** produce only one sequential funnel ending in a tiny final sample.

Produce two complementary outputs.

### A. Hard-eligibility funnel

Only restrictions needed for the broad mover/family-history design.

Example structure:

```
Research universe
-> usable demographics
-> current destination observed
-> current-arrival timing observed
-> at least one origin concept observed
-> dated fertility history usable
= Core mover master
```

### B. Orthogonal flag / tier table

From the core mover master, report counts and overlap for:

- origin tiers A/B/C/D;
- migration tiers A/B/C/D;
- fertility-history tiers;
- marriage-history tiers;
- cross-county / cross-prefecture / cross-province;
- move-reason groups;
- balanced ±1 / ±3 / ±5;
- 1 / 3 / 5 post years available;
- 1 / 3 / 5 pre years available;
- province-level geography;
- prefecture-level geography;
- legacy CBR matched / unmatched.

This is much more informative than one long chain of arbitrary drops.

---

## 13. Key diagnostic comparisons

The re-audit should compare the current 21,383 sample against the redesigned core mover master.

At minimum compare:

- survey year;
- move cohort;
- age at move;
- education;
- hukou type;
- marital status at move if available;
- parity at move;
- move reason;
- origin;
- destination;
- years since arrival at interview;
- fertility before move;
- fertility after move.

This will reveal what population the current sample selects.

Especially quantify the selection created by:

1. balanced `±5`;
2. work/business restriction;
3. cross-province restriction;
4. CBR matching.

---

## 14. No new causal model yet

This re-audit is a sampling and measurement task.

Do not add new causal specifications yet.

Do not choose the final fertility-place measure yet.

Do not search for significance across alternative samples.

The immediate goal is to establish a transparent large master sample and a hierarchy of analysis-ready subsamples.

---

## 15. Deliverables

Create:

```
fertility/SAMPLE_REAUDIT.md
fertility/SAMPLE_TIER_COUNTS.csv
fertility/SAMPLE_FLAG_DICTIONARY.md
```

If code is required, place it in a clearly named audit script and document its path.

The report must end with:

1. recommended Core Mover Master definition;
2. its sample size;
3. counts by origin quality tier;
4. counts by geographic scope;
5. counts by event-window support;
6. counts by move reason;
7. counts by fertility-history quality;
8. counts by marriage-history quality;
9. comparison with the legacy 21,383 sample;
10. a recommendation for which tiers should be used for:
   - main birth event study;
   - strict identification robustness;
   - marriage geography analysis;
   - future prefecture-level analysis.

