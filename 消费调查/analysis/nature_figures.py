"""Nature-series six main and ten Extended Data figures from aggregate tables only."""
from argparse import ArgumentParser
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.ticker import PercentFormatter

COL={'cash':'#30343B','food':'#2B7A91','medical':'#C46B38'}
MARK={'cash':'o','food':'s','medical':'D'}
FORMS=['cash','food','medical']
AMOUNTS=[200,1000,5000]
FS=['T','O','S','A','O+S','O+A','ALL']
MM=1/25.4

def load(root,name):return pd.read_csv(root/'tables'/name)
def source(root,name,tab):tab.to_csv(root/'tables'/f'{name}_data.csv',index=False)
def style():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'axes.labelsize':7,'axes.titlesize':8,'xtick.labelsize':6.5,'ytick.labelsize':6.5,'legend.fontsize':6.5,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white','figure.facecolor':'white'})
def panel(ax,label,title=None):
    ax.text(-.10,1.06,label,transform=ax.transAxes,fontweight='bold',fontsize=9,va='top')
    if title:ax.set_title(title,loc='left',pad=7,fontweight='semibold')
def save(fig,out,name):
    fig.savefig(out/f'{name}.pdf',bbox_inches='tight',facecolor='white')
    fig.savefig(out/f'{name}.png',dpi=600,bbox_inches='tight',facecolor='white')
    plt.close(fig)
def err(ax,x,y,lo,hi,**kw):ax.errorbar(x,y,yerr=[np.asarray(y)-np.asarray(lo),np.asarray(hi)-np.asarray(y)],capsize=2,lw=1.1,**kw)

def fig1(root,out):
    cells=load(root,'nature_design_cells.csv');dist=load(root,'nature_outcome_distributions.csv');fx=load(root,'nature_average_effects.csv')
    source(root,'nature_fig1a',cells);source(root,'nature_fig1b',dist[dist.scope.eq('form')]);source(root,'nature_fig1c',pd.concat([cells.assign(panel='cell_means'),fx[(fx['sample']=='R')&(fx.outcome=='outcome_ord')&(fx.amount.astype(str)=='pooled')].assign(panel='pooled_contrasts')],ignore_index=True))
    fig=plt.figure(figsize=(183*MM,140*MM));gs=fig.add_gridspec(2,2,height_ratios=[1,1.1],wspace=.34,hspace=.56)
    a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[0,1]);c=fig.add_subplot(gs[1,:])
    panel(a,'a','Randomized 3 × 3 design');a.set_xlim(0,3);a.set_ylim(0,3)
    for i,t in enumerate(FORMS):
        for j,v in enumerate(AMOUNTS):
            n=int(cells[(cells.transfer_type==t)&(cells.amount==v)].N.iloc[0]);a.add_patch(Rectangle((j,2-i),1,1,facecolor=COL[t],alpha=.12,edgecolor='white'))
            a.text(j+.5,2.5-i,f'n = {n}',ha='center',va='center',fontsize=7)
    a.set_xticks([.5,1.5,2.5],['RMB 200','RMB 1,000','RMB 5,000']);a.xaxis.tick_top();a.set_yticks([2.5,1.5,.5],['Cash','Food voucher','Medical account']);a.tick_params(length=0)
    a.text(.5,-.16,'Six stated additional-consumption categories',transform=a.transAxes,ha='center',fontsize=6.5)
    panel(b,'b','Full stated-response distribution');form=dist[dist.scope.eq('form')];catcol=['#E8EEF1','#C4D7DD','#97BCC7','#69A0B2','#3D7B91','#17495B']
    for i,t in enumerate(FORMS):
        g=form[form.form.eq(t)].sort_values('category');left=0
        for _,r in g.iterrows():b.barh(i,r.share,left=left,height=.55,color=catcol[int(r.category)-1],edgecolor='white',linewidth=.5);left+=r.share
        b.text(1.01,i,f'N={int(g.N.iloc[0]):,}',va='center',fontsize=6.5)
    b.set_yticks(range(3),['Cash','Food','Medical']);b.invert_yaxis();b.set_xlim(0,1.2);b.set_xticks([0,.25,.5,.75,1]);b.xaxis.set_major_formatter(PercentFormatter(1));b.set_xlabel('Share of respondents');
    handles=[Rectangle((0,0),1,1,color=z) for z in catcol];b.legend(handles,['None','<10%','10–25%','25–50%','50–75%','>75%'],ncol=3,loc='lower center',bbox_to_anchor=(.5,-.45),frameon=False)
    panel(c,'c','Mean stated-response category by form and amount')
    for t in FORMS:
        g=cells[cells.transfer_type.eq(t)].sort_values('amount');y=g.ordinal_mean.to_numpy();se=g.ordinal_sd.to_numpy()/np.sqrt(g.N.to_numpy())
        err(c,range(3),y,y-1.96*se,y+1.96*se,color=COL[t],marker=MARK[t],label=t.title())
    c.set_xticks(range(3),['RMB 200','RMB 1,000','RMB 5,000']);c.set_ylabel('Mean response category (1–6)');c.legend(frameon=False,ncol=3,loc='upper right')
    q=fx[(fx['sample']=='R')&(fx.outcome=='outcome_ord')&(fx.amount.astype(str)=='pooled')]
    label='  '.join(f'{r.contrast}: {r.effect:+.2f} [{r.lo:+.2f}, {r.hi:+.2f}]' for _,r in q[q.contrast.isin(['food-cash','medical-cash'])].iterrows())
    c.text(.5,-.31,'Pooled ordinal contrasts (95% CI): '+label,transform=c.transAxes,ha='center',fontsize=6.5)
    fig.subplots_adjust(bottom=.14);save(fig,out,'nature_fig1')

