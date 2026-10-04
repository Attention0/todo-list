"""Read-only comparisons of prose, retained outputs and DOCX structure.
No analysis pipeline is imported or executed; no estimates or tests are fitted.
"""
from pathlib import Path
import csv, re, json, subprocess, zipfile, hashlib
from docx import Document
from docx.oxml.ns import qn
M=Path(__file__).resolve().parents[1]; B=M.parent/'jebo_v4'; REPO=M.parents[2]
BASE='0685af82e06df1f43590c015379c2fb94fc4ac86'
s=(M/'JEBO_manuscript_v4_1.md').read_text(encoding='utf8')
old=(B/'JEBO_manuscript_v4.md').read_text(encoding='utf8')
u=(M/'JEBO_supplement_v4_1.md').read_text(encoding='utf8')
oldu=(B/'JEBO_supplement_v4.md').read_text(encoding='utf8')
checks=[]
def check(name,ok,detail=''):
    checks.append({'check':name,'passed':bool(ok),'detail':detail})
    if not ok:print('FAIL:',name,detail)
def tables(t):return [b.strip() for b in t.split('\n\n') if b.strip().startswith('|')]
ab=s.split('## Abstract')[1].split('Keywords:')[0]
intro=s.split('## 1 Introduction')[1].split('## 2 Conceptual')[0]
six=s.split('## 6 ')[1].split('## 7 ')[0]
old6=old.split('## 6 ')[1].split('## 7 ')[0]
check('Abstract 170–200 words',170<=len(ab.split())<=200,str(len(ab.split())))
early=' '.join(intro.split()[:500])
check('Three puzzles within first 500 words',all(t in early for t in ['Medical','nearly flat','Food declines less','mean form differences narrow']))
check('Section 6 shorter',len(six.split())<len(old6.split()),f'{len(old6.split())} -> {len(six.split())}')
check('Technical audit detail migrated',all(x not in six for x in ['RMSE','MDE','0.381','0.0610','0.12%','51.2','0.927']))
check('Main first three numeric tables unchanged',tables(s)[:3]==tables(old)[:3])
check('All 36 supplement tables unchanged',tables(u)==tables(oldu),str(len(tables(u))))
check('Questionnaire unchanged',u.split('## S9 ')[1].split('## S10 ')[0]==oldu.split('## S9 ')[1].split('## S10 ')[0])
check('References unchanged',s.split('## References')[1]==old.split('## References')[1])
for folder in ['figures','source_data']:
    for p in (B/folder).iterdir():
        if p.is_file():check('Exact PR20 copy '+folder+'/'+p.name,(M/folder/p.name).read_bytes()==p.read_bytes())
for name in ['JEBO_V4_1_WRITING_SPEC.md','JEBO_V4_1_WORK.md']:
    stored=subprocess.check_output(['git','show','9b6d445b5d95ef5c015eb433e650f4cd564aad47:消费调查/'+name],cwd=REPO).decode('utf8')
    check('Main authority '+name,(REPO/'消费调查'/name).read_text(encoding='utf8')==stored.replace('\r\n','\n'))
out=REPO/'消费调查/results/jebo_review_revision'
def rows(name):return list(csv.DictReader((out/name).open(encoding='utf8')))
cells=rows('adult_share_yuan_table.csv')
for r in cells:
    check('Main cell share '+r['form']+'/'+r['amount'],f"{float(r['midpoint'])*100:.2f}%" in s)
    check('Main cell yuan '+r['form']+'/'+r['amount'],f"{float(r['yuan']):,.2f}" in s)
for form,cat in [('cash',1),('cash',6),('cash',3),('food',1),('food',6),('food',3),('food',4),('medical',1),('medical',3),('medical',5),('medical',6)]:
    for amount in ['200','5000']:
        r=next(r for r in cells if r['form']==form and r['amount']==amount)
        check(f'Anatomy {form}/{cat}/{amount}',f"{float(r['share'+str(cat)])*100:.2f}%" in s)
family=rows('scientific_family42.csv')
for line,(outcome,test) in zip(tables(s)[2].splitlines()[2:],[('midpoint','cash'),('top75','cash'),('ordinal','cash'),('top75','omnibus'),('top75','cash-food'),('top75','cash-medical')]):
    r=next(r for r in family if r['outcome']==outcome and r['test']==test)
    for v,col in zip(line.strip('| ').split('|')[1:],['p','holm42','minP42']):
        check(f'Frozen p transcription {outcome}/{test}/{col}',abs(float(v)-float(r[col]))<=max(1e-7,abs(float(r[col]))*.005))
