# MPC size-curve final evidence strengthening

日期：2026-10-02。依据 `MPC_SIZE_CURVE_STRENGTHENING_WORK.md`，直接扩展 PR #9 (`d749f5c`)，不重跑其 discovery pipeline，不修改 manuscript。汇总、代码、五组图和复现说明均位于 `results/mpc_final_strengthening/`。

## 1. Bottom-line judgment

**plausible main story but must be written as suggestive**（选项 2）。本轮增强了一个更窄的事实：Cash 的最高 stated MPC 档随金额压缩较强，Food 与 Medical 在这一 margin 上方向一致，equal-weight Restricted−Cash 的概率斜率差清楚。但没有建立“效应 genuinely upper-tail concentrated”：所有四项直接 cross-threshold contrasts 都不精确。Link/relative scales 方向一致、nominal evidence 有支持，multiplicity-adjusted evidence 则较弱；原始 ordinal primary reference 仍不足以支持一个普遍、强确定的 mean-MPC curve claim。最强表述应是 **“form-by-size differences are most visible in the upper tail”**，而不是 “tail-specific law”。这轮不会以辅助 threshold 结果替换原始序数 primary estimand。

## 2. Restricted vs Cash

Restricted 是 `0.5 Food + 0.5 Medical` 的潜在结果均值/斜率平均，不是第四个随机处理，也不是把两组按人数直接合并。R/unadjusted、`z=(-1,0,1)`、OLS HC3；每单位代表金额增加五倍。以下 Holm family 是任务书六个 estimands：Cash、Food、Medical、Restricted、Restricted−Cash、Food−Medical，在每个 outcome 内固定；Food−Cash/Medical−Cash 为补充 contrasts，原有 PR #9 五项检验保留原解释。

| Outcome | Cash slope | Food slope | Medical slope | Restricted slope | Restricted−Cash [95% CI] | Raw / Holm p |
|---|---:|---:|---:|---:|---|---|
| Ordinal score | −.1160 | −.0787 | .0291 | −.0248 | .0912 [−.0165,.1989] | .0970 / .4089 |
| Midpoint | −.02593 | −.01672 | .00112 | −.00780 | .01813 [−.00005,.03631] | .0507 / .2027 |
| Alternative top=1 | −.03099 | −.01826 | −.00008 | −.00917 | .02182 [.00177,.04187] | .0329 / .1521 |
| Any spending | .00025 | .00522 | .01559 | .01041 | .01015 [−.02121,.04151] | .5257 / 1.0000 |
| ≥10% | −.01202 | −.01727 | .02430 | .00352 | .01553 [−.01889,.04996] | .3765 / 1.0000 |
| ≥25% | −.03244 | −.03672 | −.00006 | −.01839 | .01405 [−.01729,.04539] | .3797 / .7594 |
| ≥50% | −.03125 | −.01756 | −.00108 | −.00932 | .02193 [−.00230,.04617] | .0761 / .3805 |
| >75% / top category | −.04055 | −.01235 | −.00965 | −.01100 | .02954 [.01043,.04865] | .00244 / .01222 |

Top-tail Food−Cash=.02819、Medical−Cash=.03090，均为正且接近，不是 Medical 一组独自驱动 pooled contrast。Food−Medical top probability slope=−.00270，CI [−.02267,.01727]，p=.7909；top logit AME difference=−.00268，CI [−.02283,.01748]，p=.7944。**不是等效性检验**，仍允许约两个百分点/step 的差别。

Average-MPC 不能作同样强的 pooling：Food−Medical ordinal=−.1078，CI [−.2292,.0137]，p=.0820；midpoint=−.01784，CI [−.03783,.00214]，p=.0801。点估计差异相对于各自 mean slopes 并不小，而 pooled ordinal 不精确。可保留 **distribution-specific pooled description**，不能称两种受限资源的整个 mean-MPC curve 已证实一致。完整 SE/CI/所有 contrasts 见 `restricted_vs_cash_slopes.csv` 和 `restricted_form_heterogeneity.csv`，图 A 保留 Food/Medical 两条浅色线使 pooling 透明。

