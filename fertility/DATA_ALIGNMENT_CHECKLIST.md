# Fertility Geography — Data Alignment Checklist

## Purpose

This file is a **reconciliation checklist**, not a statement that every item below is already known to be true.

Chat currently has a working understanding of the CMDS project from prior discussion, but the final source of truth must be the actual questionnaires, raw/clean data, code and generated samples in the Work environment.

**Work must verify every item below and classify it as:**

- **Confirmed** — directly supported by questionnaire/data/code;
- **Partially confirmed** — available only in some years or with important assumptions;
- **Incorrect** — Chat's current working understanding is wrong;
- **Unknown** — cannot be established from the available project material.

Do not silently reconcile disagreements. Record them explicitly.

---

## A. Main sample and survey structure

| Item to verify | Chat working understanding | Evidence Work must report |
|---|---|---|
| Survey structure | CMDS is primarily repeated cross-section; retrospective variables may permit reconstruction of past events, but this is not equivalent to a true longitudinal panel | Exact survey design, respondent IDs across waves, whether any individuals can actually be linked over time |
| Survey years | Multiple CMDS years are available, but the set actually usable for fertility/migration analysis must be verified | Year-by-year raw N, modules, usable N and reason for inclusion/exclusion |
| Main sample philosophy | Keep a broad main sample first; do **not** impose cross-province, balanced-panel or other restrictive filters merely to make identification look cleaner | Current code restrictions and sample loss from each; identify which are necessary for measurement versus optional robustness restrictions |
| Sex/age risk set | Fertility outcomes require a biologically/economically meaningful risk set rather than an arbitrary all-migrant sample | Exact age/sex restrictions and how risk sets change for first birth, higher-order birth, marriage and fertility intention outcomes |
| Current migrant selection | CMDS samples migrants observed at the destination; this may create selection on remaining in migration rather than returning home | Whether return migrants/nonmigrants are absent by design; what population the sample represents |

---

## B. Geography and migration history

### B1. Origin definitions

Work must separately audit and preserve:

1. **Hukou origin**
2. **Previous residence / residence immediately before the current destination**, if observed
3. Birthplace / place of upbringing, if observed
4. First place left at migration, if observed

Do **not** collapse these definitions into a single "origin" variable.

Required reconciliation table:

| Origin concept | Exact variable(s) | Years | Geographic level | Directly observed or inferred? | Missing share | Main interpretation problem |
|---|---|---|---|---|---:|---|

The preferred workflow is to retain multiple origin definitions and attach an origin-source flag, rather than prematurely choosing one.

### B2. Destination

Verify separately:

- survey sampling location;
- current residence;
- current city/prefecture;
- current county/district;
- province;
- administrative codes used for external merges.

Report the finest geography that is consistently available for both origin and destination.

### B3. Migration timing

The following are **not interchangeable** and must be audited separately:

- first year leaving hukou place;
- first migration year;
- first year becoming a migrant;
- arrival year in current destination;
- latest move year;
- duration in current city.

Work must identify which event each variable truly dates.

### B4. Multiple moves

Test whether the observed history is actually:

```
origin -> current destination
```

or may instead be:

```
origin -> intermediate place(s) -> current destination
```

Required outputs:

- whether number of prior moves is observed;
- whether previous city is observed;
- whether intermediate destinations are observed;
- share of respondents for whom a single-move interpretation is defensible;
- whether a recent-mover or one-move robustness sample can be constructed without redefining the main sample.

### B5. Migration motives

Audit the exact categories and sample shares for:

- employment / job transfer;
- business;
- education;
- marriage;
- family reunification;
- child education;
- housing;
- hukou/institutional reasons;
- other.

The existence of a migration-reason variable is useful for diagnosis but **does not by itself make migration exogenous**.

---

## C. Marriage and fertility histories

### C1. Marriage timing

Verify exact availability of:

- current marital status;
- ever married;
- age/year/month at first marriage;
- remarriage/divorce/widowhood;
- spouse co-residence;
- spouse hukou/origin/current location;
- spouse education/occupation/income.

Determine whether one can classify:

```
marriage before move
marriage near move
marriage after move
```

and with what timing error.

### C2. Birth history

