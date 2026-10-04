# JEBO v4 Writing Specification — three puzzles, distributional anatomy, disciplined mechanisms

## 0. Purpose

This document governs a new JEBO manuscript rewrite built on the completed scientific work in PR #19.

**Scientific source of truth:** PR #19, branch `feature/jebo-review-revision`, head `363313c8adc52cce252c11390a32e46c7a98d25f`.

The new manuscript must **retain PR19's statistical corrections, estimand repairs, measurement boundaries, reference audits, and mechanism-precision results**, but it should no longer read like a reviewer-response memo. The paper needs a stronger economic narrative.

The writing goal is:

> **v2's narrative energy + PR19's scientific discipline.**

Do not strengthen any claim by changing the analysis. Strengthen the paper by choosing the right empirical facts, ordering them well, explaining why they are puzzling, and making the logic cumulative.

No new exploratory analysis is authorized by this writing specification. If a desired sentence would require a new statistical test that PR19 does not contain, write it as a descriptive fact from the randomized cells or omit the inferential claim.

---

# 1. Central paper idea

The paper should revolve around one visually obvious 3×3 pattern:

- **Cash:** stated spending share declines clearly with transfer size.
- **Food:** stated spending share declines, but less.
- **Medical:** stated spending share is almost flat.
- **Across forms:** the three mean shares are farthest apart at RMB 200 and much closer at RMB 5,000.

Adult midpoint-coded means from PR19:

| Form | RMB 200 | RMB 1,000 | RMB 5,000 |
|---|---:|---:|---:|
| Cash | 25.30% | 22.67% | 20.16% |
| Food | 22.70% | 19.98% | 19.49% |
| Medical | 17.73% | 17.83% | 17.84% |

This pattern should be presented as **three connected puzzles**.

## Puzzle 1 — Medical flatness

A declining finite-windfall spending share is compatible with standard consumption smoothing, concavity, liquidity constraints, and familiar empirical evidence. Cash therefore supplies a useful benchmark.

What is unusual is that Medical is almost exactly flat in the observed mean cells.

The manuscript should ask:

> Why does the usual size dependence visible in Cash almost disappear for Medical?

Do **not** say classical theory universally predicts a decline. Say a decline is consistent with standard theory and common empirical patterns, making Medical's flatness notable.

## Puzzle 2 — Food does not fall faster than Cash

A simple increasing-bindingness intuition says that a category-restricted voucher may become harder to absorb as the amount rises. Under that sharp version, Food might be expected to decline at least as fast as, or faster than, Cash.

The observed Food mean declines less than Cash.

PR19 further shows that the historical Food bindingness proxy goes in the opposite direction from the sharp simple prediction.

The manuscript should ask:

> Why does a restricted Food resource not show a steeper size decline than unrestricted Cash?

## Puzzle 3 — Cross-form convergence

At RMB 200:
- Cash 25.3
- Food 22.7
- Medical 17.7

At RMB 5,000:
- Cash 20.2
- Food 19.5
- Medical 17.8

The Cash–Medical gap shrinks from about 7.6pp to about 2.3pp; Cash–Food shrinks to below 1pp in the observed means.

The paper should ask:

> Why does transfer form matter much more at small amounts than at large amounts?

This is the broadest puzzle and should organize the paper.

### Inferential boundary

The randomized **cell means and their observed convergence are facts about this experiment**. A general population form×size interaction is more demanding and remains uncertain under PR19's 42-test correction.

The manuscript should therefore distinguish:

- **descriptive 3×3 pattern:** clear and central;
- **formal general interaction claim:** suggestive / uncertain.

Do not let the second erase the first. Do not let the first be written as if it proves the second.

---

# 2. The paper's first major empirical contribution: anatomy of the three puzzles

The paper should not jump from mean curves directly to mechanisms.

Before theory or mechanism tests, use the full six-bin distributions to ask:

> What probability movements generate Cash's decline, Food's weaker decline, Medical's flat mean, and the observed convergence?

This section should be empirical and intuitive.

## 2.1 First clarify the scale: this is a percentage-share puzzle, not a yuan-collapse puzzle

Use PR19's share/yuan results:

### Cash
- midpoint share: 25.30% → 22.67% → 20.16%
- implied yuan: 50.60 → 226.69 → 1,008.19
- incremental midpoint-implied response:
  - 200→1,000: 0.220 [0.193, 0.248]
  - 1,000→5,000: 0.195 [0.170, 0.220]
