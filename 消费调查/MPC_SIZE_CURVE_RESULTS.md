# MPC size-curve story discovery results

日期：2026-10-02。任务书：`MPC_SIZE_CURVE_WORK.md`。本轮仅使用原始调查数据重估规定的曲线、分布和小规模理论检验；未修改 manuscript。完整汇总、脚本和图见 `results/mpc_size_curve/`。

### 1. Executive finding

**Headline survives as suggestive evidence, not a strong paper-organizing result.** Cash 的 stated MPC 随金额下降，Medical 的平均反应变化较小，Medical−Cash differential amount slope 在 R/A/C、序数/midpoint/alternative-top 编码中方向一致，且两段相邻金额的差异方向一致。不过，首要的 raw/unadjusted ordinal 五项主检验中，该 differential 的 Holm p=0.0778，ordered logit/probit 也未通过各自五项校正；除最高档外，多数 threshold differential 不够精确。Q1 缩小、Q2 序数差异接近零。最清楚的分布事实是 Cash 最高 stated MPC 档明显减少，而“任何额外消费”概率基本不变。没有把 Medical 不显著的自身斜率称为精确平坦，也没有用机制检验补救主检验的不足。

### 2. The 3×3 fact

5,497 名受访者各回答一个随机情景，不是同一个人的三条曲线。复现 PR #3 的九格均值，沿用 PR #8 的一次测量识别限制；没有重跑全部基础随机化/预测审计。

| Form | N：200 / 1,000 / 5,000 | Ordinal：200 → 1,000 → 5,000 | Midpoint stated MPC |
|---|---|---|---|
| Cash | 619 / 595 / 584 | 2.934 → 2.803 → 2.702 | .2527 → .2268 → .2008 |
| Food | 614 / 620 / 602 | 2.785 → 2.669 → 2.628 | .2281 → .2009 → .1947 |
| Medical | 615 / 612 / 636 | 2.462 → 2.531 → 2.520 | .1770 → .1786 → .1792 |

Cash 两段都下降；Food 的下降主要在第一段；Medical 序数小幅先升后降，midpoint 小幅上升。图 1 展示未经模型平滑的格均值和点态 95% CI，不把三点外推成连续剂量反应。

### 3. Formal amount-slope tests

主模型 `Y ~ form*z`，`z=(-1,0,1)`；每单位是金额增加五倍，等价于 centered log(amount)/log(5)，不是增加一元。下表为 R、unadjusted、HC3；CI 未作多重校正。五项主 family 按任务书固定，Medical−Food 为 secondary。

| Ordinal estimand | Slope | SE | 95% CI | Raw p | Holm p |
|---|---:|---:|---|---:|---:|
| Cash | −.1160 | .0454 | [−.2050, −.0270] | .0106 | .0530 |
| Food | −.0787 | .0452 | [−.1673, .0099] | .0818 | .2454 |
| Medical | .0291 | .0424 | [−.0540, .1122] | .4922 | .9844 |
| Food−Cash | .0373 | .0641 | [−.0882, .1629] | .5602 | .9844 |
| Medical−Cash | .1451 | .0621 | [.0234, .2668] | .0195 | .0778 |
| Medical−Food | .1078 | .0620 | [−.0137, .2292] | .0820 | — |

| Midpoint estimand | Slope | SE | 95% CI | Raw p | Holm p |
|---|---:|---:|---|---:|---:|
| Cash | −.02593 | .00775 | [−.04112, −.01074] | .00082 | .00411 |
| Food | −.01672 | .00764 | [−.03168, −.00175] | .02854 | .08563 |
| Medical | .00112 | .00676 | [−.01212, .01437] | .86789 | .86789 |
| Food−Cash | .00921 | .01088 | [−.01212, .03053] | .39745 | .79490 |
| Medical−Cash | .02705 | .01028 | [.00690, .04720] | .00852 | .03409 |
| Medical−Food | .01784 | .01020 | [−.00214, .03783] | .08013 | — |

Top-bin=1.0 下 Medical−Cash=.03091，CI [.00884,.05299]，Holm p=.02425。Ordered logit differential=.1511，CI [.0085,.2938]，raw/Holm p=.0378/.1892；ordered probit=.0940，CI [.0097,.1783]，p=.0289/.1156。Ordered 模型采用显式 HC1 score-Hessian sandwich。它们是各自 latent-index 单位，不能与 ordinal/midpoint 的效应量直接相减，也未建立 proportional-odds 假设。

