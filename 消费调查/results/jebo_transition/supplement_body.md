# Supplementary material

Transfer size and stated spending: Distributional evidence from cash and earmarked resources

Zelin Liu and Yinghao Pan

## S1. Design, coding and analysis populations

The adult-primary sample A includes recorded ages18–100, with observed adult ages ending at81 (N=5,480). The historical full sample R has5,497 records, including17 recorded minors. Re-analysis of adults does not resolve the ethics and consent requirements for the original collection. The original questionnaire places15 attitude items, including three subitems, before the transfer scenarios. Background information is returned through the questionnaire platform. Recruitment channel, field dates, consent and ethics documents, allocation logs and the stopping rule must be documented before submission; the separate author-information checklist identifies these outstanding items. The analysis does not infer them from platform metadata.

Each respondent answers one hypothetical scenario. The Food voucher is noncashable, covers food/daily necessities and expires after six months; Medical is a long-lived personal medical-account credit for medical-related expenditure. The outcome concerns additional total spending relative to existing plans. The forms also differ in explanatory wording, including the lowest-category description. Food and medical expenditure questions precede the scenarios and may prime categories. The question has no common explicit horizon. The exact original Chinese questionnaire remains in the private source archive; aggregate documentation does not replace verification of the instrument and its administration.

The six category scores are1–6. Midpoints are0/.05/.175/.375/.625/.875. Positive-category means categories2–6; other thresholds are categories3–6,4–6,5–6 and6. The last has the verbal label above75%, with a75–100% yuan example. No midpoint is an observed amount. Ordinal coding imposes equal rank spacing; ordered-link alternatives introduce latent-scale assumptions instead. TableS1 gives all adult cell frequencies, and TableS2 gives the five threshold profiles. Amount lines connect independent randomized groups, not repeated observations.

{s1}

{s2}

## S2. First-order factor effects and form contrasts

Saturated nine-cell means identify the marginal contrasts. Form effects average cell differences equally over the three amounts; amount effects average equally over the three forms. All uncertainty uses HC3. The highest-category family contains two omnibus tests and four reference contrasts: Food–Cash, Medical–Cash,1,000–200 and5,000–200. Holm adjustment is within those six tests. The ordinal and midpoint rows are supplied descriptively, without implying a new correction family. A separate six-test family compares Food–Cash and Medical–Cash at each amount for the highest category. TableS4 includes pointwise and simultaneous intervals; the positive Food point estimate at5,000 does not establish a crossover.

{s3}

{s4}

## S3. Interaction family and statistical calibration

For each of seven codings, the linear model contains an intercept, two form indicators, z=log(amount/200)/log(5), and two form×z terms. Its omnibus interaction has two degrees of freedom; each Cash-versus-form contrast has one. The21-test family holds sample, model and amount representation fixed. It was defined after earlier exploration and does not have preregistered status. Robustness specifications address sensitivity and remain visible separately; treating their dependent p values as a count of independent replications would be misleading.

Holm is applied to the21 nominal p values. The joint min-P method stacks HC3 interaction influence contributions across outcomes to construct a14×14 covariance V. In each of10,000 draws, a centered Gaussian vector V^(1/2)g supplies the joint coefficient errors. Each omnibus Wald statistic is mapped through its chi-square distribution with its own degrees of freedom, and each scalar contrast supplies a two-sided normal p value. The minimum across all21 p values is compared with each observed p. Adjusted values use(1+number of simulated minima no greater than the observed p)/(B+1). Tiny negative covariance eigenvalues attributable to round-off are truncated at zero.

This construction targets an asymptotic joint centered-error law, using the unrestricted covariance. It is not randomization inference under a sharp treatment null. The covariance and all seven grouped sufficient-statistic fits were previously checked against respondent-row regressions, with discrepancies below6×10^−16 in coefficients and4×10^−17 in covariance entries. No such respondent-level fitting is newly performed for the JEBO transition. Bonferroni simultaneous95% intervals across the21 tests accompany scalar contrasts. A min-P value near0.039 has Monte Carlo standard error around0.002; its threshold crossing is not a separate robust discovery.

{s5}

Prior calibration used1,000 independently generated datasets per scenario, each with a complete coefficient/HC3 refit and999 calibration draws. The three scenarios were a pooled null, additive probability main effects, and a partial null with15 true and6 false restrictions. The partial-null alternative shifts mass between intermediate Food categories while leaving the highest-category interaction null. TableS6 reports family rejection rates with exact binomial intervals. These limited scenarios do not establish universal finite-sample control or power for the observed effect.

{s6}

The earlier1,500-row diagnostic mixed outcome/contrast choices with samples, links and amount representations. Its unnormalized maximum combined absolute scalar z values with square roots of multidimensional Wald statistics. In4,949 of5,000 saved draws, a four-degree-of-freedom row supplied that maximum. The leading model types were saturated OLS/LPM and logit, not primarily the ordered location-scale fit. Applying degrees-of-freedom-specific p transformations to the same saved grid changed the focal full-sample omnibus adjusted value from0.414 to0.370. That corrects a scale problem but retains the old family and null-model limitations. It is not the current primary inference.

