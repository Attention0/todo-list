"""Read-only manuscript bibliography audit against Crossref/NBER metadata."""
from pathlib import Path
import json,re,urllib.request,urllib.parse,difflib,concurrent.futures
from docx import Document
import pandas as pd
OUT=Path(__file__).resolve().parent
MAN=Path('G:/桌面/科研/项目-消费调查/NC_MPC_manuscript_draft_v2.docx')
TITLES=[
'Mental accounting and consumer choice','The behavioral life-cycle hypothesis','Mental accounting matters',
'Mental accounting mechanisms in energy decision-making and behaviour',
'Context induces distortions in value representations across multiple elicitation methods and learning modalities',
'Neural processes mediating contextual influences on human choice behaviour','The psychology of windfall gains',
'Mental accounting and small windfalls: evidence from an online grocer','Fungibility, labels, and consumption',
'The labeling effect of a child benefit system','Cash by any other name? Evidence on labeling from the UK Winter Fuel Payment',
'Testing paternalism: cash versus in-kind transfers','How are SNAP benefits spent? Evidence from a retail panel',
'Five facts about MPCs: evidence from a randomized experiment','Is a dollar a dollar? How transfer design shapes household spending',
'Household expenditure and the income tax rebates of 2001','Consumer spending and the economic stimulus payments of 2008',
'Consumption, income changes, and heterogeneity: evidence from two fiscal stimulus programs','Fiscal policy and MPC heterogeneity',
'What would you do with $500? Spending responses to gains, losses, news, and loans','Reported MPC and unobserved heterogeneity',
'Why don’t households smooth consumption? Evidence from a $25 million experiment',
'Less Is More: consumer spending and the size of economic stimulus payments','Latent heterogeneity in the marginal propensity to consume',
'Mental accounting and the marginal propensity to consume','Windfall income shocks with finite planning horizons',
'The wealthy hand-to-mouth','Effects of a monthly unconditional cash transfer starting at birth on family investments among US families with low income',
'Effects of unconditional cash transfers on family processes and wellbeing among mothers with low incomes',
'A systematic review and meta-analysis of the impact of cash transfers on subjective well-being and mental health in low- and middle-income countries']
CLAIMS=[
'Mental-accounting conceptual framework, not evidence of this survey mechanism',
'Behavioral life-cycle account framework, not a unique form-by-size prediction',
'Mental accounting framework, not direct identification in current data',
'Energy-account context only; does not establish transfer-size scaling',
'Context-dependent experimental value representation; not MPC/transfer evidence',
'Neural contextual choice processes; not MPC/transfer evidence',
'Windfall spending psychology; not a universal size gradient',
'Small windfalls change basket/hedonic purchases in an online grocery setting',
'Budget labels affect experimentally elicited consumption despite fungibility',
'Child benefit labeling and category-specific household spending',
'Winter fuel labeling and fuel spending, not overall transfer-size curve',
'Cash vs in-kind evidence in a different program context',
'SNAP food-spending response differs from cash despite inframarginality',
'Realized cash-like vs expiring-card MPC; expiry bundled, not our same estimand',
'Food-store MPC varies by cash/kind and payment recurrence; not total consumption',
'Realized spending responses to2001 rebates; different measurement/horizon',
'Realized spending response to2008 stimulus; different context/horizon',
'Stimulus-response heterogeneity; not proof of current moderators',
'Hypothetical MPC is associated with cash-on-hand/liquidity; association',
'Hypothetical gains responses; larger-gain extensive response can increase, not universal negative size law',
'Reported MPC negatively related to cash on hand; not personal-income equivalence',
'Experiment on spending and liquidity/household characteristics',
'Hypothetical size heterogeneity differs by liquidity/affluence; not universal negative size law',
'Latent realized MPC variation weakly explained jointly by observables; not current universal-effect proof',
'Mental-account framing research; no direct process identification in our questionnaire',
'Finite-planning-horizon model is candidate explanation, not empirical identification here',
'Illiquid wealthy may be hand-to-mouth; income alone not liquidity',
'Family investment effects of repeated early-life transfers; not size/form MPC evidence',
'Maternal wellbeing/family-process transfer effects; not size/form MPC evidence',
'Cash transfers and wellbeing meta-analysis; not size/form MPC evidence']
KNOWN={1:'10.1287/mksc.4.3.199',2:'10.1111/j.1465-7295.1988.tb01520.x',3:'10.1002/(SICI)1099-0771(199909)12:3<183::AID-BDM318>3.0.CO;2-F',4:'10.1038/s41560-020-00704-6',5:'10.1038/s41467-026-72644-w',6:'10.1038/ncomms12416',7:'10.1006/obhd.1994.1063',8:'10.1016/j.jebo.2009.04.007',9:'10.1093/jeea/jvw007',10:'10.1257/aer.90.3.571',11:'10.1016/j.jpubeco.2014.06.007',12:'10.1257/app.6.2.195',13:'10.1257/aer.20170866',14:'10.1257/aer.20240138',15:'10.3386/w35698',16:'10.1257/aer.96.5.1589',17:'10.1257/aer.103.6.2530',18:'10.1257/mac.6.4.84',19:'10.1257/mac.6.4.107',20:'10.1093/restud/rdaa076',21:'10.1257/pol.20180420',22:'10.1257/mac.20150390',23:'10.1257/mac.20220169',24:'10.1093/restud/rdaf102',26:'10.1016/j.jfineco.2025.104174',27:'10.1353/eca.2014.0002',28:'10.1038/s41562-024-01915-7',29:'10.1038/s41467-025-62438-x',30:'10.1038/s41562-021-01252-z'}
REMOVE={4,5,6,28,29,30}
KNOWN[22]='10.1257/mac.20150331'  # Verified NBER and AEA publication record.
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def fetch(number,title,citation):
    if number==25:return dict(ref_number=number,citation=citation,verified='YES publisher working-paper page',exact_title=title,authors='René Bernard',journal_status='Deutsche Bundesbank Discussion Paper13/2023',volume='',pages='',DOI='',source_url_or_doi='https://www.bundesbank.de/en/publications/research/discussion-papers/mental-accounting-and-the-marginal-propensity-to-consume-909438',claim_supported=CLAIMS[number-1],action='keep only bounded framing background; no direct process claim',metadata_scope='publisher page verified via web, not peer-reviewed journal')
    op=urllib.request.build_opener(urllib.request.ProxyHandler({'https':'http://127.0.0.1:7897'}))
    base='https://api.crossref.org/works'
    url=base+'/'+urllib.parse.quote(KNOWN[number],safe='') if number in KNOWN else base+'?'+urllib.parse.urlencode({'query.title':title,'rows':3})
    try:
        with op.open(url,timeout=30) as r:m=json.loads(r.read())['message']
        items=[m] if number in KNOWN else m['items']
        best=max(items,key=lambda x:difflib.SequenceMatcher(None,norm(title),norm(x.get('title',[''])[0])).ratio())
        exact=best.get('title',[''])[0];similarity=difflib.SequenceMatcher(None,norm(title),norm(exact)).ratio()
        authors='; '.join(' '.join([a.get('given',''),a.get('family','')]).strip() for a in best.get('author',[]))
        first=citation.split('.',1)[-1].strip().split(',')[0].strip()
        valid=similarity>.90 and norm(first) in norm(authors)
        action='remove from core Intro: not directly relevant to transfer-form-by-size estimand' if number in REMOVE else 'keep; distinguish hypothetical/realized and bundled intervention attributes'
        if not valid:action='flag/delete pending primary verification; do not treat as a verified citation'
        return dict(ref_number=number,citation=citation,verified='YES metadata; bounded claim' if valid else 'NO',exact_title=exact,authors=authors,journal_status='; '.join(best.get('container-title',[])),volume=best.get('volume',''),pages=best.get('page',best.get('article-number','')),DOI=best.get('DOI',''),year=str(best.get('published',{}).get('date-parts',[[]])[0]),source_url_or_doi='https://doi.org/'+best.get('DOI',''),claim_supported=CLAIMS[number-1] if valid else 'NOT VERIFIED',action=action,metadata_scope='Crossref publisher-deposited bibliographic record; not a full-text claim replication',title_similarity=similarity)
    except Exception as e:return dict(ref_number=number,citation=citation,verified='NO retrieval failed',source_url_or_doi=url,claim_supported='NOT VERIFIED',action='flag/delete pending verification',failure=str(e))
def main():
    pars=[p.text for p in Document(MAN).paragraphs]
    refs=[p for p in pars if re.match(r'^\d+\. ',p)]
    assert len(refs)==30
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows=list(pool.map(lambda i:fetch(i+1,TITLES[i],refs[i]),range(30)))
    for i,row in enumerate(rows):
        if row['verified'].startswith('NO'):
            rows[i]=fetch(i+1,TITLES[i],refs[i])
    pd.DataFrame(rows).to_csv(OUT/'reference_audit.csv',index=False)
    print(pd.DataFrame(rows)[['ref_number','verified','exact_title','DOI']].to_string(index=False))
if __name__=='__main__':main()
