"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import math

import pytest

from fum_rt.core.cosmology import (
    BudgetExceededError,
    BudgetTick,
    DenseAccessError,
    GrainScatteringShim,
    HorizonActivityEvent,
    RetardedKernelSH,
    RouterEnergyPartition,
    RouterRuntimeTelemetry,
    RouterSplitEvent,
    VacuumAccumulator,
    check_router_budget_invariant,
)


def _event(**kwargs: object) -> HorizonActivityEvent:
    defaults = dict(
        t=0,
        x=(0.0,),
        dotA=1.0,
        horizon_id="h-0",
        dt_ret=1.0,
    )
    defaults.update(kwargs)
    return HorizonActivityEvent(**defaults)


def test_retarded_kernel_local_causal_accumulation() -> None:
    kernel = RetardedKernelSH(epsilon=0.2, local_radius=1.5, max_events=4)
    events = [
        _event(t=5, x=(0.0,), dotA=2.0, dt_ret=4.0),
        _event(t=6, x=(0.5,), dotA=1.5, dt_ret=3.0),
    ]
    value = kernel.compute(t=8.0, position=(0.25,), events=events)
    expected = 0.0
    for ev in events:
        dt = 8.0 - ev.t
        spatial = max(0.0, 1.0 - abs(ev.x[0] - 0.25) / 1.5)
        temporal = math.exp(-dt / ev.dt_ret)
        expected += ev.dotA * spatial * temporal
    expected *= 0.2
    assert value == pytest.approx(expected)


def test_retarded_kernel_rejects_acausal_and_distant_events() -> None:
    kernel = RetardedKernelSH(epsilon=1.0, local_radius=1.0, max_events=3)
    events = [
        _event(t=10, x=(0.0,), dt_ret=3.0),  # dt < 0 at evaluation -> no contribution
        _event(t=2, x=(5.0,), dt_ret=10.0),  # distance exceeds radius -> ignored
        _event(t=4, x=(0.0,), dt_ret=2.0),  # dt > dt_ret -> ignored
    ]
    value = kernel.compute(t=9.0, position=(0.0,), events=events)
    assert value == pytest.approx(0.0)


def test_retarded_kernel_budget_guard() -> None:
    kernel = RetardedKernelSH(epsilon=1.0, local_radius=1.0, max_events=2)
    events = [_event(t=i + 1, x=(0.0,), dt_ret=5.0) for i in range(3)]
    with pytest.raises(BudgetExceededError):
        kernel.compute(t=6.0, position=(0.0,), events=events)


def test_router_budget_invariant_passes_when_epsilon_small_and_drift_within_tol() -> None:
    result = check_router_budget_invariant(
        [1.0, 1.0 + 5e-9, 1.0 - 4e-9],
        epsilon=1e-9,
        tol_abs=1e-8,
        tol_p95=1e-8,
    )
    assert result["gate_active"]
    assert result["pass"]


def test_router_budget_invariant_fails_on_excess_drift() -> None:
    result = check_router_budget_invariant(
        [1.0, 1.0 + 2e-7],
        epsilon=1e-9,
        tol_abs=1e-8,
        tol_p95=1e-8,
    )
    assert result["gate_active"]
    assert not result["pass"]
    assert result["drift_max"] == pytest.approx(2e-7)


def test_router_budget_invariant_inactive_when_epsilon_large() -> None:
    result = check_router_budget_invariant(
        [1.0, 1.1, 0.9],
        epsilon=1e-3,
        tol_abs=1e-8,
        tol_p95=1e-8,
    )
    assert not result["gate_active"]
    assert result["pass"]


def test_vacuum_accumulator_eta_zero_returns_baseline() -> None:
    kernel = RetardedKernelSH(epsilon=0.5, local_radius=1.0, max_events=4)
    accumulator = VacuumAccumulator(kernel=kernel, rho_lambda=2.0, eta=0.0)
    budget = BudgetTick(tick=0, max_ops=2, max_emits=2, ttl=1)
    events = [_event(t=2, x=(0.0,), dotA=5.0, dt_ret=3.0)]
    result = accumulator.evaluate(
        t=5.0,
        position=(0.0,),
        events=events,
        budget=budget,
    )
    assert result == pytest.approx(2.0)


