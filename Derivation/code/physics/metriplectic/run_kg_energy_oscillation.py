#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Any
import numpy as np
import sys
import hashlib
import os

# Path setup
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path_by_tag, log_path_by_tag, write_log, build_slug
from common.authorization.approval import check_tag_approval
from common.plotting.core import apply_style, get_fig_ax, save_figure
from common.data.results_db import (
    begin_run,
    add_artifacts,
    log_metrics,
    end_run_success,
    end_run_failed,
)
from physics.metriplectic.kg_ops import kg_energy, kg_verlet_step


@dataclass
class Spec:
    N: int
    dx: float
    c: float
    m: float
    seed_scale: float
    bands: List[Tuple[int, int]]
    seeds_per_band: int
    checkpoints: List[int]
    tag: str
    steps: int
    dt_strategy: str
    dt_ladder_count: int


def _env_audit() -> Dict[str, Any]:
    import numpy
    return {
        "python": sys.version,
        "numpy": numpy.__version__,
        "threads": {
            "OMP_NUM_THREADS": os.getenv("OMP_NUM_THREADS"),
            "MKL_NUM_THREADS": os.getenv("MKL_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.getenv("OPENBLAS_NUM_THREADS"),
        },
        "fft": {"plan": os.getenv("VDM_FFT_PLAN", "deterministic")},
    }


def _lambda_k_spectral(N: int, dx: float) -> np.ndarray:
    # Eigenvalues of -\Delta for spectral derivative: lambda_k = (2πk/L)^2 with L = N*dx
    L = N * dx
    k_idx = np.fft.fftfreq(N, d=dx) * L  # integer-like k
    om = 2.0 * np.pi * k_idx / L
    return (om * om)


def _omega_max(N: int, dx: float, c: float, m: float) -> float:
    lam = _lambda_k_spectral(N, dx)
    return float(np.sqrt(m * m + (c * c) * np.max(lam)))


def _dt_ladder(spec: Spec) -> List[float]:
    if spec.dt_strategy == "discrete_omega_max_geometric":
        wmax = _omega_max(spec.N, spec.dx, spec.c, spec.m)
        dt_max = 0.8 / max(wmax, 1e-30)
        return [dt_max / (2 ** j) for j in range(spec.dt_ladder_count)]
    raise ValueError(f"Unknown dt strategy: {spec.dt_strategy}")


def _band_limited_init(N: int, L: float, band: Tuple[int, int], seed: int, scale: float) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, L, N, endpoint=False)
    phi = np.zeros(N, dtype=float)
    for m in range(band[0], band[1] + 1):
        phase = rng.uniform(0.0, 2.0 * np.pi)
        phi += np.sin((2.0 * np.pi * m / L) * x + phase)
    phi *= (scale / max(np.max(np.abs(phi)), 1e-12))
    pi = np.zeros_like(phi)
    return phi, pi


def _hash_raw(arr: np.ndarray) -> str:
    return hashlib.sha256(memoryview(np.ascontiguousarray(arr)).tobytes()).hexdigest()


