"""
VDM v8 Engram IO
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Provides .h5 and .npz checkpointing specifically for the v8 Connectome.
Handles phi, psi, E0, adj, debt, and walker telemetry.
"""

from __future__ import annotations

import os
import numpy as np
from typing import Tuple, List

import h5py
HAVE_H5 = True


def _adj_to_csr(adj: List[np.ndarray], N: int) -> Tuple[np.ndarray, np.ndarray]:
    """Convert neighbor-lists to CSR arrays: row_ptr, col_idx."""
    row_ptr = np.zeros(N + 1, dtype=np.int64)
    total = 0
    for i in range(N):
        deg = int(adj[i].size)
        row_ptr[i] = total
        total += deg
    row_ptr[N] = total
    col_idx = np.zeros(total, dtype=np.int32)
    pos = 0
    for i in range(N):
        nbrs = adj[i]
        if nbrs.size > 0:
            k = nbrs.size
            col_idx[pos : pos + k] = nbrs.astype(np.int32, copy=False)
            pos += k
    return row_ptr, col_idx


def _csr_to_adj(row_ptr: np.ndarray, col_idx: np.ndarray, N: int) -> List[np.ndarray]:
    """Convert CSR arrays to neighbor-lists."""
    adj = []
    for i in range(N):
        start = int(row_ptr[i])
        end = int(row_ptr[i + 1])
        if end > start:
            adj.append(col_idx[start:end].astype(np.int32, copy=False))
        else:
            adj.append(np.zeros(0, dtype=np.int32))
    return adj


def save_engram(run_dir: str, connectome, fmt: str = "h5") -> str:
    """Save v8 runtime state to an engram."""
    os.makedirs(run_dir, exist_ok=True)
    step = connectome._tick

    if fmt.lower() == "h5":
        if not HAVE_H5:
            raise RuntimeError("h5py is required but not installed.")
        path = os.path.join(run_dir, f"state_{step}.h5")
        _save_h5(path, connectome)
        return path

    path = os.path.join(run_dir, f"state_{step}.npz")
    _save_npz(path, connectome)
    return path


def _save_h5(path: str, conn):
    with h5py.File(path, "w") as f:
        # Save metadata
        f.attrs["version"] = "v8"
        f.attrs["N"] = int(conn.N)
        f.attrs["tick"] = int(conn._tick)
        f.attrs["kT"] = float(conn.kT)

        # Save node fields
        f.create_dataset("phi_curr", data=conn.phi_curr, compression="gzip")
        f.create_dataset("phi_prev", data=conn.phi_prev, compression="gzip")
        f.create_dataset("debt", data=conn.debt, compression="gzip")
        f.create_dataset("last_visit", data=conn.last_visit, compression="gzip")

        # Save CSR representation of adj, psi_curr, psi_prev
        row_ptr_adj, col_idx_adj = _adj_to_csr(conn.adj, conn.N)

        row_ptr_E0, col_idx_E0 = _adj_to_csr(conn.E0, conn.N)

        f.create_dataset("adj_row_ptr", data=row_ptr_adj, compression="gzip")
        f.create_dataset("adj_col_idx", data=col_idx_adj, compression="gzip")

        f.create_dataset("E0_row_ptr", data=row_ptr_E0, compression="gzip")
        f.create_dataset("E0_col_idx", data=col_idx_E0, compression="gzip")

        # Flatten Psi arrays mimicking CSR layout
        psi_curr_flat = np.concatenate([p for p in conn.psi_curr]) if any(p.size > 0 for p in conn.psi_curr) else np.array([], dtype=np.float32)
        psi_prev_flat = np.concatenate([p for p in conn.psi_prev]) if any(p.size > 0 for p in conn.psi_prev) else np.array([], dtype=np.float32)

        f.create_dataset("psi_curr_flat", data=psi_curr_flat, compression="gzip")
        f.create_dataset("psi_prev_flat", data=psi_prev_flat, compression="gzip")


