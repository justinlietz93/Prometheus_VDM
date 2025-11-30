from __future__ import annotations

"""
Void Lensing Cross-Correlation Meter v1 runner (T2 instrument) — scaffold only.

This runner is a T2 instrument scaffold for the cosmology/void_lensing domain.
It wires CLI, spec loading, config construction, and placeholder calls into the
meter and gate modules.

Non-goals for this file:
- No physics or numerics (no stacking, no wall/shoulder/interface detection).
- No artifact writing via io_paths (no PNG/CSV/JSON outputs).
- No approval/DB side effects.

Canon references (read-only, see proposal for details):
- Derivation/Cosmology/Void_Lensing/T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md
- Derivation/Unification/T0_Unification_Program_Spec_v1.md
- Derivation/code/common/authorization/README.md
- Derivation/code/common/io_paths.py
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

# Locate Derivation root and add Derivation/code and this domain folder to sys.path.
_THIS_FILE = Path(__file__).resolve()
_DERIVATION_ROOT: Optional[Path] = None
for parent in _THIS_FILE.parents:
    if parent.name == "Derivation":
        _DERIVATION_ROOT = parent
        break
if _DERIVATION_ROOT is None:
    # Best-effort fallback; keeps the runner usable in non-standard layouts.
    try:
        _DERIVATION_ROOT = _THIS_FILE.parents[3]
    except Exception:
        _DERIVATION_ROOT = _THIS_FILE.parent

_CODE_ROOT = _DERIVATION_ROOT / "code"
_DOMAIN_ROOT = _CODE_ROOT / "physics" / "cosmology" / "void_lensing"
for _p in (_CODE_ROOT, _DOMAIN_ROOT):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

# Optional imports – these may not exist yet during early scaffolding.
try:  # pragma: no cover - optional in scaffold
    from common import io_paths as _io_paths  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    _io_paths = None  # type: ignore[assignment]

try:  # pragma: no cover - optional in scaffold
    from common.authorization import approval as _approval_mod  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
    _approval_mod = None  # type: ignore[assignment]

try:  # pragma: no cover - local meter module
    import meter  # type: ignore[import]
except Exception:  # pragma: no cover
    meter = None  # type: ignore[assignment]

try:  # pragma: no cover - local gates module
    import void_lensing_meter_gates as vl_gates  # type: ignore[import]
except Exception:  # pragma: no cover
    vl_gates = None  # type: ignore[assignment]

# Required metric keys as defined by the T2 proposal's output schema stub.
REQUIRED_METRIC_KEYS = [
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
]


def _load_spec(path: Path) -> Dict[str, Any]:
    """Load a JSON spec file from disk."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _build_config_from_spec(spec: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Build a lightweight config dict from a spec dict.

    Expected spec shape (per proposal §5.1.4):
        {
            "run_name": "...",
            "version": "1.0.0",
            "tag": "void_lensing_meter-v1",
            "schema_ref": ".../void_lensing_meter-v1.schema.json",
            "parameters": {
                "backend": "...",
                "z_bin": [z_min, z_max],
                "R_v_bin": [R_min, R_max],
                ...
            },
            "seeds": [0, 1, ...]
        }
    """
    parameters = spec.get("parameters", {}) or {}
    backend = parameters.get("backend", "UNKNOWN")
    z_bin = list(parameters.get("z_bin", [0.0, 0.0]))
    R_v_bin = list(parameters.get("R_v_bin", [0.0, 0.0]))

    # Normalize bins to length 2 for structural checks.
    if len(z_bin) < 2:
        z_bin = (z_bin + [0.0, 0.0])[:2]
    if len(R_v_bin) < 2:
        R_v_bin = (R_v_bin + [0.0, 0.0])[:2]

    config: Dict[str, Any] = {
        "tag": spec.get("tag", "void_lensing_meter-v1"),
        "backend": backend,
        "z_bin": z_bin,
        "R_v_bin": R_v_bin,
        "parameters": parameters,
        "seeds": spec.get("seeds", []),
    }
    return config


def _placeholder_results(config: Mapping[str, Any]) -> Dict[str, Any]:
    """Construct a metrics dict with all required keys and neutral placeholder values."""
    backend = str(config.get("backend", "UNKNOWN"))
    z_bin = list(config.get("z_bin", [0.0, 0.0]))
    R_v_bin = list(config.get("R_v_bin", [0.0, 0.0]))
    if len(z_bin) < 2:
        z_bin = (z_bin + [0.0, 0.0])[:2]
    if len(R_v_bin) < 2:
        R_v_bin = (R_v_bin + [0.0, 0.0])[:2]

    metrics: Dict[str, Any] = {
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
    return metrics


def run_meter_and_collect_results(config: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Call the meter implementation if available, otherwise return placeholder metrics.

    In scaffold mode, kappa_map and void_catalog are passed as None. This function
    must remain free of any physics or artifact-writing side effects.
    """
    if meter is not None and hasattr(meter, "run_meter"):
        try:
            return meter.run_meter(  # type: ignore[call-arg]
                kappa_map=None,
                void_catalog=None,
                config=dict(config),
            )
        except Exception:
            # Safe fallback for early development failures.
            return _placeholder_results(config)
    return _placeholder_results(config)


def _evaluate_gates_structural(results: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Structural gate evaluation.

    If the gate module is present, delegate to its evaluate_gates() function.
    Otherwise, or on error, return a PENDING_IMPLEMENTATION status with any
    missing keys listed.
    """
    if vl_gates is not None and hasattr(vl_gates, "evaluate_gates"):
        try:
            out = vl_gates.evaluate_gates(results)  # type: ignore[call-arg]
            if isinstance(out, dict):
                return out
        except Exception:
            # Fall through to structural-only behavior.
            pass

    missing = [k for k in REQUIRED_METRIC_KEYS if k not in results]
    return {
        "status": "PENDING_IMPLEMENTATION",
        "missing_keys": missing,
        "gates": {},
    }


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Void Lensing Cross-Correlation Meter v1 runner (T2 scaffold).",
    )
    parser.add_argument(
        "--spec",
        type=str,
        required=True,
        help="Path to a void_lensing_meter spec JSON (mocks or data).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load spec and build config only; do not call meter or gates.",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entry point for the T2 void-lensing meter scaffold."""
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    spec_path = Path(args.spec).expanduser().resolve()
    if not spec_path.is_file():
        parser.error(f"--spec file not found: {spec_path}")
        return 2

    spec = _load_spec(spec_path)
    config = _build_config_from_spec(spec)

    if args.dry_run:
        # Spec + config are structurally valid; nothing further to do.
        return 0

    # Non–dry-run scaffold path: still no physics or IO, just structure checks.
    results = run_meter_and_collect_results(config)
    _ = _evaluate_gates_structural(results)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())