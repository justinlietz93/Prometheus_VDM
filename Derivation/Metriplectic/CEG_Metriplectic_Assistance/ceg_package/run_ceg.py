#!/usr/bin/env python3
"""
CEG Metriplectic Instrument — one-file entry point.

Usage
-----
    # Run with default spec (N=256, dt=0.02, 12 seeds, 5 lambda values):
    python run_ceg.py

    # Run with custom spec file:
    python run_ceg.py --spec specs/default_v1c.json

    # Run with inline overrides (comma-separated seeds):
    python run_ceg.py --N 128 --dt 0.05 --seeds 1,2,3 --steps 100

Requirements:  Python 3.10+, numpy, scipy (matplotlib optional for plots)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure the package directory is importable when run directly
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from ceg_instrument import CegSpec, run_ceg  # noqa: E402


def _load_spec(path: str | None) -> dict:
    if path is None:
        default = Path(__file__).resolve().parent / "specs" / "default_v1c.json"
        if default.exists():
            return json.loads(default.read_text())
        # Built-in fallback
        return {
            "grid": {"N": 256, "dx": 1.0},
            "params": {"c": 1.0, "m": 0.5, "D": 1.0, "r": 0.1, "u": 0.0, "m_lap_operator": "spectral"},
            "dt": 0.02,
            "steps": 200,
            "seeds": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "lambdas": [0.0, 0.1, 0.2, 0.3, 0.5],
            "budget": 1e-2,
        }
    return json.loads(Path(path).read_text())


def main() -> None:
    ap = argparse.ArgumentParser(description="Run CEG Metriplectic Assisted-Echo experiment")
    ap.add_argument("--spec", type=str, default=None, help="Path to spec JSON (default: specs/default_v1c.json)")
    ap.add_argument("--N", type=int, default=None, help="Grid size override")
    ap.add_argument("--dt", type=float, default=None, help="Time step override")
    ap.add_argument("--steps", type=int, default=None, help="Number of time steps override")
    ap.add_argument("--seeds", type=str, default=None, help="Comma-separated seed list override (e.g. 1,2,3)")
    ap.add_argument("--budget", type=float, default=None, help="Energy budget override")
    ap.add_argument("--no-plot", action="store_true", help="Suppress figure output")
    args = ap.parse_args()

    raw = _load_spec(args.spec)

    # Apply inline overrides
    if args.N is not None:
        raw["grid"]["N"] = int(args.N)
    if args.dt is not None:
        raw["dt"] = float(args.dt)
    if args.steps is not None:
        raw["steps"] = int(args.steps)
    if args.seeds is not None:
        raw["seeds"] = [int(s.strip()) for s in args.seeds.split(",")]
    if args.budget is not None:
        raw["budget"] = float(args.budget)

    spec = CegSpec(
        grid=raw["grid"],
        params=raw["params"],
        dt=float(raw["dt"]),
        steps=int(raw["steps"]),
        seeds=[int(s) for s in raw["seeds"]],
        lambdas=[float(l) for l in raw["lambdas"]],
        budget=float(raw["budget"]),
        tag=raw.get("tag"),
    )

    print(f"Running CEG experiment: N={spec.grid['N']}, dt={spec.dt}, "
          f"steps={spec.steps}, seeds={spec.seeds}, lambdas={spec.lambdas}")

    results = run_ceg(spec)

    # Print summary
    print("\n=== CEG Summary ===")
    ceg_summary = results.get("ceg_summary", {})
    for lam_key in sorted(ceg_summary, key=lambda k: float(k)):
        v = ceg_summary[lam_key]
        print(f"  lambda={lam_key}: median={v['median']:.6f}  mean={v['mean']:.6f}  n={v['n']}")

    print("\n=== Gate Ledger ===")
    ledger = results.get("gate_ledger_summary", {})
    all_pass = True
    for gate_name, info in ledger.items():
        pr = info.get("pass_rate")
        meets = info.get("meets_rate", info.get("passed", 0) == 1)
        status = "PASS" if meets else "FAIL"
        if not meets:
            all_pass = False
        if pr is not None:
            print(f"  {gate_name}: {status}  ({info.get('passed', 0)}/{info.get('n', 0)} passed, rate={pr:.3f})")
        else:
            print(f"  {gate_name}: {status}")

    print(f"\nOverall: {'ALL GATES PASS ✓' if all_pass else 'SOME GATES FAILED ✗'}")

    # Optional plot
    if not args.no_plot:
        try:
            import matplotlib.pyplot as plt
            pairs = sorted(
                ((float(k), v.get("median", 0.0)) for k, v in ceg_summary.items()),
                key=lambda t: t[0],
            )
            xs = [p[0] for p in pairs]
            ys = [p[1] for p in pairs]
            plt.figure(figsize=(6, 4))
            plt.plot(xs, ys, "o-", label="median CEG")
            plt.axhline(0.05, color="red", linestyle="--", alpha=0.5, label="G5 threshold (0.05)")
            plt.xlabel("λ")
            plt.ylabel("Median CEG")
            plt.title("CEG vs λ")
            plt.legend()
            plt.tight_layout()
            out_fig = Path(__file__).resolve().parent / "ceg_result.png"
            plt.savefig(out_fig, dpi=150)
            plt.close()
            print(f"\nFigure saved: {out_fig}")
        except ImportError:
            pass

    return results


if __name__ == "__main__":
    main()
