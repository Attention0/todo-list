"""Independent validation of specified results, not additional empirical exploration."""
import argparse,re,subprocess,importlib.metadata as meta
import statsmodels.api as sm
from common import *
p=argparse.ArgumentParser();p.add_argument('--data',required=True);a=p.parse_args();d=load(a.data)
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(check=name,passed=bool(ok),detail=detail));assert ok,(name,detail)
M=ROOT/'manuscript'/'jebo_v3';hist=json.loads((O/'historical_hashes.json').read_text())
check('Historical hashes',all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in hist.items()),str(len(hist))+' archived files')
manifest=subprocess.check_output(['git','show','0aa5681:'+str((O/'REVIEWER_REANALYSIS_MANIFEST.md').relative_to(ROOT.parent)).replace('\\','/')],cwd=ROOT.parent)
check('First-commit protocol unchanged',manifest==(O/'REVIEWER_REANALYSIS_MANIFEST.md').read_bytes())
check('Exact base ancestry',subprocess.call(['git','merge-base','--is-ancestor','926b05022189661bdfe4dc41d24ad900c77bbd12','HEAD'],cwd=ROOT.parent)==0)
check('Branch',subprocess.check_output(['git','branch','--show-current'],cwd=ROOT.parent).decode().strip()=='feature/jebo-review-revision')
cc=np.array([[int(((d.cell==j)&(d.ordinal==k)).sum()) for k in range(1,7)] for j in range(9)])
check('54 raw adult counts',np.array_equal(cc,counts()) and cc.sum()==5480)
cells=pd.read_csv(O/'adult_share_yuan_table.csv');check('Share-yuan identity',np.max(abs(cells.yuan-cells.midpoint*cells.amount))<1e-9)
check('Raw category sums',all(sum(cells['count'+str(k)][j] for k in range(1,7))==cells.N[j] for j in range(9)))
inc=pd.read_csv(O/'incremental_yuan_response.csv');e=[]
for f in FORMS:
    x=cells[cells.form==f];e.extend(np.diff(x.yuan)/np.diff(x.amount))
check('All6 increments',np.allclose(e,inc[inc.contrast=='within-form'].estimate,atol=1e-12))
pair=inc[inc.contrast!='within-form'];check('Increment Holm6',np.allclose(holm(pair.p),pair.holm6))
el=pd.read_csv(O/'endpoint_elasticity.csv');check('Endpoint elasticities',np.allclose([np.log(x.yuan.iloc[-1]/x.yuan.iloc[0])/np.log(25) for f in FORMS for x in [cells[cells.form==f]]],el.iloc[:3].estimate))
# All21 slopes and their complete cross-outcome covariance independently from rows.
F=np.eye(3)[d.form.map(dict(zip(FORMS,range(3))))];X=np.column_stack([F,F*(d.z.to_numpy()+1)[:,None]])
bread=np.linalg.inv(X.T@X);YY=d[OUTCOMES].to_numpy();bb=bread@X.T@YY;h=np.einsum('ij,jk,ik->i',X,bread,X)
U=((YY-X@bb)/(1-h[:,None]))[:,:,None]*(X@bread[:,3:])[:,None,:];V=U.reshape(len(d),21).T@U.reshape(len(d),21)
frozen=json.loads((O/'family42_covariance.json').read_text());check('Full42 cross-outcome covariance',np.allclose(V,frozen['covariance'],atol=1e-12),str(float(np.max(abs(V-np.array(frozen['covariance']))))))
check('All21 form slopes',np.allclose(bb[3:,:].T.ravel(),frozen['estimates'],atol=1e-12))
fam=pd.read_csv(O/'scientific_family42.csv');check('Exact42 family',len(fam)==42 and fam.groupby('outcome').size().eq(6).all() and len(fam.outcome.unique())==7)
check('Holm42',np.allclose(holm(fam.p),fam.holm42,atol=1e-12))
old=pd.read_csv(PRIOR/'scientific_family21.csv');old=old[old['sample']=='A'];joined=old.merge(fam,on=['sample','outcome','test'],suffixes=('_old','_new'));check('Historical21 estimands unchanged',len(joined)==21 and np.max(abs(joined.p_old-joined.p_new))<1e-11)
val,vec=np.linalg.eigh(np.array(frozen['covariance']));sim=np.random.default_rng(2026100419).normal(size=(10000,21))@(vec*np.sqrt(np.maximum(val,0))[None,:]).T
ps=[]
for j in range(7):
    u=sim[:,3*j:3*j+3];vv=V[3*j:3*j+3,3*j:3*j+3];ct=np.array([[1,-1,0],[1,0,-1]]);du=u@ct.T;dv=ct@vv@ct.T
    ps+=[2*stats.norm.sf(abs(u[:,k])/np.sqrt(vv[k,k])) for k in range(3)];ps+=[stats.chi2.sf(np.einsum('bi,ij,bj->b',du,np.linalg.inv(dv),du),2)];ps+=[2*stats.norm.sf(abs(du[:,k])/np.sqrt(dv[k,k])) for k in range(2)]
