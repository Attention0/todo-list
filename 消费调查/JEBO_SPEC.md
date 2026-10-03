# JEBO research specification — MPC size dependence × transfer form

## 0. Project status and purpose

This specification replaces the previous Nature Human Behaviour / Nature Communications positioning as the **current target-specific research framing** for the consumption-survey project. It does **not** erase or invalidate earlier work. All prior empirical work remains part of the audit trail.

The current target outlet is:

**Journal of Economic Behavior & Organization (JEBO)**

The intended paper is a behavioral-economics paper about the interaction between two classic margins:

1. **the size dependence of the marginal propensity to consume (MPC)**; and
2. **the fungibility / earmarking / spendability of the resource received.**

The central question is:

> **Does the well-known decline of MPC with transfer size depend on the form in which resources are provided?**

The proposed paper should be written around the randomized 3×3 form-by-amount experiment, not around prediction, machine learning, HTE discovery, person–context decomposition, or a Nature-style claim about general human behavior.

The paper should aim to be a **clean JEBO behavioral paper with one main puzzle**, not a broad methods paper.

---

## 1. Empirical lineage that must be treated as frozen background

The JEBO project must start from the latest complete stacked branch:

- PR #9: MPC size-curve discovery and distribution anatomy
- PR #10: bounded size-curve strengthening
- PR #11: who-drives / theory-variable moderation
- PR #12: all-X screen
- PR #13: Nature-style figure package
- PR #14: Hero response-atlas figure
- PR #15: NC revision evidence audit
- PR #16: finite-family reanalysis and NC v5 manuscript

The working base should be **PR #16 / branch `feature/nc-evidence-revision`**, which already stacks on the prior analysis and figure lineage.

Do not merge the old PR chain merely to perform the JEBO work. Do not overwrite historical outputs.

The NC v5 manuscript is a **source document**, not the template to preserve. It should be mined for correct design descriptions, estimates, limitations, and references, but the JEBO paper should be reorganized from scratch.

---

## 2. Current empirical facts that should organize the JEBO paper

Primary adult sample: approximately **N = 5,480**.

Randomized design:

### Transfer form
1. Cash
2. Food / daily-consumption voucher, non-cashable and valid for six months
3. Medical personal-account credit, restricted to medical-related spending and long-lived

### Transfer amount
1. RMB 200
2. RMB 1,000
3. RMB 5,000

Each respondent sees exactly one of the nine cells.

### Core descriptive pattern

Approximate midpoint-coded stated MPC cell means:

| Form | RMB 200 | RMB 1,000 | RMB 5,000 |
|---|---:|---:|---:|
| Cash | 0.253 | 0.227 | 0.201 |
| Food | 0.228 | 0.201 | 0.195 |
| Medical | 0.177 | 0.179 | 0.179 |

The adult-sample trend estimates already established in PR #16 are approximately:

- Cash midpoint slope per fivefold increase: **−2.57 pp**
- Food midpoint slope: **−1.61 pp**
- Medical midpoint slope: approximately **0**
- Cash ordinal slope: clearly negative
- Medical ordinal slope: approximately flat

The high-spending response category (>75%) shows:

- Cash: approximately **13.4% → 9.0% → 5.3%**
- Food: approximately **9.8% → 6.9% → 7.5%**
- Medical: approximately **6.0% → 5.2% → 3.9%**

The cash “essentially no additional spending” share is nearly unchanged across size, approximately 27–29%.

This motivates the distributional description:

> The decline in stated cash MPC is most visibly associated with compression of high-spending responses rather than a growing mass of respondents who report no additional spending.

This is a descriptive statement. Existing direct cross-threshold tests do **not** establish a uniquely tail-specific causal mechanism.

### Inference boundary

PR #16 is the authoritative evidence audit for the form-by-size interaction.

For adult Top75:

- form-by-size omnibus raw P ≈ .009
- Holm across the 21-test scientific family ≈ .181
- joint min-P ≈ .082

For the Cash–Medical slope difference:

- raw P ≈ .0038
- Holm ≈ .079
- joint min-P ≈ .039

Therefore the JEBO manuscript must distinguish:

**Strong / relatively secure evidence**
- randomized form level effects;
- randomized amount effects;
- declining Cash size gradient;
- distributional shape visible in raw cells.

