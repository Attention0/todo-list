# JEBO v4 Writing Work Plan

## Mission

Write a new JEBO manuscript that uses PR #19 as the scientific source of truth but restores a strong economic narrative around the three empirical puzzles and their distributional anatomy.

Read first:

- `消费调查/JEBO_V4_WRITING_SPEC.md`
- PR #19 result package on `feature/jebo-review-revision`
- `消费调查/results/jebo_review_revision/RESULT.md`
- `消费调查/results/jebo_review_revision/FINAL_AUDIT.md`
- `消费调查/manuscript/jebo_v3/JEBO_manuscript_v3.md`
- `消费调查/manuscript/jebo_v3/JEBO_supplement_v3.md`
- `消费调查/manuscript/jebo_v3/RESPONSE_TO_JEBO_REVIEW.md`

Scientific base:
- PR19 head: `363313c8adc52cce252c11390a32e46c7a98d25f`

Do not revert any PR19 statistical or logical repair.

---

## 1. Branching

Create a new branch from the exact PR19 head:

`feature/jebo-v4-narrative-rewrite`

Base the eventual stacked PR on:

`feature/jebo-review-revision`

Do not modify PR19 historical scientific outputs.

---

## 2. Writing-only rule

This task is primarily a manuscript rewrite, not a new empirical search.

Allowed:
- reuse PR19 outputs;
- recompute simple displayed arithmetic from PR19 aggregate cell tables;
- redesign figures from existing PR19 aggregate source data;
- create a descriptive 200→5000 six-bin change figure using existing adult cell distributions;
- verify literature and bibliographic metadata;
- reorganize supplement and tables.

Not allowed:
- new thresholds;
- new subgroup definitions;
- new moderators;
- new interaction families;
- new specification searches;
- new mechanism variables;
- new inferential tests designed after seeing the data.

If a desired claim would require a new test not already in PR19:
- either phrase it descriptively;
- or move it to future work;
- do not create a new test without a new explicit authorization.

---

## 3. Drafting order

### Step 1 — Story memo

Before rewriting the manuscript, create:

`消费调查/manuscript/jebo_v4/V4_STORY_MEMO.md`

It must state in one page:

- the three puzzles;
- the percentage-vs-yuan distinction;
- the Cash/Food/Medical distributional paths;
- the explanation sequence;
- the unified behavioral interpretation;
- the inferential boundaries inherited from PR19.

Do not begin the full manuscript until this memo is internally coherent.

### Step 2 — Main figure storyboard

Create:

`V4_FIGURE_STORYBOARD.md`

Specify:
- what each main figure teaches;
- where it enters the narrative;
- which PR19 source CSV supplies it;
- whether it is raw/descriptive or inferential.

### Step 3 — Rewrite the manuscript

Create:

`消费调查/manuscript/jebo_v4/JEBO_manuscript_v4.md`

Then generate:

`JEBO_manuscript_v4.docx`

Use the outline and tone rules in the specification.

### Step 4 — Rewrite supplement around main-paper needs

Create:
- `JEBO_supplement_v4.md`
- `JEBO_supplement_v4.docx`

Do not simply copy v3 supplement order. Reorder it to support the new paper flow.

### Step 5 — Highlights and cover-facing summary

Create:
- `JEBO_Highlights_v4.docx`
- `V4_EDITOR_SUMMARY.md`

Highlights should foreground:
- three-puzzle pattern;
- mean convergence;
- distributional anatomy;
- share vs yuan distinction;
- bounded mechanism interpretation.

---

## 4. Required narrative in Introduction

The Introduction must not start with a measurement caveat.

It should start with the substantive question:

> Does the form of a transfer matter equally when transfers are small and large?

Within the first three paragraphs it must establish:

- Cash declines with size;
- Food declines less;
- Medical is almost flat;
- form differences are largest at RMB 200 and much smaller at RMB 5,000.

Within the next two paragraphs:
- distinguish percentage share from implied yuan;
- preview the distributional anatomy.

Then:
- preview the progressive explanation strategy;
- state the unified candidate interpretation;
- position contributions in literature.

Do not bury the three puzzles behind p-values.

---

## 5. Required Results structure

Use the specification's order:

### Section 4 — Three puzzles in randomized cells
- raw 3×3 means;
- share vs yuan;
- 42-family trend inference.

### Section 5 — Anatomy of the puzzles
- Cash distribution;
- Food distribution;
- Medical distribution;
- convergence without distributional identity.

### Section 6 — What can explain the puzzles?
- standard benchmark;
- scale;
- bottom category;
- simple bindingness;
- category need;
- income/liquidity;
- observable types.

### Section 7 — Unified interpretation
- resource categorization/perceived spendability as a candidate account;
- explicit unmeasured-mediator boundary;
- future testable predictions.

---

## 6. Distributional writing requirements

Use the adult raw PR19 cell distribution values directly.

The manuscript must explicitly state:

### Cash 200→5000
- bottom 27.35→27.41
- Top75 13.43→5.34
- 10–25 rises 20.39→24.48

### Food 200→5000
- bottom 31.16→30.05
- Top75 9.79→7.51
- 10–25 rises 19.90→23.87
- 25–50 falls 15.50→11.52

### Medical 200→5000
- bottom 38.60→35.49
- 10–25 rises 18.57→23.50
- 50–75 rises 5.54→7.26
- Top75 falls 6.03→3.94
- midpoint mean remains ~17.7→17.8

Core Medical sentence:

> Medical's flat mean is not a static distribution; it is the net result of offsetting movements across response categories.

