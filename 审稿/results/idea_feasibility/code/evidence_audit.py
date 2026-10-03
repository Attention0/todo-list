"""Read-only availability/selection audit; no regressions or identity exports."""
import argparse,collections,csv,hashlib,json,pathlib,re,urllib.request,urllib.error,urllib.parse,xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime,timezone
from html.parser import HTMLParser

def records(path):
 if path.suffix=='.jsonl':
  with path.open(encoding='utf-8-sig') as f:
   for line in f:
    if line.strip():yield json.loads(line)
  return
 dec=json.JSONDecoder();buf='';pos=0;start=False
 with path.open(encoding='utf-8-sig') as f:
  while True:
   if pos>=len(buf) or not start:
    buf=buf[pos:]+f.read(1048576);pos=0
    if not buf:raise ValueError('Truncated JSON')
   while pos<len(buf) and buf[pos] in ' \r\n\t,':pos+=1
   if not start:
    if pos>=len(buf):continue
    if buf[pos]!='[':raise ValueError('JSON array required')
    pos+=1;start=True;continue
   if pos>=len(buf):continue
   if buf[pos]==']':return
   try:x,end=dec.raw_decode(buf,pos)
   except json.JSONDecodeError:
    chunk=f.read(1048576)
    if not chunk:raise
    buf=buf[pos:]+chunk;pos=0;continue
   yield x;pos=end

def number(x):
 try:return float(x)
 except (ValueError,TypeError):return float('nan')

def history(h):
 # Only fully bounded spells ending in 2024 or earlier. Open ends and 2025 dates stay unknown.
 good=[];invalid=0
 for j in h or []:
  if not isinstance(j,dict):invalid+=1;continue
  try:s=int(j['start']);e=int(j['end'])
  except (ValueError,TypeError,KeyError):invalid+=1;continue
  dom=(j.get('institution') or {}).get('domain')
  if not dom or s<1900 or e<s or e>2024:invalid+=1;continue
  good.append((str(dom).strip().lower(),s,e))
 return good,invalid

