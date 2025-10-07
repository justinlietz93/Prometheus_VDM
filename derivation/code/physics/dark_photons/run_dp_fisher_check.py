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

from common.io_paths import log_path, write_log


@dataclass
class FisherSpec:
    # Toy likelihood: y ~ N(theta * x, sigma^2). Fisher for theta: I = (1/sigma^2) sum x_i^2
    n: int = 200
    sigma: float = 1.0
    seed: int = 7
    dx: float = 1e-3  # finite-difference step for loglike second derivative test
    rel_tol: float = 0.10  # 10%
    tag: str = "DP-fisher-v1"


def analytic_fisher(x: np.ndarray, sigma: float) -> float:
    return float(np.sum(x * x) / (sigma * sigma))


def negloglike(theta: float, x: np.ndarray, y: np.ndarray, sigma: float) -> float:
    r = y - theta * x
    return 0.5 * float(np.sum(r * r) / (sigma * sigma))


def run_fisher_check(spec: FisherSpec) -> Dict[str, Any]:
    rng = np.random.default_rng(spec.seed)
    x = rng.normal(0.0, 1.0, size=spec.n)
    theta0 = 0.3
    y = theta0 * x + rng.normal(0.0, spec.sigma, size=spec.n)

    I_analytic = analytic_fisher(x, spec.sigma)

    # Finite-difference Hessian estimate of second derivative of negloglike at MLE ~ theta_hat
    # For this linear-Gaussian model, MLE is close to least squares.
    theta_hat = float(np.sum(x * y) / np.sum(x * x))
    dx = spec.dx
    f_p = negloglike(theta_hat + dx, x, y, spec.sigma)
    f_m = negloglike(theta_hat - dx, x, y, spec.sigma)
    f_0 = negloglike(theta_hat, x, y, spec.sigma)
    # second derivative via central difference
    d2 = (f_p - 2.0 * f_0 + f_m) / (dx * dx)
    I_fd = float(d2)  # For Gaussian, Hessian equals Fisher at the MLE (expected equality)

    rel_err = abs(I_fd - I_analytic) / max(I_analytic, 1e-30)
    passed = bool(rel_err <= spec.rel_tol and np.isfinite([I_fd, I_analytic, rel_err]).all())

    # CSV table (single-row but keep extensible)
    csvp = log_path("dark_photons", f"fisher_check__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as fcsv:
        fcsv.write("I_analytic,I_fd,rel_err,theta_hat,n,sigma,dx\n")
        fcsv.write(f"{I_analytic},{I_fd},{rel_err},{theta_hat},{spec.n},{spec.sigma},{spec.dx}\n")

    logj = {
        "params": {"n": spec.n, "sigma": spec.sigma, "dx": spec.dx, "seed": spec.seed},
        "estimates": {"I_analytic": I_analytic, "I_fd": I_fd, "theta_hat": theta_hat},
        "rel_err": rel_err,
        "gate": {"rel_tol": spec.rel_tol, "passed": passed},
        "csv": str(csvp)
    }
    write_log(log_path("dark_photons", f"fisher_check__{spec.tag}", failed=not passed), logj)
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="Dark photon Fisher consistency quick check (≤10% rel err gate)")
    p.add_argument("--n", type=int, default=200)
    p.add_argument("--sigma", type=float, default=1.0)
    p.add_argument("--dx", type=float, default=1e-3)
    p.add_argument("--rel_tol", type=float, default=0.10)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--tag", type=str, default="DP-fisher-v1")
    args = p.parse_args()
    spec = FisherSpec(n=args.n, sigma=args.sigma, seed=args.seed, dx=args.dx, rel_tol=args.rel_tol, tag=args.tag)
    out = run_fisher_check(spec)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
