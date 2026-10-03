"""Assemble narrative, tables and provenance from frozen aggregate CSVs only."""
from pathlib import Path
import csv,json,re,shutil,hashlib
O=Path(__file__).resolve().parent;P=O.parent/'nc_evidence_revision';M=O.parents[1]/'manuscript'/'jebo_v1';M.mkdir(parents=True,exist_ok=True)
def read(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rows):
 with Path(p).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def num(r,k):return float(r[k])
def pv(x):return '—' if x=='' else '<0.001' if float(x)<.001 else f'{float(x):.4f}' if .049<float(x)<.051 else f'{float(x):.3f}'
def ci(r,k=100):
 digits=3 if k==1 else 2
 return f'{num(r,"estimate")*k:.{digits}f} [{num(r,"lo")*k:.{digits}f}, {num(r,"hi")*k:.{digits}f}]'
def table(title,head,rows,note=''):
 return '### '+title+'\n\n'+'| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+'\n'.join('| '+' | '.join(str(v).replace('|','/') for v in row)+' |' for row in rows)+'\n\n'+note
def adult(file):return [r for r in read(P/file) if r.get('sample')=='A']
dist=adult('distribution.csv');profiles=adult('profiles.csv');within=adult('within_form_slopes.csv');family=adult('scientific_family21.csv');effects=adult('main_effects.csv');contrasts=adult('form_contrasts.csv');cells=read(O/'extensive_intensive_cells.csv');dec=read(O/'extensive_intensive_decomposition.csv')
blocks={}
blocks['table1']=table('Table 1. Randomized scenarios and adult cell sizes',['Form and use rights','RMB 200','RMB 1,000','RMB 5,000'],[['Cash: unrestricted',618,592,580],['Food: noncashable food/daily-necessities vouchers; six-month expiry',613,619,599],['Medical: medical-related personal-account credit; long-lived',614,611,634]],'N=5,480 adults. Each respondent sees one scenario. Form bundles permitted use, liquidity, label, timing and wording. The outcome concerns additional total spending, not only eligible purchases.')
rows=[]
for y in ['ordinal','midpoint','top75']:
 k=1 if y=='ordinal' else 100
 for r in within:
  if r['outcome']==y:rows.append([{'ordinal':'Ordinal','midpoint':'Midpoint','top75':'>75%'}[y],r['test'].title(),ci(r,k),pv(r['p']),'—'])
 for r in family:
  if r['outcome']==y and r['test']!='omnibus':rows.append([{'ordinal':'Ordinal','midpoint':'Midpoint','top75':'>75%'}[y],r['test'].replace('cash','Cash').replace('food','Food').replace('medical','Medical'),ci(r,k),pv(r['p']),pv(r['holm21'])])
blocks['table2']=table('Table 2. Within-form trends and Cash-versus-form slope differences',['Outcome','Trend / contrast','Estimate [95% CI]','Nominal p','Holm 21'],rows,'Per fivefold amount increase. Ordinal units are score points; midpoint and highest-category (>75%) units are percentage points. Intervals are pointwise HC3. Within-form p values are nominal, not members of the21-test interaction family. Omnibus Holm/min-P values: ordinal0.844/0.373, midpoint0.522/0.232, highest category0.181/0.082. Highest-category Cash–Food and Cash–Medical min-P values are0.105 and0.039. All21 results and simultaneous intervals are in TableS5 and the source CSV.')
rows=[]
for r in dec:
 row=[r['form'].title()]
 for s in ['extensive','intensive','total']:row.append(f'{num(r,s)*100:.2f} [{num(r,s+"_lo")*100:.2f}, {num(r,s+"_hi")*100:.2f}]')
 rows.append(row)
