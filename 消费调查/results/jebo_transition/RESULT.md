# JEBO transition result

## Summary

本轮完整执行冻结的 JEBO transition plan，最终选择 **Story C**：现金的报告支出份额随金额下降，完整分布与描述性分解说明这种下降主要伴随正响应组的条件份额降低；Food 和 Medical 提供分别呈现的比较。形式间斜率差异仍为 suggestive，不把重新定位当成统计证据升级。Bernard (2023) 已联合研究金额与支付形式，并分解响应边际，因此撤回“首次联合设计／首次分解”的创新主张。可保留的增量是具体受限用途、三个名义金额、完整响应分布以及差异梯度的不确定性；增量有限，但比原来的宽泛故事更准确。

新增分解改善了经济描述，没有提供独立复制或识别心理机制。Cash 的 200→5,000 元 midpoint 均值变化为 −5.136 个百分点，参与部分 −0.021，条件正响应部分 −5.114。Food 对应 −3.205、+0.337、−3.542；Medical 对应 +0.115、+0.879、−0.764。后处理条件组与对称乘积分解都是描述性对象。

## Literature and JEBO position

已读取并原样引入 GitHub main 提交 7b6ca3f 的 `消费调查/LITERATURE_BENCHMARK_SURVEY_CONSUMPTION.md`。本轮地图含 54 篇文章与一个另列的经典书章，其中 13 篇用于近年 JEBO 对照。正文引用 30 项。逐行记录发表状态、原文／工作稿／摘要访问范围，不把工作稿版式或摘要信息冒充最终发表版全文。

最近邻是 Bernard；Fuster–Kaplan–Zafar 提供响应边际的直接比较；Boehm–Fize–Jaravel 提供真实消费与转移形式的对照；Lee、Pauls–Laudi 和 Pavlova 提供 JEBO 中形式、框架与测量的参照。详见 GITHUB_LITERATURE_RECONCILIATION.md。旧文献笔记中的 portability/ML 主线没有重新启动。

## Evidence and interpretation

- 较强证据：Cash 内部金额梯度、原始分布，以及既定局部校正下的最高档形式／金额主效应。Cash ordinal 趋势的 p 值明确标为 nominal。
- 保持 suggestive：Top75 交互 omnibus Holm21=0.180508、min-P21=0.082092；Cash–Medical 为 0.079229/0.039096。没有只挑显著的一个调整值。
- 未确认交叉：5,000 元 Food–Cash 的 Top75 差为 +2.17 pp，pointwise CI [−0.63,4.97]，Holm6=0.387。
- 未识别机制：心理账户、相对规模与计划期限均未直接测量；Food bindingness 三重交互不能被用来排除机械约束。
- 不把 Q1/Q2 零差异、150-variable null 或人口校准解释为等价、无异质性或全国代表性。

## Files changed and key implementation decisions

新稿目录：`消费调查/manuscript/jebo_v1/`。

- `JEBO_manuscript_v1.md` / `.docx`：9 个编号章节，180 词摘要、1,583 词引言，作者—年份引用、关键词与 JEL；正文 17 页，包括 3 表、3 图。
- `JEBO_supplement_v1.md` / `.docx`：10 节、15 表、13 页。
- `JEBO_CLAIM_LEDGER.csv`：119 个实质段落／表格块，记录类型、强度、具体来源和措辞限制。
- `JEBO_REFERENCE_AUDIT.csv`：30 条正文引用及来源范围；`SOURCE_MANIFEST.md`、`AUTHOR_INFORMATION_REQUIRED.md`。
- `figures/fig1_atlas`, `fig2_curves`, `fig3_margins`：各 PNG/PDF/SVG，附源 CSV。复用 PR14 atlas 几何和顺序渐变，改用 PR16 成人汇总量，避免混用历史全样本。
- `消费调查/results/jebo_transition/`：冻结协议、证据表、文献地图、期刊参照、概念表、故事选择、新分解及复现和验收记录。

