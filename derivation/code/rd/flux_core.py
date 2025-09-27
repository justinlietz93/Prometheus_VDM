#!/usr/bin/env python3
"""
Flux-form diffusion update (antisymmetric edge fluxes) for RD PDE:

  ∂t φ = D ∇² φ,  with edge fluxes on a regular grid:

    F_ij = - (D/a) (φ_j - φ_i),   F_ij = -F_ji
    φ_i^{n+1} = φ_i^{n} - (Δt/a) Σ_{j∈N(i)} F_ij

This module implements conservative updates via discrete divergence of fluxes.
With periodic or homogeneous Neumann BCs and f ≡ 0, the total mass Σ_i φ_i
is conserved to machine precision (up to floating round-off), matching Lemma F.1.

Scope:
- Regular Cartesian grids in 1D and 2D (NumPy). Extension to 3D is straightforward.
- Periodic and homogeneous Neumann (no-flux) BCs supported.
- Vectorized, no Python-side global schedulers; pure local stencils.

Runtime policy:
- Derivation/validation only. Keep observability read-only.
- No scans in fum_rt/core or maps are introduced here (this is under derivation/).

Author: Justin K. Lietz
"""

from __future__ import annotations
from typing import Tuple, Literal, Optional
import numpy as np

BC = Literal["periodic", "neumann"]


def _divergence_from_flux_1d(F_right: np.ndarray, a: float) -> np.ndarray:
    """
    Compute -∂x F using right-face fluxes F_right located on edges between i and i+1.

    Cell-centered divergence with periodic wrap assumed by caller when needed:
      divF[i] = (F_right[i] - F_right[i-1]) / a
    """
    # F_right shape: (N,) faces between i and i+1; face i is between i and i+1
    return (F_right - np.roll(F_right, 1)) / a


def _divergence_from_flux_2d(Fx: np.ndarray, Fy: np.ndarray, a: float) -> np.ndarray:
    """
    Compute -∇·F using face-centered fluxes Fx, Fy:
      Fx[i, j] is flux on the face between (i, j) and (i, j+1) (east face),
      Fy[i, j] is flux on the face between (i, j) and (i+1, j) (north face).

    Cell-centered divergence (i,j):
      divF[i, j] = (Fx[i, j] - Fx[i, j-1]) / a + (Fy[i, j] - Fy[i-1, j]) / a
    """
    div_x = (Fx - np.roll(Fx, 1, axis=1)) / a
    div_y = (Fy - np.roll(Fy, 1, axis=0)) / a
    return div_x + div_y


def flux_update_periodic(phi: np.ndarray, D: float, dt: float, a: float) -> np.ndarray:
    """
    Conservative flux-form update with periodic BCs (1D or 2D).

    Parameters
    ----------
    phi : np.ndarray
        Field values at cell centers. Shape (N,) or (Ny, Nx).
    D : float
        Diffusion coefficient (L^2 / T).
    dt : float
        Time step (T).
    a : float
        Grid spacing (L), uniform.

    Returns
    -------
    phi_next : np.ndarray
        Updated field, same shape as phi.
    """
    if phi.ndim == 1:
        # Right-face flux between i and i+1 with periodic wrap:
        # F_right[i] between cell i and i+1 (east face)
        phi_right = np.roll(phi, -1)
        F_right = -(D / a) * (phi_right - phi)
        divF = _divergence_from_flux_1d(F_right, a)
        return phi - dt * divF

    if phi.ndim == 2:
        # East face fluxes (Fx): faces between (i,j) and (i,j+1)
        phi_east = np.roll(phi, -1, axis=1)
        Fx = -(D / a) * (phi_east - phi)
        # North face fluxes (Fy): faces between (i,j) and (i+1,j)
        phi_north = np.roll(phi, -1, axis=0)
        Fy = -(D / a) * (phi_north - phi)
        divF = _divergence_from_flux_2d(Fx, Fy, a)
        return phi - dt * divF

    raise ValueError("flux_update_periodic: only 1D or 2D arrays are supported.")


