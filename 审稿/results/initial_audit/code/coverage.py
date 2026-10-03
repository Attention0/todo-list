import sys,json,pathlib,collections,argparse,pandas as pd
sys.path.insert(0,str(pathlib.Path('outputs/initial_audit/code').resolve()))
from audit import records
ap=argparse.ArgumentParser();ap.add_argument('--project',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);args=ap.parse_args();r=args.project/'data';o=args.out/'tables'
raw=list(records(r/'iclr2026_reviews_10000.jsonl'));nums=[x['submission_number'] for x in raw]
stats=[dict(metric='raw_submission_number_min',n=min(nums)),dict(metric='raw_submission_number_max',n=max(nums)),dict(metric='raw_missing_numbers_in_range',n=len(set(range(min(nums),max(nums)+1))-set(nums)))]
del raw
for name in ['profiles_cache.json','nameprism_nat.json','nameprism_eth.json']:
 obj=json.loads((r/name).read_text(encoding='utf-8'));stats.append(dict(metric=name+'_records',n=len(obj)))
 if name=='profiles_cache.json':
  for field in ['gender','race','country','expertise']:
   stats.append(dict(metric=name+'_'+field+'_nonempty',n=sum((v or {}).get(field) not in [None,'',[],{},'unknown','Unknown'] for v in obj.values())))
 del obj
pd.DataFrame(stats).to_csv(o/'additional_coverage.csv',index=False)
from datetime import datetime,timezone,timedelta
checks=collections.Counter()
for row in records(r/'replies_official-review.json'):
    for textcol,mscol in [('tcdate','cdate'),('tmdate','mdate')]:
        text=row.get(textcol);ms=row.get(mscol)
        if isinstance(text,str) and isinstance(ms,(float,int)):
            t=datetime.fromisoformat(text).replace(tzinfo=timezone.utc).timestamp()*1000
            checks[textcol+'_n']+=1
            checks[textcol+'_utc_equal_cdate']+=int(abs(t-ms)<1000)
            checks[textcol+'_shanghai_equal_cdate']+=int(abs(t-28800000-ms)<1000)
pd.DataFrame([dict(check=k,n=v) for k,v in checks.items()]).to_csv(o/'timezone_checks.csv',index=False)
# Immutable source fingerprints are separately rechecked after all analysis.
print('Supplemental coverage completed')

