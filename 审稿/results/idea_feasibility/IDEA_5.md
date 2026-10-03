# Idea 5 — Familiarity: Bias or Information?

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：proximity 的 favoritism 路径与 private/domain information 路径分离。

X：严格 dated pre-treatment coauthor/network/institution proximity。Y：judgment: score/confidence；information: 正确且独有问题、具体技术纠错、response/uptake。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

undated coauthor snapshot 不可用；部分 dated institution 正例 556，但没有可信完整负例。未发现实际 conflict recency cutoff 下可用的近阈值设计。

Assignment：COI 规则直接排除近关系；剩余关系与共同领域、私有信息及 AC 匹配有关。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：连接者掌握更多有用信息，且信息质量不能被 topic E 完全代表。是否可测：盲评公开论证只能测量部分，private information 不能完整测量。 是否可差分：不能；paper FE、E controls、generic harshness 均不能消除 pair-specific 私有信息。

## 可行 specification

若构念合格可同时描述 judgment 与 information outcomes；二者相关模式不足以分离机制。若实际 COI threshold 可恢复，先分析 eligibility/assignment jump，不能直接做 assigned-only score RD。

## Fatal reviewer objection / 是否可回答

冲突阈值改变“谁可被分配”，不随机改变同一 reviewer 的 familiarity；未被分配的人没有 review，条件于 assignment 会选择样本。

当前不能。即便有效政策 RD 最多识别排除规则/团队政策效应，不自动识别 friendship 导致 favoritism。机制需既定的独立信息或身份暴露变化；不能为已结束的2026假设一个新实验。

## Minimal decisive test / falsification

先证实真实 cutoff/第一阶段/共同支持和统一 paper-level outcome；再要求一个能保持技术信息但改变关系可见性的已存在设计。高分+高技术含量同时兼容信息与偏袒，不能算决定性支持；没有路径隔离则 kill bias claim。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

实际 COI 配置、dated 合作/机构区间、被排除及未分配候选、同一时间窗 outcome，以及可核验的独立关系可见性/信息变化；当前未找到该机制实验。

**NOT CREDIBLY IDENTIFIABLE IN ICLR 2026**。放弃本年 bias-vs-information 因果区分；可以保留明确注明非机制识别的描述。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
