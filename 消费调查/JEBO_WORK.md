# JEBO transition work plan — MPC size dependence × transfer form

## 0. Mission

Execute a target-specific transition of the consumption-survey paper from the current NC v5 package to a **Journal of Economic Behavior & Organization (JEBO)** paper.

This is **not** a request to restart open-ended empirical discovery.

The work has five substantive goals:

1. freeze and simplify the current evidence from PR #9–#16;
2. build a serious JEBO-oriented literature and outlet map;
3. run only a very small set of newly authorized, literature-motivated analyses;
4. decide the cleanest defensible JEBO behavioral story;
5. write and package a new JEBO manuscript from scratch.

The current preferred story is:

> **Transfer form and transfer size are jointly behaviorally relevant: stated MPC declines clearly with transfer size for Cash, less for Food, and little for Medical in the observed cells. The Cash decline is associated with compression of high-spending responses rather than an increase in zero-spending responses.**

The story is a candidate to be sharpened, not a conclusion to be forced.

Read `消费调查/JEBO_SPEC.md` in full before doing any work.

---

# PART I. BRANCH, DEPENDENCIES, AND EVIDENCE FREEZE

## 1. Base branch

Create a new branch:

`feature/jebo-repositioning`

from the latest head of:

`feature/nc-evidence-revision` / PR #16.

This is important because PR #16 already stacks on the relevant PR #9–#15 lineage.

Do not merge historical PRs automatically.

Do not edit or delete old result packages.

## 2. Required source review before any new analysis

Read at minimum:

### PR #16
- `消费调查/manuscript/nc_v5/manuscript.md`
- `消费调查/manuscript/nc_v5/NC_MPC_manuscript_v5.docx`
- `消费调查/manuscript/nc_v5/RESPONSE_MEMO.md`
- `消费调查/results/nc_evidence_revision/RESULT.md`
- `scientific_family21.csv`
- `within_form_slopes.csv`
- `form_contrasts.csv`
- `main_effects.csv`
- `mechanism_tests.csv`
- `distribution.csv`
- relevant prediction / relative-scale / calibration outputs only as needed for interpretation

### PR #15
- `NC_REVISION_RESULT.md`
- `revised_intro_outline.md`
- `NC_revision_literature_map.md`
- `mechanism_prediction_table.md`
- `relative_scale_falsification_memo.md`
- `questionnaire_mechanism_audit.md`

### PR #14
- `HERO_FIGURE_RESULT.md`
- Hero figure source, caption and audit

### PR #13
- main-figure captions and source tables

### PR #12 / #11
- all-X and who-drives result notes

### PR #10 / #9
- `MPC_FINAL_STRENGTHENING_RESULTS.md`
- `MPC_SIZE_CURVE_RESULTS.md`
- threshold / restricted-vs-cash / specification / yuan-scaling outputs

Do not rely only on PR summaries. Trace all manuscript headline numbers to aggregate source tables.

## 3. Create an evidence-freeze memo

Before new analysis create:

`消费调查/results/jebo_transition/JEBO_EVIDENCE_FREEZE.md`

It must contain:

### A. Design facts
- sample sizes;
- nine randomized cells;
- exact transfer-form descriptions;
- response-category wording;
- adult-primary definition;
- hypothetical/stated nature.

### B. Strong findings
Separate:
- form main effects;
- amount main effects;
- Cash within-form size gradient;
- raw distribution facts.

### C. Suggestive findings
- form×size omnibus;
- Cash–Food and Cash–Medical differential slopes;
- Top75 interaction evidence;
- pooled Restricted summaries.

### D. Findings explicitly not established
- tail specificity;
- Food–Medical equivalence;
- Medical invariance;
- mental-accounting mechanism;
- bindingness exclusion;
- national representativeness;
- realized MPC.

### E. Source map
For every number likely to enter the JEBO manuscript, record:
- source file;
- row / estimand;
- sample;
- outcome;
- whether raw, pointwise, Holm-adjusted, min-P-adjusted, or descriptive.

No manuscript writing before this memo exists.

---

# PART II. JEBO LITERATURE MAP

## 4. Build a serious literature map

Create:

`消费调查/results/jebo_transition/JEBO_LITERATURE_MAP.md`

and:

`消费调查/results/jebo_transition/jebo_literature_matrix.csv`

Target roughly **35–60 serious papers**, prioritizing peer-reviewed economics / behavioral-economics work.

