"""Presentation only: frozen approved aggregate inputs; no raw data or model-fitting imports."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter,MaxNLocator
from matplotlib.lines import Line2D
from pypdf import PdfReader,PdfWriter
from PIL import Image,ImageOps,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent
RESULTS=ROOT.parent
COLORS={'cash':'#1F4E79','food':'#2A9D8F','medical':'#D97757','restricted':'#7564A3','neutral':'#7A7A7A'}
MARKERS={'cash':'o','food':'s','medical':'^','restricted':'D'}
FORMS=['cash','food','medical'];AMOUNTS=[200,1000,5000];Y=['ordinal','midpoint','top75']
MM=1/25.4
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','Liberation Sans','DejaVu Sans'],'font.size':8,'axes.labelsize':8,'axes.titlesize':8.5,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'axes.linewidth':.6,'xtick.major.width':.6,'ytick.major.width':.6,'xtick.major.size':2.5,'ytick.major.size':2.5,'axes.spines.top':False,'axes.spines.right':False,'axes.facecolor':'white','figure.facecolor':'white','pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.unicode_minus':False,'savefig.facecolor':'white'})
SOURCE_NAMES={'cells':('mpc_size_curve','fig1_source.csv'),'distribution':('mpc_size_curve','fig2_source.csv'),'thresholds':('mpc_size_curve','fig3_source.csv'),'pooled':('mpc_final_strengthening','figA_source.csv'),'threshold_profile':('mpc_final_strengthening','figB_source.csv'),'relative':('mpc_final_strengthening','figC_source.csv'),'specification':('mpc_final_strengthening','figD_source.csv'),'yuan':('mpc_final_strengthening','figE_source.csv'),'allx':('mpc_allx_screen','all_screen_results.csv'),'families':('mpc_allx_screen','family_summary.csv'),'groups':('mpc_allx_screen','subjective_objective_summary.csv')}
INPUTS={};AUDIT=[];EXPORTS=[]

def read(key):
    folder,name=SOURCE_NAMES[key];path=RESULTS/folder/name;t=pd.read_csv(path);t['source_file']='消费调查/results/'+folder+'/'+name;t['source_row']=np.arange(1,len(t)+1);t['source_commit']=subprocess.check_output(['git','log','-1','--format=%H','--',str(path)],text=True).strip();INPUTS[key]=dict(path=str(path.relative_to(RESULTS.parent)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),rows=len(t),commit=t.source_commit.iloc[0]);return t

def source(t,name,figure,definition):
    t=t.copy();t['figure']=figure;t['plotted_definition']=definition;t.to_csv(ROOT/name,index=False)
    fields=[c for c in ['panel','outcome','form','amount','target','threshold','variable','coding','sample','scale','source_file','source_row','source_commit'] if c in t]
    for row in t[fields].to_dict('records'):AUDIT.append(dict(figure=figure,plotted_statistic=definition,**row))
    return t

def setup(n=2,height=80,rows=1):
    fig,ax=plt.subplots(rows,n,figsize=(180*MM,height*MM),squeeze=False);fig.subplots_adjust(left=.085,right=.982,top=.85,bottom=.27,wspace=.32,hspace=.5)
    return fig,ax.flatten()

def label(ax,letter,title):
    offset=-.045/ax.get_position().width
    ax.text(offset,1.09,letter,transform=ax.transAxes,fontweight='bold',fontsize=10,va='bottom');ax.set_title(title,loc='left',pad=9,fontweight='normal');ax.set_axisbelow(True);ax.yaxis.grid(True,color='#eeeeee',linewidth=.4)

def percent(ax):ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))

def amounts(ax):ax.set_xticks([0,1,2],['¥200','¥1,000','¥5,000']);ax.set_xlim(-.16,2.16)

def legend(fig,forms=FORMS,y=.08):
    handles=[Line2D([],[],color=COLORS[f],marker=MARKERS[f],markersize=3.8,lw=1.6 if f=='cash' else 1.2,linestyle='--' if f=='restricted' else '-',markerfacecolor='white' if f=='restricted' else COLORS[f],label='Restricted (equal weight)' if f=='restricted' else f.title()) for f in forms]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.53,y),ncol=len(forms),frameon=False,handlelength=2.3,columnspacing=2)

def curves(ax,g,forms=FORMS):
    for f in forms:
        q=g[g.form.eq(f)].set_index('amount').reindex(AMOUNTS);v=q.estimate.to_numpy();low=q.lower_ci.to_numpy();high=q.upper_ci.to_numpy()
        ax.errorbar([0,1,2],v,yerr=np.array([v-low,high-v]),color=COLORS[f],marker=MARKERS[f],markersize=3.4,lw=1.6 if f=='cash' else 1.15,elinewidth=.65,capsize=1.7,capthick=.65,linestyle='--' if f=='restricted' else '-',markerfacecolor='white' if f=='restricted' else COLORS[f],zorder=4 if f=='cash' else 3)
    amounts(ax)

def save(fig,name):
    # Fixed page size; no tight-bbox resizing of journal-width figures.
    fig.canvas.draw();box=fig.get_tightbbox(fig.canvas.get_renderer());width,height=fig.get_size_inches()
    assert box.x0>=0 and box.y0>=0 and box.x1<=width and box.y1<=height,(name,'content outside fixed page',box.bounds)
    for ext in ['pdf','svg','png']:
        path=ROOT/(name+'.'+ext);fig.savefig(path,dpi=600,metadata={'Creator':'Frozen PR9-12 visualization package'} if ext=='pdf' else None);EXPORTS.append(path.name)
        if ext=='svg':path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    plt.close(fig)

def main_curves(cells,pooled,thresholds):
    chunks=[]
    for y in Y:
        if y=='ordinal':
            q=cells.copy();q['estimate']=q.ordinal_mean;q['lower_ci']=q.ordinal_mean-1.96*q.ordinal_se;q['upper_ci']=q.ordinal_mean+1.96*q.ordinal_se;q['ci_definition']='existing PR9 mean +/- 1.96 sample-mean SE'
        else:
            q=pooled[pooled.outcome.eq(y)&pooled.form.isin(FORMS)].copy().rename(columns={'lo':'lower_ci','hi':'upper_ci'});q=q.merge(cells[['form','amount','N']],on=['form','amount'],validate='one_to_one');q['ci_definition']='existing PR10 5000 stratified-bootstrap percentile interval'
        q['outcome']=y;q['panel']={'ordinal':'A','midpoint':'B','top75':'C'}[y];chunks.append(q[['panel','outcome','form','amount','estimate','lower_ci','upper_ci','N','ci_definition','source_file','source_row','source_commit']])
    f1=source(pd.concat(chunks,ignore_index=True),'figure1_main_source.csv','Figure1','approved cell mean and approved pointwise95% CI; ordinal interval arithmetic exactly reproduces PR9 legend')
    fig,axes=setup(3,78);fig.subplots_adjust(left=.095,wspace=.55)
    titles=['Ordinal response','Midpoint-coded MPC','High-MPC tail'];ylabs=['Mean stated spending-\nresponse category','Midpoint-coded stated MPC','Pr(stated MPC >75%)']
    for ax,y,title,yl,letter in zip(axes,Y,titles,ylabs,'ABC'):
        label(ax,letter,title);curves(ax,f1[f1.outcome.eq(y)]);ax.set_ylabel(yl)
        if y=='ordinal':ax.set_ylim(1,4);ax.set_yticks([1,2,3,4])
        else:percent(ax);ax.set_ylim(0,.35 if y=='midpoint' else .18);ax.set_yticks([0,.1,.2,.3] if y=='midpoint' else [0,.05,.1,.15])
    fig.text(.54,.185,'Randomized transfer amount',ha='center',fontsize=8);legend(fig,y=.055);save(fig,'fig1_three_outcomes')
    f2=pooled[pooled.form.isin(['cash','restricted'])].copy().rename(columns={'lo':'lower_ci','hi':'upper_ci'});f2['panel']=f2.outcome.map({'midpoint':'A','top75':'B'});f2['arm_type']=np.where(f2.form.eq('restricted'),'derived equal-weight contrast','randomized treatment');f2['N']=f2.apply(lambda r:int(cells.loc[cells.amount.eq(r.amount)&(cells.form.isin(['food','medical']) if r.form=='restricted' else cells.form.eq('cash')),'N'].sum()),axis=1);f2['N_definition']='pooled count for derived Restricted; estimate not N-weighted'
    f2=source(f2,'figure2_main_source.csv','Figure2','approved PR10 Cash / equal-weight Restricted pointwise bootstrap curves')
    fig,axes=setup(2,78)
    for ax,y,title,letter in zip(axes,['midpoint','top75'],['Midpoint-coded MPC','High-MPC tail'],'AB'):
        label(ax,letter,title);g=f2[f2.outcome.eq(y)];curves(ax,g,['cash','restricted']);percent(ax);ax.set_ylim(0,.35 if y=='midpoint' else .18);ax.set_ylabel('Midpoint-coded stated MPC' if y=='midpoint' else 'Pr(stated MPC >75%)');ax.set_yticks([0,.1,.2,.3] if y=='midpoint' else [0,.05,.1,.15])
        for i,a in enumerate(AMOUNTS):
            v=g[g.amount.eq(a)].set_index('form').estimate;ax.plot([i-.055,i-.055],[v.cash,v.restricted],color='#bcbcbc',lw=.65,zorder=1)
    fig.text(.54,.185,'Randomized transfer amount',ha='center',fontsize=8);legend(fig,['cash','restricted'],.055);save(fig,'fig2_cash_restricted_puzzle')
    f3a=thresholds[thresholds.threshold.eq('any_spending')].copy().rename(columns={'probability':'estimate','lo':'lower_ci','hi':'upper_ci'});f3a['outcome']='any_spending';f3a['panel']='A';f3a['ci_definition']='existing PR9 Bernoulli mean +/-1.96 SE'
    f3b=f1[f1.outcome.eq('top75')].copy();f3b['panel']='B';f3=source(pd.concat([f3a,f3b],ignore_index=True),'figure3_main_source.csv','Figure3','existing any-spending threshold and Top75 cell curves; uncertainty retained from their respective approved sources')
    fig,axes=setup(2,78)
    for ax,y,title,letter in zip(axes,['any_spending','top75'],['Any additional spending','High-MPC tail'],'AB'):
        label(ax,letter,title);curves(ax,f3[f3.outcome.eq(y)]);percent(ax);ax.set_ylabel('Pr(any additional spending)' if y=='any_spending' else 'Pr(stated MPC >75%)');ax.set_ylim(0,1 if y=='any_spending' else .18);ax.set_yticks([0,.25,.5,.75,1] if y=='any_spending' else [0,.05,.1,.15])
    cash=f3[(f3.outcome=='top75')&f3.form.eq('cash')].set_index('amount')
    for x,a,offset in [(0,200,(12,16)),(2,5000,(-36,-24))]:axes[1].annotate(f'{100*cash.loc[a,"estimate"]:.1f}%',xy=(x,cash.loc[a,'estimate']),xytext=offset,textcoords='offset points',color=COLORS['cash'],fontsize=7.5,arrowprops=dict(arrowstyle='-',color=COLORS['cash'],lw=.5))
    fig.text(.54,.185,'Randomized transfer amount',ha='center',fontsize=8);legend(fig,y=.055);save(fig,'fig3_distribution_anatomy')

def null_figure(allx,families,groups):
    source(allx[allx.target.isin(['cash','rc'])],'figure4_main_source.csv','Figure4','six approved all-X families: one omnibus per representation, including unsupported factors; no new standardization')
    source(groups,'figure4_summary_source.csv','Figure4 summary','approved descriptive representation and corrected-discovery counts; six families, not independent group tests')
    source(families,'figure4_family_minima_source.csv','Figure4','approved family minimum BH q; compact allowed layout')
    fig,axes=setup(2,87);fig.subplots_adjust(bottom=.34,top=.82,wspace=.37)
    for ax,target,title,letter in zip(axes,['cash','rc'],['Cash slope moderation','Restricted - Cash moderation'],'AB'):
        label(ax,letter,title);q=families[families.target.eq(target)].set_index('outcome').reindex(Y);vals=q.min_q.to_numpy()
        ax.hlines(range(3),.1,vals,color='#d8d8d8',lw=1);ax.scatter(vals,range(3),s=28,marker='D',edgecolor=COLORS['cash' if target=='cash' else 'restricted'],facecolor='white',lw=1.1,zorder=4)
        for j,(y,v) in enumerate(zip(Y,vals)):
            # All estimable q-values retained as faint non-inferential rug ticks.
            qq=allx[(allx.target==target)&(allx.outcome==y)].q.dropna().to_numpy();ax.scatter(qq,np.full(len(qq),j+.13),marker='|',s=12,color='#a7a7a7',alpha=.12,linewidth=.45)
            ax.text(v-.045,j-.16,f'{v:.3f}',ha='right',va='center',fontsize=7,color=COLORS['neutral'])
        ax.axvline(.1,color=COLORS['neutral'],ls=':',lw=.8);ax.set(xlim=(0,1.06),ylim=(2.5,-.55),yticks=range(3),yticklabels=['Ordinal','Midpoint','Top75'],xlabel='BH q (family minimum)',xticks=[0,.1,.5,1]);ax.yaxis.grid(False);ax.text(.03,1.02,'Each outcome: 0 / 150 with q < 0.10',transform=ax.transAxes,fontsize=7.2,color='#333333')
    tile=[('subjective','raw','Raw subjective'),('objective','raw','Raw objective'),('subjective','constructed','Constructed subjective'),('objective','constructed','Constructed objective')]
    for i,(domain,origin,title) in enumerate(tile):
        r=groups[(groups.target=='cash')&(groups.outcome=='midpoint')&groups.domain.eq(domain)&groups.origin.eq(origin)].iloc[0];x=.14+i*.225;fig.text(x,.18,title,ha='center',fontsize=6.8,color='#444444');fig.text(x,.105,f'{int(r.X_screened)} screened  |  0 discovered',ha='center',fontsize=7)
    fig.text(.53,.035,'Counts apply to every outcome / target; no corrected signature is not equivalence.',ha='center',fontsize=6.7,color=COLORS['neutral']);save(fig,'fig4_observables_null')

def extended(distribution,profile,relative,spec,yuan,allx):
    s=source(profile,'ED1_threshold_profile_source.csv','Extended Data1','approved bootstrap-covariance threshold differential slopes and pointwise intervals');fig,axes=setup(1,76);ax=axes[0];fig.subplots_adjust(bottom=.25,left=.12,top=.86);ax.errorbar(range(5),s.estimate,yerr=[s.estimate-s.lo,s.hi-s.estimate],fmt='D-',ms=3.5,color=COLORS['restricted'],mfc='white',lw=1.15,elinewidth=.7,capsize=2);ax.axhline(0,color=COLORS['neutral'],lw=.6);ax.set_xticks(range(5),['Any spending','≥10%','≥25%','≥50%','>75%']);ax.set_ylabel('Restricted - Cash differential slope');ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0));ax.set_xlabel('Stated-spending threshold');label(ax,'A','Nested-threshold profile');save(fig,'ED1_threshold_profile')
    source(relative,'ED2_relative_scales_source.csv','Extended Data2','existing within-form changes and between-form changes / ratio contrasts; approved bootstrap percentile CIs');fig,axes=setup(3,117,2);fig.subplots_adjust(left=.12,top=.9,bottom=.13,wspace=.65,hspace=.65)
    scales=['probability_difference','risk_ratio','odds_ratio'];roles=['within_form_descriptive','between_form_comparison'];titles=['Probability change','Risk ratio','Odds ratio']
    for i,role in enumerate(roles):
        for j,scale in enumerate(scales):
            ax=axes[i*3+j];actual_scale=scale if i==0 or j==0 else 'ratio_of_'+('risk_ratios' if j==1 else 'odds_ratios');g=relative[(relative.role==role)&(relative.scale==actual_scale)].copy();assert len(g)==(4 if i==0 else 3);labels=g.estimand.str.replace('-',' - ',regex=False).str.title();ax.errorbar(g.estimate,range(len(g)),xerr=[g.estimate-g.lo,g.hi-g.estimate],fmt='D',ms=3,color=COLORS['neutral'],elinewidth=.7,capsize=1.5,mfc='white');ax.set_yticks(range(len(g)),labels,fontsize=6);ax.invert_yaxis();ax.axvline(0 if j==0 else 1,color='#bbbbbb',lw=.6);ax.xaxis.set_major_locator(MaxNLocator(3))
            if j==0:ax.xaxis.set_major_formatter(PercentFormatter(1,decimals=0))
            else:ax.set_xscale('log');ax.set_xticks([.25,.5,1,2,4],['0.25','0.5','1','2','4']);ax.minorticks_off()
            label(ax,chr(65+i*3+j),titles[j] if i==0 else ['Difference in changes','Ratio of risk ratios','Ratio of odds ratios'][j]);ax.yaxis.grid(False)
    fig.text(.54,.035,'Top75: randomized ¥200 to ¥5,000 endpoint comparisons',ha='center',fontsize=8);save(fig,'ED2_relative_scales')
    source(spec,'ED3_specification_curve_source.csv','Extended Data3','approved comparable RC interaction estimates: fixed order, original pointwise HC3/HC1 delta intervals');fig,axes=setup(1,143,3);fig.subplots_adjust(top=.93,bottom=.09,left=.115,hspace=.82)
    for ax,coding,letter,title in zip(axes,['midpoint','top75','top75_logit_AME'],'ABC',['Midpoint-coded MPC','Top75: linear probability','Top75: logit probability marginal effect']):
        g=spec[spec.coding.eq(coding)].copy();g['sample_order']=g['sample'].map({'R':0,'A':1,'C':2,'Q1':3,'Q2':4});g['adj_order']=g.adjustment.map({'unadjusted':0,'adjusted':1});g['amount_order']=g.amount_representation.map({'trend':0,'endpoint':1});g=g.sort_values(['sample_order','adj_order','amount_order']);x=np.arange(len(g));ax.errorbar(x,g.comparable_estimate,yerr=[g.comparable_estimate-g.comparable_lo,g.comparable_hi-g.comparable_estimate],fmt='none',ecolor='#b4abc9',elinewidth=.65,capsize=1.3)
        for adj,fill in [('unadjusted','white'),('adjusted',COLORS['restricted'])]:
            for rep,marker in [('trend','o'),('endpoint','^')]:
                ix=g.adjustment.eq(adj)&g.amount_representation.eq(rep);ax.scatter(x[ix],g.loc[ix,'comparable_estimate'],marker=marker,s=13,edgecolors=COLORS['restricted'],facecolors=fill,linewidths=.7,zorder=3)
        for pos in [3.5,7.5,11.5,15.5]:ax.axvline(pos,color='#eeeeee',lw=.5)
        ax.axhline(0,color=COLORS['neutral'],lw=.65);ax.set_xticks([1.5,5.5,9.5,13.5,17.5],['R','A','C','Q1','Q2']);ax.yaxis.set_major_locator(MaxNLocator(4,steps=[1,2,5,10]));ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0));ax.set_ylabel('RC slope difference');ax.set_xlim(-.6,19.6);label(ax,letter,title)
    fig.text(.54,.025,'○ unadjusted   ● adjusted   circles: trend   triangles: unrestricted endpoint / 2',ha='center',fontsize=7);save(fig,'ED3_specification_curve')
    source(yuan,'ED4_share_yuan_source.csv','Extended Data4','approved midpoint share and implied amount×share with existing bootstrap CIs');fig,axes=setup(2,78)
    for ax,outcome,letter,title in zip(axes,['midpoint','implied_yuan'],'AB',['Stated MPC share','Implied additional spending']):
        q=yuan.rename(columns={outcome:'estimate',('midpoint_lo' if outcome=='midpoint' else 'yuan_lo'):'lower_ci',('midpoint_hi' if outcome=='midpoint' else 'yuan_hi'):'upper_ci'});curves(ax,q,FORMS+['restricted']);label(ax,letter,title);ax.set_ylim(bottom=0);ax.set_ylabel('Midpoint-coded stated MPC' if outcome=='midpoint' else 'Implied spending (RMB)')
        if outcome=='midpoint':percent(ax);ax.set_ylim(0,.35)
        else:ax.yaxis.set_major_locator(MaxNLocator(4))
    fig.text(.54,.185,'Randomized transfer amount',ha='center',fontsize=8);legend(fig,FORMS+['restricted'],y=.055);save(fig,'ED4_share_yuan')
    source(distribution,'figureS_distribution_source.csv','Extended Data5 / Figure S distribution','approved unconditional category p1-p6 at each randomized form×amount; no new counts or smoothing');fig,axes=setup(3,93);fig.subplots_adjust(top=.84,bottom=.3,left=.09,wspace=.22);bincols=['#f0f0f0','#d5d9dc','#aab7c1','#7b91a3','#49677e','#1F4E79'];bins=['No extra spending','<10%','10-25%','25-50%','50-75%','>75%']
    for ax,f,letter in zip(axes,FORMS,'ABC'):
        g=distribution[distribution.form.eq(f)].set_index('amount').reindex(AMOUNTS);bottom=np.zeros(3)
        for k,color in enumerate(bincols):v=g['p'+str(k+1)].to_numpy();ax.bar(range(3),v,bottom=bottom,width=.63,color=color,edgecolor='white',lw=.4);bottom+=v
        amounts(ax);ax.set_ylim(0,1);percent(ax);ax.set_yticks([0,.5,1]);ax.set_ylabel('Response composition' if f=='cash' else '');label(ax,letter,f.title())
    handles=[plt.Rectangle((0,0),1,1,color=c) for c in bincols];fig.legend(handles,bins,ncol=3,loc='lower center',bbox_to_anchor=(.53,.04),frameon=False,fontsize=7);fig.text(.54,.2,'Randomized transfer amount',ha='center',fontsize=8);save(fig,'ED5_full_distribution')
    source(allx[allx.target.isin(['cash','rc'])],'ED6_allx_detailed_source.csv','Extended Data6','approved scalar interactions per R SD, factor omnibus raw p at x=0 solely for display; no new standardization, ranking or threshold selection');fig,axes=setup(3,118,2);fig.subplots_adjust(top=.9,bottom=.13,left=.09,wspace=.38,hspace=.5)
    for i,target in enumerate(['cash','rc']):
        for j,y in enumerate(Y):
            ax=axes[i*3+j];g=allx[(allx.target==target)&(allx.outcome==y)&allx.status.eq('ok')];numeric=g[g.kind.ne('categorical')];categorical=g[g.kind.eq('categorical')]
            for origin,marker in [('raw','o'),('constructed','^')]:
                gg=numeric[numeric.origin.eq(origin)];ax.scatter(gg.estimate,-np.log10(gg.p),s=10,marker=marker,facecolors='#7A7A7A' if origin=='constructed' else 'white',edgecolors='#7A7A7A',linewidths=.5,alpha=.65)
            ax.scatter(np.zeros(len(categorical)),-np.log10(categorical.p),s=12,marker='D',facecolors='white',edgecolors='#333333',linewidths=.5);ax.axvline(0,color='#cccccc',lw=.6);ax.set_ylim(0,2.3);ax.xaxis.set_major_locator(MaxNLocator(3));ax.set_xlabel('Scalar interaction per R SD');ax.set_ylabel('-log10(raw p)' if j==0 else '');label(ax,chr(65+i*3+j),('Cash' if target=='cash' else 'RC')+' / '+y.title());ax.text(.03,.93,'0 / 150: BH q < 0.10',transform=ax.transAxes,fontsize=6.7,color='#333333')
    fig.text(.54,.035,'Raw: open circles; constructed: filled triangles; factor omnibus: diamonds at x=0 (no signed effect).',ha='center',fontsize=6.7,color=COLORS['neutral']);save(fig,'ED6_allx_detailed')

def contact_sheet():
    names=['fig1_three_outcomes','fig2_cash_restricted_puzzle','fig3_distribution_anatomy','fig4_observables_null'];writer=PdfWriter()
    for name in names:writer.append(str(ROOT/(name+'.pdf')))
    with open(ROOT/'main_figures_combined.pdf','wb') as stream:writer.write(stream)
    canvas=Image.new('RGB',(2400,1400),'white');draw=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',32)
    for i,name in enumerate(names):
        img=Image.open(ROOT/(name+'.png')).convert('RGB');img=img.resize((1100,round(img.height*1100/img.width)),Image.Resampling.LANCZOS);x=50+(i%2)*1200;y=45+(i//2)*680;draw.text((x,y),'FIGURE '+str(i+1),font=font,fill='#333333');canvas.paste(img,(x,y+55))
    canvas.save(ROOT/'main_figures_contact_sheet.png');qa=ROOT/'qa';qa.mkdir(exist_ok=True);ImageOps.grayscale(canvas).save(qa/'contact_sheet_grayscale.png')
    # A 180mm figure reduced by50% is89-90mm; physical PNG DPI remains explicit.
    for name in names:
        im=Image.open(ROOT/(name+'.png'));im.resize((im.width//2,im.height//2),Image.Resampling.LANCZOS).save(qa/(name+'_89mm.png'),dpi=(600,600))

def run():
    ROOT.mkdir(exist_ok=True);tables={key:read(key) for key in SOURCE_NAMES};main_curves(tables['cells'],tables['pooled'],tables['thresholds']);null_figure(tables['allx'],tables['families'],tables['groups']);extended(tables['distribution'],tables['threshold_profile'],tables['relative'],tables['specification'],tables['yuan'],tables['allx']);contact_sheet();pd.DataFrame(AUDIT).to_csv(ROOT/'plot_statistic_audit.csv',index=False)
    for key,info in INPUTS.items():assert hashlib.sha256((RESULTS.parent/info['path']).read_bytes()).hexdigest()==info['sha256'],key+' source modified'
    (ROOT/'source_manifest.json').write_text(json.dumps(dict(inputs=INPUTS,outputs=EXPORTS,no_raw_data_read=True,no_model_fitting=True,font='Arial',page_width_mm=180,png_dpi=600),indent=2),encoding='utf-8');print('Produced four main, six extended, combined PDF and contact sheet from eleven frozen aggregate inputs.',flush=True)

if __name__=='__main__':run()
