# Data dictionary

核心数据单位为 reviewer-paper review（29,813行），不是完整 assignment matrix。所有 local 路径均相对 PROJECT_AUDIT 中项目根目录。Observed / Constructed / Inferred / Assumed / Not observable 五类证据在下文分别标记；不要把字段名称当含义证据。

## 表与单位

| 表 | 单位与键 | 覆盖/缺口 |
|---|---|---|
| data/iclr2026_reviews_10000.jsonl | paper；submission_number/submission_id，嵌套 authors 与 reviews | 10,090篇；7,655篇有review、29,813reviews；真实profile mapping仅限所获样本 |
| data/main_dataset.json | review；reviewer_nickname；sub_number+reviewer_id可能重复 | 29,813行，7,655篇，13,560个非空reviewer ID；not assignment panel |
| data/submissions_info.json | paper；submission_number/id/forum | 19,602条；title/abstract/keywords/venue/arXiv；不同状态/时点 |
| data/replies_official-review.json | 当前 official review note；id/forum | 75,748条唯一id，全部version=2；不包含完整edit历史 |
| data/replies_official-comment.json | comment；id/forum/replyto，角色signature | 167,342条、14,031个不同submission_number（含缺失状态需另核）；未合入main |
| data/reviewer_info.csv | profile；id | 13,561条，有效content 13,557 |
| data/author_info.csv | profile；id | 28,465条，有效content 28,452；作者slot join重复计数 |
| data/profiles_cache.json | profile-keyed缓存 | 19,236 keys，可含null；gender来源未验证 |
| data/reviewer_coauthors.json / author_coauthors.json | ego profile→coauthor IDs list | 无edge日期、publication文本；只能无日期snapshot网络 |
| data/nameprism_nat.json / nameprism_eth.json | name→分类概率dictionary | 各34,025 keys；不等于真实国籍/种族，无生成code或accuracy |
| authors/reviewers/names.pkl | ID/name lists | 审计不需要，未反序列化 |

## 主要变量语义

| 变量/组 | 语义与证据 | 时点/限制 |
|---|---|---|
| sub_number, sub_id, sub_forum | Observed paper keys | number不可跨年，47行没连上public submission |
| reviewer_nickname | Observed review note ID | 名称不是昵称；与current review id连29766行 |
| reviewer_id, reviewer_profile | Observed所获身份映射 | 2,343缺失；泄露来源风险，不发布行级映射 |
| authors_list, first_author | Observed snapshot作者profile IDs | 106 review行作者列表空；不自行填补身份 |
| paper.title/abstract/keywords/primary_area/venue | Observed 公开submission字段 | 47行缺失；paper.authorids严重缺失，不能替代snapshot作者映射 |
| rating_initial/confidence_initial, official_review_initial_content | Observed后期current note值 | 29,766可用；全部对应raw current content；字段不是历史initial edit |
| rating_final/confidence_final, official_review_final_content | Observed旧JSONL快照值 | 29,813可用；全部对应snapshot content；非最终decision时评语 |
| rating_diff, confidence_diff | Constructed snapshot minus later current | 不能称rebuttal effect或final minus initial chronology |
| official_review_initial_tcdate/tmdate | Observed naive北京时间字符串 | native cdate/mdate证实+8h；tcdate仅note创建，不代表阅读开始 |
| *_tcdate_ms, time_required_ms/time_left_ms | Constructed毫秒与固定窗口差 | 上海localize与native时间一致；47缺失日期的整数不算有效时间；硬编码UTC 10/10–10/31不是正式review deadline |
| official_review_initial_order | Constructed所观测样本内reviewer创建顺序 | 只看到部分任务；不能解释完整review workload/order |
| *_summary/strengths/weaknesses/questions_length | Constructed Python len(text) | 是字符数而非word count；final/current snapshots不可换成审稿质量 |
| official_review_initial_full_text_entropy_zlib | Constructed compressed byte ratio | 非严格Shannon entropy；短文本阈值30 bytes、长文本/模板影响 |
| official_review_initial_full_text_sentiment_vader | Constructed通用lexicon情感 | 缺review返回0会被误当中性；未验证学术批评语境 |
| reviewer_history / authors_list_history | Observed profile履历lists | 后期查询，自报、日期缺失、重叠职位；非冻结assignment日前资料 |
| reviewer_expertise / authors_list_expertise | Observed自报keyword lists | 24,657 review行reviewer非空；有start/end但快照时点晚，没有经验证pair similarity |
| reviewer_relations / authors_list_relations | Observed自报关系lists | 可以研究advisor等，但不保证完整或事前冻结；绝不自动叫friendship |
| reviewer_gender / first_author_gender / authors_list_gender | Constructed/inferred来源不明的标签 | 名字推断代码零散，无accuracy/uncertainty基准；未知保持未知 |
| arxiv_entry_id/published/updated/authors | Constructed API首命中及其元数据 | 未校验title，missing=未查/失败/没命中混合；不等于no preprint |
| institution_overlap_snapshot（本轮） | Constructed双方domain sets交集 | start年份≤2025；双方每位作者有可用dated-start domain才定义0；不是同一时期同机构，缺失为NaN |
| coauthor_overlap_undated（本轮） | Constructed双向任一名单含对方 | 两方查询名单存在才定义0；空名单仍可能漏收，含本次submission共同作者，不能称prior coauthor |

