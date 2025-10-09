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

import math

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


def _ive(nu: int, x: float) -> float:
    """Exponentially scaled I_v: e^{-x} I_v(x) for stability at large x."""
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")
    if hasattr(special, "ive"):
        return float(special.ive(nu, x))
    # Fallback: when ive is unavailable, attempt to scale manually; guard overflow
    val = _iv(nu, x)
    try:
        return float(val * math.exp(-float(x)))
    except Exception:
        # If overflow, return a large sentinel to keep ratios finite when possible
        return float("inf")


def _kve(nu: int, x: float) -> float:
    """Exponentially scaled K_v: e^{x} K_v(x) for stability at large x."""
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")
    if hasattr(special, "kve"):
        return float(special.kve(nu, x))
    val = _kv(nu, x)
    try:
        return float(val * math.exp(float(x)))
    except Exception:
        return float("inf")


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
    """Compute (I'_ν / I_ν)(x) using ratio identities with scaled Bessels for stability.

    Identity: I'_ν = (I_{ν-1} + I_{ν+1})/2 ⇒ I'_ν/I_ν = (I_{ν-1}/I_ν + I_{ν+1}/I_ν)/2.
    Using scaled ive cancels exponential growth in the ratios.
    """
    x = float(max(x, _EPS))
    try:
        In = _ive(nu, x)
        if not np.isfinite(In) or abs(In) < _EPS:
            # Fall back to direct ratio if scaled fails
            Iv = _iv(nu, x)
            if abs(Iv) < _EPS:
                return np.sign(_ivp(nu, x)) * 1e6
            return _ivp(nu, x) / Iv
        Im = _ive(nu - 1, x)
        Ip = _ive(nu + 1, x)
        return float(0.5 * ((Im / In) + (Ip / In)))
    except Exception:
        # Ultimate fallback
        Iv = _iv(nu, x)
        if abs(Iv) < _EPS:
            return np.sign(_ivp(nu, x)) * 1e6
        return _ivp(nu, x) / Iv


