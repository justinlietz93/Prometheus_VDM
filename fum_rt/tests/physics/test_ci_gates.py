"""Tests for cosmology router CI gate validators."""

from __future__ import annotations

import pytest

from fum_rt.physics.ci_gates import (
    GateViolationError,
    validate_payload,
    validate_required_gates,
    validate_gate_summary,
)


def _base_payload(**gates: bool) -> dict:
    return {
        "gates": gates,
        "gate_summary": {"all_passed": all(gates.values()), "failed": [k for k, v in gates.items() if not v]},
    }


def test_validate_payload_passes_when_all_gates_present() -> None:
    payload = _base_payload(
        budget_within_limits=True,
        locality_respected=True,
        qdrift_delta_below_tol=True,
    )
    result = validate_payload(
        payload,
        ["budget_within_limits", "locality_respected", "qdrift_delta_below_tol"],
    )
    assert set(result.keys()) == {
        "budget_within_limits",
        "locality_respected",
        "qdrift_delta_below_tol",
    }


def test_validate_payload_raises_on_missing_gate() -> None:
    payload = _base_payload(budget_within_limits=True)
    with pytest.raises(GateViolationError):
        validate_required_gates(payload, ["budget_within_limits", "locality_respected"])


def test_validate_payload_raises_on_failed_gate() -> None:
    payload = _base_payload(
        budget_within_limits=True,
        locality_respected=False,
    )
    with pytest.raises(GateViolationError):
        validate_payload(payload, ["budget_within_limits", "locality_respected"])


def test_validate_gate_summary_requires_all_passed() -> None:
    payload = {
        "gates": {"a": True},
        "gate_summary": {"all_passed": False, "failed": ["a"]},
    }
    with pytest.raises(GateViolationError):
        validate_gate_summary(payload)