def fig2(root,out):
    cv=load(root,'nature_level_cv_summary.csv');inc=load(root,'nature_level_increment.csv');ld=load(root,'nature_latent_diagnostics.csv');li=load(root,'nature_latent_increment.csv')
    source(root,'nature_fig2a',cv[cv.model.eq('rf')]);source(root,'nature_fig2b',inc[inc.model.eq('rf')]);source(root,'nature_fig2c',pd.concat([ld.assign(kind='factor'),li.assign(kind='heldout')],ignore_index=True))
    fig=plt.figure(figsize=(183*MM,135*MM));gs=fig.add_gridspec(2,2,height_ratios=[1,.8],wspace=.4,hspace=.55)
    a=fig.add_subplot(gs[0,:]);b=fig.add_subplot(gs[1,0]);c=fig.add_subplot(gs[1,1]);panel(a,'a','Out-of-sample prediction from locked information sets')
    z=cv[cv.model.eq('rf')].set_index('feature_set').loc[FS].reset_index();err(a,np.arange(7),z.r2,z.lo,z.hi,fmt='o',color='#30343B');a.axhline(0,color='#777777',lw=.7)
    a.set_xticks(range(7),FS);a.set_ylabel('Repeated-CV out-of-sample R²');a.set_ylim(min(-.02,z.lo.min()-.008),max(.075,z.hi.max()+.006))
    for j in [1,6]:a.annotate(f'{z.r2.iloc[j]*100:.1f}%',(j,z.r2.iloc[j]),xytext=(4,4),textcoords='offset points',fontsize=6)
    panel(b,'b','Increment from subjective information');z=inc[inc.model.eq('rf')].set_index('expanded').loc[['O+S','O+A','ALL']]
    err(b,z.delta_r2,np.arange(3),z.lo,z.hi,fmt='o',color='#30343B') if False else None
    for i,(_,r) in enumerate(z.iterrows()):b.errorbar(r.delta_r2,i,xerr=[[r.delta_r2-r.lo],[r.hi-r.delta_r2]],fmt='o',color='#30343B',capsize=2)
    b.axvline(0,color='#777777',lw=.7);b.axvline(.01,color='#B16C3D',lw=.8,ls='--');b.axvline(.02,color='#B16C3D',lw=.8,ls=':');b.set_yticks(range(3),['O + S','O + A','ALL']);b.invert_yaxis();b.set_xlabel('Δ out-of-sample R² versus O');b.text(.01,2.8,'+0.01 / +0.02 practical-gain benchmarks',fontsize=5.5,color='#8A5030')
    panel(c,'c','Coherent subjective dimensions');r=li.iloc[0];c.scatter([0,1],[r.O_r2,r.O_plus_latent_r2],color=['#30343B','#2B7A91'],s=25);c.plot([0,1],[r.O_r2,r.O_plus_latent_r2],color='#888888',lw=.8)
    c.set_xticks([0,1],['Objective / needs','+ latent states']);c.set_ylabel('Held-out R²');c.set_ylim(0,max(.05,r.O_plus_latent_r2+.014));c.text(.5,.83,f'Δ R² = {r.increment:+.3f}',transform=c.transAxes,ha='center',fontsize=7)
    c.text(.5,.72,'Three domain PCs; α = '+', '.join(f'{v:.2f}' for v in ld.cronbach_alpha),transform=c.transAxes,ha='center',fontsize=5.5)
    save(fig,out,'nature_fig2')

