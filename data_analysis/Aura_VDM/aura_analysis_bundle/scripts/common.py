from __future__ import annotations
import json, os, re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
import h5py
import numpy as np
import pandas as pd


def ensure_dir(p: str | Path) -> Path:
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_events_jsonl(path: str | Path) -> pd.DataFrame:
    rows = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    df = pd.DataFrame(rows)
    if 't' not in df.columns and 'evt_t' in df.columns:
        df['t'] = df['evt_t']
    return df


def load_utd_events(paths: Iterable[str | Path]) -> pd.DataFrame:
    rows = []
    for path in paths:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                rec['_source_file'] = str(Path(path).name)
                rows.append(rec)
    return pd.DataFrame(rows)


def flatten_macro_events(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        row = {
            'file': r.get('_source_file'),
            'type': r.get('type'),
            'macro': r.get('macro'),
            'score': r.get('score')
        }
        args = r.get('args') if isinstance(r.get('args'), dict) else {}
        row.update(args)
        why = args.get('why') if isinstance(args.get('why'), dict) else {}
        for k, v in why.items():
            row[f'why_{k}'] = v
        rows.append(row)
    return pd.DataFrame(rows)


def parse_dashboard_targets(html_path: str | Path, available_fields: Iterable[str]) -> List[str]:
    html = Path(html_path).read_text(encoding='utf-8', errors='ignore')
    available = set(map(str, available_fields))
    desired = [
        'connectome_entropy',
        'vt_entropy',
        'sie_v2_valence_01',
        'vt_coverage',
        'active_edges',
        'b1_z',
        'homeostasis_pruned',
        'homeostasis_bridged',
        'omega_mean',
        'a_mean',
        'active_synapses',
        'cohesion_components',
        'complexity_cycles',
        'ute_in_count',
        'ute_text_count',
    ]
    return [m for m in desired if m in available and m in html]


def standardize(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors='coerce')
    mu = s.mean()
    sd = s.std(ddof=0)
    if not np.isfinite(sd) or sd == 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - mu) / sd


def two_state_kmeans(X: np.ndarray, n_iter: int = 50) -> np.ndarray:
    # deterministic 2-means with quantile init
    x = np.asarray(X, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    c0 = np.nanpercentile(x, 25, axis=0)
    c1 = np.nanpercentile(x, 75, axis=0)
    labels = np.zeros(len(x), dtype=int)
    for _ in range(n_iter):
        d0 = np.nansum((x - c0) ** 2, axis=1)
        d1 = np.nansum((x - c1) ** 2, axis=1)
        new = (d1 < d0).astype(int)
        if np.array_equal(new, labels):
            break
        labels = new
        if np.any(labels == 0):
            c0 = np.nanmean(x[labels == 0], axis=0)
        if np.any(labels == 1):
            c1 = np.nanmean(x[labels == 1], axis=0)
    return labels


def parse_h5_snapshot(path: str | Path) -> Tuple[Dict, Dict]:
    path = Path(path)
    with h5py.File(path, 'r') as f:
        W = f['sparse/W'][:]
        col = f['sparse/col_idx'][:]
        row_ptr = f['sparse/row_ptr'][:]
        adc = json.loads(f['adc_json'][()].decode('utf-8'))
    n = len(W)
    nnz = len(col)
    degrees = np.diff(row_ptr)
    territories = adc.get('territories', [])
    terr_rows = []
    for terr in territories:
        terr_rows.append({'territory': terr.get('id'), 'mass': terr.get('mass', np.nan)})
    summary = {
        'file': path.name,
        'tick': int(re.search(r'(\d+)', path.stem).group(1)) if re.search(r'(\d+)', path.stem) else np.nan,
        'bytes': path.stat().st_size,
        'n_nodes': int(n),
        'nnz_edges': int(nnz),
        'mean_degree': float(np.mean(degrees)),
        'median_degree': float(np.median(degrees)),
        'max_degree': int(np.max(degrees)),
        'mean_weight': float(np.mean(W)),
        'std_weight': float(np.std(W)),
        'territories': len(territories),
    }
    return summary, {'W': W, 'col': col, 'row_ptr': row_ptr, 'territories': terr_rows}
