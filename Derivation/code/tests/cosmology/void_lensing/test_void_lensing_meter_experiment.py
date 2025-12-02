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

    # Gate JSON must contain a status field inside gate_results and a run_receipts block.
    gates_json_path = Path(artifacts["gates_json"])
    gate_payload = _load_json(gates_json_path)
    gate_results = gate_payload.get("gate_results", {})
    assert "status" in gate_results, "Gate results JSON missing 'status' field"

    receipts = gate_payload.get("run_receipts", {})
    assert isinstance(receipts, dict) and receipts, "Gate results JSON missing 'run_receipts' block"
    # Minimal structural checks on the receipts payload: commit alias and seeds list.
    assert "git_commit" in receipts, "run_receipts missing 'git_commit' alias"
    assert "seeds" in receipts and isinstance(receipts["seeds"], list), "run_receipts missing 'seeds' list"

    # Gate metrics must include the preregistered H1–H3 metrics.
    gate_metrics = gate_payload.get("gate_metrics", {})
    assert isinstance(gate_metrics, dict) and gate_metrics, "Gate results JSON missing 'gate_metrics' block"
    for metric in ("R2_wall", "AUROC_sh", "beta_bias"):
        assert metric in gate_metrics, f"gate_metrics missing '{metric}'"
        assert isinstance(
            gate_metrics[metric],
            (int, float),
        ), f"gate_metrics['{metric}'] must be numeric"

    # Runs JSON should mirror the same run_receipts block for consistency.
    runs_json_path = Path(artifacts["runs_json"])
    runs_payload = _load_json(runs_json_path)
    runs_receipts = runs_payload.get("run_receipts", {})
    assert isinstance(runs_receipts, dict) and runs_receipts, "Runs JSON missing 'run_receipts' block"

    # Per-run metrics should satisfy the output schema's required keys.
    schema_path = _PHYSICS_ROOT / "schemas" / "void_lensing_meter-v1.schema.json"
    schema = _load_json(schema_path)
    required = schema.get("required", [])
    assert isinstance(required, list) and required, "Schema required[] must be a non-empty list"

    runs = runs_payload.get("runs", [])
    assert isinstance(runs, list) and runs, "Runs JSON missing 'runs' list"
    for run in runs:
        metrics = run.get("metrics", {})
        assert isinstance(metrics, dict) and metrics, "Each run must contain a non-empty 'metrics' dict"
        for key in required:
            assert key in metrics, f"Run metrics missing required key from schema: {key}"

def test_synthetic_mocks_grid_experiment_dry_run() -> None:
    """CLI dry-run should succeed on the extended mocks-grid spec."""
    from Derivation.code.physics.cosmology.void_lensing.experiments import (  # type: ignore[import]
        T2_void_lensing_meter_synthetic_mocks_v1 as exp,
    )

    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-grid-v1.json"
    assert spec_path.is_file(), f"Grid spec file not found: {spec_path}"

    exit_code = exp.main(["--spec", str(spec_path), "--dry-run"])
    assert exit_code == 0


