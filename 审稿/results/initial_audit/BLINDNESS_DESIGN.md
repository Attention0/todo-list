# Blindness / identification audit

## 已证实的制度与未观测的实际曝光

| 年份/阶段 | 制度证据 | 本地可见信息 | 识别意义 |
|---|---|---|---|
| ICLR 2026 投稿与初评 | 官方CFP明确double blind，允许arXiv | 只有2026；snapshot后来带真实身份不证明reviewer当时可见 | 没有single blind对照年 |
| 正常discussion | reviewer guide给出11月11日开放discussion | raw comment table存在，current notes是version2 | 讨论引入新信息，实际author识别不观察 |
| 安全事件前后 | 官方12月3日公告证实泄露及11月27/28冻结、回退、AC重分配 | notes与快照内容差异可观测，谁看过泄露不可观测 | 非全会议统一变成single blind，也不是随机treatment |
| 最终决策 | 本地文件截止2026年1月上旬，没有完整decisions | current/public submission status不等于完整final outcome | 不能用旧快照分析真实final接受率 |

[官方CFP](https://iclr.cc/Conferences/2026/CallForPapers)规定评审阶段双方匿名。[Author Guide](https://iclr.cc/Conferences/2026/AuthorGuide)允许审稿回应与讨论。PDF、自引、arXiv、代码站点、topic和既往关系均可能暴露身份，但本地没有reviewer实际识别的测量。公开publication早于review并不等于该reviewer看过，更不等于单盲制度。

## 事件时序及同时变化

[ICLR官方事件说明，2025-12-03](https://blog.iclr.cc/2025/12/03/iclr-2026-response-to-security-incident/)：11月27日发现漏洞并修复、review编辑被冻结；28日reviews被回退，AC重新分配；公告还指出可能早于11月11日已被利用。原reviewers没有整体重新分配。identity泄露、潜在联系/干扰、评分回退、AC变化、延长meta-review阶段同时发生。本地10,090篇快照与公告所说流传数据特征相符，但精确获取来源与每人的曝光均未验证。

因此，11月27日不能当唯一干净起点；把treated定义为本地有identity的记录会把样本获取与真实行为混在一起。回退制造的分差也不是自然的行为恢复。没有未泄露样本的同期历史scores、完整revision面板或曝光强度，事件研究/DiD现在不可实施。

原[Reviewer Guide](https://iclr.cc/Conferences/2026/ReviewerGuide)中的常规日历与事件后的安排不同；[AC Guide](https://iclr.cc/Conferences/2026/AreaChairGuide)还残留2024字样及互相矛盾的日期，不能逐日机械当2026最终有效规则。以事件公告覆盖事件后的安排；具体冻结对象与历史note版本还需API edits或官方归档核验。

## 数据已揭示的测量问题

`加载数据` cells 26,36–38把旧JSONL rating命名为final、后期raw note rating命名为initial。29,813 final content全部与旧快照一致；29,766 initial全部与保存的current note一致。后者tmdate均在release之后，review raw所有记录version2；没有证明恢复后current=某个不可改的真正initial。`rating_diff`应解释snapshot-current contrast，不用于rebuttal因果。

arXiv匹配来自`爬取arxiv` get_arxiv_details，标题核验被注释、max_results=1、异常全部None；当前保存source只查询分段索引，缺无命中/未查/失败标记。先校验论文实体、首版v1发布时间及是否早于**每条review的可确认首次评分时点**，再构造exposure candidate。不能把NULL当没上传，或把arxiv_updated当第一次公开。

## 候选设计与门槛

| 设计 | 当前状态 | 首要门槛/威胁 |
|---|---|---|
| single→double跨年DiD/断点 | currently infeasible | 没有跨年观测或可验证制度切换；会议规模、量表、算法等并发变化 |
| author/institution reputation × regime | currently infeasible | 缺reputation与single-blind样本；所有2026同一nominal regime |
| prior proximity × verified pre-review arXiv（paper FE） | feasible with additional construction；仅关联 | arXiv与quality/选择相关；topic expertise、reviewer严厉度及实际识别均未控制 |
| 泄露事件研究 / exposed-control比较 | currently infeasible | 实际曝光/未曝光不观察、起点污染、冻结与回退/AC变化并发 |
| 单篇reviewer差异 | descriptive only / 构造后可继续 | paper FE不能清除reviewer-level affinity、bid和人工选择；paper-levelarXiv主效应被FE吸收 |
| triple differences | currently infeasible | 至少需要可信制度/曝光与相应第三维；目前不能从名字预测造出treatment |

高声誉作者更容易被认出、已有network proximity导致身份推断等都是待检验假设（Inferred/Assumed），不是本轮Observed结果。下一轮优先修复版本血缘和预印本实体匹配，补合法的历史公开数据及assignment证据，再决定是否投入制度因果设计。
