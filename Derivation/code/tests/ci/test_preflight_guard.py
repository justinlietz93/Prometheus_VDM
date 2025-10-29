"""
CI sanity tests for the preflight runtime guard.

These tests verify that inside the test environment, attempts to start a
non-preflight run are rejected with a clear AssertionError, and that the
preflight convenience API works as intended.

Note:
- We place these under tests/ci to avoid coupling with any specific domain tests.
- Only SQLite DB rows are created (no artifact files are written).
"""
from __future__ import annotations

from pathlib import Path
import os
import pytest

from common.data import results_db as rdb


def _make_dummy_script(tmp_path: Path) -> Path:
    p = tmp_path / "dummy_runner.py"
    p.write_text("# dummy runner for CI guard tests\n", encoding="utf-8")
    return p


def test_forbid_begin_run_in_tests(tmp_path: Path):
    script = _make_dummy_script(tmp_path)
    domain = "ci_preflight_guard"
    tag = "misuse_direct"

    with pytest.raises(AssertionError) as exc:
        rdb.begin_run(domain, str(script), tag)

    msg = str(exc.value)
    assert "Forbidden begin_run() usage in tests" in msg  # nosec B101 (asserts in tests are intended)
    assert "Use common.data.results_db.begin_preflight_run" in msg  # nosec B101


def test_forbid_begin_real_run_helper_in_tests(tmp_path: Path):
    script = _make_dummy_script(tmp_path)
    domain = "ci_preflight_guard"
    tag = "misuse_helper"

    with pytest.raises(AssertionError) as exc:
        # Helper delegates to begin_run(preflight=False) which must be blocked in tests
        rdb.begin_real_run(domain, str(script), tag)

    assert "Forbidden begin_run() usage in tests" in str(exc.value)  # nosec B101


def test_allow_begin_preflight_run_and_query(tmp_path: Path):
    script = _make_dummy_script(tmp_path)
    domain = "ci_preflight_guard"
    tag = "ok_preflight"

    # Ensure approval enforcement cannot interfere even if enabled for real runs
    os.environ["RESULTSDB_SKIP_APPROVAL_CHECK"] = "1"

    handle = rdb.begin_preflight_run(domain, str(script), tag, params={"ci": True})
    try:
        # Minimal lifecycle to exercise writes and hashing
        rdb.log_metrics(handle, {"step": 1})
        rdb.end_run_success(handle, metrics={"ok": 1})

        # Query through the dedicated helper and validate preflight-only
        rows = rdb.get_preflight_runs(domain, str(script))
        # Preflight helper enforces a fixed tag value 'preflight'
        assert any(r.get("tag") == "preflight" for r in rows)  # nosec B101
        assert all(int(r.get("preflight", 0)) == 1 for r in rows)  # nosec B101

        # Table naming should reflect the preflight variant
        assert handle.table.endswith("_preflight")  # nosec B101

        # Convenience helper should return the latest preflight row
        latest = rdb.get_latest_preflight(domain, str(script))
        assert latest is not None  # nosec B101
        assert latest.get("tag") == "preflight"  # nosec B101
    finally:
        # Cleanup the domain DB file to keep CI workspace tidy
        try:
            Path(handle.db_path).unlink(missing_ok=True)
        except Exception as e:
            # Best-effort cleanup only; emit a warning instead of silent pass
            import warnings
            warnings.warn(f"CI preflight guard test cleanup failed: {e}")
