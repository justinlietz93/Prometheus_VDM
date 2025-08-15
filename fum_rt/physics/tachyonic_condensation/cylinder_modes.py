"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Finite-radius cylindrical (tube) mode solver for the FUM scalar EFT.

This implements the radial eigenvalue condition described in
[derivation/finite_tube_mode_analysis.md](derivation/finite_tube_mode_analysis.md:1).

Equation of motion for small fluctuations about a piecewise-constant background:
    (∂_t^2 - c^2 ∇_⊥^2 - c^2 ∂_z^2) φ + m^2(r) φ = 0
with
    m_in^2 = -μ^2     for r < R  (tachyonic interior)
    m_out^2 =  2μ^2   for r > R  (massive exterior)
and wave speed c (dimensionless units; see [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:117-134)).

Using separation φ ∝ e^{-i ω t} e^{i k z} u_ℓ(r) e^{iℓθ} and defining
    ω^2 - c^2 k^2 = - c^2 κ^2,
the radial equation reduces (piecewise) to modified Bessel equations. The matching at r = R yields
the secular equation for each angular momentum ℓ:

    (κ_in / κ_out) [I'_ℓ(κ_in R) / I_ℓ(κ_in R)] + [K'_ℓ(κ_out R) / K_ℓ(κ_out R)] = 0

with
    κ_in^2  = μ^2 / c^2 - κ^2,
    κ_out^2 = κ^2 + 2μ^2 / c^2.

Tachyonic (unstable) modes correspond to κ^2 > 0 (so that at k=0, ω^2 = - c^2 κ^2 < 0).

APIs:
- compute_kappas(R, mu, c=1.0, ell_max=12, kappa_max=None, num_brackets=512, tol=1e-8)
    Returns a list of dicts { 'ell', 'kappa', 'k_in', 'k_out' }.

- mode_functions(R, root)
    Returns a dict with 'u_in(r)', 'u_out(r)', and 'u(r)' callables normalized so u(R) = 1.

References:
- [derivation/finite_tube_mode_analysis.md](derivation/finite_tube_mode_analysis.md:1)
- [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:125-193)
- [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:117-134)

Author: Justin K. Lietz
Date: 2025-08-09
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

try:
    from scipy import optimize, special
    _HAVE_SCIPY = True
except Exception:
    _HAVE_SCIPY = False
    special = None
    optimize = None


_EPS = 1e-14


def _iv(nu: int, x: float) -> float:
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")
    return float(special.iv(nu, x))


def _kv(nu: int, x: float) -> float:
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")
    return float(special.kv(nu, x))


def _ivp(nu: int, x: float) -> float:
    """
    Derivative d/dx I_ν(x). Prefer special.ivp if available; otherwise use
    the stable relation d/dx I_ν = (I_{ν-1} + I_{ν+1})/2.
    """
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")
    if hasattr(special, "ivp"):
        return float(special.ivp(nu, x))
    # Fallback for older scipy: symmetric finite-difference via recurrence
    return 0.5 * (special.iv(nu - 1, x) + special.iv(nu + 1, x))


def _kvp(nu: int, x: float) -> float:
    """
    Derivative d/dx K_ν(x). Prefer special.kvp; otherwise use
    d/dx K_ν = - (K_{ν-1} + K_{ν+1})/2.
    """
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")
    if hasattr(special, "kvp"):
        return float(special.kvp(nu, x))
    return -0.5 * (special.kv(nu - 1, x) + special.kv(nu + 1, x))


def _dlnI(nu: int, x: float) -> float:
    """Compute (I'_ν / I_ν)(x) with basic guarding."""
    x = float(max(x, _EPS))
    Iv = _iv(nu, x)
    if abs(Iv) < _EPS:
        return np.sign(_ivp(nu, x)) * 1e6  # large magnitude surrogate
    return _ivp(nu, x) / Iv


def _dlnK(nu: int, x: float) -> float:
    """Compute (K'_ν / K_ν)(x) with basic guarding."""
    x = float(max(x, _EPS))
    Kv = _kv(nu, x)
    if abs(Kv) < _EPS:
        return -np.sign(_kvp(nu, x)) * 1e6  # large magnitude surrogate (note K decays)
    return _kvp(nu, x) / Kv


def _secular_value(kappa: float, ell: int, R: float, mu: float, c: float) -> float:
    """
    Evaluate the secular equation value:
        f(κ) = (κ_in/κ_out) * (I'_ℓ / I_ℓ)(κ_in R) + (K'_ℓ / K_ℓ)(κ_out R)
    Roots f(κ)=0 provide allowed κ for given (ℓ, R, μ, c).
    Valid only when κ_in^2 >= 0.
    """
    if kappa <= 0.0 or R <= 0.0 or mu <= 0.0 or c <= 0.0:
        return np.nan
    cinv = 1.0 / c
    k_in2 = (mu * cinv) ** 2 - kappa ** 2
    if k_in2 <= 0.0:
        # Outside the domain where interior solution uses I_ℓ with real argument.
        return np.nan
    k_out2 = kappa ** 2 + 2.0 * (mu * cinv) ** 2
    k_in = float(np.sqrt(k_in2))
    k_out = float(np.sqrt(k_out2))
    x_in = k_in * R
    x_out = k_out * R

    try:
        val = (k_in / k_out) * _dlnI(ell, x_in) + _dlnK(ell, x_out)
    except Exception:
        return np.nan
    # Guard absurd values that destabilize sign checks
    if not np.isfinite(val) or abs(val) > 1e12:
        return np.nan
    return float(val)


