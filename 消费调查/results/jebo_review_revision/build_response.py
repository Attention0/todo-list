from common import *
import shutil
M=ROOT/'manuscript'/'jebo_v3'
letter='''# Response to the reviewer driven JEBO revision

This letter addresses the eight substantive issues and the bounded analyses in the supplied revision specification. We accept the scale, sign and measurement criticisms and have changed the central description accordingly. The revision distinguishes the observed six-category answers, midpoint-implied yuan, assumption-dependent affine parameters and unresolved mechanisms. No further outcomes, moderators or alternative censoring rules were explored. Author collection metadata remain pending, so this is a draft revision rather than a submission-ready package.

## 1 Spending share versus implied yuan

**Assessment.** Correct. A declining coded share does not establish weak incremental yuan spending or a declining local MPC. The previous emphasis on the Cash share curve underdeveloped this distinction.

**Existing and new evidence.** Adult cells were independently rebuilt from the original data (all54 counts agree). Cash implied yuan is50.60/226.69/1008.19 at the three amounts. New4,000-draw bootstrap results give Cash interval increments0.220 [0.193,0.248] and0.195 [0.170,0.220], Food0.193/0.194 and Medical0.179/0.178. All six pairwise interval tests lose Holm6 significance. Endpoint elasticities are0.930/0.953/1.002, with uncertainty disclosed.

**Revision.** Main Sections2.1 and4.2, Table2 and Figures2–3 now distinguish share, implied yuan, finite increments and elasticity. The abstract reports both scales. Implied yuan growth alone is no longer advertised as a substantive discovery.

**Boundary.** We do not accept a stronger claim of demonstrated large-amount equivalence or confinement of all form differences to small transfers. High-interval Cash–Food CI is[−0.0349,0.0365], and Cash–Medical[−0.0176,0.0510]. Absolute Cash–Medical implied-yuan gaps grow with amount. Neither visual convergence nor overlapping intervals provides an equivalence test.

## 2 The affine benchmark

**Assessment.** Correct that constant yuan is an uninformative straw benchmark. Existing midpoint means suggested an affine comparison but could not establish it without uncertainty and fit checks.

**New evidence.** The midpoint full model slopes are Cash0.198/Food0.194/Medical0.178. The common-slope restriction has p=.381; simultaneous common-intercept/common-slope restrictions reject (Holm3=.000423). The separate intercept restriction has Holm3=.061. A form-intercept/common-slope fit has RMSE18.28 and saturated-cell lack-of-fit p=.178; the full model RMSE4.17,p=.710. Pairwise slope and intercept confidence intervals remain broad.

**Interval analysis.** The original questionnaire provides no numeric bottom-category boundary. We published its audit before fitting, merged categories1+2 below10% conditionally, and used a right-censored top above75%, disclosing its75–100% example. Four fits (full/common slope × constant/amount-specific scale) and all180 merged probabilities are reported. Both full models complete4,000 bootstrap draws with no failures. The constant-scale model has maximum category error20.81pp; the alternative improves it to8.78pp but changes latent slopes markedly. Numerical convergence does not establish validity.

**Revision and withdrawal.** Section3.3 explains the estimands and mapping; Section4.3 and Table3 report fit/uncertainty. Constant-yuan exclusion is removed from the narrative. Equal slopes, an intercept-only mechanism, coding-robust latent MPCs and psychological meanings for zero-transfer intercepts are not claimed. The review's stronger parsimonious story remains a compatible description, not a proven decomposition of form effects.

## 3 Spendability is not measured

**Assessment.** Correct. The read-only local v2 title uses 'Transfer Size and Spendability' and later promotes a spendability synthesis. The repository v1 was already more qualified in some places; we do not attribute the exact local-v2 wording to every previous version.

**Revision.** The selected title is 'Transfer size and form in stated spending responses'. Spendability is removed from title, abstract, keywords and causal conclusions, and appears only in Discussion as a candidate for future direct measurement. There are no measures of perceived spendability, intended allocation, mental-account assignment, common planning horizon or self-control mediators. A mechanism funnel is removed. The four figures show distributions, scales, increments and Food raw cells.

**Boundary.** A plausible behavioral interpretation is not a measured construct or causal mediation result. No existing result can supply the missing mediator.

## 4 Food bindingness sign and proxy interpretation

**Assessment.** Correct. The local-v2 statement 'exactly in the direction predicted' was an error. We acknowledge the sign error directly: under the sharp increasing-bindingness account, Food−Cash size slope should be negative in the more-likely-binding group. The observed positive slope is opposite to that prediction.

**Reproduction and new analysis.** Adult Cash/Food N3,621. G=1 iff six times the monthly food-band lower bound exceeds5000; G=0 merely fails that condition. The independently reproduced gradients are+8.00pp [3.83,12.18] for G=0,N815 and+1.33pp [−1.35,4.01] for G=1,N2806. G1−G0 is−6.67pp [−11.63,−1.71], historical Holm7=.0504. Figure4 and TableS6 report all12 raw cells and all six response bins.

**Continuous precision.** Ordered food-band moderation of the highest-category gradient is+0.29pp perSD [−2.33,2.91], adjusted+0.44pp [−2.29,3.17]. The frozen three outcomes by two versions all have Holm6=1. Nominal80% MDE for the primary coefficient is3.75pp perSD; the six-test conservative value4.65pp. The observed10th–90th span permits changes of−6.00 to+7.49pp, so meaningful moderation remains unresolved.

**Ratio correction.** A complete ratio-only model requires both common and form-dependent log-amount/log-food coefficient sums to be zero. The new two-degree-of-freedom highest-category tests yield Holm6=.0426/.0437 for M1/M2; midpoint/ordinal restrictions reject more strongly. The earlier interaction-only test did not test the whole model and used a different lower-bound sample N3476. New analogous one-degree-of-freedom values are labelled separately; the historical p=.415,Holm7=1 remains archived.

**Revision and boundary.** Sections5.1–5.2 replace affirmative bindingness language with a contradicted sharp proxy prediction and imprecise continuous moderation. Food includes daily necessities as well as food, and G does not observe counterfactual redemption or a uniform consumption horizon. These limitations prevent rejection of every bindingness model; they do not justify reversing the sharp prediction to fit the result.

## 5 Bottom category and decomposition

**Assessment.** Correct. The bottom response is verbal 'essentially no additional consumption', with form-specific saving/debt wording. It is not an observed exact zero. Above-bottom is not a clean probability of spending anything; the lowest positive percentage label also changes its yuan meaning with T.

**Existing evidence and revision.** The product identity is unchanged, but the terms are renamed bottom-category component and conditional-above-bottom component. Cash endpoint total−5.14pp decomposes into−0.02/−5.11pp. Sections2.3 and4.4 and TableS5 explain why conditioning on a treatment-affected answer is not a causal comparison of fixed spenders. All manuscript displays use measurement-faithful language; legacy code identifiers remain only for replication continuity.

**Withdrawal.** We remove claims that larger Cash fails to discourage actual participation or that the decomposition demonstrates a Fuster-style extensive/intensive contrast. Fuster's instrument and filtered adjustment margin differ. Approximate labels, missing exact-zero boundary and differing horizons are substantive reasons the reviewer-proposed cross-study comparison cannot be interpreted causally.

## 6 Null moderators and mechanism precision

**Assessment.** Correct. Nonrejection does not establish absence, homogeneity or equivalence. Earlier income, emergency-capacity, category-need, screens and broad observable results cannot form an exclusion funnel.

**New ledger.** Each specified account has a prediction, result status, source, sample/units, CI, scalar80% MDE where valid and conservative family value. Observed moderator spans translate CIs into compatible gradient changes only when units match. Joint restrictions have no unique scalar MDE; prediction summaries and observational moderation are not manufactured into causal percent explained. Historical baseline-moderator fits retain N5497 and matching full-sample standardization/benchmark, explicitly separated from adult Food analyses.

**Revision.** Section5 and TablesS7 distinguish a contradicted sharp prediction, an affirmative restriction rejection, absence of affirmative moderation and insufficient precision. No generic mechanism is ruled out by a null. Emergency fundraising and income associations are renamed descriptive associations, not positive controls. Cash size is the studied factor, and the income sign is opposite the generic validation prediction. The strict Q2 screen has broad intervals and is not privileged as a validity guarantee.

## 7 Timing and expanded multiplicity

**Assessment.** Correct. The study was not preregistered. Follow-ups were frozen only after earlier same-data results, before their own execution. Main and supplement state this explicitly, with no unqualified confirmatory status or internal development language.

**42-test results.** Seven outcomes × three within-form trends, one2-df omnibus and two Cash pairwise contrasts. Holm42 and joint min-P42 use the existing estimands and HC3 covariance. Cash midpoint retains evidence (Holm=.0392,min-P=.0199), Cash highest-category retains evidence (.000051/.000100), Cash ordinal does not (.400/.182). Highest-category omnibus becomes .334/.149; Cash–Food .422/.192 and Cash–Medical .147/.0686. Conservative scalar simultaneous intervals include zero for cross-form contrasts. All42 rows and the old21 family are disclosed.

**Method boundary.** P-value normalization combines tests with their correct null degrees of freedom, avoiding incompatible raw Wald scales. Gaussian centered-error min-P is asymptotic, not exact randomization inference. Robustness sample/model variants are documented separately. Expansion weakens some claims; no new family or model is chosen to recover significance. The historical old300-model correction remains history rather than the new primary scientific number.

## 8 Methods collection records and outlet positioning

**Assessment.** Correct that the methods need complete study records. We read the original questionnaire/data labels, existing repository evidence and local study drafts. Formal recruitment, ethics and fieldwork records were not found; prior draft assertions are not independent documentation. An author question was sent, and missing fields are listed without invented facts.

**Delivered detail.** Adult characteristic/missingness and eight-test balance tables, current/legacy income counts, exact household/food labels, all nine Chinese scenarios plus complete English translation, and Q1/Q2 definitions with both passed/failed results are supplied. The15 screen items are numbered before the scenario; actual deployed ordering still needs author confirmation. They are response-style screens, not validated attention checks. The existing age×education calibration is feasible but unstable (uncapped ESS315,max weight51.2; cap10 ESS1191,target gap16.5pp) and cannot supply representativeness.

**Literature.** Ten priority papers are currently checked using primary sources and bounded prior source audits. Shapiro–Slemrod is included; Parker–Souleles is restricted to actual-rebate measurement evidence. Fuster's different elicitation, heterogeneous size patterns in Andreolli–Surico, Crossley's wording effects, Bernard's prior joint design and Bonomo's food-store rather than total-consumption outcome are discussed. Boehm's realized transfers and the Lee/Pauls JEBO comparators define the contribution boundary. Working papers are labelled. There is no first-joint-design or measured-spendability novelty claim.

**Journal format and unresolved facts.** Numbered sections, author-year bibliography, compact main tables and four figures are supplied as editable Word plus source text and aggregate figure data. The official JEBO guide returned403 during refresh; an abstract under250 words is a conservative preparation choice, not a falsely verified live rule. Elsevier's primary AI policy is verified and its declaration section included before references. Human authors' review/responsibility confirmation is pending. Recruitment/date/incentive/randomization/ethics/consent/funding/conflict/CRediT/data-sharing fields are explicit author requirements. These facts cannot be completed from the response distributions, and the package remains a draft.

## Claims retained and withdrawn

Retained: the adult six-bin distributions; coded Cash share/highest-category trends with42-test uncertainty; incremental midpoint-implied yuan and elasticities; an assumption-bound affine description; corrected Food proxy sign; precision limits. Withdrawn or downgraded: measured spendability, structural/local MPC interpretation, complete mechanism exclusion, actual spending participation, Fuster margin priority, affirmative simple-bindingness, full ratio support from an incomplete restriction, universal size gradients, national representativeness, equal slopes and all-form convergence. This revision repairs the estimands and evidence rather than strengthening the story through additional exploration.
'''
(M/'RESPONSE_TO_JEBO_REVIEW.md').write_text(letter,encoding='utf8')
claims=[
('Adult sample','5480','adult_share_yuan_table.csv','3.1; Table1','Observed delivered adults; recruitment/ethics unresolved'),
('Cash share endpoint','25.29935% to20.16379%','adult_share_yuan_table.csv','4.1','Midpoint coding, hypothetical'),
('Cash implied yuan','50.60 to1008.19','adult_share_yuan_table.csv','4.2','Arithmetic re-expression, not observed'),
('Cash increments','.220113/.195375','incremental_yuan_response.csv','Abstract;4.2;Table2','Finite increments not derivatives'),
('Food increments','.193048/.193728','incremental_yuan_response.csv','4.2;Table2','Conditional on midpoint coding'),
('Medical increments','.178522/.178470','incremental_yuan_response.csv','4.2;Table2','Conditional on midpoint coding'),
('High interval Cash-Food','.001647 CI−.034856,.036539','incremental_yuan_response.csv','4.2','No equivalence'),
('High interval Cash-Medical','.016905 CI−.017565,.050990','incremental_yuan_response.csv','4.2','No equivalence'),
('Elasticities','.929513/.952716/1.002010','endpoint_elasticity.csv','4.2','Descriptive log endpoint change'),
('Midpoint affine slopes','.198224/.193651/.178476','affine_midpoint_parameters.csv','4.3;Table3','No structural MPC'),
('Affine slope equality','p=.381295','affine_model_comparison.csv','4.3','Nonrejection not equal slopes'),
('Affine joint common restriction','Holm3=.000423','affine_model_comparison.csv','4.3','Does not establish intercept-only explanation'),
('Interval fit sensitivity','max probability errors20.81/8.78pp','interval_affine_diagnostics.csv','4.3','Constant-scale misspecification; latent slopes unstable'),
('Interval bootstrap','8000 successful draws','interval_bootstrap_status.csv','3.3;4.3','Convergence not validity'),
('Cash midpoint42','Holm=.039176,minP=.019898','scientific_family42.csv','4.4;Table4','Coding-specific evidence'),
('Cash ordinal42','Holm=.399504,minP=.181782','scientific_family42.csv','4.4;Table4','No adjusted evidence'),
('Cash Top7542','Holm=.000051,minP=.000100','scientific_family42.csv','4.4;Table4','MinP simulation resolution'),
('Top75 interaction42','Holm=.333939,minP=.148585','scientific_family42.csv','4.4','Suggestive, not established'),
('Food crossing','Food-Cash2.1677pp CI−.6311,4.9665','nc_evidence_revision/form_contrasts.csv','4.1','Historical Holm6=.387; no precise crossing'),
('Factorial main effects','Medical−Cash−4.1738pp;5000−200−4.1479pp','nc_evidence_revision/main_effects.csv','4.1','Balanced averages; historical family6'),
('Bottom decomposition','−.0211/−5.1144pp Cash','bottom_category_decomposition.csv','4.4;S5','Code identity, not participation or causal conditional effect'),
('Sharp Food sign','Food−CashG0+8.0049pp/G1+1.3322pp','food_bindingness_sign_reproduction.csv','5.1','Opposite sharp prediction, proxy limitations'),
('Continuous Food','Top75.002893/.004387;Holm6=1','food_bindingness_continuous.csv;food_bindingness_adjusted.csv','5.1','Observational moderation not absence'),
('Full Food ratio','Top75Holm6=.042601/.043721','food_bindingness_ratio.csv','5.1','Joint2df; proxy models, old1dfdifferent sample'),
('Food precision','MDE3.7452/4.6520pp;spanCI−6.0045,+7.4949pp','MECHANISM_PREDICTION_PRECISION_LEDGER.csv','5.2','Compatible range not causal explained share'),
('Relative income gain','.1716%/.1245% REL versus ABS','nc_evidence_revision/prediction_scores.csv','5.2','Small fixed-fold predictive gains, not model proof'),
('Q1/Q2','pre-numbered15items;N2715/1208','mpc_size_curve/size_curve.py;nc_evidence_revision/screen_cell_counts.csv','5.2;S8','Response-style screens; deployment order confirm'),
('Reweighting','ESS314.84/cap1190.95,target gap.16526','nc_evidence_revision/calibration_diagnostics.csv','5.2','No representativeness'),
('Spendability','No direct measure','QUESTIONNAIRE_APPENDIX.md','6','Discussion candidate only'),
('Metadata','Formal records not located','STUDY_METADATA_AUDIT.md','3.1;Declarations','Author confirmation required'),
('Novelty','Bernard joint form×size predates study','JEBO_V3_REFERENCE_AUDIT.csv','1;2','Narrower design extension, no priority'),
('Timing','Not preregistered; fixed after prior same-data results','REVIEWER_REANALYSIS_MANIFEST.md','3.2;S4','No retroactive confirmatory status'),
('AI declaration','Tool purposes disclosed; human signoff pending','JOURNAL_REQUIREMENTS_AUDIT.md','Before References','No invented author certification')]
save(pd.DataFrame(claims,columns=['claim','value','source','location','boundary']),'JEBO_V3_CLAIM_LEDGER.csv');shutil.copyfile(O/'JEBO_V3_CLAIM_LEDGER.csv',M/'JEBO_V3_CLAIM_LEDGER.csv')
matrix=(O/'REVIEW_ISSUE_MATRIX.md').read_text(encoding='utf8')
if '## Execution disposition' not in matrix:
    matrix+='\n\n## Execution disposition\n\nAll numbered scientific corrections and bounded analyses completed. Source-specific v2 sign/title/decomposition quotations are verified in LOCAL_V2_CLAIM_AUDIT.md. New numerical families and all four figures are complete. AFFINE_RESPONSE_RESULT, FAMILY42_RESULT, FOOD_BINDINGNESS_RESULT and the precision ledger supply the results. Main/supplement now reside only in jebo_v3. Author collection records and live JEBO portal checks remain pending, explicitly listed in AUTHOR_INFORMATION_REQUIRED.md; no empirical extension is authorized to fill those gaps. Final numerical/protection and visual verification are recorded in FINAL_AUDIT.md.\n'
    note('REVIEW_ISSUE_MATRIX.md',matrix)
print('Response covers eight issues plus multiplicity, literature and submission metadata;33 claims traced.')
