#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np

# sys.path setup
import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import log_path, write_log
from physics.metriplectic.kg_ops import spectral_laplacian


@dataclass
class StructSpec:
    grid: Dict[str, Any]
    params: Dict[str, Any]
    draws: int = 100
    tag: str | None = None


def _slug(base: str, spec: StructSpec) -> str:
    tag = spec.params.get("tag") if isinstance(spec.params, dict) else None
    if tag is None:
        tag = getattr(spec, "tag", None)
    return f"{base}__{str(tag).strip().replace(' ', '-') if tag else base}"


def apply_J(v: np.ndarray, dx: float, c: float, m: float) -> np.ndarray:
    """Apply canonical symplectic J to (phi; pi): [[0, I], [-I, 0]] v.

    This checks skew-symmetry of J itself, independent of the Hamiltonian's K.
    """
    N2 = v.size
    if N2 % 2 != 0:
        raise ValueError("apply_J expects v to be concatenation of (phi, pi) with even length")
    N = N2 // 2
    phi = v[:N]
    pi = v[N:]
    out_phi = pi
    out_pi = -phi
    return np.concatenate([out_phi, out_pi])


def apply_M(u: np.ndarray, dx: float, D: float, lap_operator: str) -> np.ndarray:
    """Apply metric operator M on scalar field (RD). Here we test phi-channel metric only as in code."""
    # Metric acts on phi only with D*(-Δ) (spectral option)
    if lap_operator == "spectral":
        return D * (-spectral_laplacian(u, dx))
    else:
        # simple 3-point stencil periodic Laplacian
        N = u.size
        um = np.roll(u, 1)
        up = np.roll(u, -1)
        return D * ((-up + 2.0 * u - um) / (dx * dx))


def run_structure_checks(spec: StructSpec) -> Dict[str, Any]:
    N = int(spec.grid["N"]) ; dx = float(spec.grid["dx"]) ; c = float(spec.params.get("c", 1.0)) ; m = float(spec.params.get("m", 0.0))
    D = float(spec.params.get("D", 1.0)) ; lap = str(spec.params.get("m_lap_operator", "spectral"))
    g = np.random.default_rng(2025)

    # Skew test for J: <v, J v> should be ~ 0
    inner_vals = []
    for _ in range(int(spec.draws)):
        v = g.standard_normal(2 * N).astype(float)
        Jv = apply_J(v, dx, c, m)
        inner = float(np.dot(v, Jv) * dx)
        inner_vals.append(abs(inner))
    skew_median = float(np.median(inner_vals))
    skew_gate_ok = skew_median <= 1e-12

    # PSD of M on phi: <u, M u> >= 0
    neg_count = 0
    vals = []
    for _ in range(int(spec.draws)):
        u = g.standard_normal(N).astype(float)
        Mu = apply_M(u, dx, D, lap)
        quad = float(np.dot(u, Mu) * dx)
        vals.append(quad)
        if quad < -1e-12:
            neg_count += 1
    psd_ok = (neg_count == 0)

    logj = {
        "J_skew": {"median_abs_vJv": skew_median, "gate": "<=1e-12", "passed": bool(skew_gate_ok)},
        "M_psd": {"min": float(np.min(vals)), "neg_count": int(neg_count), "draws": int(spec.draws), "gate": "0 negatives", "passed": bool(psd_ok)}
    }
    failed = not (skew_gate_ok and psd_ok)
    write_log(log_path("metriplectic", _slug("metriplectic_structure_checks", spec), failed=failed), logj)
    if failed:
        write_log(log_path("metriplectic", _slug("CONTRADICTION_REPORT_structure", spec), failed=True), {
            "reason": "Structure gate failure",
            "spec": {"grid": spec.grid, "params": spec.params, "draws": int(spec.draws)},
            "metrics": logj
        })
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="Metriplectic structure sanity checks: skew(J), PSD(M)")
    p.add_argument("--spec", type=str, required=True)
    p.add_argument("--draws", type=int, default=100)
    args = p.parse_args()
    raw = json.loads(Path(args.spec).read_text())
    tag = raw.get("tag") or (raw.get("params", {}).get("tag"))
    ss = StructSpec(grid=raw["grid"], params=raw["params"], draws=int(args.draws), tag=tag)
    out = run_structure_checks(ss)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
