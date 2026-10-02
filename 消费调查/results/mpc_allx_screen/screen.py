"""Locked all-X slope screen. Aggregate exports only; no respondent predictions."""
from pathlib import Path
import argparse,json,hashlib,warnings
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import StratifiedKFold
from inventory import make_inventory,ROOT,wd

Y_NAMES=['ordinal','midpoint','top75']
TARGETS={'cash':np.array([1.,0,0]),'rc':np.array([-1.,.5,.5]),'food_cash':np.array([-1.,1,0]),'medical_cash':np.array([-1.,0,1])}
SEED=20261005
ORDERED_FACTORS={'q43_edu','q28_hhsize','q29_foodexp','q30_medexp','q49_citytier','need_group','group::liquidity','group::income','group::food','group::medical'}

def encode(s,kind):
    if kind=='categorical':
        levels=sorted(s.dropna().unique());a=np.column_stack([(s==v).astype(float) for v in levels[1:]])
        return a,levels,1.
    sd=s.std();return ((s-s.mean())/sd).to_numpy()[:,None],None,sd

def support(d,a,levels=None,arms=None):
    if levels is not None:
        # Each factor level must identify its own form-specific amount slope.
        cats=np.argmax(np.column_stack([1-a.sum(axis=1),a]),axis=1)
        for f in arms or wd.FORMS:
            for j in range(len(levels)):
                ix=(d.form.to_numpy()==f)&(cats==j)
                if ix.sum()<3 or d.loc[ix,'z'].nunique()<2:return 'sparse category/form: N<3 or fewer than two amounts'
    return ''

def hc3(b,y):
    if len(b)<=b.shape[1] or np.linalg.matrix_rank(b)!=b.shape[1]:raise ValueError('rank deficient design')
    inverse=np.linalg.inv(b.T@b);beta=inverse@b.T@y;res=y-b@beta;h=np.sum((b@inverse)*b,axis=1)
    if np.max(h)>=1-1e-9:raise ValueError('HC3 saturated leverage')
    scores=b*(res/(1-h))[:,None];cov=inverse@(scores.T@scores)@inverse
    return beta,cov

def fit(d,a,y,levels=None,controls=None,arms=None):
    fail=support(d,a,levels,arms)
    if fail:raise ValueError(fail)
    z=d.z.to_numpy();b=np.column_stack([np.ones(len(d)),z,a,z[:,None]*a]);removed=0
    if controls is not None:
        for col in controls.T:
            if np.linalg.matrix_rank(np.column_stack([b,col]))>b.shape[1]:b=np.column_stack([b,col])
            else:removed+=1
    beta=[];cov=[]
    for f in wd.FORMS:
        if arms is not None and f not in arms:
            beta.append(np.zeros(b.shape[1]));cov.append(np.zeros((b.shape[1],b.shape[1])));continue
        ix=d.form.to_numpy()==f;bb,cc=hc3(b[ix],np.asarray(y)[ix]);beta.append(bb);cov.append(cc)
    return np.array(beta),np.array(cov),removed

def extract(model,w,k,require_wald=True):
    beta,cov,_=model;ix=np.arange(2+k,2+2*k);b=w@beta[:,ix];v=sum(w[j]**2*cov[j][np.ix_(ix,ix)] for j in range(3))
    identified=np.linalg.matrix_rank(v)==k
    if require_wald and not identified:raise ValueError('singular moderation covariance')
    stat=float(b@np.linalg.solve(v,b)) if identified else np.nan;p=float(stats.chi2.sf(stat,k)) if identified else np.nan;se=np.sqrt(np.maximum(0,np.diag(v)))
    scalar=k==1
    return dict(estimate=float(b[0]) if scalar else np.nan,se=float(se[0]) if scalar else np.nan,lo=float(b[0]-1.96*se[0]) if scalar else np.nan,hi=float(b[0]+1.96*se[0]) if scalar else np.nan,wald=stat,df=k,p=p,profile=json.dumps(b.tolist()),profile_se=json.dumps(se.tolist())),b,se

def direction(profiles):
    if any(not isinstance(p,str) for p in profiles):return False,np.nan
    a=[np.array(json.loads(p)) for p in profiles]
    if len(a[0])==1:return bool(all(np.sign(v[0])==np.sign(a[0][0]) and v[0]!=0 for v in a)),1. if all(np.sign(v[0])==np.sign(a[0][0]) for v in a) else -1.
    norms=[np.linalg.norm(v) for v in a]
    if min(norms)==0:return False,np.nan
    cs=[a[i]@a[j]/(norms[i]*norms[j]) for i,j in [(0,1),(0,2),(1,2)]]
    major=any(np.any((np.abs(a[i])/norms[i]>.5)&(np.sign(a[i])!=np.sign(a[j]))) for i in range(3) for j in range(3))
    return min(cs)>0 and not major,float(min(cs))

