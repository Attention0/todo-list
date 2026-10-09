"""Read-only source audit; writes aggregate evidence and local diagnostic history.

Run under WSL: python3 fertility/audit/reconcile_20261004.py
No model fitting and no source dataset modification.
"""
from pathlib import Path
import hashlib
import ast
import json
import numpy as np
import pandas as pd

ROOT = Path('/home/liuze/project-cmds_fertility')
HERE = Path(__file__).resolve().parent
# Reproduce the published population exactly, without rewriting old reports.
source = HERE / 'sample_definition_20260920.py'
ns = {'__file__': str(source)}
exec(compile(source.read_text().split('rows=[]')[0], str(source), 'exec'), ns)
d, m = ns['d'], ns['m']
base = pd.read_csv(ns['BASE'], low_memory=False)
e = {'base_n':len(base), 'master_n':len(m), 'duplicate_ids':int(base.mother_id.duplicated().sum()),
     'inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ns['BASE'],ns['LEGACY'],source]}}
fields = ['first_marriage_year','first_marriage_month','first_leave_year','first_leave_month',
          'current_arrive_year','current_arrive_month','origin_province_code','origin_province_name',
          'origin_county_code','origin_county_name','dest_city_name','dest_county_name',
          'migration_count_total','migration_city_count_total','first_move_start_year',
          'first_move_city_code','first_move_city_name','mother_marital_status','spouse_education',
          'spouse_hukou_nature','children_total_reported','child1_birth_year','child1_birth_month']
e['waves'] = []
for year,g in base.groupby('survey_year'):
    q=m[m.survey_year.eq(year)]
    e['waves'].append({'year':int(year),'base':len(g),'master':len(q),
                      'nonmissing':{c:int(g[c].notna().sum()) for c in fields if c in g},
                      'sources':g.children_count_source.value_counts(dropna=False).to_dict(),
                      'master_birth_age_range':[float(q.mother_birth_year.min()),float(q.mother_birth_year.max())] if len(q) else []})
by=m[ns['child_y']]
future=by.gt(m.survey_year,axis=0)
tooearly=by.lt(m.mother_birth_year+10,axis=0)
e['date_quality']={'future_child_women':int(future.any(axis=1).sum()),'child_before_maternal_age10':int(tooearly.any(axis=1).sum()),
 'arrival_age_over45':int(m.age_at_move.gt(45).sum()),'survey_age_over45':int((m.survey_year-m.mother_birth_year).gt(45).sum()),
 '2017_roster_total':int(m.survey_year.eq(2017).sum()),'2017_labeled_A':int((m.survey_year.eq(2017)&m.fertility_history_tier.eq('A')).sum())}
def count(flag):
    n=int(flag.sum());return {'n':n,'lost':len(m)-n,'lost_pct':round(100*(len(m)-n)/len(m),3)}
flags={
 'birth_direct_waves_2012_2016':m.survey_year.le(2016),
 'marriage_date':m.first_marriage_year.notna(),
 'origin_county_code':m.origin_county_code.notna(),
 'first_leave_known':m.first_leave_year.notna(),
 'same_leave_arrival_year':m.first_leave_year.eq(m.current_arrive_year),
 'reported_one_move':m.migration_count_total.eq(1),
 'reported_one_city':m.migration_city_count_total.eq(1),
 'explicit_multi':m.migration_count_total.gt(1)|m.migration_city_count_total.gt(1),
 'inferred_B':m.origin_quality_tier.eq('B'),
 'recent_2years':m.years_since_arrival.between(0,2),
 'work':m.current_move_reason_group.eq('work_business'),
 'education':m.current_move_reason_group.eq('study_training'),
 'cross_province':m.current_move_scope.eq(1),
 'within_province':m.current_move_scope.isin([2,3]),
 'known_nonfamily_nonmarriage':m.current_move_reason_group.notna() & ~m.current_move_reason_group.isin(['marriage','follow_family','care_family','kinship_network','elderly_migration']),
}
for k in [1,2,3,5]:
    birthnear=by.sub(m.current_arrive_year,axis=0).abs().le(k).any(axis=1)
    marnear=(m.first_marriage_year-m.current_arrive_year).abs().le(k)
    if k<=2:
        flags[f'birth_donut_pm{k}']=~birthnear
        flags[f'marriage_birth_donut_pm{k}_known_marriage']=m.first_marriage_year.notna()&~birthnear&~marnear
    if k!=2:
        flags[f'balanced_pm{k}_published']=m[f'balanced_pm{k}']
        flags[f'balanced_pm{k}_age15_45']=m.age_at_move.ge(15+k)&m.age_at_move.le(45-k)&m.years_since_arrival.ge(k)
e['subsamples']={k:count(v) for k,v in flags.items()}
e['reasons']=m.current_move_reason_group.fillna('missing').value_counts().to_dict()
e['marital']=m.mother_marital_status.value_counts(dropna=False).to_dict()
e['birth_relative_counts']={str(r):int(by.sub(m.current_arrive_year,axis=0).eq(r).any(axis=1).sum()) for r in range(-3,4)}
e['marriage_relative_counts']={str(r):int((m.first_marriage_year-m.current_arrive_year).eq(r).sum()) for r in range(-3,4)}
e['event_support_age15_45']={str(r):int((m.age_at_move.add(r).between(15,45)&m.years_since_arrival.ge(r)).sum()) for r in range(-10,11)}
e['parity_at_arrival']=by.lt(m.current_arrive_year,axis=0).sum(axis=1).value_counts().sort_index().to_dict()
e['year_ranges']={'move':[float(m.current_arrive_year.min()),float(m.current_arrive_year.max())],
                  'survey':[float(m.survey_year.min()),float(m.survey_year.max())]}
# Graph of the existing legacy province sample, with locations as shared nodes.
l=pd.read_csv(ns['LEGACY'],low_memory=False)
e['legacy_columns']=list(l.columns)
oc='origin_prov';dc='dest_prov'
if {oc,dc}<=set(l):
    od=l.groupby([oc,dc]).size();adj={}
    for a,b in od.index:
        adj.setdefault(str(a),set()).add(str(b));adj.setdefault(str(b),set()).add(str(a))
    seen=set();components=[]
    for a in adj:
        if a in seen:continue
        todo=[a];comp=set()
        while todo:
            v=todo.pop()
            if v in comp:continue
            comp.add(v);todo.extend(adj[v]-comp)
        seen|=comp;components.append(len(comp))
    e['legacy_graph']={'women':len(l),'origins':l[oc].nunique(),'destinations':l[dc].nunique(),
      'directed_od':len(od),'components':components,'od_quantiles':od.quantile([.25,.5,.75,.9]).to_dict(),
      'od_under5':int(od.lt(5).sum()),'degree_min':min(map(len,adj.values())), 'degree_max':max(map(len,adj.values()))}
e['legacy_gap']=l.delta_birth_pre3.describe(percentiles=[.01,.25,.5,.75,.99]).to_dict()
e['legacy_gap_sign']={'positive':int(l.delta_birth_pre3.gt(0).sum()),'negative':int(l.delta_birth_pre3.lt(0).sum()),'zero':int(l.delta_birth_pre3.eq(0).sum())}
# Read only the literal source paths and geography mapper, not analysis modules.
import re
tree=ast.parse((ROOT/'code/marriage_fertility_geography.py').read_text())
env={'pd':pd,'np':np,'re':re,'Path':Path}
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['BIRTH_XLSX','PROVINCES','VALID_PROV'] for t in node.targets):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'source','exec'),env)
    if isinstance(node,ast.FunctionDef) and node.name=='pcode':
        exec(compile(ast.Module(body=[node],type_ignores=[]),'source','exec'),env)
