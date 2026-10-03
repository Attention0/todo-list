# Matching and assignment audit

## Assignment能确认到哪一步

官方[Reviewer Guide](https://iclr.cc/Conferences/2026/ReviewerGuide)要求9月28日–10月4日bidding；同一页面说明reciprocal reviewer加入受到筛选。官方[AC Guide](https://iclr.cc/Conferences/2026/AreaChairGuide)说明基于research profiles分配、AC可推荐/调整reviewers并招募emergency reviewers，目标至少3份有质量评审。页面有陈旧日期，应仅把这些机制陈述作为公开证据，不能据此复原精确2026算法。

本地没有bids、affinity edges、完整eligible reviewer pool、candidate matrix、capacity参数、matching随机seed/solver、阈值或manual adjustment logs。只能看到已发生review及部分身份，未交review的assignment看不到；观察到的reviewer load只是**截断样本内**负担。TPMS未找到证据；不能把OpenReview平台可用的算法称为ICLR实际选择。

[OpenReview官方matching文档](https://docs.openreview.net/how-to-guides/paper-matching-and-assignment/how-to-do-automatic-assignments/how-to-setup-paper-matching-by-calculating-affinity-scores-and-conflicts)说明平台可基于profile/publication计算affinity和conflicts，COI可配置回溯年限、domain/relations/publications；这是通用平台能力，不确认2026实际COI参数、模型或阈值。

`想法251225.docx`里的“完全随机分配”是未经佐证的Assumed。bids、专业匹配、COI及AC干预均能产生selection。paper FE只吸收论文共同特征，不能消除不同reviewer的专业知识、宽严程度或被选择的原因。

## 三类matching与人口学

| 指标 | 本地现状 | 事前时点与解释 |
|---|---|---|
| Topic/expertise embeddings | 未保存向量、历史publication文本/日期、model或相似度结果 | 不伪造embedding；需要assignment日前出版物与当时submission文本 |
| self-reported expertise关键词 | reviewer_expertise有24,657行非空 | 后期profile快照，有start/end但不证明当时填报；可构造lexical overlap，不能冒称官方affinity |
| bids / affinity / self-expertise at bid time | Not observable | 缺真正ex ante matching条件；confidence不能填补 |
| 共同署名 | 两份ego coauthor lists，可做snapshot overlap | 缺edge日期；可能包含2026本次投稿/事后publication；本轮只叫undated overlap |
| shortest network distance / shared prior coauthors | 可以在部分OpenReview graph构造 | 截断网络、时间泄漏和收录缺失；不是全学术合作图 |
| 同机构 / 历史机构 | history domain/start/end已保存 | 本轮dated-start domain overlap允许不同时期；原同时间算法缺日期填0且把missing当False，需改成unknown |
| advisor/genealogy | self-report relations有字段 | coverage不完整；需关系类型与有效日期，未构造可靠全网络 |
| country | profile history或cache有字段 | 是机构所在地候选，非姓名推断的国籍；时点、迁移、多职位需核验 |
| attended same lab/conference | 无可靠专门表 | 不强行推断 |
| author citations/h-index / past top venue/ICLR / prestige | 没有构造或外部dated指标 | 可用ID链接外部来源，但需要历史截止日，不能使用2026后的累积值 |
| reviewer seniority/current role | df_test notebook探索 | 2026现职快照不能等同2025assignment时seniority；非reputation |
| gender / NamePrism属性 | 主表/缓存有标签，NamePrism query notebook为空 | 来源准确率与uncertainty无验证；不补推，不跑人口学因果回归 |

## 本轮新增的有限诊断

`code/audit.py::insts`仅用非空institution domain、可解析start且≤2025的经历；任一作者缺有效履历时把整个pair记unknown。双方有资料、domains不交才记0；domain交集为1。不要求同期、未处理学校/子域实体合并，不称same current institution或friendship。domain集合是事后profile快照，不能事前因果使用。

`coauthor_overlap_undated`检测reviewer list含任一作者或author list含reviewer；要求双方list查询记录存在。空list并不证明没有真实共同署名；OpenReview可能未收录。没有publication date，不称prior familiarity。

两个X分别对rating_initial与confidence_initial做paper within-demeaning、去重paper-reviewer、只保留X在paper内变化的complete-case论文；paper-cluster SE，无其他controls、没有reviewer FE。四个模型仅描述关联；跨paper reviewer相关性意味着以后需考虑two-way clustering。详见 [within_paper_associations.csv](tables/within_paper_associations.csv) 和 EMPIRICAL_FACTS。

## 四级识别判断

1. 自然matching correlation：可报告，必须说明样本获取与profile coverage的selection。
2. Conditional matching：paper FE诊断可做，加入reviewer FE和dated expertise后更有信息，但仍非随机。
3. Algorithm/capacity/threshold quasi-random：目前没有候选集/阈值/容量log，无证据。
4. Causal：本轮没有能支持该解释的assignment设计。

下一轮应先拿到合法的dated publication/relations资料、冻结版本及公开assignment文档；若能获得授权bids/affinity/完整候选池，才比较assigned和eligible未分配pairs。不得把没有review的pair自动当eligible control。