blocks['table3']=table('Table 3. Descriptive decomposition of the RMB 200-to-5,000 change',['Form','Participation component','Conditional-positive component','Total midpoint change'],rows,'Percentage points, with pointwise95% cell-stratified bootstrap percentile intervals (4,000 draws, seed2026100316). Components sum to the total before rounding. Positive-group membership is post-treatment; the conditional component is not a causal intensive-margin effect. No component-significance selection is used.')
caps={1:('fig1_atlas','Figure 1. Response distributions and midpoint means. A: six unconditional response categories in each adult cell, shaded from light to dark in spending order. B: midpoint-coded shares and pointwise95% normal intervals from cell variances. Cash/Food/Medical cell Ns at200/1,000/5,000 are618/592/580,613/619/599 and614/611/634. The lowest category means essentially no increase. Lines join independent randomized groups at three discrete amounts, not within-person paths. All panels use adults (N=5,480).'),2:('fig2_curves','Figure 2. Form-specific size profiles. A: mean ordinal score (1–6); B: midpoint-coded spending share. Error bars are pointwise95% normal intervals, not simultaneous interaction intervals. Adult cells and Ns are as in Figure1. Lines connect three independent groups. Equal ordinal spacing and within-bin midpoint values are separate coding assumptions; similar Medical means do not establish invariance.'),3:('fig3_margins','Figure 3. Participation and high-response margins. A: probability of choosing a category above essentially no increase; B: probability of the above75% category. Adult sample and cell Ns are as in Figure1. Error bars are pointwise95% normal intervals. The Cash upper response falls while its positive-category frequency is similar at the endpoints. These are between-group distributions; no claim of exclusively tail-specific change or a fixed set of responders is implied.')}
for i,(n,cap) in caps.items():blocks['figure'+str(i)]=f'![{cap.split(". ")[1]}](figures/{n}.png)\n\n'+cap
rows=[]
for r in cells:
 shares=[int(r['count'+str(j)])/int(r['N'])*100 for j in range(1,7)]
 rows.append([r['form'].title(),r['amount'],r['N']]+[f'{v:.1f}' for v in shares])
blocks['s1']=table('Table S1. All adult response bins',['Form','RMB','N','None*','<10%','10–25%','25–50%','50–75%','>75%'],rows,'Percent of respondents. *Essentially no increase, not an observed exact zero. Rows sum to100 before rounding.')
rows=[]
for r in cells:
 row=[r['form'].title(),r['amount']]
 for y in ['any_spending','ge10','ge25','ge50','top75']:
  q=next(q for q in profiles if q['form']==r['form'] and q['amount']==r['amount'] and q['outcome']==y);row.append(f'{num(q,"estimate")*100:.2f}')
 rows.append(row)
blocks['s2']=table('Table S2. Complete adult threshold profiles',['Form','RMB','Positive','≥10%','≥25%','≥50%','>75%'],rows,'Percent. Full pointwise intervals are in profiles.csv; no threshold was added for this transition.')
rows=[]
for r in effects:
 if r['outcome'] in ['ordinal','midpoint','top75'] and 'omnibus' not in r['test']:rows.append([r['outcome'],r['test'],ci(r,1 if r['outcome']=='ordinal' else 100),pv(r['p']),pv(r['holm6'])])
