"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Condensation and spectrum (diagonal-λ baseline) for the finite-tube FUM scalar EFT.

This module implements a minimal, numerically stable first pass of Section 6–7 in
[derivation/finite_tube_mode_analysis.md](derivation/finite_tube_mode_analysis.md:1):
- Build diagonal quartic couplings N4_ℓ ≈ λ ∫ r dr dθ u_ℓ^4 (projecting λ φ^4 onto each mode)
- Find condensate amplitudes v_ℓ by minimizing V_eff^{tube} ≈ ½ m_ℓ^2 v_ℓ^2 + ¼ N4_ℓ v_ℓ^4
- Compute post-condensation mass matrix in the diagonal approximation M^2_ℓ ≈ m_ℓ^2 + 3 N4_ℓ v_ℓ^2
- Scan E(R) = E_bg(R) + V_eff^{tube}(v_ℓ(R)) over R to locate minima (Bordag Fig. 5 analogue)

Caveats:
- This is the "diagonal-λ" baseline: N4 couplings are approximated as diagonal in mode index.
  Off-diagonal overlap terms N4(ℓ_i) are set to zero for simplicity/robustness.
- The integral for N4_ℓ uses u_ℓ(r) normalized with u_ℓ(R) = 1 from
  [fum_rt/physics/cylinder_modes.py](fum_rt/physics/cylinder_modes.py:1).

Equations:
- Radial mode spectrum (κ-roots) and u_ℓ(r) are from the cylinder solver; masses:
    m_ℓ^2(R) = - c^2 κ_ℓ^2(R).
- Diagonal quartic projection (per mode):
    N4_ℓ(R) = λ ∫_0^∞ r dr ∫_0^{2π} dθ [u_ℓ(r)]^4 = (2π) λ ∫_0^∞ r [u_ℓ(r)]^4 dr.

- Condensate amplitude (tree-level, diagonal):
    v_ℓ^2 = max(0, - m_ℓ^2 / N4_ℓ), else 0 if m_ℓ^2 ≥ 0.

- Post-condensation mass eigenvalues (diagonal baseline):
    M_ℓ^2 = m_ℓ^2 + 3 N4_ℓ v_ℓ^2.

References:
- [derivation/finite_tube_mode_analysis.md](derivation/finite_tube_mode_analysis.md:1)
- [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:125-193)
- [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:117-134)

Author: Justin K. Lietz
Date: 2025-08-09
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .cylinder_modes import compute_kappas, mode_functions


@dataclass
class ModeEntry:
    ell: int
    kappa: float
    k_in: float
    k_out: float


def _radial_integral_u4(
    R: float,
    u: Callable[[float], float],
    r_max_factor: float = 10.0,
    dr: float = 1e-2,
) -> float:
    """
    Compute integral I = ∫_0^∞ r [u(r)]^4 dr by truncating at r_max = r_max_factor * R.

    Args:
      R: tube radius (sets normalization u(R) = 1 from mode_functions)
      u: callable radial mode function u(r)
      r_max_factor: how many radii to integrate outwards (default 10)
      dr: radial step

    Returns:
      I ~ ∫_0^{r_max} r u(r)^4 dr (float)
    """
    r_max = max(R * float(r_max_factor), 5.0 * R)
    if r_max <= 0.0:
        return 0.0
    # Create grid including R and up to r_max
    n_steps = max(10, int(np.ceil(r_max / dr)))
    rs = np.linspace(0.0, r_max, n_steps, dtype=np.float64)
    vals = []
    for r in rs:
        try:
            val = float(u(float(r)))
            vals.append((r * (val ** 4)))
        except Exception:
            vals.append(0.0)
    vals = np.asarray(vals, dtype=np.float64)
    I = float(np.trapz(vals, rs))
    return I


def build_quartic_diagonal(
    R: float,
    modes: Sequence[ModeEntry],
    lam: float,
    c: float,
) -> Dict[int, float]:
    """
    Build diagonal quartic coefficients N4_ℓ ≈ (2π) λ ∫ r u_ℓ^4 dr for each provided mode.

    Args:
      R: radius
      modes: list of ModeEntry (ell, kappa, k_in, k_out)
      lam: quartic λ > 0
      c: wave speed

    Returns:
      mapping ell -> N4_ell (float >= 0)
    """
    N4: Dict[int, float] = {}
    for m in modes:
        fns = mode_functions(R=R, root={"ell": float(m.ell), "k_in": m.k_in, "k_out": m.k_out})
        u = fns["u"]
        I = _radial_integral_u4(R, u)  # ∫ r u^4 dr
        N4_ell = float(2.0 * np.pi * lam * I)
        # numerical guard
        if not np.isfinite(N4_ell) or N4_ell < 0.0:
            N4_ell = 0.0
        N4[int(m.ell)] = N4_ell
    return N4


def find_condensate_diagonal(
    R: float,
    modes: Sequence[ModeEntry],
    N4: Dict[int, float],
    c: float,
) -> Dict[int, float]:
    """
    Find condensate amplitudes v_ℓ in the diagonal approximation:
      v_ℓ^2 = max(0, - m_ℓ^2 / N4_ℓ), m_ℓ^2 = - c^2 κ_ℓ^2, so v_ℓ^2 = c^2 κ_ℓ^2 / N4_ℓ if N4_ℓ>0.

    Returns:
      mapping ell -> v_ell (float)
    """
    v: Dict[int, float] = {}
    for m in modes:
        ell = int(m.ell)
        N4_ell = float(N4.get(ell, 0.0))
        m2 = - (c ** 2) * (m.kappa ** 2)
        if N4_ell > 0.0 and m2 < 0.0:
            v2 = (c ** 2) * (m.kappa ** 2) / N4_ell
            v[ell] = float(np.sqrt(max(0.0, v2)))
        else:
            v[ell] = 0.0
    return v


