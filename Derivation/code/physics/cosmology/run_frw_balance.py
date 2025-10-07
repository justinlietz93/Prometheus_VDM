#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List

import numpy as np

import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log


@dataclass
class FRWSpec:
    rho: List[float]        # energy density time series (dimensionless units OK)
    a: List[float]          # scale factor time series
    t: List[float]          # time stamps (monotone)
    tol_rms: float = 1e-6
    tag: str = "FRW-balance-v1"


def continuity_residual(rho: np.ndarray, a: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Compute discrete residual for FRW continuity equation: d/dt (rho a^3) + p d/dt(a^3) = 0.

    For a single fluid with effective equation of state p = w rho, one can write:
        d/dt (rho a^3) + w rho d/dt(a^3) ≈ 0  => residual = finite-difference LHS.
    Here we adopt a default w=0 (dust) unless user supplies p(t) separately in future versions.
    """
    rho = np.asarray(rho, dtype=float)
    a = np.asarray(a, dtype=float)
    t = np.asarray(t, dtype=float)
    if rho.size < 3 or a.size != rho.size or t.size != rho.size:
        raise ValueError("rho, a, t must have same length >= 3")
    # Default: dust (w=0). Future: allow p(t) injection.
    w = 0.0
    V = a ** 3
    # Central differences for interior, one-sided ends
    dV = np.gradient(V, t)
    dQ = np.gradient(rho * V, t)
    res = dQ + w * rho * dV
    return res


def run_frw_balance(spec: FRWSpec) -> Dict[str, Any]:
    rho = np.asarray(spec.rho, dtype=float)
    a = np.asarray(spec.a, dtype=float)
    t = np.asarray(spec.t, dtype=float)
    res = continuity_residual(rho, a, t)
    rms = float(np.sqrt(np.mean(res * res)))
    passed = bool(rms <= float(spec.tol_rms))

    # Artifacts
    import matplotlib.pyplot as plt
    figp = figure_path("cosmology", f"frw_continuity_residual__{spec.tag}", failed=not passed)
    plt.figure(figsize=(6.4, 4.0))
    plt.plot(t, res, "-o", ms=3)
    plt.axhline(0.0, color="#444", lw=1)
    plt.xlabel("t")
    plt.ylabel("residual (d/dt[rho a^3] + w rho d/dt[a^3])")
    plt.title(f"FRW continuity residual (RMS ≈ {rms:.3e})")
    plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()

    csvp = log_path("cosmology", f"frw_continuity_residual__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("t,rho,a,residual\n")
        for ti, ri, ai, rsi in zip(t, rho, a, res):
            f.write(f"{ti},{ri},{ai},{rsi}\n")

    logj = {"tol_rms": float(spec.tol_rms), "rms": rms, "passed": passed, "figure": str(figp), "csv": str(csvp)}
    write_log(log_path("cosmology", f"frw_balance__{spec.tag}", failed=not passed), logj)
    if not passed:
        write_log(log_path("cosmology", f"CONTRADICTION_REPORT_frw_balance__{spec.tag}", failed=True), {
            "reason": "FRW continuity RMS residual exceeded tolerance",
            "gate": {"rms": f"<= {spec.tol_rms}"},
            "metrics": logj,
            "artifacts": {"figure": str(figp), "csv": str(csvp)}
        })
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="FRW continuity residual runner")
    p.add_argument("--series", type=str, required=False, help="JSON with keys rho,a,t and optional tol_rms")
    args = p.parse_args()
    if args.series:
        raw = json.loads(args.series)
        spec = FRWSpec(rho=raw["rho"], a=raw["a"], t=raw["t"], tol_rms=float(raw.get("tol_rms", 1e-6)))
    else:
        # Simple dust test: rho ~ a^{-3} => residual ~ 0
        t = np.linspace(0.0, 10.0, 201)
        a = (1.0 + 0.1 * t)
        rho = 1.0 / np.maximum(a ** 3, 1e-9)
        spec = FRWSpec(rho=rho.tolist(), a=a.tolist(), t=t.tolist(), tol_rms=1e-6)
    out = run_frw_balance(spec)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
