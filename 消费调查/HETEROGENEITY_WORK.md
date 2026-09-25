# 消费调查项目 — Heterogeneity Exploration Work Instructions

## 0. Objective

基于现有调查数据，对 stated marginal propensity to consume（stated MPC）及 transfer fungibility 的异质性做一次系统、可复现、尽量不受单一故事驱动的探索。

本阶段的目的不是立即写论文，也不是挑显著结果。

本阶段只回答：

1. 哪些 baseline economic characteristics 系统性预测 stated MPC？
2. 哪些 baseline subjective / social-attitude characteristics 系统性预测 stated MPC？
3. 哪些特征系统性改变 cash / food / medical 三类 transfer 的消费反应差异？
4. 哪些特征系统性改变“fungibility gap”：
   - food vs cash；
   - medical vs cash；
   - restricted transfer vs cash；
5. theory-guided 线性模型与 data-driven ML heterogeneity 是否指向相似的人群和变量？
6. 哪些结果在不同 outcome coding、样本口径、模型与 multiple-testing correction 下仍然稳定？
7. 最终哪些异质性事实足够强，值得发展成论文故事？

先阅读：
- `消费调查/SPEC.md`
- `消费调查/DATA_AUDIT.md`
- `消费调查/FIRST_LOOK.md`

把前三份文件视为事实基础和证据纪律。

---

# 1. General discipline

## 1.1 不预设故事

不要假定：
- liquidity 一定最重要；
- mental accounting 一定存在；
- restricted transfer 一定提高或降低 MPC；
- social attitudes 一定有解释力；
- medical account 一定代表 precautionary saving。

允许数据告诉我们：
- 某些理论变量几乎没有解释力；
- 某些原本被认为“次要”的变量反而稳定；
- cash、food、medical 的异质性来源完全不同。

## 1.2 区分三种对象

必须严格区分：

### A. Level heterogeneity

谁的 stated MPC 本身更高？

例如：
[
E[Y_i|X_i]
]

这主要是相关性问题。

### B. Treatment-effect heterogeneity

某个 baseline characteristic 是否改变 randomized transfer form / amount 对 outcome 的处理效应？

例如：
[
E[Y_i(food)-Y_i(cash)|X_i=x]
]

由于 treatment 是随机的，这类 conditional treatment-effect heterogeneity 有因果解释空间，但 baseline X 本身并不是随机的。

### C. Fungibility heterogeneity

重点对象不是某类人的 MPC 高低，而是：

[
Delta_i^{food}=Y_i(food)-Y_i(cash)
]

以及：

[
Delta_i^{medical}=Y_i(medical)-Y_i(cash)
]

以及必要时：

[
Delta_i^{restricted}
=Y_i(restricted)-Y_i(cash)
]

这些 conditional contrasts 是本阶段最重要的对象。

---

# 2. Outcomes

## 2.1 Primary outcome

主 outcome 保持原始 6 档：

- 1 = 基本不额外消费；
- 2 = <10%；
- 3 = 10–25%；
- 4 = 25–50%；
- 5 = 50–75%；
- 6 = >75%。

变量：`outcome_ord`。

任何 headline heterogeneity 都必须首先在原始 ordered outcome 上能够看见。

## 2.2 Secondary continuous approximation

使用既有：
- 1 → 0
- 2 → 0.05
- 3 → 0.175
- 4 → 0.375
- 5 → 0.625
- 6 → 0.875

构造 `mpc_midpoint`。

只用于：
- 量级直观化；
- 线性模型；
- ML。

不要把小数点解释成真实 realized MPC。

至少保留 alternative top coding：
- category 6 → 1.0

并检查核心排序与 HTE 是否改变。

## 2.3 Useful binary / threshold outcomes

为检验 floor concentration 是否驱动结果，额外构造：

- `any_spend`: outcome > 1
- `mpc_10plus`: outcome >= 3
- `mpc_25plus`: outcome >= 4
- `high_mpc`: outcome >= 5

这些是 robustness outcomes，不是主 outcome。

若某项异质性只在单一阈值下出现，不应视为强事实。

---

# 3. Treatment objects

构造并固定：

- `transfer_type`: cash / food / medical
- `amount`: 200 / 1000 / 5000
- `treatment_cell`: 9 cells

