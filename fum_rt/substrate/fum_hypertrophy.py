# fum_hypertrophy.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This module handles the growth of the FUM substrate, including the addition
of new computational units (neurons) and the formation of their initial
connections based on void dynamics.
"""
import numpy as np
import torch
from scipy.sparse import csc_matrix

from FUM_Void_Equations import universal_void_dynamics

class Hypertrophy:
    """
    Manages the growth of the Substrate's connectome.
    """
    def __init__(self, seed=42):
        """
        Initializes the growth manager.
        """
        self.rng = np.random.default_rng(seed=seed)

    def grow(self, substrate, num_new_neurons):
        """
        Grows the substrate by expanding the connectome and all associated state arrays.
        This method is designed to be called on a Substrate instance.

        Args:
            substrate: The Substrate instance to modify.
            num_new_neurons (int): The number of new neurons to add.
        """
        if num_new_neurons <= 0:
            return

        old_n = substrate.num_neurons
        new_n = old_n + num_new_neurons
        
        print(f"\n--- HYPERTROPHY: SUBSTRATE GROWTH ---")
        print(f"Adding {num_new_neurons} new neurons to the existing {old_n}.")

        # --- Create new neuron properties on CPU first ---
        new_is_excitatory = self.rng.choice([True, False], num_new_neurons, p=[0.8, 0.2])
        new_tau_m = self.rng.normal(loc=20.0, scale=np.sqrt(2.0), size=num_new_neurons)
        new_v_thresh = self.rng.normal(loc=-55.0, scale=np.sqrt(2.0), size=num_new_neurons)
        new_v_rest = np.full(num_new_neurons, -65.0)
        new_refractory_period = np.full(num_new_neurons, 5.0)
        new_r_mem = np.full(num_new_neurons, 10.0)

        # --- Expand the connectome based on the backend ---
        if substrate.device_type == 'gpu':
            W_cpu = substrate.W.cpu().numpy()
        else:
            W_cpu = substrate.W.toarray() if isinstance(substrate.W, csc_matrix) else substrate.W

        new_W = np.zeros((new_n, new_n))
        new_W[:old_n, :old_n] = W_cpu

        # --- Connect new neurons using Void Dynamics ---
        # 1. Create a potential connection matrix for new neurons (outgoing)
        potential_connections_out = self.rng.random((num_new_neurons, old_n)) * 0.05 
        # 2. Evolve it with void dynamics
        delta_out = universal_void_dynamics(potential_connections_out, substrate.time_step)
        evolved_connections_out = potential_connections_out + delta_out
        # 3. Threshold to form actual connections
        new_connections_out = np.where(evolved_connections_out > 0.01, evolved_connections_out, 0)
        
        # 1. Create a potential connection matrix for new neurons (incoming)
        potential_connections_in = self.rng.random((old_n, num_new_neurons)) * 0.05
        # 2. Evolve it
        delta_in = universal_void_dynamics(potential_connections_in, substrate.time_step)
        evolved_connections_in = potential_connections_in + delta_in
        # 3. Threshold
        new_connections_in = np.where(evolved_connections_in > 0.01, evolved_connections_in, 0)

        # Add new connections to the main matrix
        new_W[old_n:new_n, :old_n] = new_connections_out
        new_W[:old_n, old_n:new_n] = new_connections_in
        
        # --- Handle backend-specific state expansions ---
        if substrate.device_type == 'gpu':
            substrate.W = torch.from_numpy(new_W).float().to(substrate.device)
            substrate.is_excitatory = torch.cat([substrate.is_excitatory, torch.from_numpy(new_is_excitatory).to(substrate.device)])
            substrate.tau_m = torch.cat([substrate.tau_m, torch.from_numpy(new_tau_m).float().to(substrate.device)])
            substrate.v_thresh = torch.cat([substrate.v_thresh, torch.from_numpy(new_v_thresh).float().to(substrate.device)])
            substrate.v_m = torch.cat([substrate.v_m, torch.from_numpy(new_v_rest).float().to(substrate.device)])
            substrate.refractory_time = torch.cat([substrate.refractory_time, torch.zeros(num_new_neurons, device=substrate.device)])
            substrate.refractory_period = torch.cat([substrate.refractory_period, torch.from_numpy(new_refractory_period).float().to(substrate.device)])
            substrate.r_mem = torch.cat([substrate.r_mem, torch.from_numpy(new_r_mem).float().to(substrate.device)])
            substrate.v_reset_tensor = torch.cat([substrate.v_reset_tensor, torch.from_numpy(np.full(num_new_neurons, -70.0)).float().to(substrate.device)])
            substrate.spikes = torch.cat([substrate.spikes, torch.zeros(num_new_neurons, dtype=torch.bool, device=substrate.device)])
        else: # CPU
            substrate.W = csc_matrix(new_W)
            substrate.is_excitatory = np.concatenate([substrate.is_excitatory, new_is_excitatory])
            substrate.tau_m = np.concatenate([substrate.tau_m, new_tau_m])
            substrate.v_thresh = np.concatenate([substrate.v_thresh, new_v_thresh])
            substrate.v_m = np.concatenate([substrate.v_m, new_v_rest])
            substrate.refractory_time = np.concatenate([substrate.refractory_time, np.zeros(num_new_neurons)])
            substrate.refractory_period = np.concatenate([substrate.refractory_period, new_refractory_period])
            substrate.r_mem = np.concatenate([substrate.r_mem, new_r_mem])
            substrate.v_reset = np.concatenate([substrate.v_reset, np.full(num_new_neurons, -70.0)])
            substrate.spikes = np.concatenate([substrate.spikes, np.zeros(num_new_neurons, dtype=bool)])
            substrate.neuron_polarities = np.concatenate([substrate.neuron_polarities, np.ones(num_new_neurons)])
            substrate.refractory_periods = np.concatenate([substrate.refractory_periods, np.zeros(num_new_neurons)])

        # Universal state expansions
        substrate.spike_times.extend([[] for _ in range(num_new_neurons)])
        substrate.num_neurons = new_n

        print(f"Growth complete. Total neurons: {substrate.num_neurons}")
        print("-------------------------------------\n")