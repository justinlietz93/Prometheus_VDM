#!/usr/bin/env python3
"""
Instrumented CEG harness.

This module provides a callable harness for running small-scale CEG experiments
in-memory. By default it does NOT write artifacts; pass `write_artifacts=True`
to enable artifact output (this should only be used with explicit approval).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from Derivation.code.physics.metriplectic.assisted_echo import EchoSpec, run_assisted_echo


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
        Results dictionary produced by `run_assisted_echo`, possibly augmented with
        simple summary diagnostics.
    """
    # Run the assisted echo experiment in-memory
    results = run_assisted_echo(spec)

    # Compute a small, human-friendly diagnostic summary
    diagnostics: Dict[str, Any] = {}
    per_seed = results.get("per_seed", [])

    # compute whether any seed+lambda produced positive ceg
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

    # If write_artifacts was requested, the caller must have approval; we do not
    # enable artifact writes by default to respect CI/no-artifact policy.
    if write_artifacts:
        # Future: write gate_ledger.json and other artifacts using common.io_paths
        # This branch intentionally left inert unless explicitly requested.
        pass

    return results
