"""
Preflight test logging helper.

Writes preflight check records into the per-domain SQLite results database
using the standardized schema in common.data.results_db. Each domain has a
single DB at Derivation/code/outputs/databases/<domain>.sqlite3 and each
"runner" (experiment script) gets its own table. For preflight, we write to a
"pre-flight variant" table for that runner, e.g.:

 - metriplectic: run_kg_rd_metriplectic_preflight
 - metriplectic: metriplectic_structure_checks_preflight
 - metriplectic: compose_preflight (for direct compose.py diagnostics)

If the runner cannot be inferred from the test name, we fall back to a generic
table named "preflight_tests" within the inferred domain.

Notes:
 - No JSONL files are created.
 - Approval checks are bypassed by marking preflight rows as engineering-only.
 - Safe to call inside pytest tests; only a single row is inserted per call.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import platform
import inspect
from typing import Any, Dict

from common import io_paths as _io
from . import results_db as _rdb


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _infer_domain_from_stack(default: str = "metriplectic") -> str:
    """Infer domain name from the calling test file path, e.g., tests/<domain>/....
    Falls back to the provided default when not found.
    """
    try:
        for fr in inspect.stack():  # pragma: no cover (best-effort)
            fn = str(fr.filename)
            parts = fn.replace("\\", "/").split("/")
            if "tests" in parts:
                i = parts.index("tests")
                if i + 1 < len(parts):
                    return parts[i + 1]
    except Exception as _e:  # Fallback on any introspection failure
        return default
    return default


def _preflight_experiment_for(domain: str, test_name: str) -> tuple[str, str]:
    """Map a preflight test to (runner_script, variant_suffix) for table naming.
    Heuristics are domain-local; extend as other domains add preflights.
    """
    name = test_name.lower()
    if domain.lower() == "metriplectic":
        if ("strang" in name) or ("j_only" in name) or ("energy" in name):
            return ("run_kg_rd_metriplectic.py", "preflight")
        if ("structure" in name) or ("skew" in name) or ("psd" in name):
            return ("metriplectic_structure_checks.py", "preflight")
        if ("m_only" in name) or ("h_theorem" in name) or ("lyapunov" in name):
            return ("compose.py", "preflight")
    # Generic fallback: record under compose.py with a generic variant (domain-local)
    return ("compose.py", "preflight_tests")


def _git_hash() -> str | None:
    # Prefer CI-provided hashes if available
    for k in ("GITHUB_SHA", "CI_COMMIT_SHA"):
        v = os.getenv(k)
        if v:
            return v
    # Fallback: optional .git/HEAD read (best-effort, no subprocess)
    try:
        head = (_io.DERIVATION_ROOT.parent / ".git" / "HEAD")
        if head.exists():
            line = head.read_text().strip()
            if line.startswith("ref:"):
                ref = line.split(" ", 1)[1]
                refpath = head.parent / ref
                if refpath.exists():
                    return refpath.read_text().strip()
            return line
    except (OSError, FileNotFoundError, PermissionError):
        return None
    return None


def _as_jsonable(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {str(k): _as_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_as_jsonable(v) for v in obj]
    # Best-effort repr for numpy types etc.
    try:
        import numpy as np  # type: ignore
    except ModuleNotFoundError:
        np = None  # type: ignore
    if 'np' in locals() and np is not None:  # type: ignore
        if isinstance(obj, (np.generic,)):  # type: ignore[attr-defined]
            return obj.item()
    return repr(obj)


def log_preflight(test_name: str, *, config: Dict[str, Any], results: Dict[str, Any], status: str | None = None, tag: str | None = None) -> Path:
    """
    Insert a single preflight record into the per-domain SQLite results DB.

    Args:
        test_name: Short identifier (e.g., "j_only_energy_slope").
        config: Input parameters/config used by the test.
        results: Output metrics/results dictionary.
        status: Optional status (e.g., "pass"/"fail"). If omitted, will try results["passed"].
        tag: Optional tag override. Default is f"pre-flight-{test_name}".
    Returns:
        Path to the per-domain SQLite DB file that was written to.
    """
    tag_val = tag or f"pre-flight-{test_name}"
    status_val = (status if status is not None else ("pass" if bool(results.get("passed", True)) else "fail"))

    # Infer domain from caller path (tests/<domain>/...), then map test -> runner preflight table
    domain = _infer_domain_from_stack("metriplectic")
    experiment, variant = _preflight_experiment_for(domain, test_name)

    # Begin a run row with engineering_only=True to bypass approvals for tests
    # Use dedicated helper to enforce preflight invariants and routing
    handle = _rdb.begin_preflight_run(domain, experiment, tag_val, params=_as_jsonable(config))

    # Log metrics: attach results + environment + test metadata
    metrics = {
        "test": test_name,
        "timestamp": _now_iso(),
        "results": _as_jsonable(results),
        "env": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "git_hash": _git_hash(),
    }
    _rdb.log_metrics(handle, metrics)

    # Finalize row status
    if status_val.lower() == "pass":
        _rdb.end_run_success(handle)
    else:
        _rdb.end_run_failed(handle, metrics=None, error_message=None)

    # Return the DB path for visibility / debugging
    return handle.db_path


__all__ = ["log_preflight"]
