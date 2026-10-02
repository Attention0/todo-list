"""Outcome-blind eligibility inventory and reuse of pre-existing X transformations."""
from pathlib import Path
import sys,argparse,json,hashlib,subprocess,io,re
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'mpc_who_drives'))
import who_drives as wd
prior=wd.prior
OLD='5d4b7819d27a390fa4931ed4c54c23f1521fe768'
SUBJ=['q01_lifesat','q02_safety','q03a_fair_dist','q03b_fair_opp','q03c_fair_rule','q04_trust_gov','q05_trust_soc','q06_socsec','q07_emergfund','q08_support','q09_gain','q10_effort','q11_mobility','q12_voice','q13_pressure','q15_fut_self','q16_fut_society','q17a_fut_econ','q17b_fut_job','q17c_fut_price','q17d_fut_fair','q17e_fut_welfare','q18_ses_now','q19_ses_past5','q20_ses_next1','q21_order','q22_vitality']
ORDERED=['q43_edu','income_h','q28_hhsize','q29_foodexp','q30_medexp','q49_citytier']
DOMAINS={'subjective_economic':['q06_socsec','q07_emergfund','q09_gain','q10_effort','q11_mobility','q13_pressure','q15_fut_self','q17a_fut_econ','q17b_fut_job','q17c_fut_price','q17e_fut_welfare','q18_ses_now','q19_ses_past5','q20_ses_next1'], 'social_confidence':['q02_safety','q03a_fair_dist','q03b_fair_opp','q03c_fair_rule','q04_trust_gov','q05_trust_soc','q08_support','q12_voice','q17d_fut_fair','q21_order','q22_vitality'], 'wellbeing_optimism':['q01_lifesat','q15_fut_self','q16_fut_society','q17a_fut_econ','q20_ses_next1']}

def git_csv(path):
    return pd.read_csv(io.StringIO(subprocess.check_output(['git','show',OLD+':消费调查/'+path]).decode('utf-8')))

def frozen_pca(data,out):
    path=out/'frozen_prior_pca.csv'
    if path.exists():
        cached=pd.read_csv(path)
        if cached['item'].isin(data.columns).all():return cached
    # Reuse old component directions; no PCA fit or new component selection.
    rows=[];half=np.random.default_rng(20260921).random(len(data))<.5
    load=git_csv('tables/final_latent_loadings.csv')
    for domain,items in DOMAINS.items():
        scaler=StandardScaler().fit(data.loc[half,items]);ll=load[load.domain.eq(domain)]
        for r in ll.itertuples():
            j=items.index(r.item);rows.append(dict(construct=domain+'_pc'+str(r.factor),item=r.item,loading=r.loading,center=scaler.mean_[j],scale=scaler.scale_[j],source='final_exploration.py/latent_dimensions; frozen discovery-half',source_commit=OLD))
    # Existing NHB diagnostic PCA directions, ALL retained in that diagnostic.
    # These are not newly fitted/selected latent dimensions and are NOT validated indices.
    nhb='92695b79d8f3de1c01fbc4f5ca06da7012bf327c'
    def get(path):return pd.read_csv(io.StringIO(subprocess.check_output(['git','show',nhb+':消费调查/results/nhb_reanalysis/'+path]).decode('utf-8')))
    ll=get('final_subjective_pca_loadings.csv');eig=get('final_subjective_pca_eigenvalues.csv').set_index('component');items=list(ll.item);scaler=StandardScaler().fit(data[items])
    for j,row in ll.iterrows():
        for pc in [c for c in ll if c.startswith('PC')]:
            k=int(pc[2:]);rows.append(dict(construct='diagnostic_global_'+pc.lower(),item=row['item'],loading=row[pc]/np.sqrt(eig.loc[k,'eigenvalue']),center=scaler.mean_[j],scale=scaler.scale_[j],source='NHB final_verification.py/subjective_diagnostics; diagnostic direction, not validated score',source_commit=nhb))
    t=pd.DataFrame(rows);t.to_csv(path,index=False);return t

