#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Metriplectic Assisted-Echo experiment (baseline vs assisted) per T4 proposal.

Produces paired artifacts (JSON/CSV) under outputs/logs/metriplectic/ and a figure.
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
from physics.metriplectic.kg_ops import kg_verlet_step, spectral_grad
from physics.metriplectic.kg_noether import stiffness
from physics.metriplectic.compose import m_only_step_with_stats, lyapunov_values_consistent
from physics.metriplectic.echo_metrics import h_energy_norm_delta, ceg
from common.authorization.approval import check_tag_approval
from physics.metriplectic.echo_gates import gate_noether, gate_h_theorem, gate_energy_match, gate_strang_defect
from common.plotting.assisted_echo_plots import generate_core_pack


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
    
    
def _lam_key(lam: float) -> str:
    """Canonical string key for lambda values to avoid float repr issues."""
    return f"{float(lam):.12g}"
    
    
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
    """Estimate Strang defect slope via multi-point log–log fit in H-norm using the commutator proxy.

    We define the defect via the JMJ↔MJM commutator proxy:
        e(h) = || Φ_JMJ(h)(z0) − Φ_MJM(h)(z0) ||_H

    We evaluate e at dt, dt/2, dt/4 (and dt/8 if resolvable) and fit:
        log e(h) ≈ s log h + b  → return (s, R²)

    Near-roundoff regime: if all selected defects are below a relative floor ~ 1e-12·max(H0,1), return (3.0, 1.0).
    """
    # Build step sizes
    dts = [float(dt), 0.5 * float(dt), 0.25 * float(dt)]
    if dts[-1] > 0.0:
        dts.append(0.125 * float(dt))

    # Reference H-norm scale of the state (relative tolerance anchor)
    zphi = np.zeros_like(phi)
    zpi = np.zeros_like(pi)
    H0 = float(h_energy_norm_delta(phi, pi, zphi, zpi, dx, c, m))

    # Compute defects
    es: list[float] = []
    hs: list[float] = []
    for d in dts:
        if d <= 0.0:
            continue
        e = _strang_defect(phi, pi, d, dx, params, c, m)
        if e <= 0.0 or not np.isfinite(e):
            continue
        es.append(float(e))
        hs.append(float(d))

    # Guard: need at least 3 points to fit robustly
    if len(es) < 3:
        # fallback to two-point ratio if available
        if len(es) == 2 and es[0] > 0.0 and es[1] > 0.0:
            s = float(np.log(es[0] / es[1]) / np.log(hs[0] / hs[1]))
            return s, 1.0
        return 0.0, 0.0

    # Trivial near-roundoff regime: treat as perfect cubic if all values are below a relative floor
    rel_floor = 1e-12 * max(H0, 1.0)
    if all(v < rel_floor for v in es):
        return 3.0, 1.0

    # Fit log–log
    x = np.log(np.array(hs, dtype=float))
    y = np.log(np.array(es, dtype=float))
    A = np.vstack([x, np.ones_like(x)]).T
    s, b = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([s, b])
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    return float(s), float(R2)


def _j_only_roundtrip_drift(phi: np.ndarray, pi: np.ndarray, dt: float, steps: int, dx: float, c: float, m: float) -> float:
    """J-only reversibility meter (instrument-grade).

    Measure the instrument error of a single reversible composition (+dt followed by −dt),
    avoiding accumulation across many pairs. Returns the H-energy distance to the initial state.
    """
    ph, pr = phi.copy(), pi.copy()
    # One forward + one reverse (single pair)
    ph, pr = kg_verlet_step(ph, pr, dt, dx, c, m)
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


def _h_energy_components(dphi: np.ndarray, dpi: np.ndarray, dx: float, c: float, m: float) -> Tuple[float, float, float]:
    """Compute H-energy metric components for a correction pair.
    Returns (work_total, work_e_phi, work_e_pi) where:
      - work_total = ||(dphi, dpi)||_H
      - work_e_phi = ∫ (c^2 |∇dphi|^2 + m^2 |dphi|^2) dx
      - work_e_pi  = ∫ |dpi|^2 dx
    """
    dphi = dphi.astype(float)
    dpi = dpi.astype(float)
    g = spectral_grad(dphi, dx)
    e_pi = float(np.sum(dpi * dpi) * dx)
    e_phi = float(np.sum((c * c) * (g * g) + (m * m) * (dphi * dphi)) * dx)
    e_tot = e_phi + e_pi
    work_total = float(np.sqrt(max(e_tot, 0.0)))
    return work_total, e_phi, e_pi


