"""Focused bibliography metadata refresh; no analysis or manuscript result changes."""
from pathlib import Path
import csv,json,urllib.request,urllib.parse,concurrent.futures,re,sys
M=Path(__file__).resolve().parents[1]; R=M.parents[1]
old={r['id']:r for r in csv.DictReader((R/'results/jebo_transition/bibliography_metadata.csv').open(encoding='utf-8-sig'))}
ids=['N01','N02','N03','N07','N12','N13','N17','N18','N20','N21','N22','N23','N24','N25','N29','N30','JP2010','KV2022','FHN2021','HS1996','PS2019','JS2026','LEE2024','PL2025']
url={
'N01':'https://pubsonline.informs.org/doi/10.1287/mksc.4.3.199',
'N02':'https://onlinelibrary.wiley.com/doi/10.1111/j.1465-7295.1988.tb01520.x',
'N03':'https://onlinelibrary.wiley.com/doi/10.1002/%28SICI%291099-0771%28199909%2912%3A3%3C183%3A%3AAID-BDM318%3E3.0.CO%3B2-F',
'N12':'https://academic.oup.com/restud/article/88/4/1760/5962017',
'N17':'https://academic.oup.com/jeea/article-abstract/15/1/99/2732085',
'N24':'https://www.nber.org/papers/w35698',
'N25':'https://www.bundesbank.de/en/publications/research/discussion-papers/mental-accounting-and-the-marginal-propensity-to-consume-909438',
'N29':'https://waseda.elsevierpure.com/en/publications/the-reality-of-consumption-comparing-self-reported-and-observed-m/',
'N30':'https://www.chicagofed.org/publications/working-papers/2026/2026-04',
'JP2010':'https://www.annualreviews.org/content/journals/10.1146/annurev.economics.050708.142933',
'KV2022':'https://doi.org/10.1146/annurev-economics-080217-053444',
'HS1996':'https://academic.oup.com/jcr/issue/23/1',
'JS2026':'https://www.sciencedirect.com/science/article/pii/S0014292126000474',
'LEE2024':'https://www.sciencedirect.com/science/article/pii/S0167268124001586',
'PL2025':'https://www.sciencedirect.com/science/article/pii/S0167268125001982'}
boundary={
'N01':'Conceptual mental coding and household budgeting; no identified mediator here.',
'N02':'Behavioral life-cycle account distinctions; not a prediction of all nine cells.',
'N03':'Background mental accounting synthesis; no unique size interaction.',
'N07':'Survey responses to actual tax rebates; not hypothetical validation.',
'N12':'Hypothetical scenarios with filtered spending adjustment; not the current bottom-bin margin.',
'N13':'Size patterns vary by resources; no universal negative size gradient.',
'N17':'Labels in incentivized consumption experiments; our bundles do not isolate labels.',
'N18':'Benefit labeling evidence; not a direct total-spending size comparison.',
'N20':'Actual in-kind/cash RCT; aggregate and item-level inframarginality differ.',
'N21':'SNAP eligible food expenditure; not total additional consumption.',
'N22':'Taiwan voucher survey and discounts; no universal voucher MPC.',
'N23':'Actual transfers and transactions, cash-like versus expiring card; fixed-amount form contrast.',
'N24':'Food-store scanner responses across programmes; working paper, not total consumption.',
'N25':'Payment mode crossed with shock size already studied; cite verified DP version, no first-design claim.',
'N29':'Linked survey and transaction results in that setting; not universal survey invalidity.',
'N30':'Direct versus filtered elicitation changes patterns; working paper, not validation of our instrument.',
'JP2010':'Consumption smoothing review; no universal finite-shock monotonicity.',
'KV2022':'Model synthesis; only qualitative background, not calibration values. Publisher links an erratum.',
'FHN2021':'Norwegian lottery and administrative data; resources and size jointly matter.',
'HS1996':'Category budgeting; not a unique transfer-form-by-size law.',
'PS2019':'Actual rebate reports compared with revealed responses; context-specific correspondence.',
'JS2026':'Italian hypothetical lottery amounts and time profiles; published EER 186 105303.',
'LEE2024':'Mobile money and remittance earmarking; willingness to spend, not a transfer MPC.',
'PL2025':'Framing a permanent tax cut and stated allocations; not randomized transfer amount or form.'}
def get(i):
    r=old[i].copy();doi=r['doi']; meta={};status=''
    if i not in ['N25','N30']:
        try:
            req=urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''),headers={'User-Agent':'JEBOWritingAudit/1.0'})
            with urllib.request.urlopen(req,timeout=25) as f:meta=json.load(f)['message']
            status='Crossref metadata retrieved 2026-10-04'
        except Exception as e:status='Crossref unavailable: '+type(e).__name__+'; primary page and inherited metadata used'
    else:status='Institutional working-paper record checked; no journal-publication claim'
    primary=url.get(i,'https://www.aeaweb.org/articles?id='+doi)
    r.update(primary_url=primary,verification_date='2026-10-04',metadata_check=status,claim_boundary=boundary[i])
    r['publication_status']='Working paper' if i in ['N24','N25','N30'] else 'Published journal article'
    r['access_scope']='Primary publisher/institutional abstract and metadata; not a new full-text review'
    if i in ['N03','HS1996','N18']:r['access_scope']='Primary publisher bibliographic record; narrow background claim; prior source verification retained'
    if i in ['LEE2024','PL2025']:r['access_scope']='Publisher full HTML sections and abstract'
    if i=='N25':r['access_scope']='Bundesbank working-paper record and previously verified paper design';r['doi']='';r['journal']='Deutsche Bundesbank Discussion Paper';r['volume']='';r['pages']='13/2023'
    if i=='N24':r['journal']='NBER Working Paper';r['volume']='';r['pages']='35698'
    if i=='N30':r['journal']='Federal Reserve Bank of Chicago Working Paper';r['volume']='';r['pages']='2026-04';r['doi']=''
    if i=='JS2026':r.update(year='2026',volume='186',pages='105303',journal='European Economic Review')
    r['crossref_title']='; '.join(meta.get('title',[]));r['crossref_volume']=meta.get('volume','');r['crossref_pages_or_article']=meta.get('page',meta.get('article-number',''))
    r['crossref_authors']='; '.join((a.get('given','')+' '+a.get('family','')).strip() for a in meta.get('author',[]))
    return r
