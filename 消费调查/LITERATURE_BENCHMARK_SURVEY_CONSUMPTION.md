# Survey-based Consumption & Context Literature Benchmark

> **用途**：消费调查项目的长期文献参照库，供 ChatGPT / Work 在修改论文、设计复核分析、规划新一轮问卷和判断投稿定位时使用。  
> **更新日期**：2026-10-03  
> **项目路径**：消费调查/  
> **当前项目核心设计**：3×3 随机情景实验；transfer form = unrestricted cash / 6个月食品日用品消费券 / 长期有效医保个人账户；amount = RMB 200 / 1,000 / 5,000；outcome = hypothetical/stated additional total consumption，6档回答。  
> **当前更强的研究问题**：不只问“不同 transfer form 是否改变平均 MPC”，而是问：当客观资源相近、呈现形式/可使用范围改变时，个体异质性的结构、可预测性与跨 context 可迁移性是否也发生改变。

---

# 0. 如何使用这份文献库

这份文件不是一般的 bibliography，而是“研究设计 benchmark”。每篇文章都尽量回答八个问题：

1. **研究问题是什么？**
2. **数据是什么？样本多大？是真实行为、survey、survey experiment 还是混合数据？**
3. **处理/情境如何设计？**
4. **识别与估计怎么做？**
5. **主要发现是什么？**
6. **文章真正讲的故事是什么？**
7. **为什么它有机会发表在这个档次？**
8. **我们可以借什么、不能借什么？**

特别说明：下面“为什么能发表”是基于论文设计、结果和期刊定位做的研究判断，**不是编辑或审稿人的官方解释**。

Work 在以后引用这些 benchmark 时，请遵守三条纪律：

- 不要笼统说“survey data 也能发好期刊”。要说明该文章靠什么把 survey 变成有识别力的证据：理论鉴别、随机 framing、真实政策锚定、跨期追踪、真实钱、跨国尺度、多研究复制、新测量指标等。
- 不要把 stated response 等同于 realized spending。必须把 Parker–Souleles（2019）、Ueda（2025）和 Crossley et al.（2025 working paper）一起看。
- 不要因为某篇文章用了类似技术就照搬结论。最重要的是找出“publication engine”：它到底把一个简单问卷结果升格成了什么更大的行为或经济学问题。

---

# 1. 最直接的 benchmark：stated MPC、windfall、transfer form 与 fungibility

## 1.0 Closest direct predecessor — Bernard (2023), Deutsche Bundesbank Discussion Paper  
### “Mental Accounting and the Marginal Propensity to Consume”

**Citation / status**  
Bernard, René. 2023. “Mental Accounting and the Marginal Propensity to Consume.” *Deutsche Bundesbank Discussion Paper* No. 13/2023.  
As of 2026-10-03, the authoritative sources located for this benchmark still list it as a Bundesbank discussion paper / SSRN working paper rather than a journal publication. Do **not** describe it as a published JEBO or other journal article unless a later publication is independently verified.  
Official sources:  
- https://www.bundesbank.de/en/publications/research/discussion-papers/mental-accounting-and-the-marginal-propensity-to-consume-909438  
- https://www.bundesbank.de/resource/blob/909438/d24b53faa075049c3ba7fe0dcdf512b3/mL/2023-05-22-dkp-13-data.pdf  
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4537003

### Why this is the closest direct predecessor to our project
Among the literature reviewed so far, Bernard is unusually close to our design because it combines:

- **hypothetical stated MPC** as the outcome;
- randomized variation in the **form / payment mode** of a windfall;
- randomized variation in **shock size**;
- an explicit **mental accounting / fungibility** interpretation;
- rich individual characteristics;
- **causal machine learning / causal forest** to study HTE;
- a direct attempt to explain **who is more sensitive to context**.

If our paper only claimed:

> payment form changes stated MPC; amount matters; treatment effects are heterogeneous; psychology/liquidity predict HTE,

then Bernard already occupies much of that territory.

Therefore Work should treat Bernard as a **direct competitive benchmark**, not a peripheral citation.

### Research question
Bernard asks how and why households respond to unexpected, transitory income shocks, with special attention to whether consumers treat economically similar money differently depending on:

1. **payment mode**;
2. **shock size**;
3. **source of income**.

The theoretical lens is mental accounting: if money is perfectly fungible, merely changing how an otherwise accessible windfall is presented or deposited should not materially change MPC.

### Main data
The main study uses the **Bundesbank Online Panel Households (BOP-HH)**.

The paper draws on two survey waves:

- December 2020: roughly 4,000 participants;
- June 2021: roughly 2,500 participants;
- after exclusions / valid MPC answers, the paper reports **6,373 MPC observations** for the core randomized scenarios.

BOP-HH is a structured German household online panel rather than an ad hoc convenience survey. The paper discusses demographic quotas / sample composition and respondent incentives.

### Core experimental design: approximately 2 × 3
The main experiment varies two dimensions.

#### Shock size
The hypothetical unexpected government payment equals either:

- **one month of household net income**, or
- **three months of household net income**.

This makes treatment size household-specific rather than a common nominal euro amount.

#### Payment mode
The windfall is described as:

1. **unspecified payment mode**;
2. **paid out in cash**;
3. **deposited into an instant-access savings account**.

The savings account is important: the paper explicitly describes it as liquid / accessible, without a lock-up that would mechanically prevent spending.

This is why the design gives a relatively clean fungibility test. Standard budget-set logic gives less reason for MPC to differ sharply between cash and an immediately accessible savings account than between cash and a genuinely restricted in-kind transfer.

### Outcome measurement
Respondents report what **percentage of the windfall they would spend over the next 12 months**, with the remainder saved or used for debt repayment.

The MPC is therefore a **hypothetical stated MPC**, not observed transaction-based consumption.

Unlike our current six-category outcome, Bernard's primary MPC elicitation is essentially a 0–100 percent share.

### Main cell means
The paper reports a clear 2 × 3 pattern. Approximate mean stated MPCs are:

| Payment mode | 1 month income | 3 months income |
|---|---:|---:|
| Unspecified | 52.3% | 46.6% |
| Cash | 53.6% | 47.3% |
| Instant-access savings account | 44.9% | 42.2% |

The exact table / regression specification should be checked in the paper before quoting numbers in a manuscript, but the qualitative pattern is robust:

- larger shocks generate lower MPC;
- savings-account presentation generates lower MPC than cash / unspecified payment;
- cash and unspecified payment are much closer to one another.

### Average treatment effects
Bernard's core results are:

1. **Payment mode matters.**  
   Compared with a windfall deposited into an instant-access savings account, stated MPC is substantially higher when the payment is cash or when payment mode is left unspecified.

2. **Shock size matters.**  
   Moving from one month to three months of household income lowers MPC.

3. **Source of income matters much less.**  
   In an additional study comparing a government windfall with a lottery-type windfall, the source itself produces little / no clear MPC difference relative to the stronger size and payment-mode effects.

The paper interprets the first two findings as broadly consistent with mental accounting.

### Why the payment-mode result is especially important
For our project, this is the crucial comparison.

Our food voucher and medical account **genuinely change the feasible use of the transfer**:

- food voucher: category restriction + six-month validity;
- medical account: medical-only restriction + long horizon;
- cash: unrestricted.

Therefore, if our MPCs differ across forms, standard budget constraints can contribute mechanically.

Bernard's cash-versus-liquid-savings comparison is in some respects a **cleaner mental-accounting manipulation**, because both forms remain highly liquid and broadly fungible in the ordinary budget-set sense.

This means we should **not** claim that our mean form effect is uniquely strong evidence of mental accounting. Bernard provides a cleaner predecessor for that narrow claim.

### Extensive and intensive margins
The paper does not stop at mean MPC. It also shows the payment-mode difference reflects changes in whether people spend at all and how much spenders allocate.

In particular, the savings-account framing increases the mass of respondents who report little or no spending and lowers spending among at least some positive spenders.

This is useful for our project because our six-category outcome may contain floor / threshold behavior that a simple mean midpoint regression obscures.

Work should therefore continue to inspect:

- zero / lowest-category incidence;
- distribution shifts;
- ordered-outcome estimates;
- not only midpoint MPC means.

### Heterogeneous treatment effects and causal machine learning
This is the part that most directly overlaps with our earlier paper design.

Bernard uses **causal forests / causal machine learning** to study heterogeneity in:

- payment-mode effects;
- shock-size effects.

The implementation uses an honest forest-style approach with many trees and out-of-bag / honest treatment-effect prediction.

The paper then asks whether predicted high- and low-treatment-effect groups differ systematically.

Candidate predictors include variables related to:

- liquidity / financial constraints;
- income and household resources;
- impatience;
- impulsiveness;
- self-control;
- planning;
- cognitive sophistication / confidence;
- other demographics and financial characteristics.

### HTE findings
The broad pattern is that larger treatment sensitivity is associated with characteristics such as:

- lower liquidity;
- weaker self-control;
- greater impatience / impulsiveness;
- weaker financial planning;
- lower cognitive sophistication.

The paper therefore connects HTE back to the mental-accounting interpretation rather than presenting the forest as a purely predictive exercise.

### What Bernard's story actually is
The story is not merely:

> “MPC differs across people.”

It is closer to:

> **Consumers violate fungibility in systematic ways. How a windfall is mentally categorized—partly shaped by payment mode and size—changes spending, and susceptibility to these mental accounts is itself heterogeneous across people.**

This is already a sophisticated **context × person heterogeneity** story.

### Why this working paper is important even though journal status is unclear
Do not infer anything about quality from the absence of a journal citation. We do not know why or whether the paper has been submitted, revised, or accepted elsewhere.

