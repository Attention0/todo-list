# 消费调查项目 — Nature-Series Figure Blueprint

## 0. Purpose

This document translates `NATURE_EMPIRICAL_ROADMAP.md` into a **publication-oriented figure specification**.

The goal is not simply to generate attractive charts. Each main figure must make **one conceptual claim**, with panel order, estimand, sample, uncertainty, visual encoding, and Extended Data support fixed in advance.

This blueprint is intended for a Nature Human Behaviour / Nature Communications style manuscript.

---

# 1. Portfolio-level figure rules

## 1.1 Number of main display items

Target:
- 5–6 main figures;
- at most 1 main table if absolutely necessary;
- push diagnostic / specification / robustness content to Extended Data.

Nature Human Behaviour Articles allow up to 8 display items.
Nature Communications Articles can allow more depending on article length, but the manuscript should still aim for a compact visual story.

Do not fill the main text with regression tables.

---

## 1.2 Figure size and export

Prepare every main figure so that it is readable at final publication scale.

Preferred main-figure target:
- double-column width: 183 mm;
- single-column only for very simple one-panel figures: 89 mm;
- maximum planned height: 170 mm.

Text at final print size:
- 5–7 pt;
- consistent sans-serif font throughout;
- panel labels slightly larger / bold.

Export:
- vector PDF for all plots with lines/text;
- SVG additionally for internal editing if convenient;
- 600 dpi PNG preview for GitHub / review;
- never rasterize text unnecessarily.

White background.

Do not use:
- 3D charts;
- shadows;
- gradients;
- unnecessary boxes;
- decorative icons;
- excessive grid lines.

---

## 1.3 Colour system

Use one **consistent colour identity** across the entire paper.

Suggested semantic mapping:
- Cash = one neutral/dark colour;
- Food = one distinct cool colour;
- Medical = one distinct warm colour.

Constraints:
- colour-blind safe;
- all panels must remain interpretable in greyscale;
- never encode significance only by colour;
- use line style / marker shape when needed.

Use exactly the same Cash / Food / Medical colours in every figure.

For feature blocks:
- Objective = one neutral colour;
- Subjective economic = a second;
- Broader attitudes = a third;
- Combined sets = progressively darker variants or neutral outlines.

Do not use rainbow palettes.

---

## 1.4 Typography and annotation

Axes:
- short plain-language labels;
- units always explicit;
- avoid variable names such as `q30_medexp` in main figures.

Use labels such as:
- “Household income”
- “Past-year medical spending”
- “Stated marginal consumption response”
- “Out-of-sample R²”
- “Medical − Cash effect”

Panel labels:
- a, b, c, d in upper-left;
- consistent placement.

Annotations:
- use direct labels where possible;
- avoid giant legends;
- no significance stars in main figures;
- exact statistical inference belongs in caption / Results text.

If an estimate is central, display:
- point estimate;
- 95% CI.

---

## 1.5 Error bars

Every figure legend must state exactly what error bars mean.

Use one convention:
- 95% confidence interval for randomized contrasts / regressions;
- 95% bootstrap CI for cross-form stability differences and predictive increments;
- fold-distribution uncertainty for cross-validation summaries.

Never mix SE and 95% CI in one panel without explicit notation.

Report exact N in figure caption for every panel if N changes.

---

## 1.6 Main-text versus Extended Data

Main-text figure = conceptual result.

Extended Data = diagnostics proving credibility.

Every main figure below has a specified Extended Data companion.

---

# 2. Figure 1 — Randomized transfer form changes stated spending responses

## Main message

> The same nominal transfer amount produces systematically different stated marginal consumption responses depending on the form in which resources are delivered.

This figure introduces the experiment and establishes the randomized phenomenon before discussing heterogeneity.

Target size:
- 183 mm wide;
- ~130–150 mm high;
- 3 panels.

---

## Fig. 1a — Experimental design

### Content

A clean 3 × 3 design matrix.

Columns:
- RMB 200
- RMB 1,000
- RMB 5,000

Rows:
- Cash
- Food/daily-needs voucher
- Medical account

