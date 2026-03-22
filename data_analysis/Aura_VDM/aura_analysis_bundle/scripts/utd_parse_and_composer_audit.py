#!/usr/bin/env python3
"""
UTD parse + composer audit for VDM (2026-02-04 run).

Outputs:
- tables/say_event_composer_audit_metrics.csv
- figures/*.png
- SHA256SUMS.csv

Notes:
- Input text lines in UTD stream have no explicit tick; this assigns them to the *next* status tick.
"""
import os, io, re, json, math, zipfile, hashlib
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def tokenize_text(text: str):
    return [w.lower() for w in re.findall(r"\S+", str(text))]

def trigrams(tokens):
    for i in range(len(tokens)-2):
        yield (tokens[i], tokens[i+1], tokens[i+2])

def jaccard(a:set, b:set):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0

def longest_common_substring_len(a, b):
    n=len(a); m=len(b)
    if n==0 or m==0:
        return 0
    prev=[0]*(m+1)
    best=0
    for i in range(1,n+1):
        curr=[0]*(m+1)
        ai=a[i-1]
        for j in range(1,m+1):
            if ai==b[j-1]:
                curr[j]=prev[j-1]+1
                if curr[j]>best: best=curr[j]
        prev=curr
    return best

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    utd_zip_path = os.environ.get("UTD_ZIP", "/mnt/data/utd_events.jsonl.20260204_150151.zip")
    out_dir = os.environ.get("OUT_DIR", "/mnt/data/vdm_intent_content_composer_audit_20260204_v1_repro")
    tables_dir=os.path.join(out_dir,"tables"); fig_dir=os.path.join(out_dir,"figures")
    os.makedirs(tables_dir, exist_ok=True); os.makedirs(fig_dir, exist_ok=True)

    zf=zipfile.ZipFile(utd_zip_path,'r')
    names=zf.namelist()

    status_records=[]
    input_texts_by_tick=defaultdict(list)
    say_events=[]
    pending_texts=[]

    for name in names:
        with zf.open(name) as f:
            for line in io.TextIOWrapper(f, encoding='utf-8', errors='ignore'):
                line=line.strip()
                if not line: continue
                obj=json.loads(line)
                if obj.get('type')=='text' and isinstance(obj.get('payload'), dict):
                    p=obj['payload']
                    if p.get('type')=='text':
                        msg=str(p.get('msg',''))
                        if msg:
                            pending_texts.append(msg)
                    elif p.get('type')=='status':
                        t=int(p.get('t'))
                        rec=p.copy()
                        status_records.append(rec)
                        if pending_texts:
                            input_texts_by_tick[t].extend(pending_texts)
                            pending_texts=[]
                elif obj.get('type')=='macro' and obj.get('macro')=='say':
                    args=obj.get('args',{})
                    why=args.get('why',{}) if isinstance(args,dict) else {}
                    t=int(why.get('t', -1))
                    say_events.append({
                        "t": t,
                        "text": args.get('text',''),
                        **{f"why_{k}":v for k,v in why.items() if k!='t'}
                    })

    status_df=pd.DataFrame(status_records).drop(columns=['type'])
    # input per tick
    input_rows=[]
    for t,msgs in input_texts_by_tick.items():
        combined=" ".join(msgs)
        toks=tokenize_text(combined)
        input_rows.append({
            "t": t,
            "input_text": combined,
            "input_msg_count": len(msgs),
            "input_token_count": len(toks),
            "input_unique_tokens": len(set(toks))
        })
    input_df=pd.DataFrame(input_rows)
    tick_df=status_df.merge(input_df, on='t', how='left')
    tick_df['has_input']=tick_df['input_msg_count'].fillna(0).astype(int)>0
    tick_df[['input_msg_count','input_token_count','input_unique_tokens']] = tick_df[['input_msg_count','input_token_count','input_unique_tokens']].fillna(0).astype(int)

    say_df=pd.DataFrame(say_events)
    say_merged=say_df.merge(tick_df, on='t', how='left')

    # token sets
    input_tokens_by_tick={int(r.t): set(tokenize_text(r.input_text)) for r in input_df.itertuples(index=False)}
    input_ticks_sorted=sorted(input_tokens_by_tick.keys())

    # trigram corpus
    corpus_tri=set()
    for r in input_df.itertuples(index=False):
        toks=tokenize_text(r.input_text)
        for tri in trigrams(toks):
            corpus_tri.add(tri)

    # TF-IDF on input docs
    input_docs=input_df.sort_values('t')
    doc_ticks=input_docs['t'].astype(int).tolist()
    docs=input_docs['input_text'].fillna("").tolist()
    vectorizer=TfidfVectorizer(lowercase=True, ngram_range=(1,2), min_df=2, max_df=0.95)
    X=vectorizer.fit_transform(docs)
    Y=vectorizer.transform(say_merged['text'].fillna("").tolist())
    S=linear_kernel(Y,X)
    doc_ticks_arr=np.array(doc_ticks)

    rows=[]
    for i,ev in enumerate(say_merged.itertuples(index=False)):
        t=int(ev.t)
        say_tokens_list=tokenize_text(ev.text)
        say_tokens=set(say_tokens_list)
        imm=jaccard(say_tokens, input_tokens_by_tick.get(t,set()))

        # trigram fraction
        tris=list(trigrams(say_tokens_list))
        tri_frac = (sum(1 for tri in tris if tri in corpus_tri)/len(tris)) if tris else 0.0

        # best TF-IDF among past docs only
        cutoff=np.searchsorted(doc_ticks_arr, t, side='right')
        sims=S[i][:cutoff] if cutoff>0 else np.array([])
        if len(sims)>0:
            top1_idx=int(np.argmax(sims))
            top1_tick=int(doc_ticks_arr[top1_idx])
            top1_sim=float(sims[top1_idx])
        else:
            top1_tick=None; top1_sim=0.0

        # best jaccard match among past input ticks (coarse pointer)
        best_j=0.0; best_tick=None
        for tick in input_ticks_sorted:
            if tick>t: break
            sim=jaccard(say_tokens, input_tokens_by_tick[tick])
            if sim>best_j:
                best_j=sim; best_tick=tick

        # contiguous overlap with best-jaccard tick
        if best_tick is not None:
            in_tokens_list=tokenize_text(" ".join(input_texts_by_tick.get(best_tick, [])))
            lcs=longest_common_substring_len(say_tokens_list, in_tokens_list)
            lcs_frac_say=lcs/len(say_tokens_list) if say_tokens_list else 0.0
        else:
            lcs=0; lcs_frac_say=0.0

        rows.append({
            "t": t,
            "has_input": bool(getattr(ev,"has_input", False)),
            "say_len_tokens": len(say_tokens_list),
            "say_unique_tokens": len(say_tokens),
            "imm_jaccard": imm,
            "tri_frac_in_corpus": tri_frac,
            "past_tfidf_top1_tick": top1_tick,
            "past_tfidf_top1_sim": top1_sim,
            "past_tfidf_top1_lag": (t-top1_tick) if top1_tick is not None else None,
            "best_all_tick_jaccard": best_tick,
            "best_all_jaccard": best_j,
            "best_all_lag": (t-best_tick) if best_tick is not None else None,
            "lcs_substr_len_vs_best_jaccard": lcs,
            "lcs_frac_say": lcs_frac_say,
        })

    out=pd.DataFrame(rows)
    out.to_csv(os.path.join(tables_dir,"say_event_composer_audit_metrics.csv"), index=False)

    # plots
    plt.figure()
    plt.hist(out['tri_frac_in_corpus'], bins=20)
    plt.xlabel("Fraction of output trigrams found in input corpus")
    plt.ylabel("Count of say events")
    plt.title("Composer signature: trigram reuse vs input corpus")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir,"trigram_fraction_hist.png"), dpi=200)
    plt.close()

    plt.figure()
    plt.hist(out['lcs_substr_len_vs_best_jaccard'], bins=20)
    plt.xlabel("Longest common contiguous token run vs best input tick")
    plt.ylabel("Count of say events")
    plt.title("Copying vs recombination: contiguous overlap lengths")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir,"lcs_contiguous_len_hist.png"), dpi=200)
    plt.close()

    # sha256 sums
    sums=[]
    for root,_,files in os.walk(out_dir):
        for fn in files:
            path=os.path.join(root,fn)
            if fn=="SHA256SUMS.csv": 
                continue
            rel=os.path.relpath(path,out_dir)
            sums.append({"file":rel,"sha256":sha256_file(path)})
    pd.DataFrame(sums).sort_values("file").to_csv(os.path.join(out_dir,"SHA256SUMS.csv"), index=False)

if __name__=="__main__":
    main()
