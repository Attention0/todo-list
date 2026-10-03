"""Frozen evidence repair. Raw data never exported; all output is aggregate."""
from pathlib import Path
import sys,json,hashlib,argparse
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
import patsy
OUT=Path(__file__).resolve().parent
OLD=OUT.parent/'nc_revision_audit'
sys.path.insert(0,str(OLD));import grid_models as gm
from secondary import covariates
sys.path.insert(0,str(OUT.parent/'mpc_size_curve'));from size_curve import prepare
SEED=2026100317
def save(df,name):df.to_csv(OUT/name,index=False)
def holm(p):return multipletests(p,method='holm')[1]
def interval(e,se,k=1):
    z=stats.norm.ppf(1-.05/(2*k))
    return dict(estimate=float(e),se=float(se),lo=float(e-1.96*se),hi=float(e+1.96*se),sim_lo=float(e-z*se),sim_hi=float(e+z*se),p=float(2*stats.norm.sf(abs(e/se))))
def Ctest(m,C,name):
    C=np.atleast_2d(C);e=C@np.asarray(m.params);v=C@np.asarray(m.cov_params())@C.T
    w=float(e@np.linalg.solve(v,e));r=dict(test=name,df=len(e),wald=w,p=float(stats.chi2.sf(w,len(e))),N=int(m.nobs))
    if len(e)==1:r.update(interval(e[0],np.sqrt(v[0,0])))
    return r
def unit(m,name):return np.eye(len(m.params))[list(m.params.index).index(name)]
def gcounts(d):
    return d.groupby(['cell','ordinal']).size().unstack(fill_value=0).reindex(index=range(9),columns=range(1,7),fill_value=0).to_numpy()
CELL=np.repeat(np.arange(9),6);K=np.tile(np.arange(1,7),9)
X,IX=gm.design(CELL,'trend');Y=np.column_stack([gm.yvals(K,y) for y in gm.OUTCOMES])
def fit21(counts):
    n=counts.reshape(-1);bread=np.linalg.inv(X.T@(n[:,None]*X));b=bread@X.T@(n[:,None]*Y)
    h=np.einsum('ij,jk,ik->i',X,bread,X);res=(Y-X@b)/(1-h[:,None])
    v=X@bread[:,IX];influ=(res[:,:,None]*v[:,None,:]).reshape(len(n),14)
    cov=influ.T@(n[:,None]*influ);e=b[IX,:].T.reshape(-1)
    return e,cov,b
def p21(e,cov):
    e=np.atleast_2d(e);p=[]
    for j in range(7):
        sl=slice(2*j,2*j+2);v=cov[sl,sl];ee=e[:,sl]
        p.extend([stats.chi2.sf(np.einsum('bi,ij,bj->b',ee,np.linalg.inv(v),ee),2),2*stats.norm.sf(np.abs(ee[:,0])/np.sqrt(v[0,0])),2*stats.norm.sf(np.abs(ee[:,1])/np.sqrt(v[1,1]))])
    return np.column_stack(p)
def minp(e,cov,B,rng):
    val,vec=np.linalg.eigh(cov);root=vec*np.sqrt(np.maximum(val,0))[None,:]
    sim=rng.normal(size=(B,len(e)))@root.T
    minima=p21(sim,cov).min(axis=1);p=p21(e,cov)[0]
    adj=(1+(minima[:,None]<=p).sum(axis=0))/(B+1)
    return p,adj