def flux_update_neumann(phi: np.ndarray, D: float, dt: float, a: float) -> np.ndarray:
    """
    Conservative flux-form update with homogeneous Neumann (no-flux) BCs (1D or 2D).

    Implementation uses zero normal flux at boundaries:
      - 1D: F_left[0] = F_right[N-1] = 0
      - 2D: Fx[:, -1] = Fx[:, -1] is the right boundary face: set to 0,
            Fx[:, -1] contributes as east face of last column; Fx[:, -1] = 0.
            Similarly for left boundary Fx[:, -1] used via roll; we handle explicitly.
            For y, set F at top/bottom boundary faces to 0.

    Parameters
    ----------
    phi : np.ndarray
        Field values at cell centers. Shape (N,) or (Ny, Nx).
    D : float
        Diffusion coefficient (L^2 / T).
    dt : float
        Time step (T).
    a : float
        Grid spacing (L), uniform.

    Returns
    -------
    phi_next : np.ndarray
        Updated field, same shape as phi.
    """
    if phi.ndim == 1:
        N = phi.shape[0]
        # compute right-face fluxes for interior faces i=0..N-2
        F_right = np.zeros_like(phi)
        dphi_right = phi[1:] - phi[:-1]
        F_right[:-1] = -(D / a) * dphi_right
        # boundary faces (no-flux): F_right[-1] corresponds to face N-1 | out → 0
        F_right[-1] = 0.0
        # divergence: (F_right[i] - F_right[i-1]) / a, with F_right[-1] = 0 (no-flux at left out of 0)
        F_left_shifted = np.roll(F_right, 1)
        F_left_shifted[0] = 0.0  # no-flux at left boundary
        divF = (F_right - F_left_shifted) / a
        return phi - dt * divF

    if phi.ndim == 2:
        Ny, Nx = phi.shape
        Fx = np.zeros_like(phi)
        Fy = np.zeros_like(phi)
        # Interior east faces j=0..Nx-2
        dphi_east = phi[:, 1:] - phi[:, :-1]
        Fx[:, :-1] = -(D / a) * dphi_east
        Fx[:, -1] = 0.0  # no-flux at right boundary face
        # Interior north faces i=0..Ny-2
        dphi_north = phi[1:, :] - phi[:-1, :]
        Fy[:-1, :] = -(D / a) * dphi_north
        Fy[-1, :] = 0.0  # no-flux at top boundary face

        # Divergence with explicit boundary handling:
        # div_x = (Fx[i,j] - Fx[i, j-1]) / a with Fx[:, -1] defined, and Fx[:, -1] as east faces of last col
        Fx_west = np.zeros_like(Fx)
        Fx_west[:, 1:] = Fx[:, :-1]
        Fx_west[:, 0] = 0.0  # no-flux at left boundary face
        div_x = (Fx - Fx_west) / a

        Fy_south = np.zeros_like(Fy)
        Fy_south[1:, :] = Fy[:-1, :]
        Fy_south[0, :] = 0.0  # no-flux at bottom boundary face
        div_y = (Fy - Fy_south) / a

        divF = div_x + div_y
        return phi - dt * divF

    raise ValueError("flux_update_neumann: only 1D or 2D arrays are supported.")


def step_diffusion_flux(phi: np.ndarray, D: float, dt: float, a: float, bc: BC = "periodic") -> np.ndarray:
    """
    Single diffusion step via flux-form update under selected BC.

    Parameters
    ----------
    phi : np.ndarray
        Field values at cell centers (1D or 2D).
    D : float
        Diffusion constant.
    dt : float
        Time step.
    a : float
        Grid spacing.
    bc : {"periodic","neumann"}
        Boundary condition.

    Returns
    -------
    phi_next : np.ndarray
    """
    if bc == "periodic":
        return flux_update_periodic(phi, D, dt, a)
    elif bc == "neumann":
        return flux_update_neumann(phi, D, dt, a)
    else:
        raise ValueError(f"Unknown bc='{bc}'")


