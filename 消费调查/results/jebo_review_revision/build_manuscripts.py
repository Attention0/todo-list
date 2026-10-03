from common import *
import shutil,re
M=ROOT/'manuscript'/'jebo_v3'
def table(headers,rows):return mdtable(pd.DataFrame(rows,columns=headers))
def ci(r,boot=False,d=3,scale=1):
    lo,hi=(r.bootstrap_lo,r.bootstrap_hi) if boot else (r.lo,r.hi)
    return f'{r.estimate*scale:.{d}f} [{lo*scale:.{d}f}, {hi*scale:.{d}f}]'
cell=pd.read_csv(O/'adult_share_yuan_table.csv');inc=pd.read_csv(O/'incremental_yuan_response.csv');el=pd.read_csv(O/'endpoint_elasticity.csv');aff=pd.read_csv(O/'affine_midpoint_parameters.csv');fam=pd.read_csv(O/'scientific_family42.csv');ip=pd.read_csv(O/'interval_affine_parameters.csv');diag=pd.read_csv(O/'interval_affine_diagnostics.csv')
tnames={'cash':'Cash','food':'Food','medical':'Medical'}
design=table(['Transfer bundle','RMB 200 N','RMB 1,000 N','RMB 5,000 N'],[[tnames[f]]+cell.query('form==@f').N.astype(int).tolist() for f in FORMS])
scale=table(['Form','200 to 1,000 increment','1,000 to 5,000 increment','Endpoint elasticity'],[[tnames[f],ci(inc.query("form==@f and interval=='low' and contrast=='within-form'").iloc[0],True),ci(inc.query("form==@f and interval=='high' and contrast=='within-form'").iloc[0],True),ci(el.query('form==@f').iloc[0],True)] for f in FORMS])
afftable=table(['Form','Midpoint intercept RMB','Midpoint slope','Interval slope constant scale','Interval slope amount scale'],[[tnames[f],ci(aff.query("model=='form_intercepts_slopes' and parameter==@p").iloc[0],True,1),ci(aff.query("model=='form_intercepts_slopes' and parameter==@s").iloc[0],True),ci(ip.query("model=='constant_full' and parameter==@s").iloc[0],True),ci(ip.query("model=='amount_full' and parameter==@s").iloc[0],True)] for f in FORMS for p,s in [(f+' intercept',f+' slope')]])
labels={'ordinal':'Ordinal score','midpoint':'Midpoint share','any_spending':'Above bottom','ge10':'At least 10% bin','ge25':'At least 25% bin','ge50':'At least 50% bin','top75':'Highest category'}
fr=[]
for y in OUTCOMES:
    c=fam.query("outcome==@y and test=='cash'").iloc[0];q=fam.query("outcome==@y and test=='omnibus'").iloc[0]
    fr.append([labels[y],f'{c.p:.4g}',f'{c.holm42:.4g}',f'{c.minP42:.4g}',f'{q.holm42:.4g}',f'{q.minP42:.4g}'])