序数 structured 2-df form×trend Wald p=.0498，而 unrestricted 4-df p=.1670，复现旧 omnibus 的弱证据；不能把检验方向预设为一次 preregistered confirmatory discovery。Midpoint 对应 p=.0251/.0954。

非参数相邻检查：Medical−Cash ordinal differential changes 为 .1997（200→1,000，CI [−.0492,.4485]）和 .0907（1,000→5,000，CI [−.1473,.3287]）；midpoint 为 .02746 和 .02664，两段 CI 都跨零。全程 midpoint differential change=.05411，CI [.01386,.09436]。不是只有一个金额格方向异常，但两段分别不足以确立相同的非零差异。

另对 ordinal/midpoint 各做 5,000 次 conditional amount-label permutation，保留每个 form 内三格人数。所有 form-specific 和 pairwise slope 均输出，含五项 Holm。**这些 p 检验 involved forms 没有任何 amount effect 的 sharp null，不检验允许共同非零斜率的 slope-equality null。** Differential equality 的主要推断仍是上述 robust contrast，不能用 permutation p 替换它或挽救 Holm 结果。见 `randomization_inference.csv`。

### 4. Distribution anatomy

Cash floor share 27.30%→27.23%，any-spending slope=.00025，CI [−.02495,.02546]，不是 extensive-margin 下降。其 top category 从 13.41%→8.91%→5.31%，下降 8.10 percentage points；中间第二/第三档分别增加 2.45/4.13 pp，第五档增加 1.84 pp。不能从独立样本的概率变化声称同一人从某档迁移到另一档。

Cash midpoint 总变化 −.05185：top-bin mass 的贡献 −.07088，被第二、第三、第五档的 +.00123、+.00723、+.01151 等部分抵消。这是概率加权恒等式，不是结构性/个体行为分解。Food 总变化 −.03337；最高档、第四档贡献 −.02152、−.01442。Medical 总变化 +.00225，却有第三/第五档贡献 +.00856/+.01065、最高档贡献 −.01687 的抵消；Medical 的平均值稳定不等于整个分布不变。

| Threshold | Cash slope | Medical slope | Medical−Cash slope | Differential raw / Holm p |
|---|---:|---:|---:|---|
| Any spending | .00025 | .01559 | .01533 | .4141 / 1.0000 |
| ≥10% | −.01202 | .02430 | .03632 | .0713 / .3567 |
| ≥25% | −.03244 | −.00006 | .03238 | .0726 / .2177 |
| ≥50% | −.03125 | −.00108 | .03017 | .0279 / .1114 |
| >75% / top category | −.04055 | −.00965 | .03090 | .0029 / .0116 |

Threshold Holm 为每个编码内同一五项 family，不是跨全部 threshold 的校正；threshold 整体为辅助分布证据。差异最清楚地集中在 top category，不能泛称五个 margin 都已验证。九格完整 p1–p6/CDF、五项 complementary probabilities、斜率和分解见对应 CSV、图 2/3。

### 5. Food inframarginality

沿用食品月支出类别的保守上下界乘六，不给 open-ended 类别赋精确支出。`strict_assigned` 是六个月 lower bound > assigned amount（Cash/Food 同规则），N=3,262；用 saturated form×amount 模型对三个金额等权 pooled，Food−Cash ordinal=−.1212，CI [−.2292,−.0132]，p=.0279；midpoint=−.01990，CI [−.03828,−.00153]，p=.0338。Clean 对应 N=3,071，ordinal=−.1226，p=.0309；alternative-top 也同向。均为未校正 secondary p。

重要限制：assigned screen 会随随机金额改变入选人群，因此它的跨金额 slope 不是固定总体的随机剂量效应。额外使用 **lower6 > 5,000 的共同样本**，使三种金额下 eligibility 相同：N=2,815；Food−Cash pooled ordinal=−.1090，CI [−.2248,.0069]，p=.0652；midpoint=−.01857，CI [−.03838,.00124]，p=.0662。共同样本 clean N=2,650，ordinal p=.0550。方向稳定、精度有限，不能称严格条件下强力拒绝 cash equivalence。

共同样本 Cash/Food midpoint slopes=−.01945/−.02563；Food−Cash differential=−.00617，CI [−.03093,.01859]。Assigned strict differential=.00212，CI [−.02105,.02529]。没有证据确立 Food 与 Cash 曲线相同，也没有证据确立其不同。Upper-bound likely-binding 只有 56 人，全部在 5,000 元；无法识别它的跨金额斜率，代码不输出伪斜率。移除这 56 人后 differential=.00746，仍接近 full-sample .00921，因此 Food 曲线不是仅靠这极小组产生。

