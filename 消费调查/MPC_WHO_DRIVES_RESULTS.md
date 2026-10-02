# Who drives the MPC size curve? — bounded observable pass

本轮直接继承 PR #9/#10，不重新选择 headline，也不更改 manuscript。新增任务书授权的范围仅为 5 个核心经济 moderator、6 个描述性变量及其有限联合/校准诊断。主 outcome 为原始 category 6（>75% top-MPC）；z=(-1,0,1)，每一步对应金额乘五。以下 slope/interaction 均为概率单位，不是 implied yuan。Restricted 始终是 Food 与 Medical 各 50%，不是样本量加权合并。

## 1. Bottom line

**当前 observables 不能提供一个可靠的“谁驱动曲线”的机制解释。** 五个核心变量在 Cash amount-slope moderation 和 Restricted−Cash moderation 的两个预定 Holm 家族中均未通过校正；六个描述性变量也没有。Cash decline 遍及各固定分组，而其总量贡献主要反映人群份额。联合交互检验较弱、增加 slope interactions 没有改善样本外预测，预测敏感度 quintiles 也没有得到正向校准。因此采用任务书的第三种 paper implication：**observables explain little; retain the reduced-form puzzle**。这是“未解释出”的结论，不是证明真实异质性不存在；不改变 PR #10 的 suggestive 定位，也不把 upper-tail visibility 升格为已证实 tail-specificity。

## 2. Who drives the Cash size gradient?

原有 Cash top-category slope 为 −0.04055，95% CI [−0.05684,−0.02425]；200→5000 原始概率变化为 −0.08101。五个变量的单 moderator、每 1 个 R 标准差的 slope moderation 如下。所有四个有序/连续 moderator 的 CI 均跨零；补贴经历是 2-df categorical 检验，不能把 yes/no/unknown 排成一条等级轴。

| Moderator | Cash z×X | 95% CI | raw p | Holm p |
|---|---:|---|---:|---:|
| Emergency liquidity Q7 | −0.00016 | [−0.02063,0.02031] | .988 | 1.000 |
| Harmonized personal income rank | 0.01129 | [−0.00742,0.03000] | .237 | 1.000 |
| Food expenditure rank | −0.00903 | [−0.02795,0.00988] | .349 | 1.000 |
| Medical expenditure rank | −0.00369 | [−0.02201,0.01463] | .693 | 1.000 |
| Prior subsidy, categorical omnibus | — | 2 df | .552 | 1.000 |

不能凭某组内部 slope 显著、另一组不显著就断言组间不同。Tier 2 的年龄、教育、家庭规模、有未成年子女、住房、工作状态亦未通过独立六变量家族；最小 Cash Holm p=.733（minor child）。完整 component/omnibus 及 Food/Medical 诊断均保留在两个 interaction tables。

## 3. Who drives the Restricted-vs-Cash difference?

基准 Restricted−Cash slope=0.02954；此次单 moderator 结果为：

| Moderator | Restricted−Cash z×X | 95% CI | raw p | Holm p |
|---|---:|---|---:|---:|
| Liquidity | 0.00235 | [−0.02112,0.02583] | .844 | 1.000 |
| Income rank | −0.01071 | [−0.03214,0.01072] | .327 | 1.000 |
| Food rank | 0.00925 | [−0.01296,0.03145] | .414 | 1.000 |
| Medical rank | 0.01806 | [−0.00362,0.03974] | .103 | .513 |
| Prior subsidy, categorical omnibus | — | 2 df | .686 | 1.000 |

固定 subgroup 的 differential 最大点估计出现在高医疗支出组（0.08071，nominal CI [0.01553,0.14589]），以及食品支出低/高组（0.05825/0.06457），而非一个清晰线性的低 liquidity 梯度。这些是描述性 subgroup estimates，不是校正后 moderation 证据，也没有为这些局部结果追加分组或非线性搜索。`subgroup_differential_slopes.csv` 和 compact forest 提供全部组的 Cash、Restricted、差值及 secondary form contrasts。

## 4. Liquidity

Q7 是主观 emergency fundraising capacity，不是可核验的资产余额。分组预定为 0–5 / 6–8 / 9–10，R N=1400/2486/1611。Cash200 top 概率分别 .16774/.11070/.13990：低组点估计更高，但并非单调。连续 Cash200 level moderation=−.01375，CI [−.04240,.01490]，只是 nominal、并不精确；联合模型也不精确。

三组 Cash endpoint change 分别 −.08700/−.07609/−.08468，Cash slopes −.04332/−.03799/−.04235；Restricted−Cash slopes .03026/.02628/.03438。低组没有明显比高组更陡，也没有更大的 differential。连续 moderation 近零；joint Cash moderation=−.00063、RC moderation=.00181，均不精确。**完整 liquidity signature 不成立**，不能写成“流动性不足驱动小额现金反应”。

## 5. Income

沿用 harmonized income rank，11–16 减十的 30 条 legacy 记录仍保留；这是粗略收入档位，不是精确统一人民币收入。原始字段测量的是个人收入，不是家庭总收入，因此不能冒充 household income 的直接检验。

