# Final Exploration Results

All quantities concern **stated MPC**—a hypothetical incremental-consumption response—not realized spending, welfare, or cash-equivalent value. This is exploratory/post hoc analysis of one Chinese online sample.

## Q1. How predictable is stated MPC with rich objective and subjective information?

Predictability is low under every representation. Form-specific random-forest OOS R² is 0.044 for Cash, 0.032 for Food, and 0.029 for Medical; ridge/elastic-net results are smaller, and gradient boosting is negative. Across outcome representations, ridge ALL R² ranges only 0.026–0.032, so the result is not an artifact of one midpoint coding.

Subjective information adds very little. Relative to O, paired RF fold gains are +0.0035 for O+S (95% bootstrap CI −0.00004, 0.0069), +0.0030 for O+A (−0.0010, 0.0067), and +0.0049 for ALL (0.0004, 0.0091). Thus the O+S interval excludes both the predeclared +0.01 and +0.02 meaningful-gain benchmarks.

## Q2. Is predictability stable across Cash, Food, and Medical forms?

Only weakly. Cross-form Spearman correlations are 0.19 for Cash→Food, 0.11 for Cash→Medical, and 0.14 for Food→Medical; recentered cross-form R² ranges 0.008–0.048. Predictor alignment is highest for Cash–Food: with O+needs, ridge coefficient correlation is 0.65 versus 0.23 for Cash–Medical; with ALL it is 0.60 versus approximately 0.00. Bootstrap intervals are broad and the regularized coefficient exercise is descriptive, but the pattern is consistent with poorer transfer to Medical.

OOF predictable variance is tiny relative to actual outcome variance: 0.00133 for the shared component versus 0.0663 for observed midpoint stated MPC. Form-specific deviation variances are 0.00060–0.00082. There is a small shared observable signal and comparably small form-specific signal, atop a much larger unexplained/latent-or-noise component.

## Q3. Does transfer form reorder who is predicted to respond strongly?

Yes descriptively, but not enough to establish a general stable ranking. Cash and Food mappings are more alike than either is to Medical, while all cross-form rank correlations remain below 0.20. Thus there is no strong observable “high stated-MPC person” type that transfers across forms. The result supports context-specific reordering more than a stable-trait interpretation, but coarse hypothetical measurement may also attenuate stability.

## Q4. Is Food non-fungibility structurally different from Medical non-fungibility?

The contrast is asymmetric. For Food−Cash, ALL-feature T/DR/R calibration slopes are −0.34, −0.49, and −0.46; the latter two have negative held-out intervals. This means the learned rankings reverse rather than validate and cannot support useful Food HTE. With O+needs or latent factors, calibration is null.

For Medical−Cash, ALL-feature calibration is positive across T (0.736; 95% CI 0.357, 1.114), DR (0.367; 0.036, 0.698), and R (0.408; 0.084, 0.732). T-learner top-minus-bottom separation is 0.102 (0.047, 0.157); DR/R separations are positive but include zero. O+needs DR calibration is 0.479 (0.172, 0.785), while subjective-only is null. Medical−Food ALL-feature calibration is null across all three learners, although an attitudes-only DR result is positive; that isolated domain result is fragile.

Amount matters: Medical−Cash HTE validates at RMB 1,000 for T and DR (calibration 1.224 and 0.978; top-bottom 0.205 and 0.154) but is null at RMB 200 and 5,000. Food−Cash remains null at every amount. Prior transparent Medical−Food moderation by income and past medical spending remains visible across R/C and Q1 screens, but medical-spending moderation loses precision under Q2. The evidence is consistent with context relevance, not a validated medical-need mechanism.

## Q5. Do latent subjective dimensions add anything beyond objective conditions?

Three discovery-half PCA dimensions are internally coherent: subjective economic state (14 items, 74.3% variance, alpha 0.973), social confidence (11, 69.7%, 0.956), and wellbeing/optimism (5, 77.3%, 0.926). Yet their held-out level-prediction gain over O+needs is only +0.0020 R² (0.0274 to 0.0294).

