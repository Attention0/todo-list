# Fertility Geography Project — Research Specification

## 1. Project goal

Build an economics research project using China Migrants Dynamic Survey (CMDS) data to study how place shapes marriage and fertility outcomes through a mover-design framework.

The closest benchmark is the Labour Economics paper using mover design to study geographic variation in fertility. This project must not stop at a China replication. The target is a substantially upgraded paper with a general-interest contribution, ideally strong enough to be developed toward an AER-level standard.

The project should therefore answer two layers of questions:

1. **Existence:** Does moving to a different local environment causally shift marriage and fertility outcomes toward the destination?
2. **Mechanism:** Why does place matter for family formation, and which parts of the local environment generate the effect?

The current phase is not to maximize the number of regressions. The current phase is to establish exactly what the CMDS data can and cannot identify.

---

## 2. Core conceptual upgrade

The baseline mover-design question is approximately:

> Do people who move to higher-fertility places subsequently behave more like residents of those destinations?

Our project should aim for a broader question:

> **Why does place shape family formation?**

The preferred conceptual object is therefore not fertility alone, but the full geography of family formation:

```
Place
  -> Marriage
  -> Timing of marriage
  -> First birth
  -> Marriage-to-birth transition
  -> Second / higher-order birth
  -> Completed or cumulative fertility
```

A successful paper should determine where in this chain place matters and what economic mechanisms generate the response.

---

## 3. Research ambition hierarchy

### Level 1 — Replication layer

Establish whether there are measurable fertility place effects among Chinese internal migrants.

Possible core exposure:

```
Destination fertility - Origin fertility
```

or a richer city-level index of the family-formation environment.

This layer is necessary but not sufficient for the final contribution.

### Level 2 — Family-formation layer

Study whether place affects the entire process of family formation rather than only number of children.

Potential outcomes include:

- marriage formation;
- age / timing of first marriage;
- first birth;
- timing from marriage to first birth;
- second birth;
- higher-order births;
- cumulative number of children;
- fertility intentions if available.

A central question is whether geographic fertility differences operate mainly through:

```
Place -> Marriage
```

or through:

```
Place -> Fertility conditional on marriage
```

or through both.

### Level 3 — Mechanism layer

Explain the place effect using economically interpretable local environments.

Candidate mechanisms include:

#### Economic constraints

- housing costs;
- wages;
- employment conditions;
- female labor-market opportunities;
- job stability;
- childcare cost / availability;
- cost of raising children.

#### Local institutions and access

- hukou status;
- access to local public services;
- education eligibility;
- maternity / health services;
- social insurance;
- housing access;
- other place-specific institutional benefits.

A potentially important hypothesis is:

> **Place effects depend on access to the place.**

Physical residence in a city need not imply equal access to the institutions and services of that city.

#### Marriage markets

- local sex ratio;
- education distribution;
- migrant composition;
- local wages / income distribution;
- marriage-market thickness;
- local marriage norms.

Potential chain:

```
Place
  -> Marriage market
  -> Marriage formation
  -> Fertility
```

#### Family networks and informal childcare

Migration may separate migrants from parents and extended family.

Potential chain:

```
Migration
  -> Distance from family network
  -> Informal childcare constraint
  -> Marriage / fertility response
```

### Level 4 — General-interest interpretation

The strongest version of the project would establish that "place" is not a homogeneous treatment.

The realized local environment may depend on:

```
Place
x Hukou / institutional access
x Family networks
x Economic constraints
x Marriage-market position
```

This would shift the paper from documenting geographic fertility differences to explaining how spatial institutions and constraints shape family formation.

---

## 4. Key identification question

CMDS is not automatically equivalent to a long individual panel.

The central design question is whether retrospective information can reconstruct a credible individual-by-year history around migration.

The ideal reconstructed data would contain:

| id | calendar_year | age | location | post_move | married | birth |
|---|---:|---:|---|---:|---:|---:|

The project must determine whether the data permit a defensible construction of:

```
MoveYear_i
MarriageYear_i
BirthYear_ik
Location_it
```

and therefore event time:

```
EventTime_it = t - MoveYear_i
```

The most important distinction is between:

1. observing the year someone first left the hukou location;
2. observing the year someone arrived at the current destination;
3. observing a complete sequence of prior locations.

These are not interchangeable.

---

## 5. Main empirical objects to evaluate

The audit should determine whether the data can support some version of the following objects.

### Place exposure

```
DeltaPlace_i =
PlaceMeasure_destination(i)
-
PlaceMeasure_origin(i)
```

For fertility specifically:

```
DeltaF_i =
Fertility_destination(i)
-
Fertility_origin(i)
```

### Event-time response

If retrospective histories are credible:

```
Y_it = f(EventTime_it, DeltaPlace_i, controls, fixed effects)
```

with emphasis on:

- pre-move patterns;
- immediate post-move effects;
- gradual assimilation;
- heterogeneous adjustment by duration.

### Marriage-versus-fertility decomposition

Where possible, separate:

- effect on marriage;
- effect on fertility conditional on marriage;
- effect on birth timing;
- effect on first versus higher-order births.

This decomposition is central to upgrading the paper beyond a direct fertility replication.

---

## 6. Why dynamics matter

The timing of the response may itself help distinguish mechanisms.

