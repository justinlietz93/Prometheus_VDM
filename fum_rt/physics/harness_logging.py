"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Reusable helpers for cosmology/physics harness logging payloads."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from typing import Any, Mapping, MutableMapping


def _iso_timestamp() -> str:
    """Return a UTC ISO-8601 timestamp (seconds resolution)."""

    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _run_git_command(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):  # pragma: no cover - defensive
        return None
    output = result.stdout.strip()
    return output or None


def gather_repo_state() -> dict[str, Any]:
    """Return lightweight git metadata for reproducibility."""

    state: dict[str, Any] = {}
    commit = _run_git_command(["rev-parse", "HEAD"])
    if commit:
        state["commit"] = commit
    branch = _run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    if branch and branch != "HEAD":
        state["branch"] = branch
    status = _run_git_command(["status", "--porcelain"])
    if status is not None:
        state["dirty"] = bool(status)
    return state


def hash_jsonable(data: Any) -> str:
    """Compute a deterministic SHA256 for JSON-serialisable ``data``."""

    serialised = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialised.encode("utf-8")).hexdigest()


def hash_file(path: str) -> str:
    """Return the SHA256 hash for ``path``."""

    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalise_mapping(mapping: Mapping[str, Any] | None) -> dict[str, Any]:
    if mapping is None:
        return {}
    return dict(mapping)


def enrich_payload(
    base_payload: Mapping[str, Any],
    *,
    script_name: str,
    gates: Mapping[str, bool],
    seeds: Mapping[str, Any] | None = None,
    budgets: Mapping[str, Any] | None = None,
    hashes: Mapping[str, str] | None = None,
    inputs: Mapping[str, Any] | None = None,
    outputs: Mapping[str, Any] | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """Return an enriched payload ready to persist to disk."""

    payload: MutableMapping[str, Any] = dict(base_payload)
    timestamp = payload.get("timestamp") or _iso_timestamp()
    payload["timestamp"] = timestamp

    base_outputs = dict(payload.get("outputs", {}))
    if outputs:
        base_outputs.update(outputs)
    if base_outputs:
        payload["outputs"] = base_outputs

    gate_map = {key: bool(value) for key, value in gates.items()}
    payload["gates"] = gate_map
    passed = sorted(name for name, ok in gate_map.items() if ok)
    failed = sorted(name for name, ok in gate_map.items() if not ok)
    payload["gate_summary"] = {
        "all_passed": not failed,
        "passed": passed,
        "failed": failed,
    }

    payload["script"] = script_name
    payload["repo"] = gather_repo_state()
    payload["seeds"] = _normalise_mapping(seeds)
    payload["budgets"] = budgets if budgets is None else dict(budgets)
    payload["hashes"] = _normalise_mapping(hashes)
    payload["inputs"] = _normalise_mapping(inputs)
    if notes:
        payload["notes"] = list(notes)

    return dict(payload)


__all__ = [
    "enrich_payload",
    "gather_repo_state",
    "hash_file",
    "hash_jsonable",
]

