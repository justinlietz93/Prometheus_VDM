#!/usr/bin/env python3
"""
RD Fisher-KPP front-speed sweep runner.

Runs multiple configurations of the experiment script and writes a CSV summary
under: derivation/code/outputs/logs/rd_front_speed_sweep_YYYYMMDDThhmmssZ.csv

Usage (PowerShell, always in venv):
  & .\venv\Scripts\Activate.ps1
  python Prometheus_FUVDM/derivation/code/physics/rd_front_speed_sweep.py

Optional flags:
  --Ds 0.5 1.0 2.0
  --rs 0.1 0.25
  --Ns 1024 2048
  --levels 0.1 0.5
  --fit_start 0.6
  --fit_end 0.9
  --T 80
  --cfl 0.2
  --seed 42
  --x0 -60
  --noise_amp 0.0
"""
import argparse
import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from itertools import product


def utc_stamp():
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())


def default_out_dirs():
    here = Path(__file__).resolve()
    base = (here.parent.parent / "outputs").resolve()
    fig_dir = base / "figures"
    log_dir = base / "logs"
    fig_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    return base, fig_dir, log_dir


def run_one(python_exe, exp_path, params):
    """Run a single experiment via subprocess; return printed JSON as dict."""
    cmd = [
        python_exe,
        str(exp_path),
        "--N", str(params["N"]),
        "--L", str(params["L"]),
        "--D", str(params["D"]),
        "--r", str(params["r"]),
        "--T", str(params["T"]),
        "--cfl", str(params["cfl"]),
        "--seed", str(params["seed"]),
        "--x0", str(params["x0"]),
        "--level", str(params["level"]),
        "--fit_start", str(params["fit_start"]),
        "--fit_end", str(params["fit_end"]),
    ]
    if params.get("noise_amp", 0.0) and float(params["noise_amp"]) != 0.0:
        cmd += ["--noise_amp", str(params["noise_amp"])]

    # Let the experiment auto-route outputs; we capture printed JSON
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Experiment failed ({res.returncode}): {res.stderr.strip()}")

    # Find last JSON object in stdout
    out = res.stdout.strip()
    last_brace = out.rfind("{")
    if last_brace == -1:
        raise ValueError(f"No JSON in experiment stdout:\n{out}")
    payload = json.loads(out[last_brace:])
    return payload


def main():
    parser = argparse.ArgumentParser(description="Sweep Fisher-KPP front-speed cases and summarize results.")
    parser.add_argument("--Ds", nargs="+", type=float, default=[0.5, 1.0, 2.0])
    parser.add_argument("--rs", nargs="+", type=float, default=[0.1, 0.25])
    parser.add_argument("--Ns", nargs="+", type=int, default=[1024])
    parser.add_argument("--levels", nargs="+", type=float, default=[0.1, 0.5])
    parser.add_argument("--fit_start", type=float, default=0.6)
    parser.add_argument("--fit_end", type=float, default=0.9)
    parser.add_argument("--T", type=float, default=80.0)
    parser.add_argument("--cfl", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--x0", type=float, default=-60.0)
    parser.add_argument("--noise_amp", type=float, default=0.0)
    args = parser.parse_args()

    here = Path(__file__).resolve()
    exp_path = (here.parent / "rd_front_speed_experiment.py").resolve()
    python_exe = sys.executable

    base, _, log_dir = default_out_dirs()
    stamp = utc_stamp()
    csv_path = log_dir / f"rd_front_speed_sweep_{stamp}.csv"

    header = [
        "timestamp", "N", "L", "D", "r", "T", "cfl", "seed", "x0", "level",
        "fit_start", "fit_end", "noise_amp",
        "c_meas", "c_th", "rel_err", "r2",
        "c_meas_grad", "rel_err_grad", "r2_grad",
        "figure", "log", "passed"
    ]

    L = 200.0  # fixed domain length for this sweep
    rows = []
    for N, D, r, level in product(args.Ns, args.Ds, args.rs, args.levels):
        params = dict(
            N=N, L=L, D=D, r=r, T=args.T, cfl=args.cfl, seed=args.seed,
            x0=args.x0, level=level, fit_start=args.fit_start, fit_end=args.fit_end,
            noise_amp=args.noise_amp
        )
        payload = run_one(python_exe, exp_path, params)
        m = payload.get("metrics", {})
        rows.append([
            stamp, N, L, D, r, args.T, args.cfl, args.seed, args.x0, level,
            args.fit_start, args.fit_end, args.noise_amp,
            m.get("c_meas"), m.get("c_th"), m.get("rel_err"), m.get("r2"),
            m.get("c_meas_grad"), m.get("rel_err_grad"), m.get("r2_grad"),
            payload.get("figure"), payload.get("log"), m.get("passed"),
        ])

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

    print(json.dumps({
        "summary_csv": str(csv_path),
        "cases": len(rows),
        "base_outdir": str(base),
    }, indent=2))


if __name__ == "__main__":
    main()