from __future__ import annotations

"""
Void Lensing Cross-Correlation Meter core (T2 instrument) — scaffold only.

This module defines the public meter API for the cosmology/void_lensing domain.
It is intentionally lightweight and free of any real physics or I/O. The
canonical contract for this meter is the T2 proposal for the void-lensing
cross-correlation meter; see project documentation for details.

In the scaffold phase this module:
- exposes a single public entry point, run_meter;
- validates presence of basic config fields where cheap; and
- returns a metrics dictionary with the required keys populated with
  neutral placeholder values.

Non-goals for this module:
- no actual stacking of κ maps or void catalogs;
- no wall, shoulder, or interface detection;
- no artifact writing or approval checks.
"""

from typing import Any, Dict, Mapping, MutableMapping, Sequence

# The required output keys are described in the proposal and repeated in the
# domain README for convenience. Keeping the list here helps keep the
# implementation and any schemas aligned during scaffold work.
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


def run_meter(
    kappa_map: Any,
    void_catalog: Any,
    config: Mapping[str, Any],
) -> Dict[str, Any]:
    """
    Void-lensing cross-correlation meter API (scaffold).

    Parameters
    ----------
    kappa_map:
        Placeholder for a convergence (κ) map object or array. In the scaffold
        this is expected to be None and is not inspected.
    void_catalog:
        Placeholder for a void catalogue structure. In the scaffold this is
        expected to be None and is not inspected.
    config:
        Configuration mapping typically built from a spec JSON. At minimum
        this should provide:

        - "backend": identifier for the upstream pipeline or dataset
        - "z_bin": 2-element sequence with redshift bin edges
        - "R_v_bin": 2-element sequence with void-radius bin edges

    Returns
    -------
    metrics:
        A dictionary with the following required keys, each populated with
        neutral placeholder values that are structurally compatible with the
        expected schema:

        - backend, z_bin, R_v_bin
        - R2_wall, S_wall
        - A_sh, AUROC_sh
        - beta_interface, beta_uncertainty, beta_bias
        - SNR, B_mode_residual
        - n_voids, quality_flags, profile

    Notes
    -----
    This function performs no real physics. It exists solely to provide a
    stable API surface and output structure for tests and higher-level
    orchestration code in the scaffold phase.
    """

    # Defensive copies and normalization of basic config fields.
    backend = str(config.get("backend", "UNKNOWN"))

    def _norm_bin(value: Any) -> list[float]:
        seq = list(value) if isinstance(value, (list, tuple)) else [0.0, 0.0]
        if len(seq) < 2:
            seq = (seq + [0.0, 0.0])[:2]
        return [float(seq[0]), float(seq[1])]

    z_bin = _norm_bin(config.get("z_bin", [0.0, 0.0]))
    R_v_bin = _norm_bin(config.get("R_v_bin", [0.0, 0.0]))

    metrics: MutableMapping[str, Any] = {
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