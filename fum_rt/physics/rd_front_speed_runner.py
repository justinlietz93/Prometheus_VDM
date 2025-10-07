#!/usr/bin/env python3
"""
RD front-speed validation runner (Fisher-KPP) for fum_rt.

CHANGE REASON:
- This file mirrors the validated physics from derivation scripts to the runtime stack.
- We have PROVEN the Fisher-KPP front speed c = 2√(D r) via reproducible scripts and derivations:
  [rd_front_speed_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:1),
  [rd_front_speed_validation.md](Prometheus_VDM/derivation/rd_front_speed_validation.md:1),
  [CORRECTIONS.md](Prometheus_VDM/derivation/computational_proofs/CORRECTIONS.md:1).
- This runner provides an independent, apples-to-apples check inside fum_rt with identical metrics/output schema.
- It DOES NOT alter runtime dynamics; it is a validation wrapper only.
"""

import argparse
import json
import math
import os
import sys
import time
from typing import Tuple

import numpy as np

# Ensure repository root on sys.path so we can import Prometheus_VDM.*
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# Import validated experiment utilities from derivation stack
from Prometheus_VDM.derivation.code.physics.reaction_diffusion.rd_front_speed_experiment import (  # noqa: E402
    run_sim,
    plot_and_save,
)


def main():
    parser = argparse.ArgumentParser(description="fum_rt mirror: Validate Fisher-KPP front speed c=2√(Dr) with identical metrics/schema.")
    parser.add_argument("--N", type=int, default=1024)
    parser.add_argument("--L", type=float, default=200.0)
    parser.add_argument("--D", type=float, default=1.0)
    parser.add_argument("--r", type=float, default=0.25)
    parser.add_argument("--T", type=float, default=80.0)
    parser.add_argument("--cfl", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--level", type=float, default=0.1)
    parser.add_argument("--x0", type=float, default=-60.0)
    parser.add_argument("--fit_start", type=float, default=0.6, help="fractional start of fit window")
    parser.add_argument("--fit_end", type=float, default=0.9, help="fractional end of fit window")
    parser.add_argument("--outdir", type=str, default=None, help="base output dir; defaults to fum_rt/physics/outputs next to this script")
    parser.add_argument("--figure", type=str, default=None, help="override figure path; otherwise script_name_timestamp.png in outdir/figures")
    parser.add_argument("--log", type=str, default=None, help="override log path; otherwise script_name_timestamp.json in outdir/logs")
    parser.add_argument("--noise_amp", type=float, default=0.0, help="optional gated noise amplitude (applied only left of the front)")
    args = parser.parse_args()

    # Output routing (identical structure: base/figures + base/logs, UTC timestamped filenames)
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    tstamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures")
    log_dir = os.path.join(base_outdir, "logs")
    figure_path = args.figure if args.figure else os.path.join(fig_dir, f"{script_name}_{tstamp}.png")
    log_path = args.log if args.log else os.path.join(log_dir, f"{script_name}_{tstamp}.json")
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    t0 = time.time()
    data = run_sim(
        args.N, args.L, args.D, args.r, args.T, args.cfl, args.seed,
        level=args.level,
        x0=args.x0,
        fit_frac=(args.fit_start, args.fit_end),
        noise_amp=args.noise_amp,
    )
    elapsed = time.time() - t0

    # Produce identical figure and payload schema
    plot_and_save(data, figure_path)

    c_meas = data["c_meas"]
    c_abs = data["c_abs"]
    c_th = data["c_th"]
    rel_err = data["rel_err"]
    r2 = data["r2"]

    payload = {
        "theory": "Fisher-KPP front speed c=2*sqrt(D*r)",
        "params": {
            "N": args.N, "L": args.L, "D": args.D, "r": args.r, "T": args.T,
            "cfl": args.cfl, "seed": args.seed, "level": args.level,
            "x0": args.x0, "fit_start": args.fit_start, "fit_end": args.fit_end,
            "noise_amp": args.noise_amp
        },
        "metrics": {
            "c_meas": c_meas,
            "c_abs": c_abs,
            "c_sign": (1.0 if (np.isfinite(c_meas) and c_meas >= 0) else -1.0),
            "c_th": c_th,
            "rel_err": rel_err,
            "r2": r2,
            "dx": data["dx"],
            "dt": data["dt"],
            "steps": data["steps"],
            "elapsed_sec": elapsed,
            "acceptance_rel_err": 0.05,
            "passed": (rel_err <= 0.05) and (np.isfinite(r2) and r2 >= 0.98),
            "c_meas_grad": data.get("c_meas_grad", float("nan")),
            "c_abs_grad": data.get("c_abs_grad", float("nan")),
            "rel_err_grad": data.get("rel_err_grad", float("nan")),
            "r2_grad": data.get("r2_grad", float("nan")),
        },
        "outputs": {
            "figure": figure_path
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps({
        "figure": figure_path,
        "log": log_path,
        "c_meas": c_meas,
        "c_abs": c_abs,
        "c_th": c_th,
        "rel_err": rel_err,
        "r2": r2,
        "c_meas_grad": payload["metrics"]["c_meas_grad"],
        "c_abs_grad": payload["metrics"]["c_abs_grad"],
        "rel_err_grad": payload["metrics"]["rel_err_grad"],
        "r2_grad": payload["metrics"]["r2_grad"],
        "passed": payload["metrics"]["passed"],
    }, indent=2))


if __name__ == "__main__":
    main()