pc=env['pcode']
m['origin_prov']=m.origin_province_code.map(pc).combine_first(m.origin_province_name.map(pc)).combine_first(m.origin_best_available.map(pc))
m['dest_prov']=m.dest_city_code.map(pc).combine_first(m.dest_province_name.map(pc))
rawmacro=pd.read_excel(env['BIRTH_XLSX'],sheet_name='原始数据')
rawmacro['prov']=pd.to_numeric(rawmacro['行政区划代码'],errors='coerce')//10000
rawmacro['year']=pd.to_numeric(rawmacro['年份'],errors='coerce')
rawmacro['rate']=pd.to_numeric(rawmacro['人口出生率(‰)'],errors='coerce')
lookup=rawmacro.drop_duplicates(['prov','year']).set_index(['prov','year']).rate
def premean(prov,year):
    return np.mean([lookup.get((prov,year-j),np.nan) for j in [1,2,3]])
m['origin_pre3']=[premean(p,t) for p,t in zip(m.origin_prov,m.current_arrive_year)]
m['dest_pre3']=[premean(p,t) for p,t in zip(m.dest_prov,m.current_arrive_year)]
m['gap']=m.dest_pre3-m.origin_pre3
e['broad_cbr']={'matched':count(m.gap.notna()),'zero':int(m.gap.eq(0).sum()),'positive':int(m.gap.gt(0).sum()),'negative':int(m.gap.lt(0).sum()),
 'by_wave':{int(y):int(g.gap.notna().sum()) for y,g in m.groupby('survey_year')},
 'invalid_province':int((m.origin_prov.isna()|m.dest_prov.isna()).sum()),
 'year_min':float(rawmacro.year.min()),'year_max':float(rawmacro.year.max()),
 'duplicate_province_year':int(rawmacro.duplicated(['prov','year']).sum())}