**Suggestive / less secure evidence**
- cross-form differences in amount slopes;
- the claim that the Cash curve is statistically different from each restricted-form curve after broad multiplicity adjustment.

The manuscript must never convert the current evidence into:
- “we prove that Medical is flat”;
- “we establish a universal form×size interaction”;
- “we identify mental accounting as the mechanism.”

---

## 3. Proposed JEBO contribution

The paper should be positioned around the idea that **fungibility and transfer scale need not be separable behavioral margins**.

Preferred high-level contribution:

> A classic regularity in consumption behavior—the dependence of spending propensity on windfall size—appears to vary with the form in which the resource is provided. Small cash transfers generate the highest stated spending propensities, while the cash MPC declines as transfer size rises; earmarked resources start at lower spending propensities and show much weaker size gradients. Thus transfer design may shape not only the level of spending propensity but also how that propensity scales with the amount received.

This framing is stronger than a generic “cash vs voucher” paper but narrower and more defensible than the previous Nature-style person–context claim.

A useful secondary puzzle is:

> **Why is the Cash–restricted gap largest for small transfers rather than large transfers?**

A simple mechanical-binding intuition could predict the opposite if restrictions become more consequential as the transfer grows. The observed convergence therefore creates a behavioral puzzle, but the paper must not claim that mechanical restrictions are ruled out: PR #16 specifically shows that the Food bindingness diagnostics do not support such an exclusion.

---

## 4. Literature architecture

The JEBO paper should engage with five literatures.

### A. MPC and windfall-size dependence

Core questions:
- Is MPC lower for larger windfalls?
- Does transfer size operate on the extensive margin, intensive margin, planning horizon, or response distribution?
- How do survey-based stated MPCs compare with realized consumption responses?

Priority references to audit and expand:
- Friedman / permanent-income discussions of small vs large windfalls
- Jappelli & Pistaferri surveys and stated-MPC work
- Fuster, Kaplan & Zafar, *Review of Economic Studies* (2021), “What Would You Do with $500?”
- Kaplan & Violante, *Annual Review of Economics* (2022), MPC review
- MPC meta-analysis evidence that estimated MPCs decline with payment size
- Korean transfer / stimulus evidence with declining MPC by transfer size
- Jappelli, Savoia & Sciacchetano, “Intertemporal MPC and shock size,” *European Economic Review* (2026)
- recent finite-planning-horizon / bounded-rationality windfall paper in *Journal of Financial Economics* (2026)

Important comparison:
Fuster–Kaplan–Zafar emphasize a **positive extensive-margin size effect** in hypothetical windfalls while conditional spending responses can fall with size. Our data appear different: the Cash no-spending share is roughly flat, while the high-MPC tail compresses. This difference is potentially important and should be investigated carefully.

### B. Mental accounting, fungibility, and small windfalls

Priority themes:
- small windfalls as narrowly framed “spendable” resources;
- money source / account labels;
- category budgets and nonfungibility;
- why economically equivalent resources may produce different spending responses.

Priority references:
- Thaler / Shefrin / mental accounting foundations
- Thaler (1999)
- “Mental accounting and small windfalls: Evidence from an online grocer” (JEBO)
- Hastings & Shapiro (QJE 2013; AER 2018)
- Abeler & Marklein (JEEA 2017)
- related household-finance / earmarking work

### C. Transfer form, restrictions, earmarking, and expiration

Priority themes:
- cash vs in-kind / restricted transfers;
- spending from earmarked benefits;
- expiry / commitment;
- form-specific “spendability.”

Priority reference:
- Boehm, Fize & Jaravel, *American Economic Review* (2025), “Five Facts about MPCs,” including the much higher MPC on an expiring card than on a cash-like transfer.

The JEBO paper must be explicit that our Food and Medical treatments **bundle several attributes**:
- permitted use,
- liquidity,
- expiry / horizon,
- salience / label,
- perhaps perceived commitment.

Therefore “form” is the randomized treatment; “mental accounting” or “restriction” is an interpretation, not separately identified.

### D. Payment form, framing, and social meaning of money

Priority references:
- Lee, Morduch, Ravindran & Shonchoy, JEBO (2024), “The social meaning of mobile money”
- JEBO (2025), “Temporal framing of tax stimuli and household consumption”
- payment-effect and digital-money literature
- source-of-funds and labeling literature

