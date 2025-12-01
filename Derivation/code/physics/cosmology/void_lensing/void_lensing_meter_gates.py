from __future__ import annotations

"""
Void Lensing Cross-Correlation Meter v1 — validation gate logic.

This module provides gate evaluation helpers for the T2 void-lensing meter.

Scope in this phase:

- Apply the preregistered numeric thresholds for the core metrics:
  - R2_wall gate:   R²_wall ≥ 0.98
  - AUROC_sh gate:  AUROC_sh ≥ 0.90
  - beta_bias gate: beta_bias ≤ 0.10
- Return a structured summary of per-metric gate status and an overall status
  "PASSED" / "FAILED" / "PENDING_IMPLEMENTATION".
- Remain side-effect free (no I/O, no logging).

The thresholds and metric names are copied from the prereg manifest
(PRE-REGISTRATION.json) and the T2 proposal for this meter; this module
should be kept in sync with those contracts.
"""

from typing import Any, Dict, Mapping, MutableMapping, Sequence

# Metrics that the gate layer expects to see in the meter results payload for
# structural checks. This list is intentionally slightly broader than the
# directly gated metrics.
REQUIRED_METRIC_KEYS: Sequence[str] = (
    "R2_wall",
    "A_sh",
    "AUROC_sh",
    "beta_interface",
    "beta_uncertainty",
    "beta_bias",
    "SNR",
    "B_mode_residual",
    "n_voids",
)

# Core preregistered gates and their numeric thresholds.
_GATE_SPECS: Mapping[str, Dict[str, Any]] = {
    "R2_wall": {
        "metric": "R2_wall",
        "operator": ">=",
        "threshold": 0.98,
        "unit": "dimensionless",
    },
    "AUROC_sh": {
        "metric": "AUROC_sh",
        "operator": ">=",
        "threshold": 0.90,
        "unit": "dimensionless",
    },
    "beta_bias": {
        "metric": "beta_bias",
        "operator": "<=",
        "threshold": 0.10,
        "unit": "dimensionless",
    },
}


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _evaluate_single_gate(name: str, results: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Evaluate a single gate given its specification and the results mapping.

    For non-gated metrics (those not in _GATE_SPECS), the returned dict has
    operator/threshold/passed=None and only echoes the value.
    """
    spec = _GATE_SPECS.get(name)
    value = results.get(name)

    if spec is None:
        # Structurally relevant metric, but not directly gated.
        return {
            "metric": name,
            "value": value,
            "operator": None,
            "threshold": None,
            "unit": None,
            "passed": None,
        }

    operator = spec["operator"]
    threshold = spec["threshold"]
    unit = spec["unit"]

    if not _is_number(value):
        # Missing or non-numeric value: cannot evaluate numerically.
        return {
            "metric": name,
            "value": value,
            "operator": operator,
            "threshold": threshold,
            "unit": unit,
            "passed": None,
        }

    v = float(value)
    thr = float(threshold)
    if operator == ">=":
        passed = v >= thr
    elif operator == "<=":
        passed = v <= thr
    else:
        # Unknown operator; treat as unevaluated.
        passed = None

    return {
        "metric": name,
        "value": v,
        "operator": operator,
        "threshold": thr,
        "unit": unit,
        "passed": passed,
    }


def evaluate_gates(results: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Evaluate preregistered gates for a single meter result mapping.

    Parameters
    ----------
    results:
        Mapping produced by the void-lensing meter. Expected to contain,
        at minimum, the keys listed in REQUIRED_METRIC_KEYS.

    Returns
    -------
    gate_results:
        Dictionary with structure:

        {
            "status": "PASSED" | "FAILED" | "PENDING_IMPLEMENTATION",
            "missing_keys": [...],
            "gates": {
                "R2_wall": { "metric": ..., "value": ..., "operator": ">=", "threshold": 0.98,
                             "unit": "dimensionless", "passed": True/False/None },
                "AUROC_sh": { ... },
                "beta_bias": { ... },
                "A_sh": { "metric": "A_sh", "value": ..., "operator": None, "threshold": None,
                          "unit": None, "passed": None },
                ...
            },
            "failed_gates": ["R2_wall", ...],  # only for gates that were evaluated and failed
        }

    Notes
    -----
    - If any of the core gating metrics (R2_wall, AUROC_sh, beta_bias) are
      missing or non-numeric, overall status is "PENDING_IMPLEMENTATION".
    - Otherwise, status is "PASSED" if all core gates pass, or "FAILED" if any
      fails.
    """
    missing = [k for k in REQUIRED_METRIC_KEYS if k not in results]

    gates: MutableMapping[str, Dict[str, Any]] = {}

    # Evaluate core preregistered gates.
    for name in ("R2_wall", "AUROC_sh", "beta_bias"):
        gates[name] = _evaluate_single_gate(name, results)

    # Additional metrics that are structurally relevant but not directly gated.
    for extra in (
        "A_sh",
        "beta_interface",
        "beta_uncertainty",
        "SNR",
        "B_mode_residual",
        "n_voids",
    ):
        if extra not in gates:
            gates[extra] = _evaluate_single_gate(extra, results)

    # Determine overall status.
    failed_gates = [
        name
        for name, info in gates.items()
        if name in _GATE_SPECS and info.get("passed") is False
    ]

    # Check for missing or non-numeric core metrics.
    core_pending = False
    for core_name in ("R2_wall", "AUROC_sh", "beta_bias"):
        info = gates.get(core_name, {})
        if info.get("passed") is None:
            core_pending = True
            break

    if core_pending:
        status = "PENDING_IMPLEMENTATION"
    elif failed_gates:
        status = "FAILED"
    else:
        status = "PASSED"

    return {
        "status": status,
        "missing_keys": missing,
        "gates": dict(gates),
        "failed_gates": failed_gates,
    }


def summarize_gate_outcomes(gate_results: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Summarize gate outcomes into a compact dictionary.

    Parameters
    ----------
    gate_results:
        Output of evaluate_gates().

    Returns
    -------
    summary:
        Dictionary with high-level information, intended for logging or quick
        structural checks. Example:

        {
            "status": "PASSED",
            "n_gates": 6,
            "n_missing": 0,
            "n_failed": 0,
            "any_values_present": true,
        }
    """
    gates = gate_results.get("gates", {}) or {}
    missing = gate_results.get("missing_keys", []) or []
    failed = gate_results.get("failed_gates", []) or []

    any_values_present = any(
        (isinstance(gate, Mapping) and gate.get("value") is not None)
        for gate in gates.values()
    )

    summary: Dict[str, Any] = {
        "status": str(gate_results.get("status", "PENDING_IMPLEMENTATION")),
        "n_gates": len(gates),
        "n_missing": len(missing),
        "n_failed": len(failed),
        "any_values_present": bool(any_values_present),
    }
    return summary