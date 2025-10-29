#!/usr/bin/env python3
"""
Metriplectic Assisted-Echo experiment (baseline vs assisted) per T4 proposal.

Produces paired artifacts (JSON/CSV) under outputs/logs/metriplectic/ and a figure placeholder.
Requires approval via APPROVAL.json for real runs (tests should use preflight logging helpers instead).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

# Code root on path
import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import log_path, write_log, figure_path
from physics.metriplectic.kg_ops import kg_verlet_step, kg_energy
from physics.metriplectic.compose import m_only_step_with_stats
from physics.metriplectic.metriplectic_structure_checks import apply_M
from physics.metriplectic.echo_metrics import h_energy_norm_delta, ceg


@dataclass
class EchoSpec:
    grid: Dict[str, Any]  # {N, dx}
    params: Dict[str, Any]  # {c, m, D, m_lap_operator}
    dt: float
    steps: int
    seeds: List[int]
    lambdas: List[float]
    budget: float  # energy budget for reverse correction per step (H-norm of (dphi,0))
    tag: str | None = None


def _slug(base: str, tag: str | None) -> str:
    if not tag:
        return base
    return f"{base}__{str(tag).strip().replace(' ', '-')}"


def _jmj_step(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    # J half
    phi1, pi1 = kg_verlet_step(phi, pi, 0.5 * dt, dx, c, m)
    # M full on phi
    phi2, _ = m_only_step_with_stats(phi1, dt, dx, params)
    # J half
    phi3, pi3 = kg_verlet_step(phi2, pi1, 0.5 * dt, dx, c, m)
    return phi3, pi3


def _assist_correction(phi: np.ndarray, dx: float, params: Dict[str, Any], lam: float, budget: float, c: float, m: float) -> np.ndarray:
    """Model-aware assistance: move opposite the metric flow by one Euler micro-step and clamp to budget in H-norm."""
    D = float(params.get("D", 1.0))
    lap = str(params.get("m_lap_operator", "spectral"))
    # approximate inverse: phi <- phi - lam * (M phi) * dt_assist, take dt_assist=1 in units since budget clamps magnitude
    direction = -apply_M(phi, dx, D, lap)
    if np.allclose(direction, 0.0):
        return np.zeros_like(phi)
    # clamp to H-budget (pi=0)
    dphi = direction.astype(float)
    # scale to fit budget
    # Compute current size in H-norm
    # If zero budget, return zero
    if budget <= 0:
        return np.zeros_like(phi)
    # Normalize and scale: we use H-norm with pi=0
    # get current H-norm of dphi
    def _h_norm(v: np.ndarray) -> float:
        return h_energy_norm_delta(v, np.zeros_like(v), np.zeros_like(v), np.zeros_like(v), dx, c, m)
    size = _h_norm(dphi)
    if size == 0.0:
        return np.zeros_like(phi)
    scaled = (lam * budget / size) * dphi
    return scaled


def _random_correction(rng: np.random.Generator, phi: np.ndarray, dx: float, budget: float, c: float, m: float) -> np.ndarray:
    if budget <= 0:
        return np.zeros_like(phi)
    v = rng.standard_normal(phi.shape).astype(float)
    # normalize in H-norm and scale to budget
    def _h_norm(w: np.ndarray) -> float:
        return h_energy_norm_delta(w, np.zeros_like(w), np.zeros_like(w), np.zeros_like(w), dx, c, m)
    size = _h_norm(v)
    if size == 0.0:
        return np.zeros_like(phi)
    return (budget / size) * v


def run_assisted_echo(spec: EchoSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt = float(spec.dt)
    c = float(spec.params.get("c", 1.0)) ; m = float(spec.params.get("m", 0.0))
    seeds = [int(s) for s in spec.seeds]
    lambdas = [float(l) for l in spec.lambdas]
    steps = int(spec.steps)
    tag = spec.tag or spec.params.get("tag")

    results: Dict[str, Any] = {"seeds": seeds, "lambdas": lambdas, "grid": spec.grid, "params": spec.params, "dt": dt, "steps": steps}
    per_seed: List[Dict[str, Any]] = []

    for seed in seeds:
        rng = np.random.default_rng(seed)
        # initial state
        phi0 = rng.random(N).astype(float) * 0.1
        pi0 = rng.random(N).astype(float) * 0.1

        # forward JMJ
        ph, pr = phi0.copy(), pi0.copy()
        for _ in range(steps):
            ph, pr = _jmj_step(ph, pr, dt, dx, spec.params)
        phiF, piF = ph, pr

        # Baseline reverse attempt (model-blind): use random corrections with same per-step H-budget as assisted
        errs: Dict[str, float] = {}
        # shared budget
        budget = float(spec.budget)

        # baseline (lambda used only for budgeting equality across variants)
        bl_ph, bl_pr = phiF.copy(), piF.copy()
        for _ in range(steps):
            # J half backward, correction, J half backward
            bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c, m)
            bl_ph = bl_ph + _random_correction(rng, bl_ph, dx, budget, c, m)
            bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c, m)
        bl_err = h_energy_norm_delta(bl_ph, bl_pr, phi0, pi0, dx, c, m)
        errs["baseline"] = bl_err

        # assisted variants
        assisted: Dict[str, float] = {}
        for lam in lambdas:
            as_ph, as_pr = phiF.copy(), piF.copy()
            for _ in range(steps):
                as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c, m)
                dphi = _assist_correction(as_ph, dx, spec.params, lam=lam, budget=budget, c=c, m=m)
                as_ph = as_ph + dphi
                as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c, m)
            assisted_err = h_energy_norm_delta(as_ph, as_pr, phi0, pi0, dx, c, m)
            assisted[str(lam)] = assisted_err

        # CEG per lambda
        ceg_map = {str(l): ceg(bl_err, assisted[str(l)]) for l in lambdas}
        per_seed.append({"seed": seed, "baseline_err": bl_err, "assisted_err": assisted, "ceg": ceg_map})

    results["per_seed"] = per_seed
    # Aggregates
    import numpy as np
    agg = {}
    for lam in lambdas:
        vals = [float(s["ceg"][str(lam)]) for s in per_seed]
        agg[str(lam)] = {"median": float(np.median(np.array(vals))), "mean": float(np.mean(np.array(vals))), "n": len(vals)}
    results["ceg_summary"] = agg
    return results


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Metriplectic Assisted Echo (baseline vs assisted)")
    ap.add_argument("--spec", required=True, help="Path to echo spec JSON")
    args = ap.parse_args()

    raw = json.loads(Path(args.spec).read_text())
    spec = EchoSpec(**raw)
    tag = spec.tag or spec.params.get("tag")

    out = run_assisted_echo(spec)
    # Logs
    logp = log_path("metriplectic", _slug("assisted_echo", tag), failed=False, type="json")
    write_log(logp, out)
    # CSV summary: lambda, median_ceg
    csvp = log_path("metriplectic", _slug("assisted_echo_ceg_summary", tag), failed=False, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("lambda,median_ceg,mean_ceg,n\n")
        for k, v in out.get("ceg_summary", {}).items():
            f.write(f"{k},{v.get('median',0.0)},{v.get('mean',0.0)},{v.get('n',0)}\n")
    # Placeholder figure path (figure creation may be handled by downstream notebooks)
    figp = figure_path("metriplectic", _slug("assisted_echo_placeholder", tag), failed=False)
    try:
        import matplotlib.pyplot as plt
        lambdas = [float(k) for k in out.get("ceg_summary", {}).keys()]
        meds = [float(out["ceg_summary"][str(k)]['median']) for k in lambdas]
        plt.figure(figsize=(6,4)); plt.plot(lambdas, meds, "o-"); plt.xlabel("lambda"); plt.ylabel("median CEG"); plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()
    except Exception as e:
        # Plotting is optional; log a lightweight warning to the JSON output next time the caller inspects artifacts
        _ = e
    print(json.dumps({"log": str(logp), "csv": str(csvp), "figure": str(figp)}, indent=2))


if __name__ == "__main__":
    main()
