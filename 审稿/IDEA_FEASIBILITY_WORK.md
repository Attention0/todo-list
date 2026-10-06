# ICLR 2026 matching ideas — clean-identification feasibility screen

## Purpose

This round is **not** a paper-writing round and **not** a specification-search round.

Use **ICLR 2026 only**. Do **not** bring in 2020–2025 data.

The objective is to decide which of the proposed matching / expert-evaluation ideas can be supported by a **clean, clearly interpretable empirical design** with the actual 2026 data plus legally/publicly obtainable pre-treatment information.

For every idea, the standard is:

> Could a skeptical Management Science / Organization Science reviewer understand exactly what variation identifies the coefficient, and could we rule out the main competing mechanism rather than merely control for it?

If the answer is no, say so. Do not rescue an idea with weak proxies or a long list of controls.

---

# I. Binding identification standard

For every proposed effect distinguish four levels:

1. **Measurement fact**  
   e.g. objective topic similarity predicts self-reported confidence.

2. **Conditional association**  
   e.g. within the same paper, socially closer reviewers score differently after controlling for measured expertise.

3. **Quasi-experimental / design-based evidence**  
   variation induced by an assignment rule, threshold, capacity constraint, randomization, or other plausibly exogenous source.

4. **Causal mechanism claim**  
   e.g. social familiarity itself causes favoritism, or expertise causes higher-quality reviews.

Only levels 3–4 count as “clean causal” for this screen.

A paper-FE regression is **not automatically causal**. Reviewer FE is **not automatically causal**. Rich controls are **not automatically causal**.

For every idea explicitly state:
- treatment / key X;
- outcome;
- exact identifying variation;
- what determines assignment into treatment;
- the most dangerous omitted variable;
- whether that omitted variable can be measured;
- whether it can be differenced out;
- whether a placebo / falsification test exists;
- what evidence would falsify the proposed mechanism.

---

# II. First task: can the 2026 assignment process be reconstructed well enough?

Before testing any substantive idea, audit whether the following are publicly/legally observable or can be reconstructed from the local project:

## 1. Reviewer pool
Can we obtain the full ICLR 2026 reviewer pool, not only reviewers who appear in the leaked/local reviewed-paper sample?

Need:
- stable reviewer profile IDs if publicly available;
- area / expertise fields;
- reviewer role;
- whether emergency reviewers can be distinguished.

Do not use unauthorized/private endpoints.

## 2. Candidate / eligible reviewer set for each paper
Can we reconstruct, even approximately:
- hard conflicts;
- recent coauthor conflicts;
- same-institution conflicts;
- advisor/advisee conflicts;
- author-declared conflicts;
- reviewer load/capacity;
- area restrictions?

If eligibility cannot be reconstructed, say so.

## 3. Bids / affinity / matching scores
Check whether any of the following are observable in the local data or public/authorized OpenReview artifacts:
- reviewer bids;
- affinity scores;
- TPMS / embedding scores;
- assignment optimizer objective;
- capacity constraints;
- AC manual adjustment logs;
- emergency reviewer additions.

If not observable, do not assume random assignment.

## 4. Assignment shocks / discontinuities
Search specifically for usable design-based variation:
- score/affinity threshold rules;
- reviewer capacity constraints;
- tie-breaking rules;
- load balancing;
- emergency reviewer assignment;
- late reviewer replacement;
- paper transfers across ACs;
- conflict-rule thresholds;
- reviewer availability cutoffs;
- algorithm changes within the same conference.

For each candidate shock:
- document the institutional rule;
- show the running variable;
- show the threshold or discontinuity;
- show sample size near the cutoff;
- show whether treatment probability actually jumps;
- test balance on pre-treatment covariates.

If no such source exists, explicitly report “no clean assignment instrument found”.

---

# III. Build three core pre-treatment constructs first

Only use information dated **before the review/assignment period**.

## A. Objective expertise

Preferred measure:
- reviewer publications dated before the 2025 ICLR review period;
- paper title + abstract / submission text frozen at submission;
- embedding similarity and/or topic-overlap.

Requirements:
- exclude publications after the cutoff;
- validate publication–reviewer identity;
- freeze the embedding model/specification before outcome analysis;
- report coverage;
- validate against reviewer confidence, but do not define expertise using confidence.

Construct several pre-specified variants:
1. max similarity to prior publication;
2. mean of top-k similarities;
3. similarity to reviewer publication centroid;
4. lexical/topic robustness measure.

## B. Social proximity

Construct only dated, pre-review measures:
- prior coauthorship before cutoff;
- years since last coauthorship;
- shortest coauthor-network distance using only pre-cutoff edges;
- prior same-institution overlap with actual date overlap;
- advisor/advisee relation if reliably dated.

Do not call undated snapshot overlap “familiarity”.

## C. Reviewer knowledge portfolio

Using only pre-cutoff publications:
- specialization / concentration;
- topic entropy;
- boundary-spanning breadth;
- seniority / publication age;
- reviewer status measures if constructible with pre-cutoff data.

All three constructs need coverage and validation tables.

---

