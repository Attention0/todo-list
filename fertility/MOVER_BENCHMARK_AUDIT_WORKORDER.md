# Fertility Geography — Mover-Design Benchmark Audit Work Order

## Objective

This task is a **research-design benchmark audit**, not a mechanism exercise and not a generic data audit.

The core research question is:

> **Geography of family formation (婚育地理): how does moving across places affect marriage and fertility?**

The two co-primary outcome families are:

1. **Marriage**
2. **Fertility**

The direct benchmark is:

**Wu & Zhu (2026), “Geographic variation in fertility: evidence from mover design,” Labour Economics 100.**

The goal is to determine:

1. what a credible mover design must minimally do;
2. what the Labour Economics benchmark already does;
3. what it still leaves vulnerable to endogeneity attacks;
4. what stronger mover/place-effect papers add;
5. what our CMDS project therefore must complete before mechanisms.

Do **not** start by searching for China-specific mechanisms. First build a mover design that can survive a serious seminar/referee identification attack.

---

# 1. Literature scope

## 1.1 Local literature folder

Read the full folder:

```
G:\桌面\科研\文章-生育地理
```

Systematically identify papers related to:

- mover design;
- place effects;
- relocation designs;
- migration and behavioral adjustment;
- neighborhood/location exposure;
- marriage;
- fertility;
- health;
- voting;
- earnings;
- other outcomes that use migration to identify contextual/place effects.

Use the local folder as the first literature base.

## 1.2 Direct benchmark

Read the **full paper and appendix** for Wu & Zhu (2026), not only prior summaries.

Verify exactly what it does in:

- main specification;
- event study;
- pre-trends;
- migration-motive tests;
- matched nonmovers;
- time-varying observables;
- plausibly exogenous moves;
- IV;
- AKM decomposition/sorting;
- parity heterogeneity;
- alternative fertility measures;
- sample restrictions;
- clustering/inference;
- robustness appendix.

Do not rely only on prior Chat notes.

## 1.3 Strong mover/place-effect comparison set

At minimum compare against high-level work such as:

- Finkelstein, Gentzkow & Williams — patient migration / health-care place effects;
- Chetty & Hendren — childhood exposure effects;
- Cantoni & Pons — relocations and voting behavior;
- Chyn & Shenhav — place effects in health at birth;
- other Top 5 / general-interest / strong field-journal mover designs found in the local folder.

Also perform a targeted literature search for recent mover/place-effect papers that materially improve identification logic.

Priority:

1. Top 5;
2. AER / AEJ / REStat / EJ / comparable general-interest;
3. strong labor/public/urban/demography field journals;
4. lower-tier papers only when they contribute a genuinely useful identification device.

Do not create a long undifferentiated bibliography.

---

# 2. Deliverable 1 — Identification architecture across mover papers

Create:

```
fertility/MOVER_LITERATURE_IDENTIFICATION_MAP.md
```

Use a common table:

| Paper | Outcome | Move definition | Treatment/place measure | Main specification | Individual FE? | Event study? | Pre-trend? | Destination-choice selection test? | Reverse causality test? | Exogenous move/shock? | Placebo / overidentification? | Multiple moves? | Return/survivor selection? | Exposure duration? | Inference/clustering | Main remaining threat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

For every important design component, explain:

- **which endogeneity threat it addresses**;
- why the test has identification content;
- what alternative explanation remains if the test fails or is absent.

The purpose is not to summarize results. The purpose is to recover the **identification architecture** of strong mover papers.

---

# 3. Deliverable 2 — Referee-style audit of the Labour Economics benchmark

Create:

```
fertility/LABOUR_E_IDENTIFICATION_AUDIT.md
```

## 3.1 What Wu & Zhu already do

Verify from the actual paper and appendix:

- individual fixed effects;
- event-study specification;
- pre-move coefficients;
- migration motives;
- matched nonmovers;
- changing observables;
- disaster-induced moves;
- IV;
- AKM-style sorting/decomposition;
- mover-only specifications;
- balanced samples;
- exclusion of selected move motives;
- alternative fertility measures;
- alternative clustering;
- first versus higher-order births;
- heterogeneity;
- any other important appendix defense.

For every item, report:

- exact design;
- exact table/figure/appendix location;
- endogeneity concern addressed;
- remaining limitation.

## 3.2 What it still does not fully solve

