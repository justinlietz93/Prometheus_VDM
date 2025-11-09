"""
License notice
- Copyright © 2025 Justin K. Lietz, Neuroca, Inc.
- Dual-license: open academic use; commercial use of proprietary VDM code requires written permission.
  See LICENSE for full terms.

GB Relaxation Meter — Oscillating Load Runner (domain=boundaries · instrument=T2)

Purpose
- Execute oscillatory-load experiments on a grain boundary (GB) specimen and evaluate the T2 meter:
  γ²-law fit, asymmetric emission threshold, cycle-Lyapunov descent, protocol-insensitivity, and A6-style
  dimensionless scaling collapse. Emits PNG/CSV/JSON artifacts and pass/fail gates.

Canon references (anchors only; no duplication of equations or numbers here)
- Algorithms: Derivation/ALGORITHMS.md#vdm-a-047   (GB Relaxation Meter · Oscillating Load)
- Equations:  Derivation/EQUATIONS.md#vdm-e-160    (GB excess energy γ² law anchor)
               Derivation/EQUATIONS.md#vdm-e-161    (Asymmetric emission threshold anchor)
               Derivation/EQUATIONS.md#vdm-e-162    (Cycle-Lyapunov monotonicity anchor)
               Derivation/EQUATIONS.md#vdm-e-163    (Moiré-contrast observable anchor)
               Derivation/EQUATIONS.md#vdm-e-164    (Dimensionless groups / scaling program anchor)
- KPIs/Gates: Derivation/VALIDATION_METRICS.md#kpi-gb-gamma2-law
               Derivation/VALIDATION_METRICS.md#kpi-gb-asym-threshold
               Derivation/VALIDATION_METRICS.md#kpi-gb-lyapunov-cycle
               Derivation/VALIDATION_METRICS.md#kpi-gb-protocol-insensitivity
               Derivation/VALIDATION_METRICS.md#kpi-gb-dimless-collapse
- Units & normalization: Derivation/UNITS_NORMALIZATION.md
- IO routing standard: Derivation/code/common/io_paths.py
- Approvals & policy:  Derivation/code/ARCHITECTURE.md (approve before runs; quarantine unapproved)

File-length policy (z.CANONICAL standard)
- Keep this file ≤ 500 lines. If additions would exceed the limit, start a new sequential file:
  run_GB_Oscillating_Load_02.py, run_GB_Oscillating_Load_03.py, …
  See patterns in Derivation/z.CANONICAL_*/00_*.md for numbering discipline.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple

import numpy as np
import sys

# Ensure common helpers on path
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from common.data.results_db import (
    begin_run,
    add_artifacts,
    log_metrics,
    end_run_success,
    end_run_failed,
)
from common.authorization.approval import check_tag_approval


# Instrument helper imports (boundaries) — registered in canon
from common.instrument_helpers.boundaries.gb_energy_gamma2_fitter import GBExcessEnergyGamma2Fitter  # noqa: F401
from common.instrument_helpers.boundaries.gb_cycle_lyapunov import GBLyapunovCycleMonitor  # noqa: F401
from common.instrument_helpers.boundaries.gb_emission_threshold import GBEmissionThresholdEstimator  # noqa: F401
from common.instrument_helpers.boundaries.gb_moire_contrast import GBMoireContrast  # noqa: F401
