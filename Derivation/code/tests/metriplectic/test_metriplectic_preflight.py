import math
import pytest
import numpy as np

from physics.metriplectic.metriplectic_structure_checks import StructSpec, run_structure_checks
from physics.metriplectic.run_kg_rd_metriplectic import StepSpec, j_reversibility_kg, j_energy_oscillation_slope, defect_diagnostic
from physics.metriplectic.compose import m_only_step_with_stats, lyapunov_values
from physics.metriplectic.kg_ops import kg_energy, kg_verlet_step
from common.data.preflight_db import log_preflight


def small_stepspec(tag: str = "test-preflight") -> StepSpec:
    return StepSpec(
        bc="periodic",
        scheme="jmj",
        grid={"N": 64, "dx": 1.0},
        params={
            "c": 1.0,
            "m": 0.5,
            "seed_scale": 0.05,
            # Provide RD coefficients for M-limb (required by compose.m_only_step_with_stats)
            "D": 1.0,
            "r": 0.0,
            "u": 0.0,
            "m_lap_operator": "spectral",
            # Increase horizon and seeds for stable slope/R^2 without long runs
            "j_energy_T": 24.0,
            "j_energy_burnT": 1.0,
            # Norm for JMJ two-grid diagnostic
            "norm": "phi_only",
            "tag": tag,
        },
        dt_sweep=[0.1, 0.05, 0.025, 0.0125],
        seeds=5,
        notes="preflight quick sweep",
        tag=tag,
    )


def _omega_max(N: int, dx: float, c: float, m: float) -> float:
    L = N * dx
    k_idx = np.fft.fftfreq(N, d=dx) * L
    om = 2.0 * np.pi * k_idx / L
    lam_max = float(np.max(om * om))
    return float(np.sqrt(m * m + (c * c) * lam_max))


def _band_limited_init(N: int, L: float, band: tuple[int, int], seed: int, scale: float):
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, L, N, endpoint=False)
    phi = np.zeros(N, dtype=float)
    for m in range(band[0], band[1] + 1):
        phase = rng.uniform(0.0, 2.0 * np.pi)
        phi += np.sin((2.0 * np.pi * m / L) * x + phase)
    phi *= (scale / max(np.max(np.abs(phi)), 1e-12))
    pi = np.zeros_like(phi)
    return phi, pi


def _energy_slope_in_memory(N: int, dx: float, c: float, m: float, seed_scale: float, dt_ladder_count: int = 4, steps: int = 400) -> tuple[float, float]:
    L = N * dx
    wmax = _omega_max(N, dx, c, m)
    dt_max = 0.8 / max(wmax, 1e-30)
    dt_list = [dt_max / (2 ** j) for j in range(dt_ladder_count)]
    AH_all: list[float] = []
    for dt in dt_list:
        amps: list[float] = []
        for (lo, hi) in [(1, 3), (4, 6)]:
            for s in range(1):
                seed = lo * 100 + hi * 10 + s
                phi, pi = _band_limited_init(N, L, (lo, hi), seed, seed_scale)
                H_series = np.empty(steps + 1, dtype=float)
                H_series[0] = kg_energy(phi, pi, dx, c, m)
                for n in range(1, steps + 1):
                    phi, pi = kg_verlet_step(phi, pi, dt, dx, c, m)
                    H_series[n] = kg_energy(phi, pi, dx, c, m)
                AH = 0.5 * (float(np.max(H_series)) - float(np.min(H_series)))
                amps.append(AH)
        AH_all.append(float(np.median(np.array(amps))))
    x = np.log(np.array(dt_list))
    y = np.log(np.array(AH_all) + 1e-30)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, b = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = A @ np.array([slope, b])
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)
    return float(slope), float(R2)


def test_j_only_reversibility_and_energy_slope(monkeypatch, tmp_path):
    # Avoid artifact writes from the runner: patch log_path/write_log to tmp/no-op
    import physics.metriplectic.run_kg_rd_metriplectic as rk
    monkeypatch.setattr(rk, "log_path", lambda domain, slug, failed=False, type="json": tmp_path / f"{slug}.{type}", raising=True)
    monkeypatch.setattr(rk, "write_log", lambda p, data: None, raising=True)
    spec = small_stepspec("preflight-j")
    # Reversibility must pass strict or cap
    jr = j_reversibility_kg(spec)
    assert (jr.get("passes_strict") or jr.get("cap_ok")), f"J-only reversibility failed: {jr}"  # nosec B101

    # Noether (energy) drift bound under time-reversal: after +dt then -dt, |W2-W0| <= 1e-8
    e01 = float(jr.get("energy_drifts", {}).get("W1_minus_W0", float("inf")))
    e20 = float(jr.get("energy_drifts", {}).get("W2_minus_W0", float("inf")))
    noether_ok = (abs(e20) <= 1e-8)

    # Energy oscillation slope ~2, R^2 ~ 1 (pure in-memory diagnostic, no artifact writes)
    slope, R2 = _energy_slope_in_memory(N=64, dx=1.0, c=1.0, m=0.5, seed_scale=0.05, dt_ladder_count=4, steps=400)
    passed = (1.95 <= slope <= 2.05) and (R2 >= 0.999)
    # Log preflight record
    log_preflight(
        "j_only_energy_slope",
        config={"N":64, "dx":1.0, "c":1.0, "m":0.5, "seed_scale":0.05, "dt_ladder_count":4, "steps":400},
        results={"reversibility": jr, "noether_ok": bool(noether_ok), "slope": float(slope), "R2": float(R2), "passed": bool(passed and noether_ok)},
        status="pass" if (passed and noether_ok) else "fail",
    )
    assert noether_ok, f"Noether drift out of bounds after time-reversal: W2-W0={e20:.3e}"  # nosec B101
    assert 1.95 <= slope <= 2.05, f"Energy-osc slope out of band: {slope}"  # nosec B101
    assert R2 >= 0.999, f"Energy-osc R2 too low: {R2}"  # nosec B101


