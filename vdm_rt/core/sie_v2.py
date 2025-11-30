"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
# sie_v2.py
# Void-faithful per-tick intrinsic drive computed directly from W and dW
# Produces a per-neuron reward vector and a smooth scalar valence in [0,1]
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass

@dataclass
class SIECfg:
    td_w: float = 0.50
    nov_w: float = 0.20
    hab_w: float = 0.10
    hsi_w: float = 0.20
    half_life_ticks: int = 600     # EMA half-life for habituation stats
    target_var: float = 0.10       # desired variance of |dW|
    reward_clip: float = 1.0
    valence_beta: float = 0.30     # smoothing for scalar valence

class SIEState:
    def __init__(self, N: int, cfg: SIECfg):
        self.cfg = cfg
        self.mu = np.zeros(N, dtype=np.float32)   # EMA mean of |dW|
        self.var = np.zeros(N, dtype=np.float32)  # EMA var of |dW|
        self.prev_W = np.zeros(N, dtype=np.float32)
        self.valence = 0.0

def _ema_update(old: np.ndarray, new: np.ndarray, half_life_ticks: int) -> np.ndarray:
    # Convert half-life to per-tick EMA alpha
    a = 1.0 - math.exp(math.log(0.5) / float(max(1, int(half_life_ticks))))
    return (1.0 - a) * old + a * new

def _novelty_norm(spike_mag: np.ndarray) -> np.ndarray:
    m = float(np.max(spike_mag)) if spike_mag.size else 0.0
    if m <= 1e-12:
        return np.zeros_like(spike_mag, dtype=np.float32)
    return (spike_mag / m).astype(np.float32)

def _hsi_norm(mu: np.ndarray, var: np.ndarray, target_var: float) -> np.ndarray:
    # mean term high when mu ~ 0.5 after implicit normalization (here we use |dW| EMA; bias toward mid-range activity)
    mean_term = 1.0 - np.minimum(1.0, np.abs(mu - 0.5) * 2.0)
    # variance term high when var close to target_var
    tv = max(1e-8, float(target_var))
    var_term = 1.0 - np.minimum(1.0, np.abs(var - tv) / tv)
    return (0.5 * (mean_term + var_term)).astype(np.float32)

def sie_step(state: SIEState, W: np.ndarray, dW: np.ndarray):
    """
    Compute per-neuron reward and smooth scalar valence:
    - novelty from |dW|
    - habituation via EMA(mu,var) of |dW|
    - TD from W - γ·prev_W (γ≈0.99), normalized
    - HSI from closeness of (mu,var) to (0.5, target_var)
    Returns:
        (reward_vec: np.ndarray[float32], valence_01: float)
    """
    cfg = state.cfg
    spikes = np.abs(dW).astype(np.float32)

    # Update habituation statistics (EMA mean/var of |dW|)
    mu_new = _ema_update(state.mu, spikes, cfg.half_life_ticks)
    diff = spikes - mu_new
    var_new = _ema_update(state.var, diff * diff, cfg.half_life_ticks)
    state.mu = mu_new.astype(np.float32)
    state.var = var_new.astype(np.float32)

    nov = _novelty_norm(spikes)
    hab = state.mu

    # TD on field with light discount, normalized by max |td|
    td = (W.astype(np.float32) - 0.99 * state.prev_W.astype(np.float32))
    mtd = float(np.max(np.abs(td))) if td.size else 0.0
    if mtd > 1e-12:
        td = (td / mtd).astype(np.float32)
    else:
        td = np.zeros_like(td, dtype=np.float32)
    state.prev_W = W.astype(np.float32)

    # HSI stability indicator
    stab = _hsi_norm(state.mu, state.var, cfg.target_var)

    # Weighted reward, clipped
    r = (cfg.td_w * td) + (cfg.nov_w * nov) - (cfg.hab_w * hab) + (cfg.hsi_w * stab)
    r = np.clip(r, -cfg.reward_clip, cfg.reward_clip).astype(np.float32)

    # Scalar valence in [0,1], smoothed
    r_bar = float(np.mean(r)) if r.size else 0.0
    v_raw = 0.5 + 0.5 * (r_bar / (cfg.reward_clip + 1e-8))
    state.valence = (1.0 - cfg.valence_beta) * float(state.valence) + cfg.valence_beta * float(v_raw)
    # numerically clip
    state.valence = float(max(0.0, min(1.0, state.valence)))

    return r, state.valence