def fig3(root,out):
    cf=load(root,'nature_cross_form.csv');sim=load(root,'nature_predictor_similarity.csv');diff=load(root,'nature_portability_differences.csv');rel=load(root,'nature_reliability_sensitivity.csv')
    source(root,'nature_fig3a',cf);source(root,'nature_fig3b',pd.concat([sim.assign(kind='similarity'),diff.assign(kind='difference')],ignore_index=True));source(root,'nature_fig3c',rel)
    fig=plt.figure(figsize=(183*MM,140*MM));gs=fig.add_gridspec(2,2,wspace=.38,hspace=.55);a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[0,1]);c=fig.add_subplot(gs[1,:])
    panel(a,'a','Cross-form rank portability');mat=np.full((3,3),np.nan)
    for _,r in cf.iterrows():mat[FORMS.index(r.source),FORMS.index(r.target)]=r.spearman
    im=a.imshow(np.ma.masked_invalid(mat),vmin=0,vmax=.4,cmap='Blues');a.set_xticks(range(3),[x.title() for x in FORMS]);a.set_yticks(range(3),[x.title() for x in FORMS]);a.set_xlabel('Target form');a.set_ylabel('Source form')
    for i in range(3):
        for j in range(3):
            if i!=j:a.text(j,i,f'{mat[i,j]:.2f}',ha='center',va='center',fontsize=7,color='#122C38')
    fig.colorbar(im,ax=a,fraction=.045,pad=.03,label='Spearman ρ')
    panel(b,'b','Predictor-map similarity');pairs=[('cash','food'),('cash','medical'),('food','medical')]
    for shift,fs,mark,col in [(-.08,'O_needs','o','#30343B'),(.08,'ALL','s','#2B7A91')]:
        z=sim[sim.feature_set.eq(fs)]
        for i,p in enumerate(pairs):
            r=z[(z.form1==p[0])&(z.form2==p[1])].iloc[0]
            b.plot(i+shift,r.coef_correlation,mark,color=col,label=fs if i==0 else None)
            b.vlines(i+shift,r.corr_lo,r.corr_hi,color=col,lw=1.1)
            b.hlines([r.corr_lo,r.corr_hi],i+shift-.025,i+shift+.025,color=col,lw=1.1)
    b.axhline(0,color='#777777',lw=.7);b.set_xticks(range(3),['Cash–Food','Cash–Medical','Food–Medical'],rotation=16);b.set_ylabel('Ridge coefficient correlation');b.legend(frameon=False)
    q=diff[(diff.metric=='coef_correlation_ALL')&(diff.comparison=='CF_minus_CM')].iloc[0]
    b.text(.5,.95,f'Cash–Food minus Cash–Medical = {q.difference:.2f}\n95% CI [{q.lo:.2f}, {q.hi:.2f}]',transform=b.transAxes,ha='center',va='top',fontsize=5.7)
    panel(c,'c','Reliability sensitivity (assumed, not estimated)')
    for (src,tgt),g in rel.groupby(['source','target']):
        if (src,tgt) not in [('cash','food'),('cash','medical'),('food','medical')]:continue
        c.plot(g.assumed_reliability,g.sensitivity_adjusted,marker=MARK[tgt],color=COL[tgt],label=f'{src.title()} → {tgt.title()}')
    for y in [.25,.5,.75]:c.axhline(y,color='#CCCCCC',lw=.5)
    c.set_xticks([.4,.6,.8]);c.set_xlabel('Assumed reliability in each form');c.set_ylabel('Sensitivity-adjusted rank correlation');c.set_ylim(0,1);c.legend(frameon=False,ncol=3,loc='upper right')
    save(fig,out,'nature_fig3')

