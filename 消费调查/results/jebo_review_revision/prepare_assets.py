import argparse,re,shutil
from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
from matplotlib.colors import to_hex
p=argparse.ArgumentParser();p.add_argument('--data',required=True);a=p.parse_args()
M=ROOT/'manuscript'/'jebo_v3';M.mkdir(parents=True,exist_ok=True);(M/'figures').mkdir(exist_ok=True);(M/'source_data').mkdir(exist_ok=True)
opts=pd.read_csv(O/'questionnaire_options.csv')
bottom={'cash':'Essentially no additional consumption (almost all the money saved because of the cash transfer is put into savings or used to repay debt)', 'food':'Essentially no additional consumption (use the voucher to buy items originally planned, and save the freed cash or repay debt)', 'medical':'Essentially no additional consumption (use the subsidy to pay originally planned medical expenses, and save the freed cash or repay debt)'}
for i,r in opts.iterrows():
    t=int(r.amount);k=int(r.category)
    words={2:f'A small part of the subsidy, approximately below 10% (approximately RMB 0–{t*.1:g})',3:f'A part of the subsidy, approximately 10–25% (approximately RMB {t*.1:g}–{t*.25:g})',4:f'About half of the subsidy, approximately 25–50% (approximately RMB {t*.25:g}–{t*.5:g})',5:f'Most of the subsidy, approximately 50–75% (approximately RMB {t*.5:g}–{t*.75:g})',6:f'Almost all of the subsidy, approximately above 75% (approximately RMB {t*.75:g}–{t:g})'}
    opts.loc[i,'english']=bottom[r.form] if k==1 else words[k]