For our purposes, the relevant fact is that the design exists publicly and directly overlaps with several claims we might otherwise present as novel.

Therefore:

- Bernard must appear in the Introduction / literature positioning if those claims remain in the manuscript;
- Work must use it as a novelty benchmark regardless of publication status.

### Bernard vs our project: direct comparison

| Dimension | Bernard (2023) | Our current project |
|---|---|---|
| Outcome | hypothetical stated MPC | hypothetical/stated additional consumption / MPC categories |
| Main randomization | shock size × payment mode | amount × transfer form |
| Size | 1 vs 3 months household income | RMB 200 / 1,000 / 5,000 |
| Form | unspecified / cash / liquid savings account | cash / food voucher / medical account |
| Budget-set change | small for cash vs liquid savings | substantial for food/medical restrictions |
| Mental accounting | central theory | candidate theory |
| Fungibility | central | central |
| HTE | causal forest | HTE / DR / BLP / GATES / ML |
| Psychology / traits | used to explain HTE | rich observables used for prediction / HTE |
| Predictive heterogeneity | yes | yes |
| Cross-context source→target prediction | **no** | **yes, core current analysis** |
| Within-vs-cross portability benchmark | **no** | **yes** |
| Direct test of X→Y mapping invariance across forms | **not the central analysis** | **yes, core current analysis** |
| Question “does a high responder remain high across contexts?” | **not directly answered** | **our proposed contribution** |

### The exact novelty constraint Bernard imposes on us
After Bernard, these statements are **not sufficient novelty claims**:

- payment form changes stated MPC;
- shock size changes MPC;
- mental accounting may violate fungibility;
- treatment effects differ across people;
- causal forest can recover treatment-effect heterogeneity;
- liquidity and psychological traits correlate with treatment sensitivity.

If our manuscript headline is still mainly one of those statements, the positioning is too close to Bernard.

### Where our potential contribution is genuinely different
The strongest distinction is:

> **Bernard studies heterogeneity in context effects. We study whether heterogeneity itself is portable across contexts.**

Bernard asks, approximately:

> Who is more sensitive to payment mode or shock size?

Our current paper asks an additional question:

> If someone appears to be a high responder, or if a set of covariates predicts high response in one transfer context, does that ordering / predictive mapping survive when the resource context changes?

Formally, our null is closer to:

[
f_{cash}(X) = f_{food}(X) = f_{medical}(X) + 	ext{context-specific intercept shifts},
]

or more loosely:

> transfer form changes the mean but leaves the mapping from person characteristics to response invariant.

The portability and invariance analyses test that null.

### Why this distinction matters conceptually
The distinction separates two ideas that are often blurred:

1. **HTE exists.**  
   Different people react differently to a treatment.

2. **HTE / behavioral type is portable.**  
   The people predicted to react strongly in one context remain the ones predicted / observed to react strongly in another context.

Bernard establishes evidence for the first kind of heterogeneity.

Our intended contribution concerns the second.

If portability fails, then some apparent “individual differences” are better understood as **person × context interactions**, not stable person-level traits.

### But Bernard also exposes a weakness in our design
Because Bernard's cash-versus-instant-access-savings manipulation leaves the budget set relatively similar, it is easier to attribute differences to mental accounting.

Our food and medical treatments alter:

- spending category restrictions;
- convertibility;
- time horizon;
- precautionary value.

Therefore, if medical shows the largest remapping, Work must not over-interpret that as proof that “individual differences are unstable in general.”

A more defensible boundary-condition story may be:

> **Individual response mappings can remain relatively portable across nearby resource contexts, but portability weakens when the transfer changes the economic and psychological construct—especially when it becomes strongly earmarked and forward-looking.**

### What Work should borrow from Bernard
1. Treat amount as theoretically meaningful, not a nuisance control.
2. Inspect extensive and intensive margins / floor behavior.
3. Use HTE only when it links back to a mechanism.
4. Explicitly distinguish liquidity-based explanations from psychology / planning / self-control.
5. Explain why a payment mode should or should not alter the budget set.
6. Keep “source”, “form”, and “size” conceptually separate.
7. Use Bernard in the Introduction as the closest predecessor for **payment-mode × MPC × causal-HTE**.

### What Work should *not* copy from Bernard
1. Do not make “mental accounting” the conclusion simply because form effects exist.
2. Do not claim our restricted transfers are economically equivalent to cash.
3. Do not make causal forest feature importance the headline.
4. Do not describe our analysis as novel merely because it uses causal ML.
5. Do not infer stable individual traits from one-treatment-per-person cross-sectional HTE.
6. Do not ignore the measurement problem created by our different form descriptions and horizons.

### Required one-sentence novelty test
Before any future manuscript revision, Work should be able to complete this sentence convincingly:

> **Bernard (2023) shows that payment mode and shock size alter stated MPC and that sensitivity to these manipulations is heterogeneous; our contribution is to show/test whether the behavioral mapping underlying such heterogeneity is itself portable across resource contexts.**

If the current empirical results cannot support the clause after the semicolon, the paper needs a narrower contribution.

---

## 1.1 Fuster, Kaplan & Zafar (2021), Review of Economic Studies  
### “What Would You Do with $500? Spending Responses to Gains, Losses, News, and Loans”

**Citation**  
Fuster, Andreas, Greg Kaplan, and Basit Zafar. 2021. “What Would You Do with $500? Spending Responses to Gains, Losses, News, and Loans.” *Review of Economic Studies* 88(4): 1760–1795.  
DOI: https://doi.org/10.1093/restud/rdaa076  
Official/author sources:  
- https://academic.oup.com/restud/article/88/4/1760/5962017  
- https://www.newyorkfed.org/research/staff_reports/sr843

### Research question
不是简单问“平均 MPC 多高”，而是用一组精心设计的 hypothetical counterfactuals 去区分消费理论：

- unexpected gain：突然多一笔钱；
- unexpected loss：突然损失一笔钱；
- news about future gain/loss：钱不是现在变化，而是未来变化；
- interest-free loan：现在获得流动性但并不增加净财富；
- transfer size：金额也变化。

核心思想是：**如果不同消费模型背后的机制不同，那么它们对这些 counterfactuals 的预测也不同。**

### Data
数据来自 New York Fed Survey of Consumer Expectations（SCE），美国全国线上 rotating panel。

- 2,586 household heads；
- 四个额外模块：2016年3月、2016年5月、2017年1月、2017年3月；
- 因为 SCE 是 panel，一些受访者参加多个模块；
- 一共获得 9,061 个 hypothetical spending responses；
- baseline gain 中金额包括 $500、$2,500、$5,000；
- 问的是未来三个月中，相比没有这笔钱时，spending / debt repayment / saving 会怎么变以及变化多少。

样本人口学和财务特征可以与 ACS / SCF 对照，论文也专门展示代表性特征。

### Design / identification
这是 survey elicitation，但不是普通相关性调查。作者把 survey 当成一个可以操纵经济状态的“counterfactual laboratory”。

基本结构：

- 先问 extensive margin：会不会改变支出；
- 再问 intensive margin：会改变多少；
- 改变 gain/loss、现在/未来、金额、loan 等；
- 比较这些反应模式与不同理论机制的预测。

由于处理的是 hypothetical scenarios，关键识别不是“真实政策 causal effect”，而是**不同 counterfactual 之间的结构性反应模式**。

### Main findings
几个最重要的事实：

1. 对意外 gain 的反应高度异质：大量人是 0，也有一批人反应很大；
2. loss 的支出反应比同规模 gain 更普遍、更大；
3. 即使是对 current gain 反应很大的人，也未必对 future gain news 有明显反应；
4. 对一年期无息贷款的反应很弱，说明“高 MPC = 短期借贷约束”不是充分解释；
5. future loss news 却会导致提前削减消费，说明简单 myopia 也不能解释全部现象；
6. 金额变化不仅改变 intensive margin，也改变是否反应的 extensive margin。

### Methods / theory connection
文章的关键不是跑一个 flexible ML，而是：

- 先建立一组 reduced-form facts；
- 再拿这些 facts 去区分 benchmark models；
- 最后用带 precautionary saving、调整消费的效用成本以及低财富家庭等元素的定量模型解释事实。

也就是说：**survey facts → theoretical discrimination → quantitative model**。

### Story
表面上：“给你 500 美元，你会花多少？”

真正故事：“我们可以通过人们如何回应 gain / loss / future news / loan，识别为什么一部分家庭有很高的 MPC，以及哪些标准消费理论解释不了这些行为。”

### Why this could publish in ReStud
这是我们最需要理解的一篇。它证明 hypothetical survey 本身不是档次天花板。

它的 publication engine 是：

- counterfactual 设计非常有理论含义；
- 不是只找相关特征，而是在排除机制；
- 多个 scenario 形成一套相互约束的事实；
- 理论模型必须同时解释这些事实；
- survey 的优势被正面利用：很多真实世界里几乎无法随机制造的 gain/loss/news/loan，可以在同一框架中被系统比较。

### Lessons for our project
最直接的启示不是“我们也问 MPC，所以可以投 ReStud”，而是：

- **不同 form 与 amount 必须被当成理论鉴别工具，而不是 9 个 cell 均值。**
- 如果 cash / food / medical 的差异能区分 pure fungibility、binding constraint、mental accounting、precautionary asset、salience 等机制，文章会明显升级。
- amount 的 200/1000/5000 不应该只是 robustness；它可以检验 restricted transfer 是否随着 bindingness 或 perceived account size 发生非线性。
- 我们的当前“跨 context mapping/invariance”故事如果成立，也要像这篇一样说明：它排除了什么简单模型？例如“form 只产生 additive mean shift，但 person-level mapping 不变”。

