"""Bounded primary-source bibliography retrieval, separate from empirical work."""
from pathlib import Path
import csv,json,re,urllib.request,urllib.parse,concurrent.futures,difflib
O=Path(__file__).resolve().parent;P=O.parents[1];C=O/'research_cache';C.mkdir(exist_ok=True)
op=urllib.request.build_opener(urllib.request.ProxyHandler({'https':'http://127.0.0.1:7897'}))
new={
'JP2010':'10.1146/annurev.economics.050708.142933',
'KV2022':'10.1146/annurev-economics-080217-053444',
'FHN2021':'10.1257/mac.20190211',
'HS2013':'10.1093/qje/qjt018',
'HS1996':'10.1086/209465',
'HS2020':'10.1016/j.red.2019.05.004',
'PS2019':'10.1257/aeri.20180333',
'CH2019':'10.1093/ej/uez013',
'BA2023':'10.1007/s00181-023-02410-0',
'JS2026':'10.1016/j.euroecorev.2026.105303',
'SO2023':'10.1016/j.red.2023.08.005',
'LEE2024':'10.1016/j.jebo.2024.04.023',
'PL2025':'10.1016/j.jebo.2025.107079',
'FR2025':'10.1016/j.jebo.2025.106899',
'PE2024':'10.1016/j.jebo.2024.04.005',
'FO2025':'10.1016/j.jebo.2025.107321',
'RE2024':'10.1016/j.jebo.2024.06.024',
'LS2024':'10.1016/j.jebo.2024.06.021',
'RC2024':'10.1016/j.jebo.2024.106705',
'LB2024':'10.1016/j.jebo.2024.106755',
'DI2024':'10.1016/j.jebo.2024.02.028',
'OV2024':'10.1016/j.jebo.2024.01.010',
'CA2023':'10.1016/j.jebo.2023.01.024'}
old=json.loads((P/'manuscript/nc_v5/references_original_order.json').read_text(encoding='utf-8'))
checks=list(csv.DictReader((O.parent/'nc_evidence_revision/reference_checks_v5.csv').open(encoding='utf-8-sig')))
prior=list(csv.DictReader((O.parent/'nc_revision_audit/reference_audit.csv').open(encoding='utf-8-sig')))
items=[]
for i in range(1,31):
    citation=old[str(i)];a=next((r for r in checks if r['original_number']==str(i)),{})
    doi=a.get('DOI','')
    if not doi:
        def score(r):
            title=r['exact_title'].lower().replace('’',"'")
            return 1 if title in citation.lower().replace('’',"'") else difflib.SequenceMatcher(None,citation.lower(),r['citation'].lower()).ratio()
        best=max(prior,key=score)
        if score(best)>.7:doi=best['DOI']
    items.append(dict(id=f'N{i:02d}',doi=doi,prior_citation=citation))
items += [dict(id=k,doi=v,prior_citation='') for k,v in new.items()]
def one(r):
    path=C/(r['id']+'_metadata.json')
    try:
        if path.exists():m=json.loads(path.read_text(encoding='utf-8'))
        else:
            if not r['doi']:return dict(**r,status='no DOI from prior audit')
            req=urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(r['doi'],safe=''),headers={'User-Agent':'ResearchBibliography/1.0'})
            m=json.load(op.open(req,timeout=35))['message'];path.write_text(json.dumps(m,ensure_ascii=False),encoding='utf-8')
        return dict(**r,status='retrieved',title=m.get('title',[''])[0],authors='; '.join((a.get('given','')+' '+a.get('family','')).strip() for a in m.get('author',[])),journal=m.get('container-title',[''])[0] if m.get('container-title') else m.get('publisher',''),year=(m.get('published-print') or m.get('published') or m['issued'])['date-parts'][0][0],volume=m.get('volume',''),pages=m.get('page',m.get('article-number','')),url=m.get('URL',''),abstract=re.sub('<[^>]+>',' ',m.get('abstract','')),accessed='2026-10-03')
    except Exception as e:return dict(**r,status='retrieval failed',error=str(e),accessed='2026-10-03')
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: rows=list(pool.map(one,items))
keys=list(dict.fromkeys(k for r in rows for k in r))
with (O/'bibliography_metadata.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
for r in rows:print(r['id'],r['status'],r.get('title',r['prior_citation']),r['doi'])