Do not pad the count with weakly related citations.

For each paper record:

- authors;
- year;
- title;
- journal / working-paper status;
- research question;
- country / population;
- actual vs stated behavior;
- experimental / quasi-experimental / observational design;
- transfer size variation?;
- transfer form / restriction variation?;
- outcome;
- key result;
- extensive vs intensive margin if relevant;
- mechanism proposed;
- whether mechanism is directly identified;
- exact relevance to our paper;
- whether it threatens or strengthens our novelty;
- DOI / stable link;
- publication status as of the current date.

## 5. Literature cluster A — MPC and shock size

At minimum investigate:

- Friedman / permanent-income discussions of small vs large windfalls;
- Jappelli & Pistaferri review / stated-MPC work;
- Fuster, Kaplan & Zafar, ReStud 2021, “What Would You Do with $500?”;
- Kaplan & Violante 2022 MPC review;
- recent MPC meta-analysis evidence on payment-size effects;
- realized stimulus evidence where transfer size varies;
- Korean universal-payment evidence with MPC by transfer size;
- Jappelli, Savoia & Sciacchetano, EER 2026, “Intertemporal MPC and shock size”;
- 2026 JFE paper on windfall shocks and finite planning horizons.

Key question:

> What does the existing literature say about whether larger windfalls change the **probability of spending anything** versus the **share spent conditional on responding**?

This is crucial because our Cash data appear to show a relatively flat no-spending margin and compression of high-MPC responses.

## 6. Literature cluster B — mental accounting / fungibility / small windfalls

At minimum investigate:

- Thaler / Shefrin foundations;
- Thaler 1985 / 1999;
- mental accounting and small windfalls;
- category budgeting;
- source-of-funds effects;
- Hastings & Shapiro;
- Abeler & Marklein;
- related household-finance mental-accounting evidence.

Key question:

> Does the literature predict that **small cash windfalls** are especially likely to be treated as immediately spendable, and does this provide a coherent interpretation of our Cash curve?

Do not convert conceptual consistency into mechanism identification.

## 7. Literature cluster C — transfer form / restrictions / earmarking / expiry

At minimum investigate:

- cash vs in-kind / restricted transfers;
- food assistance and fungibility;
- labels / earmarks;
- expiry and commitment;
- Boehm, Fize & Jaravel, AER 2025, “Five Facts about MPCs”;
- any papers that explicitly compare MPC across cash-like and restricted / expiring resources.

Key novelty question:

> Has anyone already randomized **both transfer form and transfer size** and shown that the **MPC-size slope itself** differs by form?

This question must be answered carefully and explicitly.

## 8. Literature cluster D — JEBO-near behavioral framing papers

At minimum investigate:

- Lee, Morduch, Ravindran & Shonchoy, JEBO 2024, “The social meaning of mobile money”;
- JEBO 2025, “Temporal framing of tax stimuli and household consumption”;
- JEBO work on mental accounting / small windfalls;
- payment-method and fungibility papers.

For each, note:
- strength of identification;
- whether outcomes are hypothetical;
- how authors frame mechanisms;
- how strong their journal-level contribution is.

The purpose is to understand what JEBO treats as a publishable behavioral fact.

## 9. Literature cluster E — stated MPC validity

Investigate:
- survey elicitation of MPC;
- hypothetical vs realized / revealed MPC;
- response bins / bunching;
- predictive or external validity;
- stated-versus-realized comparisons;
- limitations of hypothetical windfall questions.

Distinguish:
- peer-reviewed evidence;
- recent working papers;
- suggestive unpublished evidence.

## 10. Produce a novelty matrix

Create a table with columns:

| Literature | Size randomized? | Form randomized? | Realized spending? | Stated MPC? | Distribution analyzed? | Extensive/intensive decomposition? | Size×form interaction? | Closest difference from us |

The final literature-map conclusion must answer:

1. What is already known about MPC and size?
2. What is already known about nonfungibility / transfer form?
3. What is known about distributional margins?
4. What exact empirical combination is new here?
5. Is “form changes the size dependence of MPC” genuinely novel enough for JEBO?

If the answer is no, stop and report the closest prior paper rather than forcing the framing.

---

# PART III. JEBO OUTLET BENCHMARK

## 11. Inspect recent JEBO papers

Create:

`消费调查/results/jebo_transition/JEBO_OUTLET_BENCHMARK.md`

Sample roughly 12–20 recent JEBO papers (preferably 2023–2026) in:
- survey experiments;
- household behavior;
- framing;
- payment;
- mental accounting;
- consumer decisions;
- behavioral finance / household finance.

Record:
- page / word length where observable;
- abstract length;
- intro structure;
- number of main figures;
- number of main tables;
- whether a theory section is used;
- whether the main contribution is a behavioral reduced-form fact or a mechanism;
- how authors discuss hypothetical outcomes;
- how much robustness stays in main text;
- typical conclusion length.

Use this to recommend a JEBO manuscript architecture.

Do not blindly imitate the Nature-family layout.

---

# PART IV. PRE-RESULT FINITE ANALYSIS MANIFEST

## 12. Freeze the only new analyses before running them

Before accessing respondent-level data for new calculations, create and commit:

`消费调查/results/jebo_transition/JEBO_ANALYSIS_MANIFEST.md`

This is a **post hoc target-transition plan**, not preregistration.

The manifest must define the exact analysis list below.

No additional new empirical analysis is authorized unless a later user instruction changes the plan.

---

# PART V. NEW ANALYSIS 1 — EXTENSIVE VS INTENSIVE SIZE EFFECT

## 13. Motivation

The most promising new JEBO-specific analysis is to connect our Cash size pattern to the classic windfall-size literature.

Existing work often separates:
- whether a household changes spending at all;
- how strongly spending changes among responders.

Our existing raw Cash cells suggest:
- no-spending share roughly stable;
- mean stated MPC declining;
- high-MPC tail declining sharply.

This deserves one transparent decomposition.

## 14. Required calculations

For each form (f) and amount (a), calculate:

1. (p_{fa} = P(any additional spending))
2. (m^+_{fa} = E[midpoint MPC | any additional spending])
3. (m_{fa} = E[midpoint MPC])

Verify the identity:

(m_{fa} = p_{fa} m^+_{fa})

up to rounding.

For the 200 → 5,000 change within each form, decompose:

(Delta m = m_{5000} - m_{200})

using a symmetric Shapley-style product decomposition:

- extensive contribution:
  (Delta p 	imes (m^+_{200}+m^+_{5000})/2)

- intensive contribution:
  (Delta m^+ 	imes (p_{200}+p_{5000})/2)

These two should sum exactly to the total difference up to numerical precision.

## 15. Interpretation rules

This decomposition is **descriptive accounting**.

Because (m^+) conditions on a post-treatment response:
- do not call it a causal intensive-margin treatment effect;
- do not compare conditional groups as if composition were fixed;
- do not make welfare claims.

The decomposition is useful for asking:

> Is Cash’s falling unconditional midpoint MPC arithmetically associated primarily with fewer people spending anything, or with lower reported spending shares among positive responders?

Repeat for all three forms.

## 16. Uncertainty

Preferred:
- show cell-level bootstrap CIs for (p), (m^+), and the two decomposition contributions if stable and easy to implement;
- stratify bootstrap by randomized cell;
- use a fixed seed;
- 2,000–5,000 draws is sufficient.

Do not create a new multiplicity family or hunt for component significance.

If bootstrap behavior is unstable, report the decomposition descriptively without overinterpreting CIs.

## 17. Outputs

Create:
- `extensive_intensive_cells.csv`
- `extensive_intensive_decomposition.csv`
- `EXTENSIVE_INTENSIVE_NOTE.md`
- optional `fig_extensive_intensive.pdf/png/svg`

The figure should be created only if it adds information beyond existing Figure 3.

---

# PART VI. NEW ANALYSIS 2 — LITERATURE-MATCHED SIZE BENCHMARK

## 18. Purpose

Create a compact table comparing our Cash pattern to published windfall-size patterns.

This is **not** a meta-analysis and does not claim parameter comparability across settings.

At minimum include for our Cash cells:
- amount;
- P(any additional spending);
- midpoint mean;
- Top75;
- descriptive conditional midpoint among positive responders.

Then extract comparable qualitative facts from:
- Fuster–Kaplan–Zafar;
- at least one realized-transfer size paper;
- recent shock-size paper(s).

## 19. Required output

Create:
- `MPC_SIZE_LITERATURE_BENCHMARK.md`
- `mpc_size_literature_benchmark.csv`

The note should answer:

- Is our extensive-margin pattern similar or different?
- Is our conditional / upper-tail compression similar or different?
- Does our transfer-form randomization add a dimension missing from the comparison papers?

No formal cross-study test.

---

# PART VII. CONCEPTUAL SYNTHESIS — NO STRUCTURAL RESCUE

## 20. Build a behavioral prediction table

Create:

`消费调查/results/jebo_transition/BEHAVIORAL_PREDICTIONS.md`

Compare the following candidate accounts:

1. standard concave consumption / PIH-style size effect;
2. liquidity / hand-to-mouth;
3. small-windfall mental accounting;
4. salience / attention / finite planning horizon;
5. mechanical restriction / bindingness;
6. earmarking / commitment / category budget.

For each account record qualitative predictions for:

- Cash level;
- Cash size gradient;
- restricted level;
- whether Cash–restricted gap should widen / shrink / be ambiguous with size;
- extensive margin;
- intensive / high-tail margin;
- which existing diagnostics speak to it;
- what is not measured.

Important:
- do not force every model to have a sharp prediction if it does not;
- label ambiguous predictions as ambiguous;
- distinguish “consistent with” from “identified by.”

Do not estimate a structural model in this task.

---

# PART VIII. STORY DECISION GATE

## 21. Create a JEBO story decision memo before manuscript writing

Create:

`消费调查/results/jebo_transition/JEBO_STORY_DECISION.md`

It must consider at least three candidate stories:

### Story A — strong form-dependent size curve
“Transfer form reshapes the MPC-size curve.”

Use only if the final evidence description can be made without hiding multiplicity uncertainty.

### Story B — preferred bounded story
“Cash shows a clear declining size gradient; restricted resources start at lower spending propensities and show weaker observed size gradients, creating a convergence puzzle.”

This is likely the safest main framing.

### Story C — distributional Cash size paper with form as comparison
“Cash MPC declines with size through compression of high-spending responses, while restricted forms provide a useful contrast.”

Use if the literature map or inference audit makes Story A/B too strong.

For each story score qualitatively:
- novelty;
- identification;
- statistical support;
- behavioral interpretability;
- JEBO fit;
- vulnerability to hypothetical-outcome criticism;
- vulnerability to multiple-testing criticism;
- dependence on unproven mechanisms.

Do not create numerical journal-acceptance probabilities.

The memo should choose the best defensible story and explain why.

---

# PART IX. MANUSCRIPT REWRITE

## 22. Create a new manuscript directory

Create:

`消费调查/manuscript/jebo_v1/`

Do not overwrite NC v5.

Required:
- `JEBO_manuscript_v1.md`
- `JEBO_manuscript_v1.docx`
- `JEBO_supplement_v1.md`
- `JEBO_supplement_v1.docx`
- `JEBO_CLAIM_LEDGER.csv`
- `JEBO_REFERENCE_AUDIT.csv`
- `SOURCE_MANIFEST.md`
- `AUTHOR_INFORMATION_REQUIRED.md`
- figures directory

## 23. Manuscript structure

Recommended structure:

1. Introduction
2. Related literature and behavioral motivation
3. Experimental design, sample and measurement
4. Transfer size and stated MPC
5. Does the size gradient depend on transfer form?
6. Distributional anatomy of the Cash size effect
7. Interpretation and alternative explanations
8. Discussion
9. Conclusion
10. References
11. Main tables / figures as appropriate

If the JEBO outlet benchmark suggests a cleaner combined structure, Work may adapt, but explain the change.

## 24. Writing style

Use economics-journal prose:
- direct;
- concrete;
- behavioral;
- not defensive;
- not Nature-style grand generalization;
- not a reviewer-response document.

The introduction should **lead with the economic question**, not with data limitations.

The paper should be confident about strong facts and explicit about uncertain ones.

Avoid repeated phrases like:
- “cannot establish” in every paragraph;
- “we do not claim” excessively;
- “frozen analysis” in the main narrative;
- implementation-heavy discussion.

Limitations should be clear but concentrated.

## 25. Abstract

Target approximately 150–220 words.

It should state:
- the size-dependence question;
- the 3×3 randomized design;
- sample size;
- core Cash / Food / Medical pattern;
- distributional margin;
- bounded inference sentence;
- contribution.

Do not mention:
- all-X;
- SHAP;
- HTE;
- calibration;
- 1,500 historical tests.

