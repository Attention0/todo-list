# Fertility Geography Project — Work Instructions

## Objective

Audit the existing CMDS fertility / marriage / migration project so that Chat and the researcher can design a credible mover-design paper from the actual data rather than from assumptions about the data.

Read `fertility/SPEC.md` first and treat it as the research-design source of truth for this phase.

Do **not** try to maximize the number of regressions. Do **not** redesign the paper before understanding the data.

Your task is to determine exactly what is observed, what is reconstructed, what is assumed, and what is impossible.

---

## Required workflow

1. Read `fertility/SPEC.md`.
2. Inspect the entire repository structure.
3. Locate all CMDS raw-data references, cleaned files, code, variable dictionaries, questionnaires, outputs and notes available in the working environment.
4. Identify the current main-sample construction code.
5. Reproduce or trace the current sample flow.
6. Audit marriage and fertility variables year by year.
7. Audit migration and geography variables year by year.
8. Audit the current local-fertility / place-exposure construction.
9. Inventory all existing tables, figures and regressions.
10. Determine which mover-design components are fully feasible, assumption-dependent or infeasible.
11. Write the required audit documents listed below.
12. Do not add a new research design unless needed to diagnose feasibility.

When code has multiple versions, identify which version actually generates the current analysis sample and current outputs.

When documentation and code disagree, report the disagreement explicitly.

---

## General evidence standard

Every substantive audit conclusion should be traceable to actual project evidence.

Whenever possible report:

- exact variable name;
- survey year(s);
- source file;
- code file and relevant section / function;
- variable coding;
- missing-value coding;
- number and share missing;
- transformations already applied;
- assumptions imposed by current code;
- consequences for identification.

Do not write vague statements such as "CMDS has migration history" without specifying which variable and what it actually measures.

Do not interpret variable labels more strongly than the questionnaire permits.

---

# Task 1 — Audit the existing project and sample construction

Create `fertility/PROJECT_STATUS.md` and `fertility/SAMPLE_CONSTRUCTION.md`.

## 1. Repository map

Document:

- raw-data locations;
- cleaned-data locations;
- scripts;
- main-sample scripts;
- regression scripts;
- figure scripts;
- table scripts;
- external-data files;
- questionnaires / codebooks;
- generated outputs;
- intermediate datasets.

Identify the likely execution order of the project.

## 2. CMDS survey years

For every CMDS year found in the project, report:

| Year | Raw N | Used in current project? | Why included/excluded? | Key modules available |
|---|---:|---|---|---|

Check whether years are excluded because questionnaires or variable definitions differ.

## 3. Current sample definition

Document every current restriction, including where applicable:

- sex;
- age;
- hukou type;
- migrant status;
- marital status;
- geographic availability;
- cross-province / cross-city move;
- first move;
- duration in destination;
- fertility-history availability;
- marriage-history availability;
- migration-history availability;
- survey-year restrictions;
- other filters.

For every restriction, give the code location and number of observations removed if reproducible.

## 4. Sample flow

Construct the best possible sample flow:

```
Raw CMDS
-> demographic restrictions
-> migrant sample
-> usable migration timing
-> usable origin
-> usable destination
-> usable marriage/fertility information
-> current mover sample
-> final regression sample
```

Report at every step:

- observations before;
- observations removed;
- percent removed;
- observations remaining;
- reason for loss.

If the current code does not save these counts, derive them when feasible without changing the substantive sample definition.

## 5. Final-sample structure

Report:

- total observations;
- unique respondents;
- survey-year distribution;
- sex distribution;
- age distribution;
- birth cohorts;
- migration cohorts;
- number of origins;
- number of destinations;
- number of origin-destination pairs;
- observations per OD pair.

If the dataset is repeated cross-section rather than a true individual panel, state this explicitly.

---

# Task 2 — Audit marriage and fertility histories

Write the relevant sections of `fertility/VARIABLE_AUDIT.md`.

The key question is:

> Can a one-time CMDS respondent be expanded into a credible retrospective person-year marriage and fertility history?

## A. Fertility variables

Search every relevant CMDS year for variables measuring:

- children ever born;
- current number of children;
- living children;
- sons / daughters;
- first-birth age;
- first-birth year;
- birth date of each child;
- age of each child;
- second birth;
- third / higher-order birth;
- most recent birth;
- pregnancy;
- fertility intentions;
- ideal number of children;
- intention for another child;
- contraception;
- family-planning information;
- abortion / miscarriage if available.

Create a year-by-year table:

| Concept | Exact variable | Year(s) | Coding | Missing share | Can event timing be recovered? | Notes |
|---|---|---|---|---:|---|---|

Explicitly determine whether one can construct:

```
birth_it = 1
```

when respondent i gives birth in calendar year t.

State separately whether one can recover:

- first-birth year;
- each child's birth year;
- birth month;
- birth order;
- births before survey;
- births before migration;
- births after migration.

If birth year is derived rather than observed, document the formula and its measurement error.

## B. Marriage variables

Search for:

- current marital status;
- ever married;
- age at first marriage;
- first-marriage year;
- first-marriage month;
- remarriage;
- divorce;
- widowhood;
- spouse co-residence;
- spouse hukou;
- spouse birthplace;
- spouse current location;
- spouse education;
- spouse occupation;
- spouse income.

Determine whether one can construct:

```
MarriageYear_i
YearsSinceMarriage_it
MarriageBeforeMove_i
MarriageAfterMove_i
```

If marriage year is inferred from:

```
survey year - current age + age at first marriage
```

report this explicitly and discuss the resulting timing error.

## C. Marriage-fertility sequencing

Determine whether the data can distinguish:

- marriage before migration;
- marriage after migration;
- first birth before migration;
- first birth after migration;
- marriage-to-first-birth duration;
- fertility conditional on already being married at migration.

This is essential for distinguishing marriage-market effects from fertility effects conditional on marriage.

---

# Task 3 — Audit migration history and mover-design feasibility

Continue `fertility/VARIABLE_AUDIT.md` and create the migration sections of `fertility/IDENTIFICATION_FEASIBILITY.md`.

The central question is:

> What migration event does CMDS actually date?

Do not treat the following as equivalent unless the questionnaire proves they are equivalent:

- year first leaving hukou place;
- year first becoming a migrant;
- year arriving in the current destination;
- year of the latest move.

## A. Origin

Audit whether the data identify:

- hukou province;
- hukou prefecture;
- hukou county;
- birthplace;
- place of upbringing;
- previous residence;
- residence immediately before current destination.

Determine whether current code uses hukou place as origin.

If yes, explicitly assess whether:

```
hukou origin = actual pre-move location
```

is observed or assumed.

## B. Destination

Audit:

- survey location;
- current residence;
- province;
- prefecture;
- county / district;
- community;
- destination administrative code.

Determine which geography refers to sampling location versus actual residence.

## C. Migration timing

Search for:

- first migration year;
- first migration age;
- year leaving hukou place;
- year arriving in current city;
- age arriving in current city;
- duration of residence;
- latest move year;
- current-city duration.

Attempt to define the best possible:

```
MoveYear_i
```

but explicitly state what event it represents.

## D. Multiple moves

Audit whether CMDS observes:

- number of moves;
- intermediate destinations;
- previous city;
- multiple migration spells;
- return migration.

Determine whether the current design effectively assumes:

```
origin -> current destination
```

when the real history may be:

```
origin -> other places -> current destination
```

Quantify this issue when possible.

## E. Migration reason

Audit categories such as:

- work;
- job transfer;
- business;
- education;
- marriage;
- family reunification;
- child education;
- housing;
- hukou;
- other.

Report the distribution of migration reasons in the current mover sample.

Pay special attention to:

- marriage-motivated movers;
- family-motivated movers;
- plausibly economic movers;
- groups that may provide cleaner identification.

Do not label a migration category "exogenous" without a defensible argument.

---

# Task 4 — Test retrospective person-year feasibility

This is one of the most important deliverables.

Determine whether each respondent can be expanded into calendar years before the survey.

A target structure is:

| id | calendar_year | age | location | event_time | married | birth |
|---|---:|---:|---|---:|---:|---:|

For each column, classify the value as:

- directly observed;
- deterministically reconstructed;
- reconstructed under an assumption;
- unavailable.