## 3. Is the effect genuinely upper-tail concentrated?

使用同一组 5,000 次 nine-cell stratified respondent bootstrap，保留各格人数及五个嵌套 threshold 的联合 covariance。以下是 Restricted−Cash 的 **直接差异**，不是比较各自 p 值；Wald CI/p 来自 joint bootstrap covariance，四项 Holm。

| Direct contrast | Estimate | SE | 95% CI | Raw / Holm p |
|---|---:|---:|---|---|
| d75−dany | .01939 | .01723 | [−.01439,.05317] | .2605 / 1.0000 |
| d75−d10 | .01401 | .01754 | [−.02036,.04838] | .4243 / 1.0000 |
| d75−d25 | .01550 | .01420 | [−.01234,.04333] | .2752 / 1.0000 |
| d75−d50 | .00761 | .00838 | [−.00881,.02403] | .3635 / 1.0000 |

所以 **tail-specificity 未建立**。Food secondary d75−d25 nominal p=.0453，Holm=.1813，也不能补救 pooled primary null；Medical 的 d75−d10/d25 点估计甚至略负。Global equal-threshold-profile Wald p=.7271（Food=.3051、Medical=.7517）；不拒绝不表示阈值效应相等。图 B 可展示“最可见的 margin”，不能据其上升外形宣称确定的尾部集中。

Multinomial logit 只作 distribution robustness：预测 Cash category-6 shares=.1352→.0867→.0543，与原始 .1341→.0891→.0531 相符；floor 预测 .2762→.2790→.2757，仍几乎不变。Medical category-6 .0610→.0506→.0417，同时第三/第五档有补偿性变化。它不会新增可靠性：最大 cell-category misfit 为 Medical/1,000 的 floor +.02930（raw .3284，fit .3577），平滑掉部分非单调变化；原始格概率始终优先。没有 headline multinomial coefficients。

## 4. Does baseline headroom explain the result?

“Baseline”在这里是 200 元情景下的处理后组概率，不是同人的 pre-treatment response。Cash 的起点更高可能影响 percentage-point headroom，但 logit/probit 与 relative change 并不能实验性分离这个机制，只是 scale robustness。

| Top-category Restricted−Cash contrast | Estimate | 95% CI | Raw / six-test Holm p |
|---|---:|---|---|
| Logit link slope difference | .31788 | [.05498,.58078] | .01779 / .08896 |
| Probit link slope difference | .16567 | [.03687,.29447] | .01170 / .05850 |
| Logit probability AME difference | .03027 | [.01035,.05018] | .00289 / .01445 |
| Probit probability AME difference | .02991 | [.01052,.04930] | .00250 / .01248 |

AME 对每个 form 的三种金额等权平均导数，delta inference 使用 analytic gradients；不是把 nonlinear interaction coefficient 当概率 DID。Restricted AME 是 Food/Medical AME 的均值，link contrast 是两个 link slopes 的平均，**不是 pooled probability 的 logit**。全部五 threshold 的两个 link 及 AME 均输出。

| Top-category endpoint scale (200→5,000) | Cash | Food | Medical | Equal-weight Restricted |
|---|---:|---:|---:|---:|
| Probability change | −.08101 | −.02460 | −.01928 | −.02194 |
| Risk ratio | .3959 | .7524 | .6795 | .7249 |
| Odds ratio | .3620 | .7324 | .6658 | .7080 |

Restricted/Cash ratio-of-risk-ratios=1.8311，percentile bootstrap CI [1.1508,3.0728]；ratio-of-odds-ratios=1.9558，CI [1.1827,3.3971]。Pooled ratios先对 Food/Medical 的概率等权混合再取比值，不平均两种 ratios。其 raw p=.0170/.0140，但预先固定的九个 comparative scale tests（三个 contrast×三种尺度）Holm 均=.0983；pooled probability-change difference=.05907，CI [.02154,.09688]，Holm=.0203。Medical/Cash 单独 relative CIs 跨 1，Food/Cash nominal CIs 不跨 1，九项 Holm 也未通过。

