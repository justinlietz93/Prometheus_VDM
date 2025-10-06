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
from physics.metriplectic.compose import (
    j_only_step, m_only_step, m_only_step_with_stats,
    jmj_strang_step, jmj_strang_step_with_stats, mjm_strang_step,
    two_grid_error_inf, lyapunov_values
)
from physics.rd_conservation.run_rd_conservation import cas_solve_linear_balance, Q_from_coeffs


@dataclass
class StepSpec:
    bc: str
    scheme: str  # j_only | m_only | jmj
    grid: Dict[str, Any]
    params: Dict[str, Any]  # {c} for J, {D,r,u} for M, may include both
    dt_sweep: List[float]
    seeds: int | List[int]
    notes: str | None = None
    # Optional tag for artifact slugs; may also be supplied via params["tag"].
    tag: str | None = None


def rng_field(N: int, scale: float, seed: int) -> np.ndarray:
    return np.random.default_rng(seed).random(N).astype(float) * scale


def select_stepper(scheme: str, dx: float, params: Dict[str, Any]):
    s = scheme.lower()
    if s == "j_only":
        return lambda W, dt: j_only_step(W, dt, dx, params)
    elif s == "m_only":
        # Enforce dg_tol by using with-stats and discarding stats
        return lambda W, dt: m_only_step_with_stats(W, dt, dx, params)[0]
    elif s == "jmj":
        # Enforce dg_tol by using with-stats and discarding stats
        return lambda W, dt: jmj_strang_step_with_stats(W, dt, dx, params)[0]
    else:
        return lambda W, dt: j_only_step(W, dt, dx, params)


def _slug(spec: StepSpec, base: str) -> str:
    """Append optional run tag to a base slug for artifact paths.

    Tag resolution order: spec.params['tag'] if present, else spec.tag.
    If no tag, returns base unchanged.
    """
    tag = None
    try:
        tag = spec.params.get("tag")
    except Exception:
        tag = None
    if tag is None:
        tag = getattr(spec, "tag", None)
    if tag is None or str(tag).strip() == "":
        return base
    # sanitize minimal: replace spaces with '-'
    safe = str(tag).strip().replace(" ", "-")
    return f"{base}__{safe}"

