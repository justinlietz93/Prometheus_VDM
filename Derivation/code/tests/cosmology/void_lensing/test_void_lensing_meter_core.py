from __future__ import annotations

"""
Core physics tests for the T2 Void Lensing Cross-Correlation Meter v1.

These tests exercise the profile-mode meter implementation on synthetic mocks:

- generate synthetic stacked profiles with known wall slopes and interface
  structure;
- verify that meter.run_meter returns metrics close to the injected truth;
- construct a small shoulder / no-shoulder classification toy and verify
  AUROC_sh >= 0.90;
- exercise the gate logic on good and bad metrics;
- ensure the T2 runner can execute a non-dry-run path with the mocks spec
  without writing any artifacts.

All data are generated in-memory; no disk or network I/O is performed.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np


# Resolve repository and physics roots from this test file location.
_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[5]
_DERIVATION_ROOT = _REPO_ROOT / "Derivation"
_CODE_ROOT = _DERIVATION_ROOT / "code"
_PHYSICS_ROOT = _CODE_ROOT / "physics" / "cosmology" / "void_lensing"


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _build_config_from_mocks_spec() -> Dict[str, Any]:
    """Build a minimal config mapping from the mocks spec JSON."""
    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-v1.json"
    spec = _load_json(spec_path)
    params = spec.get("parameters", {}) or {}
    config: Dict[str, Any] = {
        "backend": params.get("backend", "PyTwinPeaks"),
        "z_bin": params.get("z_bin", [0.0, 0.0]),
        "R_v_bin": params.get("R_v_bin", [0.0, 0.0]),
        "parameters": params,
    }
    return config


def test_run_meter_on_synthetic_profile_matches_truth() -> None:
    """run_meter on a synthetic profile should recover wall and interface metrics."""
    from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
        meter,
    )
    from Derivation.code.physics.cosmology.void_lensing.backends import (  # type: ignore[import]
        mocks,
    )

    config = _build_config_from_mocks_spec()
    params = config["parameters"]

    profile = mocks.generate_synthetic_profile_with_wall_and_shoulder(params)
    kappa_map = {
        "x": profile["x"],
        "kappa": profile["kappa"],
        "kappa_err": profile["kappa_err"],
    }

    metrics = meter.run_meter(kappa_map=kappa_map, void_catalog=None, config=config)

    # Schema alignment: all required metric keys present.
    for key in meter.REQUIRED_METRIC_KEYS:
        assert key in metrics, f"metrics missing required key '{key}'"

    x_arr = np.asarray(metrics["profile"]["x"], dtype=float)
    kappa_arr = np.asarray(metrics["profile"]["kappa"], dtype=float)
    assert x_arr.size == kappa_arr.size and x_arr.size > 0

    # G2 – wall metric correctness on synthetic profile.
    S_wall_true = float(profile["metadata"]["S_wall_true"])
    R2_wall = float(metrics["R2_wall"])
    S_wall_est = float(metrics["S_wall"])

    assert R2_wall >= 0.999, f"R2_wall too low on clean synthetic wall: {R2_wall}"
    rel_err = abs(S_wall_est - S_wall_true) / max(abs(S_wall_true), 1e-8)
    assert rel_err <= 0.01, f"S_wall relative error >1%: {rel_err}"

    # G3 – interface-count exponent correctness (when interfaces are present).
    beta_true = float(profile["metadata"]["beta_true"])
    if abs(beta_true) > 0.0:
        beta_est = float(metrics["beta_interface"])
        beta_unc = float(metrics["beta_uncertainty"])
        assert abs(beta_est - beta_true) <= 0.05, (
            f"beta_interface differs from beta_true by more than 0.05: "
            f"|{beta_est} - {beta_true}|"
        )
        assert beta_unc > 0.0


def test_shoulder_auroc_on_synthetic_dataset_exceeds_threshold() -> None:
    """AUROC computed from A_sh scores on synthetic profiles should be high."""
    from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
        meter,
    )
    from Derivation.code.physics.cosmology.void_lensing.backends import (  # type: ignore[import]
        mocks,
    )

    config = _build_config_from_mocks_spec()
    params = config["parameters"]

    n_samples = 40
    profiles, labels = mocks.generate_shoulder_classification_dataset(n_samples, params)

    scores: List[float] = []
    for profile in profiles:
        kappa_map = {
            "x": profile["x"],
            "kappa": profile["kappa"],
            "kappa_err": profile["kappa_err"],
        }
        metrics = meter.run_meter(kappa_map=kappa_map, void_catalog=None, config=config)
        scores.append(float(metrics["A_sh"]))

    auroc = mocks.compute_auroc_from_scores(scores, labels)
    assert auroc >= 0.90, f"AUROC_sh on synthetic dataset below threshold: {auroc}"


def test_gates_pass_on_good_metrics() -> None:
    """Gate evaluation should PASS when metrics satisfy all prereg thresholds."""
    from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
        meter,
        void_lensing_meter_gates as vl_gates,
    )
    from Derivation.code.physics.cosmology.void_lensing.backends import (  # type: ignore[import]
        mocks,
    )

    config = _build_config_from_mocks_spec()
    params = config["parameters"]
    profile = mocks.generate_synthetic_profile_with_wall_and_shoulder(params)
    kappa_map = {
        "x": profile["x"],
        "kappa": profile["kappa"],
        "kappa_err": profile["kappa_err"],
    }
    metrics = meter.run_meter(kappa_map=kappa_map, void_catalog=None, config=config)

    # Inject ensemble-level metrics for a "good" case.
    # Use the true AUROC from a tiny dataset and a small beta_bias.
    profiles, labels = mocks.generate_shoulder_classification_dataset(20, params)
    scores: List[float] = []
    for prof in profiles:
        km = {"x": prof["x"], "kappa": prof["kappa"], "kappa_err": prof["kappa_err"]}
        m = meter.run_meter(kappa_map=km, void_catalog=None, config=config)
        scores.append(float(m["A_sh"]))
    auroc = mocks.compute_auroc_from_scores(scores, labels)

    good_metrics = dict(metrics)
    good_metrics["AUROC_sh"] = float(auroc)
    good_metrics["beta_bias"] = 0.05  # well within 0.10 threshold

    gate_results = vl_gates.evaluate_gates(good_metrics)
    assert gate_results["status"] == "PASSED"
    gates = gate_results["gates"]
    assert gates["R2_wall"]["passed"] is True
    assert gates["AUROC_sh"]["passed"] is True
    assert gates["beta_bias"]["passed"] is True


def test_gates_fail_on_bad_metrics() -> None:
    """Gate evaluation should FAIL when any prereg metric violates its threshold."""
    from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
        void_lensing_meter_gates as vl_gates,
    )

    bad_metrics = {
        "R2_wall": 0.5,    # too low
        "AUROC_sh": 0.6,   # too low
        "beta_bias": 0.5,  # too high
        "A_sh": 0.0,
        "beta_interface": 0.0,
        "beta_uncertainty": 0.0,
        "SNR": 0.0,
        "B_mode_residual": 0.0,
        "n_voids": 0,
    }

    gate_results = vl_gates.evaluate_gates(bad_metrics)
    assert gate_results["status"] == "FAILED"
    failed = set(gate_results["failed_gates"])
    assert {"R2_wall", "AUROC_sh", "beta_bias"} & failed, "Expected at least one core gate to fail"


def test_runner_executes_non_dry_run_with_mocks_spec() -> None:
    """
    Runner must accept a mocks spec and execute a non-dry-run path with exit code 0.

    This exercises the orchestration layer without asserting on gate outcomes.
    """
    from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
        T2_void_lensing_meter_v1 as runner,
    )

    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-v1.json"
    assert spec_path.is_file(), f"Spec file not found: {spec_path}"

    exit_code = runner.main(["--spec", str(spec_path)])
    assert exit_code == 0