Latent factors do not predict Food−Cash HTE (calibration 0.022; 95% CI −0.314, 0.358). Medical−Cash calibration is 0.480 (0.140, 0.820), essentially the same as O+needs alone (0.479), although its top-bottom separation is 0.094 (0.038, 0.149). This is not evidence that a latent psychological mechanism adds beyond objective/needs information.

## Q6. Does predictable HTE create useful transfer-form targeting gains?

No. Honest IPW values are 0.223 for all Cash, 0.208 for all Food, and 0.181 for all Medical. The depth-2 policy tree assigns everyone Cash. The ML argmax policy assigns 60.4% Cash, 29.6% Food, and 10.1% Medical, but its gain versus all Cash is −0.0133 (95% bootstrap CI −0.0277, 0.0014). Predictable HTE does not translate into meaningful targeting gains in stated MPC.

## Q7. Are results robust to survey response-style concerns and sample composition?

Medical patterns are more robust than Food patterns. Across R, C, Q1, and Q2, the pooled Medical−Cash effect remains negative (Q2: −0.333; 95% CI −0.564, −0.102). Food−Cash is stable in R/C but loses precision in Q1 and is near zero in Q2. Medical−Food income moderation remains negative through Q2; past-medical-spending moderation is positive through Q1 but null in Q2. Q2 retains only 1,208 respondents, so both selection and loss of precision matter.

The sample is young (mean 33.2; only 1.6% age 60+), 53.0% female, and 78.9% junior-college-or-more. Official census comparisons are descriptive because frames differ: sex imbalance is modest, while age and education differences are large. These incompatibilities preclude defensible population raking. Generalization beyond educated online Chinese adults is therefore limited.

## Q8. Which framing is best supported: economics, general human behaviour, or policy design?

| Position | Strongest fact | Weakest link | Evidence type | Stated outcome | Single-study barrier | What would strengthen it |
|---|---|---|---|---|---|---|
| Economics | Rich observables explain little; randomized form contrasts and Medical−Cash HTE add a fungibility dimension | No realized MPC and weak Medical−Food flexible HTE | Randomized mean effects plus predictive HTE | Serious but manageable if labeled precisely | Moderate | Administrative spending or repeated choices |
| Human behaviour | Cross-form ranks are weak and Cash–Food mappings align more than Cash–Medical | Low reliability may mimic context specificity; no replication | Predictive/descriptive plus randomized context | Serious, potentially fatal for a broad claim | Serious | Preregistered multi-sample replication with behavioral outcomes |
| Policy design | Honest policy evaluation finds no gain over uniform Cash | Objective is stated MPC, not welfare or delivery cost | Randomized-design IPW | Serious | Serious | Real outcomes, policy constraints, external validation |

The economics framing currently has the clearest estimands and most defensible scope. The broader human-behaviour framing is plausible as a question, not yet established as a general result. The policy null is useful but cannot by itself support design recommendations.

### Nature-style generality check

| General object | Supporting evidence | Evidence against | Measurement limitation | Broader than this setting? |
|---|---|---|---|---|
| Context dependence of nominally equivalent resources | Randomized mean form effects; weak cross-form transfer; Medical-specific mapping | Shared signal exists; no within-person potential outcomes | Hypothetical coarse stated MPC | Suggestive only |
| Stability of individual differences | Cash–Food coefficient alignment | All cross-form rank correlations <0.20 | Noise can attenuate stability | Not established |
| Objective versus subjective predictability | O+S gain CI excludes +0.01 | Small positive ALL gain | Self-report blocks and outcome share method variance | Potentially broad but needs replication |
| Targetability | OOF Medical−Cash calibration | Policy value does not beat all Cash | Stated-MPC objective is not welfare | Policy-specific |

## A. Five strongest facts

