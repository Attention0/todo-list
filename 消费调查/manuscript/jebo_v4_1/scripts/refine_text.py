"""Deterministic editorial transformations of PR20 text. No empirical computation."""
from pathlib import Path
import re

M=Path(__file__).resolve().parents[1]
B=M.parent/'jebo_v4'
s=(B/'JEBO_manuscript_v4.md').read_text(encoding='utf8')
def section(start,end,new):
    global s
    a=s.index(start);b=s.index(end,a)
    s=s[:a]+new.strip()+'\n\n'+s[b:]
def replace(old,new):
    global s
    assert old in s,old[:80]
    s=s.replace(old,new,1)

section('## Abstract','Keywords:', '''## Abstract

Does transfer form matter equally at small and large amounts? A randomized survey experiment assigns 5,480 adults in China to Cash, Food-voucher or Medical-account transfers of RMB 200, 1,000 or 5,000. In the observed cells, Cash spending shares decline with amount, Food declines less, and Medical remains nearly flat; mean differences between forms shrink sharply. The distributions reveal different paths toward these closer means. Cash's highest-response category contracts while its bottom category remains stable. Food shows broader redistribution, and Medical combines offsetting category movements behind a flat mean. Midpoint-implied yuan rises strongly across all three forms, locating the puzzle in allocation shares. A sharp prediction that increasing Food restrictions steepen its decline relative to Cash has the opposite observed sign under an expenditure proxy. Broader need and resource diagnostics are inconclusive at the available precision. Formal cross-form interaction evidence remains uncertain after multiplicity adjustment. We organize the joint pattern around resource categorization: small cash receipts may invite current spending, larger sums broader allocation, and earmarked resources allocation around designated uses. This interpretation concerns hypothetical stated responses to bundled scenarios; the categorization process is not directly measured.''')

