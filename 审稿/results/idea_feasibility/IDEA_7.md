# Idea 7 — Peers as Competitors

本审计仅使用 ICLR 2026 的评审/分配过程。历史出版只允许作为该年 assignment 前的构念来源，不引入其他年份的 conference outcomes。Level 1=测量事实；2=条件关联；3=设计识别；4=机制因果。仅3–4算 clean causal。当前所有判定都以实际观察到的证据为准，不把待取得数据视为已经存在的设计。

## Estimand / treatment / outcome

目标：同等 expertise 下科学竞争导致战略性评价。

X：distinct competition：相同狭窄 niche、同时期 agenda、可靠无合作，而非单纯 topic similarity。Y：评分和独立验证的技术审查正确性/选择性。若讨论因果，目标是在其他路径不变时改变 X 的 potential-outcome contrast，而不是相关系数本身。

## 实际 variation、assignment 与 DAG

当前 topic/无合作 proxies 既不合格也不外生；没有观察到同等 E、不同 competition 的随机 reviewer swap。

Assignment：主题最接近的 reviewer 同时最有资格、最可能有竞争动机，也最可能识别缺陷。 DAG（文字）：潜在 paper/reviewer/pair 属性同时影响 assignment 和 X/Y；只观察 assigned pairs 可打开选择路径。最危险 omitted variable：竞争者拥有更精确的专业知识并采用合理的高标准。是否可测：可验证部分技术异议，但完整 private expertise/评价标准和动机不可测。 是否可差分：不能；reviewer FE 不能消除对某篇同 niche paper 的特殊知识。E matching 只控制测量误差很大的代理。

## 可行 specification

先证明 competition 与 E 有独立支持：同 E band 中有可靠 dated agenda/no-collaboration 差异。没有真实前期 graph，缺边不能等同从未合作。reviewer own submissions 仅依法公开可链接时使用。当前不做 strategic regression。

## Fatal reviewer objection / 是否可回答

更严厉恰恰是更懂行，topic overlap 的负系数不能证明 sabotage。

当前不能。随机或准随机 comparable reviewer assignment 可识别 competitor-type effect，但战略动机仍需正确性基准及路径隔离。

## Minimal decisive test / falsification

先检查真实 eligible candidate 中同 E 不同 competition 的共同支持和外生 swap；再由不知道关系的专家核验批评真伪。若差异都是正确技术问题/更高合理标准，战略评价主张被推翻；没有 swap 则 causal claim 不成立。

任何获准进入 level 3 的设计都必须在真实 identifying sample 内做预处理 balance；以冻结 paper 属性作为不可受后续分配影响的 placebo，并检查 treatment 是否预测它。未来 coauthor edge 只能作为时点泄漏诊断，不能作 treatment；它也可能被本次互动影响，因此相似关联不是泄漏的唯一证明。保留 max/top-5/centroid/lexical 四种 E、dated network/institution 两类 P 的预指定定义，leave-one-definition-out 不一致会降低测量可信度，绝不修复内生性。

当前实际执行的是数据可用性、时点和 missingness 审计，未执行不存在的 cutoff balance、placebo outcome 回归或未来 edge 测试。没有验证 publication corpus/完整 dated graph，就不伪造这些统计量；详见 CORE_CONSTRUCTS 与 PRIORITY_TESTS。

## Specific additional data / verdict

pre-cutoff identity-validated publication/agenda、完整 dated coauthor graph、依法可链接 own submission、candidate E 与真实分配随机源、盲评技术基准。

**NOT CREDIBLY IDENTIFIABLE IN ICLR 2026**。放弃2026现有数据的战略竞争因果主张；避免把近主题 reviewer 标为竞争者。

补齐可观测信息并不保证获得外生变化；因此不以 “CLEAN WITH SPECIFIC ADDITIONAL DATA” 代替尚未发现的制度设计。
