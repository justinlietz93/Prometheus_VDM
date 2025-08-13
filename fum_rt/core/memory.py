import os
import json
import numpy as np
from typing import List, Tuple

# Optional HDF5 backend (preferred)
try:
    import h5py  # type: ignore
    HAVE_H5 = True
except Exception:
    HAVE_H5 = False

# Import ADC dataclasses for (de)serialization
try:
    from .adc import Territory as ADCTerritory, Boundary as ADCBoundary, _EWMA as _ADC_EWMA  # type: ignore
except Exception:
    ADCTerritory = None  # type: ignore
    ADCBoundary = None  # type: ignore
    _ADC_EWMA = None  # type: ignore


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


# -----------------------
# ADC (de)serialization
# -----------------------
def _ewma_to_dict(w) -> dict:
    try:
        return {
            "alpha": float(getattr(w, "alpha", 0.15)),
            "mean": float(getattr(w, "mean", 0.0)),
            "var": float(getattr(w, "var", 0.0)),
            "init": bool(getattr(w, "init", False)),
        }
    except Exception:
        return {"alpha": 0.15, "mean": 0.0, "var": 0.0, "init": False}


def _ewma_from_dict(d):
    try:
        a = float(d.get("alpha", 0.15))
        m = float(d.get("mean", 0.0))
        v = float(d.get("var", 0.0))
        ini = bool(d.get("init", False))
        if _ADC_EWMA is not None:
            return _ADC_EWMA(alpha=a, mean=m, var=v, init=ini)  # type: ignore
    except Exception:
        pass
    if _ADC_EWMA is not None:
        return _ADC_EWMA(alpha=0.15)  # type: ignore
    return None


def _adc_to_dict(adc) -> dict:
    """Serialize ADC internals into a JSON-friendly dict."""
    try:
        terr = []
        for key, t in getattr(adc, "_territories", {}).items():
            try:
                dom, cov = key
            except Exception:
                dom, cov = "", 0
            terr.append({
                "key": [str(dom), int(cov)],
                "id": int(getattr(t, "id", 0)),
                "mass": float(getattr(t, "mass", 0.0)),
                "conf": float(getattr(t, "conf", 0.0)),
                "ttl": int(getattr(t, "ttl", 0)),
                "w_stats": _ewma_to_dict(getattr(t, "w_stats", None)),
                "s_stats": _ewma_to_dict(getattr(t, "s_stats", None)),
            })
        bounds = []
        for key, b in getattr(adc, "_boundaries", {}).items():
            try:
                a, c = key
            except Exception:
                a, c = 0, 0
            bounds.append({
                "a": int(a),
                "b": int(c),
                "ttl": int(getattr(b, "ttl", 0)),
                "cut_stats": _ewma_to_dict(getattr(b, "cut_stats", None)),
                "churn": _ewma_to_dict(getattr(b, "churn", None)),
            })
        fcnt = []
        for key, cnt in getattr(adc, "_frontier_counter", {}).items():
            try:
                dom, cov = key
            except Exception:
                dom, cov = "", 0
            fcnt.append({
                "key": [str(dom), int(cov)],
                "count": int(cnt),
            })
        return {
            "id_seq": int(getattr(adc, "_id_seq", 1)),
            "territories": terr,
            "boundaries": bounds,
            "frontier_counter": fcnt,
        }
    except Exception:
        return {}


def _adc_load_from_dict(adc, state: dict) -> None:
    """Populate ADC internals from a previously serialized dict."""
    if adc is None or not isinstance(state, dict):
        return
    try:
        terr_d = {}
        max_id = 0
        for t in state.get("territories", []):
            try:
                dom, cov = t.get("key", ["", 0])
                tid = int(t.get("id", 0))
                max_id = max(max_id, tid)
                wj = t.get("w_stats", {})
                sj = t.get("s_stats", {})
                w_stats = _ewma_from_dict(wj)
                s_stats = _ewma_from_dict(sj)
                if ADCTerritory is not None:
                    terr = ADCTerritory(
                        key=(str(dom), int(cov)),
                        id=tid,
                        mass=float(t.get("mass", 0.0)),
                        conf=float(t.get("conf", 0.0)),
                        ttl=int(t.get("ttl", 0)),
                        w_stats=w_stats if w_stats is not None else (_ADC_EWMA(alpha=0.15) if _ADC_EWMA else None),  # type: ignore
                        s_stats=s_stats if s_stats is not None else (_ADC_EWMA(alpha=0.15) if _ADC_EWMA else None),  # type: ignore
                    )
                    terr_d[(str(dom), int(cov))] = terr
            except Exception:
                continue
        bnd_d = {}
        for b in state.get("boundaries", []):
            try:
                a = int(b.get("a", 0))
                c = int(b.get("b", 0))
                cut = _ewma_from_dict(b.get("cut_stats", {}))
                chrn = _ewma_from_dict(b.get("churn", {}))
                if ADCBoundary is not None:
                    bnd = ADCBoundary(
                        a=min(a, c),
                        b=max(a, c),
                        cut_stats=cut if cut is not None else (_ADC_EWMA(alpha=0.2) if _ADC_EWMA else None),  # type: ignore
                        churn=chrn if chrn is not None else (_ADC_EWMA(alpha=0.2) if _ADC_EWMA else None),  # type: ignore
                        ttl=int(b.get("ttl", 0)),
                    )
                    bnd_d[(min(a, c), max(a, c))] = bnd
            except Exception:
                continue
        fcnt = {}
        for fc in state.get("frontier_counter", []):
            try:
                dom, cov = fc.get("key", ["", 0])
                fcnt[(str(dom), int(cov))] = int(fc.get("count", 0))
            except Exception:
                continue
        setattr(adc, "_territories", terr_d)
        setattr(adc, "_boundaries", bnd_d)
        setattr(adc, "_frontier_counter", fcnt)
        try:
            id_seq = int(state.get("id_seq", max_id + 1))
        except Exception:
            id_seq = max_id + 1
        setattr(adc, "_id_seq", max(1, id_seq))
    except Exception:
        return