核心 treatment contrasts：

1. food - cash
2. medical - cash
3. restricted (food + medical) - cash
4. medical - food

amount-specific contrasts：

- food200 - cash200
- food1000 - cash1000
- food5000 - cash5000
- medical200 - cash200
- medical1000 - cash1000
- medical5000 - cash5000

原则：

- pooled contrasts 用于提高 precision；
- amount-specific contrasts 用于发现异质性结构；
- 不因单金额显著而忽略 pooled / joint evidence。

---

# 4. Baseline variable inventory

先建立 `tables/heterogeneity_variable_map.csv`。

对所有候选 baseline variables 记录：

- variable name
- questionnaire item
- concept/domain
- type: continuous / ordinal / categorical / binary
- missingness
- coding
- transformation
- whether used in main theory-guided analysis
- whether used only in exploratory ML

不得直接把所有题“原样扔进回归”。

---

# 5. Economic-domain grouping

至少按以下经济学维度整理变量。

## 5.1 Objective / quasi-objective economic conditions

优先包括：

- age
- gender
- education
- monthly income
- hukou
- employment status
- work-unit type
- housing tenure
- children
- household size
- food spending
- medical spending
- prior subsidy experience
- province / city tier（适当编码，不要制造大量稀疏 dummy）

建议形成子类：

### Economic resources
- income
- education
- employment
- housing

### Household needs
- household size
- children
- food spending
- medical spending

### Institutional / labor-market position
- hukou
- work status
- work-unit type
- city tier

## 5.2 Subjective economic state

优先包括：

- Q6 social protection
- Q7 emergency liquidity
- Q9 sense of gains from development
- Q10 effort can improve life
- Q11 upward mobility
- Q13 pressure affordability
- Q15 future self
- Q17 economic development
- Q17 employment/income
- Q17 prices/affordability
- Q18 subjective socioeconomic position
- Q19 past mobility
- Q20 expected future position

建议形成子类：

### Liquidity / resilience
- Q7
- income
- housing
- employment

### Perceived protection / economic security
- Q6
- Q13
- medical spending
- employment status

### Expectations / permanent-income beliefs
- Q15
- Q17 economy
- Q17 employment/income
- Q17 prices
- Q20

### Subjective socioeconomic position / mobility
- Q18
- Q19
- Q20
- Q10
- Q11

## 5.3 Broader social attitudes

包括但不限于：

- life satisfaction
- safety
- fairness dimensions
- government/public institution trust
- generalized trust
- social support
- voice/response
- national outlook
- order
- vitality

这些变量可以探索，但要与 economic-state block 分开。

目标之一正是比较：

> stated MPC / fungibility heterogeneity 更主要由客观经济约束解释，还是由主观经济状态 / broader social attitudes 解释？

不要把所有 Q1–Q22 合成一个无解释力的“social mindset index”。

---

# 6. Data preprocessing

## 6.1 Continuous / ordinal variables

- 保留原始 coding；
- 另生成 z-score 版本用于 interaction coefficient 可比性；
- 明确变量方向，使更高值尽量具有清楚含义。

## 6.2 Categorical variables

- 使用合理 dummy / one-hot encoding；
- 小 cell 合并时必须记录规则；
- 避免 province × many-category 造成严重维度膨胀。

## 6.3 Missingness

当前大部分变量无 item missing。

如果后续衍生变量产生 missing：
- 报告 N；
- 不默认均值填补；
- ML 若需要 imputation，使用训练折内部 imputation，避免 leakage。

## 6.4 Straight-liner / age concerns

主分析：
- raw N=5,497

稳健性：
- clean candidate N=5,171

核心异质性至少在这两套样本上对照。

---

# 7. Descriptive heterogeneity before modeling

在复杂模型前，先做简单描述。

## 7.1 Outcome levels

对每个重要 baseline variable：

- 分位数组 / 合理组别；
- 报 cash / food / medical 三类 mean outcome；
- 报 95% CI；
- 报样本量。

重点变量至少包括：
- income
- Q7 liquidity
- Q6 protection
- Q15 future self
- Q17 employment/income
- subjective SES
- food spending
- medical spending
- age
- education