def scan(d,X,inv,defs,out):
    rows=[];components=[];slopes=[];codes={};ys={y:d[y].to_numpy() for y in Y_NAMES}
    for n,(var,info) in enumerate(defs.items()):
        ok=X[var].notna();dd=d.loc[ok];a,lev,sd=encode(X.loc[ok,var],info['kind']);codes[var]=(a,lev,sd,ok.to_numpy());models={}
        for y in Y_NAMES:
            for target,w in TARGETS.items():
                reason='';key=(y,'cash' if target=='cash' else 'full')
                if key not in models:
                    try:models[key]=fit(dd,a,ys[y][ok],lev,arms=['cash'] if target=='cash' else None)
                    except (ValueError,np.linalg.LinAlgError) as e:models[key]=None;models[key+('reason',)]=str(e)
                model=models[key];reason=models.get(key+('reason',),'')
                r=dict(variable=var,outcome=y,target=target,N=int(dd.form.eq('cash').sum()) if target=='cash' else len(dd),cash_N=int(dd.form.eq('cash').sum()),R_complete_case_N=len(dd),origin=info['origin'],domain=info['domain'],kind=info['kind'],status='ok' if model is not None else 'nonestimable',failure_reason=reason,family_size=len(defs))
                if model is not None:
                    result,b,se=extract(model,w,a.shape[1]);r.update(result)
                    r['original_unit_estimate']=r['estimate']/sd if lev is None else np.nan
                    r['direction_projection']=float(b[0]) if lev is None else float(np.arange(1,len(lev))@b/np.sum(np.arange(1,len(lev))**2)) if var in ['q43_edu','q28_hhsize','q29_foodexp','q30_medexp','q49_citytier'] else np.nan
                    for j in range(a.shape[1]):
                        cat=lev[j+1] if lev is not None else 'per_SD';catN=int((X.loc[ok,var]==cat).sum()) if lev is not None else len(dd)
                        if catN>=10:components.append(dict(variable=var,outcome=y,target=target,category=cat,reference=lev[0] if lev is not None else 'R mean',N=catN,estimate=b[j],se=se[j],lo=b[j]-1.96*se[j],hi=b[j]+1.96*se[j],p=2*stats.norm.sf(abs(b[j]/se[j])),multiplicity='nominal diagnostic, not co-primary'))
                    if lev is not None and target in ['cash','rc']:
                        beta,cov,_=model;k=a.shape[1]
                        for j,cat in enumerate(lev):
                            catN=int((X.loc[ok,var]==cat).sum())
                            if catN<10:continue
                            v=np.zeros(beta.shape[1]);v[1]=1
                            if j:v[2+k+j-1]=1
                            for f in range(3):
                                if target=='cash' and f!=0:continue
                                if target=='rc' and f==0:continue
                                estimate=float(v@beta[f]);s=float(np.sqrt(v@cov[f]@v));slopes.append(dict(variable=var,outcome=y,category=cat,form=wd.FORMS[f],N=catN,estimate=estimate,se=s,lo=estimate-1.96*s,hi=estimate+1.96*s))
                rows.append(r)
        if (n+1)%20==0:print('Primary screen',n+1,'/',len(defs),flush=True)
    t=pd.DataFrame(rows);t['q']=np.nan;t['holm_p']=np.nan
    for target in ['cash','rc']:
        for y in Y_NAMES:
            ix=t.index[t.target.eq(target)&t.outcome.eq(y)];p=t.loc[ix,'p'].fillna(1).to_numpy();t.loc[ix,'q']=multipletests(p,method='fdr_bh')[1];t.loc[ix,'holm_p']=multipletests(p,method='holm')[1]
            bad=ix[t.loc[ix,'status'].ne('ok')];t.loc[bad,['q','holm_p']]=np.nan
            t.loc[ix].sort_values(['q','variable'],na_position='last').to_csv(out/f'allx_{target}_{y}.csv',index=False)
    t.to_csv(out/'all_screen_results.csv',index=False);pd.DataFrame(components).to_csv(out/'component_contrasts.csv',index=False);pd.DataFrame(slopes).to_csv(out/'categorical_form_slopes.csv',index=False)
    return t,codes