The historical family also combined different additive nulls across links. In one ordered location-scale construction, the constrained fit zeroed both location and scale interactions while some reported tests involved location alone. The old7/200 simulation examined a fixed-score family maximum under a pooled null, rather than a single isolated test, but did not refit the entire estimation procedure or establish useful power. These limitations are retained in the analysis history. The narrower21-test family is more interpretable; it cannot retroactively eliminate selection across the research programme.

## S4. Threshold and specification sensitivity

The original420-specification grid crosses seven outcome/model representations, five overlapping samples, two covariate choices, two amount representations and three form contrasts. Its supplied summary contains20 specifications per outcome/contrast. Highest-category Food–Cash and Medical–Cash signs are consistent across that grid, but intervals and ordinal contrasts are less stable. Sign counts are descriptive. Changing sample definitions changes the target population, and nonlinear latent-scale coefficients do not share the probability scale of a linear model. No pooled specification-curve p value is constructed.

{s7}

Ordered logit/probit and location-scale sensitivity are retained in the historical tables, including failed-fit/status fields rather than selected successful fits. In the full-sample trend ordered-logit example, the omnibus nominal p is0.0816 and Cash–Medical p is0.0378; these are latent-location results, not probability-effect magnitudes. The broader grid includes adult and response-screen variants. In particular, strict Q2 ordinal contrasts attenuate and may change sign. Stability of the highest-category point estimates should not be generalized to every coding. The primary adult ordinal omnibus remains nonsignificant even before the21-test correction.

Direct historical tests comparing the highest-category slope difference with other threshold differences did not establish exclusive tail specificity. For the derived Restricted–Cash contrast, all four top-versus-lower-threshold Holm values are1.000. Restricted always means the equally weighted average0.5Food+0.5Medical, not a fourth randomized arm and not an assertion of Food–Medical equivalence. The main paper therefore describes visible high-response compression while retaining the full bins.

Adult endpoint risk and odds ratios for the highest response are supplied in TableS8. Cash's larger relative decline shows why proximity to zero alone is not a sufficient arithmetic account of its steeper probability decline. These within-form ratios are not adjusted tests that relative slopes differ across forms. Implied-yuan outcomes in the earlier package multiply the assigned amount by midpoint scores. Their increases are partly mechanical and do not validate actual spending or a constant-yuan behavioral model. The earlier full-sample Cash implied-yuan elasticity was0.929; this is an arithmetic translation with coding assumptions, not a new JEBO result.

{s8}

## S5. Extensive/conditional decomposition

Only this new empirical calculation was authorized for the target transition. Its post hoc analysis manifest was committed before execution. We use the approved adult54 category counts (nine cells×six categories), not respondent records. Within each cell, p=1−share(category1), m is the midpoint mean and m+=m/p. The endpoint identity is Δm=Δp×(m+low+m+high)/2+Δm+×(plow+phigh)/2. All nine mean identities and all three decompositions pass to numerical tolerance1×10^−14.

Bootstrap sampling uses numpy's default_rng with seed2026100316 and4,000 draws. For each cell and draw, a multinomial draw with its observed N and six observed category frequencies is exactly equivalent to sampling categorical records with replacement within that cell. Cells are sampled independently, with fixed cell sizes. Percentile2.5%/97.5% intervals are pointwise. No draw has zero positive-category observations; no redraw or selective exclusion is needed. Identities hold for every draw. The decomposition introduces no new hypothesis tests, subgroup searches, thresholds or contribution percentages near a zero total.

TableS10 reports all cell quantities and conditional-positive intervals. Main Table3 reports endpoint contributions. The conditional group is selected by an outcome after assignment. Its mean and the associated product component are descriptive; they do not identify a causal intensive-margin effect for a stable population. This is the same selection issue even if the contribution's pointwise interval excludes zero.

{s10}

## S6. Conceptual predictions

TableS9 summarizes the six accounts considered in interpretation. These are conditional predictions rather than fitted models. A broad theory with ambiguous gap predictions is not confirmed by a matching sign. No structural estimation, Bayesian mechanism comparison or additional mediator search is performed.

{s9}

## S7. Income-relative scale and Food expenditure

The unrestricted income model is a logit with form-specific intercepts, log(amount) slopes and log(income) slopes. ABS sets the three income slopes to zero. REL sets each income slope equal to the negative of its amount slope. ABS and REL are nonnested restrictions of the unrestricted model. A separate form×amount×income test includes all lower-order terms. TableS11 gives the seven-test diagnostic family, including income, Food and response-screen tests.

The M1 current-income mapping uses250,750,2,000.5,5,500.5,11,500.5 and20,000 RMB for codes1–6; legacy codes11–16 use500,2,000.5,4,000.5,6,500.5,10,000.5 and16,000.5. M2 changes only codes1,6 and11 to125,30,000 and250. These represent income bands, not exact household resources; legacy income is personal income. Five cell-stratified folds are constructed in the full sample with seed20261003, then restricted to adults. Model comparisons share folds, and scaling uses training data only. All fits converged in the existing prediction analysis.

