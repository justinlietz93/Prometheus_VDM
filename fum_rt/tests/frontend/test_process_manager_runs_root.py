"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import os
import re
import sys

from fum_rt.frontend.services.process_manager import ProcessManager


def _stub_popen(monkeypatch):
    """
    Install a harmless FakeProc to avoid launching real subprocesses during tests.
    Ensures poll() returns None so start() proceeds without early-exit path.
    """
    class FakeProc:
        def __init__(self, *args, **kwargs):
            self._poll = None
            self.stdin = None

        def poll(self):
            return self._poll

        def terminate(self):
            self._poll = 0

        def wait(self, timeout=None):
            return 0

        def kill(self):
            self._poll = -9

    monkeypatch.setattr(
        "fum_rt.frontend.services.process_manager.subprocess.Popen",
        lambda *a, **k: FakeProc(),
        raising=True,
    )
    # Remove sleeps in detection loop for test speed
    monkeypatch.setattr(
        "fum_rt.frontend.services.process_manager.time.sleep",
        lambda s: None,
        raising=True,
    )


def test_start_defaults_run_dir_under_runs_root(tmp_path, monkeypatch):
    """
    When profile omits run_dir, ProcessManager.start() must synthesize rr/<YYYYMMDD_HHMMSS>
    under the UI-selected runs_root, not ./runs. This guards the default path semantics.

    Verifies that:
      - start() injects profile['run_dir'] BEFORE _build_cmd is called
      - The synthesized run_dir lives under runs_root and matches the timestamp pattern
      - start() returns the same explicit run_dir (explicit branch)
    """
    rr = tmp_path / "runs_root"
    rr.mkdir(parents=True, exist_ok=True)

    pm = ProcessManager(str(rr))
    recorded: dict = {}

    def fake_build_cmd(self, profile):
        # Capture the profile as seen by _build_cmd to assert start() injected run_dir.
        recorded["profile"] = dict(profile)
        return [sys.executable, "-c", "print('noop')"]

    monkeypatch.setattr(ProcessManager, "_build_cmd", fake_build_cmd, raising=True)
    _stub_popen(monkeypatch)

    ok, rd = pm.start({})  # no run_dir in profile
    assert ok is True, "start() should succeed in test harness"
    assert "profile" in recorded, "ProcessManager._build_cmd was not invoked"
    prof = recorded["profile"]
    rd_spec = prof.get("run_dir")
    assert rd_spec, "run_dir was not synthesized under runs_root"
    assert rd_spec.startswith(str(rr)), f"run_dir '{rd_spec}' does not start with runs_root '{rr}'"

    base = os.path.basename(rd_spec.rstrip(os.path.sep))
    assert re.match(r"^\d{8}_\d{6}$", base), f"run_dir basename '{base}' does not match YYYYMMDD_HHMMSS"

    # start() should return the explicit run_dir when specified on the command
    assert rd == rd_spec, "start() did not return the explicit synthesized run_dir"


def test_start_respects_explicit_run_dir(tmp_path, monkeypatch):
    """
    When profile specifies run_dir explicitly (e.g., adoption/engram case),
    ProcessManager.start() must NOT override it with synthesized rr/<timestamp>.
    """
    rr = tmp_path / "rr"
    rr.mkdir(parents=True, exist_ok=True)
    explicit = tmp_path / "custom" / "sessionX"
    explicit.mkdir(parents=True, exist_ok=True)

    pm = ProcessManager(str(rr))
    recorded: dict = {}

    def fake_build_cmd(self, profile):
        recorded["profile"] = dict(profile)
        return [sys.executable, "-c", "print('noop')"]

    monkeypatch.setattr(ProcessManager, "_build_cmd", fake_build_cmd, raising=True)
    _stub_popen(monkeypatch)

    ok, rd = pm.start({"run_dir": str(explicit)})
    assert ok is True
    assert "profile" in recorded
    assert recorded["profile"].get("run_dir") == str(explicit), "Explicit run_dir was altered"
    assert rd == str(explicit), "Returned run_dir does not match explicit path"