def test_synthetic_mocks_grid_experiment_writes_artifacts(tmp_path: Path, monkeypatch: Any) -> None:
    """
    Running the extended grid experiment (non-dry-run) should produce JSON, CSV,
    and PNG artifacts under the dedicated grid domain.
    """
    from Derivation.code.physics.cosmology.void_lensing.experiments import (  # type: ignore[import]
        T2_void_lensing_meter_synthetic_mocks_v1 as exp,
    )
    from Derivation.code.common import io_paths as io_paths_mod  # type: ignore[import]

    # Redirect all artifact paths used by io_paths into a tmp directory.
    monkeypatch.setattr(io_paths_mod, "OUTPUTS", tmp_path, raising=True)

    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-grid-v1.json"
    assert spec_path.is_file(), f"Grid spec file not found: {spec_path}"

    spec = _load_json(spec_path)
    summary = exp.run_experiment_grid(spec, dry_run=False)

    artifacts = summary.get("artifacts", {})
    # We expect at least runs JSON, gates JSON, CSV, and one PNG figure.
    for key in ("runs_json", "gates_json", "runs_csv", "figure"):
        assert key in artifacts, f"Artifact key '{key}' missing from summary.artifacts"
        path = Path(artifacts[key])
        assert path.is_file(), f"Artifact path for '{key}' does not exist: {path}"

    # Gate JSON must contain a status field inside gate_results and a run_receipts block.
    gates_json_path = Path(artifacts["gates_json"])
    gate_payload = _load_json(gates_json_path)
    gate_results = gate_payload.get("gate_results", {})
    assert "status" in gate_results, "Grid gate results JSON missing 'status' field"

    receipts = gate_payload.get("run_receipts", {})
    assert isinstance(receipts, dict) and receipts, "Grid gate results JSON missing 'run_receipts' block"
    assert "git_commit" in receipts, "Grid run_receipts missing 'git_commit' alias"
    assert "seeds" in receipts and isinstance(
        receipts["seeds"], list
    ), "Grid run_receipts missing 'seeds' list"

    # Gate metrics must include the preregistered H1–H3 metrics.
    gate_metrics = gate_payload.get("gate_metrics", {})
    assert isinstance(gate_metrics, dict) and gate_metrics, "Grid gate results JSON missing 'gate_metrics' block"
    for metric in ("R2_wall", "AUROC_sh", "beta_bias"):
        assert metric in gate_metrics, f"grid gate_metrics missing '{metric}'"
        assert isinstance(
            gate_metrics[metric],
            (int, float),
        ), f"grid gate_metrics['{metric}'] must be numeric"

    # Runs JSON should mirror the same run_receipts block for consistency.
    runs_json_path = Path(artifacts["runs_json"])
    runs_payload = _load_json(runs_json_path)
    runs_receipts = runs_payload.get("run_receipts", {})
    assert isinstance(runs_receipts, dict) and runs_receipts, "Grid runs JSON missing 'run_receipts' block"

    # Per-run metrics should satisfy the output schema's required keys.
    schema_path = _PHYSICS_ROOT / "schemas" / "void_lensing_meter-v1.schema.json"
    schema = _load_json(schema_path)
    required = schema.get("required", [])
    assert isinstance(required, list) and required, "Schema required[] must be a non-empty list"

    runs = runs_payload.get("runs", [])
    assert isinstance(runs, list) and runs, "Grid runs JSON missing 'runs' list"
    for run in runs:
        metrics = run.get("metrics", {})
        assert isinstance(metrics, dict) and metrics, "Each grid run must contain a non-empty 'metrics' dict"
        for key in required:
            assert key in metrics, f"Grid run metrics missing required key from schema: {key}"


def test_synthetic_mocks_grid_v3_has_three_families() -> None:
    """
    The v3 mocks-grid spec should enumerate exactly three distinct mocks families
    via its backends list.
    """
    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-grid-v3.json"
    assert spec_path.is_file(), f"Grid v3 spec file not found: {spec_path}"

    spec = _load_json(spec_path)
    parameters = spec.get("parameters", {}) or {}
    backends = parameters.get("backends", [])
    assert isinstance(backends, list) and backends, "Grid v3 spec must define a non-empty 'backends' list"

    families = sorted(set(str(b) for b in backends))
    assert len(families) == 3, f"Expected exactly 3 distinct mocks families in v3 spec, found {len(families)}"
    assert set(families) == {"PyTwinPeaks", "FlagshipLike", "stress_test"}


def test_synthetic_mocks_grid_v3_dry_run_covers_all_families() -> None:
    """
    CLI dry-run on the v3 mocks-grid spec should succeed, and the constructed grid
    should contain runs from all declared mocks families.
    """
    from Derivation.code.physics.cosmology.void_lensing.experiments import (  # type: ignore[import]
        T2_void_lensing_meter_synthetic_mocks_v1 as exp,
    )

    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-grid-v3.json"
    assert spec_path.is_file(), f"Grid v3 spec file not found: {spec_path}"

    # Dry-run the CLI path to ensure the harness accepts the v3 spec without
    # writing artifacts or requiring approval.
    exit_code = exp.main(["--spec", str(spec_path), "--dry-run"])
    assert exit_code == 0

    spec = _load_json(spec_path)
    parameters = spec.get("parameters", {}) or {}
    backend_list = parameters.get("backends", [])
    families_from_spec = {str(b) for b in backend_list}
    assert families_from_spec, "Grid v3 spec backends list must not be empty"

    # Build the grid directly and check that each declared family appears in at
    # least one grid cell.
    grid = exp.build_grid_from_spec_grid_v1(spec)
    assert len(grid) >= len(families_from_spec), "Grid size must be at least the number of mocks families"

    families_in_grid = {
        str(cell.get("parameters", {}).get("mocks_family", cell.get("backend", "")))
        for cell in grid
    }
    assert families_in_grid == families_from_spec, (
        f"Grid v3 must contain runs from all mocks families; "
        f"expected {families_from_spec}, got {families_in_grid}"
    )