blocks['s3']=table('Table S3. Equal-weight marginal factor contrasts',['Outcome','Contrast','Estimate [95% CI]','Nominal p','Holm 6'],rows,'Ordinal score units; otherwise percentage points. Holm6 applies only to highest-category results; the two omnibus tests are included in that family and retained in main_effects.csv.')
blocks['s4']=table('Table S4. Highest-category form contrasts at each amount',['Contrast','RMB','Estimate [pointwise95% CI]','Simultaneous95% CI','Holm6'],[[r['test'],r['amount'],ci(r),f'[{num(r,"sim_lo")*100:.2f}, {num(r,"sim_hi")*100:.2f}]',pv(r['holm6'])] for r in contrasts],'Bonferroni simultaneous intervals cover the six contrasts. Adult sample.')
blocks['s5']=table('Table S5. Adult interaction family',['Outcome','Test','Nominal p','Holm21','Min-P21'],[[r['outcome'],r['test'],pv(r['p']),pv(r['holm21']),pv(r['minP21'])] for r in family],'All21 tests retained. Scalar estimates and Bonferroni simultaneous intervals are in scientific_family21.csv. Seven codings are dependent descriptions of one response.')
sim=read(P/'simulation_results.csv')
blocks['s6']=table('Table S6. Existing complete-refit simulation checks',['Scenario','Method','FWER [95% CI]','False-null power'],[[r['scenario'].replace('_',' '),r['method'],f'{num(r,"FWER"):.3f} [{num(r,"lo"):.3f}, {num(r,"hi"):.3f}]','—' if not r['false_null_mean_power'] else f'{num(r,"false_null_mean_power"):.3f}'] for r in sim],'1,000 refitted datasets per scenario;999 draws per fit; no failed refits. Power is mean rejection over six false restrictions in the partial-null simulation, not observed-effect power.')
grid=read(O.parent/'mpc_final_strengthening'/'specification_stability_summary.csv')
blocks['s7']=table('Table S7. Historical420-grid descriptive summary',['Coding','Contrast','Specs','Positive sign (%)','CI excludes0 (%)'],[[r['coding'],r['estimand'],r['specifications'],f'{num(r,"share_positive")*100:.0f}',f'{num(r,"share_CI_excludes_zero")*100:.0f}'] for r in grid],'Historical R/A/C/Q1/Q2 samples; positive means the named form/derived Restricted slope exceeds Cash. Each row summarizes20 dependent specifications. Different codings have different scales; this is not a new test.')
rat=read(P/'adult_endpoint_ratios.csv');rows=[]
for f in ['cash','food','medical']:
 row=[f.title()]
 for scale in ['risk_ratio','odds_ratio']:
  r=next(r for r in rat if r['form']==f and r['scale']==scale);row.append(f'{num(r,"estimate"):.3f} [{num(r,"lo"):.3f}, {num(r,"hi"):.3f}]')
 rows.append(row)
