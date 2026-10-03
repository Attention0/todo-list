# ICLR 2026 assignment identification audit

## 实际可观察范围

本地 main 有29,813 review rows、7,655 paper、13,560非空 reviewer IDs。公开2026 committee页面现在有18,054 reviewer profile链接（unique也是18,054），覆盖本地13,549 reviewer；另有1,634 AC、79 SAC。角色标签和公开稳定ID可在内存中用于计数，但本轮不导出任何ID/人名/映射。公开名单是会后名单，不是assignment时冻结的完整 reviewer pool；11个未匹配本地ID的原因未验证，不能解释为假身份。[官方2026 roster](https://iclr.cc/Conferences/2026/ProgramCommittee)

匿名 reviewer group、一个forum notes、一个review edits请求均返回403。未登录、未使用原notebook凭据、未绕过权限，未重试被拒请求。403只说明本次访问失败，不证明记录不存在或所有forum都不可公开。详见 public_access_checks.csv。当前notes的version=2不是两个时间版本；所有75,748 current review notes都只有当前表示，没有原始编辑序列。OpenReview edit有独立权限，当前note可读不保证edit可读。[官方edit对象文档](https://docs.openreview.net/getting-started/objects-in-openreview/introduction-to-edits)

## 逐项可恢复性

| 所需对象 | 现有证据 | 可用于 clean assignment？ |
|---|---|---|
| pool/role/area | 会后公开角色名单；retrospective profile expertise自报 | 否，缺当时availability/area eligibility/emergency role |
| hard/author-declared COI | 未找到初始逐paper排除矩阵 | 否 |
| recent coauthor COI | undated coauthors；无完整dated publication graph | 否，不能把缺边当无COI |
| same institution/advisor COI | retrospective histories/relations；缺当时完整区间与配置 | 否 |
| reviewer capacity/load | 可数最终出现的review，不见初始capacity、active负载与拒绝/退出 | 否，最终数量不是分配前capacity |
| bids | 2026指南有bidding流程；无本地bid矩阵 | 否 |
| official affinity/TPMS/embedding | 无真实分配分数和候选矩阵 | 否，重算similarity不等于官方affinity |
| optimizer | 平台支持多种solver，但未确认2026实际版本、目标函数、参数 | 否，不能假设采用Randomized solver |
| manual/emergency/replacement | 指南允许并要求手工补充；无slot/触发/调整日志 | 否，review日期不能单独分类 |

2026 SAC指南明确规定：三名自动分配，AC可以替换其中除一名外的reviewer，第四名须手工加入；同时说明AC不见作者身份。因而“自动”不意味着随机，“第四人”不能当准随机边际，保留的一人也没有随机保留证据。[2026 SAC guide](https://iclr.cc/Conferences/2026/SeniorAreaChairGuide) AC指南的补救/emergency流程随不响应或低质量发生，具有明显潜在内生触发。[2026 AC guide](https://iclr.cc/Conferences/2026/AreaChairGuide) 这些是制度声明，不是实际分配日志；指南存在旧年份链接/日期不一致，因此本轮不由指南日期推断真实执行时间。[2026 Reviewer guide](https://iclr.cc/Conferences/2026/ReviewerGuide)

平台文档支持MinMax/Fairflow/Randomized等方法与capacity配置，仅证明平台能力；不是ICLR2026使用证据。即使确为randomized，仍需实际候选集、抽样概率与override，不能当均匀随机。[官方matching文档](https://docs.openreview.net/how-to-guides/paper-matching-and-assignment/how-to-do-automatic-assignments/how-to-run-a-paper-matching)

## Candidate shocks：逐一设计门槛

NA表示未观察到所需变量或设计样本，不表示样本量为0、第一阶段为0或balance通过。

| 候选 | 制度依据/实际状态 | running variable / threshold | cutoff附近N | treatment jump | pre-treatment balance / exclusion |
|---|---|---|---|---|---|
| affinity threshold | 未确认实际2026规则 | NA / NA | NA | NA | 未能运行，affinity与潜在专业度直接相关 |
| capacity constraint | 平台支持；无2026配置 | 当时active load未知 / capacity未知 | NA | NA | 未能运行；load也直接影响effort/time |
| tie-breaking | 未发现实际tie/random seed log | 实际score ties未知 / NA | NA | NA | 未能运行；近分不代表随机 |
| load balancing | 最终review数可见；初始负载未知 | 分配前load未知 / NA | NA | NA | 未能运行；退出/拒绝内生 |
| emergency addition | 指南：不响应/低质量补救；无flag/log | 触发质量/时间未知 / 实际deadline未知 | NA | NA | 未能运行；paper困难与原review质量直接影响Y |
| late replacement | 指南允许；无原新slot映射 | 退出原因/时间未知 / NA | NA | NA | 未能运行；新reviewer信息顺序不同 |
| fourth reviewer | SAC规定手工加入 | AC discretion / 没有随机cutoff | NA | NA | 没有随机性证据，不能用人数当IV |
| AC transfer | incident后重分AC有官方证据 | 同一conference捆绑政策；无独立cutoff | NA | NA | freeze/reset/压力同时改变，排除限制不成立 |
| conflict recency | 平台有可配置年限；未知2026值 | 最后合作日期未知 / 实际阈值未知 | NA | NA | 未能运行；assigned-only score RD有选择，policy不等于familiarity |
| availability cutoff | 未找到冻结availability/log | NA / NA | NA | NA | 未能运行 |
| within-conference algorithm change | 未发现部署版本/时间记录 | NA / NA | NA | NA | 未能运行；不能从incident推断算法变化 |

平台示例COI年限不能充当2026阈值。[官方conflict配置说明](https://docs.openreview.net/how-to-guides/paper-matching-and-assignment/how-to-do-automatic-assignments/how-to-setup-paper-matching-by-calculating-affinity-scores-and-conflicts)

## Incident 与 chronology

官方事后说明漏洞起于rebuttal开始附近；11月27日事件后rollback scores、冻结讨论、重新分配AC，新AC判断若正常讨论会怎样。不能以首次披露日当身份暴露开始，也不能把AC transfer当随机reviewer replacement。[2026 retrospective](https://blog.iclr.cc/2026/03/31/a-retrospective-on-the-iclr-2026-review-process/) [incident response](https://blog.iclr.cc/2025/12/03/iclr-2026-response-to-security-incident/)

现有snapshot的rating_final来自11月28日旧snapshot，rating_initial来自较晚current notes；不是自然pre/post。真实decision存在，但local缺meta/decision表，匿名样本访问失败；不声称所有public final decision不可获取。重建历史需要合法独立edits/snapshots与incident操作标签。

No clean assignment instrument found. 未计算任意第一阶段、RD或balance回归，因为未找到可定义的识别样本；增加控制无法填补这一缺口。

No assignment-based source of plausibly exogenous variation was identified.
