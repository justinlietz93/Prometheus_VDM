#!/usr/bin/env python3
"""Optimize free symbolic parameters (tau0,tau1) to minimize RMS_after on deterministic samples.

Strategy:
- Rebuild symbolic solution (linsolve) for the small-N system as in flux_symbolic_full.py.
- Keep free symbols (tau0,tau1) as optimization variables.
- Lambdify H(Wi,Wj,alpha,beta,r,u,...free_params).
- For numeric evaluation apply protections: np.nan_to_num, then tanh scaling to bound H values.
- Minimize RMS_after across saved deterministic samples using scipy.optimize.minimize.
"""
from __future__ import annotations
import sys
from pathlib import Path
import json
import numpy as np
import glob
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from sympy import symbols, diff, log, simplify, expand, Matrix, linsolve
import sympy as sp
from scipy.optimize import minimize

SWEEP_DIR = ROOT / 'derivation' / 'outputs' / 'logs' / 'conservation_law'


def build_symbolic_solution():
    W1, W2, alpha, beta, r, u = symbols('W1 W2 alpha beta r u')
    t = 0
    delta1 = alpha * W1 * (1 - W1) - beta * W1
    Q1 = log(W1) - log(r - u * W1) - r * t
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

    # return solution tuple (may include free symbols like tau0,tau1)
    return sol, (W1, W2, alpha, beta, r, u)


def build_H_expression(sol, symbols_tuple):
    # sol is tuple c0..c4 expressions; may contain free symbols
    W1, W2, alpha, beta, r, u = symbols_tuple
    monomials = [(1,0),(0,1),(1,1),(2,0),(0,2)]
    ck = list(sol)
    H_expr = 0
    for (a,b), c in zip(monomials, ck):
        H_expr += c * (W1**a) * (W2**b)
    H_expr = simplify(H_expr)
    return H_expr


def load_latest_samples():
    files = sorted(glob.glob(str(SWEEP_DIR / 'flux_sweep_*.json')))
    if not files:
        raise SystemExit('no sweep files found; run flux_sweep.py first')
    latest = files[-1]
    with open(latest, 'r', encoding='utf-8') as f:
        data = json.load(f)
    samples = data.get('samples', [])
    return data, samples, latest


def make_H_fn(H_sym, symbols_tuple, free_syms):
    # Prepare lambdify with arguments order: W1,W2,alpha,beta,r,u, *free_syms
    args = (symbols_tuple[0], symbols_tuple[1], symbols_tuple[2], symbols_tuple[3], symbols_tuple[4], symbols_tuple[5]) + tuple(free_syms)
    H_fn = sp.lambdify(args, H_sym, 'numpy')
    return H_fn


def evaluate_rms_for_params(params, H_fn, free_syms, samples, data):
    # params: list of values for free_syms, len matches
    rnum = float(data.get('r', 0.15))
    unum = float(data.get('u', 0.25))
    N_samples = len(samples)
    rms_list = []

    # numeric protection settings
    nan_to_num_kwargs = {'nan': 0.0, 'posinf': 1e6, 'neginf': -1e6}
    scale = 1.0  # tanh scaling

    for s in samples:
        W0 = np.array(s['W0'], dtype=float)
        W1num = np.array(s['W1'], dtype=float)
        eps = 1e-12
        denom0 = (rnum - unum * W0)
        denom0 = np.where(np.abs(denom0) < eps, np.copysign(eps, denom0), denom0)
        W0_safe = np.where(np.abs(W0) < eps, np.copysign(eps, W0), W0)
        Q0 = np.log(np.abs(W0_safe)) - np.log(np.abs(denom0))
        denom1 = (rnum - unum * W1num)
        denom1 = np.where(np.abs(denom1) < eps, np.copysign(eps, denom1), denom1)
        W1_safe = np.where(np.abs(W1num) < eps, np.copysign(eps, W1num), W1num)
        Q1 = np.log(np.abs(W1_safe)) - np.log(np.abs(denom1))
        deltaQ = Q1 - Q0

        N = len(W0)
        Hmat = np.zeros((N, N), dtype=float)
        # evaluate H_ij for each pair
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                args = (W0[i], W0[j], 0.25, 0.1, rnum, unum) + tuple(params)
                try:
                    val = H_fn(*args)
                except Exception:
                    val = np.nan
                # coerce to float and protect
                val = np.array(val, dtype=float)
                val = np.nan_to_num(val, **nan_to_num_kwargs)
                # stabilizer borrowed from void equations idea: saturate via tanh
                val = np.tanh(val / scale) * scale
                Hmat[i, j] = float(val)

        corrected = np.zeros(N, dtype=float)
        for i in range(N):
            corrected[i] = deltaQ[i] - np.sum(Hmat[:, i] - Hmat[i, :])

        rms_list.append(np.sqrt(np.mean(corrected**2)))

    return float(np.mean(rms_list))


def main():
    sol, symbols_tuple = build_symbolic_solution()
    H_sym = build_H_expression(sol, symbols_tuple)

    # determine free symbols in solution (exclude the standard symbols)
    std_syms = set(symbols_tuple)
    free_syms = sorted(list(H_sym.free_symbols - std_syms), key=lambda s: s.name)
    print('free_syms:', free_syms)

    H_fn = make_H_fn(H_sym, symbols_tuple, free_syms)

    data, samples, latest = load_latest_samples()

    # initial params zeros
    x0 = np.zeros(len(free_syms), dtype=float)
    if len(x0) == 0:
        print('no free parameters to optimize; exiting')
        return

    def obj(x):
        return evaluate_rms_for_params(tuple(x), H_fn, free_syms, samples, data)

    res = minimize(obj, x0, method='Powell', options={'xtol':1e-6, 'ftol':1e-6, 'maxiter':200})

    best = res.x.tolist()
    best_rms = res.fun
    before_rms = evaluate_rms_for_params(tuple([0]*len(x0)), H_fn, free_syms, samples, data)

    out = {
        'timestamp': int(time.time()),
        'sweep_file': latest,
        'free_symbols': [str(s) for s in free_syms],
        'initial_params': [0.0]*len(x0),
        'best_params': best,
        'rms_before': before_rms,
        'rms_after': float(best_rms),
        'optimizer_result': {'success': bool(res.success), 'message': res.message}
    }

    report_path = Path(latest).parent / f'opt_H_params_{int(time.time())}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print('wrote', report_path)

if __name__ == '__main__':
    main()