低（rank1–3）、中（4）、高（5–6）组 Cash200 top 概率为 .13125/.13077/.14070，并没有低收入小现金反应更强的 level signature。端点降幅 −.09043/−.08713/−.06046，方向上低/中组更大；但 Cash moderation=.01129、RC moderation=−.01071 均不精确、Holm=1。Joint estimates .01539/−.01491，CI 仍跨零。RC subgroup slopes .02944/.03561/.01509 也不是清晰单调证据。故最多是弱的方向性倾向，不是完整 income mechanism。

## 6. Consumption needs

Food rank 与 Cash200 level 存在正向关联：单变量每 SD=.04565，nominal CI [.01678,.07452]；联合=.04673，CI [.01464,.07883]。这只是 level association，**不能解释 amount curve**。Food rank 的 Cash slope 和 RC slope moderation 未通过检验，直接 Food−Cash moderation=.00322，CI [−.02305,.02949]。

Medical rank 的 RC moderation=.01806，raw p=.103、Holm=.513；联合=.01476，CI [−.00842,.03793]。真正 need-matching 对应的 Medical−Cash moderation=.00801，CI [−.01584,.03185]。反而 Medical rank×Food−Cash 是 nominal .02812，p=.0295，未作 confirmatory interpretation，且不能当作医疗需求匹配证据。这一跨域局部结果是保留的脆弱事实，不用于机制救援。

医疗需求为过去一年家庭自费支出，而账户长期有效，不能认证 medical bindingness；食品支出为家庭月度分类，不等于个人需求。两者都没有形成对整个 form×size puzzle 一致且校正后精确的解释。

## 7. Prior subsidy experience

原始 yes/no/unknown 三组 N=2753/2269/475。Cash slopes −.04073/−.04579/−.01355；RC slopes .03380/.02914/.00387。Unknown 样本较小、CI 很宽，不能当作“无经验”或者第三档经验强度。Cash 和 RC 的 2-df omnibus raw p=.552/.686，Holm 均=1；joint yes/unknown components 也不精确。没有证据支持“熟悉补贴的人具有明确不同的 size sensitivity”。图中的 dummy coefficients 是每 1 SD 编码变化，不是未经缩放的 yes−no 差。

## 8. Contribution decomposition

用所有 R 的固定 subgroup share 乘以各组 Cash5000−Cash200 概率变化。每一个变量的分区单独加总，得到共同人口构成标准化的总变化，而非强制等于未标准化 raw −.08101。五个标准化总变化在 −.07975 到 −.08204 之间，差异来自各 arm 的有限样本构成。没有人口代表性权重。

| Separate partition | R group shares | Shares of standardized Cash decline |
|---|---|---|
| Liquidity low / middle / high | 25.5% / 45.2% / 29.3% | 27.2% / 42.3% / 30.5% |
| Income low / middle / high | 25.7% / 43.5% / 30.9% | 29.1% / 47.5% / 23.4% |
| Food low / middle / high | 22.3% / 60.1% / 17.7% | 30.7% / 42.8% / 26.4% |
| Medical low / middle / high | 19.9% / 66.4% / 13.7% | 21.7% / 60.5% / 17.8% |
| Subsidy yes / no / unknown | 50.1% / 41.3% / 8.6% | 50.7% / 46.3% / 3.0% |

因此大量降幅发生在人数最多的中档收入/医疗支出人群；liquidity 的贡献几乎随份额分布。食品支出两端组相对人口份额贡献更多，是描述性、非单调事实，不自动构成机制。所有 cell N、Wilson CI、endpoint CI、weighted contribution CI 都已报告；contribution share 是不带因果含义的描述性比率。**不同变量的贡献不能相加**，不声称“income explains X%”。

## 9. Joint explanatory power

五个概念变量用六列表示（补贴 yes 和 unknown 两列），完整包含 form/z/X 所有指定 lower-order 与三阶交互，仍保留三 form 独立块。Joint Cash moderation Wald=5.065（6 df，p=.535）；RC Wald=4.923（6 df，p=.554）；两检验 Holm 均=1。

平均 RC slope 从基准 .02954 到 joint .02807，CI [.00884,.04730]；Cash 从 −.04055 到 −.04080。平均 randomized pattern 仍在，不能称作 observables “解释掉”效应。实测 X profiles 的 fitted Cash slope p5–p95=[−.07111,−.00997]，RC=[−.00810,.06565]，但这只是带估计噪声的拟合范围，不是已观测个体斜率、也不是已识别的真实 variance explained。

同一五折下，OOF MSE 为 baseline .068811、含 form-specific X levels 的参考模型 .068188、增加所有 slope interactions 的 joint 模型 .068512。**交互增益 level−full=−.000324**（相对 −0.475%）；499 次 model-refit exponential bootstrap CI [−.001206,−.000121]，属固定 learner/fold 的次要诊断，不用于新的“显著更差”headline。Full 相对 baseline 的微小 .000299 改善 CI [−.001229,.000494]，混合了 level 与 interaction，不能解释成 heterogeneity 被预测出来。

## 10. Prediction / calibration