结论：Food 低于 Cash 的 secondary level pattern 有一致方向，但固定共同样本的不确定性阻止将其作为已经证明的强第二层。它不证明 mental accounting。

### 6. Medical need matching

Q30 过去一年自费医疗支出 **类别 rank** 在 R 中标准化，不是人民币线性剂量，也不是长期账户的严格 bindingness。图示分组预先取 low=0–500、middle=501–5,000、high>5,000。模型含 form×z×need 的全部 lower-order terms。

R ordinal Medical×need=.1176 per SD，CI [.0126,.2226]，p=.0281；C=.1299，CI [.0212,.2386]，p=.0192：higher need 与中心金额下 Medical−Cash gap 较小相一致。Midpoint=.01514，CI [−.00264,.03292]，p=.0952；C p=.0805。不能将 ordinal 的 nominal significance 升格为已验证的 causal matching mechanism。

Medical×z×need ordinal=.00431，CI [−.12607,.13469]，p=.9484；C=.01988，p=.7756。Midpoint=.00560，CI [−.01647,.02767]，p=.6188。Need 模型中的中心差异斜率仍 ordinal=.13485、midpoint=.02532；没有证据表明 need 已解释 Medical−Cash size-gradient difference。高 need 分组较小、CI 较宽，组内视觉起伏不作为 subgroup 发现。

跨领域比较：Food×food-spending ordinal=−.0107，CI [−.1170,.0956]，p=.8435；C=−.0063，p=.9115。Food 三重交互也不精确。Medical 的方向不能推广为共同 Food/Medical “matching law”，更不能合成 fungibility index。

### 7. Classic MPC determinants

仅使用 Q7 应急筹资、harmonized income rank、食品/医疗支出和 prior subsidy experience。Q7 是主观筹资能力，不是观测现金余额。Cash z×liquidity ordinal=.02166，CI [−.03364,.07697]：方向对应更强筹资能力者的负斜率略缓，但不能确立这种差异。Medical−Cash slope×liquidity=.03439，CI [−.10171,.17049]；slope×income=.02456，CI [−.10866,.15778]。这些 null 是不精确的，不是等效性结论。

联合 theory block 加四个经济变量的完整 form×z 交互和 prior subsidy 因子。Medical−Cash at R mean covariates：ordinal=.13619，CI [.01593,.25646]，raw/Holm p=.0264/.1058；midpoint=.02540，CI [.00543,.04538]，p=.0127/.0508。与未调整的 .14510/.02705 接近；标准变量没有消除点估计，也没有改善为强 primary evidence。Prior subsidy 在该模型中作为分类 level control，不做新 moderator catalogue。

M1 additive→M2 form curves 的 ordinal OOF R² .00617→.00663，midpoint .00622→.00680，改善很小；M3 .04220/.03649。Ordinal AIC 20,357.58→20,355.68→20,141.04；BIC 20,384.03→20,395.35→20,352.63。AIC/BIC 对增设两条 curve 的支持不同，不能用样本内拟合替代 differential inference。5-fold cell-stratified folds 在所有三个模型之间相同。

### 8. ML diagnostic

只用相同经济变量与 randomized form/z，固定 depth=3、minimum leaf=150 的 shallow regression tree；三个 split seeds、每个五折，没有调参或 SHAP。15 个训练折均首先在 food-spending rank 分裂，不是 form/amount；OOF midpoint MSE=.06486/.06500/.06557。Full-fit average standardized surface 将 Cash/Food 预测为 .21064、Medical=.19185，三个金额不区分；该树没有重现 amount gradient。

这意味着弱曲线信号不足以进入这个保守树，而不是新证据证明 amount 没有效果；也不是 flexible model 支持本轮故事。没有发现可用的相反 nonlinear 曲线，更未借机增加深度/变量来追求支持。原始九格与 formal contrasts 为结论依据。

### 9. Robustness and measurement threats

| Sample | N | Unadjusted ordinal Medical−Cash slope [95% CI] | Holm p | Midpoint slope |
|---|---:|---|---:|---:|
| R | 5,497 | .1451 [.0234,.2668] | .0778 | .02705 |
| A | 5,480 | .1416 [.0197,.2635] | .0912 | .02626 |
| C | 5,171 | .1766 [.0513,.3019] | .0286 | .03262 |
| Q1 | 2,715 | .0815 [−.0976,.2605] | 1.0000 | .01957 |
| Q2 | 1,208 | −.0008 [−.2864,.2849] | 1.0000 | .01532 |

