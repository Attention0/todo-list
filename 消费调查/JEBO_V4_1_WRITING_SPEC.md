# JEBO v4.1 Writing Refinement Specification — sharpen the economics, remove reviewer-response tone

## 0. Purpose

This is a **writing-only refinement** of the completed JEBO v4 manuscript in PR #20.

Scientific source of truth:
- PR #20
- branch: `feature/jebo-v4-narrative-rewrite`
- head: `0685af82e06df1f43590c015379c2fb94fc4ac86`

The v4 scientific content is already the correct base. This revision must **not** add new empirical analysis, new hypothesis tests, new moderators, new specifications, or new literature-driven empirical searches.

The goal is narrower and important:

> **Make the manuscript read like a strong JEBO paper rather than a reviewer-response document.**

Keep all PR19/PR20 statistical boundaries and factual corrections. Improve the manuscript by:
- strengthening the central economic fact;
- simplifying the main-text mechanism discussion;
- moving technical audit detail to the supplement;
- making the unified interpretation more coherent and memorable;
- ending the paper with the substantive finding rather than with defensive caveats.

---

# 1. Core principle

The main paper should be organized around one central empirical configuration:

> **Cash, Food, and Medical follow different distributional adjustment paths as transfer size increases, yet their mean stated spending shares move substantially closer together.**

This is stronger and more informative than any one of the following alone:
- “Cash MPC declines with size”;
- “form×size interaction is significant/not significant”;
- “spendability may matter”;
- “share and yuan differ.”

The reader should remember:

1. Cash declines clearly.
2. Food declines less.
3. Medical's mean is nearly flat.
4. Small-transfer form differences are large.
5. Large-transfer mean differences are much smaller.
6. The three forms reach closer means through **different changes in the response distribution**.
7. This is a spending-share/allocation puzzle, not a collapse in implied yuan spending.

Everything else should serve this fact.

---

# 2. What must remain unchanged scientifically

Do not alter any of the following PR19/PR20 conclusions:

1. Cash midpoint and Top75 trends survive the 42-test correction.
2. Cash ordinal trend does not survive the 42-test correction.
3. Cross-form interactions remain uncertain under the expanded correction.
4. Similar large-amount incremental-yuan point estimates do not establish equal slopes.
5. Affine models are descriptive, not structural.
6. Interval-model parameters depend on residual-scale assumptions.
7. The Food sharp increasing-bindingness prediction has the wrong observed sign under the historical proxy.
8. Continuous moderator nulls are imprecise and cannot exclude meaningful heterogeneity.
9. Above-bottom/bottom-category decomposition is a coding identity, not a causal participation/intensive-margin decomposition.
10. Resource categorization / perceived spendability is not directly measured.
11. The survey is hypothetical and the form treatments bundle multiple attributes.
12. Missing recruitment/ethics/randomization implementation facts must not be invented.

The revision should **change emphasis and prose, not scientific content**.

---

# 3. Main writing problem to fix

V4 is scientifically sound, but some paragraphs still read like:
- response to reviewer comments;
- statistical audit;
- limitation-first exposition.

Common symptoms to remove:
- paragraphs ending automatically with “however / cannot establish / should not be interpreted…”;
- too many p-values, MDEs, calibration errors and model-comparison details in the main text;
- repeated restatement of inferential boundaries after the reader already understands them;
- mechanism sections that read as a list of diagnostics rather than a sequence of economic questions;
- Discussion ending by shrinking the paper to the narrowest safe statement.

The correct writing strategy is:

> **claim the randomized-cell facts strongly, explain them clearly, and place inferential boundaries exactly where they matter.**

Do not turn every paragraph into a disclaimer.

---

# 4. Abstract revision

The Abstract should be more substantive and less audit-like.

Preferred structure:

1. Question: does transfer form matter equally at small and large amounts?
2. Design: randomized 3×3, N=5,480 adults.
3. Three-puzzle fact:
   - Cash declines;
   - Food declines less;
   - Medical is nearly flat;
   - mean form gaps shrink sharply with amount.
4. Distributional anatomy:
   - Cash = high-response compression with stable bottom;
   - Food = broader redistribution;
   - Medical = offsetting movements behind a flat mean.
5. Scale clarification:
   - implied yuan rises strongly;
   - this is an allocation-share puzzle.