仅执行预定五变量线性交互诊断，无新 HTE 搜索、调参、树、RF/SHAP。五折按原九 cell 分层；每个人的 sensitivity forecast 与 quintile cutpoints 均来自不包含其 outcome 的 training fold。Cash sensitivity 定义为 p200−p5000（正值为下降）；RC sensitivity 定义为 Restricted endpoint change 减 Cash endpoint change。用设计概率 1/9 的 cross-fitted AIPW scores 校准，并同时展示 held-out quintile 原始 randomized endpoint estimates。499 次同权重跨 fold bootstrap 重拟合模型、重新分组，CI 不只把训练模型当作已知。

Cash forecast Q1→Q5 平均 .02405→.13914；实际 AIPW decline .08431→.04622，raw randomized decline .09357→.04034，不是预期正排序。校准 slope=−.18295，bootstrap CI [−1.49523,.56235]；最高−最低 AIPW difference=−.03809，CI [−.20290,.16397]。RC 校准 slope=−.07505，CI [−1.63689,.56439]；Q5−Q1=−.01030，CI [−.22562,.19457]。不能证明负向 sorting，也不能确认稳定正向 sorting。

OOF R² 为 baseline .00753、levels .01650、full .01183，均为个体 binary outcome 总变异的预测度，**不是 treatment-effect heterogeneity explained fraction**。LPM observed predictions 中 full 有 5.18% 越出 [0,1]；全部 counterfactuals 4.85%。没有静默裁剪用于 sensitivity；clipped MSE level/full=.068146/.068394，仍无交互改善。Bootstrap CI 是 conditional-fold、smooth linear learner 的有限样本诊断；quintile 边界、稀疏 tail、共享 training folds 与非规则排序限制其解释，不是独立复制或精确 RI。

## 11. Robustness and negative evidence

按结果前固定规则，以两个 primary omnibus raw p 的较小值排序，选 Medical 与 Income 做有限 robustness；它们不是校正后“发现”。只重复 top75/ordinal/midpoint/ge50 × R/A/C/Q1/Q2，全部 320 component/omnibus rows 保留，不扩展其余变量。

Medical 的 RC top moderation 在 R/A/C/Q1/Q2 为 .01806/.01660/.01912/.02278/.02045，方向一致，但所有 CI 跨零；Q2 CI [−.02637,.06727] 很宽。Income RC top 为 −.01071/−.01074/−.01151/−.02627/−.02333，也全不精确。R 的其他 outcomes 对两变量 Cash/RC 均不精确。Q1 income ge50 Cash=.03190（nominal CI [.00270,.06110]）、RC=−.03461（[−.06913,−.00010]）是局部、选择后的脆弱结果，Q2/primary top 不确认。Medical Cash moderation 在 top 与 ordinal/midpoint 的方向并不统一，且 ordinal/midpoint 在 Q2 反转；没有隐藏这些结果。Q1/Q2 不是更好识别的总体。

本轮 null 的 CI 仍容许经济上有意义的差异；尤其小 unknown/high-need subgroup 的精度有限。不把未显著当作等价，不把局部 nominal 显著当作机制证实。

## 12. Mechanism interpretation

实验识别：在随机 form/amount 条件下，固定 pre-treatment observable 的 subgroup amount effects，以及实验效应随 X 的 moderation。X 本身未随机，不能说 liquidity/income/need 导致曲线。每个人只有一个 scenario，不能推断其从小额到大额实际改变了多少。

Observables suggest：降幅在多个组内广泛存在；population-size 最大的组承载更多总变化；income 有弱方向倾向，food 有 level association，medical 有局部三阶点估计。它们**没有共同满足完整的机制 signature、multiplicity precision、joint survival 与 honest sorting**。

Unknown：真正驱动差异的是何种状态/认知、是否存在可靠的个体 sensitivity、假想分档反应与真实支出之间关系、form bundle 的哪些属性重要。不能把现有 null 升格为 mental budgeting、latent trait 或其他未经测试机制；也不据此启动心理变量搜索。

## 13. Paper implication

选择 **observables explain little; retain the reduced-form puzzle**。这五个常规 observable 在本数据/本限定模型下没有提供一致且可样本外验证的 who-drives layer。不要使用“limited financial slack households drive the unusual small-transfer response”的强句，也不要把个人收入 proxy 写成已完成 household-income mechanism test。

当前 paper 可保留 PR #10 的 **plausible main story but suggestive** 证据边界，加上“standard observable markers do not readily account for the form-by-size pattern”的限定性机制 null。不能因此把主故事自动升级为 strong enough，也不能写成“所有 observables 与曲线无关”或“不可解释部分占真实 heterogeneity 的百分之多少”。未修改论文正文。

## 14. Stop decision

**不再对当前数据追加 observable-variable exploration。** 已穷尽本任务书的有限变量、贡献分解、联合模型及校准诊断；进一步心理变量、HTE/SHAP/forest、大规模 subgroup、latent/cluster 或新 cutpoint 搜索没有本轮科学授权或依据。完整交付后提交新 stacked PR，依赖 #10/#9，不自行 merge。未来若要机制因果识别，需要新设计/新数据与明确假设，不在本轮实施。