Each cell displays:
- randomized N;
- only a short label, not paragraph text.

Below matrix, one arrow to outcome:

“Additional total consumption relative to original plan”
→ six response categories.

Do NOT put questionnaire wording in full.

### Purpose

Make randomization immediately legible to a non-economist reader.

### No statistical annotation.

---

## Fig. 1b — Full outcome distributions by transfer form

### Sample
Raw R.

### Data
Original 1–6 outcome categories.

### Plot
100% stacked horizontal bars, one bar per transfer form:
1. Cash
2. Food
3. Medical

Order categories left-to-right:
- none
- <10%
- 10–25%
- 25–50%
- 50–75%
- >75%

Use a sequential light-to-dark fill for outcome categories.

Do not reuse Cash/Food/Medical colours here because the fill encodes response category.

### Key requirement
Add total N at right of each bar.

### Purpose
Show the entire distribution, not only midpoint means.

---

## Fig. 1c — Randomized form effects across transfer sizes

### Outcome
Primary visual:
ordinal 1–6 response.

### X-axis
Amount:
- 200
- 1,000
- 5,000 RMB

### Y-axis
Mean stated response category.

### Series
Three lines:
- Cash
- Food
- Medical

### Uncertainty
95% CI around cell mean.

### Add below / inset
A compact contrast strip showing pooled:
- Food − Cash
- Medical − Cash

with 95% CI.

### Purpose
Show:
- Medical consistently lower;
- Food modestly lower;
- amount dependence.

Do not rely on midpoint MPC here.

---

## Extended Data for Fig. 1

### ED Fig. 1
Nine-cell category distributions.

### ED Fig. 2
Midpoint-MPC and alternative top-category coding.

### ED Table 1
Randomization balance and omnibus balance test.

### ED Table 2
Exact 3×3 cell Ns and treatment contrast estimates.

---

# 3. Figure 2 — Rich information explains little of who reports a high MPC

## Main message

> Even unusually rich objective and subjective baseline information predicts only a small fraction of stated-MPC heterogeneity.

This is the direct ReStud-style bridge.

Target:
- 183 mm wide;
- 120–140 mm high;
- 3 panels.

---

## Fig. 2a — Out-of-sample predictability by information set

### Outcome
Midpoint stated MPC.

### X-axis
Feature set in fixed order:
1. Treatment only (T)
2. Objective/needs (O)
3. Subjective economic (S)
4. Broader attitudes (A)
5. O + S
6. O + A
7. ALL

### Y-axis
Repeated-CV OOS R².

### Plot
Point + interval plot, not bars if possible.

For each feature set:
- point = mean across identical repeated folds;
- vertical interval = empirical 95% fold / bootstrap interval.

Use one model for the headline panel:
- Random Forest OR best prespecified nonlinear model.

Add a small secondary marker for ridge if space permits.

Do not place four model families in the main panel.

### Horizontal reference
y = 0.

### Direct annotation
On O and ALL:
- “~4–5% of variance predicted”

No significance stars.

---

## Fig. 2b — Incremental value of subjective information

### Estimands

[
Delta R^2_{O+S-O}
]

[
Delta R^2_{O+A-O}
]

[
Delta R^2_{ALL-O}
]

### Plot
Forest plot.

### X-axis
Incremental OOS R².

### Point
Paired mean fold difference.

### CI
95% paired bootstrap CI.

### Vertical reference lines
- 0
- +0.01
- +0.02

Label +0.01 and +0.02 as:
- “predeclared practical-gain benchmarks”

### Purpose
Make the null result visually affirmative:
the data can rule out large predictive gains from subjective information.

---

## Fig. 2c — Coherent subjective states still add little

### Left side
Three latent subjective dimensions:
- Subjective economic state
- Social confidence
- Wellbeing/optimism

Show internal consistency as small text or dot:
alpha / variance explained.

### Right side
Two held-out model points:
- Objective/needs
- Objective/needs + latent subjective dimensions

Y-axis:
held-out R².

### Main annotation
[
Delta R^2 approx 0.002
]