if '--cached' in sys.argv:
    rows=list(csv.DictReader((M/'JEBO_V4_REFERENCE_AUDIT.csv').open(encoding='utf8')))
else:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(get,ids))
    rows.append(dict(id='FR1957',doi='',title='A Theory of the Consumption Function',authors='Milton Friedman',journal='Princeton University Press',year='1957',volume='',pages='',primary_url='https://www.nber.org/books-and-chapters/theory-consumption-function/permanent-income-hypothesis',verification_date='2026-10-04',metadata_check='NBER original book/chapter record checked',publication_status='Published book',access_scope='Primary NBER chapter record',claim_boundary='Permanent versus transitory income conceptual benchmark; no universal size monotonicity.'))
keys=list(dict.fromkeys(k for r in rows for k in r))
with (M/'JEBO_V4_REFERENCE_AUDIT.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,keys);w.writeheader();w.writerows(rows)
def authors(s):
    out=[]
    for a in s.split('; '):
        bits=a.split();out.append(bits[-1]+', '+''.join(b[0]+'.' for b in bits[:-1]))
    return ', '.join(out)
refs=[]
for r in rows:
    author=authors(r['authors']);title=r['title']
    if r['id']=='N02':title='The behavioral life-cycle hypothesis'
    if r['id']=='N13':author='Andreolli, M., Surico, P.'
    vol=r.get('volume','').removesuffix('.0');pages=r.get('pages','')
    loc=r['journal']+(' '+vol if vol else '')+(', '+pages if pages else '')
    # Canonical DOI links avoid long publisher redirects in the bibliography.
    link=('https://doi.org/'+urllib.parse.quote(r['doi'],safe='/:;().-')) if r.get('doi') else r['primary_url']
    refs.append(f"{author}, {r['year']}. {title}. {loc}. {link}")
refs.sort();p=M/'JEBO_manuscript_v4.md';s=p.read_text(encoding='utf8');s=s.split('## References')[0]+'## References\n\n'+'\n\n'.join(refs)+'\n';p.write_text(s,encoding='utf8')
# Compact readable reference-status audit in supplement; full DOI/access detail stays in CSV.
p=M/'JEBO_supplement_v4.md';s=p.read_text(encoding='utf8').split('## S11 Reference verification')[0]
s+='\n\n## S11 Reference verification\n\nThe focused source refresh is dated 4 October 2026. The accompanying JEBO_V4_REFERENCE_AUDIT.csv records every cited work, DOI where applicable, primary URL, access scope, metadata checks and claim boundaries. Bibliographic checks do not imply new full-text access. Jappelli et al. is now cited as a published European Economic Review article; Bonomo et al., Bernard and Crossley et al. are identified as working-paper versions. The conceptual citations do not identify mechanisms in this experiment.\n\n'
s+='| Work | Verified version | Scope of use |\n| --- | --- | --- |\n'
for r in sorted(rows,key=lambda x:x['authors'].split()[-1]):s+=f"| {authors(r['authors'])} ({r['year']}) | {r['journal']} {r.get('volume','')} {r.get('pages','')} | {r['claim_boundary']} |\n"
p.write_text(s,encoding='utf8')
print(json.dumps({'references':len(rows),'crossref_success':sum('retrieved' in r.get('metadata_check','') for r in rows),'metadata_failures':[r['id'] for r in rows if 'unavailable' in r.get('metadata_check','')]},indent=2))