blocks['s8']=table('Table S8. Adult highest-category endpoint ratios',['Form','Risk ratio [95% CI]','Odds ratio [95% CI]'],rows,'5,000 versus200. Pointwise log-scale delta-method intervals, not tests comparing ratios across forms.')
blocks['s10']=table('Table S9. Adult cell decomposition quantities',['Form','RMB','Positive (%)','Midpoint (%)','Conditional midpoint [95% CI] (%)'],[[r['form'].title(),r['amount'],f'{num(r,"p_any")*100:.2f}',f'{num(r,"midpoint")*100:.2f}',f'{num(r,"conditional_midpoint")*100:.2f} [{num(r,"conditional_midpoint_lo")*100:.2f}, {num(r,"conditional_midpoint_hi")*100:.2f}]'] for r in cells],'N and all three bootstrap interval sets are in extensive_intensive_cells.csv. Conditional-positive means are descriptive.')
predrows=[['Concave consumption / PIH','Cash decline conditional on consumption-function assumptions','Equal if fully fungible; otherwise ambiguous','Horizon, preferences and wealth'],['Liquidity / hand-to-mouth','High small-shock response near constraints','Both margins; gap ambiguous','Liquid resources and exogenous liquidity'],['Small-windfall mental accounts','Lower conditional shares if larger gains enter assets','Gap may shrink under additional assumptions','Account categorization / intended use'],['Attention / planning','Entry may rise as conditional share falls','Expiry and salience can change either margin','Attention and planning horizon'],['Mechanical eligibility restriction','Cash benchmark; eligible spending matters','Gap sign depends on substitution and timing','Counterfactual eligible spending'],['Earmarking / commitment','Category budgets influence allocation','Either margin; gap ambiguous','Independent label/commitment manipulation']]
blocks['s9']=table('Table S10. Conceptual predictions and missing measurements',['Account','Cash/margin implication','Form comparison','Missing for identification'],predrows,'Predictions require auxiliary assumptions. Income/expenditure diagnostics speak to selected implications; none uniquely identifies a process. Full synthesis: BEHAVIORAL_PREDICTIONS.md.')
mech=read(P/'mechanism_tests.csv')
blocks['s11']=table('Table S11. Direct diagnostic restrictions',['Restriction','N','df','Nominal p','Holm7'],[[r['test'].replace('_',' '),r['N'],r['df'],pv(r['p']),pv(r['holm7'])] for r in mech],'Adult highest-category outcome. Seven tests form one local family. Full coefficient details and group contrasts are in mechanism_details.csv.')
pred=read(P/'prediction_scores.csv')
blocks['s12']=table('Table S12. Existing held-out prediction comparisons',['Mapping','Model','Log loss','Gain vs ABS (%)'],[[r['mapping'],r['model'],f'{num(r,"logloss"):.6f}',f'{num(r,"relative_gain_vs_ABS")*100:.3f}'] for r in pred],'Positive gain means lower loss. Common fixed folds; no materiality gate or new inferential test.')
qs=[r for r in read(P/'mechanism_details.csv') if r['test'].startswith('Q')]
blocks['s13']=table('Table S13. Highest-category screen-group slope differences',['Screen / pass(1) or fail(0) / contrast','Group N','Estimate [95% CI] (pp)'],[[r['test'],int(float(r['subgroup_N'])),ci(r)] for r in qs],'Food–Cash or Medical–Cash per fivefold amount increase. Direct pass/fail joint tests, not separate subgroup significance, appear in TableS11.')
cal=read(P/'calibration_diagnostics.csv')
blocks['s14']=table('Table S14. Census-weight diagnostics',['Scheme','ESS','Maximum normalized weight','Largest target gap (pp)'],[[r['scheme'],f'{num(r,"ESS"):.1f}',f'{num(r,"max_weight"):.2f}',f'{num(r,"max_abs_target_discrepancy")*100:.2f}'] for r in cal],'Source: National Bureau of Statistics2020census Table4-1, https://www.stats.gov.cn/sj/pcsj/rkpc/7rp/zk/html/A0401.jpg . Twelve joint cells. Targets and effects: calibration_cells.csv / calibration_effects.csv. Weights do not establish representativeness.')
archive=[['PR9 size-curve discovery','mpc_size_curve','R primary; original cells/thresholds/ordered fits'],['PR10 finite strengthening','mpc_final_strengthening','420grid; tail tests; implied yuan; local adjustments'],['PR11 theory-variable moderation','mpc_who_drives','R primary; fixed moderator tests and power limits'],['PR12 observable screen','mpc_allx_screen','150planned variables; failed-fit accounting and FDR'],['PR13 approved figures','nature_main_figures','Historical mostlyR sources, not reused as adult values'],['PR14 atlas','mpc_hero_figure','Geometry reused; original numbers retained unchanged'],['PR15 revision audit','nc_revision_audit','1,500grid; ordered models; diagnostics; obsolete criteria disclosed'],['PR16 evidence revision','nc_evidence_revision','Authoritative adultA family21/diagnostics; no re-estimation here'],['JEBO transition','jebo_transition','Adult aggregate-only decomposition and literature synthesis']]
blocks['archive']=table('Table S15. Source archive and sample scope',['Stage','Directory under results/','Scope'],archive,'All earlier packages remain unchanged. Historical local adjustments are not substituted for the primary interaction family.')
lit={r['id']:r for r in read(O/'jebo_literature_matrix.csv')}
keys=['N01','N02','N03','N04','N05','N06','N12','N13','N17','N18','N19','N20','N21','N22','N23','N24','N25','N26','N29','N30','JP2010','KV2022','FHN2021','HS1996','PS2019','JS2026','LEE2024','PL2025','FR2025']
refs=[];audit=[]
for k in keys:
 r=lit[k]
 for fld in ['year','volume','pages']:r[fld]=re.sub(r'\.0$','',r[fld])
 names=[]
 for a in r['authors'].split('; '):
  parts=a.split();names.append(parts[-1]+', '+''.join(p[0]+'.' for p in parts[:-1]))
 title=r['title'].rstrip('.*')
 if k=='N02':title='The behavioral life-cycle hypothesis'
 citation=f'{", ".join(names)}, {r["year"]}. {title}. {r["journal"]}'
 if r['volume']:citation+=', '+r['volume']
 if r['pages']:citation+=', '+r['pages']
 citation+='.'
 link=r['url'];citation+=' '+link
 refs.append(citation)
 audit.append(dict(reference_id=k,citation=citation,doi=r['doi'],publication_status=r['publication_status'],accessed='2026-10-03',source_scope=r['source_scope'],supported_statement=r['key_result_margins'],qualification=r['relevance_novelty'],verdict='Use only within recorded scope; no unsupported numeric extraction'))