结论不是“只在 pp 尺度有结果”：relative/link 点估计和 nominal inference 支持方向，AME 与线性概率效应接近。但也不是“headroom 已排除”：link/relative multiplicity-corrected证据较弱，没有直接识别 headroom 的反事实。图 C 的 CI 为未校正的 pointwise bootstrap intervals，不能代替 Holm。

## 5. Specification stability

严格执行 **420 个**预定 specs：5 samples×2 adjustments×2 amount representations×7 outcome representations×3 contrasts。固定 control block，包含所有 Q1/Q2；没有挑显著模型。Trend 每单位五倍金额；saturated endpoint 保留全程原估计，并仅在 comparable columns 除以 2。Logit AME 是平均局部导数，saturated logit 是端点概率变化；这只是透明的共同显示单位，不把不同函数形式视为同一精确 estimand。

| Restricted−Cash coding（各20 specs） | Positive sign | Raw CI >0 | Comparable median / range |
|---|---:|---:|---|
| Ordinal | 80% | 20% | .09098 / [−.02963,.12073] |
| Midpoint | 100% | 40% | .01804 / [.00904,.02432] |
| Alt top | 100% | 60% | .02173 / [.01313,.02855] |
| Top probability | 100% | 70% | .03098 / [.02849,.03610] |
| Top logit AME/endpoint probability | 100% | 60% | .03052 / [.02847,.03430] |
| Ordered logit（separate latent scale） | 70% | 0% | .08663 / [−.09821,.11578] |
| Ordered probit（separate latent scale） | 80% | 20% | .05992 / [−.04318,.07705] |

Raw-R outcome SD 标准化的 median/range：ordinal .05883 [−.01916,.07807] SD per step；midpoint .07008 [.03512,.09448]；alt-top .07687 [.04644,.10098]。Probability 保留概率单位；ordered latent scales 分开、不混合，也不输出伪“共同标准化”效应。所有份额是重叠数据上的描述性稳定性，不是独立 replication 数或新的假设检验；“CI >0”是 raw 点态标准，不是全 multiverse 的多重校正显著率。

| Sample | Unadjusted ordinal pooled differential [CI] | Unadjusted top probability differential [CI] |
|---|---|---|
| R | .09121 [−.01650,.19892] | .02954 [.01043,.04865] |
| A | .09076 [−.01722,.19874] | .02954 [.01039,.04868] |
| C | .11974 [.00900,.23049] | .03352 [.01370,.05333] |
| Q1 | .03846 [−.12231,.19924] | .02854 [−.00146,.05853] |
| Q2 | −.02869 [−.28115,.22376] | .03179 [−.01573,.07931] |

Top probability 的 Q2 点估计没有消失，但 CI 宽；ordinal Q2 为负、ordered 部分 specs 也负，不能隐藏。Q1 adjusted top OLS nominal CI 刚过零（p=.0466），logit AME 未过（p=.0683），不能只展示这个有利规格。Quality restrictions 改变分析总体且在分配后选定，不是新的“最真实”样本。

## 6. MPC share versus absolute stated spending

Auxiliary `ImpliedAdditionalYuan = midpoint×amount`。这不是 realized spending，也不是不同于 share 的独立确认。全部九格与 derived Restricted 的 bootstrap CI 见表和图 E。

| Form | Midpoint share：200→5,000 | Implied yuan：200→5,000 | Endpoint eta [95% bootstrap CI] |
|---|---|---|---|
| Cash | .2527→.2008 | 50.53→1,004.07 | .9286 [.8880,.9708] |
| Food | .2281→.1947 | 45.61→973.42 | .9509 [.9062,.9944] |
| Medical | .1770→.1792 | 35.40→896.23 | 1.0039 [.9576,1.0518] |
| Restricted | .2025→.1870 | 40.50→934.82 | .9752 [.9437,1.0062] |

