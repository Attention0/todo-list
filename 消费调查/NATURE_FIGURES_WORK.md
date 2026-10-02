# Nature-level main figures package for the MPC paper

## 0. Goal

Create a polished, publication-ready four-figure main-text package for the consumer-survey paper.

This is a VISUALIZATION task, not a new empirical-analysis task.

Use only already established results from PR #9–#12 and their existing source-data tables. Do not alter estimands, re-run exploratory searches, change samples, invent new smoothing, or create new substantive claims.

The visual standard should be suitable for a Nature-family / Nature Communications submission:
- clean;
- minimal;
- high information density;
- no decorative clutter;
- immediately readable at journal column width;
- visually coherent across all figures;
- every panel should have one clear message.

The figures must tell the paper story in sequence:

1. Transfer form changes how stated MPC scales with transfer size.
2. The Cash-versus-restricted gap is most pronounced for small transfers and attenuates with size.
3. The mean pattern is driven visually by compression of the high-MPC tail, not by an extensive-margin collapse.
4. Rich observed characteristics do not provide a stable explanation for the form-by-size pattern.

Do not modify the manuscript in this task.

---

# PART I. GLOBAL VISUAL SYSTEM

## 1. Figure dimensions and export

Produce each main figure as:
- vector PDF;
- SVG;
- 600 dpi PNG;
- source-data CSV;
- editable plotting script.

Also provide:
- one combined PDF containing all four figures;
- one contact sheet PNG showing the four figures together.

No raster-only text.

Target sizing:
- figures should remain legible at ~180 mm full-page width;
- individual text should remain readable if reduced to ~89 mm single-column width where applicable.

## 2. Typography

Use a clean sans-serif typeface available in the environment, preferably:
- Arial;
- Helvetica;
- Liberation Sans;
- or another close journal-safe sans-serif.

Approximate final-size typography:
- panel labels A/B/C: 9–10 pt bold;
- axis titles: 8–9 pt;
- tick labels: 7–8 pt;
- legends: 7–8 pt;
- annotations: 7–8 pt.

Avoid oversized titles inside plots.

Main figure titles should NOT be embedded as giant chart titles. Use concise panel subtitles only where necessary.

## 3. Color system

Use a colorblind-safe, restrained palette and keep it identical across all figures.

Preferred treatment colors:

- Cash: deep navy / blue, approximately #1F4E79
- Food: teal / green, approximately #2A9D8F
- Medical: muted orange / terracotta, approximately #D97757
- Restricted equal-weight contrast: muted violet, approximately #7564A3
- Neutral/reference: medium gray, approximately #7A7A7A

If exact hex values render poorly, Work may adjust slightly, but:
- Cash must remain the strongest visual emphasis;
- Food and Medical should remain visually distinct;
- Restricted must never look like a randomized fourth treatment;
- gray should be used for reference/null/secondary information.

Use white background.

Do not use:
- rainbow palettes;
- gradients;
- saturated red/green opposition;
- heavy shadows;
- 3D effects.

## 4. Lines and markers

Treatment lines:
- Cash: strongest line weight;
- Food / Medical: slightly lighter;
- Restricted: medium weight and, where useful, dashed or outlined to visually communicate that it is a derived contrast.

Use distinct marker shapes only if needed for accessibility:
- Cash circle;
- Food square;
- Medical triangle;
- Restricted diamond/open circle.

Keep markers small and elegant.

## 5. Axes and grid

- Remove top/right spines where appropriate.
- Use either no grid or very faint horizontal grid lines.
- Avoid boxed plotting regions.
- Use direct labels where possible instead of legends.
- Use consistent y-axis units and percentage formatting.
- Do not truncate axes in ways that visually exaggerate treatment differences.
- If panels have different outcome units, make this explicit.

## 6. Confidence intervals

Use 95% confidence intervals from the existing approved source tables.

Prefer:
- thin vertical error bars;
- or light ribbons when lines are central and ribbons do not obscure overlap.

Do not encode statistical significance by stars on the plotted points.

Formal p-values / adjusted p-values belong in captions or tables, not as visual clutter.

## 7. Panel labels and annotations

Panel labels:
- A, B, C, etc.
- upper-left;
- consistent positioning.

Annotations should be sparse and declarative, e.g.:
- "Cash: 13.4% → 5.3%"
- "0 of 150 representations: BH q<0.10"

Do not annotate every point.

---

