#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

FUM Live Dashboard — Entry point
- Thin wrapper that delegates app construction to fum_rt.frontend.app.build_app.
- Use this script to launch the dashboard locally.

Run:
  pip install -r requirements.txt
  python fum_live.py --runs-root runs
"""
import argparse
from fum_rt.frontend.app import build_app


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--runs-root", default="runs")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8050)
    p.add_argument("--debug", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    app = build_app(args.runs_root)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
