# fum_v1_main.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import os
import sys
import time
# Ensure the parent directory is in the Python path to find FUM_Visualizer_Module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from tqdm import tqdm

# --- FUM V2 Core Components (Final Refactored & Renamed Versions) ---
from fum_substrate import Substrate
from fum_stimulus import StimulusGenerator
from fum_ute import encode_event
from FUM_Void_Equations import get_universal_constants
from fum_sie import SelfImprovementEngine
from fum_ehtp import Introspection_Probe_Module
from fum_analysis import FUM_Analysis
from fum_data_curation import DataCuration
from fum_runtime_analysis import RuntimeAnalysis
from FUM_AdvancedMath.fum.apply_revgsp import apply_revgsp_updates # Corrected import
from fum_structural_homeostasis import perform_structural_homeostasis
from fum_validated_math import calculate_modulation_factor # Corrected import
from logger import Logger
from FUM_Visualizer_Module.fum_visualizer import (
    plot_network_graph,
    void_driven_layout,
    plot_3d_network_graph,
    export_connectome_json,
    export_connectome_npz,
)
from fum_hypertrophy import Hypertrophy
from fum_growth_arbiter import GrowthArbiter

# --- Parameters for Phase 1: Random Seed Sprinkling ---
NUM_NEURONS = 1000 # Neurons in the connectome terrain. Sparsity increases with scale
K_NEAREST_NEIGHBORS = 8 # 
NUM_STIMULI_TO_PRESENT = 1000 # Raw ASCII data stimuli, higher != better
PATTERN_DURATION = 30 # ms
UTE_TARGET_FREQUENCY = 50.0 # Hz

RUN_ID = f"phase1_FUM_Demo_run_{int(time.time())}"
RESULTS_DIR = os.path.join("FUM_Demo_runs", RUN_ID)

# Hyperparameters for Valence-Gated Synaptic Plasticity (VGSP)
ETA = 0.01 # Base learning rate
LAMBDA_DECAY = 0.001 # Weight decay term, CRITICAL for stability
STIMULUS_SCALING_FACTOR = 0.1 # CRITICAL for preventing hyperactivity from external input
 
VGSP_PARAMS = {
    'A_plus': 0.05, 'A_minus': 0.06, 'tau_plus': 20.0, 'tau_minus': 20.0,
}