def test_structure_checks_J_skew_and_M_psd(monkeypatch, tmp_path):
    # Avoid artifact writes: patch save_figure and write_log to tmp/no-op
    import physics.metriplectic.metriplectic_structure_checks as sc
    monkeypatch.setattr(sc, "save_figure", lambda domain, slug, fig, failed=False: tmp_path / f"{slug}.png", raising=True)
    monkeypatch.setattr(sc, "write_log", lambda p, data: None, raising=True)
    ss = StructSpec(grid={"N": 64, "dx": 1.0}, params={"c": 1.0, "m": 0.5, "D": 1.0, "m_lap_operator": "spectral"}, draws=48, tag="preflight-struct")
    out = run_structure_checks(ss)
    log_preflight(
        "structure_checks_J_skew_M_PSD",
        config={"grid": ss.grid, "params": ss.params, "draws": ss.draws},
        results=out,
        status="pass" if (out["J_skew"]["passed"] and out["M_psd"]["passed"]) else "fail",
    )
    assert out["J_skew"]["passed"], f"J skew check failed: {out}"  # nosec B101
    assert out["M_psd"]["passed"], f"M PSD check failed: {out}"  # nosec B101


def test_strang_defect_slope_near_three(monkeypatch, tmp_path):
    # Avoid artifact writes: patch figure/log paths and savefig to tmp/no-op
    import physics.metriplectic.run_kg_rd_metriplectic as rk
    monkeypatch.setattr(rk, "figure_path", lambda domain, slug, failed=False: tmp_path / f"{slug}.png", raising=True)
    monkeypatch.setattr(rk, "log_path", lambda domain, slug, failed=False, type="json": tmp_path / f"{slug}.{type}", raising=True)
    import matplotlib.pyplot as plt
    monkeypatch.setattr(plt, "savefig", lambda *args, **kwargs: None, raising=True)
    spec = small_stepspec("preflight-defect")
    dd = defect_diagnostic(spec)
    slope = float(dd["fit"]["slope"]) ; R2 = float(dd["fit"]["R2"]) 
    log_preflight(
        "strang_defect_jmj_mjm",
        config={"grid": spec.grid, "params": spec.params, "dt_sweep": spec.dt_sweep, "seeds": int(spec.seeds) if isinstance(spec.seeds, int) else list(spec.seeds)},
        results={"slope": slope, "R2": R2, "fit": dd.get("fit", {}), "passed": bool(2.8 <= slope <= 3.2 and R2 >= 0.999)},
        status="pass" if (2.8 <= slope <= 3.2 and R2 >= 0.999) else "fail",
    )
    assert slope >= 2.8 and slope <= 3.2, f"Strang defect slope not ~3: slope={slope}"  # nosec B101
    assert R2 >= 0.999, f"Strang defect R2 too low: {R2}"  # nosec B101


def test_m_only_h_theorem_monotonicity():
    # H-theorem: discrete Lyapunov L_h must not increase under M-only step
    N, dx = 64, 1.0
    params = {"D": 1.0, "r": 0.0, "u": 0.0, "m_lap_operator": "spectral", "dg_tol": 1e-12}
    rng = np.random.default_rng(123)
    W0 = rng.random(N).astype(float) * 0.1
    L0 = lyapunov_values(W0, dx, float(params["D"]), float(params["r"]), float(params["u"]))
    passed_all = True
    deltas = []
    for dt in [0.1, 0.05, 0.025, 0.0125]:
        W1, stats = m_only_step_with_stats(W0, dt, dx, params)
        L1 = lyapunov_values(W1, dx, float(params["D"]), float(params["r"]), float(params["u"]))
        deltas.append(float(L1 - L0))
        passed = (L1 <= L0 + 1e-12)
        passed_all = passed_all and passed
        assert passed, f"H-theorem violated at dt={dt}: L1-L0={L1-L0}"  # nosec B101
    log_preflight(
        "m_only_h_theorem",
        config={"N": N, "dx": dx, "params": params},
        results={"deltas": deltas, "passed": bool(passed_all)},
        status="pass" if passed_all else "fail",
    )