def _find_roots_for_ell(
    ell: int,
    R: float,
    mu: float,
    c: float,
    kappa_max: Optional[float],
    num_brackets: int,
    tol: float,
) -> List[float]:
    """
    Search for roots of f(κ) over κ ∈ (0, κ_max^{eff}) by sign bracketing.

    κ_in^2 = μ^2/c^2 - κ^2 must be ≥ 0, so κ ≤ μ/c. We clamp κ_max to < μ/c.
    """
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")

    kappa_cap = (mu / c) * 0.999
    if kappa_max is None or not np.isfinite(kappa_max):
        kappa_max_eff = kappa_cap
    else:
        kappa_max_eff = min(float(kappa_max), kappa_cap)
        if kappa_max_eff <= 1e-9:
            kappa_max_eff = kappa_cap

    kappas = []
    grid = np.linspace(1e-9, kappa_max_eff, num_brackets + 1)
    fvals = []
    for x in grid:
        fv = _secular_value(x, ell, R, mu, c)
        # Replace NaNs with None to break bracketing across invalid regions
        fvals.append(fv if np.isfinite(fv) else None)

    for i in range(len(grid) - 1):
        f0 = fvals[i]
        f1 = fvals[i + 1]
        if f0 is None or f1 is None:
            continue
        if f0 == 0.0:
            root = grid[i]
        elif f1 == 0.0:
            root = grid[i + 1]
        elif np.sign(f0) == np.sign(f1):
            continue
        else:
            a, b = grid[i], grid[i + 1]
            try:
                root = optimize.brentq(
                    lambda x: _secular_value(x, ell, R, mu, c),
                    a,
                    b,
                    xtol=tol,
                    rtol=tol,
                    maxiter=200,
                )
            except Exception:
                continue
        # Deduplicate near-equal roots
        if len(kappas) == 0 or abs(root - kappas[-1]) > 1e-6:
            kappas.append(float(root))
    return kappas


def compute_kappas(
    R: float,
    mu: float,
    c: float = 1.0,
    ell_max: int = 12,
    kappa_max: Optional[float] = None,
    num_brackets: int = 512,
    tol: float = 1e-8,
) -> List[Dict[str, float]]:
    """
    Compute κ-roots of the secular equation for ℓ = 0,1,...,ell_max.

    Args:
      R: cylinder radius (dimensionless units)
      mu: tachyon scale (baseline EFT parameter)
      c: wave speed (from 𝓛_K = ½(∂_t φ)^2 − ½ c^2 (∇φ)^2)
      ell_max: highest angular momentum to consider
      kappa_max: optional upper bound (< μ/c), defaults to 0.999 μ/c
      num_brackets: grid count for sign bracketing
      tol: root solver tolerance

    Returns:
      list of dict: { 'ell', 'kappa', 'k_in', 'k_out' } for each root found (kappa > 0).
    """
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")

    results: List[Dict[str, float]] = []
    for ell in range(int(max(0, ell_max)) + 1):
        roots = _find_roots_for_ell(
            ell=ell,
            R=R,
            mu=mu,
            c=c,
            kappa_max=kappa_max,
            num_brackets=num_brackets,
            tol=tol,
        )
        for kappa in roots:
            k_in = float(np.sqrt(max(0.0, (mu / c) ** 2 - kappa ** 2)))
            k_out = float(np.sqrt(max(0.0, kappa ** 2 + 2.0 * (mu / c) ** 2)))
            results.append(
                {
                    "ell": float(ell),
                    "kappa": float(kappa),
                    "k_in": float(k_in),
                    "k_out": float(k_out),
                }
            )
    return results


def mode_functions(
    R: float,
    root: Dict[str, float],
) -> Dict[str, Callable[[float], float]]:
    """
    Construct piecewise radial mode functions normalized so u(R) = 1.

    Inside (r < R):  u_in(r) = A I_ℓ(k_in r), with A = 1 / I_ℓ(k_in R).
    Outside (r > R): u_out(r) = B K_ℓ(k_out r), with B = 1 / K_ℓ(k_out R).

    Args:
      R: tube radius
      root: dict from compute_kappas entry, requires 'ell', 'k_in', 'k_out'.

    Returns:
      dict with callables: { 'u_in', 'u_out', 'u' }
    """
    ell = int(root["ell"])
    k_in = float(root["k_in"])
    k_out = float(root["k_out"])

    x_in_R = max(_EPS, k_in * R)
    x_out_R = max(_EPS, k_out * R)

    I_R = _iv(ell, x_in_R)
    K_R = _kv(ell, x_out_R)
    if abs(I_R) < _EPS or abs(K_R) < _EPS:
        raise FloatingPointError("Unstable normalization at r=R: I_ℓ or K_ℓ ~ 0")

    A = 1.0 / I_R
    B = 1.0 / K_R

    def u_in(r: float) -> float:
        rr = float(max(0.0, r))
        return float(A * _iv(ell, max(_EPS, k_in * rr)))

    def u_out(r: float) -> float:
        rr = float(max(0.0, r))
        return float(B * _kv(ell, max(_EPS, k_out * rr)))

    def u(r: float) -> float:
        rr = float(max(0.0, r))
        if rr <= R:
            return u_in(rr)
        return u_out(rr)

    return {"u_in": u_in, "u_out": u_out, "u": u}


if __name__ == "__main__":
    # Minimal self-test (requires scipy)
    R_test = 3.0
    mu_test = 1.0
    c_test = 1.0
    try:
        roots = compute_kappas(R=R_test, mu=mu_test, c=c_test, ell_max=4, num_brackets=256)
        print(f"[cylinder_modes] Found {len(roots)} roots for R={R_test}, mu={mu_test}, c={c_test}")
        if roots:
            fns = mode_functions(R_test, roots[0])
            print("[cylinder_modes] u(R) =", fns["u"](R_test))
    except Exception as e:
        print("Self-test skipped or failed:", e)