### Caution
Fuster et al. 有四轮模块和大量 scenario variation；我们当前是一人只看到一个 3×3 cell。不能把他们的 respondent-level repeated information 当成我们也具备。

---

## 1.2 Jappelli & Pistaferri (2014), AEJ: Macroeconomics  
### “Fiscal Policy and MPC Heterogeneity”

**Citation**  
Jappelli, Tullio, and Luigi Pistaferri. 2014. “Fiscal Policy and MPC Heterogeneity.” *American Economic Journal: Macroeconomics* 6(4): 107–136.  
DOI: https://doi.org/10.1257/mac.6.4.107  
Official: https://www.aeaweb.org/articles?id=10.1257/mac.6.4.107

### Data
2010 Italian Survey of Household Income and Wealth（SHIW）。

这个代表性家庭调查拥有丰富的：

- income；
- liquid resources / cash-on-hand；
- wealth；
- household balance sheet；
- socioeconomic characteristics。

关键 survey question 直接问：如果出现一个 unexpected transitory income change，家庭会消费其中多少。

### Main finding
平均 reported MPC 约 48%。

更重要的是：

- 低 cash-on-hand 家庭 MPC 明显高；
- 富裕/资源充足家庭 MPC 较低；
- pattern 与 precautionary-saving model 相吻合。

作者进一步将异质性用于财政政策 counterfactual：如果转移针对不同资源分布位置的家庭，aggregate consumption stimulus 会有多大差别。

### Methods/story
这篇文章的逻辑非常经济学：

**一个简单 survey elicitation → household balance sheet heterogeneity → precautionary-saving theory → fiscal targeting implications。**

### Why publish
它并不靠复杂 ML，也不靠真实消费流水。

关键在于：

- SHIW 是高质量代表性 household finance survey；
- stated MPC 与完整 household balance sheet 连起来；
- 异质性直接对应理论中的 cash-on-hand / precautionary saving；
- 最后把微观异质性推成宏观财政政策含义。

### Lessons for us
“demographics 能否预测 MPC”不是最终问题。必须回答：

- 哪种可观测维度有经济理论含义？
- context × household resource 是否对应一个明确 constraint？
- 我们的 food bindingness、medical expenditure / liquidity / precautionary-saving proxies 能否形成同样清楚的理论对话？

---

## 1.3 Jappelli & Pistaferri (2020), AEJ: Economic Policy  
### “Reported MPC and Unobserved Heterogeneity”

**Citation**  
Jappelli, Tullio, and Luigi Pistaferri. 2020. “Reported MPC and Unobserved Heterogeneity.” *American Economic Journal: Economic Policy* 12(4): 275–297.  
DOI: https://doi.org/10.1257/pol.20180420

### Data/design
继续使用 Italian SHIW，但利用 2010 和 2016 两期 reported MPC panel information。

### Question
2014 那篇发现 cash-on-hand 与 MPC 强负相关，但有没有可能是 persistent unobserved household traits 同时影响 cash-on-hand 与 MPC？

这篇直接研究 omitted/unobserved heterogeneity。

### Method
利用 panel structure，使用能控制 household unobserved heterogeneity 的 regression methods，再看 cash-on-hand–MPC relationship 是否消失。

### Finding
控制 unobserved heterogeneity 后关系会减弱，但 bias 并没有大到推翻原始经济关系。

最后仍将 estimated MPC 用于 revenue-neutral fiscal targeting。

### Why publish
不是重复“低流动性的人 MPC 高”，而是把上一代 survey MPC 文献最容易被攻击的 identification 问题拿出来解决。

### Lessons for us
我们做 HTE、SHAP、prediction 时尤其要警惕：

- 可观察 traits 与 response 的关联，不等于 stable individual trait；
- 如果我们真正想讲 “individual heterogeneity”，就必须区分 observable heterogeneity、latent heterogeneity 和 noise；
- 当前一人一个 treatment cell 的设计不能直接把 cross-form differences 解释成 individual-level fungibility trait。

---

## 1.4 Lewis, Melcangi & Pilossoph (2026), Review of Economic Studies  
### “Latent Heterogeneity in the Marginal Propensity to Consume”

**Citation**  
Lewis, Daniel, Davide Melcangi, and Laura Pilossoph. 2026. “Latent Heterogeneity in the Marginal Propensity to Consume.” *Review of Economic Studies*.  
DOI: https://doi.org/10.1093/restud/rdaf102  
Official: https://academic.oup.com/restud/article/doi/10.1093/restud/rdaf102/8489895

### Data
2008 US Economic Stimulus Payments。

重点不是再找更多 observables，而是利用 stimulus variation 恢复 MPC 的 **unconditional latent distribution**。

### Method
核心方法是 clustering regression。

传统 HTE 做法通常是：

MPC = treatment × observed characteristic。

作者反过来问：

> 如果我们先不假定异质性一定沿着收入、年龄、流动性等 observables 排列，数据本身暗示存在怎样的 latent MPC groups/distribution？

### Findings
- 家庭在一个季度内花掉 rebate 的比例，从约 4% 到 133% 都存在；
- 不同家庭还会把 transfer 花在不同 goods 上；
- 很多 observables 单独看与 MPC 相关，但联合进入后多数关系消失；
- income 与 average propensity to consume 是较稳健的例外；
- 所有 household observables 合起来只能解释约 **8% 的 MPC variation**。

### Story
不是“我们找到更好的 predictor”，而是：

> MPC heterogeneity 很大，但它主要是 latent 的；依靠常见 observables 去定义 heterogeneity，会严重低估其结构。

### Why publish
- 问题击中现代 heterogeneous-agent macro 的核心参数；
- 有方法贡献：直接恢复 latent distribution；
- 结果反驳“找到足够多的人口学变量就能理解 MPC heterogeneity”的隐含设想；
- 对 macro calibration 有直接含义。

### Lessons for us
这篇对我们的 ML 部分是一个非常重要的纪律：

**“41个特征预测力低”本身不是 contribution。**

因为顶刊已经明确告诉大家，MPC observables 的解释力可能本来就弱。

我们的更强空间是：

- latent heterogeneity 是否在不同 context 下以同一种方式显现？
- 如果在 context A 中识别到的 high responder，在 context B 中不再是 high responder，那么问题不只是“latent”，而是“latent heterogeneity 的 mapping 是否 context-dependent”。

这就是当前 cross-context portability / invariance 线相对于 Lewis et al. 的真正潜在增量。

---

## 1.5 Boehm, Fize & Jaravel (2025), American Economic Review  
### “Five Facts about MPCs: Evidence from a Randomized Experiment”

**Citation**  
Boehm, Johannes, Etienne Fize, and Xavier Jaravel. 2025. “Five Facts about MPCs: Evidence from a Randomized Experiment.” *American Economic Review* 115(1): 1–42.  
DOI: https://doi.org/10.1257/aer.20240138  
Official: https://www.aeaweb.org/articles?id=10.1257/aer.20240138

### Data
真实银行客户环境中的 randomized experiment，并结合：

- household bank accounts；
- card transactions；
- socioeconomic characteristics；
- liquidity / wealth information。

它不是 stated survey，而是我们必须面对的“真实转移形式”高标准 benchmark。

### Treatment
比较两种 transitory transfers：

1. cash-like transfer；
2. 通过一张卡发放、剩余资金三周后过期的 transfer。

经济资源都是短期刺激，但第二种有明显 form / expiration restriction。

### Findings
五个 headline facts 中最重要的：

- cash-like transfer 的 one-month MPC ≈ 23%；
- expiring-card transfer 的 MPC ≈ 61%；
- 61% vs 23% 与强 fungibility 假设难以一致；
- spending response 高度集中在最初几周；
- 即使 liquid wealthy，MPC 也不一定低；
- unconditional MPC distribution 很宽。

### Story
这是极强的 fungibility benchmark：

> 即使资源价值相近，transfer 的载体和可使用期限也会改变消费反应。

### Why publish in AER
- real money + randomized form；
- high-frequency transactions；
- clean timing；
- form manipulation 本身有理论意义；
- 直接挑战 macro models 中 money fungibility / standard MPC calibration。

### Lessons for us
我们的 cash / 6-month food voucher / long-horizon medical account在概念上非常接近“resource form matters”。

但必须诚实：

- 我们是 hypothetical stated spending；
- 他们是真实钱 + transaction data；
- 我们如果只证明 mean MPC across form differs，贡献远弱于这篇。

所以我们的必要增量是：**form 不只是改变 mean，还可能改变 heterogeneity structure / mapping / portability。**

---

## 1.6 Peersman & Wauters (2024), Energy Economics  
### “Heterogeneous household responses to energy price shocks”

**Citation**  
Peersman, Gert, and Joris Wauters. 2024. “Heterogeneous household responses to energy price shocks.” *Energy Economics* 132: 107421.  
DOI: https://doi.org/10.1016/j.eneco.2024.107421

### Data/design
在比利时 National Bank consumer survey 中嵌入 hypothetical energy-price-shock questions。

处理包括不同 sign 和 magnitude 的 monthly energy bill shock，例如：

- +€20；
- +€50；
- +€100；
- −€50。

然后问：

- 是否减少/增加 energy use；
- energy use 改多少；
- 支付能源账单后，其他消费和 saving 怎么变。

由此构造：

- contemplated price elasticity of energy demand；
- MPC after paying energy bill。

### Key contribution
它没有把 amount 仅当成“强度不同”，而是系统看：

- positive vs negative shock；
- small vs large shock；
- extensive vs intensive margin；
- household characteristics 对这些 slope/nonlinearity 的调节。

