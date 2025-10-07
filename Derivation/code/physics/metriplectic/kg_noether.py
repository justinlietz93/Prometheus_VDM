#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np

# Ensure code root on sys.path
import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from physics.metriplectic.kg_ops import spectral_grad, spectral_laplacian


@dataclass
class NoetherSpec:
    grid: Dict[str, Any]
    params: Dict[str, Any]
    dt: float
    steps: int
    seed: int | None = 1234
    tag: str | None = None


def _slug(base: str, spec: NoetherSpec) -> str:
    tag = spec.params.get("tag") if isinstance(spec.params, dict) else None
    if tag is None:
        tag = getattr(spec, "tag", None)
    return f"{base}__{str(tag).strip().replace(' ', '-') if tag else base}"


def stiffness(phi: np.ndarray, dx: float, c: float, m: float) -> np.ndarray:
    """K phi = -c^2 Δ_h phi + m^2 phi (periodic spectral)"""
    return -(c * c) * spectral_laplacian(phi, dx) + (m * m) * phi


def verlet_step_with_half(phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, c: float, m: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Perform one Störmer-Verlet step returning (phi_new, pi_half, pi_new)."""
    lap_phi = spectral_laplacian(phi, dx)
    pi_half = pi + 0.5 * dt * ((c * c) * lap_phi - (m * m) * phi)
    phi_new = phi + dt * pi_half
    lap_phi_new = spectral_laplacian(phi_new, dx)
    pi_new = pi_half + 0.5 * dt * ((c * c) * lap_phi_new - (m * m) * phi_new)
    return phi_new, pi_half, pi_new


def discrete_energy(phi_n: np.ndarray, phi_np1: np.ndarray, pi_half: np.ndarray, dx: float, c: float, m: float) -> float:
    """Leapfrog/Verlet discrete energy exactly conserved for linear KG:

    E_d = 1/2 ||pi_{n+1/2}||^2 + 1/2 <phi_{n+1}, K phi_n>.
    """
    Kphi_n = stiffness(phi_n, dx, c, m)
    term_k = 0.5 * float(np.sum(pi_half * pi_half) * dx)
    term_p = 0.5 * float(np.sum(phi_np1 * Kphi_n) * dx)
    return term_k + term_p


def discrete_momentum(phi_n: np.ndarray, phi_np1: np.ndarray, pi_half: np.ndarray, dx: float) -> float:
    """Translation Noether momentum (discrete midpoint variant):

    P_d = < pi_{n+1/2}, ∇_h ( (phi_{n+1}+phi_n)/2 ) >.
    """
    phi_mid = 0.5 * (phi_np1 + phi_n)
    grad_mid = spectral_grad(phi_mid, dx)
    return float(np.sum(pi_half * grad_mid) * dx)


def run_noether(spec: NoetherSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt = float(spec.dt)
    c = float(spec.params.get("c", 1.0)) ; m = float(spec.params.get("m", 0.0))
    steps = int(spec.steps)
    rng = np.random.default_rng(int(spec.seed) if spec.seed is not None else None)
    scale = float(spec.params.get("seed_scale", 0.05))
    phi = rng.random(N).astype(float) * scale
    pi = rng.random(N).astype(float) * scale

    times: List[float] = [] ; E_d: List[float] = [] ; P_d: List[float] = []
    t = 0.0
    # initial half-step values derived from first step
    for n in range(steps):
        phi_new, pi_half, pi_new = verlet_step_with_half(phi, pi, dt, dx, c, m)
        Ed = discrete_energy(phi, phi_new, pi_half, dx, c, m)
        Pd = discrete_momentum(phi, phi_new, pi_half, dx)
        times.append(t + 0.5 * dt)
        E_d.append(float(Ed))
        P_d.append(float(Pd))
        # advance
        phi, pi = phi_new, pi_new
        t += dt

    # per-step changes
    dE = [abs(E_d[i+1] - E_d[i]) for i in range(len(E_d)-1)]
    dP = [abs(P_d[i+1] - P_d[i]) for i in range(len(P_d)-1)]
    max_dE = float(max(dE) if dE else 0.0)
    max_dP = float(max(dP) if dP else 0.0)
    eps = float(np.finfo(float).eps) ; sqrtN = float(np.sqrt(N))
    bound = eps * sqrtN
    pass_energy = (max_dE <= 1e-12) or (max_dE <= 10.0 * bound)
    pass_momentum = (max_dP <= 1e-12) or (max_dP <= 10.0 * bound)

    # Save CSV
    csvp = log_path("metriplectic", _slug("kg_noether_energy_momentum", spec), failed=not (pass_energy and pass_momentum), type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("t,E_disc,P_disc\n")
        for ti, Ei, Pi in zip(times, E_d, P_d):
            f.write(f"{ti},{Ei},{Pi}\n")

    # reversibility test over steps
    phi0, pi0 = np.copy(rng.bit_generator.random_raw() or phi), np.copy(pi)  # placeholders to satisfy type
    # Reconstruct exact initial (phi0, pi0) by re-running one trajectory with recorded seed
    rng2 = np.random.default_rng(int(spec.seed) if spec.seed is not None else None)
    phi0 = rng2.random(N).astype(float) * scale
    pi0 = rng2.random(N).astype(float) * scale
    phi_f, pi_f = phi0.copy(), pi0.copy()
    for _ in range(steps):
        phi_f, _, pi_f = verlet_step_with_half(phi_f, pi_f, dt, dx, c, m)
    # reverse
    for _ in range(steps):
        # reversing with -dt
        phi_f, _, pi_f = verlet_step_with_half(phi_f, pi_f, -dt, dx, c, m)
    rev_err = float(max(np.linalg.norm(phi_f - phi0, ord=np.inf), np.linalg.norm(pi_f - pi0, ord=np.inf)))
    pass_rev = rev_err <= 1e-12 or rev_err <= 1e-10

    logj = {
        "dt": dt, "steps": steps, "N": N,
        "max_per_step_delta": {"E_disc": max_dE, "P_disc": max_dP},
        "epsilon": eps, "sqrtN": sqrtN, "epsilon_sqrtN": bound,
        "passed": {"energy": pass_energy, "momentum": pass_momentum, "reversibility": pass_rev},
        "csv": str(csvp)
    }
    failed = not (pass_energy and pass_momentum and pass_rev)
    write_log(log_path("metriplectic", _slug("kg_noether_energy_momentum", spec), failed=failed), logj)
    if failed:
        write_log(log_path("metriplectic", _slug("CONTRADICTION_REPORT_kg_noether", spec), failed=True), {
            "reason": "Noether gate failure",
            "spec": {"dt": dt, "steps": steps, "grid": spec.grid, "params": spec.params},
            "metrics": logj,
            "artifacts": {"csv": str(csvp)}
        })
    return logj


def dispersion_check(spec: NoetherSpec, k_list: List[int] | None = None) -> Dict[str, Any]:
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; dt = float(spec.dt)
    c = float(spec.params.get("c", 1.0)) ; m = float(spec.params.get("m", 0.0))
    steps = int(spec.steps)
    if not k_list:
        k_list = [1, 2, 3]
    omega2: List[float] = [] ; k2: List[float] = []
    for k in k_list:
        x = np.arange(N) * dx
        phi = np.sin(2.0 * np.pi * k * x / (N * dx)) * 1e-3
        pi = np.zeros_like(phi)
        samples: List[float] = []
        for _ in range(steps):
            phi, _, pi = verlet_step_with_half(phi, pi, dt, dx, c, m)
            samples.append(float(phi[0]))
        s = np.array(samples, dtype=float)
        # dominant frequency via FFT
        S = np.fft.rfft(s)
        freqs = np.fft.rfftfreq(s.size, d=dt)
        idx = int(np.argmax(np.abs(S[1:])) + 1)  # skip zero freq
        omega = 2.0 * np.pi * freqs[idx]
        omega2.append(float(omega * omega))
        k_phys = 2.0 * np.pi * k / (N * dx)
        k2.append(float(k_phys * k_phys))

    # Fit omega^2 = m^2 + c^2 k^2
    x = np.array(k2, dtype=float) ; y = np.array(omega2, dtype=float)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, intercept])
    ss_res = float(np.sum((y - y_pred)**2)) ; ss_tot = float(np.sum((y - np.mean(y))**2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    passed = (abs(slope - c * c) / max(c * c, 1e-12) < 0.05) and (abs(intercept - m * m) / max(m * m, 1e-12) < 0.05) and (R2 >= 0.999)

    # Artifacts
    import matplotlib.pyplot as plt
    figp = figure_path("metriplectic", _slug("kg_dispersion", spec), failed=not passed)
    plt.figure(figsize=(5.2, 4.0))
    plt.plot(k2, omega2, "o", label="measured")
    xs = np.linspace(0, max(k2) * 1.05, 100)
    plt.plot(xs, slope * xs + intercept, "-", label=f"fit: ω^2 ≈ {slope:.3f} k^2 + {intercept:.3f}")
    plt.xlabel("k^2") ; plt.ylabel("ω^2") ; plt.legend() ; plt.tight_layout()
    plt.savefig(figp, dpi=150) ; plt.close()

    csvp = log_path("metriplectic", _slug("kg_dispersion", spec), failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("k2,omega2\n")
        for xi, yi in zip(k2, omega2):
            f.write(f"{xi},{yi}\n")

    logj = {"fit": {"slope": float(slope), "intercept": float(intercept), "R2": float(R2)}, "passed": bool(passed), "figure": str(figp), "csv": str(csvp)}
    write_log(log_path("metriplectic", _slug("kg_dispersion", spec), failed=not passed), logj)
    if not passed:
        write_log(log_path("metriplectic", _slug("CONTRADICTION_REPORT_kg_dispersion", spec), failed=True), {
            "reason": "Dispersion gate failure",
            "spec": {"dt": float(spec.dt), "steps": int(spec.steps), "grid": spec.grid, "params": spec.params},
            "metrics": logj,
            "artifacts": {"figure": str(figp), "csv": str(csvp)}
        })
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="KG Noether checks (energy/momentum) and optional dispersion")
    p.add_argument("--spec", type=str, required=True, help="Path to KG⊕RD spec JSON (for N, dx, c, m, tag)")
    p.add_argument("--steps", type=int, default=256)
    p.add_argument("--dt", type=float, default=None, help="Override dt (default: min of spec.dt_sweep)")
    p.add_argument("--dispersion", action="store_true")
    args = p.parse_args()
    spec_path = Path(args.spec)
    raw = json.loads(spec_path.read_text())
    tag = raw.get("tag") or (raw.get("params", {}).get("tag"))
    dt = float(args.dt if args.dt is not None else min(raw["dt_sweep"]))
    nspec = NoetherSpec(grid=raw["grid"], params=raw["params"], dt=dt, steps=int(args.steps), seed=1234, tag=tag)
    noether = run_noether(nspec)
    result = {"noether": noether}
    if args.dispersion:
        result["dispersion"] = dispersion_check(nspec)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
