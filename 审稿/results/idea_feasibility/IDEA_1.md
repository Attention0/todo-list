# Idea 1 — Expertise–Independence Frontier

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：增加专业匹配是否必然牺牲独立性。

X：预先定义的专业相似度 E 与 dated proximity P；政策处理是额外独立性约束。Y：可行匹配的总专业度损失，及已分配 pair 的 E–P 分布。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

现有数据只有被选中的 reviewer–paper pairs。它可以支持描述性分布，不能识别候选集中的机会成本。组织 frontier 需要同一候选矩阵上的可行反事实优化；不是评分回归。

Assignment：领域匹配、冲突排除、容量、AC 选择共同决定被观察的 pair。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：候选资格和容量约束造成的选择截断。是否可测：只有真实逐 paper 候选资格、当时容量、冲突和目标函数可完整测量；当前公开角色名单不能替代。 是否可差分：不能；paper FE 只比较已经被分配的 reviewer，不恢复未分配但可行的 pairs。

## 可行 specification

若 E、P 合格，报告 assigned-pair 散点/分箱。若候选矩阵合格，固定人数、容量、COI 与领域约束，分别求 maximize ΣE、加入预先定义网络距离、加入 dated coauthor/institution 排除后的最优 ΣE。成本=基准最优值−约束最优值；报告可行性和测量敏感性。

## Fatal reviewer objection / 是否可回答

你只观察被组织选中的组合，所谓 expertise cost 可能只是漏掉的可用候选人。

当前不能。取得完整且时点一致的候选矩阵与构念后，可以回答运营上的反事实 frontier，但仍不能据此声称 proximity 导致 favoritism。

## Minimal decisive test / falsification

先检验能否复现实际分配的硬约束、每个 reviewer 负载与每个 paper 名额。若真实可行集内加强独立性没有降低最优 E，机械 trade-off 主张被推翻。若降低，也只是指定约束和构念下的 frontier。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

初始 reviewer pool、逐 paper eligibility/COI、capacity/load、领域限制、matching objective 和手工 override，加冻结提交文本与验证过的前期出版/关系记录。

**CONDITIONAL / ASSOCIATIONAL ONLY**。保留描述性问题；暂不绘制伪 expertise–proximity 图，不运行不可行的 counterfactual。组织 frontier 当前未识别。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
