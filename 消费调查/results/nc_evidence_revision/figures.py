from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
O=Path(__file__).resolve().parent
F=O.parent.parent/'manuscript'/'nc_v5'/'figures';F.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'Arial','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'black','text.color':'black','pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})
forms=['cash','food','medical'];colors=['#111111','#407c9e','#94aebd'];markers=['o','s','^'];amounts=[200,1000,5000]
def finish(fig,name):
    for ext in ['png','pdf','svg']:fig.savefig(F/(name+'.'+ext),dpi=300,bbox_inches='tight')
    plt.close(fig)
def subset(file,**kw):
    d=pd.read_csv(O/file)
    for k,v in kw.items():d=d[d[k]==v]
    return d
d=subset('distribution.csv',sample='A');p=subset('profiles.csv',sample='A')
fig,ax=plt.subplots(1,2,figsize=(9,4.8),gridspec_kw={'width_ratios':[1.55,1]},layout='constrained')
palette=plt.cm.Blues(np.linspace(.18,.95,6));labs=['No increase','<10%','10–25%','25–50%','50–75%','>75%']
for f,form in enumerate(forms):
    for j,amt in enumerate(amounts):
        y=8-(f*3+j);g=d[(d.form==form)&(d.amount==amt)].sort_values('category');left=0
        for k,r in enumerate(g.itertuples()):ax[0].barh(y,r.share,left=left,color=palette[k],height=.76,edgecolor='white',linewidth=.5,label=labs[k] if y==8 else None);left+=r.share
ax[0].set_yticks(range(9),[f'{f.title()}  {a:,}' for f in forms for a in amounts][::-1]);ax[0].xaxis.set_major_formatter(PercentFormatter(1));ax[0].set_xlim(0,1);ax[0].set_xlabel('Share of respondents');ax[0].set_title('a  Complete response distributions',loc='left',pad=12)
ax[0].legend(ncol=3,loc='upper center',bbox_to_anchor=(.48,-.15),frameon=False,fontsize=8.5,handlelength=1.5,columnspacing=1)
for f,form in enumerate(forms):
    g=p[(p.form==form)&(p.outcome=='midpoint')].sort_values('amount');ax[1].errorbar(range(3),g.estimate*100,yerr=g.se*196,marker=markers[f],color=colors[f],capsize=3,label=form.title())
ax[1].set_xticks(range(3),['200','1,000','5,000']);ax[1].set_xlabel('Transfer amount (RMB)');ax[1].set_ylabel('Midpoint-coded stated share (%)');ax[1].set_ylim(10,28);ax[1].set_title('b  Descriptive average',loc='left',pad=12);ax[1].legend(frameon=False,loc='upper right',fontsize=9)
finish(fig,'fig1_distributions')
fig,ax=plt.subplots(1,2,figsize=(9,4.2),layout='constrained')
for f,form in enumerate(forms):
    g=p[(p.form==form)&(p.outcome=='top75')].sort_values('amount');ax[0].errorbar(np.arange(3)+(f-1)*.04,g.estimate*100,yerr=g.se*196,color=colors[f],marker=markers[f],capsize=3,label=form.title())
ax[0].set_xticks(range(3),['200','1,000','5,000']);ax[0].set_xlabel('Transfer amount (RMB)');ax[0].set_ylabel('Highest-category response (%)');ax[0].set_ylim(0,18);ax[0].set_title('a  High stated spending',loc='left',pad=12);ax[0].legend(frameon=False,fontsize=9)
c=subset('form_contrasts.csv',sample='A')
for f,form in enumerate(['food','medical']):
    g=c[c.test==form+'-cash'].sort_values('amount');x=np.arange(3)+(f-.5)*.12
    ax[1].errorbar(x,g.estimate*100,yerr=np.vstack([(g.estimate-g.sim_lo)*100,(g.sim_hi-g.estimate)*100]),fmt='none',color=colors[f+1],alpha=.45,lw=1,capsize=3)
    ax[1].errorbar(x,g.estimate*100,yerr=g.se*196,color=colors[f+1],marker=markers[f+1],lw=2,capsize=0,label=form.title()+' − Cash')
