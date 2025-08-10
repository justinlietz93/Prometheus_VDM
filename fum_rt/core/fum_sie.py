# fum_sie.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from scipy.sparse import csc_matrix

# --- FUM Modules (optional external helpers) ---
# Keep copyright and your original API intact; add robust fallbacks so fum_rt
# does not depend on external paths being on PYTHONPATH.
try:
    from fum_validated_math import (
        calculate_modulation_factor as _ext_calculate_modulation_factor,
        calculate_stabilized_reward as _ext_calculate_stabilized_reward,
    )
    _HAVE_VALIDATED_MATH = True
except Exception:
    _HAVE_VALIDATED_MATH = False
    _ext_calculate_modulation_factor = None
    _ext_calculate_stabilized_reward = None


def _sigmoid(x: float) -> float:
    x = float(np.clip(x, -500.0, 500.0))
    return 1.0 / (1.0 + np.exp(-x))


def _calculate_modulation_factor(total_reward: float) -> float:
    """
    Blueprint Rule 3 helper: squash to [-1, 1].
    Falls back to internal implementation if the external helper is not available.
    """
    if _HAVE_VALIDATED_MATH and _ext_calculate_modulation_factor is not None:
        try:
            return float(_ext_calculate_modulation_factor(total_reward))
        except Exception:
            pass
    return 2.0 * _sigmoid(total_reward) - 1.0


def _calculate_stabilized_reward(td_error, novelty, habituation, self_benefit, external_reward):
    """
    Blueprint Rule 3 helper: stabilized reward blend (weights + damping).
    Mirrors early_FUM_tests/FUM_Demo/fum_validated_math.py semantics when available.
    """
    if _HAVE_VALIDATED_MATH and _ext_calculate_stabilized_reward is not None:
        try:
            return float(_ext_calculate_stabilized_reward(td_error, novelty, habituation, self_benefit, external_reward))
        except Exception:
            pass
    # Internal fallback (mirrors the reference file)
    W_TD, W_NOVELTY, W_HABITUATION, W_SELF_BENEFIT, W_EXTERNAL = 0.5, 0.2, 0.1, 0.2, 0.8
    td_norm = float(np.clip(td_error, -1.0, 1.0))
    alpha_damping = 1.0 - np.tanh(abs(novelty - self_benefit))
    damped_novelty_term = alpha_damping * (W_NOVELTY * novelty - W_HABITUATION * habituation)
    damped_self_benefit_term = alpha_damping * (W_SELF_BENEFIT * self_benefit)
    if external_reward is not None:
        w_r = W_EXTERNAL if external_reward > 0 else (1.0 - W_EXTERNAL)
        total_reward = w_r * external_reward
    else:
        total_reward = (W_TD * td_norm) + damped_novelty_term + damped_self_benefit_term
    return float(total_reward)