### Findings
- energy demand 对涨价和降价不对称；
- price elasticity 会随 price-shock magnitude 改变；
- household heterogeneity 在 price increase 下明显，在 price decrease 下弱很多；
- MPC 与 income、saving buffer、financial uncertainty、appetite to consume、household-head gender 等相关；
- 作者还比较了 targeting low-income households 的补贴与普遍 VAT reduction 对 non-energy consumption 的政策效果。

### Why publish
一个 hypothetical survey 被做成了“response function”论文：

**sign × size × extensive/intensive margin × household heterogeneity × policy counterfactual。**

### Lessons for us
这是 200/1000/5000 amount 维度最值得学习的文章之一。

Work 以后不能只报告“5000 的 treatment effect 比 200 大/小”。要测试：

- form effect 是否随 amount 非线性；
- amount 是否改变 extensive/floor/ceiling structure；
- X×form mapping 是否在 amount 不同的时候更稳定或更不稳定；
- 必须 formal test differences，而不是“一组显著、另一组不显著”。

---

## 1.7 Crossley, Fisher, Levell & Low (2023), Economics Letters  
### “Stimulus payments and private transfers”

**Citation**  
Crossley, Thomas F., Paul Fisher, Peter Levell, and Hamish Low. 2023. “Stimulus payments and private transfers.” *Economics Letters* 222: 110944.  
DOI: https://doi.org/10.1016/j.econlet.2022.110944

### Data/design
survey experiment，核心 hypothetical payment 是 **£500**。

随机改变一句信息：

- 一组只是问：如果你得到 £500；
- 另一组明确告诉你：**所有 households 都得到同样的 £500**（public windfall）。

其他经济资源基本相同。

### Finding
知道“别人也都拿到”的 public-windfall 组 MPC 高约 11%。

作者进一步利用 reported transfer intentions 解释机制：

- unspecified/private windfall 时，获得钱的人可能向其他更需要的 household 做 private transfer；
- 如果大家都得到 public payment，这种 private redistribution 被 crowd out；
- 因此自己消费比例提高。

### Story
非常值得我们学：

> 不是“framing 会影响 survey answer”，而是一个微小 context 信息改变了资源的社会意义，进而通过 private transfers 改变 MPC。

### Why publish
Economics Letters 篇幅很短，但逻辑闭环非常漂亮：

random wording → causal MPC difference → concrete mechanism。

### Lessons for us
cash / food / medical 的“形式”也可能携带：

- social meaning；
- earmarking；
- future security；
- perceived intended use；
- moral / normative cue。

所以“form effect”不应该被简化为纯物理预算约束。

同时，机制必须具体。单说“mental accounting”太宽。

---

## 1.8 Drescher, Fessler & Lindner (2020), Economics Letters  
### “Helicopter money in Europe: New evidence on the marginal propensity to consume across European households”

**Citation**  
Drescher, Katharina, Pirmin Fessler, and Peter Lindner. 2020. *Economics Letters* 195: 109416.  
DOI: https://doi.org/10.1016/j.econlet.2020.109416

### Data
第三轮 Eurosystem Household Finance and Consumption Survey（HFCS）。

- 17 European countries；
- 58,515 household observations with required data；
- harmonized household balance-sheet data；
- hypothetical lottery windfall = household 一个月的 net income；
- 问未来 12 个月会花掉多少比例。

### Findings
- 各国平均 MPC 大约 33%–57%；
- 回答在 0、50%、100% 有明显 mass points；
- MPC 随 income 上升而下降；
- wealth relationship 没那么清楚；
- country mean 和 country 内 distribution 都差异很大。

### Methods
强调：

- harmonized question；
- survey weights；
- household balance sheet；
- cross-country comparison；
- income/wealth distribution heterogeneity。

### Why publish
方法并不复杂，优势在数据：

- 17国；
- 统一问法；
- 代表性 household survey；
- 58k+；
- 完整 balance sheet；
- 处在疫情后“helicopter money”政策讨论的关键时间点。

### Lessons for us
如果 contribution 只是“不同人 MPC 不同”，必须有极强的数据规模/代表性/跨国优势才容易成立。

我们没有这个规模优势，因此必须靠 **设计和行为结构**，不能靠 descriptive heterogeneity。

---

## 1.9 Albuquerque & Green (2023), Journal of Macroeconomics  
### “Financial concerns and the marginal propensity to consume in COVID times”

**Citation**  
Albuquerque, Bruno, and Georgina Green. 2023. *Journal of Macroeconomics* 78: 103563.  
DOI: https://doi.org/10.1016/j.jmacro.2023.103563

### Data
representative UK household survey，hypothetical transfer = £500。

### Question
疫情期间，家庭对未来财务状况的担忧是否解释 MPC heterogeneity？

### Finding
担心未来“make ends meet”的家庭，reported MPC 大约高 20%；控制 liquidity constraints 等 household characteristics 后仍然有关系。

### Story
expectations / financial distress 是比静态 demographics 更有经济内容的 heterogeneity dimension，且有 targeting implications。

### Why publish
这是比较传统但完整的 field-journal paper：

- representative data；
- 清晰 macro question；
- 一个有经济机制的 predictor；
- policy targeting。

### Lessons for us
这类文章说明“找到一个 heterogeneity predictor”当然可以发表，但贡献上限与 ReStud/NHB 型文章不同。

我们的心理、经济预期变量最好作为解释 heterogeneity structure 的辅助证据，而不是把正文变成几十个 subgroup regressions。

---

# 2. Survey MPC 的 validity 与 measurement frontier

这一部分必须和上面一起读。它决定我们如何写“hypothetical stated MPC”。

## 2.1 Parker & Souleles (2019), AER: Insights  
### “Reported Effects versus Revealed-Preference Estimates: Evidence from the Propensity to Spend Tax Rebates”

**Citation**  
Parker, Jonathan A., and Nicholas S. Souleles. 2019. *American Economic Review: Insights* 1(3): 273–290.  
DOI: https://doi.org/10.1257/aeri.20180333

### Design
作者直接比较两种 measurement：

1. reported effect：问 household 政策让你改变了多少 spending；
2. revealed-preference estimate：利用 2008 US federal stimulus payments 的 quasi-random timing，从实际支出变化中推断 spending response。

### Findings
- self-reported spending response 更大的 household，也有更大的 revealed-preference response；
- 两种方法得到的 average propensity 相近；
- 但 liquidity 与 propensity 的关系在两种 measurement 下并不完全一致。

### Why important
这是 stated-MPC 文章经常引用的正面 validity evidence。

它说明：

**不能因为是 self-report 就自动认为没有行为信息。**

### Lesson for us
可以用来支持 stated response 的 informational content，但措辞必须克制：

- 它并不证明所有 hypothetical vignette 都能准确预测 actual spending；
- 它证明在一个真实 tax-rebate setting 中 reported and revealed measures 有相当程度的一致性，尤其在平均水平和排序方面存在支持性证据。

---

## 2.2 Ueda (2025), Economics Letters  
### “The reality of consumption: Comparing self-reported and observed marginal propensity to consume”

**Citation**  
Ueda, Kozo. 2025. *Economics Letters* 247: 112179.  
DOI: https://doi.org/10.1016/j.econlet.2025.112179

### Data
把 survey 与 **bank transaction data** 连起来，并利用实际 lump-sum transfer。

### Findings
- observed/actual MPC 显著为正，约 0.3；
- 但 individual-level self-reported MPC 与 observed MPC 之间没有显著关系。

### Story
这是 Parker–Souleles 的重要反向证据：在另一个制度、样本和 measurement setting 中，self-report 未必能恢复 individual actual MPC。

### Why publish
问题非常干净：

> survey MPC 到底测到了真实个人消费倾向吗？

银行交易数据让作者可以直接做 measurement validation。

### Lessons for us
这篇必须主动引用，而不是回避。

它尤其提醒：

- 不要把我们的 outcome 称为 realized MPC；
- 不要说“我们识别每个人真实的消费倾向”；
- 我们更安全、更准确的 construct 是 **stated consumption response under controlled transfer contexts**。

更有意思的是，如果 stated response 本身会随 context 系统变化，那么我们的贡献可以被定义为：

> 人们在资源呈现不同的情况下如何形成消费意向，以及个体差异是否能跨这些受控情境保持稳定。

这比声称预测银行卡支出更符合数据。

---

## 2.3 Crossley, Fisher, Levell & Low (2025), IFS/CEPR Working Paper  
### “Eliciting the Marginal Propensity to Consume in Surveys”

**Status**：working paper，不是已发表 journal benchmark。  
IFS WP 25/25. DOI: https://doi.org/10.1920/wp.ifs.2025.2525  
https://ifs.org.uk/publications/eliciting-marginal-propensity-consume-surveys

### Design
随机 survey experiment，比较不同 MPC elicitation wording：

- direct question；
- filtered question。

### Findings
只改变 question format，就可能让 mean MPC：

- 从低于 0.1；
- 到高于 0.5。

而且 wording 不只改变 mean，还改变：

- extensive margin；
- MPC 与 payment size 的关系；
- MPC 与 spending horizon 的关系；
- MPC 与 liquidity 的关系。

filtered format 得到的结果更接近 covariance-restriction approach。

### Why this matters enormously for us
这几乎直接告诉我们：

**“context 改变 heterogeneity mapping”有两种可能解释：真实行为构念变化，或者 measurement instrument 变化。**

因此当前 NHB_REVIEW_REANALYSIS 中的 exact vignette wording audit 是必要的，而不是编辑性细节。

### Required project response
Work 必须区分：

1. transfer form 真正改变 resource constraint / mental account；
2. 不同 form 的 vignette wording 自己改变了受访者对 outcome question 的理解；
3. cash/food/medical 是否在 validity horizon、allowed uses、future usability 等方面改变了 economic construct。

