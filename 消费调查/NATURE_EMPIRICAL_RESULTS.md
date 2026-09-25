# Nature-series locked empirical package: results

This is a locked re-estimation of previously explored, **hypothetical stated-MPC** data, not a preregistered confirmation or a realized-consumption study. The original ordinal 1–6 response is primary for randomized mean effects; midpoint stated MPC is auxiliary for prediction, HTE ranking, and policy value. Raw R N=5,497 unless noted. All intervals below are 95% intervals of the specified type; full estimates and figure-panel source data are in `tables/nature_*.csv`.

## Claim 1 — Stated MPC is weakly predictable even with rich information

Under identical repeated five-fold, nine-cell-stratified splits, RF out-of-sample R² is 0.0465 for objective/needs O (fold-bootstrap interval 0.0388–0.0536) and 0.0482 for ALL (0.0404–0.0555). Treatment-only T is about 0.005. Ridge, elastic net, and histogram boosting also remain low; the full model's mean R² is 0.0395, 0.0427, and 0.0353, respectively. Fold-level RMSE and MAE are exported. The prior outcome-representation checks yield only about 0.026–0.032 ridge R² across ordinal, midpoint, alternative top, and threshold codings. These are prediction facts about a coarse stated response, not an estimate of the variance of latent preferences. Figure 2 and ED Figs. 3–4 show the result.

## Claim 2 — Subjective states add little incremental predictive value

On paired RF folds, O+S minus O is +0.00343 R² (fold-bootstrap interval +0.00010 to +0.00671); ALL minus O is +0.00168 (−0.00144 to +0.00499). Both upper bounds are below the predeclared +0.01 and +0.02 practical-gain thresholds. The discovery-half, held-out three-domain PCA test from the validated baseline adds +0.00201 R² (0.02739 to 0.02940) over objective/needs information. The domains have high internal consistency, but neither their existence nor the null increment licenses “psychology does not matter.” Subjective predictors and the outcome are both self-reports, and this common method may affect interpretation in either direction. Figure 2b–c and ED Fig. 5 show the evidence.

## Claim 3 — Response rankings have limited cross-form portability

Source-form RF predictions rank target-form observed midpoint stated MPC weakly: Cash→Food Spearman ρ=0.188, Cash→Medical 0.112, and Food→Medical 0.140; the three reverse directions are 0.198, 0.141, and 0.153. Recentered target R² across all six directed transfers ranges approximately 0.008–0.047. The shared OOF predicted component has variance 0.00133 versus observed midpoint outcome variance 0.0663; form-specific deviation variances are 0.00060–0.00082. These component variances are descriptive and non-additive.

Measurement noise is an important competing explanation. Under the **assumption**, not estimate, of equal outcome reliability 0.4, the classical attenuation heuristic gives Cash→Food 0.470 and Cash→Medical 0.280; at reliability 0.6 they are 0.313 and 0.187. Thus the observed portability is low, but plausible unmeasured unreliability could make underlying Cash–Food stability moderate. Figure 3 must be read as “observed portability is low,” not proof that true preferences are unstable.

## Claim 4 — Cash–Food is more portable than Cash–Medical

The directed rank-correlation difference Cash→Food minus Cash→Medical is +0.0758 (target-respondent bootstrap interval +0.0115 to +0.1370); Cash→Food minus Food→Medical is +0.0479 (−0.0154 to +0.1090). The ALL-feature ridge coefficient-vector correlation difference Cash–Food minus Cash–Medical is +0.595 (stratified-refit bootstrap interval +0.030 to +0.635), with a similarly positive cosine difference. The objective/needs-only coefficient difference interval includes zero, as do sign-agreement differences. The first two metrics support a relative Cash–Food/Cash–Medical distinction, but not uniform superiority across all blocks and similarity measures. The Spearman interval holds source models fixed and therefore omits source-training uncertainty. Figure 3b and ED Figs. 6–7 show these checks.

## Claim 5 — Medical−Cash HTE is more predictable than Food−Cash HTE

Under common global outer folds, the headline-seed Medical−Cash OOF calibration slope is +0.604 (HC1 interval +0.230 to +0.978) for T, +0.329 (−0.004 to +0.662) for DR, and +0.281 (−0.050 to +0.612) for R. Food−Cash slopes are −0.239, −0.259, and −0.238, all with headline-seed intervals including zero. Positive Medical top-minus-bottom separation is clearest for T: +0.0904 (+0.0339 to +0.1470); DR and R headline intervals include zero.

