"""Grouped likelihood/individual-score engine. Groups are sufficient, not clusters.

Covariance weights count individual independent scores; no respondent export.
All null bootstrap draws share the same Gaussian person multipliers, compressed
exactly by sufficient group (form, amount, outcome category, sample membership).
"""
import numpy as np
import pandas as pd
from scipy import stats, optimize
from scipy.special import expit
from scipy.optimize._numdiff import approx_derivative

OUTCOMES=['ordinal','midpoint','any_spending','ge10','ge25','ge50','top75']
SAMPLES=['R','A','C','Q1','Q2']
MODELS=['OLS_HC3','logit','probit','ordered_logit','ordered_probit','ordered_location_scale']
CONTRASTS=['omnibus','cash-food','cash-medical','food-medical','restricted-cash']
REPS=['trend','saturated','endpoint']
MID=np.array([0,.05,.175,.375,.625,.875])

def groups(d):
    bits=np.ones(len(d),int)
    for j,s in enumerate(SAMPLES[1:],1):bits+=d['sample_'+s].to_numpy().astype(int)*(2**j)
    raw=pd.DataFrame({'cell':d.cell,'bits':bits,'category':d.ordinal})
    rows=[]
    for (cell,b),part in raw.groupby(['cell','bits']):
        c=part.category.value_counts()
        for k in range(1,7):rows.append(dict(cell=cell,bits=b,category=k,count=int(c.get(k,0)),block_N=len(part)))
    return pd.DataFrame(rows)

def design(cell,rep,ordered=False):
    cell=np.asarray(cell);f=cell//3;a=cell%3
    food=(f==1).astype(float);medical=(f==2).astype(float)
    amount=(a-1).astype(float)[:,None] if rep=='trend' else ((a==2).astype(float)[:,None] if rep=='endpoint' else np.column_stack([a==1,a==2]).astype(float))
    main=np.column_stack([np.ones(len(cell)),food,medical,amount])
    X=np.column_stack([main,food[:,None]*amount,medical[:,None]*amount])
    if ordered:X=X[:,1:];main=main[:,1:]
    interactions=list(range(main.shape[1],X.shape[1]))
    return X,interactions

def yvals(category,outcome):
    k=np.asarray(category,int)
    if outcome=='ordinal':return k.astype(float)
    if outcome=='midpoint':return MID[k-1]
    return (k>=dict(any_spending=2,ge10=3,ge25=4,ge50=5,top75=6)[outcome]).astype(float)

def ordered_score(p,X,k,link,scale=False):
    q=X.shape[1];beta=p[:q];gamma=p[q:q+5]
    cuts=np.r_[gamma[0],gamma[0]+np.cumsum(np.exp(gamma[1:]))]
    sigma=np.exp(np.clip(X@p[q+5:],-12,12)) if scale else np.ones(len(X))
    eta=X@beta
    kk=k.astype(int)-1
    hi=np.where(kk<5,cuts[np.minimum(kk,4)],np.inf)
    lo=np.where(kk>0,cuts[np.maximum(kk-1,0)],-np.inf)
    uhi=(hi-eta)/sigma;ulo=(lo-eta)/sigma
    if link=='logit':
        H,L=expit(uhi),expit(ulo);dh=H*(1-H);dl=L*(1-L)
    else:H,L=stats.norm.cdf(uhi),stats.norm.cdf(ulo);dh=stats.norm.pdf(uhi);dl=stats.norm.pdf(ulo)
    pr=np.clip(H-L,1e-14,1)
    sb=(dl-dh)[:,None]*X/sigma[:,None]
    J=np.zeros((5,5));J[:,0]=1
    for j in range(1,5):J[j:,j]=np.exp(gamma[j])
    sh=J[np.minimum(kk,4)]*dh[:,None];sl=J[np.maximum(kk-1,0)]*dl[:,None]
    sh[kk==5]=0;sl[kk==0]=0
    st=(sh-sl)/sigma[:,None]
    score=np.column_stack([sb,st])/pr[:,None]
    if scale:
        ph=np.where(np.isfinite(uhi),uhi,0)*dh
        pl=np.where(np.isfinite(ulo),ulo,0)*dl
        score=np.column_stack([score,(pl-ph)[:,None]*X/pr[:,None]])
    return pr,score

