"""Source fidelity, vector/export validation and Poppler PDF proofs; no estimation."""
from pathlib import Path
import json,hashlib,subprocess,shutil,ast
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from pypdf import PdfReader
from PIL import Image,ImageDraw,ImageFont
from plot_figures import ROOT,RESULTS,SOURCE_NAMES

def run():
    checks=[]
    def check(name,condition):
        assert condition,name;checks.append(name);print('PASS',name,flush=True)
    manifest=json.loads((ROOT/'source_manifest.json').read_text())
    for key,m in manifest['inputs'].items():check('unchanged approved input '+key,hashlib.sha256((RESULTS.parent/m['path']).read_bytes()).hexdigest()==m['sha256'])
    def prior(key):folder,name=SOURCE_NAMES[key];return pd.read_csv(RESULTS/folder/name)
    f1=pd.read_csv(ROOT/'figure1_main_source.csv');cells=prior('cells');pooled=prior('pooled')
    check('Figure1 exactly1x3 source27 randomized cell rows',len(f1)==27 and f1.groupby('panel').size().eq(9).all() and not f1.duplicated(['outcome','form','amount']).any())
    for r in f1.itertuples():
        g=cells[(cells.form==r.form)&(cells.amount==r.amount)].iloc[0]
        if r.outcome=='ordinal':expected=[g.ordinal_mean,g.ordinal_mean-1.96*g.ordinal_se,g.ordinal_mean+1.96*g.ordinal_se]
        else:
            p=pooled[(pooled.outcome==r.outcome)&(pooled.form==r.form)&(pooled.amount==r.amount)].iloc[0];expected=[p.estimate,p.lo,p.hi]
        check('Fig1 '+r.outcome+'/'+r.form+'/'+str(r.amount)+' approved number/CI/N',np.allclose([r.estimate,r.lower_ci,r.upper_ci],expected,rtol=0,atol=1e-14) and r.N==g.N)
    f2=pd.read_csv(ROOT/'figure2_main_source.csv');check('Figure2 exactly12 Cash/derived rows',len(f2)==12 and set(f2.form)=={'cash','restricted'})
    for r in f2.itertuples():
        p=pooled[(pooled.outcome==r.outcome)&(pooled.form==r.form)&(pooled.amount==r.amount)].iloc[0];check('Fig2 '+r.outcome+'/'+r.form+'/'+str(r.amount)+' unchanged approved CI',np.allclose([r.estimate,r.lower_ci,r.upper_ci],[p.estimate,p.lo,p.hi],rtol=0,atol=1e-14))
        if r.form=='restricted':
            v=pooled[(pooled.outcome==r.outcome)&pooled.form.isin(['food','medical'])&pooled.amount.eq(r.amount)].estimate;check('equal-weight mixture not pooled-N weighting '+r.outcome+'/'+str(r.amount),np.isclose(r.estimate,.5*v.sum(),atol=1e-14) and r.arm_type=='derived equal-weight contrast')
    f3=pd.read_csv(ROOT/'figure3_main_source.csv');thresholds=prior('thresholds');check('Figure3 eighteen source rows',len(f3)==18)
    for r in f3.itertuples():
        p=(thresholds[(thresholds.threshold=='any_spending')&(thresholds.form==r.form)&(thresholds.amount==r.amount)].iloc[0] if r.outcome=='any_spending' else pooled[(pooled.outcome=='top75')&(pooled.form==r.form)&(pooled.amount==r.amount)].iloc[0]);vals=[p.probability,p.lo,p.hi] if r.outcome=='any_spending' else [p.estimate,p.lo,p.hi];check('Fig3 '+r.outcome+'/'+r.form+'/'+str(r.amount)+' approved curves',np.allclose([r.estimate,r.lower_ci,r.upper_ci],vals,rtol=0,atol=1e-14))
    allx=prior('allx');f4=pd.read_csv(ROOT/'figure4_main_source.csv');check('all900 primary X tests retained with failures',len(f4)==900 and f4.status.eq('nonestimable').sum()==24)
    merged=f4.merge(allx,on=['variable','outcome','target'],suffixes=('_new','_old'),validate='one_to_one')
    for field in ['estimate','lo','hi','p','q','holm_p','N']:check('Figure4 unchanged '+field,np.allclose(merged[field+'_new'],merged[field+'_old'],equal_nan=True,rtol=0,atol=1e-14))
    fam=prior('families');check('six minima exact and none corrected',len(fam)==6 and fam.BH_q_lt10.eq(0).all() and (fam.min_q>=.1).all())
    files={'ED1_threshold_profile_source.csv':('threshold_profile',5),'ED2_relative_scales_source.csv':('relative',21),'ED3_specification_curve_source.csv':('specification',60),'ED4_share_yuan_source.csv':('yuan',12),'figureS_distribution_source.csv':('distribution',9),'ED6_allx_detailed_source.csv':('allx',900)}
    for name,(key,n) in files.items():
        new=pd.read_csv(ROOT/name);old=prior(key)
        if key=='allx':old=old[old.target.isin(['cash','rc'])].reset_index(drop=True)
        check(name+' exact row count',len(new)==n)
        for field in old.columns:
            if pd.api.types.is_numeric_dtype(old[field]):check(name+' unchanged numeric '+field,np.allclose(new[field],old[field],equal_nan=True,rtol=0,atol=1e-14))
            else:check(name+' unchanged coding '+field,new[field].fillna('').astype(str).to_list()==old[field].fillna('').astype(str).to_list())
    dist=pd.read_csv(ROOT/'figureS_distribution_source.csv');check('nine full six-bin compositions sum100%',np.allclose(dist[['p'+str(i) for i in range(1,7)]].sum(axis=1),1,atol=1e-14))
    names=['fig1_three_outcomes','fig2_cash_restricted_puzzle','fig3_distribution_anatomy','fig4_observables_null','ED1_threshold_profile','ED2_relative_scales','ED3_specification_curve','ED4_share_yuan','ED5_full_distribution','ED6_allx_detailed'];qa=ROOT/'qa';qa.mkdir(exist_ok=True)
    poppler=shutil.which('pdftoppm');check('Poppler PDF renderer available',poppler is not None)
    for name in names:
        pdf=PdfReader(ROOT/(name+'.pdf'));check(name+' one vector180mm page',len(pdf.pages)==1 and abs(float(pdf.pages[0].mediabox.width)*25.4/72-180)<.03 and len(pdf.pages[0].images)==0 and len(pdf.pages[0].extract_text())>40)
        png=Image.open(ROOT/(name+'.png'));check(name+'600dpi at180mm width',abs(png.width-180/25.4*600)<2 and abs(png.info['dpi'][0]-600)<1)
        svg=(ROOT/(name+'.svg')).read_text(encoding='utf-8');check(name+' editable vector SVG text', '<text' in svg and '<image' not in svg and ET.fromstring(svg).tag.endswith('svg'))
        subprocess.run([poppler,'-r','150','-singlefile','-png',str(ROOT/(name+'.pdf')),str(qa/(name+'_pdf'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    combined=PdfReader(ROOT/'main_figures_combined.pdf');check('combined four pages preserve vector contents',len(combined.pages)==4 and all(combined.pages[i].get_contents().get_data()==PdfReader(ROOT/(names[i]+'.pdf')).pages[0].get_contents().get_data() for i in range(4)))
    subprocess.run([poppler,'-r','120','-png',str(ROOT/'main_figures_combined.pdf'),str(qa/'combined')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    # Compact proof of all four pages in the combined file.
    proof=Image.new('RGB',(2200,1400),'white');draw=ImageDraw.Draw(proof);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26)
    for i in range(4):
        im=Image.open(qa/('combined-'+str(i+1)+'.png')).convert('RGB');im=im.resize((1000,round(im.height*1000/im.width)));x=50+(i%2)*1100;y=35+(i//2)*680;draw.text((x,y),'Combined PDF page '+str(i+1),font=font,fill='black');proof.paste(im,(x,y+45))
    proof.save(qa/'combined_pdf_proof.png')
    audit=pd.read_csv(ROOT/'plot_statistic_audit.csv');check('all ten figures have row-level source audit',audit.figure.str.startswith('Figure').any() and audit.figure.str.startswith('Extended').any() and audit.source_file.notna().all() and audit.source_row.ge(1).all() and audit.source_commit.str.len().eq(40).all())
    tree=ast.parse((ROOT/'plot_figures.py').read_text(encoding='utf-8'));imports=[node.module for node in ast.walk(tree) if isinstance(node,ast.ImportFrom)]+[alias.name for node in ast.walk(tree) if isinstance(node,ast.Import) for alias in node.names];check('plotter no estimator/raw-data imports',not any(str(m).startswith(('statsmodels','sklearn','size_curve','who_drives','screen')) for m in imports) and 'read_stata' not in (ROOT/'plot_figures.py').read_text(encoding='utf-8'))
    for path in ROOT.glob('*.csv'):check(path.name+' aggregate-only schema',not set(pd.read_csv(path).columns)&{'id','respondent_id','fold_id','individual_prediction','scen_mpc','cate_oof'})
    result=dict(status='passed',checks=checks,assertions=len(checks),rendered_pdf_pages=14,manual_visual_review='recorded separately in FIGURE_AUDIT.md; automated checks do not assert manual approval')
    (ROOT/'verification_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('ALL',len(checks),'CHECKS PASSED',flush=True)

if __name__=='__main__':run()