def primary(d):
    rows=[];slopes=[]
    for sample,x in [('A',d[d.sample_A]),('R',d)]:
        e,cov,b=fit21(gcounts(x));p,adj=minp(e,cov,10000,np.random.default_rng(SEED));hp=holm(p)
        for j,y in enumerate(gm.OUTCOMES):
            m=smf.ols(y+'~C(form)*z',x).fit(cov_type='HC3')
            for k,name in enumerate(['omnibus','cash-food','cash-medical']):
                r=dict(sample=sample,outcome=y,test=name,N=len(x),df=2 if k==0 else 1,p=p[j*3+k],holm21=hp[j*3+k],minP21=adj[j*3+k])
                if k:r.update(interval(-e[2*j+k-1],np.sqrt(cov[2*j+k-1,2*j+k-1]),21))
                rows.append(r)
            for form in ['cash','food','medical']:
                v=unit(m,'z')+(unit(m,'C(form)[T.'+form+']:z') if form!='cash' else 0)
                r=Ctest(m,v,form);r.update(sample=sample,outcome=y);slopes.append(r)
    save(pd.DataFrame(rows),'scientific_family21.csv');save(pd.DataFrame(slopes),'within_form_slopes.csv')
def descriptions(d):
    rows=[];dist=[];effects=[];contrasts=[]
    for sample,x in [('A',d[d.sample_A]),('R',d)]:
        for (form,amount),g in x.groupby(['form','amount']):
            for y in gm.OUTCOMES:rows.append(dict(sample=sample,form=form,amount=amount,outcome=y,N=len(g),**interval(g[y].mean(),g[y].std(ddof=1)/np.sqrt(len(g)))))
            for k in range(1,7):dist.append(dict(sample=sample,form=form,amount=amount,category=k,N=len(g),count=int(g.ordinal.eq(k).sum()),share=g.ordinal.eq(k).mean()))
        xx=np.eye(9)[x.cell];weights={}
        for f in [1,2]:
            v=np.zeros(9);v[3*f:3*f+3]=1/3;v[:3]=-1/3;weights[['food-cash','medical-cash'][f-1]]=v
        for a in [1,2]:
            v=np.zeros(9);v[[a,3+a,6+a]]=1/3;v[[0,3,6]]=-1/3;weights[['1000-200','5000-200'][a-1]]=v
        for y in gm.OUTCOMES:
            m=sm.OLS(x[y],xx).fit(cov_type='HC3');rr=[]
            for name,v in weights.items():rr.append(Ctest(m,v,name))
            rr.append(Ctest(m,np.array(list(weights.values())[:2]),'form_omnibus'))
            rr.append(Ctest(m,np.array(list(weights.values())[2:]),'amount_omnibus'))
            for r,hp in zip(rr,holm([r['p'] for r in rr])):r.update(sample=sample,outcome=y,holm6=hp if y=='top75' else np.nan);effects.append(r)
            if y=='top75':
                rr=[]
                for a,amount in enumerate([200,1000,5000]):
                    for f,form in [(1,'food'),(2,'medical')]:
                        v=np.eye(9)[3*f+a]-np.eye(9)[a];r=Ctest(m,v,form+'-cash');r.update(amount=amount,sample=sample)
                        r.update(interval(r['estimate'],r['se'],6));rr.append(r)
                for r,hp in zip(rr,holm([r['p'] for r in rr])):r['holm6']=hp;contrasts.append(r)
    for arr,name in [(rows,'profiles.csv'),(dist,'distribution.csv'),(effects,'main_effects.csv'),(contrasts,'form_contrasts.csv')]:save(pd.DataFrame(arr),name)
