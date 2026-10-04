# Fertility Geography — Identification Upgrade Plan

## 1. Research strategy

The project should use Wu & Zhu (2026), **"Geographic variation in fertility: evidence from mover design," Labour Economics 100, 102895**, as the closest benchmark.

The goal is **not** to argue that a similar paper makes our project uninteresting. The benchmark establishes that the question is publishable and provides a useful starting design. Our advantage is a different institutional setting, unusually large internal migration flows, hukou-based access, policy changes and potentially much richer cross-place heterogeneity.

The correct sequence is:

```
benchmark replication / translation
-> identify and close causal-identification gaps
-> establish a defensible China mover design
-> only then exploit CMDS/China-specific data to discover the distinctive result
-> build mechanisms around results that survive the clean design
```

Do not start by searching for a surprising mechanism and then retrofit identification.

---

## 2. What the Labour Economics benchmark already does

The benchmark is stronger than a simple before/after mover regression. According to the published article, it uses PSID 1969–2019 and includes:

1. individual fixed effects;
2. event-study pre-trend analysis;
3. self-reported migration-motive balance;
4. matched event studies using in-state nonmovers;
5. AKM-style sorting diagnostics using covariance between individual and place effects;
6. tests using changes in time-varying observables;
7. moves associated with natural disasters as a plausibly more exogenous subset;
8. an IV strategy following the Chyn–Shenhav place-effect design;
9. movers-only specifications;
10. exclusion of job-related relocations;
11. balanced-panel specifications;
12. alternative birth-rate measures;
13. alternative clustering choices;
14. heterogeneity by first versus higher-order births and demographic groups;
15. an AKM-style variance decomposition;
16. correlations of estimated place effects with local contraception, healthcare and other state characteristics.

Therefore our upgrade cannot simply be "add an event study" or "control for migration reason." Those are benchmark requirements, not contributions.

---

## 3. What top mover/place-effect papers teach us

The most useful comparison set includes:

- Finkelstein, Gentzkow & Williams (QJE 2016), patient migration and health-care use;
- Chetty & Hendren (QJE 2018 I/II), childhood exposure effects;
- Cantoni & Pons (AER 2022), relocations and voting behavior;
- Chyn & Shenhav (AEJ: Economic Policy 2025), place effects in health at birth;
- related modern worker-location mover designs.

The central lesson is that a convincing mover design does not rest on one regression. It builds a **stack of falsification and overidentification tests** that make alternative selection stories increasingly hard to sustain.

For this project, the main threats are unusually fertility-specific:

```
unobserved fertility shock
-> migration decision / destination choice
-> observed birth
```

and, in CMDS:

```
fertility / family event
-> return or onward migration
-> probability of remaining in the sampled destination
-> being observed in CMDS
```

These two channels must be attacked directly.

---

# 4. Identification program

The tasks below are ordered by priority. The main sample should remain broad. Restrictive samples are diagnostics/robustness exercises unless measurement logically requires the restriction.

## Tier 0 — Measurement must be credible before causal estimation

### 0.1 Verify the actual move

Need to know:

- actual previous residence;
- arrival year in current destination;
- whether hukou origin equals previous residence;
- whether intermediate moves occurred.

Run the main design under multiple defensible origin definitions where possible:

```
Origin A = previous residence
Origin B = hukou origin
```

and preserve an origin-source indicator.

**Failure mode:** if event time refers to first migration but destination refers to current city after multiple moves, the event study is mis-timed and the treatment gap is mismeasured.

### 0.2 Construct an independent place measure

Preferred hierarchy:

1. external city × year fertility measure, age-standardized;
2. external multi-year pre-move city fertility measure;
3. CMDS measure from an independent sample / split sample;
4. leave-one-out CMDS measure;
5. raw same-sample city mean only as a descriptive object.

For CMDS-internal measures, test:

- leave-one-out;
- split-sample estimation;
- leave-cohort-out;
- leave-survey-year-out;
- minimum cell sizes;
- reliability/shrinkage.

**Reason:** the focal respondent's own fertility must not mechanically define the destination's "fertility environment."

### 0.3 Define fertility risk sets correctly

