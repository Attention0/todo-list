from pathlib import Path
import json,re,hashlib,zipfile
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from docx import Document
from lxml import etree
O=Path(__file__).resolve().parent;M=O.parent.parent/'manuscript'/'nc_v5'
checks={}
def ok(k,condition):
    assert bool(condition),k
    checks[k]=True
def read(n):return pd.read_csv(O/n)
s=read('scientific_family21.csv')
ok('two samples with exactly21 scientific tests',len(s)==42 and s.groupby('sample').size().eq(21).all())
for sample,g in s.groupby('sample'):
    ok(sample+' Holm recomputed',np.allclose(g.holm21,multipletests(g.p,method='holm')[1]))
    q=g[g.test!='omnibus'];ok(sample+' interval and P algebra',np.allclose(q.p,2*stats.norm.sf(abs(q.estimate/q.se))) and np.allclose(q.lo,q.estimate-1.96*q.se))
dist=read('distribution.csv');ok('all cell category sums',np.allclose(dist.groupby(['sample','form','amount']).share.sum(),1) and dist.groupby(['sample','form','amount'])['count'].sum().equals(dist.groupby(['sample','form','amount']).N.first()))
ok('adult and full Ns',dist[dist['sample']=='A']['count'].sum()==5480 and dist[dist['sample']=='R']['count'].sum()==5497)
pr=read('profiles.csv');con=read('form_contrasts.csv');errors=[];varerrors=[]
for r in con.itertuples():
    x=pr[(pr['sample']==r.sample)&(pr.outcome=='top75')&(pr.amount==r.amount)].set_index('form');f=r.test.split('-')[0];a=x.loc[f];c=x.loc['cash'];errors.append(abs(r.estimate-(a.estimate-c.estimate)))
    v=sum(z.estimate*(1-z.estimate)*z.N/(z.N-1)**2 for z in [a,c]);varerrors.append(abs(r.se*r.se-v))
ok('saturated form effects independently recover cell means and HC3',max(errors)<1e-12 and max(varerrors)<1e-12)
me=read('mechanism_tests.csv');md=read('mechanism_details.csv');g0=md[md.test=='Food-Cash slope G=0'].iloc[0];g1=md[md.test=='Food-Cash slope G=1'].iloc[0];tri=me[me.test=='inframarginal_triple1df'].iloc[0]
ok('disjoint subgroup triple contrast algebra',abs(tri.estimate-(g1.estimate-g0.estimate))<1e-12 and abs(tri.se**2-(g0.se**2+g1.se**2))<1e-12)
ok('seven diagnostic Holm tests',len(me)==7 and np.allclose(me.holm7,multipletests(me.p,method='holm')[1]))
cal=read('calibration_diagnostics.csv');cc=read('calibration_cells.csv');ok('population cap and targets',cal[cal.scheme=='cap10'].max_weight.iloc[0]<=10+1e-9 and np.allclose(cc.uncapped_share,cc.target_share) and len(cc)==12)
ok('calibration reports remaining target mismatch',cal[cal.scheme=='cap10'].max_abs_target_discrepancy.iloc[0]>.16)
cv=read('prediction_folds.csv');ok('all50 logistic CV fits converged',len(cv)==50 and cv.converged.all())
sim=read('simulation_results.csv');ok('3000 full refits and no failures',len(sim)==6 and sim.replicates.eq(1000).all() and sim.failed_refits.eq(0).all() and sim.calibration_draws.eq(999).all())
old=read('legacy_family_comparison.csv');old0=pd.read_csv(O.parent/'nc_revision_audit'/'specification_grid.csv');ok('historical1500 original P values reproduced',len(old)==1500 and np.allclose(old.legacy_maxnorm,old0.global_maxT_p))
ok('both extreme source counts',read('legacy_extreme_sources.csv').draw_count.sum()==5000 and read('legacy_maxnorm_extreme_sources.csv').draw_count.sum()==5000)
ok('frozen plan hash unchanged',hashlib.sha256((O/'freeze.json').read_bytes()).hexdigest()==json.loads((O/'verification.json').read_text())['freeze_sha256'])
for p in M.glob('*.docx'):
    d=Document(p);ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(p) as z:
        for n in ['word/document.xml','word/styles.xml']:
            root=etree.fromstring(z.read(n));ok(p.stem+n+' no paragraph borders',not root.xpath('//w:pBdr',namespaces=ns))
    for name in ['Title','Heading 1','Heading 2']:ok(p.stem+name+' black',str(d.styles[name].font.color.rgb)=='000000')
    ok(p.stem+' no unresolved build tokens',not any('{cite:' in q.text or '{figure' in q.text or '{table1}' in q.text for q in d.paragraphs))
d=Document(M/'NC_MPC_manuscript_v5.docx');txt='\n'.join(p.text for p in d.paragraphs);body=txt[:txt.index('References')]
ok('main figure first citation order',body.index('Figure 1')<body.index('Fig. 2')<body.index('Fig. 3a')<body.index('Fig. 3b'))
ok('supplement figure first citation order',body.index('Supplementary Fig. 1')<body.index('Supplementary Fig. 2'))
ok('author confirmation not silently removed',txt.count('[AUTHOR CONFIRMATION REQUIRED:')==3)
ok('no internal PR or audit log language in scientific prose',not re.search(r'\bPR\s*#?\d|audit log|feature/',body))
ok('all31 references cited in first occurrence order',set(json.loads((M/'reference_number_map.json').read_text()).values())==set(range(1,32)))
for p in O.glob('*.csv'):
    cols=set(pd.read_csv(p,nrows=0).columns);ok(p.name+' aggregate column privacy',not cols.intersection({'id','respondent_id','phone','email','name','fold_assignment','prediction_individual'}))
(O/'package_verification.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'document_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in M.glob('*.docx')},'limitations':['No recruitment or ethics documents supplied','Gaussian minP asymptotic, not exact','Weighting does not confer population representativeness','Metadata not full-text validation','Visual QA recorded separately']},indent=2),encoding='utf8')
print(f'{len(checks)} checks passed')