def _dlnK(nu: int, x: float) -> float:
    """Compute (K'_ν / K_ν)(x) using ratio identities with scaled Bessels for stability.

    Identity: K'_ν = - (K_{ν-1} + K_{ν+1})/2 ⇒ K'_ν/K_ν = - (K_{ν-1}/K_ν + K_{ν+1}/K_ν)/2.
    Using scaled kve cancels exponential decay in the ratios.
    """
    x = float(max(x, _EPS))
    try:
        Kn = _kve(nu, x)
        if not np.isfinite(Kn) or abs(Kn) < _EPS:
            Kv = _kv(nu, x)
            if abs(Kv) < _EPS:
                return -np.sign(_kvp(nu, x)) * 1e6
            return _kvp(nu, x) / Kv
        Km = _kve(nu - 1, x)
        Kp = _kve(nu + 1, x)
        return float(-0.5 * ((Km / Kn) + (Kp / Kn)))
    except Exception:
        Kv = _kv(nu, x)
        if abs(Kv) < _EPS:
            return -np.sign(_kvp(nu, x)) * 1e6
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
    # Guard absurd values: saturate to preserve sign for bracketing
    if not np.isfinite(val):
        return np.nan
    if abs(val) > 1e12:
        return float(1e12 if val > 0 else -1e12)
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
    Adaptive search for roots of f(κ) over κ ∈ (0, κ_max^{eff}) by sign bracketing.

    Refinements:
      - Reparameterize κ = (μ/c) sin θ to avoid invalid interior region and to
        sample more uniformly near both endpoints (θ ∈ (0, π/2)).
      - Multi-resolution scanning: if no roots are found on a coarse grid,
        automatically refine the grid up to a small number of levels.

    κ_in^2 = μ^2/c^2 - κ^2 must be ≥ 0, so κ ≤ μ/c. We effectively clamp via θ.
    """
    if not _HAVE_SCIPY:
        raise RuntimeError("scipy is required for cylinder_modes")

    def _kappa_from_theta(theta: float) -> float:
        # Map θ ∈ (0, π/2) to κ = (μ/c) sin θ, keeping clear of endpoints
        return (mu / c) * math.sin(theta)

    def _g(theta: float) -> float:
        # Compose secular with θ-parameterization
        k = _kappa_from_theta(theta)
        return _secular_value(k, ell, R, mu, c)

    def _scan(num: int) -> List[float]:
        roots_theta: List[float] = []
        # Stay away from poles at the endpoints
        th_eps = 1e-8
        th_lo = th_eps
        th_hi = 0.5 * math.pi - th_eps
        grid = np.linspace(th_lo, th_hi, int(num) + 1)
        fvals: List[Optional[float]] = []
        for th in grid:
            try:
                v = _g(float(th))
                fvals.append(v if (v is not None and np.isfinite(v)) else None)
            except Exception:
                fvals.append(None)

        for i in range(len(grid) - 1):
            th0, th1 = float(grid[i]), float(grid[i + 1])
            f0, f1 = fvals[i], fvals[i + 1]
            # Skip across invalid segments; refinement may split these later
            if f0 is None or f1 is None:
                continue
            # Exact hits at samples
            if f0 == 0.0:
                roots_theta.append(th0)
                continue
            if f1 == 0.0:
                roots_theta.append(th1)
                continue
            # Sign change → bracket (or try midpoint if ambiguous small-same-sign)
            if np.sign(f0) == np.sign(f1):
                # If both small but same sign, try a midpoint probe to catch sharp crossings
                if abs(f0) < 1e-6 and abs(f1) < 1e-6:
                    thm = 0.5 * (th0 + th1)
                    try:
                        fm = _g(thm)
                    except Exception:
                        fm = None
                    if fm is not None and np.isfinite(fm) and np.sign(fm) != np.sign(f0):
                        # Now have a bracket (th0, thm)
                        th1 = thm
                        f1 = fm
                    else:
                        continue
                else:
                    continue
            # At this point we have a bracket (th0, th1)
            th_root = None
            try:
                th_root = optimize.brentq(
                    lambda th: _g(float(th)),
                    th0,
                    th1,
                    xtol=tol,
                    rtol=tol,
                    maxiter=200,
                )
            except Exception:
                # If Brent fails (rare), try bisection as a fallback
                try:
                    th_root = optimize.bisect(
                        lambda th: _g(float(th)), th0, th1, xtol=tol, rtol=tol, maxiter=200
                    )
                except Exception:
                    th_root = None
            if th_root is not None:
                roots_theta.append(float(th_root))

        # Secant refinement from local minima of |f| to catch missed roots without clear brackets
        absf = [abs(v) if (v is not None and np.isfinite(v)) else float("inf") for v in fvals]
        # Identify interior local minima indices
        cand_idx: List[int] = []
        for j in range(1, len(absf) - 1):
            if absf[j] < absf[j - 1] and absf[j] < absf[j + 1] and absf[j] < 1e-3:
                cand_idx.append(j)
        for j in cand_idx[: max(8, len(cand_idx))]:  # cap attempts per scan
            th_guess = float(grid[j])
            # Two-point secant using neighbors as initial guesses (not requiring sign change)
            th0s = float(grid[j - 1])
            th1s = float(grid[j + 1])
            th_star = None
            try:
                th_star = optimize.newton(lambda th: _g(float(th)), x0=th_guess, x1=th1s, tol=tol, maxiter=100)
            except Exception:
                try:
                    th_star = optimize.newton(lambda th: _g(float(th)), x0=th_guess, x1=th0s, tol=tol, maxiter=100)
                except Exception:
                    th_star = None
            if th_star is None:
                continue
            if not (1e-9 < th_star < 0.5 * math.pi - 1e-9):
                continue
            f_star = _g(float(th_star))
            if f_star is None or not np.isfinite(f_star) or abs(f_star) > 1e-6:
                continue
            roots_theta.append(float(th_star))

        # Deduplicate and sort by θ
        roots_theta = sorted(list({round(rt, 12): rt for rt in roots_theta}.values()))
        # Map to κ, deduplicate by κ as well
        kappas_local: List[float] = []
        for th in roots_theta:
            k = _kappa_from_theta(th)
            if (len(kappas_local) == 0) or (abs(k - kappas_local[-1]) > 1e-6):
                kappas_local.append(float(k))
        return kappas_local

    # Multi-resolution refinement if no roots on coarse grid
    kappas: List[float] = _scan(num_brackets)
    if len(kappas) == 0:
        # escalate scanning resolution modestly up to 2 extra levels
        for factor in (2, 4):
            kappas = _scan(int(num_brackets * factor))
            if len(kappas) > 0:
                break

    # Additional complementary scans to catch roots near singular regions
    def _scan_chebyshev(num: int) -> List[float]:
        # Chebyshev nodes on θ ∈ (0, π/2)
        n = int(max(4, num))
        j = np.arange(n + 1)
        # Nodes in [-1,1]: x_j = cos(π j / n), map to (0, π/2)
        x = np.cos(np.pi * j / n)
        th = 0.25 * np.pi * (x + 1.0)
        th[0] = max(th[0], 1e-8)
        th[-1] = min(th[-1], 0.5 * np.pi - 1e-8)
        fvals: List[Optional[float]] = []
        for t in th:
            try:
                v = _g(float(t))
                fvals.append(v if (v is not None and np.isfinite(v)) else None)
            except Exception:
                fvals.append(None)
        roots: List[float] = []
        for i in range(len(th) - 1):
            t0, t1 = float(th[i]), float(th[i + 1])
            f0, f1 = fvals[i], fvals[i + 1]
            if f0 is None or f1 is None or np.sign(f0) == np.sign(f1):
                continue
            th_root = None
            try:
                th_root = optimize.brentq(lambda th: _g(float(th)), t0, t1, xtol=tol, rtol=tol, maxiter=200)
            except Exception:
                try:
                    th_root = optimize.bisect(lambda th: _g(float(th)), t0, t1, xtol=tol, rtol=tol, maxiter=200)
                except Exception:
                    th_root = None
            if th_root is not None:
                roots.append(float(th_root))
        roots = sorted(list({round(rt, 12): rt for rt in roots}.values()))
        # map to κ
        kappas_local: List[float] = []
        for thv in roots:
            kv = _kappa_from_theta(thv)
            if len(kappas_local) == 0 or abs(kv - kappas_local[-1]) > 1e-6:
                kappas_local.append(float(kv))
        return kappas_local

    def _scan_u(num: int) -> List[float]:
        # Parameterize by u = k_in R, u ∈ (0, (μ/c) R)
        u_max = (mu / c) * R
        if u_max <= 1e-12:
            return []
        us = np.linspace(1e-9, u_max * 0.999, int(num) + 1)
        def g_u(u: float) -> float:
            # k_in = u/R, κ = sqrt((μ/c)^2 - k_in^2)
            k_in = u / max(R, _EPS)
            s2 = (mu / c) ** 2 - k_in ** 2
            if s2 <= 0:
                return float("nan")
            kappa = math.sqrt(s2)
            return _secular_value(kappa, ell, R, mu, c)
        fvals: List[Optional[float]] = []
        for u in us:
            try:
                v = g_u(float(u))
                fvals.append(v if (v is not None and np.isfinite(v)) else None)
            except Exception:
                fvals.append(None)
        kappas_local: List[float] = []
        for i in range(len(us) - 1):
            u0, u1 = float(us[i]), float(us[i + 1])
            f0, f1 = fvals[i], fvals[i + 1]
            if f0 is None or f1 is None or np.sign(f0) == np.sign(f1):
                continue
            u_root = None
            try:
                u_root = optimize.brentq(lambda uu: g_u(float(uu)), u0, u1, xtol=tol, rtol=tol, maxiter=200)
            except Exception:
                try:
                    u_root = optimize.bisect(lambda uu: g_u(float(uu)), u0, u1, xtol=tol, rtol=tol, maxiter=200)
                except Exception:
                    u_root = None
            if u_root is not None:
                k_in = u_root / max(R, _EPS)
                s2 = (mu / c) ** 2 - k_in ** 2
                if s2 > 0:
                    kv = math.sqrt(s2)
                    if len(kappas_local) == 0 or abs(kv - kappas_local[-1]) > 1e-6:
                        kappas_local.append(float(kv))
        return kappas_local

    # Merge complementary scans
    extra_k = []
    if len(kappas) == 0:
        extra_k.extend(_scan_chebyshev(max(8, num_brackets // 2)))
        extra_k.extend(_scan_u(max(8, num_brackets // 2)))
    else:
        # Even if some found, we can attempt to discover missed ones with coarse extra scans
        extra_k.extend(_scan_chebyshev(max(8, num_brackets // 4)))
        extra_k.extend(_scan_u(max(8, num_brackets // 4)))

    if extra_k:
        merged = sorted(list({round(x, 9): x for x in (list(kappas) + extra_k)}.values()))
        kappas = merged
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
      c: wave speed (from 𝓛_K = ½(∂_t φ)^2 - ½ c^2 (∇φ)^2)
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


def has_root_potential(
    R: float,
    mu: float,
    c: float,
    ell: int,
    probes: int = 64,
    eps: float = 1e-8,
) -> bool:
    """
    Heuristic test: does the secular function exhibit any sign change across θ ∈ (0, π/2)?

    Returns True if a sign change is detected between any adjacent probe points,
    indicating at least one root for this (R, mu, c, ell) at k=0. This defines
    which (R, ℓ) pairs are physically allowed and should be counted as attempts.
    """
    if not (_HAVE_SCIPY and R > 0 and mu > 0 and c > 0):
        return False
    th_lo = eps
    th_hi = 0.5 * math.pi - eps
    grid = np.linspace(th_lo, th_hi, int(max(8, probes)))
    prev: Optional[float] = None
    for th in grid:
        kappa = (mu / c) * math.sin(float(th))
        fv = _secular_value(kappa, ell, R, mu, c)
        if fv is None or not np.isfinite(fv):
            continue
        if prev is None:
            prev = fv
            continue
        if np.sign(prev) != np.sign(fv):
            return True
        prev = fv
    return False


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