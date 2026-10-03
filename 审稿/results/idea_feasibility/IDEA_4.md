# Idea 4 — Gatekeepers of the Frontier

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：specialists 对 boundary-spanning paper 的独特评价效应。

X：预处理 reviewer specialization × 冻结 paper 的 boundary-spanning。Y：原始评价 score，辅助技术问题类型/正确性。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

不同 paper–reviewer pair 的交互项；目前没有实际 affinity band 内的随机 reviewer type variation。狭窄相似度带只是假设，不是证据。

Assignment：AC/算法按细粒度主题、方法、兴趣和 bids 选择 reviewer。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：未观测 pair-specific intellectual fit / 方法认同。是否可测：真实 affinity/bids 可部分测量，但 embedding 与官方分配依据不同，思想契合仍可能未测。 是否可差分：paper+reviewer FE 不能消除 reviewer 对某个具体跨领域 paper 的独特匹配。

## 可行 specification

score_rp=paper FE+reviewer FE+β boundary_p×specialization_r+预指定控制。只在构念合格后可做 level 2；paper 主效应/reviewer 主效应被 FE 吸收。当前不运行该回归。

## Fatal reviewer objection / 是否可回答

specialist 恰好被分给某类 frontier paper，交互效应就是选择性匹配。

当前不能。必须有实际部署的随机 tie-breaking/随机 solver 概率与 eligible bands，且 manual overrides 可追踪；仅加 affinity 控制不能回答。

## Minimal decisive test / falsification

在真实而非事后制造的 eligible affinity ties 内复现随机概率，检验 paper 的前期方法/novelty 与 reviewer harshness 平衡；若类型仍由 bids/AC preference 强烈决定，则 kill causal design。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

dated reviewer portfolio、冻结 paper/前期文献、真实 affinity/bids、candidate bands、随机种子/概率或 tie log、manual adjustment。

**CONDITIONAL / ASSOCIATIONAL ONLY**。保留为条件关联；不把双 FE 交互当组织 gatekeeping 因果证据。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
