#!/usr/bin/env python3
"""
RD dispersion validation runner (linear regime) for fum_rt.

CHANGE REASON:
- This file mirrors the validated physics from derivation scripts to the runtime stack.
- We have PROVEN the RD linear dispersion σ(k) = r - D k^2 via reproducible scripts and derivations:
  [rd_dispersion_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py),
  [rd_validation_plan.md](Prometheus_VDM/derivation/rd_validation_plan.md),
  [CORRECTIONS.md](Prometheus_VDM/derivation/computational_proofs/CORRECTIONS.md).
- This runner provides an independent, apples-to-apples check inside fum_rt with identical metrics/output schema.
- It DOES NOT alter runtime dynamics; it is a validation wrapper only.
"""

import argparse
import json
import math
import os
import sys
import time

import numpy as np

# Ensure repository root on sys.path so we can import Prometheus_VDM.*
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# Import validated experiment utilities from derivation stack
from Prometheus_VDM.derivation.code.physics.reaction_diffusion.rd_dispersion_experiment import (  # noqa: E402
    run_linear_sim,
    analyze_dispersion,
    plot_and_save_dispersion,
)


def main():
    parser = argparse.ArgumentParser(description="fum_rt mirror: Validate RD linear dispersion σ(k) with identical metrics/schema.")
    parser.add_argument("--N", type=int, default=1024)
    parser.add_argument("--L", type=float, default=200.0)
    parser.add_argument("--D", type=float, default=1.0)
    parser.add_argument("--r", type=float, default=0.25)
    parser.add_argument("--T", type=float, default=10.0)
    parser.add_argument("--cfl", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--amp0", type=float, default=1e-6, help="Initial noise amplitude (std dev).")
    parser.add_argument("--record", type=int, default=80, help="Number of snapshots to record.")
    parser.add_argument("--m_max", type=int, default=64, help="Max mode index m to fit (clamped by N//2).")
    parser.add_argument("--fit_start", type=float, default=0.1, help="fractional start of fit window")
    parser.add_argument("--fit_end", type=float, default=0.4, help="fractional end of fit window")
    parser.add_argument("--outdir", type=str, default=None, help="base output dir; defaults to fum_rt/physics/outputs next to this script")
    parser.add_argument("--figure", type=str, default=None, help="override figure path; otherwise script_name_timestamp.png in outdir/figures")
    parser.add_argument("--log", type=str, default=None, help="override log path; otherwise script_name_timestamp.json in outdir/logs")
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
    sim = run_linear_sim(args.N, args.L, args.D, args.r, args.T, args.cfl, args.seed, amp0=args.amp0, record_slices=args.record)
    analysis = analyze_dispersion(sim, args.D, args.r, args.L, args.m_max, (args.fit_start, args.fit_end))
    elapsed = time.time() - t0

    # Produce identical figure and payload schema
    plot_and_save_dispersion(analysis, figure_path, title=f"RD dispersion (linear): D={args.D}, r={args.r}")

    # Acceptance criteria (conservative for multi-mode fit; mirrors derivation script)
    acceptance = {
        "med_rel_err_max": 0.10,
        "r2_array_min": 0.98,
    }
    med_rel_err = float(analysis["med_rel_err"])
    r2_array = float(analysis["r2_array"])
    passed = (
        (math.isfinite(med_rel_err) and med_rel_err <= acceptance["med_rel_err_max"]) and
        (math.isfinite(r2_array) and r2_array >= acceptance["r2_array_min"])
    )

    payload = {
        "theory": {
            "continuum": "sigma_c(k) = r - D k^2",
            "discrete": "sigma_d(m) = r - (4 D / dx^2) sin^2(pi m / N)"
        },
        "params": {
            "N": args.N, "L": args.L, "D": args.D, "r": args.r, "T": args.T,
            "cfl": args.cfl, "seed": args.seed, "amp0": args.amp0,
            "record": args.record, "m_max": args.m_max,
            "fit_start": args.fit_start, "fit_end": args.fit_end,
        },
        "metrics": {
            "med_rel_err": med_rel_err,
            "r2_array": r2_array,
            "acceptance": acceptance,
            "passed": passed,
        },
        "series": {
            "m_vals": analysis["m_vals"],
            "k_vals": analysis["k_vals"],
            "sigma_meas": analysis["sigma_meas"],
            "sigma_disc": analysis["sigma_disc"],
            "sigma_cont": analysis["sigma_cont"],
            "r2_meas": analysis["r2_meas"],
            "rel_err": analysis["rel_err"],
            "good_mask": analysis["good_mask"],
        },
        "outputs": {
            "figure": figure_path
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_sec": elapsed,
    }

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps({
        "figure": figure_path,
        "log": log_path,
        "med_rel_err": payload["metrics"]["med_rel_err"],
        "r2_array": payload["metrics"]["r2_array"],
        "passed": payload["metrics"]["passed"],
    }, indent=2))


if __name__ == "__main__":
    main()