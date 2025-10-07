#!/usr/bin/env python3
"""
Reaction-exact step for the logistic on-site law in RD:

dW/dt = r W - u W^2, with closed form update over dt:

W(t+dt) = ( r W(t) e^{r dt} ) / ( u W(t) (e^{r dt} - 1) + r ).

Assumptions: r>0, u>=0 typical; numerically stabilized via expm1.

Runtime policy:
- Purely local; supports per-site dt for event-driven census firing.
- No global scans, no schedulers; observability is read-only.

Reference ODE invariant (for diagnostics only):
Q(W,t) = ln( W / (r - u W) ) - r t.
"""

from typing import Union, Optional
import numpy as np

ArrayLike = Union[float, np.ndarray]

def reaction_exact_step(W: ArrayLike,
                        r: ArrayLike,
                        u: ArrayLike,
                        dt: ArrayLike,
                        clip_eps: float = 1e-12,
                        dtype: Optional[np.dtype] = None) -> np.ndarray:
    """
    Compute the exact logistic reaction step over one micro-interval dt.

    Parameters
    ----------
    W : array-like
        Current on-site values (scalar or ndarray).
    r : array-like
        Linear growth coefficient.
    u : array-like
        Quadratic saturation coefficient.
    dt : array-like
        Time increment (scalar or broadcastable to W).
    clip_eps : float
        Denominator guard to prevent catastrophic cancellation.
    dtype : Optional[np.dtype]
        Computation dtype (defaults to float64).

    Returns
    -------
    np.ndarray
        Next values W(t+dt) with shape broadcast from inputs.
    """
    x = np.array(W, dtype=dtype if dtype is not None else np.float64)
    r_arr = np.array(r, dtype=x.dtype)
    u_arr = np.array(u, dtype=x.dtype)
    dt_arr = np.array(dt, dtype=x.dtype)

    # Use expm1 for numerical stability: e = exp(r dt), s = e - 1
    s = np.expm1(r_arr * dt_arr)
    e = s + 1.0

    # Handle u ≈ 0 path (linear growth) separately to avoid 0/0 in formula
    u_zero = np.isclose(u_arr, 0.0)

    denom = u_arr * x * s + r_arr
    if np.isscalar(denom):
        if abs(denom) < clip_eps:
            denom = np.sign(denom) * clip_eps if denom != 0 else clip_eps
    else:
        zero_mask = np.isclose(denom, 0.0, atol=clip_eps, rtol=0.0)
       # Replace near-zero denominators with signed epsilon to keep direction
        denom = np.where(zero_mask,
                         np.where(denom > 0, clip_eps, -clip_eps),
                         denom)

    num = r_arr * x * e
    W_next = num / denom

    if np.any(u_zero):
        W_lin = x * e
        mask = u_zero
        if not np.array(mask).shape == x.shape:
            mask = np.broadcast_to(mask, x.shape)
        W_next = np.where(mask, W_lin, W_next)

    return W_next


def logistic_invariant_Q(W: ArrayLike,
                         r: ArrayLike,
                         u: ArrayLike,
                         t: ArrayLike) -> np.ndarray:
    """
    Logarithmic first integral for the autonomous logistic ODE:
    Q(W,t) = ln( W / (r - u W) ) - r t.

    Note: This is ODE-only; with diffusion the invariant is not preserved.
    """
    x = np.array(W, dtype=np.float64)
    r_arr = np.array(r, dtype=x.dtype)
    u_arr = np.array(u, dtype=x.dtype)
    t_arr = np.array(t, dtype=x.dtype)
    eps = 1e-15
    denom = r_arr - u_arr * x
    zero_mask = np.isclose(denom, 0.0, atol=eps, rtol=0.0)
    denom = np.where(zero_mask,
                     np.where(denom > 0, eps, -eps),
                     denom)
    return np.log(x / denom) - r_arr * t_arr


if __name__ == "__main__":
    # Smoke tests
    W0 = np.array([0.1, 0.5], dtype=np.float64)
    r = 0.25
    u = 0.25
    dt = 1.0
    W1 = reaction_exact_step(W0, r, u, dt)
    print("W1:", W1)

    # u -> 0 limit should match exponential growth exactly
    W1_lin = reaction_exact_step(W0, r, 0.0, dt)
    W1_lin_ref = W0 * np.exp(r * dt)
    rel_err = np.max(np.abs(W1_lin - W1_lin_ref) /
                     np.maximum(1e-12, np.abs(W1_lin_ref)))
    print("u=0 rel_err:", rel_err)
    assert rel_err < 1e-12
    print("reaction_exact_step: OK")