- endpoint elasticity: 0.930 [0.887, 0.971]

### Food
- implied-yuan increments: 0.193 and 0.194
- endpoint elasticity: 0.953

### Medical
- implied-yuan increments: 0.179 and 0.178
- endpoint elasticity: 1.002

The key interpretation:

> The puzzle concerns how the **share of the transfer allocated to additional spending** changes across form and size. Absolute implied spending continues to rise strongly.

Do not describe a 20-fold increase in yuan as a separate behavioral discovery; it is partly arithmetic. Use it to define the scale of the puzzle correctly.

The affine model belongs here only as a compact descriptive aid:
[
Y approx a_f+b_f T.
]

PR19:
- midpoint slopes: Cash .198, Food .194, Medical .178;
- common-slope restriction p=.381;
- form-intercept/common-slope benchmark fits the midpoint cell means reasonably but does not prove equal slopes;
- interval-censored parameters are residual-scale-sensitive and cannot be structural MPCs.

Use this to say:

> Much of the visible cross-form divergence is concentrated at the small-transfer end, while incremental yuan responses are descriptively closer at larger amounts.

Do not write "the forms have equal marginal MPCs."

---

## 2.2 Cash anatomy — what produces the decline?

Adult raw shares, RMB 200 → 5,000:

- bottom: 27.35% → 27.41%
- <10%: 17.96% → 20.17%
- 10–25%: 20.39% → 24.48%
- 25–50%: 15.86% → 15.69%
- 50–75%: 5.02% → 6.90%
- >75%: 13.43% → 5.34%

Main interpretation:

> Cash's mean decline is most visibly associated with a sharp compression of the very highest spending-share responses, while the bottom-category share is almost unchanged.

Use "most visibly" or equivalent. Do not claim formal tail-specificity, because earlier direct threshold-difference tests did not establish that stronger statement.

The PR19 decomposition may be used, with corrected terminology:
- total endpoint midpoint change: −5.14pp
- bottom-category component: −0.02pp
- conditional-above-bottom component: −5.11pp

State clearly that this is a coding identity, not an extensive/intensive causal decomposition.

The narrative insight is:

> Cash does not fall because the observed distribution piles into the bottom response category; it falls because very high spending-share responses become much less common and mass shifts toward lower/middle shares.

---

## 2.3 Food anatomy — why is the decline weaker?

Adult raw shares, RMB 200 → 5,000:

- bottom: 31.16% → 30.05%
- <10%: 17.29% → 21.70%
- 10–25%: 19.90% → 23.87%
- 25–50%: 15.50% → 11.52%
- 50–75%: 6.36% → 5.34%
- >75%: 9.79% → 7.51%

Key idea:

> Food reaches a lower mean through a different redistribution path from Cash.

Cash has a dramatic top-bin compression. Food shows a more diffuse reallocation from middle-high and high categories toward low/middle categories, while its bottom category does not rise.

Do not write "Food is just a weaker Cash version." Emphasize different distributional paths.

This is an empirical answer to part of Puzzle 2 before invoking any theory.

---

## 2.4 Medical anatomy — a flat mean with a moving distribution

This must be one of the paper's most memorable facts.

Adult raw shares, RMB 200 → 5,000:

- bottom: 38.60% → 35.49%
- <10%: 18.40% → 16.72%
- 10–25%: 18.57% → 23.50%
- 25–50%: 12.87% → 13.09%
- 50–75%: 5.54% → 7.26%
- >75%: 6.03% → 3.94%

Mean midpoint:
- 17.73% → 17.84%

Core sentence:

> **Medical's flat mean is not a static distribution. It is the net result of offsetting movements across response categories.**

This is stronger and more interesting than simply saying Medical is flat.

Important inferential rule:
- PR19 provides the raw randomized distributions.
- Unless PR19 already contains a formal full-distribution test, describe these changes as observed cell movements.
- Do not say "the Medical distribution changes significantly" without a pre-existing test.

This observation should answer part of Puzzle 1:
- Medical is not obviously "unresponsive to amount";
- instead, amount changes different parts of the response distribution in offsetting directions.

---

## 2.5 Convergence in means does not imply distributional identity

At RMB 5,000:

