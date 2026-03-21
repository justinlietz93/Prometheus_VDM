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

# ── Path setup ──
SCRIPT_DIR = Path(__file__).resolve().parent
PARENT_DIR = SCRIPT_DIR.parent
RUNTIME_DIR = PARENT_DIR / "runtime"

for p in [str(SCRIPT_DIR), str(PARENT_DIR), str(RUNTIME_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ── Imports ──
from vdm_runtime import (
    Connectome,
    LatticeEdge,
    build_grid_lattice_spec,
    build_ring_lattice_spec,
    get_constants,
)

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

    def __init__(self, conn: Connectome, initial_edges, run_metadata: dict | None = None):
        self.conn = conn
        self.N = conn.N
        self.run_metadata = dict(run_metadata or {})

        e0_map = [{} for _ in range(self.N)]
        for edge in initial_edges:
            if isinstance(edge, LatticeEdge):
                u, v = edge.u, edge.v
                geom_weight = edge.geom_weight
            else:
                u, v = edge
                geom_weight = 1.0
            e0_map[u][v] = geom_weight
            e0_map[v][u] = geom_weight

        self.E0 = [
            np.array(sorted(nbr_map), dtype=np.int32)
            for nbr_map in e0_map
        ]
        self.E0_geom_weight = [
            np.array([nbr_map[j] for j in sorted(nbr_map)], dtype=np.float32)
            for nbr_map in e0_map
        ]
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

    @property
    def geom_weight(self):
        return self.conn.geom_weight

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

    def _flatten_ragged(self, ragged, dtype=np.float32):
        data = []
        for row in ragged:
            data.extend(float(v) for v in row)
        return np.array(data, dtype=dtype)

    def get_adj_csr(self):
        """Current adjacency as CSR."""
        return self._build_csr(self.conn.adj)

    def get_psi_csr_data(self):
        """Bond field values aligned with adj CSR col_idx."""
        return self._flatten_ragged(self.conn.psi_curr, dtype=np.float32)

    def get_geom_csr_data(self):
        """Geometry weights aligned with adj CSR col_idx."""
        return self._flatten_ragged(self.conn.geom_weight, dtype=np.float32)

    def get_e0_csr(self):
        """Initial lattice as CSR."""
        return self._e0_csr

    def get_e0_geom_csr_data(self):
        """Initial lattice geometry weights aligned with E0 CSR."""
        return self._flatten_ragged(self.E0_geom_weight, dtype=np.float32)


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
        if adapter.run_metadata:
            meta.attrs["run_metadata"] = json.dumps(adapter.run_metadata)
            lattice_meta = adapter.run_metadata.get("lattice_metadata", {})
            for key in (
                "boundary",
                "stencil",
                "weight_rule",
                "transport_calibration",
                "transport_renormalization",
            ):
                if key in lattice_meta:
                    meta.attrs[key] = lattice_meta[key]

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
        grp.create_dataset("geom_weight_csr_data", data=adapter.get_geom_csr_data())

        # Initial lattice CSR
        e0_row, e0_col = adapter.get_e0_csr()
        grp.create_dataset("E0_csr_row_ptr", data=e0_row)
        grp.create_dataset("E0_csr_col_idx", data=e0_col)
        grp.create_dataset("E0_geom_weight_csr_data", data=adapter.get_e0_geom_csr_data())

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

def build_cubic_lattice(
    N: int,
    boundary: str = "open",
    stencil: str = "26",
    transport_calibration: str = "legacy_face_6_low_k",
):
    """
    Build a 3D cubic lattice closest to N nodes.
    Returns (actual_N, lattice_def, Lx, Ly, Lz).
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

    lattice_def = build_grid_lattice_spec(
        Lx,
        Ly,
        Lz,
        boundary=boundary,
        stencil=stencil,
        calibration=transport_calibration,
    )
    return actual_N, lattice_def, Lx, Ly, Lz


def _coord_to_index(x: int, y: int, z: int, shape, boundary: str = "periodic"):
    """Map lattice coordinates back to the flattened node index."""
    lx, ly, lz = shape
    if boundary == "periodic":
        return int((x % lx) + (y % ly) * lx + (z % lz) * lx * ly)
    if not (0 <= x < lx and 0 <= y < ly and 0 <= z < lz):
        return -1
    return int(x + y * lx + z * lx * ly)


def _sphere_indices(center, radius: int, shape, boundary: str = "periodic") -> list[int]:
    """Integer lattice ball around a 3D center."""
    lx, ly, lz = shape
    cx, cy, cz = center
    indices = []
    r2 = radius * radius
    for dz in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy + dz * dz > r2:
                    continue
                index = _coord_to_index(cx + dx, cy + dy, cz + dz, shape, boundary)
                if index >= 0:
                    indices.append(index)
    return sorted(set(indices))


# ═══════════════════════════════════════════════════════════════════════════
# Stimulus patterns
# ═══════════════════════════════════════════════════════════════════════════

def apply_stimulus(
    conn: Connectome,
    mode: str,
    tick: int,
    N: int,
    amp: float = 0.08,
    lattice_shape=None,
    boundary: str = "periodic",
):
    """
    Apply stimulus to the field.  This IS the first observation.

    Modes:
      pulse   — single bidirectional injection at t=0
      sensory — periodic injection simulating sensor input
      sweep   — wavefront moving across lattice each tick
    """
    if mode == "pulse":
        if tick != 0:
            return
        if lattice_shape and all(dim > 1 for dim in lattice_shape):
            lx, ly, lz = lattice_shape
            n_stim = max(5, N // 50)
            radius = max(1, int(round(((3.0 * n_stim) / (4.0 * np.pi)) ** (1.0 / 3.0))))
            region_a = _sphere_indices(
                (lx // 4, ly // 2, lz // 2),
                radius,
                lattice_shape,
                boundary,
            )
            region_b = _sphere_indices(
                (3 * lx // 4, ly // 2, lz // 2),
                radius,
                lattice_shape,
                boundary,
            )
        else:
            n_stim = max(5, N // 50)
            half = n_stim // 2
            center_a = N // 4
            center_b = 3 * N // 4
            region_a = [(center_a + i) % N for i in range(-half, half + 1)]
            region_b = [(center_b + i) % N for i in range(-half, half + 1)]
        conn.stimulate(region_a, np.full(len(region_a), +amp))
        conn.stimulate(region_b, np.full(len(region_b), -amp))
        return

    if mode == "sensory":
        if tick % 20 != 0:
            return
        if lattice_shape and all(dim > 1 for dim in lattice_shape):
            lx, ly, lz = lattice_shape
            centers = [
                (lx // 5, ly // 3, lz // 2),
                (4 * lx // 5, 2 * ly // 3, lz // 2),
                (lx // 2, ly // 2, lz // 5),
                (lx // 2, ly // 2, 4 * lz // 5),
            ]
            center = centers[(tick // 20) % len(centers)]
            n_stim = max(3, N // 100)
            radius = max(1, int(round(((3.0 * n_stim) / (4.0 * np.pi)) ** (1.0 / 3.0))))
            indices = _sphere_indices(center, radius, lattice_shape, boundary)
            amps = np.array(
                [amp * (1.0 if i % 2 == 0 else -1.0) for i in range(len(indices))],
                dtype=np.float64,
            )
        else:
            n_stim = max(3, N // 100)
            offset = (tick // 20 * n_stim * 7) % N
            indices = [(offset + i) % N for i in range(n_stim)]
            amps = np.array(
                [amp * (1.0 if i % 2 == 0 else -1.0) for i in range(n_stim)],
                dtype=np.float64,
            )
        conn.stimulate(indices, amps)
        return

    if mode == "sweep":
        if lattice_shape and all(dim > 1 for dim in lattice_shape):
            lx, ly, lz = lattice_shape
            x_plane = tick % lx if boundary == "periodic" else min(tick, lx - 1)
            indices = [
                _coord_to_index(x_plane, y, z, lattice_shape, boundary)
                for z in range(lz)
                for y in range(ly)
            ]
            indices = [idx for idx in indices if idx >= 0]
        else:
            n_per_tick = max(1, N // 200)
            offset = (tick * n_per_tick) % N
            indices = [(offset + i) % N for i in range(n_per_tick)]
        if not indices:
            return
        amps = np.array(
            [amp * np.sin(2.0 * np.pi * i / max(len(indices), 1)) for i in range(len(indices))],
            dtype=np.float64,
        )
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
    parser.add_argument("--boundary", type=str, default="open",
                        choices=["open", "periodic"],
                        help="Boundary condition for cubic lattices")
    parser.add_argument("--stencil", type=str, default="26",
                        choices=["6", "18", "26"],
                        help="Local cubic stencil")
    parser.add_argument("--transport-calibration", type=str,
                        default="legacy_face_6_low_k",
                        choices=["legacy_face_6_low_k", "none"],
                        help="Renormalization used to preserve low-k transport")
    parser.add_argument("--log-every", type=int, default=1,
                        help="Log every N ticks")
    parser.add_argument("--out-dir", type=str, default=None,
                        help="Output directory (auto-generated if None)")
    args = parser.parse_args()

    # ── Build lattice ──
    if args.lattice == "cubic":
        N, lattice_def, Lx, Ly, Lz = build_cubic_lattice(
            args.N,
            boundary=args.boundary,
            stencil=args.stencil,
            transport_calibration=args.transport_calibration,
        )
        edges = lattice_def.edges
        lattice_meta = dict(lattice_def.metadata)
        lattice_desc = f"{Lx}×{Ly}×{Lz} cubic (periodic)"
        lattice_desc = (
            f"{Lx}x{Ly}x{Lz} cubic "
            f"({lattice_meta['boundary']}, stencil={lattice_meta['stencil']}, "
            f"renorm={lattice_meta['transport_renormalization']:.6f})"
        )
    else:
        N = args.N
        lattice_def = build_ring_lattice_spec(N, k=3)
        edges = lattice_def.edges
        lattice_meta = dict(lattice_def.metadata)
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
    conn = Connectome(N, initial_edges=edges, lattice_metadata=lattice_meta)

    # ── Save run config ──
    run_metadata = {
        "N": N,
        "lattice": args.lattice,
        "Lx": Lx,
        "Ly": Ly,
        "Lz": Lz,
        "edges": len(edges),
        "stimulus": args.stimulus,
        "amp": args.amp,
        "ticks": args.ticks,
        "constants": get_constants(),
        "timestamp": timestamp,
        "lattice_metadata": lattice_meta,
    }
    if args.lattice == "cubic":
        run_metadata["boundary"] = lattice_meta["boundary"]
        run_metadata["stencil"] = lattice_meta["stencil"]
        run_metadata["transport_calibration"] = lattice_meta["transport_calibration"]
        run_metadata["transport_renormalization"] = lattice_meta["transport_renormalization"]
        run_metadata["weight_rule"] = lattice_meta["weight_rule"]
    if args.stimulus == "pulse":
        run_metadata["pulse_geometry"] = "compact_blob"
    with open(os.path.join(out_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(run_metadata, f, indent=2)

    # ── Setup logger ──
    h5_path = os.path.join(out_dir, "run_log.h5")
    adapter = TelemetryAdapter(conn, edges, run_metadata=run_metadata)

    if HAS_ENGRAM:
        logger = EngramLogger(h5_path, adapter, run_metadata=run_metadata)
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
        apply_stimulus(
            conn,
            args.stimulus,
            t,
            N,
            args.amp,
            lattice_shape=(Lx, Ly, Lz),
            boundary=lattice_meta.get("boundary", "periodic"),
        )

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
                "n_computed": result["n_computed"],
                "mean_degree": result["mean_degree"],
                "phi_mean": result["phi_mean"],
                "phi_var": result["phi_var"],
            }
            logger.log_tick(adapter, info)

    # ── Finalize ──
    total = time.time() - t_start
    if logger:
        if HAS_ENGRAM and hasattr(logger, "log_snapshot"):
            logger.log_snapshot(adapter)
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
    print(f"  Dashboard:  python -m scripts.dashboard \"{h5_path}\"")
    print(f"{'═' * 60}")


if __name__ == "__main__":
    main()