## Missingness与coverage

field_coverage采用顶层 null/空字符串/空list/空dict 检查；数字0算观测到，list=[null]仍算非空，所以多作者nested coverage必须另核；Unknown人口学标签不能因为非空就当known。profile IDs成功join不等于真实身份消歧成功。

| role     |   rows |   unique_ids |   valid_content |   history |   expertise |   relations |   orcid |   dblp |   gscholar |   semanticScholar |
|:---------|-------:|-------------:|----------------:|----------:|------------:|------------:|--------:|-------:|-----------:|------------------:|
| reviewer |  13561 |        13561 |           13557 |     13557 |       12105 |       11974 |    5745 |   9560 |      11189 |              3136 |
| author   |  28465 |        28465 |           28452 |     28431 |       23388 |       22359 |   11188 |  13147 |      17159 |              4037 |

| metric                                 |     n |
|:---------------------------------------|------:|
| raw_submission_number_min              |     1 |
| raw_submission_number_max              | 10240 |
| raw_missing_numbers_in_range           |   150 |
| profiles_cache.json_records            | 19236 |
| profiles_cache.json_gender_nonempty    | 16976 |
| profiles_cache.json_race_nonempty      |     0 |
| profiles_cache.json_country_nonempty   | 19129 |
| profiles_cache.json_expertise_nonempty | 16710 |
| nameprism_nat.json_records             | 34025 |
| nameprism_eth.json_records             | 34025 |

主表所有字段逐项的非空率、缺失数与类型如下（分母统一29,813）：