| Bin | Cash | Food | Medical |
|---|---:|---:|---:|
| bottom | 27.4% | 30.1% | 35.5% |
| <10% | 20.2% | 21.7% | 16.7% |
| 10–25% | 24.5% | 23.9% | 23.5% |
| 25–50% | 15.7% | 11.5% | 13.1% |
| 50–75% | 6.9% | 5.3% | 7.3% |
| >75% | 5.3% | 7.5% | 3.9% |

The 10–25% bin is strikingly similar across forms, while bottom and upper tails remain visibly different.

Use this to make a precise point:

> **Average spending shares converge strongly, but the underlying response distributions do not become identical. The three forms reach similar means through different internal reallocations.**

Do not claim formal equality or inequality of the full distributions unless existing PR19 inference supports it.

This is central to Puzzle 3.

---

# 3. The paper's second major contribution: explanation by progressively sharper questions

Restore the intellectual energy of the v2 mechanism section, but keep PR19's logic.

Do **not** call this a "mechanism funnel" that sequentially rules mechanisms out.

The preferred framing is:

> **We subject increasingly substantive explanations to progressively sharper implications of the data.**

Each subsection should begin with:
1. the mechanism or benchmark;
2. what it would naturally imply for one or more of the three puzzles;
3. what the distributional evidence already tells us;
4. what PR19's formal diagnostics add;
5. what remains unresolved.

---

## 3.1 Standard size dependence as the benchmark

Cash's decline is not itself mysterious.

Use classical and modern consumption theory to establish that a declining finite-transfer spending share can arise from:
- consumption smoothing;
- concavity of a finite-horizon consumption function;
- liquidity constraints / hand-to-mouth behavior;
- precautionary allocation;
- heterogeneous adjustment.

Literature should support **compatibility**, not a universal theorem.

The real question becomes:

> Why is familiar size dependence strong for Cash, weaker for Food, and almost absent in Medical mean responses?

This reframing makes Medical flatness and cross-form convergence the puzzles.

---

## 3.2 Pure arithmetic / scale explanations

Clarify what is and is not mechanical.

Weak benchmark:
- constant-yuan spending is not a serious theory and should not receive much space.

Useful scale result:
- share falls while implied yuan rises nearly proportionally;
- affine description summarizes the cells;
- interval model sensitivity prevents structural interpretation.

Conclusion:

> The phenomenon is a change in spending **shares and distributions**, not a collapse of yuan spending.

This narrows the object to explain but does not identify a mechanism.

---

## 3.3 Bottom-category accumulation is not the main observed path

Use the distributional anatomy:
- Cash bottom share nearly unchanged;
- Food bottom share slightly lower;
- Medical bottom share lower at 5,000 than at 200.

Therefore no story centered only on more respondents moving into the bottom category can organize all three puzzles.

Phrase carefully:
- this is about the **observed bottom response category**, not actual zero spending;
- do not call it a true participation margin.

This is a strong descriptive constraint on explanations.

---

## 3.4 Simple increasing mechanical bindingness

Write the prediction correctly.

If a larger Food voucher becomes progressively harder to absorb within eligible expenditure, a sharp simple account predicts a more negative Food-vs-Cash size gradient in households more likely to face bindingness.

PR19:
- historical proxy subgroup Food−Cash Top75 gradient:
  - G=0: +8.00pp [3.83, 12.18]
  - G=1: +1.33pp [−1.35, 4.01]
- G1−G0: −6.67pp, historical Holm≈.050
- continuous moderator tests imprecise;
- full ratio restrictions reject under both mappings for Top75 and more strongly for midpoint/ordinal.

Use the result as follows:

> The sharp simple increasing-bindingness prediction is not supported by the observed sign and is contradicted conditional on the historical proxy definition.

Immediately bound the claim:
- the proxy is coarse;
- Food includes daily necessities as well as food;
- subgroup status is observational;
- this does not reject every model with use restrictions.

This subsection directly addresses Puzzle 2.

---

## 3.5 Baseline category need

Ask:
- if Food and Medical responses were primarily governed by ordinary eligible spending needs, should baseline food/medical expenditure organize the size gradients?

PR19 / earlier frozen diagnostics:
- no stable precise continuous moderation signature;
- confidence intervals remain wide enough to allow meaningful heterogeneity.

Conclusion:

> Baseline category needs do not provide a sufficient organizing account at the available precision.

Do not say "need is ruled out."

Connect to the distributions:
- Medical's flat mean is generated by offsetting category movements, making a one-dimensional need story especially incomplete.

---

## 3.6 Relative income and liquidity

Ask:
- is the apparent size pattern simply about transfer size relative to household resources?

Use PR19:
- relative-income representations do not materially dominate nominal scale;
- direct moderation is not precisely established;
- income/liquidity CIs allow meaningful heterogeneity.

Conclusion:

> Relative financial scale remains plausible, but it does not parsimoniously organize the three puzzles in the observed data.

Do not use non-significance as equivalence.

---

## 3.7 Observable household types

Use the bounded moderator/all-X evidence only after the theory-driven tests.

Main text should be short:
- no stable observable moderator signature was identified across core economic variables;
- broader observable screens did not yield corrected stable candidates;
- available precision is insufficient to conclude homogeneous responses.

Best language:

> The three-puzzle pattern is not readily reducible to one observed household type, although meaningful latent or poorly measured heterogeneity remains possible.

Move detailed all-X tables to supplement.

---

# 4. Unified interpretation

The paper should aim for a unified interpretation that must face **all** of the following:

1. Cash has a strong declining share.
2. Food declines less.
3. Medical mean is flat.
4. Medical's flat mean masks offsetting distributional movements.
5. Small-transfer form gaps are much larger than large-transfer gaps.
6. Mean convergence does not imply identical full distributions.
7. Implied yuan spending still rises strongly.
8. Simple increasing Food bindingness does not fit the observed sign.
9. Standard observables do not provide a clean single-type explanation.

The unified interpretation must therefore be broader than "restriction" and broader than "Cash MPC declines."

Preferred language:

> **Resource form appears to matter most for how small transfers are allocated across spending-share responses. As transfer size grows, broader allocation considerations become increasingly important, reducing—but not eliminating—the differences associated with form.**

A behavioral candidate may be described as:

> **resource categorization / perceived spendability**

But this must remain an interpretation, not an identified mediator.

A good synthesis paragraph should say:

- small unrestricted Cash produces an unusually large mass of high spending-share responses;
- as Cash grows, that high-response premium compresses;
- Food starts from a less extreme distribution and adjusts more diffusely;
- Medical starts with the lowest spending-share distribution, and larger amounts generate offsetting internal movements rather than a mean decline;
- these paths produce strong convergence in mean shares without full distributional identity.

Then:

> One candidate account is that form matters most when a resource can be treated as a small, readily categorized allocation. Larger transfers induce a broader allocation problem, while earmarked resources arrive partially categorized from the outset.

Immediately add:
- this process is not directly measured;
- planning horizon, mental account, saving intentions and perceived spendability are absent from the survey;
- future experiments must measure/manipulate these processes.

The tone should be intellectually affirmative:
- "This pattern is consistent with..."
- "The evidence points to a useful hypothesis..."
- "A natural interpretation is..."

Avoid:
- "we prove mental accounting";
- "we identify spendability";
- "all alternatives are ruled out."

---

# 5. Detailed manuscript outline

## Title

Do not use a dull purely measurement title.

Generate 5 candidate titles after the manuscript is written. Preferred direction:

- **When Transfer Form Matters: Spending Responses across Small and Large Transfers**
- **Transfer Form Matters Most for Small Transfers**
- **How Transfer Size Reshapes Spending Responses across Cash and Earmarked Resources**
- **Small Transfers, Large Differences: Cash and Earmarked Spending Responses**
- **Transfer Size, Resource Form, and the Distribution of Stated Spending**

Final title should be assertive but not claim a statistically established universal interaction.

"Spendability" should not be the title's identified construct.

---

## Abstract

Target ~170–220 words unless the current verified JEBO guide requires otherwise.

Sequence:
1. broad question: does resource form matter equally across transfer sizes?
2. randomized 3×3 design and N=5,480 adults;
3. three-puzzle 3×3 fact;
4. percentage vs yuan distinction;
5. distributional anatomy:
   - Cash high-response compression;
   - Medical flat mean masks offsetting changes;
6. simple bindingness prediction fails in direction under the proxy;
7. formal interaction remains uncertain under 42-test correction;
8. unified interpretation as a candidate, not identified mechanism.

