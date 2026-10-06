# Core pre-treatment constructs

## 统一时点与状态

主cutoff固定2025-09-01 00:00 UTC，保守早于本年正式review/assignment。只有年份的出版/任职记录仅纳入截至2024年底的记录；这会损失2025早期信息，但避免把年份不精确的后期记录放入前期。将来有确切公开日期才允许纳入cutoff前2025记录。仅用于ICLR2026构念，不引入其他年份conference outcomes。提交文本也必须取得cutoff/提交时冻结版本，current metadata不可假定冻结。

“Build”的诚实结果是：本地不具有构建A/C的原始出版语料，B仅有部分回溯正例；故不以自报expertise、confidence或undated overlaps造替代变量，不产出虚假embedding/portfolio。可用性诊断和严格日期/overlap代码已运行。

## A Objective expertise

先验证reviewer–publication identity：公共profile链接只作为线索，核验作者、机构、共同作者与歧义；不只按同名匹配。publication日期与freeze paper版本合格后，预先冻结文本处理、model版本/权重hash和topic编码规则，且先于outcome分析。四种预指定E：max cosine；mean top-5（不足5用全部并记录N）；与归一化publication centroid的cosine；词汇/topic overlap。无出版不填0，标记unknown；同一模型用于所有候选，不用结果挑模型。

验证包括独立人工topic判定、identity抽检、年份边界审计、四定义leave-one-out。confidence只作convergent calibration，不作E定义，也不能据此验证因果效应。当前没有可冻结的已运行embedding模型，故不声称embedding结果存在。

## B Dated proximity

定义：cutoff前合作edge、years since last coauthor、仅前期edge的shortest path、同一机构的实际任职区间交集、可靠dated advisor关系。网络非连通与未完整观测要区分；undated list不能推出边发生于review前。机构代码要求双方完整数字start/end、1900≤start≤end≤2024；同domain且区间交叠才记正例。拒绝缺end/2025end等不合格区间，不将缺失填负例。

得到556/29,813行含一个保守pre2025区间交叠，属于partial retrospective candidate positives，尚未独立验证机构/identity/record correctness。完整可用于定义负例的history行=0；29,257行仍unknown；可定义的556全为正，paper内有正负variation=0。这是信息不足，不是不存在实际无关系reviewer。不能对这个样本跑within-paper proximity effect。

## C Reviewer portfolio

从同一identity-validated前期出版语料构建：固定topic vocabulary，topic share的Herfindahl concentration、Shannon entropy、预定义边界跨度、最早发表到cutoff的seniority；status只用cutoff前可冻结的public citation/职位等可信记录。不能用会后累计citation替代前期status。若仅能取publication years/titles，不能假装已获得abstract/citation history。

## Coverage / validation（实际运行）

| 构念/支持 | 分母 | 有效数量 | 验证状态 |
|---|---|---|---|
| local reviewer profile saved publications字段 |13,561 CSV rows|0|字段盘点，不代表现实没有出版 |
| local author saved publications字段 |28,465 CSV rows|0|同上 |
| reviewer public DBLP link |13,561|9,560|链接非identity验证 |
| author public DBLP link |28,465|13,147|同上 |
| deterministic public publication availability pilot |3 profile links|0 successful，3 URLError|访问未完成，不是identity否定 |
| A validated E |29,813 review rows|0|缺dated corpus和freeze paper，不可计算 |
| B dated institution候选正例 |29,813|556|partial retrospective，尚未独立验证 |
| B 完整负例资格 |29,813|0|unknown绝不填0 |
| B dated coauthor/network/advisor |29,813|0 usable validated values|本地无dated graph；不是无真实关系 |
| C validated portfolio/status |13,560 local reviewer IDs|0|未获得合格publication corpus |

详细支持计数见profile_field_support.csv、dated_proximity_availability.csv、dated_proximity_variation.csv、public_publication_pilot.csv；字段名如emails只是存在数量，未输出地址。3人的公开pilot按CSV首个合法DBLP链接确定、先于outcome，不代表全体可获取率，也不证明公共bibliography不可取得。没有retry/TLS bypass。

## Missingness selection

有ID的27,470 review rows（评分可用27,423）current rating均值4.2695、confidence 3.6668；缺ID的2,343行均值4.2185、confidence 3.6500。profile_link是ID存在指标，不代表E可构建。paper组计数可重叠；current score/文本都是结果变量，只用于描述缺失选择，不能作assignment前balance。area分布、authorslots、文本长度已汇总。不能据这些均值接近声称missing at random。全部E不可用，无法比较E coverage的结果选择；应明确report unavailable。

## Leakage 与决定性风险

retrospective profile可能增删history、publication、relations；current submission可能修改内容；prior原代码历史domain重合不要求实际时间交叠。旧undated coauthor阳性和arXiv首搜索结果不得带入新构念。未来edge只诊断漏时/遗漏，且可能受本次互动影响；没有dated graph就不执行此negative control。测量多定义与缺失审计只能校验构念，不能产生外生分配。
