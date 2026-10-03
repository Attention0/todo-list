from common import *
import shutil
M=ROOT/'manuscript'/'jebo_v3'
old=pd.read_csv(O.parent/'jebo_transition'/'bibliography_metadata.csv').fillna('')
priority={'N07':('https://www.aeaweb.org/articles?id=10.1257/000282803321455368','Publisher article metadata; actual tax-rebate survey context','Actual rebate reports; not hypothetical realized-spending validation'),
'N12':('https://academic.oup.com/restud/article/88/4/1760/5962017','Publisher abstract and article page','Filter/positive-response extensive margin differs from current verbal bottom bin'),
'N13':('https://www.aeaweb.org/articles?id=10.1257/mac.20220169','Publisher abstract, citation, journal issue','Opposite size responses across affluent and liquidity-poor groups; no universal decline'),
'N23':('https://ftp.aeaweb.org/articles/pdf/doi/10.1257/aer.20240138','Publisher citation and abstract','Realized transfer-form experiment, fixed amount; cash-like vs expiring card'),
'N24':('https://www.nber.org/papers/w35698','Primary institution cached abstract and metadata; direct fetch403','September2026 working paper; food-store scanner response, not total consumption'),
'N25':('https://www.bundesbank.de/resource/blob/909438/d24b53faa075049c3ba7fe0dcdf512b3/mL/2023-05-22-dkp-13-data.pdf','Primary full PDF; design, equation1 and means from prior targeted audit','Already jointly varies form and size; our study has no first-joint-design priority'),
'N30':('https://www.chicagofed.org/publications/working-papers/2026/2026-04','Primary abstract and WP metadata','Question wording changes distributions and size effects; working paper not published article'),
'PS2019':('https://www.aeaweb.org/articles?id=10.1257/aeri.20180333','Publisher article metadata and original targeted measurement audit','Reports about actual rebates can discriminate revealed spending response; not blanket validation'),
'LEE2024':('https://www.sciencedirect.com/science/article/pii/S0167268124001586','Publisher abstract, highlights and metadata','Willingness to spend in migrant setting; not MPC or unrestricted/eligible transfer grid'),
'PL2025':('https://doi.org/10.1016/j.jebo.2025.107079','Publisher article text and metadata','Temporal framing of real permanent tax cut; not randomized cut amount/form')}
assert set(priority).issubset(set(old.id)),set(priority)-set(old.id)
keep=list(priority)+['N01','N02','N03','N17','N18','N21','N29']
audit=[]
for id in keep:
    r=old[old.id==id].iloc[0].to_dict();r['priority']=id in priority
    if id in priority:r['primary_url'],r['access_scope'],r['claim_boundary']=priority[id];r['verification_date']='2026-10-03';r['verification']='Current primary web recheck plus bounded prior source audit'
    else:r.update(primary_url=r['url'],access_scope='Inherited same-day bibliographic verification from jebo_transition; not new full-text review',verification_date='2026-10-03',verification='Historical metadata retained',claim_boundary='Use only established narrow background or measurement claim')
    if id=='N13':r['authors']='Michelle Andreolli; Paolo Surico';r['author_name_note']='Current AEA citation spells Michelle; prior Crossref mirror spells Michele. Publisher citation used, no identity inference.'
    audit.append(r)