def mechanisms(d):
    a=d[d.sample_A].copy();a['la']=np.log(a.amount);rows=[];details=[];lr=[]
    for mapping in ['M1','M2']:
        a['li']=np.log(a['income_'+mapping]);a['li']-=a.li.mean()
        u=smf.glm('top75~C(form)*(la+li)',a,family=sm.families.Binomial()).fit(cov_type='HC0')
        la=[unit(u,'la'),unit(u,'C(form)[T.food]:la'),unit(u,'C(form)[T.medical]:la')]
        li=[unit(u,'li'),unit(u,'C(form)[T.food]:li'),unit(u,'C(form)[T.medical]:li')]
        for name,cm in [('income_ABS3df',li),('income_REL3df',np.array(li)+np.array(la))]:
            r=Ctest(u,cm,name);r.update(mapping=mapping,scale='logit coefficient restriction');(rows if mapping=='M1' else details).append(r)
        a['rel']=a.la-a.li
        for name,formula in [('ABS','top75~C(form)*la'),('REL','top75~C(form)*rel')]:
            reduced=smf.glm(formula,a,family=sm.families.Binomial()).fit()
            lr.append(dict(mapping=mapping,test=name,LR=2*(u.llf-reduced.llf),df=3,p=stats.chi2.sf(2*(u.llf-reduced.llf),3)))
        t=smf.glm('top75~C(form)*la*li',a,family=sm.families.Binomial()).fit(cov_type='HC0')
        cm=[unit(t,'C(form)[T.food]:la:li'),unit(t,'C(form)[T.medical]:la:li')]
        r=Ctest(t,cm,'income_triple2df');r.update(mapping=mapping,scale='logit');(rows if mapping=='M1' else details).append(r)
    food=a[a.form.isin(['cash','food'])].copy();food['G']=(food.food_lower6>5000).astype(int)
    m=smf.ols('top75~C(form)*z*G',food).fit(cov_type='HC3')
    r=Ctest(m,unit(m,'C(form)[T.food]:z:G'),'inframarginal_triple1df');r['scale']='probability per fivefold';rows.append(r)
    for g in [0,1]:
        v=unit(m,'C(form)[T.food]:z')+g*unit(m,'C(form)[T.food]:z:G');r=Ctest(m,v,'Food-Cash slope G='+str(g));r['subgroup_N']=int((food.G==g).sum());details.append(r)
    f=food[food.food_lower6>0].copy();f['lf']=np.log(f.food_lower6)
    m=smf.ols('top75~C(form)*(la+lf)',f).fit(cov_type='HC3')
    r=Ctest(m,unit(m,'C(form)[T.food]:la')+unit(m,'C(form)[T.food]:lf'),'ratio_restriction1df');r['scale']='probability per log unit';rows.append(r)
    for name in ['C(form)[T.food]:la','C(form)[T.food]:lf']:details.append(Ctest(m,unit(m,name),'ratio_decomposition '+name))
    count=[]
    for q in ['Q1','Q2']:
        a['passq']=a['sample_'+q].astype(int)
        m=smf.ols('top75~C(form)*z*passq',a).fit(cov_type='HC3')
        cm=[unit(m,'C(form)[T.food]:z:passq'),unit(m,'C(form)[T.medical]:z:passq')]
        rows.append(Ctest(m,cm,q+'_triple2df'))
        for passed in [0,1]:
            for form in ['food','medical']:
                v=unit(m,f'C(form)[T.{form}]:z')+passed*unit(m,f'C(form)[T.{form}]:z:passq')
                r=Ctest(m,v,q+' '+str(passed)+' '+form+'-cash');r['subgroup_N']=int(a.passq.eq(passed).sum());details.append(r)
        for (p,form,amount),g in a.groupby(['passq','form','amount']):count.append(dict(screen=q,passed=p,form=form,amount=amount,N=len(g),events=int(g.top75.sum())))
    assert len(rows)==7
    for r,hp in zip(rows,holm([r['p'] for r in rows])):r['holm7']=hp
    save(pd.DataFrame(rows),'mechanism_tests.csv');save(pd.DataFrame(details),'mechanism_details.csv');save(pd.DataFrame(lr),'income_LR_sensitivity.csv');save(pd.DataFrame(count),'screen_cell_counts.csv')
