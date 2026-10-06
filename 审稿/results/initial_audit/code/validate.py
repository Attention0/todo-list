"""Check source immutability, aggregate consistency, parser boundaries and publication privacy."""
import argparse,csv,hashlib,json,pathlib,re,tempfile
import numpy as np,pandas as pd,statsmodels.api as sm,statsmodels.formula.api as smf
from audit import records,insts,time
ap=argparse.ArgumentParser();ap.add_argument('--project',required=True,type=pathlib.Path);ap.add_argument('--out',required=True,type=pathlib.Path);a=ap.parse_args();out=a.out
checks={}
for row in csv.DictReader((out/'tables/file_inventory.csv').open(encoding='utf-8')):
 p=a.project/row['path'];h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 assert h.hexdigest()==row['sha256'],row['path']
checks['unchanged_original_files']=23
for col in ['rating_initial','rating_final','confidence_initial','confidence_final']:
 assert pd.read_csv(out/'tables'/f'{col}_distribution.csv').n.sum()==29813
p=pd.read_csv(out/'tables/reviews_per_paper.csv');assert p.papers.sum()==7655;assert (p.reviews*p.papers).sum()==29813
checks['sample_and_distribution_totals']='pass'
with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
 p=pathlib.Path(tmp)/'fixture.json';expected=[{'x':'x'*1100000},{'x':[1,2,3]},None,5];p.write_text(json.dumps(expected),encoding='utf-8');assert list(records(p))==expected
 p.write_text('[{"x":',encoding='utf-8')
 try:list(records(p));raise AssertionError('accepted truncated JSON')
 except json.JSONDecodeError:pass
checks['streaming_parser_chunk_boundaries_and_truncation']='pass'
assert insts([{'start':None,'institution':{'domain':'test.invalid'}}])==set()
assert time('2025-10-30 08:50:07')==pd.Timestamp('2025-10-30 00:50:07',tz='UTC')
checks['missing_history_not_filled_and_shanghai_conversion']='pass'
q=pd.DataFrame({'paper':[1,1,1,2,2,2,3,3,3],'x':[0,1,0,1,0,1,0,1,1],'y':[2,4,3,8,5,7,3,6,5]})
z=q[['x','y']]-q.groupby('paper')[['x','y']].transform('mean');b=sm.OLS(z.y,z[['x']]).fit().params['x'];b2=smf.ols('y~x+C(paper)',q).fit().params['x'];assert abs(b-b2)<1e-10
checks['within_transform_matches_dummy_paper_FE']='pass'
files=[p for p in out.rglob('*') if '__pycache__' not in p.parts];patterns=[r'~[A-Za-z][A-Za-z_\.]+\d+',r'(?<![\w])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',r'gh[pousr]_[A-Za-z0-9]{20,}',r'sk-[A-Za-z0-9]{20,}',r'(?i)(?:password|api_key|access_token)\s*=\s*[\"\'][^\"\']+[\"\']']
for p in files:
 if not p.is_file():continue
 assert p.suffix in ['.md','.csv','.json','.py','.svg'],p.name
 assert p.stat().st_size<200000,p.name
 text=p.read_text(encoding='utf-8-sig')
 for pat in patterns:assert not re.search(pat,text),f'Privacy pattern match in {p.name}'
checks['publication_privacy_scan']='pass; no person IDs, emails or credential literals'
import matplotlib
checks['matplotlib_version']=matplotlib.__version__
(out/'VALIDATION.md').write_text('# Validation actually executed\n\n'+ '\n'.join(f'- {k}: {v}' for k,v in checks.items())+'\n\n审计完整运行成功；早期运行曾遇内存不足，已改为内容指纹与仅保留相关ID的集合后全量重跑成功。Supplemental coverage曾因null profile中断，修复后成功重跑。未重跑原网络采集、登录或写源文件的notebooks；旧图表均traced only。\n',encoding='utf-8')
print(json.dumps(checks,indent=2))