def run(spec: Spec, approved: bool, engineering_only: bool, proposal: str | None) -> Dict[str, Any]:
    L = spec.N * spec.dx
    dt_list = _dt_ladder(spec)
    AH_all: List[float] = []
    rel_AH_all: List[float] = []
    e_rev_max: float = 0.0
    
    # Determinism posture is caller-controlled via env; we record audit
    env_audit = _env_audit()

    # For each dt: run seeds across bands, compute energy amplitude, aggregate median
    for dt in dt_list:
        amps: List[float] = []
        rel_amps: List[float] = []
        for (lo, hi) in spec.bands:
            for s in range(spec.seeds_per_band):
                seed = (lo * 10_000 + hi * 100 + s)
                phi0, pi0 = _band_limited_init(spec.N, L, (lo, hi), seed, spec.seed_scale)
                # Forward evolve over steps, collect energies, hash checkpoints
                phi, pi = phi0.copy(), pi0.copy()
                H_series = np.empty(spec.steps + 1, dtype=float)
                H_series[0] = kg_energy(phi, pi, spec.dx, spec.c, spec.m)
                hashes: List[str] = []
                cpi = 0
                for n in range(1, spec.steps + 1):
                    phi, pi = kg_verlet_step(phi, pi, dt, spec.dx, spec.c, spec.m)
                    H_series[n] = kg_energy(phi, pi, spec.dx, spec.c, spec.m)
                    if n in spec.checkpoints:
                        # Hash raw buffers concatenated deterministic order
                        hashes.append(_hash_raw(phi) + ":" + _hash_raw(pi))
                        cpi += 1
                # Reverse time
                for n in range(spec.steps, 0, -1):
                    phi, pi = kg_verlet_step(phi, pi, -dt, spec.dx, spec.c, spec.m)
                e_rev = max(float(np.max(np.abs(phi - phi0))), float(np.max(np.abs(pi - pi0))))
                if e_rev > e_rev_max:
                    e_rev_max = e_rev
                # Energy amplitude and relative
                AH = 0.5 * (float(np.max(H_series)) - float(np.min(H_series)))
                rel = AH / max(float(np.mean(H_series)), 1e-30)
                amps.append(AH)
                rel_amps.append(rel)
        # Aggregate medians across seeds/bands
        AH_all.append(float(np.median(np.array(amps))))
        rel_AH_all.append(float(np.median(np.array(rel_amps))))

    # Fit log–log AH vs dt
    x = np.log(np.array(dt_list))
    y = np.log(np.array(AH_all))
    p, b = np.polyfit(x, y, 1)
    y_pred = p * x + b
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    R2 = 1.0 - (ss_res / ss_tot if ss_tot > 0 else 0.0)

    quarantine = engineering_only or (not approved)
    # Plotting via common.plotting.core
    apply_style("light")
    fig, ax = get_fig_ax(size=(6.2, 4.2))
    xs = np.linspace(float(np.min(x)), float(np.max(x)), 200)
    ax.plot(x, y, "o", label="data")
    ax.plot(xs, p * xs + b, "-", label=f"fit p={p:.4f}, R^2={R2:.6f}")
    ax.set_xlabel(r"$\log(\Delta t)$"); ax.set_ylabel(r"$\log(A_H)$"); ax.set_title("KG Energy Oscillation Scaling")
    ax.legend(loc="best", fontsize=8)
    slug = build_slug("kg_energy_osc_fit", spec.tag)
    figp = save_figure("metriplectic", slug, fig, failed=quarantine)
    # Store plot metadata under logs/ (not next to figures)
    plot_meta = {"plot": {"kind": "loglog", "x": "log(dt)", "y": "log(A_H)"}, "stats": {"p": float(p), "R2": float(R2)}}
    plot_meta_path = log_path_by_tag("metriplectic", "kg_energy_osc_fit_plotmeta", spec.tag, failed=quarantine, type="json")
    write_log(plot_meta_path, plot_meta)

    csvp = log_path_by_tag("metriplectic", "kg_energy_osc_fit", spec.tag, failed=quarantine, type="csv")
    with csvp.open("w", encoding="utf-8") as fcsv:
        fcsv.write("dt,AH,rel_AH\n")
        for dt, ah, rah in zip(dt_list, AH_all, rel_AH_all):
            fcsv.write(f"{dt},{ah},{rah}\n")

    # Gate checks
    rel_min_dt = float(rel_AH_all[-1]) if len(rel_AH_all) > 0 else float("inf")
    passed = bool((1.95 <= p <= 2.05) and (R2 >= 0.999) and (rel_min_dt <= 1e-4))

    logj = {
        "tag": spec.tag,
        "grid": {"N": spec.N, "dx": spec.dx},
        "params": {"c": spec.c, "m": spec.m, "seed_scale": spec.seed_scale, "bands": spec.bands, "seeds_per_band": spec.seeds_per_band},
        "dt_list": dt_list,
        "AH": AH_all,
        "rel_AH": rel_AH_all,
        "fit": {"p": float(p), "R2": float(R2)},
        "e_rev": float(e_rev_max),
        "checkpoints": spec.checkpoints,
        "env_audit": env_audit,
        "figure": str(figp),
        "csv": str(csvp),
        "gate": {"p_range": [1.95, 2.05], "R2_min": 0.999, "rel_AH_min_dt": 1e-4},
        "passed": bool(passed)
    }
    write_log(log_path_by_tag("metriplectic", "kg_energy_osc_fit", spec.tag, failed=quarantine), logj)

    # Results DB lifecycle
    try:
        handle = begin_run(
            domain="metriplectic",
            experiment=str(Path(__file__).resolve()),
            tag=spec.tag,
            params={
                "N": spec.N, "dx": spec.dx, "c": spec.c, "m": spec.m,
                "seed_scale": spec.seed_scale, "bands": spec.bands,
                "seeds_per_band": spec.seeds_per_band, "steps": spec.steps,
                "dt_strategy": spec.dt_strategy, "dt_ladder_count": spec.dt_ladder_count,
            },
            engineering_only=bool(quarantine),
        )
        add_artifacts(handle, {"figure": str(figp), "csv": str(csvp)})
        log_metrics(handle, {
            "p": float(p), "R2": float(R2), "e_rev_max": float(e_rev_max),
            "rel_AH_min_dt": float(rel_min_dt), "passed": bool(passed)
        })
        if passed:
            end_run_success(handle)
        else:
            end_run_failed(handle, metrics={"passed": False})
    except Exception as _e:
        # Non-fatal: preserve artifacts/log even if DB write fails
        _ = _e
    return logj


def main():
    import argparse
    p = argparse.ArgumentParser(description="KG J-only energy oscillation amplitude scaling and time-reversal QC")
    p.add_argument("--spec", type=str, default=str(Path(__file__).with_name("specs") / "kg_energy_osc.v1.json"))
    p.add_argument("--allow-unapproved", action="store_true")
    args = p.parse_args()

    # Approval check
    approved, engineering_only, proposal = check_tag_approval("metriplectic", "KG-energy-osc-v1", args.allow_unapproved, CODE_ROOT)

    with open(args.spec, "r", encoding="utf-8") as fs:
        s = json.load(fs)
    spec = Spec(
        N=int(s["grid"]["N"]), dx=float(s["grid"]["dx"]),
        c=float(s["params"]["c"]), m=float(s["params"]["m"]), seed_scale=float(s["params"]["seed_scale"]),
        bands=[tuple(b) for b in s["params"]["bands"]], seeds_per_band=int(s["params"]["seeds_per_band"]),
        checkpoints=list(s["params"]["checkpoints"]), tag=str(s["params"]["tag"]),
        steps=int(s["steps"]), dt_strategy=str(s["dt_strategy"]), dt_ladder_count=int(s["dt_ladder_count"]))

    out = run(spec, approved=approved, engineering_only=engineering_only, proposal=proposal)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