The **direct** Medical-minus-Food difference is stronger evidence than separate significance labels. DR calibration differs by +0.588 (stratified-bootstrap interval +0.145 to +1.008; bootstrap p=0.0093) and DR observed top–bottom separation by +0.0782 (+0.0116 to +0.1465; p=0.0213). T differences are also positive; R calibration differs positively, but its top–bottom difference interval includes zero. Over ten prespecified fold/learner seeds, Medical calibration point estimates are positive in all 10/10 runs for each T, DR, and R, while Food is predominantly negative. The repeated seeds are not independent replications, and common-fold headline DR/R uncertainty plus quality-screen sensitivity preclude a strong multi-learner/measurement-robust general-behaviour claim. Figure 4 and ED Figs. 8–9 report the evidence.

Transparent moderation is secondary to OOF validation. In the focused jointly adjusted ordinal Medical−Food model, income is −0.146 (HC1 interval −0.246 to −0.046), education −0.145 (−0.243 to −0.047), and prior medical spending +0.110 (+0.008 to +0.212) per standardized predictor. Within-amount randomization inference gives BH-adjusted q values of 0.009, 0.006, and 0.012, respectively, for the three Medical−Food trends; Medical−Cash income and medical-spending q values are approximately 0.042, education 0.052. HC3, province/city-tier FE, geographic-cluster, sample, factor, and amount-saturated specifications are in supplementary tables. Prior medical spending is a proxy for exposure/need, not a causal mechanism or strict bindingness measure.

Food is a meaningful null case, but not a quality-invariant one. The Raw pooled Food−Cash ordinal effect is −0.119 (HC1 interval −0.221 to −0.017). The strict and very-strict inframarginal groups remain negative: −0.121 (−0.229 to −0.013; N=3,262) and −0.125 (−0.246 to −0.003; N=2,899). The prespecified Food-moderator confidence limits and BH q values are exported; they rule out some large slopes but not all smaller heterogeneity. Under the Q2 response-style screen, the Food average effect is +0.016 (−0.227 to +0.258), so it should not be headlined as equally robust to Medical.

## Claim 6 — Medical HTE is amount-specific

At RMB 1,000, Medical−Cash calibration is +1.035 (HC1 interval +0.505 to +1.565) for T and +0.925 (+0.467 to +1.384) for DR; top–bottom separations are +0.181 (+0.086 to +0.276) and +0.182 (+0.088 to +0.275). At RMB 200 and 5,000 the calibration intervals span zero. A two-df amount×treatment×standardized-prediction omnibus rejects equal calibration patterns (T p=0.0029; DR p=0.00062). In ten fixed-seed reruns, RMB 1,000 calibration is positive with a lower 95% bound above zero in 10/10 T and 10/10 DR runs; neither other amount achieves this. This is an amount-specific qualifier, not evidence that RMB 1,000 is an optimal policy amount. Figure 5a shows the result; Fig. 5b–c display the secondary, transparent Medical−Food income and spending patterns.

## Claim 7 — Personalization does not improve stated-MPC policy value

The uniform Cash benchmark has IPW value 0.2230 and cross-fitted DR value 0.2277 in midpoint stated MPC. The depth-2 tree assigns all respondents to Cash in the headline seed, so its gain is zero. ML argmax assigns 60.4% Cash, 29.6% Food, and 10.1% Medical, but its gain versus Cash is −0.0133 by IPW (paired bootstrap interval −0.0272 to +0.0001) and −0.00873 by DR (−0.0194 to +0.00198). Across ten fixed fold seeds, ML gains remain negative pointwise: IPW range −0.016 to −0.008, DR range −0.010 to −0.004. The tree is nearly all-Cash across seeds (mean 97.3% Cash). These are honest OOF evaluations for a stated-consumption objective; they are not welfare comparisons or a recommendation to deploy Cash. Figure 6 displays DR values; IPW and seed checks are in supplementary tables.

## Claim 8 — Which claims survive response-quality restrictions?

The pooled ordinal Medical−Cash effect remains negative in R (−0.309, −0.408 to −0.209), C (−0.322, −0.424 to −0.220), Q1 (−0.387, −0.532 to −0.242), and Q2 (−0.333, −0.564 to −0.102). This is the clearest quality-robust randomized finding. Food−Cash is negative in R/C, imprecise in Q1, and null in Q2. OOS level predictability falls under the strictest screen: ALL R² is 0.0496 in R, 0.0449 in C, 0.0226 in Q1, and 0.0100 in Q2.

Medical−Cash **HTE calibration is not comparably robust**: cross-fitted DR is +0.329 (−0.004 to +0.662) in R, +0.612 (+0.286 to +0.937) in C, +0.246 (−0.192 to +0.684) in Q1, and +0.194 (−0.410 to +0.799) in Q2. Q1/Q2 intervals are broad because they retain 2,715/1,208 total respondents, but the change is material for a Nature-style claim. The Q2 result is neither evidence of no HTE nor a quality-robust validation. ED Fig. 10 displays mean-effect/moderator sensitivity; the predictability/HTE screen table is supplementary.