### Purpose
Prevent critique:
“Maybe single questionnaire items are noisy; aggregate them.”

The answer:
even internally coherent latent dimensions barely improve prediction.

---

## Extended Data for Fig. 2

### ED Fig. 3
Same prediction comparison for:
- ridge;
- elastic net;
- RF;
- HGB.

### ED Fig. 4
Outcome-representation robustness:
- ordinal score;
- midpoint;
- top-coded midpoint;
- threshold outcomes.

### ED Fig. 5
Permutation importance, clearly labeled predictive not causal.

### ED Table 3
Exact mean/CI/RMSE/MAE by model and feature set.

### ED Table 4
Latent-factor loadings and diagnostics.

---

# 4. Figure 3 — Individual response rankings have limited portability across transfer forms

## Main message

> Observable rankings of who responds strongly do not transfer well across resource-delivery contexts, and Cash–Food mappings are more similar than Cash–Medical mappings.

This should be the conceptual centre of a Nature-style paper.

Target:
- 183 mm wide;
- ~145 mm high;
- 3 panels.

---

## Fig. 3a — Cross-form prediction portability matrix

### Statistic
Spearman correlation between:
- prediction trained in source form;
- realized stated response in target form.

### Matrix
Rows = training form.
Columns = testing form.

Off-diagonal cells only:
- Cash→Food
- Cash→Medical
- Food→Cash
- Food→Medical
- Medical→Cash
- Medical→Food

### Display
Heatmap with numerical value printed in every cell.

Scale:
fixed from 0 to a modest upper bound such as .30 or .40;
do not use an exaggerated full-colour diverging scale unless negative values occur.

### Do not show diagonal.
Diagonal should be blank or grey.

### Purpose
Reader should immediately see all correlations are low.

---

## Fig. 3b — Predictor-map similarity

### Statistic
Ridge coefficient-vector correlation.

### X-axis
Pair:
- Cash–Food
- Cash–Medical
- Food–Medical

### Y-axis
Coefficient-vector correlation.

### Series
Two key feature sets:
- Objective + needs
- ALL

### Points + 95% bootstrap CI.

### Formal annotations
Above pairwise comparisons, report:
- bootstrap difference Cash–Food minus Cash–Medical;
- bootstrap difference Cash–Food minus Food–Medical.

Do not use significance brackets unless aesthetically necessary.

Preferred:
small text:
“Difference = …, 95% CI …”

### Purpose
Show that Cash and Food share a more similar predictive map.

---

## Fig. 3c — Reliability attenuation sensitivity

This is mandatory if making a context-specificity claim.

### Starting statistic
Observed cross-form rank correlations.

### Assumed outcome reliability
Three scenarios:
- 0.4
- 0.6
- 0.8

### Plot
For each form pair, a line across assumed reliabilities showing attenuation-corrected correlation under classical independent measurement error.

### X-axis
Assumed reliability.

### Y-axis
Sensitivity-adjusted cross-form correlation.

### Add horizontal guides
0.25, 0.50, 0.75 if useful, labeled descriptively:
- low/moderate/high only in caption, not as hard scientific categories.

### Explicit subtitle
“Sensitivity analysis; reliability is assumed, not estimated.”

### Purpose
Directly address the strongest interpretation threat:
low cross-form stability may partly reflect noisy stated measurement.

If correction allows correlations near 1 under plausible reliability, the main claim must be weakened.

---

## Optional Fig. 3d — Shared vs form-specific predictable variance

Only include if visually clear.

### Plot
Stacked / grouped variance bars:
- Shared predictable component
- Cash-specific deviation
- Food-specific deviation
- Medical-specific deviation
- Total observed outcome variance shown as reference line.

### Important
Do not visually imply these components exactly partition total outcome variance unless mathematically true.

If decomposition is non-additive, use separate bars and say so.

---

## Extended Data for Fig. 3

### ED Fig. 6
Cross-form recentered R² and calibration slopes.

### ED Fig. 7
Coefficient cosine similarity and sign agreement.

### ED Table 5
Formal bootstrap difference tests.

---

# 5. Figure 4 — Fungibility heterogeneity differs across transfer contexts