def sweep_two_grid(spec: StepSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"])
    dx = float(spec.grid["dx"])
    step = select_stepper(spec.scheme, dx, spec.params)
    seed_list = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    dt_vals = [float(d) for d in spec.dt_sweep]
    dt_to_errs: Dict[float, List[float]] = {d: [] for d in dt_vals}
    samples = []
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    for seed in seed_list:
        W0 = rng_field(N, seed_scale, seed)
        for dt in dt_vals:
            e = two_grid_error_inf(step, W0, dt)
            dt_to_errs[dt].append(e)
            samples.append({"seed": int(seed), "dt": float(dt), "two_grid_error_inf": float(e)})
    med = [float(np.median(dt_to_errs[d])) for d in dt_vals]
    s_lower = spec.scheme.lower()
    trivial_exact = bool(s_lower == "j_only" and all(m < 1e-14 for m in med))
    if trivial_exact:
        slope, R2 = 0.0, 1.0
        failed_gate = False
        expected = None
    else:
        x = np.log(np.array(dt_vals, dtype=float))
        y = np.log(np.array(med, dtype=float) + 1e-30)
        A = np.vstack([x, np.ones_like(x)]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        y_pred = A @ np.array([slope, intercept])
        ss_res = float(np.sum((y - y_pred) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
        # Gates: allow explicit thresholds via params; fallback to expected ~2 for JMJ/M-only
        gate_slope = spec.params.get("gate_slope")
        gate_R2 = float(spec.params.get("gate_R2", 0.999))
        expected = 2.0 if s_lower in ("jmj", "m_only") else None
        slope_min = float(gate_slope) if gate_slope is not None else (expected - 0.1 if expected is not None else -np.inf)
        failed_gate = bool((slope < slope_min) or (R2 < gate_R2))

    # Artifacts
    fig_path = figure_path("metriplectic", _slug(spec, f"residual_vs_dt_{spec.scheme}"), failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_vals, med, "o-")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("two-grid error ||Φ_dt - Φ_{dt/2}∘Φ_{dt/2}||_∞")
    title = f"{spec.scheme} two-grid: slope≈{float(slope):.3f}, R2≈{float(R2):.4f}"
    if trivial_exact:
        title += " (trivial exact)"
    plt.title(title)
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()

    sweep_exact = {"scheme": spec.scheme, "bc": spec.bc, "samples": samples}
    write_log(log_path("metriplectic", _slug(spec, f"sweep_exact_{spec.scheme}"), failed=failed_gate), sweep_exact)
    summary = {
        "scheme": spec.scheme,
        "dt": dt_vals,
        "two_grid_error_inf_med": med,
        "fit": {"slope": float(slope), "R2": float(R2)},
        "expected_slope": (None if expected is None else float(expected)),
        "failed": failed_gate,
        "gate": {"slope_min": (None if np.isneginf(slope_min) else float(slope_min)), "R2_min": float(gate_R2)},
        "figure": str(fig_path),
        "trivial_exact": trivial_exact
    }
    write_log(log_path("metriplectic", _slug(spec, f"sweep_dt_{spec.scheme}"), failed=failed_gate), summary)
    csv_path = log_path("metriplectic", _slug(spec, f"residual_vs_dt_{spec.scheme}"), failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("dt,two_grid_error_inf_median\n")
        for d, e in zip(dt_vals, med):
            f.write(f"{d},{e}\n")
    return summary


def j_reversibility_check(spec: StepSpec) -> Dict[str, Any]:
    # Always evaluate J-only reversibility, independent of provided scheme
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt = float(min(spec.dt_sweep))
    step = select_stepper("j_only", dx, spec.params)
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    W0 = rng_field(N, seed_scale, 17)
    W1 = step(W0, dt)
    # Reverse with -dt
    W2 = step(W1, -dt)
    rev_err = float(np.linalg.norm(W2 - W0, ord=np.inf))
    # L2 norm preservation (unitary spectral shift)
    l2_0 = float(np.linalg.norm(W0))
    l2_1 = float(np.linalg.norm(W1))
    l2_2 = float(np.linalg.norm(W2))
    l2_drift_01 = float(abs(l2_1 - l2_0))
    l2_drift_20 = float(abs(l2_2 - l2_0))
    # Gates: strict and cap thresholds
    tol_rev_strict = float(spec.params.get("j_only_rev_strict", 1e-12))
    tol_rev_cap = float(spec.params.get("j_only_rev_cap", 1e-10))
    tol_l2 = float(spec.params.get("j_only_l2_cap", 1e-10))
    passes_strict = (rev_err <= tol_rev_strict) and (l2_drift_01 <= tol_l2) and (l2_drift_20 <= tol_l2)
    cap_ok = (rev_err <= tol_rev_cap) and (l2_drift_01 <= tol_l2) and (l2_drift_20 <= tol_l2)
    passes = passes_strict
    # Pragmatic FFT-based bound logging (do not change gates):
    eps = float(np.finfo(float).eps)
    sqrtN = float(np.sqrt(N))
    denom = eps * sqrtN if eps * sqrtN > 0.0 else 1.0
    observed_c = float(rev_err / denom)
    logj = {
        "rev_inf_error": rev_err, "dt": dt, "passes": passes,
        "passes_strict": passes_strict, "cap_ok": cap_ok,
        "l2_norms": {"W0": l2_0, "W1": l2_1, "W2": l2_2},
        "l2_drifts": {"W1_minus_W0": l2_drift_01, "W2_minus_W0": l2_drift_20},
        "tolerances": {"rev_inf_strict": tol_rev_strict, "rev_inf_cap": tol_rev_cap, "l2_cap": tol_l2},
        "fft_roundoff_bound": {"epsilon": eps, "sqrtN": sqrtN, "epsilon_sqrtN": denom, "observed_c": observed_c}
    }
    # If strict fails but cap holds, log justification and mark as failed to keep gate conservative
    if (not passes) and cap_ok:
        logj["justification"] = "FFT round-off observed; strict 1e-12 not met, but <= 1e-10 cap holds."
    write_log(log_path("metriplectic", _slug(spec, "j_reversibility"), failed=not passes), logj)
    return logj


def m_lyapunov_check(spec: StepSpec) -> Dict[str, Any]:
    if spec.scheme.lower() not in ("m_only", "jmj"):
        return {"skipped": True}
    N = int(spec.grid["N"]); dx = float(spec.grid["dx"]) ; dt = float(min(spec.dt_sweep))
    params = spec.params
    # Guard: require DG params for M-step
    for k in ("D", "r", "u"):
        if k not in params:
            return {"skipped": True, "reason": f"missing_param:{k}"}
    step = select_stepper(spec.scheme, dx, params)
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    W = rng_field(N, seed_scale, 123)
    series = []
    L_prev = lyapunov_values(W, dx, float(params.get("D", 0.0)), float(params.get("r", 0.0)), float(params.get("u", 0.0)))
    for k in range(20):
        Wn1 = step(W, dt)
        L_now = lyapunov_values(Wn1, dx, float(params.get("D", 0.0)), float(params.get("r", 0.0)), float(params.get("u", 0.0)))
        series.append({"step": k+1, "delta_L": float(L_now - L_prev), "L": float(L_now)})
        W = Wn1; L_prev = L_now
    tol_pos = 1e-12
    violations = int(sum(1 for s in series if s["delta_L"] > tol_pos))
    failed = bool(violations > 0)
    fig_path = figure_path("metriplectic", _slug(spec, f"lyapunov_delta_per_step_{spec.scheme}"), failed=failed)
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    plt.figure(figsize=(6,4)); plt.plot([s["step"] for s in series],[s["delta_L"] for s in series],"o-")
    plt.axhline(0.0, color='k', linewidth=0.8)
    plt.xlabel("step"); plt.ylabel("ΔL_h")
    plt.title(f"Lyapunov per step ({spec.scheme})")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    logj = {"series": series, "violations": violations, "tol_pos": tol_pos, "figure": str(fig_path), "failed": failed}
    write_log(log_path("metriplectic", _slug(spec, f"lyapunov_series_{spec.scheme}"), failed=failed), logj)
    return logj


def small_dt_sweep_polish(spec: StepSpec) -> Dict[str, Any]:
    """Repeat JMJ with smaller dt sweep and tighter DG tolerance; log Newton stats.

    Uses dt_sweep_small from params if present, else defaults to [0.02,0.01,0.005,0.0025].
    Passes dg_tol=1e-12 (overridable via params). Aggregates stats across seeds.
    """
    if spec.scheme.lower() != "jmj":
        return {"skipped": True}
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; params = dict(spec.params)
    params["dg_tol"] = float(params.get("dg_tol", 1e-12))
    dt_vals = [0.02, 0.01, 0.005, 0.0025, 0.00125]
    dt_vals = [float(d) for d in spec.params.get("dt_sweep_small", dt_vals)]
    seeds = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    dt_to_errs: Dict[float, List[float]] = {d: [] for d in dt_vals}
    newton_rows = []
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    for seed in seeds:
        W0 = rng_field(N, seed_scale, seed)
        for dt in dt_vals:
            # Run JMJ with stats to capture Newton behavior in the M step
            step_stats = []
            def step_with_stats(W_in, dt_in):
                W1 = j_only_step(W_in, 0.5 * dt_in, dx, params)
                W2, stats = m_only_step_with_stats(W1, dt_in, dx, params)
                step_stats.append({"iters": int(stats.get("iters", 0)), "final_residual_inf": float(stats.get("final_residual_inf", 0.0)), "backtracks": int(stats.get("backtracks", 0)), "converged": bool(stats.get("converged", False))})
                W3 = j_only_step(W2, 0.5 * dt_in, dx, params)
                return W3
            e = two_grid_error_inf(step_with_stats, W0, dt)
            dt_to_errs[dt].append(e)
            if step_stats:
                s0 = step_stats[0]
                newton_rows.append({"seed": int(seed), "dt": float(dt), **s0})
    med = [float(np.median(dt_to_errs[d])) for d in dt_vals]
    x = np.log(np.array(dt_vals, dtype=float))
    y = np.log(np.array(med, dtype=float) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, intercept])
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    failed_gate = bool(slope < 2.9 or R2 < 0.999)
    # Artifacts
    fig_path = figure_path("metriplectic", _slug(spec, f"residual_vs_dt_small_{spec.scheme}"), failed=failed_gate)
    plt.figure(figsize=(6, 4))
    plt.plot(dt_vals, med, "o-")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("two-grid error ||Φ_dt - Φ_{dt/2}∘Φ_{dt/2}||_∞")
    plt.title(f"{spec.scheme} small-dt: slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    # Logs
    write_log(log_path("metriplectic", _slug(spec, f"sweep_small_exact_{spec.scheme}"), failed=failed_gate), {"samples": [{"seed": r["seed"], "dt": r["dt"]} for r in newton_rows]})
    summary = {
        "scheme": spec.scheme,
        "dt": dt_vals,
        "two_grid_error_inf_med": med,
        "fit": {"slope": float(slope), "R2": float(R2)},
        "failed": failed_gate,
        "figure": str(fig_path),
        "newton_stats": newton_rows,
        "dg_tol": float(params["dg_tol"]) 
    }
    write_log(log_path("metriplectic", _slug(spec, f"sweep_small_dt_{spec.scheme}"), failed=failed_gate), summary)
    csv_path = log_path("metriplectic", _slug(spec, f"sweep_small_dt_{spec.scheme}"), failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("dt,two_grid_error_inf_median\n")
        for d, e in zip(dt_vals, med):
            f.write(f"{d},{e}\n")
    # Newton stats CSV
    csv2 = log_path("metriplectic", _slug(spec, f"newton_stats_small_{spec.scheme}"), failed=failed_gate, type="csv")
    with csv2.open("w", encoding="utf-8") as f:
        f.write("seed,dt,iters,final_residual_inf,backtracks,converged\n")
        for r in newton_rows:
            f.write(f"{r['seed']},{r['dt']},{r['iters']},{r['final_residual_inf']},{r['backtracks']},{int(r['converged'])}\n")
    return summary


def commutator_defect_diagnostic(spec: StepSpec) -> Dict[str, Any]:
    """Measure Strang defect ||Φ^JMJ_Δt - Φ^MJM_Δt||_∞ vs Δt and fit scaling.

    Acts as a proxy for commutator strength; expected ≈ O(Δt^3) under smoothness.
    """
    if spec.scheme.lower() != "jmj":
        return {"skipped": True}
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; params = dict(spec.params)
    # Prefer the small-dt sweep for defect measurement if provided
    dt_default = [0.02, 0.01, 0.005, 0.0025, 0.00125]
    dt_vals = [float(d) for d in params.get("defect_dt", params.get("dt_sweep_small", dt_default))]
    seeds = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    dt_to_def: Dict[float, List[float]] = {float(d): [] for d in dt_vals}
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    for seed in seeds:
        W0 = rng_field(N, seed_scale, seed)
        for dt in dt_vals:
            W_jmj = jmj_strang_step(W0, dt, dx, params)
            W_mjm = mjm_strang_step(W0, dt, dx, params)
            def_err = float(np.linalg.norm(W_jmj - W_mjm, ord=np.inf))
            dt_to_def[float(dt)].append(def_err)
    dt_vals = [float(d) for d in dt_vals]
    med = [float(np.median(dt_to_def[d])) for d in dt_vals]
    x = np.log(np.array(dt_vals, dtype=float))
    y = np.log(np.array(med, dtype=float) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, intercept])
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    failed_gate = bool(R2 < 0.999)
    fig_path = figure_path("metriplectic", _slug(spec, "strang_defect_vs_dt"), failed=failed_gate)
    plt.figure(figsize=(6,4)); plt.plot(dt_vals, med, "o-"); plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("||Φ^JMJ_Δt - Φ^MJM_Δt||_∞"); plt.title(f"Strang defect: slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(fig_path, dpi=150); plt.close()
    logj = {"dt": dt_vals, "defect_med": med, "fit": {"slope": float(slope), "R2": float(R2)}, "figure": str(fig_path), "failed": failed_gate}
    write_log(log_path("metriplectic", _slug(spec, "strang_defect_vs_dt"), failed=failed_gate), logj)
    csv_path = log_path("metriplectic", _slug(spec, "strang_defect_vs_dt"), failed=failed_gate, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("dt,strang_defect_median\n")
        for d, e in zip(dt_vals, med):
            f.write(f"{d},{e}\n")
    return logj


def robustness_v5_grid(spec: StepSpec) -> Dict[str, Any]:
    """Run a small grid of (r,u,D,N) tuples; aggregate median slopes and Lyapunov violations.

    Gate: PASS if ≥80% of tuples satisfy (slope ≥ 2.9, R2 ≥ 0.999, Lyapunov violations = 0).
    """
    tuples = spec.params.get("v5_grid")
    if tuples is None:
        tuples = [
            {"r": 0.2, "u": 0.25, "D": 1.0, "N": 128},
            {"r": 0.1, "u": 0.2,  "D": 0.5, "N": 128},
            {"r": 0.3, "u": 0.25, "D": 1.0, "N": 256},
        ]
    results = []
    passes = 0
    for tup in tuples:
        grid = {"N": int(tup.get("N", spec.grid["N"])), "dx": float(spec.grid["dx"])}
        params = dict(spec.params)
        params.update({"D": float(tup["D"]), "r": float(tup["r"]), "u": float(tup["u"])})
        local = StepSpec(bc=spec.bc, scheme=spec.scheme, grid=grid, params=params, dt_sweep=spec.dt_sweep, seeds=spec.seeds, notes="v5_grid")
        sw = sweep_two_grid(local)
        ly = m_lyapunov_check(local)
        slope = float(sw.get("fit", {}).get("slope", 0.0))
        R2 = float(sw.get("fit", {}).get("R2", 0.0))
        viol = int(ly.get("violations", 0)) if isinstance(ly, dict) else 0
        ok = (slope >= 2.9) and (R2 >= 0.999) and (viol == 0)
        passes += int(ok)
        results.append({
            "tuple": tup,
            "slope": slope,
            "R2": R2,
            "lyapunov_violations": viol,
            "pass": bool(ok),
            "two_grid_log": sw,
            "lyapunov_log": ly
        })
    pass_rate = float(passes) / float(len(tuples) if tuples else 1)
    passed = bool(pass_rate >= 0.8)
    logj = {"results": results, "pass_rate": pass_rate, "passed": passed}
    write_log(log_path("metriplectic", _slug(spec, "robustness_v5_grid"), failed=not passed), logj)
    # CSV for quick scan
    csvp = log_path("metriplectic", _slug(spec, "robustness_v5_grid"), failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("D,r,u,N,slope,R2,lyapunov_violations,pass\n")
        for rj in results:
            t = rj["tuple"]
            f.write(f"{t['D']},{t['r']},{t['u']},{t['N']},{rj['slope']},{rj['R2']},{rj['lyapunov_violations']},{int(rj['pass'])}\n")
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
    write_log(log_path("metriplectic", _slug(spec, "step_spec_snapshot"), failed=False), {
        "bc": spec.bc, "scheme": spec.scheme, "grid": spec.grid, "params": spec.params,
        "dt_sweep": spec.dt_sweep, "seeds": spec.seeds, "notes": spec.notes
    })

    # Diagnostics
    # Always compute J-only reversibility on the same grid/dt
    j_rev = j_reversibility_check(spec)
    # Lyapunov series for JMJ and M-only
    m_lya = m_lyapunov_check(spec)
    spec_m = StepSpec(bc=spec.bc, scheme="m_only", grid=spec.grid, params=spec.params, dt_sweep=spec.dt_sweep, seeds=spec.seeds, notes=spec.notes)
    m_lya_m = m_lyapunov_check(spec_m)
    # Two-grid sweeps for both JMJ and M-only
    sweep = sweep_two_grid(spec)
    sweep_m = sweep_two_grid(spec_m)
    small = small_dt_sweep_polish(spec)
    defect = commutator_defect_diagnostic(spec)
    v5 = robustness_v5_grid(spec)
    # Fixed-dt |ΔS| comparison panel across j_only, m_only, jmj (for paper narrative)
    try:
        _fixed_dt_deltaS_compare(spec)
    except Exception as e:
        # Non-fatal; logged for transparency
        write_log(log_path("metriplectic", _slug(spec, "fixed_dt_deltaS_compare_error"), failed=True), {"error": str(e)})

    print(json.dumps({
        "scheme": spec.scheme,
        "j_reversibility": j_rev,
        "m_lyapunov_jmj": m_lya,
        "m_lyapunov_m_only": m_lya_m,
        "two_grid_jmj": sweep,
        "two_grid_m_only": sweep_m,
        "small_dt_sweep": small,
        "strang_defect": defect,
        "robustness_v5": v5
    }, indent=2))


# ----------------------
# Helpers for |ΔS| panel
# ----------------------

def _fixed_dt_deltaS_compare(spec: StepSpec) -> Dict[str, Any]:
    """Produce a 1x3 panel comparing |ΔS| at fixed dt for j_only, m_only, jmj.

    Uses CAS-derived Q'(W)=a0+a1 W+a2 W^2 to build S(W)=∑ Q(W_i) Δx.
    Logs PNG + CSV + JSON under outputs/{figures,logs}/metriplectic.
    """
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LogLocator, LogFormatter
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt = float(min(spec.dt_sweep))
    params = spec.params
    # Derive coefficients for Q' using RD CAS helper (aligned with (D,r,u))
    cas = cas_solve_linear_balance(dx, float(params.get("D", 0.0)), float(params.get("r", 0.0)), float(params.get("u", 0.0)), samples=4000, seed=7)
    coeffs = cas["coeffs"]
    a0, a1, a2 = float(coeffs["a0"]), float(coeffs["a1"]), float(coeffs["a2"])

    def S_of(W: np.ndarray) -> float:
        return float(np.sum(Q_from_coeffs(W, a0, a1, a2)) * dx)

    seed_list = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    schemes = ["j_only", "m_only", "jmj"]
    step_map = {s: select_stepper(s, dx, params) for s in schemes}

    combined_rows = []
    summaries: Dict[str, Any] = {}
    fig_path = figure_path("metriplectic", _slug(spec, "fixed_dt_deltaS_compare"), failed=False)
    plt.figure(figsize=(15, 5))
    for idx, sch in enumerate(schemes, start=1):
        vals = [] 
        samples = []
        for seed in seed_list:
            W0 = rng_field(N, seed_scale, seed)
            S0 = S_of(W0)
            W1 = step_map[sch](W0, dt)
            S1 = S_of(W1)
            dS = float(S1 - S0)
            vals.append(abs(dS))
            samples.append({"seed": int(seed), "delta_S": dS})
            combined_rows.append({"scheme": sch, "seed": int(seed), "abs_delta_S": abs(dS)})
        summaries[sch] = {
            "dt": dt,
            "median_abs_delta_S": float(np.median(vals)),
            "mean_abs_delta_S": float(np.mean(vals)),
            "max_abs_delta_S": float(np.max(vals))
        }
        ax = plt.subplot(1, 3, idx)
        # Use log-scaled x-axis with log-spaced bins to reduce label crowding
        vals_pos = [v for v in vals if v > 0]
        if len(vals_pos) == 0:
            # Fallback: add a tiny epsilon to avoid zero-only arrays
            vals_pos = [1e-16]
        vmin = float(min(vals_pos))
        vmax = float(max(vals_pos))
        # Expand bounds slightly for margins
        lo = max(vmin * 0.9, 1e-20)
        hi = vmax * 1.1 if vmax > 0 else 1.0
        bins_count = min(20, max(5, len(vals)//2))
        edges = np.logspace(np.log10(lo), np.log10(hi), bins_count + 1)
        ax.hist(vals_pos, bins=edges)
        ax.set_xscale('log')
        ax.grid(True, which='both', alpha=0.25)
        # Ticks: at most ~5 major ticks, with readable log formatter and slight rotation
        ax.xaxis.set_major_locator(LogLocator(base=10, numticks=5))
        ax.xaxis.set_major_formatter(LogFormatter(base=10, labelOnlyBase=False))
        ax.tick_params(axis='x', labelrotation=25)
        ax.set_xlabel("|ΔS| (log scale)")
        if idx == 1:
            ax.set_ylabel("count")
        ax.set_title(f"{sch} (dt={dt})", fontsize=11)
        # Annotate median and max for quick read
        ax.text(0.98, 0.95,
                f"median={np.median(vals_pos):.2e}\nmax={np.max(vals_pos):.2e}",
                transform=ax.transAxes, ha='right', va='top', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.7, edgecolor='none'))
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3)
    plt.savefig(fig_path, dpi=150)
    plt.close()

    # Logs: JSON + CSV
    jsonj = {"figure": str(fig_path), "dt": dt, "summaries": summaries}
    write_log(log_path("metriplectic", _slug(spec, "fixed_dt_deltaS_compare"), failed=False), jsonj)
    csv_path = log_path("metriplectic", _slug(spec, "fixed_dt_deltaS_compare"), failed=False, type="csv")
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("scheme,seed,abs_delta_S\n")
        for row in combined_rows:
            f.write(f"{row['scheme']},{row['seed']},{row['abs_delta_S']}\n")
    return jsonj


if __name__ == "__main__":
    main()
