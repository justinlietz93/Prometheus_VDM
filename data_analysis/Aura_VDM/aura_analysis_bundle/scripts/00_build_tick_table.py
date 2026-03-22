#!/usr/bin/env python3
"""Build a unified tick table from one or more events.jsonl sources.

Supports sources that are:
  - a .zip containing one or more members named *events.jsonl
  - a raw .jsonl file

Outputs:
  tables/tick_table_full.csv.gz

Notes:
  - Keeps only msg=='tick' records.
  - Extracts scalar fields (int/float/bool) and selected utd_spool scalar fields.
  - Adds derived columns: has_input, did_say (from utd_events.zip if provided), input_episode_id
  - Reindexes to full integer tick range.
"""
import argparse, json, zipfile, io
from pathlib import Path
import numpy as np
import pandas as pd

def iter_tick_records(source_path: str):
    if source_path.endswith('.zip'):
        with zipfile.ZipFile(source_path,'r') as zf:
            members=[n for n in zf.namelist() if n.endswith('events.jsonl')]
            if not members:
                raise FileNotFoundError(f'No events.jsonl member inside {source_path}')
            for member in members:
                with zf.open(member) as f:
                    tf=io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                    for line in tf:
                        line=line.strip()
                        if not line:
                            continue
                        try:
                            obj=json.loads(line)
                        except Exception:
                            continue
                        if isinstance(obj, dict) and obj.get('msg')=='tick':
                            yield obj
    else:
        with open(source_path,'r',encoding='utf-8', errors='ignore') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                try:
                    obj=json.loads(line)
                except Exception:
                    continue
                if isinstance(obj, dict) and obj.get('msg')=='tick':
                    yield obj

def extract_tick_features(rec: dict) -> dict:
    out={}
    for k,v in rec.items():
        if k in ('evt_memory_dict','evt_trail_dict','evt_firing_dict'):
            continue
        if isinstance(v,(int,float,bool)) or v is None:
            out[k]=int(v) if isinstance(v,bool) else v
    spool=rec.get('utd_spool')
    if isinstance(spool, dict):
        for sk,sv in spool.items():
            if isinstance(sv,(int,float,bool)):
                out[f'utd_spool_{sk}']=int(sv) if isinstance(sv,bool) else sv
    return out

def parse_utd_say_ticks(utd_zip_path: str):
    say_ticks=set()
    if not utd_zip_path:
        return say_ticks
    with zipfile.ZipFile(utd_zip_path,'r') as zf:
        for name in zf.namelist():
            if not name.endswith('.jsonl'):
                continue
            with zf.open(name) as f:
                tf=io.TextIOWrapper(f, encoding='utf-8', errors='ignore')
                for line in tf:
                    if '"macro": "say"' not in line:
                        continue
                    try:
                        obj=json.loads(line)
                    except Exception:
                        continue
                    t=obj.get('args',{}).get('why',{}).get('t')
                    if isinstance(t,int):
                        say_ticks.add(t)
    return say_ticks

def build_input_episode_ids(has_input: np.ndarray, bridge_gaps: int=2) -> np.ndarray:
    ep_id=np.full(len(has_input), -1, dtype=int)
    cur=-1
    gap=0
    in_ep=False
    for i,hi in enumerate(has_input):
        if hi==1:
            if not in_ep:
                cur += 1
                in_ep=True
            ep_id[i]=cur
            gap=0
        else:
            if in_ep:
                gap += 1
                if gap<=bridge_gaps:
                    ep_id[i]=cur
                else:
                    in_ep=False
                    gap=0
    return ep_id

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--events', nargs='+', required=True, help='events.jsonl sources (.zip or .jsonl)')
    ap.add_argument('--utd_zip', default='', help='Optional utd_events.zip to mark did_say ticks')
    ap.add_argument('--out_csv_gz', required=True, help='Output path for tick_table_full.csv.gz')
    args=ap.parse_args()

    rows=[]
    for src in args.events:
        for rec in iter_tick_records(src):
            row=extract_tick_features(rec)
            if 't' in row:
                rows.append(row)

    if not rows:
        raise RuntimeError('No tick rows parsed.')

    df=pd.DataFrame(rows)
    df=df.drop_duplicates(subset=['t']).sort_values('t').set_index('t')

    full_index=pd.Index(range(int(df.index.min()), int(df.index.max())+1), name='t')
    df=df.reindex(full_index)

    # derived: input + say
    has_input=((df.get('ute_text_count',0).fillna(0)>0) | (df.get('ute_in_count',0).fillna(0)>0)).astype(int)
    df['has_input']=has_input
    df['input_episode_id']=build_input_episode_ids(has_input.values, bridge_gaps=2)

    say_ticks=parse_utd_say_ticks(args.utd_zip) if args.utd_zip else set()
    df['did_say']=df.index.to_series().apply(lambda t: 1 if int(t) in say_ticks else 0).astype(int)

    out_path=Path(args.out_csv_gz)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.reset_index().to_csv(out_path, index=False, compression='gzip')
    print(f'Wrote {out_path} ({out_path.stat().st_size/1e6:.2f} MB)')

if __name__=='__main__':
    main()