Estimate separate outcomes for:

- first birth among childless women;
- second birth among one-child women;
- higher-order births where policy/risk set permits;
- any annual birth among women of reproductive age;
- marriage formation among unmarried individuals.

Do not mechanically control for post-treatment marriage in the total fertility effect. Treat "fertility conditional on marriage" as a separate estimand.

---

## Tier 1 — Necessary causal-defense analyses

### 1.1 Fertility-induced migration / reverse causality

This should be more explicit than in the benchmark because childbirth itself can trigger migration in China.

Construct event-time indicators for:

- conception/birth 1–2 years before migration;
- birth in migration year;
- marriage immediately before migration;
- marriage in migration year;
- first birth immediately after migration.

Required diagnostics:

1. pre-move fertility hazard by destination fertility gap;
2. marriage hazard by destination fertility gap;
3. "donut" specifications excluding moves within ±1 year of marriage/birth;
4. broader ±2-year donut;
5. exclude marriage/family-reunification movers;
6. separately estimate work/education movers;
7. test whether treatment gap predicts migration timing itself.

If effects disappear only after removing moves surrounding marriage or birth, the interpretation must shift from "place causes fertility" toward "family formation causes migration."

### 1.2 Event-study pre-trends with a meaningful pre-period

Use the longest credible pre-period permitted by actual residence histories.

The key coefficients are not merely whether individual pre-period coefficients are insignificant. Report:

- joint pre-trend test;
- slope of pre-trend;
- economic magnitude relative to post effect;
- bins far from the move;
- confidence intervals.

If pre-move location is uncertain, do not present a conventional pre-trend graph as if it were clean.

### 1.3 Within-origin comparison

A strong specification should compare movers who begin from similar origins but move to destinations with different fertility environments.

Candidate controls/fixed effects:

- origin FE;
- origin × migration-cohort FE;
- origin × survey-year FE;
- age/cohort FE;
- migration-reason FE;
- possibly origin × reason × cohort cells where support permits.

The conceptual comparison is:

```
same/similar origin
+ similar move timing
+ different destination fertility environment
```

rather than a pooled comparison of all high-gap and low-gap movers.

### 1.4 Destination-choice observables and balance

Regress the destination fertility gap on pre-move characteristics that are not themselves outcomes of the move:

- age;
- education determined before move;
- hukou;
- origin characteristics;
- pre-move marital/parity status;
- migration reason;
- baseline labor status if truly pre-move;
- family background if available.

Do not use post-move covariates as ordinary "controls" when they may be mediators.

### 1.5 Up-moves versus down-moves and symmetry

Estimate separately:

- low-fertility -> high-fertility;
- high-fertility -> low-fertility.

Ask whether response is symmetric in sign/magnitude and whether pre-trends differ.

Asymmetry may be substantively interesting, but it can also reveal destination selection.

### 1.6 Multiple-move robustness

Run, when feasible:

- one-move / previous-residence sample;
- recent movers;
- respondents for whom first migration year equals current-city arrival year;
- broad main sample with all movers.

The main point is to establish whether compressed migration histories drive results.

### 1.7 CMDS stock-sample / survivorship selection

This is a major design difference from PSID.

Test whether duration in destination and observable settlement propensity vary with:

- fertility gap;
- parity;
- marriage status;
- births after move;
- migration reason.

Where possible use:

- duration-specific estimates;
- recently arrived movers;
- settlement-intention / return-intention outcomes;
- inverse-probability or reweighting diagnostics only if a credible selection model can be justified.

Do not claim these fully solve unobserved return-migration selection.

### 1.8 Standard-error level

Because treatment varies at origin/destination/place level, compare:

- individual-robust SE;
- origin-clustered;
- destination-clustered;
- two-way origin × destination clustering when feasible;
- wild-cluster/bootstrap methods if effective cluster counts are small.

The preferred inference should reflect the actual level of independent treatment variation.

---

## Tier 2 — Top-journal-style overidentification and validation

### 2.1 Group-specific place-effect placebo tests

This is one of the strongest possible upgrades inspired by Chetty–Hendren.

