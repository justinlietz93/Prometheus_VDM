#!/usr/bin/env python3
# VDM dimensionless helpers (LBM + RD + memory steering)
"""
Dimensionless numbers and lattice-unit helpers used across VDM runners.

Overview
- This module centralizes formulas for common non-dimensional groups and lattice-BGK
    relationships so experiments remain consistent and easy to audit.
- It is pure (no I/O) and safe to import in any runner or test.

Assumptions and conventions
- Lattice units (LBM): Δx = Δt = 1 (when stated); D2Q9 BGK with speed of sound
    c_s = 1/sqrt(3). Kinematic viscosity in lattice units is ν = (τ - 0.5)/3.
- Dimensionless groups follow standard fluid/transport conventions.
- Small epsilons (1e-15) are added in denominators purely to avoid division-by-zero
    in edge cases; they do not change scaling for well-posed inputs.

Units (typical)
- U: velocity [m/s], L: length [m], D: diffusivity [m^2/s], ν: kinematic viscosity [m^2/s]
- τ (tau): lattice relaxation time [lattice time units]

Quick reference
- lbm_cs(): lattice sound speed c_s in lattice units.
- lbm_viscosity_from_tau(τ): ν = (τ − 0.5)/3 in lattice units (D2Q9 BGK).
- reynolds_lbm(U, L, τ): Re = U L / ν using ν from τ (lattice-unit analysis).
- mach_lbm(U): Ma = U / c_s in lattice units.
- peclet(U, L, D): Pe = U L / D.
- damkohler(...): convective Da = k L / U; diffusive Da = k L^2 / D.
- steering_number(θ, ||∇m||, λ): Si = θ ||∇m|| / λ (internal to VDM steering analyses).
- void_number(Λ, Θ, Γ): Π_void = (Λ · Θ) / Γ (internal VDM diagnostic).
"""
from __future__ import annotations
import numpy as np

SQRT3 = np.sqrt(3.0)

def lbm_cs() -> float:
    """Return the LBM lattice sound speed c_s in lattice units.

    Model: D2Q9 BGK (isothermal) where c_s = 1/sqrt(3).
    Units: [lattice length]/[lattice time] (dimensionless in the Δx=Δt=1 convention).
    """
    return 1.0 / SQRT3

def lbm_viscosity_from_tau(tau: float) -> float:
    """Compute kinematic viscosity ν from relaxation time τ in lattice units.

    Formula (D2Q9 BGK): ν = (τ − 0.5) / 3.
    Constraints: τ > 0.5 for positive viscosity; τ close to 0.5 approaches inviscid/unstable regimes.
    Returns: ν in lattice units.
    """
    return (float(tau) - 0.5) / 3.0

def reynolds_lbm(U: float, L: float, tau: float) -> float:
    """Compute Reynolds number Re from velocity U, length L, and lattice τ.

    Steps: ν = (τ − 0.5)/3, then Re = U L / ν.
    Units: U and L follow the chosen unit system; when using lattice units, U and L
    are in lattice units and ν matches lattice scaling.
    Edge cases: adds 1e-15 to ν to prevent division-by-zero.
    """
    nu = lbm_viscosity_from_tau(tau)
    return (float(U) * float(L)) / (nu + 1e-15)

def mach_lbm(U: float) -> float:
    """Compute Mach number Ma = U / c_s in lattice units.

    Validity: LBM typically assumes Ma ≲ 0.1 for weakly compressible flows.
    """
    return float(U) / lbm_cs()

def peclet(U: float, L: float, D: float) -> float:
    """Compute Péclet number Pe = U L / D.

    Interpretation: advection-to-diffusion ratio; large Pe implies advection-dominated transport.
    Edge cases: adds 1e-15 to D in the denominator to avoid division-by-zero.
    """
    return (float(U) * float(L)) / (float(D) + 1e-15)

def damkohler(U: float, L: float, k: float, mode: str = "convective", D: float | None = None) -> float:
    """Compute Damköhler number (reaction vs. transport timescales).

    Modes
    - convective: Da = k L / U (reaction time vs. advection time)
    - diffusive : Da = k L^2 / D (reaction time vs. diffusion time)

    Parameters
    - U: characteristic velocity (>0)
    - L: characteristic length (>0)
    - k: reaction rate (≥0)
    - D: diffusivity (required for mode="diffusive")

    Returns
    - Da (dimensionless). Raises ValueError if mode is not recognized or required D is missing.
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
    """Compute a VDM steering number Si = θ · ||∇m|| / λ.

    Context: Used in VDM "memory steering" analyses to compare control magnitude
    (θ · ||∇m||) against a regularization scale (λ). Larger Si implies stronger
    steering influence relative to the regularizer.
    """
    return (float(theta) * float(grad_m_norm)) / (float(lam) + 1e-15)

def void_number(Lambda: float, Theta: float, Gamma: float) -> float:
    """Compute Π_void = (Λ · Θ) / Γ — a VDM diagnostic for void re-organization pressure.

    Interpretation: proportional to the product (Λ · Θ) scaled by Γ; the exact
    physical mapping is domain-specific within VDM and is treated as a diagnostic ratio.
    """
    return (float(Lambda) * float(Theta)) / (float(Gamma) + 1e-15)

def soft_clip(x, lo, hi):
    """Elementwise clamp to the closed interval [lo, hi].

    Equivalent to min(max(x, lo), hi) applied pointwise over NumPy arrays or scalars.
    Useful for keeping fields within admissible bounds during diagnostics or plotting.
    """
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