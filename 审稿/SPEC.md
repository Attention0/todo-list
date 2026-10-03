# ICLR 审稿项目 — SPEC

## 0. 本阶段目标

这是一个关于 ICLR 同行评审制度与 reviewer–author matching 的研究项目。当前已知的大方向包括：

- 单盲（single-blind）与双盲（double-blind）审稿；
- reviewer 与 author / paper 的匹配；
- reviewer 的专业匹配、熟悉程度、机构/地理/学术网络关系；
- review score、confidence、review text、最终接收等结果；
- 审稿制度、匹配机制与审稿行为之间的关系。

本阶段**不是**直接确定论文故事，也不是尽可能多跑回归。

第一目标是让 Chat 基于本地项目中的真实数据、代码和现有结果，准确回答：

1. 我们到底拥有什么数据？
2. 单盲/双盲在数据中到底如何出现，是否存在可以识别的制度变化？
3. reviewer–paper / reviewer–author matching 到底可以构造哪些变量？
4. assignment 是怎样产生的，哪些匹配可以近似视为外生，哪些明显存在 selection？
5. 当前项目已经做出了哪些事实，哪些只是设想？
6. 哪几个研究问题既有学术价值，又最可能被现有数据可信识别？

---

# 1. 项目地图：Chat 首先需要知道什么

请 Work 完整盘点本地 ICLR 项目，回答并记录：

## 1.1 文件与代码结构

识别：

- 项目根目录；
- 原始数据；
- 清洗后数据；
- 中间数据；
- reviewer / author / paper mapping 文件；
- OpenReview 或其他来源的抓取代码；
- 数据清洗脚本；
- matching / similarity / network 构造脚本；
- 回归脚本；
- 表格和作图脚本；
- notebooks；
- README / notes / 草稿；
- 已生成的 tables / figures / regression logs。

给出“当前 pipeline 最可能的执行顺序”。

如存在多个版本，指出哪个版本实际生成当前结果。

---

# 2. 数据来源与覆盖范围

## 2.1 数据来源

逐项说明数据来自哪里，例如：

- OpenReview；
- ICLR 官方页面；
- Semantic Scholar / OpenAlex / DBLP / Crossref；
- 自己构建的作者履历、机构、论文引用或合作网络；
- 其他外部数据。

对每个来源说明：

- 数据抓取/下载方式；
- 是否可公开复现；
- 最后更新时间；
- 数据覆盖年份；
- 是否存在 API / 页面结构变化；
- 是否有缺失年份或缺失字段。

## 2.2 年份与制度

逐年整理 ICLR 数据，至少给出：

| Year | Papers | Reviews | Reviewers | Authors | Blindness regime | 数据完整性 | 备注 |
|---|---:|---:|---:|---:|---|---|---|

不要根据文件名猜制度。

请寻找可验证的官方规则、项目文档或数据证据，确认每一年：

- single-blind / double-blind / 其他制度；
- 作者身份何时对 reviewer 可见；
- reviewer 身份何时对作者可见；
- rebuttal / discussion 的存在与时间；
- reviewer bidding / assignment 是否可观察；
- desk reject / withdrawn paper 如何处理；
- reviewer score scale 是否跨年一致；
- confidence scale 是否跨年一致。

如果制度变化并非整个会议统一发生，而是 track、阶段或字段层面的变化，明确说明。

---

# 3. 数据的观测单位与 ID 结构

明确列出所有主要表以及 unit of observation，例如：

- paper；
- author-paper；
- reviewer-paper assignment；
- review；
- review revision；
- reviewer；
- author；
- institution；
- historical publication；
- coauthor edge。

对所有关键 ID 说明：

- paper_id；
- review_id；
- reviewer_id；
- author_id；
- forum / submission id；
- institution id；
- external scholarly id。

检查：

- 是否能跨年份追踪同一个 reviewer；
- 是否能跨年份追踪同一个 author；
- reviewer 和 author 是否可能是同一人；
- 名称消歧是怎样做的；
- 多账号/重名/改名如何处理；
- reviewer identity 有多少比例可以可靠链接到公开学术身份。

给出主要 join 的成功率和失败率。

---

# 4. Reviewer–paper / reviewer–author matching

这是本项目的核心之一。

请盘点现有代码中已经存在或可以可靠构造的 matching measures。

## 4.1 Topic / expertise matching

例如：

