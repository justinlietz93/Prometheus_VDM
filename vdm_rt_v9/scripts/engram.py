"""
VDM v9 Engram IO
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Provides .h5 checkpointing for the v9 Connectome.

TWO-TIER LOGGING:
  Summary row  — 10 scalars per tick.  Always logged.  Cheap.
  Full snapshot — phi, psi, adj, debt, last_visit.  Only on schedule
                  (e.g. every 50 ticks) or on explicit request.

This keeps H5 files small even for 125k+ nodes over hundreds of ticks.
The dashboard reads summary for timeseries plots and snapshots for 3D.
"""

from __future__ import annotations

import os
import numpy as np
from typing import Tuple, List

import h5py


# ═══════════════════════════════════════════════════════════════════════════
# CSR conversion utilities
# ═══════════════════════════════════════════════════════════════════════════

def _adj_to_csr(adj: List[np.ndarray], N: int) -> Tuple[np.ndarray, np.ndarray]:
    """Convert ragged adjacency to CSR: (row_ptr, col_idx)."""
    row_ptr = np.zeros(N + 1, dtype=np.int64)
    total = 0
    for i in range(N):
        row_ptr[i] = total
        total += int(adj[i].size)
    row_ptr[N] = total
    col_idx = np.zeros(total, dtype=np.int32)
    pos = 0
    for i in range(N):
        k = adj[i].size
        if k > 0:
            col_idx[pos:pos + k] = adj[i].astype(np.int32, copy=False)
            pos += k
    return row_ptr, col_idx


def _csr_to_adj(row_ptr: np.ndarray, col_idx: np.ndarray, N: int) -> List[np.ndarray]:
    """Convert CSR to ragged adjacency."""
    adj = []
    for i in range(N):
        s, e = int(row_ptr[i]), int(row_ptr[i + 1])
        adj.append(col_idx[s:e].astype(np.int32, copy=False) if e > s
                   else np.zeros(0, dtype=np.int32))
    return adj


# ═══════════════════════════════════════════════════════════════════════════
# Single-state checkpoint (save / load)
# ═══════════════════════════════════════════════════════════════════════════

def save_engram(run_dir: str, conn, fmt: str = "h5") -> str:
    """Save full Connectome state to a single checkpoint file."""
    os.makedirs(run_dir, exist_ok=True)
    path = os.path.join(run_dir, f"state_{conn._tick}.h5")

    with h5py.File(path, "w") as f:
        f.attrs["version"] = "v9"
        f.attrs["N"] = int(conn.N)
        f.attrs["tick"] = int(conn._tick)
        f.attrs["kT"] = float(conn.kT)

        f.create_dataset("phi_curr", data=conn.phi_curr, compression="gzip")
        f.create_dataset("phi_prev", data=conn.phi_prev, compression="gzip")
        f.create_dataset("debt", data=conn.debt, compression="gzip")
        f.create_dataset("last_visit", data=conn.last_visit, compression="gzip")

        rp, ci = _adj_to_csr(conn.adj, conn.N)
        f.create_dataset("adj_row_ptr", data=rp, compression="gzip")
        f.create_dataset("adj_col_idx", data=ci, compression="gzip")

        psi_flat = (np.concatenate([p for p in conn.psi_curr])
                    if any(p.size > 0 for p in conn.psi_curr)
                    else np.array([], dtype=np.float32))
        f.create_dataset("psi_curr_flat", data=psi_flat, compression="gzip")

        psi_prev_flat = (np.concatenate([p for p in conn.psi_prev])
                         if any(p.size > 0 for p in conn.psi_prev)
                         else np.array([], dtype=np.float32))
        f.create_dataset("psi_prev_flat", data=psi_prev_flat, compression="gzip")

    return path


def load_engram(path: str, conn) -> None:
    """Load checkpoint into an existing Connectome."""
    with h5py.File(path, "r") as f:
        N = int(f.attrs.get("N", conn.N))
        if N != conn.N:
            raise ValueError(f"Engram N={N} != Connectome N={conn.N}")

        conn._tick = int(f.attrs.get("tick", 0))
        conn.kT = float(f.attrs.get("kT", 0.0))
        conn.phi_curr = f["phi_curr"][...]
        conn.phi_prev = f["phi_prev"][...]
        conn.debt = f["debt"][...]
        conn.last_visit = f["last_visit"][...]

        rp = f["adj_row_ptr"][...]
        ci = f["adj_col_idx"][...]
        conn.adj = _csr_to_adj(rp, ci, N)

        psi_flat = f["psi_curr_flat"][...]
        conn.psi_curr = []
        for i in range(N):
            s, e = int(rp[i]), int(rp[i + 1])
            conn.psi_curr.append(psi_flat[s:e].astype(np.float32)
                                 if e > s else np.zeros(0, dtype=np.float32))

        if "psi_prev_flat" in f:
            pp = f["psi_prev_flat"][...]
            conn.psi_prev = []
            for i in range(N):
                s, e = int(rp[i]), int(rp[i + 1])
                conn.psi_prev.append(pp[s:e].astype(np.float32)
                                     if e > s else np.zeros(0, dtype=np.float32))
        else:
            conn.psi_prev = [p.copy() for p in conn.psi_curr]


