# ICLR initial project audit

审计日期：2026-10-03（Asia/Shanghai）。需求基线：Attention0/todo-list main `a2c36d4a9af697300c72ae9f9a4d3abdd8670ec1` 的 `审稿/SPEC.md` 与 `审稿/WORK.md`。没有修改需求或原项目。

## 项目定位与范围

根目录：`G:\桌面\科研\项目-iclr审稿`。依据是五个非空 notebooks、完整 review/submission/profile/coauthor 数据及两份项目 notes，内容一致指向 ICLR 2026；目录没有 `.git`、README、独立回归脚本、环境锁文件或自动化入口。`G:\桌面\科研\文章-iclr审稿` 为相关文献 PDF 和文献概览，属于辅助文献目录，不是数据 pipeline；微信附件中的同名 JSONL 是候选输入副本，未作为另一个研究项目或独立样本使用。

原目录共 23 个文件：6 个 ipynb（`nameprism查询.ipynb` 为零字节）、2 个 docx、15 个数据文件。完整相对路径、大小、UTC 修改时间、SHA256 见 [file_inventory.csv](tables/file_inventory.csv)。读取了所有非空 notebook 的全部 source 和 output 类型、两份 docx 的文字及全部核心 JSON/CSV；没有运行含登录信息或覆盖源文件的原 notebook。未逐张核验 docx 内嵌截图，相关图表只能 traced only。

## 数据与覆盖

|   year |   raw_papers |   raw_papers_with_reviews |   raw_reviews |   main_rows |   main_papers |   main_reviewers |   main_authors |   raw_reviewers |   raw_authors |   public_submissions |   public_review_rows |   public_unique_review_ids |   comment_rows |   comment_papers |   reviewer_author_overlap | regime                                             |
|-------:|-------------:|--------------------------:|--------------:|------------:|--------------:|-----------------:|---------------:|----------------:|--------------:|---------------------:|---------------------:|---------------------------:|---------------:|-----------------:|--------------------------:|:---------------------------------------------------|
|   2026 |        10090 |                      7655 |         29813 |       29813 |          7655 |            13560 |          28465 |           13560 |         31817 |                19602 |                75748 |                      75748 |         167342 |            14031 |                      5820 | nominal double blind; incident exposure unobserved |

只观测到 2026 Conference；日期位于 2025 是该届投稿审稿时间，不是另一个会议年份。快照文件名 `10000` 并非实际 N：10,090 个不同 submission number，范围 1–10,240，范围内缺 150 个号。主表只保留有 reviews 的 7,655 篇，剔除 2,435 篇无 review 的快照论文，也丢掉相应 author 覆盖。公开 submission 表 19,602 行、review 表 75,748 行、comment 表 167,342 行是不同时间/状态的抓取对象，不能把这些数直接当 final eligible conference population。

## 来源、时点与可公开复现性

