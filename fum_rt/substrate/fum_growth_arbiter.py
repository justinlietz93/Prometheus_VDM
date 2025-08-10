# fum_growth_arbiter.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This module contains the GrowthArbiter, a class responsible for deciding
when and *how much* to grow the network. It implements the "super saturation" 
and "void debt" principles, where growth is triggered by stability and the 
amount of growth is determined by accumulated system pressure.
"""
import numpy as np
from collections import deque

class GrowthArbiter:
    """
    Monitors network metrics to decide when and how much to grow.
    """
    def __init__(self, stability_window=10, trend_threshold=0.001, debt_growth_factor=0.1):
        """
        Initializes the GrowthArbiter.

        Args:
            stability_window (int): Number of recent steps to check for stability.
            trend_threshold (float): Max change for a metric to be "flat."
            debt_growth_factor(float): Scales accumulated debt to number of neurons.
        """
        self.stability_window = stability_window
        self.trend_threshold = trend_threshold
        self.debt_growth_factor = debt_growth_factor

        self.weight_history = deque(maxlen=stability_window)
        self.synapse_history = deque(maxlen=stability_window)
        self.complexity_history = deque(maxlen=stability_window)
        self.cohesion_history = deque(maxlen=stability_window)
        
        self.is_stable = False
        self.void_debt_accumulator = 0.0

    def update_metrics(self, metrics):
        """
        Updates the historical metrics and checks for system stability.
        
        Args:
            metrics (dict): A dictionary containing the latest network metrics.
        """
        self.weight_history.append(metrics.get('avg_weight', 0))
        self.synapse_history.append(metrics.get('active_synapses', 0))
        self.complexity_history.append(metrics.get('total_b1_persistence', 0))
        self.cohesion_history.append(metrics.get('cluster_count', -1))

        if len(self.weight_history) < self.stability_window:
            self.is_stable = False
            return

        is_cohesive = all(count == 1 for count in self.cohesion_history)
        is_weight_flat = abs(self.weight_history[0] - self.weight_history[-1]) < self.trend_threshold
        is_synapse_flat = abs(self.synapse_history[0] - self.synapse_history[-1]) < 3
        is_complexity_flat = abs(self.complexity_history[0] - self.complexity_history[-1]) < self.trend_threshold

        if is_cohesive and is_weight_flat and is_synapse_flat and is_complexity_flat:
            if not self.is_stable:
                print("\n--- GROWTH ARBITER: System has achieved STABILITY ---")
                print("--- Now accumulating 'void debt' from residual valence. ---")
            self.is_stable = True
        else:
            if self.is_stable:
                print("\n--- GROWTH ARBITER: System has left stable state. Resetting debt.---")
                self.void_debt_accumulator = 0.0 # Reset debt if stability is lost
            self.is_stable = False

    def accumulate_and_check_growth(self, valence_signal):
        """
        If the system is stable, accumulates void debt. If the debt crosses
        a threshold, returns the number of neurons to grow.

        Args:
            valence_signal (float): The residual system pressure signal.

        Returns:
            int: The number of new neurons to add, or 0.
        """
        if not self.is_stable:
            return 0

        self.void_debt_accumulator += abs(valence_signal) # Accumulate pressure

        # Check if the accumulated debt triggers growth
        # We'll use a simple linear threshold for now.
        if self.void_debt_accumulator > 1.0: 
            num_new_neurons = int(np.ceil(self.void_debt_accumulator * self.debt_growth_factor))
            
            print("\n--- GROWTH ARBITER: VOID DEBT THRESHOLD REACHED ---")
            print(f"Accumulated Debt: {self.void_debt_accumulator:.3f}")
            print(f"Triggering organic growth of {num_new_neurons} new neuron(s).")
            print("---------------------------------------------------\n")

            self.void_debt_accumulator = 0.0 # Reset debt after triggering
            self.is_stable = False # System will become unstable after growth, reset
            self.clear_history() # Clear history to re-evaluate stability
            return num_new_neurons

        return 0

    def clear_history(self):
        """Resets all metric histories."""
        self.weight_history.clear()
        self.synapse_history.clear()
        self.complexity_history.clear()
        self.cohesion_history.clear()