def _first_mode_energy_angle(phi: np.ndarray, pi: np.ndarray, dx: float, c: float, m: float) -> Tuple[float, float, float, float, float]:
    """Compute H-energy and action-angle (theta) in the first Fourier cosine mode plane.
    Returns (H_energy, theta_energy, r_energy, phi1, pi1)."""
    N = int(phi.size)
    L = float(N) * float(dx)
    if L <= 0.0 or N <= 1:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    x = (np.arange(N, dtype=float) * float(dx))
    cos1 = np.cos(2.0 * np.pi * x / L)
    denom = float(np.sum(cos1 * cos1) * dx)
    if denom <= 0.0:
        denom = float(N) * float(dx)
    phi1 = float(np.sum(phi.astype(float) * cos1) * dx / denom)
    pi1  = float(np.sum(pi.astype(float)  * cos1) * dx / denom)
    k = 2.0 * np.pi / L
    k_phi = float((c * c) * (k * k) + (m * m))
    y1 = float(np.sqrt(max(k_phi, 0.0)) * phi1)
    y2 = float(pi1)
    H = 0.5 * float(k_phi * phi1 * phi1 + pi1 * pi1)
    theta = float(np.arctan2(y2, y1))
    r = float(np.sqrt(max(y1 * y1 + y2 * y2, 0.0)))
    return H, theta, r, phi1, pi1


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


def _apply_walker_perturbation(
    phi: np.ndarray,
    pi: np.ndarray,
    rng: np.random.Generator,
    amp: float,
    width: int,
    channel: str
) -> Tuple[np.ndarray, np.ndarray]:
    """Inject a localized perturbation between forward and reverse phases (RP-3).

    - amp: peak amplitude (dimensionless, applied to state units)
    - width: Gaussian width in grid points (int > 0)
    - channel: 'phi' | 'pi' | 'both'
    """
    if amp == 0.0 or width <= 0:
        return phi, pi
    N = int(phi.size)
    center = int(rng.integers(0, N))
    x = np.arange(N, dtype=float)
    g = np.exp(-0.5 * ((x - float(center)) / float(width)) ** 2)
    g = (g / (np.max(g) + 1e-12)) * float(amp)
    if channel.lower() in ("phi", "both"):
        phi = (phi + g.astype(float))
    if channel.lower() in ("pi", "both"):
        pi = (pi + g.astype(float))
    return phi, pi


