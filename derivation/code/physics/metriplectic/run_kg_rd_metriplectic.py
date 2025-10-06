#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np

# Ensure code root on sys.path
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from physics.metriplectic.kg_ops import kg_verlet_step, kg_energy
from physics.metriplectic.compose import (
    m_only_step_with_stats, jmj_strang_step_with_stats, mjm_strang_step,
    two_grid_error_inf
)


@dataclass
class StepSpec:
    bc: str
    scheme: str  # j_only | m_only | jmj
    grid: Dict[str, Any]
    params: Dict[str, Any]
    dt_sweep: List[float]
    seeds: int | List[int]
    notes: str | None = None
    tag: str | None = None


def _slug(spec: StepSpec, base: str) -> str:
    tag = spec.params.get("tag") if isinstance(spec.params, dict) else None
    if tag is None:
        tag = getattr(spec, "tag", None)
    if not tag:
        return base
    return f"{base}__{str(tag).strip().replace(' ', '-')}"


def rng_pair(N: int, scale: float, seed: int) -> Tuple[np.ndarray, np.ndarray]:
    g = np.random.default_rng(seed)
    return g.random(N).astype(float) * scale, g.random(N).astype(float) * scale


def j_only_kg_step(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    return kg_verlet_step(phi, pi, dt, dx, float(params.get("c", 1.0)), float(params.get("m", 0.0)))


def j_reversibility_kg(spec: StepSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt = float(min(spec.dt_sweep))
    scale = float(spec.params.get("seed_scale", 0.1))
    phi0, pi0 = rng_pair(N, scale, 17)
    E0 = kg_energy(phi0, pi0, dx, float(spec.params.get("c", 1.0)), float(spec.params.get("m", 0.0)))
    phi1, pi1 = j_only_kg_step(phi0, pi0, dt, dx, spec.params)
    E1 = kg_energy(phi1, pi1, dx, float(spec.params.get("c", 1.0)), float(spec.params.get("m", 0.0)))
    phi2, pi2 = j_only_kg_step(phi1, pi1, -dt, dx, spec.params)
    E2 = kg_energy(phi2, pi2, dx, float(spec.params.get("c", 1.0)), float(spec.params.get("m", 0.0)))
    rev_err = float(max(np.linalg.norm(phi2 - phi0, ord=np.inf), np.linalg.norm(pi2 - pi0, ord=np.inf)))
    # Gates
    tol_rev_strict = float(spec.params.get("j_only_rev_strict", 1e-12))
    tol_rev_cap = float(spec.params.get("j_only_rev_cap", 1e-10))
    energy_drift_01 = float(abs(E1 - E0))
    energy_drift_20 = float(abs(E2 - E0))
    tol_E = float(spec.params.get("j_only_energy_cap", 1e-12))
    passes_strict = (rev_err <= tol_rev_strict) and (energy_drift_01 <= tol_E) and (energy_drift_20 <= tol_E)
    cap_ok = (rev_err <= tol_rev_cap) and (energy_drift_01 <= max(tol_E, 1e-10)) and (energy_drift_20 <= max(tol_E, 1e-10))
    # FFT roundoff bound for reference
    eps = float(np.finfo(float).eps) ; sqrtN = float(np.sqrt(N)) ; denom = eps * sqrtN if eps*sqrtN>0 else 1.0
    observed_c = float(rev_err / denom)
    logj = {
        "rev_inf_error": rev_err,
        "dt": dt,
        "passes": passes_strict,
        "passes_strict": passes_strict,
        "cap_ok": cap_ok,
        "energy_drifts": {"W1_minus_W0": energy_drift_01, "W2_minus_W0": energy_drift_20},
        "tolerances": {"rev_inf_strict": tol_rev_strict, "rev_inf_cap": tol_rev_cap, "E_cap": tol_E},
        "fft_roundoff_bound": {"epsilon": eps, "sqrtN": sqrtN, "epsilon_sqrtN": eps*sqrtN, "observed_c": observed_c}
    }
    if (not passes_strict) and cap_ok:
        logj["justification"] = "Round-off observed; strict 1e-12 not met; <=1e-10 cap holds."
    write_log(log_path("metriplectic", _slug(spec, "j_reversibility_kg"), failed=not passes_strict), logj)
    return logj


def m_only_sweep(spec: StepSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; seeds = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    dt_vals = [float(d) for d in spec.dt_sweep]
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    params = dict(spec.params)
    params["m_lap_operator"] = str(params.get("m_lap_operator", "spectral"))
    def m_step_fn(W_in: np.ndarray, dt_in: float):
        # reuse RD DG step (spectral by default for KG⊕RD)
        return m_only_step_with_stats(W_in, dt_in, dx, params)[0]
    # two-grid on scalar field W (apply DG to phi only, pi is not present in M)
    dt_to_errs: Dict[float, List[float]] = {d: [] for d in dt_vals}
    for seed in seeds:
        phi0 = np.random.default_rng(seed).random(N).astype(float) * seed_scale
        for dt in dt_vals:
            e = two_grid_error_inf(m_step_fn, phi0, dt)
            dt_to_errs[dt].append(e)
    med = [float(np.median(dt_to_errs[d])) for d in dt_vals]
    x = np.log(np.array(dt_vals, dtype=float)) ; y = np.log(np.array(med, dtype=float) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T ; slope, b = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, b]) ; ss_res = float(np.sum((y - y_pred)**2)) ; ss_tot = float(np.sum((y - np.mean(y))**2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot>0 else 0.0)
    failed = bool((slope < 2.9) or (R2 < 0.999))
    # artifacts
    figp = figure_path("metriplectic", _slug(spec, f"residual_vs_dt_m_only"), failed=failed)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6,4)); plt.plot(dt_vals, med, "o-"); plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("two-grid error ||Φ_dt - Φ_{dt/2}∘Φ_{dt/2}||_∞")
    plt.title(f"M-only two-grid: slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()
    logj = {"scheme": "m_only", "dt": dt_vals, "two_grid_error_inf_med": med, "fit": {"slope": float(slope), "R2": float(R2)}, "failed": failed, "figure": str(figp)}
    write_log(log_path("metriplectic", _slug(spec, "sweep_dt_m_only"), failed=failed), logj)
    csvp = log_path("metriplectic", _slug(spec, "residual_vs_dt_m_only"), failed=failed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("dt,two_grid_error_inf_median\n")
        for d, e in zip(dt_vals, med):
            f.write(f"{d},{e}\n")
    return logj


def jmj_kg_rd_sweep(spec: StepSpec) -> Dict[str, Any]:
    # Compose J(kg) and M(DG) as Strang with spectral M
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt_vals = [float(d) for d in spec.dt_sweep]
    seeds = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    seed_scale = float(spec.params.get("seed_scale", 0.1))
    params = dict(spec.params)
    params["m_lap_operator"] = str(params.get("m_lap_operator", "spectral"))

    def jmj_step_scalar(W: np.ndarray, dt: float) -> np.ndarray:
        # Lift scalar W to (phi,pi), apply JMJ then return phi component for error measure
        phi0 = W.copy()
        pi0 = np.zeros_like(W)
        # J half
        phi1, pi1 = kg_verlet_step(phi0, pi0, 0.5*dt, dx, float(params.get("c",1.0)), float(params.get("m",0.0)))
        # M full (DG on phi only)
        phi2, stats = m_only_step_with_stats(phi1, dt, dx, params)
        # J half
        phi3, pi3 = kg_verlet_step(phi2, pi1, 0.5*dt, dx, float(params.get("c",1.0)), float(params.get("m",0.0)))
        return phi3

    dt_to_errs: Dict[float, List[float]] = {d: [] for d in dt_vals}
    for seed in seeds:
        phi0 = np.random.default_rng(seed).random(N).astype(float) * seed_scale
        for dt in dt_vals:
            e = two_grid_error_inf(jmj_step_scalar, phi0, dt)
            dt_to_errs[dt].append(e)
    med = [float(np.median(dt_to_errs[d])) for d in dt_vals]
    x = np.log(np.array(dt_vals, dtype=float)) ; y = np.log(np.array(med, dtype=float) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T ; slope, b = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, b]) ; ss_res = float(np.sum((y - y_pred)**2)) ; ss_tot = float(np.sum((y - np.mean(y))**2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot>0 else 0.0)
    failed = bool((slope < 2.9) or (R2 < 0.999))
    # artifacts
    import matplotlib.pyplot as plt
    figp = figure_path("metriplectic", _slug(spec, f"residual_vs_dt_jmj"), failed=failed)
    plt.figure(figsize=(6,4)); plt.plot(dt_vals, med, "o-"); plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("two-grid error ||Φ_dt - Φ_{dt/2}∘Φ_{dt/2}||_∞")
    plt.title(f"JMJ two-grid (KG⊕RD spectral-DG): slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()
    logj = {"scheme": "jmj", "dt": dt_vals, "two_grid_error_inf_med": med, "fit": {"slope": float(slope), "R2": float(R2)}, "failed": failed, "figure": str(figp)}
    write_log(log_path("metriplectic", _slug(spec, "sweep_dt_jmj"), failed=failed), logj)
    csvp = log_path("metriplectic", _slug(spec, "residual_vs_dt_jmj"), failed=failed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("dt,two_grid_error_inf_median\n")
        for d, e in zip(dt_vals, med):
            f.write(f"{d},{e}\n")
    return logj


def defect_diagnostic(spec: StepSpec) -> Dict[str, Any]:
    # Measure ||Φ^JMJ_Δt - Φ^MJM_Δt||_∞ on phi component
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; params = dict(spec.params)
    params["m_lap_operator"] = str(params.get("m_lap_operator", "spectral"))
    dt_vals = [float(d) for d in params.get("dt_sweep_small", [0.02, 0.01, 0.005, 0.0025])]
    seeds = list(range(int(spec.seeds))) if isinstance(spec.seeds, int) else [int(s) for s in spec.seeds]
    seed_scale = float(spec.params.get("seed_scale", 0.1))

    def jmj_step_pair(W: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
        phi0 = W.copy(); pi0 = np.zeros_like(W)
        # J half
        phi1, pi1 = kg_verlet_step(phi0, pi0, 0.5*dt, dx, float(params.get("c",1.0)), float(params.get("m",0.0)))
        # M full
        phi2, _ = m_only_step_with_stats(phi1, dt, dx, params)
        # J half
        phi3, pi3 = kg_verlet_step(phi2, pi1, 0.5*dt, dx, float(params.get("c",1.0)), float(params.get("m",0.0)))
        # Reverse order (MJM)
        phi_m1, _ = m_only_step_with_stats(phi0, 0.5*dt, dx, params)
        phi_m2, pi_m2 = kg_verlet_step(phi_m1, pi0, dt, dx, float(params.get("c",1.0)), float(params.get("m",0.0)))
        phi_m3, _ = m_only_step_with_stats(phi_m2, 0.5*dt, dx, params)
        return phi3, phi_m3

    dt_to_def: Dict[float, List[float]] = {d: [] for d in dt_vals}
    for seed in seeds:
        W0 = np.random.default_rng(seed).random(N).astype(float) * seed_scale
        for dt in dt_vals:
            a, b = jmj_step_pair(W0, dt)
            dt_to_def[dt].append(float(np.linalg.norm(a - b, ord=np.inf)))
    med = [float(np.median(dt_to_def[d])) for d in dt_vals]
    x = np.log(np.array(dt_vals, dtype=float)) ; y = np.log(np.array(med, dtype=float) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T ; slope, b = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, b]) ; ss_res = float(np.sum((y - y_pred)**2)) ; ss_tot = float(np.sum((y - np.mean(y))**2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot>0 else 0.0)
    figp = figure_path("metriplectic", _slug(spec, "strang_defect_vs_dt"), failed=False)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6,4)); plt.plot(dt_vals, med, "o-"); plt.xscale("log"); plt.yscale("log")
    plt.xlabel("dt"); plt.ylabel("||Φ^JMJ_Δt - Φ^MJM_Δt||_∞ (phi)")
    plt.title(f"Strang defect (KG⊕RD): slope≈{float(slope):.3f}, R2≈{float(R2):.4f}")
    plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()
    logj = {"dt": dt_vals, "defect_med": med, "fit": {"slope": float(slope), "R2": float(R2)}, "figure": str(figp)}
    write_log(log_path("metriplectic", _slug(spec, "strang_defect_vs_dt"), failed=False), logj)
    csvp = log_path("metriplectic", _slug(spec, "strang_defect_vs_dt"), failed=False, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("dt,strang_defect_median\n")
        for d, e in zip(dt_vals, med):
            f.write(f"{d},{e}\n")
    return logj


def main():
    import argparse
    p = argparse.ArgumentParser(description="KG⊕RD Metriplectic Runner (additive)")
    p.add_argument("--spec", type=str, required=True)
    p.add_argument("--scheme", type=str, default=None)
    args = p.parse_args()
    spec_path = Path(args.spec)
    spec = StepSpec(**json.loads(spec_path.read_text()))
    if args.scheme:
        spec.scheme = args.scheme

    # Snapshot with minimal provenance
    write_log(log_path("metriplectic", _slug(spec, "step_spec_snapshot"), failed=False), {
        "bc": spec.bc, "scheme": spec.scheme, "grid": spec.grid, "params": spec.params,
        "dt_sweep": spec.dt_sweep, "seeds": spec.seeds, "notes": spec.notes
    })

    # Diagnostics
    j_rev = j_reversibility_kg(spec)
    m_sw = m_only_sweep(spec)
    jmj_sw = jmj_kg_rd_sweep(spec)
    defect = defect_diagnostic(spec)

    print(json.dumps({
        "scheme": spec.scheme,
        "j_reversibility_kg": j_rev,
        "two_grid_m_only": m_sw,
        "two_grid_jmj": jmj_sw,
        "strang_defect": defect
    }, indent=2))


if __name__ == "__main__":
    main()