## 7.2 Fungibility-gap plots

对每个重要 baseline variable，画：

[
Food-Cash
]

以及：

[
Medical-Cash
]

的 conditional treatment-effect plot。

优先使用：
- terciles / quartiles；
- 或 continuous marginal-effect plot。

不要用过细 bins。

---

# 8. Theory-guided linear / generalized-linear models

## 8.1 Baseline model

对 continuous approximation：

[
Y_i = alpha + T_i + A_i + T_i 	imes A_i + epsilon_i
]

其中：
- T = transfer type
- A = amount

先复现 reduced-form。

## 8.2 One-variable-at-a-time HTE

对每个 baseline X：

[
Y_i =
alpha
+ T_i
+ A_i
+ X_i
+ T_i 	imes X_i
+ A_i 	imes X_i
+ T_i 	imes A_i
+ epsilon_i
]

必要时加入：
[
T_i 	imes A_i 	imes X_i
]

但三重交互只作为 exploratory，且必须报告 precision。

对每个 X 提取：

- cash slope / association
- food-cash HTE
- medical-cash HTE
- restricted-cash HTE

统一输出 effect + SE + 95% CI + p-value + q-value。

## 8.3 Domain models

按经济学 domain 分块进入：

Model E1: objective economic conditions

Model E2: liquidity / resilience

Model E3: expectations / permanent-income beliefs

Model E4: protection / precautionary motives

Model E5: baseline needs

Model S1: broader social attitudes

然后比较：
- incremental R²
- cross-validated predictive performance
- treatment-interaction explanatory power
- joint Wald tests

重点回答：

> 哪一类变量解释 outcome level？
> 哪一类变量解释 treatment-effect heterogeneity？
> 哪一类变量解释 fungibility gap？

## 8.4 Full regularized interaction model

构造：

[
Y_i =
alpha + T_i + A_i + X_i + T_i X_i + A_i X_i
]

使用：
- ridge
- lasso
- elastic net

通过 nested / cross-validation 选 penalty。

不要用同一样本既选变量又报告 naive classical p-values。

regularized model 主要用于：
- 稳定筛选；
- 预测；
- 与 ML 对照。

---

# 9. Ordered-outcome robustness

主 HTE 若主要基于 midpoint OLS，需要在 ordered outcome 上验证方向。

至少：

- ordered logit / probit
- proportional-odds model
- 若 proportional odds 明显失效，报告并考虑 generalized ordered model

重点不是解释所有 latent-index coefficient，而是看：
- heterogeneity sign
- ranking
- predicted probability shifts

是否与 linear approximation 一致。

---

# 10. Multiple testing control

这是本项目非常重要的纪律。

对 one-variable-at-a-time heterogeneity：

- 同一 family 内报告 raw p；
- Benjamini-Hochberg FDR q-values；
- 标明 family definition：
  - objective economic
  - subjective economic
  - broader social attitudes
  - baseline needs

不要把 raw p<0.05 当成 strong fact。

最终 strong heterogeneity 至少满足：
- effect 有明确经济量级；
- 方向在多种 outcome coding 下稳定；
- raw vs clean sample 稳定；
- 最好 FDR 后仍有证据；
- theory-guided 与 ML 至少部分一致。

---

# 11. Machine-learning exploration

目标不是用机器学习“替代经济学”，而是尽量少先验地回答：

> baseline X 中，到底有哪些变量稳定预测 stated MPC level 与 treatment-effect heterogeneity？

## 11.1 Prediction of MPC level

先做纯预测：

[
Y_i = f(X_i)
]

不包含 treatment 或单独分 treatment 估计均可。

模型至少比较：

- linear / ridge baseline
- random forest
- gradient boosting / XGBoost or HistGradientBoosting

使用 repeated K-fold CV。

报告：
- out-of-sample R² / RMSE
- permutation importance
- partial dependence / ALE for top variables

不要把 SHAP/importance 自动解释为因果。

## 11.2 Treatment-effect heterogeneity

优先采用适合 randomized treatment 的 honest / cross-fitted 方法。

### Binary contrasts

分别构造：

A. food vs cash sample
B. medical vs cash sample
C. restricted vs cash sample

对每个 contrast 估计 CATE：