section('## 1 Introduction','## 2 Conceptual', '''## 1 Introduction

Does the form of a transfer matter equally when transfers are small and large? Households decide both how much of an unexpected resource to spend and what purposes that resource should serve. A small cash payment can enter everyday purchases; a food voucher arrives with an eligible use; a medical-account balance can remain available for future care. Increasing each from a modest receipt to a substantial sum may change its place in the household budget. Our question is how the contrast between these forms varies with amount, and which parts of the spending-response distribution account for that variation.

A declining finite-windfall spending share is compatible with consumption smoothing and liquidity-based reasoning. A small receipt can finance a pressing purchase, whereas a larger receipt can also replenish savings or cover future needs (Friedman, 1957; Jappelli and Pistaferri, 2010; Kaplan and Violante, 2022). That familiar Cash logic does not by itself explain a flat Medical mean, a gentler Food decline, or sharply narrowing mean gaps between forms. These comparisons introduce questions about eligible uses, substitution and how recipients categorize resources. They also distinguish our question from a search for a universal negative relationship between cash amount and spending share.

We study a randomized survey experiment crossing Cash, Food and Medical transfers with RMB 200, 1,000 and 5,000. Each of 5,480 adults in China answers one hypothetical scenario using six ordered categories of additional total consumption. The midpoint-coded means present three puzzles. First, Cash declines from 25.30% to 22.67% and 20.16%, while Medical remains nearly flat at 17.73%, 17.83% and 17.84%. Second, Food declines less than Cash, from 22.70% to 19.98% and 19.49%, despite the intuition that larger restricted transfers become harder to absorb. Third, mean form differences narrow sharply: the Cash–Medical gap falls from about 7.6 to 2.3 percentage points, and the Cash–Food gap ends below one point. Figure 1 presents the nine underlying distributions. These observed-cell patterns define the puzzles addressed in the paper.

The convergence is in spending shares, not in the disappearance of absolute spending responses. Multiplying each midpoint-coded share by the transfer amount gives implied additional yuan. Cash rises from about RMB 51 to RMB 1,008; Food from RMB 45 to RMB 975; and Medical from RMB 35 to RMB 892. Figure 2 places the scales side by side. A declining share can thus accompany a large increase in implied spending, and a narrowing share gap need not imply a narrowing yuan gap. The economic question concerns how respondents divide a windfall relative to its size.

The distributional anatomy makes that question more precise. Cash's highest-response frequency falls from 13.43% to 5.34%, while its bottom frequency stays near 27.4%. Food shows a smaller top contraction and more diffuse reallocation across the middle. Medical's flat mean combines a shrinking bottom and top with growth in intermediate categories. At RMB 5,000, all three forms have approximately 24% in the 10–25% category, yet their bottom and upper frequencies remain different. Figure 3 makes these distinct paths visible. Mean convergence therefore coexists with different distributional profiles. These comparisons are between independent respondent groups, rather than individual transitions across amounts.

We then ask increasingly demanding questions of this configuration. Ordinary size dependence provides the Cash benchmark; the yuan scale clarifies the allocation problem; bottom-category arithmetic locates the Cash decline away from its lowest response. A sharper account predicts that growing Food restrictions should make its size gradient more negative relative to Cash where eligible expenditure is low. Under the available expenditure proxy, the observed sign is the opposite. Category need, relative income, liquidity and observable household characteristics offer broader explanations, but the available diagnostics do not distinguish them decisively. The sequence identifies what an explanation must accommodate, rather than selecting a mechanism by elimination.

We propose resource categorization across scale as the most coherent organizing interpretation of the joint pattern. Small Cash may be readily assigned to current purchases, while a larger receipt invites a broader decision over consumption, saving, debt and future needs. Food and Medical already carry designated uses. Their mean shares may consequently change less with amount, with Medical's persistent balance allowing different needs to produce offsetting responses. The account connects the distinctive high-response mass for small Cash to the closer means at large amounts. It is an interpretation of the configuration, not a tested ranking of mechanisms: the survey contains no direct measure of categorization or perceived spendability.

The inference distinguishes the observed configuration from a general form-by-size effect. Cash's midpoint and highest-category trends survive adjustment across 42 comparisons; its ordinal trend does not. Cross-form interactions remain uncertain after that adjustment. The strongest statistical evidence is therefore within Cash, while the comparative puzzles concern the observed cells. This distinction guides the analysis without reducing its substantive object to a single coefficient.

The contribution connects evidence on transfer size with evidence on the meaning and use of resources. Fagereng et al. (2021) relate lottery responses to balance sheets; Fuster et al. (2021) find increasing responses to hypothetical gains through their elicited spending-adjustment margin; Andreolli and Surico (2026) document differing size responses across household resources. Jappelli et al. (2026) connect gain size to the timing of intended consumption. Our comparison adds Food and Medical bundles and shows how similar average shares can arise through sharply different category patterns. A direct percentage-bin response describes a different object from Fuster et al.'s filtered adjustment margin.

Mental accounting and budgeting provide a language for those allocation differences (Thaler, 1985, 1999; Shefrin and Thaler, 1988; Heath and Soll, 1996). Labeling studies examine the uses attached to resources (Kooreman, 2000; Abeler and Marklein, 2017), while cash and in-kind studies distinguish eligible-category expenditure from broader consumption (Cunha, 2014; Hastings and Shapiro, 2018; Kan et al., 2017). Bernard (2023) already studies payment mode jointly with shock size. Building on that joint question, our three-amount comparison gives the full response distribution a central role in explaining the Cash, Food and Medical paths.

Real-transfer studies anchor this question in observed behavior. Boehm et al. (2025) compare cash-like and rapidly expiring transfers using realized consumption, and Bonomo et al. (2026) study food-store spending across programmes with different forms and timing. They provide stronger evidence about actual spending; our stated total-consumption distributions address a different outcome and set of resource bundles. Within JEBO, Lee et al. (2024) connect mobile money's social meaning to willingness to spend, and Pauls and Laudi (2025) study temporal framing of a permanent tax cut. Their common concern with resource representation motivates our question about how form and amount jointly shape stated allocation.

Elicitation research defines the scope of that contribution. Shapiro and Slemrod (2003) and Parker and Souleles (2019) study reports about actual rebates; Ueda (2025) examines linked survey and transaction responses in another setting. Crossley et al. (2026) show that direct and filtered questions produce different distributions and relationships with size, horizon and liquidity. We therefore study the allocation expressed through this particular direct-bin instrument. Sections 2 and 3 describe the conceptual setting and design. Sections 4 and 5 establish the puzzles and their anatomy; Sections 6 and 7 develop the explanation and interpretation. Sections 8 and 9 discuss the implications and conclude.''')

