"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import argparse
import os

from fum_rt.frontend.app import build_app


def main() -> None:
    ap = argparse.ArgumentParser(description="VDM Live Dashboard launcher (compat shim).")
    ap.add_argument("--runs-root", default="runs", help="Path to runs root directory (default: ./runs)")
    ap.add_argument("--host", default="127.0.0.1", help="Dash host (default: 127.0.0.1)")
    ap.add_argument("--port", type=int, default=8060, help="Dash port (default: 8060)")
    args = ap.parse_args()

    # Preserve CLI choices in env for downstream components that may read them
    os.environ.setdefault("RUNS_ROOT", os.path.abspath(args.runs_root))
    os.environ.setdefault("DASH_HOST", args.host)
    os.environ.setdefault("DASH_PORT", str(args.port))
    os.environ.setdefault("PYTHONUNBUFFERED", "1")

    app = build_app(os.environ["RUNS_ROOT"])
    print(f"[fum_live] runs_root={os.environ['RUNS_ROOT']}")
    print(f"[fum_live] Starting Dash on http://{args.host}:{args.port}")
    # Avoid debug reloader to prevent duplicate callbacks
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