| variable                                          |   rows |   present |   nonempty |   missing_or_empty | types                              |
|:--------------------------------------------------|-------:|----------:|-----------:|-------------------:|:-----------------------------------|
| arxiv_authors                                     |  29813 |     29813 |      13409 |              16404 | {"NoneType": 16404, "str": 13409}  |
| arxiv_entry_id                                    |  29813 |     29813 |      13409 |              16404 | {"NoneType": 16404, "str": 13409}  |
| arxiv_published                                   |  29813 |     29813 |      13409 |              16404 | {"NoneType": 16404, "str": 13409}  |
| arxiv_updated                                     |  29813 |     29813 |      13409 |              16404 | {"NoneType": 16404, "str": 13409}  |
| authors_list                                      |  29813 |     29813 |      29707 |                106 | {"list": 29813}                    |
| authors_list_expertise                            |  29813 |     29813 |      29707 |                106 | {"list": 29813}                    |
| authors_list_gender                               |  29813 |     29813 |      29707 |                106 | {"list": 29813}                    |
| authors_list_history                              |  29813 |     29813 |      29707 |                106 | {"list": 29813}                    |
| authors_list_homepage                             |  29813 |     29813 |      29707 |                106 | {"list": 29813}                    |
| authors_list_relations                            |  29813 |     29813 |      29707 |                106 | {"list": 29813}                    |
| confidence_diff                                   |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| confidence_final                                  |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| confidence_initial                                |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| first_author                                      |  29813 |     29813 |      29707 |                106 | {"str": 29707, "NoneType": 106}    |
| first_author_gender                               |  29813 |     29813 |      26494 |               3319 | {"str": 26506, "NoneType": 3307}   |
| official_review_final_content                     |  29813 |     29813 |      29813 |                  0 | {"dict": 29813}                    |
| official_review_final_questions_length            |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| official_review_final_strengths_length            |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| official_review_final_summary_length              |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| official_review_final_weaknesses_length           |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| official_review_initial_content                   |  29813 |     29813 |      29766 |                 47 | {"dict": 29766, "NoneType": 47}    |
| official_review_initial_full_text                 |  29813 |     29813 |      29766 |                 47 | {"str": 29813}                     |
| official_review_initial_full_text_entropy_zlib    |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| official_review_initial_full_text_sentiment_vader |  29813 |     29813 |      29813 |                  0 | {"float": 29813}                   |
| official_review_initial_order                     |  29813 |     29813 |      27470 |               2343 | {"float": 27470, "NoneType": 2343} |
| official_review_initial_questions_length          |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| official_review_initial_strengths_length          |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| official_review_initial_summary_length            |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| official_review_initial_tcdate                    |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| official_review_initial_tcdate_ms                 |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| official_review_initial_time_left_ms              |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| official_review_initial_time_required_ms          |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| official_review_initial_tmdate                    |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| official_review_initial_weaknesses_length         |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| paper.TLDR                                        |  29813 |     29813 |      14471 |              15342 | {"NoneType": 15342, "str": 14471}  |
| paper.abstract                                    |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| paper.authorids                                   |  29813 |     29813 |       6312 |              23501 | {"NoneType": 23501, "list": 6312}  |
| paper.keywords                                    |  29813 |     29813 |      29766 |                 47 | {"list": 29766, "NoneType": 47}    |
| paper.primary_area                                |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| paper.supplementary_material                      |  29813 |     29813 |      12320 |              17493 | {"NoneType": 17493, "str": 12320}  |
| paper.title                                       |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| paper.venue                                       |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| rating_diff                                       |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| rating_final                                      |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| rating_initial                                    |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| reviewer_expertise                                |  29813 |     29813 |      24657 |               5156 | {"list": 27283, "NoneType": 2530}  |
| reviewer_gender                                   |  29813 |     29813 |      24241 |               5572 | {"str": 24242, "NoneType": 5571}   |
| reviewer_history                                  |  29813 |     29813 |      27464 |               2349 | {"list": 27464, "NoneType": 2349}  |
| reviewer_homepage                                 |  29813 |     29813 |      20123 |               9690 | {"str": 20124, "NoneType": 9689}   |
| reviewer_id                                       |  29813 |     29813 |      27470 |               2343 | {"str": 27470, "NoneType": 2343}   |
| reviewer_nickname                                 |  29813 |     29813 |      29813 |                  0 | {"str": 29813}                     |
| reviewer_number                                   |  29813 |     29813 |      29766 |                 47 | {"float": 29766, "NoneType": 47}   |
| reviewer_profile                                  |  29813 |     29813 |      27470 |               2343 | {"dict": 27470, "NoneType": 2343}  |
| reviewer_relations                                |  29813 |     29813 |      24557 |               5256 | {"list": 27464, "NoneType": 2349}  |
| reviews                                           |  29813 |     29813 |      29813 |                  0 | {"dict": 29813}                    |
| sub_cdate                                         |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| sub_forum                                         |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| sub_id                                            |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| sub_mdate                                         |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |
| sub_number                                        |  29813 |     29813 |      29813 |                  0 | {"int": 29813}                     |
| sub_odate                                         |  29813 |     29813 |      29766 |                 47 | {"str": 29766, "NoneType": 47}     |

## 量表、时间与outcomes

2026保存current rating观测支持集为{0,2,4,6,8,10}，confidence为{1,2,3,4,5}，47行缺失；两个快照的分布分别保留在四个 *_distribution.csv。这里只确认Observed支持集；尝试官方review invitation endpoint收到403，正式问卷锚点文案/0是否有特殊含义未确认，不用均匀0–10整数假设替代。不存在跨年score harmonization任务或已保存单盲年。

[timezone_checks.csv](tables/timezone_checks.csv)用75,748条原note的整数cdate/mdate逐条比较：tcdate/tmdate字符串按Asia/Shanghai解释与整数相符（秒截断误差<1000ms），按UTC解释无一相符。日期范围表已转UTC，不是本地显示时间。arXiv元数据自带UTC offset。Deadline必须另用正式AoE日历，不能沿用代码窗口。

初评/final/revision需先补历史edits及冻结时间。可靠度相对较高的是current-note rating/confidence、同快照review字符长度与所观测review数；confidence是审稿时自报结果，不是ex ante expertise。discussion有raw comments但未可靠构造成reviewer activity；创建时间不是response speed/阅读耗时；sentiment与compression需验证才可当文本机制。

Not observable：真实author observability、reviewer bids/affinity/完整候选池/完整负assignment、容量约束与人工调整log、独立institution prestige、citations/h-index、真实accept/reject/metareview的完整链接、跨年制度面板和完整review revision history。不能从rating阈值制造accept outcome。
