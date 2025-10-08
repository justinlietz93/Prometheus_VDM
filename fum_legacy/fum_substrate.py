# fum_substrate.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from scipy.sparse import csc_matrix, find

# FUM Modules
from fum_initialization import create_knn_graph

class Substrate:
    """
    Represents the FUM's computational medium or "Substrate".
    
    VERSION 3: This version is fully compliant with the FUM documentation for
    the ELIF neuron model and its associated homeostatic plasticity mechanisms.
    """
    def __init__(self, num_neurons: int, k: int):
        """
        Initializes the Substrate.

        Args:
            num_neurons (int): The number of Computational Units (CUs).
            k (int): The number of nearest neighbors for the initial k-NN graph.
        """
        self.num_neurons = num_neurons
        
        # --- Neuron Types (80% Excitatory, 20% Inhibitory) ---
        self.is_excitatory = np.random.choice([True, False], num_neurons, p=[0.8, 0.2])

        # --- CU parameters (vectorized) ---
        # As per docs, neuron params are heterogeneous, drawn from a normal distribution.
        self.tau_m = np.random.normal(loc=20.0, scale=np.sqrt(2.0), size=num_neurons)
        self.v_rest = np.full(num_neurons, -65.0)
        self.v_reset = np.full(num_neurons, -70.0) # Corrected to -70mV as per docs (A.4.ii)
        self.v_thresh = np.random.normal(loc=-55.0, scale=np.sqrt(2.0), size=num_neurons)
        self.refractory_period = np.full(num_neurons, 5.0)
        self.r_mem = np.full(num_neurons, 10.0) # Membrane resistance (Mohm)

        # --- Parameters for Intrinsic Plasticity (A.6) ---
        self.ip_target_rate_min = 0.1 # Hz
        self.ip_target_rate_max = 0.5 # Hz
        self.ip_v_thresh_adjustment = 0.1 # mV
        self.ip_tau_m_adjustment = 0.1 # ms
        self.ip_v_thresh_bounds = (-60.0, -50.0)
        self.ip_tau_m_bounds = (15.0, 25.0)

        # --- CU State variables (vectorized) ---
        self.v_m = np.full(num_neurons, self.v_rest)
        self.refractory_time = np.zeros(num_neurons)
        
        # --- UTE-specific attributes ---
        self.neuron_polarities = np.ones(num_neurons)  # Default polarity of 1
        self.refractory_periods = np.zeros(num_neurons)  # Current refractory periods for UTE
        
        # --- Synaptic Pathways: Subquadratic k-NN Initialization ---
        self.W = create_knn_graph(num_neurons, k, self.is_excitatory).tocsc()

        # --- Simulation state ---
        self.spikes = np.zeros(num_neurons, dtype=bool)
        self.spike_times = [[] for _ in range(num_neurons)]
        self.time_step = 0

    def run_step(self, external_currents, dt=1.0):
        """
        Runs one full, vectorized step of the Substrate's dynamics.
        """
        # Correctly apply membrane resistance only to synaptic currents inside the dv calculation
        synaptic_currents = self.W.dot(self.spikes.astype(np.float32))
        
        not_in_refractory = self.refractory_time <= 0
        
        # The full, correct ELIF update equation from the documentation
        dv = (
            -(self.v_m[not_in_refractory] - self.v_rest[not_in_refractory]) 
            + self.r_mem[not_in_refractory] * synaptic_currents[not_in_refractory] 
            + external_currents[not_in_refractory]
        ) / self.tau_m[not_in_refractory]
        
        self.v_m[not_in_refractory] += dv * dt
        
        self.refractory_time -= dt

        spiking_mask = self.v_m >= self.v_thresh
        self.spikes = spiking_mask
        
        self.v_m[spiking_mask] = self.v_reset[spiking_mask]
        self.refractory_time[spiking_mask] = self.refractory_period[spiking_mask]
        
        spiking_indices = np.where(spiking_mask)[0]
        current_time = self.time_step * dt
        for i in spiking_indices:
            self.spike_times[i].append(current_time)

        self.time_step += 1

    def apply_intrinsic_plasticity(self, window_ms=50, dt=1.0):
        """
        Applies intrinsic plasticity to neuron parameters based on their recent
        firing rate, as per documentation section A.6.
        """
        window_steps = int(window_ms / dt)
        analysis_start_time = max(0, (self.time_step - window_steps) * dt)
        window_duration_s = (self.time_step * dt - analysis_start_time) / 1000.0

        if window_duration_s == 0:
            return

        for i in range(self.num_neurons):
            spikes_in_window = [t for t in self.spike_times[i] if t >= analysis_start_time]
            rate_hz = len(spikes_in_window) / window_duration_s
            
            # Adjust v_thresh
            if rate_hz > self.ip_target_rate_max:
                self.v_thresh[i] += self.ip_v_thresh_adjustment
            elif rate_hz < self.ip_target_rate_min:
                self.v_thresh[i] -= self.ip_v_thresh_adjustment
                
            # Adjust tau_m
            if rate_hz > self.ip_target_rate_max:
                self.tau_m[i] -= self.ip_tau_m_adjustment
            elif rate_hz < self.ip_target_rate_min:
                self.tau_m[i] += self.ip_tau_m_adjustment

        # Clamp parameters to their bounds
        np.clip(self.v_thresh, self.ip_v_thresh_bounds[0], self.ip_v_thresh_bounds[1], out=self.v_thresh)
        np.clip(self.tau_m, self.ip_tau_m_bounds[0], self.ip_tau_m_bounds[1], out=self.tau_m)

    def apply_synaptic_scaling(self, target_sum=1.0):
        """
        Applies simple multiplicative scaling to incoming excitatory weights to
        keep the total input around a target value. Based on the reference
        validation script and documentation B.7.ii.
        """
        W_dense = self.W.toarray()
        
        # Calculate sum of incoming positive (excitatory) weights for each neuron
        incoming_exc_sums = np.sum(np.maximum(W_dense, 0), axis=0)
        
        # Avoid division by zero
        incoming_exc_sums[incoming_exc_sums < 1e-6] = 1.0
        
        # Calculate scaling factors needed to bring sum to target
        scale_factors = target_sum / incoming_exc_sums
        
        # Get a dense matrix of the excitatory weights only
        exc_W_dense = W_dense.copy()
        exc_W_dense[W_dense < 0] = 0
        
        # Apply scaling multiplicatively to the excitatory weights
        scaled_exc_W = exc_W_dense * scale_factors[np.newaxis, :]
        
        # Reconstruct the full weight matrix
        W_dense[W_dense > 0] = scaled_exc_W[W_dense > 0]
        
        self.W = csc_matrix(W_dense)
        self.W.prune()