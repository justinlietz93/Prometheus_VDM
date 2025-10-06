
#!/usr/bin/env python3
import json, argparse, os, sys, math, re
from collections import defaultdict
import numpy as np
import pandas as pd

def load_jsonl(path):
    rows=[]
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try:
                rows.append(json.loads(line))
            except Exception:
                # minor cleanup for trailing commas
                line=re.sub(r",\s*}", "}", re.sub(r",\s*]", "]", line))
                rows.append(json.loads(line))
    return pd.DataFrame(rows)

def lag_corr(x, y, max_lag=12):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    out=[]
    for lag in range(-max_lag, max_lag+1):
        if lag<0:
            a = x[-lag:]; b = y[:len(y)+lag]
        elif lag>0:
            a = x[:-lag]; b = y[lag:]
        else:
            a = x; b = y
        m = np.isfinite(a) & np.isfinite(b)
        if m.sum()>3 and np.std(a[m])>0 and np.std(b[m])>0:
            out.append({"lag":lag, "corr": float(np.corrcoef(a[m],b[m])[0,1])})
        else:
            out.append({"lag":lag, "corr": None})
    return out

def bursts(mask):
    bursts=[]
    start=None; length=0
    for i, val in enumerate(mask):
        if val:
            if start is None:
                start=i; length=1
            else:
                length+=1
        else:
            if start is not None:
                bursts.append((start, i-1, length))
                start=None; length=0
    if start is not None:
        bursts.append((start, len(mask)-1, length))
    return bursts