replace('Bernard (2023) already studies payment modes jointly with shock size, making a claim of a first form-by-size experiment inappropriate.', 'Bernard (2023) studies payment modes jointly with shock size, demonstrating the relevance of considering these two dimensions together.')
replace('These checks neither verify allocation implementation nor establish representativeness. Supplement S1 retains category labels, city-tier information and the 30 observations with a legacy income-band scheme.', 'Supplement S1 reports the balance diagnostics, category labels, city-tier information and the 30 observations with a legacy income-band scheme.')
replace('The available documentation identifies Tencent Questionnaire as the hosting platform. Verified recruitment, fieldwork, allocation-implementation and ethics details are pending author documentation. The analysis sample and instrument can be described from the delivered materials, but neither the recruitment frame nor a nationally representative sampling claim can be established from them. The separate draft-only author note lists the required records, including consent and the circumstances of participation by recorded minors.', 'Tencent Questionnaire hosted the survey. Recruitment, fieldwork dates, allocation implementation and ethics/consent records await author confirmation. The sample is not established as nationally representative; Supplement S1 describes the available documentation and outstanding collection information.')
section('Trend models use form indicators', '## 4 Three puzzles', '''Trend models interact form with a log-fivefold amount step: RMB 200 to 1,000 and RMB 1,000 to 5,000 are each one step. The 42-test family combines seven codings with three within-form trends, a cross-form omnibus interaction and two Cash–restricted-form contrasts. We report heteroskedasticity-robust estimates with Holm and joint min-P adjustments. Supplement S3 gives the complete family, earlier interaction tests and simultaneous intervals.

The study was not preregistered. Additional analyses were specified after earlier results were known and before their calculation; Supplement S3 records that sequence. The resulting correction addresses outcome and contrast choice without conferring prospective confirmatory status.

### 3.3 Scales and explanatory comparisons

We compare midpoint shares, their implied yuan values and finite increments between amounts. Cell-stratified bootstrap intervals use 4,000 draws. Affine fits summarize the yuan profiles, and interval-censored sensitivities examine dependence on coding and residual scale (Supplements S4–S5). These are descriptive representations of stated responses.

Explanatory comparisons use the specified Food-expenditure proxy and continuous moderator, followed by category need, income, liquidity and observable characteristics. Supplements S6–S8 retain the model definitions, correction families, sample differences and precision summaries. The comparisons ask how well these measured characteristics organize the pattern across transfer amounts and forms.''')
replace('These cell comparisons motivate the question of form-specific size responses without themselves establishing a population interaction or equivalence at the large amount.', 'Food occupies an intermediate mean path, while the Cash and Medical means approach one another from very different starting levels.')
replace('The atlas also cautions against treating the two restricted forms as a single treatment.', 'The atlas shows why the two restricted forms warrant separate attention.')
replace('Figure 2 displays the midpoint share and its implied-yuan counterpart with the original pointwise bootstrap intervals.', 'Figure 2 displays midpoint shares and implied yuan with pointwise bootstrap intervals.')
replace('from the existing 4,000 cell-stratified bootstrap draws', 'from 4,000 cell-stratified bootstrap draws')
section('Over RMB 1,000–5,000,', '### 4.3', '''Over RMB 1,000–5,000, finite incremental implied-yuan responses are numerically close, especially for Cash and Food. Their difference is 0.00165 yuan per transfer yuan, with a 95% interval of −0.03486 to 0.03654. The interval allows both similar and meaningfully different responses; equal slopes are not established. Supplement S4 reports all six interval-specific pairwise comparisons, none of which rejects after Holm adjustment.''')
replace('A mean decline measured through midpoint distances is therefore better supported than a coding-independent claim that every aspect of the distribution shifts downward.', 'The evidence for the coded mean and the highest category is stronger than the evidence for the ordinal-score trend. These are distinct summaries of one categorical response; none is a test that every aspect of the distribution shifts downward.')
section('The cross-form highest-category omnibus', '## 5 Anatomy', '''The highest-category omnibus and both focal cross-form contrasts do not survive the expanded correction; both scalar contrasts have simultaneous intervals containing zero. A steeper Cash tail decline is therefore suggestive despite the detectable within-Cash trend. Medical's near-flat mean and the narrowing mean gaps remain features of the observed cells. The following anatomy explains how those cell means arise.''')
replace('The resulting distribution is more nuanced than a uniform shift of each respondent toward a smaller answer.', 'The contraction at the top coexists with increases in several lower categories, including 50–75%.')
section('The bottom-code identity helps locate', '### 5.2', '''The coded mean equals the probability of an above-bottom answer times its conditional mean code. The symmetric decomposition attributes −0.02 points of Cash's −5.14-point endpoint change to the probability component and −5.11 points to the conditional-code component, with rounding. Almost all the coded decline therefore lies among the above-bottom categories. This is an arithmetic decomposition of independent cells, not a causal participation or intensive-margin estimate (Supplement S2).''')
replace('The earlier amount-specific contrast is imprecise, so the crossing cannot establish superior spending effects of vouchers. It does show why a simple description of uniformly lower restricted-form responses misses part of the observed pattern.', 'The amount-specific contrast is imprecise (Supplement S3), but the observed crossing makes a simple description of uniformly lower restricted-form responses incomplete.')
replace('Conversely, these descriptive offsets do not establish a population distributional change or identify which respondents would change their answers. They supply a more informative target for a theory or a future experiment than mean invariance alone.', 'The offsets supply a more informative target for explanation than mean invariance alone.')
replace('This common concentration helps the mean shares approach one another. Yet bottom frequencies', 'The similar middle-category frequencies coexist with bottom frequencies')
replace('remain 27.41%, 30.05% and 35.49%, and highest-category frequencies remain', 'of 27.41%, 30.05% and 35.49%, and highest-category frequencies of')
replace('The mean shares converge strongly, but the distributions do not become identical. This statement describes the cell profiles; it is not a new formal equality or inequality test.', 'The mean shares converge strongly in the observed cells, but the distributions do not become identical.')
section('Together, the three paths sharpen', '## 6 What', '''The central empirical fact is therefore not merely that the three means move closer. It is that Cash, Food and Medical arrive at those closer means through different distributional paths. An account of Cash's top contraction alone misses Medical's offsets; an account of lower restricted-form levels alone misses Food's gentler decline. These differences set the questions for the explanation that follows.''')

