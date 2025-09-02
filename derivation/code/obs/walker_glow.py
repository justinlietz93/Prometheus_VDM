#!/usr/bin/env python3
"""
Walker 'glow' observability channel (read-only).

Update rule (per census fire):
  M_i^{n+1} = M_i^{n} + α · 1{fire at i} + β · Σ_{j∈N(i)} |F_{ji}|

Where:
- 1{fire at i} is the indicator of a local event at site i (from census_clocks).
- F_{ji} is the incoming flux from neighbor j to i (antisymmetric: F_{ji} = -F_{ij}).
- α, β ≥ 0 are scalar weights.
- M never feeds back into dynamics (observability-only).

Inputs (from census step):
- fired: boolean mask of fired sites
- flux dict:
  * 1D: {"F_right": F_right}, where F_right[i] is flux on face (i → i+1)
  * 2D: {"Fx": Fx, "Fy": Fy}, east/north faces where Fx[y,x] is flux (x → x+1),
        and Fy[y,x] is flux (y → y+1)

BCs supported:
- "periodic": wraparound neighbors on a regular grid (1D/2D)
- "neumann": homogeneous no-flux; boundary incoming from outside is zero

Author: Justin K. Lietz
"""

from __future__ import annotations
from typing import Optional, Dict, Literal
import numpy as np

BC = Literal["periodic", "neumann"]


def update_glow(M: np.ndarray,
                fired: np.ndarray,
                flux: Dict[str, np.ndarray],
                alpha: float,
                beta: float,
                bc: BC = "periodic") -> np.ndarray:
    """
    Update glow intensity M given fired mask and local flux magnitudes.

    Parameters
    ----------
    M : np.ndarray
        Current intensity (same shape as fired).
    fired : np.ndarray (bool)
        Fired mask from census engine.
    flux : dict
        1D: {"F_right": ndarray}
        2D: {"Fx": ndarray, "Fy": ndarray}
    alpha : float
        Weight for fire indicator.
    beta : float
        Weight for incoming flux magnitude.
    bc : {"periodic","neumann"}
        Boundary condition for incoming estimation.

    Returns
    -------
    np.ndarray
        Next intensity field.
    """
    M = np.array(M, copy=True)
    fired = np.array(fired, dtype=bool, copy=False)

    if M.shape != fired.shape:
        raise ValueError("M and fired must have the same shape.")

    if M.ndim == 1:
        F_right = flux.get("F_right", None)
        if F_right is None:
            raise ValueError("1D glow update requires flux['F_right'].")

        if bc == "periodic":
            incoming = np.abs(np.roll(F_right, 1)) + np.abs(F_right)
        else:
            # Neumann: no incoming from outside; drop wrap terms
            incoming = np.empty_like(F_right)
            incoming[0] = np.abs(F_right[0])            # from right face only
            incoming[1:-1] = np.abs(F_right[1:-1]) + np.abs(F_right[:-2])
            incoming[-1] = np.abs(F_right[-2])          # from left interior face only

        M_next = M + alpha * fired.astype(M.dtype) + beta * incoming.astype(M.dtype)
        return M_next

    if M.ndim == 2:
        Fx = flux.get("Fx", None)
        Fy = flux.get("Fy", None)
        if Fx is None or Fy is None:
            raise ValueError("2D glow update requires flux['Fx'] and flux['Fy'].")

        if bc == "periodic":
            # Incoming from east and west:
            incoming_x = np.abs(np.roll(Fx, 1, axis=1)) + np.abs(-Fx)
            # Incoming from north and south:
            incoming_y = np.abs(np.roll(Fy, 1, axis=0)) + np.abs(-Fy)
        else:
            # Neumann: zero-flux at boundaries
            incoming_x = np.zeros_like(Fx)
            incoming_y = np.zeros_like(Fy)
            # West incoming (from j-1): |Fx[:, j-1]|, j>=1
            incoming_x[:, 1:] += np.abs(Fx[:, :-1])
            # East incoming (from j+1): |-Fx[:, j]| = |Fx[:, j]|
            incoming_x[:, :]  += np.abs(-Fx)
            # South incoming (from i-1): |Fy[i-1, :]|, i>=1
            incoming_y[1:, :] += np.abs(Fy[:-1, :])
            # North incoming (from i+1): |-Fy[i, :]| = |Fy[i, :]|
            incoming_y[:, :]  += np.abs(-Fy)

        incoming = incoming_x + incoming_y
        M_next = M + alpha * fired.astype(M.dtype) + beta * incoming.astype(M.dtype)
        return M_next

    raise ValueError("update_glow supports 1D or 2D arrays only.")


if __name__ == "__main__":
    # Smoke tests
    rng = np.random.default_rng(123)
    alpha, beta = 0.5, 0.1

    # 1D periodic
    N = 16
    M = np.zeros(N, dtype=np.float64)
    fired = rng.random(N) < 0.2
    F_right = rng.normal(size=N)
    M1 = update_glow(M, fired, {"F_right": F_right}, alpha, beta, bc="periodic")
    print("1D periodic M sum:", float(M1.sum()))

    # 2D periodic
    Ny, Nx = 8, 10
    M2 = np.zeros((Ny, Nx), dtype=np.float64)
    fired2 = rng.random((Ny, Nx)) < 0.2
    Fx = rng.normal(size=(Ny, Nx))
    Fy = rng.normal(size=(Ny, Nx))
    M2n = update_glow(M2, fired2, {"Fx": Fx, "Fy": Fy}, alpha, beta, bc="periodic")
    print("2D periodic M sum:", float(M2n.sum()))
    print("walker_glow: OK")