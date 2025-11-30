from __future__ import annotations

"""
Preflight scaffold tests for the T2 Void Lensing Cross-Correlation Meter v1.

These tests are structural only:
- they ensure that the runner, meter, gate, and backend modules import cleanly;
- they validate that the JSON schema and specs are parseable and self-consistent;
- they exercise the runner CLI in --dry-run mode without executing any physics.

No figures/logs are written and no approval manifests are modified.
"""

import json
from pathlib import Path
from typing import Any, Dict

import importlib


# Resolve repository and physics roots from this test file location.
_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parents[5]
_DERIVATION_ROOT = _REPO_ROOT / "Derivation"
_CODE_ROOT = _DERIVATION_ROOT / "code"
_PHYSICS_ROOT = _CODE_ROOT / "physics" / "cosmology" / "void_lensing"


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_can_import_scaffold_modules() -> None:
    """Runner, meter, gates, and backends must all import without side effects."""

    runner = importlib.import_module(
        "Derivation.code.physics.cosmology.void_lensing.T2_void_lensing_meter_v1"
    )
    meter = importlib.import_module(
        "Derivation.code.physics.cosmology.void_lensing.meter"
    )
    gates = importlib.import_module(
        "Derivation.code.physics.cosmology.void_lensing.void_lensing_meter_gates"
    )
    akra = importlib.import_module(
        "Derivation.code.physics.cosmology.void_lensing.backends.akra_hsc_y1"
    )
    dps = importlib.import_module(
        "Derivation.code.physics.cosmology.void_lensing.backends.desy3_dps"
    )
    mocks = importlib.import_module(
        "Derivation.code.physics.cosmology.void_lensing.backends.mocks"
    )

    assert hasattr(runner, "main")
    assert hasattr(meter, "run_meter")
    assert hasattr(gates, "evaluate_gates")
    assert hasattr(akra, "load_kappa_map")
    assert hasattr(dps, "load_kappa_map")
    assert hasattr(mocks, "load_mock_suite")


def test_schema_is_valid_json_and_has_required_keys() -> None:
    """Output schema must be valid JSON and contain the canonical metric keys."""

    from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
        T2_void_lensing_meter_v1 as runner,
    )

    schema_path = _PHYSICS_ROOT / "schemas" / "void_lensing_meter-v1.schema.json"
    schema = _load_json(schema_path)

    # Basic JSON Schema structure
    assert "$schema" in schema
    assert "title" in schema
    assert "properties" in schema and isinstance(schema["properties"], dict)
    assert "required" in schema and isinstance(schema["required"], list)

    properties = schema["properties"]
    required = set(schema["required"])

    # All metrics that the runner expects must appear in the schema.
    for key in runner.REQUIRED_METRIC_KEYS:
        assert key in properties, f"Schema missing property for metric '{key}'"
        assert key in required, f"Schema required[] missing metric '{key}'"


def test_runner_dry_run_executes_without_physics() -> None:
    """
    Runner must accept --spec and --dry-run and exit with code 0.

    This test only verifies that:
    - spec JSON is loadable;
    - config construction does not raise; and
    - the CLI returns 0 without calling into heavy physics or doing any I/O.
    """

    from Derivation.code.physics.cosmology.void_lensing import (  # type: ignore[import]
        T2_void_lensing_meter_v1 as runner,
    )

    spec_path = _PHYSICS_ROOT / "specs" / "void_lensing_meter-mocks-v1.json"
    assert spec_path.is_file(), f"Spec file not found: {spec_path}"

    exit_code = runner.main(["--spec", str(spec_path), "--dry-run"])
    assert exit_code == 0