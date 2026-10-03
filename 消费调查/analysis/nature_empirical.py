"""Locked Nature-series empirical package. Aggregate outputs only.

Usage: python nature_empirical.py delivery.dta --out ../nature-output
The input stays outside the repository; no respondent-level predictions/folds are saved.
"""
from argparse import ArgumentParser
from pathlib import Path
import json, math, sys
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heterogeneity_formal as hf
import final_exploration as fe

SEED=20260921
SEEDS=list(range(SEED,SEED+10))
FORMS=['cash','food','medical']
COLORS={'cash':'#30343B','food':'#2B7A91','medical':'#C46B38'}
QUALITY_ITEMS=['q01_lifesat','q02_safety','q03a_fair_dist','q03b_fair_opp','q03c_fair_rule','q04_trust_gov','q05_trust_soc','q06_socsec','q07_emergfund','q08_support','q09_gain','q10_effort','q11_mobility','q12_voice','q13_pressure']

def folds(d,seed=SEED,repeats=1):
    """Shared respondent folds, stratified by original randomized form x amount."""
    for rep in range(repeats):
        cv=StratifiedKFold(5,shuffle=True,random_state=seed+rep)
        for k,(tr,te) in enumerate(cv.split(d,d.cell)):
            yield rep*5+k,tr,te

def ci_mean(x,B=4000,seed=SEED):
    x=np.asarray(x,float); rng=np.random.default_rng(seed)
    boot=np.mean(rng.choice(x,(B,len(x)),replace=True),axis=1)
    return np.quantile(boot,[.025,.975])

def quality_masks(d):
    x=d[QUALITY_ITEMS]; sd=x.std(1); unique=x.nunique(1); extreme=x.isin([0,10]).mean(1)
    return {'R':np.ones(len(d),bool),'A':d.sample_A.to_numpy(),'C':d.sample_C.to_numpy(),
            'Q1':(d.sample_A&(sd>=1)&(unique>=4)).to_numpy(),
            'Q2':(d.sample_A&(sd>=1.5)&(unique>=5)&(extreme<=.8)).to_numpy()}

def cell_distributions(d,out):
    rows=[]
    for scope,groups in [('form',['transfer_type']),('amount',['amount']),('cell',['transfer_type','amount'])]:
        for keys,g in d.groupby(groups):
            if not isinstance(keys,tuple):keys=(keys,)
            form=keys[0] if 'transfer_type' in groups else 'all'
            amount=keys[-1] if 'amount' in groups else 'all'
            for y in range(1,7):
                p=(g.outcome_ord==y).mean(); rows.append([scope,form,amount,y,len(g),int((g.outcome_ord==y).sum()),p,(g.outcome_ord<=y).mean()])
    pd.DataFrame(rows,columns=['scope','form','amount','category','N','count','share','cumulative_share']).to_csv(out/'nature_outcome_distributions.csv',index=False)
    d.groupby(['transfer_type','amount']).agg(N=('cell','size'),ordinal_mean=('outcome_ord','mean'),ordinal_sd=('outcome_ord','std'),midpoint_mean=('mpc_midpoint','mean')).reset_index().to_csv(out/'nature_design_cells.csv',index=False)
    balance=pd.read_csv(Path(__file__).resolve().parents[1]/'tables'/'balance.csv')
    balance.to_csv(out/'nature_randomization_balance.csv',index=False)

def effects(d,out,masks):
    rows=[]
    for sample,mask in masks.items():
        dd=d.loc[mask]
        for outcome in ['outcome_ord','mpc_midpoint','mpc_alt','any_spend','mpc_10plus','mpc_25plus','mpc_50plus']:
            m=smf.ols(f'{outcome}~C(transfer_type)*C(amount)',dd).fit(cov_type='HC1')
            for amount in [200,1000,5000,'pooled']:
                for t,c in [('food','cash'),('medical','cash'),('medical','food')]:
                    w={f'C(transfer_type)[T.{t}]':1,f'C(transfer_type)[T.{c}]':-1}
                    if amount=='pooled':
                        for a in [1000,5000]:
                            w[f'C(transfer_type)[T.{t}]:C(amount)[T.{a}]']=1/3
                            w[f'C(transfer_type)[T.{c}]:C(amount)[T.{a}]']=-1/3
                    elif amount!=200:
                        w[f'C(transfer_type)[T.{t}]:C(amount)[T.{amount}]']=1
                        w[f'C(transfer_type)[T.{c}]:C(amount)[T.{amount}]']=-1
                    b,se,lo,hi,p=hf.ctest(m,w)
                    rows.append([sample,outcome,amount,f'{t}-{c}',b,se,lo,hi,p,len(dd)])
    pd.DataFrame(rows,columns=['sample','outcome','amount','contrast','effect','se','lo','hi','p','N']).to_csv(out/'nature_average_effects.csv',index=False)