The abstract should not read like a limitations paragraph.

Only one sentence at the end should state the key boundary:
- hypothetical stated responses;
- no identified psychological mediator.

---

## 1. Introduction

Approximate target: 1,500–1,900 words.

### Paragraph 1 — Economic question
Transfer policy varies both form and size. Does form matter equally when transfers are small versus large?

### Paragraph 2 — Benchmark
Declining finite-windfall spending shares are compatible with standard consumption theory and common empirical evidence. That makes Cash's decline familiar rather than the only novelty.

### Paragraph 3 — Three puzzles
State the 3×3 cell means immediately and name the three puzzles:
- Medical flatness;
- Food does not fall faster than Cash;
- form gaps shrink sharply with amount.

### Paragraph 4 — Scale clarification
Share convergence is not yuan collapse. Give implied-yuan and finite-increment results.

### Paragraph 5 — Distributional discovery
Preview:
- Cash decline = high-response compression with stable bottom share;
- Food adjusts differently;
- Medical flat mean masks offsetting movements;
- mean convergence does not imply full distributional identity.

### Paragraph 6 — Explanation strategy
We ask increasingly sharp questions:
- ordinary size dependence;
- arithmetic/scale;
- bottom-category accumulation;
- bindingness;
- category need;
- relative resources/liquidity;
- observable types.

### Paragraph 7 — Main interpretive conclusion
Resource form appears most consequential for small-transfer allocation; larger amounts reduce visible form differences in spending shares. Resource categorization/perceived spendability is a candidate account, not measured.

### Paragraphs 8–10 — Literature contributions
Three literatures:
1. MPC / windfall size;
2. cash vs in-kind / fungibility / mental accounting;
3. survey elicitation / distributional MPC measurement.

### Final intro paragraph — roadmap.

Do not spend the Introduction defending every limitation. Put major inferential boundaries where relevant, and consolidate the rest later.

---

## 2. Conceptual background and literature

### 2.1 Standard size dependence
Permanent-income/consumption-smoothing benchmark, heterogeneous-agent/liquidity literature, finite-windfall size evidence.

### 2.2 Resource form, restrictions and mental accounting
Cash/in-kind, vouchers, labels, mental budgets, payment representation.

### 2.3 Why form-by-size patterns are theoretically ambiguous
Explain why simple restrictions can predict one direction under added assumptions, while categorization/planning may generate another.

### 2.4 Measurement and elicitation
Direct vs filtered MPC questions, hypothetical vs realized spending, horizons.

This section should set up predictions used later. It should not become a generic literature review.

---

## 3. Design, sample and estimands

Keep PR19's corrected methods.

Must include:
- 3×3 random assignment description;
- exact form bundles;
- adult N and cell Ns;
- questionnaire response bins;
- midpoint, ordinal, Top75 and above-bottom definitions;
- no common explicit horizon;
- bottom category not exact zero;
- stated/hypothetical outcome;
- 42-test family;
- reviewer-stage timing statement;
- interval model only as sensitivity;
- missing recruitment/ethics facts flagged until authors supply them.

Main methods should be readable. Put code-like detail in supplement.

---

## 4. Three puzzles in the randomized cells

### 4.1 The 3×3 mean pattern
Lead with the 3×3 table and figure.

### 4.2 Percentage shares versus implied yuan
Use Figure 2 and incremental responses.

### 4.3 Formal trend evidence
Report 42-family results compactly:
- Cash midpoint survives;
- Cash Top75 survives;
- ordinal does not;
- cross-form interactions remain uncertain.

Important writing rule:
do not let this subsection retroactively erase the visual/descriptive pattern. Explain that interaction inference answers a stronger population question.

---

## 5. Anatomy of the puzzles: full response distributions

This should be a substantial results section, not a robustness appendix.

### 5.1 Cash
High-response compression; stable bottom share.

### 5.2 Food
Diffuse redistribution; smaller top compression; not simply a scaled Cash pattern.

### 5.3 Medical
Flat mean, offsetting internal movements.

### 5.4 Convergence without distributional identity
Compare distributions at 5,000 and explain different paths to similar means.

A new descriptive figure may be created from PR19's adult aggregate data:
- three panels showing 200→5,000 change in six-bin shares for Cash, Food, Medical;
or
- grouped difference bars by response category.

