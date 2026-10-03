import argparse,json
import statsmodels.api as sm
import statsmodels.formula.api as smf
from common import *
p=argparse.ArgumentParser();p.add_argument('--data',required=True);a=p.parse_args()
d=load(a.data); cnt=counts();ns=cnt.sum(1);cell=np.repeat(np.arange(9),6);form=cell//3;amount=AMOUNTS[cell%3];n=cnt.ravel()
raw=np.array([[int(((d.cell==j)&(d.ordinal==k)).sum()) for k in range(1,7)] for j in range(9)])
assert np.array_equal(raw,cnt) and ns.sum()==5480
rng=np.random.default_rng(2026100417);B=4000
boots=np.stack([rng.multinomial(int(N),row/N,size=B) for row,N in zip(cnt,ns)],axis=1)
means=cnt@SCORES/ns;bm=boots@SCORES/ns;yuan=means*np.tile(AMOUNTS,3);by=bm*np.tile(AMOUNTS,3)
se=np.sqrt(np.array([np.repeat(SCORES,c).var(ddof=1)/N for c,N in zip(cnt,ns)]));vy=(se*np.tile(AMOUNTS,3))**2*ns/(ns-1)
rows=[];dist=[]
for j,(c,N) in enumerate(zip(cnt,ns)):
    lo,hi=np.quantile(bm[:,j],[.025,.975]);r=dict(form=FORMS[j//3],amount=int(AMOUNTS[j%3]),N=N,ordinal=c@np.arange(1,7)/N,midpoint=means[j],midpoint_lo=lo,midpoint_hi=hi,yuan=yuan[j],yuan_lo=lo*AMOUNTS[j%3],yuan_hi=hi*AMOUNTS[j%3],top75=c[-1]/N,above_bottom=1-c[0]/N)
    for key,vals in [('ordinal',boots[:,j]@np.arange(1,7)/N),('top75',boots[:,j,-1]/N),('above_bottom',1-boots[:,j,0]/N)]:r[key+'_lo'],r[key+'_hi']=np.quantile(vals,[.025,.975])
    for k in range(6):r['count'+str(k+1)]=c[k];r['share'+str(k+1)]=c[k]/N;dist.append(dict(sample='A',form=r['form'],amount=r['amount'],N=N,category=k+1,count=c[k],share=c[k]/N))
    rows.append(r)
save(rows,'adult_share_yuan_table.csv');save(dist,'adult_cell_distribution.csv')
inc=[];elastic=[];irs={};ers={}
for f in range(3):
    ix=3*f
    for label,l,h,delta in [('low',0,1,800),('high',1,2,4000)]:
        v=np.zeros(9);v[ix+h]=1/delta;v[ix+l]=-1/delta;boot=by@v;e=yuan@v
        r=dict(form=FORMS[f],interval=label,contrast='within-form',**inf(e,np.sqrt(v@np.diag(vy)@v)))
        r['bootstrap_lo'],r['bootstrap_hi']=np.quantile(boot,[.025,.975]);inc.append(r);irs[f,label]=(v,boot)
    eta=np.log(yuan[ix+2]/yuan[ix])/np.log(25);be=np.log(by[:,ix+2]/by[:,ix])/np.log(25)
    elastic.append(dict(form=FORMS[f],contrast='within-form',estimate=eta,bootstrap_lo=np.quantile(be,.025),bootstrap_hi=np.quantile(be,.975)));ers[f]=be
pair=[]
for l in ['low','high']:
    for f,g in [(0,1),(0,2),(1,2)]:
        v=irs[f,l][0]-irs[g,l][0];be=irs[f,l][1]-irs[g,l][1]
        pair.append(dict(form='',interval=l,contrast=FORMS[f]+'-'+FORMS[g],**inf(yuan@v,np.sqrt(v@np.diag(vy)@v)),bootstrap_lo=np.quantile(be,.025),bootstrap_hi=np.quantile(be,.975)))
for r,h in zip(pair,holm([r['p'] for r in pair])):r['holm6']=h
save(inc+pair,'incremental_yuan_response.csv')
for f,g in [(0,1),(0,2),(1,2)]:
    be=ers[f]-ers[g];elastic.append(dict(form='',contrast=FORMS[f]+'-'+FORMS[g],estimate=elastic[f]['estimate']-elastic[g]['estimate'],bootstrap_lo=np.quantile(be,.025),bootstrap_hi=np.quantile(be,.975)))
save(elastic,'endpoint_elasticity.csv')

# OLS grouped sufficient statistics preserve individual outcome dispersion and HC3.
F=np.eye(3)[form];t=amount/1000.;y=np.tile(SCORES,9)*amount
Xs={'common':np.column_stack([np.ones(54),t]),'form_intercepts':np.column_stack([F,t]),'form_intercepts_slopes':np.column_stack([F,F*t[:,None]])}
fits={};parameters=[];fitrows=[];comparisons=[]
for name,X in Xs.items():
    b,v,br=grouped_fit(X,y,n);fits[name]=(b,v)
    Xcell=X[::6];bb=by@(Xcell*ns[:,None])@br
    names=['intercept','slope'] if name=='common' else [f+' intercept' for f in FORMS]+(['common slope'] if name=='form_intercepts' else [f+' slope' for f in FORMS])
    scale=np.array([1 if 'intercept' in q else .001 for q in names])
    for j,nm in enumerate(names):parameters.append(dict(model=name,parameter=nm,**inf(b[j]*scale[j],np.sqrt(v[j,j])*scale[j]),bootstrap_lo=np.quantile(bb[:,j]*scale[j],.025),bootstrap_hi=np.quantile(bb[:,j]*scale[j],.975)))
    if name=='form_intercepts_slopes':
        for typ,off,k in [('intercept',0,1),('slope',3,.001)]:
            for f,g in [(0,1),(0,2),(1,2)]:
                C=np.eye(6)[off+f]-np.eye(6)[off+g];be=bb@C*k
                parameters.append(dict(model=name,parameter=f'{FORMS[f]}-{FORMS[g]} {typ}',**inf(C@b*k,np.sqrt(C@v@C)*k),bootstrap_lo=np.quantile(be,.025),bootstrap_hi=np.quantile(be,.975)))
    fitted=Xcell@b;res=yuan-fitted
    # Saturated-cell residual projection gives all independent lack-of-fit contrasts.
    R=np.eye(9)-Xcell@br@Xcell.T@np.diag(ns);rv=R@np.diag(vy)@R.T;w=float(res@np.linalg.pinv(rv)@res);df=9-X.shape[1]
    comparisons.append(dict(comparison=name+' vs saturated cells',wald=w,df=df,p=stats.chi2.sf(w,df),RMSE=float(np.sqrt(np.average(res*res,weights=ns))),type='diagnostic lack-of-fit'))
    for j in range(9):fitrows.append(dict(model=name,form=FORMS[j//3],amount=int(AMOUNTS[j%3]),observed_yuan=yuan[j],predicted_yuan=fitted[j],error=res[j],N=ns[j]))
for name,model,C in [('common vs form intercepts','form_intercepts',np.array([[1,-1,0,0],[1,0,-1,0]])),('common slope vs form slopes','form_intercepts_slopes',np.array([[0,0,0,1,-1,0],[0,0,0,1,0,-1]])),('common vs form intercepts and slopes','form_intercepts_slopes',np.array([[1,-1,0,0,0,0],[1,0,-1,0,0,0],[0,0,0,1,-1,0],[0,0,0,1,0,-1]]))]:
    b,v=fits[model];comparisons.append(dict(comparison=name,type='nested robust Wald',**wald(b,v,C)))
for r,h in zip(comparisons[-3:],holm([r['p'] for r in comparisons[-3:]])):r['holm3']=h
save(parameters,'affine_midpoint_parameters.csv');save(comparisons,'affine_model_comparison.csv');save(fitrows,'affine_midpoint_fit.csv')

# Joint42 influence covariance of the21 form-specific slopes.
X=np.column_stack([F,F*(cell%3)[:,None]]);bread=np.linalg.inv(X.T@(n[:,None]*X));YY=np.tile(YS,(9,1));b=bread@X.T@(n[:,None]*YY)
h=np.einsum('ij,jk,ik->i',X,bread,X);res=(YY-X@b)/(1-h[:,None]);vv=X@bread[:,3:]
IF=(res[:,:,None]*vv[:,None,:]).reshape(54,21);cov=IF.T@(n[:,None]*IF);e=b[3:,:].T.ravel()
def p42(ee):
    ee=np.atleast_2d(ee);pp=[]
    for j in range(7):
        sl=slice(3*j,3*j+3);v=cov[sl,sl];u=ee[:,sl];C=np.array([[1,-1,0],[1,0,-1]]);dd=u@C.T;dv=C@v@C.T
        pp += [2*stats.norm.sf(abs(u[:,k])/np.sqrt(v[k,k])) for k in range(3)]
        pp += [stats.chi2.sf(np.einsum('bi,ij,bj->b',dd,np.linalg.inv(dv),dd),2)]
        pp += [2*stats.norm.sf(abs(dd[:,k])/np.sqrt(dv[k,k])) for k in range(2)]
    return np.column_stack(pp)
val,vec=np.linalg.eigh(cov);root=vec*np.sqrt(np.maximum(val,0))[None,:];sim=np.random.default_rng(2026100419).normal(size=(10000,21))@root.T
pp=p42(e)[0];mins=p42(sim).min(1);adj=(1+(mins[:,None]<=pp).sum(0))/10001;hp=holm(pp)
fam=[];maxerr=0
for j,yname in enumerate(OUTCOMES):
    u=e[3*j:3*j+3];v=cov[3*j:3*j+3,3*j:3*j+3]
    mm=smf.ols(yname+'~C(form)*z',d,eval_env=-1).fit(cov_type='HC3')
    for f in range(3):
        C=np.zeros(len(mm.params));C[list(mm.params.index).index('z')]=1
        if f:C[list(mm.params.index).index(f'C(form)[T.{FORMS[f]}]:z')]=1
        maxerr=max(maxerr,abs(C@mm.params-u[f]),abs(C@mm.cov_params()@C-v[f,f]))
    for k,test in enumerate(['cash','food','medical','omnibus','cash-food','cash-medical']):
        idx=6*j+k;r=dict(sample='A',outcome=yname,test=test,N=5480,df=2 if k==3 else 1,p=pp[idx],holm42=hp[idx],minP42=adj[idx])
        if k!=3:
            C=np.eye(3)[k] if k<3 else np.eye(3)[0]-np.eye(3)[k-3]
            r.update(inf(C@u,np.sqrt(C@v@C),42))
        fam.append(r)
assert maxerr<1e-11;save(fam,'scientific_family42.csv');save([r for r in fam if r['test']!='omnibus'],'family42_simultaneous_intervals.csv')
(O/'family42_covariance.json').write_text(json.dumps(dict(seed=2026100419,draws=10000,covariance=cov.tolist(),estimates=e.tolist(),independent_statsmodels_max_error=maxerr,minimum_eigenvalue=float(val.min())),indent=2))

# Only eight baseline variables in the frozen balance list.
vars=['q42_age','q41_gender','q43_edu','q46_income','q28_hhsize','q24_workstat','q23_hukou','q49_citytier']
sample=[];balance=[]
reader=pd.io.stata.StataReader(a.data,convert_categoricals=False);labels=reader.variable_labels();vl=reader.value_labels()
for name in vars:
    x=d[name];sample.append(dict(variable=name,category='summary',label=labels.get(name,''),N=x.notna().sum(),missing=x.isna().sum(),mean=x.mean(),sd=x.std(),p10=x.quantile(.1),p90=x.quantile(.9)))
    if name=='q42_age':
        m=smf.ols(name+'~C(cell)',d,eval_env=-1).fit(cov_type='HC3');C=np.eye(len(m.params))[1:];r=wald(np.asarray(m.params),np.asarray(m.cov_params()),C);balance.append(dict(variable=name,type='HC3 age omnibus',**r))
    else:
        tab=pd.crosstab(d.cell,x);w,pv,df,exp=stats.chi2_contingency(tab);balance.append(dict(variable=name,type='categorical chi-square diagnostic',wald=w,df=df,p=pv,min_expected=exp.min()))
        # Stata label-set names may differ from variable names; original codes are
        # retained where no safely matched label exists.
        labelset=vl.get(reader._lbllist[reader._varlist.index(name)],{})
        for category,count in x.value_counts(dropna=False).sort_index().items():sample.append(dict(variable=name,category=category,label=labelset.get(category,''),N=count,missing=int(pd.isna(category))))
for r,hp in zip(balance,holm([r['p'] for r in balance])):r['holm8']=hp
save(sample,'sample_characteristics.csv');save(balance,'randomization_balance.csv')
save(d.assign(income_scheme=np.where(d.q46_income>=11,'legacy','current')).groupby('income_scheme').size().rename('N').reset_index(),'income_scheme_counts.csv')
note('CELL_REPRODUCTION_CHECK.md',f'''# Adult reproduction

All54 counts rebuilt independently from the authorized raw file agree exactly
with PR16's adult distribution.csv. Nine Ns sum to5,480. All share×amount yuan
values are computed from these counts, with4,000 fixed-seed multinomial respondent-
equivalent bootstrap draws. Raw records are never exported. Grouped OLS HC3 uses
individual-observation leverage and within-cell outcome dispersion, not nine mean
observations. Family42 grouped estimates/covariances match respondent-row HC3 to
{maxerr:.3g}. Seeds and outcomes are fixed by the plan committed at0aa5681.
''')
note('FAMILY42_RESULT.md','# Family42\n\n'+mdtable(pd.DataFrame(fam)[['outcome','test','p','holm42','minP42']])+'\n\nThe 21 joint form slopes retain cross-outcome dependence. Scalar tests are mapped to normal p values and omnibus tests to chi-square2 before min-P. Asymptotic Gaussian centered-error inference is not exact randomization inference. Original21 results remain archived;42 is a reviewer sensitivity, not retroactive preregistration.')
print(pd.DataFrame(inc+pair)[['form','interval','contrast','estimate','bootstrap_lo','bootstrap_hi','holm6']].to_string(index=False));print(pd.DataFrame(elastic).to_string(index=False));print(pd.DataFrame(comparisons).to_string(index=False));print(pd.DataFrame(fam).query("outcome in ['ordinal','midpoint','top75'] and test in ['cash','omnibus']")[['outcome','test','p','holm42','minP42']].to_string(index=False))