def level_cv(d,out):
    rows=[]; split=list(folds(d,repeats=2))
    for fs,cols in hf.SETS.items():
        X=hf.add_design(d,cols)
        X['form_cash']=d.transfer_type.eq('cash').astype(int)
        X['form_food']=d.transfer_type.eq('food').astype(int)
        X['form_medical']=d.transfer_type.eq('medical').astype(int)
        X=X.drop(columns='type');use=list(X.columns)
        for model in ['ridge','elastic_net','rf','hgb']:
            for fold,tr,te in split:
                p=fe.pipe_for(use,model).fit(X.iloc[tr],d.mpc_midpoint.iloc[tr])
                y=d.mpc_midpoint.iloc[te]; pred=p.predict(X.iloc[te])
                rows.append([fs,model,fold,len(te),r2_score(y,pred),math.sqrt(mean_squared_error(y,pred)),mean_absolute_error(y,pred)])
    tab=pd.DataFrame(rows,columns=['feature_set','model','fold','N_test','r2','rmse','mae'])
    tab.to_csv(out/'nature_level_cv_folds.csv',index=False)
    sm=[]
    for (fs,model),g in tab.groupby(['feature_set','model']):
        lo,hi=ci_mean(g.r2)
        sm.append([fs,model,g.r2.mean(),lo,hi,g.rmse.mean(),g.mae.mean(),g.r2.min(),g.r2.max(),len(g)])
    pd.DataFrame(sm,columns=['feature_set','model','r2','lo','hi','rmse','mae','fold_min','fold_max','folds']).to_csv(out/'nature_level_cv_summary.csv',index=False)
    paired=[]
    for model,g in tab.groupby('model'):
        p=g.pivot(index='fold',columns='feature_set',values='r2')
        for target in ['O+S','O+A','ALL']:
            v=p[target]-p['O']; lo,hi=ci_mean(v)
            paired.append([model,'O',target,v.mean(),lo,hi,hi<.01,hi<.02])
    pd.DataFrame(paired,columns=['model','base','expanded','delta_r2','lo','hi','rules_out_001','rules_out_002']).to_csv(out/'nature_level_increment.csv',index=False)

def cross_form(d,out):
    # Fixed source models; respondent bootstrap quantifies target-outcome uncertainty.
    predictions={}; rows=[]
    for source in FORMS:
        a=d[d.transfer_type.eq(source)]; Xa,cols=fe.design(a,hf.FEATURES)
        model=fe.pipe_for(cols,'rf').fit(Xa,a.mpc_midpoint)
        for target in FORMS:
            if source==target:continue
            b=d[d.transfer_type.eq(target)]; Xb,_=fe.design(b,hf.FEATURES)
            pred=model.predict(Xb); y=b.mpc_midpoint.to_numpy()
            predictions[(source,target)]=(pred,y)
            rec=pred-pred.mean()+y.mean()
            rho=stats.spearmanr(pred,y).statistic
            slope=np.cov(pred,y)[0,1]/np.var(pred,ddof=1)
            rows.append([source,target,len(b),rho,r2_score(y,rec),slope])
    pd.DataFrame(rows,columns=['source','target','N','spearman','recentered_r2','slope']).to_csv(out/'nature_cross_form.csv',index=False)
    rng=np.random.default_rng(SEED); B=3000; contrasts=[]
    for a,b,label in [(('cash','food'),('cash','medical'),'CF_minus_CM'),(('cash','food'),('food','medical'),'CF_minus_FM')]:
        pa,ya=predictions[a]; pb,yb=predictions[b]
        obs=stats.spearmanr(pa,ya).statistic-stats.spearmanr(pb,yb).statistic
        boot=[]
        for _ in range(B):
            ia=rng.integers(len(ya),size=len(ya)); ib=rng.integers(len(yb),size=len(yb))
            boot.append(stats.spearmanr(pa[ia],ya[ia]).statistic-stats.spearmanr(pb[ib],yb[ib]).statistic)
        lo,hi=np.quantile(boot,[.025,.975]); contrasts.append(['spearman',label,obs,lo,hi,B,'fixed source models; target-observation bootstrap'])
    return predictions,contrasts

def coefficient_differences(d,out,contrasts):
    rng=np.random.default_rng(SEED); rows=[]
    for name,cols in [('O_needs',hf.OBJECTIVE+hf.NEEDS),('ALL',hf.FEATURES)]:
        raw=d[cols]; cats=[c for c in cols if c in hf.NOMINAL+hf.ORDERED]
        X=pd.get_dummies(raw,columns=cats,dtype=float); X=((X-X.mean())/X.std().replace(0,1)).fillna(0).to_numpy()
        y=d.mpc_midpoint.to_numpy(); form=d.transfer_type.to_numpy()
        ix={t:np.flatnonzero(form==t) for t in FORMS}
        def calc(sample):
            co={t:Ridge(alpha=10).fit(X[sample[t]],y[sample[t]]).coef_ for t in FORMS}
            outv={}
            for a,b in [('cash','food'),('cash','medical'),('food','medical')]:
                u,v=co[a],co[b]
                outv[(a,b)]=(np.corrcoef(u,v)[0,1],np.dot(u,v)/(np.linalg.norm(u)*np.linalg.norm(v)),(np.sign(u)==np.sign(v)).mean())
            return outv
        obs=calc(ix); B=600; boot={k:[] for k in obs}
        for _ in range(B):
            zz=calc({t:rng.choice(v,len(v),replace=True) for t,v in ix.items()})
            for k,v in zz.items():boot[k].append(v)
        for k,v in obs.items():
            q=np.quantile(boot[k],[.025,.975],axis=0)
            rows.append([name,*k,*v,q[0,0],q[1,0],q[0,1],q[1,1],q[0,2],q[1,2]])
        for metric,j in [('coef_correlation',0),('cosine',1),('sign_agreement',2)]:
            for a,b,label in [(('cash','food'),('cash','medical'),'CF_minus_CM'),(('cash','food'),('food','medical'),'CF_minus_FM')]:
                v=obs[a][j]-obs[b][j]; z=np.array(boot[a])[:,j]-np.array(boot[b])[:,j]
                lo,hi=np.quantile(z,[.025,.975]); contrasts.append([metric+'_'+name,label,v,lo,hi,B,'stratified respondent bootstrap with source-model refits'])
    pd.DataFrame(rows,columns=['feature_set','form1','form2','coef_correlation','cosine','sign_agreement','corr_lo','corr_hi','cos_lo','cos_hi','sign_lo','sign_hi']).to_csv(out/'nature_predictor_similarity.csv',index=False)
    pd.DataFrame(contrasts,columns=['metric','comparison','difference','lo','hi','bootstrap_B','method']).to_csv(out/'nature_portability_differences.csv',index=False)

