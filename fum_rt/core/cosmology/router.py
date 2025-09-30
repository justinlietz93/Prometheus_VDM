"""Retarded sourcing kernel and router channel utilities for the cosmology module."""

from __future__ import annotations

import json
from dataclasses import dataclass
import math
from typing import Dict, Iterable, List, Sequence, Set, Tuple

from .events import BudgetExceededError, BudgetTick, HorizonActivityEvent, RouterSplitEvent


def _normalize_position(coords: Sequence[float]) -> Tuple[float, ...]:
    """Normalize a coordinate sequence into a finite tuple."""

    try:
        tupled = tuple(float(c) for c in coords)
    except Exception as exc:  # pragma: no cover - defensive conversion
        raise ValueError("coordinates must be convertible to float") from exc
    if not tupled:
        raise ValueError("coordinates must not be empty")
    if len(tupled) > 4:
        raise ValueError("coordinates must remain local (≤4 entries)")
    for value in tupled:
        if not math.isfinite(value):
            raise ValueError("coordinates must be finite")
    return tupled


def _percentile(values: Sequence[float], p: float) -> float:
    if not values:
        return 0.0
    if p <= 0.0:
        return float(min(values))
    if p >= 1.0:
        return float(max(values))
    ordered = sorted(float(v) for v in values)
    idx = int(math.floor(p * (len(ordered) - 1)))
    idx = max(0, min(len(ordered) - 1, idx))
    return float(ordered[idx])


@dataclass
class RetardedKernelSH:
    """Local, causal retarded kernel for horizon sourcing."""

    epsilon: float
    local_radius: float
    max_events: int = 64

    def __post_init__(self) -> None:
        self.epsilon = float(self.epsilon)
        if not math.isfinite(self.epsilon):
            raise ValueError("epsilon must be finite")
        self.local_radius = float(self.local_radius)
        if not math.isfinite(self.local_radius) or self.local_radius <= 0.0:
            raise ValueError("local_radius must be positive and finite")
        if not isinstance(self.max_events, int):
            raise ValueError("max_events must be an integer")
        if self.max_events <= 0:
            raise ValueError("max_events must be positive")

    def compute(
        self,
        t: float,
        position: Sequence[float],
        events: Iterable[HorizonActivityEvent],
        *,
        budget: BudgetTick | None = None,
    ) -> float:
        """Evaluate S_H(t, x) over a bounded, local horizon activity tape."""

        t_eval = float(t)
        if not math.isfinite(t_eval):
            raise ValueError("evaluation time must be finite")
        x = _normalize_position(position)

        total = 0.0
        count = 0
        ops_used = 0
        emits_used = 0
        for event in events:
            if budget is not None:
                budget.guard(ops_used, emits_used, 0)
            if not isinstance(event, HorizonActivityEvent):
                raise TypeError("events must be HorizonActivityEvent instances")
            count += 1
            if count > self.max_events:
                raise BudgetExceededError("retarded kernel event budget exhausted")
            ops_used += 1
            dt = t_eval - float(event.t)
            if dt <= 0.0:
                continue
            dt_ret = float(event.dt_ret)
            if not math.isfinite(dt_ret) or dt_ret <= 0.0:
                continue
            if dt > dt_ret:
                continue
            event_pos = _normalize_position(event.x)
            if len(event_pos) != len(x):
                raise ValueError("event and evaluation positions must share dimensionality")
            dist = self._distance(x, event_pos)
            if dist > self.local_radius:
                continue
            weight = self._weight(dt, dist, dt_ret)
            if weight <= 0.0:
                continue
            dotA = float(event.dotA)
            if not math.isfinite(dotA):
                continue
            total += dotA * weight
        if budget is not None:
            budget.guard(ops_used, emits_used, 0)
        emits_used += 1
        if budget is not None:
            budget.guard(ops_used, emits_used, 0)
        return self.epsilon * total

    def _weight(self, dt: float, distance: float, dt_ret: float) -> float:
        radius = self.local_radius
        if radius <= 0.0:
            return 0.0
        spatial = max(0.0, 1.0 - distance / radius)
        if spatial <= 0.0:
            return 0.0
        temporal = math.exp(-dt / dt_ret)
        return spatial * temporal

    @staticmethod
    def _distance(a: Tuple[float, ...], b: Tuple[float, ...]) -> float:
        return math.sqrt(sum((ai - bi) * (ai - bi) for ai, bi in zip(a, b)))


