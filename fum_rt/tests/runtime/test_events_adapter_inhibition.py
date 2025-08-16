import math
import pytest

from fum_rt.runtime.events_adapter import observations_to_events
from fum_rt.core.proprioception.events import (
    BaseEvent,
    DeltaWEvent,
    SpikeEvent,
    VTTouchEvent,
    EdgeOnEvent,
)
from fum_rt.core.cortex.maps.inhibitionmap import InhibitionMap
from fum_rt.core.cortex.maps.excitationmap import ExcitationMap


class Obs:
    """Minimal Observation stub matching adapter expectations."""
    def __init__(self, kind: str, tick: int = 0, nodes=None, meta=None, **kwargs):
        self.kind = kind
        self.tick = int(tick)
        self.nodes = list(nodes or [])
        self.meta = dict(meta or {})
        # pass-through any optional fields (e.g., loop_gain, s_mean, u, v)
        for k, v in (kwargs or {}).items():
            setattr(self, k, v)


def _has_event(evts, cls, **attrs):
    for e in evts:
        if not isinstance(e, cls):
            continue
        ok = True
        for k, v in attrs.items():
            if getattr(e, k, None) != v:
                ok = False
                break
        if ok:
            return True
    return False


def _collect(evts, cls):
    return [e for e in evts if isinstance(e, cls)]


def test_delta_w_negative_emits_inhibitory_spike_and_deltawevent():
    # Given a delta_w observation with negative dw
    obs = Obs(kind="delta_w", tick=5, nodes=[1, 2, 3], meta={"dw": -0.3})
    evts = observations_to_events([obs])

    # Then DeltaWEvent exists for each of the nodes (bounded to first 16 — here 3)
    dws = _collect(evts, DeltaWEvent)
    assert len(dws) == 3
    assert all(isinstance(e, DeltaWEvent) and e.dw == -0.3 for e in dws)

    # And inhibitory SpikeEvent (sign=-1) is synthesized for each node
    inh = [e for e in evts if isinstance(e, SpikeEvent) and int(getattr(e, "sign", 0)) < 0]
    assert len(inh) == 3
    # amp is clipped to [0,1], here 0.3; allow float tolerance
    assert all(math.isclose(float(getattr(e, "amp", 0.0)), 0.3, rel_tol=1e-6, abs_tol=1e-6) for e in inh)


def test_region_stat_emits_vt_touch_and_excit_spikes():
    # Given a region_stat observation
    obs = Obs(kind="region_stat", tick=7, nodes=[10, 11], s_mean=0.6)
    evts = observations_to_events([obs])

    vt = _collect(evts, VTTouchEvent)
    exc = [e for e in evts if isinstance(e, SpikeEvent) and int(getattr(e, "sign", 0)) > 0]

    assert {int(e.token) for e in vt} == {10, 11}
    # spike amp should reflect s_mean (>= 1.0 default replaced by s_mean when available)
    assert len(exc) == 2
    assert all(math.isclose(float(getattr(e, "amp", 0.0)), 0.6, rel_tol=1e-6, abs_tol=1e-6) for e in exc)


def test_cycle_hit_emits_edge_on_and_excit_spikes():
    # Given a cycle_hit with two endpoints
    obs = Obs(kind="cycle_hit", tick=9, nodes=[4, 5], loop_gain=2.5)
    evts = observations_to_events([obs])

    assert _has_event(evts, EdgeOnEvent, u=4, v=5) or _has_event(evts, EdgeOnEvent, u=5, v=4)
    exc = [e for e in evts if isinstance(e, SpikeEvent) and int(getattr(e, "sign", 0)) > 0]
    # Two endpoints => two excit spikes
    assert len(exc) == 2
    # amp should reflect loop_gain (since > 0)
    assert all(math.isclose(float(getattr(e, "amp", 0.0)), 2.5, rel_tol=1e-6, abs_tol=1e-6) for e in exc)


def test_inhibition_map_folds_negative_dw_and_inhibitory_spike():
    # Build events for a single node with both inhibitory sources
    t = 12
    evts = [
        DeltaWEvent(kind="delta_w", t=t, node=42, dw=-0.8),
        SpikeEvent(kind="spike", t=t, node=42, amp=0.9, sign=-1),
        # Control: a positive spike should be ignored by InhibitionMap
        SpikeEvent(kind="spike", t=t, node=7, amp=1.0, sign=+1),
        # Control: a positive dw should be ignored by InhibitionMap
        DeltaWEvent(kind="delta_w", t=t, node=7, dw=+0.2),
    ]

    inh = InhibitionMap(head_k=16, half_life_ticks=32, spike_gain=1.0, dW_gain=0.5)
    inh.fold(evts, tick=t)
    snap = inh.snapshot()

    # Expect at least 1 inhibitory entry registered
    assert int(snap.get("inh_count", 0)) >= 1
    # Max value should reflect some contribution from either inhibitory spike or |dw|
    assert float(snap.get("inh_max", 0.0)) > 0.0


def test_excitation_map_ignores_inhibitory_and_accepts_positive_sources():
    t = 21
    evts = [
        DeltaWEvent(kind="delta_w", t=t, node=13, dw=+0.4),
        SpikeEvent(kind="spike", t=t, node=13, amp=0.7, sign=+1),
        # Inhibitory controls (should be ignored by ExcitationMap)
        DeltaWEvent(kind="delta_w", t=t, node=14, dw=-0.3),
        SpikeEvent(kind="spike", t=t, node=14, amp=0.8, sign=-1),
    ]

    exc = ExcitationMap(head_k=16, half_life_ticks=32, spike_gain=1.0, dW_gain=0.5)
    exc.fold(evts, tick=t)
    snap = exc.snapshot()

    assert int(snap.get("exc_count", 0)) >= 1
    assert float(snap.get("exc_max", 0.0)) > 0.0