def concordance(t,defs,out):
    rows=[]
    for target in ['cash','rc']:
        for var,info in defs.items():
            g=t[t.variable.eq(var)&t.target.eq(target)].set_index('outcome').reindex(Y_NAMES);consistent,cos=direction(g.profile.tolist());q=g.q.to_numpy();count=int(np.sum(q<.1));r=dict(variable=var,target=target,origin=info['origin'],domain=info['domain'],kind=info['kind'],construct_family='|'.join(info['components']),direction_consistent=consistent,min_profile_cosine=cos,fdr_outcomes=count,min_q=np.nanmin(q) if np.isfinite(q).any() else np.nan,representation_corroborated=False)
            for y in Y_NAMES:
                for col in ['estimate','direction_projection','p','q','holm_p','profile']:r[y+'_'+col]=g.loc[y,col]
            r['tier']='A_provisional' if count>=2 and consistent else 'B' if count==1 and consistent else 'C' if count==0 and g.p.min()<.05 else 'D';rows.append(r)
    c=pd.DataFrame(rows);mapping=[]
    loads=pd.read_csv(out/'frozen_prior_pca.csv')
    for ix,r in c.iterrows():
        var=r.variable;info=defs[var];same=c[(c.target==r.target)&(c.variable!=var)&(c.construct_family==r.construct_family)]
        broad=[];hits=[]
        for comp in info['components']:
            raw=c[(c.target==r.target)&(c.variable==comp)]
            if raw.empty:continue
            rr=raw.iloc[0];loading=1.
            ll=loads[(loads.construct==var)&(loads.item==comp)]
            if len(ll):loading=ll.loading.iloc[0]
            aligned=all(np.sign(r[y+'_estimate'])==np.sign(rr[y+'_estimate']*loading) for y in Y_NAMES) if np.isfinite(r.ordinal_estimate) and np.isfinite(rr.ordinal_estimate) else np.nan
            if aligned is True or aligned==True:broad.append(comp)
            if rr.fdr_outcomes>0 and (aligned is True or aligned==True):hits.append(comp)
            if info['origin']=='constructed':
                for y in Y_NAMES:mapping.append(dict(constructed=var,raw_component=comp,target=r.target,outcome=y,loading=loading,construct_estimate=r[y+'_estimate'],construct_profile=r[y+'_profile'],construct_p=r[y+'_p'],construct_q=r[y+'_q'],raw_estimate=rr[y+'_estimate'],raw_profile=rr[y+'_profile'],raw_p=rr[y+'_p'],raw_q=rr[y+'_q'],aligned=aligned,raw_profile_cosine=rr.min_profile_cosine,comparison='factor versus scalar profile; not signed' if info['kind']!=defs[comp]['kind'] and defs[comp]['kind']=='categorical' else 'loading oriented'))
        # Affine copies are deliberately not independent representation support.
        if len(info['components'])>1:corroborated=len(broad)>=2 and len(hits)>=2
        else:
            # Binary numeric/dummy copies are affine, not distinct representation evidence.
            alternatives=same[same.kind.eq('categorical') & same.fdr_outcomes.ge(2)&same.direction_consistent] if info['kind']!='categorical' else same[same.kind.eq('numeric') & same.fdr_outcomes.ge(2)&same.direction_consistent]
            corroborated=len(alternatives)>0
        c.loc[ix,'representation_corroborated']=corroborated;c.loc[ix,'aligned_raw_components']=len(broad);c.loc[ix,'aligned_fdr_raw_components']=len(hits)
        if r.tier=='A_provisional':c.loc[ix,'tier']='A' if corroborated else 'D_uncorroborated_cross_outcome'
    c['shortlisted']=False
    for target in ['cash','rc']:
        ix=c.index[c.target.eq(target)&c.tier.eq('A')].tolist()+c[c.target.eq(target)&c.tier.eq('B')].sort_values(['min_q','variable']).head(5).index.tolist();c.loc[ix,'shortlisted']=True
    c.to_csv(out/'cross_outcome_concordance.csv',index=False)
    m=pd.DataFrame(mapping);m['construct_component_interpretation']='absent in raw FDR / direction diagnostic only'
    if len(m):
        for (v,target),g in m.groupby(['constructed','target']):
            nn=g[g.raw_q.lt(.1)].raw_component.nunique();aligned=g[g.aligned.eq(True)].raw_component.nunique();label='broad across components' if nn>=2 and aligned>=2 else 'one FDR raw item' if nn==1 else 'canceled / opposing components' if aligned==0 else 'absent in raw FDR; direction only';m.loc[g.index,'construct_component_interpretation']=label
    m.to_csv(out/'raw_constructed_concordance.csv',index=False)
    summary=[]
    for (target,y,domain,origin),g in t[t.target.isin(['cash','rc'])].groupby(['target','outcome','domain','origin']):
        cc=c[(c.target==target)&c.variable.isin(g.variable)]
        summary.append(dict(target=target,outcome=y,domain=domain,origin=origin,X_screened=len(g),estimable=int(g.status.eq('ok').sum()),q_lt_10=int(g.q.lt(.1).sum()),q_lt_05=int(g.q.lt(.05).sum()),holm_lt_05=int(g.holm_p.lt(.05).sum()),consistent_three_outcomes=int(cc.direction_consistent.sum()),tier_A=int(cc.tier.eq('A').sum()),tier_B=int(cc.tier.eq('B').sum())))
    pd.DataFrame(summary).to_csv(out/'subjective_objective_summary.csv',index=False);return c