fr='Friedman, M., 1957. The Permanent Income Hypothesis. In A Theory of the Consumption Function, pp.20–37. Princeton University Press. https://www.nber.org/books-and-chapters/theory-consumption-function/permanent-income-hypothesis'
refs.append(fr);audit.append(dict(reference_id='FR1957',citation=fr,doi='',publication_status='Published book chapter',accessed='2026-10-03',source_scope='NBER primary chapter record',supported_statement='Permanent versus transitory income distinction',qualification='No universal negative finite-size slope attributed',verdict='Accept'))
blocks['references']='\n\n'.join(sorted(refs,key=str.casefold));writecsv(M/'JEBO_REFERENCE_AUDIT.csv',audit)
for src,target in [('manuscript_body.md','JEBO_manuscript_v1.md'),('supplement_body.md','JEBO_supplement_v1.md')]:
 t=(O/src).read_text(encoding='utf8')
 if src=='manuscript_body.md':t=t.replace('Supplementary Table S9','Supplementary Table S10')
 else:t=t.replace('TableS10 reports all cell','TableS9 reports all cell').replace('TableS9 summarizes','TableS10 summarizes')
 for k,v in blocks.items():t=t.replace('{'+k+'}',v)
 # Normalize spacing introduced by compact audit notes without changing numeric values.
 t=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', t) if False else t
 assert not re.search(r'\{(?:s\d+|table\d+|figure\d+|references|archive)\}',t)
 (M/target).write_text(t+'\n',encoding='utf8')
