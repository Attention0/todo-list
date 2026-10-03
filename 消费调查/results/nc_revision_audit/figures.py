"""Finite audit figures, aggregate sources only; no selection by P."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy import stats
OUT=Path(__file__).resolve().parent
COLORS=['#1F4E79','#2A9D8F','#D97757'];FORMS=['cash','food','medical'];MARKERS=['o','s','^']
plt.rcParams.update({'font.family':'Arial','font.size':8,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':7,'axes.linewidth':.6,'pdf.fonttype':42,'svg.fonttype':'none'})

def finish(fig,name):
    for ax in fig.axes:
        ax.spines[['top','right']].set_visible(False)
    fig.canvas.draw()
    bb=fig.get_tightbbox(fig.canvas.get_renderer());w,h=fig.get_size_inches()
    assert bb.x0>=0 and bb.y0>=0 and bb.x1<=w and bb.y1<=h,(name,bb,w,h)
    for ext in ['pdf','svg','png']:
        p=OUT/f'{name}.{ext}';fig.savefig(p,dpi=600)
        if ext=='svg':p.write_text('\n'.join(l.rstrip() for l in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)

def profile_figs():
    t=pd.read_csv(OUT/'form_amount_profiles.csv')
    for name,outcomes,h in [('fig_form_top75',['top75'],75),('fig_form_extended',['ordinal','midpoint'],80)]:
        fig,axes=plt.subplots(1,len(outcomes),figsize=(180/25.4,h/25.4),squeeze=False)
        fig.subplots_adjust(left=.115,right=.96,bottom=.26,top=.84,wspace=.35)
        for j,(y,ax) in enumerate(zip(outcomes,axes.flat)):
            for i,f in enumerate(FORMS):
                d=t[(t.outcome==y)&(t.form==f)].sort_values('amount')
                ax.errorbar(range(3),d.estimate,yerr=[d.estimate-d.lo,d.hi-d.estimate],color=COLORS[i],marker=MARKERS[i],ms=3.5,lw=1.5 if i==0 else 1.1,elinewidth=.7,capsize=2,label=f.title())
            ax.set_xticks(range(3),['¥200','¥1,000','¥5,000'])
            ax.set_ylim((1,4) if y=='ordinal' else (0,.35) if y=='midpoint' else (0,.18))
            if y=='top75':ax.set_yticks([0,.05,.10,.15])
            if y!='ordinal':ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
            ax.set_ylabel({'ordinal':'Mean stated category (individual scale1–6)','midpoint':'Midpoint-coded stated MPC','top75':'Pr(stated response >75%)'}[y])
            ax.grid(axis='y',color='#EEF0F2',lw=.4)
            ax.legend(frameon=False,fontsize=7,loc='upper right')
            ax.text(-.075,1.08,chr(65+j),transform=ax.transAxes,fontweight='bold',fontsize=10)
        finish(fig,name)

def specifications():
    t=pd.read_csv(OUT/'specification_grid.csv')
    groups=list(t.groupby(['outcome','model'],sort=False))
    assert len(groups)==20
    fig,axes=plt.subplots(5,4,figsize=(180/25.4,240/25.4))
    fig.subplots_adjust(left=.10,right=.98,bottom=.06,top=.96,wspace=.52,hspace=.70)
    colors={'R':'#1F4E79','A':'#527997','C':'#849FB5','Q1':'#777777','Q2':'#AAAAAA'}
    source=[]
    for ax,((outcome,model),d) in zip(axes.flat,groups):
        ax.axhline(0,color='#777777',lw=.5)
        for j,r in enumerate(d.itertuples()):
            if r.status!='ok':continue
            est=json.loads(r.profile);lo=json.loads(r.profile_lo);hi=json.loads(r.profile_hi)
            for k,(e,l,h) in enumerate(zip(est,lo,hi)):
                xx=j+(k-(len(est)-1)/2)*.15
                ax.errorbar(xx,e,yerr=[[e-l],[h-e]],color=colors[r.sample],ms=1.3,marker='o',lw=.35,elinewidth=.35,alpha=.7)
                source.append(dict(spec_id=r.spec_id,component=k+1,estimate=e,lo=l,hi=h,index=j,panel=outcome+'/'+model))
        ax.set_title(outcome+' / '+model.replace('ordered_','ord. ').replace('OLS_HC3','OLS'),fontsize=6.5)
        ax.tick_params(labelsize=5.8)
        ax.set_xticks([0,37,74]);ax.set_xlim(-2,77)
    fig.text(.53,.014,'Finite specification index · fixed R/A/C/Q1/Q2 × amount × contrast order; own-scale estimates',ha='center',fontsize=6.5)
    pd.DataFrame(source).to_csv(OUT/'specification_figure_source.csv',index=False)
    finish(fig,'fig_specification_family')

def quality():
    t=pd.read_csv(OUT/'quality_gradient_source.csv')
    fig,axes=plt.subplots(1,2,figsize=(180/25.4,80/25.4))
    fig.subplots_adjust(left=.11,right=.97,bottom=.25,top=.85,wspace=.35)
    for j,(target,ax) in enumerate(zip(['cash-food','cash-medical'],axes)):
        d=t[t.contrast==target].set_index('sample').loc[['R','A','C','Q1','Q2']]
        ax.axhline(0,color='#777777',lw=.65)
        ax.errorbar(range(5),100*d.estimate,yerr=[100*(d.estimate-d.lo),100*(d.hi-d.estimate)],fmt='o',color=COLORS[0],ms=3.5,elinewidth=.75,capsize=2)
        ax.set_xticks(range(5),['R','A','C','Q1','Q2']);ax.set_ylim(-12,8)
        ax.set_ylabel('Top75 slope difference (pp / fivefold)')
        ax.set_title(target.replace('-',' − ').title(),fontsize=8)
        ax.text(-.08,1.08,chr(65+j),transform=ax.transAxes,fontweight='bold',fontsize=10)
    fig.text(.53,.04,'Nested quality selections change sample composition; not exogenous quality treatments',ha='center',fontsize=7)
    finish(fig,'fig_quality_gradient')

def binding():
    t=pd.read_csv(OUT/'bindingness_ratio_source.csv');t=t[(t['sample']=='R')&(t.outcome=='top75')]
    order=['<=.10','(.10,.25]','(.25,.50]','(.50,1]','>1'];d=t.set_index('ratio_bin').reindex(order)
    fig,ax=plt.subplots(figsize=(180/25.4,76/25.4));fig.subplots_adjust(left=.14,right=.97,bottom=.28,top=.88)
    ax.axhline(0,color='#777777',lw=.7)
    ax.errorbar(range(5),d.estimate*100,yerr=[(d.estimate-d.lo)*100,(d.hi-d.estimate)*100],fmt='o',ms=4,color=COLORS[0],elinewidth=.8,capsize=2)
    ax.set_xticks(range(5),['≤0.10','0.10–0.25','0.25–0.50','0.50–1','>1'])
    ax.set_ylabel('Cash − Food Top75 gap (pp)')
    ax.set_xlabel('Assigned amount / conservative six-month food spending',labelpad=10)
    ax.text(.01,1.05,'Between-person association, not a causal bindingness gradient',transform=ax.transAxes,fontsize=7.5)
    finish(fig,'fig_bindingness_ratio')

def relative():
    t=pd.read_csv(OUT/'relative_scale_cv.csv')
    fig,axes=plt.subplots(1,3,figsize=(180/25.4,80/25.4));fig.subplots_adjust(left=.105,right=.97,bottom=.25,top=.84,wspace=.32)
    for j,(outcome,ax) in enumerate(zip(['top75','ordinal','midpoint'],axes)):
        ax.axhline(0,color='#777777',lw=.6);ax.axhline(1,color='#BBBBBB',ls=':',lw=.7)
        for k,mapping in enumerate(['M1','M2','rank']):
            d=t[(t.outcome==outcome)&(t.mapping==mapping)].set_index('sample').loc[['R','A','C','Q1','Q2']]
            ax.plot(range(5),d.relative_improvement*100,marker=MARKERS[k],ms=3,color=COLORS[k],lw=.9,label=mapping)
        ax.set_xticks(range(5),['R','A','C','Q1','Q2']);ax.set_title(outcome,fontsize=8);ax.set_ylim(-1.5,1.5)
        ax.text(-.11,1.08,chr(65+j),transform=ax.transAxes,fontweight='bold',fontsize=10)
    axes[0].set_ylabel('Relative reduction in held-out loss (%)')
    axes[-1].legend(frameon=False,fontsize=6.5,loc='lower right')
    fig.text(.53,.06,'REL versus ABS · unified five folds · dotted line: revision-stage 1% materiality rule',ha='center',fontsize=7)
    finish(fig,'fig_relative_scale')

def allx():
    t=pd.read_csv(OUT.parent/'mpc_allx_screen/all_screen_results.csv');t=t[t.target.isin(['cash','rc'])];source=[]
    fig,axes=plt.subplots(2,3,figsize=(180/25.4,125/25.4));fig.subplots_adjust(left=.105,right=.97,bottom=.10,top=.94,wspace=.35,hspace=.45)
    for j,((target,outcome),d) in enumerate(t.groupby(['target','outcome'],sort=False)):
        ax=axes.flat[j];p=d.p.dropna().sort_values().to_numpy();expected=(np.arange(len(p))+.5)/len(p)
        ax.plot(-np.log10(expected),-np.log10(p),'.',ms=2,color='#777777');lim=max(np.max(-np.log10(expected)),np.max(-np.log10(p)))
        ax.plot([0,lim],[0,lim],color='#BBBBBB',lw=.65)
        ax.set_title(target+'/'+outcome,fontsize=7);ax.set_xlabel('Expected −log10 P',fontsize=7);ax.set_ylabel('Observed −log10 P',fontsize=7)
        ax.text(.04,.90,f'q<.10: {int((d.q<.1).sum())}/150',transform=ax.transAxes,fontsize=6.5)
        for rank,(ex,ob) in enumerate(zip(expected,p)):source.append(dict(target=target,outcome=outcome,rank=rank+1,expected_P=ex,raw_P=ob))
    pd.DataFrame(source).to_csv(OUT/'allx_QQ_source.csv',index=False)
    t.groupby(['target','outcome']).agg(estimable=('p','count'),min_q=('q','min'),q_10=('q',lambda x:(x<.1).sum()),q_05=('q',lambda x:(x<.05).sum())).reset_index().to_csv(OUT/'allx_supplemental_counts.csv',index=False)
    # Preserve full corrected-P distribution as aggregate screen results, not individual data.
    t[['variable','target','outcome','status','p','q','holm_p']].to_csv(OUT/'allx_q_distribution.csv',index=False)
    finish(fig,'fig_allx_supplemental')

if __name__=='__main__':
    profile_figs();specifications();quality();binding();relative();allx();print('Seven audit figures exported.')