section('## 6 What', '## 7 A unified', '''## 6 Explaining the three puzzles

### 6.1 Consumption smoothing as the starting benchmark

A household can devote much of a small windfall to a pressing purchase and a smaller share of a larger receipt once that need is covered. Cash's declining mean and contracting highest-response category fit this logic. Standard smoothing is therefore a plausible benchmark. Explaining why Food declines less, Medical is nearly flat and their mean gaps narrow requires additional distinctions involving eligible uses, timing or allocation. The comparison across resource forms is where the harder economic question begins.

### 6.2 Scale and the affine description

Larger receipts can support much more spending even when their spending shares fall. An affine yuan profile, Y = a + bT, makes the connection explicit: its share is a/T + b. A positive intercept over the observed range permits a declining share alongside constant finite increments. The midpoint fits describe the cell means reasonably well, but neither common slopes nor an intercept-only explanation is established. The interval-model parameters also depend on residual-scale assumptions and are not structural MPCs (Supplements S4–S5). Scale explains what the puzzle is, not why the three resource forms follow different paths.

### 6.3 Accumulation in the bottom category

Could declining shares simply reflect more answers at the bottom? Cash's bottom frequency stays near 27.4%, and the decomposition locates almost all of its coded mean decline in the above-bottom component. Food and Medical have smaller bottom frequencies at the large amount. Bottom-category accumulation therefore supplies no common account of these paths. The relevant changes lie in the middle and upper categories, with the coding identity and its measurement limits set out in Supplement S2.

### 6.4 Increasing Food bindingness

If a larger voucher becomes harder to absorb in eligible purchases, a sharp prediction is that Food's size gradient should be more negative relative to Cash where eligible expenditure is low. The expenditure proxy distinguishes respondents whose six-month food-band lower bound exceeds RMB 5,000 (G = 1) from those who fail that condition (G = 0). Under this proxy, the prediction is a negative Food–Cash gradient in G = 0.

The observed sign is the opposite. The highest-category Food–Cash gradient in G = 0 is +8.00 percentage points per fivefold amount step, with a 95% interval of 3.83 to 12.18 (Figure 4). Food thus has the less negative gradient in the group to which the sharp prediction applies. This contradicts that prediction conditional on the proxy. Because the expenditure bands are coarse and vouchers also cover daily necessities, the result does not reject all models of binding constraints or substitution.

![Food Cash highest-category frequencies by the expenditure proxy](figures/fig4_food_raw_cells.png)

Figure 4. Food and Cash highest-category responses by expenditure proxy. G = 1 means the six-month food-band lower bound exceeds RMB 5,000; G = 0 fails that condition. Panel Ns are 815 and 2,806 adult Cash/Food respondents. The sharp prediction is a negative Food–Cash size gradient in G = 0; the observed gradient is positive. Whiskers are pointwise normal-binomial cell intervals. The proxy classifies expenditure capacity, not observed voucher bindingness.

The complete ratio-only models, which ask whether amount relative to food expenditure organizes the responses, are also rejected under both specified mappings (Supplement S6). These results leave simple increasing Food bindingness without the pattern it would need to explain Food's gentler decline. They turn attention toward differences in needs and allocation rather than the restriction alone.

### 6.5 Category need

Medical's offsets suggest an economic possibility: some households anticipate useful additional purchases, while others expect the balance to replace planned expenses or remain for later care. Food's broader redistribution may likewise reflect different routine needs. The continuous Food-expenditure comparison examines whether such needs systematically change the Food–Cash size gradient. For the highest category, the estimate is +0.29 percentage points per standard deviation of the ordered expenditure band, with a 95% interval of −2.33 to 2.91. Adjusted estimates and the medical-need diagnostic remain imprecise (Supplements S6–S7). Baseline category need does not provide a clear organizing explanation at the available precision; meaningful heterogeneity remains possible.

### 6.6 Relative income and liquidity

The same transfer can be modest for one household and substantial for another. A relative-resource explanation would organize the pattern by amount compared with income or available liquidity. The relative-income specifications offer only small gains over nominal amount in held-out prediction, and the restrictions do not establish a relative-income law. Income and emergency fundraising capacity are descriptive correlates, with moderator intervals allowing meaningful differences (Supplement S7). Relative financial scale remains plausible, but these measured resources do not parsimoniously organize the three observed paths into one account.

### 6.7 Observable household types

The remaining question is whether readily observed household types or response styles concentrate the pattern. The broad observable screen finds no stable moderator under its corrections and prediction diagnostics. Response-style screens also provide no clear separation, with substantial uncertainty in the stricter subgroup. Their definitions, pass/fail comparisons and the unstable age-by-education calibration appear in Supplements S7–S8. No readily observed type supplies a stable account in these checks, although unobserved or imprecisely measured heterogeneity remains possible.

Table 4 brings these answers together. The positive Food sign is informative against a specific prediction; the other comparisons establish the scope and precision of broader explanations. The joint configuration still calls for an account linking how resources arrive with how their allocation changes across amounts.

Table 4. Economic explanations and the distributional evidence

| Account | Main evidence | Implication |
| --- | --- | --- |
| Consumption smoothing | Cash mean and highest-category frequency decline | Plausible Cash benchmark; the comparative paths require more |
| Scale and affine response | Yuan rises while shares fall; incremental estimates are close | Clarifies allocation shares without establishing equal slopes |
| Bottom accumulation | Cash bottom frequency is stable; Food and Medical bottoms fall | Does not account for the mean paths |
| Sharp Food bindingness | Positive Food–Cash gradient in G = 0 | Opposite to the sharp negative prediction under the proxy |
| Category need | Food moderation interval spans meaningful differences | No clear organizing explanation at the available precision |
| Relative resources | Small prediction gains over nominal amount | No compelling common account of the three paths |
| Observable types | No stable separation in the reported screens | Heterogeneity remains possible |

Note: These comparisons address different economic predictions and use different estimands. They do not jointly identify a mechanism. Full estimates and precision summaries appear in Supplements S4–S8.''')

