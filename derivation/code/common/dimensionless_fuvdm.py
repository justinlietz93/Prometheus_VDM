#!/usr/bin/env python3
# FUVDM dimensionless helpers (LBM + RD + memory steering)
"""
Canonical dimensionless numbers used across FUVDM runners.
Lattice units for LBM: dx=dt=1, c_s = 1/sqrt(3).
"""
from __future__ import annotations
import numpy as np

SQRT3 = np.sqrt(3.0)

def lbm_cs() -> float:
    """LBM lattice sound speed (l.u.)."""
    return 1.0 / SQRT3

def lbm_viscosity_from_tau(tau: float) -> float:
    """D2Q9 BGK kinematic viscosity ν in lattice units: ν=(τ−0.5)/3."""
    return (float(tau) - 0.5) / 3.0

def reynolds_lbm(U: float, L: float, tau: float) -> float:
    """Reynolds number Re = U L / ν in lattice units."""
    nu = lbm_viscosity_from_tau(tau)
    return (float(U) * float(L)) / (nu + 1e-15)

def mach_lbm(U: float) -> float:
    """Mach number Ma = U / c_s in lattice units."""
    return float(U) / lbm_cs()

def peclet(U: float, L: float, D: float) -> float:
    """Péclet number Pe = U L / D."""
    return (float(U) * float(L)) / (float(D) + 1e-15)

def damkohler(U: float, L: float, k: float, mode: str = "convective", D: float | None = None) -> float:
    """
    Damköhler number.
    - mode="convective": Da = k L / U
    - mode="diffusive" : Da = k L^2 / D  (requires D)
    """
    if mode == "convective":
        return (float(k) * float(L)) / (float(U) + 1e-15)
    elif mode == "diffusive":
        if D is None:
            raise ValueError("D must be provided for mode='diffusive'")
        return float(k) * (float(L) ** 2) / (float(D) + 1e-15)
    else:
        raise ValueError("mode must be 'convective' or 'diffusive'")

def steering_number(theta: float, grad_m_norm: float, lam: float) -> float:
    """Steering number Si = θ ||∇m|| / λ."""
    return (float(theta) * float(grad_m_norm)) / (float(lam) + 1e-15)

def void_number(Lambda: float, Theta: float, Gamma: float) -> float:
    """Π_void = (Λ · Θ) / Γ — void re-organization pressure."""
    return (float(Lambda) * float(Theta)) / (float(Gamma) + 1e-15)

def soft_clip(x, lo, hi):
    """Elementwise clamp to [lo, hi]."""
    return np.minimum(np.maximum(x, lo), hi)

__all__ = [
    "lbm_cs",
    "lbm_viscosity_from_tau",
    "reynolds_lbm",
    "mach_lbm",
    "peclet",
    "damkohler",
    "steering_number",
    "void_number",
    "soft_clip",
]