def reliability(out):
    tab=pd.read_csv(out/'nature_cross_form.csv'); rows=[]
    for _,r in tab.iterrows():
        for rel in [.4,.6,.8]:
            # Classical independent-error attenuation for two noisy measurements;
            # applied to ranks only as an illustrative approximation.
            adj=min(1,r.spearman/rel)
            rows.append([r.source,r.target,r.spearman,rel,adj,'assumed equal reliability in source and target; not estimated'])
    pd.DataFrame(rows,columns=['source','target','observed_spearman','assumed_reliability','sensitivity_adjusted','assumption']).to_csv(out/'nature_reliability_sensitivity.csv',index=False)

def hte_oof(d,treated,control,method,seed=SEED,cols=None):
    cols=hf.FEATURES if cols is None else cols
    global_fold=np.full(len(d),-1)
    for k,_,te in folds(d,seed):global_fold[te]=k
    chosen=d.transfer_type.isin([treated,control]).to_numpy(); dd=d.loc[chosen].reset_index(drop=True).copy()
    W=dd.transfer_type.eq(treated).astype(int).to_numpy(); Y=dd.mpc_midpoint.to_numpy()
    # These are randomized design probabilities within amount, not fitted propensities.
    e=dd.amount.map(dd.groupby('amount').transfer_type.apply(lambda x:(x==treated).mean())).to_numpy()
    tau=np.zeros(len(dd)); foldid=global_fold[chosen]
    for k in range(5):
        tr=np.flatnonzero(foldid!=k);te=np.flatnonzero(foldid==k)
        Xtr,Xte=fe.encode_fold(dd.iloc[tr],dd.iloc[te],cols)
        acols=[200,1000,5000]
        atr=np.column_stack([(dd.amount.iloc[tr].to_numpy()==a).astype(float) for a in acols])
        ate=np.column_stack([(dd.amount.iloc[te].to_numpy()==a).astype(float) for a in acols])
        Xtr=np.c_[Xtr,atr];Xte=np.c_[Xte,ate];wt=W[tr];yt=Y[tr];et=e[tr]
        if method=='t':
            kw=dict(n_estimators=110,min_samples_leaf=25,max_features=.5,n_jobs=-1,random_state=seed+k)
            m1=RandomForestRegressor(**kw).fit(Xtr[wt==1],yt[wt==1]);m0=RandomForestRegressor(**kw).fit(Xtr[wt==0],yt[wt==0])
            tau[te]=m1.predict(Xte)-m0.predict(Xte);continue
        inner=StratifiedKFold(3,shuffle=True,random_state=seed+k)
        mu=np.zeros(len(tr));m1=np.zeros(len(tr));m0=np.zeros(len(tr))
        for a,b in inner.split(Xtr,dd.cell.iloc[tr]):
            kw=dict(max_iter=100,min_samples_leaf=25,l2_regularization=3,random_state=seed+k)
            if method=='dr':
                q1=HistGradientBoostingRegressor(**kw).fit(Xtr[a][wt[a]==1],yt[a][wt[a]==1]);q0=HistGradientBoostingRegressor(**kw).fit(Xtr[a][wt[a]==0],yt[a][wt[a]==0])
                m1[b]=q1.predict(Xtr[b]);m0[b]=q0.predict(Xtr[b])
            else:
                q=HistGradientBoostingRegressor(**kw).fit(Xtr[a],yt[a]);mu[b]=q.predict(Xtr[b])
        if method=='dr':
            pseudo=m1-m0+wt*(yt-m1)/et-(1-wt)*(yt-m0)/(1-et);weights=None
        else:
            wr=wt-et;pseudo=(yt-mu)/wr;weights=wr**2
        learner=RandomForestRegressor(n_estimators=110,min_samples_leaf=30,max_features=.5,n_jobs=-1,random_state=seed+k)
        learner.fit(Xtr,pseudo,sample_weight=weights);tau[te]=learner.predict(Xte)
    return dd,W,Y,tau,foldid

