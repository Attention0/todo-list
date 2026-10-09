# Mover / place-effect 文献识别架构地图

审计日期 2026-10-07。目的不是综述显著结果，而是区分：**测量前提 → 识别假设 → 能证伪的预测 → 仍不能排除的解释**。三类设计不能混用：重复结果的 person/place FE；儿童 age-at-move 暴露设计；有状态依赖/风险退出的婚育转移。

## 1. 来源清单与阅读层级

系统清点 `G:\桌面\科研\文章-生育地理`：12 篇 PDF 加 `笔记.docx`。对全部 PDF 做文本检索/相关识别章节阅读；对直接 benchmark 29 页正文与内嵌附录完整核验。其他论文按其与本任务的识别关系重点阅读，**不宣称所有独立 online appendices 都已取得或重估**。笔记只有概念提要，不作为论文证据。

页码约定：除注明“印刷”外，Lxx 为本地 PDF 页码（封面算一页）；Wxx 为网页/外部 PDF。文件名中的期刊/年份不是版本证明。

| ID | 本地文件识别名 / 作者 | 核验版本与阅读重点 | 证据边界 |
|---|---|---|---|
| L01 | `AEJEP-2025-Chyn, Eric, and Na'ama Shenhav...pdf` | Chyn & Shenhav，AEJ:EP 17(4), 260–291；33页；pp.5–9、26–28，Eq.1/5、§II/VI | 本地是正式主文；引用的独立 supplemental tables A10–A13 由主文说明核对，未另声称直接读取附件表值 |
| L02 | `AEJPOL-2026-Geographic Variation in Mental Health Treatment Utilization.pdf` | Hui Ding；本地48页为2025-03-30稿，pp.10、15–17及附表；[正式2026发表](https://www.aeaweb.org/articles?id=10.1257/pol.20230402)为18(1):35–68 | 识别细节引用本地稿，不把本地页码称最终期刊页码 |
| L03 | `AER-2022-Does Context Outweigh Individual Characteristics...pdf` | Cantoni & Pons；本地55页为2021-09稿；pp.12–20，§3–4、A.6说明 | AER 2022论文的本地前版，不是附录已完整归档证明；MATE 条件按本地稿 |
| L04 | `AER-2025-The Role of People versus Places in Individual Carbon Emissions.pdf` | Eva Lyubich；AER115(5):1439–1484；46页；pp.11–12、22–25、结果异质性与时间稳定性 | 正式主文；leave-out connected set 与修正直接可核 |
| L05 | `JHE-2022-Malleability of Alcohol Consumption.pdf` | Hinnosaar & Liu；JHE85:102648；13页扫描版；视觉核 pp.3–5 的数据、式1、CPS动机、假设 | 扫描件无文字层；另阅读 [AEA作者会议稿](https://www.aeaweb.org/conference/2022/preliminary/paper/ikybTGet) W03 的相关方法/附录，不混淆稿件与发表版表号 |
| L06 | `JHE-2025-Regional Variation in Mental Healthcare Utilization and Suicide.pdf` | Saxby, Buchmueller, de New & Petrie；JHE102:103029；26页；§2.6、Fig.2/3、Appendix A1–A3说明 | 直接核到 external HILDA 动机 + origin FE 检验，不把对称分布当作无选择证明 |
| L07 | `Labour-2026-EGeographic variation in fertility- evidence from mover design.pdf` | Wu & Zhu；Labour100:102895；29页；正文及全部内嵌附录 | 本轮最深审计，见独立文件；replication package 定位未执行 |
| L08 | `QJE-2023-Children’s Indirect Exposure to the U.S. Justice System.pdf` | Finlay, Mueller-Smith & Street；QJE138(4):2181起；45页；§VIII.B pp.28–34，Table I/II | 以出生地×种族和搬家年龄为核心，不能误归为重复年度个体FE event study |
| L09 | `QJE-2025-What Drives Risky Prescription Opioid Use.pdf` | Finkelstein, Gentzkow & Li；QJE140(4):3133起；59页含封面；§III–V，尤其pp.21–24 | 重点是动态潜在结果/非迁移者趋势和 cohort 权重；模型机制不用于本轮实证 |
| L10 | `Restat-2025-Partial Outsourcing of Public Programs Evidence on Determinants of Choice in Medicare.pdf` | Cabral, Carey & Son；本地49页为2025-01-14稿；pp.7–10、Eq.1/2、n.7/9 | 用本地稿版本，不据文件名臆造卷期；匹配与双向聚类直接可核 |
| L11 | `The RAND J of Economics - 2026 - Beheshti - What Causes Geographic Variation in Drug Prescribing Evidence from Physician.pdf` | Beheshti & Neller；26页；pp.2–3、Fig.1/2；[DOI](https://doi.org/10.1111/1756-2171.70069) | local title中的双空格不影响定位；用文章本身的 origin×event FE、专业组LOO，不推定发布日期排版无误 |
| L12 | `WP-2026-Geographic Variation in Healthcare Utilization The Role of Physicians.pdf` | Badinski, Finkelstein, Gentzkow & Hull；105页，2026-05稿；§3/4，pp.28–29，connected set | 作为工作稿引用，不升级为已发表Top5；[NBER项目页](https://www.nber.org/papers/w31749) |

### 补充检索（2026-10-07，优先作者/期刊原文）

- **W01 FGW (2016)**，*Sources of Geographic Variation in Health Care: Evidence from Patient Migration*，QJE131(4):1681–1726。[作者正式全文](https://web.stanford.edu/~gentzkow/research/movers.pdf)。重点§II/III、pp.1693、1698–1700、1712–13及推断脚注；实际有小而显著的 pretrend，不能概括为“顶刊都要求不显著”。
- **W02 Chetty & Hendren (2018), Part I**，QJE133(3):1107–1162。[作者正式PDF](https://hendren.scholars.harvard.edu/sites/g/files/omnuum9171/files/hendren/files/movers_paper1.pdf)。重点§V的兄弟姐妹、位移冲击、own-cohort/gender/quantile竞争预测；不是成年人的年度重复Y设计。作者网页卷号有笔误，采用PDF首页133。
- **W04 Chiovelli, Michalopoulos, Papaioannou & Sequeira (2026)**，*Civil War–Induced Displacement and Human Capital*，QJE141(2):1211–1268。[期刊开放全文](https://doi.org/10.1093/qje/qjag009)。新近检索增量：强制迁移仍需分开 spatial sorting、地方暴露及 uprootedness；利用家庭内和战时变化验证；其重建对象是存活人口，不能借该论文抹去我们的 survivor 边界。
- **M01 Kline, Saggio & Sølvsten (2020)**，Econometrica，*Leave-Out Estimation of Variance Components*，[作者全文](https://eml.berkeley.edu/~pkline/papers/KSS2020.pdf)。方法补充：估计FE的方差需扣除噪声；应用先例以直接读到的 L04 为主。
- **M02 Rambachan & Roth (2023)**，REStud90(5):2555–2591，*A More Credible Approach to Parallel Trends*，[作者全文](https://www.jonathandroth.com/assets/files/HonestParallelTrends_Main.pdf)。以明确的偏离限制做敏感性，不把 pre-test 非拒绝当识别证明；未在CMDS实施。
- **M03 Goldsmith-Pinkham, Hull & Kolesár (2024)**，AER114(12):4015–4051，[期刊](https://doi.org/10.1257/aer.20221116)。多重处理与异质性可能带来 contamination；提醒报告实际 estimand/权重，不是声称任何 mover TWFE 必然错。
- **M04 Borusyak, Hull & Jaravel (2025)**，Econometrics Journal28(1):83–108，[原文](https://doi.org/10.1093/ectj/utae003)。公式式 IV 必须说明外生 shocks 的赋值设计；“别人的平均数”或 sample splitting 本身不是外生性来源。

未把搜索命中数当质量：陆军婚姻迁移研究等仅列为后续可能线索，没有把未深读的材料编成已验证识别表。最新工作稿 L12 与新发表 W04 提供的是新的识别约束，非为了凑“2026文献”。

## 2. 共同识别架构表

“未核”表示本轮没有足够直接证据，不等于原文没有。“无随机赋值”不是否定论文；最后一列才是尚存替代解释。L01–L12 来源/版本/页码见上；W01/W02 核心架构列入同表。

| Paper | Outcome | Move definition | Treatment/place measure | Main specification | Individual FE? | Event study? | Pre-trend? | Destination-choice selection test? | Reverse causality test? | Exogenous move/shock? | Placebo / overidentification? | Multiple moves? | Return/survivor selection? | Exposure duration? | Inference/clustering | Main remaining threat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L07 Wu–Zhu Labour2026 | annual birth；孩次分量、婚姻进入辅项 | PSID跨州，首次为事件 | 独立NCHS race-specific州出生率差 | Δ×r + person/year/age/event FE；另AKM | 是 | −3…+3 | 两个独立leads、90%CI | 迁前balance、主/次动机、同源IV | 意愿子样本、婚姻进入、特征PCA | 灾害州子样本，不是随机安置 | PCA结果；婚姻进入；非own-v-other | 基线含，另全剔除 | panel能跟随；balanced非校正 | 年度动态/累积 | household；另state | 同步家庭计划、IV排除限制；AKM噪声 |
| W01 FGW QJE2016 | 医疗利用 | HRR单次，claims验证真实移动 | HRR平均利用差/area FE | patient+place FE；gap×r | 是 | 是 | 小显著pretrend，窄窗核验 | 方向/对称、健康与生活事件辅助资料 | 急性健康冲击的尖峰/持久性逻辑 | 非随机赋值 | 加性/年龄组检验 | 单次主样本，含多次敏感性 | 死亡/HMO进出敏感性 | 动态稳定性 | patient bootstrap | 同期未观测健康冲击仍可选目的地 |
| W02 Chetty–Hendren QJE2018 I | 成年收入、婚姻、teen birth等 | 家庭跨CZ/county；儿童年龄 | permanent residents相应群体预测差 | move age×quality；家庭内比较 | 家庭FE验证；非person-year FE | age-at-move曲线，非同一成年Y前后 | 不是常规成人Y leads | 兄弟姐妹、时变家庭、displacement | 家庭变化/不同年龄验证 | 大规模外迁冲击+预测 | own cohort/gender/quantile竞争预测 | 单次基线；多次暴露扩展 | 不是CMDS destination stock；本轮未核专门流失表 | 核心识别维度 | 本轮未核最终聚类细节 | 年龄相关选择、共同家庭时变输入 |
| L03 Cantoni–Pons AER2022（本地2021稿） | 注册、投票、党派 | 跨州/县，选举面板 | 地区平均投票差；place FE | voter/place FE、gap×event；MATE验证 | 是 | 按选举期 | 多期leads | 对称、人口组、MATE条件检验 | 排年龄转折组；承认同步冲击不可直接排除 | 未见随机赋值 | 加性对称与组特异、条件MATE | 具体spell扩展本轮未核 | 各迁移cohort全观察窗比较；数据库覆盖限制 | post-election动态 | voter与state两向 | 突然政治倾向变化与去向共同决定；carryover假设 |
| L01 Chyn–Shenhav AEJ:EP2025 | 出生体重/孕期，非出生概率 | 两次出生记录之间住址变化 | 母亲LOO地点平均出生体重差 | mother+place+birth-order/year FE | mother FE | 按相对出生序，不按迁移年 | 迁前出生结果 | 同源其他mothers IV、military附近 | maternal index、completed fertility预测 | military地区代理；非个人随机assign | index；nonmover donor；IV prebirth | 主剔重复，附录包含 | 至少多次出生选择；仅州内可跟随 | 实际move日期不明，暴露不能精定 | origin zip cluster；分解bootstrap/split sample | 生育本身/州外退出选择及同时母亲冲击 |
| L04 Lyubich AER2025 | 家庭碳排放 | census/ACS跨CBSA/tract记录 | place FE；地点排放均值差 | household/place FE；event样式；KSS variance | household FE | 两次观测为主的变化/时长比较 | 主样本不能做常规leads；另PSID检验 | 对称、异质性、生活事件稳定组 | 特征控制/稳定组、preference drift检查 | 无随机赋值 | 加性/异质性/时段检查 | 两观察间完整路径不知 | 稳定成人组成/联结选择仍在 | 距move时长 | bootstrap；KSS leave-out household match | 时变偏好/内生家庭组成；外部pretrend不等同自身样本 |
| L09 Finkelstein–Gentzkow–Li QJE2025 | risky opioid use | 单次跨州cohort（OD×moveyear） | 匹配nonmover的时变地区差 | cohort DID后gap回归；动态状态模型/GMM | 差分净化固定差；非单一TWFE | 是 | 动态pre/post moments | 条件对照；模型允许持久selection | 无anticipation；要求selection不在move时跳变 | 主mover非随机assign | 动态模型与未直接targeted图形对照 | 主单次 | 本轮未核专门退出校正 | 核心状态依赖/历史暴露 | Bayesian bootstrap 50 | 同步选择跳变、模型动态假设 |
| L08 Finlay等 QJE2023 | 间接司法暴露及成年结果 | 17岁前一次跨CZ | 目的county暴露指数 | birth-county×race、cohort等；年龄交互；sibling验证 | 非person-year；有sibling FE扩展 | 非常规event study | 成年结果无个人年度leads | 同出生地、家庭内、目的地traits | 家庭内/年龄验证，不排尽家庭冲击 | 未见外生assign | 控制/家庭内对照 | 限一次 | CJARS覆盖和存活/追踪边界 | 儿童move年龄 | birth CZ cluster | 年龄/目的地共同选择、覆盖差异 |
| L02 Ding AEJ:EP2026（本地2025稿） | 精神健康服务/药物使用 | HRR单次，claims destination份额增≥.75 | 迁前一年nonmover率差 | person/year/age FE、gap×r | 是 | −8…+7及尾bins | 有 | ACS离婚/丧偶/退休与Δ | 隐性需求未体现在利用的替代解释+ACS检验 | 非随机assign | 生活事件、Oster敏感性 | 单次 | 连续PartD条件/样本选择 | 年度dynamic | beneficiary cluster | 潜在需求和去向同步变化，连续保险选择 |
| L05 Hinnosaar–Liu JHE2022 | 家庭酒精购买 | 单次跨州；不知道确切move日 | nonmover州均值差 | household/time FE、gap×quarter | household FE | 是；主排move年 | 迁前三年变化对Δ | 外部CPS动机；稳定家庭特征 | 离婚/工作等共同冲击敏感性 | 非随机assign | 相似零售条件处理记录偏差 | 主单次 | balanced/持续观察敏感性 | 短期季度 | household；OD-pair替代 | 未观测偏好与去向，购买记录不是所有消费 |
| L06 Saxby等 JHE2025 | 精神服务/药物利用 | 单次跨PHN，行政地址更新 | nonmover地区利用差 | patient/place及quarter/event FE | 是 | 季度 | 是，日期滞后另设参考 | 对称；HILDA健康动机含origin FE | 健康动机与Δ的外部验证 | 非随机assign | 外部动机资料 | 主单次 | 本轮未核完整退出处理 | quarterly dynamics | individual cluster | 潜在健康需求/地址滞后；对称不证明无选择 |
| L10 Cabral–Carey–Son（本地2025稿） | Medicare Advantage选择 | 跨county面板 | county MA份额差 | person/year/age/event FE；另place FE | 是 | 是 | MA及药物利用健康proxy | 同源性别种族年龄等exact matched nonmovers | 迁前健康变化检验 | 非随机assign | 健康proxy | 描述中有多次者；主细则本轮未核 | 保险状态跟踪；专门return本轮未核 | 排move及next年估稳态 | individual；另origin/destination | 同时健康/保险偏好与去向选择 |
| L11 Beheshti–Neller RAND2026 | 医师处方支出 | 医师跨HRR | specialty-specific LOO均值差 | person FE + origin×relative-year FE | physician FE | 是 | 是 | 迁前处方rank预测Δ，明确组内来源比较 | 方向/事前行为；不能排同步偏好 | 非随机assign | 专业组/来源和病人地域检查 | 本轮未核完整路径处理 | 原地病人延续的附录检查；退出未核 | post动态 | physician cluster | 同步病人组合/偏好改变 |
| L12 Badinski等 2026-05 WP | 医疗接触数与每次利用 | 患者和医生跨HRR + 区内匹配变化 | patient/physician/place FE | 三类FE、匹配和迁移识别 | 两类主体FE | 两类mover图 | 两类leads | 方向对比、specialty内/健康调整 | 同期需求及患者医生匹配冲击讨论 | 非随机assign | 两类mover的识别限制交叉验证 | 有复杂多地执业处理；非简单一次居住计数 | claims样本及matching条件；退出未核 | 动态检查 | patient/doctor分别cluster；分解Bayesian bootstrap | 病情冲击同时导致匹配/迁移，三类FE不免疫 |

W04 为定向新文献补充而非套入重复Y事件研究：战争期间儿童迁移，以存活人口重建路径；同家庭及年龄暴露验证削弱 sorting，却仍需要区分搬迁损失和目的地效果。借鉴的是**外生触发不等于单一地点处理**，不是把战争/灾害移作我们的现成工具变量。

## 3. 文献真正要求的识别逻辑

| 设计组件 | 针对的内生性威胁 | 为什么有识别内容 | 通过后仍存在 / 失败意味着什么 | 对本项目等级 |
|---|---|---|---|---|
| 明确actual move与独立place指标 | 错事件、错来源、本人结果进入处理 | 构造的冲击才对应已定义暴露；独立donors排机械共变 | 外部率仍混人口构成；地址更新≠真迁移；测量失败则不估因果 | T0 |
| 固定效应或同人差分 | 固定个体偏好决定住哪 | 允许个体水平与目的地相关，识别来自变化 | 不吸收同步时变计划；初婚/首胎终止样本不能机械照抄 | T1；具体FE不是所有Y硬性要求 |
| 同源/同cohort动态比较 | origin shocks、不同来源构成 | 比较更相似的出发条件，去掉同源共同走势 | 同来源者也按计划选目的地；静态origin FE被person FE吸收 | T1 |
| 迁前动态与量级敏感性 | 渐进选择/预期改变 | 未来去向不应预测未经处理的结果变化 | 同步冲击无leads；低power非证据；成人完成结果无法有童年前成年收入leads | T1，依estimand实施 |
| 家庭事件/迁移动机/计划检验 | 结婚、怀孕、工作同时促迁与改Y | 可观测触发因素应与Δ不系统相关，且时间顺序透明 | 漏报、不完整意愿与不可见计划仍在；事后稳定组可有collider | T1 |
| Single move / 实际暴露重建 | 前后归错地，carryover | 更接近定义的原居住→目的地变化 | 剔重复会改变总体；一个城市不等于一个spell | T0测量 + T1诊断 |
| 流失/留存检查 | 生育影响返乡而影响被抽中 | 面板可观察退出时点并诊断；stock必须限制目标与敏感性 | 没有arrival/exit分母不能识别selection权重；通过意向检验也非实际留存 | T1 |
| Own-group与无关group竞争预测 | 一般性地区选择伪装特定环境 | 在同时控制相关预测后，差异性预测提供可证伪约束 | 共线/真实溢出/按事后组别选择使零假设失效 | T2 |
| 暴露长度、age-at-move、多次路径 | 静态selection假装累积地方效应 | 不同暴露长度给出额外受约束的模式 | 成人年龄、cohort、生育间隔、留存梯度可生成同样形状；不能强制线性同化 | T2验证；动态解释T1 |
| 冲击/IV + 排除限制 | 去向和时点共同选择 | 只有真实外生assign或可辩护shock隔离误差时才新增因果信息 | 灾害有直接效应；同源均值含共同冲击；strong first stage并不检验外生 | T2条件项，不强制找IV |
| AKM leave-out/方差修正 | 噪声扩大方差、伪sorting | 纠正有限样本噪声需额外连通与误差条件 | 不解决内生move；不能把小covariance当排除限制检验 | 若做因果分解则必要，否则后置 |
| 正确依赖结构与少簇推断 | 地区共同扰动、有效处理数虚增 | SE反映实际assignment/误差层级 | 不修复偏误；很多人但少省仍信息有限 | T1 |

## 4. 不同结果不能照抄的四个地方

1. **儿童暴露 ≠ 成年婚育 event study**。Chetty–Hendren 的关键是迁移年龄与长期预测的交互，验证是家庭内/组别预测；不应要求其画同一孩子幼年“成人收入前趋势”。我们有部分可回溯婚育日期，应利用，但必须避免按迁移时未婚/零胎筛选后制造结构性全零leads。
2. **出生体重 ≠ 生不生孩子**。Chyn–Shenhav 的 mother FE 比较已经出生的不同孩子，event time 是出生顺序。其 completed-fertility 检验针对出生样本选择，不能直接提供婚姻/首胎 hazard 的分母或孕期暴露。
3. **投票/医疗利用 ≠ 一次性初婚/首胎**。状态退出和carryover改变风险组。Cantoni–Pons 的 MATE 检查值得学习，但其无持久效应等条件不能机械转用。L09 的动态潜在结果说明为什么应写清楚路径和时间权重；本轮不要求估计其结构模型。
4. **AKM方差份额 ≠ event-study slope**。两者所需的加性、异质性、噪声条件不同；个体FE、external gap、connected set也分别解决不同问题。不能用“个人与地点 FE 不相关”一项替代所有识别诊断。

## 5. 哪些升级真正优先

对 CMDS 最有价值：合法风险人口/独立分母、实际与代理居住轨迹分开、家庭形成导致迁移的排序诊断、同来源组内有效动态比较、可量化的pretrend不确定性、目的地stock选择边界。其次才是相关群体环境的竞争预测、真正外生设计、噪声修正的AKM。

不优先：堆几十个窗口、无有效支持的education movers、以当期收入/婚姻“控制一切”、把工作动机叫外生、用没有returnees分母的IPW、直接复用别人的同源均值IV。顶刊的共同标准不是每篇都做同一套，而是**每项关键假设都有对应数据和可能推翻它的证据**。

## 6. 交付与来源完整性说明

本次发布为分析性 Markdown，不上传本地付费论文、提取全文、微观数据或PDF图片。完整 local inventory 的页数、SHA-256 与文件名已在本地核验；直接benchmark hash见独立审计。比较稿版本与未核附件明确留痕，未核条目不参与断言“原文缺少某防御”。工单要求的最少四组（FGW、Chetty–Hendren、Cantoni–Pons、Chyn–Shenhav）及本地其余相关论文均覆盖；近期补充检索与方法文献分开标注。

下一步执行任务、A/B/C可行性、样本成本和通过/失败解释统一见 [MOVER_CORE_CHECKLIST.md](MOVER_CORE_CHECKLIST.md)。本轮文献阅读不等于实证验证通过，也不修改旧样本定义或开启机制。