Construct fertility environments specific to the individual's relevant group where data permit, for example:

- age group;
- parity;
- marital status;
- policy-eligibility group;
- possibly hukou status.

Then test whether an individual's fertility responds more strongly to the destination fertility pattern of **her own relevant group** than to unrelated groups.

Examples:

```
childless woman -> destination first-birth rate should matter
                 destination third-birth rate should not predict as strongly

woman aged 25-29 -> destination fertility of women 25-29 should matter
                   fertility of post-reproductive women should not
```

These are not generic placebo outcomes; they are **overidentification tests** exploiting heterogeneous predicted place effects.

### 2.2 Exposure-duration logic

Top mover designs often gain credibility when treatment responses scale with actual exposure.

Test whether response varies with:

- years since arrival;
- age at arrival;
- duration under the destination policy/institutional environment.

A causal place story is stronger if the response evolves in a coherent exposure pattern rather than appearing only as a one-time discontinuity associated with the move.

For fertility, interpret carefully because timing/spacing mechanically matter.

### 2.3 Leave-one-origin / other-mover prediction IV

Adapt the Chyn–Shenhav logic where data support it.

Potential object:

```
predicted destination quality gap
= destination/origin fertility quality estimated from other movers / independent observations
```

Use strictly separated samples so focal individuals do not create their own instrument.

Required tests:

- first-stage strength;
- pre-move placebo outcome;
- sensitivity to leave-one-origin and leave-one-destination constructions;
- exclusion restriction discussion.

### 2.4 Plausibly exogenous migration shocks in China

Potential candidates should be treated as research hypotheses, not automatically valid instruments.

#### Hukou reforms

Could help if reforms shift migration costs/access in a way that changes exposure to destinations.

But verify:

- rollout timing;
- city-level intensity;
- whether reforms directly affect fertility through public-service access.

If the reform directly changes fertility-relevant benefits, it may identify **access to place** rather than serve as an excluded instrument for migration.

#### Administrative / labor-market relocation shocks

Search project/external data for plausibly exogenous displacement or assignment-type moves.

Do not label job transfer as exogenous without evidence.

### 2.5 Fertility-policy shocks as validation/mechanism, not naive migration IV

The two-child policy directly changes fertility incentives, so it generally **fails the exclusion restriction as an IV for place exposure**.

A better use is interaction / difference-in-differences logic:

```
pre vs post policy
x eligibility/parity
x destination institutional access / local constraint
```

This can test whether the measured place effect reflects binding fertility constraints or local implementation/access.

### 2.6 AKM connected-set and finite-sample bias diagnostics

If retaining AKM decomposition:

1. construct the mobility graph;
2. report connected set;
3. diagnose thin city links;
4. compare raw and bias-corrected variance components if feasible;
5. use split-sample / leave-out methods where possible;
6. separate descriptive covariance from causal sorting claims.

A large estimated variance of place fixed effects can be inflated by noisy small-cell place estimates.

---

## Tier 3 — Robustness package after the core design survives

Run only after Tier 0–2 feasibility is understood.

- province vs prefecture vs county/place definitions;
- external versus internal fertility measures;
- alternative age standardization;
- alternative event windows;
- recent movers only;
- exclude marriage movers;
- exclude family reunification movers;
- work movers only;
- cross-province movers;
- within-province movers;
- stable hukou groups;
- alternative cluster levels;
- placebo move dates;
- placebo destination measures;
- reweight movers to broader CMDS composition.

Do **not** define one extremely restrictive robustness sample as the only "main" sample unless measurement makes it necessary.

---

# 5. Mechanisms: what the benchmark leaves open

The Labour Economics paper correlates place effects with state characteristics such as contraception and healthcare infrastructure. These are useful correlations, but they do not by themselves identify mechanisms causally.

Our mechanism stage should distinguish:

```
place effect exists
```

from

```
we know why place effect exists
```

After the causal mover design is stable, exploit China-specific margins:

1. **Hukou / access to place**
   - same physical city, unequal public-service access;
   - interaction between destination quality and access eligibility;
   - strongest conceptual possibility: place is not equivalent to access to place.

