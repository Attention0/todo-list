# NHB round-2 reviewer response work plan

## Purpose

This is a **targeted closure round** based on the latest manuscript comments. The scientific story is already fixed:

> Transfer form can shift average stated spending without generating a clearly identifiable set of responders or broadly remapping observable individual differences.

Do **not** reopen story search, add broad moderator scans, or return to the old “limited portability” headline. The objective is to close the remaining reviewer questions, sharpen the evidence, and prepare publication-quality main/Extended Data figures.

Primary inputs:
- current respondent-level survey data and questionnaire/codebook;
- the existing NHB reanalysis pipeline and results under `消费调查/results/nhb_reanalysis/`;
- the current manuscript and latest comments;
- `消费调查/NHB_REVIEW_REANALYSIS.md`;
- `消费调查/NHB_FINAL_VERIFICATION.md`.

Write new code and aggregate outputs to:

`消费调查/results/nhb_round2/`

Never commit raw respondent-level data, identifiers, fold-level predictions, or bootstrap draws containing respondent information.

---

# 1. Mean effects: finish primary-effect reporting

## 1.1 Full-sample and robustness contrasts

For Raw, Adult, Clean, Q1 and Q2 samples, report all three pooled form contrasts:
- Food − Cash
- Medical − Cash
- Medical − Food

For each:
- ordinal 1–6 outcome as primary;
- midpoint outcome as secondary;
- estimate, SE, 95% CI, exact two-sided P;
- Holm-adjusted P within the three pooled contrasts;
- standardized effect size for the ordinal outcome.

Create one compact table rather than many separate outputs.

## 1.2 Ordered-outcome robustness

Fit ordered logit and ordered probit models with:
- transfer form;
- amount fixed effects.

Report average marginal effects or a concise probability-scale summary for Food vs Cash and Medical vs Cash.

Do not replace the primary randomized mean contrasts with ordered-model coefficients; this is robustness only.

## 1.3 Response-category and amount diagnostics

Report:
- share selecting the lowest response category by form;
- the 9 form × amount cell means and 95% CIs;
- formal joint form × amount interaction test;
- exact Medical − Cash contrasts at RMB 200, 1,000 and 5,000.

Do not infer amount heterogeneity from separate significance levels.

---

# 2. Food voucher: close the bindingness and wording alternatives

## 2.1 Inframarginal versus potentially binding respondents

Using the existing pre-treatment spending-bound classification, estimate Food − Cash separately for:
- strictly inframarginal respondents;
- all remaining respondents who are not strictly inframarginal.

Then estimate a single interaction model testing:

Food × strictly-inframarginal

with amount fixed effects.

Report:
- N by subgroup and arm;
- ordinal primary estimate;
- midpoint sensitivity;
- interaction estimate and 95% CI.

The purpose is to test whether the Food effect is materially larger when the restriction can plausibly bind.

## 2.2 Bindingness categories

If sample sizes allow, retain the previous three-way classification:
- strict inframarginal;
- ambiguous;
- likely binding.

Report a joint interaction test, but do not over-interpret small cells.

## 2.3 Form-specific lowest-option wording sensitivity

The lowest response option had different explanatory wording across forms.

Run two prespecified sensitivity checks:
1. exclude respondents choosing category 1 and re-estimate Food − Cash / Medical − Cash among the remaining response categories;
2. alternatively collapse categories 1–2 and re-estimate an ordinal/binary robustness specification.

Label these analyses explicitly as **wording-sensitivity checks**, not causal corrections.

If conclusions change materially, report this clearly.

---

# 3. Is ~5% predictability a model/sample limitation or an information limit?

## 3.1 Model-family comparison

Using identical folds and the same feature set, compare held-out performance for:
- ridge;
- elastic net / lasso or a sparse penalized linear model;
- random forest;
- histogram gradient boosting or another already-supported tree booster.

Report:
- OOS R²;
- Spearman;
- RMSE;
- same five seeds/common folds.

Do not select a winner post hoc; the goal is to show whether low predictability is learner-specific.

## 3.2 Treatment-only baseline and incremental value

Fit a baseline model using only randomized form and amount.

Then report:
- treatment-only OOS R²;
- full-profile OOS R²;
- incremental OOS R² from adding baseline characteristics.

## 3.3 Theory-guided feature ablation

