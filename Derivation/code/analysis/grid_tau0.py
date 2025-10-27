#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Quick grid scan over tau0 to evaluate RMS_after for the symbolic H candidate.
Prints best tau0 and a small table.
"""
from pathlib import Path
import sys, json, glob
ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import numpy as np
import sympy as sp
from sympy import symbols, diff, log, simplify, expand, Matrix, linsolve

SWEEP_DIR = ROOT / 'derivation' / 'outputs' / 'logs' / 'conservation_law'
files = sorted(glob.glob(str(SWEEP_DIR / 'flux_sweep_*.json')))
if not files:
    raise SystemExit('no sweep files')
latest = files[-1]
with open(latest,'r') as f:
    data = json.load(f)
samples = data.get('samples', [])

# build symbolic solution (same as optimize script)
W1, W2, alpha, beta, r, u = symbols('W1 W2 alpha beta r u')
delta1 = alpha * W1 * (1 - W1) - beta * W1
Q1 = log(W1) - log(r - u * W1)
dQ1 = simplify(diff(Q1, W1) * delta1)
monomials = [(1,0),(0,1),(1,1),(2,0),(0,2)]
coeffs = symbols('c0:5')
contribs = []
for (a,b) in monomials:
    term = (W2**a * W1**b) - (W1**a * W2**b)
    contribs.append(term)
terms = []
for a in range(0,4):
    for b in range(0,4 - a):
        terms.append(W1**a * W2**b)
M = []
RHS = []
for term in terms:
    row = [simplify(expand(contribs[k].coeff(term))) for k in range(len(coeffs))]
    M.append(row)
    RHS.append(simplify(expand(dQ1.coeff(term))))
Mat = Matrix(M)
RHSv = Matrix(RHS)
sol_set = linsolve((Mat, RHSv))
if not sol_set:
    raise SystemExit('no symbolic solution')
sol = list(sol_set)[0]

# build H_sym using sol (free symbols may include tau0)
monomials = [(1,0),(0,1),(1,1),(2,0),(0,2)]
ck = list(sol)
H_sym = 0
for (a,b), c in zip(monomials, ck):
    H_sym += c * (W1**a) * (W2**b)
H_sym = simplify(H_sym)

# identify free symbols
std_syms = set((W1,W2,alpha,beta,r,u))
free_syms = sorted(list(H_sym.free_symbols - std_syms), key=lambda s: s.name)
print('free_syms=', free_syms)
if len(free_syms) == 0:
    print('no free params; nothing to scan')
    sys.exit(0)

# lambdify H function with args W1,W2,alpha,beta,r,u,tau0
args = (W1,W2,alpha,beta,r,u) + tuple(free_syms)
H_fn = sp.lambdify(args, H_sym, 'numpy')

# evaluation helper (same protections)
def eval_RMS_for_tau0(tau0):
    rnum = float(data.get('r',0.15))
    unum = float(data.get('u',0.25))
    rms_list = []
    for s in samples:
        W0 = np.array(s['W0'],dtype=float)
        W1num = np.array(s['W1'],dtype=float)
        denom0 = (rnum - unum * W0)
        denom0 = np.where(np.abs(denom0) < 1e-12, np.copysign(1e-12, denom0), denom0)
        W0_safe = np.where(np.abs(W0) < 1e-12, np.copysign(1e-12, W0), W0)
        Q0 = np.log(np.abs(W0_safe)) - np.log(np.abs(denom0))
        denom1 = (rnum - unum * W1num)
        denom1 = np.where(np.abs(denom1) < 1e-12, np.copysign(1e-12, denom1), denom1)
        W1_safe = np.where(np.abs(W1num) < 1e-12, np.copysign(1e-12, W1num), W1num)
        Q1 = np.log(np.abs(W1_safe)) - np.log(np.abs(denom1))
        deltaQ = Q1 - Q0
        N = len(W0)
        Hmat = np.zeros((N,N),dtype=float)
        for i in range(N):
            for j in range(N):
                if i==j: continue
                try:
                    val = H_fn(W0[i], W0[j], 0.25, 0.1, rnum, unum, tau0)
                except Exception:
                    val = np.nan
                val = np.nan_to_num(val, nan=0.0, posinf=1e6, neginf=-1e6)
                val = np.tanh(val)
                Hmat[i,j]=float(val)
        corrected = np.zeros(N,dtype=float)
        for i in range(N):
            corrected[i] = deltaQ[i] - np.sum(Hmat[:,i] - Hmat[i,:])
        rms_list.append(np.sqrt(np.mean(corrected**2)))
    return float(np.mean(rms_list))

# grid
grid = np.linspace(-2.0,2.0,81)
vals = []
for g in grid:
    vals.append(eval_RMS_for_tau0(g))
vals = np.array(vals)
bi = np.argmin(vals)
print('best tau0 grid=',grid[bi],'rms=',vals[bi])
# print small table around best
for i in range(max(0,bi-3), min(len(grid),bi+4)):
    print(f'{grid[i]:6.3f} -> {vals[i]:.6f}')

# write report
out = {'grid':grid.tolist(),'vals':vals.tolist(),'best_tau0':float(grid[bi]),'best_rms':float(vals[bi])}
with open(SWEEP_DIR / 'grid_tau0_report.json','w') as f:
    json.dump(out,f,indent=2)
print('wrote', SWEEP_DIR / 'grid_tau0_report.json')
