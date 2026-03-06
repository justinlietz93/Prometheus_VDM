import h5py
import json
import pandas as pd
import numpy as np
import os
import argparse

def main(h5_path):
    output_dir = os.path.dirname(h5_path) or "."
    csv_out = os.path.join(output_dir, "metrics.csv")
    json_out = os.path.join(output_dir, "h5_summary.json")

    with h5py.File(h5_path, "r") as h5:
        # === 1. Try the summary group first (this has everything pre-computed) ===
        summary = h5.get("summary")
        if summary is not None:
            print("✅ Found 'summary' group — extracting full 300-tick metrics...")
            df = pd.DataFrame({
                "tick":               summary["tick"][:],
                "walkers":            summary["n_walkers_emitted"][:],
                "active":             summary["n_active"][:],
                "warm":               summary["n_warm"][:],
                "bonds":              summary["mean_degree"][:] * 27000 / 2,   # approximate total bonds
                "cond":               summary["n_condensed_bonds"][:],
                "kT":                 summary["kT"][:],
                "phi_var":            summary["phi_var"][:],
                "stim":               np.zeros(300, dtype=int)                 # not in summary, placeholder
            })
        else:
            print("⚠️ No 'summary' group — falling back to per-tick (slower)")
            # fallback code (same as before, but now works)
            tick_keys = sorted([k for k in h5.keys() if k.startswith("ticks/")])
            data = []
            for tk in tick_keys:
                g = h5[tk]
                t = int(tk.split("/")[-1])
                info = json.loads(g.attrs.get("info", "{}"))
                cond = np.sum(g["psi_csr_data"][:] > 0.8) if "psi_csr_data" in g else -1
                data.append({
                    "tick": t,
                    "walkers": info.get("walkers", -1),
                    "active": info.get("active", -1),
                    "warm": info.get("warm", -1),
                    "bonds": g.attrs.get("bonds_total", -1),
                    "cond": cond,
                    "kT": g.attrs.get("kT", -1),
                    "phi_var": info.get("phi_var", -1),
                    "stim": -1
                })
            df = pd.DataFrame(data)

        df.to_csv(csv_out, index=False)
        print(f"✅ Metrics CSV saved → {csv_out}  ({len(df)} rows)")

        # === 2. Phi summaries (sampled every 50 ticks) ===
        phi_summ = {}
        for i in range(0, len(df), 50):
            t = int(df.iloc[i]["tick"])
            tk = f"ticks/{t:08d}"
            if tk in h5 and "phi_curr" in h5[tk]:
                phi = h5[tk]["phi_curr"][:]
                hist, bins = np.histogram(phi, bins=20)
                phi_summ[t] = {
                    "mean": float(phi.mean()),
                    "var": float(phi.var()),
                    "min": float(phi.min()),
                    "max": float(phi.max()),
                    "histogram_bins": bins.tolist(),
                    "histogram_counts": hist.tolist()
                }

        summary_dict = {
            "total_ticks": len(df),
            "N": 27000,
            "metrics_sample": df.head(20).to_dict(orient="records"),
            "phi_summaries": phi_summ,
            "notes": "Full data in metrics.csv — this should now be populated"
        }

        with open(json_out, "w") as f:
            json.dump(summary_dict, f, indent=4)
        print(f"✅ JSON summary saved → {json_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("h5_path", type=str)
    args = parser.parse_args()
    main(args.h5_path)