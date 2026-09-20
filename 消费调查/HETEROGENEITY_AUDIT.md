# 消费调查异质性分析审计

## 1 范围和 estimand 纪律

本轮严格执行 `HETEROGENEITY_WORK.md`，使用与 `DATA_AUDIT.md`、`FIRST_LOOK.md` 相同的交付数据和 questionnaire-verified treatment mapping。原始 respondent-level 数据没有写入仓库。

分析严格区分三类对象：

1. **Stated MPC level heterogeneity**：baseline X 与 `E[Y|X]` 的相关性；没有把 X 的系数解释为因果作用。
2. **Randomized treatment-effect heterogeneity**：baseline X 是否改变随机 transfer type/amount 的 conditional treatment contrast。由于 treatment 随机，conditional contrast 有因果解释空间，但 X 本身不是随机变量。
3. **Fungibility heterogeneity**：`food-cash`、`medical-cash`、`restricted-cash` 的 conditional average treatment effects；没有构造不可观察的个体级 gap。另保留 `medical-food` 作为 transfer-form HTE，而不把它称为 cash fungibility gap。

## 2 样本和 outcomes

- Raw sample：N=5,497。
- Clean candidate：N=5,171；沿用首轮审计规则，排除 Q1–Q13 全同值、年龄不在 18–100、重复 ID 或 assignment 异常。原始数据未删除或覆盖。
- Primary outcome：`outcome_ord`，原始 1–6 档。
- Secondary：`mpc_midpoint`（0, .05, .175, .375, .625, .875）与 `mpc_alt`（最后一档改为 1.0）。
- Threshold robustness：`any_spend`、`mpc_10plus`、`mpc_25plus`、`high_mpc`。

Headline HTE 必须先在 `outcome_ord` 上出现；midpoint 与 threshold 只用于量级、ML 和 robustness。

## 3 变量 inventory 和 transformations

`tables/heterogeneity_variable_map.csv` 记录 41 个 pre-treatment variables 的题号、concept、domain、type、missingness、coding、transformation 和用途。

| Domain | 主要内容 | 数量 |
|---|---|---:|
| Objective conditions | 年龄、性别、教育、收入、户籍、就业、单位、住房、既往补贴、城市级别 | 10 |
| Baseline needs | 子女、家庭人数、食品支出、医疗支出 | 4 |
| Subjective economic state | Q6、Q7、Q9–11、Q13、Q15、Q17 经济/就业/价格/福利、Q18–20 | 14 |
| Broader attitudes | 生活满意度、安全、公平、信任、支持、voice、国家前景、秩序、活力 | 13 |

连续和 ordinal 变量保留原编码，并为 interaction 生成 z-score。Q46 的旧码 11–16 先按交付说明归并为 1–6。Categorical variables 在 ML 中 one-hot；在统一单变量线性 scan 中的 z-score coefficient 只是 code trend，分类变量的精细含义不靠该 coefficient 单独下结论。Province 因类别多且可能稀疏，没有进入 HTE feature set；city tier 进入。

数据没有 item missing。ML pipeline 仍在训练折内部定义 median/mode imputation，以防未来数据版本出现缺失并避免 leakage。

## 4 Descriptive first pass

在复杂模型前，对 income、Q7、Q6、Q15、Q17 employment/income、subjective SES、food spending、medical spending、age、education 做 tercile/合理分组，分别输出 cash/food/medical mean、SE、95% CI、N，以及 food-cash、medical-cash conditional contrasts。完整结果见：

- `tables/heterogeneity_descriptive_levels.csv`
- `tables/heterogeneity_descriptive_gaps.csv`

## 5 Theory-guided models

### 5.1 One-variable-at-a-time

对每个 X、raw/clean、七类 outcome，估计：

`Y ~ transfer_type × amount + X + transfer_type × X + amount × X`

统一提取：

- level association；
- food-cash HTE；
- medical-cash HTE；
- restricted-cash HTE；
- medical-food HTE。

报告 effect、robust SE、95% CI、raw p 和 primary family q。完整网格共 2,870 行，保存在 `tables/heterogeneity_theory_scan.csv`。另在每个金额子样本中估计 amount-specific contrasts，见 `heterogeneity_amount_specific.csv`。

