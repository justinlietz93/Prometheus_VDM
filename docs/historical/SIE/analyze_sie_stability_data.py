"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a proprietary license. Use requires written
permission from Justin K. Lietz. See LICENSE file for full terms.

SIE Stability Analysis - Multi-objective reward integration validation
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys # Import sys for command-line args
import glob # Import glob for file matching
import argparse # Import argparse

def analyze_data(data_path):
    """Loads and analyzes the SIE stability simulation data."""
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    print(f"Loading data from {data_path}...")
    try:
        data = np.load(data_path, allow_pickle=True) # Allow pickle for params dict
    except Exception as e:
        print(f"Error loading data file: {e}")
        return

    print("Data loaded successfully. Keys:", list(data.keys()))

    # Extract data arrays
    reward = data['reward']
    mod_factor = data['mod_factor']
    weight_norm = data['weight_norm']
    v_state_avg = data['v_state_avg']
    td_error = data['td_error']
    novelty = data['novelty']
    habituation = data['habituation']
    self_benefit = data['self_benefit']
    params = data['params'].item() # Extract params dictionary

    print("\n--- Simulation Parameters ---")
    print(params)

    print("\n--- Stability Analysis ---")

    # 1. Reward Signal Analysis
    reward_mean = np.mean(reward)
    reward_std = np.std(reward)
    print(f"Total Reward: Mean={reward_mean:.4f}, StdDev={reward_std:.4f}")
    # Check for unbounded growth or extreme values
    if np.any(np.abs(reward) > 10): # Arbitrary threshold for "extreme"
        print("Warning: Potential instability detected - reward signal has extreme values.")
    elif reward_std > 1.0: # Arbitrary threshold for high variance
        print("Warning: High variance observed in reward signal.")
    else:
        print("Reward signal appears stable.")

    # 2. Modulation Factor Analysis
    mod_mean = np.mean(mod_factor)
    mod_std = np.std(mod_factor)
    print(f"Modulation Factor: Mean={mod_mean:.4f}, StdDev={mod_std:.4f}")
    # Should stay within [-1, 1] by definition of sigmoid, but check std dev
    if mod_std > 0.5: # Arbitrary threshold
         print("Warning: High variance observed in modulation factor.")
    else:
         print("Modulation factor appears stable.")


    # 3. Weight Norm Analysis
    print(f"Weight Norm: Start={weight_norm[0]:.4f}, End={weight_norm[-1]:.4f}")
    # Check for unbounded growth
    if weight_norm[-1] > weight_norm[0] * 5: # Arbitrary threshold for significant growth
        print("Warning: Significant weight growth observed. Check for potential unboundedness.")
    else:
        print("Weight norm growth appears bounded in this run.")
        
    # 4. V(state) Analysis
    print(f"Avg V(state): Start={v_state_avg[0]:.4f}, End={v_state_avg[-1]:.4f}")
    # Check for convergence
    final_std = np.std(v_state_avg[-1000:]) # Std dev over last 1000 steps
    print(f"Avg V(state) final 1000 steps: StdDev={final_std:.4f}")
    if final_std < 0.01: # Arbitrary threshold for convergence
        print("Average V(state) appears to have converged.")
    else:
        print("Average V(state) shows continued fluctuation.")

    # 5. Component Interaction Analysis (Example: Correlation)
    try:
        # Ensure arrays are not constant before calculating correlation
        if np.std(novelty) > 1e-6 and np.std(self_benefit) > 1e-6:
             corr_matrix = np.corrcoef(novelty, self_benefit)
             # Extract the correlation coefficient between the two variables
             corr_nov_sb = corr_matrix[0, 1] 
             print(f"Correlation(Novelty, Self-Benefit): {corr_nov_sb:.4f}")
             if corr_nov_sb < -0.5:
                 print("Note: Strong negative correlation between novelty and self-benefit observed, damping mechanism likely active.")
        else:
            print("Could not calculate novelty/self-benefit correlation: One or both variables have zero variance.")
            
    except Exception as e:
        print(f"Error calculating novelty/self-benefit correlation: {e}")

    # --- Further Analysis Ideas ---
    # - Plot distributions of reward components
    # - Analyze frequency spectrum of reward signal for oscillations
    # - Perform parameter sensitivity analysis by comparing runs with different params

    print("\nAnalysis complete.")
    # Returnmetrics for aggregation
    return {
        'params': params,
        'reward_mean': reward_mean,
        'reward_std': reward_std,
        'mod_factor_mean': mod_mean,
        'mod_factor_std': mod_std,
        'weight_norm_start': weight_norm[0],
        'weight_norm_end': weight_norm[-1],
        'v_state_converged': final_std < 0.01,
        'v_state_final_std': final_std
    }


def analyze_sweep_results(results_dir):
    """Loads data from multiple simulation runs and compares results."""
    data_files = sorted(glob.glob(os.path.join(results_dir, 'sie_stability_data_eta*_lambda*.npz')))
    
    if not data_files:
        print(f"No simulation data files found in {results_dir}")
        return

    print(f"Found {len(data_files)} simulation data files. Analyzing sweep...")
    
    sweep_summary = []
    for data_path in data_files:
        print(f"\n--- Analyzing: {os.path.basename(data_path)} ---")
        analysis_results = analyze_data(data_path)
        if analysis_results:
             sweep_summary.append(analysis_results)
             
    # Sort results by lambda_decay for clearer comparison
    # Sort results primarily by lambda_decay, then by eta for clearer comparison
    sweep_summary.sort(key=lambda x: (x['params']['lambda_decay'], x['params']['eta']))

    print("\n\n--- Parameter Sweep Summary ---")
    print("Lambda Decay | Eta   | Final ||W|| | Reward Mean | Reward Std | V(state) Converged | V(state) Final Std")
    print("------------|-------|-------------|-------------|------------|--------------------|-------------------")
    for result in sweep_summary:
        p = result['params']
        lam = p['lambda_decay']
        eta_val = p['eta'] # Get eta value
        final_norm = result['weight_norm_end']
        r_mean = result['reward_mean']
        r_std = result['reward_std']
        v_conv = result['v_state_converged']
        v_std = result['v_state_final_std']
        print(f"{lam:<12.6f} | {eta_val:<5.3f} | {final_norm:<11.4f} | {r_mean:<11.4f} | {r_std:<10.4f} | {str(v_conv):<18} | {v_std:<17.4f}")

    print("----------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze SIE Stability Simulation Data.')
    parser.add_argument('--sweep', action='store_true', help='Analyze all sweep results in the results directory.')
    parser.add_argument('--file', type=str, help='Analyze a specific data file.')

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, '..', 'results')

    if args.sweep:
        analyze_sweep_results(results_dir)
    elif args.file:
        analyze_data(args.file)
    else:
        # Default behavior: analyze the single default file if no flags are given
        default_data_path = os.path.join(results_dir, 'sie_stability_data.npz') # Default name if not using sweeps
        print("No specific file or --sweep flag provided. Analyzing default file.")
        analyze_data(default_data_path)
