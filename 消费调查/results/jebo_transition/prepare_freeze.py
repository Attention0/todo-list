"""Read approved aggregate sources and record the pre-decomposition evidence freeze."""
from pathlib import Path
import csv, hashlib, json
from docx import Document
O=Path(__file__).resolve().parent
P=O.parents[1]
R=O.parent/'nc_evidence_revision'
files=['profiles.csv','distribution.csv','within_form_slopes.csv','scientific_family21.csv','main_effects.csv','form_contrasts.csv','mechanism_tests.csv','mechanism_details.csv','prediction_scores.csv','calibration_diagnostics.csv','calibration_effects.csv']
rows=[]
for name in files:
    with (R/name).open(encoding='utf-8-sig',newline='') as f:
        for n,r in enumerate(csv.DictReader(f),1):
            if 'sample' in r and r['sample']!='A': continue
            rows.append(dict(source_file=str((R/name).relative_to(P)),data_row=n,source_commit='f3124aa820e0b4de3540aaaeb64ffdeb7ca19228',sample=r.get('sample','see N and source definition'),record=json.dumps(r,ensure_ascii=False)))
with (O/'approved_source_rows.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
hashes={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for folder in [P/'results',P/'manuscript'/'nc_v5'] for f in folder.rglob('*') if f.is_file() and 'jebo_transition' not in f.parts and not any(x in f.parts for x in ['__pycache__','qa','qa-final'])}
(O/'historical_input_hashes.json').write_text(json.dumps(hashes,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
doc=Document(P/'manuscript/nc_v5/NC_MPC_manuscript_v5.docx')
assert '5,480' in '\n'.join(p.text for p in doc.paragraphs)
text='''# JEBO evidence freeze

Base PR16 head f3124aa820e0b4de3540aaaeb64ffdeb7ca19228. Prepared before the new decomposition and before manuscript authoring. Earlier NC and discovery outputs remain read-only historical evidence. Exact approved rows are in approved_source_rows.csv; hashes of historical result/manuscript files are in historical_input_hashes.json.

## Design

The full dataset has 5,497 respondents; adults (recorded age at least 18) number 5,480. Each answers one hypothetical randomized vignette. Cash cell Ns are 618/592/580, Food 613/619/599, Medical 614/611/634 at RMB200/1,000/5,000. Cash is unrestricted; Food/daily-necessities vouchers are noncashable and expire after six months; Medical personal-account credits are restricted to medical-related expenditure and long-lived. The outcome asks additional TOTAL spending relative to prior plans, not only spending in the eligible category.

Six original categories: essentially no additional spending; below10%;10–25%;25–50%;50–75%;above75%. Amount examples accompany the percentage bins; the top example is75–100%. No common explicit spending horizon and no payment incentive. Form bundles eligible use, liquidity, expiry and explanatory wording. Background fields come from the platform; exact recruitment, field dates, allocation logs, stopping rule, ethics and consent still require author documents. Existing full-sample balance audit across41 observed variables found no BH-adjusted imbalance; no adult balance test is newly run.

## Relatively secure findings

Adult Cash midpoint slope is −.0256844 per fivefold amount increase, pointwise95%CI[−.0409241,−.0104447], rawP=.0009555. Cash ordinal slope−.115239, CI[−.204524,−.025954], rawP=.011414. These are approved within-form tests, not newly selected or corrected tests. Historical full-sample ordinal Holm5=.053 warns against presenting every representation as multiplicity-robust. Food midpoint−.0160677; Medical+.0005730, with a wide interval [−.012654,.013800]. Nonsignificance does not establish invariance.

The raw adult Cash Top75 probabilities are .134304/.089527/.053448. Its lowest-category share is .273463/.285473/.274138. Form-average Medical−Cash Top75 is−4.1738pp (pointwiseCI−5.8374,−2.5102; Holm6<.001). Amount-average5000−200 is−4.1480pp (CI−5.8637,−2.4322; Holm6<.001). Food−Cash average−1.1603pp is less precise. All sources and exact values, including other outcomes, are preserved in the row map.

## Suggestive findings

Adult ordinal omnibus raw/Holm21/minP21=.060289/.844045/.372663; midpoint=.032626/.522022/.231577; Top75=.009025/.180508/.082092. Adult Top75 Cash−Medical raw/Holm/minP=.003773/.079229/.039096; Cash−Food=.012426/.223668/.105489. Both Bonferroni21 intervals cross zero. Finite-family correction does not account for all historical research choices.

Food−Cash at5000 is+2.1677pp, pointwiseCI[−.6311,4.9665], Holm6=.387. Do not confirm a crossover. Equal-weight Restricted is a derived0.5Food+0.5Medical summary, never a fourth arm; historical pooled results retain their original samples and local correction families.

## Not established

Tail specificity (direct historical cross-threshold tests unconvincing); Food–Medical equivalence; Medical invariance; mental accounting; exclusion of bindingness; nationally representative effects; realized MPC. The Food expenditure triple contrast has rawP=.008396/Holm7=.050373 and specifically prevents exclusion of restrictions. Relative-income prediction gains are small and do not identify a process. Q1/Q2 Top75 pass/fail direct tests are .927/.994, but historical ordinal Q2 contrasts attenuate; do not generalize Top75 screen stability to all codings. Census weights have ESS315 uncapped or1191 with normalized cap10, not restored representativeness. All-X nulls do not establish zero moderation.

## Source review and precedence

Reviewed NCv5 text/Word, response memo and RESULT; PR15 result, intro outline, literature map, prediction table, relative-scale and questionnaire audits; PR14 Hero source/caption/audit; PR13 captions; PR12 all-X and PR11 who-drives notes; PR9 and PR10 discovery/strengthening notes and approved aggregate sources. PR16 supersedes obsolete1%relative-scale gates, mixed-statistic correction interpretation, bindingness exclusion and weighting-not-feasible language. Ordinal-score coding avoids monetary midpoint assumptions but still assumes equal rank spacing. The JEBO story decision must preserve this distinction.
'''
(O/'JEBO_EVIDENCE_FREEZE.md').write_text(text,encoding='utf-8')
print(f'Frozen {len(hashes)} historical files; mapped {len(rows)} approved aggregate rows; NC Word inspected.')
