from __future__ import annotations

"""
fum_rt.tests.core.test_runner_budget

CI: Verify the void-walker runner is one-shot per tick and enforces microsecond budgets.

- No schedulers, no timers: pure function invoked once per tick by runtime loop.
- Global time guard must drop remaining scouts upon exceeding max_us.
- Rotation by budget["tick"] provides fairness (round-robin start index).

This test uses a deterministic monkeypatch of runner.perf_counter_ns to avoid flaky wall-clock timings.
"""

from typing import Any, List
import math

import os

from fum_rt.core.cortex.void_walkers import runner as _runner


class _FakeEvent:
    def __init__(self, kind: str = "vt_touch") -> None:
        self.kind = kind
        # Optional fields that reducers might access (kept minimal)
        self.t = 0


class _FakeScout:
    def __init__(self, label: str) -> None:
        self.label = label
        self.calls = 0

    def step(self, *, connectome: Any = None, bus: Any = None, maps: Any = None, budget: Any = None) -> list:
        self.calls += 1
        # Emit a minimal event payload (duck-typed BaseEvent)
        return [_FakeEvent("vt_touch")]


def _make_fake_perf_counter_ns(increment_ns: int):
    """
    Returns a deterministic perf_counter_ns function:
    - First call returns 0
    - Each subsequent call increases by increment_ns
    """
    state = {"ns": 0}

    def _fake() -> int:
        v = state["ns"]
        state["ns"] = v + int(increment_ns)
        return v

    return _fake


def test_runner_respects_max_us_breaks(monkeypatch) -> None:
    """
    With increment_ns=600_000 (600 us) per perf_counter_ns call and max_us=1000:
    - Only the first scout executes before the global guard breaks the loop.
    """
    # Patch perf_counter_ns in the runner module namespace
    fake_perf = _make_fake_perf_counter_ns(increment_ns=600_000)
    monkeypatch.setattr(_runner, "perf_counter_ns", fake_perf, raising=True)

    # Prepare scouts (would run 5 if unbounded)
    scouts = [_FakeScout(f"s{i}") for i in range(5)]

    evs = _runner.run_scouts_once(
        connectome=None,
        scouts=scouts,
        maps=None,
        budget={"tick": 0, "visits": 16, "edges": 8, "ttl": 64},
        bus=None,
        max_us=1000,  # 1 ms global budget
    )

    # Exactly one scout should have run
    total_calls = sum(s.calls for s in scouts)
    assert total_calls == 1, f"Expected 1 scout to run under budget; got {total_calls}"
    assert isinstance(evs, list) and len(evs) == 1, "Runner should have returned single event from the first scout"


def test_runner_round_robin_start_index(monkeypatch) -> None:
    """
    With the same deterministic timing and a nonzero tick:
    - Rotation by budget['tick'] should start from that index.
    - Since global guard breaks after first, the selected scout is the rotated head.
    """
    fake_perf = _make_fake_perf_counter_ns(increment_ns=600_000)
    monkeypatch.setattr(_runner, "perf_counter_ns", fake_perf, raising=True)

    scouts = [_FakeScout(f"s{i}") for i in range(5)]
    tick = 3  # rotation offset

    _ = _runner.run_scouts_once(
        connectome=None,
        scouts=scouts,
        maps=None,
        budget={"tick": tick},
        bus=None,
        max_us=1000,
    )

    ran_indices = [i for i, s in enumerate(scouts) if s.calls > 0]
    assert ran_indices == [tick], f"Expected only rotated head scout index {tick} to run; got {ran_indices}"