def prediction(d):
    folds=np.zeros(len(d),int)
    for k,(_,te) in enumerate(StratifiedKFold(5,shuffle=True,random_state=20261003).split(d,d.cell)):folds[te]=k
    a=d[d.sample_A].copy();a['fold']=folds[d.sample_A];a['la']=np.log(a.amount);rows=[];scores=[]
    for mapping in ['M1','M2']:
        a['li']=np.log(a['income_'+mapping]);a['rel']=a.la-a.li
        models={'additive':'C(form)+la','ABS':'C(form)*la','REL':'C(form)*rel','unrestricted':'C(form)*(la+li)','triple':'C(form)*la*li'}
        losses={}
        for name,formula in models.items():
            X=np.asarray(patsy.dmatrix(formula,a));y=a.top75.to_numpy();loss=np.zeros(len(a))
            for fold in range(5):
                train=a.fold.to_numpy()!=fold;test=~train
                scale=X[train].std(axis=0);scale[scale<1e-10]=1
                m=LogisticRegression(penalty=None,solver='newton-cholesky',fit_intercept=False,max_iter=100,tol=1e-9).fit(X[train]/scale,y[train]);p=np.clip(m.predict_proba(X[test]/scale)[:,1],1e-12,1-1e-12)
                loss[test]=-y[test]*np.log(p)-(1-y[test])*np.log1p(-p)
                rows.append(dict(mapping=mapping,model=name,fold=fold,N_train=int(train.sum()),N_test=int(test.sum()),logloss=loss[test].mean(),converged=bool(m.n_iter_.max()<100)))
            losses[name]=loss
        for name,l in losses.items():scores.append(dict(mapping=mapping,model=name,N=len(a),logloss=l.mean(),absolute_gain_vs_additive=losses['additive'].mean()-l.mean(),relative_gain_vs_additive=1-l.mean()/losses['additive'].mean(),absolute_gain_vs_ABS=losses['ABS'].mean()-l.mean(),relative_gain_vs_ABS=1-l.mean()/losses['ABS'].mean()))
    save(pd.DataFrame(rows),'prediction_folds.csv');save(pd.DataFrame(scores),'prediction_scores.csv')
def simulations(d):
    cnt=gcounts(d[d.sample_A]);ns=cnt.sum(axis=1);pooled=cnt.sum(axis=0)/cnt.sum();z=np.tile([-1,0,1],3);f=np.repeat([0,1,2],3)
    prob0=np.tile(pooled,(9,1));v=np.array([.014,-.006,-.003,-.003,-.001,-.001]);v2=np.array([.006,.002,-.002,-.003,-.002,-.001])
    prob1=prob0+(f-1)[:,None]*v+z[:,None]*v2
    prob2=prob1.copy();prob2[(f==1),2]+=z[f==1]*.025;prob2[(f==1),3]-=z[f==1]*.025
    results=[];rng=np.random.default_rng(SEED+1)
    for name,prob in [('pooled_null',prob0),('additive_probability_main_effects',prob1),('partial_null_intermediate_food_interaction',prob2)]:
        assert np.all(prob>0) and np.allclose(prob.sum(axis=1),1)
        te,tc,_=fit21(prob*ns[:,None]);true=np.ones(21,bool)
        for j in range(7):true[3*j:3*j+3]=[np.all(np.abs(te[2*j:2*j+2])<1e-10),abs(te[2*j])<1e-10,abs(te[2*j+1])<1e-10]
        rejected={'holm':[],'minP':[]};power={'holm':[],'minP':[]}
        for b in range(1000):
            draw=np.array([rng.multinomial(int(n),p) for n,p in zip(ns,prob)]);e,cov,_=fit21(draw);p,mp=minp(e,cov,999,rng)
            for method,pp in [('holm',holm(p)),('minP',mp)]:
                rejected[method].append(bool(np.any(pp[true]<=.05)));power[method].append(float(np.mean(pp[~true]<=.05)) if (~true).any() else np.nan)
        for method in rejected:
            k=sum(rejected[method]);lo=stats.beta.ppf(.025,k,1001-k) if k else 0;hi=stats.beta.ppf(.975,k+1,1000-k) if k<1000 else 1
            results.append(dict(scenario=name,method=method,replicates=1000,true_nulls=int(true.sum()),rejections=k,FWER=k/1000,lo=lo,hi=hi,false_null_mean_power=np.nanmean(power[method]) if (~true).any() else np.nan,failed_refits=0,calibration_draws=999))
        print('simulation complete',name,flush=True)
    save(pd.DataFrame(results),'simulation_results.csv')