section('## 7 A unified', '## Author declarations', '''## 7 A unified behavioral interpretation

### 7.1 Resource categorization across scale

We propose resource categorization across scale as the most coherent organizing interpretation of the joint pattern. The central idea is that the allocation invited by a receipt depends on both its form and its size. An unrestricted small windfall may be assigned readily to current purchases; a larger sum may prompt consideration of saving, debt and future needs. A resource that arrives with an eligible use already has a place in that decision. The account connects the three observed paths, without requiring the forms to become behaviorally identical at large amounts.

For Cash, the distinctive starting point is the relatively large high-response mass at RMB 200. As amount rises, that mass contracts while the bottom remains stable. In the proposed account, a larger unrestricted receipt invites a broader allocation than an amount that can readily be absorbed into current purchases. The reduction in the small-Cash high-response premium then helps connect its own decline to the narrowing mean gaps.

Food arrives with a designated use. Its lower small-amount mean and less pronounced highest-response mass are consistent with that purpose already shaping allocation. As amount rises, its response distribution changes more diffusely across the middle and top. Medical combines a specified use with a persistent balance. That combination can accommodate both current needs and future care, allowing different responses to offset in the mean. The persistence is an attribute of the scenario; how strongly recipients mentally categorize that balance is part of the proposed explanation.

Together these paths suggest that increasing amount weakens the distinctive small-Cash allocation pattern, bringing the mean shares closer while leaving different bottom and upper frequencies. The survey does not measure the categorization process itself. Perceived spendability is a candidate construct, and the preference for this organizing account is interpretive rather than a tested superiority over competing mechanisms. In particular, the account accommodates Medical's offsets without uniquely predicting their near cancellation.

### 7.2 A direct test of the interpretation

The interpretation leads to a concrete experiment. Fix the consumption horizon and vary labels, eligible-use restrictions, expiry and liquidity separately. Measure perceived spendability and the intended division among current purchases, saving, debt and future needs before observing realized transactions. A manipulation that assigns unrestricted receipts to a broader future budget should reduce the small-Cash high-response premium if categorization drives it; the corresponding effect for already earmarked resources provides a comparative prediction.

Medical's offsets make current needs and anticipated future use especially valuable measurements. Tracking allocations as well as total spending would show whether similar means conceal different responses to the same resource. Randomized categorization prompts and explicit mediation assumptions would be needed to distinguish the proposed process from redemption constraints, substitution or different planning horizons. This design turns the organizing interpretation into a prospectively testable account.

## 8 Discussion

Transfer form is most strongly reflected in mean spending shares at the small end of the observed amount range. The large gaps at RMB 200 are much smaller at RMB 5,000, where Food lies close to Cash and Medical's nearly flat mean is closer to both. This is the comparative contribution of the nine-cell configuration. The corrected cross-form interactions remain uncertain, so the pattern characterizes these observed cells rather than establishing a general law about transfer size.

Similar average shares can conceal different distributional adjustments. Cash's highest category contracts, Food reallocates more broadly, and Medical combines movements that nearly cancel in the mean. Medical makes the point especially clearly: mean flatness leaves substantial differences between its category profiles unexplained. Looking at the full response distribution therefore changes the target of economic explanation, even when it leaves the mean comparison unchanged.

For transfer design, the configuration motivates studying form and size jointly. A comparison at one amount need not describe the allocation problem at another; future real-transfer studies can test that possibility directly. The distinction between shares and yuan also matters. Strongly rising implied yuan accompanies the narrowing share gaps, and absolute yuan gaps can grow. Policy evaluation consequently needs spending amounts, category expenditure, substitution and timing alongside average shares. These stated responses do not rank welfare or aggregate stimulus effects across the three forms.

The design has clear limits. Responses are hypothetical and unincentivized, elicited in approximate bins without a common explicit spending horizon. Form bundles eligibility, expiry and account structure. Recruitment and fieldwork records, allocation implementation and ethics/consent documentation await confirmation, and the sample is not established as representative. The analyses were not preregistered. Cross-form interactions and moderator estimates retain substantial uncertainty; categorization and perceived spendability are unmeasured. These limits define what a follow-up must identify and measure directly.

The central empirical fact is that Cash, Food and Medical approach much closer mean shares through markedly different distributional paths. A distinction pronounced for small receipts is less pronounced in the large-amount means, while the category profiles remain different. Resource categorization offers a coherent hypothesis linking these facts. The next experiment should measure and manipulate that process directly; the present configuration motivates the mechanism without identifying it.

## 9 Conclusion

In the observed cells, Cash spending shares decline with amount, Food declines less, and Medical's mean remains nearly flat. The closer large-amount means emerge through top-category compression, diffuse redistribution and offsetting changes, respectively. Implied yuan rises strongly throughout, locating the puzzle in allocation shares. The sharp simple Food-bindingness prediction has the opposite sign under the expenditure proxy. Resource categorization across scale provides an organizing hypothesis for the joint pattern and a target for direct experimental testing. The configuration suggests that transfer size changes how strongly resource form is reflected in stated spending allocation.''')
replace('Statistical outputs were computed with Python libraries; this revision reuses those results and redraws aggregate figures.', 'Statistical outputs were computed with Python libraries; the present writing refinement reuses those results and figures unchanged.')
(M/'JEBO_manuscript_v4_1.md').write_text(s,encoding='utf8')