# PART II. FIGURE 1 — THREE DEFINITIONS OF THE MPC-SIZE CURVE

## 8. Core purpose

Figure 1 should be the visual centerpiece.

Message:

> Across three ways of representing the elicited response, Cash exhibits the strongest decline with transfer size, while Food and especially Medical show flatter profiles.

This must be a 1 × 3 horizontal combined figure.

## 9. Panel structure

### Panel A — Original ordinal response

Y-axis:
- mean original response category, 1–6.

X-axis:
- RMB 200
- RMB 1,000
- RMB 5,000

Lines:
- Cash
- Food
- Medical

Use raw randomized-cell means and approved 95% CIs.

Do NOT label this as "MPC" without qualification.
Preferred y-axis label:
- "Mean stated spending-response category"

Add a tiny note beneath or in caption:
- Higher categories indicate a larger stated share spent.

### Panel B — Midpoint-coded stated MPC

Y-axis:
- midpoint-coded stated MPC share.

Use the established coding:
0, .05, .175, .375, .625, .875.

Prefer percentage-point display:
- 0%
- 10%
- 20%
- 30%

Y-axis label:
- "Midpoint-coded stated MPC"

Same X and treatment lines as Panel A.

This panel should visually anchor the economic interpretation.

### Panel C — High-MPC tail

Y-axis:
- probability of choosing category 6 (>75%).

Y-axis label:
- "Pr(stated MPC >75%)"

Display as percent.

Same X and treatment lines.

This panel should make the Cash upper-tail compression immediately visible.

## 10. Figure 1 layout details

The three panels should:
- share the same X positions;
- use identical treatment colors;
- have equal plotting widths;
- align x-axis ticks vertically;
- use concise outcome labels.

Do NOT force the same y-scale across different outcome units.

Direct-label each treatment line near RMB 5,000 if this remains readable.
Otherwise use one compact shared legend centered beneath the panels.

Use actual amount labels rather than z=-1/0/1 in the figure.

Lines connect three randomized discrete amounts only; do not imply continuous dose-response.

## 11. Existing inputs

Use existing PR #9 / #10 source data wherever possible:
- fig1_source.csv;
- figA_source.csv;
- corresponding approved cell means/CIs.

If the exact three-panel source table does not exist, construct a new aggregate source CSV solely by reshaping already approved summary data.

No respondent-level export.

Required source:
- figure1_main_source.csv

Columns should include:
- panel/outcome;
- form;
- amount;
- estimate;
- lower CI;
- upper CI;
- N where available.

---

# PART III. FIGURE 2 — THE PUZZLE: THE FORM GAP ATTENUATES WITH SIZE

## 12. Core purpose

Figure 2 should directly communicate the paper's surprising pattern.

Message:

> The Cash-versus-restricted difference is larger for small transfers and attenuates as transfer size increases, opposite the simplest "restrictions become more binding at larger amounts" intuition.

Do not state that standard theory is violated.
The figure should show the empirical pattern only.

## 13. Preferred layout: 1 × 2

### Panel A — Midpoint MPC: Cash vs Restricted

Show:
- Cash;
- Restricted = 0.5 Food + 0.5 Medical.

Use approved equal-weight Restricted estimates from PR #10.

Plot the two curves across:
- 200;
- 1,000;
- 5,000.

Use:
- Cash deep navy solid;
- Restricted muted violet dashed or open-marker.

Very clearly note in caption:
- Restricted is an equal-weight derived contrast, not a fourth randomized treatment.

If visually clean, lightly shade or annotate the vertical difference between the curves at each amount.

Do NOT create pseudo-CIs for the gap unless they are available from approved bootstrap results.

### Panel B — Top-MPC probability: Cash vs Restricted

Same design, but Y:
- Pr(MPC >75%).

This should display the strongest and cleanest distributional version of the puzzle.

Optional small annotation:
- Cash 200→5000 high-MPC probability change ≈ −8.1 pp.
- Restricted change ≈ −2.2 pp.

Use exact approved values from PR #10.

## 14. Optional alternative if superior

If a direct "gap" figure is visually clearer, Work may use:

Y-axis:
- Cash minus Restricted difference

across the three transfer amounts,

with two panels:
- midpoint MPC gap;
- Top75 probability gap.

But only use this alternative if:
- exact approved gap estimates and CIs can be computed from existing approved aggregate/bootstrap outputs;
- it visually improves understanding;
- no new inferential procedure is introduced.

