# fum_growth_arbiter.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

Purpose
- Unified growth/cull arbiter driven by the void-equation philosophy.
- Extends your original GrowthArbiter with explicit culling and debt accounting.
- Keeps growth pressure as "void debt" when stable and releases it into organic growth.
- When unstable, trends toward culling and reduces debt accordingly.

Blueprint references
- Rule 1: Parallel Local & Global Systems (arbiter is part of the Global System).
- Rule 3: SIE total_reward is the global pressure input (valence/drive).
- Rule 4/4.1: Structural homeostasis and repair triggers.
Time complexity: O(1) per tick (deque pushes and simple checks).
"""

from collections import deque
from typing import Dict
import numpy as np

# Try to align defaults with your universal constants; fall back to safe values.
try:
    from FUM_Void_Equations import get_universal_constants  # noqa: F401
    _UC = get_universal_constants()
    _ALPHA_DEF = float(_UC.get("ALPHA", 0.25))
    _BETA_DEF = float(_UC.get("BETA", 0.10))
except Exception:
    _ALPHA_DEF = 0.25
    _BETA_DEF = 0.10


class GrowthArbiter:
    """
    Monitors rolling metrics to decide when and how much to grow or cull.

    Parameters
    - stability_window: ticks considered to test for a "flat" plateau.
    - trend_threshold: max delta across the window to be considered flat.
    - debt_growth_factor: scale accumulated void debt into new neurons when stable.
    - alpha_growth: growth rate scaling (maps to ALPHA).
    - beta_cull: cull rate scaling (maps to BETA).

    Returns from accumulate_and_decide()
    - dict(grow=int, cull=int, void_debt=float, stable=bool)

    Notes
    - Debt accumulates only while stable; culling reduces debt (cannot drop below 0).
    - Actual target selection for cull/growth (which neurons/edges) is done by the connectome,
      guided by void pulses and S_ij; this arbiter only decides magnitudes and timing.
    """

    def __init__(self,
                 stability_window: int = 10,
                 trend_threshold: float = 0.001,
                 debt_growth_factor: float = 0.10,
                 alpha_growth: float = _ALPHA_DEF,
                 beta_cull: float = _BETA_DEF):
        self.stability_window = int(stability_window)
        self.trend_threshold = float(trend_threshold)
        self.debt_growth_factor = float(debt_growth_factor)
        self.alpha_growth = float(alpha_growth)
        self.beta_cull = float(beta_cull)

        self.weight_history = deque(maxlen=self.stability_window)
        self.synapse_history = deque(maxlen=self.stability_window)
        self.complexity_history = deque(maxlen=self.stability_window)
        self.cohesion_history = deque(maxlen=self.stability_window)

        self.is_stable: bool = False
        self.void_debt_accumulator: float = 0.0  # grows when stable; reduced on cull

    def clear_history(self):
        self.weight_history.clear()
        self.synapse_history.clear()
        self.complexity_history.clear()
        self.cohesion_history.clear()

    def update_metrics(self, metrics: Dict):
        """
        Update historical metrics and recompute stability flag.

        Expected keys (robust to naming differences used elsewhere):
        - avg_weight: float
        - active_synapses: int
        - total_b1_persistence or complexity_cycles: float
        - cohesion_components or cluster_count: int
        """
        self.weight_history.append(float(metrics.get("avg_weight", 0.0)))
        self.synapse_history.append(int(metrics.get("active_synapses", 0)))

        complexity = metrics.get("total_b1_persistence", metrics.get("complexity_cycles", 0.0))
        self.complexity_history.append(float(complexity))

        cohesion = metrics.get("cohesion_components", metrics.get("cluster_count", 1))
        self.cohesion_history.append(int(cohesion))

        if len(self.weight_history) < self.stability_window:
            self.is_stable = False
            return

        is_cohesive = all(c == 1 for c in self.cohesion_history)
        is_weight_flat = abs(self.weight_history[0] - self.weight_history[-1]) < self.trend_threshold
        is_synapse_flat = abs(self.synapse_history[0] - self.synapse_history[-1]) < 3
        is_complexity_flat = abs(self.complexity_history[0] - self.complexity_history[-1]) < self.trend_threshold

        self.is_stable = bool(is_cohesive and is_weight_flat and is_synapse_flat and is_complexity_flat)

    def accumulate_and_decide(self, valence_signal: float) -> Dict:
        """
        Unified decision surface for growth/cull driven by a global pressure (valence).

        Logic
        - If stable: accumulate void debt with |valence|. When debt > 1.0, grow:
            grow = ceil(debt * debt_growth_factor * alpha_growth)
            reset debt, mark unstable, clear history (system re-equilibrates).
        - If unstable: propose cull proportional to beta_cull and |valence|:
            cull = floor(|valence| * beta_cull)
            reduce debt by beta_cull * cull (clamped at 0).
        """
        grow = 0
        cull = 0
        pressure = abs(float(valence_signal))

        if self.is_stable:
            self.void_debt_accumulator += pressure
            if self.void_debt_accumulator > 1.0:
                grow = int(np.ceil(self.void_debt_accumulator * self.debt_growth_factor * self.alpha_growth))
                grow = max(0, grow)
                self.void_debt_accumulator = 0.0
                self.is_stable = False  # perturbation from growth expected
                self.clear_history()
        else:
            cull = int(np.floor(pressure * self.beta_cull))
            cull = max(0, cull)
            if cull > 0:
                self.void_debt_accumulator = max(0.0, self.void_debt_accumulator - (self.beta_cull * cull))

        return {
            "grow": grow,
            "cull": cull,
            "void_debt": float(self.void_debt_accumulator),
            "stable": bool(self.is_stable),
        }