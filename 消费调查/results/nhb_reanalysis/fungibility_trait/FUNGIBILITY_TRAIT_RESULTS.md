# Individual fungibility latent trait：结论与识别审计

日期：2026-10-01。执行依据：`消费调查/FUNGIBILITY_LATENT_TRAIT_INVESTIGATION.md`。

## 结论

**现有数据不支持把“已识别稳定 individual fungibility latent trait”作为论文核心贡献。原因是该构念无法被当前设计识别；这不等于证明 trait 不存在。建议回退到 randomized transfer-form/context effects，并保留有边界的条件平均效应异质性。**

原始 `.dta` 独立核查：5,497 行，5,497 个唯一 ID，无缺失或重复 ID；每人恰好回答一个随机情景、一个 form、一个金额。任何两个 form 的同人重叠均为 **0**，同一 form/金额的重复回答亦为 **0**。`scen_mpc` 是九个随机情景列合并而来的派生字段，不是第二次测量。问卷明确每人仅随机作答九个版本中的一个；不存在个人内部呈现顺序可供分析，也没有重测时间或 test–retest 观测。

## 数据结构及 reliability

九格样本数与上一轮一致：Cash 200/1000/5000 为 619/595/584，Food 为 614/620/602，Medical 为 615/612/636。详见 `trait_measurement_cells.csv`。

每个 ID 的 MPC 次数恒为 1。每个 form 有一次观测的 ID 分别为 Cash 1,798、Food 1,836、Medical 1,863，其余 form 缺失；每个金额也仅在被分配的 form 下出现一次。此缺失是随机实验设计导致，而非应当插补的漏答。

不能估计 MPC test–retest reliability、个体差值 reliability、ICC 或个体因子分数 reliability。此前社会心态项目的 Cronbach alpha 衡量那些主观题目的内部一致性，不是 MPC 的 reliability，也不是 fungibility 的 reliability。

## 潜变量模型为何不识别

对模型 `MPC_if = alpha_f + lambda_f theta_i + epsilon_if`，当前数据只观测各 form 的边际分布，缺少同一人的 cross-form 联合分布。即使固定 `Var(theta)=1` 并假定独立误差，也只得到 `Var(MPC_f)=lambda_f²+Var(epsilon_f)`；无法将载荷方差与残差方差分开，更无法估计个体分数或跨 form covariance。

`trait_nonidentification_witness.csv` 给出纯代数示例：假定共同因子占边际方差 0%、25%、50%、75%、100%，都能保持相同的边际方差。这些是假设情景，并非拟合结果。更强的离散结果也成立：相同的各 form 六档分布，可以通过独立配对或共同分位数配对构造出完全不同的 cross-form joint distributions；随机分组的一次回答无法区分它们。任何在这里输出 precise latent variance/reliability 的 factor model 都依赖数据外限制。

此外，即使未来观测到共同因子，它也可能仅代表一般消费反应水平，而非独立的 fungibility 维度。若所有 `lambda_f` 相等，theta 在所有两两差值中抵消。若载荷不相等，差值包含 `(lambda_cash-lambda_food)theta`，但仍需比较一般 MPC 因子与 form contrast 因子；不能只给共同因子命名为 fungibility。当前数据既无法辨别这两个维度，也无法检验一维 fungibility 的合理性。

## 可识别的方差分解

本轮只分解随机 cell 均值之间的方差与剩余方差，没有估计个体 random effects。

| Outcome | 分组 | 组均值方差占比 | 未分解剩余方差占比 |
|---|---|---:|---:|
| 原始 ordinal | form | 0.685% | 99.315% |
| 原始 ordinal | form×amount | 0.884% | 99.116% |
| Midpoint | form | 0.613% | 99.387% |
| Midpoint | form×amount | 0.941% | 99.059% |

这是一份样本内描述性分解，有限样本均值波动也进入组间部分。剩余包括一般个体差异、潜在 person×form 差异、测量误差与其他变异；**不能把剩余全部叫 noise，也不能全部叫 trait**。小组间方差占比不表示随机均值效应不成立。