This is a re-expression of existing PR19 aggregate results, not a new statistical analysis.

Do not add unplanned inferential tests.

---

## 6. What can explain the three puzzles?

Use the progressive logic in Section 3 of this specification.

Suggested subsections:
6.1 Standard size dependence explains the benchmark, not the cross-form puzzle  
6.2 Scale and affine descriptions  
6.3 Bottom-category accumulation is insufficient  
6.4 The sharp mechanical-bindingness prediction  
6.5 Baseline category need  
6.6 Relative income and liquidity  
6.7 Observable heterogeneity and precision

Each subsection should end with a one- or two-sentence **interim conclusion** that tells the reader what the explanation can and cannot account for.

Do not end every paragraph with caveats. Put precision numbers where they matter, then move on.

---

## 7. A unified behavioral interpretation

This section should synthesize Sections 5 and 6.

It should be constructive, not apologetic.

Core structure:
1. Restate the three distinct distributional adjustment paths.
2. Explain why no one-dimensional mechanical account naturally captures all three.
3. Propose resource categorization/perceived spendability as a coherent candidate account.
4. Explain how it can accommodate:
   - small Cash high-response premium;
   - weaker Food compression;
   - Medical offsetting reallocation;
   - mean convergence at larger amounts.
5. Explicitly state what the current design does not observe.
6. Derive concrete predictions for a future experiment.

Future experiment predictions should be specific:
- directly measure perceived spendability;
- elicit intended allocation across current spending/saving/debt/future spending;
- impose common horizon;
- separately randomize label, restriction, expiry/liquidity;
- ideally use realized transfers/transactions.

This makes the interpretation scientifically useful even though it is not identified here.

---

## 8. Discussion

Do not make Discussion a list of weaknesses.

Structure it around contributions:

### 8.1 Behavioral contribution
Form matters most at small amounts in the observed share profiles; size changes the importance of resource form.

### 8.2 Distributional contribution
Similar means can hide very different distributional movements; Medical is the clearest example.

### 8.3 Transfer-design contribution
Cash vs earmarked comparisons at one amount may not transport to other amounts.

### 8.4 Measurement boundary
Share vs yuan; hypothetical responses; bundled treatments; horizon.

### 8.5 What would resolve the mechanism
Future design.

Limitations should be integrated, not piled up at the start.

---

## 9. Conclusion

Short and memorable.

Suggested logic:

> Cash shows familiar size compression, Food less, Medical almost none. The result is strong convergence in average stated spending shares as transfer size increases. Yet the three forms arrive there through different changes in the response distribution, and absolute intended spending continues to rise strongly. The sharpest simple bindingness account does not organize the pattern, while available household characteristics do not supply a single precise alternative. Transfer form therefore appears most consequential at small scales, motivating a behavioral hypothesis in which resource categorization and perceived spendability change with scale.

Then one final boundary sentence:
the current survey motivates but does not directly identify that psychological process.

---

# 6. Writing style requirements

## 6.1 Tone

The manuscript should sound like a JEBO paper with a real finding.

Use confident declarative prose for facts that PR19 supports.

Good:
- "The randomized cells reveal three puzzles."
- "Medical's flat mean masks offsetting movements across the response distribution."
- "Transfer-form differences are largest at the smallest amount in the observed cells."
- "The sharp simple bindingness prediction has the wrong sign under the historical proxy."

Avoid defaulting to:
- "we cannot...";
- "we do not...";
- "this should not...";
in every paragraph.

Use limitations where they change interpretation, not as a verbal tic.

## 6.2 Do not confuse confidence with overclaiming

Strong writing is allowed:
- "reveals";
- "shows" for raw randomized cell facts;
- "is consistent with";
- "contradicts the sharp prediction" where PR19 actually establishes sign contradiction;
- "provides a puzzle";
- "suggests a candidate account."

Do not use:
- "proves";
- "establishes the mechanism";
- "rules out liquidity";
- "shows equal slopes";
- "demonstrates full convergence";
- "identifies spendability."

## 6.3 Paragraph architecture

Each paragraph should have:
1. one clear claim;
2. the most relevant evidence;
3. one interpretation.

Avoid audit-style paragraphs that stack five caveats and multiple p values.

Put dense inferential detail in tables/supplement and cite it in prose.

## 6.4 Narrative rhythm