def save_checkpoint(run_dir: str, step: int, connectome, fmt: str = "h5", adc=None) -> str:
    """
    Save runtime state (engram) for dense or sparse backends.

    Args:
        run_dir: run directory
        step: tick index
        connectome: Connectome or SparseConnectome
        fmt: "h5" (preferred) or "npz" (compat)
        adc: Optional ADC instance to persist alongside the connectome
    """
    os.makedirs(run_dir, exist_ok=True)
    backend = "sparse" if hasattr(connectome, "adj") else "dense"

    if fmt.lower() == "h5":
        if not HAVE_H5:
            # Fallback transparently to npz if h5py isn't available
            fmt = "npz"
        else:
            path = os.path.join(run_dir, f"state_{step}.h5")
            _save_h5(path, connectome, backend, adc)
            return path

    # default/fallback npz
    path = os.path.join(run_dir, f"state_{step}.npz")
    _save_npz(path, connectome, backend, adc)
    return path


def _save_h5(path: str, connectome, backend: str, adc=None):
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

        # Optional: persist ADC in a single JSON dataset for portability
        if adc is not None:
            try:
                state_json = json.dumps(_adc_to_dict(adc))
                f.create_dataset("adc_json", data=state_json, dtype=h5py.string_dtype(encoding="utf-8"))
            except Exception:
                pass


def _save_npz(path: str, connectome, backend: str, adc=None):
    adc_json = None
    if adc is not None:
        try:
            adc_json = json.dumps(_adc_to_dict(adc))
        except Exception:
            adc_json = None

    if backend == "dense":
        if adc_json is None:
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
                adc_json=adc_json,
            )
    else:
        row_ptr, col_idx = _adj_to_csr(connectome.adj, int(connectome.N))
        if adc_json is None:
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
        else:
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
                adc_json=adc_json,
            )


def load_engram(path: str, connectome, adc=None) -> None:
    """
    Load an engram from .h5 or .npz and populate the provided connectome instance.
    If ADC state is present and 'adc' is provided, populate it as well.

    - Dense: sets W, A, E, threshold
    - Sparse: sets W, adj (neighbor lists), threshold
    - ADC (optional): territories, boundaries, counters
    """
    p = str(path)
    if p.lower().endswith(".h5"):
        if not HAVE_H5:
            raise RuntimeError("h5py not installed but .h5 requested")
        _load_h5(p, connectome, adc)
        return
    # npz fallback
    _load_npz(p, connectome, adc)


def _apply_common_attrs(meta: dict, connectome):
    # Resize N if needed (safe for our numpy arrays here)
    N = int(meta.get("N", connectome.N))
    connectome.N = N
    # threshold, lambda_omega if present
    if "threshold" in meta:
        connectome.threshold = float(meta["threshold"])
    if "lambda_omega" in meta:
        connectome.lambda_omega = float(meta["lambda_omega"])


def _load_h5(path: str, connectome, adc=None):
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

        # Load ADC if present
        if adc is not None:
            try:
                ds = f.get("adc_json", None)
                if ds is not None:
                    raw = ds[()]
                    if isinstance(raw, bytes):
                        raw = raw.decode("utf-8", errors="ignore")
                    state = json.loads(raw)
                    _adc_load_from_dict(adc, state)
            except Exception:
                pass


def _load_npz(path: str, connectome, adc=None):
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

    # Load ADC if present
    if adc is not None:
        try:
            if hasattr(data, "files") and "adc_json" in data.files:
                raw = data["adc_json"]
                # raw could be 0-d array of str/bytes
                if isinstance(raw, np.ndarray):
                    if raw.dtype.kind in ("U", "S") and raw.shape == ():
                        raw_val = raw.item()
                    else:
                        raw_val = raw.tolist()
                        if isinstance(raw_val, list) and raw_val:
                            raw_val = raw_val[0]
                else:
                    raw_val = raw
                if isinstance(raw_val, bytes):
                    raw_val = raw_val.decode("utf-8", errors="ignore")
                if isinstance(raw_val, (str,)):
                    state = json.loads(raw_val)
                    _adc_load_from_dict(adc, state)
        except Exception:
            pass
