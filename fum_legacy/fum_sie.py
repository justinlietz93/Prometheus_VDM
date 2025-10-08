# fum_sie.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from scipy.sparse import csc_matrix

# --- FUM Modules ---
from fum_validated_math import calculate_modulation_factor

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
        
        # --- Placeholders for Phase 2+ Components ---
        # Per documentation, these are initialized but not used in Phase 1.
        # CRET: Credit and Responsibility Estimation Task buffer
        self.cret_buffer = np.zeros(num_neurons, dtype=np.float32)
        # TD Value Function: Learns to predict future rewards.
        self.td_value_function = np.zeros(num_neurons, dtype=np.float32)
        
        self.last_reward_time = -1

    def update_and_calculate_valence(self, W: csc_matrix, external_signal: float, time_step: int) -> float:
        """
        Updates the Core's internal state and calculates the total valence signal.
        This version implements the full, correct reward modulation logic.

        Args:
            W (csc_matrix): The current state of the Substrate's synaptic pathways.
            external_signal (float): Any feedback from the environment (e.g., task success).
            time_step (int): The current simulation time step.

        Returns:
            float: The total, unified valence signal for this time step.
        """
        # --- 1. Calculate Core Valence Components ---

        # TD Error is the immediate, raw external signal
        self.td_error = external_signal

        # Self-benefit is based on network sparsity (a drive for efficiency)
        num_possible_connections = W.shape[0] * (W.shape[1] - 1)
        density = W.nnz / num_possible_connections if num_possible_connections > 0 else 0
        self.self_benefit = 1.0 - density # Higher reward for lower density

        # --- 2. Calculate Modulation Factor ---
        # The total reward is modulated through a sigmoid to prevent explosive feedback
        # This is the critical step that was missing.
        total_reward_for_modulation = self.td_error + self.self_benefit
        # The correct function from fum_validated_math is `calculate_modulation_factor` which was not being used
        modulation_factor = calculate_modulation_factor(total_reward_for_modulation)


        # --- 3. Update Novelty based on the *modulated* signal ---
        # Drive for exploration is triggered by significant positive, modulated events
        if modulation_factor > 0.5 and (time_step - self.last_reward_time) > 150:
            self.novelty = 0.9
            self.last_reward_time = time_step
        else:
            # Novelty decays exponentially
            self.novelty *= 0.98

        # --- 4. Combine Components for the Final Valence Signal ---
        # This combines the drive for efficiency (self_benefit modulated) with the
        # drive for exploration (novelty).
        total_valence = (modulation_factor + self.novelty) / 2.0


        # --- 5. Final Output ---
        # Ensure the final valence passed to the learning rule is a simple, non-negative float.
        # The VGSP rule is designed for a signal in the [0, 1] range.
        return max(0, abs(total_valence))