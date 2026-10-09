# RESULT — mover identification benchmark audit

2026-10-07。Branch: `feature/fertility-mover-benchmark-20261007`。本轮按最新 `fertility/WORK.md` 和 `MOVER_BENCHMARK_AUDIT_WORKORDER.md` 执行；不做机制，不新增因果回归。

## Summary

交付“婚 + 育”共同主结果的识别路线图。Labour Economics 已有相当多防御，不能误写成未做婚姻、意愿、灾害、IV、多次迁移或州聚类。仍然脆弱的是同步家庭计划与去向选择、IV排除限制、前趋势信息量和动态/方差解释；CMDS 另有更基础的测量与入选问题。

## 六个最终问题

### 1. Minimum 5–10 elements

八项：明确迁移事件与独立处理；合法的两类人口/风险集；目的地可比性及组内来源动态；婚育计划反向因果；有信息量的迁前诊断；重复迁移与留存；动态estimand/比较组；正确依赖结构与有效信息量。测量前提未通过，不作因果结论。

### 2. Wu & Zhu 已完成哪些？

个体与时间FE、实际PSID居住州、外部种族特异NCHS环境、迁前图、observables及主/次动机、有限波次迁前生育意愿、婚姻进入、母亲特征PCA、灾害子样本、同源地其他movers IV、匹配nonmovers、mover-only、balanced、剔job-change与重复movers、替代环境和州聚类；AKM有最大connected set。逐项页码/表图见审计。

### 3. Labour 最重要的 3–5 个缺口

1. 平坦leads、动机和婚姻零结果仍不能排除迁移附近的怀孕/家庭计划与去向共同决定。
2. 同源均值leave-person-out IV不等于外生；灾害触发也未随机化目的地。
3. 两个独立leads、90%CI不足以说明可排除多大的偏差；需经济量级/联合检验/敏感性。
4. 孩次分量不是parity风险集hazard；短期累加不是完成生育；失访/限制样本的目标人群须明确。
5. 若保留因果方差份额，AKM还需leave-out/噪声修正；零person-place covariance不证明无时变选择。

### 4. 额外 3–5 个 CMDS 威胁

户籍不是真前址、到达不等于完整spell；当前master按出生史入选，漏掉2012–16的63,336位当前未婚女性；2017 roster非完整出生史且没有可用婚期；目的地stock未观察退出者；省CBR构成率与细地方/婚姻环境不等价，当前covariates也不是迁前历史。数字承接PR #22核验，本轮未重跑。

### 5. 两类风险集 / event studies 怎样分别做？

婚从独立female base恢复，年初未初婚为风险集，事件后退出；未知婚期不填未婚，2016/18同居口径另列。生育分别为all eligible的any birth、年初parity0的first birth、parity1的second transition。未知历史不填零；同年/双胞胎与部分访谈年明确处理。

每年风险集的hazard与固定较早基线组的累计发生概率并列。不能先筛到达前未婚/无孩再以结构性全零leads证明无选择。r以当前到达计时；缺月份不强排顺序。总生育效果不控制迁后婚姻；迁前已进入婚/同居者是另一个estimand，非完整当前已婚史。

### 6. 下一步先跑哪 5–10 项？

按序8项：P1两套风险人口/边界测试；P2迁移时钟、来源质量和Δ支持；P3近迁移婚育/孕期假设与动机诊断；P4分Y动态、累计曲线和pretrend信息量；P5同来源×cohort支持与动态比较；P6路径质量/stock留存诊断；P7crossed geography及少簇推断；P8独立群体环境竞争预测。第一批是P1–P3的重建/描述，P8需前项支持。没有现成有效IV，不先跑机制或方差分解。

## Files changed

- `fertility/MOVER_LITERATURE_IDENTIFICATION_MAP.md`：12篇本地PDF的版本/阅读记录；共同17列表；四组必读对照；定向近期/方法检索；检验→威胁→残余解释。
- `fertility/LABOUR_E_IDENTIFICATION_AUDIT.md`：完整29页正文及内嵌附录的逐项对账；A–J和Tier1/2/3；复现待核问题单。
- `fertility/MOVER_CORE_CHECKLIST.md`：两类Y、风险集/动态估计约束、8项优先任务与A/B/C、所需变量、样本成本、通过/失败解释。
- `RESULT.md`：本交付记录。未修改SPEC/WORK、旧数据定义、业务代码或微观数据。

## Key implementation decisions

main基准 `1874d375231ed6a6a040bc8df0d336b5fc48474d`。原生Git同步遇到连接重置，按用户工作流转已授权GitHub API发布，不反复登录/网页上传。前轮数据文件在PR #22，main读取404；用固定commit链接依赖，未擅自merge或复制其未合并改动。旧本地未提交文件保留。

本轮主来源是本地全文，区分正式版/工作稿。扫描酒精论文用页面核看及作者会议稿补充；非核心独立online appendix未取得的项目明确标“未核”。不上传受版权保护PDF/提取文本。文献改善的是识别判断，不是宣布我们的因果估计已成立。

## Testing performed

- 实际：读取最新任务与SPEC；系统清点本地12PDF+笔记，提取全文、识别段落及页码；Labour全文与内嵌附录逐项核验，关键页面图像复核；定向检索官方期刊/作者资料。
- 实际：读取前轮两份数据审计并核对本轮引用的关键计数和可行性边界；没有重跑微观数据审计。
- 实际文档验收 PASS：4文件、9个Markdown表（文献17列/任务12列）、所有相对链接、11个任务包ID、A–J覆盖、6个最终问题及RESULT必需section均通过自动检查；检查不是对实证识别有效性的统计检验。
- 未执行：PSID replication、CMDS新回归、机制、外部新数据合并或文中下一轮风险集测试。这里交付的是已核文献路线图，不是这些实证工作已通过。

## Acceptance Criteria

- [x] 最新工单要求的三份文件及RESULT存在。
- [x] benchmark正文和同PDF附录、已有防御和真实缺口分开；页码可追溯。
- [x] 至少FGW、Chetty–Hendren、Cantoni–Pons、Chyn–Shenhav及本地其他相关研究对照；近期定向补检索。
- [x] 婚与育共同主结果；独立风险集、退出/累计量、禁止控制迁后婚姻。
- [x] Tier0/1/2/3、A/B/C、样本成本和8项优先分析；不伪装未知为可行。
- [x] 无机制或新因果模型；不改原SPEC/WORK、不merge。
- [x] GitHub已发布并创建PR #23；创建返回4个新增文件、无删除；随后更新本记录元数据并回读核验。

## Known issues

主要数据识别缺口未被文字审计消除；完整返乡/退出与前居住轨迹仍缺。Labour计量实现有时间聚合/单位、r=0、Table2计数、脚注13差值及Table3/5加总待代码复现核对；这些仅是待核，不指称已证伪。对照论文的所有外置appendix未逐一下载，未核项目不用于断言作者没做。

## Branch / Commit SHA / PR

- Branch: `feature/fertility-mover-benchmark-20261007`
- Commit SHA（完整审计快照）: `aaf17f8581b3fd2583fc9d2436d272edcec7640f`。后续提交仅更新本RESULT的发布元数据；最终分支head以PR为准，避免自引用SHA。
- PR: [#23 — mover identification benchmark audit](https://github.com/Attention0/todo-list/pull/23)，open；不自动merge。