{s11}

{s12}

The gains are descriptive; no1% hurdle or any other materiality rule decides whether relative scale “works.” Fold-level uncertainties are not treated as independent because training sets overlap. The alternative mapping preserves the broad prediction ranking. Rejecting ABS indicates additional income information; nonrejection of REL does not establish the ratio as a sufficient explanation, still less identify mental accounting.

For Food, G=1 when six times the monthly food-expenditure lower bound exceeds5,000. The Cash/Food adult sample is3,621, with2,806 classified and815 remaining. The form×z×G model includes all lower-order terms. Its direct triple difference, rather than comparing separate subgroup significance, is the relevant test. A separate amount/food-expenditure ratio restriction uses3,476 adults with positive lower bounds; its adjusted p=1.000 supplies no positive evidence that the ratio is correct. The classification assumes stable eligible spending and does not observe counterfactual redemption or cash substitution.

## S8. Response-style screens and descriptive associations

C excludes constant responses across15 zero-to-ten attitude items and duplicate identifiers, leaving5,171 adults. Q1 requires sample standard deviation≥1 and at least4 distinct responses (N=2,715). Q2 requires standard deviation≥1.5, at least5 distinct values and no more than80% at the endpoints0 or10 (N=1,208). Q1/Q2 here name analysis samples, not the first two questionnaire questions. Their code uses neither treatment assignment nor spending outcome. The relevant items precede the vignette in the questionnaire, although administration timestamps and possible advance exposure are not documented.

These are response-style screens, not validated measures of dishonest or inattentive responding. They can select genuine attitudes and variance preferences. Direct joint tests of whether highest-category form×amount effects differ between passers and failers have nominal p=0.927/0.994 and Holm p=1.000 for both screens. The subgroup estimates and intervals are in TableS13; event/cell counts remain available in screen_cell_counts.csv. Null differences do not demonstrate equivalent effects. The historical constant-response-excluded omnibus nominal p=0.0036 is smaller than the full-sample0.0080, but selecting that sample as primary on this basis would compound selection.

{s13}

Earlier “positive controls” are renamed descriptive Cash associations. Cash size is the focal phenomenon itself, emergency fundraising has highest-category Holm p=0.063, and income rank has a positive association rather than the prespecified negative expectation (Holm p=0.006). These cannot independently validate hypothetical responses as realized behavior. They use the historical full Cash sample N=1,798 and adjust jointly for dose, income rank and emergency fundraising; do not substitute their estimates for the adult primary results.

The existing who-drives analysis found no moderator surviving its local Holm families; its joint Cash and Restricted–Cash moderation p values were0.535 and0.554. The broad150-variable screen likewise did not identify a stable FDR-adjusted moderator. These nulls are not equivalence evidence. For example, the plug-in minimum detectable Cash–Food highest-category moderation by income rank is about3.34 percentage points per standard deviation. That precision is insufficient to rule out substantial moderation. No further moderator screening is performed, and neither ML predictions nor variable importance are interpreted as identified individual treatment slopes.

## S9. Population calibration

The2020 Chinese census Table4-1 supplies joint age/education targets. Four adult age groups (18–29,30–44,45–59,60+) crossed with three education groups (junior secondary or less, high/secondary vocational, tertiary) give12 cells with observed sample support. Support in broad cells does not imply coverage within them: only90 respondents are60 or older, and observed age ends at81. The targets concern2020, not the survey recruitment population.

Uncapped weights equal target share/sample share. Capped weights are min(λw,10), with λ chosen to retain mean1, so the normalized maximum is truly10. Exact balance and that cap cannot both be achieved here. Effective sample size is314.8 under uncapped weights and1,191.0 when capped; the largest target-cell gap after capping is16.53 percentage points. Weighted uncertainty is conditional on these weights, not inclusive of the unknown selection process. TableS14 reports diagnostics; the full cell targets and weighted effects remain in the aggregate archive. This feasible sensitivity does not justify national generalization.

{s14}

## S10. Analysis lineage and source directory

The sequence is discovery of the size/distribution pattern, bounded threshold/specification strengthening, theory-variable moderation, broad observable screening, presentation of the distribution atlas, revision-stage statistical/measurement audit, and the current finite-family reanalysis. The JEBO transition adds only the product decomposition and literature synthesis. It does not re-estimate the previous hypotheses, shrink their families further or recast post hoc results as preregistered. The archive preserves unfavorable results and old versions alongside the current interpretation.

{archive}

Aggregate source files, analysis code and figure-generation scripts accompany this package. Respondent records are not included. Access conditions for de-identified data, consent restrictions and an archival identifier require author documentation. The source manifest links the analysis base and identifies which historical outputs are descriptive or superseded; these distinctions are essential when reusing numbers. No change in journal positioning changes the status of the evidence.