shutil.copyfile(O.parent.parent/'manuscript'/'nc_v5'/'AUTHOR_INFORMATION_REQUIRED.md',M/'AUTHOR_INFORMATION_REQUIRED.md')
(M/'AUTHOR_INFORMATION_REQUIRED.md').write_text('''# JEBO投稿前作者信息清单

科学内容和分析包已形成；以下事实不能从数据或问卷中补造，故当前仍为作者审阅稿。

1. 招募渠道、供应商、调查日期、抽样框/配额、补偿、邀请/开始/完成/交付人数及排除原因；腾讯问卷后台字段不等于实际招募渠道。
2. 事前样本量依据、停止规则；没有事前功效分析时如实说明。
3. 随机分配算法/比例、展示与时间日志，前置态度题及后台年龄的采集时点。
4. 伦理批准或正式豁免的机构、编号、日期；知情同意；原始17名记录未成年者是否受覆盖。成人主分析不补救原始伦理程序。
5. 作者单位/联系方式复核，资金、贡献、利益冲突与致谢确认。
6. 去标识数据共享权限、同意限制、申请条件；长期代码/聚合数据存档标识。不得把GitHub链接写成已有存档DOI。

这些是投稿手续与研究记录的真实缺口。未将“已批准”“全国代表性”“预注册”或“实际支出”写入正文以掩盖缺口。旧NC稿不改动。
''',encoding='utf8')
(M/'.gitignore').write_text('qa/\n__pycache__/\n',encoding='utf8')
paths=['distribution.csv','profiles.csv','within_form_slopes.csv','scientific_family21.csv','main_effects.csv','form_contrasts.csv','mechanism_tests.csv','mechanism_details.csv','prediction_scores.csv','calibration_diagnostics.csv']
manifest=['# JEBO source manifest','', 'Base: PR16, commit f3124aa820e0b4de3540aaaeb64ffdeb7ca19228. https://github.com/Attention0/todo-list/pull/16 . New branch feature/jebo-repositioning stacks on feature/nc-evidence-revision; no old PR merged.','', 'Pre-analysis freeze commit950e90f; story gate commitb6e7b22. The only new empirical operation uses54 adult cell-category counts for the product decomposition and4,000fixed-seed bootstrap draws. No respondent-level input, new model, threshold, subgroup or multiplicity family is introduced.','', '## Main provenance','', '| Output | Source |','|---|---|','| Figure1 adult atlas | PR14geometry; PR16distribution.csv/profiles.csv |','| Figures2/3 | PR16profiles.csv |','| Table1 | Adult distribution counts and questionnaire descriptions |','| Table2 | PR16within_form_slopes.csv/scientific_family21.csv |','| Table3 | extensive_intensive_decomposition.csv |','| Supplement | TablesS1–S15 source labels and archive map |','', '## Approved input hashes','']
for n in paths:manifest.append(f'- results/nc_evidence_revision/{n}: {hashlib.sha256((P/n).read_bytes()).hexdigest()}')
manifest+=['','Literature: 54 curated papers plus a foundational book chapter; 13 recent JEBO comparators with explicit access limits. Bernard2023 is the nearest predecessor and changes the novelty claim. Working papers are labelled. Author/institution working-version layout counts are not presented as published counts.','', 'Questionnaire/raw files remain private and untouched. No respondent IDs, raw exports or restricted copyrighted PDFs are published. research_cache and QA renders are ignored. The article is not certified submission-ready while AUTHOR_INFORMATION_REQUIRED.md remains unresolved.']
(M/'SOURCE_MANIFEST.md').write_text('\n'.join(manifest)+'\n',encoding='utf8')
# Paragraph/table-row coverage; source sets are explicit, not a substitute for manual reading.
ledger=[]
for filename in ['JEBO_manuscript_v1.md','JEBO_supplement_v1.md']:
 section='Front matter'
 for n,b in enumerate((M/filename).read_text(encoding='utf8').split('\n\n'),1):
  if b.startswith('#'):section=b.splitlines()[0].lstrip('# ');continue
  if not b.strip() or section=='References' or b.startswith('!['):continue
  if section in ['Front matter','Tables and figures'] and len(b.split())<15:continue
  sources='Approved source map; '+('jebo_literature_matrix.csv; BEHAVIORAL_PREDICTIONS.md' if ('literature' in section.lower() or section.startswith('1.') or section.startswith('2.')) else 'nc_evidence_revision aggregate tables')
  if any(x in b for x in ['decomposition','conditional-positive component','product']):sources+='; extensive_intensive_cells.csv; extensive_intensive_decomposition.csv'
  if 'Table' in section:sources+='; table footnote identifies exact file/family'
  flags=','.join(w for w in ['flat','invariant','mental accounting','fungibility','earmark','restriction','tail','mechanism','representative','MPC','spending'] if w.lower() in b.lower())
  kind='limitation' if any(x in b for x in ['does not','do not','not establish','not identify','limitations','require author']) else 'inference' if any(x in b for x in [' p=',' p<','95%','Holm']) else 'interpretation' if any(x in b for x in ['may ','could ','consistent','account']) else 'fact'
  strength='suggestive / explicitly bounded' if 'suggestive' in b or 'interaction' in b else 'descriptive' if kind in ['fact','interpretation'] else 'qualified inference or limitation'
  ledger.append(dict(location=f'{filename} :: {section} :: block{n}',claim_text=b,claim_type=kind,source=sources,strength_status=strength,audit_flags=flags,wording_acceptable='Yes, subject to stated scope; manual final review'))
writecsv(M/'JEBO_CLAIM_LEDGER.csv',ledger)
summary=dict(main_words=len((M/'JEBO_manuscript_v1.md').read_text().split()),intro_words=len((O/'manuscript_body.md').read_text().split('## 1. Introduction')[1].split('## 2.')[0].split()),abstract_words=len((O/'manuscript_body.md').read_text().split('## Abstract')[1].split('Keywords:')[0].split()),references=len(refs),claim_blocks=len(ledger))
(O/'assembly_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(summary)