[
	au(x)=E[Y(1)-Y(0)|X=x]
]

优先方法：

- causal forest / generalized random forest if available
- DR-learner / R-learner as robustness
- honest sample splitting
- cross-fitting

由于 treatment 已随机，propensity 可使用设计概率 / sample probability；不要无必要地复杂建模 propensity。

### Multi-treatment

若环境支持，可额外使用 multi-treatment causal forest / generalized random forest。

但 binary contrasts 是主版本，更容易解释和诊断。

## 11.3 Honest evaluation

对 ML CATE：

- train/test 或 cross-fitting；
- 不在训练集上展示“发现的异质性”；
- 做 calibration / best linear predictor；
- 将预测 CATE 分成 quintiles；
- 在 held-out data 中比较 top vs bottom CATE groups 的实际 treatment contrasts。

必须报告：
- group N
- treatment balance
- effect
- CI

这一步比 variable importance 更重要。

## 11.4 Variable importance for HTE

输出：
- top variables for food-cash CATE
- top variables for medical-cash CATE
- top variables for restricted-cash CATE

并按 domain 汇总。

检查：
- objective economic variables 是否占主导；
- subjective economic variables 是否增加明显信息；
- broader social attitudes 是否有 incremental value。

---

# 12. “Fungibility” 的操作化

现有数据不能直接观察个人对 cash 和 food/medical 的两个潜在结果。

因此不要构造个体级 observed fungibility gap。

“fungibility heterogeneity”必须定义为：

[
	au_{food-cash}(x)
=
E[Y(food)-Y(cash)|X=x]
]

以及：

[
	au_{medical-cash}(x)
=
E[Y(medical)-Y(cash)|X=x]
]

这是 conditional average treatment-effect object。

## 12.1 Food fungibility

特别关注：
- baseline food spending
- household size
- children
- income
- liquidity
- subjective SES
- expectations

保留既有 clearly inframarginal / ambiguous / likely binding 分类。

新增：
- 在 clearly inframarginal sample 内重复全部核心 HTE 搜索；
- 但不要在 N 很小的 binding group 中过度解释。

核心问题：

> 哪些 baseline traits 预测 “即使 restriction 不 binding，food 仍不像 cash”？

## 12.2 Medical fungibility

特别关注：
- past medical spending
- age
- children
- household size
- perceived social protection
- liquidity
- employment
- income
- future expectations

避免把 past OOP spending 当成严格 bindingness measure。

核心问题：

> 哪些人把 medical-account transfer 的当前消费反应处理得最不像 cash？

---

# 13. Comparing objective conditions vs subjective states

这是本阶段必须专门回答的问题。

建立至少四套 predictive / heterogeneity feature sets：

### Set O
只有 objective / quasi-objective variables：
- demographics
- income
- employment
- housing
- household composition
- food / medical spending
- hukou
- city tier

### Set S
只有 subjective economic-state variables：
- liquidity perception
- protection
- expectations
- subjective SES / mobility
- pressure

### Set A
只有 broader social-attitude variables：
- trust
- fairness
- safety
- order
- vitality
- life satisfaction
- social support
- voice

### Set ALL
全部 pre-treatment covariates

比较：

1. prediction of stated MPC level
2. prediction / calibration of food-cash CATE
3. prediction / calibration of medical-cash CATE

报告：

- O 是否已经解释大部分？
- S 是否在 O 之外有 incremental predictive value？
- A 是否仍有 incremental value？
- 哪些 subjective variables 提供了 objective data 无法提供的信息？

不要只比较 in-sample R²；优先 out-of-sample performance。

---

# 14. Dimension reduction / indices

可以探索，但不要机械 PCA 后就拿 PC1 当“心态”。

允许：

- standardized domain indices
- PCA within a clearly defined domain
- factor analysis for highly correlated expectation / social-attitude items

但每个 index 必须：
- 有明确变量组成；
- 解释方差；
- 方向可解释；
- 与简单平均 index 对比。

若 PCA/factor 没有明显优势，优先使用简单、透明的 standardized average。

---

# 15. Robustness grid

所有 top findings 至少在以下维度做 robustness：

## Sample
- raw
- clean candidate