@dataclass
class VacuumAccumulator:
    """Retarded-kernel accumulator for the vacuum (dark energy) channel."""

    kernel: RetardedKernelSH
    rho_lambda: float
    eta: float

    def __post_init__(self) -> None:
        self.rho_lambda = float(self.rho_lambda)
        self.eta = float(self.eta)
        if not math.isfinite(self.rho_lambda):
            raise ValueError("rho_lambda must be finite")
        if not math.isfinite(self.eta):
            raise ValueError("eta must be finite")

    def evaluate(
        self,
        t: float,
        position: Sequence[float],
        events: Iterable[HorizonActivityEvent],
        *,
        budget: BudgetTick | None = None,
    ) -> float:
        """Return ρ_vac(t) = ρ_Λ + η·S_H(t, x)."""

        base = self.rho_lambda
        if self.eta == 0.0:
            if budget is not None:
                budget.guard(0, 1, 0)
            return base
        contribution = self.kernel.compute(
            t=t,
            position=position,
            events=events,
            budget=budget,
        )
        return base + self.eta * contribution


@dataclass
class GrainScatteringShim:
    """Finite-size soliton grain scattering shim with monotone cross-section."""

    r_star: float
    mass_scale: float
    v_scale: float
    alpha: float = 2.0
    sigma_floor: float = 1e-4
    sigma_ceiling: float = 50.0

    def __post_init__(self) -> None:
        self.r_star = float(self.r_star)
        self.mass_scale = float(self.mass_scale)
        self.v_scale = float(self.v_scale)
        self.alpha = float(self.alpha)
        self.sigma_floor = float(self.sigma_floor)
        self.sigma_ceiling = float(self.sigma_ceiling)
        for name in ("r_star", "mass_scale", "v_scale", "alpha", "sigma_floor", "sigma_ceiling"):
            value = getattr(self, name)
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.r_star <= 0.0:
            raise ValueError("r_star must be positive")
        if self.mass_scale <= 0.0:
            raise ValueError("mass_scale must be positive")
        if self.v_scale <= 0.0:
            raise ValueError("v_scale must be positive")
        if self.alpha <= 0.0:
            raise ValueError("alpha must be positive")
        if self.sigma_floor <= 0.0:
            raise ValueError("sigma_floor must be positive")
        if self.sigma_ceiling <= self.sigma_floor:
            raise ValueError("sigma_ceiling must exceed sigma_floor")

    @property
    def sigma0(self) -> float:
        """Geometric cross-section per unit mass at v → 0."""

        geom = math.pi * self.r_star * self.r_star
        return min(self.sigma_ceiling, max(self.sigma_floor, geom / self.mass_scale))

    def cross_section_per_mass(self, velocity: float) -> float:
        """Return σ_T/m(v) with monotone fall-off controlled by ``alpha``."""

        v = abs(float(velocity))
        if not math.isfinite(v):
            raise ValueError("velocity must be finite")
        ratio = (v / self.v_scale) ** self.alpha
        value = self.sigma0 / (1.0 + ratio)
        return min(self.sigma_ceiling, max(self.sigma_floor, value))

    def curve(self, velocities: Sequence[float]) -> List[Dict[str, float]]:
        """Return a monotone-decreasing σ_T/m curve over the supplied velocity grid."""

        sanitized = sorted(abs(float(v)) for v in velocities)
        if not sanitized:
            raise ValueError("velocities must contain at least one entry")
        values: List[Dict[str, float]] = []
        last_sigma = None
        for v in sanitized:
            sigma_val = self.cross_section_per_mass(v)
            if last_sigma is not None and sigma_val > last_sigma + 1e-12:
                sigma_val = last_sigma
            values.append({"v": v, "sigmaT_over_m": sigma_val})
            last_sigma = sigma_val
        return values

    def curve_to_json(self, velocities: Sequence[float]) -> str:
        """Serialize the scattering curve as JSON for downstream tooling."""

        curve = self.curve(velocities)
        return json.dumps(curve, sort_keys=True)