Preferred:
fact → puzzle → distributional anatomy → explanation → synthesis.

Avoid:
method → caveat → adjusted p → caveat → another test → limitation.

## 6.5 Terminology

Preferred:
- stated spending share;
- midpoint-coded share;
- midpoint-implied yuan;
- finite incremental implied-yuan response;
- response distribution;
- bottom category;
- above-bottom category;
- high-response category;
- observed convergence in mean shares;
- resource form;
- resource bundle;
- candidate behavioral account.

Avoid unqualified:
- MPC when the local-derivative meaning is implied;
- participation;
- extensive margin;
- actual spending;
- structural MPC;
- spendability as measured variable.

"MPC" may be used when explicitly defined as a stated finite-transfer share and connected to the literature, but the manuscript should not slide between local and finite MPC concepts.

---

# 7. Literature requirements

The literature review must not be a citation inventory. Every cited cluster should answer: **what prediction, benchmark, or measurement issue does this literature contribute to our three puzzles?**

## 7.1 Standard consumption / MPC benchmark

Must engage:
- Friedman / permanent-income benchmark;
- Jappelli & Pistaferri review;
- Kaplan & Violante on heterogeneous MPCs / liquidity;
- Fagereng et al. on heterogeneity;
- Shapiro & Slemrod survey MPC tradition;
- Fuster, Kaplan & Zafar (2021);
- Andreolli & Surico (2026);
- Jappelli et al. (2026) if still relevant/verified.

Use this literature to say:
- declining finite-windfall shares are compatible with standard theory;
- size responses can differ across households and elicitation settings;
- no universal monotonic theorem should be claimed.

## 7.2 Transfer form, fungibility, labels and restrictions

Must engage:
- Thaler (1985, 1999);
- Shefrin & Thaler;
- Heath & Soll;
- Kooreman;
- Abeler & Marklein;
- Hastings & Shapiro;
- Cunha where relevant;
- Kan et al. on shopping vouchers;
- Bonomo, Ruffini & Schanzenbach — verify current status;
- Boehm, Fize & Jaravel (2025).

Use these to frame:
- full fungibility benchmark;
- formal restrictions;
- category budgets;
- labels and mental accounting;
- realized-transfer evidence versus our hypothetical stated outcomes.

## 7.3 Closest joint form/size predecessor

Bernard (2023) must be discussed directly.

Do not claim first joint design.

Explain the difference:
- payment mode / account representation versus category-restricted Food/Medical bundles;
- our three amounts;
- full response distributions;
- our focus on the three-puzzle pattern.

Verify whether it is still a working paper at the revision date.

## 7.4 JEBO behavioral comparators

Directly engage:
- Lee et al. (JEBO 2024);
- Pauls & Laudi (JEBO 2025).

Explain why they demonstrate JEBO relevance:
- representation/earmarking can shape stated allocation;
- but their mechanisms and outcomes differ from ours.

Verify volume/article/page information.

## 7.5 Measurement and elicitation

Must engage:
- Parker & Souleles (2019);
- Crossley et al. (current status, 2026);
- Ueda (2025) if retained.

Be balanced:
- do not cite Parker–Souleles as universal validation;
- use Crossley to explain that elicitation format and horizon can change measured MPC-size patterns;
- distinguish hypothetical vignette response from realized consumption.

## 7.6 Citation rules

- Verify every 2025–2026 publication status, volume, pages/article number and DOI using primary publisher/Crossref sources.
- Working papers must be labelled working papers.
- Do not cite a paper for a claim it does not make.
- Prefer fewer, more directly discussed references to a long decorative list.
- Main text should contain a clear dialogue with the closest literature, especially Bernard, Fuster, Andreolli–Surico, Crossley, Bonomo/Boehm, Lee and Pauls–Laudi.

---

# 8. Figures and tables

The main manuscript should visually reinforce the story.

## Figure 1 — The 3×3 puzzle
Full adult six-bin response atlas or a redesigned version that makes all nine cells easy to compare.

## Figure 2 — Percentage and yuan scales
Two panels:
- midpoint-coded share by amount and form;
- midpoint-implied yuan by amount and form.

Keep PR19 bootstrap intervals.

## Figure 3 — Distributional anatomy
Create from existing PR19 adult aggregate data only.

