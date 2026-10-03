"""Attach precise source sets to the manually reviewed claim blocks; no analysis."""
from pathlib import Path
import csv, json, hashlib, platform, importlib.metadata

O=Path(__file__).resolve().parent
M=O.parents[1]/'manuscript'/'jebo_v1'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

# File paths below are relative to results/. Numeric rows can be located using
# sample/outcome/test labels in the claim and approved_source_rows.csv.
main={
 'Abstract':['nc_evidence_revision/profiles.csv','nc_evidence_revision/scientific_family21.csv','jebo_transition/extensive_intensive_decomposition.csv'],
 '1.':['nc_evidence_revision/profiles.csv','nc_evidence_revision/main_effects.csv','nc_evidence_revision/scientific_family21.csv','jebo_transition/extensive_intensive_cells.csv','jebo_transition/extensive_intensive_decomposition.csv','jebo_transition/jebo_literature_matrix.csv'],
 '2.':['jebo_transition/jebo_literature_matrix.csv','jebo_transition/BEHAVIORAL_PREDICTIONS.md'],
 '3.':['jebo_transition/JEBO_EVIDENCE_FREEZE.md','nc_evidence_revision/distribution.csv','nc_evidence_revision/analyze.py'],
 '4.':['nc_evidence_revision/profiles.csv','nc_evidence_revision/within_form_slopes.csv','nc_evidence_revision/main_effects.csv'],
 '5.':['nc_evidence_revision/scientific_family21.csv','nc_evidence_revision/form_contrasts.csv','nc_evidence_revision/profiles.csv'],
 '6.':['jebo_transition/extensive_intensive_cells.csv','jebo_transition/extensive_intensive_decomposition.csv','jebo_transition/decompose.py','jebo_transition/MPC_SIZE_LITERATURE_BENCHMARK.md'],
 '7.':['nc_evidence_revision/mechanism_tests.csv','nc_evidence_revision/mechanism_details.csv','nc_evidence_revision/prediction_scores.csv','jebo_transition/BEHAVIORAL_PREDICTIONS.md'],
 '8.':['nc_evidence_revision/calibration_diagnostics.csv','nc_evidence_revision/mechanism_tests.csv','jebo_transition/jebo_literature_matrix.csv','jebo_transition/JEBO_EVIDENCE_FREEZE.md'],
 '9.':['nc_evidence_revision/profiles.csv','nc_evidence_revision/scientific_family21.csv','jebo_transition/extensive_intensive_decomposition.csv']}
supp={
 'S1.':main['3.'], 'S2.':['nc_evidence_revision/main_effects.csv','nc_evidence_revision/form_contrasts.csv'],
 'S3.':['nc_evidence_revision/analyze.py','nc_evidence_revision/scientific_family21.csv','nc_evidence_revision/simulation_results.csv','nc_evidence_revision/legacy_family_comparison.csv','nc_evidence_revision/legacy_maxnorm_extreme_sources.csv'],
 'S4.':['mpc_final_strengthening/specification_stability_summary.csv','nc_evidence_revision/adult_endpoint_ratios.csv','jebo_transition/JEBO_EVIDENCE_FREEZE.md'],
 'S5.':main['6.'], 'S6.':main['2.'], 'S7.':main['7.'],
 'S8.':['nc_evidence_revision/mechanism_tests.csv','nc_evidence_revision/mechanism_details.csv','nc_evidence_revision/screen_cell_counts.csv','jebo_transition/JEBO_EVIDENCE_FREEZE.md'],
 'S9.':['nc_evidence_revision/calibration_diagnostics.csv','nc_evidence_revision/calibration_cells.csv','nc_evidence_revision/calibration_effects.csv'],
 'S10.':['jebo_transition/historical_input_hashes.json','jebo_transition/JEBO_EVIDENCE_FREEZE.md']}
tables={
 'Table 1.':main['3.'],'Table 2.':['nc_evidence_revision/within_form_slopes.csv','nc_evidence_revision/scientific_family21.csv'],
 'Table 3.':['jebo_transition/extensive_intensive_decomposition.csv'],
 'Table S1.':['nc_evidence_revision/distribution.csv'],'Table S2.':['nc_evidence_revision/profiles.csv'],
 'Table S3.':supp['S2.'],'Table S4.':['nc_evidence_revision/form_contrasts.csv'],
 'Table S5.':['nc_evidence_revision/scientific_family21.csv'],'Table S6.':['nc_evidence_revision/simulation_results.csv'],
 'Table S7.':['mpc_final_strengthening/specification_stability_summary.csv'],
 'Table S8.':['nc_evidence_revision/adult_endpoint_ratios.csv'],'Table S9.':['jebo_transition/extensive_intensive_cells.csv'],
 'Table S10.':['jebo_transition/BEHAVIORAL_PREDICTIONS.md'],'Table S11.':['nc_evidence_revision/mechanism_tests.csv'],
 'Table S12.':['nc_evidence_revision/prediction_scores.csv'],'Table S13.':['nc_evidence_revision/mechanism_details.csv'],
 'Table S14.':supp['S9.'],'Table S15.':supp['S10.']}
ledger=read(M/'JEBO_CLAIM_LEDGER.csv')
for r in ledger:
    section=r['location'].split(' :: ')[1]
    mapping={**(supp if 'supplement' in r['location'] else main),**tables}
    selected=next((v for k,v in mapping.items() if section.startswith(k)),['jebo_transition/JEBO_EVIDENCE_FREEZE.md'])
    if r['claim_text'].startswith(('Figure 1.','Figure 2.','Figure 3.')):
        selected=['nc_evidence_revision/distribution.csv','nc_evidence_revision/profiles.csv']
    for path in selected:assert (O.parent/path).is_file(),path
    r['source']='; '.join('results/'+p for p in selected)
    r['source']+='; row locator: sample/outcome/test in block and approved_source_rows.csv'
    r['wording_acceptable']='Reviewed: retain stated-outcome, sample, adjustment and descriptive/causal qualifications in this block'
with (M/'JEBO_CLAIM_LEDGER.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(ledger[0]));w.writeheader();w.writerows(ledger)

maintext=(M/'JEBO_manuscript_v1.md').read_text(encoding='utf8')
assert 'zlliu2026@nsd.pku.edu.cn' in maintext
assert '23, 40-52.' in maintext and '26, 609-643.' in maintext
assert len(read(M/'JEBO_REFERENCE_AUDIT.csv'))==30
body=maintext.split('## References')[0]
for r in read(M/'JEBO_REFERENCE_AUDIT.csv'):
    first=r['citation'].split(',')[0]
    assert first in body,('Uncited reference',first)
versions={'python':platform.python_version()}
for package in ['numpy','pandas','matplotlib','python-docx','pypdf']:
    versions[package]=importlib.metadata.version(package)
(O/'software_versions.json').write_text(json.dumps(versions,indent=2)+'\n',encoding='utf8')
out={'claim_blocks':len(ledger),'source_paths_verified':True,'references_all_cited':30,
     'email_preserved':True,'publisher_verified_page_range_repairs':['Heath and Soll 1996: 40-52','Shefrin and Thaler 1988: 609-643'],
     'docx_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in M.glob('*.docx')}}
(O/'final_audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8')
print(json.dumps(out,indent=2))
