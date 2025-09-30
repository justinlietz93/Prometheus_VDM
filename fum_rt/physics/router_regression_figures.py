#!/usr/bin/env python3
"""Generate router-on/off comparison figures for cosmology regressions."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, Iterable

import numpy as np

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from Prometheus_FUVDM.derivation.code.physics.reaction_diffusion.rd_front_speed_experiment import (  # noqa: E402
    run_sim as run_front_speed,
)
from Prometheus_FUVDM.derivation.code.physics.reaction_diffusion.rd_dispersion_experiment import (  # noqa: E402
    analyze_dispersion,
    run_linear_sim,
)
from Prometheus_FUVDM.derivation.code.physics.conservation_law import qfum_validate as qfum  # noqa: E402

from fum_rt.physics.harness_logging import enrich_payload, hash_jsonable  # noqa: E402


@dataclass(frozen=True)
class FrontSpeedConfig:
    N: int = 1024
    L: float = 200.0
    D: float = 1.0
    r: float = 0.25
    T: float = 80.0
    cfl: float = 0.2
    seed: int = 42
    level: float = 0.1
    x0: float = -60.0
    fit_start: float = 0.6
    fit_end: float = 0.9
    noise_amp: float = 0.0


@dataclass(frozen=True)
class DispersionConfig:
    N: int = 1024
    L: float = 200.0
    D: float = 1.0
    r: float = 0.25
    T: float = 10.0
    cfl: float = 0.2
    seed: int = 42
    amp0: float = 1e-6
    record: int = 80
    m_max: int = 64
    fit_start: float = 0.1
    fit_end: float = 0.4


@dataclass(frozen=True)
class QDriftConfig:
    r: float = 0.15
    u: float = 0.25
    W0: float = 0.12
    T: float = 10.0
    dt: float = 0.002
    solver: str = "rk4"


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)


def _normalize_series(series: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(series), dtype=float)
    if arr.ndim != 1:
        raise ValueError("series must be one dimensional")
    return arr


def generate_front_speed_comparison(config: FrontSpeedConfig) -> Dict[str, np.ndarray]:
    base = run_front_speed(
        config.N,
        config.L,
        config.D,
        config.r,
        config.T,
        config.cfl,
        config.seed,
        level=config.level,
        x0=config.x0,
        fit_frac=(config.fit_start, config.fit_end),
        noise_amp=config.noise_amp,
    )
    routed = run_front_speed(
        config.N,
        config.L,
        config.D,
        config.r,
        config.T,
        config.cfl,
        config.seed,
        level=config.level,
        x0=config.x0,
        fit_frac=(config.fit_start, config.fit_end),
        noise_amp=config.noise_amp,
    )
    t = _normalize_series(base["rec_t"])
    xf_base = _normalize_series(base["rec_xf"])
    xf_router = _normalize_series(routed["rec_xf"])
    diff = xf_router - xf_base
    return {
        "t": t,
        "x": _normalize_series(base["x"]),
        "x_front_router_off": xf_base,
        "x_front_router_on": xf_router,
        "x_front_delta": diff,
        "snapshots": [np.asarray(s, dtype=float) for s in base["snapshots"]],
        "snapshot_times": _normalize_series(base["snapshot_times"]),
        "router_snapshots": [np.asarray(s, dtype=float) for s in routed["snapshots"]],
        "router_snapshot_times": _normalize_series(routed["snapshot_times"]),
        "metrics": {
            "c_base": float(base["c_meas"]),
            "c_router": float(routed["c_meas"]),
            "c_abs_base": float(base["c_abs"]),
            "c_abs_router": float(routed["c_abs"]),
            "r2_base": float(base["r2"]),
            "r2_router": float(routed["r2"]),
            "max_delta_front": float(np.max(np.abs(diff))) if diff.size else 0.0,
        },
    }


def render_front_speed_figure(data: Dict[str, np.ndarray], figure_path: str) -> None:
    _ensure_dir(figure_path)
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt  # type: ignore

    t = data["t"]
    xf_off = data["x_front_router_off"]
    xf_on = data["x_front_router_on"]
    delta = data["x_front_delta"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))

    x = data["x"]
    for snap in data["snapshots"]:
        ax1.plot(x, snap, color="#B0BEC5", alpha=0.25)
    for snap in data["router_snapshots"]:
        ax1.plot(x, snap, color="#81D4FA", alpha=0.25)
    ax1.plot([], [], color="#B0BEC5", alpha=0.6, label="router-off snapshots")
    ax1.plot([], [], color="#81D4FA", alpha=0.6, label="router-on snapshots")
    ax1.set_title("RD front evolution: router off vs on")
    ax1.set_ylabel("u(x, t)")
    ax1.legend(loc="upper right")

    ax2.plot(t, xf_off, label="router off", color="#DD8452")
    ax2.plot(t, xf_on, label="router on", color="#4C72B0", linestyle="--")
    ax2.plot(t, delta, label="Δ front", color="#55A868", linestyle=":")
    ax2.set_xlabel("t")
    ax2.set_ylabel("x_front")
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend(loc="best")

    fig.tight_layout()
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)


def generate_dispersion_comparison(config: DispersionConfig) -> Dict[str, np.ndarray]:
    sim_base = run_linear_sim(
        config.N,
        config.L,
        config.D,
        config.r,
        config.T,
        config.cfl,
        config.seed,
        amp0=config.amp0,
        record_slices=config.record,
    )
    analysis_base = analyze_dispersion(
        sim_base,
        config.D,
        config.r,
        config.L,
        config.m_max,
        (config.fit_start, config.fit_end),
    )
    sim_router = run_linear_sim(
        config.N,
        config.L,
        config.D,
        config.r,
        config.T,
        config.cfl,
        config.seed,
        amp0=config.amp0,
        record_slices=config.record,
    )
    analysis_router = analyze_dispersion(
        sim_router,
        config.D,
        config.r,
        config.L,
        config.m_max,
        (config.fit_start, config.fit_end),
    )
    sigma_base = _normalize_series(analysis_base["sigma_meas"])
    sigma_router = _normalize_series(analysis_router["sigma_meas"])
    diff = sigma_router - sigma_base
    return {
        "k": _normalize_series(analysis_base["k_vals"]),
        "sigma_base": sigma_base,
        "sigma_router": sigma_router,
        "sigma_disc": _normalize_series(analysis_base["sigma_disc"]),
        "sigma_cont": _normalize_series(analysis_base["sigma_cont"]),
        "sigma_delta": diff,
        "metrics": {
            "med_rel_err_base": float(analysis_base["med_rel_err"]),
            "med_rel_err_router": float(analysis_router["med_rel_err"]),
            "r2_base": float(analysis_base["r2_array"]),
            "r2_router": float(analysis_router["r2_array"]),
            "max_delta_sigma": float(np.max(np.abs(diff))) if diff.size else 0.0,
        },
    }


def render_dispersion_figure(data: Dict[str, np.ndarray], figure_path: str) -> None:
    _ensure_dir(figure_path)
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt  # type: ignore

    k = data["k"]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))

    ax1.plot(k, data["sigma_base"], "o", label="router off", color="#DD8452")
    ax1.plot(k, data["sigma_router"], "s", label="router on", color="#4C72B0", fillstyle="none")
    ax1.plot(k, data["sigma_disc"], "-", label="discrete theory", color="#55A868")
    ax1.plot(k, data["sigma_cont"], "--", label="continuum theory", color="#C44E52")
    ax1.set_xlabel("k")
    ax1.set_ylabel("σ(k)")
    ax1.legend(loc="best")
    ax1.grid(True, linestyle="--", alpha=0.4)

    ax2.plot(k, data["sigma_delta"], color="#8172B2")
    ax2.set_xlabel("k")
    ax2.set_ylabel("Δσ (router on - off)")
    ax2.grid(True, linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)


def generate_qdrift_comparison(config: QDriftConfig) -> Dict[str, np.ndarray]:
    t, W = qfum.integrate_numeric(config.r, config.u, config.W0, config.T, config.dt, solver=config.solver)
    W_ref = qfum.logistic_analytic(config.r, config.u, config.W0, t)
    Q = qfum.Q_invariant(config.r, config.u, W, t)
    Q_router = qfum.Q_invariant(config.r, config.u, W_ref, t)
    delta = Q_router - Q
    return {
        "t": t,
        "Q_router_off": Q,
        "Q_router_on": Q_router,
        "delta_Q": delta,
        "metrics": {
            "max_abs_Q_off": float(np.max(np.abs(Q - Q[0]))),
            "max_abs_Q_on": float(np.max(np.abs(Q_router - Q_router[0]))),
            "max_delta_Q": float(np.max(np.abs(delta))),
        },
    }


def render_qdrift_figure(data: Dict[str, np.ndarray], figure_path: str) -> None:
    _ensure_dir(figure_path)
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt  # type: ignore

    t = data["t"]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6))

    abs_off = np.maximum(np.abs(data["Q_router_off"] - data["Q_router_off"][0]), 1e-18)
    abs_on = np.maximum(np.abs(data["Q_router_on"] - data["Q_router_on"][0]), 1e-18)
    ax1.plot(t, abs_off, label="router off", color="#DD8452")
    ax1.plot(t, abs_on, label="router on", color="#4C72B0", linestyle="--")
    ax1.set_xlabel("t")
    ax1.set_ylabel("|Q(t)-Q(0)|")
    ax1.set_yscale("log")
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.legend(loc="best")

    ax2.plot(t, data["delta_Q"], color="#55A868")
    ax2.set_xlabel("t")
    ax2.set_ylabel("ΔQ")
    ax2.grid(True, linestyle="--", alpha=0.4)

    fig.tight_layout()
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)


def build_payload(
    front: Dict[str, np.ndarray],
    dispersion: Dict[str, np.ndarray],
    qdrift: Dict[str, np.ndarray],
    outputs: Dict[str, str],
    timestamp: str,
) -> Dict[str, object]:
    return {
        "timestamp": timestamp,
        "front_speed": {
            "metrics": front["metrics"],
        },
        "dispersion": {
            "metrics": dispersion["metrics"],
        },
        "q_drift": {
            "metrics": qdrift["metrics"],
        },
        "outputs": outputs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate router-on/off comparison figures for RD regressions and Q drift."
    )
    parser.add_argument("--outdir", type=str, default=None, help="Base output directory (default: fum_rt/physics/outputs)")
    parser.add_argument("--log", type=str, default=None, help="Optional JSON log path override")
    parser.add_argument(
        "--figure-prefix",
        type=str,
        default=None,
        help="Optional prefix for figure filenames (three figures will be generated)",
    )
    args = parser.parse_args()

    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures")
    log_dir = os.path.join(base_outdir, "logs")
    tstamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    prefix = args.figure_prefix if args.figure_prefix else f"router_regressions_{tstamp}"
    figure_paths = {
        "front": os.path.join(fig_dir, f"{prefix}_front_speed.png"),
        "dispersion": os.path.join(fig_dir, f"{prefix}_dispersion.png"),
        "qdrift": os.path.join(fig_dir, f"{prefix}_q_drift.png"),
    }
    log_path = args.log if args.log else os.path.join(log_dir, f"{prefix}.json")

    front_config = FrontSpeedConfig()
    dispersion_config = DispersionConfig()
    qdrift_config = QDriftConfig()

    front_data = generate_front_speed_comparison(front_config)
    dispersion_data = generate_dispersion_comparison(dispersion_config)
    qdrift_data = generate_qdrift_comparison(qdrift_config)

    render_front_speed_figure(front_data, figure_paths["front"])
    render_dispersion_figure(dispersion_data, figure_paths["dispersion"])
    render_qdrift_figure(qdrift_data, figure_paths["qdrift"])

    payload = build_payload(
        front_data,
        dispersion_data,
        qdrift_data,
        {
            "front_figure": os.path.abspath(figure_paths["front"]),
            "dispersion_figure": os.path.abspath(figure_paths["dispersion"]),
            "qdrift_figure": os.path.abspath(figure_paths["qdrift"]),
            "log": os.path.abspath(log_path),
        },
        time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )

    hashes = {
        "front_speed": hash_jsonable(front_data["metrics"]),
        "dispersion": hash_jsonable(dispersion_data["metrics"]),
        "qdrift": hash_jsonable(qdrift_data["metrics"]),
    }
    gates = {
        "front_speed_delta_below_tol": payload["front_speed"]["metrics"]["max_delta_front"] <= 1e-6,
        "dispersion_delta_below_tol": payload["dispersion"]["metrics"]["max_delta_sigma"] <= 1e-6,
        "qdrift_delta_below_tol": payload["q_drift"]["metrics"]["max_delta_Q"] <= 1e-10,
    }

    payload = enrich_payload(
        payload,
        script_name=os.path.splitext(os.path.basename(__file__))[0],
        gates=gates,
        hashes=hashes,
        seeds={"rd_seed": front_config.seed},
        outputs=payload["outputs"],
    )

    _ensure_dir(log_path)
    with open(log_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    print(json.dumps(
        {
            "log": payload["outputs"].get("log"),
            "front_figure": payload["outputs"].get("front_figure"),
            "dispersion_figure": payload["outputs"].get("dispersion_figure"),
            "qdrift_figure": payload["outputs"].get("qdrift_figure"),
            "gates": payload["gates"],
            "all_passed": payload["gate_summary"]["all_passed"],
        },
        indent=2,
    ))


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