# ═══════════════════════════════════════════════════════════════════════════
# EngramLogger — two-tier: summary every tick, snapshots on schedule
# ═══════════════════════════════════════════════════════════════════════════

class EngramLogger:
    """
    Two-tier H5 logger.

    Every tick:     append one row to summary/ (10 scalars, ~80 bytes).
    Every K ticks:  write full snapshot to snapshots/ (phi, psi, adj).

    For 125k nodes, 300 ticks, snapshot_every=50:
      Summary:   300 rows × 80 bytes  = 24 KB
      Snapshots: 6 × ~3 MB each       = 18 MB
      Total:     ~18 MB instead of ~900 MB
    """

    def __init__(self, path: str, conn, snapshot_every: int = 50):
        self.path = path
        self.N = conn.N
        self.snapshot_every = snapshot_every
        self.f = h5py.File(path, "w")

        # Metadata
        meta = self.f.create_group("metadata")
        meta.attrs["runtime_version"] = "v9"
        meta.attrs["N"] = self.N
        meta.attrs["snapshot_every"] = snapshot_every

        # Store E0 (initial lattice) once — it never changes
        if hasattr(conn, 'E0'):
            rp, ci = _adj_to_csr(conn.E0, self.N)
        elif hasattr(conn, 'adj'):
            rp, ci = _adj_to_csr(conn.adj, self.N)
        else:
            rp = np.zeros(self.N + 1, dtype=np.int64)
            ci = np.array([], dtype=np.int32)
        self.f.create_dataset("E0_row_ptr", data=rp, compression="gzip")
        self.f.create_dataset("E0_col_idx", data=ci, compression="gzip")

        # Groups
        self.snap_grp = self.f.create_group("snapshots")

        # Summary accumulators (written to datasets at close)
        self._sum = {
            "tick": [], "kT": [], "phi_var": [], "phi_mean": [],
            "n_active": [], "n_warm": [], "n_walkers_emitted": [],
            "n_condensed_bonds": [], "mean_degree": [], "max_degree": [],
            "bonds_total": [], "n_computed": [],
        }

    def log_tick(self, conn, info: dict):
        """
        Log one tick.  Always writes summary row.
        Writes full snapshot only on schedule.
        """
        tick = conn._tick

        # ── Summary row (cheap: just scalars) ──
        total_edges = sum(a.size for a in conn.adj)
        psi_flat = np.concatenate([p for p in conn.psi_curr
                                   if p.size > 0]) if total_edges > 0 else np.array([])
        n_cond = int(np.sum(psi_flat > 0.8)) if psi_flat.size > 0 else 0
        max_deg = max((a.size for a in conn.adj), default=0)

        self._sum["tick"].append(tick)
        self._sum["kT"].append(conn.kT)
        self._sum["phi_var"].append(info.get("phi_var", float(np.var(conn.phi_curr))))
        self._sum["phi_mean"].append(info.get("phi_mean", float(np.mean(conn.phi_curr))))
        self._sum["n_active"].append(info.get("n_active", 0))
        self._sum["n_warm"].append(info.get("n_warm", 0))
        self._sum["n_walkers_emitted"].append(info.get("n_walkers", 0))
        self._sum["n_condensed_bonds"].append(n_cond)
        self._sum["mean_degree"].append(total_edges / self.N if self.N > 0 else 0.0)
        self._sum["max_degree"].append(max_deg)
        self._sum["bonds_total"].append(total_edges // 2)
        self._sum["n_computed"].append(info.get("n_computed", 0))

        # ── Full snapshot (expensive: only on schedule) ──
        if tick % self.snapshot_every == 0:
            self._write_snapshot(conn, tick)

    def log_snapshot(self, conn):
        """Force a snapshot right now (e.g. final tick)."""
        self._write_snapshot(conn, conn._tick)

    def _write_snapshot(self, conn, tick: int):
        key = f"{tick:08d}"
        if key in self.snap_grp:
            return  # already written
        g = self.snap_grp.create_group(key)
        g.create_dataset("phi_curr", data=conn.phi_curr.astype(np.float32),
                         compression="gzip")
        g.create_dataset("phi_prev", data=conn.phi_prev.astype(np.float32),
                         compression="gzip")
        g.create_dataset("debt", data=conn.debt, compression="gzip")
        g.create_dataset("last_visit", data=conn.last_visit, compression="gzip")

        rp, ci = _adj_to_csr(conn.adj, conn.N)
        g.create_dataset("adj_csr_row_ptr", data=rp, compression="gzip")
        g.create_dataset("adj_csr_col_idx", data=ci, compression="gzip")

        psi_flat = (np.concatenate([p for p in conn.psi_curr])
                    if any(p.size > 0 for p in conn.psi_curr)
                    else np.array([], dtype=np.float32))
        g.create_dataset("psi_csr_data", data=psi_flat, compression="gzip")

    def close(self):
        """Write summary datasets and close file."""
        summary = self.f.create_group("summary")
        for k, v in self._sum.items():
            if not v:
                continue
            dtype = np.int64 if isinstance(v[0], int) else np.float64
            summary.create_dataset(k, data=np.array(v, dtype=dtype))

        # Write final snapshot if not already written
        ticks = self._sum["tick"]
        if ticks and ticks[-1] % self.snapshot_every != 0:
            # Need the conn object — caller should call log_snapshot() before close
            pass

        self.f.close()
