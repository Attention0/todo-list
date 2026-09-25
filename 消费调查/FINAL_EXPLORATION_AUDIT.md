# Final Exploration Audit

## Scope and estimands

This final exploratory pass asks whether heterogeneity in the hypothetical incremental-consumption response is a stable observable trait or is specific to transfer form. It preserves the Raw R (N=5,497), Adult A, and Clean C definitions, coding, outcome hierarchy, and inference rules in the prior formal audit. New estimands are: form-specific out-of-sample outcome prediction; cross-form rank transfer and coefficient alignment; cross-fitted shared and form-specific predicted variance; held-out incremental prediction from subjective blocks and latent dimensions; pairwise conditional randomized treatment-effect heterogeneity for Food−Cash, Medical−Cash, and Medical−Food; amount-specific HTE; and honest policy value relative to the best uniform form.

No respondent-level records, factor scores, fold assignments, or OOF predictions are committed. All `final_*.csv` files are aggregate results.

## Transformations and prediction

The analysis uses the frozen preparation function in `analysis/heterogeneity_formal.py`. Amount is included in outcome models. Nominal and ordered variables use the prior coding; missingness is handled inside fold-specific preprocessing. Separate Cash, Food, and Medical models use identical feature definitions and repeated five-fold splits. Ridge, elastic net, random forest, and histogram gradient boosting report fold-level R², RMSE, and MAE. Cross-form transfer trains a random forest in one form, predicts another without refitting, and allows only mean recentering. Ridge coefficient vectors are compared after common standardized encoding using correlation, cosine similarity, sign agreement, and 300 respondent bootstrap resamples.

The shared-versus-specific decomposition uses global five-fold OOF form-specific predictions. For each respondent it constructs `G=(mu_cash+mu_food+mu_medical)/3` and deviations `D_t=mu_t-G`; only aggregate variances are exported.

## Cross-fitting and HTE implementation

Outer five-fold splits are stratified by original form×amount cells. Propensity is the known empirical randomization probability conditional on amount within each pairwise contrast. The T learner fits treatment-specific random forests in each outer training fold.

The DR learner makes three nuisance folds inside every outer training fold. Treatment-specific outcome nuisances are histogram gradient boosting models; every training observation's DR pseudo-outcome uses nuisance predictions from a model that did not use that observation's outcome. A random forest then learns the pseudo-outcome and predicts the untouched outer fold.

The R learner cross-fits `m(X,A)=E[Y|X,A]` without treatment as a direct regressor, forms Robinson residuals `Y-m` and `W-e(A)`, and fits a random forest to `(Y-m)/(W-e)` with weights `(W-e)^2`; it predicts only the outer held-out fold. Evidence is reported as held-out BLP calibration and observed top-minus-bottom CATE-quintile separation, before any feature interpretation. A reliable causal-forest package was unavailable; no fragile dependency was installed.

## Nested prediction, outcome representation, and psychometrics

Fixed folds from the formal RF exercise compare O with O+S, O+A, and ALL. Paired fold differences use 10,000 fold-resampling bootstrap draws and practical-equivalence thresholds of +0.01 and +0.02 OOS R². Ridge sensitivity covers ordinal code, primary and alternative midpoint mappings, and four threshold outcomes.

Subjective items were assigned before association testing to three conceptual domains: subjective economic state (14 items), social confidence/institutional-social environment (11), and wellbeing/optimism (5). Standardization and PCA loadings were estimated on a seeded discovery half; fixed loadings score the held-out half. Components with eigenvalue >1 were retained, capped at three; each domain retained one component. Loadings, explained variance, and Cronbach alpha are reported. The domains are not asserted to be orthogonal, and conceptually overlapping outlook items make their labels descriptive rather than validated psychological mechanisms. Exploratory factor analysis and respondent clustering were not added: PCA already produced strong single factors, while the optional clustering exercise would introduce a post-hoc profile search without independent validation.

## Policy evaluation

Uniform Cash, Food, and Medical policies, a depth-2 interpretable tree, and an ML argmax policy are compared. Form-specific potential-outcome predictions and policy assignments are OOF. Policy values use IPW with known one-third assignment probabilities and 3,000 respondent bootstrap draws. The policy tree is learned only on other folds. A separate DR policy value was not implemented; therefore policy conclusions rely on randomized-design IPW, not agreement between IPW and DR.

## Response quality and generalizability

Pre-treatment 0–10 items yield within-person SD, extreme share, midpoint share, unique response count, and entropy. Q1 requires Adult A, SD≥1, and at least four unique values; Q2 requires SD≥1.5, at least five unique values, and extreme share≤0.8. These are sensitivity screens, not primary exclusions. The data contain no duration, IP/device information, formal attention checks, or defensible reverse-coded consistency test.

Internal composition covers age, sex, education, hukou, employment, city tier, province, and income. Descriptive external comparisons use official 2020 Population Census margins from the National Bureau of Statistics for [sex](https://www.stats.gov.cn/zt_18555/zdtjgz/zgrkpc/dqcrkpc/ggl/202302/t20230215_1904000.html), [education](https://www.stats.gov.cn/zt_18555/zdtjgz/zgrkpc/dqcrkpc/ggl/202302/t20230215_1903999.html), and [age](https://www.stats.gov.cn/zt_18555/zdtjgz/zgrkpc/dqcrkpc/ggl/202302/t20230215_1903996.html). The online adult sample and census population frames are not compatible enough for defensible raking; hukou is also not interchangeable with current urban residence. No weights were constructed.

## Protocol deviations and reproducibility notes

- No causal forest was run because `econml`/`causalml` was unavailable.
- Policy value uses correct OOF IPW but not a second DR evaluator.
- Factor selection uses the eigenvalue>1 rule rather than a simulated parallel analysis; discovery-half validation limits outcome overfitting.
- The optional baseline-profile clustering was omitted to avoid a weakly identified post-hoc phenotype search.
- Amount-specific formal tests of differences in calibration are not emphasized; cell-level intervals are reported because nine-cell precision is limited.
- After modular debugging, the final script passed syntax compilation and completed an uninterrupted end-to-end reproduction. Aggregate numeric outputs matched the staged results exactly or to floating-point tolerance (maximum absolute difference 1.3e-15). Random seeds are fixed at 20260921.
