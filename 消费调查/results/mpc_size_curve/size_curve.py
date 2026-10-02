"""Locked size-curve discovery. Aggregate outputs only; no respondent export."""
from pathlib import Path
import argparse,json,hashlib,warnings
from importlib.metadata import version
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeRegressor,export_text
from sklearn.metrics import mean_squared_error
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
warnings.filterwarnings('ignore',category=FutureWarning)
SEED=20261002
FORMS=['cash','food','medical']; AMT=[200,1000,5000]
SCEN=['q32_cash200','q33_cash1k','q34_cash5k','q35_vouch200','q36_vouch1k','q37_vouch5k','q38_med200','q39_med1k','q40_med5k']
MID=[0,.05,.175,.375,.625,.875]
BASE='C(form)*z'
CONTROLS='q42_age+I(q42_age**2)+C(q41_gender)+C(q43_edu)+C(income)+C(q23_hukou)+C(q24_workstat)+C(q25_unittype)+C(q26_housing)+C(q27_minorchild)+C(q28_hhsize)+C(q29_foodexp)+C(q30_medexp)+C(q31_gotsubsidy)+C(q49_citytier)'
def prepare(path):
 d=pd.read_stata(path,convert_categoricals=False); hit=d[SCEN].notna(); assert hit.sum(axis=1).eq(1).all(); c=hit.to_numpy().argmax(1)
 d['form']=np.array(FORMS)[c//3];d['amount']=np.array(AMT)[c%3];d['z']=c%3-1;d['cell']=c
 d['ordinal']=d[SCEN].bfill(axis=1).iloc[:,0].astype(int);d['midpoint']=d.ordinal.map(dict(enumerate(MID,1)));d['alt_top']=d.ordinal.map(dict(enumerate(MID[:-1]+[1.],1)))
 assert np.array_equal(d.scen_mpc,d.ordinal) and np.array_equal(d.scen_amount,d.amount)
 assert d.ordinal.between(1,6).all() and d.id.is_unique
 assert d.scen_type.map({1:'cash',2:'food',3:'medical'}).eq(d.form).all()
 d['income']=np.where(d.q46_income.between(11,16),d.q46_income-10,d.q46_income)
 items=['q01_lifesat','q02_safety','q03a_fair_dist','q03b_fair_opp','q03c_fair_rule','q04_trust_gov','q05_trust_soc','q06_socsec','q07_emergfund','q08_support','q09_gain','q10_effort','q11_mobility','q12_voice','q13_pressure'];x=d[items]
 d['sample_A']=d.q42_age.between(18,100);d['sample_C']=d.sample_A&x.nunique(axis=1).gt(1)&~d.id.duplicated(False);d['sample_Q1']=d.sample_A&x.std(axis=1).ge(1)&x.nunique(axis=1).ge(4);d['sample_Q2']=d.sample_A&x.std(axis=1).ge(1.5)&x.nunique(axis=1).ge(5)&x.isin([0,10]).mean(axis=1).le(.8)
 for v,n in [('q30_medexp','need'),('q29_foodexp','foodneed'),('q07_emergfund','liquidity'),('income','income_z')]:d[n]=(d[v]-d[v].mean())/d[v].std()
 for j,n in enumerate(['any_spending','ge10','ge25','ge50','top75'],2):d[n]=d.ordinal.ge(j).astype(int)
 return d
def test(m,w):
 v=np.zeros(len(m.params));names=list(m.params.index)
 for k,a in w.items():v[names.index(k)]=a
 t=m.t_test(v);ci=t.conf_int()[0];return [float(np.asarray(t.effect).item()),float(np.asarray(t.sd).item()),*ci,float(np.asarray(t.pvalue).item())]
def slopeweights():
 f='C(form)[T.food]:z';m='C(form)[T.medical]:z'
 return {'cash':{'z':1},'food':{'z':1,f:1},'medical':{'z':1,m:1},'food-cash':{f:1},'medical-cash':{m:1},'medical-food':{m:1,f:-1}}
def slopes(m,meta):
 rows=[[*meta,k,*test(m,w)] for k,w in slopeweights().items()];adj=multipletests([r[-1] for r in rows[:5]],method='holm')[1]
 return [r+[float(adj[i]) if i<5 else np.nan,int(m.nobs)] for i,r in enumerate(rows)]
COLS=['outcome','sample','specification','estimand','slope','se','lo','hi','p','holm_p','N']
def run(data,out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);figs=out/'figures';figs.mkdir(exist_ok=True);d=prepare(data)
 outcomes=['ordinal','midpoint','alt_top','any_spending','ge10','ge25','ge50','top75'];samples={'R':d,'A':d[d.sample_A],'C':d[d.sample_C],'Q1':d[d.sample_Q1],'Q2':d[d.sample_Q2]}
 rows=[]
 for sn,x in samples.items():
  for y in outcomes:
   for sp,form in [('unadjusted',BASE),('adjusted',BASE+'+'+CONTROLS)]:rows+=slopes(smf.ols(y+'~'+form,x).fit(cov_type='HC3'),[y,sn,sp])
 tab=pd.DataFrame(rows,columns=COLS);primary=tab[tab.estimand.isin(FORMS)].copy();primary['form']=primary.estimand;primary.to_csv(out/'primary_amount_slopes.csv',index=False);tab[~tab.estimand.isin(FORMS)].to_csv(out/'differential_slopes.csv',index=False)
 joint=[]
 for y in outcomes[:3]:
  for label,formula in [('structured_2df',BASE),('unrestricted_4df','C(form)*C(amount)')]:
   m=smf.ols(y+'~'+formula,d).fit(cov_type='HC3');terms=[n for n in m.params.index if 'C(form)' in n and ':' in n];r=np.zeros((len(terms),len(m.params)))
   for j,n in enumerate(terms):r[j,list(m.params.index).index(n)]=1
   w=m.wald_test(r,scalar=True);joint.append([y,label,float(w.statistic),len(terms),float(w.pvalue)])
 pd.DataFrame(joint,columns=['outcome','test','wald','df','p']).to_csv(out/'joint_curve_tests.csv',index=False)
 # Ordered models: latent-index slopes are distinct from probability effects.
 ordered=[];X=pd.DataFrame({'z':d.z,'food':d.form.eq('food').astype(float),'medical':d.form.eq('medical').astype(float)});X['food_z']=X.food*X.z;X['medical_z']=X.medical*X.z
 for dist in ['logit','probit']:
  # Generic statsmodels likelihood results silently fall back to HC0 for HC3.
  # Use the score/Hessian sandwich with explicit n/(n-k) HC1 correction instead.
  model=OrderedModel(d.ordinal,X,distr=dist).fit(method='bfgs',disp=False,cov_type='HC0',maxiter=300)
  model._results.cov_params_default *= model.nobs/(model.nobs-len(model.params))
  assert model.mle_retvals['converged'],dist+' failed to converge'
  for k,w in {'cash':{'z':1},'food':{'z':1,'food_z':1},'medical':{'z':1,'medical_z':1},'food-cash':{'food_z':1},'medical-cash':{'medical_z':1},'medical-food':{'medical_z':1,'food_z':-1}}.items():ordered.append([dist,k,*test(model,w)])
 ot=pd.DataFrame(ordered,columns=['model','estimand','slope','se','lo','hi','p']);ot['holm_p']=np.nan
 for dist in ['logit','probit']:
  ix=ot.index[(ot.model==dist)&(ot.estimand!='medical-food')];ot.loc[ix,'holm_p']=multipletests(ot.loc[ix,'p'],method='holm')[1]
 ot['covariance']='score-Hessian sandwich HC1 n/(n-k)';ot['N']=len(d);ot.to_csv(out/'ordered_slopes.csv',index=False)
 cells=[];th=[];decomp=[]
 for (f,a),g in d.groupby(['form','amount']):
  probs=[g.ordinal.eq(k).mean() for k in range(1,7)];cells.append([f,a,len(g),g.ordinal.mean(),g.ordinal.std()/len(g)**.5,g.midpoint.mean(),g.midpoint.std()/len(g)**.5,g.ordinal.median(),probs[0],probs[-1],*probs,*np.cumsum(probs)])
  for y in outcomes[3:]:
   p=g[y].mean();se=(p*(1-p)/len(g))**.5;th.append([f,a,y,len(g),p,se,max(0,p-1.96*se),min(1,p+1.96*se)])
 cs=pd.DataFrame(cells,columns=['form','amount','N','ordinal_mean','ordinal_se','midpoint_mean','midpoint_se','median_category','floor_share','top_share']+[f'p{k}' for k in range(1,7)]+[f'cdf{k}' for k in range(1,7)]);cs.to_csv(out/'cell_summary.csv',index=False)
 tt=pd.DataFrame(th,columns=['form','amount','threshold','N','probability','se','lo','hi']);tt.to_csv(out/'threshold_curves.csv',index=False);tab[tab.outcome.isin(outcomes[3:])].to_csv(out/'threshold_slope_contrasts.csv',index=False)
 for f in FORMS:
  x=cs[cs.form.eq(f)].set_index('amount')
  for k,m in enumerate(MID,1):delta=x.loc[5000,f'p{k}']-x.loc[200,f'p{k}'];decomp.append([f,k,delta,m,delta*m])
 pd.DataFrame(decomp,columns=['form','category','probability_shift_5000_minus_200','midpoint_weight','mean_change_contribution']).to_csv(out/'distribution_decomposition.csv',index=False)
 pair=[]
 for y in outcomes[:3]:
  for f in FORMS:
   x=d[d.form.eq(f)];model=smf.ols(y+'~C(amount)',x).fit(cov_type='HC3')
   for a,b in [(1000,200),(5000,1000),(5000,200)]:w={f'C(amount)[T.{a}]':1};w.update({f'C(amount)[T.{b}]':-1} if b!=200 else {});pair.append([y,f,a,b,*test(model,w)])
 pd.DataFrame(pair,columns=['outcome','form','amount_high','amount_low','change','se','lo','hi','p']).to_csv(out/'pairwise_amount_changes.csv',index=False)
 # Adjacent differential changes using raw independent cell means.
 adj=[]
 for y in outcomes[:3]:
  for t in ['food','medical']:
   for a,b in [(1000,200),(5000,1000),(5000,200)]:
    groups=[d[(d.form==f)&(d.amount==v)][y] for f,v in [(t,a),(t,b),('cash',a),('cash',b)]];eff=sum(s*g.mean() for s,g in zip([1,-1,-1,1],groups));se=sum(g.var()/len(g) for g in groups)**.5;adj.append([y,t+'-cash',a,b,eff,se,eff-1.96*se,eff+1.96*se,2*stats.norm.sf(abs(eff/se))])
 pd.DataFrame(adj,columns=['outcome','contrast','amount_high','amount_low','change','se','lo','hi','p']).to_csv(out/'adjacent_differential_changes.csv',index=False)
 # Food bound sensitivity: common all-amount strict sample additionally prevents amount-dependent composition.
 low=d.q29_foodexp.map({1:0,2:501,3:1001,4:2001,5:3001,6:5001})*6;upper=d.q29_foodexp.map({1:500,2:1000,3:2000,4:3000,5:5000,6:np.inf})*6
 food=[]
 screens={'all':np.ones(len(d),bool),'strict_assigned':low>d.amount,'strict_all_amounts':low>5000,'very_strict_assigned':low>=2*d.amount,'possibly_inframarginal':upper>=d.amount,'likely_binding':upper<d.amount}
 screens.update({name+'_clean':mask&d.sample_C for name,mask in list(screens.items()) if name in ['strict_assigned','strict_all_amounts']})
 for name,mask in screens.items():
  x=d[mask&d.form.isin(['cash','food'])];
  for y in outcomes[:3]:
   if x.groupby(['form','amount']).size().size!=6:continue
   model=smf.ols(y+'~'+BASE,x).fit(cov_type='HC3')
   for k,w in {'food-cash_at_1000':{'C(form)[T.food]':1},'cash_slope':{'z':1},'food_slope':{'z':1,'C(form)[T.food]:z':1},'food-cash_slope':{'C(form)[T.food]:z':1}}.items():food.append([name,y,len(x),k,*test(model,w)])
   saturated=smf.ols(y+'~C(form)*C(amount)',x).fit(cov_type='HC3')
   w={'C(form)[T.food]':1,'C(form)[T.food]:C(amount)[T.1000]':1/3,'C(form)[T.food]:C(amount)[T.5000]':1/3}
   food.append([name,y,len(x),'food-cash_pooled_equal_amount',*test(saturated,w)])
  for a in AMT:
   g=x[x.amount.eq(a)];food.append([name,'cell_N',len(g),str(a),np.nan,np.nan,np.nan,np.nan,np.nan])
 pd.DataFrame(food,columns=['screen','outcome','N','estimand','effect','se','lo','hi','p']).to_csv(out/'food_inframarginal_curve.csv',index=False)
 mechanisms=[]
 for sn,x in {'R':d,'C':d[d.sample_C]}.items():
  for y in outcomes[:2]:
   for t,v in [('food','foodneed'),('medical','need'),('cash','liquidity'),('medical','liquidity'),('food','liquidity'),('medical','income_z'),('food','income_z')]:
    dd=x if t=='cash' else x[x.form.isin(['cash',t])];formula=y+'~z*'+v if t=='cash' else y+'~C(form)*z*'+v
    m=smf.ols(formula,dd).fit(cov_type='HC3')
    terms=['z:'+v] if t=='cash' else [f'C(form)[T.{t}]:{v}',f'C(form)[T.{t}]:z',f'C(form)[T.{t}]:z:{v}']
    for term in terms:mechanisms.append([sn,y,t,v,term,len(dd),*test(m,{term:1})])
 mt=pd.DataFrame(mechanisms,columns=['sample','outcome','form','moderator','term','N','effect','se','lo','hi','p']);mt.to_csv(out/'theory_mechanism_tests.csv',index=False);mt[mt.moderator.eq('need')].to_csv(out/'medical_need_matching_curve.csv',index=False);mt[mt.moderator.isin(['liquidity','income_z'])].to_csv(out/'liquidity_curve_heterogeneity.csv',index=False)
 needcells=[]
 d['need_group']=pd.cut(d.q30_medexp,[0,2,4,6],labels=['low_0_to_500','middle_501_to_5000','high_above_5000'])
 for (ng,f,a),g in d.groupby(['need_group','form','amount'],observed=True):needcells.append([str(ng),f,a,len(g),g.ordinal.mean(),g.ordinal.std()/len(g)**.5,g.midpoint.mean(),g.midpoint.std()/len(g)**.5])
 pd.DataFrame(needcells,columns=['need_group','form','amount','N','ordinal_mean','ordinal_se','midpoint_mean','midpoint_se']).to_csv(out/'medical_need_cell_summary.csv',index=False)
 # Small theory block retains form slopes while allowing need/liquidity effect modification.
 theory=BASE+'+(C(form)*z)*(need+foodneed+liquidity+income_z)+C(q31_gotsubsidy)'
 forms={'M1_additive':'C(form)+z','M2_curves':BASE,'M3_theory':theory};compare=[]
 folds=list(StratifiedKFold(5,shuffle=True,random_state=SEED).split(d,d.cell))
 for y in outcomes[:2]:
  for name,formula in forms.items():
   m=smf.ols(y+'~'+formula,d).fit(cov_type='HC3');pred=np.zeros(len(d))
   for tr,te in folds:pred[te]=smf.ols(y+'~'+formula,d.iloc[tr]).fit().predict(d.iloc[te])
   compare.append([y,name,m.rsquared,m.aic,m.bic,mean_squared_error(d[y],pred),1-sum((d[y]-pred)**2)/sum((d[y]-d[y].mean())**2)])
   if name=='M3_theory':
    pd.DataFrame(slopes(m,[y,'R','theory_block']),columns=COLS).to_csv(out/f'theory_adjusted_slopes_{y}.csv',index=False)
 pd.DataFrame(compare,columns=['outcome','model','in_sample_r2','aic','bic','oof_mse','oof_r2']).to_csv(out/'model_comparison.csv',index=False)
 # Limited shallow tree, same economic covariates, no unrestricted discovery.
 xx=pd.get_dummies(d[['form','z','need','foodneed','liquidity','income_z','q31_gotsubsidy']],columns=['form','q31_gotsubsidy'],dtype=float);ml=[];surfaces=[]
 for seed in [SEED,SEED+1,SEED+2]:
  tree=DecisionTreeRegressor(max_depth=3,min_samples_leaf=150,random_state=seed);pr=np.zeros(len(d));roots=[]
  for tr,te in StratifiedKFold(5,shuffle=True,random_state=seed).split(d,d.cell):tree.fit(xx.iloc[tr],d.midpoint.iloc[tr]);pr[te]=tree.predict(xx.iloc[te]);roots.append(xx.columns[tree.tree_.feature[0]])
  ml.append([seed,mean_squared_error(d.midpoint,pr),';'.join(roots)]);tree.fit(xx,d.midpoint)
  for f in FORMS:
   # Average over covariates is a diagnostic model surface, not causal subgroup selection.
   for a,z in zip(AMT,[-1,0,1]):
    cf=xx.copy();cf['z']=z
    for ff in FORMS:cf['form_'+ff]=float(ff==f)
    surfaces.append([seed,f,a,tree.predict(cf).mean()])
 pd.DataFrame(ml,columns=['seed','oof_mse','outer_fold_root_features']).to_csv(out/'ml_diagnostic.csv',index=False);pd.DataFrame(surfaces,columns=['seed','form','amount','predicted_midpoint']).to_csv(out/'ml_surface.csv',index=False)
 # Conditional permutation exact scheme: global sharp null within each form, not slope-equality null.
 rng=np.random.default_rng(SEED);ri=[]
 for y in ['ordinal','midpoint']:
  obs=smf.ols(y+'~'+BASE,d).fit();observed={k:test(obs,w)[0] for k,w in slopeweights().items()};values={k:[] for k in observed};arrays={f:(g.z.to_numpy(),g[y].to_numpy()) for f,g in d.groupby('form')}
  for b in range(5000):
   slopes_b={}
   for f in FORMS:
    z0,yy=arrays[f];zz=rng.permutation(z0);slopes_b[f]=np.dot(zz-zz.mean(),yy-yy.mean())/sum((zz-zz.mean())**2)
   for k in values:
    val=slopes_b[k] if k in FORMS else slopes_b[k.split('-')[0]]-slopes_b[k.split('-')[1]];values[k].append(val)
  for k in observed:ri.append([y,k,observed[k],(1+sum(abs(np.asarray(values[k]))>=abs(observed[k])))/5001,5000,'Amount labels permuted within form preserving all nine cell counts; sharp null of no amount effect in involved form(s), NOT equal possibly nonzero slopes'])
 rit=pd.DataFrame(ri,columns=['outcome','estimand','slope','permutation_p','B','null']);rit['holm_p']=np.nan
 for y in ['ordinal','midpoint']:
  ix=rit.index[rit.outcome.eq(y)&rit.estimand.ne('medical-food')];rit.loc[ix,'holm_p']=multipletests(rit.loc[ix,'permutation_p'],method='holm')[1]
 rit.to_csv(out/'randomization_inference.csv',index=False)
 figures(cs,tt,tab,pd.DataFrame(needcells,columns=['need_group','form','amount','N','ordinal_mean','ordinal_se','midpoint_mean','midpoint_se']),out)
 (out/'manifest.json').write_text(json.dumps({'seed':SEED,'N':len(d),'sample_N':{k:len(v) for k,v in samples.items()},'data_sha256':hashlib.sha256(Path(data).read_bytes()).hexdigest(),'versions':{p:version(p) for p in ['numpy','pandas','scipy','statsmodels','scikit-learn','matplotlib']},'primary_family':list(slopeweights())[:5],'reuse':['PR3 treatment/outcome/sample definitions','PR8 one observation per respondent identification'],'individual_outputs_written':False,'ordered_models_converged':True},indent=2),encoding='utf-8')
 print(tab[(tab['sample']=='R')&(tab.specification=='unadjusted')&tab.outcome.isin(outcomes[:3])].to_string(index=False))
def figures(cs,tt,tab,nc,out):
 figs=out/'figures'
 for y in ['ordinal','midpoint']:
  fig,ax=plt.subplots(figsize=(7,4))
  for f in FORMS:
   g=cs[cs.form.eq(f)];ax.errorbar(g.amount,g[y+'_mean'],yerr=1.96*g[y+'_se'],marker='o',capsize=3,label=f)
  ax.set(xscale='log',xticks=AMT,xticklabels=['200','1,000','5,000'],xlabel='Transfer amount (RMB)',ylabel='Mean stated response ('+y+')');ax.xaxis.set_minor_locator(NullLocator());ax.legend();fig.tight_layout();fig.savefig(figs/f'fig1_{y}.png',dpi=220);plt.close(fig)
 cs.to_csv(out/'fig1_source.csv',index=False)
 fig,axes=plt.subplots(1,3,figsize=(12,4))
 for ax,f in zip(axes,FORMS):
  g=cs[cs.form.eq(f)];bottom=np.zeros(3)
  for k in range(1,7):ax.bar(range(3),g[f'p{k}'],bottom=bottom,label=str(k));bottom+=g[f'p{k}'].to_numpy()
  ax.set(title=f,xticks=range(3),xticklabels=['200','1000','5000'],ylabel='Response share')
 axes[-1].legend(title='Category',loc='upper left',bbox_to_anchor=(1.02,1),fontsize=8);fig.tight_layout();fig.savefig(figs/'fig2_distribution.png',dpi=220);plt.close(fig);cs.to_csv(out/'fig2_source.csv',index=False)
 fig,axes=plt.subplots(2,3,figsize=(12,7))
 for ax,y in zip(axes.flat,['any_spending','ge10','ge25','ge50','top75']):
  for f in FORMS:
   g=tt[(tt.form==f)&(tt.threshold==y)];ax.errorbar(g.amount,g.probability,yerr=1.96*g.se,marker='o',label=f)
  ax.set(xscale='log',title=y,xticks=AMT,xticklabels=['200','1000','5000'],ylabel='Unconditional probability');ax.xaxis.set_minor_locator(NullLocator());ax.legend(fontsize=8)
 axes.flat[-1].axis('off');fig.tight_layout();fig.savefig(figs/'fig3_thresholds.png',dpi=220);plt.close(fig);tt.to_csv(out/'fig3_source.csv',index=False)
 forest=tab[(tab.outcome.isin(['ordinal','midpoint','alt_top']))&(tab.specification=='unadjusted')];fig,axes=plt.subplots(1,3,figsize=(17,11))
 for ax,y in zip(axes,['ordinal','midpoint','alt_top']):
  g=forest[forest.outcome.eq(y)];ix=np.arange(len(g));ax.errorbar(g.slope,ix,xerr=[g.slope-g.lo,g.hi-g.slope],fmt='o');ax.set(yticks=ix,yticklabels=g['sample']+' '+g.estimand,xlabel='Change per fivefold amount increase',title=y);ax.axvline(0,color='black')
 fig.tight_layout();fig.savefig(figs/'fig4_slopes.png',dpi=220);plt.close(fig);forest.to_csv(out/'fig4_source.csv',index=False)
 food=pd.read_csv(out/'food_inframarginal_curve.csv');fig,axes=plt.subplots(1,3,figsize=(15,5));screens=['all','strict_assigned','strict_all_amounts','strict_all_amounts_clean']
 for ax,est,title in zip(axes[:2],['food-cash_pooled_equal_amount','food-cash_slope'],['Food minus Cash: pooled level','Food minus Cash: amount slope']):
  g=food[(food.outcome=='ordinal')&(food.estimand==est)&food.screen.isin(screens)];ax.errorbar(g.effect,np.arange(len(g)),xerr=1.96*g.se,fmt='o');ax.set(yticks=np.arange(len(g)),yticklabels=g.screen,title=title,xlabel='Ordinal score contrast');ax.axvline(0,color='black')
 gap=nc[nc.form.eq('medical')].merge(nc[nc.form.eq('cash')],on=['need_group','amount'],suffixes=('_medical','_cash'));gap['gap']=gap.ordinal_mean_medical-gap.ordinal_mean_cash;gap['se']=(gap.ordinal_se_medical**2+gap.ordinal_se_cash**2)**.5
 for group in gap.need_group.unique():
  x=gap[gap.need_group.eq(group)];axes[2].errorbar(x.amount,x.gap,yerr=1.96*x.se,marker='o',label=group)
 axes[2].set(xscale='log',title='Medical minus Cash by prior need',xticks=AMT,xticklabels=['200','1000','5000'],ylabel='Ordinal score contrast');axes[2].xaxis.set_minor_locator(NullLocator());axes[2].axhline(0,color='black');axes[2].legend(fontsize=7);fig.tight_layout();fig.savefig(figs/'fig5_mechanisms.png',dpi=220);plt.close(fig);food.to_csv(out/'fig5_food_source.csv',index=False);gap.to_csv(out/'fig5_medical_source.csv',index=False)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('--out',required=True);a=p.parse_args();run(a.data,a.out)
