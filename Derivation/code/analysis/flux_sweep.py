#!/usr/bin/env python3
"""Numeric sweep: compute Δ(sum Q_i) statistics across random seeds.

Writes JSON summary to derivation/code/outputs/logs/conservation_law/flux_sweep_<ts>.json
"""
from __future__ import annotations
import os, json, time
from pathlib import Path
import numpy as np

# Ensure repo imports resolve
import sys
# add repository root to PYTHONPATH (parents[3] resolves to repo root)
sys.path.append(str(Path(__file__).resolve().parents[3]))

# Avoid importing the dense Connectome (do not set FORCE_DENSE).
# Instead sample W directly using numpy and evaluate void dynamics from
# the canonical Void_Equations module. This keeps the test non-invasive.
import importlib.util
from pathlib import Path as _P

# load Void_Equations module directly to avoid fum_rt package init side-effects
fve_path = _P(__file__).resolve().parents[3] / 'fum_rt' / 'fum_advanced_math' / 'void_dynamics' / 'Void_Equations.py'
spec = importlib.util.spec_from_file_location('Void_Equations', str(fve_path))
FVE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FVE)

# Q invariant as in qfum_validate mapping r = alpha - beta, u = alpha
def Q_invariant(r: float, u: float, W: np.ndarray, t: float) -> np.ndarray:
    eps = 1e-16
    W = np.asarray(W, dtype=np.float64)
    denom = (r - u * W)
    denom = np.where(np.abs(denom) < eps, np.copysign(eps, denom), denom)
    W_safe = np.where(np.abs(W) < eps, np.copysign(eps, W), W)
    return np.log(np.abs(W_safe)) - np.log(np.abs(denom)) - r * float(t)


def single_run(N, seed, r, u, deterministic=False):
    rng = np.random.RandomState(seed)
    # sample initial W in (0,1) matching runtime initialization style
    W0 = rng.rand(N).astype(np.float64)
    Q0 = Q_invariant(r, u, W0, 0.0)
    if deterministic:
        # deterministic skeleton: re = ALPHA * W * (1 - W); gdsp = -BETA * W
        ALPHA = getattr(FVE, 'ALPHA', 0.25)
        BETA = getattr(FVE, 'BETA', 0.1)
        effective_alpha = ALPHA * 1.0
        effective_beta = BETA * 1.0
        re = effective_alpha * W0 * (1.0 - W0)
        gd = - effective_beta * W0
        dW = re + gd
    else:
        # call canonical void dynamics implementation
        dW = FVE.universal_void_dynamics(W0, t=0.0, domain_modulation=1.0, sie_drive=1.0, use_time_dynamics=False)
    W1 = np.clip(W0 + dW, 0.0, 1.0)
    Q1 = Q_invariant(r, u, W1, 0.0)
    delta = Q1 - Q0
    return float(np.sum(delta)), float(np.max(np.abs(delta))), W0, W1


def main():
    N = 64
    k = 4
    trials = 40
    r = 0.25 - 0.10  # alpha-beta mapping used in repo
    u = 0.25
    seeds = list(range(1000, 1000 + trials))
    results = []
    deterministic = True
    save_samples = 6
    samples = []

    if deterministic:
        # Monkeypatch the universal_void_dynamics to remove noise and time-phase
        import importlib
        try:
            vda = importlib.import_module('fum_rt.core.void_dynamics_adapter')
        except Exception:
            vda = None

        def universal_deterministic(W, t, domain_modulation=1.0, sie_drive=None, use_time_dynamics=False):
            # deterministic skeleton: re = ALPHA * W * (1 - W); gdsp = -BETA * W
            try:
                from fum_rt.fum_advanced_math.void_dynamics import Void_Equations as FVE
                ALPHA = getattr(FVE, 'ALPHA', 0.25)
                BETA = getattr(FVE, 'BETA', 0.1)
            except Exception:
                ALPHA = 0.25
                BETA = 0.1
            effective_alpha = ALPHA * float(domain_modulation)
            effective_beta = BETA * float(domain_modulation)
            W = W.astype(float)
            re = effective_alpha * W * (1.0 - W)
            gd = - effective_beta * W
            return re + gd

        if vda is not None:
            vda.universal_void_dynamics = universal_deterministic
    for idx, s in enumerate(seeds):
        ds, dmax, W0, W1 = single_run(N, s, r, u, deterministic=deterministic)
        entry = {'seed': int(s), 'delta_sum_Q': ds, 'delta_max_abs': dmax}
        results.append(entry)
        # save a few sample W0/W1 for fitting
        if deterministic and idx < save_samples:
            samples.append({'seed': int(s), 'W0': W0.tolist(), 'W1': W1.tolist()})

    out = {
        'timestamp': int(time.time()),
        'N': N, 'k': k, 'trials': trials,
        'r': r, 'u': u,
    'results': results,
    'deterministic': bool(deterministic),
    'samples': samples,
    }

    out_dir = Path(__file__).resolve().parents[2] / 'outputs' / 'logs' / 'conservation_law'
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = out_dir / f"flux_sweep_{int(time.time())}.json"
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print('wrote', fname)

if __name__ == '__main__':
    main()
 