In particular test whether location can defensibly be coded as:

```
t < MoveYear_i  -> origin
t >= MoveYear_i -> destination
```

If this is only an assumption, explain exactly why and identify which respondents are most likely to violate it.

Determine whether a credible pre-move outcome window exists.

---

# Task 5 — Audit geography and place definition

Add a geography section to `fertility/VARIABLE_AUDIT.md`.

## 1. Geographic levels

For origin and destination separately, identify the finest available level:

- province;
- prefecture city;
- county / district.

Determine the finest level consistently usable across all selected survey years.

## 2. Harmonization

Check for:

- inconsistent administrative codes across years;
- city-code format differences;
- municipality treatment;
- county-to-district changes;
- missing or suppressed geography.

Document whether current code already harmonizes codes.

## 3. Support

For province, prefecture and county levels when feasible, report:

- number of origins;
- number of destinations;
- number of OD pairs;
- observations per OD pair;
- P25;
- median;
- P75;
- P90;
- share of OD pairs with very small cell sizes.

Assess whether prefecture-level analysis is statistically plausible.

## 4. External merge keys

Identify the geographic IDs that could support merges with:

- census;
- statistical yearbooks;
- housing prices;
- wages;
- female employment;
- childcare;
- education;
- health services;
- hukou / public-service measures;
- sex ratio;
- marriage rates;
- fertility measures.

Do not build all external merges yet. Document the keys and feasibility.

---

# Task 6 — Audit the current place-fertility measure

Find every code object that corresponds to:

- origin fertility;
- destination fertility;
- local fertility;
- fertility gap;
- place exposure;
- destination-origin difference.

Document the exact formulas.

## A. Definition

Classify the current measure as one or more of:

- crude birth rate;
- TFR;
- age-specific fertility;
- children ever born;
- births per woman;
- completed fertility;
- CMDS sample fertility;
- census fertility;
- other.

## B. Data source

State whether it comes from:

- CMDS;
- census;
- yearbook;
- another dataset.

## C. Time structure

Determine whether the measure is:

```
Fertility_c
```

or:

```
Fertility_ct
```

or cohort-specific.

## D. Composition adjustment

Check whether the measure adjusts for:

- age;
- cohort;
- marital status;
- migrant composition.

If not, explain potential compositional bias.

## E. Mechanical correlation

If CMDS respondents are used to construct local fertility, determine whether respondent i's own outcome enters the place measure.

Check for:

- leave-one-out;
- leave-cohort-out;
- leave-survey-year-out.

## F. Treatment distribution

If current treatment is:

```
DeltaF_i = Fertility_destination(i) - Fertility_origin(i)
```

report:

- N;
- mean;
- standard deviation;
- percentiles;
- min / max;
- share positive;
- share negative;
- mass near zero.

Generate or locate distributions for:

- origin fertility;
- destination fertility;
- fertility gap.

Do not invent figures if the environment cannot generate them.

## G. Validation

Where already possible, assess whether local fertility rankings are stable across:

- survey years;
- alternative definitions;
- CMDS versus external sources.

---

# Task 7 — Inventory existing analyses

Create `fertility/EXISTING_RESULTS.md`.

For every existing table, figure or regression, report:

- file / output name;
- code producing it;
- dependent variable;
- treatment / key regressor;
- sample;
- fixed effects;
- controls;
- standard-error clustering;
- geographic level;
- estimated direction;
- approximate magnitude;
- interpretation currently implied;
- important caveats.

Separate descriptive results from causal / quasi-causal results.

Do not treat statistical significance as proof of identification.

---

# Task 8 — Produce the identification-feasibility assessment

Create `fertility/IDENTIFICATION_FEASIBILITY.md`.

Classify each component into three categories.

## Level A — Fully feasible from observed information

No major timing or location assumption is required beyond ordinary data cleaning.

## Level B — Feasible only with explicit assumptions

State each assumption separately and assess its plausibility.

## Level C — Not feasible with current CMDS information

Do not propose cosmetic workarounds that silently change the estimand.

At minimum evaluate:

