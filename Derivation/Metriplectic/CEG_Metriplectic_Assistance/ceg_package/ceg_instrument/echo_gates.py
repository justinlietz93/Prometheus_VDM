#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Gate checks for the CEG instrument.  Five gates certify each run:

- G1 (Noether): J-only energy drift ≤ tolerance
- G2 (H-theorem): M-only entropy production ≥ 0
- G3 (Energy match): baseline and assisted use identical work budgets
- G4 (Strang defect): splitting error scales as O(dt³) with R² ≥ 0.999
- G5 (CEG threshold): median CEG across seeds ≥ 0.05
"""
from __future__ import annotations

from typing import Dict, Any


def gate_noether(time_reversal_energy_drift: float, tol: float = 1e-12) -> Dict[str, Any]:
    ok = abs(float(time_reversal_energy_drift)) <= float(tol)
    return {"gate": "G1_Noether_J", "tol": tol, "drift": float(time_reversal_energy_drift), "passed": bool(ok)}


def gate_h_theorem(delta_sigma_min: float, tol: float = 1e-12) -> Dict[str, Any]:
    ok = (float(delta_sigma_min) >= -float(tol))
    return {"gate": "G2_H_theorem_M", "tol": tol, "delta_sigma_min": float(delta_sigma_min), "passed": bool(ok)}


def gate_energy_match(rel_diff: float, tol: float = 1e-4) -> Dict[str, Any]:
    ok = abs(float(rel_diff)) <= float(tol)
    return {"gate": "G3_EnergyMatch", "tol": tol, "rel_diff": float(rel_diff), "passed": bool(ok)}


def gate_strang_defect(slope: float, r2: float) -> Dict[str, Any]:
    ok = (float(slope) >= 2.90) and (float(r2) >= 0.999)
    return {"gate": "G4_StrangDefect", "slope": float(slope), "R2": float(r2), "passed": bool(ok)}
