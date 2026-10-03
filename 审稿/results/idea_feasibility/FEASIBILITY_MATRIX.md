# ICLR 2026 clean-identification feasibility matrix

审计日期：2026-10-03。没有 CLEAN NOW，也没有已被证实只差特定数据即可执行的 clean assignment design。1、2、4 的 verdict 是设计上最多可保留条件关联，不表示当前测量已完整。3 的 verdict 针对强 Claim B；Claim A 仍可保留 level 1。5–8 的强机制主张当前不能可信识别。“未发现”不等于证明所有权限内的机构日志都不存在。

| Idea | Core claim | Best available design | Identification level | Main confound | Can confound be ruled out? | Data needed | Verdict |
|---|---|---|---|---|---|---|---|
| 1 Expertise–Independence Frontier | 增加专业匹配是否必然牺牲独立性 | assigned-pair 描述；candidate frontier 未识别 | 1–2；组织 frontier 未识别 | 候选资格和容量约束造成的选择截断 | 否 | 初始 reviewer pool、逐 paper eligibility/COI、capacity/load、领域限制、matching objective 和手工 override，加冻结提交文本与验证过的前期出版/关系记录。 | CONDITIONAL / ASSOCIATIONAL ONLY |
| 2 The Best Review Team Is Not the Best Reviewers | 团队互补性超出平均个体专业度的信息收益 | 团队/文本描述 | 2（构念补齐后） | paper 的潜在难度/缺陷与 AC 的补救行为 | 否 | 自动/手工 slot、原始/替换/emergency 关系、分配时间、触发原因、候选集合与抽签概率、同期负载，以及独立技术 issue 编码。 | CONDITIONAL / ASSOCIATIONAL ONLY |
| 3 Confidence vs Competence | A: confidence calibration；B: confident reviewer 的意见影响后续判断 | A 测量；B chronology 不合格 | A:1；B:无3–4 | confident reviewer 同时持有更有说服力的正确技术信息 | 否 | 依法授权完整 review edits、读写权限可核验的历史、pre-discussion snapshot、正常讨论时间及暴露关系、meta/decision、incident 操作日志；另需真正外生 confidence/意见暴露证据。 | NOT CREDIBLY IDENTIFIABLE IN ICLR 2026 |
| 4 Gatekeepers of the Frontier | specialists 对 boundary-spanning paper 的独特评价效应 | paper+reviewer FE 交互仅关联 | 2（构念补齐后） | 未观测 pair-specific intellectual fit / 方法认同 | 否 | dated reviewer portfolio、冻结 paper/前期文献、真实 affinity/bids、candidate bands、随机种子/概率或 tie log、manual adjustment。 | CONDITIONAL / ASSOCIATIONAL ONLY |
| 5 Familiarity: Bias or Information? | proximity 的 favoritism 路径与 private/domain information 路径分离 | proximity 描述也受缺失限制 | 无3–4 | 连接者掌握更多有用信息，且信息质量不能被 topic E 完全代表 | 否 | 实际 COI 配置、dated 合作/机构区间、被排除及未分配候选、同一时间窗 outcome，以及可核验的独立关系可见性/信息变化；当前未找到该机制实验。 | NOT CREDIBLY IDENTIFIABLE IN ICLR 2026 |
| 6 Status as a Substitute for Expertise | 低 E reviewer 因识别作者身份而依赖 status | pre-release 描述 | 无3–4 | paper 质量和传播行为同时决定 status proxy、可见性和评价 | 否 | 冻结作者 status/出版记录、标题人工核验的发布时间、依法取得实际身份接触证据，以及独立的可见性规则/随机化日志。 | NOT CREDIBLY IDENTIFIABLE IN ICLR 2026 |
| 7 Peers as Competitors | 同等 expertise 下科学竞争导致战略性评价 | 竞争构念尚未建立 | 无3–4 | 竞争者拥有更精确的专业知识并采用合理的高标准 | 否 | pre-cutoff identity-validated publication/agenda、完整 dated coauthor graph、依法可链接 own submission、candidate E 与真实分配随机源、盲评技术基准。 | NOT CREDIBLY IDENTIFIABLE IN ICLR 2026 |
| 8 Who Should the Organization Listen To? | 组织对 expertise/confidence/status/proximity 的实际权重与应有权重 | incident-policy 预测需 labels | 无3–4 | 被采纳 reviewer 的未观测论证正确性及 AC 私人判断 | 否 | 合法完整 pre-discussion/edit/meta/decision、incident reset/freeze/AC 操作、真正外生意见暴露，以及独立技术质量/正确性标签。 | NOT CREDIBLY IDENTIFIABLE IN ICLR 2026 |

逐项精确 variation、最强反驳和决定性检验见 IDEA_1.md–IDEA_8.md。全局结论：不增加结果回归；优先获取/核验 assignment 制度与历史测量。无有效候选集时，连组织 frontier 的描述性反事实也不能计算。