## Main message

> The Food−Cash response gap is not predictably structured by observed traits, whereas Medical−Cash heterogeneity shows reproducible out-of-sample structure.

This figure must demonstrate the asymmetry directly.

Target:
- 183 mm wide;
- ~135–150 mm high;
- 3 panels.

---

## Fig. 4a — Food−Cash honest CATE validation

### X-axis
OOF predicted CATE quintile, 1–5.

### Y-axis
Observed randomized Food − Cash contrast in midpoint stated MPC.

### Point
Within-quintile randomized contrast.

### Error bars
95% CI.

### Overlay
Thin dashed line showing mean predicted CATE per quintile only if helpful.

### Horizontal reference
0.

### Main method
Use one prespecified learner for display:
- cross-fitted DR learner.

T/R learners go in Extended Data.

### Expected visual
No monotonic positive gradient.

---

## Fig. 4b — Medical−Cash honest CATE validation

Exactly same:
- axis scale;
- quintile bins;
- CI convention;
- method;
- y-range.

This identical scaling is essential.

Expected:
positive ordering / gradient.

---

## Fig. 4c — Formal asymmetry test

### Two possible estimands

1. calibration slope
2. top-minus-bottom observed treatment-effect separation

Plot both as paired Food vs Medical estimates.

Preferred design:
two small forest rows per metric:
- Food−Cash
- Medical−Cash

Then on right:
difference:
[
Medical - Food
]

with bootstrap 95% CI.

### Purpose
Prove:
“Medical HTE is more predictable than Food HTE”
rather than infer from separate p-values.

### No feature importance in main figure.

---

## Extended Data for Fig. 4

### ED Fig. 8
T / DR / R learner comparison.

### ED Fig. 9
Seed stability across 10 seeds.

For each learner:
- dot per seed;
- summary interval.

### ED Table 6
All calibration / top-bottom estimates and formal difference tests.

---

# 6. Figure 5 — Medical-context heterogeneity is amount-specific and economically patterned

## Main message

> The predictable Medical−Cash heterogeneity is concentrated at an intermediate transfer size and aligns with selected economic characteristics, rather than being a universal form effect.

Target:
- 183 mm wide;
- ~140 mm;
- 3 panels.

---

## Fig. 5a — HTE calibration by transfer amount

### X-axis
RMB:
- 200
- 1,000
- 5,000

### Y-axis
Medical−Cash calibration slope.

### Series
- cross-fitted T learner
- cross-fitted DR learner

### Points + 95% CI.

### Reference
0.

### Annotation
Do not label 1,000 as “optimal”.
Simply show strongest validation at 1,000.

---

## Fig. 5b — Household income moderation

### X-axis
Income category, ordered from low to high.

### Y-axis
Medical − Food OR Medical − Cash randomized contrast.

Choose ONE contrast in the main figure based on the paper claim.

If the paper centres fungibility against cash, prefer:
Medical − Cash.

If the transparent linear result is much stronger for Medical − Food, keep Medical − Food but explicitly label it as a secondary contrast.

### Display
Adjusted or raw randomized contrast within income bins.

Prefer:
- observed treatment means converted to contrast;
- 95% CI.

Do not show only a linear regression slope.

Overlay a thin fitted trend if useful.

---

## Fig. 5c — Prior medical-spending moderation

Same structure:
- ordered past-year medical spending categories;
- randomized contrast;
- 95% CI.

Use human-readable category labels.

### Purpose
Show the most interpretable context-relevance pattern.

### Important
Caption:
“Past medical spending is a proxy for prior medical exposure/need and is not a causal treatment or a strict bindingness measure.”

---

## Extended Data for Fig. 5

### ED Fig. 10
Education moderation.

### ED Table 7
Joint income / education / medical-spending moderation model.

### Supplement
Province FE / HC1 / HC3 / cluster / RI / clean-sample robustness.

Because NHB permits a maximum of 10 Extended Data display items, remaining dense robustness should move to Supplementary Tables rather than creating more Extended Data figures.

---

# 7. Figure 6 — Predictable heterogeneity does not imply useful personalization

