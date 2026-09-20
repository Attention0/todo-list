# 消费调查项目 — Initial Data Audit / Work Instructions

## Objective

对“社会心态小调查”的实际交付数据做第一轮严格数据审计和最小化 exploratory analysis，为 Chat 与研究者判断 JDE-level 研究方向提供事实基础。

先阅读 `消费调查/SPEC.md`，把它作为当前研究问题和证据纪律的 source of truth。

本轮 **不要追求大量回归，也不要先写论文故事**。第一目标是确认数据质量、随机化、变量含义和最基本 treatment patterns。

---

## 0. 找到并记录实际数据

在可访问的工作环境中定位：
- 原始调查交付 Excel / CSV / dta 等；
- 变量标签或 codebook；
- 问卷文字版；
- 平台导出说明；
- 已有清洗代码；
- 已有分析代码；
- 已有表格/图形/报告。

不要修改原始数据。

不要将 respondent-level raw data 上传到 GitHub。

创建：
- `消费调查/DATA_AUDIT.md`
- `消费调查/FIRST_LOOK.md`

如果需要运行代码，可另建分析脚本；所有结果必须可复现。

---

# Task 1 — 数据结构和样本质量

## 1.1 基础结构

报告：
- 数据文件名和格式；
- 行数、列数；
- 是否一行对应一个 respondent；
- respondent ID 是否存在；
- ID 是否唯一；
- 完全重复记录数量；
- 关键变量缺失情况；
- 是否存在调查时长、开始/结束时间、IP/设备、渠道、quality flag 等平台变量（如有，仅汇总，不输出个人信息）。

建立简要变量字典，至少覆盖：
- Q1–Q31；
- 情景题 Q32–Q40；
- 平台背景变量 Q41–Q49；
- 额外平台字段（若有）。

对每个变量记录：
- 实际列名；
- label；
- coding；
- missing coding；
- 非缺失 N；
- 与问卷文字版是否一致。

若问卷与交付数据不一致，明确记录。

## 1.2 异常答卷检查

检查但不要擅自删除：
- 重复 ID；
- 多个 treatment 情景同时非缺失；
- 所有 treatment 情景都缺失；
- 大量 0–10 题完全相同（straight-lining）；
- 明显不可能的年龄/收入/家庭结构编码；
- 极短答题时间（仅当数据有 timing）；
- 其他平台 quality flags。

分别报告：
- 原始 N；
- 每类异常 N 和占比；
- 若剔除后的 N。

主报告先保留 raw sample 与 clean candidate sample 两套口径，不要在没有说明的情况下直接删样本。

---

# Task 2 — 审计 3×3 随机实验

问卷设计：
- Cash × 200 / 1000 / 5000；
- Food voucher × 200 / 1000 / 5000；
- Medical account × 200 / 1000 / 5000。

数据中理论上 Q32–Q40 每人应恰好有一个非缺失值。

## 2.1 Assignment integrity

逐人检查：
- 恰好 1 个 Q32–Q40 非缺失的比例；
- 0 个非缺失；
- >1 个非缺失。

构造明确变量：
- `transfer_type` = cash / food / medical；
- `amount` = 200 / 1000 / 5000；
- `treatment_cell` = 1,...,9；
- `outcome_ord` = 原始 1,...,6。

不要依赖列名猜 treatment，必须与问卷版本对应核对。

## 2.2 Cell size

输出九个 cell 的：
- N；
- 占总样本比例；
- 相对完全均匀随机分配 N/9 的偏离。

做适当的 multinomial / chi-square assignment check，并报告是否存在异常，但不要把“cell 数量不完全一样”自动解释成随机化失败。

## 2.3 Randomization balance

对 treatment type、amount 和九 cell 分别检查 baseline balance。

优先变量：
- 性别；
- 年龄；
- 学历；
- 月收入；
- 户籍；
- 工作状态；
- 单位类型；
- 住房；
- 子女；
- 家庭人数；
- 食品支出；
- 医疗支出；
- 是否过去收到补贴；
- 省份/城市级别（适当汇总）；
- Q6 社保保护；
- Q7 应急流动性；
- Q13 压力承受；
- Q15–17 未来预期。

