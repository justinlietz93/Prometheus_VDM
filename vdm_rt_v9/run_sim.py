"""
VDM v9 Runner — Stimulus-Driven Metriplectic Klein-Gordon
Usage: python run_sim.py --N 1000 --ticks 200 --stimulus pulse

The system starts in superposition (φ = 0.5 everywhere, kT = 0).
Nothing moves until stimulus arrives.  Stimulus = first observation.

Stimulus modes:
  pulse    — single injection at t=0 into a cluster of nodes
  sensory  — periodic injection simulating ongoing sensor input
  sweep    — wavefront moving across the lattice

Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.
"""

import sys
import os
import time
import argparse
import json
import numpy as np
from datetime import datetime
from pathlib import Path
from scipy.sparse import csr_matrix

# ── Path setup ──
SCRIPT_DIR = Path(__file__).resolve().parent
PARENT_DIR = SCRIPT_DIR.parent
RUNTIME_DIR = PARENT_DIR / "runtime"

for p in [str(SCRIPT_DIR), str(PARENT_DIR), str(RUNTIME_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ── Imports ──
from vdm_runtime import Connectome, get_constants, build_ring_lattice, build_grid_lattice

# Try to import EngramLogger; fall back to standalone H5 logging if unavailable
try:
    from scripts.engram import EngramLogger
    HAS_ENGRAM = True
except ImportError:
    HAS_ENGRAM = False
    print("[WARN] EngramLogger not found in scripts/. Using standalone H5 logging.")

try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False
    print("[WARN] h5py not found. Logging to JSON only.")


# ═══════════════════════════════════════════════════════════════════════════
# Telemetry Adapter — bridges vdm_core.Connectome to EngramLogger
# ═══════════════════════════════════════════════════════════════════════════

class TelemetryAdapter:
    """
    Wraps the vdm_core.Connectome to expose the properties that
    EngramLogger and the 3D dashboard expect.

    The Connectome uses ragged adjacency (list of int32 arrays).
    The logger expects CSR-format adjacency and bond fields.
    This adapter does the conversion lazily and caches per-tick.
    """

    def __init__(self, conn: Connectome, initial_edges):
        self.conn = conn
        self.N = conn.N

        # Store initial lattice (E0) as ragged lists for CSR conversion
        e0_map = [[] for _ in range(self.N)]
        for u, v in initial_edges:
            e0_map[u].append(v)
            e0_map[v].append(u)
        self.E0 = [np.array(sorted(set(nbrs)), dtype=np.int32) for nbrs in e0_map]

        self._last_sync_tick = -1
        self._cached_adj_csr = None
        self._cached_psi_data = None
        self._e0_csr = self._build_csr(self.E0)

    # ── Properties expected by EngramLogger ──

    @property
    def _tick(self):
        return self.conn._tick

    @property
    def kT(self):
        return self.conn.kT

    @property
    def phi_curr(self):
        return self.conn.phi_curr.astype(np.float32)

    @property
    def phi_prev(self):
        return self.conn.phi_prev.astype(np.float32)

    @property
    def debt(self):
        return self.conn.debt

    @property
    def last_visit(self):
        return self.conn.last_visit

    @property
    def adj(self):
        """Ragged adjacency — same format as Connectome."""
        return self.conn.adj

    @property
    def psi_curr(self):
        return self.conn.psi_curr

    @property
    def psi_prev(self):
        return self.conn.psi_prev

    # ── CSR conversion for H5 logging ──

    def _build_csr(self, ragged_adj):
        """Convert ragged adjacency to CSR (row_ptr, col_idx)."""
        row_ptr = np.zeros(self.N + 1, dtype=np.int64)
        cols = []
        for i in range(self.N):
            nbrs = ragged_adj[i]
            row_ptr[i + 1] = row_ptr[i] + len(nbrs)
            cols.extend(int(j) for j in nbrs)
        col_idx = np.array(cols, dtype=np.int32)
        return row_ptr, col_idx

    def get_adj_csr(self):
        """Current adjacency as CSR."""
        return self._build_csr(self.conn.adj)

    def get_psi_csr_data(self):
        """Bond field values aligned with adj CSR col_idx."""
        data = []
        for i in range(self.N):
            data.extend(float(v) for v in self.conn.psi_curr[i])
        return np.array(data, dtype=np.float32)

    def get_e0_csr(self):
        """Initial lattice as CSR."""
        return self._e0_csr


# ═══════════════════════════════════════════════════════════════════════════
# Standalone H5 Logger (fallback when EngramLogger unavailable)
# ═══════════════════════════════════════════════════════════════════════════

class StandaloneH5Logger:
    """Minimal H5 logger matching the engram format."""

    def __init__(self, path: str, adapter: TelemetryAdapter):
        if not HAS_H5PY:
            raise RuntimeError("h5py required for H5 logging")
        self.f = h5py.File(path, "w")
        self.adapter = adapter

        # Metadata
        meta = self.f.create_group("metadata")
        meta.attrs["N"] = adapter.N
        meta.attrs["runtime_version"] = "v9"
        meta.attrs["constants"] = json.dumps(get_constants())
        meta.attrs["timestamp"] = datetime.now().isoformat()

        # Summary datasets (growable)
        self.summary = self.f.create_group("summary")
        self._summary_keys = [
            "tick", "n_walkers_emitted", "n_active", "n_warm",
            "mean_degree", "max_degree", "kT", "phi_var",
            "n_condensed_bonds", "walker_density",
        ]
        self._summary_arrays = {k: [] for k in self._summary_keys}
        self.ticks_grp = self.f.create_group("ticks")

    def log_tick(self, adapter: TelemetryAdapter, info: dict):
        tick = adapter._tick
        tick_key = f"{tick:08d}"
        grp = self.ticks_grp.create_group(tick_key)

        # Field state
        grp.create_dataset("phi_curr", data=adapter.phi_curr)
        grp.create_dataset("phi_prev", data=adapter.phi_prev)
        grp.create_dataset("debt", data=adapter.debt)
        grp.create_dataset("last_visit", data=adapter.last_visit)

        # Adjacency CSR
        row_ptr, col_idx = adapter.get_adj_csr()
        grp.create_dataset("adj_csr_row_ptr", data=row_ptr)
        grp.create_dataset("adj_csr_col_idx", data=col_idx)

        # Bond field
        grp.create_dataset("psi_csr_data", data=adapter.get_psi_csr_data())

        # Initial lattice CSR
        e0_row, e0_col = adapter.get_e0_csr()
        grp.create_dataset("E0_csr_row_ptr", data=e0_row)
        grp.create_dataset("E0_csr_col_idx", data=e0_col)

        # Summary row
        psi_data = adapter.get_psi_csr_data()
        degrees = np.diff(row_ptr)
        self._summary_arrays["tick"].append(tick)
        self._summary_arrays["n_walkers_emitted"].append(info.get("n_walkers", 0))
        self._summary_arrays["n_active"].append(info.get("n_active", 0))
        self._summary_arrays["n_warm"].append(info.get("n_warm", 0))
        self._summary_arrays["mean_degree"].append(
            float(np.mean(degrees)) if len(degrees) > 0 else 0.0)
        self._summary_arrays["max_degree"].append(
            int(np.max(degrees)) if len(degrees) > 0 else 0)
        self._summary_arrays["kT"].append(adapter.kT)
        self._summary_arrays["phi_var"].append(info.get("phi_var", 0.0))
        self._summary_arrays["n_condensed_bonds"].append(
            int(np.sum(psi_data > 0.8)))
        self._summary_arrays["walker_density"].append(
            info.get("n_walkers", 0) / adapter.N)

    def close(self):
        # Write summary arrays
        for k, v in self._summary_arrays.items():
            if v:
                dtype = np.int64 if k in ("tick", "n_walkers_emitted",
                    "n_active", "n_warm", "max_degree",
                    "n_condensed_bonds") else np.float64
                self.summary.create_dataset(k, data=np.array(v, dtype=dtype))
        self.f.close()


# ═══════════════════════════════════════════════════════════════════════════
# Lattice generators
# ═══════════════════════════════════════════════════════════════════════════

def build_cubic_lattice(N: int):
    """
    Build a 3D cubic lattice closest to N nodes.
    Returns (actual_N, edges, Lx, Ly, Lz).
    """
    L = int(round(N ** (1.0 / 3.0)))
    # Try to get close to N
    Lx, Ly, Lz = L, L, L
    actual_N = Lx * Ly * Lz

    # If too far off, adjust
    if actual_N < N:
        Lz += 1
        actual_N = Lx * Ly * Lz
    if actual_N < N:
        Ly += 1
        actual_N = Lx * Ly * Lz

    edges = build_grid_lattice(Lx, Ly, Lz, periodic=True)
    return actual_N, edges, Lx, Ly, Lz


def _coord_to_index(x: int, y: int, z: int, shape):
    """Map periodic lattice coordinates back to the flattened node index."""
    lx, ly, lz = shape
    return int((x % lx) + (y % ly) * lx + (z % lz) * lx * ly)


def _sphere_indices(center, radius: int, shape) -> list[int]:
    """Periodic integer lattice ball around a 3D center."""
    lx, ly, lz = shape
    cx, cy, cz = center
    indices = []
    r2 = radius * radius
    for dz in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy + dz * dz > r2:
                    continue
                indices.append(_coord_to_index(cx + dx, cy + dy, cz + dz, shape))
    return sorted(set(indices))


# ═══════════════════════════════════════════════════════════════════════════
# Stimulus patterns
# ═══════════════════════════════════════════════════════════════════════════

def apply_stimulus(conn: Connectome, mode: str, tick: int, N: int,
                   amp: float = 0.08, lattice_shape=None):
    """
    Apply stimulus to the field.  This IS the first observation.

    Modes:
      pulse   — single bidirectional injection at t=0
      sensory — periodic injection simulating sensor input
      sweep   — wavefront moving across lattice each tick
    """
    if mode == "pulse":
        if tick == 0:
            # Use compact periodic blobs in physical coordinates instead of
            # flattened memory-order slabs, which bias the system into planes.
            if lattice_shape and all(dim > 1 for dim in lattice_shape):
                lx, ly, lz = lattice_shape
                n_stim = max(5, N // 50)
                radius = max(1, int(round(((3.0 * n_stim) / (4.0 * np.pi)) ** (1.0 / 3.0))))
                region_a = _sphere_indices((lx // 4, ly // 2, lz // 2), radius, lattice_shape)
                region_b = _sphere_indices((3 * lx // 4, ly // 2, lz // 2), radius, lattice_shape)
            else:
                # Ring / fallback: compact local neighborhoods.
                n_stim = max(5, N // 50)
                half = n_stim // 2
                center_a = N // 4
                center_b = 3 * N // 4
                region_a = [(center_a + i) % N for i in range(-half, half + 1)]
                region_b = [(center_b + i) % N for i in range(-half, half + 1)]
            conn.stimulate(region_a, np.full(len(region_a), +amp))
            conn.stimulate(region_b, np.full(len(region_b), -amp))

    elif mode == "sensory":
        # Periodic bursts every 20 ticks, different locations
        if tick % 20 == 0:
            n_stim = max(3, N // 100)
            # Location cycles through the lattice
            offset = (tick // 20 * n_stim * 7) % N
            indices = [(offset + i) % N for i in range(n_stim)]
            # Alternating sign for bidirectional stimulus
            amps = np.array([amp * (1 if i % 2 == 0 else -1)
                            for i in range(n_stim)])
            conn.stimulate(indices, amps)

    elif mode == "sweep":
        # Wavefront: stimulate a thin slice each tick
        n_per_tick = max(1, N // 200)
        offset = (tick * n_per_tick) % N
        indices = [(offset + i) % N for i in range(n_per_tick)]
        amps = np.array([amp * np.sin(2 * np.pi * i / n_per_tick)
                        for i in range(n_per_tick)])
        conn.stimulate(indices, amps)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="VDM v9 Runner — Stimulus-Driven Metriplectic Klein-Gordon")
    parser.add_argument("--N", type=int, default=1000,
                        help="Target number of nodes (actual may differ for cubic)")
    parser.add_argument("--ticks", type=int, default=200,
                        help="Number of ticks to simulate")
    parser.add_argument("--stimulus", type=str, default="pulse",
                        choices=["pulse", "sensory", "sweep"],
                        help="Stimulus mode")
    parser.add_argument("--amp", type=float, default=0.08,
                        help="Stimulus amplitude")
    parser.add_argument("--lattice", type=str, default="cubic",
                        choices=["cubic", "ring"],
                        help="Lattice topology")
    parser.add_argument("--log-every", type=int, default=1,
                        help="Log every N ticks")
    parser.add_argument("--out-dir", type=str, default=None,
                        help="Output directory (auto-generated if None)")
    args = parser.parse_args()

    # ── Build lattice ──
    if args.lattice == "cubic":
        N, edges, Lx, Ly, Lz = build_cubic_lattice(args.N)
        lattice_desc = f"{Lx}×{Ly}×{Lz} cubic (periodic)"
    else:
        N = args.N
        edges = build_ring_lattice(N, k=3)
        Lx, Ly, Lz = N, 1, 1
        lattice_desc = f"k=3 ring"

    # ── Output directory ──
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.out_dir:
        out_dir = args.out_dir
    else:
        out_dir = str(SCRIPT_DIR / f"runs/{timestamp}_N{N}_{args.stimulus}")
    os.makedirs(out_dir, exist_ok=True)

    print("═" * 60)
    print("  VDM v9 — Stimulus-Driven Metriplectic Klein-Gordon")
    print("═" * 60)
    print(f"  Nodes:     {N}")
    print(f"  Lattice:   {lattice_desc}")
    print(f"  Edges:     {len(edges)}")
    print(f"  Stimulus:  {args.stimulus} (amp={args.amp})")
    print(f"  Ticks:     {args.ticks}")
    print(f"  Output:    {out_dir}")
    print(f"  Constants: {get_constants()}")
    print("═" * 60)

    # ── Create connectome (superposition) ──
    conn = Connectome(N, initial_edges=edges)

    # ── Save run config ──
    config = {
        "N": N, "lattice": args.lattice,
        "Lx": Lx, "Ly": Ly, "Lz": Lz,
        "edges": len(edges), "stimulus": args.stimulus,
        "amp": args.amp, "ticks": args.ticks,
        "constants": get_constants(),
        "timestamp": timestamp,
    }
    if args.stimulus == "pulse":
        config["pulse_geometry"] = "compact_blob"
    with open(os.path.join(out_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)

    # ── Setup logger ──
    h5_path = os.path.join(out_dir, "run_log.h5")
    adapter = TelemetryAdapter(conn, edges)

    if HAS_ENGRAM:
        logger = EngramLogger(h5_path, adapter)
    elif HAS_H5PY:
        logger = StandaloneH5Logger(h5_path, adapter)
    else:
        logger = None
        print("[WARN] No H5 logging available. Console output only.")

    # ── Run ──
    t_start = time.time()

    print(f"\n{'tick':>5} {'walkers':>7} {'active':>6} {'warm':>5} "
          f"{'bonds':>6} {'cond':>5} {'kT':>10} {'φ_var':>8} "
          f"{'stim':>4}  {'dt':>5}")

    for t in range(args.ticks):
        t0 = time.time()

        # Apply stimulus
        apply_stimulus(conn, args.stimulus, t, N, args.amp, lattice_shape=(Lx, Ly, Lz))

        # Physics step
        result = conn.step(t)
        dt_exec = time.time() - t0

        # Condensed bond count
        psi_data = adapter.get_psi_csr_data()
        n_condensed = int(np.sum(psi_data > 0.8))

        # Console output
        if t < 20 or t % 10 == 0 or t == args.ticks - 1:
            print(f"{t:5d} {result['n_walkers']:7d} {result['n_active']:6d} "
                  f"{result['n_warm']:5d} {result['bonds_total']:6d} "
                  f"{n_condensed:5d} {conn.kT:10.2e} "
                  f"{result['phi_var']:8.4f} "
                  f"{result['stimulus_active']:4d}  "
                  f"{dt_exec:5.3f}s")

        # Log
        if logger and (t % args.log_every == 0 or t == args.ticks - 1):
            info = {
                "n_walkers": result["n_walkers"],
                "n_active": result["n_active"],
                "n_warm": result["n_warm"],
                "mean_degree": result["mean_degree"],
                "phi_mean": result["phi_mean"],
                "phi_var": result["phi_var"],
            }
            logger.log_tick(adapter, info)

    # ── Finalize ──
    total = time.time() - t_start
    if logger:
        logger.close()

    # Final state summary
    phi = conn.phi_curr
    near0 = int(np.sum(phi < 0.1))
    near1 = int(np.sum(phi > 0.9))
    middle = N - near0 - near1

    print(f"\n{'═' * 60}")
    print(f"  Done in {total:.1f}s ({total/args.ticks:.3f}s/tick)")
    print(f"  Final state:")
    print(f"    near φ=0: {near0}   near φ=1: {near1}   middle: {middle}")
    print(f"    phi_var:  {np.var(phi):.4f}")
    print(f"    kT:       {conn.kT:.2e}")
    print(f"    bonds:    {sum(a.size for a in conn.adj) // 2}")
    print(f"  Engram:     {h5_path}")
    print(f"  Dashboard:  python -m vdm_rt.v8.dashboard '{h5_path}'")
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