def _save_npz(path: str, conn):
    row_ptr_adj, col_idx_adj = _adj_to_csr(conn.adj, conn.N)
    row_ptr_E0, col_idx_E0 = _adj_to_csr(conn.E0, conn.N)

    psi_curr_flat = np.concatenate([p for p in conn.psi_curr]) if any(p.size > 0 for p in conn.psi_curr) else np.array([], dtype=np.float32)
    psi_prev_flat = np.concatenate([p for p in conn.psi_prev]) if any(p.size > 0 for p in conn.psi_prev) else np.array([], dtype=np.float32)

    np.savez_compressed(
        path,
        version="v8",
        N=int(conn.N),
        tick=int(conn._tick),
        kT=float(conn.kT),
        phi_curr=conn.phi_curr,
        phi_prev=conn.phi_prev,
        debt=conn.debt,
        last_visit=conn.last_visit,
        adj_row_ptr=row_ptr_adj,
        adj_col_idx=col_idx_adj,
        E0_row_ptr=row_ptr_E0,
        E0_col_idx=col_idx_E0,
        psi_curr_flat=psi_curr_flat,
        psi_prev_flat=psi_prev_flat,
    )


def load_engram(path: str, connectome) -> None:
    """Load an engram into a v8 Connectome."""
    p = str(path)
    if p.lower().endswith(".h5"):
        if not HAVE_H5:
            raise RuntimeError("h5py not installed but .h5 requested")
        _load_h5(p, connectome)
        return
    _load_npz(p, connectome)


def _restore_psi(row_ptr: np.ndarray, psi_flat: np.ndarray, N: int) -> List[np.ndarray]:
    """Reconstruct list of psi arrays from flattened array and row_ptr."""
    psi = []
    for i in range(N):
        start = int(row_ptr[i])
        end = int(row_ptr[i + 1])
        if end > start:
            psi.append(psi_flat[start:end].astype(np.float32, copy=False))
        else:
            psi.append(np.zeros(0, dtype=np.float32))
    return psi


def _load_h5(path: str, conn):
    with h5py.File(path, "r") as f:
        version = f.attrs.get("version", "v8")
        if version != "v8":
            raise ValueError(f"v8 Connectome cannot load engrams from version {version}")

        N = int(f.attrs.get("N", conn.N))
        if N != conn.N:
            raise ValueError(f"Engram N={N} does not match Connectome N={conn.N}")

        conn._tick = int(f.attrs.get("tick", 0))
        conn.kT = float(f.attrs.get("kT", 1e-3))

        conn.phi_curr = f["phi_curr"][...]
        conn.phi_prev = f["phi_prev"][...]
        conn.debt = f["debt"][...]
        conn.last_visit = f["last_visit"][...]

        row_ptr_adj = f["adj_row_ptr"][...]
        col_idx_adj = f["adj_col_idx"][...]
        conn.adj = _csr_to_adj(row_ptr_adj, col_idx_adj, N)

        row_ptr_E0 = f["E0_row_ptr"][...]
        col_idx_E0 = f["E0_col_idx"][...]
        conn.E0 = _csr_to_adj(row_ptr_E0, col_idx_E0, N)

        psi_curr_flat = f["psi_curr_flat"][...]
        conn.psi_curr = _restore_psi(row_ptr_adj, psi_curr_flat, N)

        psi_prev_flat = f["psi_prev_flat"][...]
        conn.psi_prev = _restore_psi(row_ptr_adj, psi_prev_flat, N)


def _load_npz(path: str, conn):
    data = np.load(path, allow_pickle=False)
    version = str(data.get("version", "v8"))
    if version != "v8":
        raise ValueError(f"v8 Connectome cannot load engrams from version {version}")

    N = int(data.get("N", conn.N))
    if N != conn.N:
        raise ValueError(f"Engram N={N} does not match Connectome N={conn.N}")

    conn._tick = int(data.get("tick", 0))
    conn.kT = float(data.get("kT", 1e-3))

    conn.phi_curr = data["phi_curr"]
    conn.phi_prev = data["phi_prev"]
    conn.debt = data["debt"]
    conn.last_visit = data["last_visit"]

    row_ptr_adj = data["adj_row_ptr"]
    col_idx_adj = data["adj_col_idx"]
    conn.adj = _csr_to_adj(row_ptr_adj, col_idx_adj, N)

    row_ptr_E0 = data["E0_row_ptr"]
    col_idx_E0 = data["E0_col_idx"]
    conn.E0 = _csr_to_adj(row_ptr_E0, col_idx_E0, N)

    psi_curr_flat = data["psi_curr_flat"]
    conn.psi_curr = _restore_psi(row_ptr_adj, psi_curr_flat, N)

    psi_prev_flat = data["psi_prev_flat"]
    conn.psi_prev = _restore_psi(row_ptr_adj, psi_prev_flat, N)
