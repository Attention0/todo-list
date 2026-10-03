# 消费调查第二轮正式异质性审计

## 1. 分析对象与样本

本轮严格执行 `HETEROGENEITY_ROBUSTNESS_WORK.md`。原始 `.dta` 仅作为只读输入，仓库只保存代码、汇总表和图，不保存 respondent-level 数据或 OOF prediction。

- Sample R：5,497，所有人均恰有一个 Q32–Q40 response。
- Sample A：5,480，仅限制年龄 18–100。
- Sample C：5,171，沿用既定 age、Q1–Q13 straight-line、duplicate/assignment 规则。

脚本每次运行均重新构造 3×3 treatment，并与 `scen_type`、`scen_amount`、`scen_mpc` 逐行核对；零/多 assignment、metadata 不一致或 outcome 超出 1–6 时立即中止。

## 2. Outcome 与 estimand

- Primary：`outcome_ord`，1–6 档 hypothetical stated incremental-consumption response。
- Auxiliary：midpoint MPC（0, .05, .175, .375, .625, .875）及 top category=1 的 alternative coding。
- Threshold：any spend、10%+、25%+、50%+。

严格区分：stated-MPC level association、随机 transfer-form HTE、Food−Cash/Medical−Cash fungibility HTE，以及非 fungibility estimand 的 Medical−Food HTE。没有构造个体层面的 observed gap。

## 3. 第一轮 specification 修正

41 个 baseline variables 固定分为：

- continuous / approximately continuous：28 个，主规格为 centered z trend；
- ordered categories：6 个，trend 与 factor/dummy 两种规格并列；
- nominal categories：7 个，只以 factor/dummy 进入，HTE 用所有 `Type×C(X)` 的 joint Wald test。

`formal_variable_map.csv` 给出完整分类。就业、单位、户籍、住房、补贴、性别和子女变量不再按数字标签 z-score 后解释为经济斜率。

## 4. 回归规格

Reduced form：

`Y ~ C(Type) * C(Amount)`。

Continuous / ordered trend pooled HTE：

`Y ~ C(Type)*C(Amount) + Xz + C(Type):Xz + C(Amount):Xz`。

候选结果的饱和模型：

`Y ~ C(Type)*C(Amount)*Xz`。

Categorical HTE：

`Y ~ C(Type)*C(Amount) + C(X) + C(Type):C(X) + C(Amount):C(X)`，先报告 omnibus Wald test。

Primary 不加 controls 或 geographic FE。Prespecified precision controls 固定为 age+age²、gender、education、income、hukou、employment、housing、minor child、household size、food/medical spending、prior subsidy、city tier；focal X 的重复版本被剔除。Controls/FE 仅用于精度和稳健性，不用于识别随机处理效应。

## 5. 标准误、固定效应与 geography

- Primary：HC1；robustness：HC3。
- Top medical-food findings：province- and city-clustered SE。
- FE：province FE 与 city-tier FE；未强行使用 city FE。

数据有 32 个 province clusters，median N=133；295 个 city clusters，median N=7、min N=1，仅 23.1% 城市含全九格。City FE 因严重稀疏未进入正式 top specifications。Province cluster 数约 30，cluster结果仅作稳健性，不替代 individual-randomization inference。

## 6. 随机化推断与多重检验

Income、education、medical spending 的 Medical−Food pooled HTE 固定 X，置换完整 treatment-cell labels 并保持九格观测数，共 2,000 次，报告双侧 randomization p。没有实现 max-|t| family correction，属于协议偏离；classical family BH-FDR 仍按 objective、needs、subjective、attitudes × estimand 固定计算，secondary outcomes 不进入 primary family。

## 7. Stated-MPC 可预测性

固定模型 T、O、S、A、O+S、O+A、ALL 均正确 dummy-code categories，并加入 treatment design。报告 in-sample R²、adjusted R²、同一 10-fold CV，以及同一 2×5-fold outer folds 下的 ridge、elastic net、random forest、histogram gradient boosting。

Penalized/tuned models 使用训练折内 5-fold tuning；imputation、standardization、one-hot 全部在 pipeline 内。为控制运行成本，使用紧凑预设网格：ridge alpha={.1,1,10,100}；elastic-net alpha={.001,.01}, l1={.1,.7}；RF max_features={.5,1}；HGB leaves={15,31}, L2=3。未增加 XGBoost/LightGBM/CatBoost。

Permutation importance 与 PDP 使用固定 70/30 holdout 上的 ALL random forest，仅解释预测，不解释机制。

## 8. Honest HTE

Food−Cash、Medical−Cash、Medical−Food 分别使用：

- RF T-learner benchmark；
- DR learner；
- R-learner style residual-on-residual learner。

所有 CATE prediction 均为 OOF；5 folds 按原始 form×amount cell 分层。Amount dummies 进入 nuisance/learner，使 amount 不成为隐藏 HTE 来源。Propensity 使用 pairwise randomized sample proportion，不拟合复杂 propensity。

验证报告 BLP calibration、OOF CATE quintiles、top-minus-bottom、每组 treated/control N 与 CI。未安装 `econml`/GRF，因此没有专门 causal forest；R/DR learner 是本轮 principled alternatives。RATE/AUTOC 未实现，属于协议偏离。

## 9. Food null 与 ordinal robustness

Food analysis 使用六个月 food-spending interval lower bound，构造 strict 和 transfer≤lower-bound×50% 的 very-strict inframarginal samples。对预设八个 traits 报告 interaction CI、BH q 和 95% CI half-width；不把 non-significance 等同于证明完全同质。

Top Medical−Food variables同时估计 ordered logit、ordered probit 与四个 threshold LPM。Ordered latent-index coefficient 只用于方向检查。

## 10. 可复现交付

- `analysis/heterogeneity_formal.py`
- `tables/formal_*.csv`
- `figures/formal_*.png`

第一轮 `heterogeneity_*` 文件均保留，没有覆盖。
