"""
Global test guard to prevent accidental use of begin_run() for real runs inside tests.

Policy:
- In Derivation/code/tests/*, all DB run rows must be preflight-only.
- Allow begin_run only when preflight=True AND variant contains 'preflight' (as enforced by results_db).
- Otherwise, raise with a clear, explicit message guiding developers/agents to use begin_preflight_run or log_preflight.
"""
from __future__ import annotations

from typing import Any, Optional
import sys

# Import the DB helper
from common.data import results_db as _rdb  # type: ignore

# Stash original function
_original_begin_run = _rdb.begin_run


def _guarded_begin_run(
    domain: str,
    experiment: str,
    tag: str,
    params: Optional[dict[str, Any]] = None,
    engineering_only: bool = False,
    *,
    variant: Optional[str] = None,
    preflight: bool = False,
):
    # Permit only preflight begin_run calls in tests (defense-in-depth with results_db invariants)
    if preflight and (variant is None or ("preflight" in str(variant).lower())):
        return _original_begin_run(
            domain,
            experiment,
            tag,
            params=params,
            engineering_only=engineering_only,
            variant=variant,
            preflight=preflight,
        )

    # Anything else is forbidden in tests: provide a clear, explicit message
    msg = (
        "Forbidden begin_run() usage in tests.\n"
        "All test writes must be preflight-only.\n\n"
        "Do this instead:\n"
        "  - Use common.data.results_db.begin_preflight_run(...)\n"
        "    or\n"
        "  - Use common.data.preflight_db.log_preflight(...) for one-shot logs.\n\n"
        "If you must call begin_run, pass: preflight=True and variant='preflight'.\n"
    )
    raise AssertionError(msg)


# Install guard
_rdb.begin_run = _guarded_begin_run  # type: ignore[assignment]
