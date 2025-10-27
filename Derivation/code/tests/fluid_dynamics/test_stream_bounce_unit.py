#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import json, time, os
import numpy as np
from Prometheus_VDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig

def run_test1():
    cfg = LBMConfig(nx=8, ny=8, tau=0.9, periodic_x=False, periodic_y=False, void_enabled=False)
    sim = LBM2D(cfg)
    sim.f[:] = 0.0
    sim.f[2, 4, 4] = 1.0
    m0 = float(sim.f.sum())
    sim.stream()
    m1 = float(sim.f.sum())
    dest = float(sim.f[2, 3, 4])
    return {"name":"north_move","mass0":m0,"mass1":m1,"dest":dest,"pass": (abs(m1 - m0) < 1e-12 and abs(dest - 1.0) < 1e-12)}

def run_test2():
    cfg = LBMConfig(nx=8, ny=8, tau=0.9, periodic_x=False, periodic_y=False, void_enabled=False)
    sim = LBM2D(cfg)
    sim.set_solid_box(top=True, bottom=False, left=False, right=False)
    sim.f[:] = 0.0
    sim.f[2, 1, 4] = 1.0
    m0 = float(sim.f.sum())
    sim.stream()
    m1 = float(sim.f.sum())
    refl = float(sim.f[4, 0, 4])
    return {"name":"top_bounce","mass0":m0,"mass1":m1,"f4_at_top":refl,"pass": (abs(m1 - m0) < 1e-12 and abs(refl - 1.0) < 1e-12)}

def main():
    t1 = run_test1()
    t2 = run_test2()
    overall = t1["pass"] and t2["pass"]
    payload = {
      "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
      "tests": [t1, t2],
      "overall_pass": overall
    }
    print(json.dumps(payload))
    out_dir = os.path.join("Prometheus_VDM","derivation","code","outputs","logs","fluid_dynamics")
    os.makedirs(out_dir, exist_ok=True)
    fname = f"stream_bounce_unit_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
    with open(os.path.join(out_dir, fname), "w") as f:
        json.dump(payload, f, indent=2)

if __name__ == "__main__":
    main()