save(audit,'JEBO_V3_REFERENCE_AUDIT.csv');shutil.copyfile(O/'JEBO_V3_REFERENCE_AUDIT.csv',M/'JEBO_V3_REFERENCE_AUDIT.csv')
note('JOURNAL_REQUIREMENTS_AUDIT.md','''# Current journal checks

Checked2026-10-03. Official JEBO guide:
https://www.sciencedirect.com/journal/journal-of-economic-behavior-and-organization/publish/guide-for-authors
returned403 through the web tool. A primary-source journal-specific abstract limit
could not be independently refreshed. We use a single paragraph below250 words as
a conservative preparation choice, NOT a verified current JEBO rule. Author-year
references, numbered sections, editable Word and separate figure sources follow
the established JEBO direction and published comparators; the author must check
live portal rules before submission. No unofficial template is treated as authority.

Elsevier primary journal AI policy was accessible at:
https://www-prod.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
It requires an end-of-manuscript declaration before references with tool/service,
purpose and human review/responsibility. The section is included; human author
review is still pending and not falsely certified. AI-assisted code preparation is
also disclosed in Methods. Statistical figures are generated from aggregate data,
not generative imagery. Funding/conflicts/CRediT and data-sharing authorization
remain author facts. A draft with placeholders is not submission-ready.
''')
note('LITERATURE_POSITION_REVISION.md','''# Revised JEBO position

The repository's existing literature reconciliation and54-paper matrix remain the
bounded starting point. This revision rechecks the ten priority sources, rather
than adding a new literature search or expanding empirical scope.

Bernard2023 is the nearest design precedent: mode×size already randomized; no
first joint design or first distribution-decomposition claim. The incremental
extension is three nominal amounts crossed with category-restricted Food and
Medical bundles in a direct binned Chinese survey instrument. Boehm2025 supplies
stronger realized form evidence, while holding amount fixed. Bonomo2026 supplies
food-store spending evidence from distinct actual transfer programmes; its retail
outcome and timing design cannot validate our total-consumption hypothetical measure.

Fuster2021 shows adjustment on a filtered extensive margin; our bottom/above-bottom
arithmetic is a different estimand and cannot establish an opposite participation
result. Andreolli–Surico2026 supports heterogeneous, not universal, size responses.
Crossley2026 makes elicitation format a first-order limitation. Shapiro–Slemrod2003
and Parker–Souleles2019 concern actual tax-rebate reports. Parker is not blanket
validation of hypothetical categories; Ueda2025 is retained as a counterweight.

JEBO comparators Lee2024 and Pauls–Laudi2025 motivate a concrete contrast about
resource presentation and context, with boundaries on hypothetical measurement.
The paper now asks whether form/size patterns describe level differences, incremental
yuan differences or both. It does not claim a measured spendability mechanism.
Choose 'Transfer size and form in stated spending responses': it names the actual
randomized comparison and measured outcome without promoting an inferred construct.
Working papers remain labelled as such. Access scope is row-specific, no blanket
claim that every referenced paper was newly read in full.
''')
note('AFFINE_RESPONSE_RESULT.md','''# Yuan and affine response to the review

Cash incremental midpoint-implied yuan:0.220113 (bootstrap95%0.192939–0.248223)
for200→1000;0.195375 (0.170340–0.220237) for1000→5000. Food:0.193048/0.193728;
Medical:0.178522/0.178470. High-interval Cash−Food0.001647
(−0.034856,0.036539); Cash−Medical0.016905 (−0.017565,0.050990).
All six pairwise interval comparisons lose Holm6 significance. This supports a
descriptive similarity of point estimates, not equivalence or proven convergence.

Endpoint elasticities Cash0.929513, Food0.952716, Medical1.002010. Shares can decline
while implied yuan grows nearly proportionally. The affine midpoint model estimates
Cash/Food/Medical slopes0.198224/0.193651/0.178476. Slope equality is not rejected
(p=.381295). Common intercept AND slope performs poorly; their joint restriction
is rejected (Holm3=.000423). The intercept-only comparison hasHolm3=.061022; it
does not prove an intercept-only mechanism. Form-intercept/common-slope RMSE18.28
and saturated lack-of-fit p=.178 versus full model RMSE4.17,p=.710. Intercepts
are zero-transfer extrapolations and not identified psychological parameters.

Censored-normal constant-scale full model has slope-equality p=.780 but maximum
category calibration error20.81pp; it is substantively misspecified. The single
amount-varying-scale sensitivity improves maximum error to8.78pp and changes slopes
to0.099646/0.074723/0.054651 (equality p=.076871). All8000 bootstrap fits converge,
but parameter sensitivity prevents coding-robust structural MPC claims. Both models
and all45 category probabilities per model remain available, including constrained
fits. No alternate censoring or model search was undertaken.

The review's scale distinction is correct. Its stronger interpretation that all
form differences are small-transfer intercept differences is not established:
large-amount absolute yuan gaps remain, pairwise incremental CIs are not equivalence
intervals, intercept comparisons are uncertain, and interval parameters depend on
distributional assumptions. The revised paper presents that boundary explicitly.
''')
author='''# Author information required before submission

The analysis/revision is complete within the frozen scope. These facts require
author records, not inference from the data or assertions in previous drafts.

| Item | Required evidence / decision | Status |
| --- | --- | --- |
| Authors and affiliations | Confirm names, institution/address, corresponding author/email | Draft names retained in audit only; confirm |
| Recruitment | Vendor/platform, sampling frame, eligibility, invitation channel | Tencent hosting does not establish vendor; missing |
| Field dates and stopping | Start/end dates, target N, stopping/exclusion rules at collection | Missing |
| Incentives | Whether/amount/how paid; distinguish survey compensation from outcome incentives | Missing; hypothetical scenarios were not paid transfers |
| Response flow | Invitations, starts, completed surveys, exclusions and unique-respondent checks | Only delivered5497 and adult5480 verified |
| Randomization | Assignment probabilities, mechanism, blocking if any, allocation logs | Instrument says system selection of one of nine; implementation missing |
| Ethics and consent | Approval/exemption institution/reference/date, consent wording and minors handling | No formal record located; excluding17 minors does not resolve collection ethics |
| Questionnaire provenance | Confirm integrated instrument reflects fielded wording and which background variables preceded exposure | Scenarios and15 attitude items precede/follow according to instrument; confirm deployment |
| Missing region | Province/city identities or defensible geographic strata if collected | Only city-tier field verified; do not call it province coverage |
| Funding / conflicts | Explicit author statements; no invented 'none' | Missing |
| CRediT | Each human author's verified contributions | Missing |
| Data availability | Confirm consent/licence for release, repository and access conditions | Only aggregate replication outputs prepared; raw private |
| AI declaration | Confirm named tools, drafting/code uses, human review and responsibility | Draft disclosure included; human sign-off pending |
| Journal submission rules | Check live JEBO guide/portal, abstract cap, highlights and files | Official guide refresh403; abstract conservatively below250 |

An author question was sent during execution. No missing fact will be invented if
no answer arrives. Draft status is maintained until these fields are resolved.
'''
note('AUTHOR_INFORMATION_REQUIRED.md',author);(M/'AUTHOR_INFORMATION_REQUIRED.md').write_text(author,encoding='utf8')
note('TITLE_SELECTION.md','''# Titles considered after results

1. Transfer size and form in stated spending responses — selected, actual estimands.
2. Spending shares and implied yuan across transfer forms — accurate but narrow.
3. Level and incremental responses to hypothetical transfers — affine emphasis risks overstatement.
4. Response distributions across cash and earmarked transfers — accurate but omits scale repair.

The selected title has no spendability or identified-mechanism claim.
''')
print('Reference audit:17 selected citations,10 current priority checks; live guide limitation recorded.')