输出 balance table，并做一个 joint orthogonality / omnibus test。

重点不是逐个 p-value 挑“显著”，而是判断 randomization 是否总体可信。

---

# Task 3 — Outcome 审计

原始 outcome 为 6 档：

1. 基本不额外消费；
2. <10%；
3. 10–25%；
4. 25–50%；
5. 50–75%；
6. >75%。

## 3.1 原始分布

首先完全不做任何 numerical MPC mapping，报告：
- 全样本六档频数/比例；
- 九个 cell 六档频数/比例；
- 按 transfer type 汇总；
- 按 amount 汇总。

必须画：
1. overall outcome distribution；
2. 3×3 cell outcome distribution；
3. 各 treatment 的 empirical CDF 或 cumulative response plot。

检查：
- floor effect（大量 category 1）；
- ceiling effect（大量 category 6）；
- cell 内是否过于集中；
- 是否出现不合理断层。

## 3.2 MPC midpoint mapping（仅作辅助）

可额外构造一个直观的 `mpc_midpoint`，但要清楚注明只是 approximation。

建议先使用：
- category 1 → 0；
- category 2 → 0.05；
- category 3 → 0.175；
- category 4 → 0.375；
- category 5 → 0.625；
- category 6 → 0.875。

同时至少做一组 alternative coding，尤其最后一档 >75% 没有精确上界信息时，要说明其敏感性。

主结论不能只依赖 midpoint OLS。

---

# Task 4 — 最小 reduced-form first look

目标是发现 pattern，不是“挖显著性”。

## 4.1 无控制变量

先估/展示：
- 九个 cell 的 mean ordered outcome；
- 九个 cell 的 mean midpoint MPC；
- type-level differences；
- amount-level differences；
- type × amount interaction。

推荐基本式：

outcome = transfer_type + amount + transfer_type × amount

ordered outcome 可用：
- raw cell means / distributions；
- ordered logit/probit 作为辅助；
- OLS on ordinal score 作为易解释描述；
- OLS on midpoint MPC 作为经济量级辅助。

报告 robust SE。

## 4.2 最重要的图

至少给出：

**Figure A**
横轴 amount = 200, 1000, 5000；
纵轴 outcome / implied MPC；
三条线分别 cash / food / medical；
带 confidence interval。

**Figure B**
每个 type × amount 的六档 outcome 分布或 CDF。

不要只给显著星号。

## 4.3 控制变量

只有在确认随机化成立后，增加预先定义的一组 baseline covariates 看 precision 是否改善。

同时报告无控制与有控制结果。

若加入控制后系数剧烈变化，应诊断原因。

---

# Task 5 — Food voucher 的 bindingness 初探

这是目前最重要的机制候选。

问卷只有“家庭每月食品支出”的分档，而 food voucher 有效期 6 个月。

因此建立：
- monthly food spending interval；
- approximate six-month food spending interval = monthly interval × 6；
- transfer amount = 200 / 1000 / 5000。

不要把区间 midpoint 当作唯一真值。

优先做 bounds-based classification：

1. **Definitely inframarginal**：
   transfer amount < six-month food-spending interval lower bound。

2. **Potentially binding / ambiguous**：
   transfer amount 落在 baseline spending interval 内。

3. **Likely extramarginal / binding**：
   transfer amount > six-month food-spending interval upper bound。

对于开放区间（如 5000+）谨慎处理。

然后比较 food-voucher 与 cash 的 treatment difference 是否随该分类变化。

核心希望看到/排除的事实：

> 即使在 clearly inframarginal group，food voucher 是否仍与 cash 产生不同消费反应？

若是，这才真正支持 non-fungibility / mental accounting 方向。

注意：baseline food expenditure 不是随机变量，异质性结果不等于独立 causal mechanism identification。

---

# Task 6 — Medical account 的机制初探

医疗支出变量是过去一年家庭自费医疗支出，而 medical account 长期有效。

因此：
- 不要直接复制 food-voucher 的严格 bindingness 解释；
- 把医疗支出视作过去医疗需求/风险的 proxy；
- 明确其局限。