2. **Fertility-policy regime**
   - first vs second birth;
   - policy eligibility;
   - local implementation/access differences.

3. **Marriage market**
   - sex ratio;
   - local migrant composition;
   - education/wage distribution;
   - marriage formation versus fertility conditional on marriage.

4. **Family network / grandparental childcare**
   - distance from hukou/home;
   - spouse origin;
   - co-residence or family proximity if observed.

5. **Economic constraints**
   - housing;
   - female labor market;
   - wages/job stability;
   - childcare/education costs.

Mechanism claims should be ranked by the strength of identification, not by how interesting the narrative sounds.

---

# 6. Concrete execution order

Work should not run everything blindly. First classify feasibility.

## Stage A — Reconcile data

Read:

- `fertility/SPEC.md`
- `fertility/WORK.md`
- `fertility/DATA_ALIGNMENT_CHECKLIST.md`

Produce `fertility/DATA_RECONCILIATION.md`.

## Stage B — Benchmark gap audit

For every item in Sections 4–5 of this file, create a matrix:

| Test/design | Benchmark does it? | Top-paper motivation | CMDS feasible? | Required variables | Sample cost | Identification value | Result if already run |
|---|---|---|---|---|---:|---|---|

Write it to:

```
fertility/IDENTIFICATION_GAP_AUDIT.md
```

Use:

- **A = feasible now**
- **B = feasible after external merge / moderate reconstruction**
- **C = infeasible with current data**

Do not mark something A unless actual variables/code support it.

## Stage C — Minimum clean-design package

Only after Stage A/B, implement the highest-value A-feasible tests first:

1. treatment/place-measure independence;
2. meaningful pre-trends;
3. fertility/marriage-around-move diagnostics;
4. within-origin design;
5. origin-definition robustness;
6. multiple-move diagnostics;
7. stock-sample/survivorship diagnostics;
8. group-specific placebo / overidentification tests if feasible;
9. inference/clustering audit.

## Stage D — External-shock and mechanism layer

Then evaluate:

- hukou reform design;
- fertility-policy interactions;
- independent external fertility/place measures;
- other exogenous migration shocks.

---

# 7. Decision rule for the paper

Do **not** judge the project by whether it reproduces exactly the U.S. result.

The project is promising if:

1. a credible mover design survives the strongest feasible selection tests;
2. the China data reveal a margin that the U.S. benchmark cannot see;
3. the distinctive result is tied to a clearly identified institutional or behavioral mechanism.

Possible valuable outcomes include:

- strong average place effects;
- little average effect but large effects only for migrants with genuine access to local institutions;
- effects concentrated in marriage rather than fertility conditional on marriage;
- effects concentrated around policy eligibility;
- strong asymmetry caused by family networks or constraints;
- evidence that hukou-origin and true previous residence imply fundamentally different place-effect estimates.

A null or heterogeneous average effect can still be informative if the clean design reveals **why** physical relocation does or does not translate into effective exposure to place.

---

## Core references

- Wu, Hantao & Man Zhu (2026), "Geographic variation in fertility: evidence from mover design," *Labour Economics* 100, 102895. DOI: 10.1016/j.labeco.2026.102895.
- Finkelstein, Amy, Matthew Gentzkow & Heidi Williams (2016), "Sources of Geographic Variation in Health Care: Evidence from Patient Migration," *Quarterly Journal of Economics* 131(4).
- Chetty, Raj & Nathaniel Hendren (2018), "The Impacts of Neighborhoods on Intergenerational Mobility I: Childhood Exposure Effects," *Quarterly Journal of Economics* 133(3).
- Chetty, Raj & Nathaniel Hendren (2018), "The Impacts of Neighborhoods on Intergenerational Mobility II: County-Level Estimates," *Quarterly Journal of Economics* 133(3).
- Cantoni, Enrico & Vincent Pons (2022), "Does Context Outweigh Individual Characteristics in Driving Voting Behavior? Evidence from Relocations within the United States," *American Economic Review* 112(4).
- Chyn, Eric & Na'ama Shenhav (2025), "Place Effects and Geographic Inequality in Health at Birth," *American Economic Journal: Economic Policy* 17(4).
