# 婚 + 育：最低可辩护 mover design 与下一轮执行清单

2026-10-07；研究设计路线图，**没有执行新因果回归或机制**。依据本轮 [文献矩阵](MOVER_LITERATURE_IDENTIFICATION_MAP.md)、[Labour 审计](LABOUR_E_IDENTIFICATION_AUDIT.md)，而非把所有 robustness 都升格为必做。

## 0. 数据证据、版本和不能跨越的边界

本轮最新任务来源为 main `1874d375231ed6a6a040bc8df0d336b5fc48474d` 的 `fertility/WORK.md` 和 `MOVER_BENCHMARK_AUDIT_WORKORDER.md`。前轮实证核验文件在 PR #22，当前 main 尚无这两个文件；本轮**通过明确的依赖链接使用，不重新包装为本轮重跑结果**：

- [DATA_RECONCILIATION.md（固定 commit）](https://github.com/Attention0/todo-list/blob/939bebf0f882faa578cba55afe32e6f7e3ac0c88/fertility/DATA_RECONCILIATION.md)
- [IDENTIFICATION_GAP_AUDIT.md（固定 commit）](https://github.com/Attention0/todo-list/blob/939bebf0f882faa578cba55afe32e6f7e3ac0c88/fertility/IDENTIFICATION_GAP_AUDIT.md)
- [聚合数据证据](https://github.com/Attention0/todo-list/blob/939bebf0f882faa578cba55afe32e6f7e3ac0c88/fertility/audit/reconciliation_evidence.json)

**Observed fact（前轮已核验、本轮读取）**：female base N=507,225（2012–18），已发布 broad fertility master M=362,245（2012–17）。2012–16 base 中 63,336 位调查时未婚女性全部不在 M；M 的 10,325 位未婚者全部来自 2017。不能把 M 称作完整婚姻或首胎风险人口。

**Observed fact**：实际上一居住地在 harmonized base 中没有被验证；168,536 人是推断来源 B，193,709 人为户籍来源 C。首离户籍年月不等于当前到达年月。“一次迁移”“一个迁入城市”不是同一变量。当前地点不是完整居住轨迹。

**Observed fact**：2017 问卷有 Q412–418，但现有 DTA 缺相应字段。2017 的 80,163 位 M 女性出生史来自 roster，不是已验证 lifetime CEB；roster 不只同住子女，但漏掉已独立分户子女。2017 没有可用初婚日期。2016/18 日期题含同居措辞；2018 当前提取缺来源地。

**Reconstruction**：现有外部 `delta_birth_pre3` 是目的省减户籍省、迁前 3 年平均 CBR（每千总人口）；匹配 323,949，缺 38,296；其中 zero=162,441、positive=64,440、negative=97,068。独立数据避免 own-observation 泄漏，**不等于**有效婚姻环境或细地理因果处理。

**Assumption**：把迁前位置设为户籍、迁后所有年份设为现城市，或者把 duration 当连续暴露，都要未观测轨迹假设。**Unknown**：退出目的地者的婚育与真实留存概率。CMDS 当前目的地 stock 不能识别所有到达者的平均因果效应。

## 1. 最低 8 个要素与停止条件

| 要素 | 等级 | 必须回答的问题 / 通过标准 |
|---|---|---|
| 1. 可解释的迁移事件与处理 | Tier 0 | date、actual/proxy origin、destination、暴露期、Δ 来源及单位均有证据；未知不能填成观测 |
| 2. 两个独立 outcome population 与动态风险集 | Tier 0 | 婚姻不按生育模块筛选；生育不按未来会生孩子筛选；未婚、零胎、缺失可区分 |
| 3. 可比性及目的地选择 | Tier 1 | 迁前状态预测 Δ；within-origin×cohort 有非退化支持；同源组动态控制非冗余 |
| 4. 家庭计划/怀孕导致迁移 | Tier 1 | 月份排序/近迁移事件、动机缺失、迁前状态比较；说明未观测计划剩余威胁 |
| 5. 有信息量的迁前动态 | Tier 1 | 分母、leads 联合检验、slope、效应尺度 CI/检测力与趋势敏感性；不以不显著为通过 |
| 6. 轨迹、重复迁移和存量留存 | Tier 1 | 一次/多次代理与宽样本对照；说明退出者未观测及可识别目标人群，不能虚构 IPW |
| 7. 动态 estimand、对照与异质性 | Tier 1 | 区分 any birth、转移 hazard、固定基线组累计事件；不把终身风险/完成生育偷换成短期系数 |
| 8. 依赖结构与有效信息量 | Tier 1 | 实际 origin/destination 支持和簇数、跨省共同冲击、few-cluster 敏感性；报告估计量真实权重 |

其中任何 Tier 0 的关键内容失败：可交付测量/选择描述，不得标“干净 mover causal effect”。代理来源设计可以单独报告**条件于明确代理假设的证据**，不能改名字就升格为 actual-residence effect。所有 Tier 1 诊断通过也不等于证明无未观测选择。

AKM 不在前 8 个必跑项：若未来声称地方方差份额，则 connectedness、leave-out support 和噪声修正成为该结果的 Tier 0/1。它不是婚育主效果的前置必交付。

## 2. 婚姻与生育：分别建人口、分别定义时间

### 2.1 共用时间骨架，但不共用筛选漏斗

从 female base 开始独立建 `marriage_universe` 和 `fertility_universe`，保存每个 wave 的路由、缺失类型、观测/重建/假设标签与纳入原因。年龄在事件年计算，不能只按调查年龄。生育预注册 15–45 岁 person-years（与前轮代码一致）；可另比较 15–44，但不能静默切换。婚姻年龄窗口单独预注册，极早日期先核原题，不能机械用法定年龄把真实早婚删除。

主年度窗口先 −3…+3，r=t−current_arrive_year；−1 为参考。窗口不是“平衡样本准入条件”。调查年若仅有部分暴露，主 annual 分析止于最后完整年；有可靠访谈月才按 person-month 暴露处理，不将未来月份补零。月份充分时，将迁移月标记为部分暴露，另用距到达的完整月份/年检验（P3/P4）。

`first_leave_year` 只作轨迹一致性变量。未知居住年份保留 unknown，不编造 annual place。同年婚育/迁移缺月份则 tie/interval-censored，不能强排先后。2012 缺到达月；2016/18 初婚/同居区别须单列；2017 不补造婚姻史。

### 2.2 婚：初婚 hazard 是 primary，累计进入概率是必要伴随量

`R^M_it = 1{初婚尚未发生于 t 年开始前，且该时点的历史可确定}`；`Y^M_it = 1{初婚在 t 发生}`。事件年纳入，之后退出风险集。经问卷代码确认的 never-married 提供截至访谈的未发生暴露；**婚期缺失的曾婚/不明者不能当 never-married**。2012–16 需从 base 恢复前述被漏掉的未婚群体；2018 仅有婚史不足以进入当前 OD 分析。

主初婚不等于 current married stock。离婚、丧偶、再婚没有完整日期，不重建假的 marriage spells。2016/18 若无法拆分法定婚姻和同居，报告 union-entry 并另列严格初婚可比波次，不混合后仍叫同一结果。

重要陷阱：不能为整张迁前 event study 先筛 `到达前仍未婚`，然后说 leads=0 证明无选择——这些人此前初婚本来就被定义为零。迁前诊断必须在**每个历史 t 的合法风险人口**，或固定较早基线 b（如 r=−3 开始前）尚未初婚的组中，观察此后的婚姻进入。需要报告不同 r 的风险组构成。

迁后累计初婚：在预先选定基线 b 未婚者中定义 `F^M_i(h)=1{b 到 h 初婚}`；事件后继续保留累计状态，不把他们从累计曲线剔除。先给原始曲线，再按相同基线年龄/cohort/历史标准化高低 Δ 对比。若基线取到达前一刻，estimand 是当时尚未婚者，不能据此检验更早初婚趋势，也必须承认 anticipation selection。

动态 hazard 是条件于“尚未发生”这一可能受过去处理影响的群体。故迁后 hazard 差异不能单独解释为原始群体总效应；必须与固定基线 cumulative incidence 同看。初婚处理最好为独立、同龄/性别可比的初婚进入环境差 ΔM（B）；当前 ΔCBR 可用于共同环境预测，但不能标为 marriage-environment 收敛率。

### 2.3 育：any birth、首胎、二胎三个不同对象

| Outcome | 分母/风险集 | 事件与退出 | 主要解释 |
|---|---|---|---|
| Any annual birth | 所有年龄合格、该年生育历史可判定女性 | 该年有一次或以上生育=1；不因已生育永久退出 | 年度生育发生概率；不是孩子数 |
| First-birth hazard | `parity_start_t=0` | 首次生育事件年=1，之后退出该风险集 | 尚未生育者的转移，不是所有女性中的“一胎分量” |
| Second-birth hazard | `parity_start_t=1` | 第二个孩子/第二次分娩定义预先固定；事件后退出 | 从一胎状态转移；迁后进入该组可由此前处理引起 |
| Higher-order | `parity_start_t>=2`，仅可靠史且支持足够 | 预先区分下一孩次与 any higher birth | 次要，不为追求完整强行运行 |
| 固定基线累计首胎/累计生育事件 | 基线 b 的零胎/全体女性，定义各自目标群体 | 保留已发生者直至截止；处理右删失 | 与 hazard 互补，区分时点与累计数量；不称完成生育 |

`parity_start_t = t 开始前累计活产孩子数`，前提是 lifetime history 完整。用年度时，早于 t 的日期计入；同年多胎不能无说明地从 parity0 写成先后两个独立风险年。主 any birth 按生育事件二元计数；首胎标首次分娩，二胎主分析宜明确是 parity1→≥2 的转移，并把首胎双胞胎导致 0→2 单列，不能假造处在 parity1 的暴露时间。若需要“第二次分娩”须另定义。

没有填出生模块不等于零生育。恢复 currently unmarried 时必须核实出生题路由/其他记录；若无法判定 lifetime parity，首胎人口仍不完整，只能给缺失界限或收集更完整数据。2017 roster Tier C 作为分开敏感性，不用来证明 lifelong childlessness。主/敏感性波次取舍报告样本成本，而不是直接把全体 2017 删除后不说明。

婚姻与生育为 co-primary，不把婚姻降为 fertility placebo。`Place→Marriage→Birth` 是总效应允许经过的路径；**总生育模型不控制迁后婚姻、收入、就业或迁后稳定特征**。婚前后顺序可描述，但不估 mediation。`初婚日期<迁移日期` 的生育比较为另外的 pre-union estimand；因缺离婚史，严格说是“迁前已进入初次婚/同居”，不能保证迁移时仍已婚。

### 2.4 估计方法的事前约束（下一阶段，尚未运行）

- P4 的诊断图先是风险集正确的年龄/cohort 标准化发生率与 Δ 的关系；不直接用一个无差别 TWFE 图替代所有 Y。
- Any-birth 可评估 Labour-style `individual FE + calendar FE + age controls + event FE + Δ×event` 作为比较基线；需报告连续剂量、不同迁移 cohorts、上/下迁移的支持/权重与异质性，不能自动套二元 staggered treatment 的 ATE 含义。
- 初婚/首胎终止事件优先采用明确基线年龄/历史控制的离散时间转移模型与标准化累计概率。短面板 FE logit 会丢掉全零者，FE LPM 在事件终止和内生风险构成下也不是自动因果方案；不为了与 benchmark 外观相似强行 individual FE。
- 比较来源与目的地的 place gap，不是简单“搬家 vs 没搬家”的效应。nonmover 对照在当前 CMDS 历史上未验证；较晚到达当前样本者也不是自动有效 never-treated，可能以前已经住在第三地。
- 如用 origin×move-cohort 截距，个体 FE 会吸收它；P5 应比较同组不同去向，并允许 origin×move-cohort×event-time 或支持足够的 origin×calendar-year 动态。精确年龄、日历年、出生 cohort 的线性关系和事件年/迁移年关系都需要归一化及 rank 检查，不堆满 FE 后让软件静默删除。
- Co-primary 家族预先指定：初婚、any birth，以及支持质量合格的 first/second transitions；报告原始 CI 与多重检验调整方案，不按显著性挑 Y。hazard 和累计量是互补 estimands，不机械相加系数。

## 3. 一张有成本和判据的任务矩阵

A=现有字段能做所述**描述诊断**；B=需适度重建/外部合并/实现；C=当前数据不能识别。能计算代理关联为 A，不代表实际居住地因果效应为 A。所有 N 均来自前轮 M，非修复后风险集最终 N；不同限制交集未知，不可相加损失。

| Priority | Analysis | Marriage / Fertility / Both | Endogeneity threat addressed | Why needed | Labour E already does? | Top mover precedent | CMDS feasible now? | Required variables | Sample cost | Interpretation if passes | Interpretation if fails |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 / T0 | 两个人口与年度/月度风险集、累计量 builder + 边界例子 | Both | 按未来婚育入选、未知填零、事件顺序错误 | 分母错会制造趋势 | annual birth 有；非我们初婚/孩次风险集 | Chyn–Shenhav 的 birth-order 对照说明不能混为 hazard | B；完整缺失史 C | base、marital status、初婚/同居年月、全部出生年月/总数、访谈月、DOB、routing | 恢复 63,336 未婚候选；最终 N 未知；2017 无婚期，80,163 roster births 单列 | 可进入描述/模型诊断；不代表迁移外生 | 停止该 Y 的因果模型，报告缺失人口及需补资料 |
| P2 / T0 | move clock、来源质量、外部 Δ 两分量与支持清单 | Both | 错 origin/日期、机械处理、无有效变异 | 先知道比较什么 | 实际住址；NCHS 独立 Δ；排重复 | FGW 实际迁移核验；Ding claims 跨地核验 | A 代理诊断；真前址 C | arrival/first_leave、one-move/city、hukou、dest、pre3 CBR、地理 crosswalk | 匹配 323,949，缺38,296；zero162,441；不是新的总样本 | 可定义 proxy-gap 条件性设计 | 来源无法验证则保留代理标签；无变异单元不估 place slope |
| P3 / T1 | 近迁移婚/育/推断孕期排序 + 动机/缺失；donut 作敏感性 | Both | 家庭计划/怀孕共同引起迁移及去向 | 直接瞄准反向因果 | 动机、意愿、婚姻有；非完整孕期 | Labour；FGW 同期健康冲击逻辑 | A 年度计数；B 月份与修复风险集；完整计划 C | marriage/birth/arrival months、reason、missing flags；孕期仅明确假设 | M birth±1 保留273,440，±2 236,884；婚+育 dated subset187,759/159,048；非 P1 最终 N | 仅削弱可见近迁移冲击；不排除计划 | 改为关联解释/需要更外生设计；不得以删后显著救结果 |
| P4 / T1 | 分 Y 迁前/迁后标准化曲线、joint leads、slope、95% CI、累计曲线/趋势敏感性 | Both | 预先演化与风险组/时长构成 | 量化可排除的偏差，而非 p>0.05 | 动态图有；完整信息量包未见 | FGW；Cantoni–Pons；Rambachan–Roth 方法补充 | B | P1风险年、Δ、age、cohort、event/calendar、协方差、每格暴露 | M年龄限制±3平衡202,191，±5 125,206；仅供成本，不主筛 | 限制渐进选择解释；不能排除同步冲击 | CI过宽=无信息，不是证明偏误；稳健大趋势则不宣称基线因果 |
| P5 / T1 | 同来源×迁移cohort支持、迁前家庭状态预测 Δ、组内动态估计 | Both | 去向选择、来源共同冲击、FE冗余 | 找真实组内反事实比较 | 主式未见该动态控制；IV不同 | Beheshti–Neller origin×event FE；Finlay 等 origin×race | A 支持/历史描述；B P1后模型 | hukou province、arrival cohort、survey wave、pre-move histories、Δ、sign | 组内 Δ 方差/单例剔除未知；31省不等于31个强识别簇 | 对可观测/共同来源时变混杂更稳健 | 支持不足则缩窄预先声明目标群体；仍有选择则降格 |
| P6 / T1 | 路径质量 + 持续居留/返乡选择诊断（并列而非逐层缩样） | Both | 压缩多次路径、婚育影响留存造成 collider | CMDS 特有关键缺口 | 多次剔除/平衡有；stock问题非同等 | FGW attrition；新近 displacement 研究的 survivor 边界 | A 描述；B 灵敏度；所有到达者留存校正 C | move/city count、duration、birth/marriage历史、2017 Q314/315/317/318/321A | 一次move54,703；一city45,183；recent≤2 135,208；2017意向最多80,163，婚史缺失 | 只支持调查时留居者的条件性描述；意向非实际退出 | duration相关差异不能称同化；需要追踪/来源地返乡数据 |
| P7 / T1 | origin/destination依赖、少簇推断和支持/影响诊断 | Both | 共同地区冲击使 SE 过小、少数省驱动 | 个体 N 不是独立处理数 | household+state已做 | Cantoni–Pons voter/state；Cabral等 origin/destination | A 支持；B 正确 estimator bootstrap | P4/P5 scores、origin/dest、ID、权重、cluster大小 | 理论无固定删样；有效簇/杠杆未知；约31×31而非961独立簇 | 提供可靠不确定性；不修复 endogeneity | 宽CI/省依赖则报告不确定，不换聚类求显著 |
| P8 / T2 | 独立年龄/孩次/初婚环境与 own-group vs unrelated-group 联合验证 | Both | 构成率代替环境、预测泄漏、一般目的地选择 | 比多加控制更有反证含义 | race-specific有，竞争预测未见 | Chetty–Hendren；Chyn–Shenhav donor separation | B；数据不够则停止 | 独立donor 的group×place×year numerator/denominator、预定组别、holdout fold | 外部/细地理交集未知；2017 county-origin80,163但无婚期，不能作为两Y共同细地理样本 | 群体相关性符合预设预测；不是证明排除限制 | 无独立差异/共线为无信息；稳定错误组预测挑战目标解释 |
| V1 / T2条件项 | 外部冲击/其他mover IV的设计论证与验证（不是默认下一跑） | Both | 个体去向/时点选择 | 仅有可信 assignment 才有升级价值 | 灾害及同源 IV 已做 | Chyn–Shenhav；Chetty–Hendren；2026 displacement | C 现成外生设计；B若后续取得有效资料 | assignment/冲击、预定来源、直接效应、donor、first-stage/weak-IV CI | 未知；CMDS military=1、study257不能造准实验 | 在另外写明排除限制下解释局部效应 | 无排除限制就不估因果 IV；绝不把生育政策作迁移排除工具 |
| V2 / T2条件项 | AKM网络、leave-out连通、偏误修正与共同支持 | Both | 稀疏迁移噪声误判地方方差/排序 | 仅未来报告因果分解时必要 | 最大connected有，修正未见 | Lyubich；Kline–Saggio–Sølvsten；Chyn–Shenhav | A省proxy graph；B修正实现；真轨迹C | 有效person-place incidence、edge multiplicity、error模型 | M省有效360,595；922有向格含self；不是实际居住网络；修正损失未知 | 仅去噪；不把proxy graph升格真实AKM | 暂停方差份额因果叙述，保留描述网络 |
| R1 / T3 | 窗口/年龄/近期、work、跨省、balanced、替代预定度量的少量对照 | Both | 特定实现/支持依赖，不能统称解决内生性 | 结果解释范围与复现稳定性 | 多数已做 | Labour Fig.5；其余文献 | A样本成本；B修复后模型 | 对应P1–P7字段，预先列差异 | work231,814；cross-province183,840；within178,405；限制交集未知 | 说明同一结论在哪些测量支持上成立 | 查测量/支持变化，不能按显著性挑样本 |

所有本文件拟议分析归属上述 P1–P8、V1–V2 或 R1；子诊断不是额外无序回归清单。P1–P2 未过关，后面的模型只可作有标签的探索。

## 4. 下一轮真正应跑的 8 项，交付什么、何时停止

1. **P1**：两套 universe + person-year risk-set flow；人工边界例子和自动断言。测试 never-married、未知婚期、同居、首胎 twins、同年两事件、调查年部分暴露、缺 roster 子女、事件前已婚/已育。报告女性数、person-years、事件数、每 r 风险分母；不发布行级微观记录。
2. **P2**：来源/时间证据表、Δ两端及匹配分布、按来源质量/迁移年/波次的有效支持。确认 province zero gap 不能检验省内城市差异；不把 zero gap 全体叫 nonmovers。
3. **P3**：近迁移婚育频数改为合法分母的发生率；月份有无分开；动机缺失保留；孕期由出生倒推只作假设诊断。donut 按删除**事件年**与删除**整个人**分别标 estimand，尤其不得删去迁后发生者后称总效应。
4. **P4**：婚与育各自的 leads/post/cumulative；先看可排除多大偏差。预定显著性、经济意义界限并同时报告 CI，不从看到的效果倒选阈值。若点估计近零，避免除以近零主效应，以预设有意义绝对幅度评估。
5. **P5**：目的地选择预测和组内动态比较；先输出剩余 Δ 方差、effective cells、两方向 overlap；小单元合并必须预先有规则，不按结果调。
6. **P6**：宽/一次move/一city/来源B/近期并列表；不同 duration 的婚育构成和2017留存意向。观察关联不估不存在的退出概率；必要时给显式假设下的 selection sensitivity，而非声称识别全体 arrivals。
7. **P7**：按 chosen estimator 审核 crossed origin/destination 与 person dependence；OD pair cluster 不等于 two-way origin/destination。少簇 bootstrap 要与交叉结构匹配，不随便套一维命令。随主结果提供有效簇、影响省与置信区间。
8. **P8**：只有 P1–P7 的结果支持继续，才建独立 ΔM/ΔF_group。group 用基线年龄/孩次，或明确动态转移模型，不按处理后的已婚/孩次分样本宣称 exogeneity。holdout 至少按个体所有年份分隔，视来源考虑wave/place/cohort外推；独立构造不能解决 donor stock selection。

第一批实际计算应是 P1–P3 的测量/描述产物；**不是先重跑旧 21,383 人回归，也不是先做 IV、AKM 或机制。** V1–V2 留到有数据/科学问题需要再启动。R1 只围绕已发现的具体敏感点。

## 5. 暴露长度、比较组和“通过”到底意味着什么

P4/P6 中按 arrival age、calendar cohort 和已观测 duration 交叉报告，不将“住得越久越像当地人”直接归于同化。晚 r 的样本更老、迁移更早且必须留到调查，出生间隔与风险退出都能产生梯度。完整历史缺失时，真正累计居住暴露为 C；报告的 years-since-arrival 为观测日期差，不是历史证明。

初婚和首胎的累计结果必须在同一基线风险组和可比 follow-up 上标准化；截短 follow-up 的女性是 right-censored，不是零事件。不能用 requiring complete future window 作为唯一主样本来隐藏这种区别。成分相同的 balanced curves 可作 P4/R1 对照，但会缩窄 target population。

通过可见诊断，最多增加“在这些测量与条件平行趋势/无同步选择假设下”的可信度。若前址、出生史或退出选择的核心未知不能补上，应最终写成**目的地留居者的户籍−现居环境差关联及其诊断**，而非全体迁移者/全中国女性的地点因果效应。明确这一边界比增加机制显著性更重要。

## 6. 不做事项

本轮不运行新因果模型、机制、政策中介、住房/托育/网络解释；下一轮也不在 Tier 0 未完成前启动它们。当前 covariates 不标“迁前”；工作/教育/拆迁动机不标“随机”；不以零 person-place covariance 证明外生；不以单次迁移代理恢复完整居住史；不把两类 Y 合成一个不透明家庭形成指数。