Eta=`log(mean implied-yuan_5000/mean implied-yuan_200)/log(25)`：比例恒定对应 1。Food−Cash eta=.02221，CI [−.03974,.08117]；Medical−Cash=.07529，CI [.01385,.13916]；Restricted−Cash=.04653，CI [−.00489,.09778]。依赖 midpoint 权重，是端点 descriptive elasticity，不是个人边际反应或结构参数。

Constant-dollar `K/T` 按三个均值 unweighted least-squares 最优 K：Cash=58.77，预测 200/1,000/5,000 shares=.29384/.05877/.01175，明显不贴合 .25267/.22681/.20081；RMSE=.14796。Food/Medical RMSE=.13800/.12772，完整 fit error 已输出，不作新结构模型或 p-value。**完全固定人民币支出**无法近似这些 midpoint cell means；但更一般的 absolute-yuan thinking、类别尺度理解或 top coding 仍无法排除。降低消费份额绝不意味着绝对消费下降。

## 7. What is supported

- 当前随机九格中的 stated response：Cash 的 top-category probability 随金额下降较强；Food 与 Medical 在这一无条件 margin 上都出现较弱压缩，equal-weight contrast 比单个 restricted form 更清楚。
- 这个 top probability contrast 对 midpoint 赋值没有依赖，logit/probit AME 与未调整 LPM 接近；relative-scale 方向提供有限支持，而不是全面通过 multiplicity 的强验证。
- 只能说差异 **most visible in the upper tail**。同一数据的平均曲线、top-bin shares、非线性 links、specifications 不是多项独立确认。
- Midpoint implied additional yuan 随金额显著增加；比例下降与绝对增量上升可同时成立。Food/Medical 的平均 size slopes仍应分别显示。

## 8. What is not supported

不得在主文称：真正 tail-specific、upper-tail difference 已显著大于 extensive margin；Food/Medical mean curves 等效；受限资源整体没有 amount gradient；headroom/measurement explanation 已排除；ordinal primary 被 pooled 检验强化为确定结果。不能以 nominal relative CI 或 multiverse positive share 替代多重校正与直接对比。

也不得称 realized MPC、welfare、固定个体 fungibility、within-person curve、precautionary-saving mechanism、因果 need matching、可普遍外推的 restriction law。Form 仍捆绑用途、期限、流动性与表述。PR #9 的 inframarginality/need matching 仍是有限 secondary evidence，本轮没有追加任何机制、moderator、HTE、SHAP、cluster 或 latent 搜索。

## 9. Recommended paper architecture

仅建议结果组织，不修改 manuscript：

1. **随机九格与金额尺度**：原始 ordinal 首先展示，midpoint 曲线辅助；明确跨人随机比较和 mean differential 不确定性。
2. **无条件 top-tail response 与 equal-weight Restricted contrast**：Food/Medical 透明显示；top probability robust contrast 是最清楚的窄事实，不宣称 tail specificity。
3. **证据边界**：相对/link尺度、直接 threshold null、有限 specification curve 同时展示，包含不利 Q1/Q2；multinomial 只作辅助 distribution check。
4. **Share vs yuan translation**：用图 E 解释 lower share 并非 lower spending；eta 为同一事实的重新表达，不作为第二套确认。

标题/abstract 的任何强化仍须保持 suggestive 的 empirical scope；不能把 Medical-only mean claim 或统一 restriction mechanism 写成定论。

## 10. Final stop decision

**停止对当前数据的进一步 exploratory analysis。**本轮任务书规定的 pooled contrasts、所有 nonlinear thresholds、relative bootstrap、direct joint-threshold tests、multinomial diagnostic、完整420-spec grid、yuan scaling 与 constant-dollar benchmark 已完成。没有科学理由继续在同一数据中增加 moderators、改 multiplicity family 或寻找替代故事；这些不会提供缺少的独立验证或测量。后续可审阅本次可复现输出及讨论写作，但不追加当前数据的探索。Manuscript 保持未修改。