## 26. Introduction

Aim for a crisp JEBO opening.

Preferred logic:

### Paragraph 1
MPC is known to depend on windfall size. Why?

### Paragraph 2
A separate literature shows resources are not behaviorally fungible. Missing question: is the size effect invariant to transfer form?

### Paragraph 3
Explain the 3×3 design.

### Paragraph 4
State raw results.

### Paragraph 5
Distributional anatomy.

### Paragraph 6
Contribution to the two literatures and evidence boundary.

Then literature discussion.

Do not open with “context vs individual differences.”

## 27. Results hierarchy

### Main Result 1
Cash stated MPC declines with amount.

### Main Result 2
Food declines less; Medical is much flatter descriptively; cross-form slope differences are suggestive rather than uniformly multiplicity-robust.

### Main Result 3
Cash’s size effect is associated with high-response compression rather than a larger no-spending mass.

### Main Result 4
Bounded mechanism diagnostics do not uniquely identify why.

The reader should understand the paper without seeing any ML or all-X result.

---

# PART X. FIGURES

## 28. Reuse rather than redesign

The current figures are already strong.

Do not launch a new visual redesign project.

### Figure 1
Use PR #14 Hero response atlas unless the JEBO benchmark strongly argues otherwise.

### Figure 2
Use a clean approved form-by-size curve:
- ordinal;
- midpoint;
- Top75 if space permits.

### Figure 3
Use:
- any-spending;
- Top75;
- optionally the new decomposition as a third panel only if immediately readable.

Prefer 3 main figures total.

## 29. Figure captions

Rewrite captions in JEBO style:
- short substantive takeaway;
- precise outcome definition;
- sample;
- CI definition;
- lines connect three randomized discrete amounts;
- no within-person interpretation;
- no “Medical is flat” claim based solely on nonsignificance.

Preserve source data and vector formats.

---

# PART XI. TABLES AND SUPPLEMENT

## 30. Main tables

Keep main text sparse.

Preferred tables:

### Table 1
Design / cell counts / treatment definitions / perhaps sample characteristics.

### Table 2
Form-specific amount slopes and cross-form slope differences:
- ordinal;
- midpoint;
- Top75.

Show raw effect sizes and CIs clearly.

Multiplicity-adjusted results should appear in a compact column or note, not dominate the table.

### Table 3
Optional decomposition / interpretation table if needed.

## 31. Supplement

Move most NC audit material out of the main paper.

Supplement should include:
- full threshold profile;
- all original response bins;
- ordered logit/probit;
- 420 specification grid;
- relative-scale checks;
- implied-yuan translation;
- Food bindingness diagnostics;
- income diagnostics;
- all-X / who-drives summary;
- quality samples;
- population calibration sensitivity;
- detailed multiplicity procedures;
- historical analysis lineage.

Do not discard inconvenient results.

---

# PART XII. CLAIM AND REFERENCE AUDIT

## 32. Claim ledger

Create `JEBO_CLAIM_LEDGER.csv`.

For every substantive manuscript claim record:
- manuscript location;
- claim text;
- type: fact / inference / interpretation / limitation;
- source;
- strength status: strong / suggestive / descriptive;
- whether wording is acceptable.

Special audit flags:
- “flat”
- “invariant”
- “mental accounting”
- “fungibility”
- “earmarked”
- “restriction”
- “tail”
- “mechanism”
- “representative”
- “MPC”
- “spending”

## 33. Reference audit

For each reference:
- verify authors / year / title / journal;
- DOI;
- publication status;
- whether the manuscript statement accurately reflects the paper;
- no citation from abstract-only snippets if full paper says something more nuanced.

For new 2025–2026 literature, record access date and status.

---

# PART XIII. JEBO-SPECIFIC METHODS AND LIMITATIONS

## 34. Hypothetical outcome

The main text must say early enough that outcomes are stated/hypothetical.

But do not let this dominate the first page.

The discussion should explain:
- hypothetical elicitation is standard in part of the MPC literature;
- random assignment identifies scenario effects on stated responses;
- it does not identify realized spending effects;
- response bins / examples may affect measurement.

## 35. Bundled transfer-form treatment

Food and Medical change several things at once:
- category restriction;
- liquidity;
- label;
- expiry / horizon;
- perhaps perceived commitment.

Therefore:
- “transfer form” is causally randomized;
- individual mechanisms are not.

