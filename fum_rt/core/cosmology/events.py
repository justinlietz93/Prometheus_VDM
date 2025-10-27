"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Event schema and guards for the cosmology router feature."""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Iterable, Tuple

from fum_rt.core.proprioception.events import BaseEvent


class BudgetExceededError(RuntimeError):
    """Raised when a budget guard detects exhaustion for the current tick."""


def _ensure_finite(value: float, name: str) -> float:
    try:
        fv = float(value)
    except Exception as exc:  # pragma: no cover - defensive conversion
        raise ValueError(f"{name} must be convertible to float") from exc
    if not math.isfinite(fv):
        raise ValueError(f"{name} must be finite")
    return fv


@dataclass(frozen=True)
class HorizonActivityEvent(BaseEvent):
    """Local horizon activity routed through the cosmology event bus."""

    kind: str = "horizon_activity"
    t: int = 0
    x: Tuple[float, ...] = field(default_factory=tuple)
    dotA: float = 0.0
    horizon_id: str = ""
    dt_ret: float = 0.0

    def __post_init__(self) -> None:
        coords: Tuple[float, ...]
        if isinstance(self.x, Iterable) and not isinstance(self.x, tuple):
            coords = tuple(float(c) for c in self.x)  # type: ignore[arg-type]
            object.__setattr__(self, "x", coords)
        else:
            coords = self.x
        if not coords:
            raise ValueError("x must contain at least one coordinate")
        for c in coords:
            _ensure_finite(c, "x coordinate")
        if len(coords) > 4:
            raise ValueError("x must be local (≤4 coordinates)")
        dt_ret = _ensure_finite(self.dt_ret, "dt_ret")
        if dt_ret < 0.0:
            raise ValueError("dt_ret must be non-negative")
        if dt_ret == 0.0:
            raise ValueError("dt_ret must encode a strictly retarded window")
        dotA = _ensure_finite(self.dotA, "dotA")
        if self.horizon_id == "":
            raise ValueError("horizon_id must be a non-empty identifier")
        if self.t < 0:
            raise ValueError("t must be non-negative")
        if dotA == 0.0:
            raise ValueError("dotA must carry observable production rate")


@dataclass(frozen=True)
class RouterSplitEvent(BaseEvent):
    """Budget split instruction for the cosmology router channels."""

    kind: str = "router_split"
    energy_budget: float = 0.0
    f_vac: float = 0.0
    f_grain: float = 0.0
    f_gw: float = 0.0

    def __post_init__(self) -> None:
        budget = _ensure_finite(self.energy_budget, "energy_budget")
        if budget < 0.0:
            raise ValueError("energy_budget must be non-negative")
        fractions = (
            _ensure_finite(self.f_vac, "f_vac"),
            _ensure_finite(self.f_grain, "f_grain"),
            _ensure_finite(self.f_gw, "f_gw"),
        )
        for name, value in zip(("f_vac", "f_grain", "f_gw"), fractions):
            if value < 0.0 or value > 1.0:
                raise ValueError(f"{name} must lie in [0, 1]")
        if abs(sum(fractions) - 1.0) > 1e-9:
            raise ValueError("router fractions must sum to 1")

    @property
    def fractions(self) -> Tuple[float, float, float]:
        """Convenience accessor for downstream consumers."""

        return (self.f_vac, self.f_grain, self.f_gw)


@dataclass(frozen=True)
class BudgetTick(BaseEvent):
    """Tick-scoped budget guard used to bound router processing."""

    kind: str = "budget_tick"
    tick: int = 0
    max_ops: int = 0
    max_emits: int = 0
    ttl: int = 1

    def __post_init__(self) -> None:
        if self.tick < 0:
            raise ValueError("tick must be non-negative")
        for name in ("max_ops", "max_emits", "ttl"):
            value = getattr(self, name)
            if not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
        if self.ttl == 0:
            raise ValueError("ttl must be at least 1 tick")

    def guard(self, ops_used: int, emits_used: int, elapsed_ticks: int) -> None:
        """Raise :class:`BudgetExceededError` when any budget is exhausted."""

        if ops_used > self.max_ops:
            raise BudgetExceededError("operation budget exhausted")
        if emits_used > self.max_emits:
            raise BudgetExceededError("emission budget exhausted")
        if elapsed_ticks >= self.ttl:
            raise BudgetExceededError("tick TTL exhausted")