def fig4(root,out):
    q=load(root,'nature_hte_quintiles.csv');h=load(root,'nature_hte_primary.csv');dif=load(root,'nature_hte_asymmetry.csv')
    for name,contrast in [('nature_fig4a','food-cash'),('nature_fig4b','medical-cash')]:source(root,name,q[(q.method=='dr')&(q.contrast==contrast)])
    source(root,'nature_fig4c',pd.concat([h.assign(kind='individual'),dif.assign(kind='difference')],ignore_index=True))
    fig=plt.figure(figsize=(183*MM,140*MM));gs=fig.add_gridspec(2,2,hspace=.56,wspace=.30);a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[0,1],sharey=a)
    for ax,contrast,label,title,col in [(a,'food-cash','a','Food − Cash',COL['food']),(b,'medical-cash','b','Medical − Cash',COL['medical'])]:
        panel(ax,label,title);z=q[(q.method=='dr')&(q.contrast==contrast)].sort_values('quintile')
        err(ax,z.quintile,z.effect,z.lo,z.hi,fmt='o-',color=col);ax.axhline(0,color='#777777',lw=.7);ax.set_xticks(range(1,6));ax.set_xlabel('OOF predicted-effect quintile');ax.set_ylabel('Observed midpoint contrast')
    a.set_ylim(-.18,.12);b.set_ylim(-.18,.12)
    lower=gs[1,:].subgridspec(1,2,wspace=.4);c1=fig.add_subplot(lower[0,0]);c2=fig.add_subplot(lower[0,1])
    panel(c1,'c','Formal asymmetry: calibration');c2.set_title('Top–bottom separation',loc='left',pad=7,fontweight='bold')
    z=dif[dif.method.eq('dr')].set_index('metric').loc[['calibration','top_bottom']]
    for ax,metric in [(c1,'calibration'),(c2,'top_bottom')]:
        r=z.loc[metric];ax.errorbar(r.medical_minus_food,0,xerr=[[r.medical_minus_food-r.lo],[r.hi-r.medical_minus_food]],fmt='o',color='#30343B',capsize=2)
        ax.axvline(0,color='#777777',lw=.7);ax.set_yticks([]);ax.set_xlabel('Medical − Food difference\n(95% stratified-bootstrap CI)')
    c1.set_xlim(-.1,1.4);c2.set_xlim(-.02,.16)
    save(fig,out,'nature_fig4')

def fig5(root,out):
    amount=load(root,'nature_amount_hte.csv');bins=load(root,'nature_moderators_binned.csv')
    source(root,'nature_fig5a',amount[amount.contrast.eq('medical-cash')]);source(root,'nature_fig5b',bins[(bins.variable=='income_h')&(bins.contrast=='medical-food')]);source(root,'nature_fig5c',bins[(bins.variable=='q30_medexp')&(bins.contrast=='medical-food')])
    fig=plt.figure(figsize=(183*MM,140*MM));gs=fig.add_gridspec(2,2,wspace=.32,hspace=.55);a=fig.add_subplot(gs[0,:]);b=fig.add_subplot(gs[1,0]);c=fig.add_subplot(gs[1,1])
    panel(a,'a','Medical − Cash heterogeneity by transfer size')
    for shift,method,col,mark in [(-.07,'t',COL['medical'],'o'),(.07,'dr',COL['food'],'s')]:
        z=amount[(amount.contrast=='medical-cash')&(amount.method==method)].sort_values('amount')
        err(a,np.arange(3)+shift,z.calibration,z.cal_lo,z.cal_hi,fmt=mark+'-',color=col,label=method.upper())
    a.axhline(0,color='#777777',lw=.7);a.set_xticks(range(3),['RMB 200','RMB 1,000','RMB 5,000']);a.set_ylabel('OOF calibration slope');a.legend(frameon=False,ncol=2)
    for ax,variable,label,title in [(b,'income_h','b','Household income'),(c,'q30_medexp','c','Past-year medical spending')]:
        panel(ax,label,title);z=bins[(bins.variable==variable)&(bins.contrast=='medical-food')].sort_values('level')
        err(ax,z.level,z.effect,z.lo,z.hi,fmt='o-',color=COL['medical']);ax.axhline(0,color='#777777',lw=.7);ax.set_ylabel('Observed ordinal Medical − Food contrast')
        if variable=='income_h':ax.set_xlabel('Income band (low → high)');ax.set_xticks(z.level)
        else:
            ax.set_xticks(z.level,['0','1–500','501–2k','2–5k','5–20k','>20k'][:len(z)])
            ax.set_xlabel('Medical spending (RMB)')
    save(fig,out,'nature_fig5')

def fig6(root,out):
    p=load(root,'nature_policy_value.csv');source(root,'nature_fig6a',p);source(root,'nature_fig6b',p[p.policy.isin(['depth2_tree','ml_argmax'])])
    fig=plt.figure(figsize=(160*MM,105*MM));gs=fig.add_gridspec(2,1,height_ratios=[1.4,.6],hspace=.58);a=fig.add_subplot(gs[0]);b=fig.add_subplot(gs[1])
    panel(a,'a','Honest policy value for stated consumption');z=p[p.estimator.eq('DR')].set_index('policy').loc[['all_cash','all_food','all_medical','depth2_tree','ml_argmax']].reset_index()
    err(a,range(len(z)),z.value,z.lo,z.hi,fmt='o',color='#30343B');a.axhline(z.iloc[0].value,color=COL['cash'],lw=.9,ls='--');a.set_xticks(range(5),['All Cash','All Food','All Medical','Depth-2 tree','ML argmax'],rotation=12);a.set_ylabel('DR policy value (midpoint stated MPC)')
    a.set_xlim(-.3,5.8);a.set_ylim(.15,.282)
    for i,y in [(3,.274),(4,.244)]:
        r=z.iloc[i];name='Tree' if i==3 else 'ML'
        a.text(4.65,y,f'{name} Δ {r.gain_vs_cash:+.3f}\n[{r.gain_lo:+.3f}, {r.gain_hi:+.3f}]',fontsize=5.3,ha='left',va='top')
    panel(b,'b','Form allocation under personalized policies');z=p[(p.estimator=='DR')&p.policy.isin(['depth2_tree','ml_argmax'])].set_index('policy').loc[['depth2_tree','ml_argmax']]
    left=np.zeros(2)
    for t in FORMS:
        values=z['share_'+t].to_numpy();b.barh(range(2),values,left=left,color=COL[t],label=t.title(),height=.45);left+=values
    b.set_yticks(range(2),['Depth-2 tree','ML argmax']);b.invert_yaxis();b.set_xlim(0,1);b.xaxis.set_major_formatter(PercentFormatter(1));b.set_xlabel('Share assigned');b.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,-.75))
    save(fig,out,'nature_fig6')

