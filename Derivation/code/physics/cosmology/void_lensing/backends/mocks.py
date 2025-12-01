from __future__ import annotations

"""
Mock backends for void-lensing κ maps and void catalogues.

This module provides **pure in-memory synthetic generators** for stacked
void-lensing profiles used to test the T2 Void Lensing Cross-Correlation
Meter v1, alongside minimal, import-safe loader stubs.

Scope in this phase:

- No real disk or network I/O.
- No dependence on external simulation or map-making codes.
- Synthetic profiles are generated from simple analytic forms with known
  wall slopes and interface-count structure, suitable for validating the
  meter's core metrics and gates on mocks.

Upstream mock suites (e.g. PyTwinPeaks tunnel-void catalogues,
morphology-weighted SBI, DESI n(z) calibrations) remain black boxes at T2;
this module only documents and implements expected interfaces for the
synthetic preflight stage.
"""

from typing import Any, Dict, Mapping, Sequence, Tuple, List

import numpy as np


def load_mock_suite(suite_name: str = "void_lensing_meter-mocks-v1") -> Tuple[None, Dict[str, Any]]:
    """
    Placeholder loader for a suite of synthetic void-lensing mocks.

    For the Phase-2 preflight core, tests are expected to call the explicit
    generators below (e.g. generate_synthetic_profile_with_wall_and_shoulder)
    rather than this stub. The interface is kept for compatibility with the
    scaffold tests.

    Parameters
    ----------
    suite_name:
        Identifier for the mock suite configuration (e.g. matches the
        spec file name under `specs/void_lensing_meter-mocks-v1.json`).

    Returns
    -------
    mock_bundle, metadata:
        Currently, `mock_bundle` is always None and `metadata` is a small
        dictionary describing the backend and implementation status.
    """
    metadata: Dict[str, Any] = {
        "backend": "mocks",
        "suite_name": suite_name,
        "status": "PENDING_IMPLEMENTATION",
        "description": "Void-lensing mock suite loader stub (use explicit generators for tests).",
    }
    return None, metadata


def load_kappa_map(mock_id: str = "mock_000") -> Tuple[None, Dict[str, Any]]:
    """
    Placeholder loader for an individual synthetic convergence (κ) map.

    Parameters
    ----------
    mock_id:
        Identifier of the mock realisation within a suite.

    Returns
    -------
    kappa_map, metadata:
        Currently, `kappa_map` is always None and `metadata` is a small
        dictionary describing the backend and implementation status.
    """
    metadata: Dict[str, Any] = {
        "backend": "mocks",
        "mock_id": mock_id,
        "status": "PENDING_IMPLEMENTATION",
        "description": "Void-lensing mock κ-map loader stub (no I/O performed).",
    }
    return None, metadata


# ---------------------------------------------------------------------------
# Synthetic profile generators (pure in-memory; no I/O)
# ---------------------------------------------------------------------------


def _linear_wall_profile(
    x: np.ndarray,
    S_wall_true: float,
) -> np.ndarray:
    """
    Construct a purely linear wall profile over all x.

    The wall fit is evaluated only on a restricted range [0.8, 1.2] in tests,
    so this simple linear form is sufficient to attain high R^2 there.
    """
    return S_wall_true * x


def _construct_interface_component(
    x: np.ndarray,
    R_interfaces: Sequence[float],
    slope_amp: float,
) -> np.ndarray:
    """
    Build a 1D profile component whose derivative changes sign at each
    radius in R_interfaces.

    The construction uses a piecewise-constant derivative that flips sign
    at each interface radius; integrating this derivative yields a profile
    with the desired interface structure.
    """
    x = np.asarray(x, dtype=float)
    R = np.asarray(R_interfaces, dtype=float)
    n = x.size
    if n < 2 or R.size == 0:
        return np.zeros_like(x)

    # Sort interfaces in ascending radius.
    R_sorted = np.sort(R)
    n_if = R_sorted.size

    dkdx = np.zeros(n - 1, dtype=float)
    s = 1.0
    i_if = 0
    for j in range(n - 1):
        x_mid = 0.5 * (x[j] + x[j + 1])
        # Flip sign whenever we cross the next interface radius.
        while i_if < n_if and x_mid >= R_sorted[i_if]:
            s *= -1.0
            i_if += 1
        dkdx[j] = s * slope_amp

    k = np.zeros_like(x)
    for j in range(n - 1):
        dx = x[j + 1] - x[j]
        k[j + 1] = k[j] + dkdx[j] * dx

    return k


def _compute_beta_true_from_interfaces(
    R_interfaces: Sequence[float],
    lambda_ref: float,
) -> float:
    """
    Compute a reference beta_true from a set of interface radii.

    This mirrors the linear fit used in the meter for beta_interface, but is
    applied directly to the interface positions and their index counts.
    """
    R = np.asarray(R_interfaces, dtype=float)
    lam = float(lambda_ref) if lambda_ref > 0.0 else float(np.median(R))
    logR = np.log(R / lam)
    y = np.arange(1, R.size + 1, dtype=float)

    X = np.vstack([np.ones_like(logR), logR]).T
    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
    _, beta_true = coeffs
    return float(beta_true)


