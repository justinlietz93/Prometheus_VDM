#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import matplotlib.pyplot as plt

# Ensure code root on sys.path
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from physics.metriplectic.compose import j_only_step, m_only_step, jmj_strang_step, two_grid_error_inf, lyapunov_values


@dataclass
class StepSpec:
    bc: str
    scheme: str  # j_only | m_only | jmj
    grid: Dict[str, Any]
    params: Dict[str, Any]  # {c} for J, {D,r,u} for M, may include both
    dt_sweep: List[float]
    seeds: int | List[int]
    notes: str | None = None


def rng_field(N: int, scale: float, seed: int) -> np.ndarray:
    return np.random.default_rng(seed).random(N).astype(float) * scale


def select_stepper(scheme: str, dx: float, params: Dict[str, Any]):
    s = scheme.lower()
    if s == "j_only":
        return lambda W, dt: j_only_step(W, dt, dx, params)
    elif s == "m_only":
        return lambda W, dt: m_only_step(W, dt, dx, params)
    elif s == "jmj":
        return lambda W, dt: jmj_strang_step(W, dt, dx, params)
    else:
        return lambda W, dt: j_only_step(W, dt, dx, params)


def sweep_two_grid(spec: StepSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"])
    dx = float(spec.grid["dx"])
    step = select_stepper(spec.scheme, dx, spec.params)
    seed_list = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    dt_vals = [float(d) for d in spec.dt_sweep]
    dt_to_errs: Dict[float, List[float]] = {d: [] for d in dt_vals}
    samples = []
    for seed in seed_list:
        W0 = rng_field(N, 0.1, seed)
        for dt in dt_vals:
            e = two_grid_error_inf(step, W0, dt)
            dt_to_errs[dt].append(e)
            samples.append({"seed": int(seed), "dt": float(dt), "two_grid_error_inf": float(e)})
    med = [float(np.median(dt_to_errs[d])) for d in dt_vals]
    x = np.log(np.array(dt_vals, dtype=float))
    y = np.log(np.array(med, dtype=float) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, intercept])
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    expected = 2.0 if spec.scheme.lower() in ("j_only", "jmj") else 2.0
    failed_gate = bool((slope < expected - 0.1) or (R2 < 0.999))

    # Artifacts
    fig_path = figure_path("metriplectic", f"residual_vs_dt_{spec.scheme}", failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_vals, med, "o-")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("two-grid error ||Φ_dt - Φ_{dt/2}∘Φ_{dt/2}||_∞")
    plt.title(f"{spec.scheme} two-grid: slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()

    sweep_exact = {"scheme": spec.scheme, "bc": spec.bc, "samples": samples}
    write_log(log_path("metriplectic", f"sweep_exact_{spec.scheme}", failed=failed_gate), sweep_exact)
    summary = {
        "scheme": spec.scheme,
        "dt": dt_vals,
        "two_grid_error_inf_med": med,
        "fit": {"slope": float(slope), "R2": float(R2)},
        "expected_slope": expected,
        "failed": failed_gate,
        "figure": str(fig_path)
    }
    write_log(log_path("metriplectic", f"sweep_dt_{spec.scheme}", failed=failed_gate), summary)
    csv_path = log_path("metriplectic", f"residual_vs_dt_{spec.scheme}", failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("dt,two_grid_error_inf_median\n")
        for d, e in zip(dt_vals, med):
            f.write(f"{d},{e}\n")
    return summary


def j_reversibility_check(spec: StepSpec) -> Dict[str, Any]:
    if spec.scheme.lower() != "j_only":
        return {"skipped": True}
    N = int(spec.grid["N"]); dx = float(spec.grid["dx"]) ; dt = float(min(spec.dt_sweep))
    step = select_stepper("j_only", dx, spec.params)
    W0 = rng_field(N, 0.1, 17)
    W1 = step(W0, dt)
    # Reverse with -dt
    W2 = step(W1, -dt)
    rev_err = float(np.linalg.norm(W2 - W0, ord=np.inf))
    passes = rev_err <= 1e-12
    logj = {"rev_inf_error": rev_err, "dt": dt, "passes": passes}
    write_log(log_path("metriplectic", "j_reversibility", failed=not passes), logj)
    return logj


def m_lyapunov_check(spec: StepSpec) -> Dict[str, Any]:
    if spec.scheme.lower() not in ("m_only", "jmj"):
        return {"skipped": True}
    N = int(spec.grid["N"]); dx = float(spec.grid["dx"]) ; dt = float(min(spec.dt_sweep))
    params = spec.params
    step = select_stepper(spec.scheme, dx, params)
    W = rng_field(N, 0.1, 123)
    series = []
    L_prev = lyapunov_values(W, dx, float(params.get("D", 0.0)), float(params.get("r", 0.0)), float(params.get("u", 0.0)))
    for k in range(50):
        Wn1 = step(W, dt)
        L_now = lyapunov_values(Wn1, dx, float(params.get("D", 0.0)), float(params.get("r", 0.0)), float(params.get("u", 0.0)))
        series.append({"step": k+1, "delta_L": float(L_now - L_prev), "L": float(L_now)})
        W = Wn1; L_prev = L_now
    tol_pos = 1e-12
    violations = int(sum(1 for s in series if s["delta_L"] > tol_pos))
    failed = bool(violations > 0)
    fig_path = figure_path("metriplectic", f"lyapunov_delta_per_step_{spec.scheme}", failed=failed)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6,4)); plt.plot([s["step"] for s in series],[s["delta_L"] for s in series],"o-")
    plt.axhline(0.0, color='k', linewidth=0.8)
    plt.xlabel("step"); plt.ylabel("ΔL_h")
    plt.title(f"Lyapunov per step ({spec.scheme})")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    logj = {"series": series, "violations": violations, "tol_pos": tol_pos, "figure": str(fig_path), "failed": failed}
    write_log(log_path("metriplectic", f"lyapunov_series_{spec.scheme}", failed=failed), logj)
    return logj


def main():
    import argparse
    p = argparse.ArgumentParser(description="Metriplectic Harness (additive to RD)")
    p.add_argument("--spec", type=str, default=str(Path(__file__).resolve().parent / "step_spec.metriplectic.example.json"))
    p.add_argument("--scheme", type=str, default=None, help="Override scheme: j_only|m_only|jmj")
    args = p.parse_args()
    spec_path = Path(args.spec)
    spec = StepSpec(**json.loads(spec_path.read_text()))
    if args.scheme:
        spec.scheme = args.scheme

    # Snapshot spec
    write_log(log_path("metriplectic", "step_spec_snapshot", failed=False), {
        "bc": spec.bc, "scheme": spec.scheme, "grid": spec.grid, "params": spec.params,
        "dt_sweep": spec.dt_sweep, "seeds": spec.seeds, "notes": spec.notes
    })

    # Diagnostics
    j_rev = j_reversibility_check(spec)
    m_lya = m_lyapunov_check(spec)
    sweep = sweep_two_grid(spec)

    print(json.dumps({
        "scheme": spec.scheme,
        "j_reversibility": j_rev,
        "m_lyapunov": m_lya,
        "two_grid": sweep
    }, indent=2))


if __name__ == "__main__":
    main()