def analyze(path, outdir=None, topk=30, max_lag=12):
    df = load_jsonl(path)
    if outdir is None:
        outdir = os.path.dirname(os.path.abspath(path)) or "."
    base = os.path.splitext(os.path.basename(path))[0]

    # Basic ranges
    metrics = ["connectome_entropy","vt_entropy","vt_coverage","avg_weight","ute_text_count"]
    ranges = {}
    for m in metrics:
        if m in df.columns:
            ranges[m] = {"min": float(np.nanmin(df[m])), "max": float(np.nanmax(df[m])), "mean": float(np.nanmean(df[m]))}

    # Correlations with speaking
    corrs={}
    if "ute_text_count" in df.columns:
        for m in ["connectome_entropy","vt_entropy","vt_coverage","avg_weight"]:
            if m in df.columns:
                s = df[["ute_text_count", m]].dropna()
                if len(s)>2 and s["ute_text_count"].std()!=0 and s[m].std()!=0:
                    corrs[m] = float(s["ute_text_count"].corr(s[m]))
                else:
                    corrs[m] = None

    # Bursts
    speak_mask = (df.get("ute_text_count", pd.Series([0]*len(df))).fillna(0)>0).astype(int).values
    burst_list = bursts(speak_mask)
    burst_lengths = [b[2] for b in burst_list]
    burst_stats = {
        "n_bursts": len(burst_list),
        "median_len": float(np.median(burst_lengths)) if burst_lengths else 0.0,
        "max_len": int(max(burst_lengths)) if burst_lengths else 0
    }

    # Lag correlations
    lagc = []
    if "connectome_entropy" in df.columns and "ute_text_count" in df.columns:
        lagc = lag_corr(df["connectome_entropy"].values, df["ute_text_count"].values, max_lag=max_lag)

    # Per-neuron analysis
    n_trail = n_mem = 0
    top_trail = []; top_mem = []
    mean_abs_corr = None
    top_keys = []

    if "evt_trail_dict" in df.columns:
        # Build union and per-tick sums
        trail_series = df["evt_trail_dict"]
        mem_series = df.get("evt_memory_dict", pd.Series([None]*len(df)))

        # Union
        all_trail_ids=set()
        all_mem_ids=set()
        for d in trail_series.dropna():
            all_trail_ids.update(d.keys())
        for d in mem_series.dropna():
            all_mem_ids.update(d.keys())
        n_trail=len(all_trail_ids); n_mem=len(all_mem_ids)

        # Positive deltas
        pos_delta_trail=defaultdict(float); pos_delta_mem=defaultdict(float)
        prev_trail=None; prev_mem=None
        sum_trail=[]; sum_mem=[]; pos_sum_trail=[]; pos_sum_mem=[]
        for d_tr, d_mem in zip(trail_series, mem_series):
            if isinstance(d_tr, dict):
                sum_trail.append(float(sum(d_tr.values())))
            else:
                sum_trail.append(np.nan)
            if isinstance(d_mem, dict):
                sum_mem.append(float(sum(d_mem.values())))
            else:
                sum_mem.append(np.nan)

            if isinstance(d_tr, dict) and isinstance(prev_trail, dict):
                s=0.0
                keys=set(prev_trail.keys()) | set(d_tr.keys())
                for k in keys:
                    dv = d_tr.get(k,0.0) - prev_trail.get(k,0.0)
                    if dv>0:
                        pos_delta_trail[k]+=dv; s+=dv
                pos_sum_trail.append(s)
            else:
                pos_sum_trail.append(np.nan)

            if isinstance(d_mem, dict) and isinstance(prev_mem, dict):
                s=0.0
                keys=set(prev_mem.keys()) | set(d_mem.keys())
                for k in keys:
                    dv = d_mem.get(k,0.0) - prev_mem.get(k,0.0)
                    if dv>0:
                        pos_delta_mem[k]+=dv; s+=dv
                pos_sum_mem.append(s)
            else:
                pos_sum_mem.append(np.nan)

            prev_trail = d_tr if isinstance(d_tr, dict) else prev_trail
            prev_mem   = d_mem if isinstance(d_mem, dict) else prev_mem

        # Top neurons by positive delta
        def top_items(d, k=15):
            return sorted(d.items(), key=lambda x: x[1], reverse=True)[:k]
        top_trail = top_items(pos_delta_trail, topk)
        top_mem   = top_items(pos_delta_mem, topk)

        # Correlations with speaking
        df2 = df.copy()
        df2["sum_trail"]=sum_trail; df2["sum_mem"]=sum_mem
        df2["pos_sum_trail"]=pos_sum_trail; df2["pos_sum_mem"]=pos_sum_mem
        corr_pos_trail = df2[["pos_sum_trail","ute_text_count"]].dropna().corr().iloc[0,1] if "ute_text_count" in df.columns else None
        corr_pos_mem   = df2[["pos_sum_mem","ute_text_count"]].dropna().corr().iloc[0,1] if "ute_text_count" in df.columns else None
        corr_sum_trail = df2[["sum_trail","ute_text_count"]].dropna().corr().iloc[0,1] if "ute_text_count" in df.columns else None
        corr_sum_mem   = df2[["sum_mem","ute_text_count"]].dropna().corr().iloc[0,1] if "ute_text_count" in df.columns else None

        # Coactivation among top-variance neurons (trail)
        T = len(df)
        trail_keys = list(all_trail_ids)
        if len(trail_keys)*T <= 12_000_000:  # guard memory
            k2idx = {k:i for i,k in enumerate(trail_keys)}
            mat = np.zeros((T, len(trail_keys)), dtype=np.float32)
            for t_idx, d in enumerate(trail_series):
                if isinstance(d, dict):
                    for k, val in d.items():
                        j = k2idx.get(k)
                        if j is not None:
                            mat[t_idx, j]=float(val)
            var = mat.var(axis=0)
            k_take = min(topk, len(trail_keys))
            top_idx = np.argsort(var)[-k_take:]
            top_keys = [trail_keys[i] for i in top_idx]
            sub = mat[:, top_idx]
            std = sub.std(axis=0)
            std[std==0]=1.0
            cor = np.corrcoef((sub - sub.mean(axis=0))/std, rowvar=False)
            off = np.abs(cor[np.triu_indices_from(cor, k=1)])
            mean_abs_corr = float(off.mean()) if off.size>0 else None

        # Save neuron tables
        pd.DataFrame(top_trail, columns=["neuron_id","pos_delta_trail"]).to_csv(os.path.join(outdir, f"{base}_top_trail.csv"), index=False)
        pd.DataFrame(top_mem, columns=["neuron_id","pos_delta_memory"]).to_csv(os.path.join(outdir, f"{base}_top_memory.csv"), index=False)

        # Save time series aggregates
        cols = [c for c in ["t","ts","sum_trail","sum_mem","pos_sum_trail","pos_sum_mem","ute_text_count"] if c in df2.columns]
        pd.DataFrame(df2[cols]).to_csv(os.path.join(outdir, f"{base}_series.csv"), index=False)

        per_neuron_summary = {
            "n_trail_neurons": int(n_trail),
            "n_memory_neurons": int(n_mem),
            "corr_pos_sum_trail_vs_speaking": float(corr_pos_trail) if corr_pos_trail is not None else None,
            "corr_pos_sum_memory_vs_speaking": float(corr_pos_mem) if corr_pos_mem is not None else None,
            "corr_sum_trail_vs_speaking": float(corr_sum_trail) if corr_sum_trail is not None else None,
            "corr_sum_memory_vs_speaking": float(corr_sum_mem) if corr_sum_mem is not None else None,
            "mean_abs_corr_topvar_trail": mean_abs_corr,
            "topvar_trail_keys": top_keys
        }
    else:
        per_neuron_summary = {"n_trail_neurons": 0, "n_memory_neurons": 0}

    report = {
        "path": path,
        "n_rows": int(len(df)),
        "t_min": int(df["t"].min()) if "t" in df.columns else None,
        "t_max": int(df["t"].max()) if "t" in df.columns else None,
        "ranges": ranges,
        "correlations_with_speaking": corrs,
        "burst_stats": burst_stats,
        "lag_corr_connectome_entropy_vs_speaking": lagc,
        "per_neuron": per_neuron_summary
    }
    out_json = os.path.join(outdir, f"{base}_report.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"[ok] wrote {out_json}")
    print(f"[ok] wrote {base}_top_trail.csv, {base}_top_memory.csv, {base}_series.csv in {outdir}")
    return report

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="events.jsonl file(s)")
    ap.add_argument("--outdir", default=None, help="output directory")
    ap.add_argument("--topk", type=int, default=30)
    ap.add_argument("--lag", type=int, default=12)
    args = ap.parse_args()
    for p in args.paths:
        analyze(p, outdir=args.outdir, topk=args.topk, max_lag=args.lag)