ax[1].axhline(0,color='.45',ls=':',lw=1);ax[1].set_xticks(range(3),['200','1,000','5,000']);ax[1].set_xlabel('Transfer amount (RMB)');ax[1].set_ylabel('Difference (percentage points)');ax[1].set_title('b  Form contrasts at each amount',loc='left',pad=12);ax[1].legend(frameon=False,loc='lower right',fontsize=9)
finish(fig,'fig2_tail')
q=pd.read_csv(O.parent/'nc_revision_audit'/'quality_gradient_source.csv');q=q[q.contrast.isin(['cash-food','cash-medical'])];q.to_csv(O/'figure3a_source.csv',index=False)
b=pd.read_csv(O/'mechanism_details.csv');b=b[b.test.str.startswith('Food-Cash slope')]
fig,ax=plt.subplots(1,2,figsize=(9,4.3),gridspec_kw={'width_ratios':[1.35,1]},layout='constrained')
for j,cname in enumerate(['cash-food','cash-medical']):
    g=q[q.contrast==cname].set_index('sample').loc[['R','A','C','Q1','Q2']]
    ax[0].errorbar(-g.estimate*100,np.arange(5)+(j-.5)*.15,xerr=g.se*196,fmt=markers[j+1],color=colors[j+1],capsize=3,label=cname.split('-')[1].title()+' − Cash')
ax[0].set_yticks(range(5),['Full  n=5,497','Adult  n=5,480','Constant-response excluded  n=5,171','Q1  n=2,715','Q2  n=1,208'],fontsize=8);ax[0].invert_yaxis();ax[0].axvline(0,color='.5',ls=':');ax[0].set_xlabel('Slope difference (pp per fivefold increase)');ax[0].set_title('a  Sample sensitivity',loc='left',pad=12);ax[0].legend(frameon=False,loc='upper center',bbox_to_anchor=(.45,-.17),ncol=2,fontsize=8.5)
ax[1].errorbar(b.estimate*100,[0,1],xerr=b.se*196,fmt='o',color='#315f79',capsize=3);ax[1].set_yticks([0,1],['Not confirmed\nn=815','Conservatively classified\nn=2,806'],fontsize=8);ax[1].invert_yaxis();ax[1].axvline(0,color='.5',ls=':');ax[1].set_xlabel('Food − Cash slope difference\n(pp per fivefold increase)');ax[1].set_title('b  Food expenditure classification',loc='left',pad=12)
finish(fig,'fig3_sensitivity')
# Same probability estimand across specifications. Saturated endpoint is profile[1].
grid=pd.read_csv(O/'legacy_family_comparison.csv');s=grid[(grid.outcome=='top75')&(grid.model=='OLS_HC3')&grid.contrast.isin(['cash-food','cash-medical'])].copy();rows=[]
for r in s.itertuples():
    v=json.loads(r.profile);lo=json.loads(r.profile_lo);hi=json.loads(r.profile_hi);i=1 if r.representation=='saturated' else 0;k=2 if r.representation=='trend' else 1
    rows.append(dict(sample=r.sample,representation=r.representation,contrast=r.contrast,estimate=-v[i]*k,lo=-hi[i]*k,hi=-lo[i]*k,N=r.N))
s=pd.DataFrame(rows);s.to_csv(O/'spec_curve_source.csv',index=False)
fig,ax=plt.subplots(1,2,figsize=(9,7),sharey=True,layout='constrained')
order=[(sam,rep) for sam in ['R','A','C','Q1','Q2'] for rep in ['trend','saturated','endpoint']]
for j,con in enumerate(['cash-food','cash-medical']):
    g=s[s.contrast==con].set_index(['sample','representation']).loc[order];y=np.arange(15)
    ax[j].errorbar(g.estimate*100,y,xerr=np.vstack([(g.estimate-g.lo)*100,(g.hi-g.estimate)*100]),fmt=markers[j+1],color=colors[j+1],capsize=2)
    ax[j].axvline(0,color='.5',ls=':');ax[j].set_title(con.split('-')[1].title()+' − Cash',loc='left');ax[j].set_xlabel('200 to 5,000 difference in differences (pp)');ax[j].set_yticks(y,[f'{sa}  {re}' for sa,re in order],fontsize=9)
ax[0].invert_yaxis();finish(fig,'figS1_specifications')
c=pd.read_csv(O/'calibration_effects.csv');fig,ax=plt.subplots(figsize=(7,3.8),layout='constrained')
for j,co in enumerate(['cash-food','cash-medical']):
    g=c[c.test==co];ax.errorbar(-g.estimate*100,np.arange(3)+(j-.5)*.15,xerr=g.se*196,fmt=markers[j+1],color=colors[j+1],capsize=3,label=co.split('-')[1].title()+' − Cash')
ax.set_yticks(range(3),['Unweighted  ESS=5,480','Joint calibration  ESS=315','Normalized weights ≤10  ESS=1,191']);ax.invert_yaxis();ax.axvline(0,color='.5',ls=':');ax.set_xlabel('Slope difference (pp per fivefold increase)');ax.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.5,-.23));finish(fig,'figS2_calibration')
print('3 main and 2 supplementary figures generated')