## Outcome
- ordinal score 1–6
- midpoint MPC
- alternative top coding
- any_spend
- 25%+ threshold

## Controls
- no controls
- minimal pre-specified controls
- domain/full controls

## Functional form
- linear interaction
- ordered model
- ML CATE / held-out subgroup validation

## Treatment aggregation
- pooled food-cash / medical-cash
- amount-specific contrasts

结果若高度依赖某一个 specification，标记为 fragile。

---

# 16. Deliverables

创建：

- `消费调查/HETEROGENEITY_AUDIT.md`
- `消费调查/HETEROGENEITY_RESULTS.md`
- `消费调查/analysis/heterogeneity_analysis.py` 或其他可复现脚本
- `消费调查/tables/heterogeneity_*.csv`
- `消费调查/figures/heterogeneity_*.png`

## 16.1 HETEROGENEITY_AUDIT.md

写：
- variables
- domains
- transformations
- model classes
- sample definitions
- multiple-testing plan
- CV / sample-splitting design
- known limitations

## 16.2 HETEROGENEITY_RESULTS.md

不要按“跑了哪些回归”组织。

必须按研究问题组织：

### A. Who has a high stated MPC?
- strongest objective predictors
- strongest subjective predictors
- incremental value of subjective information

### B. Who responds differently to transfer form?
- strongest food-cash HTE
- strongest medical-cash HTE
- amount dependence

### C. Who treats a yuan as a yuan?
- strongest fungibility-heterogeneity facts
- especially clearly inframarginal food sample

### D. Objective conditions vs subjective states
- O / S / A / ALL predictive comparison

### E. Theory-guided vs ML
- where they agree
- where they disagree

### F. Robustness
- stable
- fragile
- null

---

# 17. Final synthesis format

报告最后必须给出以下内容。

## 17.1 Top 10 raw findings

不评价“论文价值”，只给事实。

每条：
- variable / subgroup
- outcome
- treatment contrast
- effect size
- CI
- N
- robustness note

## 17.2 Strong heterogeneity facts

只有满足多数以下条件才能进入：
- reasonable N
- economically meaningful effect
- stable raw / clean
- stable across outcome coding
- not purely one-threshold result
- survives or is reasonably robust to multiple testing
- supported by held-out ML / theory-guided consistency

## 17.3 Interesting but fragile

专门列：
- p<0.05 但 FDR 后消失
- single specification only
- small subgroup
- ML-only discovery not confirmed out of sample

## 17.4 Important nulls

必须报告理论上本来可能重要但实际没有稳定解释力的变量。

例如：
- Q6 social protection
- Q7 liquidity
- expectations
- trust / fairness

若它们真是 null，不要隐藏。

## 17.5 Candidate story clusters

不要写论文 introduction。

只允许把 stable facts 聚类成最多 3–5 个“候选故事簇”，例如：

- liquidity / financial resilience
- baseline need / bindingness
- expectations / precautionary motives
- subjective socioeconomic insecurity
- broader social mindset

每个故事簇说明：
- 支持它的事实
- 反对它的事实
- 目前最大识别缺口

## 17.6 Bottom-line memo

最后只回答：

1. stated MPC 的异质性主要由什么解释？
2. food-cash fungibility heterogeneity 主要由什么解释？
3. medical-cash fungibility heterogeneity 主要由什么解释？
4. subjective variables 相对于 objective economics variables 有没有额外解释力？
5. 哪些结果最值得下一步写成 paper story？
6. 哪些原本看似重要的故事应当放弃？

---

# 18. Interpretation limits

始终明确：

- outcome 是 hypothetical stated MPC，不是 realized spending；
- respondent-level CATE 无法直接观察，只能估 conditional average treatment effects；
- baseline X 的系数 / HTE pattern 不意味着 X 本身有因果作用；
- ML feature importance 不是 causal mechanism；
- fungibility 在本文是 transfer-form consumption-response equivalence，而不是直接 welfare valuation；
- 没有 cash equivalent / WTP / utility measurement，因此不能声称“某种钱价值更低”；
- 没有实际消费明细，因此不能分析 expenditure composition；
- 外部有效性受平台样本年轻、高学历影响。

本阶段的任务不是证明一个故事，而是把数据中真正稳定的异质性结构完整地找出来。
