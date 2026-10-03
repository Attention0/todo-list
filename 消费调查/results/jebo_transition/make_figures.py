"""Presentation only: adapt approved PR14 geometry to PR16 adult aggregates."""
from pathlib import Path
import importlib.util,json,hashlib
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parent;P=O.parent/'nc_evidence_revision';F=O.parents[1]/'manuscript'/'jebo_v1'/'figures';F.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('hero',O.parent/'mpc_hero_figure'/'plot_hero.py');hero=importlib.util.module_from_spec(spec);spec.loader.exec_module(hero)
hero.OUT=F;hero.BIN_LABELS[0]='Essentially\nno increase'
hero.TREATMENT=['#111111','#407c9e','#94aebd'] # approved NCv5 curve palette
def save(fig,name):
 name='fig1_atlas' if name=='hero_figure' else name
 for ext in ['png','pdf','svg']:
  path=F/(name+'.'+ext);fig.savefig(path,dpi=400,bbox_inches='tight')
  if ext=='svg':path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf8').splitlines())+'\n',encoding='utf8')
 plt.close(fig)
hero.save=save
d=pd.read_csv(P/'distribution.csv');d=d[d['sample']=='A'];p=pd.read_csv(P/'profiles.csv');p=p[p['sample']=='A'];rows=[]
for ix,r in d.iterrows():rows.append(dict(panel='A',statistic='category_share',form=r.form,amount=r.amount,category=r.category,estimate=r.share,lower_ci=np.nan,upper_ci=np.nan,N=r.N,sample='A',source_file='nc_evidence_revision/distribution.csv',source_row=ix+1))
for ix,r in p[p.outcome=='midpoint'].iterrows():rows.append(dict(panel='B',statistic='midpoint_mean',form=r.form,amount=r.amount,category=np.nan,estimate=r.estimate,lower_ci=r.lo,upper_ci=r.hi,N=r.N,sample='A',source_file='nc_evidence_revision/profiles.csv',source_row=ix+1))
s=pd.DataFrame(rows);s.to_csv(F/'fig1_source.csv',index=False);hero.hero_figure(s)
plt.rcParams.update({'font.family':'Arial','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
for name,outs,labels,lims in [('fig2_curves',['ordinal','midpoint'],['Ordinal response score (1–6)','Midpoint-coded share (%)'],[(2.2,3.15),(10,29)]),('fig3_margins',['any_spending','top75'],['Positive-category response (%)','Highest-category response (%)'],[(50,82),(0,18)])]:
 fig,axes=plt.subplots(1,2,figsize=(9,4.1),layout='constrained')
 used=[]
 for j,(ax,y,label,lim) in enumerate(zip(axes,outs,labels,lims)):
  for i,f in enumerate(hero.FORMS):
   g=p[(p.form==f)&(p.outcome==y)].sort_values('amount');assert len(g)==3,(name,y)
   k=1 if y=='ordinal' else 100
   ax.errorbar(np.arange(3)+(i-1)*.025,g.estimate*k,yerr=np.vstack([(g.estimate-g.lo)*k,(g.hi-g.estimate)*k]),color=hero.TREATMENT[i],marker=hero.MARKERS[i],capsize=3,label=f.title(),lw=1.5)
   used.extend(dict(r,source_row=ix+1,source_file='nc_evidence_revision/profiles.csv') for ix,r in g.iterrows())
  ax.set_xticks(range(3),['200','1,000','5,000']);ax.set_xlabel('Transfer amount (RMB)');ax.set_ylabel(label);ax.set_ylim(*lim);ax.set_title(('A  ' if j==0 else 'B  ')+label,loc='left',fontsize=10);ax.grid(axis='y',color='#eeeeee',lw=.6)
 axes[0].legend(frameon=False,fontsize=9,loc='best');save(fig,name);pd.DataFrame(used).to_csv(F/(name+'_source.csv'),index=False)
(F/'FIGURE_PROVENANCE.md').write_text('''# Figure provenance

All main figures use PR16 adult sample A (N=5,480), not the earlier full sample. Figure1 calls the PR14 Hero drawing function with approved adult bin frequencies and midpoint means. Atlas geometry and six ordered light-to-dark swatches are preserved; curve colors use the approved NCv5 palette consistently across figures. The lowest-category legend is clarified as essentially no increase. Mean intervals are the approved PR16 pointwise95% normal intervals, not the earlier PR14 bootstrap intervals. Figures2/3 reuse the approved curve/error-bar grammar, with no new estimator or threshold.

Lines join three independent randomized groups at log-even amounts. Figure-source CSVs carry exact source rows; no respondent data used. PNG/PDF/SVG outputs are supplied. No fourth main or decomposition figure is created: decomposition is Table3.
''',encoding='utf8')
print('3 adult figures generated')
