# Nature targeted revision: audit

## Scope and fixed baseline

This is the targeted package specified in `NATURE_REVISION_WORK.md`, applied to the existing locked Nature empirical package. It answers only three reviewer-style questions: which broad observable domains carry the limited signal across forms; whether low observed R² could reflect outcome noise; and why learned personalization does not improve the full-sample stated-consumption objective. The original ordinal randomized mean-effect estimand and the midpoint stated-MPC prediction/HTE/policy estimands remain unchanged. `NATURE_EMPIRICAL_RESULTS.md`, its six main figures, and ten Extended Data figures were not overwritten. This is post hoc revision analysis, not new preregistered evidence.

The external source is `G:\桌面\科研\项目-消费调查\社会心态小调研数据(1).dta` (3,010,162 bytes; SHA-256 `16996C88FDD20F5084B62A8503A8EEC1D4C6EC7CAFF489EFF109500F629694FE`). The script imports the frozen `heterogeneity_formal.prep`, `final_exploration` form-specific RF pipeline, and `nature_empirical` global fold/policy definitions. All N=5,497 raw respondents have exactly one valid randomized 3×3 scenario response under the frozen preparation. Adult A, Clean C, Q1, and Q2 retain their existing definitions. The original 1–6 category remains primary for mean effects; midpoint stated MPC is used here only where the locked prediction and policy analyses already used it. No respondent-level data, folds, fitted values, DR scores, or policy assignments are exported.

## A. Predictor-domain map

The 41 locked predictors are partitioned once, with no overlap, into seven broad domains:

| Domain | Fixed variables / allocation decision |
|---|---|
| Resources / socioeconomic position | education, harmonized income, work status, work-unit type, housing. Objective only. |
| Liquidity | Q7 emergency-fund capacity, kept isolated because no close alternate direct liquidity measure is present. |
| Household needs / exposure | children, household size, monthly food-spending band, prior-year out-of-pocket medical-spending band. |
| Expectations / future outlook | own and societal future, economy, jobs, prices, fairness, welfare, expected SES change. Q20 belongs here. |
| Subjective security / pressure | social protection, gain/effort/mobility beliefs, pressure, present and past SES. Q18/Q19 are **not** mixed into objective resources. |
| Broader social attitudes / wellbeing | life satisfaction, safety, fairness, trust, support, voice, order, vitality. |
| Demographics / exposure | age, sex, hukou, city tier, past subsidy receipt. Q31 is an exposure descriptor, not a randomized treatment. |

Domain-drop importance is `R²(ALL) − R²(ALL without domain)`, separately by form, on the frozen midpoint outcome. The RF has 180 trees, minimum leaf 20, and max-features fraction 0.5, with amount as a categorical predictor. Three prespecified seeds (20260921–20260923) generate five global folds stratified by the original nine randomized cells. Arm-specific training uses only the training-fold respondents in that form; all preprocessing is fitted inside the fold. Each domain comparison uses the same held-out respondents and fold partition as ALL. Point estimates average three complete OOF R² differences; seed minima/maxima are shown. Intervals resample respondents 1,000 times within each disjoint form arm while holding all OOF fits fixed. Pairwise context-difference intervals use independent arm resamples and the repeated predictions. They reflect validation-sample uncertainty conditional on these fits, not full training-set uncertainty or independent replication.

The secondary ridge analysis uses the locked common pooled one-hot/standardized encoding and ridge alpha 10 without changing the predictor set. The encoded numeric matrix is held in float32 to limit bootstrap memory copies; displayed coefficients are reported to no more than three decimal places. All 41 raw predictors and encoded columns are exported. A fixed **pooled treatment-blind** top-20 absolute-coefficient display subset is selected before viewing form-specific signs. Three hundred independent-within-arm bootstrap refits provide 2.5th/10th/25th/50th/75th/90th/97.5th distribution percentiles for every form coefficient and every pairwise coefficient difference, plus domain mean-absolute-coefficient percentile summaries. In a regularized high-dimensional fit, some percentile distributions are shifted relative to the full-sample point estimate; these are diagnostic uncertainty summaries, not multiplicity-adjusted per-feature tests. Ridge coefficient magnitude is not directly comparable to RF domain-drop importance. No single-variable significance scan, SHAP, or causal mechanism inference was conducted.

