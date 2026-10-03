"""Bounded primary-source retrieval; no survey data access."""
from pathlib import Path
import urllib.request,concurrent.futures,json,re
from pypdf import PdfReader
O=Path(__file__).resolve().parent; C=O/'research_cache';C.mkdir(exist_ok=True)
URLS={
'boehm':'https://jmboehm.github.io/Helicopter.pdf',
'fuster':'https://www.minneapolisfed.org/institute/working-papers/wp18-15.pdf',
'lee':'https://economics.fiu.edu/research/working-papers/2024/2402.pdf',
'pavlova':'https://fenix.iseg.ulisboa.pt/downloadFile/563083097460642/Pavlova%20%282025%29.pdf',
'savings':'https://idbinvest.org/en/download/15430',
'retirement':'https://www.adamleive.com/wp-content/uploads/2023/10/FLC_Crowdout_10_23.pdf',
'loot':'https://eprints.soton.ac.uk/505957/1/1-s2.0-S016726812400369X-main.pdf',
'jappelli':'https://www.riksbank.se/globalassets/media/rapporter/working-papers/2024/no.-443-intertemporal-mpc-and-shock-size.pdf'}
def one(kv):
 k,u=kv;p=C/(k+'.pdf');r={'id':k,'url':u,'accessed':'2026-10-03'}
 try:
  if not p.exists():
   op=urllib.request.build_opener(urllib.request.ProxyHandler({'https':'http://127.0.0.1:7897'}))
   p.write_bytes(op.open(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
  pages=[p.extract_text() or '' for p in PdfReader(p).pages];s='\n'.join(f'\n---PAGE {i+1}---\n'+t for i,t in enumerate(pages));(C/(k+'.txt')).write_text(s,encoding='utf8')
  r.update(status='full text retrieved',pages=len(pages),words=len(s.split()),figure_labels=sorted(set(re.findall(r'(?:Figure|Fig\.)\s*(\d+)',s))),table_labels=sorted(set(re.findall(r'Table\s*(\d+)',s))))
 except Exception as e:r.update(status='failed',error=str(e)[:200])
 return r
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(one,URLS.items()))
 (O/'primary_pdf_access.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows,indent=2))
