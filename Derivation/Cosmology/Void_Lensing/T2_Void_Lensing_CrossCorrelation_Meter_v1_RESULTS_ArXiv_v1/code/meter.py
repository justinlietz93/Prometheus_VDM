from __future__ import annotations

"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Void Lensing Cross-Correlation Meter core (T2 instrument) — profile-mode implementation.

This module defines the public meter API for the cosmology/void_lensing domain.
It remains free of any real I/O or external dependencies beyond numpy. The
canonical contract for this meter is the T2 proposal for the void-lensing
cross-correlation meter; see project documentation for details.

In this phase the module:

- exposes a single public entry point, run_meter;
- supports a "profile mode" where kappa_map is a mapping with arrays
  {"x", "kappa", "kappa_err"} representing a stacked, dimensionless profile;
- computes wall, shoulder, interface-count, and diagnostic metrics from that
  1D profile; and
- returns a metrics dictionary with all required keys populated with
  dimensionless, schema-compatible values.

Non-goals for this module:

- no direct loading of κ maps or void catalogues from disk;
- no use of approval databases or artifact-writing helpers;
- no coupling to specific AKRA/DES pipelines (handled in backends).

All heavy map geometry and catalogue handling will be added later in backends
that construct 1D profiles and then call into these helpers.
"""

from typing import Any, Dict, Mapping, MutableMapping, Sequence, Tuple

import numpy as np

REQUIRED_METRIC_KEYS: Sequence[str] = (
    "backend",
    "z_bin",
    "R_v_bin",
    "R2_wall",
    "S_wall",
    "A_sh",
    "AUROC_sh",
    "beta_interface",
    "beta_uncertainty",
    "beta_bias",
    "SNR",
    "B_mode_residual",
    "n_voids",
    "quality_flags",
    "profile",
)


def _as_ndarray_1d(name: str, values: Any) -> np.ndarray:
    """Convert input to a 1D float64 numpy array, raising if empty."""
    arr = np.asarray(values, dtype=float)
    if arr.ndim == 0:
        arr = arr.reshape(1)
    elif arr.ndim > 1:
        arr = arr.reshape(-1)
    if arr.size == 0:
        raise ValueError(f"{name} must contain at least one element")
    return arr


def _ensure_monotonic_increasing(x: np.ndarray, *others: np.ndarray) -> Tuple[np.ndarray, ...]:
    """Sort x (and associated arrays) in increasing order of x."""
    order = np.argsort(x)
    x_sorted = x[order]
    sorted_others = tuple(arr[order] for arr in others)
    return (x_sorted, *sorted_others)


def compute_wall_metrics(
    x: np.ndarray,
    kappa: np.ndarray,
    kappa_err: np.ndarray | None,
    x_wall_range: Sequence[float],
) -> Tuple[float, float]:
    """Compute wall slope S_wall and coefficient of determination R2_wall."""
    x_min, x_max = float(x_wall_range[0]), float(x_wall_range[1])
    mask = (x >= x_min) & (x <= x_max)
    if mask.sum() < 2:
        return 0.0, 0.0

    x_w = x[mask]
    k_w = kappa[mask]

    if kappa_err is not None:
        err_w = kappa_err[mask]
        # Guard against zeros / negatives.
        w = np.where(err_w > 0.0, 1.0 / (err_w**2), 1.0)
    else:
        w = np.ones_like(k_w)

    # Design matrix for linear model: k = a + b x
    X = np.vstack([np.ones_like(x_w), x_w]).T
    sqrt_w = np.sqrt(w)
    Xw = X * sqrt_w[:, None]
    yw = k_w * sqrt_w
    coeffs, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    a_hat, b_hat = coeffs

    k_pred = a_hat + b_hat * x_w
    # Weighted R^2
    k_mean = np.average(k_w, weights=w)
    ss_res = np.sum(w * (k_w - k_pred) ** 2)
    ss_tot = np.sum(w * (k_w - k_mean) ** 2)
    if ss_tot <= 0.0:
        R2 = 0.0
    else:
        R2 = 1.0 - float(ss_res / ss_tot)

    return float(b_hat), float(R2)


def compute_shoulder_metrics(
    x: np.ndarray,
    kappa: np.ndarray,
    kappa_err: np.ndarray | None,
    x_wall_range: Sequence[float],
    x_bg_range: Sequence[float],
) -> Dict[str, float]:
    """
    Compute shoulder amplitude A_sh and location x_sh from a 1D profile.

    This implementation searches for a **local perturbation** (shoulder) on top
    of the slowly-varying wall trend in the region x > max(1, x_wall_max), and
    then standardizes that deviation using background statistics over
    x in x_bg_range.
    """
    x_wall_max = float(x_wall_range[1])
    x_min_sh = max(1.0, x_wall_max)
    x_bg_min, x_bg_max = float(x_bg_range[0]), float(x_bg_range[1])

    # Shoulder search region: between x_min_sh and start of background.
    shoulder_mask = (x >= x_min_sh) & (x < x_bg_min)
    if shoulder_mask.sum() == 0:
        return {
            "A_sh": 0.0,
            "x_sh": float(np.nan),
            "kappa_sh": 0.0,
            "kappa_bg_mean": 0.0,
            "kappa_bg_std": 0.0,
        }

    x_sh_region = x[shoulder_mask]
    k_sh_region = kappa[shoulder_mask]

    # Use a simple local-linear detrend only to *locate* the shoulder as a
    # localized perturbation on top of the slowly-varying trend.
    if x_sh_region.size >= 2:
        X = np.vstack([np.ones_like(x_sh_region), x_sh_region]).T
        coeffs, *_ = np.linalg.lstsq(X, k_sh_region, rcond=None)
        k_trend = coeffs[0] + coeffs[1] * x_sh_region
        k_resid = k_sh_region - k_trend
        idx_local = int(np.argmax(np.abs(k_resid)))
    else:
        idx_local = 0

    x_sh = float(x_sh_region[idx_local])
    kappa_sh = float(k_sh_region[idx_local])

    # Background statistics (using the original κ profile).
    bg_mask = (x >= x_bg_min) & (x <= x_bg_max)
    if bg_mask.sum() == 0:
        kappa_bg_mean = 0.0
        kappa_bg_std = 0.0
    else:
        k_bg = kappa[bg_mask]
        kappa_bg_mean = float(np.mean(k_bg))
        kappa_bg_std = float(np.std(k_bg, ddof=1)) if k_bg.size > 1 else 0.0

    eps = 1e-8
    denom = kappa_bg_std if kappa_bg_std > 0.0 else eps
    # Define the shoulder amplitude as the contrast of the local κ value
    # relative to the large-scale background, standardized by the background
    # scatter. For the synthetic mocks, this yields:
    # - A_sh ≈ 0 for profiles without a compensation shoulder; and
    # - A_sh ≫ 0 when a clear shoulder bump is present.
    signal = float(k_resid[idx_local])
    A_sh = signal / denom

    return {
        "A_sh": float(A_sh),
        "x_sh": x_sh,
        "kappa_sh": kappa_sh,
        "kappa_bg_mean": float(kappa_bg_mean),
        "kappa_bg_std": float(kappa_bg_std),
    }


def compute_interface_metrics(
    x: np.ndarray,
    kappa: np.ndarray,
    lambda_ref: float,
    x_interface_range: Sequence[float] | None = None,
) -> Dict[str, float]:
    """
    Compute interface-count exponent beta_interface and its uncertainty.

    Interfaces are defined as sign-changes in d kappa / d x, and N_int is
    constructed as the cumulative count of interfaces versus radius.

    Parameters
    ----------
    x, kappa:
        1D arrays defining the radial coordinate and convergence profile.
    lambda_ref:
        Reference scale λ_ref used to form the dimensionless radius R / λ_ref.
    x_interface_range:
        Optional [x_min, x_max] range within which interfaces are searched.
        When provided, only this subregion is used to construct the derivative
        and count sign changes, which is useful to exclude local structure
        (e.g. shoulders) that should not contribute to the interface-count
        scaling.
    """
    # Optionally restrict to a subrange for interface detection.
    if x_interface_range is not None:
        x_min, x_max = float(x_interface_range[0]), float(x_interface_range[1])
        region_mask = (x >= x_min) & (x <= x_max)
        if region_mask.sum() < 3:
            return {
                "beta_interface": 0.0,
                "beta_uncertainty": 0.0,
                "n_interfaces": 0,
            }
        x = x[region_mask]
        kappa = kappa[region_mask]

    if x.size < 3:
        return {
            "beta_interface": 0.0,
            "beta_uncertainty": 0.0,
            "n_interfaces": 0,
        }

    # Finite-difference derivative.
    dkdx = np.gradient(kappa, x)

    # Suppress tiny derivatives that are likely numerical noise.
    eps = 1e-6 * max(1.0, float(np.max(np.abs(dkdx))))
    dkdx_thresh = np.where(np.abs(dkdx) >= eps, dkdx, 0.0)
    signs = np.sign(dkdx_thresh)

    interface_positions: list[float] = []
    for j in range(1, signs.size):
        if signs[j - 1] == 0.0 or signs[j] == 0.0:
            continue
        if signs[j - 1] * signs[j] < 0.0:
            # Interface located between x[j-1] and x[j]; take midpoint.
            interface_positions.append(float(0.5 * (x[j - 1] + x[j])))

    n_interfaces = len(interface_positions)
    if n_interfaces < 2:
        return {
            "beta_interface": 0.0,
            "beta_uncertainty": 0.0,
            "n_interfaces": int(n_interfaces),
        }

    x_int = np.asarray(interface_positions, dtype=float)
    # Use interface radii themselves as the sample of R values.
    R = x_int
    # Guard against invalid lambda_ref.
    lam = float(lambda_ref) if lambda_ref > 0.0 else float(np.median(R))
    logR = np.log(R / lam)

    # Fit N_int(R_k) = N0 + beta * log(R_k / lam), where N_int = 1..n_interfaces.
    y = np.arange(1, n_interfaces + 1, dtype=float)
    X = np.vstack([np.ones_like(logR), logR]).T
    coeffs, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
    N0_hat, beta_hat = coeffs

    if logR.size > 2:
        dof = logR.size - 2
        ss_res = residuals[0] if residuals.size > 0 else 0.0
        sigma2 = ss_res / dof if dof > 0 and ss_res > 0.0 else 0.0
        # Covariance matrix = sigma^2 * (X^T X)^-1
        XtX_inv = np.linalg.inv(X.T @ X)
        beta_var = sigma2 * XtX_inv[1, 1]
        beta_sigma = float(np.sqrt(beta_var)) if beta_var > 0.0 else 0.0
    else:
        beta_sigma = 0.0

    return {
        "beta_interface": float(beta_hat),
        "beta_uncertainty": float(beta_sigma),
        "n_interfaces": int(n_interfaces),
    }


def compute_aux_diagnostics(
    x: np.ndarray,
    kappa: np.ndarray,
    kappa_err: np.ndarray | None,
    n_voids: int,
    min_voids_per_bin: int,
) -> Dict[str, Any]:
    """Compute SNR, B-mode residual placeholder, and quality flags."""
    if kappa_err is None or np.all(kappa_err <= 0.0):
        SNR = 0.0
    else:
        # SNR^2 = sum( (kappa / sigma)^2 ).
        snr2 = float(np.sum((kappa / kappa_err) ** 2))
        SNR = float(np.sqrt(max(snr2, 0.0)))

    B_mode_residual = 0.0  # Placeholder for synthetic 1D mocks.

    flags: list[str] = []
    if n_voids <= 0:
        flags.append("n_voids_unknown")
    else:
        flags.append("synthetic_profile")
    if n_voids < min_voids_per_bin:
        flags.append("insufficient_voids")

    return {
        "SNR": SNR,
        "B_mode_residual": float(B_mode_residual),
        "n_voids": int(n_voids),
        "quality_flags": flags,
    }


def run_meter(
    kappa_map: Any,
    void_catalog: Any,
    config: Mapping[str, Any],
) -> Dict[str, Any]:
    """
    Void-lensing cross-correlation meter API (profile-mode implementation).

    Parameters
    ----------
    kappa_map:
        In this phase, expected to be a mapping with keys "x", "kappa",
        and optionally "kappa_err", representing the stacked, dimensionless
        profile x = r / R_v and its convergence values.
    void_catalog:
        Placeholder for a void catalogue structure. Currently unused in
        profile mode.
    config:
        Configuration mapping typically built from a spec JSON. At minimum
        this should provide:
          - "backend": identifier for the upstream pipeline or dataset
          - "z_bin": 2-element sequence with redshift bin edges
          - "R_v_bin": 2-element sequence with void-radius bin edges
        Optionally it may contain a "parameters" sub-mapping with:
          - "x_wall_range", "x_bg_range", "lambda_ref",
          - "min_voids_per_bin", etc.

    Returns
    -------
    metrics:
        Dictionary matching the void_lensing_meter-v1 schema, with all
        required keys populated.

    Notes
    -----
    - This function performs no I/O.
    - For now, AUROC_sh and beta_bias are left at neutral values; they are
      intended to be computed over ensembles of synthetic profiles in tests.
    """
    backend = str(config.get("backend", "UNKNOWN"))

    def _norm_bin(value: Any) -> list[float]:
        seq = list(value) if isinstance(value, (list, tuple)) else [0.0, 0.0]
        if len(seq) < 2:
            seq = (seq + [0.0, 0.0])[:2]
        return [float(seq[0]), float(seq[1])]

    z_bin = _norm_bin(config.get("z_bin", [0.0, 0.0]))
    R_v_bin = _norm_bin(config.get("R_v_bin", [0.0, 0.0]))

    parameters = config.get("parameters", {}) or {}
    x_wall_range = parameters.get("x_wall_range", [0.8, 1.2])
    x_bg_range = parameters.get("x_bg_range", [2.5, 4.0])
    lambda_ref = float(parameters.get("lambda_ref", 1.0))
    min_voids_per_bin = int(parameters.get("min_voids_per_bin", 0))
    # For synthetic tests we treat n_voids ≈ min_voids_per_bin unless
    # a more precise value is provided later.
    n_voids = min_voids_per_bin

    # Profile-mode handling.
    profile_x = None
    profile_kappa = None
    profile_kappa_err = None

    if isinstance(kappa_map, Mapping) and "x" in kappa_map and "kappa" in kappa_map:
        profile_x = _as_ndarray_1d("profile.x", kappa_map["x"])
        profile_kappa = _as_ndarray_1d("profile.kappa", kappa_map["kappa"])
        if profile_x.size != profile_kappa.size:
            raise ValueError("profile.x and profile.kappa must have the same length")
        if "kappa_err" in kappa_map:
            profile_kappa_err = _as_ndarray_1d("profile.kappa_err", kappa_map["kappa_err"])
            if profile_kappa_err.size != profile_kappa.size:
                raise ValueError("profile.kappa_err must have the same length as profile.kappa")
        else:
            # Default to a small constant error to enable SNR and weighted fits.
            profile_kappa_err = np.full_like(profile_kappa, 1e-2, dtype=float)

        profile_x, profile_kappa, profile_kappa_err = _ensure_monotonic_increasing(
            profile_x, profile_kappa, profile_kappa_err
        )

        S_wall, R2_wall = compute_wall_metrics(
            profile_x,
            profile_kappa,
            profile_kappa_err,
            x_wall_range=x_wall_range,
        )
        shoulder = compute_shoulder_metrics(
            profile_x,
            profile_kappa,
            profile_kappa_err,
            x_wall_range=x_wall_range,
            x_bg_range=x_bg_range,
        )
        # Restrict interface detection to a region predominantly containing the
        # large-scale interface structure (e.g. beyond the shoulder), to avoid
        # counting local shoulder-induced extrema as separate interfaces.
        x_int_min = float(parameters.get("x_interface_min", x_bg_range[0] - 0.5))
        x_int_max = float(parameters.get("x_interface_max", float(profile_x[-1])))

        iface = compute_interface_metrics(
            profile_x,
            profile_kappa,
            lambda_ref=lambda_ref,
            x_interface_range=[x_int_min, x_int_max],
        )
        aux = compute_aux_diagnostics(
            profile_x,
            profile_kappa,
            profile_kappa_err,
            n_voids=n_voids,
            min_voids_per_bin=min_voids_per_bin,
        )

        metrics: MutableMapping[str, Any] = {
            "backend": backend,
            "z_bin": z_bin,
            "R_v_bin": R_v_bin,
            "R2_wall": R2_wall,
            "S_wall": S_wall,
            "A_sh": shoulder["A_sh"],
            # AUROC_sh is an ensemble-level metric; left at neutral here.
            "AUROC_sh": 0.0,
            "beta_interface": iface["beta_interface"],
            "beta_uncertainty": iface["beta_uncertainty"],
            # beta_bias is defined over an ensemble vs. known truth; neutral here.
            "beta_bias": 0.0,
            "SNR": aux["SNR"],
            "B_mode_residual": aux["B_mode_residual"],
            "n_voids": aux["n_voids"],
            "quality_flags": aux["quality_flags"],
            "profile": {
                "x": profile_x.tolist(),
                "kappa": profile_kappa.tolist(),
                "kappa_err": profile_kappa_err.tolist(),
            },
        }
    else:
        # Fallback: preserve the previous scaffold behaviour if no profile is provided.
        metrics = {
            "backend": backend,
            "z_bin": z_bin,
            "R_v_bin": R_v_bin,
            "R2_wall": 0.0,
            "S_wall": 0.0,
            "A_sh": 0.0,
            "AUROC_sh": 0.0,
            "beta_interface": 0.0,
            "beta_uncertainty": 0.0,
            "beta_bias": 0.0,
            "SNR": 0.0,
            "B_mode_residual": 0.0,
            "n_voids": 0,
            "quality_flags": [],
            "profile": {
                "x": [],
                "kappa": [],
                "kappa_err": [],
            },
        }

    # Ensure that all required keys exist even if the structure above changes.
    for key in REQUIRED_METRIC_KEYS:
        if key not in metrics:
            metrics[key] = None

    return dict(metrics)