#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Instrumented CEG harness: thin wrapper around run_assisted_echo that adds a
top-level 'diagnostics' summary and optionally suppresses artifact I/O.

Intended for programmatic/test use where callers want structured output without
writing logs or figures to disk.
"""
from __future__ import annotations

from typing import Any, Dict

from physics.metriplectic.assisted_echo import EchoSpec, run_assisted_echo


def run_ceg_harness(spec: EchoSpec, *, write_artifacts: bool = True) -> Dict[str, Any]:
    """Run the CEG assisted-echo experiment and return structured results.

    Parameters
    ----------
    spec:
        Fully-populated :class:`EchoSpec` describing the run.
    write_artifacts:
        When ``False`` the harness skips writing logs/figures to disk (useful
        for unit tests and programmatic calls).  When ``True`` behaviour is
        identical to calling :func:`run_assisted_echo` directly.

    Returns
    -------
    dict
        All keys produced by :func:`run_assisted_echo` plus:

        ``diagnostics`` : dict
            High-level gate-pass summary extracted from ``gate_ledger_summary``.
    """
    if write_artifacts:
        result = run_assisted_echo(spec)
    else:
        # Temporarily disable file I/O by monkey-patching the logging helpers.
        # This keeps the harness self-contained without requiring changes to the
        # upstream runner.
        import physics.metriplectic.assisted_echo as _ae_mod
        import common.io_paths as _io_mod

        _orig_log_path = _io_mod.log_path
        _orig_figure_path = _io_mod.figure_path
        _orig_write_log = _io_mod.write_log

        class _DevNull:
            """Path-like object that silently ignores open/write calls."""

            def __init__(self, *_a, **_kw):
                pass

            def open(self, *_a, **_kw):
                import io
                return io.StringIO()

            def __str__(self):
                return "/dev/null"

            def __fspath__(self):
                return "/dev/null"

        def _noop_log_path(*_a, **_kw):
            return _DevNull()

        def _noop_figure_path(*_a, **_kw):
            return _DevNull()

        def _noop_write_log(_path, _data, **_kw):
            pass

        _io_mod.log_path = _noop_log_path  # type: ignore[assignment]
        _io_mod.figure_path = _noop_figure_path  # type: ignore[assignment]
        _io_mod.write_log = _noop_write_log  # type: ignore[assignment]
        try:
            result = run_assisted_echo(spec)
        finally:
            _io_mod.log_path = _orig_log_path
            _io_mod.figure_path = _orig_figure_path
            _io_mod.write_log = _orig_write_log

    # Build diagnostics summary from gate ledger
    ledger: Dict[str, Any] = result.get("gate_ledger_summary", {})
    diagnostics: Dict[str, Any] = {}
    for gate_name, info in ledger.items():
        if isinstance(info, dict):
            diagnostics[gate_name] = {
                "passed": info.get("passed", 0),
                "failed": info.get("failed", 0),
                "pass_rate": info.get("pass_rate"),
                "meets_rate": info.get("meets_rate", False),
            }

    result["diagnostics"] = diagnostics
    return result


__all__ = ["run_ceg_harness"]