def overlap(r,a):return any(x==y and max(s,u)<=min(e,v) for x,s,e in r for y,u,v in a)
class Roster(HTMLParser):
 def __init__(self):super().__init__();self.role=None;self.sets=collections.defaultdict(set);self.links=collections.Counter()
 def handle_starttag(self,tag,attrs):
  at=dict(attrs)
  if tag=='h2':self.role=at.get('id')
  if tag=='a' and self.role in ['top-200-reviewers','reviewer','area-chair','senior-area-chair']:
   u=urllib.parse.urlparse(at.get('href',''));q=urllib.parse.parse_qs(u.query)
   if u.hostname=='openreview.net' and u.path=='/profile' and 'id' in q:
    self.links[self.role]+=1;self.sets[self.role].add(q['id'][0])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);ap.add_argument('--public-probes',action='store_true');args=ap.parse_args();d=args.project/'data';out=args.out
 if out.resolve().is_relative_to(args.project.resolve()):raise ValueError('Output must be outside the read-only original project')
 (out/'tables').mkdir(parents=True,exist_ok=True)
 def save(name,rows):pd.DataFrame(rows).to_csv(out/'tables'/(name+'.csv'),index=False)
 nfields=[];pilots=[];csv.field_size_limit(100000000)
 for role in ['reviewer','author']:
  n=0;counts=collections.Counter()
  with (d/(role+'_info.csv')).open(encoding='utf-8-sig',newline='') as f:
   for row in csv.DictReader(f):
    n+=1
    try:c=json.loads(row['profile']).get('content',{})
    except (ValueError,TypeError):c={}
    for k,v in c.items():
     if v not in [None,'',[],{}]:counts[k]+=1
    if role=='reviewer' and len(pilots)<3 and isinstance(c.get('dblp'),str) and '/pid/' in c['dblp']:
     pilots.append(c)
  for k in sorted(set(counts)|{'publications'}):nfields.append(dict(role=role,field=k,nonempty_profile_rows=counts[k],denominator=n))
 save('profile_field_support',nfields)
 mainids=set();compact=[];social=collections.Counter();chronology=collections.Counter();seen={};proximity=[]
 for r in records(d/'main_dataset.json'):
  rid=r.get('reviewer_id');pid=r['sub_number']
  if rid:mainids.add(rid)
  rh,ri=history(r.get('reviewer_history'));ah=[];ai=0;ahraw=r.get('authors_list_history') or []
  for h in ahraw:
   hh,ii=history(h);ah.extend(hh);ai+=ii
  social['rows']+=1;social['reviewer_has_bounded_pre2025_spell']+=int(bool(rh));social['all_authors_have_bounded_pre2025_spell']+=int(bool(ahraw) and all(history(h)[0] for h in ahraw))
  positive=overlap(rh,ah);social['positive_dated_institution_overlap_lower_bound']+=int(positive)
  complete=bool(rh) and bool(ahraw) and ri==0 and ai==0 and all(history(h)[0] for h in ahraw) and len(ahraw)==len(r.get('authors_list') or [])
  social['complete_retrospective_history_rows']+=int(complete)
  if positive or complete:proximity.append(dict(paper=pid,x=int(positive)))
  text=r.get('official_review_initial_content') or {};chars=sum(len(str((text.get(k) or {}).get('value') or '')) for k in ['summary','strengths','weaknesses','questions'])
  compact.append(dict(profile_link=bool(rid),paper=pid,rating=number(r.get('rating_initial')),confidence=number(r.get('confidence_initial')),author_slots=len(r.get('authors_list') or []),chars=chars,area=r.get('paper.primary_area') or 'missing'))
  if r.get('official_review_initial_tcdate'):chronology['dated_current_review']+=1
  if r.get('rating_initial') is not None and r.get('rating_final')!=r.get('rating_initial'):chronology['different_snapshot_rating']+=1
 df=pd.DataFrame(compact)
 selection=[]
 for known,g in df.groupby('profile_link'):
  selection.append(dict(profile_link=bool(known),review_rows=len(g),papers=g.paper.nunique(),rating_n=g.rating.notna().sum(),rating_mean=g.rating.mean(),confidence_mean=g.confidence.mean(),mean_author_slots=g.author_slots.mean(),mean_review_chars=g.chars.mean()))
 save('profile_missingness_selection',selection)
 area=pd.crosstab(df.area,df.profile_link);arearows=[]
 for cat,row in area.iterrows():
  arearows.append(dict(area=cat,missing_id_rows=int(row.get(False,0)),linked_id_rows=int(row.get(True,0))))
 save('profile_missingness_by_area',arearows)
 save('dated_proximity_availability',[dict(metric=k,n=v,denominator=social['rows']) for k,v in sorted(social.items())])
 if proximity:
  q=pd.DataFrame(proximity);n=q.groupby('paper').x.nunique();save('dated_proximity_variation',[dict(metric='informative_papers_in_partial_retrospective_positive_or_complete_subset',n=int((n>1).sum())),dict(metric='defined_rows_positive_or_complete_subset',n=len(q)),dict(metric='unknown_rows',n=social['rows']-len(q))])
 else:save('dated_proximity_variation',[dict(metric='defined_rows',n=0)])
 # Public/local review counts are not assignment logs. Dates alone cannot label emergency replacements.
 ref=next(records(d/'replies_official-review.json'));pub=collections.Counter();fields=collections.Counter();dates=[]
 for r in records(d/'replies_official-review.json'):
  pub['reviews']+=1;pub['version_2']+=int(r.get('version')==2);fields.update(r.keys());pub['has_numeric_cdate']+=int(isinstance(r.get('cdate'),int))
  invitations=r.get('invitations') or []
  pub['invitation_label_contains_emergency']+=int(any('emergency' in s.lower() for s in invitations))
  pub['has_replacement_or_emergency_flag']+=int(any(k in r for k in ['replacement','emergency','assignment_time','capacity','bid','affinity']))
 save('review_lineage_support',[dict(metric=k,n=v) for k,v in sorted(pub.items())])
 source=[]
 if args.public_probes:
  url='https://iclr.cc/Conferences/2026/ProgramCommittee'
  with urllib.request.urlopen(url,timeout=25) as f:html=f.read().decode('utf-8')
  parser=Roster();parser.feed(html)
  save('public_roster_coverage',[dict(role=role,profile_links=parser.links[role],unique_profile_ids=len(ids),local_reviewers_in_role=len(mainids&ids),local_unique_reviewers=len(mainids),complete_assignment_time_pool=False) for role,ids in sorted(parser.sets.items())])
  source.append(dict(check='2026_public_roster',status=200,records=len(parser.sets.get('reviewer',set())),meaning='post-conference role list; not frozen eligibility matrix'))
  urls=[('reviewer_group','https://api2.openreview.net/groups?id=ICLR.cc/2026/Conference/Reviewers'),('public_forum_notes','https://api2.openreview.net/notes?forum='+ref['forum']+'&limit=1000'),('public_review_edits','https://api2.openreview.net/notes/edits?note.id='+ref['id']+'&limit=1000')]
  for label,url in urls:
   try:
    with urllib.request.urlopen(url,timeout=15) as f:obj=json.load(f);code=f.status
    source.append(dict(check=label,status=code,records=len(obj.get('notes',obj.get('edits',obj.get('groups',[])))),meaning='anonymous access; no person-level export'))
   except urllib.error.HTTPError as e:source.append(dict(check=label,status=e.code,records=None,meaning='denied; no authentication or bypass; does not prove nonexistent'))
   except Exception as e:source.append(dict(check=label,status=type(e).__name__,records=None,meaning='access unverified'))
  save('public_access_checks',source)
  # Three deterministic valid DBLP links, selected before any outcomes. Metadata stays in memory.
  pilot=collections.Counter();pilot['profiles_attempted']=len(pilots)
  for c in pilots:
   parsed=urllib.parse.urlparse(c['dblp']);path=parsed.path
   if parsed.hostname not in ['dblp.org','www.dblp.org','dblp.uni-trier.de']:pilot['unsupported_host']+=1;continue
   path=re.sub(r'\.(html|xml)$','',path)+'.xml'
   try:
    with urllib.request.urlopen('https://dblp.org'+path,timeout=15) as f:xml=ET.fromstring(f.read())
    pilot['responses_ok']+=1;aliases={str(n.get('fullname','')).casefold() for n in c.get('names',[])}
    pilot['exact_profile_fullname_match']+=int(xml.attrib.get('name','').casefold() in aliases)
    pubs=xml.findall('r');pilot['publication_records']+=len(pubs)
    for p in pubs:
     year=p.find('.//year');title=p.find('.//title')
     if year is not None and year.text and year.text.isdigit() and int(year.text)<=2024:
      pilot['conservative_pre2025_publications']+=1;pilot['pre2025_with_title']+=int(title is not None)
      pilot['pre2025_with_abstract']+=int(p.find('.//abstract') is not None)
   except urllib.error.HTTPError as e:pilot['http_'+str(e.code)]+=1
   except Exception as e:pilot[type(e).__name__]+=1
  save('public_publication_pilot',[dict(metric=k,n=v) for k,v in sorted(pilot.items())])
 metadata=dict(scope='ICLR 2026 Conference outcomes only',publication_cutoff_utc='2025-09-01T00:00:00Z',year_only_conservative_cutoff='2024-12-31',regressions_run=0,main_rows=len(df),unique_reviewers=len(mainids),network_requests_enabled=args.public_probes,input_role='retrospective local data plus anonymous public probes',raw_person_rows_exported=0,run_time_utc=datetime.now(timezone.utc).isoformat())
 (out/'RUN_METADATA.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8');print(json.dumps(metadata))
if __name__=='__main__':main()
