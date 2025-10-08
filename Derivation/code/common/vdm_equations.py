"""
VDM Canonical Equations — runtime evaluators with traceable references

Purpose

- Provide a single import surface for core equations referenced in Derivation/EQUATIONS.md.
- Keep numerical helpers close to the documented canon with explicit parameterization and audit trail (VDM-E-### references).

Design notes

- Pure module: zero side effects and no I/O; safe to import in tests and runners.
- Explicit parameters: pass everything needed; defaults mirror common mappings only when unambiguous.
- References: inline docstrings point to entries in Derivation/EQUATIONS.md for accountability.

Implemented (key entries)

- Potential V and derivatives V', V'' (VDM-E-012, VDM-E-058)
- RD reaction f(φ) and logistic exact step (VDM-E-015, VDM-E-025)
- RD dispersion σ(k), discrete σ_d(m), and KPP speed c_front (VDM-E-017, -034, -035, -018)
- Discrete↔Continuum parameter maps (VDM-E-029, -050)
- Klein-Gordon wave speed c^2 from lattice parameters (VDM-E-014, -041, -077)
- Stabilized vacuum v_λ and effective mass m_eff^2 (VDM-E-059, -060)

License: Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import numpy as np


# ------------------------------
# Parameters (lightweight typed bags)
# ------------------------------

@dataclass(frozen=True)
class PotentialParams:
    """Parameters for stabilized potential.

    V(φ) = (α/3) φ^3 - (r/2) φ^2 + (λ/4) φ^4, with r = α - β (VDM-E-012, -058)
    """
    alpha: float
    beta: float
    lam: float = 0.0

    @property
    def r(self) -> float:
        return self.alpha - self.beta


@dataclass(frozen=True)
class RDParams:
    """Reaction-diffusion continuum parameters (VDM-E-015, -028, -050)."""
    D: float
    r: float
    u: float
    lam: float = 0.0


@dataclass(frozen=True)
class LatticeParams:
    """Discrete lattice parameters for mapping (VDM-E-011, -029, -041)."""
    J: float
    a: float
    gamma: float | None = None  # optional damping for RD map (VDM-E-044, -050)


# ------------------------------
# Potential and derivatives (VDM-E-012, -058)
# ------------------------------

def V(phi: np.ndarray | float, p: PotentialParams) -> np.ndarray | float:
    """Stabilized potential V(φ).

    V(φ) = (α/3) φ^3 - (r/2) φ^2 + (λ/4) φ^4, r = α - β (VDM-E-012, -058)
    """
    r = p.r
    return (p.alpha / 3.0) * np.asarray(phi) ** 3 - 0.5 * r * np.asarray(phi) ** 2 + (p.lam / 4.0) * np.asarray(phi) ** 4


def Vp(phi: np.ndarray | float, p: PotentialParams) -> np.ndarray | float:
    """V'(φ) = α φ^2 - r φ + λ φ^3 (VDM-E-012)."""
    r = p.r
    phi = np.asarray(phi)
    return p.alpha * phi ** 2 - r * phi + p.lam * phi ** 3


def Vpp(phi: np.ndarray | float, p: PotentialParams) -> np.ndarray | float:
    """V''(φ) = 2α φ - r + 3λ φ^2 (VDM-E-012)."""
    r = p.r
    phi = np.asarray(phi)
    return 2.0 * p.alpha * phi - r + 3.0 * p.lam * phi ** 2


# ------------------------------
# RD reaction term and exact step (VDM-E-015, -028, -025)
# ------------------------------

def rd_reaction(phi: np.ndarray | float, r: float, u: float, lam: float = 0.0) -> np.ndarray | float:
    """Reaction term f(φ) = r φ − u φ² − λ φ³ (VDM-E-015, -028).

    Interpretation: logistic (quadratic) growth with optional cubic saturation.
    Stability/scale: Signs and magnitudes of (r, u, λ) determine fixed points and stiffness.
    """
    phi = np.asarray(phi)
    return r * phi - u * phi ** 2 - lam * phi ** 3


def logistic_exact_step(W: np.ndarray | float, dt: float, r: float, u: float) -> np.ndarray | float:
    """Exact step for dW/dt = r W − u W² over Δt (VDM-E-025).

    Useful for stiff regimes and reference solutions: preserves positivity for W≥0 with r,u≥0.
    """
    W = np.asarray(W)
    exp_rt = np.exp(r * dt)
    return (r * W * exp_rt) / (u * W * (exp_rt - 1.0) + r)


# ------------------------------
# Dispersion and front speed (VDM-E-017, -034, -035, -018)
# ------------------------------

def dispersion_continuum(k: np.ndarray | float, D: float, r: float) -> np.ndarray | float:
    """Continuum dispersion relation σ(k) = r − D k² (VDM-E-017, -035)."""
    k = np.asarray(k)
    return r - D * k ** 2


def dispersion_discrete(m: np.ndarray | int, N: int, L: float, D: float, r: float) -> np.ndarray | float:
    """Discrete dispersion σ_d(m) = r − (4D/Δx²) sin²(π m / N), Δx = L/N (VDM-E-034)."""
    m = np.asarray(m)
    dx = L / float(N)
    return r - (4.0 * D / (dx ** 2)) * np.sin(np.pi * m / float(N)) ** 2