# IV. Screen the eight ideas

For each idea below, do not try to make it work. Determine the strongest design actually available.

## Idea 1 — Expertise–Independence Frontier

### Question
Does greater reviewer expertise mechanically come with lower independence from the authors?

### Minimal fact
Estimate the empirical relationship between objective expertise and pre-review social proximity.

### Strong claim we would like
Reviewer assignment faces a real trade-off: gaining expertise requires sacrificing independence.

### Clean-design requirement
To claim an **organizational assignment frontier**, assigned pairs alone are insufficient. We need either:
- the eligible reviewer–paper candidate matrix; or
- a documented assignment algorithm/constraint allowing counterfactual feasible assignments.

Tasks:
1. plot expertise vs proximity among assigned pairs;
2. if candidate pool is reconstructible, compare assigned vs feasible unassigned pairs;
3. solve counterfactual assignments under:
   - maximize expertise only;
   - maximize expertise subject to network-distance constraints;
   - maximize expertise subject to institution/coauthor constraints;
4. estimate the expertise cost of extra independence.

Verdict must distinguish:
- clean descriptive pair-level trade-off;
- clean organizational assignment frontier;
- not identified.

## Idea 2 — The Best Review Team Is Not the Best Reviewers

### Question
Does reviewer-team complementarity generate more useful information than simply maximizing average individual expertise?

### Key constructs
- average expertise;
- expertise diversity / topic coverage;
- redundancy among reviewers;
- social-network diversity;
- semantic overlap of review weaknesses/questions.

### Outcomes
Prefer outcomes with a clear information interpretation:
- unique issues raised per reviewer;
- semantic redundancy among reviews;
- distinct technical dimensions covered;
- author responses addressing reviewer-specific points;
- later discussion uptake by other reviewers.

Do **not** use score variance alone as “review quality”.

### Clean-design requirement
Need exogenous or plausibly exogenous variation in team composition, or a design that isolates marginal reviewer assignment.

Search for:
- late/emergency reviewer additions;
- reviewer replacement;
- capacity-induced marginal assignments;
- quasi-random fourth reviewer additions.

If absent, classify team-composition effects as observational.

## Idea 3 — Confidence vs Competence

### Question
Do organizations recognize objective expertise, or do confident reviewers exert disproportionate influence?

Split into two separate claims.

### Claim A: confidence calibration
Objective expertise -> self-reported confidence.

This can be a clean **measurement fact** if expertise is pre-treatment and validated.

### Claim B: influence
When reviewers disagree, whose opinion moves later evaluations / final decision?

Need:
- trustworthy review-edit lineage;
- pre-discussion score;
- post-discussion score;
- timestamps;
- final AC/meta-review/decision if available.

Because ICLR 2026 had a security incident, explicitly test whether the revision window is contaminated by rollback/freeze/reassignment.

If clean pre/post discussion history cannot be reconstructed independently of the incident, Claim B is currently infeasible.

Do not infer influence from simple correlation between initial score and final mean.

## Idea 4 — Gatekeepers of the Frontier

### Question
Do specialized reviewers evaluate boundary-spanning / interdisciplinary ideas differently from boundary-spanning reviewers?

Construct:
- reviewer specialization/breadth from pre-cutoff publications;
- paper interdisciplinarity / novelty from paper content and prior literature.

Candidate regression:
score_{rp} = paper FE + reviewer FE + paper-boundary-spanning × reviewer-specialization + controls.

But explicitly audit pair-selection bias:
- are specialist reviewers selectively assigned to particular kinds of boundary-spanning papers?
- does measured official/approximate affinity predict both assignment and the interaction?

Clean-design target:
- assignment shock or narrow affinity band where reviewer type varies quasi-randomly.

Without such variation, paper+reviewer FE remains conditional association only.

## Idea 5 — Familiarity: Bias or Information?

### Question
Does social proximity change judgments because of favoritism, or because connected reviewers possess useful private/domain information?

Need two distinct outcome families:

**Judgment outcomes**
- rating;
- confidence.

**Information-production outcomes**
- unique technical issues;
- specificity;
- factual/technical corrections;
- author response;
- uptake by other reviewers;
- later score changes attributable to raised issues, if chronology is valid.

Clean-design target:
Find a source of variation in social proximity that is not simply expertise.

Search especially for:
- dated conflict-rule thresholds;
- recency cutoffs for coauthorship;
- institution-change boundaries;
- assignment constraints that exclude some close ties but allow slightly more distant ties.

A raw “coauthor vs not” regression is not sufficient.

If no exogenous proximity variation exists, classify “bias vs information” as not causally separable.

## Idea 6 — Status as a Substitute for Expertise

### Question
When reviewer expertise is low, do evaluators rely more on author/institution status?

Requires:
- pre-cutoff author status;
- pre-cutoff reviewer expertise;
- credible author-identity observability.

Potential observability measures:
- verified pre-review arXiv;
- code/public project release;
- highly distinctive self-citation / research-line clues.

But these are proxies, not actual deanonymization.

Clean-design requirement:
Need a plausibly exogenous source of identity observability, not merely authors’ endogenous decision to post on arXiv.