6. Mechanism result:
   - sharp simple Food bindingness prediction has the wrong sign;
   - broader need/resource moderators are not decisive.
7. Unified interpretation:
   - resource categorization provides the most coherent organizing interpretation of the joint pattern.
8. Final boundary sentence:
   - stated hypothetical responses;
   - mechanism not directly measured.

Do not include too many correction-family details in the Abstract. One short phrase such as “formal cross-form interaction evidence remains uncertain after multiplicity adjustment” is enough.

Target: about 170–200 words.

---

# 5. Introduction refinement

Keep the current v4 structure, but sharpen it.

## 5.1 Opening

The first three paragraphs should remain strongly substantive.

Within the first ~500 words, the reader should know:
- Cash declines;
- Food declines less;
- Medical is flat;
- gaps shrink sharply at large amounts;
- these are the three puzzles.

Do not start with measurement limitations.

## 5.2 Standard theory benchmark

State clearly:

> A declining finite-windfall spending share is compatible with standard consumption-smoothing and liquidity-based reasoning.

Then immediately explain why the real puzzle is comparative:

> What standard Cash logic does not explain by itself is why the Medical mean is flat, why Food does not decline faster than Cash, and why the form gaps narrow so strongly with size.

This contrast should be sharper than in v4.

## 5.3 Scale paragraph

Keep the percentage/yuan distinction, but make it serve the puzzle.

Preferred message:

> The convergence is in spending shares, not in the disappearance of absolute spending responses.

Do not overdevelop affine-model details in the Introduction.

## 5.4 Distribution paragraph

This should be one of the strongest Intro paragraphs.

Use:
- Cash: high-response compression;
- Food: more diffuse reallocation;
- Medical: offsetting movement;
- mean convergence without distributional identity.

This should preview Section 5 vividly.

## 5.5 Mechanism-preview paragraph

Replace any “diagnostic catalogue” tone with a progressive reasoning sequence:

> We then ask increasingly demanding questions of the three-puzzle pattern.

Sequence:
1. ordinary size dependence;
2. scale/arithmetic;
3. bottom-category accumulation;
4. mechanical bindingness;
5. category need;
6. relative income/liquidity;
7. observable types.

State:
- one sharp Food prediction is contradicted;
- broader alternatives remain incompletely distinguished;
- the most coherent organizing interpretation is resource categorization across scale.

## 5.6 Contribution paragraphs

Keep the literature positioning but shorten where possible.

The Introduction should not spend more prose on novelty defense than on the empirical contribution.

Closest dialogue to foreground:
- Fuster / Andreolli–Surico / Jappelli et al. for size;
- Bernard for joint form×size precedent;
- Boehm/Bonomo for realized transfer-form evidence;
- Lee/Pauls–Laudi for JEBO behavioral representation;
- Crossley/Parker–Souleles for elicitation boundaries.

---

# 6. Section 5 — Distributional anatomy

This is currently the strongest part of the paper.

**Do not weaken it.**

Retain the core language:
- Cash: contraction of the highest-response category with stable bottom;
- Food: diffuse redistribution;
- Medical: flat mean generated by offsetting movements;
- convergence without distributional identity.

Strengthen one conceptual sentence at the end of Section 5:

> **The central empirical fact is therefore not merely that the three means move closer. It is that Cash, Food and Medical arrive at those closer means through different distributional paths.**

This sentence should bridge directly to Section 6.

Do not add extra caveats beyond the existing essential measurement boundary.

---

# 7. Section 6 — Remove audit tone, keep logic

This section needs the largest stylistic revision.

The main text should answer economic questions. Technical precision should move to the supplement.

## 7.1 General rule

Each subsection should have this structure:

1. **Economic idea / prediction**
2. **What the distributional evidence implies**
3. **What the formal PR19 diagnostic adds**
4. **Interim conclusion in plain economic language**

Do not lead with model names, p-values, MDEs, or calibration statistics.

## 7.2 6.1 Standard size dependence

Keep it short.

Main point:

> Standard smoothing can rationalize Cash's decline, but it does not explain why Medical is flat, Food declines less, and the three forms move closer.

This establishes the benchmark and moves on.

## 7.3 6.2 Scale / affine