def verify(d):
    e,cov,b=fit21(gcounts(d));errors=[];covs=[]
    for j,y in enumerate(gm.OUTCOMES):
        m=smf.ols(y+'~C(form)*z',d).fit(cov_type='HC3');cm=np.array([unit(m,'C(form)[T.food]:z'),unit(m,'C(form)[T.medical]:z')]);errors.extend(np.abs(cm@m.params-e[2*j:2*j+2]));covs.extend(np.abs(cm@np.asarray(m.cov_params())@cm.T-cov[2*j:2*j+2,2*j:2*j+2]).ravel())
    assert max(errors)<1e-10 and max(covs)<1e-10
    old=pd.read_csv(OLD/'table_A1_focal_estimand.csv');new=pd.read_csv(OUT/'scientific_family21.csv');r=new[(new['sample']=='R')&(new.outcome=='top75')]
    for row in r.itertuples():assert abs(row.p-float(old.loc[old.estimand==row.test,'p'].iloc[0]))<1e-10
    assert all(pd.read_csv(OUT/'prediction_folds.csv').converged)
    result=dict(independent_statsmodels_max_error=max(errors),independent_HC3_max_error=max(covs),historical_focal_p_reproduced=True,raw_sha256=hashlib.sha256(Path(ARGS.data).read_bytes()).hexdigest(),freeze_sha256=hashlib.sha256((OUT/'freeze.json').read_bytes()).hexdigest(),N=len(d),adult_N=int(d.sample_A.sum()),individual_exports=False)
    (OUT/'verification.json').write_text(json.dumps(result,indent=2))
def legacy(d):
    g=gm.groups(d);grid,blocks,_,diag=gm.run_grid(g)
    rng=np.random.default_rng(20261003);draws=rng.normal(size=(5000,len(g)))*np.sqrt(g['count'].to_numpy())[None,:]
    minima=np.ones(5000);maximum=np.zeros(5000);who=np.zeros(5000,int);oldwho=np.zeros(5000,int)
    for j,b in enumerate(blocks):
        w=np.sum((draws@b)**2,axis=1);p=stats.chi2.sf(w,b.shape[1]);hit=p<minima;who[hit]=j;minima=np.minimum(minima,p);oldhit=np.sqrt(w)>maximum;oldwho[oldhit]=j;maximum=np.maximum(maximum,np.sqrt(w))
    grid['legacy_minP']=[(1+np.sum(minima<=p))/5001 for p in grid.p];grid['legacy_maxnorm']=[(1+np.sum(maximum>=s))/5001 for s in grid.statistic]
    old=pd.read_csv(OLD/'specification_grid.csv');assert np.allclose(grid.legacy_maxnorm,old.global_maxT_p)
    save(grid,'legacy_family_comparison.csv');dom=grid.iloc[who][['df','model','sample','representation']].value_counts().rename('draw_count').reset_index();save(dom,'legacy_extreme_sources.csv')
    dom=grid.iloc[oldwho][['df','model','sample','representation']].value_counts().rename('draw_count').reset_index();save(dom,'legacy_maxnorm_extreme_sources.csv')
    print('legacy comparison complete',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--part',choices=['core','simulation','legacy'],default='core');ARGS=p.parse_args()
    assert hashlib.sha256(Path(ARGS.data).read_bytes()).hexdigest()==json.loads((OUT/'freeze.json').read_text())['raw_sha256']
    d=covariates(prepare(ARGS.data))
    if ARGS.part=='core':primary(d);descriptions(d);mechanisms(d);prediction(d);verify(d);print('core complete',flush=True)
    elif ARGS.part=='simulation':simulations(d)
    else:legacy(d)