相对 NC v5，正文按经济问题→随机设计→现金梯度→形式比较→分布分解→解释边界重新组织。历史 1,500 检验、420 规格、ordered 模型、relative-scale、bindingness、Q1/Q2、收入描述、人口校准和 all-X/who-drives 留在补充材料与来源目录。主文不再呈现审稿流程或机器学习故事。历史包均未改写。

## Testing performed

实际执行的检查如下，详见 verification_results.json、deterministic_reproduction.json 和 final_audit.json：

1. 395 个历史文件逐一 SHA-256 比对，全部不变。
2. 从成人 54 个分类计数独立复核 63 个 profile 均值，最大误差 5.56e−17；N=5,480。
3. 独立 grouped HC3 计算核对 21 个组内斜率与标准误，最大误差 2.39e−15；复核 21 个 nominal 交互 p 值及 Holm 校正。
4. 九格乘积恒等式、三个端点分解与全部 bootstrap 分解通过 1e−14 容差。
5. 固定种子 2026100316、4,000 次固定格子大小抽样；无零正响应 draw。重复运行四个分析输出逐字节一致。
6. 图表成人样本、3 个单页矢量图、DOCX 表图结构、摘要／引言长度、引用覆盖、119 个 claim blocks 与最终文本对应关系通过。
7. 主文 17 页、补充 13 页及 3 个独立图 PDF 逐页／逐图检查；修复排版问题后复查，见 VISUAL_QA.md。

没有重新运行历史 respondent-level 模型或 min-P 模拟；其既有输出与限制明确引用。没有新增显著性检验、阈值、样本筛选、调节变量或校正家族。

## Acceptance Criteria

| 要求 | 结果 |
|---|---|
| 从 PR16 最新 head 建 stacked 分支 | 满足；基点 f3124aa，发布前再次核对未变化 |
| 分析前冻结，写作前故事决策 | 满足；950e90f / b6e7b22 |
| 有限新分析与停止规则 | 满足；只有既定分解，后续仅复现与校验 |
| 35–60 篇文献、近期 JEBO 对照 | 满足；54 / 13，访问局限逐项标注 |
| 创新遇到最近邻时重新定位 | 满足；Story C，明确 Bernard 重叠 |
| 新稿、补充、图、来源与声明审计 | 满足；独立 jebo_v1 目录 |
| 不改历史结果、不上传个体数据、不 merge | 满足；历史哈希及发布范围检查 |
| 投稿所需真实作者信息 | 尚待作者补齐，单列清单，不虚构 |

## Final intellectual check

只看标题、摘要、Figure 1 与前两页，读者能看到“金额如何改变报告支出的分布，以及受限资源提供何种比较”的具体问题，且能看到最接近前人的边界。进一步阅读推断部分不会突然发现被隐藏的非显著 omnibus：摘要已写明交互为 suggestive，引言和结果均报告两个既定校正值。故事清楚可信，但其新颖性和假设性结果仍可能不足以满足编辑；本轮不以继续挖掘来掩盖这一风险。

## Known issues

本包是可供作者审阅的 JEBO 风格稿，不是已经满足全部投稿手续的成稿。招募日期／渠道、随机化与停止记录、伦理与同意、资金／贡献／利益冲突、数据共享权限仍需真实文件。官方 Guide for Authors 访问返回 403，不能声称已核实最新匿名化、行距或门户附件规则。部分文献只有官方摘要或工作稿全文，缺失的最终版结构信息已标注。假设性分档、无统一明确期限、组合处理和事后分析史是研究本身的限制。

`git diff --check` 对原样引入的 JEBO_SPEC.md 与长期文献库报告原有 Markdown 双空格换行；未改写这两个源文件。新建交付目录单独通过 whitespace 检查，生成 SVG 的行尾空格已规范化。

## Branch, Commit SHA and PR

- Branch: `feature/jebo-repositioning`
- Stacked base: `feature/nc-evidence-revision`
- Base commit: `f3124aa820e0b4de3540aaaeb64ffdeb7ca19228`
- Protocol commit: `950e90f`
- Story-gate commit: `b6e7b22`
- Delivery commit: recorded after the manuscript commit, in the follow-up metadata commit.
- PR: recorded immediately after creation. No old PR will be merged.
