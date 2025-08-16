# fum_rt/core/substrate/substrate.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
import torch
from scipy.sparse import csc_matrix, find

# FUM Modules
from fum_initialization import create_knn_graph

class Substrate:
    """
    Represents the FUM's computational medium or "Substrate".
    
    VERSION 4 (MERGED): This version combines the stable V3 architecture with
    the GPU acceleration and Growth features from the V9 refactor.
    """
    def __init__(self, num_neurons: int, k: int, device: str = 'auto'):
        """
        Initializes the Substrate.

        Args:
            num_neurons (int): The number of Computational Units (CUs).
            k (int): The number of nearest neighbors for the initial k-NN graph.
            device (str): 'auto', 'gpu', or 'cpu'.
        """
        self.num_neurons = num_neurons
        self._setup_device(device)
        self.backend = np if self.device_type == 'cpu' else torch
        
        # --- Neuron Types (80% Excitatory, 20% Inhibitory) ---
        self.rng = np.random.default_rng(seed=42)
        is_excitatory_np = self.rng.choice([True, False], num_neurons, p=[0.8, 0.2])

        # --- CU parameters (vectorized, created on CPU first) ---
        tau_m_np = self.rng.normal(loc=20.0, scale=np.sqrt(2.0), size=num_neurons)
        self.v_rest = np.full(num_neurons, -65.0)
        v_reset_np = np.full(num_neurons, -70.0)
        v_thresh_np = self.rng.normal(loc=-55.0, scale=np.sqrt(2.0), size=num_neurons)
        refractory_period_np = np.full(num_neurons, 5.0)
        r_mem_np = np.full(num_neurons, 10.0)

        # --- Parameters for Intrinsic Plasticity (A.6) ---
        self.ip_target_rate_min = 0.1 # Hz
        self.ip_target_rate_max = 0.5 # Hz
        self.ip_v_thresh_adjustment = 0.1 # mV
        self.ip_tau_m_adjustment = 0.1 # ms
        self.ip_v_thresh_bounds = (-60.0, -50.0)
        self.ip_tau_m_bounds = (15.0, 25.0)
        
        # --- Synaptic Pathways: k-NN Initialization (on CPU first) ---
        W_np = create_knn_graph(num_neurons, k, is_excitatory_np).toarray()
        
        # --- Create state vars and move to GPU if requested ---
        if self.device_type == 'gpu':
            self.is_excitatory = torch.from_numpy(is_excitatory_np).to(self.device)
            self.tau_m = torch.from_numpy(tau_m_np).float().to(self.device)
            self.v_thresh = torch.from_numpy(v_thresh_np).float().to(self.device)
            self.v_m = torch.from_numpy(self.v_rest).float().to(self.device)
            self.refractory_time = torch.zeros(num_neurons, device=self.device)
            self.refractory_period = torch.from_numpy(refractory_period_np).float().to(self.device)
            self.r_mem = torch.from_numpy(r_mem_np).float().to(self.device)
            self.v_reset_tensor = torch.from_numpy(v_reset_np).float().to(self.device)
            self.spikes = torch.zeros(num_neurons, dtype=torch.bool, device=self.device)
            self.W = torch.from_numpy(W_np).float().to(self.device)
        else: # cpu
            self.is_excitatory = is_excitatory_np
            self.tau_m = tau_m_np
            self.v_reset = v_reset_np
            self.v_thresh = v_thresh_np
            self.refractory_period = refractory_period_np
            self.r_mem = r_mem_np
            self.v_m = np.full(num_neurons, self.v_rest)
            self.refractory_time = np.zeros(num_neurons)
            self.neuron_polarities = np.ones(num_neurons)
            self.refractory_periods = np.zeros(num_neurons)
            self.W = csc_matrix(W_np)
            self.spikes = np.zeros(num_neurons, dtype=bool)
        self.spike_times = [[] for _ in range(num_neurons)]
        self.time_step = 0

    def run_step(self, external_currents, dt=1.0):
        """
        Runs one full step of the Substrate's dynamics, dispatching to the correct backend.
        """
        if self.device_type == 'gpu':
            self._run_step_gpu(external_currents, dt)
        else:
            self._run_step_cpu(external_currents, dt)
        
        self.time_step += 1

    def _run_step_cpu(self, external_currents, dt):
        """
        Runs one full, vectorized step of the Substrate's dynamics on the CPU.
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

    def _run_step_gpu(self, external_currents, dt):
        """
        Runs one full, vectorized step of the Substrate's dynamics on the GPU.
        """
        external_currents_gpu = torch.from_numpy(external_currents).float().to(self.device)
        synaptic_currents = torch.mv(self.W, self.spikes.float())
        
        not_in_refractory = self.refractory_time <= 0
        v_rest_gpu = torch.from_numpy(self.v_rest).float().to(self.device)
        
        dv = (-(self.v_m[not_in_refractory] - v_rest_gpu[not_in_refractory]) + self.r_mem[not_in_refractory] * synaptic_currents[not_in_refractory] + external_currents_gpu[not_in_refractory]) / self.tau_m[not_in_refractory]
        self.v_m[not_in_refractory] += dv * dt
        
        self.refractory_time -= dt
        self.refractory_time.clamp_(min=0)
        
        spiking_mask = self.v_m >= self.v_thresh
        self.spikes = spiking_mask
        
        self.v_m[spiking_mask] = self.v_reset_tensor[spiking_mask]
        self.refractory_time[spiking_mask] = self.refractory_period[spiking_mask]
        
        spiking_indices = torch.where(spiking_mask)[0].cpu().numpy()
        current_time = self.time_step * dt
        for i in spiking_indices:
            self.spike_times[i].append(current_time)

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

    def _setup_device(self, device_preference):
        if device_preference == 'gpu':
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
                self.device_type = 'gpu'
                print("--- Substrate configured to run on GPU. ---")
            else:
                print("Warning: GPU requested but not available. Falling back to CPU.")
                self.device = torch.device("cpu")
                self.device_type = 'cpu'
        elif device_preference == 'cpu':
            self.device = torch.device("cpu")
            self.device_type = 'cpu'
            print("--- Substrate configured to run on CPU. ---")
        else: # auto
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
                self.device_type = 'gpu'
                print("--- Substrate configured to run on GPU. ---")
            else:
                self.device = torch.device("cpu")
                self.device_type = 'cpu'
                print("--- Substrate configured to run on CPU. ---")