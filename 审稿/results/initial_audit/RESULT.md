# RESULT — Initial ICLR audit

## Summary

2026-10-03完成第一轮read-only项目与identification审计，需求为审稿/SPEC.md及WORK.md，基于main a2c36d4a9af697300c72ae9f9a4d3abdd8670ec1。找到项目G:\桌面\科研\项目-iclr审稿；原23个文件哈希校验未变。交付六份报告、聚合诊断、可复运行代码；未上传原身份数据。

## Files changed

本次只新增 `审稿/results/initial_audit/` 下：

- BLINDNESS_DESIGN.md
- code/audit.py
- code/coverage.py
- code/validate.py
- DATA_DICTIONARY.md
- EMPIRICAL_FACTS.md
- figures/distributions.svg
- MATCHING_DESIGN.md
- PROJECT_AUDIT.md
- README.md
- RESEARCH_OPTIONS.md
- RUN_METADATA.json
- tables/additional_coverage.csv
- tables/confidence_final_distribution.csv
- tables/confidence_initial_distribution.csv
- tables/date_ranges.csv
- tables/diagnostic_summary.csv
- tables/disagreement.csv
- tables/field_coverage.csv
- tables/file_inventory.csv
- tables/join_checks.csv
- tables/profile_coverage.csv
- tables/rating_final_distribution.csv
- tables/rating_initial_distribution.csv
- tables/review_versions.csv
- tables/reviews_per_paper.csv
- tables/snapshot_contrast.csv
- tables/timezone_checks.csv
- tables/within_paper_associations.csv
- tables/year_structure.csv
- VALIDATION.md
- RESULT.md（本文件）

## Key implementation decisions

- 不执行带登录或源文件写入的notebooks；从source/output追踪旧pipeline，明确reproduced vs traced only。
- 大JSON用流式解析；内容用SHA256核对，身份只用于本地集合连接且不导出。所有输出为aggregate统计；没有行级hashed人表。
- 不把名字推断当人口学真值，不把confidence当expertise，不制造accept、official affinity或blindness treatment。
- paper FE仅四个描述性诊断；剔除重复paper-reviewer组合，unknown保留缺失，SE按paper聚类；后续需处理reviewer跨paper相关性。
- native Git clone遭网络连接重置/失败，没有重复尝试登录或使用GUI；按已授权GitHub connector Git-data API发布，以已读main为parent，保持完整仓库base tree。

## Testing performed

实际运行audit.py全量29,813 reviews；coverage.py额外统计与75,748 notes时区比较；validate.py验证23源文件fingerprints、分布与sample totals、跨chunk JSON/truncated错误、missing历史不填0、上海时区、within transform与dummy FE一致、发布内容隐私pattern扫描。全部最终通过，版本见RUN_METADATA/VALIDATION。

早期运行出现内存不足与null profile错误，已修复并重跑成功；验证遇__pycache__后改为明确交付文件范围。没有声称网络采集或原探索图成功复现。原旧结果均在PROJECT_AUDIT逐项标记。

## Acceptance Criteria

- 项目、数据年份、表/ID/joins/missingness/scale：完成，有相对文件、cell/function、variable、N与输出路径。
- blindness：官方证据已核实2026 nominal double blind；不存在本地single-blind对照；实际曝光未知，事件并发机制列明。
- assignment：bidding/profile matching/AC adjustment有公开证据；算法/COI参数/完整candidate pool不可观测，未宣称随机。
- matching与outcomes：区分expertise/social/status；current/old snapshot血缘明确；无dated embeddings或声誉指标，未伪造替代。
- existing results：六个notebook文件（五个非空）及两份notes审计；原图和部分试验traced only；没有主回归结果被误标成已执行。
- Step4：year/distribution/review structure/social代理与paperFE/disagreement已执行；topic和reputation×regime明确不可估计原因。
- 六份指定报告与五个统一格式research options：完成。
- 隐私与原项目安全：仅代码、汇总、报告；原23文件未改；发布扫描通过。
- feature分支/commit/PR：本文件随分析提交；实际SHA与PR在发布后补充，不merge。

## Known issues

身份mapping原始取得来源不可公开复现；快照样本非会议人口；无完整revision/assignment/dated publication记录。arXiv匹配校验关闭，missing状态混杂。人口学标签无准确率证据。正式rating问卷锚点API返回403，报告只给Observed支持集。机构/合作proxy不能当朋友、prior COI或因果。没有真实final decision完整主表。docx内嵌截图未逐张核验，只作为notes探索描述。补齐数据后的研究设计留到下一轮。

## Branch

`feature/iclr-initial-audit-20261003`

## Commit SHA

Publication pending; analysis commit SHA will be recorded after remote creation. A later metadata-only commit can record its parent analysis SHA without circular self-reference.

## PR

Publication pending; URL will be appended after creation. No merge requested or performed.
