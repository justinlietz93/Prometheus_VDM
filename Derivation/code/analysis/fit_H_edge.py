#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Fit edge-correction ansatz H_edge using saved deterministic samples.

Reads the latest flux_sweep JSON under Derivation/outputs/logs/conservation_law,
reconstructs Connectome adjacency per sample seed, and fits coefficients for
H_ij = sum_k c_k * phi_k(W_i, W_j) using least squares on equations
    DeltaQ_i = sum_j (H_ji - H_ij)

Basis functions: [W_i, W_j, W_i*W_j]
"""
from __future__ import annotations
import json, time, sys
from pathlib import Path
import numpy as np

# repo root
ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import glob
from operator import itemgetter

# find latest flux_sweep json
log_dir = ROOT / 'derivation' / 'outputs' / 'logs' / 'conservation_law'
files = sorted(glob.glob(str(log_dir / 'flux_sweep_*.json')))
if not files:
    raise SystemExit('no flux_sweep json found; run flux_sweep.py first')
latest = files[-1]
print('using', latest)
with open(latest, 'r', encoding='utf-8') as f:
    data = json.load(f)

samples = data.get('samples', [])
if not samples:
    raise SystemExit('no samples saved in sweep json; enable deterministic mode with samples')

r = float(data.get('r', 0.15))
u = float(data.get('u', 0.25))

# basis functions
def phi_basis(Wi, Wj):
    return np.array([Wi, Wj, Wi * Wj], dtype=float)

K = 3  # number of basis funcs
A_rows = []
b_vec = []

for s in samples:
    seed = int(s['seed'])
    W0 = np.array(s['W0'], dtype=float)
    W1 = np.array(s['W1'], dtype=float)
    # delta Q
    eps = 1e-12
    denom0 = (r - u * W0)
    denom0 = np.where(np.abs(denom0) < eps, np.copysign(eps, denom0), denom0)
    W0_safe = np.where(np.abs(W0) < eps, np.copysign(eps, W0), W0)
    Q0 = np.log(np.abs(W0_safe)) - np.log(np.abs(denom0)) - r * 0.0
    denom1 = (r - u * W1)
    denom1 = np.where(np.abs(denom1) < eps, np.copysign(eps, denom1), denom1)
    W1_safe = np.where(np.abs(W1) < eps, np.copysign(eps, W1), W1)
    Q1 = np.log(np.abs(W1_safe)) - np.log(np.abs(denom1)) - r * 0.0
    deltaQ = Q1 - Q0

    # assume full connectivity between distinct nodes for fitting (avoid importing Connectome)
    N = len(W0)
    # For each node i, equation: deltaQ[i] = sum_j (H_ji - H_ij)
    # Parameterize H_ij = sum_k c_k * phi_k(W_i, W_j)
    # So deltaQ[i] = sum_k c_k * sum_j (phi_k(W_j,W_i) - phi_k(W_i,W_j))
    for i in range(N):
        row = np.zeros(K, dtype=float)
        for j in range(N):
            if i == j:
                continue
            # include all pairs (i != j) to avoid dependency on Connectome
            exists = True
            ph_ji = phi_basis(W0[j], W0[i])
            ph_ij = phi_basis(W0[i], W0[j])
            row += (ph_ji - ph_ij)
        A_rows.append(row)
        b_vec.append(deltaQ[i])

A_mat = np.vstack(A_rows)
b = np.array(b_vec, dtype=float)

# solve least squares
coef, *_ = np.linalg.lstsq(A_mat, b, rcond=None)
residuals = b - A_mat.dot(coef)
rms = np.sqrt(np.mean(residuals**2))
print('fitted coefficients:', coef.tolist())
print('rms residual:', float(rms))

# write fit report
out = {
    'timestamp': int(time.time()),
    'sweep_file': str(latest),
    'basis': ['Wi', 'Wj', 'Wi*Wj'],
    'coefficients': coef.tolist(),
    'rms_residual': float(rms)
}
report_path = log_dir / f'fit_H_edge_{int(time.time())}.json'
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)
print('wrote', report_path)