探索 medical vs cash treatment effect 是否随以下变量变化：
- past medical spending；
- Q6 社保保护感；
- Q7 应急资金能力；
- 月收入；
- 年龄；
- 有无子女；
- 对未来经济/就业的预期。

优先画少量有理论动机的 heterogeneity figures，不要做几十个 subgroup p-value mining。

特别检查：

> 医疗账户是否呈现与食品券明显不同的 amount gradient？

如果是，记录这一事实供下一轮理论设计使用。

---

# Task 7 — 其他机制与异质性，只做筛查

候选：
- liquidity constraint：Q7；
- perceived social protection：Q6；
- future expectations：Q15–17；
- income；
- prior subsidy experience：Q31；
- household size / children；
- housing；
- employment status。

对每个候选机制：
- 给经济学动机；
- 只做 treatment interaction；
- 报 effect size + CI；
- 明确 exploratory status。

不要使用 Q1–Q22 的几十个社会心态变量进行无约束 data mining。

可先做相关矩阵/降维描述，判断这些题是否高度共线，但不要因此自动构造一个没有经济含义的总指数。

---

# Task 8 — 样本构成与外部有效性

描述样本：
- age；
- sex；
- education；
- income；
- hukou；
- employment；
- geography；
- city tier；
- household composition。

判断是否存在明显平台样本选择，例如：
- 青年占比极高；
- 高学历占比极高；
- 特定地区集中；
- 收入分布异常。

本轮只描述数据本身。

如未接入权威人口基准，不要自行声称“代表全国居民”。

---

# Task 9 — Power / precision

基于实际样本量和 outcome variance，报告：

- 每个 treatment cell 的标准误；
- cash vs food / cash vs medical 的 detectable effect 粗略量级；
- type × amount interaction 的 precision；
- 主要 subgroup 后剩余 N。

如果 cell 很小或 subgroup power 极差，明确指出。

目的不是做复杂 retrospective power ritual，而是判断：
- 主效应是否可识别得足够精确；
- 哪些机制分析实际没有统计能力。

---

# Task 10 — 必须交付的报告

## A. `消费调查/DATA_AUDIT.md`

必须包括：
1. 数据来源与文件结构；
2. N / variables / ID / duplicates；
3. missingness；
4. treatment assignment integrity；
5. 9-cell size；
6. randomization balance；
7. outcome coding；
8. sample quality concerns；
9. 可用变量字典；
10. 最重要的数据限制。

## B. `消费调查/FIRST_LOOK.md`

只回答以下问题：

1. Cash / food / medical 的消费反应是否肉眼有差异？
2. amount 从 200 → 1000 → 5000 时，三类 transfer 的反应如何变化？
3. 是否有明显 type × amount interaction？
4. food voucher 在 clearly inframarginal households 中是否仍区别于 cash？
5. medical account 是否呈现不同于 food voucher 的模式？
6. 哪 2–3 个异质性事实最强、最有经济含义？
7. 哪些结果最不稳健？
8. 样本和 measurement 最大的问题是什么？
9. 现有数据最支持哪条研究主线？
10. 下一轮问卷/实验最值得新增哪 3–5 个变量或 treatments？

最后给一个非常简短的结论，格式为：

- **Strong facts:** 数据里最可靠的 3–5 个事实。
- **Weak / uncertain facts:** 看起来有趣但 precision 或设计不足的结果。
- **Fatal concerns (if any):** 可能阻止当前设计形成论文的关键问题。
- **Next design priorities:** 下一轮最值得补的内容。

---

## 输出原则

- 所有结论必须可追溯到实际数据和代码。
- 所有 N、均值、比例、effect size 都报告明确数值。
- 图比大回归表更优先。
- 不挑显著性讲故事。
- 不将 hypothetical stated response 写成 actual realized consumption。
- 不把“消费增加”写成“偏好更高”或“福利更高”。
- 不把 baseline subgroup interaction 自动解释为 causal mechanism。
- 若数据与问卷设计冲突，优先报告冲突。