1. Stated-MPC prediction is low: form-specific RF OOS R² is 0.044/0.032/0.029 for Cash/Food/Medical, across repeated five-fold R-sample CV; ridge outcome-representation R² remains 0.026–0.032.
2. Cross-form stability is weak: RF Spearman transfer is 0.19 Cash→Food, 0.11 Cash→Medical, and 0.14 Food→Medical; regularized ALL coefficient correlation is 0.60 Cash–Food and approximately 0.00 Cash–Medical, with bootstrap uncertainty.
3. Medical−Cash HTE has positive OOF calibration across T/DR/R: 0.736 (0.357, 1.114), 0.367 (0.036, 0.698), and 0.408 (0.084, 0.732), respectively, in R with outer-fold evaluation; top-bottom evidence is strongest for T.
4. Medical−Cash predictability is amount-specific: at RMB 1,000, T/DR calibration is 1.224 (0.710, 1.738) and 0.978 (0.524, 1.432), while RMB 200 and 5,000 intervals include zero.
5. Medical form effects survive response-quality screens: Medical−Cash is −0.309 (−0.408, −0.209) in R and −0.333 (−0.564, −0.102) in Q2; sample restriction changes precision but not direction.

## B. Five strongest nulls

1. O+S adds only +0.0035 OOS R² (95% bootstrap CI −0.00004, 0.0069) over O; +0.01 and +0.02 gains are ruled out on the paired RF folds.
2. Latent subjective dimensions add only +0.0020 held-out level R² and do not calibrate Food−Cash HTE (0.022; −0.314, 0.358).
3. Food−Cash flexible HTE does not validate: ALL T/DR/R learned rankings are null or reverse in held-out data, and amount-specific calibration is null at all three amounts.
4. Medical−Food ALL-feature HTE is null across T/DR/R: calibration 0.053, 0.159, and 0.130, all with intervals spanning zero.
5. Personalization has no policy-value gain: ML argmax minus all Cash is −0.0133 (−0.0277, 0.0014), and the depth-2 tree chooses Cash for everyone.

## C. Stable-trait vs context-specific verdict

There is little evidence for a general observable “high stated-MPC person”: absolute OOS prediction is low and cross-form rank transfer is below 0.20. Predictor mappings are relatively more stable between Cash and Food than between Cash and Medical, while Medical−Cash—but not Food−Cash—shows reproducible cross-fitted HTE calibration. The balance of evidence favors a modest form-specific context response over a stable observable trait, especially for Medical, but does not separate genuine latent preference heterogeneity from coarse measurement, hypothetical bias, and response noise.

## D. Economics-paper interpretation

The defensible economics contribution is that rich objective and subjective observables explain little stated-MPC variation, while randomized transfer form changes both mean response and, for Medical versus Cash, part of the conditional response mapping; Food non-fungibility is broadly present but its observable HTE does not validate. This extends an MPC-predictability question toward transfer-form fungibility without treating baseline correlates as causal or stated MPC as realized expenditure.

## E. Nature-style interpretation

A cautious human-behaviour interpretation is that observable rankings of hypothetical responses to nominal resources transfer poorly across delivery contexts, with Cash and Food more similar than Medical, and that rich subjective reports add little predictive information. This is potentially broader than MPC, but the current evidence supports a context-specific empirical pattern in this setting—not a general law of human behavioural instability.

## F. Why the Nature-style interpretation may fail

- The outcome is hypothetical stated MPC, not realized behaviour.
- The study uses one young, highly educated Chinese online sample.
- There is no independent replication.
- The exploration is post hoc and not preregistered.
- There is no validation against actual expenditure.
- Flexible ML is weak or unstable: Food rankings reverse, Medical−Food is null, and Medical−Cash top-bottom intervals depend on learner.
- Cross-form differences may partly reflect coarse outcome measurement or survey-response noise.

## G. Best single paper question supported by the data

Do observable individual differences in stated consumption responses generalize across transfer forms, or does the delivery context—especially a medical account—reshape who responds?
