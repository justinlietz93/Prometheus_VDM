#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Self-contained CEG Metriplectic Assisted-Echo experiment.

Adapted from Derivation/code/physics/metriplectic/assisted_echo.py with all
repo-internal imports replaced by local package imports so this directory can
be used standalone.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np

from .kg_ops import kg_verlet_step, spectral_grad
from .kg_noether import stiffness
from .compose import m_only_step_with_stats, lyapunov_values_consistent
from .echo_metrics import h_energy_norm_delta, ceg
from .echo_gates import gate_noether, gate_h_theorem, gate_energy_match, gate_strang_defect


@dataclass
class CegSpec:
    """Specification for a CEG assisted-echo run."""
    grid: Dict[str, Any]       # {N, dx}
    params: Dict[str, Any]     # {c, m, D, r, u, m_lap_operator, ...}
    dt: float
    steps: int
    seeds: List[int]
    lambdas: List[float]
    budget: float              # energy budget per step (H-norm)
    tag: str | None = None


def _lam_key(lam: float) -> str:
    return f"{float(lam):.12g}"


def _jmj_step(
    phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]
) -> Tuple[np.ndarray, np.ndarray]:
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    phi1, pi1 = kg_verlet_step(phi, pi, 0.5 * dt, dx, c, m)
    phi2, _ = m_only_step_with_stats(phi1, dt, dx, params)
    phi3, pi3 = kg_verlet_step(phi2, pi1, 0.5 * dt, dx, c, m)
    return phi3, pi3


def _mjm_step(
    phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]
) -> Tuple[np.ndarray, np.ndarray]:
    phi1, _ = m_only_step_with_stats(phi, 0.5 * dt, dx, params)
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    phi2, pi2 = kg_verlet_step(phi1, pi, dt, dx, c, m)
    phi3, _ = m_only_step_with_stats(phi2, 0.5 * dt, dx, params)
    return phi3, pi2


def _strang_defect(
    phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any], c: float, m: float
) -> float:
    a_phi, a_pi = _jmj_step(phi.copy(), pi.copy(), dt, dx, params)
    b_phi, b_pi = _mjm_step(phi.copy(), pi.copy(), dt, dx, params)
    return h_energy_norm_delta(a_phi, a_pi, b_phi, b_pi, dx, c, m)


