"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a proprietary license. Use requires written
permission from Justin K. Lietz. See LICENSE file for full terms.

SIE Stability Simulation - Multi-objective reward integration validation
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import os # Import os module
import argparse # Import argparse for command-line arguments

# --- Simulation Parameters ---
NUM_NEURONS = 100 # Simplified network size for simulation
NUM_CLUSTERS = 10 # Number of functional clusters
SIMULATION_STEPS = 10000
ETA = 0.01 # Base STDP learning rate
GAMMA = 0.9 # TD discount factor
ALPHA = 0.1 # TD learning rate
TARGET_VAR = 0.05 # Target variance for self_benefit calculation
LAMBDA = 0.001 # Weight decay coefficient (NEW)
DT = 1.0 # Simulation time step (ms)
TAU_MEMBRANE = 10.0 # LIF membrane time constant (ms)
V_THRESH = 1.0 # LIF threshold voltage
V_RESET = 0.0 # LIF reset voltage
INHIB_FRACTION = 0.2 # Fraction of inhibitory neurons
DEFAULT_SCALING_TARGET = NUM_NEURONS * 0.1 # Default target sum for synaptic scaling

# SIE Component Weights (Example - will be varied in tests)
W_TD = 0.5
W_NOVELTY = 0.2
W_HABITUATION = 0.1
W_SELF_BENEFIT = 0.2
W_EXTERNAL = 0.8 # Weight for external reward when available

# --- Helper Functions ---

def sigmoid(x):
    # Add small epsilon to prevent overflow with large negative x
    x = np.clip(x, -500, 500) 
    return 1 / (1 + np.exp(-x))

def calculate_sie_components(current_state, recent_inputs, habituation_counters, spike_rates_history, V_states, external_reward=None):
    """Calculates the components of the SIE reward signal."""
    # --- TD Error ---
    current_state_idx = current_state['cluster_id']
    next_state_idx = np.random.randint(NUM_CLUSTERS) # Placeholder
    r = external_reward if external_reward is not None else 0 
    td_error = r + GAMMA * V_states[next_state_idx] - V_states[current_state_idx]

    # --- Novelty ---
    current_input = current_state['input_pattern']
    novelty = 1.0
    matched_idx = -1
    if len(recent_inputs) > 0:
        # Ensure consistent shapes for dot product if input dim varies
        input_len = len(current_input)
        similarities = [np.dot(current_input, inp[:input_len]) / (np.linalg.norm(current_input) * np.linalg.norm(inp[:input_len]) + 1e-9) 
                        for inp in recent_inputs if len(inp) >= input_len] # Handle potential shape mismatches gracefully
        if similarities:
            max_similarity = np.max(similarities)
            novelty = 1.0 - max_similarity
            # Find index corresponding to max similarity among valid comparisons
            valid_indices = [idx for idx, inp in enumerate(recent_inputs) if len(inp) >= input_len]
            if valid_indices:
                 matched_idx_local = np.argmax(similarities)
                 matched_idx = valid_indices[matched_idx_local]

    # --- Habituation ---
    habituation = 0.0
    if matched_idx != -1 and max_similarity > 0.9:
         # Ensure matched_idx is valid for habituation_counters
         if matched_idx < len(habituation_counters):
             habituation_counters[matched_idx] = min(1.0, habituation_counters[matched_idx] + 0.1)
             habituation = habituation_counters[matched_idx]
         else:
             print(f"Warning: matched_idx {matched_idx} out of bounds for habituation_counters (size {len(habituation_counters)})")


    # Decay counters
    habituation_counters *= 0.995 

    # --- Self-Benefit (Homeostasis-Based) ---
    self_benefit = 0.5 # Default value
    if len(spike_rates_history) > 100: 
        # Use rates from the last 100 steps, not the entire history for variance
        relevant_rates = spike_rates_history[-100:]
        if len(relevant_rates) > 1: # Need at least 2 points for variance
             current_variance = np.var(relevant_rates)
             # Avoid division by zero if TARGET_VAR is 0
             if TARGET_VAR > 1e-9:
                 self_benefit = 1.0 - min(1.0, np.abs(current_variance - TARGET_VAR) / TARGET_VAR) 
             else:
                 self_benefit = 1.0 if current_variance < 1e-9 else 0.0


    # --- Normalization & Damping ---
    td_norm = np.clip(td_error, -1, 1) 
    novelty_norm = novelty 
    habituation_norm = habituation
    self_benefit_norm = self_benefit 
    
    alpha_damping = 1.0 - np.tanh(np.abs(novelty_norm - self_benefit_norm)) 
    
    damped_novelty_term = alpha_damping * (W_NOVELTY * novelty_norm - W_HABITUATION * habituation_norm)
    damped_self_benefit_term = alpha_damping * (W_SELF_BENEFIT * self_benefit_norm)

    w_r = W_EXTERNAL if external_reward is not None else (1 - W_EXTERNAL)
    w_internal = 1 - w_r
    
    internal_reward = (W_TD * td_norm + 
                       damped_novelty_term + 
                       damped_self_benefit_term)
                       
    total_reward = w_r * r + w_internal * internal_reward

    # --- Update History ---
    # Ensure habituation counter size matches recent inputs size
    max_history_size = 50 
    if len(recent_inputs) >= max_history_size: 
        recent_inputs.pop(0)
        # Shift habituation counters - this was missing!
        habituation_counters = np.roll(habituation_counters, -1)
        habituation_counters[-1] = 0 # Clear the last element
        
    recent_inputs.append(current_input)

    return total_reward, td_error, novelty, habituation, self_benefit, next_state_idx

