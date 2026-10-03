# Idea 2 — The Best Review Team Is Not the Best Reviewers

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：团队互补性超出平均个体专业度的信息收益。

X：固定平均 E 时，团队 topic/network diversity 和 redundancy 的变化。Y：独立验证的 unique technical issues、distinct dimensions、正确技术纠错；次要为 reviewer-specific response/uptake。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

只存在不同 paper 的被选择团队差异。2026 指南规定三人自动、第四人手工；第四人本身不是随机处理。没有观察到有资格且同等 E 候选间的随机边际替换。

Assignment：AC 手工补充、低质量/未响应 reviewer、困难 paper 和时间约束共同决定人数与组成。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：paper 的潜在难度/缺陷与 AC 的补救行为。是否可测：内容和初始质量可测量一部分，AC 私人判断、未响应原因和真实候选集合当前不能完整测量。 是否可差分：不能。paper 内新增 reviewer 同时改变时间、信息顺序和负载；跨 paper FE 无法消除团队层面的选择。

## 可行 specification

先预注册 issue taxonomy，盲评正确性与重复率，报告编码一致性。描述模型 U_p=α+β diversity_p+γ mean(E)_p；β 明确为关联。不把 score variance 当质量，不把 reviewer_number 当分配顺序。

## Fatal reviewer objection / 是否可回答

更困难或初始 review 更差的 paper 才获得互补的额外 reviewer；容量冲击还直接改变努力与完成时间。

当前不能。真正随机或有已知概率的边际 reviewer 分配，且排除直接负载/时间路径，才能识别团队组合效应。即便如此，组合效应不自动等于纯互补机制。

## Minimal decisive test / falsification

取得 slot 的分配前信息和分配日志，在同一合格且相似 E 候选组内检验 reviewer 类型概率及预处理平衡；用独立 issue gold standard 检验新增信息。无随机源或收益完全由 individual E/完成时间解释，则放弃互补因果解释。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

自动/手工 slot、原始/替换/emergency 关系、分配时间、触发原因、候选集合与抽签概率、同期负载，以及独立技术 issue 编码。

**CONDITIONAL / ASSOCIATIONAL ONLY**。保留信息产出的描述性研究；不追求当前团队构成的因果系数。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