## Main message

> Although Medical−Cash treatment-effect heterogeneity is partly predictable, personalized assignment does not outperform a uniform Cash policy for the stated-consumption objective.

This is a high-value null.

Target:
- preferably 120–136 mm or 183 mm wide;
- 1–2 panels.

---

## Fig. 6a — Honest policy value

### X-axis
Policies:
- All Cash
- All Food
- All Medical
- Depth-2 policy tree
- ML argmax

### Y-axis
OOF/IPW mean midpoint stated MPC under policy.

### Point + 95% CI.

### Add
Horizontal line at all-Cash value.

### Direct label
For personalized policies:
- gain vs Cash
- 95% CI

Do not use bars; point-range plot preferred.

---

## Fig. 6b — Allocation shares

Optional.

100% stacked bars for:
- policy tree
- ML argmax

Show:
- Cash share
- Food share
- Medical share.

If policy tree assigns 100% Cash, this may be stated in panel a annotation instead and panel b omitted.

### Purpose
Explain why “predictable HTE” does not translate to targeting gains.

---

## Extended Data / Supplement

- IPW versus cross-fitted DR policy value.
- repeated-seed personalized policy stability.
- policy-tree rules.

---

# 8. Extended Data figure cap and proposed allocation

Nature Human Behaviour allows at most 10 Extended Data display items.

Use them strategically.

Proposed:

1. ED Fig. 1 — nine-cell full outcome distributions
2. ED Fig. 2 — outcome-coding robustness
3. ED Fig. 3 — prediction model-family comparison
4. ED Fig. 4 — prediction outcome-representation robustness
5. ED Fig. 5 — latent factor diagnostics summary
6. ED Fig. 6 — cross-form recentered R² / calibration
7. ED Fig. 7 — coefficient similarity robustness
8. ED Fig. 8 — HTE learner comparison
9. ED Fig. 9 — repeated-seed HTE stability
10. ED Fig. 10 — response-quality screen robustness

Everything else:
- Supplementary Tables;
- Supplementary Figures only if journal format permits and useful.

---

# 9. Response-quality robustness figure

Because this is a major concern for a stated survey outcome, one Extended Data figure should be dedicated to it.

## ED Fig. 10

Four rows:
- Raw R
- Clean C
- Q1
- Q2

Columns:
1. Food−Cash average effect
2. Medical−Cash average effect
3. income moderation
4. medical-spending moderation

Point + 95% CI.

Display N for each screen.

This shows in one place:
- Medical results are more robust;
- Food is quality-sensitive;
- strict screens reduce N substantially.

Do not hide this asymmetry.

---

# 10. Figure legends

Every main figure legend should be written so the figure can be understood without the Results text.

Legend structure:

1. One-sentence descriptive title.
2. Panel-by-panel description.
3. Outcome definition.
4. Sample definition / exact N.
5. Statistical estimator.
6. What error bars represent.
7. Whether analysis is OOF / cross-fitted / bootstrap.
8. Any multiplicity correction if relevant.

Avoid discussing broad interpretation in the legend.

Example template:

“**Fig. 4 | Predictability of heterogeneous responses differs between food and medical transfers.** a,b, Observed randomized treatment contrasts across quintiles of out-of-fold predicted conditional treatment effects for Food versus Cash (a) and Medical versus Cash (b), estimated using a cross-fitted doubly robust learner. Points show within-quintile treatment contrasts in midpoint-coded stated MPC; error bars show 95% confidence intervals. c, Calibration and top-versus-bottom separation estimates for the two contrasts; difference estimates are obtained from [bootstrap/permutation procedure]. N=… for Food–Cash and N=… for Medical–Cash.”

Work must generate a draft legend file:
- `figures/nature_figure_legends.md`

---

# 11. Main-figure statistical discipline

## 11.1 No significance stars

Do not use:
- *
- **
- ***

Use:
- point estimates;
- CIs;
- exact p-values in text / caption only where necessary.

## 11.2 Same axes for direct comparisons

For:
- Food vs Medical CATE validation;
- form-specific predictability;
- amount-specific HTE;