joined=m[['mother_id','gap']].merge(l[['mother_id','delta_birth_pre3']],on='mother_id')
assert np.allclose(joined.gap,joined.delta_birth_pre3,equal_nan=True)
e['broad_cbr']['legacy_overlap_verified']=len(joined)
od=m.groupby(['origin_prov','dest_prov']).size()
adj={}
for a,b in od.index:
    adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
seen=set();components=[]
for node in adj:
    if node in seen:continue
    todo=[node];comp=set()
    while todo:
        v=todo.pop()
        if v in comp:continue
        comp.add(v);todo.extend(adj[v]-comp)
    seen|=comp;components.append(len(comp))
e['broad_graph']={'valid_women':int(od.sum()),'origins':int(m.origin_prov.nunique()),'destinations':int(m.dest_prov.nunique()),
 'directed_od':len(od),'components':components,'od_quantiles':od.quantile([.25,.5,.75,.9]).to_dict(),
 'od_under5':int(od.lt(5).sum()),'degree_excluding_self':{str(k):len(v-{k}) for k,v in adj.items()},
 'destination_counts':m.dest_prov.value_counts().to_dict()}
e['unmarried_selection']={str(y):{'base_unmarried':int(g.mother_marital_status.eq(1).sum()),
 'master_unmarried':int(m.loc[m.survey_year.eq(y),'mother_marital_status'].eq(1).sum())} for y,g in base.groupby('survey_year')}
# Small history kept OUTSIDE git: real respondent IDs are never published.
hist=[]
for year,g in m.groupby('survey_year'):
    for _,z in g.head(2).iterrows():
        births=z[ns['child_y']].dropna().to_numpy(dtype=float)
        for t in range(int(max(z.mother_birth_year+15,z.current_arrive_year-3)),int(min(z.mother_birth_year+45,z.survey_year-1,z.current_arrive_year+3))+1):
            hist.append({'id':z.mother_id,'calendar_year':t,'age':t-z.mother_birth_year,
             'location':'hukou_ASSUMED' if t<z.current_arrive_year else 'current_destination_ASSUMED',
             'event_time':t-z.current_arrive_year,'ever_married_proxy':None if pd.isna(z.first_marriage_year) else int(t>=z.first_marriage_year),
             'parity_start':int((births<t).sum()),'birth':int((births==t).any())})
local=HERE.parents[2]/'diagnostic_private_20261004';local.mkdir(exist_ok=True)
pd.DataFrame(hist).to_csv(local/'person_year_diagnostic.csv',index=False)
e['diagnostic_history']={'rows':len(hist),'persons':pd.DataFrame(hist).id.nunique(),'path_local_only':str(local/'person_year_diagnostic.csv')}
# Optional raw module coverage: extract only aggregate nonmissing counts.
raw=Path('/mnt/g/桌面/科研/数据-CMDS流动人口/cmds2017a卷.dta')
e['settlement_raw_path_exists']=raw.exists()
if raw.exists():
    with pd.read_stata(raw,iterator=True,convert_categoricals=False) as reader:
        labels=reader.variable_labels()
    cols=[c for c in ['newID','q101a1','q101b1','Q314','Q315','Q317','Q318','Q321A'] if c in labels]
    rr=pd.read_stata(raw,columns=cols,convert_categoricals=False)
    rr=rr[('2017_'+rr.newID.astype(str)).isin(set(m.mother_id))]
    rr=rr.replace(r'^\s*$',np.nan,regex=True)
    e['settlement_2017']={c:{'label':labels[c],'nonmissing':int(rr[c].notna().sum()),'values':rr[c].value_counts().head(8).to_dict()} for c in cols if c.startswith('Q')}
    e['questionnaire_raw_discrepancy_2017']={p:[c for c in labels if c.upper().startswith(p)] for p in ['Q412','Q413','Q414','Q415','Q416','Q417','Q418']}
def clean(o):
    if isinstance(o,dict):return {str(k):clean(v) for k,v in o.items()}
    if isinstance(o,list):return [clean(v) for v in o]
    if isinstance(o,(np.integer,np.floating)):return o.item()
    return o
(HERE/'reconciliation_evidence.json').write_text(json.dumps(clean(e),ensure_ascii=False,indent=2),encoding='utf-8')
assert len(m)==362245 and not base.mother_id.duplicated().any()
assert all(v['n']+v['lost']==len(m) for v in e['subsamples'].values())
print(json.dumps({'master':len(m),'cbr_match':e['broad_cbr']['matched'],'checks':'passed'},ensure_ascii=False))
