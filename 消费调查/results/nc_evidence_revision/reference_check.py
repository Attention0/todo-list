"""Dated publisher-deposited metadata checks; not a full-text validation."""
from pathlib import Path
import json,re,urllib.request,urllib.parse,difflib,concurrent.futures,os
import pandas as pd
O=Path(__file__).resolve().parent;M=O.parent.parent/'manuscript'/'nc_v5'
refs=json.loads((M/'references_original_order.json').read_text(encoding='utf8'));nums=json.loads((M/'reference_number_map.json').read_text())
prior=pd.read_csv(O.parent/'nc_revision_audit'/'reference_audit.csv').fillna('')
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def work(item):
    old,cite=item
    if old=='31':return dict(original_number=31,new_number=nums[old],status='official census image visually inspected',url='https://www.stats.gov.cn/sj/pcsj/rkpc/7rp/zk/html/A0401.jpg')
    hit=max(prior.itertuples(),key=lambda r:difflib.SequenceMatcher(None,norm(cite),norm(r.citation)).ratio())
    similarity=difflib.SequenceMatcher(None,norm(cite),norm(hit.citation)).ratio()
    known=similarity>.72 and bool(hit.DOI)
    endpoint='https://api.crossref.org/works/'+urllib.parse.quote(hit.DOI,safe='') if known else 'https://api.crossref.org/works?'+urllib.parse.urlencode({'query.bibliographic':cite,'rows':1})
    result=dict(original_number=int(old),new_number=nums[old],citation=cite,checked_on='2026-10-03',prior_similarity=similarity,scope='Publisher-deposited metadata only; claims require bounded source reading')
    try:
        proxy=os.getenv('HTTPS_PROXY','');opener=urllib.request.build_opener(urllib.request.ProxyHandler({'https':proxy}) if proxy else urllib.request.ProxyHandler({}))
        req=urllib.request.Request(endpoint,headers={'User-Agent':'ResearchReferenceAudit/1.0'})
        with opener.open(req,timeout=25) as res:msg=json.load(res)['message']
        record=msg if known else msg['items'][0];title=record.get('title',[''])[0];result.update(status='retrieved',DOI=record.get('DOI',''),title=title,title_in_citation=norm(title) in norm(cite),journal='; '.join(record.get('container-title',[])),volume=record.get('volume',''),pages=record.get('page',record.get('article-number','')),date=json.dumps(record.get('published',{}).get('date-parts',[])),url='https://doi.org/'+record.get('DOI',''))
    except Exception as e:result.update(status='retrieval failed',error=str(e),DOI=hit.DOI if known else '',url=hit.source_url_or_doi if known else '')
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(work,refs.items()))
t=pd.DataFrame(rows).sort_values('new_number');t.to_csv(O/'reference_checks_v5.csv',index=False)
print(t[['original_number','new_number','status','title_in_citation','volume','pages']].to_string(index=False))