def update_weights(W, eligibility_trace, total_reward, mod_factor, eta, decay_lambda, is_inhibitory):
    """Applies the modulated STDP update with weight decay and E/I constraints."""
    eta_effective = eta * (1 + mod_factor)
    hebbian_update = eta_effective * total_reward * eligibility_trace
    decay_term = decay_lambda * W
    
    W += hebbian_update - decay_term
    
    inhib_indices = np.where(is_inhibitory)[0]
    excit_indices = np.where(~is_inhibitory)[0]
    if len(inhib_indices) > 0:
        W[inhib_indices, :] = np.minimum(W[inhib_indices, :], 0) 
    if len(excit_indices) > 0:
        W[excit_indices, :] = np.maximum(W[excit_indices, :], 0) 
        
    W = np.clip(W, -1.0, 1.0) 
    np.fill_diagonal(W, 0)
    return W

def apply_synaptic_scaling(W, target_sum):
    """Applies simple multiplicative scaling to incoming weights."""
    # Calculate sum of incoming positive weights for each neuron
    # Ensure W is treated as float for sum, prevent potential type issues
    incoming_sums = np.sum(np.maximum(W.astype(float), 0), axis=0) 
    # Avoid division by zero or very small numbers
    incoming_sums[incoming_sums < 1e-6] = 1.0 
    scale_factors = target_sum / incoming_sums
    # Apply scaling multiplicatively 
    W_scaled = W * scale_factors[np.newaxis, :] 
    # Re-apply clipping after scaling
    W_scaled = np.clip(W_scaled, -1.0, 1.0)
    return W_scaled

# --- Simulation Loop ---

