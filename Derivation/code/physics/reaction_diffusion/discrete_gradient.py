#!/usr/bin/env python3
"""
Discrete-gradient (AVF-style) RD integrator ensuring Lyapunov monotonicity in practice.

PDE (dimensionless RD form):
    ∂t φ = D ∇² φ + f(φ),     f(φ) = r φ - u φ^2 - λ φ^3,
with Lyapunov functional
    L[φ] = ∫ ( D/2 |∇φ|^2 + V_hat(φ) ) dx,   with  V_hat'(φ) = -f(φ)
⇒  V_hat(φ) = - (r/2) φ^2 + (u/3) φ^3 + (λ/4) φ^4 + const.

AVF discrete step (Gonzalez/Quispel-McLaren style):
    (φ^{n+1} - φ^n)/Δt = D ∇²_h( (φ^{n+1}+φ^n)/2 ) + f_bar(φ^n, φ^{n+1})
with
    f_bar = - (V_hat(φ^{n+1}) - V_hat(φ^n)) / (φ^{n+1} - φ^n)   if φ^{n+1} ≠ φ^n,
    f_bar = f(φ^n)                                              otherwise.

This guarantees ΔL ≤ 0 in the ideal AVF scheme. Here we implement a fixed-point
solver for φ^{n+1}. For practical use: a few Picard iterations typically suffice.

Scope:
- 1D/2D regular Cartesian grids, periodic or homogeneous Neumann BCs.
- NumPy implementation (Derivation/validation only). No dense scans in fum_rt/core.

Author: Justin K. Lietz
"""

from __future__ import annotations
from typing import Tuple, Literal, Optional
import numpy as np

BC = Literal["periodic", "neumann"]


def V_hat(phi: np.ndarray, r: float, u: float, lam: float) -> np.ndarray:
    """V_hat(φ) with V_hat'(φ) = -f(φ) = -(r φ - u φ^2 - λ φ^3)."""
    return -0.5 * r * phi**2 + (u/3.0) * phi**3 + 0.25 * lam * phi**4


def f_react(phi: np.ndarray, r: float, u: float, lam: float) -> np.ndarray:
    """f(φ) = r φ - u φ^2 - λ φ^3."""
    return r * phi - u * phi**2 - lam * phi**3


def f_bar(phi_n: np.ndarray, phi_np1: np.ndarray, r: float, u: float, lam: float, eps: float = 1e-14) -> np.ndarray:
    """
    Discrete gradient of V_hat: f_bar = - (V_hat(φ^{n+1}) - V_hat(φ^n)) / (φ^{n+1} - φ^n).
    Fallback to f(φ^n) when difference is tiny.
    """
    dphi = phi_np1 - phi_n
    mask = np.abs(dphi) > eps
    out = np.empty_like(phi_n)
    if np.any(mask):
        dv = V_hat(phi_np1[mask], r, u, lam) - V_hat(phi_n[mask], r, u, lam)
        out[mask] = - dv / dphi[mask]
    if np.any(~mask):
        out[~mask] = f_react(phi_n[~mask], r, u, lam)
    return out


def laplacian_periodic(phi: np.ndarray, a: float) -> np.ndarray:
    """Centered periodic discrete Laplacian in 1D/2D."""
    if phi.ndim == 1:
        return (np.roll(phi, -1) + np.roll(phi, 1) - 2.0 * phi) / (a*a)
    if phi.ndim == 2:
        north = np.roll(phi, -1, axis=0)
        south = np.roll(phi,  1, axis=0)
        east  = np.roll(phi, -1, axis=1)
        west  = np.roll(phi,  1, axis=1)
        return (north + south + east + west - 4.0 * phi) / (a*a)
    raise ValueError("laplacian_periodic supports 1D or 2D only.")


def laplacian_neumann(phi: np.ndarray, a: float) -> np.ndarray:
    """
    Homogeneous Neumann Laplacian using mirrored boundaries (zero normal derivative).
    """
    if phi.ndim == 1:
        left  = np.empty_like(phi); right = np.empty_like(phi)
        left[0] = phi[0];           left[1:] = phi[:-1]
        right[-1] = phi[-1];        right[:-1] = phi[1:]
        return (left + right - 2.0 * phi) / (a*a)
    if phi.ndim == 2:
        north = np.empty_like(phi); south = np.empty_like(phi)
        east  = np.empty_like(phi); west  = np.empty_like(phi)
        north[0, :] = phi[0, :];               north[1:, :] = phi[:-1, :]
        south[-1, :] = phi[-1, :];             south[:-1, :] = phi[1:, :]
        east[:, -1]  = phi[:, -1];             east[:, :-1]  = phi[:, 1:]
        west[:, 0]   = phi[:, 0];              west[:, 1:]   = phi[:, :-1]
        return (north + south + east + west - 4.0 * phi) / (a*a)
    raise ValueError("laplacian_neumann supports 1D or 2D only.")