如果第三种尤其强，就应该把故事写成 **boundary conditions on behavioral portability**，而不是夸张成 universally unstable individual differences。

---

## 2.4 Pavlova (2025), JEBO  
### “Framing effects in consumer expectations surveys”

**Citation**  
Pavlova. 2025. *Journal of Economic Behavior & Organization* 231: 106899.  
DOI: https://doi.org/10.1016/j.jebo.2025.106899

### Data/design
德国代表性 sample，survey 内嵌 randomized experiment，分成四组。

作者系统操纵：

- “prices in general” vs “inflation rate”的 wording；
- probabilistic distribution format vs 更简单的 minimum / maximum / most-likely format。

### Findings
framing 会显著改变：

- mean expected inflation；
- individual uncertainty；
- distributional responses。

更简单的 wording 和较少限制的 format 往往带来更高的 expected inflation；不同 uncertainty elicitation 也会改变测量结果。

### Why publish in JEBO
这里 measurement 本身就是 behavioral object：

> consumer expectations 并不是一个完全独立于 measurement frame 的 latent number。

### Lessons for us
这是我们“context matters”故事的机会，也是威胁。

机会：context 可以重塑被 elicited 的 economic response，本身是行为事实。  
威胁：如果我们声称测量的是稳定真实 MPC，就会被反问是不是纯 wording artifact。

因此论文要把 construct 定义得准确。

---

# 3. JEBO / behavioral economics：form、framing、social meaning、mental accounts

## 3.1 Pauls & Laudi (2025), JEBO  
### “Temporal framing of tax stimuli and household consumption”

**Citation**  
Pauls, Thomas, and Marten Laudi. 2025. *Journal of Economic Behavior & Organization* 235: 107079.  
DOI: https://doi.org/10.1016/j.jebo.2025.107079

### Setting
真实政策背景：德国 solidarity surcharge abolition，给 household 带来永久性 disposable-income increase。

受访者来自一家大型德国 retail bank 的 clients。

主样本约 1,414；政策实施前 survey 后，约六个月后还做 ex-post follow-up，回访约 1,080 人（约 76% retention）。

### Randomized treatment
所有人面对本质相同的 individualized tax cut，但信息被随机呈现成：

- Euros per month；
- Euros per year；
- Euros per 10-year period。

也就是说，**经济资源不变，只改变 temporal frame。**

### Outcome
政策前：

- intended share spent；
- intended saving；
- intended debt repayment。

政策后约六个月：

- self-reported realized allocation。

### Findings
与 monthly framing 相比：

- yearly frame 的 intended spending share 低约 8.0 percentage points；
- 10-year frame 低约 9.4 pp；
- saving 相应更高；
- ex-post reported allocation 仍能看到接近的 pattern，而不是事前 intention 完全消失。

效果对较大的 tax cut 以及部分 financial-literacy / cognitive-reflection 维度也更明显。

### Story
同一永久收入增加，仅仅把它 mental representation 成“每月一点”或“十年很多”，就会改变 household 如何分配它。

这是非常干净的 mental accounting / scaling / framing 故事。

### Why publish in JEBO
这是与我们最接近的 JEBO benchmark：

- random framing；
- real policy anchored；
- individualized economic amount；
- pre-policy intention；
- six-month follow-up；
- realized self-report；
- heterogeneity 机制。

样本量不是巨大，说明 JEBO 并不要求 survey N 必须上万。

### Lessons for us
我们的 cash / food / medical 比“monthly/yearly/10-year”变化更大，所以 treatment effect 不奇怪。

真正值得学的是：

- 是否能找到“经济对象相同、representation 不同”的清晰表述；
- 是否能用 follow-up / second-wave validation 提高可信度；
- 如果现在不能 follow-up，就更需要 formal invariance + wording audit + theoretical boundary conditions。

---

## 3.2 Lee, Morduch, Ravindran & Shonchoy (2024), JEBO  
### “The social meaning of mobile money: Earmarking reduces the willingness to spend in migrant households”

**Citation**  
Lee, Jean N., Jonathan Morduch, Saravana Ravindran, and Abu S. Shonchoy. 2024. *Journal of Economic Behavior & Organization* 221: 675–688.  
DOI: https://doi.org/10.1016/j.jebo.2024.04.023

### Data/setting
Bangladesh migrant families：

- urban migrant workers；
- rural origin households；
- mobile money 在这里大量承载 remittance。

survey 被嵌入一个 broader dual-site experiment 中，能对 sender–receiver relationship 做更干净的控制。

### Experimental elicitation
随机让受访者考虑：

- 用 cash；
- 用 mobile money

购买一组 common goods，并 eliciting willingness to purchase / willingness to pay。

### Result
反直觉地，农村 household 使用 mobile money 时 willingness to spend **低 24%–31%**。

urban sample 中没有类似 payment effect。

### Mechanism
作者强调 mobile money 不只是“数字化的钱”。

在 rural receiving households 中，它与：

- migrant sender；
- remittance purpose；
- health / education / saving 等用途；
- social relationship

绑定，因此带有 earmark / social meaning。

### Story
**钱的载体会携带来源和用途的社会意义，因此经济上同样的钱并不完全 fungible。**

### Why publish
它不是“cash vs digital”平均差异，而是：

- 结果与 conventional payment-effect prediction 相反；
- rural vs urban pattern 提供 mechanism diagnostic；
- institutional setting 解释为什么 form 的含义不同；
- sociological “social meaning of money” 与 behavioral mental accounts 接起来。

### Lessons for us
这篇非常适合用在 Introduction 中解释：

> context 并不一定是表面 framing；资源的形式可能携带用途、来源、时间和社会意义，从而重塑消费反应。

food voucher / medical account 尤其具备明显 earmarking。

---

## 3.3 Jeworrek & Tonzer (2026), JEBO  
### “Inflation concerns and green product consumption: Evidence from a nationwide survey and a framed field experiment”

**Citation**  
Jeworrek, Sabrina, and Lena Tonzer. 2026. *Journal of Economic Behavior & Organization* 248: 107673.  
DOI: https://doi.org/10.1016/j.jebo.2026.107673

### Evidence chain
这篇很适合作为“如何把 survey 做厚”的模板。

**Stage 1: nationwide survey**
- Germany；
- almost 1,200 respondents；
- organic-food purchase 作为 green consumption proxy；
- stated organic purchasing 与 climate concern 正相关；
- 与 inflation concern 负相关；
- 后者主要由 below-median environmental attitude group 驱动。

**Stage 2: framed field experiment**
- 用 priming 随机提高 inflation concern salience；
- 同时可以区分纯 budget constraint 与心理 salience；
- 放松预算约束本身并没有显著改变 organic share；
- inflation priming 却降低了特定 subgroup 的 organic share。

**Stage 3: survey experiment**
- 约 1,800 respondents；
- 复现 inflation prime；
- 检验机制：organic 是否被视为 luxury、social norm 是否改变等。

RCT preregistered。

### Why publish
publication engine 是 **triangulation**：

correlation → causal experiment → mechanism experiment。

### Lessons for us
如果当前 survey 单次设计不足以完全支撑 NHB claim，最有价值的 future extension 往往不是加更多 ML，而是：

- 第二个 sample；
- 更精确的 context manipulation；
- mechanism-specific questions；
- validation / replication。

---

## 3.4 Guo, Tang, Xie & Yin (2025), JEBO  
### “Navigating fiscal fog: Household expectations in an uncertain fiscal environment”

**Citation**  
Guo, Junjie, Li Tang, Shihan Xie, and Penghui Yin. 2025. *Journal of Economic Behavior & Organization* 240: 107321.  
DOI: https://doi.org/10.1016/j.jebo.2025.107321

### Data
- 美国 households；
- 2024–2025 四轮；
- Prolific；
- 总样本超过 5,000。

### Design
large-scale online survey RCT：

- control：收到 hypothetical fiscal expansion 信息；
- treatment：同样的信息，但额外加入政策实施的不确定性。

### Outcomes
- expected government spending growth；
- subjective uncertainty；
- planned real consumption；
- open-ended narratives / beliefs。

### Findings
fiscal expansion news 会降低 planned private consumption；增加 policy uncertainty 后，这一 crowd-out 反而减弱，主要因为 household 对 government-spending growth 的预期更新更弱、posterior uncertainty 更高。

作者再把 survey evidence 与 stylized model / calibrated DSGE 联系起来。

### Why publish
survey 不停留在 stated consumption：

theory → testable hypotheses → randomized information → expectations → planned consumption → structural model。

### Lessons for us
如果我们想走更 economics 的路线，应该把：

- form effect；
- fungibility；
- context mapping

与一个明确的 behavioral model/null model 对起来。

例如直接定义 null：

**form 只改变截距，不改变 X→response mapping。**

然后用 X×form / cross-context portability 去检验。

---

## 3.5 Liscow & Pershing (2022), National Tax Journal  
### “Why Is So Much Redistribution In-Kind and Not in Cash? Evidence from a Survey Experiment”

**Citation**  
Liscow, Zachary, and Abigail Pershing. 2022. *National Tax Journal* 75(2): 313–354.  
DOI: https://doi.org/10.1086/719402

### Question
经济学家常强调 cash 给 recipient 更多 choice，但现实中政府 redistribution 很多是 in-kind。为什么公众支持这种设计？

### Survey experiment
一般公众在：

- cash transfer；
- 只能用于 necessities 的 in-kind transfer

之间做政策选择。

还加入关于“choice 的价值”的 persuasion treatment。

此外另有 below-poverty respondent sample，问 recipients 自己偏好什么。

