"""Read-only ICLR audit. Only aggregate tables are exported; raw identities stay in memory."""
import argparse, collections, csv, hashlib, json, math, pathlib, re, sys
import numpy as np
import pandas as pd
import statsmodels.api as sm

def records(path):
    if path.suffix == '.jsonl':
        with path.open(encoding='utf-8-sig') as f:
            for line in f:
                if line.strip(): yield json.loads(line)
        return
    decoder=json.JSONDecoder(); buf=''; pos=0; eof=False; started=False
    with path.open(encoding='utf-8-sig') as f:
        while True:
            if pos>=len(buf) or not started:
                buf=buf[pos:]+f.read(1048576);pos=0
                if not buf: raise ValueError('Truncated JSON array')
            while pos<len(buf) and buf[pos] in ' \r\n\t,':pos+=1
            if not started:
                if pos>=len(buf):continue
                if buf[pos]!='[':raise ValueError('Expected JSON array')
                pos+=1;started=True;continue
            if pos>=len(buf):continue
            if buf[pos]==']':return
            try:value,end=decoder.raw_decode(buf,pos)
            except json.JSONDecodeError:
                chunk=f.read(1048576)
                if not chunk:raise
                buf=buf[pos:]+chunk;pos=0;continue
            yield value;pos=end

def present(x): return x is not None and x!='' and x!=[] and x!={}
def val(x): return x.get('value') if isinstance(x,dict) else x

def numeric(x):
    try: return float(val(x))
    except (ValueError,TypeError): return np.nan

def time(x):
    if x is None or x=='':return pd.NaT
    try:
        t=pd.Timestamp(x)
        return (t.tz_localize('Asia/Shanghai') if t.tzinfo is None else t).tz_convert('UTC')
    except (ValueError,TypeError):return pd.NaT