R precision-adjusted ordinal=.1598，CI [.0395,.2802]，Holm p=.0452；A=.1567，C=.1865。采用既有 objective+needs controls（年龄及平方，其余分类）；不是显著性筛选，也不能用 adjusted/C 显著性取代 raw unadjusted priority。Q1/Q2 不仅 CI 变宽，点估计也变小；Q2 ordinal 近零不能隐去。Quality restrictions 是随机分配后分析选择的筛选，可能改变 population/composition，不证明在“更真实”总体中效果消失。C 也只能作为 sensitivity。

核心测量威胁：hypothetical stated response、六档、floor、top coding；不是 realized marginal consumption，也不是政策刺激量。比例下降可能来自受访者用绝对人民币预算思考：Cash 200→5,000 的 midpoint implied stated additional yuan 约 50.5→1,004.1，比例下降不等于绝对消费下降。Medical 约35.4→896.2；这些是 midpoint proxy，不是真实花费。最高档压缩可由 scale/absolute-yuan response 产生；当前没有连续金额作答或实际行为可排除它。

形式还捆绑期限、用途、流动性与表述，不能把所有差异归因于“earmarking”一个属性。当前样本没有加代表性权重，未证明总体外推。均值、阈值与相邻检验并非独立复制；多次编码和筛选不能当多组独立显著证据。

### 10. Strongest surprising facts

最清楚的新细化事实是 **Cash 的 size gradient 主要是无条件 upper-tail compression，而非更多人选择完全不增加消费**。Medical top-bin shrinkage 较弱，top-threshold slope difference=.03090 per fivefold increase，CI [.01057,.05122]；这让均值曲线有明确的分布来源，而不只是三条画线。Medical−Cash 在两个相邻区间 midpoint difference 均约 +.027，方向一致但单段尚不精确。Medical 均值几乎不动的同时其分布有抵消变化，排除了“均值不变就是全分布不变”的叙述。

### 11. Facts that are expected / already known

Cash/Food/Medical 格均值与九格人数已在 PR #3 中出现，本轮没有将重复 first look 作为新发现。每人只有一次 MPC 测量、不能识别 stable individual fungibility trait，沿用 PR #8。Cash 较大金额对应较低 stated spending share 与经典候选机制相容；仅有这个主效应不够构成 transfer-design 新贡献。过去支出与 Medical level relevance 的正方向并不新奇，也不识别机制。

### 12. Candidate mechanisms

候选仅保留三类：restricted/long-lived medical wealth 改变当前可支配资源解释；用途/期限/标签改变心理预算；按绝对金额而不是比例回答的 scale effect。Medical need 有弱 level-matching 信号，却没有 need×size 的证据；Food 方向一致的 inframarginal level gap 也只排查简单预算集解释，不能在期限、领取/使用摩擦和心理账户之间选择。没有直接测 precautionary saving、实际储蓄、现金等价或福利，故本轮不作确定机制归因。

### 13. Stories killed by the data

不支持把 Medical 精确平坦、分布 invariant 或它“导致 precautionary saving”写成结论；没有 equivalence test 或机制处理。Food/Medical 两类统一 need-matching law 不获支持。Food−Cash curve equality 与 inequality 都没有精确验证。保守树自动发现同一 size curve 的故事失败。Stable individual fungibility/within-person remapping 不可识别，不能重新引入；realized MPC/welfare/普遍行为法则均超出设计。最强的 universal, robust-to-all-quality-screens size-curve claim 也不获本轮支持，但不应因此声称 raw average differential 等于零。

### 14. Nature Communications story decision

**interesting but still underpowered / suggestive**。保留为值得审视的 reduced-form candidate，不能现在把它锁定为强 Nature Communications paper story。理由是方向与经济尺度在主要样本/编码一致、two-step pattern 与 tail anatomy 可解释、标准 theory block 不消除点估计；反面是 ordinal primary Holm 不过线、ordered models 的 family-corrected证据弱、多数 threshold differential 不精确、Q2 点估计消失、fixed-inframarginal 第二层有限、ML 不验证曲线，且比例尺度与捆绑设计仍是替代解释。所有 prescribed analysis 到此结束；不继续 moderator 搜索，不修改 manuscript，不把一个辅助 top-threshold 检验升级为普适 MPC 定律。