### Findings
- general population 明显更偏好 in-kind；
- paternalistic reasons 很重要；
- persuasion treatment 会移动 preference，但没有完全逆转总体 pattern；
- below-poverty respondents 更偏好 cash；
- 但公众愿意支持更大的 in-kind transfer；
- 在“更大的 in-kind vs 更小的 cash”时 recipient preference 也可能改变。

### Why publish
这篇抓住一个大的 public-economics puzzle：

**理论上 cash choice-dominates，为什么实际制度大量选择 in-kind？**

survey experiment 用来解释制度偏好背后的 behavioral/paternalistic logic。

### Lessons for us
非常重要的一条：

**MPC/stimulus effect ≠ welfare/preference。**

如果 food voucher 比 cash 引发更高 stated consumption，我们不能写成“food voucher 更好”或“受访者更喜欢 food voucher”。

当前数据没有：

- cash equivalent；
- WTA/WTP；
- preference over transfer forms；
- welfare。

---

# 4. Real transfer / in-kind benchmark：用来界定我们能声称什么

## 4.1 Cunha (2014), AEJ: Applied Economics  
### “Testing Paternalism: Cash versus In-Kind Transfers”

**Citation**  
Cunha, Jesse. 2014. *American Economic Journal: Applied Economics* 6(2): 195–230.  
Official AEA article / DOI 可从 AEA 页面检索。

### Setting
墨西哥 food-assistance randomized experiment，直接比较：

- cash；
- in-kind food transfer。

### Core economics
区分一个极关键概念：

- 如果 in-kind transfer 对 household 原本就会购买的 food 是 inframarginal，它理论上不必扭曲预算选择；
- 如果对具体 item 是 extramarginal/binding，则可能改变消费组合。

### Findings/story
总体 food transfer 很多时候接近 inframarginal，但具体 goods 的 distortion 不同；消费 composition 变化并不自动转化成显著 health gains。

### Why publish
真实随机政策 + textbook economic concept（inframarginality）+ welfare-relevant outcome。

### Lessons for us
我们 SPEC 中 food baseline-spending / transfer-size ratio 的想法有明确先例。

但必须注意：

- 食品券 6 个月；
- baseline food spending 是月度分档；
- 所以 bindingness 只能做区间/边界敏感性分析；
- medical baseline expenditure 与 long-horizon medical account 更不匹配。

---

# 5. Nature Human Behaviour / Nature Portfolio：survey-based work 怎样跨过“只是问卷”的门槛

## 5.1 Gennetian et al. (2024), Nature Human Behaviour  
### “Effects of a monthly unconditional cash transfer starting at birth on family investments among US families with low income”

**Citation**  
Gennetian, Lisa A., Greg J. Duncan, Nathan A. Fox, Sarah Halpern-Meekin, Katherine Magnuson, Kimberly G. Noble, Hirokazu Yoshikawa, et al. 2024. *Nature Human Behaviour* 8: 1514–1529.  
DOI: https://doi.org/10.1038/s41562-024-01915-7

### Design
Baby’s First Years 类长期 randomized cash-transfer design。

四个美国 metropolitan areas 的低收入母亲，在 childbirth 后随机获得：

- high cash gift: $333 / month；
- low cash gift: $20 / month；

持续儿童出生后的最初若干年。

### Outcomes
前三年观察：

- child-specific goods；
- early-learning activities / parental time；
- core household expenditures；
- public-benefit receipt；
- poverty status；
- maternal employment；
- childcare；
- subjective well-being。

不少 expenditure/time measures 依赖 repeated survey reports，但 treatment 本身是真实、长期、随机的钱。

### Findings
high-transfer households：

- 更多 child-specific goods spending；
- 更多 child-specific early-learning activities；
- 其他 core household expenditures 变化不多；
- public-benefit receipt / poverty status 有部分变化；
- maternal paid work、childcare time、subjective well-being 等不少 outcome 没有显著变化。

### Story
核心不是“钱让消费上升多少”，而是一个基础 human-behaviour question：

> 长期、无条件的收入增加如何被低收入家庭转化成儿童投资、时间使用和家庭生活？

### Why NHB
- real, long-duration randomized income change；
- fundamental human-development question；
- multi-domain outcome；
- null results 也有理论信息；
- economics + psychology + child development + policy 跨学科。

### Lesson for us
NHB 并不要求所有 outcome 都显著。

“很多东西不变”可以是贡献，前提是它界定了一个重要行为结构。

因此我们若发现：

- 人的整体 rank/predictability 并不稳定；
- treatment sensitivity 也很难被 observables 捕捉；

这些“prediction fails”并非天然负面。但必须回答它们揭示了什么 **general human-behaviour principle**。

---

## 5.2 Stenlund et al. (2024), Communications Psychology  
### “How spending decisions shape happiness in everyday life”

**Citation**  
Stenlund, Säde, Yingchi Guo, Jason Rights, Ryan Dwyer, Elizabeth Dunn, et al. 2024. *Communications Psychology* 2: 124.  
DOI: https://doi.org/10.1038/s44271-024-00166-6

### Data-generating process
样本只有 **200 participants**，但数据极其特殊：

- 7 countries；
- 每人真的获得 $10,000；
- 需要在三个月内花掉；
- 持续填写 spending diaries；
- 每笔 purchase 写 description 和 happiness；
- baseline、3-month、6-month 还有 subjective well-being。

平均每人约：

- 16 purchases；
- 平均每笔约 $565；
- 主分析约 198 people / 3,083 purchases。

### Coding
open-ended purchases 由 independent coders 分类；

- 原始 26 类；
- 很少出现的 category 排除；
- 最终 17 个主要 spending categories；
- coder agreement 很高。

### Statistical method
random-intercept multilevel models：

- purchase = level 1；
- person = level 2。

关键是 **person-mean centering**。

作者不是比较“买体验的人 vs 还债的人谁更快乐”，而是：

> 对同一个人而言，他的一笔 experience spending 相比他自己的其他 spending，是否带来更高 happiness？

这样大量消除了 between-person confounding。

### Why publish
这是一个反例，说明 Nature Portfolio 并不机械追求 N 大：

- N=200 也可以；
- 但每个人真的拿 $10,000；
- repeated purchase-level observations；
- 真实自然消费；
- 多国；
- within-person design；
- data-generation 极难得。

### Lessons for us
我们现在 N≈5,497 并不意味着证据自动比 N=200 强。

Nature-style value 更看：

- data-generating process 是否独特；
- design 是否能回答一个干净的人类行为问题；
- 有没有 within-person / repeated / multimethod validation。

如果未来能做第二轮，**同一 respondent 跨 form 的 partial repeated design** 会极大增强“stable individual difference / portability”问题的识别。

---

## 5.3 Langlois & Chandon (2024), Communications Psychology  
### “Experiencing nature leads to healthier food choices”

**Citation**  
Langlois, Maria, and Pierre Chandon. 2024. *Communications Psychology* 2: 24.  
DOI: https://doi.org/10.1038/s44271-024-00072-x

### Design
不是一个超大 survey，而是 **5 个 between-subject experiments**：

- n=39；
- n=698；
- n=885；
- n=1,191；
- n=913；

总计约 3,726 participants，覆盖三个国家和不同情境。

### Variation
Study 1：
- 真实走 20 分钟 park vs city street；
- 之后真实 snack buffet；
- 记录实际 healthy/unhealthy consumption。

Studies 2–5：
- virtual / image nature vs urban/control；
- meal / food choices；
- incentive-compatible or more direct choice outcomes；
- mechanism tests。

online studies preregistered，并做 power analyses。

### Story
“nature exposure → healthier food choice”是一个非常简单、外行也立刻能懂的 proposition。

文章价值来自：

- field + online；
- real consumption + choice；
- different stimuli；
- multiple countries；
- multiple replications；
- mechanism/boundary checks。

### Why publish
Nature-family 很典型的 **convergent evidence** 结构：

一个简单命题，被不同 operationalization repeatedly supported。

### Lessons for us
如果要把“context reshapes individual differences”推成 NHB 风格，最理想的是：

- 不同 transfer contexts；
- 不同 amounts；
- 不同 model classes；
- 不同 metrics；
- adult-only / quality samples；
- 最好未来再有 independent sample / second experiment。

一个随机森林 heatmap 不够。

---

## 5.4 Fabre, Douenne & Mattauch (2025), Nature Human Behaviour  
### “Majority support for global redistributive and climate policies”

**Citation**  
Fabre, Adrien, Thomas Douenne, and Linus Mattauch. 2025. *Nature Human Behaviour* 9: 1583–1594.  
DOI: https://doi.org/10.1038/s41562-025-02175-9

### Data architecture
两层证据。

**Global survey**
- 40,680 respondents；
- 20 countries；
- 覆盖约 72% global CO2 emissions；
- 衡量对 global policies 的 stated support。

**Western follow-up surveys**
- 8,000 respondents；
- France, Germany, Spain, UK, USA；
- Europe 3,000；
- US wave 1 3,000；
- US wave 2 2,000。

### Why follow-up
作者知道“stated support”会被质疑：

- 真心支持还是 cheap talk？
- 知道个人成本后还支持吗？
- 有没有 bandwagon / design dependence？
- 背后的 rationale 是什么？

因此进一步做 survey experiments 检查 sincerity、cost salience、alternative designs 等。

### Why NHB
重要启示是：

**NHB 可以发表 stated preferences。**

但做法不是把 stated preference 假装成 realized political behavior，而是：

- 明确 construct；
- 超大跨国 scope；
- 用后续 experiments 验证其 sincerity / mechanism / boundary。

### Lessons for us
这给 stated MPC 的写法一个模板：

我们不必不断道歉“不是银行卡数据”，但必须：

