"""
VDM v8 Validation Gates
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Self-test script implementing directive §12 validation gates.
Run: cd runtime && python -m vdm_rt.v8.verify
"""

from __future__ import annotations

import inspect
import sys


def _gate(name: str, passed: bool, detail: str = "") -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] Gate {name}" + (f" — {detail}" if detail else ""))
    return passed


def run_gates() -> bool:
    results = []

    # ------------------------------------------------------------------
    # Gate 1: Import
    # ------------------------------------------------------------------
    try:
        from vdm_rt.v8 import Connectome, get_constants
        results.append(_gate("1: Import", True))
    except Exception as e:
        results.append(_gate("1: Import", False, str(e)))
        print("\nCannot proceed without import. Aborting.")
        return False

    # ------------------------------------------------------------------
    # Gate 2: CF constraint consistency
    # ------------------------------------------------------------------
    c = get_constants()
    checks = [
        abs(c["D_DIFF"] - c["C_SQ"] / c["GAMMA_DAMP"]) < 1e-10,
        abs(c["TAU"] - 1.0 / c["GAMMA_DAMP"]) < 1e-10,
        abs(c["C_SQ"] - 2.0 * c["J_COUPLING"]) < 1e-10,  # a=1
    ]
    results.append(_gate("2: CF constraints", all(checks),
                         f"D={c['D_DIFF']:.6f}, C2={c['C_SQ']:.6f}, tau={c['TAU']:.6f}"))

    # ------------------------------------------------------------------
    # Gate 3: No RNG in physics path
    # ------------------------------------------------------------------
    from vdm_rt.v8 import void_equations, gauge, connectome as conn_mod
    violations = []
    for mod_name, mod in [("void_equations", void_equations),
                          ("gauge", gauge),
                          ("connectome", conn_mod)]:
        src = inspect.getsource(mod)
        for lineno, line in enumerate(src.splitlines(), 1):
            stripped = line.strip()
            if "np.random" in stripped or "random." in stripped:
                if stripped.startswith("#") or stripped.startswith('"'):
                    continue
                violations.append(f"{mod_name}:{lineno}: {stripped[:80]}")

    results.append(_gate("3: No RNG in physics",
                         len(violations) == 0,
                         f"{len(violations)} violations"))

    # ------------------------------------------------------------------
    # Gate 4: Tachyonic condensation
    # ------------------------------------------------------------------
    import numpy as np

    N = 200
    idx = np.arange(N, dtype=np.float32)
    perturbation = np.sin(2.0 * np.pi * idx / 7.0).astype(np.float32) * 1e-4

    conn = Connectome(N=N, perturbation=perturbation)
    for t in range(500):
        conn.step(t)

    phi_var = float(conn.phi_curr.var())
    results.append(_gate("4: Tachyonic condensation",
                         phi_var > 0.01,
                         f"Var(phi) = {phi_var:.4f} after 500 ticks"))

    # ------------------------------------------------------------------
    # Gate 5: Bond formation (topology emerges from dynamics)
    # ------------------------------------------------------------------
    total_bonds = sum(a.size for a in conn.adj)
    results.append(_gate("5: Bond formation",
                         total_bonds > 0,
                         f"{total_bonds} bond DOFs after 500 ticks"))

    # ------------------------------------------------------------------
    # Gate 6: kT measured from dynamics (not hardcoded)
    # ------------------------------------------------------------------
    results.append(_gate("6: kT measured",
                         conn.kT > 0,
                         f"kT = {conn.kT:.6e}"))

    # ------------------------------------------------------------------
    # Gate 7: Walker emergence
    # ------------------------------------------------------------------
    N2 = 100
    idx2 = np.arange(N2, dtype=np.float32)
    pert2 = np.sin(2.0 * np.pi * idx2 / 7.0).astype(np.float32) * 1e-4

    conn2 = Connectome(N=N2, perturbation=pert2)
    from vdm_rt.v8.gauge import emit_counts
    phi_dot_0 = conn2.phi_curr - conn2.phi_prev
    n0 = int(emit_counts(phi_dot_0, conn2.kT).sum())

    n_after = 0
    walker_tick = -1
    for t in range(200):
        info = conn2.step(t)
        n_after = info.get("n_walkers", 0)
        if n_after > 0 and walker_tick < 0:
            walker_tick = t

    results.append(_gate("7: Walker emergence",
                         n0 == 0 and walker_tick >= 0,
                         f"t=0: {n0} walkers, first at t={walker_tick}"))

    # ------------------------------------------------------------------
    # Gate 8: Decoherence
    # ------------------------------------------------------------------
    N3 = 200
    idx3 = np.arange(N3, dtype=np.float32)
    pert3 = np.sin(2.0 * np.pi * idx3 / 7.0).astype(np.float32) * 1e-4

    conn3 = Connectome(N=N3, perturbation=pert3)
    total_removed = 0
    for t in range(1000):
        info = conn3.step(t)
        total_removed += info.get("bonds_removed", 0)

    results.append(_gate("8: Decoherence",
                         total_removed > 0,
                         f"{total_removed} bonds decohered in 1000 ticks"))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    n_pass = sum(results)
    n_total = len(results)
    print(f"\n{'=' * 40}")
    print(f"  {n_pass}/{n_total} gates passed")
    print(f"{'=' * 40}")
    return n_pass == n_total

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    n_pass = sum(results)
    n_total = len(results)
    print(f"\n{'=' * 40}")
    print(f"  {n_pass}/{n_total} gates passed")
    print(f"{'=' * 40}")
    return n_pass == n_total


if __name__ == "__main__":
    print("VDM v8 Physics Core — Validation Gates")
    print("=" * 40)
    success = run_gates()
    sys.exit(0 if success else 1)
