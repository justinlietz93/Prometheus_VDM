"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

#!/usr/bin/env python3
import json, argparse, os, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_jsonl(path):
    rows=[]
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try:
                rows.append(json.loads(line))
            except Exception:
                line=re.sub(r",\s*}", "}", re.sub(r",\s*]", "]", line))
                rows.append(json.loads(line))
    return pd.DataFrame(rows)

def grid_from_series(series, size, reducer="mean"):
    acc = np.zeros((size*size,), dtype=np.float64)
    cnt = np.zeros((size*size,), dtype=np.int32)
    last = np.full((size*size,), np.nan, dtype=np.float64)
    for d in series:
        if not isinstance(d, dict): 
            continue
        for k, v in d.items():
            try:
                idx = int(k)
            except:
                continue
            if idx<0 or idx>=size*size: 
                continue
            val = float(v)
            acc[idx]+=val
            cnt[idx]+=1
            last[idx]=val
    if reducer=="mean":
        with np.errstate(invalid="ignore", divide="ignore"):
            arr = acc/np.where(cnt==0, np.nan, cnt)
    else:
        arr = last
    return np.reshape(arr, (size, size))

def infer_size(df):
    max_id = -1
    for col in ["evt_trail_dict","evt_memory_dict"]:
        if col in df.columns:
            for d in df[col].dropna():
                for k in d.keys():
                    try:
                        max_id = max(max_id, int(k))
                    except:
                        pass
    if max_id < 0:
        raise ValueError("No per-neuron dicts found.")
    size = int(np.ceil(np.sqrt(max_id+1)))
    return size

def save_heat(arr, path, title):
    plt.figure()
    plt.imshow(arr, origin="lower", interpolation="nearest")
    plt.colorbar()
    plt.title(title)
    plt.xlabel("col"); plt.ylabel("row")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("events", help="events.jsonl path")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    df = load_jsonl(args.events)
    outdir = args.outdir or os.path.dirname(os.path.abspath(args.events)) or "."
    size = infer_size(df)

    layers=[]
    if "evt_trail_dict" in df.columns:
        trail_mean = grid_from_series(df["evt_trail_dict"].dropna(), size=size, reducer="mean")
        trail_last = grid_from_series(df["evt_trail_dict"].dropna(), size=size, reducer="last")
        layers += [("trail_mean", trail_mean), ("trail_last", trail_last)]
    if "evt_memory_dict" in df.columns:
        mem_mean = grid_from_series(df["evt_memory_dict"].dropna(), size=size, reducer="mean")
        mem_last = grid_from_series(df["evt_memory_dict"].dropna(), size=size, reducer="last")
        layers += [("memory_mean", mem_mean), ("memory_last", mem_last)]

    for name, arr in layers:
        path = os.path.join(outdir, f"{os.path.basename(args.events).split('.')[0]}_{name}.png")
        save_heat(arr, path, title=name)

    # Save arrays for further use
    npz_path = os.path.join(outdir, f"{os.path.basename(args.events).split('.')[0]}_layers.npz")
    np.savez_compressed(npz_path, **{name:arr for name,arr in layers})
    print(f"Saved {len(layers)} heatmaps and arrays to {outdir}")

if __name__ == "__main__":
    main()