family=table(['Outcome','Cash p','Cash Holm42','Cash minP42','Interaction Holm42','Interaction minP42'],fr)
abstract='''A decline in the spending share of a larger transfer need not imply a weak response in yuan. We examine both scales in a randomized survey experiment assigning 5,480 adults in China to hypothetical Cash, Food-voucher or Medical-account transfers of RMB 200, 1,000 or 5,000. The Cash midpoint-coded spending share falls from 25.3% to 20.2%, while implied additional yuan grows from 51 to 1,008. Its incremental implied response is 0.220 over the first amount interval and 0.195 over the second, compared with approximately 0.193 for Food and 0.179 for Medical. A descriptive affine model accommodates the nine midpoint means, but neither equal form slopes nor an intercept-only explanation is established. Censored-normal sensitivities depend strongly on residual-scale assumptions. In a 42-test family spanning seven response codings and six trend tests, Cash midpoint and highest-category trends retain evidence, whereas the ordinal trend and cross-form interaction do not. A food-expenditure subgroup pattern has the opposite sign to a sharp increasing-bindingness prediction, and continuous moderation remains imprecise. The experiment distinguishes observed response distributions, coded scales and mechanism predictions; it does not identify a psychological mediator or realized consumption effects.'''
main=f'''# Transfer size and form in stated spending responses

Author details to be supplied separately before submission.

## Abstract

{abstract}

Keywords: transfer size; earmarking; stated spending; marginal propensity to consume; survey experiment

JEL classification: D12; D14; D91; E21

## 1 Introduction

Transfers differ in what recipients can do with them and in how large they are. A small cash payment, a voucher for groceries and daily necessities, and a balance in a medical account enter the household budget with different rights and cues. These differences may matter for reported spending, but an apparent size effect also depends on the scale on which spending is expressed. A fall in the fraction of a transfer allocated to consumption can accompany a substantial, almost proportional increase in additional yuan. Understanding this distinction is necessary before assigning a behavioral explanation to a declining spending-share curve.

We study a randomized survey experiment in China that crosses three resource bundles with three nominal amounts. Each respondent sees one hypothetical Cash, Food or Medical scenario worth RMB 200, 1,000 or 5,000 and reports how much total consumption would exceed their original plan. The response uses six ordered categories with percentage labels and yuan examples. Among 5,480 adults, the Cash midpoint-coded share falls from 25.3% to 20.2% between the endpoint amounts. Yet its implied additional spending rises from RMB 51 to RMB 1,008. The relevant empirical question is whether differences across forms mainly concern levels at smaller amounts, incremental yuan responses, or both.

The scale comparison sharpens the description. Cash has an incremental midpoint-implied yuan response of 0.220 from RMB 200 to 1,000 and 0.195 from RMB 1,000 to 5,000. Food is approximately 0.193 in both intervals, and Medical approximately 0.179. High-interval Cash–Food point estimates are especially close, but their confidence interval permits meaningful differences in either direction. A form-specific affine model describes the midpoint means well. Its fitted intercepts and slopes are uncertain, and an interval-censored sensitivity changes substantially when the residual scale can vary with amount. We therefore report the affine function as a descriptive benchmark rather than as a structural consumption function.

Evidence about trends must also account for the choice of outcome. Across a family of 42 tests, the Cash midpoint and highest-category trends remain detectable; the Cash ordinal trend does not. Cross-form slope differences are not robust to the expanded correction. This distinction permits a clear within-Cash coded pattern without elevating the more demanding form-by-size interaction into an established result. The highest-category Food frequency exceeds Cash at RMB 5,000, but that crossing is itself imprecise. It cannot establish that a restricted transfer induces more total spending.

Our contribution is a bounded extension of related designs. Bernard (2023) already randomizes payment mode and shock size, using cash, an instant-access savings account and an unspecified mode. We add category-restricted Food and Medical bundles across three nominal amounts and compare the observed distribution with share and implied-yuan descriptions. There is no claim of the first joint design or of a new extensive-margin result. Boehm et al. (2025) provide stronger evidence from actual transfers and transactions, holding the transfer amount fixed. Our instrument addresses a complementary stated-response comparison and cannot substitute for that realized-spending evidence.

The paper also separates mechanism predictions from their precision. A sharp version of increasing Food bindingness predicts a more negative Food–Cash size gradient where a restriction is more likely to bind. The historical subgroup estimate is positive, contradicting that prediction conditional on an imperfect expenditure proxy. Continuous food-expenditure moderation has a wide confidence interval, and income, liquidity and response-style diagnostics do not exclude economically meaningful moderation. These findings constrain specific interpretations while leaving the underlying behavioral process unresolved.

Section 2 places the comparison in the literature. Section 3 describes the design and estimands. Section 4 reports distributions, scales and multiplicity. Section 5 evaluates Food predictions and the precision of other diagnostics. Section 6 discusses the scope of the evidence.

## 2 Transfer size form and measurement

### 2.1 Spending shares and finite increments

For an amount T, a reported finite-windfall share S summarizes an allocation of the whole transfer. Multiplying a coded share by T gives an implied yuan amount Y. Neither object is automatically the local derivative of consumption with respect to income. The finite increment between two amounts is the difference in mean implied yuan divided by the difference in transfer amount. It uses a different denominator from either endpoint share and is identified here from different respondents assigned to the two scenarios.

An affine description, Y = a + bT within a form, implies a share a/T + b. A positive fitted intercept can therefore accompany a declining share with relatively stable incremental yuan responses. This is a useful benchmark, not a theory of how a household treats a zero transfer: zero lies outside the design. Differences in fitted intercepts or slopes can reflect coding, heterogeneous responses and the bundled scenarios as well as preferences or constraints.

Size responses need not be universally decreasing. Fuster et al. (2021) find that larger hypothetical gains increase reported responses through the extensive margin of adjustment in their elicitation design. Andreolli and Surico (2026) report higher responses to large gains among affluent households and higher responses to small gains among liquidity-poor households. Their findings motivate attention to resource heterogeneity and question design; they do not supply a monotonicity condition that all populations or instruments must satisfy.

### 2.2 Resource bundles and the JEBO comparison

Mental accounting permits budgets and labels to affect allocation (Thaler, 1985, 1999; Shefrin and Thaler, 1988). Labeling evidence also shows that a benefit's purpose can influence expenditure even when it is not a fully binding restriction (Kooreman, 2000; Abeler and Marklein, 2017). Evidence on SNAP demonstrates that eligible spending can respond differently from unrestricted resources, but category expenditure and total additional consumption are distinct outcomes (Hastings and Shapiro, 2018).

Bonomo et al. (2026), a working paper, compare actual transfer programmes using food-store scanner data. They find stronger short-run food-store responses to in-kind than cash benefits and to recurring than one-time payments. This supports considering both form and timing, but it does not predict our total-consumption categories or validate their hypothetical measurement. Boehm et al. (2025) separately show that a cash-like transfer and a rapidly expiring card can produce different realized consumption responses. Our Food scenario also bundles an eligible-use restriction with expiry; Medical bundles a different eligible category with an accumulating account. These contrasts cannot isolate a pure label effect.

Two JEBO studies clarify the paper's behavioral location. Lee et al. (2024) study willingness to spend with mobile money in migrant households, emphasizing the social meaning of a payment instrument. Pauls and Laudi (2025) study temporal framing of a permanent tax cut among bank clients; the representation of the same income flow changes its reported allocation. Our comparison concerns nominal amounts and resource bundles rather than willingness to pay or the framing of a recurring tax cut. Its useful contribution is a transparent comparison of those stated distributions, not identification of the same mechanism in a new setting.

### 2.3 The elicitation boundary

The response is a direct binned question about hypothetical additional total consumption. Shapiro and Slemrod (2003) and Parker and Souleles (2019) concern reports about actual tax rebates. The latter links reported effects to revealed spending estimates in that setting; it does not validate all hypothetical instruments. Ueda (2025) provides a further caution about correspondence between self-reported and observed responses. Crossley et al. (2026), a working paper, show that direct and filtered questions change the response distribution and its relationship with payment size, horizon and liquidity. Elicitation format is thus part of the interpretation, not a minor measurement detail.

Our lowest category says essentially no additional consumption rather than recording an exact zero. Above-bottom-category probability is consequently not an observed spending-participation probability. Its yuan meaning may also change with transfer size because the neighboring label is below approximately 10% of T. Comparing this arithmetic component with another study's filtered extensive margin cannot establish an opposite behavioral response.

## 3 Design data and estimands

### 3.1 Scenarios and analysis sample

The integrated questionnaire states that the system randomly selects one of nine versions, and each respondent answers only that version. In the delivered data, exactly one of the nine scenario columns is populated per respondent. Cash is a one-time unrestricted payment into a bank account or WeChat/Alipay, available for spending, saving or debt repayment. Food is an electronic voucher restricted to food and daily necessities, valid for six months and noncashable. Medical is a credit to a medical-insurance personal account, usable for the respondent's and family's medical expenses, with long-term validity and accumulating balances. All versions ask about total consumption above the original plan. There is no shared explicit spending horizon across forms. The treatment is assignment to these complete descriptions, rather than to a single economic restriction.

The delivered dataset contains 5,497 responses, including 17 with recorded age below 18. The analysis uses the 5,480 respondents aged 18–100. Table 1 reports the cell counts. Mean recorded age is 33.3 years; 53.0% are women, and 49.2% report a bachelor's degree. Background fields used in the eight-variable balance audit have no missing values in the adult sample. Supplementary tables retain category labels, the 30 observations with a legacy income-band scheme, and city-tier information. City tier does not establish province coverage or national representativeness. None of the eight baseline balance tests rejects after Holm correction; sparse income cells limit the chi-square diagnostic. Balance nonrejection is not proof of correct randomization.

The hosting platform is identified in the available project documentation as Tencent Questionnaire. Recruitment vendor and sampling frame, field dates, survey compensation, invitation/start/completion counts, allocation implementation and formal ethics/consent records have not been verified from the available sources. These items require author documentation before submission. The original integrated questionnaire and data establish scenario wording and delivered counts; they do not establish those collection facts. Excluding recorded minors does not resolve the ethics of their original participation. No claim of an approved or exempt protocol is made here without the corresponding record.

### 3.2 Outcomes and inference

The original categories are essentially no additional consumption; approximately below 10%; 10–25%; 25–50%; 50–75%; and above 75%, each accompanied by yuan examples. The top example ends at the transfer amount even though the verbal threshold is open. We report all six frequencies, the ordinal score 1–6, midpoint codes 0, 0.05, 0.175, 0.375, 0.625 and 0.875, above-bottom-category probability, and the four higher category thresholds. These are seven representations of one answer, not seven independent behavioral measurements. Midpoint-implied yuan is T times the midpoint code and is not observed expenditure.

Trend models regress each representation on form indicators and a log-fivefold amount step, with all form interactions. One step moves from 200 to 1,000 or from 1,000 to 5,000; the linear trend summarizes both intervals. HC3 covariance uses respondent-level outcome dispersion. The 42-test sensitivity includes, for each of seven codings, three within-form trends, a two-degree-of-freedom interaction test, and Cash–Food and Cash–Medical slope contrasts. We report nominal p values, Holm42 and joint Gaussian centered-error min-P42. Scalar tests are converted to normal p values and omnibus statistics to their appropriate chi-square p values before taking the minimum. Joint dependence across outcomes is retained. Min-P uses 10,000 fixed-seed draws and is asymptotic inference, not an exact randomization test. Conservative simultaneous scalar intervals use Bonferroni42. Separate, explicitly identified families apply to the six pairwise incremental-yuan contrasts, three nested affine comparisons, six food-band moderator tests and six ratio restrictions.

The study was not preregistered. Reviewer-stage analyses were fixed after earlier results from the same dataset were known and before these new calculations. Their freezing restricts further analytic flexibility; it does not give them retrospective confirmatory status. Earlier families and response-style sensitivities remain disclosed in the supplement. AI-assisted tools supported drafting and preparation of analysis scripts; estimates were computed by deterministic statistical software and checked against independent respondent-level calculations and aggregate identities. Human author review remains required.

### 3.3 Yuan affine and interval descriptions

We estimate finite incremental implied-yuan responses and endpoint log elasticities from the nine adult cell means. Cell-stratified respondent-equivalent bootstrap intervals use 4,000 draws. The same draws support the affine midpoint regression and its parameter intervals. We compare a common intercept and slope, form intercepts with a common slope, and form intercepts and slopes, reporting HC3 Wald comparisons and lack of fit against saturated cell means.

The interval sensitivity does not invent a numerical boundary between the first two categories. It merges them below 10% conditional on interpreting essentially no increase as below that threshold, retains the three interior intervals, and right-censors above 75%. This mapping imposes an interpretation of approximate wording; it is not coding-free identification. A normal latent-yuan affine model uses a common constant residual scale, with one alternative allowing separate residual scales at the three amounts. Both permit a negative latent lower tail and have no nonnegative structural spending interpretation. Each unrestricted model uses 4,000 bootstrap draws; constrained common-slope fits and all cell-by-category calibration discrepancies are also reported. Calibration, rather than convergence alone, determines whether the model offers a useful summary.

## 4 Distributions shares and implied yuan

### 4.1 Raw responses and first-order contrasts

Figure 1 displays the adult response atlas. The Cash midpoint means at RMB 200, 1,000 and 5,000 are 25.30%, 22.67% and 20.16%; Food means are 22.70%, 19.98% and 19.49%; Medical means are 17.73%, 17.83% and 17.84%. Cash highest-category frequencies decline from 13.43% to 8.95% and 5.34%. Food frequencies are 9.79%, 6.95% and 7.51%, and Medical frequencies 6.03%, 5.24% and 3.94%. The six-bin atlas shows where each mean and threshold result comes from rather than letting the highest category stand in for the entire distribution.

Factorial main effects average equally over the other randomized factor. In the historical adult six-test highest-category family, Medical–Cash is −4.17 percentage points (95% CI −5.84 to −2.51; Holm p<0.001), and Food–Cash is −1.16 points (−2.99 to 0.66; Holm p=0.213). Averaging equally over forms, RMB 5,000 rather than RMB 200 lowers the highest-category frequency by 4.15 points (−5.86 to −2.43; Holm p<0.001). These averaging contrasts answer different questions from unequal size gradients and retain their original disclosed family.

At RMB 5,000, Food exceeds Cash in the highest category by 2.17 points (95% CI −0.63 to 4.97; Holm6 p=0.387 across the historical six amount-specific contrasts). The sign is compatible with a reversal of the small-amount ordering, but the crossing is not precisely established. Lower endpoint frequencies can affect comparisons of absolute probability changes; historical odds-scale checks preserve a larger Cash decline and do not make the form interaction conclusive. Neither a visual crossing nor an overlapping interval establishes equal overall distributions.

### 4.2 The yuan re-expression

Figure 2 displays share and implied-yuan scales together. Cash implied yuan is 50.60, 226.69 and 1,008.19; Food is 45.40, 199.84 and 974.75; Medical is 35.46, 178.27 and 892.15. Multiplication by the assigned amount is arithmetic. The informative comparisons are the incremental responses and their uncertainty, not the observation that a much larger payment implies more yuan.

Table 2 and Figure 3 show those increments. Cash's low-interval estimate is 0.220 [0.193, 0.248], falling descriptively to 0.195 [0.170, 0.220] in the high interval. Food's estimates are 0.193 [0.168, 0.218] and 0.194 [0.169, 0.221]; Medical's are 0.179 [0.156, 0.202] and 0.178 [0.157, 0.201]. The high-interval Cash–Food difference is 0.0016 [−0.0349, 0.0365], and Cash–Medical is 0.0169 [−0.0176, 0.0510]. None of the six pairwise interval contrasts retains Holm6 significance. Similar point estimates describe the cells, while these intervals preclude an equivalence claim. We have no independent economically justified equivalence margin.

Endpoint elasticities are 0.930 [0.887, 0.971] for Cash, 0.953 [0.908, 0.996] for Food, and 1.002 [0.955, 1.046] for Medical. These are descriptive log changes in midpoint-implied yuan between the endpoint amounts. They distinguish a falling finite-transfer share from a nearly proportional yuan response without identifying a derivative or a psychological shift. Form differences in percentage shares are larger at the smallest amount, but absolute implied-yuan gaps need not shrink: Cash–Medical is about RMB 15 at 200 and RMB 116 at 5,000. A claim that all form differences are confined to small transfers would be incorrect.

### 4.3 How useful is the affine benchmark

Table 3 reports the form-specific affine estimates. Midpoint slopes are 0.198 for Cash, 0.194 for Food and 0.178 for Medical. Cash–Food is 0.0046 with bootstrap CI [−0.0273, 0.0348], and Cash–Medical is 0.0197 [−0.0099, 0.0499]. The robust slope-equality test has p=0.381. A common slope is a parsimonious description compatible with these intervals, not a demonstrated equality.

The common-intercept/common-slope model has weighted cell RMSE RMB 30.76 and rejects saturated-cell fit. Allowing form intercepts reduces RMSE to 18.28 (lack-of-fit p=0.178); allowing form slopes as well reduces it to 4.17 (p=0.710). Jointly imposing common intercept and slope is rejected after Holm3 (p=0.000423). The separate intercept restriction has Holm3 p=0.061, and the slope restriction Holm3 p=0.381. These results favor allowing form differences somewhere in the affine description but do not establish that they are exclusively intercept differences. In the unrestricted midpoint model, the fitted Cash intercept is RMB 18.7 [2.7, 35.3], Food 6.4 [−10.1, 22.5], and Medical −0.2 [−14.5, 14.5]. Their interpretation is limited by extrapolation beyond the observed amounts.

The interval sensitivities limit any stronger conclusion. With a constant residual scale, the model converges but misses an individual merged-category probability by as much as 20.81 percentage points. Allowing the scale to vary with amount lowers that maximum discrepancy to 8.78 points but changes the latent slopes from roughly 0.23–0.24 to 0.05–0.10 (Table 3). Slope-equality p values are 0.780 and 0.077, respectively. These are assumption-dependent diagnostic tests. All 8,000 bootstrap fits converge; that numerical result cannot rescue poor calibration or turn latent parameters into realized MPCs. The midpoint scale findings remain useful descriptions of the coded answers, but the interval analysis does not establish coding-robust structural slopes.

### 4.4 Trend inference and the bottom-category decomposition

Table 4 presents the enlarged multiplicity family. The Cash midpoint trend is −2.57 percentage points per fivefold amount step (nominal p=0.000956; Holm42 p=0.0392; min-P42 p=0.0199). The Cash highest-category trend is −4.05 points (Holm42 p=0.000051; min-P42 p=0.000100, the simulation resolution). The ordinal trend is −0.115 categories (nominal p=0.0114), but Holm42 p=0.400 and min-P42 p=0.182. We retain that loss of evidence rather than using its nominal interval as a robustness certificate.

The highest-category cross-form omnibus has nominal p=0.0090, Holm42 p=0.334 and min-P42 p=0.149. Cash–Food and Cash–Medical gradients have Holm42 p=0.422 and 0.147, and min-P42 p=0.192 and 0.0686. Their Bonferroni42 intervals include zero. The observed steeper Cash tail decline remains suggestive across forms, even though the within-Cash coded trend survives correction. The original 21-test family and the expanded 42-test sensitivity are both reported in the supplement, with no claim that either was selected before data collection.

For the midpoint outcome, the mean equals above-bottom-category probability times its conditional-above-bottom mean because the bottom code is zero. A symmetric product decomposition attributes the endpoint Cash change of −5.14 points to a bottom-category component of −0.02 points and a conditional-above-bottom component of −5.11 points. Food components are +0.34 and −3.54 points, and Medical +0.88 and −0.76 points. This is a coding identity. It neither measures exact spending participation nor identifies a causal response among a fixed subgroup, since category selection is affected by assignment. The lowest verbal label and its neighboring percentage threshold also need not represent a common yuan cutoff at different amounts. The decomposition therefore cannot establish a Fuster-style extensive/intensive contrast.

## 5 Predictions and precision

### 5.1 Food expenditure and the sign of bindingness

A sharp simple increasing-bindingness account predicts a more negative Food–Cash size gradient among households for whom a larger voucher is harder to absorb. Let G=1 indicate that six times the lower bound of a respondent's monthly food-expenditure band exceeds RMB 5,000. G=0 fails that proxy condition; it is not observed bindingness. This six-month comparison borrows the Food expiry period and does not supply a common consumption horizon or counterfactual redemption measure. Baseline food alone also omits the daily necessities eligible under the voucher.

Figure 4 plots the raw adult Cash/Food cells within these two groups. Food–Cash highest-category gradients are +8.00 points per fivefold step in G=0 (95% CI 3.83 to 12.18; N=815) and +1.33 points in G=1 (−1.35 to 4.01; N=2,806). G=1 minus G=0 is −6.67 points (−11.63 to −1.71; historical Holm7 p=0.0504). The positive gradient in G=0 is opposite to the sharp negative prediction. It must not be described as exactly predicted or as affirmative evidence that simple increasing bindingness explains the Cash–Food pattern. Imperfect classification, substitution and other restrictions remain possible; this contradiction does not reject every model with binding constraints.

We next use the ordered monthly food band as the frozen continuous moderator, standardized within the 3,621 adult Cash/Food respondents. The highest-category Food–Cash size-gradient moderation is +0.29 points per standard deviation (95% CI −2.33 to 2.91). Adjustment for log mapped income and ordered household size gives +0.44 points (−2.29 to 3.17). The midpoint and ordinal coefficients are also imprecise. All six focal unadjusted/adjusted tests have Holm6 p=1.000. Household size is top-coded at six or more, and income is band mapped, so adjustment does not fully measure household needs or resources.

The ratio-only sensitivity imposes two restrictions: both the common and form-dependent log-amount coefficients must be the negatives of their log expenditure coefficients. Testing only the interaction restriction is insufficient to test that entire model. Under the two frozen food-band mappings, the full restriction has highest-category Holm6 p=0.0426 and 0.0437; corresponding midpoint and ordinal restrictions are rejected more strongly. The historical one-degree-of-freedom nonrejection therefore cannot support a complete ratio-only account. These proxy-based fits do not reject all expenditure-normalized behavior, but they provide no affirmative evidence that a single transfer-to-food ratio organizes the responses.

### 5.2 What the remaining diagnostics can distinguish

The nominal 80% minimum detectable moderation for the unadjusted highest-category food-band test is 3.75 percentage points per standard deviation; a conservative six-test adjustment raises it to 4.65 points. Across the observed 10th–90th food-band span, its pointwise confidence interval permits a change in the Food–Cash size gradient from −6.00 to +7.49 points per fivefold step. Those possibilities are large relative to the adult Cash highest-category slope of −4.05 points. The interval is a range of compatible observational moderation, not a causal fraction of the pattern explained. Nonrejection provides little basis for excluding a category-need mechanism.

Historical income diagnostics reject a pure nominal-only restriction within their original family, while a pure relative-income restriction and income three-way interaction do not retain corrected evidence. Relative scaling improves held-out highest-category prediction by only about 0.12%–0.17% under the two mappings. These small fixed-fold prediction gains do not establish substantive superiority. A predictor comparison and a nonrejected coefficient restriction are different criteria. Neither establishes relative-scale sufficiency nor excludes income-related behavior. The full prediction-and-precision ledger preserves their exact estimands and identifies joint tests for which no unique scalar MDE exists.

Emergency fundraising capacity, income rank and baseline category needs are observational associations, not positive controls validating the survey. Cash amount is itself the studied factor and cannot serve as an independent positive control. The historical income association has the opposite sign to the generic validation prediction, and the emergency-capacity association is marginal after its original correction. These patterns do not imply a failed instrument or a universal mechanism; they show why validation language was too strong. Historical moderator confidence intervals permit substantial changes, and broad observable-screen nonrejections do not establish population homogeneity. The earlier full-delivery associations are clearly separated from the new adult estimates in the supplement.

Q1 and Q2 are response-style screens based on variation across 15 attitude items numbered before the scenario. They are not validated attention checks. The integrated instrument supports treating their component answers as pre-scenario measurements, subject to confirmation of the deployed survey sequence; it does not establish that passing either screen measures comprehension. Historical pass/fail highest-category interaction tests do not detect heterogeneity, but the strict screen leaves only 1,208 adults and wide subgroup intervals. The supplement reports both passed and failed groups. Age-by-education calibration is technically possible but unstable: the uncapped historical adult weights have effective sample size 315 and maximum weight 51.2; capping at 10 leaves effective N=1,191 and a target discrepancy of 16.5 points. Reweighting does not make this convenience sample nationally representative.

## 6 Discussion and conclusion

The experiment provides a concrete comparison of stated response distributions across resource bundles and amounts. Its strongest scale-specific result is a falling Cash midpoint-coded share and highest-category frequency, alongside a nearly proportional increase in implied yuan. Large-amount incremental yuan point estimates are closer across forms, especially Cash and Food, than the share curves alone suggest. Their intervals and the affine comparisons leave meaningful slope differences possible. The findings therefore motivate reporting levels and finite increments together rather than treating a declining share as direct evidence of a declining local MPC.

Perceived spendability remains a candidate interpretation for future measurement. The survey records no direct perceived-spendability scale, intended allocation, mental-account assignment, planning horizon or self-control mediator. A declining Cash share can arise under more than one account, and the Food proxy sign does not support the sharp simple bindingness story. The evidence does not form a sequence of mechanism exclusions ending in a psychological explanation. A follow-up would need to distinguish changes in account assignment and horizon from eligible-spending constraints using direct measures and realized transactions; the current data cannot complete that distinction.

The design also bundles eligible use, expiry, liquidity and account structure. The lack of a common explicit horizon is especially consequential when Food expires after six months while Medical balances persist. Approximate response labels, midpoint coding, unverified recruitment records and uneven sample coverage further constrain interpretation. Censored-normal fit sensitivity makes those coding limits visible rather than eliminating them. These constraints prevent a national spending multiplier or a general ranking of cash and in-kind policy effectiveness from being inferred from the present experiment.

The paper's contribution is thus an empirical comparison with transparent scales and uncertainty. Within this instrument, size and form shape the observed cells, but the expanded family does not establish a general form-by-size interaction. The precision audit distinguishes a contradicted sharp Food prediction from unresolved moderation and an unmeasured interpretation. That distinction is necessary for the stated-response evidence to inform subsequent behavioral work without claiming more than the design identifies.

## Author declarations

Recruitment and field dates, incentives and survey flow, randomization implementation, ethics/consent, funding, competing interests and CRediT statements require verified author information before submission. Data availability: aggregate tables and reproducible analysis scripts are prepared; access to respondent-level data depends on confirmation of consent and sharing permissions. No public-release commitment for those records is made in this draft.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

OpenAI ChatGPT/Codex supported literature checking, manuscript drafting and revision, and preparation of analysis scripts. Statistical outputs were computed with Python libraries, and figures were drawn from aggregate results. The human authors must review and edit the resulting content and confirm responsibility before submission; that review and sign-off are pending in this draft.

## References

{{REFERENCES}}

## Tables and figures

### Table 1 Randomized scenario counts

{design}

Note: Adult N=5,480. Form names denote the complete bundles described in Section 3, including different eligible uses and validity. Counts are rebuilt from the original delivered records.

### Table 2 Incremental implied yuan and endpoint elasticities

{scale}

Note: Increment is the difference in cell mean midpoint-implied yuan divided by 800 or 4,000. Elasticity is log(Y at 5,000 / Y at 200) divided by log(25). Brackets are pointwise 95% percentile intervals from 4,000 cell-stratified bootstrap draws. These are coded stated-response summaries, not observed consumption derivatives. All six pairwise interval comparisons are disclosed in Table S2.

### Table 3 Affine descriptions and scale sensitivity

{afftable}

Note: Brackets are pointwise 95% bootstrap intervals, 4,000 draws per unrestricted model. Midpoint slopes are implied yuan per transfer yuan. Interval slopes are latent-normal parameters under the conditional five-bin mapping and must not be read as realized MPCs. Constant-scale fit has maximum probability error 20.81 points; amount-scale fit 8.78 points. Intercepts extrapolate to zero transfer outside the observed design. Full nested comparisons and interval intercepts, scales and calibration appear in the supplement.

### Table 4 Within Cash and cross form inference in the 42 test family

{family}

Note: Seven codings × three within-form trends, one 2-df omnibus and two Cash pairwise slope contrasts. All 42 nominal/adjusted results and scalar simultaneous intervals are in Table S4. 'At least' labels denote category cutoffs, not exact observed spending amounts. Min-P uses 10,000 centered Gaussian draws with joint influence covariance and p-value normalization by test degrees of freedom.

![Adult six-category response atlas](figures/fig1_response_atlas.png)

Figure 1. Adult response distributions by form and amount. The same sequential light-to-dark palette denotes ascending response categories. The bottom label is verbal and does not establish exact zero spending. All nine cells use the original six categories.

![Shares and implied yuan](figures/fig2_share_and_yuan.png)

Figure 2. Midpoint-coded shares and midpoint-implied yuan. Error bars are pointwise 95% bootstrap intervals from 4,000 draws. Dashed lines in the yuan panel are the form-specific affine midpoint fits. The two panels use different horizontal scales to make the share comparison and yuan increment readable; no derivative is inferred.

![Incremental implied yuan responses](figures/fig3_incremental_response.png)

Figure 3. Finite incremental midpoint-implied yuan responses. Error bars are pointwise 95% cell-stratified bootstrap intervals. Similar point estimates in the high interval do not demonstrate equivalent form responses. Pairwise inference uses the six-test family rather than visual overlap.

![Food subgroup raw cells](figures/fig4_food_raw_cells.png)

Figure 4. Raw highest-category frequencies by the Food lower-bound proxy. G=1 has six times the monthly food-band lower bound above RMB 5,000; G=0 fails that condition. Pointwise normal intervals describe individual cell frequencies. The sharp increasing-bindingness prediction is a negative Food–Cash size gradient in the more-likely-binding group; the G=0 fitted gradient is positive. These groups do not directly measure redemption constraints.
'''
refs=pd.read_csv(O/'JEBO_V3_REFERENCE_AUDIT.csv',dtype=str).fillna('')
refs['sortkey']=refs.authors.map(lambda x:x.split(';')[0].split()[-1])
reftext=[]
for r in refs.sort_values('sortkey').itertuples():
    authors=', '.join(n.split()[-1]+', '+''.join(p[0]+'.' for p in n.strip().split()[:-1]) for n in r.authors.split(';'));pages=str(r.pages);journal=r.journal;vol=str(r.volume).removesuffix('.0')
    if r.id=='N24':journal='NBER Working Paper 35698'
    if r.id=='N25':journal='Deutsche Bundesbank Discussion Paper 13/2023'
    tail=(' '+vol if vol else '')+(', '+pages if pages else '')
    reftext.append(f'{authors}, {r.year}. {r.title}. {journal}{tail}. '+r.primary_url)