Preferred default remains the two-curve comparison because it is immediately interpretable.

## 15. Required source

- figure2_main_source.csv

Clearly flag rows as:
- randomized treatment;
- derived equal-weight contrast.

---

# PART IV. FIGURE 3 — DISTRIBUTION ANATOMY: WHERE DOES THE CASH DECLINE COME FROM?

## 16. Core purpose

Message:

> Cash's falling average stated MPC is not primarily an extensive-margin phenomenon; it is most visibly associated with compression of the high-MPC tail.

The figure should be visually simple enough to understand in seconds.

## 17. Preferred layout: 1 × 2

### Panel A — Any additional spending

Y:
- Pr(any additional spending)

Across 200 / 1,000 / 5,000 for:
- Cash;
- Food;
- Medical.

This panel should visually show that the extensive margin is relatively flat.

Use the approved threshold data.

### Panel B — Spend >75%

Y:
- Pr(stated MPC >75%)

Across the same amounts/forms.

This panel should show the sharp Cash decline.

The conceptual contrast between A and B is the entire point.

## 18. Required annotation

In Panel B, annotate the Cash endpoints only:
- approximately 13.4% at 200;
- approximately 5.3% at 5,000.

Use exact approved values.

Do not annotate every form.

## 19. Supplemental distribution figure

Also produce a supplementary six-bin composition figure using the existing six-category shares:
- preferably 100% stacked bars;
- form × amount displayed compactly;
- categories ordered from no additional spending to >75%.

This six-bin figure is NOT necessarily a main figure.

Name:
- Figure Sx — full stated-MPC distribution.

It should help reviewers verify that the threshold framing is not hiding the rest of the distribution.

## 20. Required source

- figure3_main_source.csv
- figureS_distribution_source.csv

---

# PART V. FIGURE 4 — RICH OBSERVABLES DO NOT EXPLAIN THE FORM-BY-SIZE PATTERN

## 21. Core purpose

This figure must summarize the all-X screen without becoming a giant data-mining graphic.

Message:

> Across a broad pre-treatment variable screen, neither subjective nor objective observables produce a stable FDR-corrected moderator of the Cash size slope or the Restricted-versus-Cash slope difference.

This is a "negative evidence" figure and must look intentional, not empty.

## 22. Preferred layout: 1 × 2 with a compact summary strip

### Panel A — Cash slope moderation screen

Create a clean ranked dot/interval plot for all eligible estimable X representations, but avoid unreadable labels.

Recommended design:
- x-axis: standardized interaction estimate, transformed to a comparable standardized-effect display only where scientifically valid;
- y-axis: ranked variables;
- because ~146 variables are too many to label, plot all as small points and label only the 8–12 largest absolute estimates;
- visually distinguish:
  - subjective;
  - objective;
  - constructed;
  - raw
  using marker fill/shape, not an explosion of colors.

Alternative:
- use x-axis = signed standardized interaction estimate;
- y-axis = −log10(raw p);
- add the BH q=.10 decision contour / threshold if correctly calculated.

Choose whichever visualization is clearer and less misleading.

Prominent annotation:
- "0 / 150 representations with BH q < 0.10"

### Panel B — Restricted−Cash slope moderation screen

Use the same visual grammar.

Prominent annotation:
- "0 / 150 representations with BH q < 0.10"

## 23. Summary strip / inset

Add a small, elegant categorical summary either beneath the two panels or as an inset:

Groups:
- raw subjective;
- raw objective;
- constructed subjective;
- constructed objective.

For each show:
- number screened;
- number BH q<.10 = 0.

Do not use a large bar chart of zeros.
A compact text/tile strip is preferable.

## 24. Important visual safeguards

- Do not imply that all X have exactly zero effects.
- Do not interpret lack of corrected discoveries as equivalence.
- Keep raw p-value "interesting" points visually neutral.
- No stars.
- Do not highlight nominally significant variables in red.
- The key message is lack of a stable corrected explanatory signature.

## 25. If Panel A/B become too dense

Allowed alternative:

Use the six family-level minimum BH q-values:
- Cash ordinal;
- Cash midpoint;
- Cash Top75;
- RC ordinal;
- RC midpoint;
- RC Top75;

and combine them with a compact subjective/objective discovery summary.

However, the preferred figure should preserve as much of the all-X screen information as possible without sacrificing readability.

