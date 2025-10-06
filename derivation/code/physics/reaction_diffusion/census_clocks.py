#!/usr/bin/env python3
"""
Asynchronous census engine (runtime-only, RD regime)
- Local hazard clocks (no external scheduler)
- Exact reaction substep at fired sites (logistic closed-form)
- Conservative, antisymmetric flux diffusion applied locally to fired sites
- Optional discrete-gradient integrator available separately

PDE (RD):
    ∂t φ = D ∇² φ + f(φ),  f(φ) = r φ - u φ^2 - λ φ^3

Hazard (per site):
    h_i := | D Δ_h φ_i + f(φ_i) |

Clock update:
    c_i ← c_i + h_i Δt
    if c_i ≥ 1: site i fires with microstep δt_i := θ / h_i, then c_i ← c_i − 1

Reaction (exact at fired sites):
    W^{+} = ( r W e^{r δt_i} ) / ( u W (e^{r δt_i} − 1) + r )

Diffusion (local flux transfers from fired sites only):
    For each fired i and each neighbor j∈N(i):
        F_{ij} = - (D/a) (φ_j − φ_i) = -F_{ji}
        φ_i ← φ_i − (δt_i/a) F_{ij}
        φ_j ← φ_j + (δt_i/a) F_{ij}
    (Mass conserved exactly when f≡0 and BCs are periodic/Neumann.)

BCs supported:
- "periodic": wraparound neighbors on a regular grid (1D/2D)
- "neumann": homogeneous no-flux (edge faces carry zero flux)

This module is derivation/validation-side only. No scans in fum_rt/core or maps/.

Author: Justin K. Lietz
"""

from __future__ import annotations
from typing import Tuple, Literal, Optional, Dict
import numpy as np

from .reaction_exact import reaction_exact_step
from .discrete_gradient import (
    laplacian_periodic, laplacian_neumann, f_react
)

BC = Literal["periodic", "neumann"]


def compute_hazard(phi: np.ndarray,
                   D: float, r: float, u: float, lam: float,
                   a: float, bc: BC = "periodic") -> np.ndarray:
    """
    h = | D Δ_h φ + f(φ) |
    """
    lap = laplacian_periodic if bc == "periodic" else laplacian_neumann
    return np.abs(D * lap(phi, a) + f_react(phi, r, u, lam))


def _flux_faces_periodic(phi: np.ndarray, D: float, a: float) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Face-centered fluxes for periodic grids.
    1D: returns (F_right, None), where F_right[i] between cell i and i+1 (wrap at end)
    2D: returns (Fx, Fy), east and north faces aligned with cell indices
    """
    if phi.ndim == 1:
        phi_right = np.roll(phi, -1)
        F_right = -(D / a) * (phi_right - phi)
        return F_right, None

    if phi.ndim == 2:
        phi_east = np.roll(phi, -1, axis=1)
        Fx = -(D / a) * (phi_east - phi)  # east faces
        phi_north = np.roll(phi, -1, axis=0)
        Fy = -(D / a) * (phi_north - phi)  # north faces
        return Fx, Fy

    raise ValueError("Only 1D or 2D phi supported.")


def _flux_faces_neumann(phi: np.ndarray, D: float, a: float) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Face-centered fluxes for homogeneous Neumann BCs (zero normal flux).
    """
    if phi.ndim == 1:
        N = phi.shape[0]
        F_right = np.zeros_like(phi)
        dphi = phi[1:] - phi[:-1]
        F_right[:-1] = -(D / a) * dphi
        F_right[-1] = 0.0  # boundary
        return F_right, None

    if phi.ndim == 2:
        Ny, Nx = phi.shape
        Fx = np.zeros_like(phi)
        Fy = np.zeros_like(phi)
        # East faces interior
        Fx[:, :-1] = -(D / a) * (phi[:, 1:] - phi[:, :-1])
        Fx[:, -1] = 0.0
        # North faces interior
        Fy[:-1, :] = -(D / a) * (phi[1:, :] - phi[:-1, :])
        Fy[-1, :] = 0.0
        return Fx, Fy

    raise ValueError("Only 1D or 2D phi supported.")


def _local_flux_apply_1d(phi: np.ndarray, F_right: np.ndarray, a: float,
                         fired: np.ndarray, delta_t: np.ndarray, bc: BC) -> np.ndarray:
    """
    Apply local flux transfers from fired cells only in 1D.
    For each fired i:
      right face: t = (δt_i / a) * F_right[i]
        φ[i] -= t; φ[i+1] += t   (if periodic; if neumann and i==N-1, skip)
      left face:  t = (δt_i / a) * F_left(i) with F_left(i) = -(D/a)(φ[i-1]-φ[i]) = -F_right[i-1]
        φ[i] -= t; φ[i-1] += t   (if neumann and i==0, skip)
    """
    N = phi.shape[0]
    out = phi.copy()
    # mask and delta_t only where fired
    dt_masked = np.where(fired, delta_t, 0.0)

    # Right edge transfers
    t_right = (dt_masked / a) * F_right  # size N
    if bc == "periodic":
        out -= t_right
        out += np.roll(t_right, -1)
    else:
        # Neumann: last face is zero by construction; also no incoming from the left of i=0
        out -= t_right
        t_in = np.zeros_like(t_right)
        t_in[:-1] = t_right[:-1]  # transfer into i+1 for i=0..N-2
        out += t_in

    # Left edge transfers: use F_left(i) = -F_right[i-1]
    F_left = -np.roll(F_right, 1)
    t_left = (dt_masked / a) * F_left
    if bc == "periodic":
        out -= t_left
        out += np.roll(t_left, 1)
    else:
        out -= t_left
        t_in = np.zeros_like(t_left)
        t_in[1:] = t_left[1:]  # transfer into i-1 for i=1..N-1
        out += t_in

    return out