def content_hash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
def insts(history):
    # Snapshot domains with recorded start year <=2025; unknown start excluded.
    if not isinstance(history,list): return set()
    result=set()
    for h in history:
        if not isinstance(h,dict): continue
        try: start=int(h.get('start'))
        except (ValueError,TypeError): continue
        if start>2025: continue
        i=h.get('institution') or {}; domain=i.get('domain')
        if domain: result.add(domain.strip().lower())
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--project',required=True,type=pathlib.Path);ap.add_argument('--out',required=True,type=pathlib.Path);a=ap.parse_args()
    d=a.project/'data';out=a.out; (out/'tables').mkdir(parents=True,exist_ok=True)
    def save(name,rows): pd.DataFrame(rows).to_csv(out/'tables'/(name+'.csv'),index=False,encoding='utf-8')
    inventory=[]
    for p in sorted(a.project.rglob('*')):
        if p.is_file():
            h=hashlib.sha256()
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
            inventory.append(dict(path=p.relative_to(a.project).as_posix(),bytes=p.stat().st_size,modified_utc=pd.Timestamp(p.stat().st_mtime,unit='s',tz='UTC').isoformat(),sha256=h.hexdigest()))
    save('file_inventory',inventory)
    profile_sets={}; profile_report=[]
    for role in ['reviewer','author']:
        ids=set();valid=set();counts=collections.Counter();n=0
        with (d/(role+'_info.csv')).open(encoding='utf-8-sig',newline='') as f:
            csv.field_size_limit(100000000)
            for row in csv.DictReader(f):
                n+=1;ids.add(row['id'])
                try: p=json.loads(row['profile']);c=p.get('content',{})
                except (ValueError,TypeError): c={}
                if c:valid.add(row['id'])
                for k in ['history','expertise','relations','orcid','dblp','gscholar','semanticScholar']:
                    counts[k]+=int(present(c.get(k)))
        profile_sets[role]=(ids,valid)
        profile_report.append(dict(role=role,rows=n,unique_ids=len(ids),valid_content=len(valid),**counts))
    save('profile_coverage',profile_report)
    print('profiles complete',flush=True)
    rawpapers={};rawreviews={};rawauthors=set();rawreviewers=set()
    for p in records(d/'iclr2026_reviews_10000.jsonl'):
        rawpapers[p['submission_number']]=len(p.get('reviews',[]))
        for au in p.get('authors',[]):
            if au.get('id'):rawauthors.add(au['id'])
        for r in p.get('reviews',[]):
            rid=(r.get('reviewer_profile') or {}).get('id')
            if rid:rawreviewers.add(rid)
            rawreviews[r['id']]=content_hash(r.get('content'))
    submissions={r['submission_number'] for r in records(d/'submissions_info.json')}
    co={}
    for role,other in [('reviewer',rawauthors),('author',rawreviewers)]:
        co[role]={r['id']:set(r.get('coauthors',[]))&other for r in records(d/(role+'_coauthors.json'))}
    reviews={};rcount=0;versions=collections.Counter()
    for r in records(d/'replies_official-review.json'):
        rcount+=1;reviews[r['id']]=content_hash(r.get('content'));versions[str(r.get('version'))]+=1
    print('reviews complete',flush=True)
    comments=collections.Counter();comment_papers=set()
    for r in records(d/'replies_official-comment.json'):
        comments['rows']+=1;comment_papers.add(r.get('submission_number'));comments['has_time']+=int(present(r.get('tcdate')))
    print('comments complete',flush=True)
    fields=collections.Counter();types=collections.defaultdict(collections.Counter);nonempty=collections.Counter();rows=[];checks=collections.Counter();authors=set();reviewers=set();reviewids=set();pairs=set();date_ranges=collections.defaultdict(list)
    for r in records(d/'main_dataset.json'):
        if len(rows)%5000==0: print('main rows',len(rows),flush=True)
        for k,v in r.items():fields[k]+=1;types[k][type(v).__name__]+=1;nonempty[k]+=int(present(v))
        pid=r['sub_number'];rid=r.get('reviewer_id');aid=r.get('authors_list') or [];revid=r.get('reviewer_nickname')
        authors.update(aid)
        if rid:reviewers.add(rid)
        checks['duplicate_review_id']+=int(revid in reviewids);reviewids.add(revid)
        checks['duplicate_paper_reviewer']+=int(rid is not None and (pid,rid) in pairs);pairs.add((pid,rid))
        checks['submission_join']+=int(pid in submissions);checks['review_join']+=int(revid in reviews);checks['raw_review_join']+=int(revid in rawreviews)
        checks['reviewer_profile_id_join']+=int(rid in profile_sets['reviewer'][0]);checks['reviewer_profile_valid']+=int(rid in profile_sets['reviewer'][1])
        checks['author_profile_slots']+=len(aid);checks['author_profile_id_join']+=sum(x in profile_sets['author'][0] for x in aid);checks['author_profile_valid']+=sum(x in profile_sets['author'][1] for x in aid)
        rr=reviews.get(revid);raw=rawreviews.get(revid)
        ci=r.get('official_review_initial_content') or {};cf=r.get('official_review_final_content') or {}
        checks['initial_equals_current_raw_content']+=int(content_hash(ci)==rr);checks['final_equals_snapshot_content']+=int(content_hash(cf)==raw)
        for col in ['rating_initial','confidence_initial']:
            key=col.split('_')[0]; checks[col+'_mismatch']+=int(not np.isnan(numeric(r.get(col))) and numeric(r.get(col))!=numeric(ci.get(key)))
        ri=numeric(r.get('rating_initial'));rf=numeric(r.get('rating_final'));cfi=numeric(r.get('confidence_initial'))
        rh=insts(r.get('reviewer_history'));ah=set().union(*(insts(h) for h in (r.get('authors_list_history') or [])))
        hist_known=bool(rh) and all(bool(insts(h)) for h in (r.get('authors_list_history') or [])) and len(r.get('authors_list_history') or [])==len(aid) and bool(aid)
        co_known=rid in co['reviewer'] and all(x in co['author'] for x in aid) and bool(aid)
        copos=bool(set(aid)&co['reviewer'].get(rid,set())) or any(rid in co['author'].get(x,set()) for x in aid)
        it=time(r.get('official_review_initial_tcdate'));mt=time(r.get('official_review_initial_tmdate'));ar=time(r.get('arxiv_published'))
        for k in ['official_review_initial_tcdate','official_review_initial_tmdate','sub_cdate','sub_mdate']:
            t=time(r.get(k))
            if pd.notna(t): date_ranges[k].append(t)
        # Native cdate/mdate confirms Shanghai strings; test original stored-ms interpretation.
        stored=numeric(r.get('official_review_initial_tcdate_ms'))
        if pd.notna(it) and not np.isnan(stored):
            checks['time_ms_equals_utc']+=int(abs(stored-(it.timestamp()+28800)*1000)<1)
            checks['time_ms_equals_shanghai_local']+=int(abs(stored-it.timestamp()*1000)<1)
        rows.append(dict(paper=pid,reviewer=rid,review=revid,rating_initial=ri,rating_final=rf,confidence_initial=cfi,confidence_final=numeric(r.get('confidence_final')),institution_overlap_snapshot=float(bool(rh&ah)) if hist_known else np.nan,coauthor_overlap_undated=float(copos) if co_known else np.nan,arxiv_match=pd.notna(ar),arxiv_before_review_candidate=pd.notna(ar) and pd.notna(it) and ar<it,review_text_chars=sum(len(str(val(ci.get(k)) or '')) for k in ['summary','strengths','weaknesses','questions']),initial_mod_after_release=pd.notna(mt) and mt>=pd.Timestamp('2025-11-11',tz='UTC')))
    df=pd.DataFrame(rows);N=len(df)
    save('field_coverage',[dict(variable=k,rows=N,present=fields[k],nonempty=nonempty[k],missing_or_empty=N-nonempty[k],types=json.dumps(types[k])) for k in sorted(fields)])
    save('year_structure',[dict(year=2026,raw_papers=len(rawpapers),raw_papers_with_reviews=sum(v>0 for v in rawpapers.values()),raw_reviews=len(rawreviews),main_rows=N,main_papers=df.paper.nunique(),main_reviewers=len(reviewers),main_authors=len(authors),raw_reviewers=len(rawreviewers),raw_authors=len(rawauthors),public_submissions=len(submissions),public_review_rows=rcount,public_unique_review_ids=len(reviews),comment_rows=comments['rows'],comment_papers=len(comment_papers),reviewer_author_overlap=len(reviewers&authors),regime='nominal double blind; incident exposure unobserved')])
    save('join_checks',[dict(check=k,n=v,denominator=checks['author_profile_slots'] if k.startswith('author_profile') and k!='author_profile_slots' else N) for k,v in sorted(checks.items())])
    save('date_ranges',[dict(field=k,min=str(min(v)),max=str(max(v))) for k,v in date_ranges.items()])
    save('review_versions',[dict(version=k,n=v) for k,v in versions.items()])
    for col in ['rating_initial','rating_final','confidence_initial','confidence_final']:
        save(col+'_distribution',[dict(year=2026,value=x,n=int(n)) for x,n in df[col].value_counts(dropna=False).sort_index().items()])
    size=df.groupby('paper').size();save('reviews_per_paper',[dict(reviews=int(x),papers=int(n)) for x,n in size.value_counts().sort_index().items()])
    save('diagnostic_summary',[dict(variable=k,n=int(df[k].notna().sum()),mean=float(df[k].mean()),sd=float(df[k].std()),min=float(df[k].min()),max=float(df[k].max())) for k in ['rating_initial','rating_final','confidence_initial','confidence_final','review_text_chars','institution_overlap_snapshot','coauthor_overlap_undated']])
    paired=df.dropna(subset=['rating_initial','rating_final']);diff=paired.rating_final-paired.rating_initial
    save('snapshot_contrast',[dict(n=len(paired),different=int((diff!=0).sum()),mean_snapshot_minus_current=float(diff.mean()),positive=int((diff>0).sum()),negative=int((diff<0).sum()),current_note_modified_after_release=int(df.initial_mod_after_release.sum()),arxiv_matches=int(df.groupby('paper').arxiv_match.first().sum()),arxiv_before_review_candidates=int(df.groupby('paper').arxiv_before_review_candidate.max().sum()))])
    results=[]
    for x in ['institution_overlap_snapshot','coauthor_overlap_undated']:
        for y in ['rating_initial','confidence_initial']:
            q=df.dropna(subset=[x,y]).drop_duplicates(['paper','reviewer']).copy();vary=q.groupby('paper')[x].nunique();q=q[q.paper.isin(vary[vary>1].index)]
            if len(q)<20 or q[x].nunique()<2:continue
            z=q[[x,y]]-q.groupby('paper')[[x,y]].transform('mean')
            fit=sm.OLS(z[y],z[[x]]).fit(cov_type='cluster',cov_kwds={'groups':q.paper})
            results.append(dict(x=x,y=y,n=len(q),papers=q.paper.nunique(),beta=float(fit.params[x]),se_paper_cluster=float(fit.bse[x]),p_asymptotic=float(fit.pvalues[x]),fe='paper demeaned; informative papers only',controls='none',interpretation='descriptive association; snapshot timing and selection unresolved'))
    save('within_paper_associations',results)
    # Aggregate disagreement by mixed observed proximity; no individual rows exported.
    groups=[]
    for x in ['institution_overlap_snapshot','coauthor_overlap_undated']:
        q=df.dropna(subset=[x,'rating_initial']).drop_duplicates(['paper','reviewer']).groupby('paper').agg(n=('rating_initial','size'),sd=('rating_initial','std'),mixed=(x,'nunique'))
        q=q[q.n>=2]
        for mixed,g in q.groupby(q.mixed>1): groups.append(dict(x=x,mixed=bool(mixed),papers=len(g),mean_score_sd=float(g.sd.mean())))
    save('disagreement',groups)
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    (out/'figures').mkdir(exist_ok=True)
    fig,axs=plt.subplots(1,2,figsize=(10,4))
    for ax,col in zip(axs,['rating_initial','confidence_initial']):
        vc=df[col].value_counts().sort_index();ax.bar(vc.index,vc.values,color='#365f8c');ax.set(title=col+' (current-note snapshot)',xlabel='Observed scale',ylabel='Review rows')
    fig.tight_layout();fig.savefig(out/'figures/distributions.svg');plt.close(fig)
    payload=dict(N=N,checks=dict(checks),result_rows=len(results),input_files=len(inventory),python=sys.version.split()[0],pandas=pd.__version__,numpy=np.__version__,statsmodels=sm.__version__ if hasattr(sm,'__version__') else __import__('statsmodels').__version__)
    (out/'RUN_METADATA.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2))
if __name__=='__main__':main()