1. observing fertility before migration;
2. observing fertility after migration;
3. constructing event time relative to migration;
4. conducting a meaningful pre-trend analysis;
5. dating marriage relative to migration;
6. separating marriage formation from fertility conditional on marriage;
7. identifying the actual city of residence before migration;
8. identifying current-destination arrival year;
9. constructing origin-destination fertility gaps;
10. prefecture-level mover design;
11. multiple-move correction;
12. merging external city-level variables;
13. measuring destination assimilation;
14. comparing immediate versus gradual responses.

End the document with:

### Three largest identification threats

Rank by importance only if the evidence clearly supports a ranking; otherwise list the three most consequential threats without arbitrary scoring.

For each threat provide:

- source of the problem;
- affected estimand;
- likely direction of bias if knowable;
- feasible diagnostic;
- feasible mitigation;
- residual limitation.

---

# Task 9 — Required matrices

Include the following in `fertility/VARIABLE_AUDIT.md` or `fertility/IDENTIFICATION_FEASIBILITY.md`.

## Research-variable matrix

| Research need | Available variable | Survey years | Quality | Main issue |
|---|---|---|---|---|

Cover at minimum:

- marriage timing;
- first birth;
- higher-order births;
- current fertility;
- fertility intention;
- origin;
- destination;
- migration timing;
- migration reason;
- spouse location;
- hukou;
- geographic merge key.

## Design-feasibility matrix

| Design component | Fully feasible | Feasible with assumptions | Not feasible | Explanation |
|---|---|---|---|---|

Only one feasibility category should be marked for each component.

---

# Task 10 — Final synthesis

At the end of `fertility/IDENTIFICATION_FEASIBILITY.md`, answer these questions explicitly.

1. What is the cleanest migration event observed in CMDS?
2. What is the cleanest origin definition?
3. What is the cleanest destination definition?
4. What marriage events can be dated?
5. What birth events can be dated?
6. Can a retrospective person-year dataset be built?
7. For which years before and after migration is it credible?
8. Is a true mover-style pre-trend test possible?
9. Is prefecture-level analysis feasible?
10. What is the current place-fertility measure?
11. What are the main mechanical / compositional problems in that measure?
12. Which parts of the Labour Economics benchmark can be replicated credibly?
13. Which benchmark components cannot be replicated?
14. Which China-specific mechanism directions are supported by actual variables?
15. What new data or external data would most improve the design?

---

# Required files

Create or update exactly these audit outputs:

```
fertility/PROJECT_STATUS.md
fertility/SAMPLE_CONSTRUCTION.md
fertility/VARIABLE_AUDIT.md
fertility/IDENTIFICATION_FEASIBILITY.md
fertility/EXISTING_RESULTS.md
```

Do not overwrite `fertility/SPEC.md` or `fertility/WORK.md` unless specifically asked.

---

# Coding rules during the audit

You may run code needed to:

- inspect variables;
- reproduce sample counts;
- summarize missingness;
- reconstruct existing variables;
- verify current outputs;
- test whether retrospective histories can be generated;
- calculate OD support;
- diagnose current place measures.

Do not add substantive new model specifications merely because they are easy to run.

If you create temporary diagnostic scripts, place them in a clearly named audit / scratch location and document them.

Never silently change current sample definitions.

---

# Reporting standard

For every important conclusion distinguish:

**Observed fact** — directly in data / questionnaire / code.

**Reconstruction** — calculated deterministically from observed variables.

**Assumption** — needed to interpret a reconstruction as a migration or family-history event.

**Unknown** — cannot be determined from available material.

This distinction is mandatory.

---

# Definition of done

The audit is complete only when:

1. the current project can be understood without rereading all code;
2. the full current sample construction is documented;
3. marriage and fertility timing variables are mapped by year;
4. migration timing and geography are mapped by year;
5. retrospective person-year feasibility has been tested;
6. the current place-fertility measure is fully documented;
7. existing results are inventoried;
8. mover-design components are classified by feasibility;
9. the largest identification threats are stated clearly;
10. the five required Markdown outputs exist and contain evidence-based conclusions.

The goal is not to make the project look feasible.

The goal is to establish the true research boundary of the CMDS data so that the next research-design stage can be ambitious **and** credible.
