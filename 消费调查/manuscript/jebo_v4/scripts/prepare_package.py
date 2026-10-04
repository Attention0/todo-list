"""Writing-only assets: read frozen aggregates; no respondent data or fitted models."""
from pathlib import Path
import csv, json, re, shutil, hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator

M=Path(__file__).resolve().parents[1]; ROOT=M.parents[1]
O=ROOT/'results'/'jebo_review_revision'; OLD=M.parent/'jebo_v3'
for sub in ['figures','source_data']: (M/sub).mkdir(exist_ok=True)
forms=['cash','food','medical']; names=['Cash','Food','Medical']
labels=['Bottom','<10%','10–25%','25–50%','50–75%','>75%']
plt.rcParams.update({'font.family':'Times New Roman','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
shades=[plt.cm.Blues(x) for x in np.linspace(.15,.9,6)]
colors=['#203f56','#657e90','#899198']
cell=pd.read_csv(O/'adult_share_yuan_table.csv')
def finish(fig,name):
    for ext in ['png','pdf']: fig.savefig(M/'figures'/f'{name}.{ext}',dpi=300,bbox_inches='tight')
    plt.close(fig)

# Exact original aggregate summaries and original uncertainty, only graphical changes.
fig,axes=plt.subplots(1,3,figsize=(10.5,3.7),sharey=True)
for fi,ax in enumerate(axes):
    x=cell[cell.form==forms[fi]]; left=np.zeros(3)
    for k in range(1,7):
        vals=x[f'share{k}'].to_numpy()*100
        ax.barh(np.arange(3),vals,left=left,color=shades[k-1],edgecolor='white',height=.62,label=labels[k-1]); left+=vals
    ax.set_title(names[fi],fontweight='bold'); ax.set_yticks(range(3),['RMB 200','RMB 1,000','RMB 5,000']); ax.invert_yaxis(); ax.set_xlim(0,100); ax.set_xlabel('Respondents (%)')
fig.legend(*axes[0].get_legend_handles_labels(),ncol=6,loc='lower center',bbox_to_anchor=(.5,-.025),frameon=False)
fig.tight_layout(rect=[0,.1,1,1]); finish(fig,'fig1_response_atlas')

fig,axes=plt.subplots(1,2,figsize=(10.5,4.2)); fit=pd.read_csv(O/'affine_midpoint_fit.csv')
for fi in range(3):
    x=cell[cell.form==forms[fi]]; a=x.amount.to_numpy(); s=x.midpoint.to_numpy()
    axes[0].errorbar(a,s*100,yerr=np.vstack([s-x.midpoint_lo,x.midpoint_hi-s])*100,marker='o',capsize=3,color=colors[fi],label=names[fi])
    axes[1].errorbar(a,x.yuan,yerr=np.vstack([x.yuan-x.yuan_lo,x.yuan_hi-x.yuan]),marker='o',capsize=3,color=colors[fi],label=names[fi])
    ff=fit[(fit.form==forms[fi])&(fit.model=='form_intercepts_slopes')]
    axes[1].plot(ff.amount,ff.predicted_yuan,ls='--',color=colors[fi],alpha=.65)
axes[0].set_xscale('log');axes[0].set_ylim(10,31);axes[0].set_ylabel('Midpoint-coded share (%)')
axes[1].set_ylim(0,1200);axes[1].set_ylabel('Midpoint-implied additional yuan')
for ax in axes:
    ax.set_xticks([200,1000,5000],['200','1,000','5,000']);ax.xaxis.set_minor_locator(NullLocator());ax.set_xlabel('Transfer amount (RMB)');ax.legend(frameon=False)
fig.tight_layout();finish(fig,'fig2_share_and_yuan')

changes=[]; fig,axes=plt.subplots(1,3,figsize=(10.5,4.1),sharex=True,sharey=True)
for fi,ax in enumerate(axes):
    x=cell[cell.form==forms[fi]].set_index('amount')
    vals=np.array([(x.loc[5000,f'share{k}']-x.loc[200,f'share{k}'])*100 for k in range(1,7)])
    for k,v in enumerate(vals,1):changes.append({'form':forms[fi],'category':k,'label':labels[k-1],'share200':x.loc[200,f'share{k}'],'share5000':x.loc[5000,f'share{k}'],'change_pp':v})
    ax.barh(range(6),vals,color=shades,edgecolor='#73818b',linewidth=.4,height=.67)
    ax.axvline(0,color='#555555',lw=.7);ax.set_title(names[fi],fontweight='bold');ax.set_yticks(range(6),labels);ax.set_xlim(-10,7);ax.set_xticks([-8,-4,0,4]);ax.set_xlabel('Change (percentage points)')
    for k,v in enumerate(vals):ax.text(v+(.16 if v>=0 else -.16),k,f'{v:+.2f}',ha='left' if v>=0 else 'right',va='center',fontsize=11)
axes[0].invert_yaxis();fig.tight_layout();finish(fig,'fig3_category_changes')
pd.DataFrame(changes).to_csv(M/'source_data'/'endpoint_category_changes.csv',index=False)

food=pd.read_csv(O/'food_bindingness_raw_cells.csv'); fig,axes=plt.subplots(1,2,figsize=(10.5,4.5),sharey=True)
for g,ax in enumerate(axes):
    for fi,f in enumerate(forms[:2]):
        x=food[(food.G==g)&(food.form==f)];pr=x.top75.to_numpy();se=np.sqrt(pr*(1-pr)/x.N)
        ax.errorbar(x.amount,pr*100,yerr=1.96*se*100,marker='o',capsize=3,color=colors[fi],label=names[fi])
    ax.set_xscale('log');ax.set_xticks([200,1000,5000],['200','1,000','5,000']);ax.xaxis.set_minor_locator(NullLocator());ax.set_xlabel('Transfer amount (RMB)');ax.set_title(['G = 0: fails proxy (N = 815)','G = 1: passes proxy (N = 2,806)'][g]);ax.set_ylim(-2,25);ax.legend(frameon=False)
axes[0].set_ylabel('Highest-category responses (%)')
fig.text(.5,.01,'Sharp prediction in G = 0: Food–Cash size gradient < 0; observed: +8.00 pp per step',ha='center',fontsize=11)
fig.tight_layout(rect=[0,.06,1,1]);finish(fig,'fig4_food_raw_cells')

inc=pd.read_csv(O/'incremental_yuan_response.csv'); fig,ax=plt.subplots(figsize=(8,4))
for fi in range(3):
    x=inc[(inc.form==forms[fi])&(inc.contrast=='within-form')];e=x.estimate.to_numpy();pos=np.arange(2)+(fi-1)*.13
    ax.errorbar(pos,e,yerr=np.vstack([e-x.bootstrap_lo,x.bootstrap_hi-e]),marker='o',ls='none',capsize=4,color=colors[fi],label=names[fi])
ax.set_xticks([0,1],['RMB 200 to 1,000','RMB 1,000 to 5,000']);ax.set_ylim(.12,.28);ax.set_ylabel('Incremental implied yuan per transfer yuan');ax.legend(frameon=False,ncol=3);fig.tight_layout();finish(fig,'figS1_incremental_response')
for fn in ['adult_cell_distribution.csv','adult_share_yuan_table.csv','affine_midpoint_fit.csv','incremental_yuan_response.csv','food_bindingness_raw_cells.csv','scientific_family42.csv']:
    shutil.copyfile(O/fn,M/'source_data'/fn)
shutil.copyfile(O/'AUTHOR_INFORMATION_REQUIRED.md',M/'AUTHOR_INFORMATION_REQUIRED.md')

def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)
src=(OLD/'JEBO_supplement_v3.md').read_text(encoding='utf8')
sections={int(re.match(r'## S(\d+)',p).group(1)):p.strip() for p in re.split(r'(?=^## S\d+ )',src,flags=re.M) if p.startswith('## S')}
order=[1,5,4,2,3,6,7,8,9,10]; blocks=[]
for new,old in enumerate(order,1):
    t=sections[old]
    t=re.sub(r'(?m)^(## S|### Table S)'+str(old)+r'(?=\D)',lambda m:m.group(1)+str(new),t)
    # Typography cleanup only, preserve table values and questionnaire wording.
    chunks=t.split('\n\n')
    for i,b in enumerate(chunks):
        if not b.startswith(('|','#')) and new!=9:
            b=re.sub(r'\b(across|least|than|are|of|the|nominal|at|N|ESS|maximum|cap|sample|seed|SD|percentiles|code|minimum|endpoints|and|has|all|conservative|below|above|hard|use|All|is|reports|positive|observed|or|scenario|Ns|discrepancy|bootstrap)(?=\d)',r'\1 ',b)
            b=b.replace('scientific42','42-test scientific').replace('N 5,497','N = 5,497').replace('no more than80%','no more than 80%')
            b=b.replace('chi-square2','chi-square with 2 degrees of freedom').replace('1.33pp','1.33 pp').replace('All new calculations','The adult analyses').replace('All new bootstrap cells','All bootstrap cells')
            chunks[i]=b
    t='\n\n'.join(chunks)
    if new==2:
        t=t.replace('Bottom category arithmetic','Original distributions and bottom-category arithmetic',1)
        rows=[]
        for r in cell.itertuples():rows.append([r.form.title(),f'{r.amount:,}',r.N]+[f'{getattr(r,"share"+str(k))*100:.2f}' for k in range(1,7)])
        raw='### Table S2a Original adult six-bin frequencies\n\n'+table(['Form','RMB','N']+labels,rows)+'\n\nNote: Frequencies in percent; original category counts and unrounded shares are in source_data/adult_cell_distribution.csv. No distributional test is added.\n\n'
        t=t.replace('### Table S2 Bottom category decomposition','### Table S2b Bottom-category decomposition')
        pos=t.index('\n\n');t=t[:pos+2]+raw+t[pos+2:]
    if new==4:
        t+='\n\n![Finite incremental implied yuan with original bootstrap intervals](figures/figS1_incremental_response.png)\n\nFigure S1. Finite incremental implied-yuan responses. Pointwise 95% intervals use the existing 4,000 cell-stratified bootstrap draws. These summarize coded hypothetical responses, not local consumption derivatives.\n'
    if new==7:
        counts=pd.read_csv(ROOT/'results/nc_revision_audit/allx_supplemental_counts.csv');cf=pd.read_csv(ROOT/'results/nc_revision_audit/allx_crossfit_reused_summary.csv')
        t+='\n\n### S7.1 Historical broad observable screen\n\nThe previously completed screen considered 150 representations per target/outcome, not 150 independent hypotheses. Cash and an earlier pooled restricted-versus-cash contrast (RC) were screened for ordinal, midpoint and highest-category outcomes. The historical full delivered sample and its original definitions are retained; no adult or separate Food/Medical screen is fitted here. No row had q < 0.10 in its original family. This is lack of detected moderation, not evidence of homogeneity.\n\n### Table S7e Historical screen correction summaries\n\n'
        t+=table(['Target','Outcome','Estimable','Minimum q','q < .10'],[[r.target,r.outcome,r.estimable,f'{r.min_q:.4f}',r.q_10] for r in counts.itertuples()])
        t+='\n\n### Table S7f Historical five-fold diagnostics\n\n'+table(['Target','Outcome','Representations','Valid train / holdout','Five train same direction','Five holdout positive'],[[r.target,r.outcome,r.representations,f'{r.five_valid_train} / {r.five_valid_holdout}',r.five_train_same_direction,r.five_holdout_positive] for r in cf.itertuples()])
        t+='\n\nNote: Five cell-stratified folds, historical seed 20261005. Training directions project into held-out coefficients; factor vectors use the training unit direction. Counts describe consistency across all five folds and are dependent, not independent replications. Sparse factor and zero-variance failures remain disclosed. Overlap with the full sample makes training comparisons optimistic. These summaries are not joint BLP/GATES tests. Exact historical tables and definitions remain in results/mpc_allx_screen and results/nc_revision_audit; they do not identify a common psychological mechanism.\n'
    blocks.append(t)
(M/'JEBO_supplement_v4.md').write_text('# Supplementary material\n\nTransfer form and the allocation of small and large windfalls\n\n'+ '\n\n'.join(blocks)+'\n',encoding='utf8')
print('Prepared aggregate-only figures, source copies and reordered supplement.')