def fit(X,y,n,model,interaction,constrained=False):
    """Return params, individual influence, covariance, null score diagnostics."""
    N=n.sum();q=X.shape[1]
    if model=='OLS_HC3':
        free=[j for j in range(q) if not constrained or j not in interaction]
        Z=X[:,free];b=np.linalg.solve((Z*n[:,None]).T@Z,(Z*n[:,None]).T@y)
        p=np.zeros(q);p[free]=b
        bread=np.linalg.inv((X*n[:,None]).T@X)
        resid=y-X@p;leverage=np.einsum('ij,jk,ik->i',X,bread,X)
        inf=(X@bread)*((resid/(1-leverage))[:,None])
        if constrained:inf-=np.average(inf,axis=0,weights=n)
        cov=(inf*n[:,None]).T@inf
        return dict(params=p,inf=inf,cov=cov,converged=True,ll=np.nan,grad=0.,hessian_min=np.linalg.eigvalsh(np.linalg.inv(bread)).min(),k=q,scale='response units')
    ordered=model.startswith('ordered');scale=model=='ordered_location_scale'
    link='logit' if 'logit' in model else 'probit'
    if ordered:
        freqs=np.bincount(y.astype(int),weights=n,minlength=7)[1:]/N
        cuts=stats.logistic.ppf(np.cumsum(freqs)[:5]) if link=='logit' else stats.norm.ppf(np.cumsum(freqs)[:5])
        start=np.r_[np.zeros(q),cuts[0],np.log(np.diff(cuts)),np.zeros(q) if scale else []]
        def score(p):return ordered_score(p,X,y,link,scale)
    else:
        start=np.zeros(q);mean=np.clip(np.average(y,weights=n),.001,.999)
        start[0]=stats.logistic.ppf(mean) if link=='logit' else stats.norm.ppf(mean)
        def score(p):
            eta=X@p
            pr=expit(eta) if link=='logit' else stats.norm.cdf(eta)
            pr=np.clip(pr,1e-12,1-1e-12)
            den=pr*(1-pr) if link=='logit' else stats.norm.pdf(eta)
            return pr, X*((y-pr)*den/(pr*(1-pr)))[:,None]
    zero=list(interaction) if constrained else []
    if scale and constrained:zero+= [q+5+j for j in interaction]
    free=np.setdiff1d(np.arange(len(start)),zero)
    def unpack(u):
        p=start.copy();p[free]=u;return p
    def objective(u):
        pr,sc=score(unpack(u))
        logp=np.log(pr) if ordered else y*np.log(pr)+(1-y)*np.log1p(-pr)
        return -n@logp/N, -(n@sc)[free]/N
    opt=optimize.minimize(objective,start[free],jac=True,method='BFGS',options={'gtol':1e-8,'maxiter':600})
    p=unpack(opt.x);pr,sc=score(p)
    H=-approx_derivative(lambda v:n@score(v)[1],p,method='3-point');H=(H+H.T)/2
    eig=np.linalg.eigvalsh(H);bread=np.linalg.inv(H)
    inf=sc@bread
    if constrained:inf-=np.average(inf,axis=0,weights=n)
    cov=(inf*n[:,None]).T@inf*N/(N-len(p))
    inf*=np.sqrt(N/(N-len(p)))
    grad=np.max(np.abs(objective(opt.x)[1]))
    converged=bool(np.isfinite(p).all() and grad<1e-5 and eig.min()>1e-7)
    ll=n@(np.log(pr) if ordered else y*np.log(pr)+(1-y)*np.log1p(-pr))
    return dict(params=p,inf=inf,cov=cov,converged=converged,ll=float(ll),grad=float(grad),hessian_min=float(eig.min()),k=len(p),scale='latent location index' if ordered else link+' index',message=str(opt.message))

def matrices(q,interaction,rep,total):
    nd=2 if rep=='saturated' else 1
    I=np.eye(total)[interaction]
    food,med=I[:nd],I[nd:]
    return {'omnibus':I,'cash-food':-food,'cash-medical':-med,'food-medical':food-med,'restricted-cash':.5*(food+med)}

def whiten(cov):
    v,u=np.linalg.eigh(cov)
    if v.min()<=1e-15:raise ValueError('singular contrast covariance')
    return u@np.diag(1/np.sqrt(v))@u.T