minimum=np.column_stack(ps).min(1);adj=(1+(minimum[:,None]<=fam.p.to_numpy()).sum(0))/10001
check('minP42 independent regeneration',np.allclose(adj,fam.minP42,atol=1e-12),'Row-level covariance independently agrees; canonical stored eigensystem fixes the nonunique basis in this rank-deficient covariance for exact seeded reproduction.')
si=pd.read_csv(O/'family42_simultaneous_intervals.csv');z=stats.norm.ppf(1-.05/(2*42));check('Bonferroni42 scalar intervals',len(si)==35 and np.allclose(si.sim_lo,si.estimate-z*si.se) and np.allclose(si.sim_hi,si.estimate+z*si.se))
aff=pd.read_csv(O/'affine_midpoint_parameters.csv');d['ty']=d.midpoint*d.amount;Fx=np.eye(3)[d.form.map(dict(zip(FORMS,range(3))))];tx=d.amount.to_numpy()/1000;xa=np.column_stack([Fx,Fx*tx[:,None]]);m=sm.OLS(d.ty,xa).fit(cov_type='HC3')
rr=aff[(aff.model=='form_intercepts_slopes')&~aff.parameter.str.contains('-')];fac=np.array([1,1,1,.001,.001,.001]);check('Midpoint affine respondent HC3',np.allclose(rr.estimate,m.params*fac) and np.allclose(rr.se,m.bse*fac))
cal=pd.read_csv(O/'interval_affine_fit.csv');check('All180 interval probabilities',len(cal)==180 and np.allclose(cal.groupby(['model','form','amount']).predicted_probability.sum(),1))
bs=pd.read_csv(O/'interval_bootstrap_status.csv');check('Interval8000 fits',len(bs)==8000 and bs.converged.all() and bs.groupby('model').size().eq(4000).all())
check('Conditional interval mapping disclosed','right censoring' in (O/'QUESTION_INTERVAL_AUDIT.md').read_text(encoding='utf8') and 'No numerical separation' in (O/'QUESTION_INTERVAL_AUDIT.md').read_text(encoding='utf8'))
food=pd.read_csv(O/'food_bindingness_raw_cells.csv');check('All12 Food cells',len(food)==12 and food.N.sum()==3621 and np.allclose(food[['share'+str(k) for k in range(1,7)]].sum(1),1))
sign=pd.read_csv(O/'food_bindingness_sign_reproduction.csv');check('Food sign and triple',sign.estimate.iloc[0]>0 and sign.estimate.iloc[1]>0 and np.isclose(sign.estimate.iloc[2],sign.estimate.iloc[1]-sign.estimate.iloc[0]))
con=pd.concat([pd.read_csv(O/'food_bindingness_continuous.csv'),pd.read_csv(O/'food_bindingness_adjusted.csv')]);check('Continuous family6',len(con)==6 and np.allclose(con.holm6,holm(con.p)))
rat=pd.read_csv(O/'food_bindingness_ratio.csv');check('Ratio full2df family6',len(rat)==6 and rat.df.eq(2).all() and np.allclose(rat.holm6,holm(rat.p)))
led=pd.read_csv(O/'MECHANISM_PREDICTION_PRECISION_LEDGER.csv');scalar=led.dropna(subset=['se']);check('Scalar MDE formulas',np.allclose(scalar.MDE80_nominal,(stats.norm.ppf(.975)+stats.norm.ppf(.8))*scalar.se) and np.allclose(scalar.MDE80_family,(stats.norm.ppf(1-.05/(2*scalar.family_K))+stats.norm.ppf(.8))*scalar.se))
check('Baseline family8',len(pd.read_csv(O/'randomization_balance.csv'))==8)
opts=pd.read_csv(O/'questionnaire_options.csv');check('54 exact response translations',len(opts)==54 and not opts.english.str.contains('differs by form').any())
main=(M/'JEBO_manuscript_v3.md').read_text(encoding='utf8');supp=(M/'JEBO_supplement_v3.md').read_text(encoding='utf8')
check('Scientific workflow language removed',not re.search(r'\b(?:PR\s*#?\d+|GitHub|Work\.md|SPEC\.md|feature/|jebo_v\d)\b',main+supp,re.I))
check('Unmeasured title removed','spendab' not in main.splitlines()[0].lower() and 'spendab' not in main.split('## Abstract')[1].split('## 1 Introduction')[0].lower())
check('No fabricated ethics certification',not re.search(r'ethic\w* (?:was |were )?approved|obtained informed consent',main,re.I))
for fn in ['adult_cell_distribution.csv','adult_share_yuan_table.csv','affine_midpoint_fit.csv','incremental_yuan_response.csv','food_bindingness_raw_cells.csv']:check('Figure source '+fn,hashlib.sha256((O/fn).read_bytes()).digest()==hashlib.sha256((M/'source_data'/fn).read_bytes()).digest())
from docx import Document
for stem,nt,ni in [('JEBO_manuscript_v3',4,4),('JEBO_supplement_v3',32,0)]:
    doc=Document(M/(stem+'.docx'));check(stem+' structure',len(doc.tables)==nt and len(doc.inline_shapes)==ni)
    check(stem+' black title',str(doc.styles['Title'].font.color.rgb)=='000000')
ver=dict(python=sys.version,packages={name:meta.version(name) for name in ['numpy','pandas','scipy','statsmodels','matplotlib','python-docx']});(O/'software_versions.json').write_text(json.dumps(ver,indent=2))
(O/'requirements.txt').write_text('\n'.join(k+'=='+v for k,v in ver['packages'].items())+'\n')
(O/'verification.json').write_text(json.dumps(dict(checks=checks,all_passed=True,historical_files=len(hist)),indent=2,ensure_ascii=False),encoding='utf8')
print('PASS',len(checks),'independent numerical/protection/structure checks')