def mass_matrix_diagonal(
    modes: Sequence[ModeEntry],
    N4: Dict[int, float],
    v: Dict[int, float],
    c: float,
) -> Dict[int, float]:
    """
    Post-condensation mass eigenvalues (diagonal baseline):
      M_ℓ^2 = m_ℓ^2 + 3 N4_ℓ v_ℓ^2,  with  m_ℓ^2 = - c^2 κ_ℓ^2.

    Returns:
      mapping ell -> M2_ell (float)
    """
    M2: Dict[int, float] = {}
    for m in modes:
        ell = int(m.ell)
        m2 = - (c ** 2) * (m.kappa ** 2)
        N4_ell = float(N4.get(ell, 0.0))
        v_ell = float(v.get(ell, 0.0))
        M2_ell = m2 + 3.0 * N4_ell * (v_ell ** 2)
        M2[ell] = float(M2_ell)
    return M2


def tube_energy_diagonal(
    modes: Sequence[ModeEntry],
    N4: Dict[int, float],
    v: Dict[int, float],
    c: float,
    E_bg: Optional[Callable[[float], float]] = None,
    R: Optional[float] = None,
) -> float:
    """
    E(R) = E_bg(R) + V_eff^{tube}(v_ℓ), diagonal baseline:
      V_eff ≈ Σ_ℓ [ ½ m_ℓ^2 v_ℓ^2 + ¼ N4_ℓ v_ℓ^4 ] with m_ℓ^2 = - c^2 κ_ℓ^2.

    Args:
      modes: list of ModeEntry
      N4: diag quartic map
      v: condensate amplitudes
      c: wave speed
      E_bg: optional background energy term E_bg(R)
      R: radius (passed to E_bg if provided)

    Returns:
      total energy (float)
    """
    V = 0.0
    for m in modes:
        ell = int(m.ell)
        m2 = - (c ** 2) * (m.kappa ** 2)
        v_ell = float(v.get(ell, 0.0))
        N4_ell = float(N4.get(ell, 0.0))
        V += 0.5 * m2 * (v_ell ** 2) + 0.25 * N4_ell * (v_ell ** 4)
    if E_bg is not None and R is not None:
        try:
            V += float(E_bg(float(R)))
        except Exception:
            pass
    return float(V)


def compute_modes_for_R(
    R: float,
    mu: float,
    c: float = 1.0,
    ell_max: int = 8,
) -> List[ModeEntry]:
    """
    Helper: compute ModeEntry list at fixed R using the cylinder solver.

    Returns:
      list of ModeEntry for ℓ = 0..ell_max, keeping the lowest κ-root per ℓ (if any).
    """
    roots = compute_kappas(R=R, mu=mu, c=c, ell_max=ell_max, num_brackets=256)
    # Option: pick at most one mode per ℓ (lowest κ)
    buckets: Dict[int, List[Dict[str, float]]] = {}
    for r in roots:
        ell = int(round(r.get("ell", 0.0)))
        buckets.setdefault(ell, []).append(r)
    modes: List[ModeEntry] = []
    for ell, lst in buckets.items():
        if not lst:
            continue
        lst_sorted = sorted(lst, key=lambda d: float(d["kappa"]))
        r0 = lst_sorted[0]
        modes.append(
            ModeEntry(
                ell=int(ell),
                kappa=float(r0["kappa"]),
                k_in=float(r0["k_in"]),
                k_out=float(r0["k_out"]),
            )
        )
    return sorted(modes, key=lambda m: m.ell)


def energy_scan(
    R_grid: Sequence[float],
    mu: float,
    lam: float,
    c: float = 1.0,
    ell_max: int = 8,
    E_bg: Optional[Callable[[float], float]] = None,
) -> Dict[str, np.ndarray]:
    """
    Scan E(R) across R_grid using the diagonal baseline.

    Args:
      R_grid: iterable of radii
      mu: tachyon scale (√(½) m_eff in the bounded EFT with m_eff = √2 μ)
      lam: quartic coupling λ > 0
      c: wave speed
      ell_max: max ℓ to consider (lowest root per ℓ)
      E_bg: optional background energy term E_bg(R)

    Returns:
      dict { 'R': np.array, 'E': np.array, 'min_R': float, 'min_E': float }
    """
    Rs = np.asarray(R_grid, dtype=np.float64)
    Es = np.full_like(Rs, np.nan, dtype=np.float64)
    for i, R in enumerate(Rs):
        try:
            modes = compute_modes_for_R(R=R, mu=mu, c=c, ell_max=ell_max)
            if not modes:
                Es[i] = np.nan
                continue
            N4 = build_quartic_diagonal(R=R, modes=modes, lam=lam, c=c)
            v = find_condensate_diagonal(R=R, modes=modes, N4=N4, c=c)
            E = tube_energy_diagonal(modes=modes, N4=N4, v=v, c=c, E_bg=E_bg, R=R)
            Es[i] = float(E)
        except Exception:
            Es[i] = np.nan
    # Find minimum over finite values
    mask = np.isfinite(Es)
    if not np.any(mask):
        return {"R": Rs, "E": Es, "min_R": float("nan"), "min_E": float("nan")}
    idx = int(np.nanargmin(Es))
    return {"R": Rs, "E": Es, "min_R": float(Rs[idx]), "min_E": float(Es[idx])}