| 输入 | 来源证据 | 本地文件修改时间（不是保证的抓取时点） | 复现与缺口 |
|---|---|---|---|
| iclr2026_reviews_10000.jsonl | notes 对应 11月28日快照；包含匿名 signature 与真实 profile 的映射 | 2025-11-28 | 原始获取脚本与合法公开获取路径不在项目；与官方所述泄露数据特征相符是 Inferred，不把身份映射当正常公开数据重新发布 |
| reviewer_info.csv / author_info.csv | 探索1 cells 13,15,17，OpenReview API2 get_profile | 2025-12-28 | 公开 profile 的部分字段可重抓，完整快照及当时权限不可保证；有 Not Found，明文登录配置留在原项目且不复制 |
| submissions_info.json | 爬取arxiv cells 0–13，已下载 OpenReview submission content + arXiv API 搜索 | 2025-12-30 | submission 抓取入口不完整；arXiv 匹配未验证、索引分段查询、有静默失败 |
| replies_official-review/comment.json | 加载数据 cells 9–17，OpenReview notes，官方 invitations/domain | 2025-12-31 | 原始 get_all_notes 完整代码未保存；review 文件只有 version=2 的当前 note，不是修订面板 |
| main_dataset.json | 加载数据合并、构造变量派生 | 2026-01-02 | 当前字段与后来的 notebook 内容存在版本漂移；不能仅靠 execution count 重建精确写入顺序 |
| profiles_cache.json | 工作指南描述 reviewer / first author demographics cache | 2025-12-28 | 原 gender 推断生成代码/验证样本未找到；不等于可靠人口学属性 |
| reviewer/author_coauthors.json | 爬取arxiv cells 17–22，get_profiles(with_publications=True) 后汇总 authorids | 2026-01-03 | 未保存 publication dates、titles、abstracts；不能复原事前网络，OpenReview 收录不覆盖所有历史论文 |
| nameprism_nat/eth.json | name-keyed 概率字典；查询 notebook 是空文件 | 2026-01-10/11 | 来源实现、置信度校准、真值验证不可复现；nat 标签不是实际国籍 |
| authors/reviewers/names.pkl | 探索1 中保存 ID 列表；names 生成入口不完整 | 2025-12-27 / 2026-01-08 | 没有执行 pickle；不需要这些文件完成此次审计 |

主数据年份/制度从 venue、signature 和官方规则交叉核对，而非只凭文件名。API2 为本地代码实际接口；未发现 v1/v2 跨年混用数据，但缺完整抓取入口与时间戳，无法审计所有 API schema 变化。现在重抓会取得事后状态，不能代替 2025 快照。

## 最可能的 pipeline

1. 外部获得 11月底 review/profile 快照（获取步骤缺失）。
2. `探索1.ipynb` cells 0–9：过滤无 reviews、explode reviews/authors、提取身份 lists；cells 13–19：OpenReview profile 抓取。
3. 获取公开 submission/review/comment notes（原采集脚本不完整）；`爬取arxiv.ipynb` cells 2–13：flatten submission 与 arXiv 查询；cells 17–22：publication coauthors 汇总。
4. `加载数据.ipynb` cells 24–28：review 行与 submission_number 左连接；cells 34–38：review ID 对当前 note；cells 41–49：author/reviewer profiles 映射；52–53：重命名。
5. `加载数据.ipynb` 55–64 与 `构造变量.ipynb` 1–28：分数差、字符长度、时间、zlib 和 VADER；后半为匹配探索，主要仅在 df_test。
6. `画图探索.ipynb` 3–5：每日/小时/截止日前时间图，内嵌 notebook，无单独导出文件。

这是 **traced** 的执行路径，不是成功端到端 reproduced。当前主表为 61 列，使用 `paper.*` 而已保存 source 多为 `content.*`；final content 的生成赋值不完整，主表却已有 final text、VADER 等。主表修改时间早于含有这些字段的后期 notebook 修改时间，证明版本来源不可仅由文件时间确定。确认的是已保存主表的数据血缘，未证明哪次交互 session 写出全部列。

## ID 与 joins

- `sub_number` 是 **单届** submission 编号；`sub_id/sub_forum` 是 submission/forum ID。跨年 join 应用 venue + ID，不能裸用 number。
- `reviewer_nickname` 实际是 review note ID，误导性名称；它不是匿名 reviewer signature，更不是真实 reviewer ID。
- `reviewer_id` 是 profile ID；匿名 `reviews.signature` 指向 reviewer-paper 签名。缺真实 ID 的 review 仍有 review ID。
- `authors_list` 为多作者 profile IDs，`first_author` 是 list 首位，不保证贡献排序或通讯作者。
- 外部 orcid/dblp/gscholar/semanticScholar 字段只是可链接指针；未完成外部姓名消歧或准确率核验。没有独立 institution ID，只有 domain/name。
- 本样本 reviewer 与 author profile IDs 交集 5,820；角色可重叠，不表示自己审自己的稿。跨年身份追踪在原则上可用 profile ID，但本地仅单年，无法验证改名、多账号和迁移。未观察到可信的姓名消歧流程。

