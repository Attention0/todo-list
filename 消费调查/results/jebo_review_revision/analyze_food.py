import argparse
import statsmodels.formula.api as smf
from common import *
p=argparse.ArgumentParser();p.add_argument('--data',required=True);a=p.parse_args()
d=load(a.data);d=d[d.form.isin(['cash','food'])].copy();assert len(d)==3621
d['G']=(d.food_lower6>5000).astype(int)
def contrast(m,w,k=1):
    v=np.zeros(len(m.params))
    for name,value in w.items():v[list(m.params.index).index(name)]=value
    return inf(v@m.params,np.sqrt(v@m.cov_params()@v),k)
raw=[];sign=[]
for (g,f,t),x in d.groupby(['G','form','amount']):
    row=dict(G=g,form=f,amount=t,N=len(x),ordinal=x.ordinal.mean(),midpoint=x.midpoint.mean(),top75=x.top75.mean(),above_bottom=x.any_spending.mean())
    for k in range(1,7):row['count'+str(k)]=int(x.ordinal.eq(k).sum());row['share'+str(k)]=x.ordinal.eq(k).mean()
    raw.append(row)
m=smf.ols('top75~C(form)*z*G',d,eval_env=-1).fit(cov_type='HC3')
for g in [0,1]:
    weights={'C(form)[T.food]:z':1}
    if g:weights['C(form)[T.food]:z:G']=1
    sign.append(dict(test='Food-Cash slope G='+str(g),N=int(d.G.eq(g).sum()),**contrast(m,weights)))
sign.append(dict(test='G1-G0 Food-Cash slope',N=len(d),**contrast(m,{'C(form)[T.food]:z:G':1})))
hist=pd.read_csv(PRIOR/'mechanism_details.csv')
for i,g in enumerate([0,1]):assert abs(sign[i]['estimate']-hist.loc[hist.test.eq('Food-Cash slope G='+str(g)),'estimate'].iloc[0])<1e-12
save(raw,'food_bindingness_raw_cells.csv');save(sign,'food_bindingness_sign_reproduction.csv')
note('FOOD_BINDINGNESS_SIGN_AUDIT.md','# Food bindingness sign audit\n\nThe frozen prediction was Food−Cash size slope<0 in the more-likely-binding group. Historical +8.00/+1.33pp are reproduced, both positive point estimates. G=0 only fails the six-month expenditure lower-bound>5,000 proxy; it is not observed bindingness. The +8.00pp estimate therefore contradicts the sharp negative-slope prediction, conditional on this imperfect proxy. It does not reject all bindingness models.\n\n'+mdtable(pd.DataFrame(sign)))
coding=[]
for target,source,transform in [('food_band_z','q29_foodexp',False),('income_z','income_M1',True),('household_band_z','q28_hhsize',False)]:
    x=np.log(d[source]) if transform else d[source];d[target]=(x-x.mean())/x.std(ddof=1)
    coding.append(dict(variable=target,source=source,transform='log' if transform else 'ordered response code',mean=x.mean(),sd=x.std(ddof=1),p10=d[target].quantile(.1),p90=d[target].quantile(.9),N=len(d)))
save(coding,'food_bindingness_moderator_coding.csv')
rows=[];coef=[]
for y in ['top75','midpoint','ordinal']:
    for adjusted in [False,True]:
        formula=y+'~C(form)*z*'+('(food_band_z+income_z+household_band_z)' if adjusted else 'food_band_z')
        m=smf.ols(formula,d,eval_env=-1).fit(cov_type='HC3')
        focal='C(form)[T.food]:z:food_band_z';r=contrast(m,{focal:1},6)
        rows.append(dict(outcome=y,adjusted=adjusted,N=len(d),estimand='Food-Cash fivefold slope moderation per1SD ordered food band',**r))
        for term in m.params.index:coef.append(dict(outcome=y,adjusted=adjusted,term=term,**inf(m.params[term],m.bse[term])))
for r,h in zip(rows,holm([r['p'] for r in rows])):r['holm6']=h
save([r for r in rows if not r['adjusted']],'food_bindingness_continuous.csv');save([r for r in rows if r['adjusted']],'food_bindingness_adjusted.csv');save(coef,'food_bindingness_coefficients.csv')
ratio=[];rc=[]
for mapping,values in [('M1',[250,750.5,1500.5,2500.5,4000.5,7500]),('M2',[125,750.5,1500.5,2500.5,4000.5,10000])]:
    d['lf']=np.log(6*d.q29_foodexp.map(dict(enumerate(values,1))));d['la']=np.log(d.amount);d['lr']=d.la-d.lf
    for y in ['top75','midpoint','ordinal']:
        m=smf.ols(y+'~C(form)*(la+lf)',d,eval_env=-1).fit(cov_type='HC3');r=smf.ols(y+'~C(form)*lr',d,eval_env=-1).fit(cov_type='HC3')
        C=np.zeros((2,len(m.params)))
        for j,terms in enumerate([['la','lf'],['C(form)[T.food]:la','C(form)[T.food]:lf']]):
            for name in terms:C[j,list(m.params.index).index(name)]=1
        result=wald(np.asarray(m.params),np.asarray(m.cov_params()),C)
        ratio.append(dict(mapping=mapping,outcome=y,N=len(d),**result,unrestricted_R2=m.rsquared,ratio_R2=r.rsquared,R2_loss=m.rsquared-r.rsquared,unrestricted_SSE=float(sum(m.resid**2)),ratio_SSE=float(sum(r.resid**2)),interaction_only1df_p=wald(np.asarray(m.params),np.asarray(m.cov_params()),C[1:])['p']))
        for name in ['la','lf','C(form)[T.food]:la','C(form)[T.food]:lf']:rc.append(dict(mapping=mapping,outcome=y,term=name,**inf(m.params[name],m.bse[name])))
for r,h in zip(ratio,holm([r['p'] for r in ratio])):r['holm6']=h
save(ratio,'food_bindingness_ratio.csv');save(rc,'food_bindingness_ratio_coefficients.csv')
note('FOOD_BINDINGNESS_RESULT.md','# Food expenditure, prediction and precision\n\n'+mdtable(pd.DataFrame(rows)[['outcome','adjusted','estimate','lo','hi','p','holm6']])+'\n\nRatio restrictions, now correctly testing BOTH common and form-dependent coefficients (2df):\n\n'+mdtable(pd.DataFrame(ratio)[['mapping','outcome','p','holm6','R2_loss','interaction_only1df_p']])+'\n\nThe sharp simple increasing-bindingness sign is contradicted in the historical G=0 proxy subgroup. Positive descriptive Food−Cash gradients cannot be relabelled as predicted. Continuous and adjusted tests describe observational moderation, not randomized expenditure or a mediated causal effect. Failure to reject a ratio restriction is not evidence that a ratio governs responses; all confidence intervals and model fit losses are retained. Food-band proxies are not exact expenditure and open-ended mappings are sensitivity assumptions. No additional moderators or outcomes were searched.')
print(pd.DataFrame(rows)[['outcome','adjusted','estimate','lo','hi','p','holm6']].to_string(index=False));print(pd.DataFrame(ratio)[['mapping','outcome','p','holm6','R2_loss']].to_string(index=False))
