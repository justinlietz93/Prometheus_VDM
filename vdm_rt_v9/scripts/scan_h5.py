import h5py
import numpy as np

path = "vdm_rt_v9/runs/20260413_152003_N20412_pulse/run_log.h5"

with h5py.File(path, "r") as f:
    snap = f["snapshots/00000999"]          # last snapshot (t=999)
    phi = snap["phi_curr"][:].astype(np.float64)
    positive = (phi > 0.5).sum()
    negative = (phi < 0.5).sum()
    mid = len(phi) - positive - negative
    total = len(phi)
    print(f"Final positive fraction: {positive/total:.6f} ({positive}/{total})")
    print(f"Negative fraction: {negative/total:.6f}")
    print(f"Mid fraction: {mid/total:.6f}")

    # Quick interface estimate (nodes with both positive and negative neighbors)
    adj_row = snap["adj_csr_row_ptr"][:]
    adj_col = snap["adj_csr_col_idx"][:]
    interface = 0
    for i in range(total):
        start, end = adj_row[i], adj_row[i+1]
        nbrs = adj_col[start:end]
        if len(nbrs) == 0: continue
        my_sign = phi[i] > 0.5
        has_opposite = any((phi[j] > 0.5) != my_sign for j in nbrs)
        if has_opposite:
            interface += 1
    print(f"Interface nodes (approx): {interface} ({interface/total:.4f})")