This literature is useful because JEBO accepts papers in which a simple framing / payment manipulation reveals a behavioral boundary condition, even when the mechanism is supported rather than structurally identified.

### E. Validity and limitations of stated MPC

The paper must treat hypothetical elicitation as a real measurement approach with known strengths and limitations, not as equivalent to realized spending.

Priority topics:
- stated vs realized / revealed MPC evidence;
- hypothetical bias;
- external validity;
- response bins and anchoring;
- the value of randomized scenario variation even when the outcome is stated.

Recent evidence comparing stated, realized and revealed MPC measures should be reviewed and clearly separated from established peer-reviewed evidence if still working-paper status.

---

## 5. JEBO outlet benchmark

Work should inspect recent JEBO papers from roughly 2023–2026 in nearby areas:
- survey experiments;
- household consumption;
- mental accounting;
- framing;
- payment form;
- fungibility;
- behavioral household finance.

The goal is not to imitate one article mechanically. Produce an outlet benchmark covering:
- typical paper length;
- number and role of main figures/tables;
- how papers state behavioral mechanisms;
- how much theory is expected;
- how hypothetical outcomes are defended;
- how limitations are written;
- how much robustness is kept in the main text versus appendix.

The current project already has visually polished figures. Do **not** redesign them merely for cosmetic novelty.

---

## 6. New empirical work allowed for the JEBO transition

The prior project correctly stopped unrestricted exploration. The JEBO transition authorizes only a **small, theory-driven, literature-motivated finite set** of new analyses.

Before running any new respondent-level analysis, Work must create and commit a frozen `JEBO_ANALYSIS_MANIFEST.md` listing the exact new estimands and outputs. This is a post hoc target-transition protocol, not preregistration.

### Allowed new analysis 1: extensive–intensive decomposition of the Cash size effect

Motivation:
The size-effect literature, especially Fuster–Kaplan–Zafar, emphasizes whether larger windfalls change:
- the probability of spending anything; and/or
- the amount/share spent conditional on responding.

Our existing figures show that Cash’s no-spending share is nearly flat while the high-spending tail shrinks.

Required decomposition for Cash, Food and Medical:

1. (p_a = P(	ext{any additional spending}|a))
2. midpoint-coded (E[MPC|any,a]), descriptive only
3. unconditional (E[MPC|a] = p_a E[MPC|any,a])
4. decompose the RMB 200 → RMB 5,000 change in unconditional midpoint MPC into:
   - extensive-margin contribution;
   - intensive-margin contribution;
   - use a symmetric / Shapley decomposition so the cross-term is not assigned arbitrarily.

Important:
- conditioning on “any spending” is post-treatment; the conditional mean is **descriptive**, not a causal estimand.
- the decomposition is an accounting identity, not mechanism identification.
- use stratified bootstrap only if uncertainty is genuinely useful; do not create a new significance contest.
- report full values for all three forms, not only Cash.

Decision value:
If Cash’s decline is overwhelmingly intensive/high-tail while the extensive margin is flat, this creates a direct and useful comparison with prior size-effect evidence.

### Allowed new analysis 2: literature-matched distribution comparison

Using only already defined categories and thresholds, prepare a compact comparison of our Cash size response to the empirical patterns reported in the windfall-size literature.

Do not fit new arbitrary thresholds.

At minimum compare:
- (P(any))
- midpoint mean
- Top75
- conditional midpoint among positive responders, descriptive

The output should be a **literature benchmark table**, not a claim that different surveys estimate the same population parameter.

### Allowed new analysis 3: simple behavioral-prediction table, not a structural estimation

Construct a conceptual prediction table with columns such as:

- standard concave consumption / PIH-style size effect;
- liquidity / hand-to-mouth;
- small-windfall mental accounting;
- finite planning horizon / attention;
- mechanical restriction / bindingness;
- earmarking / commitment.

Rows should include qualitative predictions for:
- Cash MPC level;
- Cash size gradient;
- restricted-form level;
- whether Cash–restricted gap should widen or shrink with size;
- extensive vs intensive margin;
- what current data do / do not observe.

This is a conceptual synthesis. Do not estimate a structural model unless separately authorized later.

### Not authorized

