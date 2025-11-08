# Derivation/code/common/instrument_helpers/prigogine_gates.py
"""
Prigogine-inspired near-equilibrium entropy instruments for VDM.

Implements light-weight, NumPy-only meters that complement the LIT/GENERIC helpers:
- Representation invariance of entropy production σ under (X' = A X, J' = A^{-T} J)
- Interference (cross-coupling) share of σ and diagonal-block PSD checks
- Open-system entropy balance (volume production vs boundary entropy flux)
- Conduction Lyapunov potential Φ(T, T0) monotone-decrease monitor (Dirichlet walls)
- Rotation split audit: antisymmetric couplings belong to J (not to M)

All artifact writing is routed via common.io_paths and adheres to repository policy.

Canon anchors (do not duplicate equations; link by anchor):
- GENERIC evolution and entropy production: VDM-E-140..145 (Derivation/EQUATIONS.md)
- Curie scalarization (isotropy): VDM-E-146 (Derivation/EQUATIONS.md)
- KPIs: kpi-entropy-prod-nonneg, kpi-onsager-resid, kpi-curie-compliance, kpi-curie-violations
- Prigogine upgrades context: see docs/misc-standards/Non-Equilibrium-Thermodynamics.md and
  Derivation/References/Nonequilibrium_&_Entropy/entropy-upgrades.md
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Any

import numpy as np
import json
import csv

# I/O routing helpers (project policy)
try:
    from common.io_paths import (
        figure_path_by_tag,
        log_path_by_tag,
        write_log,
        build_slug,
        ensure_dir,
    )
except Exception:
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
    from io_paths import (  # type: ignore
        figure_path_by_tag,
        log_path_by_tag,
        write_log,
        build_slug,
        ensure_dir,
    )

# Optional plotting
try:
    import matplotlib.pyplot as plt  # type: ignore

    _HAVE_MPL = True
except Exception:
    _HAVE_MPL = False


ND = np.ndarray


def _as64(x: Any) -> ND:
    return np.asarray(x, dtype=np.float64)


def _sym(A: ND) -> ND:
    return 0.5 * (A + A.T)


def _skew(A: ND) -> ND:
    return 0.5 * (A - A.T)


# ----------------------------- Representation invariance -----------------------------


@dataclass
class ReprInvTrial:
    condA: float
    max_abs_diff: float
    rel_max_diff: float


@dataclass
class ReprInvReport:
    trials: List[ReprInvTrial]
    worst_rel: float
    worst_abs: float
    m: int
    n_cells: int
    meta: Dict[str, Any]


def _sample_A(m: int, kind: str, rng: np.random.Generator, cond_max: float = 10.0) -> Tuple[ND, float]:
    """Sample an m×m transform A.
    kind='haar': orthonormal (QR of Gaussian) → cond ~ 1
    kind='well_cond': construct with singular values in [1, cond_max]
    """
    if kind == "haar":
        G = rng.standard_normal((m, m))
        Q, R = np.linalg.qr(G)
        # Ensure right-handed orientation
        d = np.sign(np.diag(R))
        Q = Q @ np.diag(d)
        return Q, 1.0
    elif kind == "well_cond":
        U, _ = np.linalg.qr(rng.standard_normal((m, m)))
        V, _ = np.linalg.qr(rng.standard_normal((m, m)))
        s_min = 1.0
        s_max = float(cond_max)
        # Log-spaced singular values for stability
        s = np.exp(np.linspace(0.0, np.log(s_max), m))
        S = np.diag(s)
        A = U @ S @ V.T
        condA = float(np.linalg.cond(A))
        return A, condA
    else:
        raise ValueError("kind must be 'haar' or 'well_cond'")


def repr_invariance_check(
    L: ND,
    X_field: ND,
    *,
    n_trials: int = 5,
    kind: str = "haar",
    cond_max: float = 10.0,
    rng: Optional[np.random.Generator] = None,
) -> ReprInvReport:
    """Check σ invariance under (X' = A X, J' = A^{-T} J).
    - X_field: shape (Ncells, m)
    - L: (m, m)
    Computes σ = X^T L X per cell, repeats under transforms, reports worst-case diffs.
    """
    L = _as64(L)
    X = _as64(X_field)
    N, m = X.shape
    rng = rng or np.random.default_rng(0)

    # Baseline per-cell σ
    sigma = np.einsum("ni,ij,nj->n", X, L, X, optimize=True)
    sigma_abs_max = float(np.max(np.abs(sigma))) if sigma.size else 1.0
    sigma_abs_max = max(1.0, sigma_abs_max)  # normalization floor

    trials: List[ReprInvTrial] = []
    worst_rel = 0.0
    worst_abs = 0.0

    for _ in range(max(1, int(n_trials))):
        A, condA = _sample_A(m, kind=kind, rng=rng, cond_max=cond_max)
        Ainv = np.linalg.inv(A)

        # Transform forces X' = A X  (row representation: X'row = Xrow @ A^T)
        Xp = X @ A.T

        # J = L X  (row representation: Jrow = Xrow @ L^T)
        J = X @ L.T
        # Transform fluxes J' = A^{-T} J   (row: J'row = Jrow @ A^{-1})
        Jp = J @ Ainv

        sigma_p = np.einsum("ni,ni->n", Xp, Jp, optimize=True)

        diff = sigma_p - sigma
        max_abs = float(np.max(np.abs(diff))) if diff.size else 0.0
        rel = max_abs / sigma_abs_max

        trials.append(ReprInvTrial(condA=condA, max_abs_diff=max_abs, rel_max_diff=rel))
        worst_rel = max(worst_rel, rel)
        worst_abs = max(worst_abs, max_abs)

    return ReprInvReport(
        trials=trials, worst_rel=float(worst_rel), worst_abs=float(worst_abs), m=m, n_cells=N, meta={"kind": kind}
    )


# ----------------------------- Interference (cross) share -----------------------------


@dataclass
class InterferenceReport:
    sigma_total: float
    sigma_diag: float
    sigma_off: float
    chi_cross: float
    diag_blocks_psd_ok: bool
    diag_blocks_min_eigs: List[float]
    meta: Dict[str, Any]


def _block_min_eigs(Ld: ND, blocks: Optional[List[Sequence[int]]]) -> Tuple[bool, List[float]]:
    """Check PSD of diagonal blocks (symmetric part) if blocks given,
    else check diagonal entries >= 0."""
    if not blocks:
        d = np.diag(Ld)
        ok = bool(np.all(d >= -1e-12))
        return ok, [float(np.min(d)) if d.size else 0.0]
    mins: List[float] = []
    ok = True
    for idxs in blocks:
        B = _sym(Ld[np.ix_(idxs, idxs)])
        try:
            w = np.linalg.eigvalsh(B)
            wmin = float(np.min(w)) if w.size else 0.0
        except np.linalg.LinAlgError:
            wmin = float("nan")
            ok = False
        mins.append(wmin)
        ok = ok and (wmin >= -1e-12)
    return ok, mins


def interference_share(
    L: ND,
    X_field: ND,
    *,
    diag_blocks: Optional[List[Sequence[int]]] = None,
) -> InterferenceReport:
    """Split σ into diagonal vs off-diagonal contributions in the chosen basis and
    check PSD of diagonal blocks.

    - L: (m, m) phenomenological matrix (use the Curie-consistent basis).
    - X_field: (Ncells, m)
    - diag_blocks: list of index lists for block PSD checks (optional).
    """
    L = _as64(L)
    X = _as64(X_field)
    Di = np.diag(np.diag(L))
    Of = L - Di

    s_total = float(np.sum(np.einsum("ni,ij,nj->n", X, L, X, optimize=True)))
    s_diag = float(np.sum(np.einsum("ni,ij,nj->n", X, Di, X, optimize=True)))
    s_off = float(np.sum(np.einsum("ni,ij,nj->n", X, Of, X, optimize=True)))
    denom = s_total if abs(s_total) > 1e-300 else 1.0
    chi = s_off / denom

    psd_ok, mins = _block_min_eigs(Di, diag_blocks)

    return InterferenceReport(
        sigma_total=s_total,
        sigma_diag=s_diag,
        sigma_off=s_off,
        chi_cross=chi,
        diag_blocks_psd_ok=psd_ok,
        diag_blocks_min_eigs=mins,
        meta={"basis": "declared tensor-rank basis (isotropic)"},
    )


# ----------------------------- Open-system entropy balance -----------------------------


def compute_boundary_heat_entropy_flux(T: ND, kappa: float, dx: float, dy: float) -> float:
    """Compute ∮ (q·n)/T dA for heat flux q = -kappa ∇T on a rectangular grid with axis-aligned walls.
    Outward normal convention. Assumes scalar T defined per cell center.
    """
    T = _as64(T)
    Ny, Nx = T.shape

    # Left wall (normal = (-1,0)), area weight = dy
    dTdx_L = (T[:, 1] - T[:, 0]) / dx
    qn_L = (-kappa * dTdx_L) * (-1.0)
    term_L = np.sum(qn_L / np.clip(T[:, 0], 1e-300, np.inf)) * dy

    # Right wall (normal = (+1,0)), area weight = dy
    dTdx_R = (T[:, -1] - T[:, -2]) / dx
    qn_R = (-kappa * dTdx_R) * (+1.0)
    term_R = np.sum(qn_R / np.clip(T[:, -1], 1e-300, np.inf)) * dy

    # Bottom wall (normal = (0,-1)), area weight = dx
    dTdy_B = (T[1, :] - T[0, :]) / dy
    qn_B = (-kappa * dTdy_B) * (-1.0)
    term_B = np.sum(qn_B / np.clip(T[0, :], 1e-300, np.inf)) * dx

    # Top wall (normal = (0,+1)), area weight = dx
    dTdy_T = (T[-1, :] - T[-2, :]) / dy
    qn_T = (-kappa * dTdy_T) * (+1.0)
    term_T = np.sum(qn_T / np.clip(T[-1, :], 1e-300, np.inf)) * dx

    return float(term_L + term_R + term_B + term_T)


@dataclass
class OpenBalanceReport:
    production: float
    boundary_entropy_flux: float
    dSdt_estimate: Optional[float]
    closure_residual: Optional[float]
    meta: Dict[str, Any]


def entropy_balance_open(
    sigma_field: ND,
    dV: float,
    *,
    boundary_entropy_flux: float,
    dSdt_estimate: Optional[float] = None,
) -> OpenBalanceReport:
    """Open-system entropy balance components.
    - production = ∫Ω σ dV
    - boundary term = ∮ (q·n)/T dA (positive outward)
    - If dS/dt is available, report closure residual: production - boundary - dS/dt
    """
    sigma_field = _as64(sigma_field)
    prod = float(np.sum(sigma_field) * dV)
    J_s = float(boundary_entropy_flux)
    closure = None
    if dSdt_estimate is not None:
        closure = prod - J_s - float(dSdt_estimate)
    return OpenBalanceReport(
        production=prod,
        boundary_entropy_flux=J_s,
        dSdt_estimate=None if dSdt_estimate is None else float(dSdt_estimate),
        closure_residual=closure,
        meta={},
    )


# ----------------------------- Conduction Lyapunov Φ monitor -----------------------------


class PhiConductionMonitor:
    """Monitor a Dirichlet-conduction Lyapunov proxy Φ(T, T0) = ∫ (T - T0)^2 dV (monotone under linear diffusion).
    Records Φ(t) and asserts ΔΦ ≤ 0 within tolerance.
    """

    def __init__(self, tol: float = 1e-12) -> None:
        self.t: List[float] = []
        self.phi: List[float] = []
        self.tol = float(tol)
        self._time = 0.0

    def update(self, T: ND, T0: ND, dt: float, dV: float) -> Dict[str, float]:
        T = _as64(T)
        T0 = _as64(T0)
        dt = float(dt)
        dV = float(dV)
        diff2 = float(np.sum((T - T0) ** 2) * dV)
        self._time += dt
        self.t.append(self._time)
        self.phi.append(diff2)
        return {"t": self._time, "phi": diff2}

    def snapshot(self) -> Dict[str, float]:
        return {
            "t": self.t[-1] if self.t else 0.0,
            "phi": self.phi[-1] if self.phi else 0.0,
            "n": float(len(self.t)),
            "tol": self.tol,
        }

    def gates(self) -> Dict[str, Any]:
        ok = True
        worst_delta = 0.0
        for i in range(1, len(self.phi)):
            d = self.phi[i] - self.phi[i - 1]
            worst_delta = min(worst_delta, d)
            if d > self.tol:
                ok = False
        return {"phi_monotone_ok": ok, "phi_worst_delta": float(worst_delta), "tol": self.tol}

    def write_artifacts(
        self,
        domain: str,
        name: str,
        tag: Optional[str],
        meta: Optional[Dict[str, Any]] = None,
        failed: bool = False,
        write_png: bool = True,
    ) -> Dict[str, str]:
        slug = build_slug(name, tag)
        json_path = log_path_by_tag(domain, f"{name}_summary", tag, failed=failed, type="json")
        csv_path = log_path_by_tag(domain, f"{name}_series", tag, failed=failed, type="csv")

        summary = {
            "slug": slug,
            "domain": domain,
            "n": len(self.t),
            "tol": self.tol,
            "gates": self.gates(),
            "meta": meta or {},
            "series_paths": {"csv": str(csv_path)},
        }
        write_log(json_path, summary)

        ensure_dir(Path(csv_path).parent)
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["t", "phi"])
            writer.writeheader()
            for ti, ph in zip(self.t, self.phi):
                writer.writerow({"t": ti, "phi": ph})

        fig_path_str = ""
        if write_png and _HAVE_MPL and self.t:
            fig_path = figure_path_by_tag(domain, f"{name}_panel", tag, failed=failed)
            try:
                plt.figure(figsize=(6.4, 3.0), dpi=150)
                plt.plot(self.t, self.phi, label="Phi(T,T0)")
                plt.xlabel("t")
                plt.ylabel("Φ")
                plt.grid(True, alpha=0.25)
                plt.title(slug)
                plt.tight_layout()
                plt.savefig(fig_path, bbox_inches="tight")
                plt.close()
                fig_path_str = str(fig_path)
            except Exception:
                fig_path_str = ""

        return {"json": str(json_path), "csv": str(csv_path), "png": fig_path_str}


# ----------------------------- Rotation split audit -----------------------------


@dataclass
class RotationSplitReport:
    antisym_norm_inf: float
    sym_min_eig: Optional[float]
    gate_antisym_leak_ok: bool
    meta: Dict[str, Any]


def rotation_split_audit(M: ND, *, tol: float = 1e-12) -> RotationSplitReport:
    """Audit that the metric limb M has no antisymmetric leakage.
    Reports ||(M - M^T)/2||_∞ and the min eigenvalue of the symmetric part.
    """
    M = _as64(M)
    A = _skew(M)
    S = _sym(M)
    ainf = float(np.max(np.abs(A))) if A.size else 0.0
    sym_min = None
    try:
        w = np.linalg.eigvalsh(S)
        sym_min = float(np.min(w))
    except np.linalg.LinAlgError:
        sym_min = None
    ok = ainf <= tol
    return RotationSplitReport(
        antisym_norm_inf=ainf, sym_min_eig=sym_min, gate_antisym_leak_ok=ok, meta={"tol": tol}
    )


# ----------------------------- Artifact writer (JSON) -----------------------------


def write_prigogine_kpi_artifacts(
    domain: str,
    name: str,
    tag: Optional[str],
    payload: Dict[str, Any],
    *,
    failed: bool = False,
) -> Dict[str, str]:
    """Write a single JSON payload for Prigogine KPI results."""
    json_path = log_path_by_tag(domain, f"{name}_prigogine", tag, failed=failed, type="json")
    write_log(json_path, payload)
    return {"json": str(json_path)}


__all__ = [
    # Representation invariance
    "repr_invariance_check",
    "ReprInvTrial",
    "ReprInvReport",
    # Interference share
    "interference_share",
    "InterferenceReport",
    # Open-system entropy balance
    "compute_boundary_heat_entropy_flux",
    "entropy_balance_open",
    "OpenBalanceReport",
    # Conduction Lyapunov monitor
    "PhiConductionMonitor",
    # Rotation split audit
    "rotation_split_audit",
    "RotationSplitReport",
    # Artifact writer
    "write_prigogine_kpi_artifacts",
]