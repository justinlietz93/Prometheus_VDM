"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import numpy as np

def compute_metrics(connectome):
   """
   Rule Ref: Blueprint Rule 4.1 (Pathology Detection Mechanisms)
   - Adds connectome_entropy to support Active Domain Cartography (Rule 7) scheduling.
   - Prefers connectome.connectome_entropy() when available (sparse-mode), falling back to local function.
   """
   # TODO GET THESE FOR FREE FROM THE VOID WALKERS
   # Prefer a connectome-native entropy calculator for sparse-mode
   try:
       h = float(connectome.connectome_entropy())
   except Exception:
       h = float(connectome_entropy(connectome))
   return {
       "avg_weight": float(connectome.W.mean()),
       "active_synapses": int(connectome.active_edge_count()),
       "cohesion_components": int(connectome.connected_components()),
       "complexity_cycles": int(connectome.cyclomatic_complexity()),
       "connectome_entropy": h,
   }

def connectome_entropy(connectome) -> float:
   """
   Rule Ref: Blueprint Rule 4.1 — Global Pathological Structure (Connectome Entropy)
   Formula: H = -Σ p_i log(p_i), where p is degree distribution of the active subgraph.
   Returns 0.0 when no active edges are present.
   """
   # Active, undirected mask
   mask = (connectome.E > connectome.threshold) & (connectome.A == 1)
   # Degree per node (count upper+lower symmetrically from full mask)
   deg = mask.sum(axis=1).astype(np.float64)
   total = deg.sum()
   if total <= 0:
       return 0.0
   p = deg / total
   # Numerical stability
   p = np.clip(p, 1e-12, 1.0)
   return float(-(p * np.log(p)).sum())


# --- Streaming z-score detector for first-difference of a scalar series (tick-based) ---
# This keeps state across ticks to detect "spikes" in a topology metric such as
# cyclomatic complexity (a B1 proxy). It is void-faithful: no tokens, only graph-native signals.
import math as _math

class StreamingZEMA:
    """
    EMA-based z-score detector on first differences of a scalar time series.

    Parameters (tick-based):
    - half_life_ticks: EMA half-life in ticks (controls smoothing window)
    - z_spike: z-threshold to enter spiking
    - hysteresis: subtract from z_spike to exit spiking (prevents chatter)
    - min_interval_ticks: minimum ticks between spike fires (cooldown)
    """
    def __init__(self, half_life_ticks: int = 50, z_spike: float = 3.0, hysteresis: float = 1.0, min_interval_ticks: int = 10):
        self.alpha = 1.0 - _math.exp(_math.log(0.5) / float(max(1, int(half_life_ticks))))
        self.z_spike = float(z_spike)
        self.hysteresis = float(max(0.0, hysteresis))
        self.min_interval = int(max(1, int(min_interval_ticks)))

        self.mu = 0.0        # EMA mean of delta
        self.var = 1e-8      # EMA variance of delta
        self.prev = None     # previous value for delta computation
        self._spiking = False
        self.last_fire_tick = -10**12

    def update(self, value: float, tick: int):
        v = float(value)
        if self.prev is None:
            self.prev = v
            return {
                "value": v, "delta": 0.0, "mu": self.mu,
                "sigma": self.var ** 0.5, "z": 0.0, "spike": False
            }

        d = v - self.prev
        self.prev = v

        a = self.alpha
        # EMA on first-difference
        self.mu = (1.0 - a) * self.mu + a * d
        diff = d - self.mu
        self.var = (1.0 - a) * self.var + a * (diff * diff)
        sigma = (self.var if self.var > 1e-24 else 1e-24) ** 0.5
        z = diff / sigma

        # Hysteresis + cooldown
        fire = False
        high = self.z_spike
        low = max(0.0, self.z_spike - self.hysteresis)
        if not self._spiking and z >= high and (int(tick) - int(self.last_fire_tick)) >= self.min_interval:
            self._spiking = True
            self.last_fire_tick = int(tick)
            fire = True
        elif self._spiking and z <= low:
            self._spiking = False

        return {
            "value": v,
            "delta": float(d),
            "mu": float(self.mu),
            "sigma": float(sigma),
            "z": float(z),
            "spike": bool(fire),
        }