def mass(phi: np.ndarray, a: float) -> float:
    """
    Compute discrete mass ∑ φ_i a^d for regular grids.
    """
    d = phi.ndim
    cell_vol = (a ** d)
    return float(np.sum(phi) * cell_vol)


def _laplacian_periodic(phi: np.ndarray, a: float) -> np.ndarray:
    """
    Reference periodic Laplacian (for testing equivalence): ∇²_h φ using standard stencil.
    """
    if phi.ndim == 1:
        return (np.roll(phi, -1) + np.roll(phi, 1) - 2.0 * phi) / (a * a)
    if phi.ndim == 2:
        north = np.roll(phi, -1, axis=0)
        south = np.roll(phi,  1, axis=0)
        east  = np.roll(phi, -1, axis=1)
        west  = np.roll(phi,  1, axis=1)
        return (north + south + east + west - 4.0 * phi) / (a * a)
    raise ValueError("Only 1D/2D supported in test Laplacian.")


def verify_mass_conservation(phi: np.ndarray, D: float, dt: float, a: float, bc: BC = "periodic", tol: float = 1e-12) -> Tuple[float, float, float]:
    """
    Perform one flux-form step and report (m0, m1, |m1-m0|).

    Returns
    -------
    (m0, m1, drift)
    """
    m0 = mass(phi, a)
    phi1 = step_diffusion_flux(phi, D, dt, a, bc=bc)
    m1 = mass(phi1, a)
    return m0, m1, abs(m1 - m0)


def verify_equivalence_with_laplacian(phi: np.ndarray, D: float, dt: float, a: float, bc: BC = "periodic", tol: float = 1e-12) -> float:
    """
    For periodic BCs, check that flux-form update equals standard explicit Laplacian update:
      φ^{n+1} = φ^n + D dt ∇²_h φ^n
    Returns max absolute difference.
    """
    if bc != "periodic":
        raise ValueError("Equivalence test is implemented for periodic BC only.")
    phi_flux = step_diffusion_flux(phi, D, dt, a, bc="periodic")
    phi_lap = phi + D * dt * _laplacian_periodic(phi, a)
    return float(np.max(np.abs(phi_flux - phi_lap)))


if __name__ == "__main__":
    # Smoke and conservation tests
    rng = np.random.default_rng(42)

    # 1D periodic
    N = 257
    a = 1.0
    D = 0.5
    dt = 0.1
    phi = rng.normal(size=N)
    m0, m1, drift = verify_mass_conservation(phi, D, dt, a, bc="periodic")
    print("[1D periodic] mass drift:", drift)
    assert drift < 1e-12

    diff = verify_equivalence_with_laplacian(phi, D, dt, a, bc="periodic")
    print("[1D periodic] flux vs laplacian max|diff|:", diff)
    assert diff < 1e-12

    # 2D periodic
    Ny, Nx = 129, 193
    phi2 = rng.normal(size=(Ny, Nx))
    m0, m1, drift = verify_mass_conservation(phi2, D, dt, a, bc="periodic")
    print("[2D periodic] mass drift:", drift)
    assert drift < 1e-12

    # 1D Neumann
    phi1 = rng.normal(size=N)
    m0, m1, drift = verify_mass_conservation(phi1, D, dt, a, bc="neumann")
    print("[1D neumann] mass drift:", drift)
    assert drift < 1e-12

    # 2D Neumann
    phi2n = rng.normal(size=(Ny, Nx))
    m0, m1, drift = verify_mass_conservation(phi2n, D, dt, a, bc="neumann")
    print("[2D neumann] mass drift:", drift)
    assert drift < 1e-12

    print("flux_core: OK")