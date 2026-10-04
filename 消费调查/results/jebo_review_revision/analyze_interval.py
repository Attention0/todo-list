"""Frozen censored-normal sensitivity; grouped records, not cell-mean regression."""
from common import *
from scipy.optimize import minimize
from scipy.special import ndtr
from scipy.optimize._numdiff import approx_derivative
assert (O/'QUESTION_INTERVAL_AUDIT.md').exists()
c6=counts(); c=np.column_stack([c6[:,:2].sum(1),c6[:,2:]])
t=np.tile(AMOUNTS/1000,3); F=np.eye(3)[np.repeat(np.arange(3),3)]
edges=np.column_stack([np.full(9,-np.inf),t[:,None]*np.array([.1,.25,.5,.75]),np.full(9,np.inf)])
N=c.sum(); rng=np.random.default_rng(2026100418)
boots=np.stack([rng.multinomial(int(row.sum()),row/row.sum(),size=4000) for row in c],axis=1)
def setup(scale,full):
    X=np.column_stack([F,F*t[:,None]]) if full else np.column_stack([F,t])
    Z=np.ones((9,1)) if scale=='constant' else np.eye(3)[np.tile(np.arange(3),3)]
    return X,Z
def evaluate(par,X,Z):
    q=X.shape[1];mu=X@par[:q];sig=np.exp(Z@par[q:]);a=(edges-mu[:,None])/sig[:,None]
    prob=np.maximum(np.diff(ndtr(a),axis=1),1e-300)
    pdf=np.exp(-.5*a*a)/np.sqrt(2*np.pi); ap=np.zeros_like(a);np.multiply(a,pdf,out=ap,where=np.isfinite(a))
    dm=(pdf[:,:-1]-pdf[:,1:])/sig[:,None]; ds=ap[:,:-1]-ap[:,1:]
    scores=np.concatenate([(dm/prob)[:,:,None]*X[:,None,:],(ds/prob)[:,:,None]*Z[:,None,:]],axis=2)
    return prob,scores
def fit(cc,X,Z,start,neutral):
    def fun(par):
        pr,sc=evaluate(par,X,Z);return -float((cc*np.log(pr)).sum())/N,-(cc[:,:,None]*sc).sum((0,1))/N
    r=minimize(fun,start,jac=True,method='L-BFGS-B',bounds=[(None,None)]*X.shape[1]+[(-9,5)]*Z.shape[1],options={'ftol':1e-12,'gtol':1e-7,'maxiter':600,'maxls':40})
    retry=False
    if not (r.success and np.max(abs(r.jac))<1e-4):
        retry=True;r=minimize(fun,neutral,jac=True,method='L-BFGS-B',bounds=[(None,None)]*X.shape[1]+[(-9,5)]*Z.shape[1],options={'ftol':1e-12,'gtol':1e-7,'maxiter':600,'maxls':40})
    ok=bool(r.success and np.max(abs(r.jac))<1e-4)
    return r,ok,retry