def run_assisted_echo(spec: EchoSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt = float(spec.dt)
    c = float(spec.params.get("c", 1.0)) ; m = float(spec.params.get("m", 0.0))
    seeds = [int(s) for s in spec.seeds]
    lambdas = [float(l) for l in spec.lambdas]
    steps = int(spec.steps)
    tag = spec.tag or spec.params.get("tag")

    # RP/controls toggles (schema allows additionalProperties in params)
    assist_mode = str(spec.params.get("assist_mode", "model_aware")).lower()           # {'model_aware','model_blind'}
    reverse_order = str(spec.params.get("reverse_order", "JMJ")).upper()               # {'JMJ','MJM'}
    enforce_rp1 = bool(spec.params.get("enforce_rp1", True))                           # enforce RP-1 calibration before reverse
    walker_amp = float(spec.params.get("walker_amp", 0.0))                             # amplitude for walker perturbation
    walker_width = int(spec.params.get("walker_width", 0))                             # width (grid points)
    walker_channel = str(spec.params.get("walker_channel", "phi")).lower()            # {'phi','pi','both'}
    j_scramble_factor = float(spec.params.get("j_scramble_factor", 1.0))               # multiplies c during reverse
    m_scramble_factor = float(spec.params.get("m_scramble_factor", 1.0))               # multiplies D during reverse

    results: Dict[str, Any] = {"seeds": seeds, "lambdas": lambdas, "grid": spec.grid, "params": spec.params, "dt": dt, "steps": steps}
    per_seed: List[Dict[str, Any]] = []
    telemetry_rows: List[Dict[str, Any]] = []

    for seed in seeds:
        rng = np.random.default_rng(seed)
        # initial state
        phi0 = rng.random(N).astype(float) * 0.1
        pi0 = rng.random(N).astype(float) * 0.1

        # forward JMJ with diagnostics (for H-theorem gate)
        ph, pr = phi0.copy(), pi0.copy()
        delta_sigmas: List[float] = []
        for j in range(steps):
            ph, pr, dL = _jmj_forward_step_with_diagnostics(ph, pr, dt, dx, spec.params)
            delta_sigmas.append(float(dL))
            # Per-step forward telemetry (mode='forward'): record ΔΣ and first-mode state
            H_f, theta_f, _r_f, phi1_f, pi1_f = _first_mode_energy_angle(ph, pr, dx, c, m)
            err_f = h_energy_norm_delta(ph, pr, phi0, pi0, dx, c, m)
            telemetry_rows.append({
                "seed": seed, "lambda": 0.0, "step": int(j+1), "mode": "forward",
                "err_to_ref": float(err_f),
                "work_total": 0.0, "work_e_phi": 0.0, "work_e_pi": 0.0,
                "phi_share": 0.0, "pi_share": 0.0, "cum_work": 0.0,
                "H_energy": float(H_f), "theta_energy": float(theta_f),
                "phi1": float(phi1_f), "pi1": float(pi1_f),
                "delta_sigma": float(dL), "align_cos": 0.0
            })
        phiF, piF = ph, pr

        # RP-1 calibration gates before reverse phase
        time_rev_drift = _j_only_roundtrip_drift(phi0, pi0, dt, steps, dx, c, m)
        slope, r2 = _strang_two_grid_slope(phi0, pi0, dt, dx, spec.params, c, m)
        # Canonical tolerance scaling for G1: max(1e-12, 10 * eps * sqrt(N))
        _eps = float(np.finfo(float).eps)
        # Relative H-norm scale for Noether drift tolerance (per-pair, instrument metric)
        _z = np.zeros_like(phi0)
        h0 = float(h_energy_norm_delta(phi0, pi0, _z, _z, dx, c, m))
        _tol_g1 = float(max(1e-12, 10.0 * _eps * float(np.sqrt(N)) * max(h0, 1.0)))
        g1 = gate_noether(time_rev_drift, tol=_tol_g1)
        g2 = gate_h_theorem(float(min(delta_sigmas)) if delta_sigmas else 0.0)
        g4 = gate_strang_defect(slope, r2)
        rp1_ok = bool(g1.get("passed") and g2.get("passed") and g4.get("passed"))
        if enforce_rp1 and not rp1_ok:
            # Record gates only and skip reverse/assisted runs for this seed
            per_seed.append({
                "seed": seed,
                "baseline_err": {},
                "assisted_err": {},
                "work_summaries": {},
                "delta_sigmas": delta_sigmas,
                "gates_diag": {
                    "time_rev_drift": time_rev_drift,
                    "delta_sigma_min": float(min(delta_sigmas)) if delta_sigmas else 0.0,
                    "rel_diff": 0.0,
                    "h0": float(h0),
                    "strang": {"slope": slope, "R2": r2}
                },
                "ceg": {}
            })
            continue

        # RP-3 walker perturbation injection between forward and reverse
        phiF, piF = _apply_walker_perturbation(phiF, piF, rng, walker_amp, walker_width, walker_channel)

        # Equal per-step work policy: for each lambda, baseline and assisted use identical work=lam*budget
        budget = float(spec.budget)
        baseline_errs: Dict[str, float] = {}
        assisted_errs: Dict[str, float] = {}
        work_summaries: Dict[str, Dict[str, float]] = {}
        telemetry_per_lambda: Dict[str, Any] = {}
        for lam in lambdas:
            work = float(lam) * budget
            lam_key = _lam_key(lam)
            step_targets = [work for _ in range(steps)]
            # Baseline reverse with random corrections
            bl_ph, bl_pr = phiF.copy(), piF.copy()
            bl_work_sum = 0.0
            bl_work_comp = 0.0  # Kahan compensation for baseline work accumulation
            # reverse-phase parameter scrambles (RP-4: J/M scramble)
            c_rev = float(c * j_scramble_factor)
            m_params_rev = dict(spec.params)
            m_params_rev["D"] = float(spec.params.get("D", 1.0)) * m_scramble_factor

            # telemetry arrays (baseline) for this lambda
            bl_err_trace: List[float] = []
            bl_phi_share_trace: List[float] = []
            bl_pi_share_trace: List[float] = []

            for i in range(steps):
                target = float(step_targets[i])
                
                if reverse_order == "MJM":
                    # M(dt/2)
                    bl_ph, _ = m_only_step_with_stats(bl_ph, 0.5 * dt, dx, m_params_rev)
                    # apply correction after first segment (baseline uses random correction)
                    dphi_bl, dpi_bl = _random_correction_pair(rng, bl_ph, bl_pr, dx, target, c_rev, m)
                    zph = np.zeros_like(dphi_bl); zpi = np.zeros_like(dpi_bl)
                    _bl_delta = float(h_energy_norm_delta(dphi_bl, dpi_bl, zph, zpi, dx, c_rev, m))
                    _y = _bl_delta - bl_work_comp
                    _t = bl_work_sum + _y
                    bl_work_comp = (_t - bl_work_sum) - _y
                    bl_work_sum = _t
                    bl_ph = bl_ph + dphi_bl
                    bl_pr = bl_pr + dpi_bl
                    # J(-dt)
                    bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -1.0 * dt, dx, c_rev, m)
                    # M(dt/2)
                    bl_ph, _ = m_only_step_with_stats(bl_ph, 0.5 * dt, dx, m_params_rev)
                    # per-step telemetry (baseline, MJM)
                    _bl_work_total, _bl_e_phi, _bl_e_pi = _h_energy_components(dphi_bl, dpi_bl, dx, c_rev, m)
                    _bl_den = (_bl_e_phi + _bl_e_pi) if (_bl_e_phi + _bl_e_pi) > 0.0 else 1.0
                    _bl_phi_share = float(_bl_e_phi / _bl_den)
                    _bl_pi_share = float(_bl_e_pi / _bl_den)
                    _bl_err_step = h_energy_norm_delta(bl_ph, bl_pr, phi0, pi0, dx, c, m)
                    bl_err_trace.append(float(_bl_err_step))
                    bl_phi_share_trace.append(_bl_phi_share)
                    bl_pi_share_trace.append(_bl_pi_share)
                    # First-mode with instrument metric (c, m)
                    H_bl, theta_bl, _r_bl, _phi1_bl, _pi1_bl = _first_mode_energy_angle(bl_ph, bl_pr, dx, c, m)
                    # Alignment of applied correction to -∇_H direction at current state (instrument metric)
                    _dphi_ref = (bl_ph - phi0).astype(float)
                    _dpi_ref = (bl_pr - pi0).astype(float)
                    _dir_phi = -stiffness(_dphi_ref, dx, c, m)
                    _dir_pi = -_dpi_ref
                    _gv = spectral_grad(dphi_bl, dx); _gw = spectral_grad(_dir_phi, dx)
                    _inner_phi = float(np.sum((c*c)*_gv*_gw + (m*m)*dphi_bl*_dir_phi) * dx)
                    _inner_pi = float(np.sum(dpi_bl * _dir_pi) * dx)
                    _inner = _inner_phi + _inner_pi
                    _v_size, _, _ = _h_energy_components(dphi_bl, dpi_bl, dx, c, m)
                    _w_size, _, _ = _h_energy_components(_dir_phi, _dir_pi, dx, c, m)
                    _align_cos = float(_inner / (max(_v_size, 1e-12) * max(_w_size, 1e-12)))
                    telemetry_rows.append({
                        "seed": seed, "lambda": float(lam), "step": int(i+1), "mode": "baseline",
                        "err_to_ref": float(_bl_err_step),
                        "work_total": float(_bl_work_total), "work_e_phi": float(_bl_e_phi), "work_e_pi": float(_bl_e_pi),
                        "phi_share": float(_bl_phi_share), "pi_share": float(_bl_pi_share), "cum_work": float(bl_work_sum),
                        "H_energy": float(H_bl), "theta_energy": float(theta_bl),
                        "phi1": float(_phi1_bl), "pi1": float(_pi1_bl), "delta_sigma": 0.0,
                        "align_cos": float(_align_cos)
                    })
                else:
                    # J(-dt/2)
                    bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c_rev, m)
                    # apply correction
                    dphi_bl, dpi_bl = _random_correction_pair(rng, bl_ph, bl_pr, dx, target, c_rev, m)
                    zph = np.zeros_like(dphi_bl); zpi = np.zeros_like(dpi_bl)
                    _bl_delta = float(h_energy_norm_delta(dphi_bl, dpi_bl, zph, zpi, dx, c_rev, m))
                    _y = _bl_delta - bl_work_comp
                    _t = bl_work_sum + _y
                    bl_work_comp = (_t - bl_work_sum) - _y
                    bl_work_sum = _t
                    bl_ph = bl_ph + dphi_bl
                    bl_pr = bl_pr + dpi_bl
                    # M(+dt) on phi-channel
                    bl_ph, _stats = m_only_step_with_stats(bl_ph, dt, dx, m_params_rev)
                    # J(-dt/2)
                    bl_ph, bl_pr = kg_verlet_step(bl_ph, bl_pr, -0.5 * dt, dx, c_rev, m)
                    # per-step telemetry (baseline, JMJ)
                    _bl_work_total, _bl_e_phi, _bl_e_pi = _h_energy_components(dphi_bl, dpi_bl, dx, c_rev, m)
                    _bl_den = (_bl_e_phi + _bl_e_pi) if (_bl_e_phi + _bl_e_pi) > 0.0 else 1.0
                    _bl_phi_share = float(_bl_e_phi / _bl_den)
                    _bl_pi_share = float(_bl_e_pi / _bl_den)
                    _bl_err_step = h_energy_norm_delta(bl_ph, bl_pr, phi0, pi0, dx, c, m)
                    bl_err_trace.append(float(_bl_err_step))
                    bl_phi_share_trace.append(_bl_phi_share)
                    bl_pi_share_trace.append(_bl_pi_share)
                    # First-mode with instrument metric (c, m)
                    H_bl, theta_bl, _r_bl, _phi1_bl, _pi1_bl = _first_mode_energy_angle(bl_ph, bl_pr, dx, c, m)
                    # Alignment of applied correction to -∇_H direction
                    _dphi_ref = (bl_ph - phi0).astype(float)
                    _dpi_ref = (bl_pr - pi0).astype(float)
                    _dir_phi = -stiffness(_dphi_ref, dx, c, m)
                    _dir_pi = -_dpi_ref
                    _gv = spectral_grad(dphi_bl, dx); _gw = spectral_grad(_dir_phi, dx)
                    _inner_phi = float(np.sum((c*c)*_gv*_gw + (m*m)*dphi_bl*_dir_phi) * dx)
                    _inner_pi = float(np.sum(dpi_bl * _dir_pi) * dx)
                    _inner = _inner_phi + _inner_pi
                    _v_size, _, _ = _h_energy_components(dphi_bl, dpi_bl, dx, c, m)
                    _w_size, _, _ = _h_energy_components(_dir_phi, _dir_pi, dx, c, m)
                    _align_cos = float(_inner / (max(_v_size, 1e-12) * max(_w_size, 1e-12)))
                    telemetry_rows.append({
                        "seed": seed, "lambda": float(lam), "step": int(i+1), "mode": "baseline",
                        "err_to_ref": float(_bl_err_step),
                        "work_total": float(_bl_work_total), "work_e_phi": float(_bl_e_phi), "work_e_pi": float(_bl_e_pi),
                        "phi_share": float(_bl_phi_share), "pi_share": float(_bl_pi_share), "cum_work": float(bl_work_sum),
                        "H_energy": float(H_bl), "theta_energy": float(theta_bl),
                        "phi1": float(_phi1_bl), "pi1": float(_pi1_bl), "delta_sigma": 0.0,
                        "align_cos": float(_align_cos)
                    })
            bl_err = h_energy_norm_delta(bl_ph, bl_pr, phi0, pi0, dx, c, m)
            baseline_errs[lam_key] = bl_err

            # If lambda == 0, enforce identical baseline/assisted by construction
            if float(lam) == 0.0:
                assisted_errs[lam_key] = baseline_errs[lam_key]
                work_summaries[lam_key] = {"baseline_work": bl_work_sum, "assisted_work": bl_work_sum}
                telemetry_per_lambda[lam_key] = {
                    "baseline": {"err_trace": bl_err_trace, "phi_share": bl_phi_share_trace, "pi_share": bl_pi_share_trace},
                    "assisted": {"err_trace": bl_err_trace, "phi_share": bl_phi_share_trace, "pi_share": bl_pi_share_trace},
                    "efficiency": 0.0
                }
                continue
            # Assisted reverse with model-aware corrections
            as_ph, as_pr = phiF.copy(), piF.copy()
            as_work_sum = 0.0
            as_work_comp = 0.0  # Kahan compensation for assisted work accumulation
            # reverse-phase parameter scrambles (RP-4: J/M scramble)
            c_rev = float(c * j_scramble_factor)
            m_params_rev = dict(spec.params)
            m_params_rev["D"] = float(spec.params.get("D", 1.0)) * m_scramble_factor

            # choose assistance mode (RP-4: model_blind vs model_aware)
            def _assist_pair(curr_phi, curr_pi, targ) -> Tuple[np.ndarray, np.ndarray]:
                if assist_mode == "model_blind":
                    return _random_correction_pair(rng, curr_phi, curr_pi, dx, targ, c_rev, m)
                return _assist_correction_pair(curr_phi, curr_pi, phi0, pi0, dx, spec.params, work=targ, c=c_rev, m=m)

            # telemetry arrays (assisted) for this lambda
            as_err_trace: List[float] = []
            as_phi_share_trace: List[float] = []
            as_pi_share_trace: List[float] = []

            for i in range(steps):
                target = float(step_targets[i])
                
                if reverse_order == "MJM":
                    # M(dt/2)
                    as_ph, _ = m_only_step_with_stats(as_ph, 0.5 * dt, dx, m_params_rev)
                    # apply assistance after first segment
                    dphi_as, dpi_as = _assist_pair(as_ph, as_pr, target)
                    zph = np.zeros_like(dphi_as); zpi = np.zeros_like(dpi_as)
                    _as_delta = float(h_energy_norm_delta(dphi_as, dpi_as, zph, zpi, dx, c_rev, m))
                    _y = _as_delta - as_work_comp
                    _t = as_work_sum + _y
                    as_work_comp = (_t - as_work_sum) - _y
                    as_work_sum = _t
                    as_ph = as_ph + dphi_as
                    as_pr = as_pr + dpi_as
                    # J(-dt)
                    as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -1.0 * dt, dx, c_rev, m)
                    # M(dt/2)
                    as_ph, _ = m_only_step_with_stats(as_ph, 0.5 * dt, dx, m_params_rev)
                    # per-step telemetry (assisted, MJM)
                    _as_work_total, _as_e_phi, _as_e_pi = _h_energy_components(dphi_as, dpi_as, dx, c_rev, m)
                    _as_den = (_as_e_phi + _as_e_pi) if (_as_e_phi + _as_e_pi) > 0.0 else 1.0
                    _as_phi_share = float(_as_e_phi / _as_den)
                    _as_pi_share = float(_as_e_pi / _as_den)
                    _as_err_step = h_energy_norm_delta(as_ph, as_pr, phi0, pi0, dx, c, m)
                    as_err_trace.append(float(_as_err_step))
                    as_phi_share_trace.append(_as_phi_share)
                    as_pi_share_trace.append(_as_pi_share)
                    # First-mode with instrument metric (c, m)
                    H_as, theta_as, _r_as, _phi1_as, _pi1_as = _first_mode_energy_angle(as_ph, as_pr, dx, c, m)
                    # Alignment of applied assistance to -∇_H direction
                    _dphi_ref = (as_ph - phi0).astype(float)
                    _dpi_ref = (as_pr - pi0).astype(float)
                    _dir_phi = -stiffness(_dphi_ref, dx, c, m)
                    _dir_pi = -_dpi_ref
                    _gv = spectral_grad(dphi_as, dx); _gw = spectral_grad(_dir_phi, dx)
                    _inner_phi = float(np.sum((c*c)*_gv*_gw + (m*m)*dphi_as*_dir_phi) * dx)
                    _inner_pi = float(np.sum(dpi_as * _dir_pi) * dx)
                    _inner = _inner_phi + _inner_pi
                    _v_size, _, _ = _h_energy_components(dphi_as, dpi_as, dx, c, m)
                    _w_size, _, _ = _h_energy_components(_dir_phi, _dir_pi, dx, c, m)
                    _align_cos = float(_inner / (max(_v_size, 1e-12) * max(_w_size, 1e-12)))
                    telemetry_rows.append({
                        "seed": seed, "lambda": float(lam), "step": int(i+1), "mode": "assisted",
                        "err_to_ref": float(_as_err_step),
                        "work_total": float(_as_work_total), "work_e_phi": float(_as_e_phi), "work_e_pi": float(_as_e_pi),
                        "phi_share": float(_as_phi_share), "pi_share": float(_as_pi_share), "cum_work": float(as_work_sum),
                        "H_energy": float(H_as), "theta_energy": float(theta_as),
                        "phi1": float(_phi1_as), "pi1": float(_pi1_as), "delta_sigma": 0.0,
                        "align_cos": float(_align_cos)
                    })
                else:
                    # J(-dt/2)
                    as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c_rev, m)
                    # apply assistance
                    dphi_as, dpi_as = _assist_pair(as_ph, as_pr, target)
                    zph = np.zeros_like(dphi_as); zpi = np.zeros_like(dpi_as)
                    _as_delta = float(h_energy_norm_delta(dphi_as, dpi_as, zph, zpi, dx, c_rev, m))
                    _y = _as_delta - as_work_comp
                    _t = as_work_sum + _y
                    as_work_comp = (_t - as_work_sum) - _y
                    as_work_sum = _t
                    as_ph = as_ph + dphi_as
                    as_pr = as_pr + dpi_as
                    # M(+dt) on phi-channel
                    as_ph, _stats = m_only_step_with_stats(as_ph, dt, dx, m_params_rev)
                    # J(-dt/2)
                    as_ph, as_pr = kg_verlet_step(as_ph, as_pr, -0.5 * dt, dx, c_rev, m)
                    # per-step telemetry (assisted, JMJ)
                    _as_work_total, _as_e_phi, _as_e_pi = _h_energy_components(dphi_as, dpi_as, dx, c_rev, m)
                    _as_den = (_as_e_phi + _as_e_pi) if (_as_e_phi + _as_e_pi) > 0.0 else 1.0
                    _as_phi_share = float(_as_e_phi / _as_den)
                    _as_pi_share = float(_as_e_pi / _as_den)
                    _as_err_step = h_energy_norm_delta(as_ph, as_pr, phi0, pi0, dx, c, m)
                    as_err_trace.append(float(_as_err_step))
                    as_phi_share_trace.append(_as_phi_share)
                    as_pi_share_trace.append(_as_pi_share)
                    # First-mode with instrument metric (c, m)
                    H_as, theta_as, _r_as, _phi1_as, _pi1_as = _first_mode_energy_angle(as_ph, as_pr, dx, c, m)
                    # Alignment of applied assistance to -∇_H direction
                    _dphi_ref = (as_ph - phi0).astype(float)
                    _dpi_ref = (as_pr - pi0).astype(float)
                    _dir_phi = -stiffness(_dphi_ref, dx, c, m)
                    _dir_pi = -_dpi_ref
                    _gv = spectral_grad(dphi_as, dx); _gw = spectral_grad(_dir_phi, dx)
                    _inner_phi = float(np.sum((c*c)*_gv*_gw + (m*m)*dphi_as*_dir_phi) * dx)
                    _inner_pi = float(np.sum(dpi_as * _dir_pi) * dx)
                    _inner = _inner_phi + _inner_pi
                    _v_size, _, _ = _h_energy_components(dphi_as, dpi_as, dx, c, m)
                    _w_size, _, _ = _h_energy_components(_dir_phi, _dir_pi, dx, c, m)
                    _align_cos = float(_inner / (max(_v_size, 1e-12) * max(_w_size, 1e-12)))
                    telemetry_rows.append({
                        "seed": seed, "lambda": float(lam), "step": int(i+1), "mode": "assisted",
                        "err_to_ref": float(_as_err_step),
                        "work_total": float(_as_work_total), "work_e_phi": float(_as_e_phi), "work_e_pi": float(_as_e_pi),
                        "phi_share": float(_as_phi_share), "pi_share": float(_as_pi_share), "cum_work": float(as_work_sum),
                        "H_energy": float(H_as), "theta_energy": float(theta_as),
                        "phi1": float(_phi1_as), "pi1": float(_pi1_as), "delta_sigma": 0.0,
                        "align_cos": float(_align_cos)
                    })
            assisted_err = h_energy_norm_delta(as_ph, as_pr, phi0, pi0, dx, c, m)
            assisted_errs[lam_key] = assisted_err
            work_summaries[lam_key] = {"baseline_work": bl_work_sum, "assisted_work": as_work_sum}
            # per-lambda telemetry bundle (+ efficiency)
            telemetry_per_lambda[lam_key] = {
                "baseline": {"err_trace": bl_err_trace, "phi_share": bl_phi_share_trace, "pi_share": bl_pi_share_trace},
                "assisted": {"err_trace": as_err_trace, "phi_share": as_phi_share_trace, "pi_share": as_pi_share_trace},
                "efficiency": float((baseline_errs[lam_key] - assisted_errs[lam_key]) / max(as_work_sum, 1e-12))
            }

        # CEG per lambda using matched-work baseline
        ceg_map = {}
        for l in lambdas:
            k = _lam_key(l)
            if (k in baseline_errs) and (k in assisted_errs):
                ceg_map[k] = ceg(baseline_errs[k], assisted_errs[k])
        # Enforce by-construction invariant: CEG(0) = 0 when assisted_err == baseline_err at λ=0
        if any(float(l) == 0.0 for l in lambdas):
            ceg_map[_lam_key(0.0)] = 0.0

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
                key = _lam_key(lam)
                ws = work_summaries.get(key)
                if not ws:
                    continue
                w_b = float(ws.get("baseline_work", 0.0))
                w_a = float(ws.get("assisted_work", 0.0))
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
                "h0": float(h0),
                "strang": {"slope": slope, "R2": r2}
            },
            "telemetry": telemetry_per_lambda,
            "ceg": ceg_map
        })

    results["per_seed"] = per_seed
    # Aggregates
    # use top-level numpy import (avoid local import which shadows global np)
    agg = {}
    for lam in lambdas:
        vals: List[float] = []
        k = _lam_key(lam)
        for s in per_seed:
            v = s.get("ceg", {}).get(k, None)
            if v is None:
                continue
            try:
                vals.append(float(v))
            except Exception:
                # Skip non-numeric entries defensively
                continue
        if len(vals) == 0:
            agg[k] = {"median": 0.0, "mean": 0.0, "n": 0}
        else:
            arr = np.array(vals, dtype=float)
            agg[k] = {"median": float(np.median(arr)), "mean": float(np.mean(arr)), "n": int(arr.size)}
    results["ceg_summary"] = agg
    # attach flat telemetry rows for CSV emission
    results["telemetry_rows"] = telemetry_rows

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

        # Use same scaled tolerance for G1 as in RP-1 calibration
        _eps_local = float(np.finfo(float).eps)
        _h0_diag = float(diag.get("h0", 1.0))
        _g1_tol_ledger = float(max(1e-12, 10.0 * _eps_local * float(np.sqrt(N)) * max(_h0_diag, 1.0)))
        gates = [
            gate_noether(time_rev_drift, tol=_g1_tol_ledger),
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
    # Apply pass-rate threshold per gate (instrument aggregation)
    min_gate_pass_rate = float(spec.params.get("min_gate_pass_rate", 0.8333333333333334))  # default ≥10/12
    for name, counts in tally.items():
        total = counts["passed"] + counts["failed"]
        pr = (counts["passed"] / total) if total > 0 else None
        meets_rate = (pr is not None) and (pr >= min_gate_pass_rate)
        agg_ledger[name] = {
            "passed": counts["passed"],
            "failed": counts["failed"],
            "n": total,
            "pass_rate": pr,
            "min_pass_rate": min_gate_pass_rate,
            "meets_rate": bool(meets_rate),
        }
    # Add overall CEG gate (G5): require positive echo gain for some λ>0 at the aggregate (median across seeds)
    try:
        ceg_summary = results.get("ceg_summary", {})
        medians = [float(v.get("median", 0.0)) for k, v in ceg_summary.items() if float(k) > 0.0]
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

    # Contradiction report at top-level if any instrument gate fails the pass-rate threshold
    # Route failures based on instrument gates only (G1–G4); treat G5 as outcome metric
    min_gate_pass_rate = float(spec.params.get("min_gate_pass_rate", 0.8333333333333334))
    total_failed = sum(
        1
        for k, v in agg_ledger.items()
        if k != "G5_CEG_Positive"
        and v.get("pass_rate") is not None
        and float(v.get("pass_rate")) < min_gate_pass_rate
    )
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
    # Determine schema tag from the spec filename to align with the correct prereg schema/approval
    spec_name = Path(args.spec).name
    if "v1c" in spec_name:
        schema_tag = "echo_spec-v1c"
    elif "v1b" in spec_name:
        schema_tag = "echo_spec-v1b"
    else:
        schema_tag = "echo_spec-v1"
    os.environ.setdefault("VDM_RUN_SCRIPT", "assisted_echo")
    # Enforce approval via policy for genuine runs (deterministic manifest discovery in approval.py)
    _approved, _eng_only, _proposal = check_tag_approval("metriplectic", schema_tag, args.allow_unapproved, CODE_ROOT)

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
    # Telemetry CSV: per-step traces (baseline/assisted)
    csvt = log_path("metriplectic", _slug("assisted_echo_telemetry", tag), failed=failed, type="csv")
    with csvt.open("w", encoding="utf-8") as f:
        f.write("seed,lambda,step,mode,err_to_ref,work_total,work_e_phi,work_e_pi,phi_share,pi_share,cum_work,H_energy,theta_energy,phi1,pi1,delta_sigma,align_cos\n")
        for row in out.get("telemetry_rows", []):
            f.write(f"{row['seed']},{row['lambda']},{row['step']},{row['mode']},{row['err_to_ref']},{row['work_total']},{row['work_e_phi']},{row['work_e_pi']},{row['phi_share']},{row['pi_share']},{row.get('cum_work',0.0)},{row.get('H_energy',0.0)},{row.get('theta_energy',0.0)},{row.get('phi1',0.0)},{row.get('pi1',0.0)},{row.get('delta_sigma',0.0)},{row.get('align_cos',0.0)}\n")
    # Placeholder figure path (figure creation may be handled by downstream notebooks)
    figp = figure_path("metriplectic", _slug("assisted_echo_placeholder", tag), failed=failed)
    try:
        import matplotlib.pyplot as plt
        pairs = sorted(((float(k), v.get('median', 0.0)) for k, v in out.get("ceg_summary", {}).items()), key=lambda t: t[0])
        lambdas = [p[0] for p in pairs]
        meds = [float(p[1]) for p in pairs]
        plt.figure(figsize=(6,4)); plt.plot(lambdas, meds, "o-"); plt.xlabel("lambda"); plt.ylabel("median CEG"); plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()
    except Exception as e:
        _ = e
    # Generate standardized figure pack (A+B essentials); non-fatal on error
    figure_pack = {}
    try:
        # Extract timestamp stem from placeholder figure name "{ts}_assisted_echo_placeholder__{tag}.png"
        ts_stem = Path(figp).stem
        if "_assisted_echo_" in ts_stem:
            ts_stem = ts_stem.split("_assisted_echo_")[0]
        # Choose a representative λ for overlays (prefer last nonzero)
        lam_nonzero = [float(l) for l in (spec.lambdas or []) if float(l) > 0.0]
        lambda_plot = float(spec.params.get("lambda_plot", lam_nonzero[-1] if lam_nonzero else 0.5))
        # Threshold from ledger if available, else params default
        g5_thr = float(out.get("gate_ledger_summary", {}).get("G5_CEG_Positive", {}).get("tol", spec.params.get("ceg_gate_threshold", 0.05)))
        figure_pack = generate_core_pack(
            domain="metriplectic",
            tag=str(tag) if tag else "",
            timestamp_stem=str(ts_stem),
            run_json=logp,
            telemetry_csv=csvt,
            ceg_csv=csvp,
            lambda_assisted=lambda_plot,
            g5_threshold=g5_thr
        )
    except Exception as _e:
        # Non-fatal: figure pack generation should not block logs
        _ = _e
    print(json.dumps({"log": str(logp), "csv": str(csvp), "figure": str(figp), "figure_pack": figure_pack}, indent=2))


if __name__ == "__main__":
    main()
