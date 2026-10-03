# Idea 3 — Confidence vs Competence

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：A: confidence calibration；B: confident reviewer 的意见影响后续判断。

X：A 为预处理 E；B 为同一分歧中 reviewer confidence/意见的外生变化。Y：A 自报 confidence；B 其他 reviewer 的真实讨论后改分及 AC 决策变化。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

A 可比较不同 pair 的 E–confidence，属于 level 1。B 当前只有两份语义倒置的快照，不能构造可信 pre/post；没有 confidence 独立于论证质量的外生变化。

Assignment：专业匹配影响 E；reviewer 性格、论证内容、真实信息和 paper 难度影响 confidence 与意见采纳。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：confident reviewer 同时持有更有说服力的正确技术信息。是否可测：可盲评部分论证正确性，但不能完整测量私人信息和可信度。 是否可差分：不能；paper FE 不消除同一 paper 内 reviewer 私有信息差异，reviewer FE 不消除 pair-specific 信息。

## 可行 specification

A：合格 E 对 confidence 做预指定分箱/校准曲线，不定义 E=confidence。B：只有完整可信 edits 才定义他人意见暴露前后的 score move；不能用当前 initial 标签或 own initial 与 final mean 的机械相关。

## Fatal reviewer objection / 是否可回答

所谓影响其实是正确意见被采用，而且 initial/final 并非自然讨论前后。

A 在构念补齐后可以回答测量问题。B 当前不能；可信 chronology 只解决 outcome，仍需外生意见/表达暴露或 assignment variation 才解决机制。

## Minimal decisive test / falsification

逐条 edits 重建原始提交、讨论编辑、incident reset；与独立冻结快照比对。若原始与正常修订不可区分，B 直接停止。若 confidence 的采纳关系完全随正确论证消失，则不能主张组织偏好自信。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

依法授权完整 review edits、读写权限可核验的历史、pre-discussion snapshot、正常讨论时间及暴露关系、meta/decision、incident 操作日志；另需真正外生 confidence/意见暴露证据。

**NOT CREDIBLY IDENTIFIABLE IN ICLR 2026**。保留 A 为测量事实；放弃本年现有数据下 B 的因果影响主张。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