def evaluate_hte(dd,W,Y,tau):
    z=pd.DataFrame({'y':Y,'W':W,'tau':tau,'tc':tau-tau.mean(),'amount':dd.amount})
    mod=smf.ols('y~W+tc+W:tc+C(amount)',z).fit(cov_type='HC1')
    cal=hf.ctest(mod,{'W:tc':1})
    z['q']=pd.qcut(z.tau,5,labels=False,duplicates='drop')+1
    rows=[]
    for q,g in z.groupby('q'):
        a=g[g.W.eq(1)].y;b=g[g.W.eq(0)].y
        eff=a.mean()-b.mean();se=math.sqrt(a.var()/len(a)+b.var()/len(b))
        rows.append([q,len(g),len(a),len(b),g.tau.mean(),eff,se,eff-1.96*se,eff+1.96*se])
    qtab=pd.DataFrame(rows,columns=['quintile','N','treated_N','control_N','predicted','effect','se','lo','hi'])
    tb=qtab.iloc[-1].effect-qtab.iloc[0].effect
    tbse=math.sqrt(qtab.iloc[-1].se**2+qtab.iloc[0].se**2)
    return cal,(tb,tbse,tb-1.96*tbse,tb+1.96*tbse),qtab

def hte_suite(d,out):
    rows=[];quints=[];seedrows=[];cache={}
    for seed in SEEDS:
        for method in ['t','dr','r']:
            for treated in ['food','medical']:
                dd,W,Y,tau,foldid=hte_oof(d,treated,'cash',method,seed)
                cal,tb,q=evaluate_hte(dd,W,Y,tau)
                seedrows.append([seed,method,treated+'-cash',cal[0],*tb[::2]])
                if seed==SEED:
                    rows.append([treated+'-cash',method,*cal,*tb,len(dd)])
                    q.insert(0,'method',method);q.insert(0,'contrast',treated+'-cash');quints.append(q)
                    cache[(treated,method)]=(dd,W,Y,tau,foldid)
        print('HTE seed completed',seed,flush=True)
    pd.DataFrame(rows,columns=['contrast','method','calibration','cal_se','cal_lo','cal_hi','cal_p','top_bottom','tb_se','tb_lo','tb_hi','N']).to_csv(out/'nature_hte_primary.csv',index=False)
    pd.concat(quints).to_csv(out/'nature_hte_quintiles.csv',index=False)
    pd.DataFrame(seedrows,columns=['seed','method','contrast','calibration','top_bottom','tb_lo']).to_csv(out/'nature_hte_seeds.csv',index=False)
    return cache

def hte_asymmetry(cache,out,B=1500):
    rng=np.random.default_rng(SEED);rows=[]
    for method in ['t','dr','r']:
        two={t:cache[(t,method)] for t in ['food','medical']}
        base={t:evaluate_hte(x[0],x[1],x[2],x[3]) for t,x in two.items()}
        obs_cal=base['medical'][0][0]-base['food'][0][0]
        obs_tb=base['medical'][1][0]-base['food'][1][0]
        vals=[]
        # Shared cash observations are resampled together; all nine design cells
        # are independently bootstrapped, keeping randomized-cell structure.
        f,m=two['food'],two['medical']
        # Both pairwise frames retain original row order from d. Match cash by id.
        fid=f[0].id.to_numpy();mid=m[0].id.to_numpy(); common=np.intersect1d(fid,mid)
        for _ in range(B):
            sampled={}
            for amount in [200,1000,5000]:
                ca=np.intersect1d(common,f[0].loc[(f[0].transfer_type=='cash')&(f[0].amount==amount),'id'].to_numpy())
                sampled[('cash',amount)]=rng.choice(ca,len(ca),replace=True)
                for t,x in [('food',f),('medical',m)]:
                    ids=x[0].loc[(x[0].transfer_type==t)&(x[0].amount==amount),'id'].to_numpy()
                    sampled[(t,amount)]=rng.choice(ids,len(ids),replace=True)
            met={}
            for t,x in [('food',f),('medical',m)]:
                dd,W,Y,tau,_=x; mapper=pd.Series(np.arange(len(dd)),index=dd.id)
                pick=np.concatenate([mapper.loc[sampled[(form,a)]].to_numpy() for a in [200,1000,5000] for form in ['cash',t]])
                try:
                    cal,tb,_=evaluate_hte(dd.iloc[pick].reset_index(drop=True),W[pick],Y[pick],tau[pick])
                    met[t]=(cal[0],tb[0])
                except (ValueError,IndexError):met[t]=(np.nan,np.nan)
            vals.append(np.subtract(met['medical'],met['food']))
        a=np.asarray(vals,float)
        for j,(metric,obs) in enumerate([('calibration',obs_cal),('top_bottom',obs_tb)]):
            lo,hi=np.nanquantile(a[:,j],[.025,.975]);p=2*min(np.nanmean(a[:,j]<=0),np.nanmean(a[:,j]>=0))
            rows.append([method,metric,obs,lo,hi,min(1,p),B])
    pd.DataFrame(rows,columns=['method','metric','medical_minus_food','lo','hi','bootstrap_p','B']).to_csv(out/'nature_hte_asymmetry.csv',index=False)