def grad_components(phi: np.ndarray, a: float, bc: BC = "periodic") -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute forward-difference gradient components (gx, gy) with BC handling.
    For 1D, returns (gx, None).
    """
    if phi.ndim == 1:
        if bc == "periodic":
            gx = (np.roll(phi, -1) - phi) / a
        else:
            gx = np.empty_like(phi)
            gx[:-1] = (phi[1:] - phi[:-1]) / a
            gx[-1]  = 0.0
        return gx, None
    if phi.ndim == 2:
        if bc == "periodic":
            gx = (np.roll(phi, -1, axis=1) - phi) / a
            gy = (np.roll(phi, -1, axis=0) - phi) / a
        else:
            gx = np.empty_like(phi); gy = np.empty_like(phi)
            gx[:, :-1] = (phi[:, 1:] - phi[:, :-1]) / a; gx[:, -1] = 0.0
            gy[:-1, :] = (phi[1:, :] - phi[:-1, :]) / a; gy[-1, :] = 0.0
        return gx, gy
    raise ValueError("grad_components supports 1D or 2D only.")


def energy_L(phi: np.ndarray, D: float, a: float, r: float, u: float, lam: float, bc: BC = "periodic") -> float:
    """
    Discrete Lyapunov functional:
        L = Σ cells [ D/2 |∇_h φ|^2 + V_hat(φ) ] a^d
    with ∇_h computed by forward differences (summation by parts matches Laplacian choices).
    """
    gx, gy = grad_components(phi, a, bc=bc)
    grad_sq = gx**2 if gy is None else gx**2 + gy**2
    cell = 0.5 * D * grad_sq + V_hat(phi, r, u, lam)
    d = phi.ndim
    return float(np.sum(cell) * (a**d))


def avf_step(phi: np.ndarray,
             D: float, r: float, u: float, lam: float,
             dt: float, a: float, bc: BC = "periodic",
             iters: int = 3) -> np.ndarray:
    """
    One AVF-style discrete-gradient step using Picard iterations.

    (φ^{n+1} - φ^n)/Δt = D ∇²_h( (φ^{n+1}+φ^n)/2 ) + f_bar(φ^n, φ^{n+1})

    Parameters
    ----------
    phi : ndarray
        Current field (1D or 2D).
    D, r, u, lam : float
        Model parameters.
    dt : float
        Time step.
    a : float
        Grid spacing.
    bc : {"periodic","neumann"}
        Boundary condition.
    iters : int
        Fixed-point iterations (small number sufficient in practice).

    Returns
    -------
    ndarray
        Next field φ^{n+1}.
    """
    lap = laplacian_periodic if bc == "periodic" else laplacian_neumann

    # Explicit Euler predictor
    phi_next = phi + dt * (D * lap(phi, a) + f_react(phi, r, u, lam))

    for _ in range(max(1, iters)):
        bar_phi = 0.5 * (phi_next + phi)
        fb = f_bar(phi, phi_next, r, u, lam)
        rhs = D * lap(bar_phi, a) + fb
        phi_next = phi + dt * rhs

    return phi_next


if __name__ == "__main__":
    # Smoke test: energy monotonicity (typical)
    rng = np.random.default_rng(0)
    a = 1.0; D = 0.5; r = 1.0; u = 0.25; lam = 0.0; dt = 0.1
    phi = rng.standard_normal((65, 97))
    L0 = energy_L(phi, D, a, r, u, lam, bc="periodic")
    phi1 = avf_step(phi, D, r, u, lam, dt, a, bc="periodic", iters=3)
    L1 = energy_L(phi1, D, a, r, u, lam, bc="periodic")
    print("ΔL =", L1 - L0)
    # In practice ΔL ≤ 0; allow tiny positive due to few Picard iters / round-off
    assert L1 - L0 <= 1e-10
    print("discrete_gradient: OK")