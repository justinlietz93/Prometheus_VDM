from __future__ import annotations

"""
Event-local memory kernel tests (void-faithful lock-in)

Confirms:
- Writes occur only at touched nodes (vt_touch, spike, delta_w).
- Smoothing occurs only along visited edges (edge_on events) and only affects the two endpoints.
- Determinism under fixed seed and identical event sequences.
"""

from typing import List

from fum_rt.core.memory import MemoryField
from fum_rt.core.proprioception.events import VTTouchEvent, EdgeOnEvent


def _mk_field(gamma=0.5, delta=0.0, kappa=0.25, seed=123) -> MemoryField:
    return MemoryField(head_k=32, keep_max=256, seed=seed, gamma=gamma, delta=delta, kappa=kappa)


def test_edge_only_spread_local() -> None:
    """
    vt_touch at u=1 sets m[1] > 0; edge_on(1,2) spreads only between 1 and 2.
    No other nodes are affected.
    """
    f = _mk_field(gamma=0.5, delta=0.0, kappa=0.25, seed=42)
    evs: List[object] = [
        VTTouchEvent(kind="vt_touch", t=1, token=1, w=2.0),  # m1 += gamma * w = 1.0
        EdgeOnEvent(kind="edge_on", t=1, u=1, v=2),
    ]
    f.fold(evs, tick=1)
    m = f.snapshot_dict(cap=10)
    # After touch: m1=1.0, m2=0.0; smoothing: d = kappa*(m2 - m1) = -0.25
    # => m1=0.75, m2=0.25
    assert abs(m.get(1, 0.0) - 0.75) < 1e-9
    assert abs(m.get(2, 0.0) - 0.25) < 1e-9
    # No other nodes created/changed
    assert 3 not in m or abs(m.get(3, 0.0)) < 1e-12


def test_no_spread_without_edge_event() -> None:
    """
    With two node touches and no edge_on, there is no inter-node smoothing.
    """
    f = _mk_field(gamma=0.5, delta=0.0, kappa=0.25, seed=7)
    evs: List[object] = [
        VTTouchEvent(kind="vt_touch", t=1, token=1, w=2.0),  # m1 += 1.0
        VTTouchEvent(kind="vt_touch", t=1, token=2, w=2.0),  # m2 += 1.0
    ]
    f.fold(evs, tick=1)
    m = f.snapshot_dict(cap=10)
    assert abs(m.get(1, 0.0) - 1.0) < 1e-9
    assert abs(m.get(2, 0.0) - 1.0) < 1e-9
    assert 3 not in m or abs(m.get(3, 0.0)) < 1e-12


def test_seed_determinism_memoryfield() -> None:
    """
    Same seed + identical events => identical snapshot dicts.
    """
    evs: List[object] = [
        VTTouchEvent(kind="vt_touch", t=1, token=5, w=1.0),
        VTTouchEvent(kind="vt_touch", t=1, token=9, w=2.0),
        EdgeOnEvent(kind="edge_on", t=1, u=5, v=9),
        VTTouchEvent(kind="vt_touch", t=2, token=7, w=3.0),
        EdgeOnEvent(kind="edge_on", t=2, u=7, v=9),
    ]
    f1 = _mk_field(gamma=0.3, delta=0.0, kappa=0.15, seed=123)
    f1.fold(evs, tick=2)
    d1 = f1.snapshot_dict(cap=100)

    f2 = _mk_field(gamma=0.3, delta=0.0, kappa=0.15, seed=123)
    f2.fold(evs, tick=2)
    d2 = f2.snapshot_dict(cap=100)

    assert d1 == d2