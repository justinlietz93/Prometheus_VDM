#!/usr/bin/env python3
"""
RD Conservation Harness (Obj-A/B/C scaffolding) — periodic BC default.

- Uses derivation/code/common/io_paths.py for logs/figures.
- Places artifacts under code/outputs/{logs,figures}/rd_conservation.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np
import matplotlib.pyplot as plt

"""Adjust sys.path so 'common' imports resolve when run as a script."""
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from physics.reaction_diffusion.reaction_exact import logistic_invariant_Q


@dataclass
class StepSpec:
    bc: str
    scheme: str
    order_p: int
    expected_dt_slope: float
    grid: Dict[str, Any]
    params: Dict[str, Any]
    dt_sweep: List[float]
    seeds: int | List[int]
    safety: Dict[str, bool]
    cfl_used: bool
    adjacency: Dict[str, Any] | None = None
    notes: str | None = None


def laplacian_periodic_1d(u: np.ndarray, dx: float) -> np.ndarray:
    return (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (dx * dx)


def mass(u: np.ndarray, dx: float) -> float:
    return float(np.sum(u) * dx)


def diffusion_only_mass_check(N: int, dx: float, D: float, dt: float, steps: int, seed: int) -> Dict[str, Any]:
    rng = np.random.default_rng(seed)
    u = rng.random(N).astype(float) * 0.1
    m0 = mass(u, dx)
    for _ in range(steps):
        lap = laplacian_periodic_1d(u, dx)
        u = u + dt * (D * lap)
    m1 = mass(u, dx)
    return {
        "N": N,
        "dx": dx,
        "D": D,
        "dt": dt,
        "steps": steps,
        "mass0": m0,
        "mass1": m1,
        "abs_delta_mass": abs(m1 - m0)
    }


def rk4_reaction_only_step(u: np.ndarray, r: float, ucoef: float, dt: float) -> np.ndarray:
    # du/dt = r u - ucoef u^2
    def f(x):
        return r * x - ucoef * x * x
    k1 = f(u)
    k2 = f(u + 0.5 * dt * k1)
    k3 = f(u + 0.5 * dt * k2)
    k4 = f(u + dt * k3)
    return u + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def reaction_only_q_invariant_convergence(r: float, ucoef: float, W0: float, dt_list: List[float], T: float) -> Dict[str, Any]:
    max_drifts: List[float] = []
    for dt in dt_list:
        steps = max(2, int(np.ceil(T / dt)))
        t = 0.0
        u = np.array([W0], dtype=float)
        q0 = float(logistic_invariant_Q(u, r, ucoef, t))
        max_drift = 0.0
        for _ in range(steps):
            u = rk4_reaction_only_step(u, r, ucoef, dt)
            t += dt
            q = float(logistic_invariant_Q(u, r, ucoef, t))
            max_drift = max(max_drift, abs(q - q0))
        max_drifts.append(max_drift)
    # Fit log-log slope
    x = np.log(np.array(dt_list, dtype=float))
    y = np.log(np.array(max_drifts, dtype=float))
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    # Plot
    fig_path = figure_path("rd_conservation", "q_invariant_convergence", failed=False)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_list, max_drifts, "o-")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("dt")
    plt.ylabel("max |ΔQ|")
    plt.title(f"RK4 reaction-only: slope≈{slope:.3f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    return {
        "dt": dt_list,
        "max_abs_Q_drift": max_drifts,
        "fit": {"slope": float(slope), "intercept": float(intercept)},
        "figure": str(fig_path)
    }


def main():
    here = Path(__file__).resolve().parent
    spec_path = here / "step_spec.example.json"
    spec = StepSpec(**json.loads(spec_path.read_text()))

    # Controls — Diffusion-only mass conservation
    N = int(spec.grid["N"])
    dx = float(spec.grid["dx"])
    D = float(spec.params["D"])
    seed = 42
    dt = min(spec.dt_sweep)
    steps = 100
    ctrl_diff = diffusion_only_mass_check(N, dx, D, dt, steps, seed)
    ctrl_diff_log = {
        "control": "diffusion_only_mass",
        "spec": {
            "N": N, "dx": dx, "D": D, "dt": dt, "steps": steps,
            "bc": spec.bc, "scheme": spec.scheme
        },
        "metrics": ctrl_diff,
        "passes": {"machine_epsilon": ctrl_diff["abs_delta_mass"] < 1e-12}
    }
    write_log(log_path("rd_conservation", "controls_diffusion", failed=not ctrl_diff_log["passes"]["machine_epsilon"]), ctrl_diff_log)

    # Controls — Reaction-only Q invariant (RK4 expected order-4)
    q_T = 10.0
    q_dt_list = [0.02, 0.01, 0.005]
    q_ctrl = reaction_only_q_invariant_convergence(float(spec.params["r"]), float(spec.params["u"]), W0=0.12, dt_list=q_dt_list, T=q_T)
    ctrl_reac_log = {
        "control": "reaction_only_Q_invariant_rk4",
        "spec": {"r": spec.params["r"], "u": spec.params["u"], "dt_list": q_dt_list, "T": q_T},
        "metrics": q_ctrl,
        "passes": {"slope_ge_3.9": q_ctrl["fit"]["slope"] >= 3.9}
    }
    write_log(log_path("rd_conservation", "controls_reaction", failed=not ctrl_reac_log["passes"]["slope_ge_3.9"]), ctrl_reac_log)

    # Record step_spec for this run (as a convenience)
    spec_log = {
        "bc": spec.bc,
        "scheme": spec.scheme,
        "order_p": spec.order_p,
        "expected_dt_slope": spec.expected_dt_slope,
        "grid": spec.grid,
        "params": spec.params,
        "dt_sweep": spec.dt_sweep,
        "seeds": spec.seeds,
        "safety": spec.safety,
        "cfl_used": spec.cfl_used,
        "adjacency": spec.adjacency,
        "notes": spec.notes
    }
    write_log(log_path("rd_conservation", "step_spec_snapshot", failed=False), spec_log)

    print(json.dumps({
        "controls_diffusion": ctrl_diff_log["passes"],
        "controls_reaction": ctrl_reac_log["passes"],
        "step_spec_logged": True
    }, indent=2))


if __name__ == "__main__":
    main()