def run_grid(g, verbose=True):
    rows=[];blocks=[];focal=[];diag=[]
    for si,sample in enumerate(SAMPLES):
        mask=(g.bits.to_numpy() & (2**si))>0
        for rep in REPS:
            sel=mask & ((g.cell.to_numpy()%3!=1) if rep=='endpoint' else True)
            gg=g[sel];n=gg['count'].to_numpy(float)
            for outcome in OUTCOMES:
                models=['OLS_HC3']+(['ordered_logit','ordered_probit','ordered_location_scale'] if outcome=='ordinal' else ['logit','probit'] if outcome not in ['midpoint'] else [])
                for model in models:
                    ident=f'{sample}/{rep}/{outcome}/{model}'
                    X,ix=design(gg.cell,rep,model.startswith('ordered'))
                    y=yvals(gg.category,outcome)
                    try:
                        full=fit(X,y,n,model,ix)
                        null=fit(X,y,n,model,ix,True)
                        if not full['converged'] or not null['converged']:raise ValueError(f'nonconvergence full/null {full["grad"]}/{null["grad"]}; eigen {full["hessian_min"]}/{null["hessian_min"]}')
                        vv=matrices(X.shape[1],ix,rep,len(full['params']))
                        diag.append(dict(model_id=ident,status='ok',N=int(n.sum()),full_gradient=full['grad'],null_gradient=null['grad'],full_hessian_min=full['hessian_min'],null_hessian_min=null['hessian_min'],full_params=json_array(full['params']),full_se=json_array(np.sqrt(np.diag(full['cov']))),parameter_order='design columns; ordered: 5 cutpoint-transform parameters; location-scale: design columns for log scale',null_params=json_array(null['params'])))
                        for target,C in vv.items():
                            e=C@full['params'];cv=C@full['cov']@C.T
                            w=whiten(cv);z=np.linalg.norm(w@e);df=len(e)
                            ni=null['inf']@C.T;nc=(ni*n[:,None]).T@ni
                            ni=ni@whiten(nc)
                            # One block per test (scalar or multivariate Wald norm).
                            master=np.zeros((len(g),df));master[sel]=ni
                            row=dict(spec_id=ident+'/'+target,sample=sample,representation=rep,outcome=outcome,model=model,contrast=target,N=int(n.sum()),df=df,estimate=e[0] if df==1 else np.nan,se=np.sqrt(cv[0,0]) if df==1 else np.nan,lo=e[0]-1.96*np.sqrt(cv[0,0]) if df==1 else np.nan,hi=e[0]+1.96*np.sqrt(cv[0,0]) if df==1 else np.nan,profile=json_array(e),profile_lo=json_array(e-1.96*np.sqrt(np.diag(cv))),profile_hi=json_array(e+1.96*np.sqrt(np.diag(cv))),statistic=z,wald=z*z,p=float(stats.chi2.sf(z*z,df)),scale=full['scale'],status='ok',failure_reason='',estimand='full pairwise interaction vector at1000/5000 vs200' if rep=='saturated' else 'per-fivefold amount slope difference' if rep=='trend' else '5000-minus200 response/link difference-in-differences')
                            rows.append(row);blocks.append(master)
                        if sample=='R' and rep=='trend' and outcome=='top75' and model=='OLS_HC3':
                            # Full design columns Intercept Food Medical z Food*z Medical*z.
                            for name,v in [('cash',[0,0,0,1,0,0]),('food',[0,0,0,1,1,0]),('medical',[0,0,0,1,0,1])]:
                                v=np.array(v);e=v@full['params'];se=np.sqrt(v@full['cov']@v)
                                focal.append(dict(estimand=name+'_slope',estimate=e,se=se,lo=e-1.96*se,hi=e+1.96*se,p=2*stats.norm.sf(abs(e/se)),N=int(n.sum()),df=1,scale='probability per fivefold',role='within-form descriptive slope'))
                    except Exception as ex:
                        diag.append(dict(model_id=ident,status='failed',failure_reason=str(ex),N=int(n.sum())))
                        for target in CONTRASTS:rows.append(dict(spec_id=ident+'/'+target,sample=sample,representation=rep,outcome=outcome,model=model,contrast=target,N=int(n.sum()),status='failed',failure_reason=str(ex)));blocks.append(None)
            if verbose:print('Grid completed',sample,rep,flush=True)
    return pd.DataFrame(rows),blocks,pd.DataFrame(focal),pd.DataFrame(diag)

def json_array(x):
    import json
    return json.dumps(np.asarray(x).tolist())

def max_statistics(matrix, sizes, draws):
    # Same grouped person-multiplier draw across every outcome/model/sample.
    values=draws@matrix;maximum=np.zeros(len(draws));start=0
    for size in sizes:
        maximum=np.maximum(maximum,np.linalg.norm(values[:,start:start+size],axis=1));start+=size
    return maximum

def multiplier(g,blocks,B,seed):
    keep=[b for b in blocks if b is not None]
    sizes=[b.shape[1] for b in keep];matrix=np.column_stack(keep)
    rng=np.random.default_rng(seed);draws=rng.normal(size=(B,len(g)))*np.sqrt(g['count'].to_numpy())[None,:]
    return max_statistics(matrix,sizes,draws),matrix,sizes