save(opts,'questionnaire_options.csv')
app=(O/'QUESTIONNAIRE_APPENDIX.md').read_text(encoding='utf8');parts=re.split(r'(?=## 版本 \d+)',app);pre=parts[0].split('English common instruction:')[0].rstrip()+'\n'
pre+='\nEnglish common instruction: Read a short hypothetical scenario and answer according to your true thoughts. The scenario is used only for academic research; there are no correct or incorrect answers. Select what you would most likely do in a similar situation. System randomization selects one of nine versions (three forms by three amounts), and each respondent answers only that version; the other eight data columns are empty.\n\n'
for j,part in enumerate(parts[1:]):
    part=part[:part.index('English scenario:')]
    t=int(AMOUNTS[j%3]);f=FORMS[j//3]
    scenario={'cash':f'Suppose the government gives you a one-time cash subsidy of RMB {t:,}, paid directly into your bank account or WeChat/Alipay. Its use is unrestricted; you can spend it, save it, or repay debt.', 'food':f'Suppose the government gives you a one-time electronic consumption voucher worth RMB {t:,}, usable only for food and daily necessities at supermarkets, food markets, convenience stores and similar outlets. It is valid for six months, cannot be cashed out, and cannot be used for other purposes.', 'medical':f'Suppose the medical-insurance authority credits RMB {t:,} to your medical-insurance personal account. The funds remain valid over the long term and can accumulate as a balance. They can be used for medical-related expenses for you and your family, including consultations, medicines, health checks, rehabilitation and nursing care. They cannot be cashed out or used for nonmedical consumption.'}[f]
    pre+=part+'English scenario: '+scenario+'\n\nEnglish question: After receiving this '+{'cash':'cash subsidy','food':'voucher','medical':'medical subsidy'}[f]+f' of RMB {t:,}, by how many yuan do you expect your TOTAL consumption to exceed your original plan?\n\n'
    pre+='\n\n'.join(str(r.category)+'. '+r.english for r in opts[(opts.form==f)&(opts.amount==t)].itertuples())+'\n\n'
note('QUESTIONNAIRE_APPENDIX.md',pre)
d=load(a.data);reader=pd.io.stata.StataReader(a.data,convert_categoricals=False);vl=reader.value_labels()
labels=[]
for var in ['q28_hhsize','q29_foodexp','q46_income','q43_edu','q41_gender','q24_workstat','q23_hukou','q49_citytier']:
    for code,label in vl[reader._lbllist[reader._varlist.index(var)]].items():labels.append(dict(variable=var,code=int(code),label_chinese=label))
save(labels,'baseline_value_labels.csv')
local=Path(a.data).parent/'JEBO_Manuscript_v2_SubmissionReady.docx'
from docx import Document
quotes=[p.text for p in Document(local).paragraphs if any(k in p.text for k in ['exactly in the direction predicted','Transfer Size and Spendability','mechanism funnel','establishes an important feature'])]
note('LOCAL_V2_CLAIM_AUDIT.md','# Read-only local v2 audit\n\nSHA256 '+hashlib.sha256(local.read_bytes()).hexdigest()+'\n\n'+ '\n\n'.join(quotes)+'\n\nThese quotations establish the specific sign/measurement/spendability problems in local v2. The earlier repository v1 already uses some qualified candidate language; the response does not invent an identical sentence in v1. Neither source draft was overwritten.')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
colors=['#233f55','#667f8e','#acb6bc'];names=['Cash','Food','Medical'];cell=pd.read_csv(O/'adult_share_yuan_table.csv')
def finish(fig,name):
    fig.savefig(M/'figures'/(name+'.png'),dpi=300,bbox_inches='tight');fig.savefig(M/'figures'/(name+'.pdf'),bbox_inches='tight');plt.close(fig)
# Sequential grayscale/blue category shades, consistently low to high.
fig,axes=plt.subplots(1,3,figsize=(10.5,3.7),sharey=True);shades=[to_hex(plt.cm.Blues(x)) for x in np.linspace(.15,.9,6)]
for fi,ax in enumerate(axes):
    x=cell[cell.form==FORMS[fi]];left=np.zeros(3)
    for k in range(1,7):
        vals=x['share'+str(k)].to_numpy()*100;ax.barh(np.arange(3),vals,left=left,color=shades[k-1],edgecolor='white',height=.62,label=['Bottom','<10%','10–25%','25–50%','50–75%','>75%'][k-1]);left+=vals
    ax.set_title(names[fi]);ax.set_yticks(range(3),['RMB 200','RMB 1,000','RMB 5,000']);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Respondents (%)')
fig.legend(*axes[0].get_legend_handles_labels(),ncol=6,loc='lower center',bbox_to_anchor=(.5,-.03),frameon=False);fig.tight_layout(rect=[0,.07,1,1]);finish(fig,'fig1_response_atlas')
fig,axes=plt.subplots(1,2,figsize=(10.5,4.3));fit=pd.read_csv(O/'affine_midpoint_fit.csv')
for fi in range(3):
    x=cell[cell.form==FORMS[fi]];a0=x.amount.to_numpy();s=x.midpoint.to_numpy();lo=x.midpoint_lo.to_numpy();hi=x.midpoint_hi.to_numpy()
    axes[0].errorbar(a0,s*100,yerr=np.vstack([s-lo,hi-s])*100,marker='o',capsize=3,color=colors[fi],label=names[fi])
    axes[1].errorbar(a0,x.yuan,yerr=np.vstack([x.yuan-x.yuan_lo,x.yuan_hi-x.yuan]),marker='o',capsize=3,color=colors[fi],label=names[fi])
    ff=fit[(fit.form==FORMS[fi])&(fit.model=='form_intercepts_slopes')];axes[1].plot(ff.amount,ff.predicted_yuan,ls='--',color=colors[fi],alpha=.65)
axes[0].set_xscale('log');axes[0].set_ylim(10,31);axes[0].set_ylabel('Midpoint-coded share (%)');axes[1].set_ylim(0,1200);axes[1].set_ylabel('Midpoint-implied additional yuan')
for ax in axes:ax.set_xticks(AMOUNTS,['200','1,000','5,000']);ax.xaxis.set_minor_locator(NullLocator());ax.set_xlabel('Transfer amount (RMB)');ax.legend(frameon=False)
fig.tight_layout();finish(fig,'fig2_share_and_yuan')
inc=pd.read_csv(O/'incremental_yuan_response.csv');fig,ax=plt.subplots(figsize=(8,4.2))
for fi in range(3):
    x=inc[(inc.form==FORMS[fi])&(inc.contrast=='within-form')];pos=np.arange(2)+(fi-1)*.13;e=x.estimate.to_numpy()
    ax.errorbar(pos,e,yerr=np.vstack([e-x.bootstrap_lo,x.bootstrap_hi-e]),marker='o',ls='none',capsize=4,color=colors[fi],label=names[fi])
ax.set_xticks([0,1],['RMB 200 to 1,000','RMB 1,000 to 5,000']);ax.set_ylim(.12,.28);ax.set_ylabel('Incremental implied yuan per transfer yuan');ax.legend(frameon=False,ncol=3);fig.tight_layout();finish(fig,'fig3_incremental_response')
food=pd.read_csv(O/'food_bindingness_raw_cells.csv');fig,axes=plt.subplots(1,2,figsize=(10.5,4.2),sharey=True)
for g,ax in enumerate(axes):
    for fi,f in enumerate(['cash','food']):
        x=food[(food.G==g)&(food.form==f)];pr=x.top75.to_numpy();se=np.sqrt(pr*(1-pr)/x.N)
        ax.errorbar(x.amount,pr*100,yerr=1.96*se*100,marker='o',capsize=3,color=colors[fi],label=names[fi])
    ax.set_xscale('log');ax.set_xticks(AMOUNTS,['200','1,000','5,000']);ax.xaxis.set_minor_locator(NullLocator());ax.set_xlabel('Transfer amount (RMB)');ax.set_title(['G = 0 fails lower-bound proxy','G = 1 passes lower-bound proxy'][g]);ax.set_ylim(-2,25);ax.legend(frameon=False)
axes[0].set_ylabel('Highest-category responses (%)');fig.tight_layout();finish(fig,'fig4_food_raw_cells')
for fn in ['adult_cell_distribution.csv','adult_share_yuan_table.csv','affine_midpoint_fit.csv','incremental_yuan_response.csv','food_bindingness_raw_cells.csv']:shutil.copyfile(O/fn,M/'source_data'/fn)
print('Four figures and exact translated questionnaire prepared; local v2 unchanged.')
