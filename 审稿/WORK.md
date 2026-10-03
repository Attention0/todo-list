# ICLR 审稿项目 — WORK

## 任务性质

这是一次 **initial project audit + identification audit**。

先阅读：

1. `审稿/SPEC.md`
2. 本地 ICLR 审稿项目中的 README / notes / code / data documentation

本轮不要直接写论文，也不要为了得到显著结果批量跑 specification。

目标是让 Chat 能基于真实项目证据判断：
- 数据到底有什么；
- single/double blind 的 variation 是否可用；
- reviewer–author / reviewer–paper matching 怎样形成；
- 已有结果做到哪里；
- 哪些研究问题真正值得继续。

---

## Step 1. 定位本地项目

在本地工作环境中找到用户所说的 ICLR 审稿项目。

优先根据以下关键词识别：
- ICLR
- OpenReview
- review / reviewer
- blind / blindness
- matching / assignment
- author
- score / confidence
- rebuttal

如果存在多个候选目录，比较 README、数据文件和脚本后识别最可能的项目根目录，并在审计报告中说明判断依据。

**不要移动、删除或覆盖原始项目文件。**

---

## Step 2. 阅读而不是先重跑

先完整查看：

- repository / directory tree；
- README；
- data dictionaries；
- notebooks；
- cleaning scripts；
- analysis scripts；
- generated outputs；
- existing manuscript / notes（若有）。

识别 pipeline 和当前 main analysis。

如代码版本冲突，找出真正生成当前 outputs 的版本。

---

## Step 3. 按 SPEC 完成四项核心审计

### A. Data audit

核实年份、来源、tables、units、IDs、joins、missingness、score scale、identity linkage。

### B. Blindness audit

核实每年/阶段真实 blind regime，不允许仅凭文件名或研究者注释推断。

如本地没有制度文档，可以使用公开可靠来源核实制度，但在输出中给出处。

### C. Matching / assignment audit

区分：
- topic expertise；
- social proximity；
- status similarity；
- demographics；
- assignment mechanism。

重点寻找 bids、affinity、conflict、capacity、algorithm、AC manual adjustment 等信息。

### D. Existing-result audit

复现或追踪现有主要 tables / figures / regressions。

如果完整重跑成本过高，可以先用代码路径 + 已有 outputs 核对，但必须标记“reproduced”还是“traced only”。

---

## Step 4. 做一轮最小但高价值的诊断分析

在不破坏现有 pipeline 的前提下，优先生成少量能决定研究方向的 aggregate diagnostics。

至少尝试（若数据允许）：

1. year-level sample / review structure table；
2. score / confidence distributions by year；
3. paper-level number of reviewers；
4. reviewer-paper topic similarity distribution；
5. topic similarity → confidence；
6. topic similarity → score，尤其是 paper fixed effects / within-paper comparison；
7. social proximity prevalence；
8. social proximity → score / confidence（先明确 selection）；
9. author/institution reputation × blindness regime 的 descriptive / regression contrast；
10. reviewer expertise/proximity 与 within-paper disagreement。

不要因为某项做不了而伪造替代变量。做不了就解释缺什么。

---

## Step 5. 输出到 Git

把代码修改、aggregate results 和审计文档提交到：

`审稿/results/initial_audit/`

至少创建：

- `PROJECT_AUDIT.md`
- `DATA_DICTIONARY.md`
- `BLINDNESS_DESIGN.md`
- `MATCHING_DESIGN.md`
- `EMPIRICAL_FACTS.md`
- `RESEARCH_OPTIONS.md`

图表可以放：
`审稿/results/initial_audit/figures/`

表格可以放：
`审稿/results/initial_audit/tables/`

如新增脚本，放：
`审稿/results/initial_audit/code/`

---

## Step 6. RESEARCH_OPTIONS 的格式

最终给 Chat 的每个候选研究问题使用统一格式：

### Question X — [short title]

**Question**  
一句话。

**Empirical variation**  
真正可用的 variation 是什么。

**Treatment / key X**

**Outcomes**

**Preferred specification / design**

**Why it may be informative**

**Biggest identification threat**

**Current evidence**

**Additional data / work needed**

**Status**
- feasible now
- feasible with additional construction
- descriptive only
- currently infeasible

不要给“Top 1 / Top 2”这类仅凭直觉的排序。Chat 会在看到证据后再决定主线。

---

## Step 7. Evidence discipline

所有结论尽量附：

- file path；
- script/function；
- variable name；
- year；
- sample N；
- missingness；
- specification；
- output path。

明确区分：

- **Observed in raw/clean data**
- **Constructed**
- **Inferred**
- **Assumed**
- **Not observable**

不要把 reviewer confidence 自动称为 expertise。
不要把 same institution / coauthor distance 自动称为 friendship。
不要把 before/after blindness dummy 自动称为 causal effect。
不要把 assignment 后观察到的变量当作 ex ante matching covariate。

---

## Step 8. Privacy / Git safety

不要向 todo-list 仓库提交：

- raw private/person-level reviewer identity files；
- emails；
- private contact information；
- credentials；
- tokens；
- API keys；
- 不必要的逐人可识别记录。

只提交代码、aggregate outputs、必要的去标识化结果和文档。

---

## 完成标准

这一轮完成时，Chat 应该不需要猜测即可回答：

1. 数据覆盖哪几年？
2. 哪些年份到底是 single / double blind？
3. blind treatment 在现实中有多“干净”？
4. reviewer assignment 到底是怎么产生的？
5. expertise、familiarity、status 三种 matching 能否区分？
6. 哪些 outcomes 最可靠？
7. 现有代码已经做了什么？
8. 最有希望的 3–6 个 research designs 是什么？
9. 每个 design 最大的 endogeneity / selection 问题是什么？
10. 下一轮最值得花算力和研究时间验证什么？

完成后 commit + push，并在 Work 对话中只需简洁汇报：
- 找到的项目根目录；
- 新增/修改的文件；
- 最重要的 5 条发现；
- Git commit SHA。