| check                              |      n |   denominator |
|:-----------------------------------|-------:|--------------:|
| author_profile_id_join             | 169683 |        169683 |
| author_profile_slots               | 169683 |         29813 |
| author_profile_valid               | 169613 |        169683 |
| confidence_initial_mismatch        |      0 |         29813 |
| duplicate_paper_reviewer           |      1 |         29813 |
| duplicate_review_id                |      0 |         29813 |
| final_equals_snapshot_content      |  29813 |         29813 |
| initial_equals_current_raw_content |  29766 |         29813 |
| rating_initial_mismatch            |      0 |         29813 |
| raw_review_join                    |  29813 |         29813 |
| review_join                        |  29766 |         29813 |
| reviewer_profile_id_join           |  27470 |         29813 |
| reviewer_profile_valid             |  27464 |         29813 |
| submission_join                    |  29766 |         29813 |
| time_ms_equals_shanghai_local      |  29766 |         29813 |
| time_ms_equals_utc                 |      0 |         29813 |

分母解释：review/提交连接均 29,813 行；author join 按重复于 review 行的 author slots 169,683，**不是**唯一作者覆盖率。reviewer 可识别行 27,470（92.14%），2,343 行缺失；有效 profile 为 27,464。真实学术身份准确率没有独立验证，不能把 ID coverage 写成 linkage accuracy。review ID 无重复，paper-real-reviewer 有 1 个重复组合；同论文回归去除这个组合的后续记录，保留第一个。只用 ID equality，不外部搜索或公开个人名单。

## 已有结果审计

| 结果 | 数据/样本 | source与实际回答 | 数值/状态 | 可复现性与最大风险 |
|---|---|---|---|---|
| reviewer history 缺失 | profile CSV，13,561 条 | 加载数据 cell4 | 内嵌 output 4 行空，0.03% | 本轮重算有效 content/history=13,557；reproduced aggregate，profile 是事后快照 |
| 机构历史重叠 | main 前3,000行 | 构造变量 check_history_conflict cell48 | 内嵌 108 positive / 3,000 | traced only；缺日期默认0/2025、未知当False，非 friendship/真实 COI |
| 重叠年限 | 同前3,000行 | calculate_shared_history_years cell50 | mean .137，max22 | traced only；2026 end默认，重复区间跨作者累加，可能重复计算 |
| reviewer current role | main df_test | extract_current_positions cell57 | 内嵌 coverage .8249086 | traced only；以2026判断现职，不是assignment日前声誉 |
| arXiv 搜索 | submission 表 | 爬取arxiv cell12 | 内嵌 4,397 hits | traced only；仅首结果、标题核验注释掉、不清楚每段运行历史 |
| 每日/小时/DDL图 | main 时间 | 画图探索 cells3–5 | 三张内嵌图，无 effect size | traced only；DDL硬编码2025-11-01 23:59:59、无AoE；不重新宣称原图复现 |
| gender heatmaps | 想法251225.docx 内嵌探索截图 | notes中的描述 | 无独立表/生成回归代码 | traced only；没有可核验数值样本、模型或SE |
| 回归/DiD/事件研究/embedding | 目录全盘 | 未找到执行脚本或表/log | 未实现 | notes中的公式是设想；不能宣称随机assignment或因果结果 |

本轮新增四个明确标为 descriptive 的 paper FE 诊断，详见 EMPIRICAL_FACTS；未跑批量 specifications。没有发现已保存 accept/reject 主分析、AC recommendation、author citations/h-index 或 prestige 指标。

## 可复现边界与后续入口

本轮 **reproduced**：全部聚合诊断、ID joins、时间解释校验与字段 missingness。原始网络抓取和完整 pipeline **traced only / incomplete**。原文件 fingerprint 在运行前后验证，见 VALIDATION。原项目不改、不移动、不删除；只新增本目录交付物。