Verify year-by-year availability of:

- children ever born;
- living children;
- birth order;
- first-birth age/year;
- birth year/month for each child;
- second/higher-order births;
- most recent birth;
- pregnancy;
- fertility intention / ideal number of children;
- contraception/family-planning variables.

The essential question is whether one can defensibly reconstruct:

```
birth_it = 1 if respondent i gives birth in calendar year t
```

and separately identify first versus higher-order births.

### C3. Fertility–migration sequencing

Work must report whether the data can identify:

- births at least 2–3 years before migration;
- pregnancy/birth in the year immediately before migration;
- birth in the migration year;
- births after migration;
- marriage-to-first-birth duration;
- fertility conditional on already being married before migration.

This sequencing is required to test **fertility-induced migration** rather than assuming it away.

---

## D. Place-fertility measure

Work must fully reconstruct the current treatment variable.

At minimum determine whether the place measure is:

- crude birth rate (CBR);
- age-specific fertility rate (ASFR);
- total fertility rate (TFR);
- births per woman / children ever born;
- a CMDS internal sample mean;
- an external census/yearbook measure;
- time-varying (city × year) or time-invariant;
- age/cohort/parity adjusted.

If CMDS itself is used to construct local fertility, Work must check:

1. whether respondent i's own outcome enters the place measure;
2. leave-one-out construction;
3. leave-cohort-out / leave-survey-year-out construction;
4. minimum city cell size;
5. sensitivity to age standardization;
6. stability across survey years;
7. comparison with an external fertility ranking where possible.

Preserve both origin and destination place measures before constructing the gap.

---

## E. Person-year reconstruction

Work must try to build a small diagnostic person-year dataset, not yet a final analysis sample.

Target structure:

| id | calendar_year | age | location | event_time | marital_status | parity | birth |
|---|---:|---:|---|---:|---|---:|---:|

Each field must be labelled as:

- directly observed;
- deterministically reconstructed;
- reconstructed under an explicit assumption;
- unavailable.

The key test is whether coding

```
t < MoveYear_i  -> origin
t >= MoveYear_i -> destination
```

is observed truth or only an assumption. If only an assumption, quantify how many respondents are most likely to violate it.

---

## F. CMDS-specific selection threats

These issues are especially important because the benchmark Labour Economics paper uses a long PSID panel, whereas CMDS may observe a stock of current migrants.

Work must diagnose:

### F1. Survivorship / stay-in-destination selection

A migrant is observed only if still in the sampled destination at survey time. Fertility may affect:

- returning home;
- onward migration;
- leaving the labor force;
- family reunification.

Therefore the observed post-move fertility response can be selected on remaining in the destination.

Report all variables that help diagnose duration, return intention, settlement intention or onward mobility.

### F2. Retrospective censoring

Older migrants mechanically contribute longer pre/post histories than recent migrants. Determine whether event-time estimates would mix migration cohorts, ages and survey years.

### F3. Policy-cohort composition

China's fertility policy changed sharply over time. Determine how migration cohorts overlap with:

- one-child era;
- selective/partial two-child relaxation;
- universal two-child era;
- three-child era if relevant to available survey years.

Do not treat policy periods as interchangeable.

---

## G. Mobility network and AKM feasibility

If the project estimates individual/place fixed effects or an AKM-style variance decomposition, Work must report:

- number of origins and destinations;
- number of OD links;
- size of the largest connected set;
- movers per city;
- degree distribution of the mobility graph;
- weakly connected/isolated cities;
- whether place effects are identified from thin mobility links.

Do not interpret a raw variance of estimated place fixed effects as causal place variance without diagnosing finite-sample / limited-mobility bias.

---

## H. Required reconciliation output from Work

Create:

```
fertility/DATA_RECONCILIATION.md
```

It must contain:

1. a row-by-row verdict on this checklist;
2. exact variable names and survey years;
3. sample counts;
4. evidence from code/questionnaires;
5. any contradiction with `SPEC.md`, `WORK.md` or prior results;
6. a final list titled **"Facts Chat can safely treat as established"**;
7. a final list titled **"Assumptions Chat must not silently make"**.

Do not change the substantive research design while performing this reconciliation.
