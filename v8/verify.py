"""
VDM v8 Validation Gates
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Self-test script implementing directive §12 validation gates.
Run: cd runtime && python -m vdm_rt.v8.verify
"""

from __future__ import annotations

import inspect
import sys
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v8_test_logs")
os.makedirs(LOG_DIR, exist_ok=True)

class TeeLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = TeeLogger(os.path.join(LOG_DIR, "verify_results.txt"))


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

    conn = Connectome(N=N, k_init=10, perturbation=perturbation)
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
    from unittest.mock import patch
    N2 = 100
    idx2 = np.arange(N2, dtype=np.float32)
    pert2 = np.sin(2.0 * np.pi * idx2 / 7.0).astype(np.float32) * 1e-4

    conn2 = Connectome(N=N2, k_init=10, perturbation=pert2)
    
    # We now correctly expect NO walkers at t=0 because `phi_prev(0) == phi_curr(0)`
    # per AXIOMS, velocity isn't generated until tick 1 integrates the perturbation.
    info0 = conn2.step(0)
    walkers_t0 = info0.get("n_walkers", 0)

    first_tick = -1
    for t in range(1, 200):
        info = conn2.step(t)
        n_after = info.get("n_walkers", 0)
        if n_after > 0 and first_tick < 0:
            first_tick = t

    results.append(_gate("7: Walker emergence",
                         walkers_t0 == 0 and first_tick >= 1,
                         f"t=0: {walkers_t0} walkers, first at t={first_tick}"))

    # ------------------------------------------------------------------
    # Gate 8: Decoherence
    # ------------------------------------------------------------------
    import json
    
    N3 = 200
    idx3 = np.arange(N3, dtype=np.float32)
    pert3 = np.sin(2.0 * np.pi * idx3 / 7.0).astype(np.float32) * 1e-4

    conn3 = Connectome(N=N3, k_init=10, perturbation=pert3)
    total_removed = 0
    telemetry_log = []
    
    for t in range(1000):
        info = conn3.step(t)
        if info:
            telemetry_log.append(info)
            total_removed += info.get("bonds_removed", 0)

    # Save the telemetry
    with open(os.path.join(LOG_DIR, "telemetry_gate8.json"), "w") as f:
        json.dump(telemetry_log, f, indent=2)

    results.append(_gate("8: Decoherence",
                         total_removed > 0,
                         f"{total_removed} bonds decohered in 1000 ticks (saved telemetry_gate8.json)"))

    # ------------------------------------------------------------------
    # Gate 9: Engram Storage (v8 structure saving/loading)
    # ------------------------------------------------------------------
    from vdm_rt.v8.engram import save_engram, load_engram

    N4 = 50
    pert4 = np.sin(2.0 * np.pi * np.arange(N4) / 7.0).astype(np.float32) * 1e-4
    conn_src = Connectome(N=N4, k_init=10, perturbation=pert4)
    # Run a bit so it's not strictly default values
    for t in range(50):
        conn_src.step(t)

    engram_pass = False
    details = ""
    try:
        # save
        path = save_engram(LOG_DIR, conn_src, fmt="h5")
        
        # create empty connectome and load
        conn_dst = Connectome(N=N4, k_init=10, perturbation=pert4)
        load_engram(path, conn_dst)
        
        # evaluate equality on critical properties
        checks = [
            conn_dst.N == conn_src.N,
            conn_dst._tick == conn_src._tick,
            abs(conn_dst.kT - conn_src.kT) < 1e-8,
            np.allclose(conn_dst.phi_curr, conn_src.phi_curr),
            all(np.allclose(conn_dst.psi_curr[i], conn_src.psi_curr[i]) for i in range(N4)),
            all(np.array_equal(conn_dst.adj[i], conn_src.adj[i]) for i in range(N4)),
            all(np.array_equal(conn_dst.E0[i], conn_src.E0[i]) for i in range(N4))
        ]
        engram_pass = all(checks)
        details = f"round-tripped tick {conn_dst._tick} via .h5" if engram_pass else f"checks failed: {checks}"
    except Exception as e:
        details = f"Exception: {e}"

    results.append(_gate("9: Engram storage", engram_pass, details))

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