## 个体差值与机械相关

没有为任何个人构造 `MPC_cash−MPC_food`。真实差值需要同时观测同一人的两种反应。模型填补未观测潜在结果再相减，只得到模型定义的条件平均 contrast，不能识别实际个体 contrast 或其可靠性。

在有重复数据的经典误差模型下，`D_CF=Y_C−Y_F` 与 `D_CM=Y_C−Y_M` 即使真实差值无关，也可因共享现金误差产生 `Cov(error_CF,error_CM)=Var(error_C)`（独立跨 form 误差假设）。差值 reliability 为 `Var(true difference)/(Var(true difference)+Var(error_C)+Var(error_F))`；当前三个组成部分均未知。跨 form 真实潜在结果的 covariance 同样未知，所以个体处理效应方差也不可识别。

## 协议逐项验证状态

| 检查 | 状态 | 原因或可识别替代 |
|---|---|---|
| 每人/form/金额测量次数 | 已完成 | 原始数据及问卷一致，恰好一次 |
| 测量误差及机械相关 | 已完成识别评估 | 没有个体差值；共享现金误差会污染差值相关 |
| Latent factor、trait variance、reliability | 不可识别 | 无同人 cross-form covariance、无重测 |
| Leave-one-form-out 个体 trait 验证 | 不可实施 | 排除唯一观测 form 后，该人没有任何 MPC 输入 |
| Split sample trait 稳定性 | 不可实施 | 分割不同人不会产生同人的第二个测量；能验证组均值但不能验证 trait |
| Cross-form reliability | 不可实施 | 没有同人配对；原有 source-model portability 是不同人的预测映射比较 |
| External validation | 已完成题目审计；trait 检验不可实施 | 无可识别 trait 分数，且无直接 mental-accounting/fungibility scale |

## External validation 题目审计

现有可用的间接相关变量：Q7 应急筹资（主观流动性）、Q26 住房（粗资产 proxy）、Q29 食品支出、Q30 自费医疗支出、Q31 既往补贴接触、Q14 收入/消费及其他压力来源，以及 Q1–22 心态、信任、保障、预期和主观地位。它们不是直接 financial attitudes/mental accounting 测量，也不是独立测量的转移可替代性。Q29/Q30 为支出水平 proxy，不是 detailed consumption habits。

未发现实际储蓄/还债行为、收入来源账户标签偏好、预算账户分隔、现金等价/WTA、跨 form 替代选择、重复转移反应。情景选项提到“存起来/还债”只是同一 MPC outcome 的说明，不能再当独立 validation outcome。因而没有报告“trait 预测这些变量”的回归；用这些变量构造分数后又回归同一变量会产生循环验证。

## 与既有结果的关系

过去的 average form effects、strict-inframarginal Food−Cash contrast 和 HTE validation，不构成同人 trait reliability 证据。随机分组允许识别平均 form effect，并在假设与充分样本下估计 `E[Y_f−Y_c|X]`；不识别 `Y_if−Y_ic` 的个人实现值和稳定性。此前 RF portability、held-out person-score 及 subjective PCA 不应被重新命名为 latent fungibility。

本轮不继续 MPC 预测、RF、SHAP 或新 moderator 搜索。推荐正文若后续重写，应以 transfer-form/context effect 为可支持的主张；不可从当前数据声称已测得稳定个体 fungibility 或否定稳定 trait 的存在。

## Figure/table 与复现

关键图 `trait_measurement_overlap.png` 展示所有 off-diagonal overlap 为零，这是识别判断的直接证据。关键表为测量次数、form overlap、重复次数和可识别方差分解。没有给出 trait loading 图或个人分数表，因为这些参数不可识别。

运行 `fungibility_trait_audit.py`，输入本地原始 `.dta`，输出本目录。原始数据 SHA-256 与上一轮一致；manifest 记录样本与版本。所有输出仅为汇总，不含 IDs、个人记录或预测。论文未修改。