Preferred design:
- three panels, one per form;
- bars show 5000 minus 200 change in the share of each of six response categories.

This should visually show:
- Cash: large negative top category;
- Food: diffuse redistribution;
- Medical: offsetting movements.

No new inferential stars.

## Figure 4 — Food sharp-prediction diagnostic
Use PR19's corrected raw subgroup figure or a cleaner version.

Clearly label:
- outcome;
- subgroup proxy;
- N;
- sign of the sharp prediction.

## Optional Figure 5 — Incremental implied-yuan responses
Keep in main only if it materially improves the scale argument. Otherwise move to supplement and retain the key estimates in Table 2.

## Main tables

### Table 1
Design and adult cell Ns.

### Table 2
3×3 midpoint share with implied yuan in parentheses, plus endpoint gaps if useful.

### Table 3
Key trend / 42-family inference:
- Cash midpoint;
- Cash Top75;
- Cash ordinal;
- cross-form omnibus / pairwise focal contrasts.

### Table 4
Compact mechanism prediction-and-precision summary:
- standard benchmark;
- sharp Food bindingness;
- category need;
- relative income/liquidity;
- observable heterogeneity.

Avoid overwhelming the main text with the full 42-test table.

---

# 9. Supplement

The supplement should carry the technical burden so the main paper can read like a paper rather than an audit.

Must include:
- full 42-test family;
- all original six-bin cell frequencies;
- old 21-test family;
- affine model details;
- interval-model assumptions and calibration;
- bootstrap details;
- full Food continuous/ratio analyses;
- MDE / precision ledger;
- all-X screen;
- response-style Q1/Q2 definitions and sensitivity;
- weighting/calibration sensitivity;
- questionnaire Chinese text + English translation;
- sample characteristics;
- balance table;
- reference audit;
- analysis timing statement.

---

# 10. Word formatting and deliverables

Create a clean submission-style Word document.

Formatting:
- Times New Roman throughout;
- body text 12 pt (小四 equivalent);
- main title 16–18 pt bold;
- section headings 14 pt bold;
- subsection headings 12 pt bold;
- tables/figure notes 9–10 pt;
- body paragraphs justified;
- first-line indent approximately 0.74 cm;
- consistent paragraph spacing;
- readable margins;
- automatic page numbers;
- figures inserted near first discussion where practical;
- table titles above tables, figure captions below figures;
- no ugly manual line breaks;
- no tracked changes/comments in the submission copy.

Also produce:
- editable Word manuscript;
- Word supplement;
- separate Highlights file;
- updated reference audit;
- updated claim ledger;
- source data for any redesigned figures.

Author metadata still missing from PR19 must remain clearly marked and must not be invented.

---

# 11. Non-negotiable scientific boundaries inherited from PR19

The new writing must preserve all of the following:

1. Cash midpoint and Top75 trends survive the expanded 42-test correction; ordinal does not.
2. Cross-form interaction remains uncertain under expanded correction.
3. Similar large-amount incremental point estimates do not establish equivalence.
4. Affine models are descriptive, not structural.
5. Interval-model parameters are scale-assumption sensitive.
6. The Food sharp increasing-bindingness prediction has the wrong observed sign under the historical proxy.
7. Continuous moderator nulls are imprecise and do not rule out meaningful heterogeneity.
8. Bottom-category decomposition is a coding identity, not causal extensive/intensive decomposition.
9. Spendability / resource categorization is a candidate interpretation, not a measured mediator.
10. The survey measures hypothetical stated responses, not realized spending.
11. Form treatments bundle use restrictions, liquidity, expiry, timing and labels.
12. Missing recruitment/ethics/randomization implementation facts must not be fabricated.

These boundaries should appear where relevant, but they must not dominate the prose.

---

# 12. Final quality test

Before delivery, ask whether a reader can answer these questions after reading only the Abstract + Introduction + Figures 1–3:

1. What are the three puzzles?
2. Why is Cash's decline not the whole contribution?
3. Why is Medical's flat mean interesting?
4. Why does Food challenge a simple bindingness intuition?
5. What exactly converges at large amounts?
6. Why is this a percentage-allocation puzzle rather than a yuan-spending collapse?
7. What do the distributions reveal that the means hide?
8. What is the strongest unified behavioral hypothesis?
9. What is still not identified?

If the answers are not obvious, rewrite before delivery.