An immediate response after moving is more consistent with rapidly changing constraints or opportunities.

A gradual response with years since migration is more consistent with:

- norm assimilation;
- network formation;
- adaptation to local institutions;
- cumulative integration into the destination.

Therefore event-time dynamics should ultimately be treated not only as an identification diagnostic but also as a mechanism diagnostic.

---

## 7. China-specific research opportunities

The China setting offers several dimensions that may create a contribution beyond the existing mover-design literature:

- very large internal migration flows;
- hukou-based institutional access;
- large cross-city differences in housing costs and labor markets;
- strong dependence on family / grandparental childcare;
- local marriage-market differences;
- rapid urbanization;
- major fertility-policy regime changes;
- potentially large differences between migrants and local residents.

A later stage may study interactions between national fertility-policy changes and local environments, but this should not be imposed before data feasibility is established.

---

## 8. Data audit required before new modeling

The next research phase must answer six concrete questions.

### A. Existing project status

- Which CMDS years are currently used?
- What code constructs the current main sample?
- What restrictions are applied?
- What outputs already exist?
- What is the exact sample flow from raw data to regression sample?

### B. Marriage and fertility histories

Can the data identify:

- first-marriage timing;
- current and past marital status;
- birth timing;
- first, second and higher-order births;
- fertility intentions;
- retrospective annual birth events?

### C. Migration histories

Can the data identify:

- hukou origin;
- actual pre-move residence;
- current destination;
- year first leaving origin;
- year arriving at destination;
- intermediate moves;
- migration reason;
- return migration?

### D. Geographic resolution

At what common level can origin and destination be harmonized?

- province;
- prefecture city;
- county / district.

Can the geography be merged reliably with external city-level data?

### E. Place measures

How is local fertility currently defined?

- CMDS internal measure;
- census;
- statistical yearbook;
- crude birth rate;
- TFR;
- age-specific fertility;
- children ever born;
- another measure.

Is the measure:

- age-adjusted;
- year-specific;
- cohort-specific;
- leave-one-out;
- externally validated?

### F. Identification boundary

Which components are:

- fully supported by observed information;
- feasible only under explicit assumptions;
- impossible with the available CMDS variables?

---

## 9. Main threats that must be investigated

At minimum, the research design must take seriously:

### Migration selection

People choose destinations. Movers to high- and low-fertility places may differ before moving.

### Reverse causality

Marriage, pregnancy or expected fertility may itself cause migration.

Marriage-motivated migration must be separately identified if possible.

### Origin mismeasurement

Hukou location may not equal the location immediately before the current move.

### Destination timing mismeasurement

First year away from hukou may not equal arrival year in the current city.

### Multiple moves

Observed current origin-destination pairs may compress a more complex migration history.

### Retrospective recall

Marriage and birth dates may be reconstructed with measurement error.

### Mechanical local fertility measures

If local fertility is computed from CMDS respondents, an individual's own outcome may mechanically enter the local measure.

### Geographic composition

Cross-place fertility differences can reflect age, cohort, marital-status and migrant-composition differences rather than local causal environments.

---

## 10. External data possibilities

The audit should preserve geography keys that may later be merged with external data on:

- census fertility;
- population structure;
- local GDP and wages;
- housing prices;
- female employment;
- childcare availability;
- education;
- healthcare;
- hukou / public-service access;
- sex ratio;
- migrant composition;
- local marriage rates;
- other city-level family-formation conditions.

Do not merge these yet unless needed to validate existing place measures. First establish merge feasibility.

---

## 11. Current-phase non-goals

During the audit phase, do not:

- add a large battery of new regressions;
- choose a final mechanism prematurely;
- treat hukou origin as true pre-move residence without checking;
- treat first migration year as current-destination arrival year without checking;
- claim a panel design if only retrospective proxies exist;
- create external-data pipelines before geography has been audited;
- optimize presentation before identification feasibility is known.

---

## 12. Required outputs from the audit phase

The audit should eventually create:

```
fertility/
  SPEC.md
  WORK.md
  PROJECT_STATUS.md
  SAMPLE_CONSTRUCTION.md
  VARIABLE_AUDIT.md
  IDENTIFICATION_FEASIBILITY.md
  EXISTING_RESULTS.md
```

The audit must also contain two compact matrices.

### Research-variable matrix

| Research need | Available variable | Survey years | Quality | Main issue |
|---|---|---|---|---|

### Design-feasibility matrix

| Design component | Fully feasible | Feasible with assumptions | Not feasible | Explanation |
|---|---|---|---|---|

---

## 13. Definition of success for this phase

This phase is complete only when we can answer, with evidence from the actual data and code:

1. What exactly is the current CMDS sample?
2. What marriage and fertility events can be dated?
3. What migration event can actually be dated?
4. What location is observed before and after migration?
5. What geographic level is usable?
6. How is the current place-fertility measure constructed?
7. Can a retrospective person-year dataset be constructed credibly?
8. Can pre-move outcomes be observed?
9. Which mover-design estimands are defensible?
10. Which benchmark-paper analyses cannot be replicated?
11. What are the three largest identification threats?
12. Which China-specific mechanism directions remain empirically feasible?

Only after these questions are resolved should the project move into the next stage of model design, mechanism selection and paper architecture.