Do NOT run:
- new unrestricted moderator searches;
- additional all-X screens;
- SHAP / RF feature ranking;
- new HTE discovery;
- clustering / latent classes;
- new response-quality thresholds;
- new outcome cutoffs;
- data-driven sample selection;
- repeated alternative multiplicity families aimed at rescuing significance;
- new “medical need” or “food need” searches beyond the already frozen diagnostics;
- specification mining;
- Bayesian rescue analysis;
- any new psychological scale built post hoc.

If the bounded decomposition fails to improve the story, report that and stop.

---

## 7. Main outcome hierarchy for JEBO

The paper should not let one arbitrary midpoint coding carry the scientific claim.

Recommended hierarchy:

### Layer 1 — raw randomized response distribution
The six original ordered response categories are the most design-faithful object.

### Layer 2 — ordinal trend
Use the original ordinal 1–6 score / ordered model as the primary coding-robust representation.

### Layer 3 — midpoint-coded MPC
Use midpoint MPC for economic interpretability and comparison with the MPC literature.

### Layer 4 — pre-existing threshold anatomy
Use:
- any additional spending;
- Top75;
- other thresholds in supplement.

Top75 is useful because the effect is visually strongest there, but the manuscript must state that direct tests did not establish exclusive tail specificity.

---

## 8. Proposed JEBO manuscript architecture

The JEBO manuscript should be newly structured as follows.

### Title candidates

Preferred:
**Transfer form and the size dependence of the marginal propensity to consume**

Alternatives:
- **When does MPC decline with transfer size? Evidence from cash and earmarked transfers**
- **Fungibility and the size dependence of spending**
- **Transfer design and the size dependence of stated consumption**

Do not oversell “mental accounting” in the title unless the literature audit and final evidence justify it.

### Abstract
Approximately 150–220 words.

Must include:
- research question;
- randomized 3×3 design;
- sample size;
- core Cash / Food / Medical pattern;
- distributional anatomy;
- transparent statement that cross-form slope differences are less precise under joint multiplicity correction;
- contribution to size-dependent MPC and fungibility literatures.

Do not include:
- ML;
- all-X screen;
- HTE;
- calibration details;
- giant robustness lists.

### 1. Introduction

Target approximately 1,500–2,000 words.

Suggested five-part flow:

1. **Classic fact / question**  
   Small and large windfalls can generate different MPCs. Most evidence studies size while holding the form of resources implicitly fixed.

2. **Missing margin**  
   A separate literature shows that money is not always fungible: labels, restrictions, payment form and earmarking change spending. The missing question is whether these two margins are separable.

3. **Design and headline pattern**  
   Introduce the 3×3 randomized experiment and the raw cell pattern.

4. **Behavioral anatomy**  
   Cash’s decline appears in the compression of high-spending responses rather than an increase in zero-spending responses.

5. **Contribution and evidence boundary**  
   Connect to the five literature streams; state clearly that form-specific slope differences are suggestive after joint correction and that mechanisms are not uniquely identified.

### 2. Related literature and behavioral motivation

Keep concise.

Organize around:
- size-dependent MPC;
- fungibility / mental accounts / transfer form;
- why their interaction is conceptually nontrivial.

A light conceptual framework is welcome, but avoid a model whose parameters cannot be identified.

### 3. Experimental design, sample and measurement

Include:
- exact form descriptions;
- exact amount randomization;
- sample construction;
- six response bins;
- adult-primary sample;
- randomization balance summary;
- stated/hypothetical nature;
- bundled treatment attributes.

Use NC v5 for verified factual details, but remove Nature-style submission/process discussion from the main scientific narrative.

### 4. Transfer size and stated MPC

Start from raw 3×3 cells.

Show:
- raw distributions;
- ordinal means;
- midpoint means;
- within-form amount slopes.

This section should establish the Cash size gradient before making the cross-form comparison.

### 5. Does the size gradient depend on transfer form?

Show:
- Food and Medical curves;
- Cash–Food and Cash–Medical slope differences;
- point estimates and uncertainty;
- the finite-family inference boundary.

The correct prose is:
- “the observed Cash decline is steeper”;
- “the pattern is consistent across several representations”;
- “formal cross-form inference is weaker after multiplicity correction.”

Do not write “Medical MPC is invariant to size” as a population fact.

### 6. Where in the response distribution does the Cash decline occur?

