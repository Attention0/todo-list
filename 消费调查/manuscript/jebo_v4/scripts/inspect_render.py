"""Generate native-size paired pages and PDF layout inventory for human visual QA."""
from pathlib import Path
from PIL import Image,ImageDraw
import pdfplumber,json
M=Path(__file__).resolve().parents[1];out=M/'qa/final';report=[]
for stem in ['JEBO_manuscript_v4','JEBO_supplement_v4','JEBO_Highlights_v4']:
    folder=out/stem;pdf=pdfplumber.open(folder/(stem+'.pdf'));pages=[]
    for i,page in enumerate(pdf.pages):
        spans=page.chars;txt=page.extract_text() or ''
        overflow=[s['text'] for s in spans if s['x0']<30 or s['x1']>page.width-25 or s['top']<20 or s['bottom']>page.height-20]
        pages.append({'page':i+1,'characters':len(txt),'overflow':overflow,'fonts':sorted(set(s['fontname'] for s in spans)),'start':txt[:100],'end':txt[-120:]})
    # Only current PDF page count: obsolete previous-render images are excluded.
    files=sorted(folder.glob('page-*.png'))[:len(pdf.pages)]
    for i in range(0,len(files),2):
        imgs=[Image.open(f).convert('RGB') for f in files[i:i+2]]
        sheet=Image.new('RGB',(sum(im.width for im in imgs),max(im.height for im in imgs)), 'white');x=0
        for im in imgs:sheet.paste(im,(x,0));x+=im.width
        sheet.save(folder/f'pair-{i+1:02d}-{min(i+2,len(files)):02d}.png')
    report.append({'document':stem,'pages':len(pdf.pages),'layout':pages})
(M/'qa/render_inventory.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps([{'document':r['document'],'pages':r['pages'],'overflow_pages':[p['page'] for p in r['layout'] if p['overflow']],'fonts':sorted(set(f for p in r['layout'] for f in p['fonts']))} for r in report],indent=2))