@dataclass(frozen=True)
class RouterEnergyPartition:
    """Energy bookkeeping across the vacuum, grain, and GW channels."""

    energy_budget: float
    vacuum: float
    grain: float
    gw: float
    tolerance: float = 1e-9

    def __post_init__(self) -> None:
        for name in ("energy_budget", "vacuum", "grain", "gw", "tolerance"):
            value = float(getattr(self, name))
            object.__setattr__(self, name, value)
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.energy_budget < 0.0:
            raise ValueError("energy_budget must be non-negative")
        for name in ("vacuum", "grain", "gw"):
            if getattr(self, name) < 0.0:
                raise ValueError(f"{name} allocation must be non-negative")
        if self.tolerance <= 0.0:
            raise ValueError("tolerance must be positive")
        self.check_conservation()

    def check_conservation(self) -> None:
        """Assert that the allocations sum to the router energy budget."""

        total = self.vacuum + self.grain + self.gw
        scale = max(1.0, self.energy_budget)
        if abs(total - self.energy_budget) > self.tolerance * scale:
            raise ValueError(
                "router channel allocations must conserve the energy budget"
            )

    def as_dict(self) -> Dict[str, float]:
        return {
            "energy_budget": self.energy_budget,
            "vacuum": self.vacuum,
            "grain": self.grain,
            "gw": self.gw,
        }

    @classmethod
    def from_split(
        cls,
        split: RouterSplitEvent,
        *,
        tolerance: float = 1e-9,
    ) -> "RouterEnergyPartition":
        energy = float(split.energy_budget)
        vacuum = energy * float(split.f_vac)
        grain = energy * float(split.f_grain)
        gw = energy * float(split.f_gw)
        return cls(
            energy_budget=energy,
            vacuum=vacuum,
            grain=grain,
            gw=gw,
            tolerance=tolerance,
        )


def check_router_budget_invariant(
    q_values: Sequence[float],
    *,
    epsilon: float,
    tol_abs: float = 1e-8,
    tol_p95: float = 1e-8,
    eps_gate: float = 1e-6,
) -> Dict[str, float | int | bool]:
    """Drift guard for the router accounting scalar Q_router."""

    try:
        seq = [float(v) for v in q_values]
    except Exception:
        return {
            "count": 0,
            "q0": 0.0,
            "drift_mean": 0.0,
            "drift_p95": 0.0,
            "drift_max": 0.0,
            "gate_active": False,
            "pass_abs": False,
            "pass_p95": False,
            "pass": False,
        }
    if not seq:
        return {
            "count": 0,
            "q0": 0.0,
            "drift_mean": 0.0,
            "drift_p95": 0.0,
            "drift_max": 0.0,
            "gate_active": False,
            "pass_abs": False,
            "pass_p95": False,
            "pass": False,
        }
    if any(not math.isfinite(v) for v in seq):
        return {
            "count": 0,
            "q0": 0.0,
            "drift_mean": 0.0,
            "drift_p95": 0.0,
            "drift_max": math.inf,
            "gate_active": False,
            "pass_abs": False,
            "pass_p95": False,
            "pass": False,
        }

    q0 = seq[0]
    drifts = [abs(v - q0) for v in seq]
    count = len(drifts)
    drift_mean = sum(drifts) / float(count)
    drift_p95 = _percentile(drifts, 0.95)
    drift_max = max(drifts)

    eps_val = abs(float(epsilon))
    gate_active = eps_val <= float(eps_gate)
    pass_abs = drift_max <= float(tol_abs)
    pass_p95 = drift_p95 <= float(tol_p95)
    passed = (not gate_active) or (pass_abs and pass_p95)

    return {
        "count": count,
        "q0": q0,
        "drift_mean": drift_mean,
        "drift_p95": drift_p95,
        "drift_max": drift_max,
        "gate_active": gate_active,
        "pass_abs": pass_abs,
        "pass_p95": pass_p95,
        "pass": passed,
    }


