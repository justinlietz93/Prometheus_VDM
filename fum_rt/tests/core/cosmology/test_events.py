from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from fum_rt.core.cosmology import (
    BudgetExceededError,
    BudgetTick,
    HorizonActivityEvent,
    RouterSplitEvent,
)


def test_horizon_activity_event_valid() -> None:
    event = HorizonActivityEvent(
        t=42,
        x=(1.0, 0.5, -0.25),
        dotA=2.5,
        horizon_id="bh-001",
        dt_ret=0.05,
    )
    assert event.kind == "horizon_activity"
    assert event.x == (1.0, 0.5, -0.25)


def test_horizon_activity_event_rejects_zero_retardation() -> None:
    with pytest.raises(ValueError):
        HorizonActivityEvent(
            t=0,
            x=(0.0,),
            dotA=1.0,
            horizon_id="bh-001",
            dt_ret=0.0,
        )


@pytest.mark.parametrize(
    "fractions",
    [
        (0.2, 0.3, 0.5),
        (0.0, 1.0, 0.0),
        (0.5, 0.25, 0.25),
    ],
)
def test_router_split_event_accepts_unit_sum(fractions: tuple[float, float, float]) -> None:
    event = RouterSplitEvent(
        energy_budget=10.0,
        f_vac=fractions[0],
        f_grain=fractions[1],
        f_gw=fractions[2],
    )
    assert pytest.approx(sum(event.fractions)) == 1.0


@pytest.mark.parametrize(
    "fractions",
    [
        (-0.1, 1.0, 0.1),
        (0.4, 0.4, 0.4),
        (0.5, 0.6, -0.1),
    ],
)
def test_router_split_event_rejects_invalid_fractions(fractions: tuple[float, float, float]) -> None:
    with pytest.raises(ValueError):
        RouterSplitEvent(
            energy_budget=1.0,
            f_vac=fractions[0],
            f_grain=fractions[1],
            f_gw=fractions[2],
        )


def test_budget_tick_guard() -> None:
    tick = BudgetTick(tick=5, max_ops=3, max_emits=2, ttl=4)
    tick.guard(ops_used=3, emits_used=1, elapsed_ticks=3)


@pytest.mark.parametrize(
    "ops, emits, elapsed",
    [
        (4, 0, 0),
        (0, 3, 0),
        (0, 0, 4),
    ],
)
def test_budget_tick_guard_raises_on_exhaustion(ops: int, emits: int, elapsed: int) -> None:
    tick = BudgetTick(tick=0, max_ops=3, max_emits=2, ttl=4)
    with pytest.raises(BudgetExceededError):
        tick.guard(ops_used=ops, emits_used=emits, elapsed_ticks=elapsed)


def test_budget_tick_rejects_invalid_ttl() -> None:
    with pytest.raises(ValueError):
        BudgetTick(tick=1, max_ops=1, max_emits=1, ttl=0)


def test_router_events_are_immutable() -> None:
    event = HorizonActivityEvent(
        t=1,
        x=(0.0, 0.0, 0.0),
        dotA=1.0,
        horizon_id="bh-immutable",
        dt_ret=0.1,
    )
    with pytest.raises(FrozenInstanceError):
        event.t = 2
    split = RouterSplitEvent(
        energy_budget=1.0,
        f_vac=0.5,
        f_grain=0.25,
        f_gw=0.25,
    )
    with pytest.raises(FrozenInstanceError):
        split.energy_budget = 2.0
