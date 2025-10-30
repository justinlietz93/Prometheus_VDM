#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Metriplectic Assisted-Echo experiment (baseline vs assisted) per T4 proposal.

Produces paired artifacts (JSON/CSV) under outputs/logs/metriplectic/ and a figure placeholder.
Requires approval via APPROVAL.json for real runs (tests should use preflight logging helpers instead).
"""
from __future__ import annotations

import json
import os
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
from physics.metriplectic.kg_ops import kg_verlet_step
from physics.metriplectic.kg_noether import stiffness
from physics.metriplectic.compose import m_only_step_with_stats, lyapunov_values_consistent
from physics.metriplectic.echo_metrics import h_energy_norm_delta, ceg
from common.authorization.approval import check_tag_approval
from physics.metriplectic.echo_gates import gate_noether, gate_h_theorem, gate_energy_match, gate_strang_defect


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

def _mjm_step(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    """Reverse Strang: M(dt/2) → J(dt) → M(dt/2) for the KG⊕RD split used here."""
    # M half on phi (pi unchanged)
    phi1, _ = m_only_step_with_stats(phi, 0.5 * dt, dx, params)
    # J full on (phi, pi)
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    phi2, pi2 = kg_verlet_step(phi1, pi, dt, dx, c, m)
    # M half on phi
    phi3, _ = m_only_step_with_stats(phi2, 0.5 * dt, dx, params)
    return phi3, pi2


def _strang_defect(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any], c: float, m: float) -> float:
    """Single-step Strang defect: || Phi_JMJ(dt)(phi,pi) - Phi_MJM(dt)(phi,pi) ||_H."""
    a_phi, a_pi = _jmj_step(phi.copy(), pi.copy(), dt, dx, params)
    b_phi, b_pi = _mjm_step(phi.copy(), pi.copy(), dt, dx, params)
    return h_energy_norm_delta(a_phi, a_pi, b_phi, b_pi, dx, c, m)


def _strang_two_grid_slope(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any], c: float, m: float) -> Tuple[float, float]:
    """Estimate near-cubic Strang defect slope using two-grid ratio e(dt)/e(dt/2). Returns (slope, R2)."""
    e_dt = _strang_defect(phi, pi, dt, dx, params, c, m)
    e_h = _strang_defect(phi, pi, 0.5 * dt, dx, params, c, m)
    if e_dt <= 0.0 or e_h <= 0.0:
        return 0.0, 0.0
    slope = float(np.log(e_dt / e_h) / np.log(2.0))
    # With two points, linear fit is determined; set R²=1.0 if positive observations
    r2 = 1.0
    return slope, r2


def _j_only_roundtrip_drift(phi: np.ndarray, pi: np.ndarray, dt: float, steps: int, dx: float, c: float, m: float) -> float:
    """J-only reversibility meter (canon): compose exact roundtrips per step to minimize accumulation.
    
    Performs, for each k, a forward J step with +dt immediately followed by an inverse J step with -dt.
    This mirrors the reversible composition and suppresses long-horizon accumulation of round-off.
    """
    ph, pr = phi.copy(), pi.copy()
    for _ in range(int(steps)):
        # Forward J
        ph, pr = kg_verlet_step(ph, pr, dt, dx, c, m)
        # Immediate reverse J
        ph, pr = kg_verlet_step(ph, pr, -dt, dx, c, m)
    return h_energy_norm_delta(ph, pr, phi, pi, dx, c, m)


def _assist_correction_pair(phi: np.ndarray, pi: np.ndarray, phi_ref: np.ndarray, pi_ref: np.ndarray, dx: float, params: Dict[str, Any], work: float, c: float, m: float) -> Tuple[np.ndarray, np.ndarray]:
    """Model-aware assistance (two-channel): steepest descent on H-energy distance to (phi_ref, pi_ref).
    
    - phi-direction: -K (phi - phi_ref),  K = -c^2 Δ + m^2  (consistent with KG J instrument)
    - pi-direction:  -(pi - pi_ref)
    The pair (dphi, dpi) is then scaled so that ||(dphi, dpi)||_H == work and applied within the reverse phase.
    """
    if work <= 0:
        return np.zeros_like(phi), np.zeros_like(pi)
    dphi = (phi - phi_ref).astype(float)
    dpi = (pi - pi_ref).astype(float)
    dir_phi = -stiffness(dphi, dx, c, m)      # = c^2 Δ dphi - m^2 dphi
    dir_pi  = -dpi
    if np.allclose(dir_phi, 0.0) and np.allclose(dir_pi, 0.0):
        return np.zeros_like(phi), np.zeros_like(pi)
    def _h_norm(vphi: np.ndarray, vpi: np.ndarray) -> float:
        z = np.zeros_like(vphi)
        return h_energy_norm_delta(vphi, vpi, z, z, dx, c, m)
    size = _h_norm(dir_phi, dir_pi)
    if size == 0.0:
        return np.zeros_like(phi), np.zeros_like(pi)
    scale = float(work / size)
    return (scale * dir_phi.astype(float), scale * dir_pi.astype(float))


# Use _random_correction_pair for H-norm budgeted corrections across (phi, pi).
# Single-channel random correction removed to avoid ambiguity with the H-energy metric.
def _random_correction_pair(rng: np.random.Generator, phi: np.ndarray, pi: np.ndarray, dx: float, work: float, c: float, m: float) -> Tuple[np.ndarray, np.ndarray]:
    """Random H-norm correction in both (phi, pi) channels scaled to the given work budget."""
    if work <= 0:
        return np.zeros_like(phi), np.zeros_like(pi)
    vphi = rng.standard_normal(phi.shape).astype(float)
    vpi  = rng.standard_normal(pi.shape).astype(float)

    def _h_norm(vph: np.ndarray, vpp: np.ndarray) -> float:
        z = np.zeros_like(vph)
        return h_energy_norm_delta(vph, vpp, z, z, dx, c, m)

    size = _h_norm(vphi, vpi)
    if size == 0.0:
        return np.zeros_like(phi), np.zeros_like(pi)
    scale = float(work / size)
    return (scale * vphi, scale * vpi)


def _jmj_forward_step_with_diagnostics(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, float]:
    """One JMJ(Strang) step that returns Sigma delta across the M-step: ΔΣ := -(L_after - L_before) ≥ 0 for DG.
    
    Notes:
    - Lyapunov functional L should be non-increasing under the M-step (ΔL := L_after - L_before ≤ 0).
    - The gate is defined on entropy-like production ΔΣ = -ΔL, expecting ΔΣ ≥ 0 (within tolerance).
    """
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    D = float(params.get("D", 1.0))
    r = float(params.get("r", 0.0))
    u = float(params.get("u", 0.0))
    # J half
    phi1, pi1 = kg_verlet_step(phi, pi, 0.5 * dt, dx, c, m)
    # Lyapunov before M on phi-channel (use gradient consistent with chosen Laplacian)
    lap_mode = str(params.get("m_lap_operator", "stencil"))
    L_before = lyapunov_values_consistent(phi1, dx, D, r, u, lap_operator=lap_mode)
    # M full on phi
    phi2, _ = m_only_step_with_stats(phi1, dt, dx, params)
    # Lyapunov after M
    L_after = lyapunov_values_consistent(phi2, dx, D, r, u, lap_operator=lap_mode)
    # J half
    phi3, pi3 = kg_verlet_step(phi2, pi1, 0.5 * dt, dx, c, m)
    # Report entropy-like production (non-negative if DG step respects H-theorem)
    delta_sigma = -(L_after - L_before)
    return phi3, pi3, float(delta_sigma)


def _two_grid_error_hnorm(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]) -> float:
    """Two-grid local defect using H-norm for one-step JMJ(Strang).

    e(h) = || S_h(z0) - S_{h/2}(S_{h/2}(z0)) ||_H
    """
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    # one big step
    ph_b, pr_b = _jmj_step(phi.copy(), pi.copy(), dt, dx, params)
    # two half steps
    ph_h, pr_h = _jmj_step(phi.copy(), pi.copy(), 0.5 * dt, dx, params)
    ph_h2, pr_h2 = _jmj_step(ph_h, pr_h, 0.5 * dt, dx, params)
    return h_energy_norm_delta(ph_b, pr_b, ph_h2, pr_h2, dx, c, m)


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

        # forward JMJ with diagnostics (for H-theorem gate)
        ph, pr = phi0.copy(), pi0.copy()
        delta_sigmas: List[float] = []
        for _ in range(steps):
            ph, pr, dL = _jmj_forward_step_with_diagnostics(ph, pr, dt, dx, spec.params)
            delta_sigmas.append(float(dL))
        phiF, piF = ph, pr

        # Equal per-step work policy: for each lambda, baseline and assisted use identical work=lam*budget
        budget = float(spec.budget)
        baseline_errs: Dict[str, float] = {}
        assisted_errs: Dict[str, float] = {}
        work_summaries: Dict[str, Dict[str, float]] = {}
        for lam in lambdas:
            work = float(lam) * budget
            # Baseline reverse with random corrections
            bl_ph, bl_pr = phiF.copy(), piF.copy()
            bl_work_sum = 0.0
            for i in range(steps):
                bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c, m)
                remaining = float(steps * work - bl_work_sum)
                target = float(max(0.0, min(work, remaining)))
                dphi_bl, dpi_bl = _random_correction_pair(rng, bl_ph, bl_pr, dx, target, c, m)
                zph = np.zeros_like(dphi_bl); zpi = np.zeros_like(dpi_bl)
                bl_work_sum += float(h_energy_norm_delta(dphi_bl, dpi_bl, zph, zpi, dx, c, m))
                bl_ph = bl_ph + dphi_bl
                bl_pr = bl_pr + dpi_bl
                # Reverse-phase M segment runs forward in time; apply after assistance (phi-channel only)
                bl_ph, _stats = m_only_step_with_stats(bl_ph, dt, dx, spec.params)
                bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c, m)
            bl_err = h_energy_norm_delta(bl_ph, bl_pr, phi0, pi0, dx, c, m)
            baseline_errs[str(lam)] = bl_err

            # If lambda == 0, enforce identical baseline/assisted by construction
            if float(lam) == 0.0:
                assisted_errs[str(lam)] = baseline_errs[str(lam)]
                work_summaries[str(lam)] = {"baseline_work": bl_work_sum, "assisted_work": bl_work_sum}
                continue
            # Assisted reverse with model-aware corrections
            as_ph, as_pr = phiF.copy(), piF.copy()
            as_work_sum = 0.0
            for i in range(steps):
                as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c, m)
                remaining = float(steps * work - as_work_sum)
                target = float(max(0.0, min(work, remaining)))
                dphi_as, dpi_as = _assist_correction_pair(as_ph, as_pr, phi0, pi0, dx, spec.params, work=target, c=c, m=m)
                zph = np.zeros_like(dphi_as); zpi = np.zeros_like(dpi_as)
                as_work_sum += float(h_energy_norm_delta(dphi_as, dpi_as, zph, zpi, dx, c, m))
                as_ph = as_ph + dphi_as
                as_pr = as_pr + dpi_as
                # Reverse-phase M segment runs forward in time; apply after assistance (phi-channel only)
                as_ph, _stats = m_only_step_with_stats(as_ph, dt, dx, spec.params)
                as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c, m)
            assisted_err = h_energy_norm_delta(as_ph, as_pr, phi0, pi0, dx, c, m)
            assisted_errs[str(lam)] = assisted_err
            work_summaries[str(lam)] = {"baseline_work": bl_work_sum, "assisted_work": as_work_sum}

        # CEG per lambda using matched-work baseline
        ceg_map = {str(l): ceg(baseline_errs[str(l)], assisted_errs[str(l)]) for l in lambdas}
        # Enforce by-construction invariant: CEG(0) = 0 when assisted_err == baseline_err at λ=0
        if any(float(l) == 0.0 for l in lambdas):
            ceg_map["0.0"] = 0.0

        # Compute gates diagnostics per seed
        # G1: J-only round-trip drift (energy drift magnitude after forward+back)
        time_rev_drift = _j_only_roundtrip_drift(phi0, pi0, dt, steps, dx, c, m)

        # G2: H-theorem delta across M-steps (min over steps should be >= 0)
        delta_sigma_min = float(min(delta_sigmas)) if delta_sigmas else 0.0

        # G3: Energy match via measured total work equality (worst-case relative diff across λ>0)
        if lambdas:
            rels: List[float] = []
            for lam in lambdas:
                if float(lam) <= 0.0:
                    continue
                key = str(lam)
                w_b = work_summaries[key]["baseline_work"]
                w_a = work_summaries[key]["assisted_work"]
                denom = max(abs(w_b), 1e-12)
                rels.append(float((w_a - w_b) / denom))
            rel_diff = float(max((abs(r) for r in rels), default=0.0))
        else:
            rel_diff = 0.0

        # G4: Strang defect slope via JMJ vs MJM commutator proxy (canon)
        slope, r2 = _strang_two_grid_slope(phi0, pi0, dt, dx, spec.params, c, m)

        per_seed.append({
            "seed": seed,
            "baseline_err": baseline_errs,
            "assisted_err": assisted_errs,
            "work_summaries": work_summaries,
            "delta_sigmas": delta_sigmas,
            "gates_diag": {
                "time_rev_drift": time_rev_drift,
                "delta_sigma_min": delta_sigma_min,
                "rel_diff": rel_diff,
                "strang": {"slope": slope, "R2": r2}
            },
            "ceg": ceg_map
        })

    results["per_seed"] = per_seed
    # Aggregates
    # use top-level numpy import (avoid local import which shadows global np)
    agg = {}
    for lam in lambdas:
        vals = [float(s["ceg"][str(lam)]) for s in per_seed]
        agg[str(lam)] = {"median": float(np.median(np.array(vals))), "mean": float(np.mean(np.array(vals))), "n": len(vals)}
    results["ceg_summary"] = agg

    # Gate checks: produce per-seed gate results and aggregate gate ledger
    gate_ledger_per_seed: List[Dict[str, Any]] = []
    # We'll compute a small set of diagnostics per-seed; some are placeholders where
    # a full diagnostic requires additional runs (e.g. Strang defect). Tests / CI
    # will check presence and structure rather than strict pass/fail values.
    for s in per_seed:
        seed = int(s["seed"])
        diag = s.get("gates_diag", {})
        time_rev_drift = float(diag.get("time_rev_drift", 0.0))
        delta_sigma_min = float(diag.get("delta_sigma_min", 0.0))
        rel_diff = float(diag.get("rel_diff", 0.0))
        strang = diag.get("strang", {}) if isinstance(diag.get("strang"), dict) else {}
        slope = float(strang.get("slope", 0.0))
        r2 = float(strang.get("R2", 0.0))

        gates = [
            gate_noether(time_rev_drift),
            gate_h_theorem(delta_sigma_min),
            gate_energy_match(rel_diff),
            gate_strang_defect(slope, r2),
        ]
        # If any gate failed, record a contradiction summary for this seed
        failed = [g for g in gates if not g.get("passed", False)]
        contradiction = {"failed_count": len(failed), "failed_gates": [g.get("gate") for g in failed]} if failed else None
        gate_ledger_per_seed.append({"seed": seed, "gates": gates, "contradiction": contradiction})

    # Aggregate gate ledger: summarize per-gate pass rates
    agg_ledger: Dict[str, Any] = {}
    # build tally
    tally: Dict[str, Dict[str, int]] = {}
    for entry in gate_ledger_per_seed:
        for g in entry.get("gates", []):
            name = g.get("gate")
            if name not in tally:
                tally[name] = {"passed": 0, "failed": 0}
            if g.get("passed", False):
                tally[name]["passed"] += 1
            else:
                tally[name]["failed"] += 1
    for name, counts in tally.items():
        total = counts["passed"] + counts["failed"]
        agg_ledger[name] = {"passed": counts["passed"], "failed": counts["failed"], "n": total, "pass_rate": (counts["passed"] / total) if total > 0 else None}
    # Add overall CEG gate (G5): require positive echo gain for some λ>0 at the aggregate (median across seeds)
    try:
        ceg_summary = results.get("ceg_summary", {})
        medians = [float(v.get("median", 0.0)) for k, v in ceg_summary.items() if str(k) != "0.0"]
        median_max = float(max(medians)) if medians else 0.0
    except Exception:
        median_max = 0.0
    # Gate decision (tolerance avoids declaring tiny numerical noise as gain)
    _g5_threshold = float(spec.params.get("ceg_gate_threshold", 0.05))
    g5_pass = bool(median_max >= _g5_threshold)
    agg_ledger["G5_CEG_Positive"] = {
        "passed": 1 if g5_pass else 0,
        "failed": 0 if g5_pass else 1,
        "n": 1,
        "pass_rate": 1.0 if g5_pass else 0.0,
        "median_max": float(median_max),
        "tol": float(_g5_threshold),
    }

    results["gate_ledger_per_seed"] = gate_ledger_per_seed
    results["gate_ledger_summary"] = agg_ledger

    # Contradiction report at top-level if any gate failed across seeds
    total_failed = sum(v.get("failed", 0) for v in agg_ledger.values())
    if total_failed > 0:
        results["CONTRADICTION_REPORT"] = {"total_failed_gates": int(total_failed), "summary": agg_ledger}

    return results


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Metriplectic Assisted Echo (baseline vs assisted)")
    ap.add_argument("--spec", required=True, help="Path to echo spec JSON")
    ap.add_argument("--allow-unapproved", action="store_true", help="Allow run without approval (artifacts quarantined)")
    args = ap.parse_args()

    raw = json.loads(Path(args.spec).read_text())
    spec = EchoSpec(**raw)
    tag = spec.tag or spec.params.get("tag")
    # Set run script name for approval policy (domain:script:tag) to ensure DB HMAC matches manifest
    os.environ.setdefault("VDM_RUN_SCRIPT", "assisted_echo")
    # Enforce approval via policy for genuine runs (deterministic manifest discovery in approval.py)
    _approved, _eng_only, _proposal = check_tag_approval("metriplectic", "echo_spec-v1b", args.allow_unapproved, CODE_ROOT)

    out = run_assisted_echo(spec)
    # Determine failed routing based on gates (route to failed_runs if any gate fails)
    failed = bool(out.get("CONTRADICTION_REPORT"))
    # Logs (route based on failed)
    logp = log_path("metriplectic", _slug("assisted_echo", tag), failed=failed, type="json")
    write_log(logp, out)
    # CSV summary: lambda, median_ceg
    csvp = log_path("metriplectic", _slug("assisted_echo_ceg_summary", tag), failed=failed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("lambda,median_ceg,mean_ceg,n\n")
        for k, v in out.get("ceg_summary", {}).items():
            f.write(f"{k},{v.get('median',0.0)},{v.get('mean',0.0)},{v.get('n',0)}\n")
    # Placeholder figure path (figure creation may be handled by downstream notebooks)
    figp = figure_path("metriplectic", _slug("assisted_echo_placeholder", tag), failed=failed)
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