The work file's permutation-importance module is optional. It was not added: the required domain-drop analysis already answers the domain question on held-out data, and an extra correlated-feature rank diagnostic would not clear the two-representation interpretation gate. No incomplete ten-seed permutation ranking is presented as evidence.

## B. Classical measurement-error sensitivity

The outcome was measured only once. Neither test-retest reliability nor a latent true-response R² is identified. Under the explicitly hypothetical classical additive-error assumption, the script computes `R²_observed / rY` on a 0.30–1.00 reliability grid in 0.01 steps for locked RF O, ALL, and paired O+S-minus-O R², transforming the corresponding locked interval endpoints and capping to logical bounds. Q1/Q2/C/R empirical OOF R² values are placed alongside, not used as reliability estimators. Cronbach alpha of subjective predictors is not used as outcome reliability. The sensitivity is neither an empirical upper bound nor a theoretical ceiling on human predictability.

## C. Policy decomposition and RMB 1,000 stress test

The full-sample OOF three-form response predictions are reproduced with the exact locked five-fold form-specific RF procedure. Known randomized form propensity is 1/3 conditional on amount. For each respondent and form, the cross-fitted DR score is `mu_form + I(A=form)*(Y−mu_form)/p`. The ML argmax rule's gain over all Cash is decomposed algebraically into `I(rule=Food)*(DR_Food−DR_Cash)` plus `I(rule=Medical)*(DR_Medical−DR_Cash)`. The two contributions sum exactly to the locked DR policy gain (tolerance <1e-10). Assignment shares, selected-subgroup average DR contrasts, population contributions, and paired 2,000-draw respondent-bootstrap intervals are exported.

Predicted crossing is defined **only** as OOF `mu_Food−mu_Cash>0` or `mu_Medical−mu_Cash>0`. The positive-share is not a fraction of people who truly benefit. DR contrasts within those predicted-positive subgroups validate only the **average** randomized effect for the selected subgroup; individual counterfactual rankings are unobserved. A fixed-bin distribution table underlies the figure.

The exploratory RMB 1,000 stress test restricts to the two randomized Cash/Medical cells (N=1,207). It refits OOF arm-specific response models within that sample, chooses Medical only for predicted positive advantage, and compares the rule to all Cash via cross-fitted DR and IPW scores using two-arm propensity 1/2. The three fixed fold seeds are 20260921–20260923; paired 2,000-draw bootstrap intervals are computed per seed. This is an amount-restricted sensitivity, **not** a replacement global policy estimand, an optimal-amount search, or a welfare calculation.

## D. Composition robustness and export discipline

Five broad predefined binary splits use age <35, education >=3 (college-plus coding), harmonized income >=4, non-agricultural hukou code 2, and city tier <=2. Within each half, the supplementary table reports N, minimum form N, unadjusted ordinal Food−Cash and Medical−Cash differences with Welch-style normal intervals, and ALL RF OOF R² only when N>=800 and every randomized cell has at least 30 observations. These are overlapping, non-independent sample descriptors, not population-transport estimates. No census propensity weighting or claim of national representativeness is made.

`analysis/nature_revision.py` writes only aggregate CSVs. `analysis/nature_revision_figures.py` makes four **candidate** figure pairs in vector PDF and 600-dpi PNG, plus exact panel source CSVs. Their legends are in `figures/nature_revision_figure_legends.md`. Figure importance and ridge maps are explicitly labelled predictive/non-causal; reliability scenarios are explicitly assumed; policy panels state the hypothetical outcome and no welfare inference. The existing locked figure portfolio is unchanged.

## Reproducibility checks and residual limits

- The final revision script was run twice with independent output directories, one of them the repository deliverable directory. All 15 aggregate CSVs have identical schema and nonnumeric fields; the maximum numeric difference is 4.00×10⁻¹⁶. All four 600-dpi PNGs are byte-identical. Python compilation and PDF-render/figure checks were also performed.
- The full-sample DR policy decomposition reproduces the locked `ml_argmax` gain to machine precision.
- No analysis uses post-assignment outcomes as predictors of held-out cases; bootstrap validation does not refit RF models, so its intervals are conditional on fitted OOF models.
- Domains are broad and correlated. Removing a domain changes the fitted representation of other domains; the resulting ΔR² is not a unique variance partition or causal attribution.
- Outcome reliability, realized spending, repeated within-person contexts, true individual treatment rankings, and a compatible national sampling frame remain unobserved.