class DenseAccessError(RuntimeError):
    """Raised when a dense adjacency accessor is invoked inside the router."""


@dataclass
class RouterRuntimeTelemetry:
    """Per-tick router runtime telemetry with budget guards."""

    budget: BudgetTick
    dense_accessors: Tuple[str, ...] = (
        "adjacency_dense",
        "adjacency_matrix",
        "neighbors_dense",
        "full_state_vector",
    )

    ops: int = 0
    emits: int = 0
    neighborhood_max_deg: int = 0

    def __post_init__(self) -> None:
        self._dense_accessors: Set[str] = {str(name) for name in self.dense_accessors}
        self._touched_nodes: Set[str] = set()
        self._touched_edges: Set[Tuple[str, str]] = set()

    def record_operation(
        self,
        *,
        nodes: Iterable[str] | None = None,
        edges: Iterable[Tuple[str, str]] | None = None,
        neighborhood_degree: int | None = None,
    ) -> None:
        """Record an operation and associated locality footprint."""

        sanitized_nodes: Set[str] = set()
        if nodes is not None:
            for node in nodes:
                sanitized_nodes.add(str(node))
        sanitized_edges: Set[Tuple[str, str]] = set()
        if edges is not None:
            for edge in edges:
                if len(edge) != 2:
                    raise ValueError("edges must be 2-tuples")
                left, right = (str(edge[0]), str(edge[1]))
                sanitized_edges.add((left, right))
        degree_value = None
        if neighborhood_degree is not None:
            degree_value = int(neighborhood_degree)
            if degree_value < 0:
                raise ValueError("neighborhood degree must be non-negative")

        candidate_ops = self.ops + 1
        self.budget.guard(candidate_ops, self.emits, 0)
        self.ops = candidate_ops
        self._touched_nodes.update(sanitized_nodes)
        self._touched_edges.update(sanitized_edges)
        if degree_value is not None:
            self.neighborhood_max_deg = max(self.neighborhood_max_deg, degree_value)

    def record_emit(self) -> None:
        """Record an emitted event within the tick budget."""

        candidate_emits = self.emits + 1
        self.budget.guard(self.ops, candidate_emits, 0)
        self.emits = candidate_emits

    def flag_dense_accessor(self, accessor_name: str) -> None:
        """Raise when a known dense accessor is invoked within the router."""

        name = str(accessor_name)
        if name in self._dense_accessors:
            raise DenseAccessError(f"dense accessor '{name}' is prohibited in router scope")

    def snapshot(self) -> Dict[str, object]:
        """Return a deterministic snapshot for logging the tick telemetry."""

        return {
            "tick": self.budget.tick,
            "ops": self.ops,
            "emits": self.emits,
            "neighborhood_max_deg": self.neighborhood_max_deg,
            "touched_nodes": sorted(self._touched_nodes),
            "touched_edges": sorted(self._touched_edges),
        }

    def gates(self) -> Dict[str, bool]:
        """Return pass/fail flags for budget and locality CI gates."""

        budget_ok = (self.ops <= self.budget.max_ops) and (
            self.emits <= self.budget.max_emits
        )
        locality_ok = (
            len(self._touched_nodes) <= self.budget.max_ops
            and len(self._touched_edges) <= self.budget.max_ops
        )
        return {
            "budget_within_limits": budget_ok,
            "locality_respected": locality_ok,
        }

__all__ = [
    "RetardedKernelSH",
    "VacuumAccumulator",
    "GrainScatteringShim",
    "RouterEnergyPartition",
    "RouterRuntimeTelemetry",
    "DenseAccessError",
    "check_router_budget_invariant",
]