Use a small fixed set of broad feature blocks:
1. demographics / socioeconomic position;
2. household resources and liquidity;
3. needs / exposure (food and medical spending, household composition);
4. expectations;
5. subjective security / pressure;
6. broader social attitudes / wellbeing.

For each block, report:
- block-only OOS performance;
- leave-one-block-out change in OOS R² from the full profile.

This is predictive description only; do not call it mechanism importance.

## 3.4 Learning curve

Estimate held-out performance as training data increase, for example:
20%, 40%, 60%, 80%, 100% of the available training sample.

Use repeated subsampling inside the existing fold logic.

Plot:
- mean OOS R² versus training fraction;
- 95% empirical interval across repeated subsamples/seeds.

Interpretation:
- if the curve is still steep at 100%, say more data may help;
- if it is visibly flattening, say the current observable feature space appears to have limited incremental signal at this sample size.

Do **not** call the asymptote “irreducible human unpredictability”.

---

# 4. Portability/remapping: complete the benchmarked evidence

## 4.1 Full 3×3 matrices by amount

Produce fully OOS 3×3 portability matrices at:
- pooled sample;
- RMB 200;
- RMB 1,000;
- RMB 5,000.

Report Spearman primary; Pearson/R² can go to supplement.

## 4.2 Refit-bootstrap uncertainty for all six cross-form directions

Extend the respondent-level model-refit bootstrap to all six off-diagonal directions:
- Cash→Food
- Cash→Medical
- Food→Cash
- Food→Medical
- Medical→Cash
- Medical→Food

Each gap must be target-normalized against the target-native OOF model.

Use at least B=1,000 draws, stratified by randomized amount, refitting both source and target models each draw.

Return:
- point estimate;
- percentile 95% interval;
- no significance-star storytelling.

## 4.3 Equal-training-size pooled-vs-form-specific comparison

The current separate-form forests use roughly one-third of the observations.

Add a fair comparison:
- pooled/common RF trained on a random subset matched to the form-specific training N;
- form-specific RF trained on its own arm;
- repeated matched subsamples.

This addresses the concern that form-specific models underperform only because they have less training data.

## 4.4 Direct score × form estimates

For the held-out person-score invariance test, report directly:
- score × Food coefficient + CI;
- score × Medical coefficient + CI;
- joint test;

for both:
- midpoint outcome;
- ordinal outcome.

Keep the interpretation bounded to **observable remapping**.

---

# 5. HTE: show each contrast directly and quantify what the design could detect

## 5.1 Separate Food−Cash and Medical−Cash validation

For each contrast and each main sample:
- BLP calibration slope + 95% CI;
- top-minus-bottom GATES + 95% CI;
- same axes/scales across Food and Medical.

Do not show only “Medical minus Food”.

Also retain the direct Medical-minus-Food difference as the formal asymmetry test.

## 5.2 HTE detectability / simulation

Run a transparent simulation calibrated to:
- actual sample sizes;
- treatment probabilities;
- observed outcome variance/noise;
- existing baseline X structure where feasible.

Inject synthetic CATE heterogeneity of increasing SD and pass it through the same cross-fitting / validation pipeline.

Estimate the approximate CATE SD needed for:
- 50% detection probability;
- 80% detection probability;

for Food−Cash and Medical−Cash.

The purpose is to show what the null Food HTE result rules out.

Do not convert this into a post hoc “power proves no heterogeneity” claim.

---

# 6. Medical account: test the boundary-condition explanation

Medical-account evidence is secondary but potentially informative. Keep analyses theory-driven.

## 6.1 Medical spending and effective bindingness

Using past-year out-of-pocket medical spending:
- report its distribution by bands;
- for each transfer amount, report the share whose past-year medical spending lower bound exceeds the transfer;
- because the medical account does not have the same six-month horizon as the food voucher, label this as a **medical-exposure / plausibly inframarginal proxy**, not a strict budget-set test.

Estimate Medical − Cash by:
- medical-spending band;
- coarse low / medium / high spending groups;
- proxy-inframarginal versus other respondents.

Test the Medical × spending interaction jointly.

## 6.2 Floor-effect sensitivity

Medical accounts have more category-1 responses.

Check whether apparent Medical HTE is driven by the floor:
- ordered probit/logit interaction specification;
- binary probability of category 1;
- repeat HTE validation after a reasonable alternative outcome representation, if methodologically defensible.

Do not discard category 1 from the main analysis.

## 6.3 Interpretation gate