Main text should retain only:
- shares fall while yuan rises;
- affine description shows that near-proportional yuan growth can coexist with declining shares;
- common-slope/equal-slope interpretation is not established.

Move details such as:
- RMSE values;
- interval calibration errors;
- alternate residual-scale parameter values;
to supplement unless absolutely necessary.

The main-text conclusion should be:

> Scale explains what the puzzle is, not why the three resource forms follow different paths.

## 7.4 6.3 Bottom category

Keep very concise.

Main point:

> The Cash decline is not generated by a growing bottom-category mass, and Food/Medical bottom shares do not provide a common account either.

Do not over-discuss decomposition mechanics here; detailed identity belongs in supplement.

## 7.5 6.4 Food bindingness

This subsection should remain strong and explicit.

State the sharp prediction first.

Then:

> Under the historical proxy, the observed sign is the opposite of that prediction.

This is one of the few places where strong wording is justified:
- “contradicts the sharp prediction” is acceptable.

Then immediately state scope:
- coarse observational proxy;
- does not reject all binding-constraint models.

Move detailed ratio-model restrictions and multiple p-values to supplement, keeping only the main result in text.

## 7.6 6.5 Category need

Reduce technical detail.

Main message:

> Baseline category need does not provide a clear organizing explanation for the three puzzles at the available precision.

One representative estimate/CI is enough in main text; move full MDE discussion to supplement.

## 7.7 6.6 Relative income/liquidity

Again, simplify.

Main message:

> Relative financial scale remains plausible, but it does not parsimoniously organize Cash, Food and Medical into one coherent pattern.

Keep only the most informative evidence in main text.

Move prediction-loss percentages and technical restriction detail to supplement unless needed for one sentence.

## 7.8 6.7 Observable types

This should be brief.

Main message:

> No readily observed household type provides a stable account of the joint pattern, although meaningful unobserved or imprecisely measured heterogeneity remains possible.

Do not discuss all-X machinery at length in main text.

---

# 8. Section 7 — Strengthen the unified interpretation

This section should be more affirmative than v4.

The preferred framing is:

> **The most coherent organizing interpretation of the joint pattern is that resource form matters most when the transfer is small enough to be treated as a readily categorized allocation.**

This is stronger than “one possible candidate” but remains scientifically valid if immediately bounded.

Then explain the three paths:

### Cash
Small Cash generates an unusually large high-spending-share mass.
As amount rises, this high-response premium compresses.

### Food
Food arrives with a designated use and therefore begins from a less extreme allocation distribution.
Its adjustment with size is more diffuse.

### Medical
Medical is the most pre-categorized/persistent resource.
Amount changes its internal response distribution, but opposing movements nearly cancel in the mean.

### Convergence
Larger amounts reduce the distinctive small-Cash premium, bringing mean spending shares closer even though distributions remain different.

This is the unified story.

Then state clearly:

> The survey does not measure the categorization process itself.

Do **not** repeat this limitation in every paragraph.

## 8.1 Preferred terminology

Good:
- “organizing interpretation”
- “coherent behavioral account”
- “resource categorization across scale”
- “perceived spendability as a candidate construct”

Avoid:
- “identified mechanism”
- “proved mental accounting”
- “we rule out all alternatives”

## 8.2 Future experiment

Keep current prospective predictions, but make them flow from the interpretation:
- directly measure perceived spendability;
- current spending vs saving/debt/future allocation;
- common horizon;
- separate label/restriction/expiry/liquidity;
- realized transfers and transactions.

---

# 9. Discussion revision

Discussion should be contribution-first.

Preferred order:

## 9.1 First contribution — size changes the importance of form

State:

> **Transfer form matters most at the small end of the observed amount range.**

Then explain:
- large gaps at RMB 200;
- much smaller gaps at RMB 5,000;
- interaction inference remains uncertain, so this is an observed-cell pattern rather than a universal law.

## 9.2 Second contribution — different routes to similar means

State:

> **Similar average spending shares can conceal very different distributional adjustments.**

Use Medical as the clearest example.

## 9.3 Third contribution — policy/behavioral interpretation

One-amount comparisons of Cash vs restricted resources may not transport across transfer sizes.

The form of a resource and the scale of the resource should be analyzed jointly.

## 9.4 Limitations