def make_inventory(data,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);raw=pd.read_stata(data,convert_categoricals=False);reader=pd.io.stata.StataReader(data);labels=reader.variable_labels();d=prior.prepare(data);X={};rows=[];mapping=[];definitions={}
    def add(name,value,label,origin,domain,kind,source,timing,eligible=True,reason='',transform='identity',components=None,provenance='raw .dta'):
        val=pd.Series(value,index=d.index);missing=int(val.isna().sum());unique=int(val.nunique());eligible=eligible and unique>1
        if unique<=1:reason=(reason+'; ' if reason else '')+'no effective variation'
        family=name
        comps=components or [name]
        if origin=='constructed':family=','.join(comps)
        row=dict(variable=name,label=label,origin=origin,domain=domain,kind=kind,timing=timing,source_question=source,missing_N=missing,missing_rate=missing/len(d),unique_values=unique,eligible=eligible,exclusion_reason=reason,transformation=transform,components='|'.join(comps),provenance=provenance,construct_family=family)
        rows.append(row)
        if eligible:X[name]=val;definitions[name]=dict(kind=kind,origin=origin,domain=domain,components=comps,transform=transform)
        if origin=='constructed':
            for c in comps:mapping.append(dict(constructed=name,raw_component=c,relationship=transform,provenance=provenance,eligible=eligible))
    for c in raw:
        q=int(re.match(r'q(\d+)',c).group(1)) if re.match(r'q(\d+)',c) else None
        if c=='id':timing='identifier';kind='identifier';eligible=False;reason='respondent identifier'
        elif c.startswith('scen_') or q in range(32,41):timing='outcome' if c=='scen_mpc' or q in range(32,41) else 'treatment';kind='categorical';eligible=False;reason='randomized assignment / scenario outcome, never baseline X'
        elif q is not None and (q<=31 or q>=41):
            timing='pre-treatment';eligible=True;reason='';kind='numeric' if c in SUBJ or c=='q42_age' else 'binary' if q==14 else 'categorical'
        else:timing='unclear';kind='unclear';eligible=False;reason='timing/provenance unverified'
        domain='subjective' if q is not None and q<=22 else 'objective'
        add(c,raw[c],labels.get(c,c),'raw',domain,kind,'Q'+str(q) if q else 'platform',timing,eligible,reason,provenance='Questionnaire Q1–31 precede scenario; Q41–49 platform background, not elicited scenario responses')
    income=d.income
    add('income_h',income,'Harmonized PERSONAL monthly income rank','constructed','objective','numeric','Q46','pre-treatment',components=['q46_income'],transform='legacy11–16 minus10, else identity',provenance='PR3 heterogeneity_formal.prep')
    add('income',income,'Same harmonized income rank, PR9 alias','constructed','objective','numeric','Q46','pre-treatment',components=['q46_income'],transform='same as income_h',provenance='PR9 prepare')
    for c in ['q42_age']+SUBJ+ORDERED:
        val=income if c=='income_h' else d[c];source=['q46_income'] if c=='income_h' else [c]
        add(c+'_z',(val-val.mean())/val.std(),'Existing standardized '+c,'constructed','subjective' if c in SUBJ else 'objective','numeric',','.join(source),'pre-treatment',components=source,transform='R mean/sample SD rank or scale',provenance='PR3 heterogeneity_formal.prep CONT+ORDERED')
    for c in ['q41_gender','q23_hukou','q24_workstat','q25_unittype','q26_housing','q27_minorchild','q31_gotsubsidy']:
        binary=d[c].nunique()==2
        add(c+'_z',(d[c]-d[c].mean())/d[c].std(),'Earlier standardized category code '+c,'constructed','objective','numeric',c,'pre-treatment',binary,'unordered multi-category code cannot be treated as numeric trend' if not binary else '',components=[c],transform='earlier R standardization; binary codes only remain legal scalar',provenance='PR3 heterogeneity_analysis.prep FEATURES; invalid nominal trends excluded')
    for name,c in [('need','q30_medexp'),('foodneed','q29_foodexp'),('liquidity','q07_emergfund'),('income_z','income_h')]:
        val=income if c=='income_h' else d[c]
        add(name,(val-val.mean())/val.std(),'PR9 standardized '+c,'constructed','subjective' if c=='q07_emergfund' else 'objective','numeric',c,'pre-treatment',components=['q46_income'] if c=='income_h' else [c],transform='R rank/scale standardized alias',provenance='PR9 prepare')
    xx,gr,meta=wd.covariates(d)
    for v in gr:
        comps=[wd.RAW[v]] if v in wd.RAW else ['q27_minorchild'] if v=='minor_child' else [wd.CATEGORIES[v][0]]
        comps=['q46_income' if c=='income' else c for c in comps]
        for col in gr[v]:add('who::'+col,xx[col],'PR11 standardized '+col,'constructed','subjective' if v=='liquidity' else 'objective','numeric',','.join(comps),'pre-treatment',components=comps,transform='R standardized rank or dummy; categorical reference unchanged',provenance='PR11 covariates; numerical aliases remain distinct inventoried tests')
    for v,b in wd.bins(d).items():
        val=b.cat.codes+1 if isinstance(b.dtype,pd.CategoricalDtype) else b.map({'yes':1,'no':2,'unknown':3})
        comp={'liquidity':'q07_emergfund','income':'q46_income','food':'q29_foodexp','medical':'q30_medexp','subsidy':'q31_gotsubsidy'}[v]
        add('group::'+v,val,'Existing fixed PR11 '+v+' partition','constructed','subjective' if v=='liquidity' else 'objective','categorical',comp,'pre-treatment',components=[comp],transform='fixed PR11 bins (not outcome-selected)',provenance='PR11 bins')
    add('need_group',pd.cut(d.q30_medexp,[0,2,4,6]).cat.codes+1,'PR9 fixed annual medical need partition','constructed','objective','categorical','Q30','pre-treatment',components=['q30_medexp'],transform='rank1–2 / 3–4 / 5–6',provenance='PR9 run')
    add('age_squared',d.q42_age**2,'Existing fixed control age squared','constructed','objective','numeric','Q42','pre-treatment',components=['q42_age'],transform='age squared',provenance='PR9 CONTROLS')
    lower=d.q29_foodexp.map({1:0,2:501,3:1001,4:2001,5:3001,6:5001})*6
    add('food_lower6',lower,'Six-month lower-bound baseline Food expenditure','constructed','objective','numeric','Q29','pre-treatment',components=['q29_foodexp'],transform='6 × lower bounds [0,501,1001,2001,3001,5001]',provenance='PR9 bound sensitivity')
    add('food_upper6',d.q29_foodexp.map({1:500,2:1000,3:2000,4:3000,5:5000,6:np.inf})*6,'Six-month upper bound, top bin unbounded','constructed','objective','numeric','Q29','pre-treatment',False,'upper bound infinity is not observed expenditure; no invented finite top cap',components=['q29_foodexp'],provenance='PR9 bounds')
    add('strict_all_amounts',lower>5000,'Common Food-inframarginal baseline group','constructed','objective','binary','Q29','pre-treatment',components=['q29_foodexp'],transform='lower6 > 5000, fixed not assigned amount',provenance='PR9 fixed sample')
    pca=frozen_pca(d,out)
    for name,g in pca.groupby('construct',sort=False):
        val=sum((d[r.item]-r.center)/r.scale*r.loading for r in g.itertuples())
        add(name,val,name+' (previous component direction, no new fit)','constructed','subjective','numeric','|'.join(g.item),'pre-treatment',components=list(g.item),transform='frozen previous PCA loadings/centers/scales',provenance=g.source.iloc[0])
    # Every transient pre-existing respondent field is inventoried, even when excluded.
    aliases={'scenario_n':'quality','treatment_cell':'treatment','transfer_type':'treatment','type':'treatment','form':'treatment','amount':'treatment','z':'treatment','cell':'treatment','outcome_ord':'outcome','outcome':'outcome','ordinal':'outcome','mpc':'outcome','mpc_midpoint':'outcome','midpoint':'outcome','mpc_alt':'outcome','alt_top':'outcome','any_spend':'outcome','any_spending':'outcome','mpc_10plus':'outcome','ge10':'outcome','mpc_25plus':'outcome','ge25':'outcome','high_mpc':'outcome','mpc_50plus':'outcome','ge50':'outcome','top75':'outcome','clean':'quality','clean_candidate':'quality','sample_A':'quality','sample_C':'quality','sample_Q1':'quality','sample_Q2':'quality','scale_sd':'quality','unique_n':'quality','extreme_share':'quality','mid_share':'quality','entropy':'quality','cate_oof':'outcome','cate':'outcome','cate_c':'outcome','tau':'outcome','tc':'outcome','quintile':'outcome','q':'outcome','person_score':'outcome','W':'treatment','strict_assigned':'treatment','very_strict_assigned':'treatment','likely_binding':'treatment','possibly_inframarginal':'treatment','fold_id':'identifier'}
    for name,t in aliases.items():
        if name in {r['variable'] for r in rows}:continue
        val=d[name] if name in d else pd.Series(np.nan,index=d.index)
        add(name,val,'Prior pipeline transient '+name,'constructed','metadata','numeric','prior scripts',t,False,'quality/style diagnostics not substantive X' if t=='quality' else 'treatment/outcome-derived or training score/identifier; prohibited X',components=['prior script expression'],provenance='PR3–PR11 analysis scripts; values absent from original data not re-fitted')
    inv=pd.DataFrame(rows);inv.to_csv(out/'all_x_variable_inventory.csv',index=False);pd.DataFrame(mapping).to_csv(out/'raw_constructed_mapping.csv',index=False)
    (out/'screen_definitions.json').write_text(json.dumps(definitions,ensure_ascii=False,indent=2),encoding='utf-8')
    state=dict(phase='inventory_complete_before_regressions',N=len(d),original_fields=len(raw.columns),inventory_fields=len(inv),eligible=len(X),data_sha256=hashlib.sha256(Path(data).read_bytes()).hexdigest(),inventory_sha256=hashlib.sha256((out/'all_x_variable_inventory.csv').read_bytes()).hexdigest(),mapping_sha256=hashlib.sha256((out/'raw_constructed_mapping.csv').read_bytes()).hexdigest(),previous_source_commit=OLD,prior11='d5a34e29b0ba575993c433f4e8825bbd88b121f4',regressions_run=False)
    (out/'inventory_manifest.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
    print(json.dumps(state,indent=2));return d,pd.DataFrame(X),inv,definitions

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('--out',default=str(ROOT));a=p.parse_args();make_inventory(a.data,a.out)