def crossfit(d,codes,t,defs,out):
    fold=np.zeros(len(d),int)
    for k,(_,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=SEED).split(d,d.cell)):fold[te]=k
    rows=[]
    for n,(var,(a,lev,sd,ok)) in enumerate(codes.items()):
        dd=d.loc[ok];ff=fold[ok]
        for k in range(5):
            train=ff!=k;test=ff==k;models={}
            for y in Y_NAMES:
                for target,w in list(TARGETS.items())[:2]:
                    for name,ix in [('train',train),('holdout',test)]:
                        try:models[y,name,target]=fit(dd.loc[ix],a[ix],dd.loc[ix,y],lev,arms=['cash'] if target=='cash' else None)
                        except (ValueError,np.linalg.LinAlgError):models[y,name,target]=None
                    full=t[(t.variable==var)&(t.outcome==y)&(t.target==target)].iloc[0]
                    sample=dd.form.eq('cash').to_numpy() if target=='cash' else np.ones(len(dd),bool)
                    r=dict(variable=var,outcome=y,target=target,fold=k+1,train_N=int((train&sample).sum()),holdout_N=int((test&sample).sum()),status='ok' if models[y,'train',target] is not None and models[y,'holdout',target] is not None else 'sparse/rank failure',train_projection=np.nan,train_profile=None,train_profile_norm=np.nan,train_same_direction=False,holdout_direction_score=np.nan,holdout_cosine=np.nan)
                    if models[y,'train',target] is not None:
                        _,bt,_=extract(models[y,'train',target],w,a.shape[1],False);r['train_projection']=float(bt[0]) if len(bt)==1 else float(np.arange(1,len(lev))@bt/np.sum(np.arange(1,len(lev))**2)) if var in ORDERED_FACTORS else np.nan;r['train_profile']=json.dumps(bt.tolist());r['train_profile_norm']=float(np.linalg.norm(bt))
                        if full.status=='ok':r['train_same_direction']=float(bt@np.array(json.loads(full.profile)))>0
                        if models[y,'holdout',target] is not None:
                            _,bh,_=extract(models[y,'holdout',target],w,a.shape[1],False)
                            if np.linalg.norm(bt)>0:r['holdout_direction_score']=float(bt@bh/np.linalg.norm(bt))
                            if np.linalg.norm(bt)>0 and np.linalg.norm(bh)>0:r['holdout_cosine']=float(bt@bh/(np.linalg.norm(bt)*np.linalg.norm(bh)))
                    rows.append(r)
        if (n+1)%20==0:print('Five-fold stability',n+1,'/',len(codes),flush=True)
    details=pd.DataFrame(rows);details.to_csv(out/'crossfit_fold_diagnostics.csv',index=False);summary=[]
    for (v,y,target),g in details.groupby(['variable','outcome','target']):
        profiles=[json.loads(p) for p in g.train_profile.dropna()]
        summary.append(dict(variable=v,outcome=y,target=target,folds=5,valid_train_folds=len(profiles),valid_holdout_folds=int(g.holdout_direction_score.notna().sum()),same_direction_train_folds=int(g.train_same_direction.sum()),median_training_estimate=g.train_projection.median() if g.train_projection.notna().any() else np.nan,median_training_profile=json.dumps(np.median(profiles,axis=0).tolist()) if profiles else None,median_training_profile_norm=g.train_profile_norm.median(),positive_holdout_direction_folds=int(g.holdout_direction_score.gt(0).sum()),mean_holdout_direction_score=g.holdout_direction_score.mean(),median_holdout_cosine=g.holdout_cosine.median(),interpretation='direction diagnostic, not independent validation or corrected test; unordered factors have profiles not signed scalar'))
    pd.DataFrame(summary).to_csv(out/'crossfit_stability.csv',index=False);return fold

def run(data,out):
    out=Path(out);d,X,inv,defs=make_inventory(data,out);frozen=json.loads((out/'inventory_manifest.json').read_text());assert frozen['phase']=='inventory_complete_before_regressions'
    t,codes=scan(d,X,inv,defs,out);c=concordance(t,defs,out);fold=crossfit(d,codes,t,defs,out)
    print('Tier counts',c.groupby(['target','tier']).size().to_dict(),flush=True)
    manifest=dict(inventory=frozen,seed=SEED,family_size=len(defs),primary_rows=int(t.target.isin(['cash','rc']).sum()),fold_cell_counts=pd.crosstab(fold,d.cell).to_dict(),completed_primary_screen=True,completed_crossfit=True)
    (out/'screen_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return d,X,defs,t,c,codes,fold

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('--out',default=str(ROOT));a=p.parse_args();run(a.data,a.out)