params=[];cal=[];diag=[];status=[]
for scale in ['constant','amount']:
    for full in [True,False]:
        X,Z=setup(scale,full);q=X.shape[1]
        neutral=np.r_[np.zeros(3),np.full(q-3,.2),np.log([.6] if scale=='constant' else [.08,.4,2.])]
        r,ok,retry=fit(c,X,Z,neutral,neutral);assert ok,(scale,full,r.message,r.jac)
        pr,sc=evaluate(r.x,X,Z)
        def grad(par):return -(c[:,:,None]*evaluate(par,X,Z)[1]).sum((0,1))
        H=approx_derivative(grad,r.x,method='3-point');H=(H+H.T)/2;inv=np.linalg.inv(H)
        meat=np.einsum('ij,ijk,ijl->kl',c,sc,sc);V=inv@meat@inv
        model=scale+('_full' if full else '_common_slope')
        diag.append(dict(model=model,loglik=float((c*np.log(pr)).sum()),parameters=len(r.x),converged=ok,retry=retry,max_gradient=float(abs(r.jac).max()),hessian_min_eigenvalue=float(np.linalg.eigvalsh(H).min()),mean_abs_probability_error=float(abs(pr-c/c.sum(1)[:,None]).mean()),max_probability_error=float(abs(pr-c/c.sum(1)[:,None]).max())))
        bb=None
        if full:
            bs=[]
            for i,cc in enumerate(boots):
                rb,ob,re=fit(cc,X,Z,r.x,neutral);status.append(dict(model=model,draw=i+1,converged=ob,retry=re,max_gradient=float(abs(rb.jac).max())))
                bs.append(rb.x if ob else np.full(len(r.x),np.nan))
                if (i+1)%500==0:print(model,i+1,'failures',sum(not s['converged'] for s in status if s['model']==model),flush=True)
            bb=np.array(bs);(O/'private_cache').mkdir(exist_ok=True);np.save(O/'private_cache'/f'{model}_bootstrap.npy',bb)
            # All valid-draw intervals explicitly carry their denominator/failures.
        names=[f+' intercept' for f in FORMS]+([f+' slope' for f in FORMS] if full else ['common slope'])+(['sigma'] if scale=='constant' else ['sigma '+str(a) for a in AMOUNTS])
        for j,name in enumerate(names):
            if j<q:
                factor=1000 if j<3 else 1;row=dict(model=model,parameter=name,**inf(r.x[j]*factor,np.sqrt(V[j,j])*factor))
                boot=bb[:,j]*factor if bb is not None else None
            else:
                row=dict(model=model,parameter=name,estimate=np.exp(r.x[j])*1000,se=np.exp(r.x[j])*1000*np.sqrt(V[j,j]),lo=np.exp(r.x[j]-1.96*np.sqrt(V[j,j]))*1000,hi=np.exp(r.x[j]+1.96*np.sqrt(V[j,j]))*1000,p=np.nan)
                boot=np.exp(bb[:,j])*1000 if bb is not None else None
            if boot is not None:row.update(bootstrap_lo=np.nanquantile(boot,.025),bootstrap_hi=np.nanquantile(boot,.975),bootstrap_valid=int(np.isfinite(boot).sum()),bootstrap_failed=int(np.isnan(boot).sum()))
            params.append(row)
        if full:
            C=np.zeros((2,len(r.x)));C[0,3:6]=[1,-1,0];C[1,3:6]=[1,0,-1]
            diag[-1].update(slope_equality_p=wald(r.x,V,C)['p'])
            for f,g in [(0,1),(0,2),(1,2)]:
                cv=np.zeros(len(r.x));cv[3+f]=1;cv[3+g]=-1;boot=bb@cv
                params.append(dict(model=model,parameter=f'{FORMS[f]}-{FORMS[g]} slope',**inf(cv@r.x,np.sqrt(cv@V@cv)),bootstrap_lo=np.nanquantile(boot,.025),bootstrap_hi=np.nanquantile(boot,.975),bootstrap_valid=int(np.isfinite(boot).sum()),bootstrap_failed=int(np.isnan(boot).sum())))
        for j in range(9):
            for k in range(5):cal.append(dict(model=model,form=FORMS[j//3],amount=int(AMOUNTS[j%3]),merged_category=k+1,count=int(c[j,k]),N=int(c[j].sum()),observed_probability=c[j,k]/c[j].sum(),predicted_probability=pr[j,k],error=pr[j,k]-c[j,k]/c[j].sum()))
save(params,'interval_affine_parameters.csv');save(cal,'interval_affine_fit.csv');save(diag,'interval_affine_diagnostics.csv');save(status,'interval_bootstrap_status.csv')
note('INTERVAL_MODEL_RESULT.md','# Censored-normal affine sensitivity\n\n'+mdtable(pd.DataFrame(diag))+'\n\nBounds are conditional on the questionnaire audit: merged below10%, 10–25%, 25–50%, 50–75%, and right-censored above75%. No zero/100% cap is imposed. The latent normal can be negative and has no structural spending interpretation. Constant residual scale is the frozen primary sensitivity; three amount-specific scales are the single frozen alternative. Sandwich covariance uses individual category scores and the observed likelihood Hessian. Bootstrap failures are retained in interval_bootstrap_status.csv and valid-draw denominators are attached to every percentile interval. Good numerical convergence does not establish measurement validity; calibration discrepancies must accompany all parameter interpretations.')
print(pd.DataFrame(diag).to_string(index=False),flush=True)