def generate_synthetic_profile_with_wall_and_shoulder(
    parameters: Mapping[str, Any],
) -> Dict[str, Any]:
    """
    Generate a synthetic stacked κ(x) profile with:

    - a clean linear wall in the range x_wall_range (default [0.8, 1.2]),
    - a compensation-like shoulder at x_sh > 1,
    - a controlled set of interface radii R_interfaces for testing beta_interface.

    Parameters
    ----------
    parameters:
        Mapping of configuration parameters, typically the "parameters" dict
        from the void_lensing_meter-mocks-v1 spec. Expected keys include:
        - "n_radial_bins" (int)
        - "x_wall_range" (2-element sequence)
        - "x_bg_range" (2-element sequence)
        - "lambda_ref" (float)
        - (optional) "shoulder_center", "shoulder_width", "shoulder_amp"

    Returns
    -------
    profile:
        Dictionary with keys:
        - "x", "kappa", "kappa_err": numpy arrays defining the profile;
        - "metadata": dict containing S_wall_true, beta_true, and other
          construction details.
    """
    n_radial_bins = int(parameters.get("n_radial_bins", 30))
    x_wall_range = parameters.get("x_wall_range", [0.8, 1.2])
    x_bg_range = parameters.get("x_bg_range", [2.5, 4.0])
    lambda_ref = float(parameters.get("lambda_ref", 1.0))

    x_min, x_max = 0.2, 4.0
    x = np.linspace(x_min, x_max, n_radial_bins, dtype=float)

    # True wall slope; chosen to be comfortably nonzero.
    S_wall_true = -0.5
    kappa_wall = _linear_wall_profile(x, S_wall_true)

    # Shoulder: a localized Gaussian bump well outside the wall-fit region.
    # The defaults are chosen so that the contribution in x ∈ x_wall_range is
    # negligible, keeping R2_wall extremely close to 1 on mocks.
    default_shoulder_center = max(float(x_wall_range[1]) + 0.4, 1.6)
    shoulder_center = float(parameters.get("shoulder_center", default_shoulder_center))
    shoulder_width = float(parameters.get("shoulder_width", 0.08))
    shoulder_amp = float(parameters.get("shoulder_amp", 0.3))

    # Interface structure: choose a small set of interface radii in the outer region
    # to avoid disturbing the wall fit.
    R_interfaces: List[float] = []
    # Place the interface radii fully outside the shoulder search region:
    # interfaces live at x >= x_bg_min, while the shoulder search ends at
    # x < x_bg_min. This prevents the interface structure from masquerading
    # as a "shoulder" in the AUROC tests.
    R_min_int = max(float(x_bg_range[0]), 2.0)
    R_max_int = min(float(x_bg_range[1]) + 0.5, 3.5)
    if R_max_int > R_min_int:
        R_interfaces = np.linspace(R_min_int, R_max_int, 4).tolist()

    interface_component = (
        _construct_interface_component(x, R_interfaces, slope_amp=0.3) if R_interfaces else np.zeros_like(x)
    )

    # Base profile WITHOUT the shoulder:
    # - For x <= x_wall_max: pure linear wall.
    # - For x > x_wall_max: interface component shifted for continuity at x_wall_max.
    x_wall_max = float(x_wall_range[1])
    wall_mask = x <= x_wall_max
    kappa_base = np.empty_like(kappa_wall)

    kappa_base[wall_mask] = kappa_wall[wall_mask]
    if R_interfaces:
        idx_wall_end = int(np.max(np.where(wall_mask)))
        offset = kappa_wall[idx_wall_end] - interface_component[idx_wall_end]
        kappa_base[~wall_mask] = interface_component[~wall_mask] + offset
    else:
        kappa_base[~wall_mask] = kappa_wall[~wall_mask]

    # Shoulder bump added on top of the base profile.
    if shoulder_amp != 0.0:
        shoulder_bump = shoulder_amp * np.exp(-0.5 * ((x - shoulder_center) / shoulder_width) ** 2)
    else:
        shoulder_bump = np.zeros_like(x)

    kappa = kappa_base + shoulder_bump

    # Small, roughly constant error bars to enable weighted fits and SNR.
    kappa_err = np.full_like(kappa, 0.02, dtype=float)

    # Define beta_true in a way that is closely matched to the meter's own
    # interface-count estimator, using the **interface-only** base profile so
    # that shoulder structure does not bias the truth for G3 tests.
    if R_interfaces:
        try:
            # Local import to avoid hard coupling at module import time.
            from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
                meter as _vl_meter,
            )

            iface_truth = _vl_meter.compute_interface_metrics(
                x=np.asarray(x, dtype=float),
                kappa=np.asarray(kappa_base, dtype=float),
                lambda_ref=float(lambda_ref),
            )
            beta_true = float(iface_truth.get("beta_interface", 0.0))
        except Exception:
            # Fallback to the analytic construction from the interface radii.
            beta_true = _compute_beta_true_from_interfaces(R_interfaces, lambda_ref)
    else:
        beta_true = 0.0

    has_shoulder = bool(shoulder_amp != 0.0)

    profile: Dict[str, Any] = {
        "x": x,
        "kappa": kappa,
        "kappa_err": kappa_err,
        "metadata": {
            "S_wall_true": float(S_wall_true),
            "beta_true": float(beta_true),
            "x_wall_range": list(map(float, x_wall_range)),
            "x_bg_range": list(map(float, x_bg_range)),
            "lambda_ref": float(lambda_ref),
            "R_interfaces": R_interfaces,
            "has_shoulder": has_shoulder,
        },
    }
    return profile


