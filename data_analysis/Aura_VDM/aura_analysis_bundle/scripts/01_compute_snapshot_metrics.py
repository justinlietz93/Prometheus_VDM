#!/usr/bin/env python3
"""Compute sparse snapshot metrics from state_*.h5 files.

Expects each H5 to contain:
  - sparse/W (N,)
  - sparse/row_ptr (N+1,)
  - sparse/col_idx (nnz,)
  - adc_json (json string)

Outputs:
  tables/snapshot_metrics.csv

Notes:
  - Computes out-degree from CSR row_ptr.
  - Gini + power-law alpha (continuous MLE approximation) on out-degree.
  - Saves top-20 hub indices and territory masses as JSON strings.
"""
import argparse, json, re
from pathlib import Path
import numpy as np
import pandas as pd
import h5py

def gini_coefficient(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    if x.size==0:
        return float('nan')
    if np.all(x==0):
        return 0.0
    x = x - x.min()
    x_sorted = np.sort(x)
    n = x_sorted.size
    cum = np.cumsum(x_sorted)
    return (n + 1 - 2 * cum.sum() / cum[-1]) / n

def powerlaw_alpha_mle(data: np.ndarray, kmin: int=5) -> float:
    data = np.asarray(data, dtype=float)
    tail = data[data >= kmin]
    n = tail.size
    if n < 2:
        return float('nan')
    return 1 + n / np.sum(np.log(tail / kmin))

def parse_adc_masses(adc_json_str: str):
    try:
        obj=json.loads(adc_json_str)
    except Exception:
        return []
    terr=obj.get('territories', [])
    masses={}
    for t in terr:
        key=t.get('key')
        if isinstance(key, list) and len(key)==2 and isinstance(key[1], int):
            masses[key[1]]=float(t.get('mass',0.0))
    if not masses:
        return []
    max_tid=max(masses.keys())
    return [masses.get(i,0.0) for i in range(max_tid+1)]

def tick_from_path(p: Path) -> int:
    m=re.search(r'state_(\d+)\.h5$', str(p))
    return int(m.group(1)) if m else -1

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--snap_dir', required=True, help='Directory containing state_*.h5')
    ap.add_argument('--out_csv', required=True)
    ap.add_argument('--topk', type=int, default=20)
    ap.add_argument('--kmin', type=int, default=5)
    args=ap.parse_args()

    snap_dir=Path(args.snap_dir)
    paths=sorted(snap_dir.glob('state_*.h5'), key=lambda p: tick_from_path(p))

    rows=[]
    for p in paths:
        tick=tick_from_path(p)
        with h5py.File(p,'r') as hf:
            W=hf['sparse/W'][:]
            row_ptr=hf['sparse/row_ptr'][:]
            col_idx=hf['sparse/col_idx'][:]
            nnz=int(col_idx.shape[0])
            N=int(W.shape[0])
            out_deg=np.diff(row_ptr).astype(int)
            mean_deg=float(out_deg.mean())
            max_deg=int(out_deg.max())
            gini=float(gini_coefficient(out_deg))
            alpha=float(powerlaw_alpha_mle(out_deg, kmin=args.kmin))
            top_idx=np.argpartition(out_deg, -args.topk)[-args.topk:]
            top_idx=top_idx[np.argsort(out_deg[top_idx])[::-1]]
            corr=float(np.corrcoef(out_deg, W)[0,1]) if np.std(out_deg)>0 and np.std(W)>0 else float('nan')
            adc_raw=hf['adc_json'][()]
            adc_str=adc_raw.decode('utf-8','ignore') if isinstance(adc_raw,(bytes,bytearray)) else str(adc_raw)
            masses=parse_adc_masses(adc_str)

        rows.append({
            'tick': tick,
            'N': N,
            'nnz': nnz,
            'mean_out_degree': mean_deg,
            'max_out_degree': max_deg,
            'gini_out_degree': gini,
            'alpha_out_degree_kmin5': alpha,
            'w_mean': float(np.mean(W)),
            'w_var': float(np.var(W)),
            'corr_outdeg_W': corr,
            'top_hubs_json': json.dumps(top_idx.tolist()),
            'territory_masses_json': json.dumps(masses),
        })

    df=pd.DataFrame(rows)
    out_path=Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f'Wrote {out_path} ({out_path.stat().st_size/1e6:.2f} MB)')

if __name__=='__main__':
    main()