def extended(root,out):
    dist=load(root,'nature_outcome_distributions.csv');fx=load(root,'nature_average_effects.csv');cv=load(root,'nature_level_cv_summary.csv');orep=load(root,'nature_outcome_sensitivity.csv');ld=load(root,'nature_latent_diagnostics.csv');cf=load(root,'nature_cross_form.csv');sim=load(root,'nature_predictor_similarity.csv');h=load(root,'nature_hte_primary.csv');seed=load(root,'nature_hte_seeds.csv');q=load(root,'nature_quality_composition.csv');qe=load(root,'nature_average_effects.csv');qm=load(root,'nature_moderators.csv')
    # ED1: nine-cell category shares
    z=dist[dist.scope.eq('cell')];source(root,'nature_ed_fig1',z);fig,axs=plt.subplots(3,3,figsize=(183*MM,130*MM),sharex=True,sharey=True)
    for i,t in enumerate(FORMS):
        for j,v in enumerate(AMOUNTS):
            g=z[(z.form==t)&(z.amount.astype(str)==str(v))].sort_values('category');axs[i,j].bar(g.category,g.share,color=COL[t],alpha=.8);axs[i,j].set_title(f'{t.title()}, RMB {v:,}; N={int(g.N.iloc[0])}',fontsize=7);axs[i,j].set_ylim(0,.42)
    fig.supxlabel('Stated response category (1–6)',fontsize=7);fig.supylabel('Share',fontsize=7);fig.tight_layout();save(fig,out,'nature_ed_fig1')
    # ED2: coding sensitivity
    z=fx[(fx['sample']=='R')&(fx.amount.astype(str)=='pooled')&fx.contrast.isin(['food-cash','medical-cash'])];source(root,'nature_ed_fig2',z);fig,ax=plt.subplots(figsize=(150*MM,85*MM))
    outcomes=['outcome_ord','mpc_midpoint','mpc_alt','any_spend','mpc_10plus','mpc_25plus','mpc_50plus']
    for t,shift in [('food-cash',-.1),('medical-cash',.1)]:
        zz=z[z.contrast==t].set_index('outcome').loc[outcomes]
        for i,(_,r) in enumerate(zz.iterrows()):ax.errorbar(r.effect,i+shift,xerr=[[r.effect-r.lo],[r.hi-r.effect]],fmt='o',color=COL[t.split('-')[0]],capsize=2,label=t if i==0 else None)
    ax.axvline(0,color='#777777',lw=.7);ax.set_yticks(range(len(outcomes)),['Ordinal','Midpoint','Alternative top','Any','≥10%','≥25%','≥50%']);ax.invert_yaxis();ax.set_xlabel('Randomized form contrast (outcome-specific scale)');ax.legend(frameon=False);fig.tight_layout();save(fig,out,'nature_ed_fig2')
    # ED3: model families
    source(root,'nature_ed_fig3',cv);fig,ax=plt.subplots(figsize=(170*MM,85*MM))
    for j,model in enumerate(['ridge','elastic_net','rf','hgb']):
        zz=cv[cv.model==model].set_index('feature_set').loc[FS]
        ax.plot(np.arange(7),zz.r2,marker=['o','s','D','^'][j],label=model)
    ax.axhline(0,color='#777777',lw=.7);ax.set_xticks(range(7),FS);ax.set_ylabel('Repeated-CV R²');ax.legend(frameon=False,ncol=4);fig.tight_layout();save(fig,out,'nature_ed_fig3')
    # ED4: outcome representations
    z=orep.groupby('outcome',as_index=False).r2.agg(['mean','std']).reset_index();source(root,'nature_ed_fig4',z);fig,ax=plt.subplots(figsize=(145*MM,80*MM));ax.errorbar(range(len(z)),z['mean'],yerr=1.96*z['std']/np.sqrt(10),fmt='o',capsize=2,color='#30343B');ax.axhline(0,color='#777777',lw=.7);ax.set_xticks(range(len(z)),z.outcome,rotation=30,ha='right');ax.set_ylabel('Ridge repeated-CV R²');fig.tight_layout();save(fig,out,'nature_ed_fig4')
    # ED5: latent diagnostics
    source(root,'nature_ed_fig5',ld);fig,axs=plt.subplots(1,2,figsize=(150*MM,75*MM));axs[0].barh(ld.domain,ld.variance_explained,color='#2B7A91');axs[0].set_xlabel('Variance explained by PC1');axs[1].barh(ld.domain,ld.cronbach_alpha,color='#30343B');axs[1].set_xlabel('Cronbach α');fig.tight_layout();save(fig,out,'nature_ed_fig5')
    # ED6: cross-form R² and slopes
    source(root,'nature_ed_fig6',cf);fig,axs=plt.subplots(1,2,figsize=(170*MM,75*MM));labels=[f'{r.source[0].upper()}→{r.target[0].upper()}' for _,r in cf.iterrows()];axs[0].scatter(range(len(cf)),cf.recentered_r2,color='#2B7A91');axs[1].scatter(range(len(cf)),cf.slope,color='#C46B38')
    for ax,ylabel in zip(axs,['Recentered R²','Calibration slope']):ax.set_xticks(range(len(cf)),labels);ax.set_ylabel(ylabel);ax.axhline(0,color='#777777',lw=.7)
    fig.tight_layout();save(fig,out,'nature_ed_fig6')
    # ED7: cosine and sign agreement
    source(root,'nature_ed_fig7',sim);fig,axs=plt.subplots(1,2,figsize=(170*MM,75*MM));zz=sim[sim.feature_set.eq('ALL')];labels=[f'{r.form1[0].upper()}–{r.form2[0].upper()}' for _,r in zz.iterrows()]
    for i,(_,r) in enumerate(zz.iterrows()):
        axs[0].plot(i,r.cosine,'o',color='#30343B');axs[0].vlines(i,r.cos_lo,r.cos_hi,color='#30343B')
        axs[1].plot(i,r.sign_agreement,'o',color='#30343B');axs[1].vlines(i,r.sign_lo,r.sign_hi,color='#30343B')
    for ax,ylabel in zip(axs,['Cosine similarity','Sign agreement']):ax.set_xticks(range(len(zz)),labels);ax.set_ylabel(ylabel)
    fig.tight_layout();save(fig,out,'nature_ed_fig7')
    # ED8: learner comparison
    source(root,'nature_ed_fig8',h);fig,axs=plt.subplots(1,2,figsize=(170*MM,75*MM))
    for i,(metric,lcol,hcol) in enumerate([('calibration','cal_lo','cal_hi'),('top_bottom','tb_lo','tb_hi')]):
        for j,t in enumerate(['food-cash','medical-cash']):
            z=h[h.contrast==t].set_index('method').loc[['t','dr','r']];x=np.arange(3)+(j-.5)*.12
            axs[i].errorbar(x,z[metric],yerr=[z[metric]-z[lcol],z[hcol]-z[metric]],fmt='o',color=COL[t.split('-')[0]],capsize=2,label=t if i==0 else None)
        axs[i].axhline(0,color='#777777',lw=.7);axs[i].set_xticks(range(3),['T','DR','R']);axs[i].set_ylabel(metric.replace('_',' '))
    axs[0].legend(frameon=False);fig.tight_layout();save(fig,out,'nature_ed_fig8')
    # ED9: repeated-seed distribution
    source(root,'nature_ed_fig9',seed);fig,axs=plt.subplots(1,2,figsize=(170*MM,75*MM))
    for i,metric in enumerate(['calibration','top_bottom']):
        for j,(method,contrast) in enumerate([(m,c) for m in ['t','dr','r'] for c in ['food-cash','medical-cash']]):
            z=seed[(seed.method==method)&(seed.contrast==contrast)];axs[i].scatter(np.full(len(z),j)+np.linspace(-.08,.08,len(z)),z[metric],s=7,color=COL[contrast.split('-')[0]],alpha=.75)
        axs[i].axhline(0,color='#777777',lw=.7);axs[i].set_xticks(range(6),['T F','T M','DR F','DR M','R F','R M']);axs[i].set_ylabel(metric.replace('_',' '))
    fig.tight_layout();save(fig,out,'nature_ed_fig9')
    # ED10: quality effects and moderators; exact screens/N shown.
    z1=qe[(qe.outcome=='outcome_ord')&(qe.amount.astype(str)=='pooled')&qe['sample'].isin(['R','C','Q1','Q2'])&qe.contrast.isin(['food-cash','medical-cash'])]
    z2=qm[(qm['sample'].isin(['R','C','Q1','Q2']))&(qm.contrast=='medical-food')&(qm.spec=='trend')&(qm.se_type=='HC1')&qm.variable.isin(['income_h','q30_medexp'])]
    source(root,'nature_ed_fig10',pd.concat([z1.assign(kind='mean_effect'),z2.assign(kind='moderator')],ignore_index=True))
    fig,axs=plt.subplots(1,4,figsize=(183*MM,85*MM),sharey=True)
    specs=[('Food − Cash',z1,'food-cash','effect'),('Medical − Cash',z1,'medical-cash','effect'),('Income moderation',z2,'income_h','effect_or_wald'),('Medical-spending moderation',z2,'q30_medexp','effect_or_wald')]
    for ax,(title,tab,key,col) in zip(axs,specs):
        g=tab[tab.contrast.eq(key) if 'contrast' in tab.columns and key in ['food-cash','medical-cash'] else tab.variable.eq(key)].set_index('sample').loc[['R','C','Q1','Q2']]
        for i,(_,r) in enumerate(g.iterrows()):ax.errorbar(r[col],i,xerr=[[r[col]-r.lo],[r.hi-r[col]]],fmt='o',color='#30343B',capsize=2)
        ax.axvline(0,color='#777777',lw=.7);ax.set_title(title,fontsize=7);ax.set_yticks(range(4),[f'{s} (N={int(g.loc[s,"N"]):,})' for s in ['R','C','Q1','Q2']]);ax.set_xlabel('Ordinal contrast / slope')
    axs[0].invert_yaxis()
    fig.tight_layout();save(fig,out,'nature_ed_fig10')

