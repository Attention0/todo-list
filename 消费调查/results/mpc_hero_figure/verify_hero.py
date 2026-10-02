"""Fidelity/export checks for presentation-only hero package."""
from pathlib import Path
import hashlib
import json
import ast
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from PIL import Image
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
PRIOR = OUT.parent/'nature_main_figures'
checks = []
def check(condition, label):
    assert condition, label
    checks.append(label)
def equal(a, b, label):
    check(np.allclose(a, b, rtol=0, atol=1e-14, equal_nan=True), label)

manifest = json.loads((OUT/'source_manifest.json').read_text(encoding='utf-8'))
for f in manifest['inputs']:
    check(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest() == f['sha256'], 'frozen input hash: '+f['path'])
dist = pd.read_csv(PRIOR/'figureS_distribution_source.csv', float_precision='round_trip')
means = pd.read_csv(PRIOR/'figure1_main_source.csv', float_precision='round_trip')
hero = pd.read_csv(OUT/'hero_figure_source.csv', float_precision='round_trip')
shift = pd.read_csv(OUT/'distribution_shift_fingerprint_source.csv', float_precision='round_trip')
check(len(hero)==63 and len(shift)==18, 'aggregate-only source row counts 54+9 / 18')
check(dist.N.sum()==5497, 'frozen total sample 5497')
check(not hero[['panel','form','amount','category']].duplicated().any(), 'hero keys unique')
for _, r in hero.iterrows():
    src = (dist if r.panel=='A' else means).iloc[int(r.source_row)-1]
    check(src.form==r.form and src.amount==r.amount and src.N==r.N, f'hero source key/N row {r.name+1}')
    check(src.source_file==r.upstream_source_file and src.source_row==r.upstream_source_row and src.source_commit==r.upstream_source_commit, f'hero upstream provenance row {r.name+1}')
    if r.panel=='A':
        equal(r.estimate, src[f'p{int(r.category)}'], f'atlas bin identity row {r.name+1}')
        check(pd.isna(r.lower_ci) and pd.isna(r.upper_ci), f'no invented atlas CI row {r.name+1}')
    else:
        equal([r.estimate,r.lower_ci,r.upper_ci], [src.estimate,src.lower_ci,src.upper_ci], f'approved mean/CI row {r.name+1}')
        check(src.outcome=='midpoint' and r.ci_definition==src.ci_definition, f'approved outcome/CI definition row {r.name+1}')
for (form,amount), d in hero[hero.panel=='A'].groupby(['form','amount']):
    equal(d.estimate.sum(), 1, f'composition sums to one {form}/{amount}')
    check((d.estimate>=0).all() and (d.estimate<=1).all(), f'valid proportions {form}/{amount}')
    m = hero[(hero.panel=='B') & (hero.form==form) & (hero.amount==amount)].iloc[0]
    equal(np.dot(d.sort_values('category').estimate,[0,.05,.175,.375,.625,.875]), m.estimate, f'distribution/mean coding consistency {form}/{amount}')
for _, r in shift.iterrows():
    lo, hi = dist.iloc[int(r.source_row_200)-1], dist.iloc[int(r.source_row_5000)-1]
    check(lo.form==r.form==hi.form and lo.amount==200 and hi.amount==5000, f'fingerprint source keys row {r.name+1}')
    equal([r.probability_200,r.probability_5000], [lo[f'p{r.category}'],hi[f'p{r.category}']], f'fingerprint endpoint identity row {r.name+1}')
    equal(r.difference, r.probability_5000-r.probability_200, f'fingerprint subtraction row {r.name+1}')
    equal(r.difference_pp, 100*r.difference, f'pp unit identity row {r.name+1}')
    check(r.N_200==lo.N and r.N_5000==hi.N, f'fingerprint approved Ns row {r.name+1}')
    check(pd.isna(r.lower_ci) and pd.isna(r.upper_ci), f'no invented difference CI row {r.name+1}')
for form,d in shift.groupby('form'):
    equal(d.difference.sum(),0,f'zero-sum distribution difference {form}')
tail = hero[(hero.panel=='A') & (hero.form=='cash') & (hero.category==6)].set_index('amount').estimate
check(f'{tail[200]*100:.1f}%'=='13.4%' and f'{tail[5000]*100:.1f}%'=='5.3%', 'approved Cash annotation rounding')
equal(shift[(shift.form=='cash') & (shift.category==6)].difference_pp.iloc[0], -8.10050456989842, 'Cash top-tail -8.1005 pp')
equal(shift[(shift.form=='cash') & (shift.category==1)].difference_pp.iloc[0], -.07607276429062, 'Cash no-spending -0.0761 pp')

for name, height in [('hero_figure',138),('distribution_shift_fingerprint',79)]:
    pdf = PdfReader(OUT/f'{name}.pdf')
    check(len(pdf.pages)==1, name+' single PDF page')
    page=pdf.pages[0]
    check(abs(float(page.mediabox.width)*25.4/72-180)<1e-7,name+' PDF width 180mm (PDF serialization tolerance)')
    check(abs(float(page.mediabox.height)*25.4/72-height)<1e-7,name+' PDF height (PDF serialization tolerance)')
    check(len(page.images)==0,name+' vector PDF, no image objects')
    check('200' in page.extract_text() and '75%' in page.extract_text(),name+' extractable PDF text')
    fonts=page['/Resources']['/Font'].get_object()
    check(any('/FontDescriptor' in ft.get_object() or '/DescendantFonts' in ft.get_object() for ft in fonts.values()),name+' embedded font resources')
    svg = ET.parse(OUT/f'{name}.svg')
    check(len(svg.findall('.//{http://www.w3.org/2000/svg}text'))>0,name+' SVG editable text')
    check(len(svg.findall('.//{http://www.w3.org/2000/svg}image'))==0,name+' SVG no raster images')
    with Image.open(OUT/f'{name}.png') as im:
        check(abs(im.width-180/25.4*600)<2 and abs(im.height-height/25.4*600)<2,name+' PNG 600dpi pixel dimensions')
        check(all(abs(d-600)<1 for d in im.info['dpi']),name+' PNG 600dpi metadata')
        check(im.convert('RGB').getpixel((0,0))==(255,255,255),name+' white background')
tree=ast.parse((OUT/'plot_hero.py').read_text(encoding='utf-8'))
imports=[n.module if isinstance(n,ast.ImportFrom) else a.name for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) for a in (n.names if isinstance(n,ast.Import) else [None])]
check(not any(x and any(t in x for t in ['statsmodels','sklearn','scipy','pyreadstat']) for x in imports), 'no estimation/raw-data libraries imported')
code=(OUT/'plot_hero.py').read_text(encoding='utf-8')
check('read_stata' not in code and '.dta' not in code and 'read_spss' not in code,'no respondent data access')
check(not any(p.suffix.lower() in ['.dta','.sav','.xlsx'] for p in OUT.iterdir()), 'no respondent-level/raw data artifacts')
result=dict(passed=len(checks), failed=0, checks=checks,
    scope='numerical/export verification; visual PDF/PNG/grayscale inspection documented separately')
(OUT/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(f'{len(checks)} checks passed.')