Only strengthen the “medical restriction bites differently across people” interpretation if:
- medical-spending moderation is directional and reasonably stable;
- the HTE signal survives at least one floor-sensitive robustness check.

Otherwise keep Medical as a specification-sensitive boundary condition.

---

# 7. Main-figure redesign for an NHB/Nature-style visual story

Do not make the main figures look like a methods appendix.

Use one consistent Cash / Food / Medical colour mapping across the entire paper.

Each main figure should communicate **one scientific proposition**, with the statistical machinery moved into the legend or Extended Data.

## Figure 1 — Same money, different form, different average response

Show:
- randomized form × amount means with 95% CIs;
- full outcome distribution in a secondary panel;
- design schematic only as a small inset or compact panel.

Do not let the 3×3 design matrix dominate the figure.

Use a non-misleading y-axis and make the full 1–6 scale visually recoverable.

## Figure 2 — Economic non-bindingness does not restore cash equivalence

Primary visual:
- Food − Cash effect by bindingness class;
- zero line is the economic-equivalence benchmark;
- show strict-inframarginal effect prominently;
- add the interaction/bindingness comparison from this round.

If clear, add a compact wording-sensitivity panel.

This should visually answer a theory question, not just display a robustness test.

## Figure 3 — Rich profiles predict little of who responds

Primary visual:
- model-family OOS R² comparison;
- learning curve;
- optional compact feature-block incremental-information panel.

Avoid a figure whose only content is five CV seed dots.

The visual question is:
> How much can we know about individual response from a rich profile, and does more data/model flexibility change that answer?

## Figure 4 — Mean effects need not imply targetable responders

Use identical axes for Food−Cash and Medical−Cash:
- CATE quintile/GATES plot or calibration plot for Food;
- same plot for Medical;
- formal Medical−Food difference in a small third panel.

This is preferable to showing only a Medical-minus-Food difference.

## Portability/remapping

Keep the 3×3 portability matrix as either:
- a compact panel in Fig. 3/4; or
- Extended Data if the main story is already clear from the targeting/HTE evidence.

If retained in main text, accompany it with target-normalized gaps and describe the scientific question in plain language:
> Does a profile learned in one resource form rank people differently in another?

---

# 8. Supplementary/reporting items to prepare from available data

Where the source data permit, prepare:
- sample characteristics table (sex, age, education, city tier, income, hukou, employment);
- exact 9-cell Ns;
- balance diagnostics;
- full predictor dictionary;
- full model settings and software/package versions;
- all sample-definition Ns.

Do not invent:
- ethics approval;
- recruitment quotas;
- incentive amount;
- completion rate;
- provider data-sharing terms;
- survey duration;
- code DOI;
- funder information.

Leave explicit author-information placeholders where these are unavailable.

---

# 9. Required outputs

Create:

- `消费调查/results/nhb_round2/ROUND2_RESULTS.md`
- `消费调查/results/nhb_round2/ROUND2_AUDIT.md`
- `消费调查/results/nhb_round2/ROUND2_MANUSCRIPT_NOTES.md`

Tables should include at minimum:
- mean-effect robustness;
- ordered-model robustness;
- bindingness interaction;
- model-family prediction;
- treatment-only vs full incremental prediction;
- feature-block ablation;
- learning-curve estimates;
- six-direction portability bootstrap;
- equal-N pooled-vs-form-specific comparison;
- held-out score × form tests;
- separate Food/Medical BLP and GATES;
- HTE simulation/detectability;
- medical-spending/bindingness analysis;
- floor-effect sensitivity.

Figures:
- `fig_round2_mean_effects.*`
- `fig_round2_food_equivalence.*`
- `fig_round2_predictability.*`
- `fig_round2_hte.*`
- optional `fig_round2_portability.*`

Each figure must have a panel-source CSV.

---

# 10. Stopping rule

After this package, stop further exploratory analysis.

The end of `ROUND2_RESULTS.md` must answer only:

1. Is the Food−Cash effect materially different between strictly inframarginal and potentially binding respondents?
2. Does low individual predictability persist across learner families and show a flattening learning curve?
3. Is there robust evidence of observable remapping after target-native benchmarking and equal-N comparisons?
4. Does the design have enough sensitivity to rule out substantively large Food−Cash CATE heterogeneity?
5. Does prior medical spending explain the Medical boundary signal, and does it survive floor-sensitive outcome checks?
6. Should the current manuscript headline be strengthened, unchanged, or weakened?

No new story should be invented after seeing these results.