def kpp_front_speed(D: float, r: float) -> float:
    """KPP front speed c_front = 2 √(D r) (VDM-E-018, -033).

    Preconditions: D ≥ 0, r ≥ 0. Raises ValueError otherwise.
    """
    if D < 0 or r < 0:
        raise ValueError("KPP front speed requires D>=0 and r>=0")
    return 2.0 * float(np.sqrt(D * r))


# ------------------------------
# Discrete ↔ Continuum mappings (VDM-E-029, -050)
# ------------------------------

def rd_from_lattice(p: PotentialParams, lat: LatticeParams) -> RDParams:
    """Map discrete lattice params to RD params (VDM-E-050).

    D = 2 J a^2 / γ,  f(φ) = (1/γ) [ (α-β) φ - α φ^2 - λ φ^3 ].
    If γ is None, fall back to site Laplacian map D = J a^2 and raw r,u,λ (VDM-E-029).
    """
    if lat.gamma is not None:
        D = 2.0 * lat.J * (lat.a ** 2) / float(lat.gamma)
        r = (p.alpha - p.beta) / float(lat.gamma)
        u = p.alpha / float(lat.gamma)
        lam = p.lam / float(lat.gamma)
        return RDParams(D=D, r=r, u=u, lam=lam)
    # No damping provided: site-Laplacian mapping
    D = lat.J * (lat.a ** 2)
    return RDParams(D=D, r=p.alpha - p.beta, u=p.alpha, lam=p.lam)


def kg_c2_from_lattice(J: float, a: float, convention: str = "per-site") -> float:
    """Wave speed squared c² from lattice coupling (VDM-E-014, -041, -077).

    - convention="per-site": c² = 2 J a² (matches VDM-E-014/077)
    - convention="per-edge": c² = κ a² with κ = 2J (equivalent)
    """
    if convention == "per-site":
        return 2.0 * J * (a ** 2)
    elif convention == "per-edge":
        kappa = 2.0 * J
        return kappa * (a ** 2)
    else:
        raise ValueError("convention must be 'per-site' or 'per-edge'")


# ------------------------------
# Stabilized vacuum and effective mass (VDM-E-059, -060)
# ------------------------------

def stabilized_vacuum(p: PotentialParams) -> float:
    """Stabilized vacuum v_λ (VDM-E-059).

    v_λ = [-α + sqrt(α² + 4 λ (α − β))] / (2 λ), for λ > 0.
    If λ = 0, use the small-λ limit φ* = r/α (positive branch) when α > 0.
    """
    if p.lam > 0:
        disc = p.alpha ** 2 + 4.0 * p.lam * (p.alpha - p.beta)
        return float((-p.alpha + np.sqrt(disc)) / (2.0 * p.lam))
    # λ == 0: use small-λ limit φ* = r/α when α>0
    if p.alpha <= 0:
        raise ValueError("alpha must be > 0 for λ=0 vacuum selection")
    return float((p.alpha - p.beta) / p.alpha)


def effective_mass_squared(p: PotentialParams) -> float:
    """Effective mass squared m_eff² = V''(v_λ) (VDM-E-060).

    m_eff² = 2 α v_λ − (α − β) + 3 λ v_λ² ≈ (α − β) + O(λ).
    """
    v = stabilized_vacuum(p)
    return float(2.0 * p.alpha * v - (p.alpha - p.beta) + 3.0 * p.lam * (v ** 2))


# ------------------------------
# Utility: wavenumber helpers
# ------------------------------

def k_from_mode(m: np.ndarray | int, L: float) -> np.ndarray | float:
    """k = 2π m / L."""
    m = np.asarray(m)
    return 2.0 * np.pi * m / float(L)


def mode_from_k(k: np.ndarray | float, L: float) -> np.ndarray | float:
    """Inverse of k_from_mode for integer m ≈ round(k L / 2π)."""
    k = np.asarray(k)
    return np.rint(k * float(L) / (2.0 * np.pi))


# ------------------------------
# Sanity self-check (optional quick regression without pytest)
# ------------------------------

def _self_check() -> Tuple[bool, str]:
    """Run a tiny set of numerical identities; returns (ok, message)."""
    p = PotentialParams(alpha=0.25, beta=0.10, lam=0.0)
    rd = RDParams(D=1.0, r=0.25 - 0.10, u=0.25, lam=0.0)

    # Front speed identity
    c = kpp_front_speed(rd.D, rd.r)
    if not np.isclose(c, 2.0 * np.sqrt(rd.D * rd.r)):
        return False, "KPP speed mismatch"

    # Dispersion consistency near k=0
    k = 1e-3
    sig = dispersion_continuum(k, rd.D, rd.r)
    if not np.isclose(sig, rd.r - rd.D * k * k):
        return False, "Dispersion formula mismatch"

    # KG mapping consistency
    c2 = kg_c2_from_lattice(J=0.5, a=1.0, convention="per-site")
    if not np.isclose(c2, 1.0):
        return False, "KG c^2 per-site mapping mismatch"

    # Logistic exact step reduces to Euler for small dt
    W0 = 0.1
    dt = 1e-6
    W1_exact = logistic_exact_step(W0, dt, rd.r, rd.u)
    W1_euler = W0 + dt * rd_reaction(W0, rd.r, rd.u, rd.lam)
    if not np.isclose(W1_exact, W1_euler, rtol=0, atol=1e-10):
        return False, "Logistic exact small-dt limit mismatch"

    return True, "OK"


if __name__ == "__main__":  # manual smoke
    ok, msg = _self_check()
    print("vdm_equations self-check:", msg)
    raise SystemExit(0 if ok else 1)