def generate_synthetic_profile_without_shoulder(
    parameters: Mapping[str, Any],
) -> Dict[str, Any]:
    """
    Generate a synthetic stacked κ(x) profile with a clean wall and interface
    structure but **no compensation shoulder**.

    This is intended for use in shoulder/no-shoulder classification tests
    for AUROC_sh.
    """
    # Copy parameters and force the shoulder amplitude to zero so that the
    # generated profile is identical to the wall+interface base profile.
    base_params: Dict[str, Any] = dict(parameters)
    base_params["shoulder_amp"] = 0.0

    profile = generate_synthetic_profile_with_wall_and_shoulder(base_params)
    profile["metadata"]["has_shoulder"] = False
    return profile


def generate_shoulder_classification_dataset(
    n_samples: int,
    parameters: Mapping[str, Any],
) -> Tuple[List[Dict[str, Any]], np.ndarray]:
    """
    Generate a small dataset of profiles with and without shoulders for
    AUROC_sh tests.

    Parameters
    ----------
    n_samples:
        Total number of profiles to generate. Half will have shoulders and
        half will not (rounded down for odd numbers).
    parameters:
        Parameter mapping passed through to the profile generators.

    Returns
    -------
    profiles, labels:
        - profiles: list of profile dicts suitable for meter.run_meter()
          (each contains "x", "kappa", "kappa_err").
        - labels: numpy array of shape (n_effective,) with 1 for "has shoulder"
          and 0 for "no shoulder".
    """
    n_pos = n_samples // 2
    n_neg = n_samples - n_pos

    profiles: List[Dict[str, Any]] = []
    labels: List[int] = []

    # Positive class: enforce a reasonably strong shoulder amplitude so that
    # A_sh is clearly separated from the no-shoulder class after detrending.
    for _ in range(n_pos):
        pos_params: Dict[str, Any] = dict(parameters)
        pos_params.setdefault("shoulder_amp", 0.6)
        prof = generate_synthetic_profile_with_wall_and_shoulder(pos_params)
        profiles.append(prof)
        labels.append(1)

    # Negative class: reuse the deterministic "no shoulder" generator (which
    # internally forces shoulder_amp = 0.0).
    for _ in range(n_neg):
        prof = generate_synthetic_profile_without_shoulder(parameters)
        profiles.append(prof)
        labels.append(0)

    return profiles, np.asarray(labels, dtype=int)


def compute_auroc_from_scores(scores: Sequence[float], labels: Sequence[int]) -> float:
    """
    Compute AUROC from a set of scores and binary labels using numpy only.

    Parameters
    ----------
    scores:
        Iterable of real-valued scores (higher should indicate stronger
        evidence for the positive class).
    labels:
        Iterable of 0/1 labels (1 = positive / has_shoulder).

    Returns
    -------
    auroc:
        Area under the ROC curve in [0, 1].
    """
    scores_arr = np.asarray(scores, dtype=float)
    labels_arr = np.asarray(labels, dtype=int)

    if scores_arr.size == 0 or labels_arr.size != scores_arr.size:
        return 0.5

    # Sort by descending score so that thresholds sweep from high → low.
    order = np.argsort(-scores_arr)
    scores_sorted = scores_arr[order]
    labels_sorted = labels_arr[order]

    P = float(np.sum(labels_sorted == 1))
    N = float(np.sum(labels_sorted == 0))
    if P == 0.0 or N == 0.0:
        # Degenerate case: only one class present.
        return 0.5

    # Unique score thresholds in descending order.
    unique_scores = np.unique(scores_sorted)[::-1]

    tprs: List[float] = []
    fprs: List[float] = []

    for thr in unique_scores:
        pred_pos = scores_sorted >= thr
        tp = float(np.sum((labels_sorted == 1) & pred_pos))
        fp = float(np.sum((labels_sorted == 0) & pred_pos))
        tprs.append(tp / P)
        fprs.append(fp / N)

    # Ensure curve starts at (0,0) and ends at (1,1).
    tprs = [0.0] + tprs + [1.0]
    fprs = [0.0] + fprs + [1.0]

    tprs_arr = np.asarray(tprs, dtype=float)
    fprs_arr = np.asarray(fprs, dtype=float)
    return float(np.trapezoid(tprs_arr, fprs_arr))
