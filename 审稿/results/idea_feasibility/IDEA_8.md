# Idea 8 — Who Should the Organization Listen To?

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：组织对 expertise/confidence/status/proximity 的实际权重与应有权重。

X：分歧情形下 reviewer 意见特征和外生意见暴露。Y：可信 AC meta/最终 decision；“应有”权重另需独立质量真值。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

当前缺可用完整正常讨论 lineage 和 local meta/decision。最终决定确实存在，但属于 rollback/freeze/AC reassignment 后的制度，不是未受干扰的自然讨论。

Assignment：AC 会依据论证有效性、共识、自身判断和处理政策选择采纳意见。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：被采纳 reviewer 的未观测论证正确性及 AC 私人判断。是否可测：技术审计能测部分，decision 不能自己作为真实质量标签。 是否可差分：不能；分歧条件本身选择样本，paper FE 不能消除意见的信息差异。

## 可行 specification

若合法获取可靠 final/meta 可估 incident-policy 下 descriptive implicit weights；cross-validation 只能优化预测该决策，不是最优科学质量。own rating 包含于 final mean 会机械相关。causal influence 要独立外生 exposure，并验证 chronology。

## Fatal reviewer objection / 是否可回答

你在预测新 AC 的回溯决策，而不是识别常规组织听谁；“optimal”只是模仿标签。

当前不能。只补 final labels 不解决 mechanism；独立质量benchmark和可信原过程+外生暴露均为必要条件。incident AC transfer 同时改变评估制度，不能作单一渠道 IV。

## Minimal decisive test / falsification

先核验原始意见、正常讨论、重置、meta/decision 各阶段 lineage，再与独立质量benchmark区分预测与规范权重；无正常窗口则停止常规 causal influence，无benchmark则禁止 optimal-quality claim。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

合法完整 pre-discussion/edit/meta/decision、incident reset/freeze/AC 操作、真正外生意见暴露，以及独立技术质量/正确性标签。

**NOT CREDIBLY IDENTIFIABLE IN ICLR 2026**。放弃常规过程的2026因果影响主张；未来若取得 labels，仅保留明确制度条件下的描述/预测。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