- reviewer 历史论文与 submission abstract/title/full text 的 embedding similarity；
- keyword / subject overlap；
- reviewer bidding；
- reviewer self-reported expertise；
- historical publication field；
- reviewer confidence（注意 confidence 是 outcome/自报信号，不应自动等同于 ex ante expertise）。

请说明每个指标的信息时点，防止使用审稿之后的信息预测审稿之前的 matching。

## 4.2 Social / academic proximity

检查能否构造：

- reviewer 与任一 author 是否曾共同署名；
- shortest coauthor-network distance；
- shared prior coauthors；
- same institution；
- previous same institution；
- same advisor / academic genealogy（若已有）；
- same country / region；
- attended same conference/lab 等（只在数据实际支持时考虑）。

尤其注意：**不能把简单的姓名/机构重合直接解释为“认识”。**

## 4.3 Status / reputation matching

检查是否已有：

- author citations；
- h-index；
- prior top-conference publications；
- prior ICLR acceptances；
- institution prestige；
- reviewer reputation；
- reviewer seniority；
- paper-team reputation。

所有声誉指标尽量使用 review decision 之前可观察的信息构造。

## 4.4 Demographic matching

如果项目已经可靠构造性别或其他人口学变量，报告：

- 数据来源；
- coverage；
- inference 方法；
- accuracy / uncertainty；
- missingness。

不要为了补齐覆盖率而强行推断人口学属性。

---

# 5. Review 与 decision outcomes

盘点可以使用的结果变量及其跨年可比性：

- initial score；
- final score；
- score revision；
- confidence；
- review length；
- review sentiment / tone；
- textual specificity；
- criticism / praise；
- review disagreement；
- variance across reviewers；
- rebuttal 后更新；
- reviewer discussion activity；
- meta-review / area-chair recommendation；
- accept / reject；
- oral / spotlight 等更高层级 decision（若存在）；
- reviewer response speed / timing（若时间戳存在）。

对 score / confidence 必须记录每年量表。

如果跨年量表改变，构造 harmonized version 时同时保留原始量表。

---

# 6. Assignment mechanism：识别的关键

请尽可能还原 reviewer assignment 的形成机制。

寻找数据或文档回答：

- 是否有 reviewer bids？
- 是否有 TPMS / affinity score / keyword matching？
- area chair 是否人工调整？
- conflicts of interest 如何定义？
- reviewer load / capacity 是否观察到？
- reviewer pool 如何形成？
- paper 被分配几个 reviewers？
- 是否存在随机成分、阈值、容量约束或算法变化？
- assignment algorithm 是否跨年变化？

这是未来识别 reviewer–paper matching effect 的核心。

请特别区分：

1. **自然形成的 matching correlation**；
2. 在可比 paper / reviewer 条件下的 conditional matching；
3. algorithm / capacity / threshold induced quasi-random assignment；
4. 真正可以支持 causal interpretation 的设计。

除非有证据，不要把 matching regression 称为因果。

---

# 7. 单盲 vs 双盲：需要特别审计什么

我们需要知道是否存在可信的 blindness variation。

请系统检查：

- ICLR 哪些年份、阶段或 track 发生制度切换；
- switch 是否与其他审稿制度同时变化；
- 同年是否存在 treatment / control；
- reviewer 在打初始分时究竟能看到哪些作者信息；
- 作者 identity 是否可能从 PDF、arXiv、GitHub、topic、self-citation 中被 reviewer 推断；
- paper 是否在 review 前已经公开到 arXiv；
- high-reputation authors 是否更容易被 deanonymize；
- blind review 是否只是 nominal blindness。

如果存在 single → double blind 的会议级时间变化，不要直接把 before/after 当作因果。

需检查可用设计，例如：

- discontinuity / staggered policy change；
- differential exposure to deanonymization；
- triple differences；
- author reputation × blindness；
- institutional prestige × blindness；
- prior familiarity × blindness；
- arXiv exposure × blindness；
- within-paper reviewer differences（若可行）。

同时列出最严重的 concurrent changes。

---

# 8. 当前已有分析

找到所有已经存在的：

- descriptive statistics；
- balance tables；
- regression tables；
- event-study / DiD；
- matching analyses；
- text analyses；
- heterogeneity analyses；
- ML / embedding analyses；
- figures。

对于每一个主要结果，记录：

- 使用数据；
- sample；
- specification；
- treatment；
- outcome；
- controls；
- fixed effects；
- standard errors；
- effect size；
- 是否可复现；
- 目前最大的识别风险。