def quality_prediction_hte(d,out,masks):
    rows=[];hte=[]
    for sn in ['R','C','Q1','Q2']:
        dd=d.loc[masks[sn]].reset_index(drop=True)
        for fs in ['O','ALL']:
            X=hf.add_design(dd,hf.SETS[fs]);pred=np.zeros(len(dd))
            X['form_cash']=dd.transfer_type.eq('cash').astype(int)
            X['form_food']=dd.transfer_type.eq('food').astype(int)
            X['form_medical']=dd.transfer_type.eq('medical').astype(int)
            X=X.drop(columns='type')
            for _,tr,te in folds(dd):
                p=fe.pipe_for(list(X.columns),'rf').fit(X.iloc[tr],dd.mpc_midpoint.iloc[tr]);pred[te]=p.predict(X.iloc[te])
            rows.append([sn,fs,len(dd),r2_score(dd.mpc_midpoint,pred),math.sqrt(mean_squared_error(dd.mpc_midpoint,pred)),mean_absolute_error(dd.mpc_midpoint,pred)])
        for t in ['food','medical']:
            z,W,Y,tau,_=hte_oof(dd,t,'cash','dr')
            cal,tb,_=evaluate_hte(z,W,Y,tau)
            hte.append([sn,t+'-cash',len(z),*cal,*tb])
        print('quality screen completed',sn,flush=True)
    pd.DataFrame(rows,columns=['sample','feature_set','N','r2','rmse','mae']).to_csv(out/'nature_quality_predictability.csv',index=False)
    pd.DataFrame(hte,columns=['sample','contrast','N','calibration','cal_se','cal_lo','cal_hi','cal_p','top_bottom','tb_se','tb_lo','tb_hi']).to_csv(out/'nature_quality_hte.csv',index=False)

def amount_hte(d,out):
    rows=[];pool=[]
    for amount in [200,1000,5000]:
        dd=d[d.amount.eq(amount)].reset_index(drop=True)
        for t in ['food','medical']:
            for method in ['t','dr']:
                z,W,Y,tau,_=hte_oof(dd,t,'cash',method)
                cal,tb,_=evaluate_hte(z,W,Y,tau)
                rows.append([amount,t+'-cash',method,len(z),*cal,*tb])
                if t=='medical':pool.append(pd.DataFrame({'amount':amount,'method':method,'y':Y,'W':W,'tc':(tau-tau.mean())/tau.std()}))
    pd.DataFrame(rows,columns=['amount','contrast','method','N','calibration','cal_se','cal_lo','cal_hi','cal_p','top_bottom','tb_se','tb_lo','tb_hi']).to_csv(out/'nature_amount_hte.csv',index=False)
    tests=[]
    for method in ['t','dr']:
        zz=pd.concat([z for z in pool if z.method.iloc[0]==method])
        m=smf.ols('y~W*C(amount)*tc',zz).fit(cov_type='HC1')
        terms=[x for x in m.params.index if 'W:C(amount)' in x and ':tc' in x]
        R=np.zeros((len(terms),len(m.params)))
        for i,x in enumerate(terms):R[i,list(m.params.index).index(x)]=1
        w=m.wald_test(R,scalar=True)
        tests.append([method,float(w.statistic),len(terms),float(w.pvalue),len(zz),'CATE standardized within amount; interaction omnibus'])
    pd.DataFrame(tests,columns=['method','wald_chi2','df','p','N','definition']).to_csv(out/'nature_amount_hte_omnibus.csv',index=False)

def amount_seed_stability(d,out):
    rows=[]
    for seed in SEEDS:
        for amount in [200,1000,5000]:
            dd=d[d.amount.eq(amount)].reset_index(drop=True)
            for method in ['t','dr']:
                z,W,Y,tau,_=hte_oof(dd,'medical','cash',method,seed)
                cal,tb,_=evaluate_hte(z,W,Y,tau)
                rows.append([seed,amount,method,cal[0],cal[2],cal[3],tb[0],tb[2],tb[3],len(z)])
    pd.DataFrame(rows,columns=['seed','amount','method','calibration','cal_lo','cal_hi','top_bottom','tb_lo','tb_hi','N']).to_csv(out/'nature_amount_seed_stability.csv',index=False)