Use:
- Hero response atlas;
- any-spending;
- Top75;
- new extensive–intensive descriptive decomposition.

This is likely the most behaviorally distinctive section.

### 7. Interpretation and alternative explanations

Keep compact.

Discuss:
- small-windfall mental accounting;
- planning / attention;
- relative scale;
- mechanical restrictions;
- food inframarginality;
- bundled form attributes.

Reuse prior diagnostics; do not create a mechanism zoo.

The conclusion should be:
> current evidence narrows some explanations but does not identify a unique mechanism.

### 8. Discussion

Discuss:
- why form and size may be jointly behaviorally relevant;
- relation to stimulus design;
- relation to in-kind / earmarked transfers;
- stated versus realized behavior;
- generalizability.

### 9. Conclusion

Short.

Return to:
> MPC-size dependence is not obviously invariant to the form of the transfer.

---

## 9. Main figures and tables

Existing graphics are already strong.

### Figure 1 — preferred opening
Reuse PR #14 Hero Figure:
- full 3×3 six-bin response atlas;
- midpoint summary curve.

Do not redraw unless needed for JEBO typography/caption formatting.

### Figure 2 — form-specific size curves
Reuse / adapt approved PR #13 / #16 source data:
- ordinal;
- midpoint;
- optionally Top75 in one multi-panel figure.

### Figure 3 — distribution anatomy
Prefer:
- Panel A: any additional spending;
- Panel B: Top75;
- optional Panel C: new extensive–intensive decomposition if visually clean.

No more than three main figures unless the literature/outlet benchmark strongly suggests otherwise.

### Main tables

Suggested:
1. Design / randomized cell counts and basic treatment definitions.
2. Main form-specific size slopes and cross-form differences.
3. Optional compact decomposition / robustness table.

Move to supplement:
- 420-specification grid;
- all-X screen;
- quality-sample details;
- population calibration;
- relative-scale diagnostics;
- ordered location-scale sensitivity;
- full mechanism diagnostics.

---

## 10. What should be removed from the NC-style main narrative

The JEBO main text should not be dominated by:
- 21-test correction mechanics;
- old 1,500-test-family history;
- max-norm vs min-P calibration details;
- all-X null screens;
- census raking;
- response-quality audit engineering;
- metadata audit;
- reproducibility implementation;
- model-verification process.

These remain important in appendices / audit files but are not the behavioral story.

The JEBO paper should read as:
**question → experiment → raw behavioral fact → distributional anatomy → interpretation → limits.**

---

## 11. Claim discipline

### Claims that are acceptable

- Cash stated MPC declines with transfer size in the randomized cells.
- Food shows a weaker decline; Medical is much flatter descriptively.
- The Cash high-spending tail visibly contracts with transfer size.
- The no-spending share is relatively stable for Cash.
- The gap between Cash and restricted resources is largest at small amounts in the observed data.
- Form-by-size differences are suggestive and directionally stable across several representations.
- Transfer form may shape the size dependence of spending propensity.
- The pattern is consistent with behavioral accounts involving mental accounting, spendability, planning or restrictions.

### Claims that are not acceptable

- Medical MPC is proven invariant to amount.
- Food and Medical are equivalent.
- The effect is proven tail-specific.
- Mental accounting is identified.
- Restrictions are ruled out.
- Respondents actually spend these amounts.
- The results estimate realized MPC.
- The sample is nationally representative.
- The paper establishes a general law of human behavior.
- Observables “do not matter” in an equivalence sense.
- The post hoc JEBO finite analysis is preregistered.

---

## 12. Final decision rule

The JEBO rewrite is worth completing if the literature audit supports the following novelty:

> Existing MPC work studies size dependence, and existing fungibility work studies form / labels / restrictions, but there is limited direct evidence on whether the **shape of the MPC–size relationship itself changes across transfer forms**.

If prior papers already cleanly establish this exact result with comparable randomized design, Work must say so and reposition rather than hide it.

The bounded new decomposition should strengthen the paper if it shows a distinct margin pattern relative to prior windfall-size work. If it does not, the paper should still rely on the raw 3×3 behavioral fact rather than invent a new mechanism.

The final target is a **clear, credible JEBO manuscript**, not maximum apparent novelty at the cost of evidential discipline.