Consolidate limitations here:
- hypothetical;
- no common horizon;
- bundled treatment;
- nonrepresentative sample;
- missing metadata;
- interaction uncertainty;
- no mediator.

Do not scatter the same caveat repeatedly before this point.

## 9.5 Ending

Remove or rewrite any ending like:

> “The most secure result is narrower…”

Preferred final Discussion paragraph:

> **The central empirical fact is not simply that Cash spending shares decline with size. Cash, Food and Medical move toward much closer average spending shares through markedly different changes in the response distribution. This makes transfer size part of the behavioral meaning of transfer form itself: the same resource distinction that is pronounced at small amounts becomes much less pronounced at larger amounts. Resource categorization provides a coherent hypothesis for this pattern, and the next experiment should measure and manipulate that process directly.**

Then one short boundary sentence:
- current data motivate but do not identify that mechanism.

---

# 10. Conclusion revision

Keep Conclusion short.

Suggested logical sequence:

1. Cash declines, Food less, Medical flat.
2. Mean shares converge strongly with amount.
3. The three forms reach closer means via different distributional paths.
4. Absolute implied yuan rises strongly, so this is a share-allocation puzzle.
5. Simple Food bindingness does not organize the pattern.
6. The most coherent behavioral hypothesis is resource categorization across scale.
7. Future experiment must identify it directly.

The final sentence should be memorable and substantive, for example:

> **Transfer size does not merely scale a resource; it changes how strongly the form of that resource is reflected in spending decisions.**

This sentence is acceptable as an interpretation of the observed configuration, not as a universal causal theorem.

---

# 11. Technical-detail migration

Move from main text to supplement where possible:

- full affine model-comparison statistics;
- interval-regression calibration errors and alternate scale parameters;
- full 42-test rows;
- full MDE calculations;
- all ratio restrictions;
- all-X implementation detail;
- Q1/Q2 technical details;
- weighting diagnostics.

Main text should retain:
- the key fact;
- one or two key estimates;
- the economic implication.

---

# 12. Figures and tables

Keep the four v4 main figures unless a layout improvement is needed.

Especially retain:
- Figure 1: 3×3 response atlas;
- Figure 2: share vs implied yuan;
- Figure 3: endpoint category-share changes;
- Figure 4: corrected Food diagnostic.

Figure 3 should remain a central figure.

Main tables should remain compact. Do not re-expand the technical tables removed to supplement.

---

# 13. Literature tone

No new broad literature search is needed.

Use the existing v4 reference audit.

The rewrite should improve **dialogue**, not add citations.

Each literature paragraph should answer one of:
- what does standard theory predict/allow?
- what is already known about size dependence?
- what is already known about resource form / earmarking?
- what does Bernard already do?
- why are realized-transfer papers stronger on behavior but different in outcome?
- what do elicitation papers imply for interpretation?

Do not write a catalog.

---

# 14. Word deliverable

Produce:

- `消费调查/manuscript/jebo_v4_1/JEBO_manuscript_v4_1.md`
- `JEBO_manuscript_v4_1.docx`
- `JEBO_supplement_v4_1.md`
- `JEBO_supplement_v4_1.docx`
- `JEBO_Highlights_v4_1.docx`
- `V4_1_CHANGELOG.md`
- `V4_1_FINAL_AUDIT.md`

Formatting should inherit v4:
- Times New Roman;
- 12 pt body;
- justified;
- first-line indent ~0.74 cm;
- clean tables/figures;
- page numbers;
- no tracked changes/comments.

Do not overwrite v4.

---

# 15. Final audit questions

Before delivery, verify:

1. Does Abstract lead with the economic finding rather than the audit?
2. Are the three puzzles obvious in the first 500 words?
3. Does Section 5 remain one of the paper's central results sections?
4. Does Section 6 read as economic reasoning rather than test-by-test reporting?
5. Is Section 7 confident enough to offer a unified organizing interpretation?
6. Does Discussion end with the paper's substantive contribution rather than retreat?
7. Are all PR19/PR20 scientific boundaries preserved?
8. Has any sentence accidentally upgraded descriptive convergence into a proven population interaction?
9. Has any sentence treated spendability/resource categorization as measured?
10. Has any new analysis been introduced? It must not be.

The final manuscript should feel **more confident because it is better organized**, not because any statistical boundary was weakened.