main=main.replace('{REFERENCES}','\n\n'.join(reftext))
(M/'JEBO_manuscript_v3.md').write_text(main,encoding='utf8')
# Supplement is numerical and sequential; all full families and original wording.
def fmtframe(df,cols=None,digits=4):
    df=df.copy() if cols is None else df[cols].copy()
    for col in df:
        if pd.api.types.is_numeric_dtype(df[col]):df[col]=df[col].map(lambda x:'' if pd.isna(x) else f'{x:.{digits}g}')
    return mdtable(df)
s=['# Supplement to Transfer size and form in stated spending responses',
'''## S1 Sample measurement and design details

All new calculations use the adult sample N=5,480; the full delivered sample N=5,497 is retained only when explicitly reusing historical fits. Raw respondent records and identifiers are not included in the replication outputs. The original instrument specifies one random scenario per person; exactly one is observed in each delivered record. No allocation probabilities or formal randomization logs were located.

The main article's declarations identify unresolved collection information. Hosting does not establish recruitment, balanced cells do not prove implementation, and adult-only analysis does not validate collection ethics. The authors must supply recruitment frame/vendor, dates, incentives, response flow, stopping and randomization details, approval/exemption and consent records, funding/conflicts, CRediT and sharing permissions.

The mean recorded age is 33.26 years (SD9.37; 10th–90th percentiles23–46). Category counts and original Chinese labels below preserve the two income schemes. Household size code6 denotes six or more, not exactly six. Food expenditure is monthly household food, while vouchers also permit daily necessities. City tier is an ordinal locality descriptor, not observed provincial coverage.''',
'### Table S1a Adult characteristics and missingness\n\n'+fmtframe(pd.read_csv(O/'sample_characteristics.csv'),['variable','category','label','N','missing','mean','sd'],5),
'### Table S1b Baseline randomization diagnostics\n\n'+fmtframe(pd.read_csv(O/'randomization_balance.csv'),['variable','df','p','holm8','min_expected'])+'\n\nNote: Age uses an HC3 omnibus; categorical variables use chi-square diagnostics across nine cells. Eight tests, Holm8. Income has sparse expected cells (minimum0.212); treat that approximation cautiously. No post hoc merging or additional balance search was performed.',
'### Table S1c Adult nine cell scale summaries\n\n'+table(['Form','RMB','N','Ordinal','Share %','Implied yuan','Above bottom %','Highest %'],[[tnames[r.form],int(r.amount),int(r.N),f'{r.ordinal:.3f}',f'{r.midpoint*100:.3f}',f'{r.yuan:.2f}',f'{r.above_bottom*100:.3f}',f'{r.top75*100:.3f}'] for r in cell.itertuples()]),
'## S2 Yuan increments and affine fits',
'### Table S2a Incremental implied yuan contrasts\n\n'+fmtframe(inc,['form','interval','contrast','estimate','bootstrap_lo','bootstrap_hi','p','holm6']),
'### Table S2b Endpoint elasticity and pairwise differences\n\n'+fmtframe(el),
'### Table S2c Midpoint affine parameters\n\n'+fmtframe(aff,['model','parameter','estimate','se','bootstrap_lo','bootstrap_hi']),
'### Table S2d Affine model comparisons\n\n'+fmtframe(pd.read_csv(O/'affine_model_comparison.csv')),
'### Table S2e Predicted and observed midpoint yuan\n\n'+fmtframe(pd.read_csv(O/'affine_midpoint_fit.csv'),['model','form','amount','observed_yuan','predicted_yuan','error']),
'''## S3 Interval affine sensitivity

The bottom category has no numeric separation from the next category. The merged five-category mapping is conditional on essentially no increase lying below10% of the transfer. The interior bounds are approximate; the top wording above75% is right-censored despite a parenthetical example ending at100%. No hard100% cap is imposed. The latent-normal lower tail permits negative values and does not claim that negative or zero actual spending was observed.

The grouped multinomial likelihood uses individual category counts. The primary scale is constant across all cells; the sole sensitivity has one sigma per amount, common across forms. Full form-intercept/form-slope and constrained common-slope models are fitted under each scale. Sandwich covariance uses individual score contributions and the observed Hessian. Both unrestricted models use4,000 independent cell-stratified bootstrap draws. All8,000 converge; the largest normalized observed-fit gradient is6.36×10−7. A fixed neutral-start retry was allowed only for numerical convergence and never changed the model or redrew samples. The per-draw convergence log is retained in aggregate replication files. Calibration is poor enough, and scale sensitivity large enough, to preclude structural interpretation.''',
'### Table S3a Interval parameters and bootstrap precision\n\n'+fmtframe(ip,['model','parameter','estimate','se','bootstrap_lo','bootstrap_hi','bootstrap_valid','bootstrap_failed']),
'### Table S3b Fit diagnostics\n\n'+fmtframe(diag,['model','loglik','slope_equality_p','mean_abs_probability_error','max_probability_error']),
'### Table S3c Merged category calibration\n\n'+fmtframe(pd.read_csv(O/'interval_affine_fit.csv'),['model','form','amount','merged_category','observed_probability','predicted_probability','error'])+'\n\nNote: The complete table reports45 probabilities per model, including both constrained fits. Category labels are below10%,10–25%,25–50%,50–75%,above75%. Errors are predicted minus observed. No numerically successful fit is silently substituted for the primary model.',
'''## S4 Multiplicity timing and historical inference

This study was not preregistered. Earlier analyses and reviewer revisions used the same dataset. The present bounded plan was fixed after those results were observed, before the new calculations. Freezing limits further analytic flexibility but does not retroactively preregister outcomes. The expanded family is a reviewer sensitivity, not a claim that the original findings were confirmed prospectively.

The family has42 tests, exactly seven codings by six tests. All within-form trends and pairwise contrasts use HC3 normal inference; the interaction omnibus uses chi-square2. Joint min-P retains the covariance of all21 within-form slopes across outcomes. Ten thousand centered unrestricted Gaussian-error draws generate a p-value minimum; adjusted probabilities use the plus-one correction. This calibrates degrees of freedom before combining tests and is not sharp-null randomization inference. Bonferroni42 scalar intervals provide conservative95% simultaneous coverage under the normal approximation. Holm and min-P answer family-selection questions; robustness samples and model alternatives are not added into this scientific family.''',
'### Table S4a Complete 42 test family\n\n'+fmtframe(fam,['outcome','test','estimate','p','holm42','minP42']),
'### Table S4b Simultaneous scalar intervals\n\n'+fmtframe(pd.read_csv(O/'family42_simultaneous_intervals.csv'),['outcome','test','estimate','sim_lo','sim_hi']),
'### Table S4c Earlier 21 interaction tests\n\n'+fmtframe(pd.read_csv(PRIOR/'scientific_family21.csv').query("sample=='A'"),['outcome','test','p','holm21','minP21','estimate']),
'### Table S4d Earlier adult factorial main effects\n\n'+fmtframe(pd.read_csv(PRIOR/'main_effects.csv').query("sample=='A'"),['outcome','test','estimate','lo','hi','p','holm6']),
'### Table S4e Earlier amount specific highest category contrasts\n\n'+fmtframe(pd.read_csv(PRIOR/'form_contrasts.csv').query("sample=='A'"),['amount','test','estimate','lo','hi','holm6']),
'''## S5 Bottom category arithmetic

For the midpoint code, E[S]=p×m where p is above-bottom-category probability and m is the conditional-above-bottom mean. Between endpoints0 and1, the symmetric decomposition is ΔE[S]=Δp×(m1+m0)/2+Δm×(p1+p0)/2. We call the terms bottom-category and conditional-above-bottom components. The bottom code is a convention and the underlying verbal response is not an exact zero. Conditioning on a response affected by assignment does not identify a causal effect among a fixed set of respondents. The labels and neighboring percentage thresholds do not impose a common yuan cutoff across amounts. The old decomposition is reproduced arithmetically without repeating the spending-participation interpretation.''']
dec=pd.read_csv(O.parent/'jebo_transition'/'extensive_intensive_decomposition.csv').rename(columns={'p_any_change':'above_bottom_change','conditional_midpoint_change':'conditional_above_bottom_change','extensive':'bottom_category_component','intensive':'conditional_above_bottom_component','extensive_lo':'bottom_lo','extensive_hi':'bottom_hi','intensive_lo':'conditional_lo','intensive_hi':'conditional_hi'})
save(dec,'bottom_category_decomposition.csv');s+=['### Table S5 Bottom category decomposition\n\n'+fmtframe(dec,['form','above_bottom_change','conditional_above_bottom_change','bottom_category_component','conditional_above_bottom_component','total','bottom_lo','bottom_hi','conditional_lo','conditional_hi'])]
s+=['''## S6 Food expenditure prediction and precision

Food−Cash is the sign convention throughout. The sharp prediction was negative in the subgroup more likely to face increasing bindingness. Historical G=0 and G=1 estimates are independently reproduced as positive8.00 and1.33pp, respectively. G=0 is failure of a conservative lower-bound proxy, not observed bindingness. The sharp prediction is contradicted conditional on the proxy, rather than confirmed. No more general bindingness model is thereby excluded.

Continuous models use all lower-order terms in form×amount-step×ordered-food-band. Adjusted models add log mapped income and ordered household size, with their full form and size interactions. Income uses the inherited M1 mapping, while household-size code6 is six or more. Standardization is within adult Cash/Food (N3,621); moderator units and10th/90th percentiles are retained below. Six focal food coefficients use Holm6. Ratio sensitivities use two frozen monthly-food proxy mappings, multiplied by six and logged. These proxy values are not observed exact expenditure. The ratio-only model requires both common and form-dependent coefficient sums to equal zero; the interaction-only restriction is not a complete model test. The one-degree-of-freedom columns apply that historical type of restriction to the new mapped-expenditure sample; the actual earlier lower-bound fit excluded the lowest food band and used N=3,476, with nominal p=0.415 (Holm7=1). These are not identical fits.''',
'### Table S6a Food subgroup raw cells\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_raw_cells.csv'),['G','form','amount','N','ordinal','midpoint','top75','above_bottom']),
'### Table S6a continued Original six category frequencies\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_raw_cells.csv'),['G','form','amount','share1','share2','share3','share4','share5','share6']),
'### Table S6b Sign reproduction\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_sign_reproduction.csv'),['test','N','estimate','lo','hi','p']),
'### Table S6c Continuous unadjusted moderation\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_continuous.csv'),['outcome','estimate','se','lo','hi','sim_lo','sim_hi','p','holm6']),
'### Table S6d Continuous adjusted moderation\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_adjusted.csv'),['outcome','estimate','se','lo','hi','sim_lo','sim_hi','p','holm6']),
'### Table S6e Moderator scaling\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_moderator_coding.csv')),
'### Table S6f Complete ratio restriction tests\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_ratio.csv'),['mapping','outcome','N','df','p','holm6','R2_loss','interaction_only1df_p']),
'### Table S6g Ratio coefficient pairs\n\n'+fmtframe(pd.read_csv(O/'food_bindingness_ratio_coefficients.csv'),['mapping','outcome','term','estimate','lo','hi']),
'''## S7 Prediction and precision ledger

For scalar estimates the nominal80% normal-design minimum detectable effect is (z0.975+z0.8)×SE; the family-adjusted value uses z at1−0.05/(2K). These plug-in quantities do not constitute realized power or justify equivalence. Joint restrictions have no unique scalar MDE. Where moderator and outcome units match, the observed10th–90th span multiplies the coefficient interval and is compared with the matching Cash trend. It is a compatible observational range, not a causal proportion explained.

Historical baseline-moderator fits retain the original full delivered sample N5,497 and full-sample standardization, with a matching full-sample headline slope. They were not rerun or searched. New Food results use adult Cash/Food standardization and the adult benchmark. Joint income and screen nonrejections are retained as restrictions with no manufactured scalar precision. All-X and prediction summaries have different estimands and cannot be converted into percent explained. The ledger separates contradiction, affirmative restriction evidence, lack of affirmative moderation and inadequate precision.''',
'### Table S7a Scalar precision\n\n'+fmtframe(pd.read_csv(O/'MECHANISM_PREDICTION_PRECISION_LEDGER.csv'),['account','N','estimate','lo','hi','family_K','MDE80_nominal','MDE80_family']),
'### Table S7b Compatible moderator ranges\n\n'+fmtframe(pd.read_csv(O/'MECHANISM_PREDICTION_PRECISION_LEDGER.csv').dropna(subset=['moderator_p10_p90_span']),['account','moderator_p10_p90_span','compatible_change_lo','compatible_change_hi','headline_slope']),
'### Table S7c Historical adult mechanism restrictions\n\n'+fmtframe(pd.read_csv(PRIOR/'mechanism_tests.csv'),['test','N','df','p','holm7','estimate','lo','hi']),
'### Table S7d Historical relative income prediction\n\n'+fmtframe(pd.read_csv(PRIOR/'prediction_scores.csv')),
'''## S8 Response style and calibration sensitivity

Q1 requires the within-person SD across15 pre-scenario attitude responses to be at least1 and at least four distinct values. Q2 requires SD at least1.5, at least five distinct values, and no more than80% endpoints (0 or10). Components are life satisfaction, safety, three fairness items, government and social trust, social security, emergency fundraising, support, gain, effort, mobility, voice and pressure. The integrated questionnaire numbers these items before scenario32; confirmation of fielded sequence remains an author item. These are response-style screens, not comprehension or attention tests. Passing can relate to respondent type, and exclusion need not improve validity.

Adult Q1 pass/fail Ns are2,715/2,765; Q2 Ns1,208/4,272. Historical highest-category joint pass/fail interaction p values are0.927 and0.994 (Holm7=1). Subgroup gradients and their intervals below prevent interpreting this as equivalence; the strict screen is especially imprecise. Ordinal results attenuate under the strict screen. The original full grid of sample and outcome robustness remains in the aggregate replication archive without adding it to the scientific42 family.

Age×education post-stratification targets the historical census transcription and does not repair the recruitment frame or selection on unobservables. Uncapped weights have ESS314.84 and maximum51.16; cap10 gives ESS1,190.95 with maximum absolute target discrepancy0.1653. These are historical sensitivity results, not a national estimate.''',
'### Table S8a Passed and failed screen gradients\n\n'+fmtframe(pd.read_csv(PRIOR/'mechanism_details.csv').loc[lambda x:x.test.str.startswith(('Q1 ','Q2 '))],['test','subgroup_N','estimate','lo','hi','p']),
'### Table S8b Screen cell counts\n\n'+fmtframe(pd.read_csv(PRIOR/'screen_cell_counts.csv')),
'### Table S8c Historical calibration diagnostics\n\n'+fmtframe(pd.read_csv(PRIOR/'calibration_diagnostics.csv')),
'## S9 Original questionnaire and English translation\n\n'+(O/'QUESTIONNAIRE_APPENDIX.md').read_text(encoding='utf8').replace('# Exact questionnaire appendix\n','').replace('## ','### '),
'## S10 Replication definitions and declarations\n\nFixed seeds are2026100417 for cell/midpoint bootstrap,2026100418 for interval bootstrap, and2026100419 for the10,000 joint min-P draws. All new bootstrap cells retain their observed sizes. Original data are hash-verified against the earlier freeze; no individual records are exported. The aggregate numerical package contains exact estimates, covariance, calibration and draw-level convergence summaries, together with analysis scripts. Outcome identifiers in machine-readable tables may retain legacy names for continuity; the displayed interpretation is always above-bottom-category rather than observed participation. Author metadata and human review of the AI-assisted preparation remain pending as stated in the main draft.']
(M/'JEBO_supplement_v3.md').write_text('\n\n'.join(s)+'\n',encoding='utf8')
print('Abstract words',len(abstract.split()),'main words',len(main.split()),'supp words',len(' '.join(s).split()))
