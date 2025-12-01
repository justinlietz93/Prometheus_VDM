from __future__ import annotations

"""
Experiment harness tests for the T2 Void Lensing Cross-Correlation Meter v1
synthetic-mocks runner.

These tests exercise the experiment-layer around meter.run_meter:

- Dry-run CLI path that builds the synthetic grid but does not write artifacts.
- A small non-dry-run experiment with io_paths.OUTPUTS redirected to a
  temporary directory, verifying that JSON/CSV/PNG artifacts are produced and
  that gate results contain a status field.

All data are generated in-memory using the mocks backend; no real κ maps
or void catalogs are touched.
"""

from pathlib import Path
from typing import Any, Dict

import json

# Resolve repository and physics roots from this test file location.
_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[5]
_DERIVATION_ROOT = _REPO_ROOT / "Derivation"
_CODE_ROOT = _DERIVATION_ROOT / "code"
_PHYSICS_ROOT = _CODE_ROOT / "physics" / "cosmology" / "void_lensing"


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_synthetic_mocks_experiment_dry_run() -> None:
    """CLI dry-run should succeed without writing artifacts."""
    from Derivation.code.physics.cosmology.void_lensing.experiments import (  # type: ignore[import]
        T2_void_lensing_meter_synthetic_mocks_v1 as exp,
    )

    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-v1.json"
    assert spec_path.is_file(), f"Spec file not found: {spec_path}"

    exit_code = exp.main(["--spec", str(spec_path), "--dry-run"])
    assert exit_code == 0


def test_synthetic_mocks_experiment_writes_artifacts(tmp_path: Path, monkeypatch: Any) -> None:
    """
    Running the experiment (non-dry-run) should produce JSON, CSV, and PNG artifacts.

    io_paths.OUTPUTS is redirected to a temporary directory so that tests do not
    write under the canonical Derivation/code/outputs tree.
    """
    from Derivation.code.physics.cosmology.void_lensing.experiments import (  # type: ignore[import]
        T2_void_lensing_meter_synthetic_mocks_v1 as exp,
    )
    from Derivation.code.common import io_paths as io_paths_mod  # type: ignore[import]

    # Redirect all artifact paths used by io_paths into a tmp directory.
    monkeypatch.setattr(io_paths_mod, "OUTPUTS", tmp_path, raising=True)

    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-v1.json"
    assert spec_path.is_file(), f"Spec file not found: {spec_path}"

    spec = _load_json(spec_path)
    summary = exp.run_experiment(spec, dry_run=False)

    artifacts = summary.get("artifacts", {})
    # We expect at least runs JSON, gates JSON, CSV, and one PNG figure.
    for key in ("runs_json", "gates_json", "runs_csv", "figure"):
        assert key in artifacts, f"Artifact key '{key}' missing from summary.artifacts"
        path = Path(artifacts[key])
        assert path.is_file(), f"Artifact path for '{key}' does not exist: {path}"

    # Gate JSON must contain a status field inside gate_results.
    gates_json_path = Path(artifacts["gates_json"])
    gate_payload = _load_json(gates_json_path)
    gate_results = gate_payload.get("gate_results", {})
    assert "status" in gate_results, "Gate results JSON missing 'status' field"