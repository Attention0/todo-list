# Idea 6 — Status as a Substitute for Expertise

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：低 E reviewer 因识别作者身份而依赖 status。

X：预处理 status × reviewer E × 实际 identity observability。Y：score/论证对 status 的依赖及信息产出。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

作者自选 arXiv/code 公开时间，缺实际 reviewer 看见身份的记录。security incident 是捆绑制度冲击，不是干净的身份可见性实验。

Assignment：优质/有资源/强声誉作者更可能预发；reviewer 专业兴趣也影响发现身份。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：paper 质量和传播行为同时决定 status proxy、可见性和评价。是否可测：可测预发布与部分文本质量，但不能测未观察的实际身份认知及全面质量。 是否可差分：不能；同一 paper 的不同 reviewer 谁发现身份也受 E、搜索行为和熟悉度影响。

## 可行 specification

核验首个 arXiv hit 是否真为该 paper，统一 UTC 后仅描述 pre-review release。status×E 回归无可见性干预不能叫 substitution。现有匹配只包含3433 paper，3093在任一观察review前发布，不能替代实际可见性。

## Fatal reviewer objection / 是否可回答

你把内生 preprint 发布误当随机 deanonymization；incident 又同时改变 pressure、AC、score 和 discussion。

当前不能；补身份线索只是改善测量。只有2026已存在且可证明与质量/匹配无关的可见性分配才可能推进，没有找到。

## Minimal decisive test / falsification

审计真实平台可见性规则是否有外生阈值，并要求 reviewer 接触日志及预处理平衡。若变化同时影响流量、技术信息或压力，则 exclusion 失败；无此规则就停止 causal status substitution。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

冻结作者 status/出版记录、标题人工核验的发布时间、依法取得实际身份接触证据，以及独立的可见性规则/随机化日志。

**NOT CREDIBLY IDENTIFIABLE IN ICLR 2026**。放弃2026现有数据下因果 status-substitution；不以 incident 或 arXiv 发帖当 IV。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