Search for:
- timing cutoffs;
- platform/publication rules;
- accidental visibility differences unrelated to paper quality.

If none, mark causal status-substitution claim infeasible.

## Idea 7 — Peers as Competitors

### Question
Do reviewers evaluate close scientific competitors differently from equally expert noncompetitors?

Construct a pre-treatment competition measure distinct from expertise:
- topic similarity;
- no collaboration;
- same narrow research niche;
- overlapping contemporaneous research agenda;
- possibly reviewer’s own submission(s) in nearby topic if lawfully/publicly linkable.

Need to demonstrate:
Competition != Expertise.

Clean-design requirement:
Need exogenous variation in whether an equally expert reviewer is a competitor.

Search for assignment rules/capacity shocks that swap comparable reviewers with different competitive proximity.

Without this, treat as highly endogenous and do not claim strategic evaluation.

## Idea 8 — Who Should the Organization Listen To?

### Question
When reviewers disagree, does the AC/decision process weight objective expertise, confidence, reviewer status, or social proximity?

Need:
- trustworthy pre-discussion reviews;
- reliable final/meta-review decision;
- no contamination from the 2026 incident;
- objective expertise/status/proximity.

First identify whether final decision data and chronology are usable.

Then test whether AC weighting can be recovered from disagreement cases.

Clean-design requirement:
Do not call predictive weights causal unless the assignment and discussion process provides exogenous variation. At minimum distinguish:
- descriptive implicit weighting;
- predictive optimal weighting;
- causal influence.

Given the 2026 incident, this idea may be impossible for this year; report that plainly if so.

---

# V. Required falsification and mechanism tests

For any idea rated “promising”, specify and, where feasible, run:

1. **Pre-treatment balance**  
   treatment must not strongly predict obvious pre-treatment paper/reviewer covariates within the identifying sample.

2. **Placebo outcome**  
   treatment should not predict outcomes it cannot plausibly affect.

3. **Negative-control relation**  
   e.g. future coauthorship should not be used as treatment; if it predicts similarly, timing leakage is likely.

4. **Alternative mechanism test**  
   show what pattern would distinguish expertise from familiarity, status, or generic reviewer harshness.

5. **Leave-one-definition-out robustness**  
   result should not depend on one arbitrary embedding, one network definition, or one status metric.

6. **Coverage / missingness selection**  
   show whether constructible reviewer profiles differ from missing-profile reviewers.

Do not add dozens of specifications. Use a small pre-specified set.

---

# VI. Deliverables

Write outputs to:

`审稿/results/idea_feasibility/`

Required files:

## 1. FEASIBILITY_MATRIX.md

One row per idea:

| Idea | Core claim | Best available design | Identification level | Main confound | Can confound be ruled out? | Data needed | Verdict |
|---|---|---|---|---|---|---|---|

Verdict must be one of:
- CLEAN NOW
- CLEAN WITH SPECIFIC ADDITIONAL DATA
- CONDITIONAL / ASSOCIATIONAL ONLY
- NOT CREDIBLY IDENTIFIABLE IN ICLR 2026

## 2. ASSIGNMENT_IDENTIFICATION.md

Document:
- reviewer pool;
- candidate set;
- bids/affinity;
- conflicts;
- capacities;
- assignment algorithm;
- any quasi-random variation;
- any threshold/shock;
- what is public vs unavailable.

End with one explicit sentence:

> “The strongest assignment-based source of plausibly exogenous variation is ______.”

If none:

> “No assignment-based source of plausibly exogenous variation was identified.”

## 3. CORE_CONSTRUCTS.md

Document objective expertise, dated proximity, reviewer portfolio:
- definition;
- cutoff;
- source;
- coverage;
- validation;
- leakage risks.

## 4. IDEA_1.md ... IDEA_8.md

For each idea give:
- estimand;
- identifying variation;
- DAG / confounding logic in words;
- feasible specification;
- fatal reviewer objection;
- whether objection is answerable;
- minimal decisive empirical test;
- verdict.

## 5. PRIORITY_TESTS.md

List only the **3–5 tests** that would most efficiently determine whether a top-journal-quality design exists.

Do not rank ideas by taste. Rank tests by information value:
- what result would kill an idea;
- what result would materially strengthen it.

---

# VII. Git and privacy

Do not commit:
- reviewer identity mapping;
- person-level private data;
- emails;
- credentials;
- API tokens;
- raw leaked identity files.

Commit only:
- code;
- aggregate diagnostics;
- figures;
- tables;
- documentation.

Use only public/authorized data access. Do not attempt to bypass OpenReview permissions.

---

# VIII. Completion criterion

This round is successful if Chat can answer, for each idea:

1. What exact empirical variation would identify it?
2. Is that variation actually present in ICLR 2026?
3. What is the single most dangerous competing mechanism?
4. Can the data/design rule it out?
5. If not, what **specific** additional data would be required?
6. Should the idea be pursued as causal, descriptive, or dropped?

The goal is to kill weak ideas early and preserve only designs that can survive skeptical top-journal review.