- 准确定义为 stated allocation response；
- 对 measurement validity 提供现有证据；
- 对 alternative wording / construct interpretation 做 audit；
- 最好用第二种 evidence 做 validation。

---

## 5.5 Falchetta et al. (2024), Nature Communications  
### “Inequalities in global residential cooling energy use to 2050”

**Citation**  
Falchetta, Giacomo, Enrica De Cian, Filippo Pavanello, et al. 2024. *Nature Communications* 15: 7874.  
DOI: https://doi.org/10.1038/s41467-024-52028-8

### Data
大型 multi-country household survey microdata：

- n = 673,215 households；
- >500 subnational administrative units；
- 25 countries；
- 这些国家约占全球 62% population、73% electricity consumption。

household variables 包括：

- AC ownership；
- electricity expenditures / quantities where available；
- total household expenditure；
- socioeconomics。

再 merge：

- electricity prices；
- urbanization；
- meteorological / climate data。

### Method
训练 two-stage statistical models：

1. AC adoption；
2. conditional energy use / AC impact。

再推到 fine-spatial-resolution 2050 scenarios。

### Why publish
survey data只是 raw material，最后产物是：

- global harmonized micro database；
- global adoption/use model；
- future climate/energy projections；
- inequality implications。

### Lessons for us
Nature Communications 路线不是“把我们的一个中国问卷做更多 robustness 就够了”。

如果走 NC，通常需要至少一项很强的扩展：

- 新 generalizable measurement；
- external data linkage；
- broad population coverage；
- independent validation；
- policy/scenario projection；
- 或极具一般性的行为规律。

---

## 5.6 Zhong et al. (2026), Nature Communications  
### “Food-related energy consumption can help reveal poverty in rural Chinese households”

**Citation**  
Zhong, Ruohan, Jinjun Xue, Xinye Zheng, Chu Wei, Qian Sun, et al. 2026. *Nature Communications* 17: 9086.  
DOI: https://doi.org/10.1038/s41467-026-76026-0

### Data
China Residential Energy Consumption Survey（CRECS），nationwide household survey。

### Key innovation
作者不是简单做“能源消费与贫困相关”。

他们提出新指标：

**Energy Engel Coefficient (EEC)**  
= household energy used for food preparation / total household energy。

### Validation
检验 EEC 是否：

- 与 region / household characteristics 有合理 pattern；
- 比 traditional expenditure Engel coefficient 更符合 Engel’s Law；
- 与 total income/expenditure 关系更一致；
- 与 subjective poverty / experience 更一致；
- 与 asset ownership 更一致。

### Result
EEC 会识别出一批传统 Engel coefficient 漏掉的 poor households，尤其 rural、small、low-income households。

### Why publish
publication engine 是 **new measurement construct + multi-dimensional validation + policy classification gain**。

### Lessons for us
如果我们要提出 “fungibility trait” 或 “context portability index”，不能只是把 cash-food 差做个分数。

必须回答：

- construct definition；
- reliability；
- discriminant validity；
- predictive/criterion validity；
- 是否优于已有指标；
- 是否能在 independent outcome/context 中验证。

当前一人一个 treatment cell 的设计，对 individual latent fungibility trait **不够强**。

---

## 5.7 Piao & Managi (2023), Scientific Reports  
### “Household energy-saving behavior, its consumption, and life satisfaction in 37 countries”

**Citation**  
Piao, Xiangdan, and Shunsuke Managi. 2023. *Scientific Reports* 13: 1382.  
DOI: https://doi.org/10.1038/s41598-023-28368-8

### Data
- 37 countries；
- internet + face-to-face survey；
- 100,956 observations。

### Question/findings
研究 household energy-saving goods / behavior、energy expenditure、income/wealth、life satisfaction。

例如：
- wealth/income 与 energy expenditure 正相关；
- 27/37 countries 中 energy expenditure 与 life satisfaction 呈正关联；
- 不同 energy-saving action 的关系不同。

### Why include it
这是一个很好的“Nature Portfolio 下限/不同类型”参照。

它能发 Scientific Reports 主要靠：

- huge scale；
- 37-country breadth；
- sustainability question；
- systematic cross-country evidence。

它不是 NHB 那种高度识别行为机制的 paper。

### Lesson
不要把“Nature 系列”当成同一个标准。Scientific Reports、Communications Psychology、Nature Communications、Nature Human Behaviour 的 publication engine 很不一样。

---

# 6. 横向比较：这些文章到底靠什么发表？

把以上文献放在一起，可以看到至少七种 publication engine。

## Engine A — Theory-discriminating counterfactuals
代表：Fuster–Kaplan–Zafar 2021 ReStud。

survey 的价值不是“便宜收数据”，而是可以构造现实中难以观察的 counterfactual，借此排除理论。

**我们的对应问题：**
cash / food / medical / amount 能排除哪些关于 fungibility、bindingness、mental accounting、precautionary saving 的模型？

---

## Engine B — Real policy + randomized framing
代表：Pauls–Laudi 2025 JEBO。

同一笔真实收入 shock，被随机用不同 mental representation 呈现，随后还有 follow-up。

**我们的对应问题：**
我们 form 的变化能否被表达为“同一 underlying resource 在不同 context/representation 下的分配”？

但要承认 food/medical 并非完全经济等价，因为 restriction 和 horizon 真变了。

---

## Engine C — Form / restriction challenges fungibility
代表：
- Boehm–Fize–Jaravel 2025 AER；
- Crossley et al. 2023 Economics Letters；
- Lee et al. 2024 JEBO；
- Cunha 2014 AEJ Applied。

共同点：

**money is not behaviorally neutral once form/source/restriction/social meaning changes.**

我们的 form effect 本身有成熟文献基础，因此不能把“现金和消费券 MPC 不一样”当成新奇 discovery。

真正的增量必须更深。

---

## Engine D — Latent heterogeneity
代表：Lewis–Melcangi–Pilossoph 2026 ReStud。

传统 observables 解释力低已经是已知 frontier。

所以：

- low R²；
- demographics weak；
- SHAP values small；

都不能单独构成 headline contribution。

更有潜力的是：

> latent heterogeneity 是否在不同 contexts 中保持相同结构？

---

## Engine E — Measurement validation
代表：
- Parker–Souleles 2019 AER:I；
- Ueda 2025 Economics Letters；
- Crossley et al. 2025 working paper；
- Pavlova 2025 JEBO。

它们共同告诉我们：

**survey response 既可能包含真实行为信息，也可能高度依赖 elicitation。**

因此论文应该把 measurement problem 变成分析的一部分，而不是在 limitations 里一句带过。

---

## Engine F — Triangulation / convergent evidence
代表：
- Jeworrek–Tonzer 2026 JEBO；
- Langlois–Chandon 2024 Communications Psychology；
- Fabre–Douenne–Mattauch 2025 NHB。

一个 survey fact 可以变成高水平文章，但常见路径是：

survey fact → second experiment → mechanism / validation → replication across context。

---

## Engine G — Rare data or new global measurement
代表：
- Stenlund et al. 2024 Communications Psychology；
- Falchetta et al. 2024 Nature Communications；
- Zhong et al. 2026 Nature Communications；
- Piao–Managi 2023 Scientific Reports。

要么 data-generating process 极其稀缺，要么 scale 极大，要么创造并验证新的 measurement。

---

# 7. 对当前“消费调查”项目最重要的定位结论

## 7.1 哪些不是足够强的 headline contribution

根据现有文献，下面这些如果单独拿出来，都不够成为 NHB 级 headline：

### “不同 transfer form 的平均 stated MPC 不一样”
已经有大量 cash vs in-kind / expiring transfer / mobile money / framing 文献。

### “人的 MPC heterogeneity 很大”
Fuster、Jappelli-Pistaferri、Lewis、Boehm 等都已经非常明确。

### “人口学变量解释 MPC 很少”
Lewis et al. 2026 已经报告 observables 只解释约 8% 的 MPC variation。

### “随机森林预测得不太好”
这是统计事实，不等于行为理论贡献。

### “某几个 subgroup treatment effect 显著”
容易沦为 conventional HTE fishing。

---

## 7.2 当前最可能有新增量的问题

如果 re-analysis 支持，最有意思的是：

> **A person who appears highly consumption-responsive in one resource context need not be similarly responsive in another. Resource form may reshape not only average spending intentions but also the apparent mapping from individual characteristics to behavior.**

换成经济学 null：

> transfer form only changes an intercept / common mean response, while the person-level mapping X→Y stays invariant.

我们的分析就是检验这个 null。

### 对应 empirical objects
- 3×3 source-target portability matrix；
- matched training size；
- within-target benchmark；
- target-normalized portability gap；
- additive model vs X×form model 的 OOS improvement；
- flexible common model vs context-specific model；
- formal difference tests；
- amount-specific invariance；
- adult-only / quality-sample robustness。

这比“context predicts better than person”更精确，也更容易和 literatures 对话。

---

## 7.3 最关键的 boundary condition：cash/food vs medical

必须特别警惕 medical condition。

cash、food voucher、medical account 并非只是在标签上不同：

- allowed uses 不同；
- cash convertibility 不同；
- validity horizon 不同；
- food voucher 六个月；
- medical account 长期有效；
- medical account 可能被看作 future precautionary asset；
- baseline medical expenditure 与未来 medical need 的对应也更弱。

因此，如果结果是：

- cash ↔ food mapping 相对可迁移；
- medical 与另外两者差别大；

最合理的故事可能不是：

> “individual differences are generally unstable across context.”

而是：

> “Portability breaks when the resource representation changes the economic/psychological construct sufficiently—especially when a transfer becomes an earmarked, forward-looking precautionary account.”

