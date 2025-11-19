#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch GWOSC open data via GWPy and write a CSV time series with header 't,h'.

Usage:
  python3 fetch_gwpy_to_csv.py --ifo H1 --start 1126259459.923 --end 1126259464.923 --fs 4096 \
    --out Derivation/code/physics/cosmology/black_holes/topo_rdm/testdata/gw150914_H1.csv
"""

import argparse
import csv
import json
import os
import sys

def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch GWPy open data and write CSV (t,h)")
    ap.add_argument("--ifo", required=True, help="Detector IFO, e.g. H1 or L1")
    ap.add_argument("--start", type=float, required=True, help="Start GPS time (seconds)")
    ap.add_argument("--end", type=float, required=True, help="End GPS time (seconds)")
    ap.add_argument("--fs", type=int, default=4096, help="Sample rate [Hz]")
    ap.add_argument("--out", required=True, help="Output CSV path (will create directories)")
    args = ap.parse_args()

    try:
        from gwpy.timeseries import TimeSeries as T  # lazy import so script fails fast if missing
    except Exception as e:
        print(json.dumps({"ok": False, "stage": "import_gwpy", "error": str(e)}))
        sys.exit(2)

    try:
        ts = T.fetch_open_data(str(args.ifo), float(args.start), float(args.end), sample_rate=int(args.fs))
    except Exception as e:
        print(json.dumps({
            "ok": False,
            "stage": "fetch_open_data",
            "ifo": str(args.ifo),
            "start": float(args.start),
            "end": float(args.end),
            "fs": int(args.fs),
            "error": str(e),
        }))
        sys.exit(3)

    try:
        out_dir = os.path.dirname(os.path.abspath(args.out))
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        with open(args.out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t", "h"])
            for ti, hi in zip(ts.times.value, ts.value):
                w.writerow([f"{ti:.9f}", f"{hi:.18e}"])
        print(json.dumps({
            "ok": True,
            "ifo": str(args.ifo),
            "out": os.path.abspath(args.out),
            "n_samples": int(len(ts)),
            "fs": int(args.fs),
            "start": float(args.start),
            "end": float(args.end),
        }, indent=2))
    except Exception as e:
        print(json.dumps({"ok": False, "stage": "write_csv", "out": args.out, "error": str(e)}))
        sys.exit(4)


if __name__ == "__main__":
    main()