def run_simulation(params):
    """Runs the SIE stability simulation."""
    print(f"Running simulation with params: {params}")
    
    # Extract parameters
    eta = params['eta']
    lambda_decay = params['lambda_decay']
    scaling_target = params['scaling_target']

    # Initialize state
    num_inhibitory = int(NUM_NEURONS * INHIB_FRACTION)
    is_inhibitory = np.zeros(NUM_NEURONS, dtype=bool)
    inhib_indices = np.random.choice(NUM_NEURONS, num_inhibitory, replace=False)
    is_inhibitory[inhib_indices] = True
    excit_indices = np.where(~is_inhibitory)[0]
    
    W = np.random.rand(NUM_NEURONS, NUM_NEURONS) * 0.1 
    if num_inhibitory > 0:
        W[inhib_indices, :] *= -1 
        W[inhib_indices, :] = np.clip(W[inhib_indices, :], -1.0, 0.0) 
    if len(excit_indices) > 0:
         W[excit_indices, :] = np.clip(W[excit_indices, :], 0.0, 1.0) 

    np.fill_diagonal(W, 0) 
    
    V_mem = np.random.rand(NUM_NEURONS) * V_THRESH 
    spikes = np.zeros(NUM_NEURONS, dtype=bool) 
    last_spike_time = np.full(NUM_NEURONS, -np.inf) 
    
    V_states = np.zeros(NUM_CLUSTERS) 
    eligibility_trace = np.zeros((NUM_NEURONS, NUM_NEURONS)) 
    TAU_ELIGIBILITY = 20.0 
    A_PLUS = 0.1 
    TAU_STDP = 15.0 

    max_history_size = 50
    recent_inputs = [] # List to store input patterns
    habituation_counters = np.zeros(max_history_size) # Match size
    spike_rates_history = []

    # History tracking
    reward_history = []
    mod_factor_history = []
    weight_norm_history = []
    v_state_history = []
    component_history = {'td': [], 'nov': [], 'hab': [], 'sb': []}

    start_time = time.time()
    for step in range(SIMULATION_STEPS):
        # --- 1. Simulate Network Activity (LIF Neurons) ---
        input_current = np.random.rand(NUM_NEURONS) * 0.5 
        synaptic_input = W @ spikes 
        dV = (-(V_mem - V_RESET) + input_current + synaptic_input) * (DT / TAU_MEMBRANE)
        V_mem += dV
        spikes = V_mem >= V_THRESH
        V_mem[spikes] = V_RESET 
        current_avg_rate = np.mean(spikes) 
        spike_rates_history.append(current_avg_rate) 
        current_cluster_id = np.random.randint(NUM_CLUSTERS) 
        current_input_pattern_for_novelty = input_current 
        current_state = {'input_pattern': current_input_pattern_for_novelty, 'cluster_id': current_cluster_id}
        
        current_time = step * DT
        last_spike_time[spikes] = current_time

        eligibility_trace *= np.exp(-DT / TAU_ELIGIBILITY) 
        spiked_indices = np.where(spikes)[0]
        # Use vectorization for eligibility trace update if possible for performance
        # This loop is slow for large N
        for i in spiked_indices: 
            valid_pre_indices = np.where((last_spike_time < current_time) & (np.arange(NUM_NEURONS) != i))[0]
            time_diffs = current_time - last_spike_time[valid_pre_indices]
            potentiation = A_PLUS * np.exp(-time_diffs / TAU_STDP)
            eligibility_trace[valid_pre_indices, i] += potentiation
            
        eligibility_trace = np.clip(eligibility_trace, 0, 1) 

        # --- 2. Calculate SIE Reward ---
        external_reward = 1.0 if step % 100 == 0 else None 
        total_reward, td, nov, hab, sb, next_state_idx = calculate_sie_components(
            current_state, recent_inputs, habituation_counters, spike_rates_history, V_states, external_reward
        )
        
        # --- 3. Update TD Value Function ---
        V_states[current_cluster_id] += ALPHA * td

        # --- 4. Calculate Modulation Factor ---
        mod_factor = 2 * sigmoid(total_reward) - 1

        # --- 5. Update Weights ---
        W = update_weights(W, eligibility_trace, total_reward, mod_factor, eta, lambda_decay, is_inhibitory) 
        
        # --- 5b. Apply Synaptic Scaling (Homeostasis) ---
        if step > 0 and step % 20 == 0: # Avoid scaling at step 0 before weights update
             W = apply_synaptic_scaling(W, target_sum=scaling_target) 
             # Re-enforce E/I after scaling
             if len(inhib_indices) > 0:
                 W[inhib_indices, :] = np.minimum(W[inhib_indices, :], 0) 
             if len(excit_indices) > 0:
                 W[excit_indices, :] = np.maximum(W[excit_indices, :], 0) 
             np.fill_diagonal(W, 0)


        # --- 6. Track History ---
        reward_history.append(total_reward)
        mod_factor_history.append(mod_factor)
        weight_norm_history.append(np.linalg.norm(W))
        v_state_history.append(np.mean(V_states))
        component_history['td'].append(td)
        component_history['nov'].append(nov)
        component_history['hab'].append(hab)
        component_history['sb'].append(sb)

        if step % 1000 == 0:
            print(f"Step {step}/{SIMULATION_STEPS} - Reward: {total_reward:.3f}, ModFactor: {mod_factor:.3f}, ||W||: {weight_norm_history[-1]:.2f}")

    end_time = time.time()
    print(f"Simulation finished in {end_time - start_time:.2f} seconds.")

    # --- 7. Plot Results ---
    plt.figure(figsize=(12, 10))
    
    plt.subplot(3, 2, 1)
    plt.plot(reward_history)
    plt.title('Total Reward')
    plt.xlabel('Step')
    plt.ylabel('Reward')

    plt.subplot(3, 2, 2)
    plt.plot(mod_factor_history)
    plt.title('Modulation Factor')
    plt.xlabel('Step')
    plt.ylabel('Factor')

    plt.subplot(3, 2, 3)
    plt.plot(weight_norm_history)
    plt.title('Weight Matrix Norm ||W||')
    plt.xlabel('Step')
    plt.ylabel('Norm')

    plt.subplot(3, 2, 4)
    plt.plot(v_state_history)
    plt.title('Average V(state)')
    plt.xlabel('Step')
    plt.ylabel('Avg Value')

    plt.subplot(3, 2, 5)
    plt.plot(component_history['nov'], label='Novelty', alpha=0.7)
    plt.plot(component_history['hab'], label='Habituation', alpha=0.7)
    plt.plot(component_history['sb'], label='Self-Benefit', alpha=0.7)
    plt.title('SIE Components (Internal)')
    plt.xlabel('Step')
    plt.ylabel('Value')
    plt.legend()
    
    plt.subplot(3, 2, 6)
    plt.plot(component_history['td'], label='TD Error', alpha=0.7)
    plt.title('SIE Component (TD Error)')
    plt.xlabel('Step')
    plt.ylabel('Value')
    plt.legend()

    plt.tight_layout()
    # Construct the correct path relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, '..', 'results') 
    os.makedirs(results_dir, exist_ok=True) 
    
    # --- 8. Save Plot and Detailed History Data ---
    # Create filenames based on parameters
    param_str = f"eta{params['eta']:.3f}_lambda{params['lambda_decay']:.6f}_scale{params['scaling_target']:.1f}"
    plot_filename = f'sie_stability_sim_{param_str}.png'
    data_filename = f'sie_stability_data_{param_str}.npz'
    plot_save_path = os.path.join(results_dir, plot_filename) 
    data_save_path = os.path.join(results_dir, data_filename)

    plt.savefig(plot_save_path) 
    print(f"Saved simulation plot to {plot_save_path}")
    # plt.show() 

    history_data = {
        'reward': np.array(reward_history),
        'mod_factor': np.array(mod_factor_history),
        'weight_norm': np.array(weight_norm_history),
        'v_state_avg': np.array(v_state_history),
        'td_error': np.array(component_history['td']),
        'novelty': np.array(component_history['nov']),
        'habituation': np.array(component_history['hab']),
        'self_benefit': np.array(component_history['sb']),
        'params': params 
    }
    np.savez(data_save_path, **history_data)
    print(f"Saved detailed simulation data to {data_save_path}")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run SIE Stability Simulation.')
    parser.add_argument('--eta', type=float, default=ETA, help=f'Base STDP learning rate (default: {ETA})')
    parser.add_argument('--lambda_decay', type=float, default=LAMBDA, help=f'Weight decay coefficient (default: {LAMBDA})')
    parser.add_argument('--scaling_target', type=float, default=DEFAULT_SCALING_TARGET, help=f'Target sum for synaptic scaling (default: {DEFAULT_SCALING_TARGET})')
    
    args = parser.parse_args()

    simulation_params = {
        'eta': args.eta,
        'w_td': W_TD, 
        'w_novelty': W_NOVELTY,
        'w_habituation': W_HABITUATION,
        'w_self_benefit': W_SELF_BENEFIT,
        'lambda_decay': args.lambda_decay,
        'scaling_target': args.scaling_target 
    }
    run_simulation(simulation_params)
