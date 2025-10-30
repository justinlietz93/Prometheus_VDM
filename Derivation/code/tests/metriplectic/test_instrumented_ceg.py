#!/usr/bin/env python3
"""
Instrumented CEG preflight harness (tests-only).

- Runs a small-scale CEG experiment fully in-memory
- Does NOT write artifacts by default (write_artifacts=False)
- Intended for CI/preflight validation under Derivation/code/tests

If you need a T3 smoke that writes artifacts, use the production
runner/spec path in physics/metriplectic (assisted_echo.py + specs).
"""
# bandit: disable=B101,B112  # pytest asserts and try/except/continue patterns acceptable in tests
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

# Import production assisted echo
from Derivation.code.physics.metriplectic.assisted_echo import EchoSpec, run_assisted_echo  # type: ignore


def run_ceg_harness(spec: EchoSpec, write_artifacts: bool = False) -> Dict[str, Any]:
    """Run a small CEG harness in-memory and return computed metrics.

    Parameters
    ----------
    spec: EchoSpec
        Echo specification (small sizes for preflight).
    write_artifacts: bool
        If True, the harness may write JSON/CSV artifacts using project helpers.
        Disabled by default to avoid CI artifact generation.

    Returns
    -------
    dict
        Results dictionary produced by `run_assisted_echo`, augmented with
        a simple diagnostics block for preflight checks.
    """
    results = run_assisted_echo(spec)

    # Add lightweight diagnostics
    diagnostics: Dict[str, Any] = {}
    per_seed = results.get("per_seed", [])

    any_positive = False
    ceg_vals: List[float] = []
    for s in per_seed:
        ceg_map = s.get("ceg", {})
        for v in ceg_map.values():
            try:
                fv = float(v)
                ceg_vals.append(fv)
                if fv > 0.0:
                    any_positive = True
            except Exception:
                continue

    diagnostics["any_positive_ceg"] = bool(any_positive)
    diagnostics["ceg_samples"] = ceg_vals[:10]
    results["diagnostics"] = diagnostics

    # Tests keep artifact writing disabled; leave hook for future
    if write_artifacts:
        # Intentionally inert in preflight; production runs should use assisted_echo.py
        pass

    return results


def test_preflight_ceg_smoke() -> None:
    """Tiny preflight: ensure assisted echo pipeline runs in-memory and returns expected keys.

    This test is intentionally small and artifact-free. It validates that the
    production `run_assisted_echo` function produces a well-formed output for a
    small grid and a couple of seeds/lambdas.
    """
    # Minimal spec (very small grid, few steps) for quick CI runs
    spec = EchoSpec(
        grid={"N": 32, "dx": 1.0/32},
        params={"c": 1.0, "m": 0.0, "D": 0.05, "m_lap_operator": "spectral"},
        dt=0.1,
        steps=5,
        seeds=[0, 1],
        lambdas=[0.0, 0.1],
        budget=1e-3,
        tag=None,
    )

    out = run_ceg_harness(spec, write_artifacts=False)

    # Basic structure checks
    assert isinstance(out, dict)
    assert "per_seed" in out and isinstance(out["per_seed"], list)
    assert len(out["per_seed"]) == len(spec.seeds)
    assert "ceg_summary" in out and isinstance(out["ceg_summary"], dict)
    for lam in spec.lambdas:
        assert str(lam) in out["ceg_summary"]

    # Diagnostics present and well-typed
    diag = out.get("diagnostics", {})
    assert isinstance(diag.get("any_positive_ceg", False), bool)
    assert isinstance(diag.get("ceg_samples", []), list)

    # Gate ledger summaries present (pass/fail policy is validated elsewhere)
    assert "gate_ledger_summary" in out and isinstance(out["gate_ledger_summary"], dict)