def main():
    """
    Main orchestrator for Phase 1: Random Seed Sprinkling.
    This script guides the initial self-assembly of the FUM's UKG.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    log_path = os.path.join(RESULTS_DIR, "03_FUM_Demo_run_log.txt")
    logger = Logger(log_path)
    sys.stdout = logger

    try:
        print(f"--- FUM - PHASE 1: RANDOM SEED SPRINKLING ---")
        print(f"--- Run ID: {RUN_ID} ---")

        # 1. Initialize all FUM components with correct nomenclature
        substrate = Substrate(num_neurons=NUM_NEURONS, k=K_NEAREST_NEIGHBORS)
        stimulus_generator = StimulusGenerator()
        num_input_neurons = int(NUM_NEURONS * 0.25)
        sie = SelfImprovementEngine(num_neurons=NUM_NEURONS)
        introspection_probe_analyzer = Introspection_Probe_Module()
        runtime_analyzer = RuntimeAnalysis(PATTERN_DURATION, num_input_neurons) # <-- NEW
        analysis_module = FUM_Analysis(RESULTS_DIR, RUN_ID)
        hypertrophy = Hypertrophy()
        growth_arbiter = GrowthArbiter()

        # Generate a 2D layout for visualization based on the initial state
        print("Generating initial network layout...")
        pos = void_driven_layout(substrate.W, dim=2)
        
        # Visualization now takes the sparse matrix directly, along with the time and position args
        plot_network_graph(substrate.W, 0, "Initial k-NN Substrate", os.path.join(RESULTS_DIR, "00_FUM_Demo_initial_connectome.png"), pos)

        # --- Initial Network Validation ---
        # As per the Phase 1 documentation, verify initial network properties.
        initial_sparsity = 1.0 - (substrate.W.nnz / (NUM_NEURONS * NUM_NEURONS))
        avg_weight_magnitude = np.mean(np.abs(substrate.W.data))
        
        e_ratio = np.sum(substrate.is_excitatory) / NUM_NEURONS
        i_ratio = 1.0 - e_ratio
        logger.log_metrics({
            "Initial Sparsity": f"{initial_sparsity:.4f} (Target: >0.95)",
            "Avg. Weight Magnitude": f"{avg_weight_magnitude:.4f} (Target: ~0.15)",
            "E/I Ratio": f"{e_ratio:.2f} E / {i_ratio:.2f} I (Target: 0.80/0.20)",
            "Tau_m (mean)": f"{np.mean(substrate.tau_m):.2f} (Target: 20.0)",
            "Tau_m (std)": f"{np.std(substrate.tau_m):.2f} (Target: {np.sqrt(2.0):.2f})",
            "V_thresh (mean)": f"{np.mean(substrate.v_thresh):.2f} (Target: -55.0)",
            "V_thresh (std)": f"{np.std(substrate.v_thresh):.2f} (Target: {np.sqrt(2.0):.2f})",
        }, "INITIAL NETWORK VALIDATION")

        # --- SIE Placeholder Validation ---
        # Verify that the Phase 2+ components are initialized correctly.
        sie_init_metrics = {
            "Plasticity Impulse (PI) Buffer Shape": sie.cret_buffer.shape,
            "Plasticity Impulse (PI) Buffer Sum": np.sum(sie.cret_buffer),
            "TD Value Function Shape": sie.td_value_function.shape,
            "TD Value Function Sum": np.sum(sie.td_value_function)
        }
        logger.log_metrics(sie_init_metrics, "SIE PLACEHOLDER VALIDATION")

        # --- Input Dataset Validation ---
        # As per the Phase 1 documentation, generate the full dataset first,
        # then analyze it for coverage, diversity, and complexity.
        print("\nGenerating and validating the full input dataset...")
        full_dataset = [stimulus_generator.get_random_stimulus() for _ in range(NUM_STIMULI_TO_PRESENT)]
        
        curation_module = DataCuration()
        dataset_metrics = curation_module.analyze_dataset(full_dataset)
        logger.log_metrics(dataset_metrics, "INPUT DATASET VALIDATION")

        start_time = time.time()

        # 2. Begin the "Sprinkling" Loop
        print(f"\nPresenting {NUM_STIMULI_TO_PRESENT} diverse, validated stimuli to guide self-organization...")
        for i, (stim_type, stimulus) in enumerate(tqdm(full_dataset, desc="Phase 1 Progress")):
            # Use the new functional UTE
            sensor_data = {'sensory_event_id': stimulus, 'intensity': 1.0}
            void_constants = get_universal_constants()
            
            spike_matrix, _ = encode_event(
                substrate=substrate,
                sensor_data=sensor_data,
                activation_duration_ms=PATTERN_DURATION,
                target_frequency=UTE_TARGET_FREQUENCY,
                refractory_period_ms=int(np.mean(substrate.refractory_period)),
                f_ref=void_constants['F_REF'],
                timestep=substrate.time_step,
                scale_factor=STIMULUS_SCALING_FACTOR
            )

            # Present the pattern to the Substrate over time (fast CSC column iteration + buffer reuse)
            spike_matrix_csc = spike_matrix.tocsc()
            external_currents = np.zeros(substrate.num_neurons, dtype=float)
            for t in range(spike_matrix_csc.shape[1]):
                start = spike_matrix_csc.indptr[t]
                end = spike_matrix_csc.indptr[t + 1]
                idx = spike_matrix_csc.indices[start:end]
                data = spike_matrix_csc.data[start:end]
                # zero and scatter-add the active inputs
                external_currents.fill(0.0)
                external_currents[idx] = data
                substrate.run_step(external_currents)
            
            # The SIE calculates the complete, final valence signal for learning
            # (calculate_modulation_factor is already applied inside SIE)
            valence_signal = sie.update_and_calculate_valence(substrate.W, 0.0, substrate.time_step)
            
            # Apply the blueprint-compliant RE-VGSP update rule
            substrate.W, vgsp_metrics = apply_revgsp_updates(
                W=substrate.W,
                spike_times=substrate.spike_times,
                time_step=substrate.time_step,
                eta=ETA,
                mod_factor=valence_signal, # Pass the final valence signal
                lambda_decay=LAMBDA_DECAY,
                params=VGSP_PARAMS,
                is_excitatory=substrate.is_excitatory
            )

            # --- Runtime Analysis moved to periodic block for speed ---

            # Periodically perform analysis and homeostasis
            if (i + 1) % 10 == 0:
                print(f"\n--- Analysis at Stimulus {i+1} ---")
                
                # Calculate spike rate variance over the last 10 stimuli
                analysis_window_ms = 10 * PATTERN_DURATION
                rate_variance = runtime_analyzer.calculate_spike_rate_variance(
                    substrate.spike_times, analysis_window_ms, substrate.num_neurons, substrate.time_step
                )
                stability_metrics = {
                    "Spike Rate Variance (Hz)": f"{rate_variance:.4f} (Target: <0.1)"
                }

                introspection_probe_metrics = introspection_probe_analyzer.perform_introspection_probe_analysis(substrate.W)
                
                # Add metrics needed by the Growth Arbiter
                # Compute average absolute weight directly from current W (robust for sparse or dense)
                try:
                    avg_weight = float(np.mean(np.abs(substrate.W.data)))  # scipy.sparse CSR/CSC: nonzero entries
                except Exception:
                    avg_weight = float(np.mean(np.abs(np.asarray(substrate.W))))  # dense fallback
                introspection_probe_metrics['avg_weight'] = avg_weight
                # Active synapses count: use nnz when available, otherwise fallback to count_nonzero
                introspection_probe_metrics['active_synapses'] = int(substrate.W.nnz) if hasattr(substrate.W, "nnz") else int(np.count_nonzero(substrate.W))

                logger.log_metrics({'valence_signal': valence_signal}, f"SIE METRICS - STIMULUS {i+1}")
                logger.log_metrics(runtime_metrics, f"RUNTIME METRICS - STIMULUS {i+1}")
                logger.log_metrics(stability_metrics, f"STABILITY METRICS - STIMULUS {i+1}")
                logger.log_metrics(vgsp_metrics, f"VGSP METRICS - STIMULUS {i+1}")
                logger.log_metrics(introspection_probe_metrics, f"EHTP METRICS - STIMULUS {i+1}")
                
                # Perform Structural Homeostasis on the sparse matrix `W`
                substrate.W = perform_structural_homeostasis(substrate.W, introspection_probe_metrics)

                # --- Organic Growth based on Void Debt ---
                growth_arbiter.update_metrics(introspection_probe_metrics)
                num_to_grow = growth_arbiter.accumulate_and_check_growth(valence_signal)
                if num_to_grow > 0:
                    hypertrophy.grow(substrate, num_to_grow)
                    # After growth, we must resize SIE buffers to match new neuron count
                    sie.resize_buffers(substrate.num_neurons)
                
                # Apply Intrinsic Plasticity to stabilize firing rates (as per docs A.6)
                substrate.apply_intrinsic_plasticity(window_ms=50)

                # Apply Synaptic Scaling to normalize inputs (as per docs B.7.ii)
                # This is done less frequently.
                if (i + 1) % 30 == 0: # Approx. every 900-1000 steps
                    substrate.apply_synaptic_scaling()
                    print(f"--- Applied Synaptic Scaling at Stimulus {i+1} ---")


                # Record data for the end-of-run dashboard
                analysis_module.record_episode_data(i + 1, substrate.W, introspection_probe_metrics)

        end_time = time.time()
        print("\n--- PHASE 1 COMPLETE ---")
        logger.log_metrics({
            "Total Time (s)": f"{end_time - start_time:.2f}",
            "Stimuli Presented": NUM_STIMULI_TO_PRESENT
        }, "PHASE 1 SUMMARY")

        # 3. Save the final, foundational UKG
        print("\nGenerating final network visualization...")
        # Note: We reuse the initial 'pos' for layout consistency, showing how connectivity changes over the same substrate
        plot_network_graph(
            substrate.W,
            len(full_dataset),
            "Foundational UKG Structure",
            os.path.join(RESULTS_DIR, "01_FUM_Demo_final_connectome.png"),
            pos
        )

        # 3b. Save interactive 3D visualization and export connectome for front-end use
        pos3 = void_driven_layout(substrate.W, dim=3)
        plot_3d_network_graph(
            substrate.W,
            len(full_dataset),
            "Foundational UKG Structure (3D)",
            os.path.join(RESULTS_DIR, "01_FUM_Demo_final_connectome_3d.png"),
            pos3
        )

        # Export machine-readable connectome artifacts
        export_connectome_json(
            substrate.W,
            pos,
            os.path.join(RESULTS_DIR, "02_FUM_connectome.json"),
            threshold=0.0
        )
        export_connectome_npz(
            substrate.W,
            os.path.join(RESULTS_DIR, "02_FUM_connectome.npz")
        )
        
        # 4. Generate the final performance dashboard
        analysis_module.create_dashboard()

        print(f"\nAll results saved to {RESULTS_DIR}")

    finally:
        sys.stdout = logger.terminal
        logger.close()

if __name__ == "__main__":
    main()