这反而可能是更可信、更有机制的 boundary-condition paper。

---

# 8. Survey-data limitation 应该怎么写

## 不要这样写
“Although our outcome is hypothetical, prior research shows hypothetical MPC is valid.”

这太绝对，也会被 Ueda 2025 和 Crossley 2025 直接反击。

## 更准确的证据结构
1. Survey MPC 是成熟方法，Jappelli–Pistaferri、Fuster et al. 等高水平文章广泛使用；
2. Parker–Souleles 在 2008 tax-rebate setting 发现 reported 与 revealed measures 在平均值和 individual ranking 上存在支持性一致；
3. 但 Ueda 发现 self-reported 与 bank-transaction MPC 在其 setting 中 individual-level correspondence 不显著；
4. Crossley et al. 进一步表明 question wording 会显著改变 MPC distribution 和 heterogeneity relations；
5. 因此本项目不把 stated response 等同于 realized spending，而是研究 **controlled hypothetical resource contexts 下的 stated allocation response**；
6. 正因为 elicitation/context 可能改变 response，本项目的 cross-context invariance 问题本身具有 measurement 与 behavior 双重含义。

---

# 9. 如果后续再做一轮问卷，最值得补什么

按上述 benchmark，优先级不应该是“再加更多人口学 predictor”。

## Priority A — Repeated / within-person cross-context validation
如果伦理与设计允许，可让一部分 respondent 在足够间隔/随机顺序下回答多个 transfer forms，或做 panel follow-up。

目的：

- test-retest reliability；
- same-person cross-form rank stability；
- distinguish latent trait from between-cell sampling noise。

这是当前 latent-fungibility idea 最大的识别缺口。

## Priority B — Elicitation robustness
随机少量 wording / response-format variants，检查：

- direct amount vs category；
- filtered vs direct；
- question order；
- form description length；
- horizon wording。

这样可以直接回应 Crossley/Pavlova measurement critique。

## Priority C — Mechanism-specific measures
少而精准地测：

- perceived earmarking；
- perceived fungibility；
- intended-use norm；
- liquidity/security；
- anticipated future medical need；
- bindingness perception；
- account salience。

不要加几十个泛心理量表。

## Priority D — External criterion
如果可能，加入：

- later reported actual spending；
- transfer preference / cash equivalent；
- incentivized small-stakes allocation；
- independent consumption/saving outcome。

哪怕只在 subsample 上做，也能显著增强 construct validity。

---

# 10. Work 以后每次提出新 story 时必须回答的 checklist

1. **这个 story 相对 Bernard 2023 的 payment-mode × size × stated-MPC × causal-HTE 设计到底多了什么？这是第一优先级 novelty check。**
2. 这个 story 相对 Fuster 2021 多了什么？
3. 相对 Lewis 2026 的“latent heterogeneity”多了什么？
4. 相对 Pauls–Laudi 2025 的“context/framing changes spending”多了什么？
5. 相对 Boehm–Fize–Jaravel 2025 的“form violates fungibility”多了什么？
6. survey validity 是否同时面对 Parker–Souleles、Ueda、Crossley 三组证据？
7. 结果是在解释 **mean effect**、**prediction**、**HTE**、**portability** 还是 **construct invariance**？不要混用。
8. 是否有一个明确 null model 被拒绝？
9. 是否 formal test “difference in differences / mapping difference”，而不是比较显著性星号？
10. medical condition 是否改变了 economic construct，而不仅是 context label？
11. 如果 headline 只剩“R²低”，就继续找更有结构的问题，不要包装统计失败。
12. 如果 headline 是“稳定 mapping 只在相近 context 中成立”，这是 boundary condition，不必强行写成 universal instability。
13. 对 NHB，要问：外行能否用一段话理解“为什么这个 human-behaviour fact 重要”？
14. 对 JEBO，要问：random context manipulation + mechanism + economic implication 是否已经闭环？
15. 对 Nature Communications，要问：是否有 generalizable measurement / large-scale external validation / projection，不要只靠同一份问卷加方法。
16. 每次图表更新都应优先展示可解释的 behavioral structure，而不是堆 feature-importance plots。

---

# 11. 建议的核心引用组合

## Stated MPC is established but must be carefully interpreted
- Jappelli & Pistaferri 2014, AEJ Macro
- Fuster, Kaplan & Zafar 2021, ReStud
- Parker & Souleles 2019, AER: Insights
- Ueda 2025, Economics Letters
- Crossley et al. 2025, IFS WP

## Closest direct predecessor
- **Bernard 2023, Deutsche Bundesbank Discussion Paper — payment mode × shock size × stated MPC × mental accounting × causal forest HTE**

## MPC heterogeneity frontier
- Jappelli & Pistaferri 2020, AEJ Economic Policy
- Lewis, Melcangi & Pilossoph 2026, ReStud
- Peersman & Wauters 2024, Energy Economics

## Fungibility / transfer form / social meaning
- Boehm, Fize & Jaravel 2025, AER
- Crossley et al. 2023, Economics Letters
- Lee et al. 2024, JEBO
- Pauls & Laudi 2025, JEBO
- Cunha 2014, AEJ Applied
- Liscow & Pershing 2022, National Tax Journal

## Survey framing / measurement
- Pavlova 2025, JEBO
- Crossley et al. 2025, IFS WP

## Nature-family design benchmarks
- Gennetian et al. 2024, Nature Human Behaviour
- Stenlund et al. 2024, Communications Psychology
- Langlois & Chandon 2024, Communications Psychology
- Fabre, Douenne & Mattauch 2025, Nature Human Behaviour
- Falchetta et al. 2024, Nature Communications
- Zhong et al. 2026, Nature Communications
- Piao & Managi 2023, Scientific Reports

---

# 12. Bottom line for this project

这批文献给出的最清楚结论是：

**survey / hypothetical MPC 并不会自动限制期刊档次；但“survey 本身”也不会贡献档次。**

高水平文章通常至少做到了下面一件：

- 让 survey counterfactual 区分理论；
- 让 randomized framing 对应明确经济机制；
- 把 stated response 与 revealed behavior / follow-up 验证；
- 用真实政策/真实钱增强 external relevance；
- 提出 latent heterogeneity 的新识别；
- 在多个 study/context 中复制；
- 创造并验证一个新 measurement；
- 或把 household microdata 扩展到全球/宏观含义。

对我们而言，最值得继续验证的不是：

> “现金、食品、医疗的 MPC 不一样。”

而是：

> **同一人的“行为类型”究竟有多大程度可以从一个经济上相近的资源情境迁移到另一个？所谓 individual heterogeneity 是稳定地属于 person，还是部分由 person × context 共同生成？**

如果数据只支持 cash-food 较稳定、medical 显著不同，也不要把它视为故事失败。它可能给出更精确的理论边界：

> **individual differences can be portable across nearby resource contexts, but portability weakens when the transfer changes from a near-cash spending resource into a strongly earmarked, forward-looking account.**

这比“所有 context 都让人变得不可预测”更可证伪，也更能与 fungibility、mental accounting、person–situation 和 measurement literatures 对话。

---

# 13. Sources checked for this benchmark

以下为本轮优先核对的官方出版页/研究机构页，Work 后续若需要精确数字、表格或补充材料，应优先回到这些原始页面，而不是依赖本文件的摘要。

- Bernard 2023, Bundesbank: https://www.bundesbank.de/en/publications/research/discussion-papers/mental-accounting-and-the-marginal-propensity-to-consume-909438
- Bernard 2023, SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4537003
- Fuster, Kaplan & Zafar, ReStud: https://academic.oup.com/restud/article/88/4/1760/5962017
- NY Fed Staff Report: https://www.newyorkfed.org/research/staff_reports/sr843
- Jappelli & Pistaferri 2014, AEA: https://www.aeaweb.org/articles?id=10.1257/mac.6.4.107
- Jappelli & Pistaferri 2020, AEA: https://www.aeaweb.org/articles?id=10.1257/pol.20180420
- Parker & Souleles 2019, AEA: https://www.aeaweb.org/articles?id=10.1257/aeri.20180333
- Lewis, Melcangi & Pilossoph, ReStud: https://academic.oup.com/restud/article/doi/10.1093/restud/rdaf102/8489895
- Boehm, Fize & Jaravel 2025, AEA: https://www.aeaweb.org/articles?id=10.1257/aer.20240138
- Pauls & Laudi 2025, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0167268125001982
- Crossley et al. 2023, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0165176522004189
- Crossley et al. 2025, IFS: https://ifs.org.uk/publications/eliciting-marginal-propensity-consume-surveys
- Ueda 2025, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0165176525000163
- Peersman & Wauters 2024, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0140988324001294
- Lee et al. 2024, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0167268124001586
- Pavlova 2025, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0167268125000198
- Jeworrek & Tonzer 2026, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S016726812600260X
- Guo et al. 2025, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S016726812500438X
- Liscow & Pershing 2022: https://www.journals.uchicago.edu/doi/10.1086/719402
- Gennetian et al. 2024, NHB: https://www.nature.com/articles/s41562-024-01915-7
- Stenlund et al. 2024, Communications Psychology: https://www.nature.com/articles/s44271-024-00166-6
- Langlois & Chandon 2024, Communications Psychology: https://www.nature.com/articles/s44271-024-00072-x
- Fabre et al. 2025, NHB: https://www.nature.com/articles/s41562-025-02175-9
- Falchetta et al. 2024, Nature Communications: https://www.nature.com/articles/s41467-024-52028-8
- Zhong et al. 2026, Nature Communications: https://www.nature.com/articles/s41467-026-76026-0
- Piao & Managi 2023, Scientific Reports: https://www.nature.com/articles/s41598-023-28368-8