def policy(d,out,seed=SEED,B=3000,write=True):
    mu=np.zeros((len(d),3));foldid=np.full(len(d),-1)
    for k,tr,te in folds(d,seed):
        foldid[te]=k
        for j,t in enumerate(FORMS):
            a=d.iloc[tr];a=a[a.transfer_type.eq(t)]
            Xa,cols=fe.design(a,hf.FEATURES);Xte,_=fe.design(d.iloc[te],hf.FEATURES)
            m=fe.pipe_for(cols,'rf').fit(Xa,a.mpc_midpoint);mu[te,j]=m.predict(Xte)
    ml=mu.argmax(1);tree=np.zeros(len(d),int)
    X=d[['income_h','q30_medexp','q29_foodexp','q42_age']]
    for k in range(5):
        tr=foldid!=k;te=foldid==k
        z=DecisionTreeClassifier(max_depth=2,min_samples_leaf=200,random_state=seed+k).fit(X.loc[tr],ml[tr])
        tree[te]=z.predict(X.loc[te])
    actual=d.transfer_type.map({t:i for i,t in enumerate(FORMS)}).to_numpy();y=d.mpc_midpoint.to_numpy();p=d.amount.map(d.groupby('amount').transfer_type.apply(lambda x:1/3)).to_numpy()
    policies={'all_cash':np.zeros(len(d),int),'all_food':np.ones(len(d),int),'all_medical':np.full(len(d),2),'depth2_tree':tree,'ml_argmax':ml}
    score={};rows=[];rng=np.random.default_rng(seed)
    for name,a in policies.items():
        ipw=(actual==a)*y/p
        dr=mu[np.arange(len(d)),a]+(actual==a)*(y-mu[np.arange(len(d)),a])/p
        score[name]=(ipw,dr)
    for name,a in policies.items():
        for est,j in [('IPW',0),('DR',1)]:
            v=score[name][j];dif=v-score['all_cash'][j]
            if B:
                idx=rng.integers(0,len(v),(B,len(v)))
                lo,hi=np.quantile(v[idx].mean(1),[.025,.975]);dlo,dhi=np.quantile(dif[idx].mean(1),[.025,.975])
            else:lo=hi=dlo=dhi=np.nan
            rows.append([name,est,v.mean(),lo,hi,dif.mean(),dlo,dhi,*[(a==k).mean() for k in range(3)]])
    tab=pd.DataFrame(rows,columns=['policy','estimator','value','lo','hi','gain_vs_cash','gain_lo','gain_hi','share_cash','share_food','share_medical'])
    if write:tab.to_csv(out/'nature_policy_value.csv',index=False)
    return tab

def policy_stability(d,out):
    rows=[]
    for seed in SEEDS:
        z=policy(d,out,seed,B=0,write=False)
        for _,r in z[z.policy.isin(['depth2_tree','ml_argmax'])].iterrows():
            rows.append([seed,r.policy,r.estimator,r.value,r.gain_vs_cash,r.share_cash,r.share_food,r.share_medical])
    pd.DataFrame(rows,columns=['seed','policy','estimator','value','gain_vs_cash','share_cash','share_food','share_medical']).to_csv(out/'nature_policy_seed_stability.csv',index=False)

def moderators(d,out,masks):
    rows=[];joint=[];binned=[]
    for sn,mask in masks.items():
        dd=d.loc[mask]
        for v in ['income_h','q43_edu','q30_medexp']:
            z=v+'_z'
            for contrast,t,c in [('medical-cash','medical','cash'),('medical-food','medical','food')]:
                f=f'outcome_ord~C(transfer_type)*C(amount)+{z}+C(transfer_type):{z}+C(amount):{z}'
                for cov in ['HC1','HC3']:
                    m=smf.ols(f,dd).fit(cov_type=cov)
                    b,se,lo,hi,p=hf.ctest(m,{f'C(transfer_type)[T.{t}]:{z}':1,f'C(transfer_type)[T.{c}]:{z}':-1})
                    rows.append([sn,v,contrast,'trend',cov,b,se,lo,hi,p,len(dd)])
                if sn in ['R','C']:
                    mm=smf.ols(f'outcome_ord~C(transfer_type)*C(amount)+C({v})+C(transfer_type):C({v})+C(amount):C({v})',dd).fit(cov_type='HC1')
                    terms=[a for a in mm.params.index if 'C(transfer_type)' in a and f'C({v})' in a]
                    R=np.zeros((len(terms),len(mm.params)))
                    for i,a in enumerate(terms):R[i,list(mm.params.index).index(a)]=1
                    w=mm.wald_test(R,scalar=True)
                    rows.append([sn,v,contrast,'factor_omnibus','HC1',float(w.statistic),np.nan,np.nan,np.nan,float(w.pvalue),len(dd)])
            if sn=='R':
                for level,g in dd.groupby(v):
                    for contrast,t,c in [('medical-cash','medical','cash'),('medical-food','medical','food')]:
                        a=g[g.transfer_type.eq(t)].outcome_ord;b=g[g.transfer_type.eq(c)].outcome_ord
                        if len(a)<20 or len(b)<20:continue
                        e=a.mean()-b.mean();se=math.sqrt(a.var()/len(a)+b.var()/len(b))
                        binned.append([v,level,contrast,len(a)+len(b),e,e-1.96*se,e+1.96*se])
        f='outcome_ord~C(transfer_type)*C(amount)'
        for v in ['income_h','q43_edu','q30_medexp']:
            z=v+'_z';f+=f'+{z}+C(transfer_type):{z}+C(amount):{z}'
        for cov in ['HC1','HC3']:
            m=smf.ols(f,dd).fit(cov_type=cov)
            for v in ['income_h','q43_edu','q30_medexp']:
                z=v+'_z';b,se,lo,hi,p=hf.ctest(m,{f'C(transfer_type)[T.medical]:{z}':1,f'C(transfer_type)[T.food]:{z}':-1})
                joint.append([sn,v,cov,b,se,lo,hi,p,len(dd)])
    pd.DataFrame(rows,columns=['sample','variable','contrast','spec','se_type','effect_or_wald','se','lo','hi','p','N']).to_csv(out/'nature_moderators.csv',index=False)
    pd.DataFrame(joint,columns=['sample','variable','se_type','effect','se','lo','hi','p','N']).to_csv(out/'nature_moderators_joint.csv',index=False)
    pd.DataFrame(binned,columns=['variable','level','contrast','N','effect','lo','hi']).to_csv(out/'nature_moderators_binned.csv',index=False)