The sample is young (mean age 33.2) and highly educated (78.9% junior college or above), and the official census comparisons are only descriptive because adult online and total-population frames differ. No defensible raking is performed. Broad age, education, hukou, and city-tier stratum contrasts are descriptive only. There is no actual spending validation, repeated-outcome reliability measure, independent sample, or preregistration.

## A. Main-text eligible results

1. Randomized form changes the original ordinal stated response: pooled Food−Cash −0.119 (−0.221, −0.017) and Medical−Cash −0.309 (−0.408, −0.209), R; distributions, amount cells, A/C, and outcome-coding checks agree directionally. Fig. 1 is eligible.
2. Low out-of-sample stated-MPC predictability: RF ALL R² 0.0482 (fold-bootstrap 0.0404, 0.0555), with low values across model families and outcome representations. Fig. 2a is eligible as a prediction result.
3. Subjective information's small incremental prediction: RF O+S−O +0.00343 (+0.00010, +0.00671), excluding +0.01; the held-out latent-factor increment is +0.00201. Fig. 2b–c is eligible with the self-report/common-method caveat.
4. Honest policy-value null: ML−Cash DR −0.00873 (−0.0194, +0.00198), IPW −0.0133 (−0.0272, +0.0001), stable negative point estimates across ten seeds. Fig. 6 is eligible for the stated-MPC objective.

## B. Extended-data only results

- Observed cross-form portability is low, and Cash→Food exceeds Cash→Medical by +0.0758 (+0.0115, +0.1370), but source-model uncertainty and unknown outcome reliability limit a general context-reordering claim. Fig. 3 is a **candidate visual**, not yet an unqualified main-text claim.
- Medical−Cash versus Food−Cash HTE predictability differs formally (DR calibration difference +0.588, +0.145 to +1.008), yet the headline common-fold DR/R Medical intervals and Q1/Q2 quality screens weaken standalone Medical HTE validation. Fig. 4 is a **candidate visual** and should not be promoted without new validation.
- RMB 1,000 Medical HTE is stable across T/DR and seeds, with amount omnibus p<0.003; it is supporting, post hoc amount-specific evidence. Fig. 5 is a **candidate visual**, not a universal Medical mechanism.
- Focused income, education, and prior-medical-spending moderation, inframarginal Food results, demographic strata, reliability scenarios, and factor diagnostics belong in Extended Data/Supplement and should not lead the Introduction.

## C. Results that should be dropped

- “Human preferences are unstable”: true response reliability and within-person counterfactual rankings are unidentified.
- “Medical need causes the heterogeneity”: prior spending and other baseline traits are not randomized mechanisms.
- “Medical HTE survives all survey-quality screens”: Q1/Q2 OOF validation is inconclusive.
- “Personalized form targeting is beneficial”: neither IPW nor DR beats uniform Cash for the stated-MPC objective.
- Attitude-only or isolated subgroup interactions as a paper centre; feature importance as causal evidence.

## D. Nature-style claim that is actually supported

In this randomized single-survey setting, transfer form changes the distribution of **stated** marginal consumption responses, rich baseline information predicts little of their individual variation, subjective states add less than one percentage point of OOS R² beyond objective/needs information, and observed predictor rankings transfer only weakly across forms. A stronger claim that context *truly reshapes stable individual differences* remains sensitivity-dependent because reliability is unmeasured and Medical HTE quality-screen validation is incomplete. The six figures constitute a locked candidate evidence package, not proof that a Nature-family editorial threshold has been met.

## E. Strongest alternative economics framing

The strongest economics framing is a precise stated-MPC/fungibility result: randomized restricted-form transfers lower stated additional consumption relative to Cash; observables explain little individual response variation; Food's average gap is difficult to target, while Medical−Cash HTE has formally greater—but quality-sensitive and amount-specific—predictability; neither form-specific prediction nor flexible policy learning beats a uniform Cash assignment for the stated-consumption objective. This does not identify realized expenditure, welfare, or causal roles of baseline moderators.

## F. Single biggest unresolved threat to interpretation

The response is a one-time, hypothetical, coarse self-report with **unknown test–retest reliability** and no realized-spending validation. Measurement noise could attenuate cross-form portability and HTE calibration, while survey-response style and online-sample selection complicate generalization. Independent preregistered replication with repeated or incentivized outcomes is the most direct way to resolve this threat.