Use this only as a descriptive cell fact unless an existing PR19 test supports more.

At RMB 5,000 explicitly note:
- 10–25 bin is 24.48 / 23.87 / 23.50 across Cash/Food/Medical;
- bottom and top categories remain different.

Core convergence sentence:

> The mean shares converge strongly, but the distributions do not become identical.

Again: descriptive, not a formal equality/inequality test.

---

## 7. New descriptive figure

Create a new main-text figure from existing PR19 adult aggregate data only:

**Figure: Change in response-category shares from RMB 200 to RMB 5,000**

Three panels:
- Cash;
- Food;
- Medical.

Within each panel show six category-share changes.

No new hypothesis tests.
No significance stars.
Use the same category ordering and neutral visual style as the atlas.

The figure should make these patterns immediately visible:
- Cash: large Top75 contraction;
- Food: more diffuse reallocation;
- Medical: offsetting movements.

Keep all figure source CSVs.

---

## 8. Mechanism section rules

Restore intellectual progression without returning to false exclusion logic.

Each mechanism subsection must contain:
- prediction/intuition;
- relevant distributional clue;
- PR19 formal diagnostic;
- interim conclusion.

Use strong wording where justified:
- "contradicts the sharp prediction" for the Food sign;
- "does not provide a sufficient organizing account" for category need;
- "does not parsimoniously organize the three puzzles" for relative resources.

Use uncertainty honestly:
- moderator nulls are precision-limited;
- no generic mechanism is ruled out by nonrejection.

Do not recreate the old mechanism funnel graphic.

---

## 9. Literature work

Perform a focused refresh, not a generic new search.

For every core literature cluster, verify primary sources and update statuses as of the revision date.

Must directly discuss:
- Friedman;
- Jappelli & Pistaferri;
- Kaplan & Violante;
- Fagereng et al.;
- Shapiro & Slemrod;
- Fuster et al. 2021;
- Andreolli & Surico 2026;
- Jappelli et al. current status if retained;
- Thaler;
- Shefrin & Thaler;
- Heath & Soll;
- Kooreman;
- Abeler & Marklein;
- Hastings & Shapiro;
- Cunha;
- Kan et al.;
- Bernard 2023;
- Boehm et al. 2025;
- Bonomo et al. current status;
- Lee et al. JEBO 2024;
- Pauls & Laudi JEBO 2025;
- Parker & Souleles 2019;
- Crossley et al. current status;
- Ueda 2025 if retained.

Create:
- `JEBO_V4_REFERENCE_AUDIT.csv`
- `V4_LITERATURE_DIALOGUE.md`

The literature dialogue file should state, for each closest paper:
- question;
- design;
- outcome;
- relevance to one of our three puzzles;
- what our paper adds;
- what we must not claim.

---

## 10. Main-text claim discipline

Use the PR19 claim ledger as a floor, then create:

`JEBO_V4_CLAIM_LEDGER.csv`

Every substantive main-text claim should be tagged as:
- randomized cell fact;
- coded/descriptive transformation;
- inferential result;
- mechanism diagnostic;
- interpretation;
- literature claim;
- limitation.

Flag any sentence that:
- treats spendability as measured;
- treats equal point estimates as equivalence;
- calls above-bottom a participation margin;
- treats null moderation as exclusion;
- describes interaction as established;
- calls interval slope structural MPC;
- claims full-distribution convergence/equality without a test.

---

## 11. Word formatting

Use submission-style formatting requested by the authors:

- Times New Roman throughout;
- 12 pt body;
- title 16–18 pt bold;
- section headings 14 pt bold;
- subsection headings 12 pt bold;
- table/figure notes 9–10 pt;
- justified body text;
- first-line indent approx. 0.74 cm;
- page numbers;
- consistent line/paragraph spacing;
- tables centered and readable;
- figures high resolution and embedded near discussion;
- clean captions and notes;
- no tracked changes/comments;
- no orphan headings or figure split problems.

Render the final DOCX page by page and inspect it visually.

---

## 12. Author metadata

Carry forward PR19's unresolved author-information checklist.

Do not invent:
- recruitment vendor/frame;
- field dates;
- incentive;
- completion rate;
- randomization implementation;
- ethics approval/exemption;
- consent;
- funding;
- COI;
- data-sharing permission;
- CRediT roles.

Mark placeholders clearly in a draft-only author note and maintain:

`AUTHOR_INFORMATION_REQUIRED.md`

The scientific manuscript should not read like an internal checklist; use neutral placeholders where unavoidable.

---

## 13. Final audit

Create:

`消费调查/manuscript/jebo_v4/V4_FINAL_AUDIT.md`

Check:

- every number against PR19 source files;
- all three puzzles visible in Abstract/Introduction;
- Medical flat-mean distribution logic correct;
- Food bindingness sign correct;
- percentage vs yuan distinction correct;
- 42-family numbers unchanged;
- no false extensive-margin language;
- no overclaim from moderator nulls;
- no spendability-as-measured claim;
- no structural interpretation of interval model;
- literature status verified;
- all figures from adult aggregate source data;
- no new inference was introduced.

---

## 14. Pull request

Open a new stacked draft PR:

- head: `feature/jebo-v4-narrative-rewrite`
- base: `feature/jebo-review-revision`

Suggested title:

**JEBO v4: restore the three-puzzle narrative on top of PR19 evidence**

Do not merge automatically.

The PR description should summarize:
1. what changed in narrative;
2. what PR19 scientific boundaries were preserved;
3. which figures/tables were reorganized;
4. whether any author metadata remain unresolved.