food=rows('food_bindingness_continuous.csv')[0]
check('Food representative estimate and CI transcribed',all(v in s for v in [f"+{float(food['estimate'])*100:.2f}",f"{float(food['lo'])*100:.2f}".replace('-','−'),f"{float(food['hi'])*100:.2f}"]))
check('Food conditional sharp sign preserved',all(x in s for x in ['negative Food–Cash gradient in G = 0','+8.00','contradicts that prediction conditional on the proxy','does not reject all models']))
check('Ordinal inference retained','The ordinal result does not.' in s)
check('Interactions remain uncertain','Cross-form interactions remain uncertain after that adjustment.' in s)
check('No equivalence upgrade','equal slopes are not established' in s and 'neither common slopes nor an intercept-only explanation is established' in s)
check('No structural upgrade','not structural MPCs' in s and 'residual-scale assumptions' in s)
check('No participation upgrade','not a causal participation or intensive-margin estimate' in s)
check('No individual-transition claim','rather than individual transitions' in s and 'uniform shift of each respondent' not in s)
check('No single-bin attribution','This common concentration helps' not in s)
check('No ordinal-to-dominance shortcut','none is a test that every aspect of the distribution shifts downward' in s)
check('Interpretive ranking explicit','interpretive rather than a tested superiority' in s)
check('Unmeasured mediator explicit','does not measure the categorization process itself' in s)
check('Medical not a unique model prediction','without uniquely predicting their near cancellation' in s)
check('Substantive conclusion',s.index('## 9 Conclusion')<s.index('## Author declarations') and 'The most secure result is narrower' not in s)
check('Technical migration retained',all(t in u for t in ['0.178','0.381','0.0610','20.8','8.8','0.0504','0.0426','0.0437','3.75','4.65','−6.00','+7.49','0.12%–0.17%']))
check('Field order not assumed','15 attitude responses numbered before the scenario' in u)
check('No internal response/audit language in main',not re.search(r'\b(PR19|PR20|reviewer|audit|GitHub|SPEC|WORK)\b',s))
check('Four figures retained in order',re.findall(r'^!\[.*?\]\(figures/(.*?)\)',s,re.M)==['fig1_response_atlas.png','fig2_share_and_yuan.png','fig3_category_changes.png','fig4_food_raw_cells.png'])
h=[p[2:].strip() for p in (M/'JEBO_Highlights_v4_1.md').read_text().split('\n\n') if p.startswith('- ')]
check('Five highlights under 85 characters',len(h)==5 and max(map(len,h))<=85,str(list(map(len,h))))
for stem,nt,ni in [('JEBO_manuscript_v4_1',4,4),('JEBO_supplement_v4_1',37,1),('JEBO_Highlights_v4_1',0,0)]:
    p=M/(stem+'.docx');d=Document(p)
    check(stem+' tables/images',len(d.tables)==nt and len(d.inline_shapes)==ni)
    check(stem+' body font',d.styles['Normal'].font.name=='Times New Roman' and d.styles['Normal'].font.size.pt==12)
    check(stem+' footer page field','PAGE' in d.sections[0].footer._element.xml)
    with zipfile.ZipFile(p) as z:
        xml=z.read('word/document.xml').decode('utf8')
        check(stem+' no changes/comments',not re.search(r'<w:(ins|del|commentRangeStart)\b',xml) and 'word/comments.xml' not in z.namelist())
protected=subprocess.check_output(['git','diff',BASE,'--name-only','--','消费调查/manuscript/jebo_v4','消费调查/manuscript/jebo_v3','消费调查/results'],cwd=REPO).decode()
check('Protected scientific/manuscript paths unchanged',not protected,protected)
check('Exact base ancestor',subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=REPO).returncode==0)
report={'base':BASE,'branch':'feature/jebo-v4-1-writing-refine','scope':'text/output comparison only; no empirical analysis executed','abstract_words':len(ab.split()),'intro_words':len(intro.split()),'main_words_before_references':len(s.split('## References')[0].split()),'section6_words':len(six.split()),'original_section6_words':len(old6.split()),'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks)}
(M/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
assert all(c['passed'] for c in checks)