不要只复制表格；说明这些结果实际上在回答什么问题。

---

# 9. 第一轮最值得验证的 empirical facts

在不预设最终论文故事的情况下，优先验证以下事实中**数据确实支持的部分**：

1. 不同年份 reviewer assignment / reviews / scores 的基本结构是否稳定？
2. reviewer–paper topic similarity 是否显著预测 reviewer confidence？
3. topic similarity 是否预测 score，以及 within-paper 比较后关系是否仍存在？
4. reviewer 与 author 的 prior coauthor / institution / network proximity 有多常见？
5. social proximity 是否对应更高 confidence、更高 score、更短/更长 review 或不同文本？
6. author reputation 与 score / accept 的关系在 single-blind 和 double-blind 环境是否不同？
7. institutional prestige 与上述结果是否存在类似变化？
8. blind regime 下 reviewer 是否仍能通过 arXiv / prior relationship / topic clues 推断 author identity？
9. 同一 paper 的 reviewers 之间，expertise / proximity 差异是否能解释 score disagreement？
10. reviewer expertise 与 author status 是否在 assignment 环节本身就非随机匹配？

这些只是 diagnosis，不代表最终论文必须包含全部内容。

---

# 10. 潜在研究问题池

Work 在完成数据审计后，可以评估以下问题的**可行性**，但不要强行得出结论。

### A. Blind review and status bias

Blindness 是否改变 reviewer 对作者声誉、机构声誉或既有学术地位的反应？

### B. Blindness and social proximity

匿名是否削弱 reviewer–author prior proximity 对评分/文本/讨论行为的关联？

### C. Expertise matching

更匹配的 reviewer 是否给出不同的 score、更高 confidence、更高 agreement 或更高质量的 review？

### D. Familiarity vs expertise

“懂这篇论文”与“认识/接近作者”可能同时提高 matching。能否将 topic expertise 与 social familiarity 分开？

### E. Assignment and evaluation

看似存在于评分阶段的 bias，有多少其实来自 reviewer assignment stage？

### F. Disagreement as information

同一 paper 内不同 reviewer 的 expertise / proximity 差异，是否系统性地产生 disagreement？AC/decision 如何聚合这些异质信号？

### G. Deanonymization

双盲制度的实际 treatment 是否应理解为“降低 author observability”，而非简单的制度 dummy？

最终优先级必须由真实数据与识别质量决定。

---

# 11. 隐私、复现与 Git 纪律

该项目涉及 reviewer / author 身份信息。

**禁止把以下内容提交到 todo-list Git 仓库：**

- 原始 reviewer identity 表；
- 私有邮箱；
- 未公开联系方式；
- respondent/person-level sensitive data；
- 不必要的逐人可识别数据；
- access tokens / API keys。

可以提交：

- 代码；
- 数据字典；
- aggregate statistics；
- 去标识化/hashed ID 的必要中间结果；
- tables / figures；
- 审计报告；
- 可公开来源链接。

如果本地项目本身已有公开 reviewer identity，也不要为了方便把整份 identity 数据复制到这个 todo-list 仓库。

---

# 12. 第一轮完成后 Chat 最需要的输出

将第一轮结果写入：

`审稿/results/initial_audit/`

至少包括：

1. `PROJECT_AUDIT.md`  
   项目结构、数据源、年份、ID、pipeline、现有结果。

2. `DATA_DICTIONARY.md`  
   核心表、变量、观测单位、coverage、missingness、跨年一致性。

3. `BLINDNESS_DESIGN.md`  
   单/双盲制度事实、可识别 variation、同时发生的制度变化、潜在设计与威胁。

4. `MATCHING_DESIGN.md`  
   assignment mechanism、已有 matching 指标、可以新增的指标、selection / identification 风险。

5. `EMPIRICAL_FACTS.md`  
   5–10 个最重要的初步事实，尽量附 aggregate tables / figures。

6. `RESEARCH_OPTIONS.md`  
   基于实际数据提出 3–6 个可行研究问题。对每一个写：
   - question；
   - treatment / variation；
   - outcome；
   - identification；
   - biggest threat；
   - additional data needed；
   - 是否值得下一轮继续。

第一轮不要写完整论文，不要为了迎合某个故事选择性汇报结果。

Chat 将依据这些文件决定下一轮研究设计。