## 26. Required source

- figure4_main_source.csv
- figure4_summary_source.csv

Use the approved PR #12 all-X results.

No new moderator search.

---

# PART VI. SUPPLEMENTARY / EXTENDED DATA FIGURES

## 27. Reformat existing robustness figures

Do NOT rebuild every old figure unless easy, but provide publication-polished versions of the most useful existing diagnostics:

### Extended Data 1 — Threshold profile
Use PR #10 figB.

### Extended Data 2 — Relative-scale robustness
Use PR #10 figC.

### Extended Data 3 — Specification curve
Use PR #10 figD.

### Extended Data 4 — MPC share versus implied yuan spending
Use PR #10 figE.

### Extended Data 5 — Full six-category distribution
From PR #9.

### Extended Data 6 — All-X detailed screen
The full all-X screen / volcano / raw-constructed diagnostics may live here if Figure 4 uses a more compact main-text summary.

Keep visual style consistent with the four main figures.

---

# PART VII. NATURE-LEVEL DESIGN PRINCIPLES

## 28. Simplify aggressively

Before finalizing each figure, ask:

> Can a reader understand the main message in 5 seconds?

Remove:
- redundant legends;
- repeated axis titles;
- excessive decimals;
- unnecessary borders;
- significance stars;
- internal chart titles;
- background shading unless it conveys information.

## 29. Preserve information density

Minimal does not mean empty.

Prefer:
- direct labeling;
- informative uncertainty;
- concise annotations;
- aligned panels;
- shared legends;
- coherent scales.

## 30. Number formatting

Percent outcomes:
- display as percentages, not decimals.

Midpoint MPC:
- preferably percent.

Ordinal:
- one decimal tick precision if needed.

Amounts:
- "¥200", "¥1,000", "¥5,000" on axes.

Confidence intervals:
- no more decimal places than substantively meaningful.

## 31. Accessibility

Check:
- grayscale readability;
- common color-vision deficiency simulation if available;
- small-size legibility;
- PDF vector output.

Do not rely on color alone for the Cash-vs-Restricted comparison.

---

# PART VIII. CAPTIONS

## 32. Write publication-ready captions

Create:
- MAIN_FIGURE_CAPTIONS.md

For each figure include:
- one-sentence substantive takeaway;
- outcome definition;
- randomized design note;
- CI definition;
- sample definition;
- Restricted-definition warning where applicable;
- statement that lines connect discrete randomized transfer amounts;
- no claim of individual within-person change.

Captions should be concise enough for Nature Communications style.

Do not overload captions with all robustness tests.

---

# PART IX. OUTPUT DIRECTORY

Create:

消费调查/results/nature_main_figures/

Required files:

- fig1_three_outcomes.pdf/svg/png
- fig2_cash_restricted_puzzle.pdf/svg/png
- fig3_distribution_anatomy.pdf/svg/png
- fig4_observables_null.pdf/svg/png
- main_figures_combined.pdf
- main_figures_contact_sheet.png

Source data:
- figure1_main_source.csv
- figure2_main_source.csv
- figure3_main_source.csv
- figure4_main_source.csv
- figure4_summary_source.csv
- figureS_distribution_source.csv

Supporting:
- MAIN_FIGURE_CAPTIONS.md
- FIGURE_STYLE_GUIDE.md
- FIGURE_AUDIT.md
- plotting scripts

Supplement / Extended Data versions where feasible.

---

# PART X. QUALITY CONTROL

## 33. Statistical fidelity

For every plotted number:
- trace it to an approved prior result/source table;
- no silent re-estimation if the approved statistic already exists;
- no respondent-level exports;
- no new substantive specification.

Create an audit table mapping:
- figure;
- panel;
- plotted statistic;
- prior source file;
- row/definition.

## 34. Visual inspection

Inspect every final PNG/PDF.

Check:
- no clipped labels;
- no overlapping legends;
- axis labels readable;
- CIs visible but not dominant;
- colors consistent;
- treatment ordering consistent;
- panel alignment;
- no distorted aspect ratios.

## 35. Final result note

Create:

消费调查/NATURE_FIGURES_RESULT.md

Briefly state:
- which four main figures were produced;
- what each communicates;
- any choices that differ from this plan and why;
- exact source files used;
- confirmation that no new empirical analysis or headline was introduced.

Submit via a new PR stacked on the latest analysis branch / dependency as appropriate.
