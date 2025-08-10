# fum_validated_math.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np

def sigmoid(x):
    """Numerically stable sigmoid function."""
    x = np.clip(x, -500, 500)
    return 1 / (1 + np.exp(-x))

def calculate_modulation_factor(total_reward: float) -> float:
    """
    Calculates the non-linear modulation factor for the learning rate,
    as specified in the SIE Stability Framework documentation.
    This squashes the total reward into a [-1, 1] range.
    """
    return 2 * sigmoid(total_reward) - 1

def calculate_stabilized_reward(td_error, novelty, habituation, self_benefit, external_reward):
    """
    Calculates the final, stabilized reward signal for the SIE, mirroring
    the logic in the reference validation script.
    """
    # These weights are taken from the reference implementation
    W_TD = 0.5
    W_NOVELTY = 0.2
    W_HABITUATION = 0.1
    W_SELF_BENEFIT = 0.2
    W_EXTERNAL = 0.8

    td_norm = np.clip(td_error, -1, 1)
    
    # Damping term to balance exploration vs. exploitation
    alpha_damping = 1.0 - np.tanh(np.abs(novelty - self_benefit))

    damped_novelty_term = alpha_damping * (W_NOVELTY * novelty - W_HABITUATION * habituation)
    damped_self_benefit_term = alpha_damping * (W_SELF_BENEFIT * self_benefit)
    
    w_r = W_EXTERNAL if external_reward is not None and external_reward > 0 else (1 - W_EXTERNAL)
    w_internal = 1 - w_r
    
    internal_reward = (W_TD * td_norm +
                       damped_novelty_term +
                       damped_self_benefit_term)
                       
    total_reward = w_r * external_reward if external_reward is not None else internal_reward
    
    return total_reward