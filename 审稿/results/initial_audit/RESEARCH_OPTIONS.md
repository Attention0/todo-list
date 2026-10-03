# Research options

五个问题不按直觉排名。当前没有feasible now的因果设计；状态区分可以立即描述和仍需数据构造的研究。

### Question 1 — Review snapshot integrity

**Question**  
已有快照与后来保存的note究竟对应哪些版本，哪些评分变化真实发生？

**Empirical variation**  
同一review ID跨两个保存时点；真正edits panel待补

**Treatment / key X**  
verified edit stage / snapshot time

**Outcomes**  
score/confidence/text change

**Preferred specification / design**  
先建立revision lineage，按官方冻结/回退时间归档；只做配对描述

**Why it may be informative**  
避免把回退或字段误命名当行为改变

**Biggest identification threat**  
两个snapshot时点缺精确获取日志；version2不是完整历史

**Current evidence**  
29813 old snapshot texts全部匹配，29766 later current notes匹配，1881对rating不同；对应tables与PROJECT_AUDIT，不是其他已发表研究的实证结论。

**Additional data / work needed**  
官方公开edit历史/本地合法历史备份、抓取日志、freeze状态

**Status**  
- feasible with additional construction

### Question 2 — Expertise and evaluation

**Question**  
事前专业接近是否与confidence、评分和分歧有关？

**Empirical variation**  
同一paper不同reviewer的事前publication topic差异

**Treatment / key X**  
dated publication→submission similarity

**Outcomes**  
confidence/score/review specificity/disagreement

**Preferred specification / design**  
历史截止publication语料构造预先固定similarity；paper与reviewer FE；与bids/affinity对照，条件关联

**Why it may be informative**  
直接区分自报confidence和专业覆盖

**Biggest identification threat**  
assignment的affinity/bids selection、paper-reviewer特殊质量维度

**Current evidence**  
有self-report expertise、paper abstract/keywords，尚无可信pair similarity；对应tables与PROJECT_AUDIT，不是其他已发表研究的实证结论。

**Additional data / work needed**  
合法dated publication文本与ID、冻结submission文本、assignment条件；文本质量需验证

**Status**  
- feasible with additional construction

### Question 3 — Proximity versus expertise

**Question**  
在topic条件相近的review者中，事前学术接近与评分/评语是否有关？

**Empirical variation**  
同论文内可验证的prior coauthor/institution/network差异

**Treatment / key X**  
dated coauthor/overlap + independently measured expertise

**Outcomes**  
score/confidence/word count/criticism-specificity

**Preferred specification / design**  
paper FE + reviewer FE + dated topic covariates；双向聚类与unknown敏感性，不直接因果

**Why it may be informative**  
当前已看到proxy可构造且有within-paper变化

**Biggest identification threat**  
COI截断选择、网络与topic共变；缺日期/收录不能当无关系

**Current evidence**  
机构proxy 1325 informative papers，合作proxy108；四个弱关联诊断；对应tables与PROJECT_AUDIT，不是其他已发表研究的实证结论。

**Additional data / work needed**  
publication dates、去掉本次submission边、关系有效日期、完整COI规则、文本人工validation

**Status**  
- feasible with additional construction

### Question 4 — Public exposure and matching

**Question**  
验证的事前arXiv公开程度是否改变proximity与评价之间的关联？

**Empirical variation**  
同一2026nominal double-blind里paper preprint候选差异及reviewer proximity

**Treatment / key X**  
verified pre-review arXiv × prior proximity

**Outcomes**  
score/confidence/review text

**Preferred specification / design**  
paper FE下估计交互项；明确paper-levelarXiv主效应被吸收，先做异质关联

**Why it may be informative**  
能描述nominal blindness下公开身份线索可能起作用的边界

**Biggest identification threat**  
arXiv publication选择与quality、实际识别不观察，网络也带expertise

**Current evidence**  
3433篇有首命中匹配；现有校验关闭，不能认定已deanonymized；对应tables与PROJECT_AUDIT，不是其他已发表研究的实证结论。

**Additional data / work needed**  
title/author/abstract/entity validation、首版日期、完整查询日志、dated expertise/proximity

**Status**  
- feasible with additional construction

### Question 5 — Evaluation disagreement and aggregation

**Question**  
不同review者的知识/接近差异是否与分歧及AC聚合有关？

**Empirical variation**  
paper内rating分散、reviewer异质性；决策样本待补

**Treatment / key X**  
within-paper expertise/proximity dispersion

**Outcomes**  
score SD、meta-review/true accept/decision tier

**Preferred specification / design**  
先描述分歧，再对真实decision做paper-level预测；不从score制造accept

**Why it may be informative**  
把review异质信息与后端decision分开

**Biggest identification threat**  
审稿人非随机，decision条件selection、因安全事件AC变化

**Current evidence**  
mixed institution组平均SD约1.49、非mixed约1.47，尚无可靠AC/decision主表；对应tables与PROJECT_AUDIT，不是其他已发表研究的实证结论。

**Additional data / work needed**  
验证expertise、实际decision/metareview、new AC assignment、完整withdrawn/desk-reject状态

**Status**  
- descriptive only

## 目前不应投入的设计

Blindness×author prestige、会议before/after、泄露DiD目前currently infeasible：没有可验证single-blind对照、dated声誉或实际曝光面板。未来引用不能直接辨别favoritism与信息优势，因为录用选择、曝光资源与引用领域差异影响outcome；notes里相应“铁证”论断不是已识别结果。先修复数据时点与变量，而非继续specification搜索。
