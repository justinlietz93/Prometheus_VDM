"""CI gate validators for cosmology router harness payloads."""

from __future__ import annotations

import json
from typing import Any, Iterable, Mapping, Sequence


class GateViolationError(RuntimeError):
    """Raised when a payload fails a required CI gate."""


def _normalise_gates(gates: Mapping[str, Any]) -> dict[str, bool]:
    return {str(name): bool(value) for name, value in gates.items()}


def validate_gate_summary(payload: Mapping[str, Any]) -> None:
    """Ensure the payload's gate summary reports a clean pass."""

    summary = payload.get("gate_summary")
    if not isinstance(summary, Mapping):
        raise GateViolationError("payload must include a gate_summary mapping")
    all_passed = bool(summary.get("all_passed"))
    if all_passed:
        return
    failed = summary.get("failed")
    if isinstance(failed, Sequence) and failed:
        joined = ", ".join(str(name) for name in failed)
        raise GateViolationError(f"gate_summary reports failing gates: {joined}")
    raise GateViolationError("gate_summary indicates a failure")


def validate_required_gates(
    payload: Mapping[str, Any], required: Iterable[str]
) -> dict[str, bool]:
    """Validate that all required gates exist and pass."""

    gates_obj = payload.get("gates")
    if not isinstance(gates_obj, Mapping):
        raise GateViolationError("payload must include a gates mapping")
    gates = _normalise_gates(gates_obj)
    missing = [name for name in required if name not in gates]
    if missing:
        joined = ", ".join(sorted(str(name) for name in missing))
        raise GateViolationError(f"missing required gates: {joined}")
    failing = [name for name in required if not gates[name]]
    if failing:
        joined = ", ".join(sorted(str(name) for name in failing))
        raise GateViolationError(f"failing gates: {joined}")
    return {name: gates[name] for name in required}


def validate_payload(payload: Mapping[str, Any], required: Iterable[str]) -> dict[str, bool]:
    """Validate the payload against the required gates and summary."""

    validate_gate_summary(payload)
    return validate_required_gates(payload, required)


def load_payload(path: str) -> Mapping[str, Any]:
    """Load a JSON payload from ``path`` for downstream validation."""

    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


__all__ = [
    "GateViolationError",
    "validate_gate_summary",
    "validate_required_gates",
    "validate_payload",
    "load_payload",
]
