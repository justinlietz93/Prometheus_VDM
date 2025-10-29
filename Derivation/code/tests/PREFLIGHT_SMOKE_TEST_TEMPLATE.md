% PREFLIGHT SMOKE TEST TEMPLATE

Purpose
-------

This template documents the recommended pattern for writing fast, deterministic "preflight" smoke
tests for experiments and runners in this repository. Preflight tests are intended to be run in CI
on every commit/PR: they must be quick, deterministic, and side-effect free (no artifact writes).

Guidelines
----------

- Use very small sizes: N <= 32, steps <= 2.
- Fix RNG seeds (explicit seeds array) for determinism.
- Call the in-memory API (e.g. `run_assisted_echo(EchoSpec(...))`) rather than the CLI that writes files.
- Assert structure and basic invariants (types/keys present), not scientific correctness.
- Do not update approval manifests or write files to `outputs/logs`.
- Run tests with PYTHONPATH=Derivation/code so `common` and `physics` imports resolve.

Example test (copy into `Derivation/code/tests/metriplectic/test_foo_preflight.py`):

```python
"""Minimal preflight-style smoke test template.

Notes:
- Keep the spec small and deterministic.
- Assert presence and types of key outputs, not that gates pass.
"""
from __future__ import annotations

# Import the runner and spec dataclass from the package layout; CI uses PYTHONPATH=Derivation/code
from Derivation.code.physics.metriplectic.assisted_echo import EchoSpec, run_assisted_echo


def test_preflight_example_minimal():
    spec = EchoSpec(
        grid={"N": 16, "dx": 1.0},
        params={"c": 1.0, "m": 0.0, "m_lap_operator": "spectral", "D": 1.0, "r": 0.0, "u": 0.0},
        dt=0.01,
        steps=1,
        seeds=[0],
        lambdas=[0.0, 1.0],
        budget=0.0,
        tag="preflight",
    )

    out = run_assisted_echo(spec)

    # Basic structural checks
    assert isinstance(out, dict)
    assert "per_seed" in out and isinstance(out["per_seed"], list)
    assert "ceg_summary" in out and isinstance(out["ceg_summary"], dict)

    # Gate ledger: ensure it is present and well-formed
    assert "gate_ledger_per_seed" in out and isinstance(out["gate_ledger_per_seed"], list)
    for entry in out["gate_ledger_per_seed"]:
        assert "gates" in entry and isinstance(entry["gates"], list)
        for g in entry["gates"]:
            assert "gate" in g and "passed" in g

    # Summary ledger present
    assert "gate_ledger_summary" in out and isinstance(out["gate_ledger_summary"], dict)

```

How to run locally
-------------------

From the repo root run:

```bash
PYTHONPATH=Derivation/code pytest -q Derivation/code/tests/<your_test_file>.py
```

When to upgrade a preflight to a main-run smoke test
---------------------------------------------------

If you need to validate artifact contents, schema compliance, or gate pass/fail under realistic conditions,
promote the test to a gated main-run smoke test (run under approval or on a schedule). Main-run smoke tests
may write artifacts and take longer to execute.
