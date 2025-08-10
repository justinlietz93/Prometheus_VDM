
import os
import numpy as np
from typing import List, Tuple

# Optional HDF5 backend (preferred)
try:
    import h5py  # type: ignore
    HAVE_H5 = True
except Exception:
    HAVE_H5 = False


def _adj_to_csr(adj: List[np.ndarray], N: int) -> Tuple[np.ndarray, np.ndarray]:
    """Convert neighbor-lists (sparse adjacency) to CSR arrays: row_ptr, col_idx."""
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
        if nbrs.size:
            k = nbrs.size
            col_idx[pos : pos + k] = nbrs.astype(np.int32, copy=False)
            pos += k
    return row_ptr, col_idx


def _csr_to_adj(row_ptr: np.ndarray, col_idx: np.ndarray, N: int) -> List[np.ndarray]:
    """Convert CSR arrays to neighbor-lists (sparse adjacency)."""
    adj = []
    for i in range(N):
        start = int(row_ptr[i])
        end = int(row_ptr[i + 1])
        if end > start:
            adj.append(col_idx[start:end].astype(np.int32, copy=False))
        else:
            adj.append(np.zeros(0, dtype=np.int32))
    return adj


def save_checkpoint(run_dir: str, step: int, connectome, fmt: str = "h5") -> str:
    """
    Save runtime state (engram) for dense or sparse backends.

    Args:
        run_dir: run directory
        step: tick index
        connectome: Connectome or SparseConnectome
        fmt: "h5" (preferred) or "npz" (compat)
    """
    os.makedirs(run_dir, exist_ok=True)
    backend = "sparse" if hasattr(connectome, "adj") else "dense"

    if fmt.lower() == "h5":
        if not HAVE_H5:
            # Fallback transparently to npz if h5py isn't available
            fmt = "npz"
        else:
            path = os.path.join(run_dir, f"state_{step}.h5")
            _save_h5(path, connectome, backend)
            return path

    # default/fallback npz
    path = os.path.join(run_dir, f"state_{step}.npz")
    _save_npz(path, connectome, backend)
    return path


def _save_h5(path: str, connectome, backend: str):
    with h5py.File(path, "w") as f:
        # Metadata as attributes
        f.attrs["backend"] = backend
        f.attrs["N"] = int(connectome.N)
        f.attrs["k"] = int(getattr(connectome, "k", 0))
        f.attrs["threshold"] = float(getattr(connectome, "threshold", 0.0))
        f.attrs["lambda_omega"] = float(getattr(connectome, "lambda_omega", 0.0))
        f.attrs["dtype"] = "float32"

        if backend == "dense":
            g = f.create_group("dense")
            g.create_dataset("W", data=connectome.W.astype(np.float32, copy=False), compression="gzip")
            g.create_dataset("A", data=connectome.A.astype(np.int8, copy=False), compression="gzip")
            g.create_dataset("E", data=connectome.E.astype(np.float32, copy=False), compression="gzip")
        else:
            # Sparse: store neighbor lists as CSR
            row_ptr, col_idx = _adj_to_csr(connectome.adj, int(connectome.N))
            g = f.create_group("sparse")
            g.create_dataset("W", data=connectome.W.astype(np.float32, copy=False), compression="gzip")
            g.create_dataset("row_ptr", data=row_ptr, compression="gzip")
            g.create_dataset("col_idx", data=col_idx, compression="gzip")


def _save_npz(path: str, connectome, backend: str):
    if backend == "dense":
        np.savez_compressed(
            path,
            backend="dense",
            N=int(connectome.N),
            k=int(getattr(connectome, "k", 0)),
            threshold=float(getattr(connectome, "threshold", 0.0)),
            lambda_omega=float(getattr(connectome, "lambda_omega", 0.0)),
            W=connectome.W.astype(np.float32, copy=False),
            A=connectome.A.astype(np.int8, copy=False),
            E=connectome.E.astype(np.float32, copy=False),
        )
    else:
        row_ptr, col_idx = _adj_to_csr(connectome.adj, int(connectome.N))
        np.savez_compressed(
            path,
            backend="sparse",
            N=int(connectome.N),
            k=int(getattr(connectome, "k", 0)),
            threshold=float(getattr(connectome, "threshold", 0.0)),
            lambda_omega=float(getattr(connectome, "lambda_omega", 0.0)),
            W=connectome.W.astype(np.float32, copy=False),
            row_ptr=row_ptr,
            col_idx=col_idx,
        )


def load_engram(path: str, connectome) -> None:
    """
    Load an engram from .h5 or .npz and populate the provided connectome instance.

    - Dense: sets W, A, E, threshold
    - Sparse: sets W, adj (neighbor lists), threshold
    """
    if path.lower().endswith(".h5"):
        if not HAVE_H5:
            raise RuntimeError("h5py not installed but .h5 requested")
        _load_h5(path, connectome)
        return
    # npz fallback
    _load_npz(path, connectome)


def _apply_common_attrs(meta: dict, connectome):
    # Resize N if needed (safe for our numpy arrays here)
    N = int(meta.get("N", connectome.N))
    connectome.N = N
    # threshold, lambda_omega if present
    if "threshold" in meta:
        connectome.threshold = float(meta["threshold"])
    if "lambda_omega" in meta:
        connectome.lambda_omega = float(meta["lambda_omega"])


def _load_h5(path: str, connectome):
    with h5py.File(path, "r") as f:
        backend = f.attrs.get("backend", "dense")
        meta = {
            "N": int(f.attrs.get("N", connectome.N)),
            "threshold": float(f.attrs.get("threshold", getattr(connectome, "threshold", 0.0))),
            "lambda_omega": float(f.attrs.get("lambda_omega", getattr(connectome, "lambda_omega", 0.0))),
        }
        _apply_common_attrs(meta, connectome)

        if backend == "dense":
            g = f["dense"]
            connectome.W = g["W"][...].astype(np.float32, copy=False)
            connectome.A = g["A"][...].astype(np.int8, copy=False)
            connectome.E = g["E"][...].astype(np.float32, copy=False)
        else:
            g = f["sparse"]
            connectome.W = g["W"][...].astype(np.float32, copy=False)
            row_ptr = g["row_ptr"][...]
            col_idx = g["col_idx"][...]
            connectome.adj = _csr_to_adj(row_ptr, col_idx, int(connectome.N))


def _load_npz(path: str, connectome):
    data = np.load(path, allow_pickle=False)
    backend = str(data.get("backend", "dense"))
    meta = {
        "N": int(data.get("N", connectome.N)),
        "threshold": float(data.get("threshold", getattr(connectome, "threshold", 0.0))),
        "lambda_omega": float(data.get("lambda_omega", getattr(connectome, "lambda_omega", 0.0))),
    }
    _apply_common_attrs(meta, connectome)
    if backend == "dense":
        connectome.W = data["W"].astype(np.float32, copy=False)
        connectome.A = data["A"].astype(np.int8, copy=False)
        connectome.E = data["E"].astype(np.float32, copy=False)
    else:
        connectome.W = data["W"].astype(np.float32, copy=False)
        row_ptr = data["row_ptr"]
        col_idx = data["col_idx"]
        connectome.adj = _csr_to_adj(row_ptr, col_idx, int(connectome.N))