# Preserve every supplementary table and the entire questionnaire verbatim.
u=(B/'JEBO_supplement_v4.md').read_text(encoding='utf8')
u=u.replace('The present bounded plan was fixed after those results were observed, before the new calculations.', 'The plan for the additional calculations was fixed after earlier results were observed and before those calculations were performed.')
u=u.replace('New Food results use adult Cash/Food standardization', 'The continuous Food results use adult Cash/Food standardization')
u=u.replace('across 15 pre-scenario attitude responses', 'across 15 attitude responses numbered before the scenario')
u=u.replace('The old decomposition is reproduced arithmetically without repeating the spending-participation interpretation.', 'The decomposition concerns the response coding rather than observed spending participation.')
u=u.replace('## S4 Yuan increments and affine fits\n', '''## S4 Yuan increments and affine fits

The full midpoint affine fit has slopes of 0.198, 0.194 and 0.178 for Cash, Food and Medical, with fitted intercepts of RMB 18.7, 6.4 and −0.2 and RMSE RMB 4.17. The common-slope model with form intercepts has lack-of-fit p = 0.178; the full-model slope-equality p value is 0.381, and the nested intercept comparison has Holm3 p = 0.0610. Nonrejection does not establish common slopes or an intercept-only account. Over RMB 1,000–5,000, the Cash–Medical finite-increment difference is 0.01691 [−0.01756, 0.05099]. None of the six pairwise interval contrasts rejects after Holm adjustment.
''')
u=u.replace('## S5 Interval affine sensitivity\n', '''## S5 Interval affine sensitivity

The maximum absolute merged-category calibration error is about 20.8 percentage points with constant residual scale and 8.8 with amount-specific scale in the unrestricted fits. The changing latent parameters and imperfect calibration preclude interpreting the fitted slopes as structural MPCs.
''')
u=u.replace('## S6 Food expenditure prediction and precision\n', '''## S6 Food expenditure prediction and precision

The G = 1 minus G = 0 highest-category Food–Cash gradient is −6.67 percentage points per fivefold step [−11.63, −1.71], with historical Holm7 p = 0.0504. The positive gradients in the two proxy groups concern a different comparison from this negative difference between gradients. For the complete two-restriction ratio models, highest-category Holm6 p values are 0.0426 and 0.0437 under the two mappings; the other four tests reject more strongly.
''')
u=u.replace('## S7 Prediction and precision ledger\n', '''## S7 Prediction and precision ledger

For unadjusted continuous Food moderation of the highest-category gradient, the nominal 80% MDE is 3.75 percentage points per standard deviation, rising to 4.65 with the six-test adjustment. The 10th–90th moderator span gives a compatible gradient-change interval of −6.00 to +7.49 points, compared with the Cash slope of −4.05 points per fivefold step. The adjusted estimate is +0.44 [−2.29, 3.17] points per standard deviation. All six focal continuous moderation tests have Holm6 p = 1.

Relative rather than nominal income scaling improves highest-category held-out prediction by about 0.12%–0.17% across the two mappings in Table S7d. These gains are distinct from those of the unrestricted model. The nominal-only restriction rejects in the historical seven-test family; the relative-income restriction and income three-way interaction do not retain corrected evidence. This combination does not establish a ratio law.

Income rank and emergency fundraising capacity are descriptive correlates rather than positive controls. The income association has the opposite sign to the generic validation prediction; emergency capacity is marginal after correction. Cash amount is the studied treatment and cannot serve as an independent validation control.
''')
(M/'JEBO_supplement_v4_1.md').write_text(u,encoding='utf8')
(M/'JEBO_Highlights_v4_1.md').write_text('''# Highlights

- Cash falls, Food falls less, and Medical stays flat in observed mean shares.

- Mean form gaps narrow with amount through different distributional paths.

- Cash loses high responses; Medical combines offsetting category changes.

- Implied yuan rises strongly while the puzzle concerns allocation shares.

- Resource categorization connects the pattern as an unmeasured hypothesis.
''',encoding='utf8')
for name in ['build_docx.py','render_word.ps1','inspect_render.py']:
    p=M/'scripts'/name
    p.write_text(p.read_text(encoding='utf8').replace('JEBO_manuscript_v4\'','JEBO_manuscript_v4_1\'').replace('JEBO_supplement_v4\'','JEBO_supplement_v4_1\'').replace('JEBO_Highlights_v4\'','JEBO_Highlights_v4_1\''),encoding='utf8')
p=M/'AUTHOR_INFORMATION_REQUIRED.md'
p.write_text(p.read_text(encoding='utf8').replace('v4 follows author specification: 191-word abstract','v4.1 follows author specification: 170–200-word target abstract'),encoding='utf8')
print('Editorial sources written; no empirical computation performed.')