def focused_medical_robustness(d,out,masks):
    top=['income_h','q43_edu','q30_medexp']
    controls=[x for x in hf.OBJECTIVE+hf.NEEDS if x not in top]
    ctrl='+'.join(f'C({x})' if x in hf.NOMINAL+hf.ORDERED else x for x in controls)
    rows=[]
    for sample in ['R','A','C','Q1','Q2']:
        z=d.loc[masks[sample]]
        for v in top:
            x=v+'_z';base=f'outcome_ord~C(transfer_type)*C(amount)*{x}'
            specs={'saturated':base,'controls':base+'+'+ctrl,'province_FE':base+'+C(q47_province)','citytier_FE':base+'+C(q49_citytier)'} if sample in ['R','C'] else {'saturated':base}
            for spec,formula in specs.items():
                covs=['HC1','HC3','province_cluster'] if sample=='R' else ['HC1']
                for cov in covs:
                    kw={'groups':z.q47_province} if cov=='province_cluster' else {}
                    m=smf.ols(formula,z).fit(cov_type='cluster' if cov=='province_cluster' else cov,cov_kwds=kw)
                    for contrast,t,c in [('medical-cash','medical','cash'),('medical-food','medical','food')]:
                        for amount in [200,1000,5000,'pooled']:
                            w={f'C(transfer_type)[T.{t}]:{x}':1,f'C(transfer_type)[T.{c}]:{x}':-1}
                            if amount=='pooled':
                                for a in [1000,5000]:
                                    w[f'C(transfer_type)[T.{t}]:C(amount)[T.{a}]:{x}']=1/3
                                    w[f'C(transfer_type)[T.{c}]:C(amount)[T.{a}]:{x}']=-1/3
                            elif amount!=200:
                                w[f'C(transfer_type)[T.{t}]:C(amount)[T.{amount}]:{x}']=1
                                w[f'C(transfer_type)[T.{c}]:C(amount)[T.{amount}]:{x}']=-1
                            b,se,lo,hi,p=hf.ctest(m,w)
                            rows.append([sample,v,contrast,spec,cov,amount,b,se,lo,hi,p,len(z)])
    pd.DataFrame(rows,columns=['sample','variable','contrast','spec','se_type','amount','effect','se','lo','hi','p','N']).to_csv(out/'nature_medical_focused_robustness.csv',index=False)

def focused_randomization_inference(d,out,B=1000):
    # Randomize form labels within fixed amount strata; the outcome and baseline
    # variable are kept fixed. Fast OLS is algebraically the same saturated trend.
    rng=np.random.default_rng(SEED);n=len(d);amount=d.amount.to_numpy();form=d.transfer_type.to_numpy();y=d.outcome_ord.to_numpy()
    rows=[]
    def fit(x,f):
        F=(f=='food').astype(float);M=(f=='medical').astype(float);A=(amount==1000).astype(float);B5=(amount==5000).astype(float)
        X=np.column_stack([np.ones(n),F,M,A,B5,F*A,F*B5,M*A,M*B5,x,F*x,M*x,A*x,B5*x])
        b=np.linalg.lstsq(X,y,rcond=None)[0]
        return b[11],b[11]-b[10]
    ix=[np.flatnonzero(amount==a) for a in [200,1000,5000]]
    for v in ['income_h','q43_edu','q30_medexp']:
        x=d[v+'_z'].to_numpy();obs=fit(x,form);null=np.zeros((B,2))
        for k in range(B):
            p=form.copy()
            for ii in ix:p[ii]=rng.permutation(p[ii])
            null[k]=fit(x,p)
        for j,contrast in enumerate(['medical-cash','medical-food']):
            pv=(1+(np.abs(null[:,j])>=abs(obs[j])).sum())/(B+1)
            rows.append([v,contrast,obs[j],pv,B,'form permuted within amount'])
    tab=pd.DataFrame(rows,columns=['variable','contrast','effect','randomization_p','permutations','scheme'])
    for contrast,ix in tab.groupby('contrast').groups.items():tab.loc[ix,'BH_q']=hf.bh(tab.loc[ix,'randomization_p'])
    tab.to_csv(out/'nature_focused_randomization_inference.csv',index=False)