class SelfImprovementEngine:
    """
    The FUM's Self-Improvement Engine (SIE).
    
    This module is the system's intrinsic motivation. It generates the
    internal, multi-objective valence signal that guides all learning and
    adaptation within the Substrate.
    """
    def __init__(self, num_neurons):
        self.num_neurons = num_neurons
        # --- Core Valence Components ---
        self.td_error = 0.0      # Represents unexpectedness or prediction error
        self.novelty = 0.0       # The drive to explore new informational states
        self.habituation = np.zeros(num_neurons) # Counter-force to Novelty
        self.self_benefit = 0.0  # The drive for efficiency and stability

        # --- Phase 2+ / buffers kept intact (preserve your original API/state) ---
        self.cret_buffer = np.zeros(num_neurons, dtype=np.float32)        # CRET
        self.td_value_function = np.zeros(num_neurons, dtype=np.float32)  # TD V

        # Internal bookkeeping (not externally required)
        self.last_reward_time = -1
        self.last_drive = None  # stores the latest computed drive packet (see get_drive)
        self._prev_density = None  # for intrinsic TD proxy (density delta)

    def update_and_calculate_valence(self, W: csc_matrix, external_signal: float, time_step: int) -> float:
        """
        Updates the Core's internal state and returns a unified valence signal in [0, 1].
        Backward-compatible with your original API, while also computing a Rule 3 drive packet.
        """
        drive = self.get_drive(W=W, external_signal=external_signal, time_step=time_step)
        # Preserve legacy behavior: return the [0,1] valence (VGSP-compatible magnitude)
        return float(drive["valence_01"])

    def update_from_runtime_metrics(self, density: float, external_signal: float, time_step: int) -> float:
        """
        Lightweight Rule 3 drive update that avoids requiring a CSC matrix.
        Preserves novelty decay and self_benefit semantics; returns valence in [0,1]
        for VGSP gating. Also updates self.last_drive for introspection.

        Args:
            density: float in [0,1] computed as W.nnz / possible_edges; self_benefit = 1 - density
            external_signal: task or environment feedback, can be None
            time_step: current tick

        Returns:
            float in [0,1]: valence magnitude for gating RE‑VGSP.
        """
        try:
            self.self_benefit = float(1.0 - float(density))
        except Exception:
            self.self_benefit = 0.0

        self.td_error = 0.0 if external_signal is None else float(external_signal)
        habituation_mean = float(self.habituation.mean() if self.habituation.size else 0.0)

        total_reward = _calculate_stabilized_reward(
            td_error=self.td_error,
            novelty=self.novelty,
            habituation=habituation_mean,
            self_benefit=self.self_benefit,
            external_reward=None if external_signal is None else float(external_signal),
        )
        modulation = _calculate_modulation_factor(total_reward)

        # Preserve your novelty trigger dynamics
        if modulation > 0.5 and (time_step - self.last_reward_time) > 150:
            self.novelty = 0.9
            self.last_reward_time = int(time_step)
        else:
            self.novelty *= 0.98

        valence_01 = max(0.0, abs((modulation + self.novelty) / 2.0))

        # Maintain a compact drive packet for downstream consumers
        self.last_drive = {
            "total_reward": float(np.clip(total_reward, -1.0, 1.0)),
            "modulation_factor": float(np.clip(modulation, -1.0, 1.0)),
            "valence_01": float(np.clip(valence_01, 0.0, 1.0)),
            "components": {
                "td_error": float(self.td_error),
                "novelty": float(self.novelty),
                "habituation_mean": float(habituation_mean),
                "self_benefit": float(self.self_benefit),
                "density": float(density),
            }
        }
        return float(self.last_drive["valence_01"])

    # --- Blueprint Rule 3 canonical helpers (kept additive to your API) ---

    def _compute_hsi_norm(self, firing_var: float = None, target_var: float = 0.15) -> float:
        """
        Rule 3 HSI component: higher when firing variance is close to target.
        Returns value in [-1, 1].
        """
        if firing_var is None:
            return 0.0
        target = max(1e-6, float(target_var))
        # Map proximity to target into [-1,1] where exact match -> +1, far -> negative
        prox = 1.0 - min(1.0, abs(float(firing_var) - target) / target)
        # Center around 0; maintain symmetry
        return float(2.0 * prox - 1.0)

    def get_drive(self, W: csc_matrix, external_signal: float, time_step: int,
                  firing_var: float = None, target_var: float = 0.15,
                  weights: dict | None = None,
                  density_override: float | None = None) -> dict:
        """
        Compute the canonical Rule 3 drive packet, preserving your novelty and sparsity logic.
        Returns:
            {
              'total_reward': [-1,1],
              'modulation_factor': [-1,1],
              'valence_01': [0,1],            # legacy-compatible magnitude
              'components': {
                   'td_error': ..., 'novelty': ..., 'habituation_mean': ...,
                   'self_benefit': ..., 'hsi_norm': ..., 'density': ...
              }
            }
        """
        # TD error and sparsity (self_benefit) as in your code
        # Allow None to mean "no external reward signal" (intrinsic-only blending)
        ext_val = 0.0 if (external_signal is None) else float(external_signal)

        # Density can be provided directly to avoid converting W; falls back to W if available
        if density_override is not None:
            density = float(min(1.0, max(0.0, density_override)))
        else:
            if W is not None:
                n = int(W.shape[0])
                num_possible_connections = n * max(0, (W.shape[1] - 1))
                density = (W.nnz / num_possible_connections) if num_possible_connections > 0 else 0.0
            else:
                density = 0.0

        # Intrinsic TD proxy from density change if external is absent/negligible
        prev = getattr(self, "_prev_density", None)
        ddens = 0.0 if prev is None else float(density - prev)
        try:
            self._prev_density = float(density)
        except Exception:
            pass
        intrinsic_td = float(np.clip(ddens * 10.0, -1.0, 1.0))
        td = float(ext_val) if abs(float(ext_val)) > 1e-9 else intrinsic_td
        self.td_error = float(td)

        # Self-benefit and a very-light EMA toward topology saturation as a habituation proxy
        self.self_benefit = float(1.0 - density)
        try:
            self.habituation = (0.995 * self.habituation) + (0.005 * float(density))
        except Exception:
            pass

        # Habituation (aggregate for now; you already maintain the vector)
        habituation_mean = float(self.habituation.mean() if self.habituation.size else 0.0)

        # HSI via variance target
        hsi_norm = self._compute_hsi_norm(firing_var=firing_var, target_var=target_var)

        # Stabilized total reward (signed), then squashed to modulation factor
        # Use intrinsic blend so TD/novelty/habituation/self_benefit all contribute
        total_reward = _calculate_stabilized_reward(
            td_error=self.td_error,
            novelty=self.novelty,
            habituation=habituation_mean,
            self_benefit=self.self_benefit,
            external_reward=None,
        )
        modulation_factor = _calculate_modulation_factor(total_reward)

        # Novelty dynamics: trigger on modulation or topology change spikes
        trigger = (modulation_factor > 0.5) or (abs(ddens) > 1e-3) or (abs(self.td_error) > 0.05)
        if trigger and (time_step - self.last_reward_time) > 50:
            # proportional to spike, capped and with partial retention
            self.novelty = float(min(0.95, max(self.novelty * 0.5, 0.3 + 3.0 * abs(intrinsic_td))))
            self.last_reward_time = int(time_step)
        else:
            self.novelty *= 0.995

        # Legacy [0,1] valence magnitude for VGSP gating as needed
        valence_01 = max(0.0, abs((modulation_factor + self.novelty) / 2.0))

        packet = {
            "total_reward": float(np.clip(total_reward, -1.0, 1.0)),
            "modulation_factor": float(np.clip(modulation_factor, -1.0, 1.0)),
            "valence_01": float(np.clip(valence_01, 0.0, 1.0)),
            "components": {
                "td_error": float(self.td_error),
                "novelty": float(self.novelty),
                "habituation_mean": float(habituation_mean),
                "self_benefit": float(self.self_benefit),
                "hsi_norm": float(hsi_norm),
                "density": float(density),
            }
        }
        self.last_drive = packet
        return packet
        """
        Resizes the internal buffers to accommodate a new number of neurons after growth.
        """
        old_num_neurons = self.num_neurons
        if new_num_neurons <= old_num_neurons:
            return

        # Calculate the number of neurons added
        num_added = new_num_neurons - old_num_neurons

        # Create zero arrays for the new neurons
        zeros_to_add = np.zeros(num_added, dtype=np.float32)

        # Add the new zero elements to the end of the existing buffers
        self.cret_buffer = np.concatenate([self.cret_buffer, zeros_to_add])
        self.td_value_function = np.concatenate([self.td_value_function, zeros_to_add])
        self.habituation = np.concatenate([self.habituation, np.zeros(num_added)])

        # Update the neuron count
        self.num_neurons = new_num_neurons
        print(f"--- SIE buffers resized to accommodate {self.num_neurons} neurons. ---")