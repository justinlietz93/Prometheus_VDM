"""
VDM v9 Engram IO.

Provides H5 checkpointing for the runtime with two-tier logging:
- summary scalars every tick
- full snapshots on a schedule
"""

from __future__ import annotations

import json
import os
from typing import List, Tuple

import h5py
import numpy as np


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
            col_idx[pos : pos + k] = adj[i].astype(np.int32, copy=False)
            pos += k
    return row_ptr, col_idx


def _csr_to_adj(row_ptr: np.ndarray, col_idx: np.ndarray, N: int) -> List[np.ndarray]:
    """Convert CSR to ragged adjacency."""

    adj = []
    for i in range(N):
        start = int(row_ptr[i])
        end = int(row_ptr[i + 1])
        if end > start:
            adj.append(col_idx[start:end].astype(np.int32, copy=False))
        else:
            adj.append(np.zeros(0, dtype=np.int32))
    return adj


def _flatten_ragged(ragged, dtype=np.float32) -> np.ndarray:
    data = []
    for row in ragged:
        data.extend(float(v) for v in row)
    return np.array(data, dtype=dtype)


def _unflatten_ragged(row_ptr: np.ndarray, flat: np.ndarray, N: int) -> List[np.ndarray]:
    rows = []
    for i in range(N):
        start = int(row_ptr[i])
        end = int(row_ptr[i + 1])
        if end > start:
            rows.append(flat[start:end].astype(np.float32, copy=False))
        else:
            rows.append(np.zeros(0, dtype=np.float32))
    return rows


def _current_adj_csr(conn) -> Tuple[np.ndarray, np.ndarray]:
    if hasattr(conn, "get_adj_csr"):
        return conn.get_adj_csr()
    return _adj_to_csr(conn.adj, conn.N)


def _current_psi_flat(conn) -> np.ndarray:
    if hasattr(conn, "get_psi_csr_data"):
        return conn.get_psi_csr_data()
    return _flatten_ragged(conn.psi_curr, dtype=np.float32)


def _current_geom_flat(conn) -> np.ndarray:
    if hasattr(conn, "get_geom_csr_data"):
        return conn.get_geom_csr_data()
    geom = getattr(conn, "geom_weight", None)
    if geom is None:
        return np.array([], dtype=np.float32)
    return _flatten_ragged(geom, dtype=np.float32)


def _initial_adj_csr(conn) -> Tuple[np.ndarray, np.ndarray]:
    if hasattr(conn, "get_e0_csr"):
        return conn.get_e0_csr()
    if hasattr(conn, "E0"):
        return _adj_to_csr(conn.E0, conn.N)
    if hasattr(conn, "adj"):
        return _adj_to_csr(conn.adj, conn.N)
    return np.zeros(conn.N + 1, dtype=np.int64), np.array([], dtype=np.int32)


def _initial_geom_flat(conn) -> np.ndarray:
    if hasattr(conn, "get_e0_geom_csr_data"):
        return conn.get_e0_geom_csr_data()
    geom = getattr(conn, "E0_geom_weight", None)
    if geom is None:
        return np.array([], dtype=np.float32)
    return _flatten_ragged(geom, dtype=np.float32)


def save_engram(run_dir: str, conn, fmt: str = "h5") -> str:
    """Save full Connectome state to a single checkpoint file."""

    os.makedirs(run_dir, exist_ok=True)
    path = os.path.join(run_dir, f"state_{conn._tick}.h5")

    with h5py.File(path, "w") as f:
        f.attrs["version"] = "v9"
        f.attrs["N"] = int(conn.N)
        f.attrs["tick"] = int(conn._tick)
        f.attrs["kT"] = float(conn.kT)
        if hasattr(conn, "lattice_metadata"):
            f.attrs["lattice_metadata"] = json.dumps(conn.lattice_metadata)

        f.create_dataset("phi_curr", data=conn.phi_curr, compression="gzip")
        f.create_dataset("phi_prev", data=conn.phi_prev, compression="gzip")
        f.create_dataset("debt", data=conn.debt, compression="gzip")
        f.create_dataset("last_visit", data=conn.last_visit, compression="gzip")

        rp, ci = _adj_to_csr(conn.adj, conn.N)
        f.create_dataset("adj_row_ptr", data=rp, compression="gzip")
        f.create_dataset("adj_col_idx", data=ci, compression="gzip")
        f.create_dataset(
            "psi_curr_flat",
            data=_flatten_ragged(conn.psi_curr, dtype=np.float32),
            compression="gzip",
        )
        f.create_dataset(
            "psi_prev_flat",
            data=_flatten_ragged(conn.psi_prev, dtype=np.float32),
            compression="gzip",
        )
        f.create_dataset(
            "geom_weight_flat",
            data=_flatten_ragged(getattr(conn, "geom_weight", []), dtype=np.float32),
            compression="gzip",
        )

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
        conn.psi_curr = _unflatten_ragged(rp, f["psi_curr_flat"][...], N)
        if "psi_prev_flat" in f:
            conn.psi_prev = _unflatten_ragged(rp, f["psi_prev_flat"][...], N)
        else:
            conn.psi_prev = [row.copy() for row in conn.psi_curr]

        if "geom_weight_flat" in f:
            conn.geom_weight = _unflatten_ragged(rp, f["geom_weight_flat"][...], N)
        else:
            conn.geom_weight = [
                np.ones_like(row, dtype=np.float32) for row in conn.psi_curr
            ]

        if "lattice_metadata" in f.attrs:
            conn.lattice_metadata = json.loads(f.attrs["lattice_metadata"])
            conn.transport_renormalization = float(
                conn.lattice_metadata.get("transport_renormalization", 1.0)
            )
            conn.dynamic_bond_geom_weight = float(
                conn.lattice_metadata.get("dynamic_bond_geom_weight", 1.0)
            )