def demographic_strata(d,out):
    rows=[]
    strata={'age_lt35':d.q42_age<35,'college_plus':d.q43_edu>=3,'nonagricultural_hukou':d.q23_hukou==2,'high_citytier':d.q49_citytier<=2}
    for name,mask in strata.items():
        for flag in [False,True]:
            z=d.loc[mask.eq(flag)]
            m=smf.ols('outcome_ord~C(transfer_type)*C(amount)',z).fit(cov_type='HC1')
            for t in ['food','medical']:
                w={f'C(transfer_type)[T.{t}]':1}
                for a in [1000,5000]:w[f'C(transfer_type)[T.{t}]:C(amount)[T.{a}]']=1/3
                b,se,lo,hi,p=hf.ctest(m,w)
                rows.append([name,flag,t+'-cash',len(z),b,lo,hi,p])
    pd.DataFrame(rows,columns=['stratum','group','contrast','N','effect','lo','hi','p']).to_csv(out/'nature_demographic_strata.csv',index=False)

def food_inframarginal(d,out):
    bounds={1:0,2:501,3:1001,4:2001,5:3001,6:5000}
    x=d[d.transfer_type.isin(['cash','food'])].copy();monthly=x.q29_foodexp.map(bounds)
    screens={'strict':x.amount<6*monthly,'very_strict':x.amount<=3*monthly}
    rows=[]
    for name,mask in screens.items():
        z=x.loc[mask];m=smf.ols('outcome_ord~C(transfer_type)*C(amount)',z).fit(cov_type='HC1')
        w={'C(transfer_type)[T.food]':1,'C(transfer_type)[T.food]:C(amount)[T.1000]':1/3,'C(transfer_type)[T.food]:C(amount)[T.5000]':1/3}
        b,se,lo,hi,p=hf.ctest(m,w);rows.append([name,len(z),b,se,lo,hi,p])
    pd.DataFrame(rows,columns=['screen','N','food_minus_cash_ordinal','se','lo','hi','p']).to_csv(out/'nature_food_inframarginal.csv',index=False)

def response_style(d,out,masks):
    x=d[QUALITY_ITEMS];sd=x.std(1);unique=x.nunique(1);extreme=x.isin([0,10]).mean(1);mid=(x==5).mean(1)
    rows=[]
    for name,mask in masks.items():
        rows.append([name,int(mask.sum()),int((unique[mask]==1).sum()),int((sd[mask]<1).sum()),sd[mask].mean(),unique[mask].mean(),extreme[mask].mean(),mid[mask].mean(),float(x.loc[mask].apply(lambda r:stats.entropy(r.value_counts(normalize=True)),axis=1).mean())])
    pd.DataFrame(rows,columns=['sample','N','complete_straightline_N','near_straightline_sd_lt1_N','mean_scale_sd','mean_unique','mean_extreme_share','mean_midpoint_share','mean_entropy']).to_csv(out/'nature_response_style.csv',index=False)

def shared_variance(out):
    tab=pd.read_csv(Path(__file__).resolve().parents[1]/'tables'/'final_shared_specific_decomposition.csv')
    total=tab.loc[tab.component.eq('actual_outcome'),'variance'].iloc[0]
    tab['ratio_to_observed']=tab.variance/total
    tab['warning']='Descriptive non-additive variances; not a partition of total variance'
    tab.to_csv(out/'nature_shared_variance.csv',index=False)

def copy_baselines(out):
    root=Path(__file__).resolve().parents[1]/'tables'
    for src,dst in [('final_latent_diagnostics.csv','nature_latent_diagnostics.csv'),('final_latent_increment.csv','nature_latent_increment.csv'),('final_latent_loadings.csv','nature_latent_loadings.csv'),('final_outcome_sensitivity.csv','nature_outcome_sensitivity.csv'),('formal_food_null_precision.csv','nature_food_null_precision.csv'),('formal_medical_food_robustness.csv','nature_medical_robustness.csv'),('formal_randomization_inference.csv','nature_randomization_inference.csv'),('final_quality_composition.csv','nature_quality_composition.csv'),('final_external_benchmarks.csv','nature_external_benchmarks.csv')]:
        pd.read_csv(root/src).to_csv(out/dst,index=False)

def main(input_path,outdir):
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    d=hf.prep(pd.read_stata(input_path,convert_categoricals=False));assert len(d)==5497
    masks=quality_masks(d)
    cell_distributions(d,out);effects(d,out,masks);print('design/effects done',flush=True)
    level_cv(d,out);print('level CV done',flush=True)
    _,contrasts=cross_form(d,out);coefficient_differences(d,out,contrasts);reliability(out);shared_variance(out);print('portability done',flush=True)
    cache=hte_suite(d,out);hte_asymmetry(cache,out);print('HTE asymmetry done',flush=True)
    quality_prediction_hte(d,out,masks);amount_hte(d,out);amount_seed_stability(d,out);print('quality/amount HTE done',flush=True)
    policy(d,out);policy_stability(d,out);moderators(d,out,masks);focused_medical_robustness(d,out,masks);focused_randomization_inference(d,out);demographic_strata(d,out);food_inframarginal(d,out);response_style(d,out,masks);copy_baselines(out)
    summary={'N_R':len(d),'N_A':int(d.sample_A.sum()),'N_C':int(d.sample_C.sum()),'seeds':SEEDS,'outer_folds':5,'level_repeats':2,'individual_outputs_written':False}
    (out/'nature_run_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    p=ArgumentParser();p.add_argument('data');p.add_argument('--out',default='nature-output');a=p.parse_args();main(a.data,a.out)