### 5.2 Multiple testing

Primary FDR family 定义为：同一 estimand 内的 objective、baseline needs、subjective economic、broader attitudes 四类变量；amount-specific scan 另按 family × contrast × amount 校正。Benjamini–Hochberg q-value 只写入 raw `outcome_ord` primary rows，避免把 secondary outcomes 当作独立发现池。

### 5.3 Domain models

预先定义 E1 objective resources、E2 liquidity/resilience、E3 expectations、E4 protection/precaution、E5 baseline needs、S1 broader attitudes 与 ALL。每个 block 同时进入 level、type interaction 与 amount interaction；报告 in-sample R²、adjusted R² 和 type-interaction joint Wald test，见 `heterogeneity_domain_models.csv`。

### 5.4 Regularized interactions

Full design 包含 type、amount、41 个 X、type×X 与 amount×X。Ridge、lasso、elastic net 采用 outer repeated 5-fold CV；lasso/elastic net 的 penalty 在训练折内部 5-fold 选择。Regularized coefficient 只用于稳定筛查，不附 naive classical p-value。结果见 `heterogeneity_regularized_cv.csv` 和 `heterogeneity_regularized_coefficients.csv`。

## 6 Ordered-outcome robustness

对 theory scan 中靠前的 variables 估计 proportional-odds ordered logit，提取 food-cash、medical-cash 和 medical-food interaction 的 latent-index sign、CI 与 p。核心 medical-food 结果的 sign 与线性 ordinal score 一致。

当前工具链没有单独的 Brant test；因此没有声称比例优势假设已被验证。七种 level/threshold outcomes 提供一个更直接的 practical stress test：若结果只在一个阈值出现，即标为 fragile。结果见 `heterogeneity_ordered_checks.csv` 与 `heterogeneity_robustness_grid.csv`。

## 7 ML prediction of stated MPC level

Feature sets：O、S、A、ALL，并额外比较 O+S 与 O+A。模型：ridge、random forest、HistGradientBoosting；评估使用 repeated 5-fold CV 的 out-of-sample R²/RMSE。Permutation importance 和 PDP 来自固定 70/30 honest holdout 的 ALL HistGradientBoosting，仅作预测解释，不作因果机制解释。

## 8 Honest / cross-fitted HTE

分别分析 food vs cash、medical vs cash、restricted vs cash：

- 5-fold stratified cross-fitting；每个 observation 的 CATE prediction 仅来自未使用其 outcome 的训练折。
- 主 learner：random-forest T-learner。
- Robustness learner：内部 3-fold nuisance cross-fitting 的 DR pseudo-outcome，再以 random forest 学习 CATE。
- Propensity 使用 contrast 样本中的随机分配比例，不额外拟合 propensity。
- Honest evaluation：按 out-of-fold predicted CATE 分 quintile，在 held-out observations 中重新估计实际 randomized contrast、CI 和 treatment balance。
- BLP calibration：在 out-of-fold prediction 上估计 treatment × centered predicted CATE slope。

比 variable importance 更重视 held-out quintile contrast 和 BLP calibration。ML importance 是 model-based importance，不是机制证据。

## 9 Food inframarginal analysis

沿用六个月食品支出 interval bounds，保留 definitely inframarginal / ambiguous / likely binding。只在 clearly inframarginal 样本中重复 income、Q7、subjective SES、household size、children、food spending、Q15、Q17 employment/income 的核心 food-cash HTE scan；不在极小的 likely-binding group 挖掘。

## 10 已知限制

- Outcome 是 hypothetical stated MPC，不是 realized spending。
- CATE 是 conditional average effect；个体潜在结果不可同时观察。
- Baseline X 的 association/interaction 不表示 X 本身有因果作用。
- ML importance 不是 causal mechanism。
- Fungibility 指 transfer-form consumption-response equivalence，不是 WTP、utility 或 welfare valuation。
- 没有支出明细，不能分析 expenditure composition。
- 平台样本年轻、高学历，外部有效性有限。
- 单变量分类 code trend、proportional-odds assumption、amount-specific family 数量和 ML learner choice 都是需要保留的模型限制。
