"""Validate audit semantics, aggregate-only artifacts and original-file immutability."""
import argparse,csv,hashlib,importlib.util,json,pathlib,re

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--inventory',type=pathlib.Path,required=True);p.add_argument('--project',type=pathlib.Path,required=True);a=p.parse_args()
 checks={};errors=[]
 spec=importlib.util.spec_from_file_location('audit',a.out/'code/evidence_audit.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 h=lambda s,e,d='example.invalid':{'start':s,'end':e,'institution':{'domain':d}}
 checks['bounded_history_positive']=mod.history([h(2020,2024)])[0]==[('example.invalid',2020,2024)]
 checks['open_end_and_2025_are_unknown']=mod.history([h(2020,None),h(2020,2025),h(2024,2020)])[0]==[]
 checks['actual_overlap_required']=mod.overlap([('example.invalid',2020,2021)],[('example.invalid',2022,2024)]) is False
 checks['inclusive_overlap']=mod.overlap([('example.invalid',2020,2021)],[('example.invalid',2021,2024)]) is True
 required=['FEASIBILITY_MATRIX.md','ASSIGNMENT_IDENTIFICATION.md','CORE_CONSTRUCTS.md','PRIORITY_TESTS.md','RESULT.md','README.md','RUN_METADATA.json']+[f'IDEA_{i}.md' for i in range(1,9)]
 checks['required_files']=all((a.out/n).is_file() for n in required)
 assignment=(a.out/'ASSIGNMENT_IDENTIFICATION.md').read_text(encoding='utf-8').strip()
 checks['required_assignment_ending']=assignment.endswith('No assignment-based source of plausibly exogenous variation was identified.')
 matrix=(a.out/'FEASIBILITY_MATRIX.md').read_text(encoding='utf-8')
 rows=[r for r in matrix.splitlines() if re.match(r'^\| [1-8] ',r)]
 allowed=['CLEAN NOW','CLEAN WITH SPECIFIC ADDITIONAL DATA','CONDITIONAL / ASSOCIATIONAL ONLY','NOT CREDIBLY IDENTIFIABLE IN ICLR 2026']
 checks['eight_valid_verdicts']=len(rows)==8 and all(r.split('|')[-2].strip() in allowed for r in rows)
 checks['priority_tests_exactly_five']=len(re.findall(r'^\d\. \*\*',(a.out/'PRIORITY_TESTS.md').read_text(encoding='utf-8'),re.M))==5
 originals=0;changed=0
 with a.inventory.open(encoding='utf-8-sig',newline='') as f:
  for row in csv.DictReader(f):
   originals+=1;fp=a.project/row['path'];digest=hashlib.file_digest(fp.open('rb'),'sha256').hexdigest()
   changed+=int(digest!=row['sha256'])
 checks['original_files_unchanged']=changed==0
 scanned=0;manifest=[]
 for fp in sorted(a.out.rglob('*')):
  if not fp.is_file() or '__pycache__' in fp.parts:continue
  if fp.name in ['VALIDATION.json','PUBLICATION.json']:continue
  scanned+=1;content=fp.read_text(encoding='utf-8-sig')
  if fp.suffix not in ['.md','.py','.json','.csv']:errors.append('unsupported_artifact_type')
  # Detect literal addresses, raw OpenReview person IDs, and credential-shaped values.
  if re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',content):errors.append('literal_email')
  if re.search(r'~[A-Za-z][A-Za-z_]+\d+',content):errors.append('literal_person_id')
  if re.search(r'(?:ghp_|github_pat_|sk-)[A-Za-z0-9_]{20,}',content):errors.append('credential_literal')
  if fp.suffix=='.csv':
   with fp.open(encoding='utf-8-sig',newline='') as f:
    cols=next(csv.reader(f))
   if any(c in ['reviewer_id','author_id','profile','email','name','forum','note_id','paper_id'] for c in cols):errors.append('person_level_column')
  manifest.append(dict(path=fp.relative_to(a.out).as_posix(),sha256=hashlib.sha256(fp.read_bytes()).hexdigest()))
 checks['privacy_scan']=not errors
 result=dict(checks=checks,all_passed=all(checks.values()),original_files_checked=originals,original_files_changed=changed,artifacts_scanned=scanned,privacy_findings=sorted(set(errors)),artifact_manifest=manifest,limitations='Heuristic privacy scan plus manual review; no guarantee against every possible free-text identifier. No identification/balance claim is validated by these checks.')
 (a.out/'VALIDATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='artifact_manifest'}));assert result['all_passed']
if __name__=='__main__':main()
