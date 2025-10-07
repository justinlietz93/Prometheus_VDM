#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

import numpy as np

import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log


@dataclass
class NoiseSpec:
    f_min: float = 1.0
    f_max: float = 1e4
    npts: int = 200
    T: float = 300.0  # K
    R: float = 50.0   # Ohm (thermal)
    S_inst0: float = 1e-22  # white instrument PSD baseline (arb)
    tag: str = "DP-noise-v1"


def thermal_psd(T: float, R: float) -> float:
    # Johnson–Nyquist: 4 k_B T R (leave units abstract; PSD scale OK)
    kB = 1.380649e-23
    return 4.0 * kB * T * R


def run_noise_budget(spec: NoiseSpec) -> Dict[str, Any]:
    f = np.geomspace(spec.f_min, spec.f_max, spec.npts)
    # Simple model: instrument white floor S_inst0, plus 1/f knee S_knee*(f0/f)
    f0 = 10.0
    S_knee = spec.S_inst0 * 10.0
    S_inst = spec.S_inst0 + S_knee * (f0 / np.maximum(f, 1e-12))
    S_bg = np.full_like(S_inst, thermal_psd(spec.T, spec.R))
    S_total = S_inst + S_bg

    # Sanity checks: finite, non-negative; monotone annotations (qualitative)
    finite_all = bool(np.isfinite(S_total).all())
    nonneg_all = bool((S_total >= 0).all())
    # crude monotone-in-frequency for the 1/f component at low f (S_inst decreasing with f)
    monotone_ok = np.all(np.diff(S_inst[: max(5, spec.npts // 4)]) <= 0.0)
    passed = bool(finite_all and nonneg_all and monotone_ok)

    # Artifacts
    import matplotlib.pyplot as plt
    figp = figure_path("dark_photons", f"noise_budget__{spec.tag}", failed=not passed)
    plt.figure(figsize=(6.4, 4.2))
    plt.loglog(f, S_inst, label="S_inst")
    plt.loglog(f, S_bg, label="S_bg (thermal)")
    plt.loglog(f, S_total, label="S_total")
    # regime annotation (very rough): where S_inst == S_bg
    idx = np.argmin(np.abs(S_inst - S_bg))
    f_star = float(f[idx])
    S_star = float(S_total[idx])
    plt.axvline(f_star, color="#888", ls="--", lw=1)
    plt.text(f_star, S_star, " f* ", rotation=90, va="bottom", ha="left", fontsize=8)
    plt.xlabel("f [arb]")
    plt.ylabel("PSD [arb]")
    plt.title("Dark-photon noise budget (S_total)")
    plt.legend(loc="best", fontsize=8)
    plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()

    # CSV sidecar
    csvp = log_path("dark_photons", f"noise_budget__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as fcsv:
        fcsv.write("f,S_inst,S_bg,S_total\n")
        for fi, si, sb, st in zip(f, S_inst, S_bg, S_total):
            fcsv.write(f"{fi},{si},{sb},{st}\n")

    # JSON log
    logj = {
        "params": {
            "f_min": spec.f_min, "f_max": spec.f_max, "npts": spec.npts,
            "T": spec.T, "R": spec.R, "S_inst0": spec.S_inst0
        },
        "series": {"f": f.tolist()},
        "minmax": {
            "S_inst_min": float(np.min(S_inst)), "S_inst_max": float(np.max(S_inst)),
            "S_bg": float(S_bg[0]),
            "S_total_min": float(np.min(S_total)), "S_total_max": float(np.max(S_total))
        },
        "annotation": {"f_star": f_star},
    "sanity": {"finite_all": bool(finite_all), "nonneg_all": bool(nonneg_all), "monotone_ok": bool(monotone_ok)},
        "passed": passed,
        "figure": str(figp),
        "csv": str(csvp)
    }
    write_log(log_path("dark_photons", f"noise_budget__{spec.tag}", failed=not passed), logj)
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="Dark photon noise budget quick runner")
    p.add_argument("--f_min", type=float, default=1.0)
    p.add_argument("--f_max", type=float, default=1e4)
    p.add_argument("--npts", type=int, default=200)
    p.add_argument("--T", type=float, default=300.0)
    p.add_argument("--R", type=float, default=50.0)
    p.add_argument("--S_inst0", type=float, default=1e-22)
    p.add_argument("--tag", type=str, default="DP-noise-v1")
    args = p.parse_args()
    spec = NoiseSpec(f_min=args.f_min, f_max=args.f_max, npts=args.npts, T=args.T, R=args.R, S_inst0=args.S_inst0, tag=args.tag)
    out = run_noise_budget(spec)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