def test_vacuum_accumulator_budget_guard_propagates() -> None:
    kernel = RetardedKernelSH(epsilon=1.0, local_radius=1.0, max_events=5)
    accumulator = VacuumAccumulator(kernel=kernel, rho_lambda=1.0, eta=0.3)
    budget = BudgetTick(tick=0, max_ops=1, max_emits=1, ttl=1)
    events = [
        _event(t=2, x=(0.0,), dotA=2.0, dt_ret=3.0),
        _event(t=3, x=(0.0,), dotA=1.0, dt_ret=3.0),
    ]
    with pytest.raises(BudgetExceededError):
        accumulator.evaluate(t=5.0, position=(0.0,), events=events, budget=budget)


def test_vacuum_accumulator_eta_scales_kernel_response() -> None:
    kernel = RetardedKernelSH(epsilon=0.1, local_radius=2.0, max_events=4)
    events = [
        _event(t=4, x=(0.0,), dotA=2.0, dt_ret=5.0),
        _event(t=5, x=(0.5,), dotA=1.5, dt_ret=4.0),
    ]
    acc = VacuumAccumulator(kernel=kernel, rho_lambda=1.0, eta=0.25)
    value = acc.evaluate(t=6.0, position=(0.25,), events=events)
    raw = kernel.compute(t=6.0, position=(0.25,), events=events)
    assert value == pytest.approx(1.0 + 0.25 * raw)


def test_grain_scattering_curve_monotone_and_bounded() -> None:
    shim = GrainScatteringShim(
        r_star=0.5,
        mass_scale=1.0,
        v_scale=150.0,
        alpha=2.0,
        sigma_floor=1e-3,
        sigma_ceiling=10.0,
    )
    velocities = [10.0, 50.0, 100.0, 300.0]
    curve = shim.curve(velocities)
    sigmas = [entry["sigmaT_over_m"] for entry in curve]
    assert all(shim.sigma_floor <= s <= shim.sigma_ceiling for s in sigmas)
    assert all(a >= b for a, b in zip(sigmas, sigmas[1:]))


def test_router_energy_partition_from_split_conserves_budget() -> None:
    split = RouterSplitEvent(
        energy_budget=12.0,
        f_vac=0.5,
        f_grain=0.3,
        f_gw=0.2,
    )
    partition = RouterEnergyPartition.from_split(split)
    allocations = partition.as_dict()
    assert pytest.approx(12.0) == allocations["energy_budget"]
    assert pytest.approx(12.0) == allocations["vacuum"] + allocations["grain"] + allocations["gw"]


def test_router_energy_partition_rejects_budget_mismatch() -> None:
    with pytest.raises(ValueError):
        RouterEnergyPartition(
            energy_budget=5.0,
            vacuum=3.0,
            grain=2.5,
            gw=0.0,
        )


def test_router_runtime_telemetry_tracks_budgets_and_locality() -> None:
    budget = BudgetTick(tick=7, max_ops=2, max_emits=1, ttl=1)
    telemetry = RouterRuntimeTelemetry(budget=budget)
    telemetry.record_operation(
        nodes=["n0"],
        edges=[("n0", "n1")],
        neighborhood_degree=3,
    )
    telemetry.record_operation()
    gates = telemetry.gates()
    assert gates["budget_within_limits"]
    assert gates["locality_respected"]
    snapshot = telemetry.snapshot()
    assert snapshot["tick"] == 7
    assert snapshot["ops"] == 2
    assert snapshot["emits"] == 0
    assert snapshot["neighborhood_max_deg"] == 3
    assert snapshot["touched_nodes"] == ["n0"]
    assert snapshot["touched_edges"] == [("n0", "n1")]
    with pytest.raises(BudgetExceededError):
        telemetry.record_operation()
    telemetry.record_emit()
    with pytest.raises(BudgetExceededError):
        telemetry.record_emit()


def test_router_runtime_telemetry_rejects_dense_accessors_and_bad_inputs() -> None:
    telemetry = RouterRuntimeTelemetry(budget=BudgetTick(tick=0, max_ops=3, max_emits=3, ttl=1))
    with pytest.raises(DenseAccessError):
        telemetry.flag_dense_accessor("adjacency_matrix")
    telemetry.flag_dense_accessor("sparse_neighbors")
    with pytest.raises(ValueError):
        telemetry.record_operation(neighborhood_degree=-1)
    with pytest.raises(ValueError):
        telemetry.record_operation(edges=[("a", "b", "c")])


def test_router_runtime_telemetry_locality_gate_flags_breach() -> None:
    budget = BudgetTick(tick=0, max_ops=1, max_emits=2, ttl=1)
    telemetry = RouterRuntimeTelemetry(budget=budget)
    telemetry.record_operation(nodes=["n0", "n1"])
    gates = telemetry.gates()
    assert gates["budget_within_limits"]
    assert not gates["locality_respected"]