def _strang_two_grid_slope(
    phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any], c: float, m: float
) -> Tuple[float, float]:
    dts = [float(dt), 0.5 * float(dt), 0.25 * float(dt), 0.125 * float(dt)]
    z = np.zeros_like(phi)
    H0 = float(h_energy_norm_delta(phi, pi, z, z, dx, c, m))
    es: List[float] = []
    hs: List[float] = []
    for d in dts:
        if d <= 0.0:
            continue
        e = _strang_defect(phi, pi, d, dx, params, c, m)
        if e <= 0.0 or not np.isfinite(e):
            continue
        es.append(float(e))
        hs.append(float(d))
    if len(es) > 0:
        rel_floor = 1e-12 * max(H0, 1.0)
        if all(v < rel_floor for v in es):
            return 3.0, 1.0
    if len(es) >= 3:
        x = np.log(np.array(hs, dtype=float))
        y = np.log(np.array(es, dtype=float))
        A = np.vstack([x, np.ones_like(x)]).T
        s, b = np.linalg.lstsq(A, y, rcond=None)[0]
        y_pred = A @ np.array([s, b])
        ss_res = float(np.sum((y - y_pred) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
        return float(s), float(R2)
    elif len(es) == 2 and es[0] > 0.0 and es[1] > 0.0:
        s = float(np.log(es[0] / es[1]) / np.log(hs[0] / hs[1]))
        return s, 1.0
    return 0.0, 0.0


def _j_only_roundtrip_drift(
    phi: np.ndarray, pi: np.ndarray, dt: float, steps: int, dx: float, c: float, m: float
) -> float:
    ph, pr = phi.copy(), pi.copy()
    ph, pr = kg_verlet_step(ph, pr, dt, dx, c, m)
    ph, pr = kg_verlet_step(ph, pr, -dt, dx, c, m)
    return h_energy_norm_delta(ph, pr, phi, pi, dx, c, m)


def _assist_correction_pair(
    phi: np.ndarray, pi: np.ndarray, phi_ref: np.ndarray, pi_ref: np.ndarray,
    dx: float, params: Dict[str, Any], work: float, c: float, m: float
) -> Tuple[np.ndarray, np.ndarray]:
    if work <= 0:
        return np.zeros_like(phi), np.zeros_like(pi)
    dphi = (phi - phi_ref).astype(float)
    dpi = (pi - pi_ref).astype(float)
    dir_phi = -stiffness(dphi, dx, c, m)
    dir_pi = -dpi
    if np.allclose(dir_phi, 0.0) and np.allclose(dir_pi, 0.0):
        return np.zeros_like(phi), np.zeros_like(pi)

    def _h_norm(vphi: np.ndarray, vpi: np.ndarray) -> float:
        z = np.zeros_like(vphi)
        return h_energy_norm_delta(vphi, vpi, z, z, dx, c, m)

    size = _h_norm(dir_phi, dir_pi)
    if size == 0.0:
        return np.zeros_like(phi), np.zeros_like(pi)
    scale = float(work / size)
    return scale * dir_phi.astype(float), scale * dir_pi.astype(float)


def _random_correction_pair(
    rng: np.random.Generator, phi: np.ndarray, pi: np.ndarray,
    dx: float, work: float, c: float, m: float
) -> Tuple[np.ndarray, np.ndarray]:
    if work <= 0:
        return np.zeros_like(phi), np.zeros_like(pi)
    vphi = rng.standard_normal(phi.shape).astype(float)
    vpi = rng.standard_normal(pi.shape).astype(float)

    def _h_norm(vph: np.ndarray, vpp: np.ndarray) -> float:
        z = np.zeros_like(vph)
        return h_energy_norm_delta(vph, vpp, z, z, dx, c, m)

    size = _h_norm(vphi, vpi)
    if size == 0.0:
        return np.zeros_like(phi), np.zeros_like(pi)
    scale = float(work / size)
    return scale * vphi, scale * vpi


def _h_energy_components(
    dphi: np.ndarray, dpi: np.ndarray, dx: float, c: float, m: float
) -> Tuple[float, float, float]:
    dphi = dphi.astype(float)
    dpi = dpi.astype(float)
    g = spectral_grad(dphi, dx)
    e_pi = float(np.sum(dpi * dpi) * dx)
    e_phi = float(np.sum((c * c) * (g * g) + (m * m) * (dphi * dphi)) * dx)
    e_tot = e_phi + e_pi
    return float(np.sqrt(max(e_tot, 0.0))), e_phi, e_pi


def _jmj_forward_step_with_diagnostics(
    phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, params: Dict[str, Any]
) -> Tuple[np.ndarray, np.ndarray, float]:
    c = float(params.get("c", 1.0))
    m = float(params.get("m", 0.0))
    D = float(params.get("D", 1.0))
    r = float(params.get("r", 0.0))
    u = float(params.get("u", 0.0))
    lap_mode = str(params.get("m_lap_operator", "stencil"))
    phi1, pi1 = kg_verlet_step(phi, pi, 0.5 * dt, dx, c, m)
    L_before = lyapunov_values_consistent(phi1, dx, D, r, u, lap_operator=lap_mode)
    phi2, _ = m_only_step_with_stats(phi1, dt, dx, params)
    L_after = lyapunov_values_consistent(phi2, dx, D, r, u, lap_operator=lap_mode)
    phi3, pi3 = kg_verlet_step(phi2, pi1, 0.5 * dt, dx, c, m)
    delta_sigma = -(L_after - L_before)
    return phi3, pi3, float(delta_sigma)


def run_ceg(spec: CegSpec) -> Dict[str, Any]:
    """Run the CEG assisted-echo experiment and return structured results.

    Parameters
    ----------
    spec : CegSpec
        Experiment specification.

    Returns
    -------
    dict
        Keys: ``ceg_summary``, ``gate_ledger_summary``, ``gate_ledger_per_seed``,
        ``per_seed``, ``seeds``, ``lambdas``, ``grid``, ``params``, ``dt``, ``steps``.
    """
    N = int(spec.grid["N"])
    dx = float(spec.grid["dx"])
    dt = float(spec.dt)
    c = float(spec.params.get("c", 1.0))
    m = float(spec.params.get("m", 0.0))
    seeds = [int(s) for s in spec.seeds]
    lambdas = [float(l) for l in spec.lambdas]
    steps = int(spec.steps)

    assist_mode = str(spec.params.get("assist_mode", "model_aware")).lower()
    reverse_order = str(spec.params.get("reverse_order", "JMJ")).upper()
    j_scramble_factor = float(spec.params.get("j_scramble_factor", 1.0))
    m_scramble_factor = float(spec.params.get("m_scramble_factor", 1.0))

    results: Dict[str, Any] = {
        "seeds": seeds, "lambdas": lambdas,
        "grid": spec.grid, "params": spec.params,
        "dt": dt, "steps": steps,
    }
    per_seed: List[Dict[str, Any]] = []
    telemetry_rows: List[Dict[str, Any]] = []

    for seed in seeds:
        rng = np.random.default_rng(seed)
        phi0 = rng.random(N).astype(float) * 0.1
        pi0 = rng.random(N).astype(float) * 0.1

        # Forward JMJ with diagnostics
        ph, pr = phi0.copy(), pi0.copy()
        delta_sigmas: List[float] = []
        for _ in range(steps):
            ph, pr, dL = _jmj_forward_step_with_diagnostics(ph, pr, dt, dx, spec.params)
            delta_sigmas.append(float(dL))
        phiF, piF = ph, pr

        # Gate pre-checks
        _eps = float(np.finfo(float).eps)
        _z = np.zeros_like(phi0)
        h0 = float(h_energy_norm_delta(phi0, pi0, _z, _z, dx, c, m))
        _sqrtN = float(np.sqrt(N))
        _tol = float(max(1e-12 * _sqrtN, 10.0 * _eps * _sqrtN * max(h0, 1.0)))
        time_rev_drift = _j_only_roundtrip_drift(phi0, pi0, dt, steps, dx, c, m)
        slope, r2 = _strang_two_grid_slope(phi0, pi0, dt, dx, spec.params, c, m)

        budget = float(spec.budget)
        baseline_errs: Dict[str, float] = {}
        assisted_errs: Dict[str, float] = {}
        work_summaries: Dict[str, Dict[str, float]] = {}

        for lam in lambdas:
            work = float(lam) * budget
            lam_key = _lam_key(lam)
            step_targets = [work] * steps

            c_rev = float(c * j_scramble_factor)
            m_params_rev = dict(spec.params)
            m_params_rev["D"] = float(spec.params.get("D", 1.0)) * m_scramble_factor

            # Baseline: random corrections
            bl_ph, bl_pr = phiF.copy(), piF.copy()
            bl_work_sum = 0.0
            bl_work_comp = 0.0
            for i in range(steps):
                target = float(step_targets[i])
                bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c_rev, m)
                dphi_bl, dpi_bl = _random_correction_pair(rng, bl_ph, bl_pr, dx, target, c_rev, m)
                z_ = np.zeros_like(dphi_bl)
                _bl_delta = float(h_energy_norm_delta(dphi_bl, dpi_bl, z_, z_, dx, c_rev, m))
                _y = _bl_delta - bl_work_comp
                _t = bl_work_sum + _y
                bl_work_comp = (_t - bl_work_sum) - _y
                bl_work_sum = _t
                bl_ph = bl_ph + dphi_bl
                bl_pr = bl_pr + dpi_bl
                bl_ph, _stats = m_only_step_with_stats(bl_ph, dt, dx, m_params_rev)
                bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c_rev, m)
                _bl_err_step = h_energy_norm_delta(bl_ph, bl_pr, phi0, pi0, dx, c, m)
                telemetry_rows.append({
                    "seed": seed, "lambda": float(lam), "step": int(i + 1), "mode": "baseline",
                    "err_to_ref": float(_bl_err_step), "cum_work": float(bl_work_sum),
                })
            bl_err = h_energy_norm_delta(bl_ph, bl_pr, phi0, pi0, dx, c, m)
            baseline_errs[lam_key] = bl_err

            if float(lam) == 0.0:
                assisted_errs[lam_key] = bl_err
                work_summaries[lam_key] = {"baseline_work": bl_work_sum, "assisted_work": bl_work_sum}
                continue

            # Assisted: model-aware corrections
            as_ph, as_pr = phiF.copy(), piF.copy()
            as_work_sum = 0.0
            as_work_comp = 0.0

            def _assist_pair(
                curr_phi: np.ndarray, curr_pi: np.ndarray, targ: float
            ) -> Tuple[np.ndarray, np.ndarray]:
                if assist_mode == "model_blind":
                    return _random_correction_pair(rng, curr_phi, curr_pi, dx, targ, c_rev, m)
                return _assist_correction_pair(
                    curr_phi, curr_pi, phi0, pi0, dx, spec.params, work=targ, c=c_rev, m=m
                )

            for i in range(steps):
                target = float(step_targets[i])
                as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c_rev, m)
                dphi_as, dpi_as = _assist_pair(as_ph, as_pr, target)
                z_ = np.zeros_like(dphi_as)
                _as_delta = float(h_energy_norm_delta(dphi_as, dpi_as, z_, z_, dx, c_rev, m))
                _y = _as_delta - as_work_comp
                _t = as_work_sum + _y
                as_work_comp = (_t - as_work_sum) - _y
                as_work_sum = _t
                as_ph = as_ph + dphi_as
                as_pr = as_pr + dpi_as
                as_ph, _stats = m_only_step_with_stats(as_ph, dt, dx, m_params_rev)
                as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c_rev, m)
                _as_err_step = h_energy_norm_delta(as_ph, as_pr, phi0, pi0, dx, c, m)
                telemetry_rows.append({
                    "seed": seed, "lambda": float(lam), "step": int(i + 1), "mode": "assisted",
                    "err_to_ref": float(_as_err_step), "cum_work": float(as_work_sum),
                })

            as_err = h_energy_norm_delta(as_ph, as_pr, phi0, pi0, dx, c, m)
            assisted_errs[lam_key] = as_err
            work_summaries[lam_key] = {"baseline_work": bl_work_sum, "assisted_work": as_work_sum}

        # Per-seed CEG
        ceg_map: Dict[str, float] = {}
        for l in lambdas:
            k = _lam_key(l)
            if k in baseline_errs and k in assisted_errs:
                ceg_map[k] = ceg(baseline_errs[k], assisted_errs[k])
        if any(float(l) == 0.0 for l in lambdas):
            ceg_map[_lam_key(0.0)] = 0.0

        # Energy match
        rels: List[float] = []
        for lam in lambdas:
            if float(lam) <= 0.0:
                continue
            ws = work_summaries.get(_lam_key(lam))
            if not ws:
                continue
            w_b = float(ws.get("baseline_work", 0.0))
            w_a = float(ws.get("assisted_work", 0.0))
            rels.append(float((w_a - w_b) / max(abs(w_b), 1e-12)))
        rel_diff = float(max((abs(r) for r in rels), default=0.0))

        per_seed.append({
            "seed": seed,
            "baseline_err": baseline_errs,
            "assisted_err": assisted_errs,
            "work_summaries": work_summaries,
            "delta_sigmas": delta_sigmas,
            "gates_diag": {
                "time_rev_drift": time_rev_drift,
                "delta_sigma_min": float(min(delta_sigmas)) if delta_sigmas else 0.0,
                "rel_diff": rel_diff,
                "h0": float(h0),
                "strang": {"slope": slope, "R2": r2},
            },
            "ceg": ceg_map,
        })

    results["per_seed"] = per_seed

    # Aggregate CEG summary
    agg: Dict[str, Any] = {}
    for lam in lambdas:
        vals: List[float] = []
        k = _lam_key(lam)
        for s in per_seed:
            v = s.get("ceg", {}).get(k)
            if v is None:
                continue
            try:
                vals.append(float(v))
            except Exception:
                continue
        if not vals:
            agg[k] = {"median": 0.0, "mean": 0.0, "n": 0}
        else:
            arr = np.array(vals, dtype=float)
            agg[k] = {"median": float(np.median(arr)), "mean": float(np.mean(arr)), "n": int(arr.size)}
    results["ceg_summary"] = agg
    results["telemetry_rows"] = telemetry_rows

    # Gate ledger per seed
    gate_ledger_per_seed: List[Dict[str, Any]] = []
    for s in per_seed:
        seed = int(s["seed"])
        diag = s.get("gates_diag", {})
        _tr_drift = float(diag.get("time_rev_drift", 0.0))
        _ds_min = float(diag.get("delta_sigma_min", 0.0))
        _rel = float(diag.get("rel_diff", 0.0))
        _strang = diag.get("strang", {})
        _slope = float(_strang.get("slope", 0.0))
        _r2 = float(_strang.get("R2", 0.0))
        _eps_local = float(np.finfo(float).eps)
        _h0_diag = float(diag.get("h0", 1.0))
        _sqrtN_l = float(np.sqrt(N))
        _g1_tol = float(max(1e-12 * _sqrtN_l, 10.0 * _eps_local * _sqrtN_l * max(_h0_diag, 1.0)))
        gates = [
            gate_noether(_tr_drift, tol=_g1_tol),
            gate_h_theorem(_ds_min, tol=_g1_tol),
            gate_energy_match(_rel),
            gate_strang_defect(_slope, _r2),
        ]
        failed = [g for g in gates if not g.get("passed", False)]
        contradiction = {"failed_count": len(failed), "failed_gates": [g.get("gate") for g in failed]} if failed else None
        gate_ledger_per_seed.append({"seed": seed, "gates": gates, "contradiction": contradiction})

    # Aggregate gate ledger
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
    min_gate_pass_rate = float(spec.params.get("min_gate_pass_rate", 0.8333333333333334))
    agg_ledger: Dict[str, Any] = {}
    for name, counts in tally.items():
        total = counts["passed"] + counts["failed"]
        pr = (counts["passed"] / total) if total > 0 else None
        meets_rate = (pr is not None) and (pr >= min_gate_pass_rate)
        agg_ledger[name] = {
            "passed": counts["passed"], "failed": counts["failed"],
            "n": total, "pass_rate": pr,
            "min_pass_rate": min_gate_pass_rate, "meets_rate": bool(meets_rate),
        }

    # G5: CEG threshold
    try:
        medians = [float(v.get("median", 0.0)) for k, v in agg.items() if float(k) > 0.0]
        median_max = float(max(medians)) if medians else 0.0
    except Exception:
        median_max = 0.0
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

    total_failed = sum(
        1 for k, v in agg_ledger.items()
        if k != "G5_CEG_Positive"
        and v.get("pass_rate") is not None
        and float(v.get("pass_rate")) < min_gate_pass_rate
    )
    if total_failed > 0:
        results["CONTRADICTION_REPORT"] = {"total_failed_gates": int(total_failed), "summary": agg_ledger}

    return results


__all__ = ["CegSpec", "run_ceg"]