Do **not** criticize for novelty's sake.

Classify missing or incomplete defenses as:

### Tier 1 — Necessary identification defenses
If absent, a serious referee can plausibly attack causal interpretation.

### Tier 2 — Strong top-journal validation
Not always indispensable, but materially strengthens a mover design.

### Tier 3 — Ordinary robustness
Useful but not a core identification requirement.

Pay special attention to:

### A. Fertility-induced migration / family-formation-induced migration

Can:

```
marriage plans
pregnancy
birth
family reunification
```

cause the move itself?

Distinguish:

```
move -> fertility
```

from:

```
fertility/family-formation plans -> move
```

Audit whether the benchmark truly rules this out.

### B. Destination choice

Why does one mover choose a high-fertility destination and another a low-fertility destination?

Assess:

- whether individual FE solve time-varying shocks;
- whether within-origin comparisons are needed;
- whether origin × cohort / origin × move-year comparisons are used or should be used;
- whether destination-choice balance is sufficiently tested.

### C. Pre-move outcome dynamics

Check whether simply showing insignificant leads is enough.

Evaluate stronger standards:

- joint pre-trend test;
- pre-trend slope;
- economic magnitude of pre-trend relative to post effect;
- longer pre-period;
- effect-scaled confidence intervals.

### D. Group-specific predicted place effects / overidentification

Use Chetty–Hendren-style logic:

A mover should respond more strongly to the destination environment relevant to **her own group** than to unrelated group environments.

Examples relevant to fertility/family formation:

- childless women should respond more to first-birth environment than third-birth environment;
- parity-1 women should respond more to second-birth environment;
- women aged 25–29 should respond more to fertility patterns for similar ages;
- unmarried individuals should respond to marriage-market/marriage-rate environments relevant to their group.

Assess whether the benchmark uses anything comparable.

### E. Exposure duration

Does the response scale coherently with:

- years since move;
- age at move;
- actual exposure duration?

Distinguish:

- immediate discontinuity;
- gradual assimilation;
- timing/spacing mechanics.

### F. Multiple moves / origin mismeasurement

Does the benchmark observe actual pre-move residence?

Could intermediate moves contaminate:

- origin;
- move date;
- event time;
- treatment difference?

### G. Return migration / onward migration / survivor selection

This is especially important for comparing panel-based studies with CMDS.

Ask:

- does the benchmark follow people after they leave?
- is sample inclusion conditioned on remaining at the destination?
- could fertility itself affect return migration or onward migration?

### H. Place-measure endogeneity / measurement error

Audit:

- whether focal observations contribute to place measures;
- leave-one-out;
- split-sample measures;
- independent external measures;
- small-cell reliability;
- shrinkage;
- place-rank stability.

### I. AKM / limited-mobility bias

If place effects or variance decompositions are estimated:

- connected set;
- leave-out connectedness;
- weak mobility links;
- finite-sample noise;
- bias-corrected variance components.

### J. Clustering / inference

Determine the proper treatment-variation level:

- individual;
- origin;
- destination;
- two-way origin × destination;
- few-cluster adjustments.

At the end, clearly separate:

> things Labour Economics does not do but probably does not need

from

> things Labour Economics does not do that remain genuine causal-identification vulnerabilities.

---

# 4. Deliverable 3 — Rebuild the outcome architecture around 婚 + 育

Create a dedicated section in:

```
fertility/MOVER_CORE_CHECKLIST.md
```

The paper's core outcome is not fertility alone.

The research object is:

> **Geography of family formation**

Marriage and fertility are co-primary outcomes.

---

## 4.1 Marriage outcomes

Primary marriage outcome:

### First-marriage hazard

Construct the risk set correctly:

```
at risk in year t
= not yet first-married before t
```

Potential outcomes:

- first marriage in year t;
- probability of entering first marriage after migration;
- timing from migration to first marriage;
- cumulative first-marriage probability by years since move.

If data permit, secondary outcomes may include:

- cohabitation;
- remarriage;
- divorce.

Do not force these if histories are incomplete.

Do not use the current fertility-selected master as the marriage risk population.

---

## 4.2 Fertility outcomes

At minimum distinguish:

### A. Any annual birth

```
birth_it
```

among women in the relevant reproductive-age exposure window.

### B. First-birth hazard

Risk set:

```
parity_{i,t-1}=0
```

### C. Second-birth hazard

Risk set:

```
parity_{i,t-1}=1
```

### D. Higher-order fertility

Only if data quality, policy regime and sample size support it.

### E. Family-formation sequencing

Explicitly distinguish:

```
Place -> Marriage -> First birth
```

from:

```
Place -> Fertility among people already married before migration
```

The latter is a separate estimand.

Do **not** control for post-move marriage as an ordinary covariate in a total-effect fertility regression.

---

# 5. Deliverable 4 — Final required mover checklist

Create:

```
fertility/MOVER_CORE_CHECKLIST.md
```

Do not create an unprioritized list of 50 robustness checks.

Organize into:

## Tier 0 — Measurement prerequisites

Examples:

- move timing;
- origin definition;
- destination definition;
- marriage risk set;
- fertility dynamic risk sets;
- treatment/place-measure independence;
- correct event-time construction.

If Tier 0 fails, causal interpretation is not allowed.

## Tier 1 — Core causal identification

Only include tests whose absence leaves a serious endogeneity attack.

Candidate families include:

- marriage/fertility behavior before move;
- fertility/family-formation-induced migration;
- destination-choice selection;
- within-origin comparisons;
- pre-trend diagnostics;
- migration-motive sensitivity;
- multiple-move sensitivity;
- return/survivor-selection diagnostics;
- correct clustering/inference.

The literature audit, not this work order, decides the final Tier 1 list.

## Tier 2 — Strong mover-design validation

Potential examples:

- group-specific destination effects;
- exposure-duration tests;
- placebo environments;
- leave-out prediction;
- matched nonmovers;
- plausibly exogenous move shocks;
- stronger overidentification tests.

## Tier 3 — Robustness

Examples:

- alternative event windows;
- recent movers;
- work movers;
- cross-province movers;
- within-province movers;
- balanced panels/windows;
- alternative clustering;
- alternative treatment definitions.

These should remain secondary unless literature evidence shows they solve a core identification problem.

---

# 6. Required task matrix

In `MOVER_CORE_CHECKLIST.md`, every proposed analysis must appear in:

| Priority | Analysis | Marriage / Fertility / Both | Endogeneity threat addressed | Why needed | Labour E already does? | Top mover precedent | CMDS feasible now? | Required variables | Sample cost | Interpretation if passes | Interpretation if fails |
|---|---|---|---|---|---|---|---|---|---:|---|---|

The most important field is:

**Endogeneity threat addressed**

Do not write vague explanations such as "for robustness."

---

# 7. CMDS mapping

Use the existing verified files:

- `fertility/DATA_RECONCILIATION.md`
- `fertility/IDENTIFICATION_GAP_AUDIT.md`

Map every benchmark requirement to current CMDS feasibility.

For each item classify:

- **A — feasible now**
- **B — feasible after moderate reconstruction / external merge**
- **C — infeasible with current data**

Do not upgrade B/C to A by changing the estimand or silently making assumptions.

In particular preserve these established data boundaries:

- true previous residence is not observed for the full sample;
- current master is selected by fertility-history availability;
- marriage and first-birth risk populations must be rebuilt;
- province CBR is an external baseline treatment, not final fine-geography place exposure;
- CMDS is a destination-stock sample and may suffer stay/return/onward selection;
- current covariates are not automatically pre-move covariates.

---

# 8. No mechanisms yet

Do **not** estimate mechanisms in this task.

Do not begin with:

- hukou access;
- housing;
- childcare;
- marriage markets;
- family networks;
- fertility-policy mechanisms.

Only discuss such variables if they are needed for identification.

The sole objective is:

> **Build a clean mover design for marriage and fertility that can be defended before moving to mechanisms.**

---

# 9. Final concise synthesis

Update `RESULT.md` with a concise answer to exactly these questions:

1. What are the minimum 5–10 elements of a credible mover design?
2. Which of them does Wu & Zhu already do?
3. What are the 3–5 most important identification gaps left by Labour Economics?
4. What are the 3–5 additional CMDS-specific threats?
5. How should marriage and fertility risk sets/event studies be constructed separately?
6. What are the first 5–10 analyses the project should actually run next?

Do not run mechanism regressions in this delivery.

The purpose of this task is to produce the **research-design roadmap** that will govern the next empirical stage.
