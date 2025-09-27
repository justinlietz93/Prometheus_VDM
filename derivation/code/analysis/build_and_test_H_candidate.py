#!/usr/bin/env python3
"""Construct H_candidate from symbolic solution (fix free params) and validate numerically.

This script recreates the small-N linear system from ``flux_symbolic_full.py``,
solves symbolically for coefficients c_k, substitutes free parameters to zero,
builds H_ij(Wi,Wj), and tests the correction on saved deterministic samples
from the latest `flux_sweep_*.json`.
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

def build_symbolic_coeffs():
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

    # build linear system: sum_k c_k * contribs[k] = dQ1
    # collect coefficients for a limited set of monomials
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

    # solve symbolically
    sol_set = linsolve((Mat, RHSv))
    if not sol_set:
        raise SystemExit('no symbolic solution')
    sol = list(sol_set)[0]

    # free symbols in solution will remain; substitute them to zero
    subs_zero = {s: 0 for s in sol.free_symbols}
    sol_fixed = [s.subs(subs_zero) for s in sol]

    # build expressions for ck in terms of W1,W2,alpha,beta,r,u
    return sol_fixed, (W1, W2, alpha, beta, r, u)

def H_expr_from_coeffs(ck, symbols_tuple):
    W1, W2, alpha, beta, r, u = symbols_tuple
    monomials = [(1,0),(0,1),(1,1),(2,0),(0,2)]
    expr = 0
    for (a,b), c in zip(monomials, ck):
        expr += c * (W1**a) * (W2**b)
    return simplify(expr)

def evaluate_on_samples(H_sym, symbols_tuple, samples_file):
    import sympy as sp
    W1_s, W2_s, alpha_s, beta_s, r_s, u_s = symbols_tuple
    subs_map = {alpha_s: 0.25, beta_s: 0.1, r_s: 0.15, u_s: 0.25}

    with open(samples_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    samples = data.get('samples', [])
    if not samples:
        raise SystemExit('no samples found')

    rms_before = []
    rms_after = []
    # for each saved sample, compute deltaQ vector and corrected residuals assuming full graph
    for s in samples:
        W0 = np.array(s['W0'], dtype=float)
        W1num = np.array(s['W1'], dtype=float)
        # compute deltaQ
        rnum = float(data.get('r', 0.15))
        unum = float(data.get('u', 0.25))
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
        # compile lambdified H function
        H_fn = sp.lambdify((symbols_tuple), H_sym, 'numpy')

        # precompute H_ij matrix
        Hmat = np.zeros((N, N), dtype=float)
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                # lambdify expects separate args: (W1,W2,alpha,beta,r,u)
                Hmat[i, j] = float(H_fn(W0[i], W0[j], 0.25, 0.1, rnum, unum))

        corrected = np.zeros(N, dtype=float)
        for i in range(N):
            corrected[i] = deltaQ[i] - np.sum(Hmat[:, i] - Hmat[i, :])

        rms_before.append(np.sqrt(np.mean(deltaQ**2)))
        rms_after.append(np.sqrt(np.mean(corrected**2)))

    return float(np.mean(rms_before)), float(np.mean(rms_after))

def main():
    sol_fixed, symbols_tuple = build_symbolic_coeffs()
    # sol_fixed are c0..c4 expressions in terms of symbols
    # build H(Wi,Wj) using these coefficients with variables W1->Wi, W2->Wj
    from sympy import symbols as S
    Wi, Wj = S('Wi Wj')

    # map c_k expressions to use Wi,Wj
    ck_sub = [c.subs({symbols_tuple[0]: Wi, symbols_tuple[1]: Wj}) for c in sol_fixed]
    H_sym = 0
    monomials = [(1,0),(0,1),(1,1),(2,0),(0,2)]
    for (a,b), c in zip(monomials, ck_sub):
        H_sym += c * (Wi**a) * (Wj**b)
    H_sym = simplify(H_sym)

    # find latest sweep json
    log_dir = ROOT / 'derivation' / 'outputs' / 'logs' / 'conservation_law'
    files = sorted(glob.glob(str(log_dir / 'flux_sweep_*.json')))
    latest = files[-1]
    print('testing H on', latest)
    before, after = evaluate_on_samples(H_sym, symbols_tuple, latest)
    out = {
        'timestamp': int(time.time()),
        'sweep_file': latest,
        'rms_before': before,
        'rms_after': after
    }
    report_path = Path(latest).parent / f'H_candidate_test_{int(time.time())}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print('wrote', report_path)

if __name__ == '__main__':
    main()