class EngramLogger:
    """
    Two-tier H5 logger.

    Every tick: append one row to summary/.
    Every K ticks: write a full snapshot to snapshots/.
    """

    def __init__(
        self,
        path: str,
        conn,
        snapshot_every: int = 50,
        run_metadata: dict | None = None,
    ):
        self.path = path
        self.N = conn.N
        self.snapshot_every = snapshot_every
        self.f = h5py.File(path, "w")
        self.run_metadata = dict(run_metadata or getattr(conn, "run_metadata", {}) or {})

        meta = self.f.create_group("metadata")
        meta.attrs["runtime_version"] = "v9"
        meta.attrs["N"] = self.N
        meta.attrs["snapshot_every"] = snapshot_every
        if self.run_metadata:
            meta.attrs["run_metadata"] = json.dumps(self.run_metadata)
            lattice_meta = self.run_metadata.get("lattice_metadata", {})
            for key in (
                "boundary",
                "stencil",
                "weight_rule",
                "transport_calibration",
                "transport_renormalization",
            ):
                if key in lattice_meta:
                    meta.attrs[key] = lattice_meta[key]

        e0_row, e0_col = _initial_adj_csr(conn)
        self.f.create_dataset("E0_row_ptr", data=e0_row, compression="gzip")
        self.f.create_dataset("E0_col_idx", data=e0_col, compression="gzip")
        self.f.create_dataset(
            "E0_geom_weight_csr_data",
            data=_initial_geom_flat(conn),
            compression="gzip",
        )

        self.snap_grp = self.f.create_group("snapshots")
        self._sum = {
            "tick": [],
            "kT": [],
            "phi_var": [],
            "phi_mean": [],
            "n_active": [],
            "n_warm": [],
            "n_walkers_emitted": [],
            "n_condensed_bonds": [],
            "mean_degree": [],
            "max_degree": [],
            "bonds_total": [],
            "n_computed": [],
        }

    def log_tick(self, conn, info: dict):
        """Log one tick and snapshot on schedule."""

        tick = conn._tick
        row_ptr, _ = _current_adj_csr(conn)
        degrees = np.diff(row_ptr)
        psi_flat = _current_psi_flat(conn)

        self._sum["tick"].append(tick)
        self._sum["kT"].append(conn.kT)
        self._sum["phi_var"].append(info.get("phi_var", float(np.var(conn.phi_curr))))
        self._sum["phi_mean"].append(info.get("phi_mean", float(np.mean(conn.phi_curr))))
        self._sum["n_active"].append(info.get("n_active", 0))
        self._sum["n_warm"].append(info.get("n_warm", 0))
        self._sum["n_walkers_emitted"].append(info.get("n_walkers", 0))
        self._sum["n_condensed_bonds"].append(int(np.sum(psi_flat > 0.8)))
        self._sum["mean_degree"].append(float(np.mean(degrees)) if degrees.size else 0.0)
        self._sum["max_degree"].append(int(np.max(degrees)) if degrees.size else 0)
        self._sum["bonds_total"].append(int(np.sum(degrees) // 2))
        self._sum["n_computed"].append(info.get("n_computed", 0))

        if tick % self.snapshot_every == 0:
            self._write_snapshot(conn, tick)

    def log_snapshot(self, conn):
        """Force a snapshot right now."""

        self._write_snapshot(conn, conn._tick)

    def _write_snapshot(self, conn, tick: int):
        key = f"{tick:08d}"
        if key in self.snap_grp:
            return

        g = self.snap_grp.create_group(key)
        g.create_dataset("phi_curr", data=conn.phi_curr.astype(np.float32), compression="gzip")
        g.create_dataset("phi_prev", data=conn.phi_prev.astype(np.float32), compression="gzip")
        g.create_dataset("debt", data=conn.debt, compression="gzip")
        g.create_dataset("last_visit", data=conn.last_visit, compression="gzip")

        row_ptr, col_idx = _current_adj_csr(conn)
        g.create_dataset("adj_csr_row_ptr", data=row_ptr, compression="gzip")
        g.create_dataset("adj_csr_col_idx", data=col_idx, compression="gzip")
        g.create_dataset("psi_csr_data", data=_current_psi_flat(conn), compression="gzip")
        g.create_dataset(
            "geom_weight_csr_data",
            data=_current_geom_flat(conn),
            compression="gzip",
        )

    def close(self):
        """Write summary datasets and close file."""

        summary = self.f.create_group("summary")
        for key, values in self._sum.items():
            if not values:
                continue
            dtype = np.int64 if isinstance(values[0], int) else np.float64
            summary.create_dataset(key, data=np.array(values, dtype=dtype))
        self.f.close()