use identical y-axis scaling across the compared panels.

## 11.3 Do not truncate zero when effect sign matters

Any treatment-effect / HTE contrast plot must visibly include zero.

Prediction R² panels may begin slightly below 0 if negative CV R² occurs.

## 11.4 Show uncertainty for nulls

Nulls are substantive results.

Never show a point estimate alone for:
- subjective incremental R²;
- Food HTE;
- personalization gain.

## 11.5 Avoid overplotting

Main figures should not contain:
- >8 line series;
- >20 regression coefficients;
- dozens of questionnaire items.

Those belong in supplement.

---

# 12. Accessibility and general-reader design

Avoid economics-only shorthand in figure titles.

Use:
- “Predicted spending response”
not:
- “MPC fitted value”

Use:
- “Transfer form”
not:
- “treatment arm” when possible.

Use:
- “Observed randomized contrast”
not:
- “CATE realization.”

Technical terminology can appear in captions and Methods.

---

# 13. File outputs Work must produce

For every main figure:

- `nature_fig1.pdf`
- `nature_fig1.png`
- ...
- `nature_fig6.pdf`
- `nature_fig6.png`

For Extended Data:
- `nature_ed_fig1.pdf/png`
- ...

Also save panel-level source tables:
- `tables/nature_fig1a_data.csv`
- `tables/nature_fig1b_data.csv`
- etc.

No figure may depend on numbers manually typed into plotting code if they already exist in analysis outputs.

All displayed statistics must be generated from source tables.

---

# 14. Required figure QC checklist

Before declaring figures final, Work must verify:

## Scientific
- every panel maps to one predeclared estimand;
- correct sample;
- exact N;
- correct CI type;
- same folds across direct ML comparisons;
- no in-sample prediction presented as OOS;
- no feature importance described causally.

## Visual
- readable at 183 mm or 89 mm target width;
- 5–7 pt text at final size;
- no clipped labels;
- white background;
- consistent Cash/Food/Medical colour mapping;
- distinguishable in greyscale;
- panel labels ordered alphabetically;
- minimal whitespace;
- no unnecessary legend duplication.

## Reproducibility
- PDF and PNG generated by script;
- panel source CSV saved;
- figure legend saved;
- random seed recorded;
- no respondent-level data exported.

---

# 15. Figure-level go/no-go logic

## Fig. 2 survives only if:
- ALL OOS predictability remains low;
- O+S gain remains <.01 with uncertainty supporting the null.

## Fig. 3 survives only if:
- cross-form portability is consistently low;
- Cash–Food vs Cash–Medical difference has some formal support;
- reliability sensitivity does not completely eliminate the interpretation.

If reliability sensitivity shows the apparent instability could easily be entirely explained by plausible measurement error, Fig. 3 must be reframed as:
“Observed cross-form portability is low”
rather than:
“Context reshapes individual differences.”

## Fig. 4 survives only if:
- Medical−Cash HTE validates OOF under ≥2 principled learners;
- Food−Cash does not;
- formal difference between Medical and Food predictability is nontrivial.

## Fig. 5 survives only if:
- amount-specific Medical result is stable across seeds / reasonable specifications;
- at least one transparent economic moderator remains robust.

## Fig. 6 survives regardless of sign if:
- policy evaluation is honest OOF;
- IPW and DR policy-value results broadly agree.

A well-estimated null is publishable evidence.

---

# 16. Desired visual narrative across pages

A reader who only looks at the six figures should understand:

### Fig. 1
Different forms of the same nominal transfer change stated spending.

### Fig. 2
Rich personal information barely predicts who responds strongly.

### Fig. 3
The little predictive signal that exists does not travel well across forms.

### Fig. 4
This context specificity is asymmetric: Medical is predictably heterogeneous; Food is not.

### Fig. 5
Medical heterogeneity is concentrated at particular stakes / economic contexts.

### Fig. 6
Even predictable heterogeneity does not make personalization better than uniform Cash.

If this six-figure story is not visible without reading regression tables, the visualization package is not ready for a Nature-series submission.