def legends(root,out):
    cell=load(root,'nature_design_cells.csv');q=load(root,'nature_hte_primary.csv');policy=load(root,'nature_policy_value.csv');amount=load(root,'nature_amount_hte.csv')
    n=int(cell.N.sum());pair_n=int(q[(q.contrast=='food-cash')&(q.method=='dr')].N.iloc[0]);pair_m=int(q[(q.contrast=='medical-cash')&(q.method=='dr')].N.iloc[0])
    txt=f'''# Nature-series figure legends (draft)

All panels use the Raw R sample (N={n:,}) unless a smaller N is stated. Responses are hypothetical stated additional consumption, not realized spending. No figure implies welfare or actual cash-equivalent value.

**Fig. 1 | Transfer form changes stated additional-consumption responses.** a, Randomized 3×3 transfer-form-by-amount design with cell N. b, Six-category response distribution by transfer form, pooled across amounts; bar segments are category shares. c, Cell mean of the original ordinal 1–6 response with 95% normal-approximation confidence intervals, plus pooled randomized contrasts estimated by a saturated form×amount linear model with HC1 intervals. N={n:,}; no multiplicity correction is used for the prespecified average contrasts.

**Fig. 2 | Rich baseline information explains little stated-MPC variation.** a, Repeated five-fold out-of-sample R² for a prespecified random forest on midpoint-coded stated MPC, using identical stratified folds for the seven locked feature sets; intervals are 95% bootstrap intervals over ten held-out fold scores. b, Paired fold differences relative to objective/needs variables with 95% fold-bootstrap intervals; vertical lines at +0.01 and +0.02 are predeclared practical-gain benchmarks. c, Held-out R² from discovery-half PCA domain scores, with factor alpha values listed. N={n:,} for a,b; c uses the held-out half. These are predictive, not causal comparisons.

**Fig. 3 | Observed response rankings have limited cross-form portability.** a, Spearman correlations between source-form model predictions and observed target-form midpoint stated MPC; each target contains a distinct randomized respondent sample. b, Ridge coefficient-vector correlations for objective/needs and ALL blocks with 95% stratified respondent-bootstrap intervals; the displayed difference is also bootstrap-tested. c, Classical attenuation sensitivity at assumed equal reliabilities 0.4, 0.6, and 0.8; reliability is not observed or estimated. N={n:,}; cross-form source models use the full source arm and never refit on target outcomes. Panel a is descriptive, not a treatment-effect estimand.

**Fig. 4 | Predictable fungibility heterogeneity differs by transfer context.** a,b, Within-quintile observed randomized midpoint stated-MPC contrast across quintiles of out-of-fold DR predicted treatment effects, using identical five-fold cell-stratified partitions and held-out outcomes. Error bars are 95% normal-approximation intervals. Food−Cash N={pair_n:,}; Medical−Cash N={pair_m:,}. c, Medical-minus-Food difference in calibration slopes and top-minus-bottom observed-effect separation, with 95% stratified respondent-bootstrap intervals that resample Cash observations jointly. Calibration models use HC1 errors. The contrast difference is exploratory but fixed by the roadmap; learner comparisons appear in Extended Data.

**Fig. 5 | Medical-context heterogeneity varies with amount and economic exposure.** a, Out-of-fold Medical−Cash calibration slopes by randomized transfer amount for T and cross-fitted DR learners, with HC1 95% confidence intervals. b,c, Raw within-band randomized Medical−Food contrasts in the original ordinal 1–6 response for household income and past-year medical-spending bands; normal-approximation 95% intervals. Medical−Food is a secondary contrast used because the transparent moderation signal is stronger there. Past medical spending is a proxy for prior exposure/need, not a causal treatment or strict bindingness measure. N={n:,} overall; amount-specific and band Ns are in panel source CSVs.

**Fig. 6 | Personalized form assignment does not improve the stated-consumption objective.** a, Cross-fitted doubly robust policy values for three uniform forms, a depth-2 tree, and ML argmax, with 95% respondent-bootstrap intervals; annotations give gains versus uniform Cash and paired bootstrap intervals. b, Out-of-fold policy allocation shares. Known one-third assignment propensities and held-out outcome-model predictions are used. N={n:,}; IPW values and seed-stability checks are provided in supplementary tables. These values concern stated midpoint MPC, not welfare or realized spending.

**Extended Data Fig. 1 | Full nine-cell outcome distributions.** Each panel is a randomized form×amount cell; bars show six-category response shares, and titles give exact cell N. Raw R; N={n:,}.

**Extended Data Fig. 2 | Form-effect robustness across outcome codings.** Pooled Food−Cash and Medical−Cash contrasts under ordinal, midpoint, alternative-top, and binary-threshold outcomes. Points and bars are HC1 estimates and 95% intervals. Scales differ across rows; N={n:,}.

**Extended Data Fig. 3 | Prediction-model family comparison.** Mean repeated-CV R² across locked information sets for ridge, elastic net, random forest, and histogram gradient boosting on identical folds. N={n:,}; full fold distributions and error metrics are in source tables.

**Extended Data Fig. 4 | Outcome-representation predictability.** Ridge repeated-CV R² across ordinal, midpoint, alternative-top, and threshold outcomes; intervals depict 95% normal intervals over ten fold scores. N={n:,}.

**Extended Data Fig. 5 | Subjective-factor diagnostics.** First-component explained variance and internal-consistency alpha for three preassigned subjective domains. Loadings come from the discovery half and are scored in the held-out half.

**Extended Data Fig. 6 | Cross-form level and slope transfer.** Mean-recentered target-form R² and calibration slope for all six directed source→target predictions. N={n:,} across randomized arms; no target-form mapping is refitted.

**Extended Data Fig. 7 | Predictor-map similarity diagnostics.** ALL-feature ridge coefficient cosine similarity and sign agreement with 95% respondent-bootstrap intervals. N={n:,}; the measures are descriptive.

**Extended Data Fig. 8 | HTE learner comparison.** T, cross-fitted DR, and Robinson R learner calibration and top–bottom separation for Food−Cash and Medical−Cash; points and bars show HC1 or normal-approximation 95% intervals. Pairwise Ns: {pair_n:,} and {pair_m:,}.

**Extended Data Fig. 9 | HTE stability over ten fixed seeds.** Each dot is a complete five-fold OOF re-estimation of calibration or top–bottom separation under one seed. Seed grid 20260921–20260930; pairwise Ns: {pair_n:,} and {pair_m:,}.

**Extended Data Fig. 10 | Response-quality sensitivity.** Rows show Raw R, Clean C, Q1 and Q2 screens with exact N; columns show pooled ordinal Food−Cash and Medical−Cash effects and Medical−Food income and prior-medical-spending moderation. Points and bars are HC1 estimates and 95% intervals. Quality screens use only baseline response-style diagnostics and are sensitivity checks, not primary exclusions.
'''
    (out/'nature_figure_legends.md').write_text(txt,encoding='utf-8')

def main(root):
    root=Path(root);out=root/'figures';out.mkdir(parents=True,exist_ok=True);style()
    for f in [fig1,fig2,fig3,fig4,fig5,fig6,extended]:f(root,out)
    legends(root,out);print('generated 6 main + 10 Extended Data figures')
if __name__=='__main__':
    p=ArgumentParser();p.add_argument('root');a=p.parse_args();main(a.root)