This distinction must remain exact.

## 36. Multiplicity history

The main paper should report the relevant adjusted inference succinctly.

Detailed history of:
- 1,500 old tests;
- maxnorm;
- min-P simulation;
- score-level procedures

belongs in supplement / methods audit.

Do not hide the history, but do not turn the paper into a statistics audit.

---

# PART XIV. STOP RULES

## 37. Stop new empirical exploration after the manifest tasks

After:
- extensive/intensive decomposition;
- literature-matched size benchmark;
- conceptual prediction synthesis;

do not add new empirical searches.

No “one more mechanism.”

No moderator fishing.

No new cutoffs.

No new sample screens.

No new multiplicity family.

If the story remains suggestive, write it as suggestive.

---

# PART XV. FINAL DELIVERABLES

## 38. Required outputs

Create:

### Core result notes
- `消费调查/results/jebo_transition/JEBO_EVIDENCE_FREEZE.md`
- `JEBO_ANALYSIS_MANIFEST.md`
- `JEBO_LITERATURE_MAP.md`
- `jebo_literature_matrix.csv`
- `JEBO_OUTLET_BENCHMARK.md`
- `EXTENSIVE_INTENSIVE_NOTE.md`
- `MPC_SIZE_LITERATURE_BENCHMARK.md`
- `BEHAVIORAL_PREDICTIONS.md`
- `JEBO_STORY_DECISION.md`
- `RESULT.md`

### New aggregate analysis outputs
- `extensive_intensive_cells.csv`
- `extensive_intensive_decomposition.csv`
- `mpc_size_literature_benchmark.csv`
- any figure source CSV if a new decomposition figure is actually used

### Manuscript
- `消费调查/manuscript/jebo_v1/JEBO_manuscript_v1.md`
- `JEBO_manuscript_v1.docx`
- `JEBO_supplement_v1.md`
- `JEBO_supplement_v1.docx`
- figure package
- claim ledger
- reference audit
- source manifest
- author-info checklist

## 39. Final result memo

`RESULT.md` should state:

1. the final JEBO story in 3–5 sentences;
2. whether the literature audit supports novelty;
3. whether the new extensive/intensive decomposition materially strengthens the story;
4. what the strongest evidence is;
5. what remains suggestive;
6. what mechanism is not identified;
7. what changed relative to NC v5;
8. which old analyses were moved to supplement;
9. exact manuscript / figure paths;
10. branch / commit / PR.

---

# PART XVI. PR DELIVERY

## 40. Pull request

Open a new PR:

- head: `feature/jebo-repositioning`
- base: `feature/nc-evidence-revision` unless the dependency structure has changed and a safer stacked base is required.

Suggested title:

**Reposition consumption survey as JEBO MPC-size × transfer-form paper**

PR body should summarize:
- literature conclusion;
- bounded new analysis;
- main story;
- manuscript rewrite;
- evidence limits;
- no unrestricted exploration.

Do not merge automatically.

---

# PART XVII. QUALITY CONTROL

## 41. Statistical fidelity

Before final delivery:
- reproduce every headline number from approved aggregate sources or the new finite analysis;
- check all decomposition identities;
- verify bootstrap seeds and cell stratification;
- check no respondent-level data are committed;
- ensure no accidental use of minors in adult-primary new analysis;
- ensure no new claim treats conditional-positive analysis as causal.

## 42. Manuscript fidelity

Check:
- title / abstract / intro all tell the same story;
- strong vs suggestive findings are distinguished consistently;
- figures and tables use the same sample and coding labels;
- Food and Medical are not silently pooled except when explicitly labeled as a derived contrast;
- “MPC” is qualified as stated / midpoint-coded where necessary;
- realized-spending language is removed where unsupported.

## 43. Visual QA

Existing figures should be reused where possible.

For any new / relabeled figure:
- inspect PDF;
- inspect PNG;
- check labels;
- check fonts;
- no clipping;
- no significance stars cluttering figures;
- source-data traceability.

## 44. Final intellectual check

Before opening the PR, answer in the result memo:

> If a JEBO editor reads only the title, abstract, Figure 1, and the first two pages, is the behavioral question obvious and interesting?

and:

> If the editor then reads the inference section, does the paper remain credible rather than appearing to have hidden the weaker interaction evidence?

If either answer is no, revise the writing—not the data search.