def _local_flux_apply_2d(phi: np.ndarray, Fx: np.ndarray, Fy: np.ndarray, a: float,
                         fired: np.ndarray, delta_t: np.ndarray, bc: BC) -> np.ndarray:
    """
    Apply local flux transfers from fired cells only in 2D.
    For each fired (i,j):
      East face:  t = (δt/a) * Fx[i,j];      φ[i,j] -= t; φ[i, j+1] += t
      West face:  t = (δt/a) * (-Fx[i,j-1]); φ[i,j] -= t; φ[i, j-1] += t
      North face: t = (δt/a) * Fy[i,j];      φ[i,j] -= t; φ[i+1, j] += t
      South face: t = (δt/a) * (-Fy[i-1,j]); φ[i,j] -= t; φ[i-1, j] += t
    """
    out = phi.copy()
    dt_masked = np.where(fired, delta_t, 0.0)

    # East contributions
    t_e = (dt_masked / a) * Fx
    if bc == "periodic":
        out -= t_e
        out += np.roll(t_e, -1, axis=1)
    else:
        out -= t_e
        t_in = np.zeros_like(t_e)
        t_in[:, :-1] = t_e[:, :-1]  # into j+1 up to Nx-2
        out += t_in

    # West contributions: need west-face flux seen from cell (i,j)
    Fx_west = np.roll(Fx, 1, axis=1)
    t_w = (dt_masked / a) * (-Fx_west)
    if bc == "periodic":
        out -= t_w
        out += np.roll(t_w, 1, axis=1)
    else:
        out -= t_w
        t_in = np.zeros_like(t_w)
        t_in[:, 1:] = t_w[:, 1:]  # into j-1 from j=1..end
        out += t_in

    # North contributions
    t_n = (dt_masked / a) * Fy
    if bc == "periodic":
        out -= t_n
        out += np.roll(t_n, -1, axis=0)
    else:
        out -= t_n
        t_in = np.zeros_like(t_n)
        t_in[:-1, :] = t_n[:-1, :]  # into i+1 up to Ny-2
        out += t_in

    # South contributions
    Fy_south = np.roll(Fy, 1, axis=0)
    t_s = (dt_masked / a) * (-Fy_south)
    if bc == "periodic":
        out -= t_s
        out += np.roll(t_s, 1, axis=0)
    else:
        out -= t_s
        t_in = np.zeros_like(t_s)
        t_in[1:, :] = t_s[1:, :]  # into i-1 from i=1..end
        out += t_in

    return out


def census_fire_step(phi: np.ndarray,
                     clocks: np.ndarray,
                     D: float, r: float, u: float, lam: float,
                     a: float, dt: float, theta: float,
                     bc: BC = "periodic") -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[str, np.ndarray]]:
    """
    Execute one census update:
      1) Build hazards h, update clocks, compute fired set and δt_i
      2) Apply exact reaction at fired sites
      3) Apply conservative local flux transfers from fired sites only

    Returns
    -------
    (phi_next, clocks_next, fired_mask, delta_t, flux_dict)
      flux_dict:
        1D: {"F_right": F_right}
        2D: {"Fx": Fx, "Fy": Fy}
    """
    assert theta > 0.0 and theta <= 1.0, "theta must be in (0,1]."
    # 1) hazard and clocks
    h = compute_hazard(phi, D, r, u, lam, a, bc=bc)
    clocks_acc = clocks + h * dt
    fired = clocks_acc >= 1.0
    delta_t = np.zeros_like(phi, dtype=phi.dtype)
    # Avoid divide-by-zero for fired sites with tiny h (degenerate), clamp h
    h_safe = np.where(fired, np.maximum(h, 1e-15), h)
    delta_t[fired] = theta / h_safe[fired]
    clocks_next = np.where(fired, clocks_acc - 1.0, clocks_acc)

    # 2) exact reaction at fired sites (broadcastable dt; non-fired get dt=0)
    phi_r = reaction_exact_step(phi, r=r, u=u, dt=delta_t)

    # 3) flux transfers from fired sites only
    if bc == "periodic":
        Fx, Fy = _flux_faces_periodic(phi_r, D, a)
    else:
        Fx, Fy = _flux_faces_neumann(phi_r, D, a)

    if phi.ndim == 1:
        phi_next = _local_flux_apply_1d(phi_r, Fx, a, fired, delta_t, bc)
        flux = {"F_right": Fx}
    elif phi.ndim == 2:
        assert Fy is not None
        phi_next = _local_flux_apply_2d(phi_r, Fx, Fy, a, fired, delta_t, bc)
        flux = {"Fx": Fx, "Fy": Fy}
    else:
        raise ValueError("Only 1D/2D fields supported.")

    return phi_next, clocks_next, fired, delta_t, flux


if __name__ == "__main__":
    # Smoke test: conservation with f≡0 (set r=u=lam=0) under periodic
    rng = np.random.default_rng(1)
    D = 0.5; r = 0.0; u = 0.0; lam = 0.0; a = 1.0; dt = 0.1; theta = 0.7
    phi = rng.standard_normal((65, 97))
    clocks = np.zeros_like(phi)

    m0 = float(np.sum(phi) * (a**phi.ndim))
    for _ in range(5):
        phi, clocks, fired, delta_t, flux = census_fire_step(
            phi, clocks, D, r, u, lam, a, dt, theta, bc="periodic"
        )
    m1 = float(np.sum(phi) * (a**phi.ndim))
    print("mass drift (periodic, f=0):", m1 - m0)
    assert abs(m1 - m0) < 1e-10

    # Basic fire rate sanity
    print("fired fraction (approx):", np.mean(fired))
    print("census_clocks: OK")