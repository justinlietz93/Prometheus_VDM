# fum_runtime_analysis.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np

class RuntimeAnalysis:
    """
    Calculates metrics related to the quality and dynamics of the SNN's
    spike-based response to a specific, recent stimulus.
    """
    def __init__(self, stimulus_duration_ms: int, num_input_neurons: int):
        """
        Args:
            stimulus_duration_ms: The time window (in ms) over which the 
                                  stimulus was presented.
            num_input_neurons: The number of neurons that receive the direct
                               stimulus pattern.
        """
        self.stimulus_duration = stimulus_duration_ms
        self.input_neuron_indices = np.arange(num_input_neurons)

    def analyze_response(self, spike_times: list[list[float]], total_neurons: int, current_sim_time: float):
        """
        Analyzes the spike trains generated in response to a stimulus.

        Args:
            spike_times: A list of lists, where spike_times[i] are the spike 
                         times for neuron i.
            total_neurons: The total number of neurons in the substrate.
            current_sim_time: The simulation time at the end of the stimulus
                              presentation.

        Returns:
            A dictionary of runtime metrics.
        """
        response_window_start = current_sim_time - self.stimulus_duration
        
        # Identify spikes that occurred *during* the last stimulus presentation
        responding_neurons = []
        response_spike_times = []
        all_response_spikes = 0
        
        for i in range(total_neurons):
            neuron_spikes_in_window = [t for t in spike_times[i] if response_window_start <= t < current_sim_time]
            if neuron_spikes_in_window:
                responding_neurons.append(i)
                response_spike_times.extend(neuron_spikes_in_window)
                all_response_spikes += len(neuron_spikes_in_window)

        if not response_spike_times:
            return {
                "Response Latency (ms)": -1,
                "Temporal Coherence (std)": -1,
                "Response SNR": 0
            }

        # --- Metric Calculations ---
        
        # 1. Latency: Time of the first spike in the response window
        first_spike_time = np.min(response_spike_times)
        latency = first_spike_time - response_window_start
        
        # 2. Temporal Coherence: Std dev of spike times
        temporal_coherence_std = np.std(response_spike_times)

        # 3. Selectivity (SNR)
        # Signal: Spikes from neurons that were SUPPOSED to fire (the input neurons)
        # Noise: Spikes from all other neurons
        signal_spikes = sum(1 for i in responding_neurons if i in self.input_neuron_indices)
        noise_spikes = all_response_spikes - signal_spikes
        
        snr = signal_spikes / noise_spikes if noise_spikes > 0 else float('inf')

        return {
            "Response Latency (ms)": f"{latency:.2f}",
            "Temporal Coherence (std)": f"{temporal_coherence_std:.4f}",
            "Response SNR": f"{snr:.4f}"
        }

    def calculate_spike_rate_variance(self, spike_times: list[list[float]], window_duration_ms: float, total_neurons: int, current_sim_time: float):
        """
        Calculates the variance of firing rates across the entire population.

        Args:
            spike_times: A list of lists of spike times.
            window_duration_ms: The duration of the analysis window in ms.
            total_neurons: The total number of neurons.
            current_sim_time: The current simulation time.

        Returns:
            The variance of the spike rates in Hz.
        """
        analysis_window_start = current_sim_time - window_duration_ms
        window_duration_s = window_duration_ms / 1000.0

        spike_rates_hz = []
        for i in range(total_neurons):
            spikes_in_window = [t for t in spike_times[i] if analysis_window_start <= t < current_sim_time]
            rate = len(spikes_in_window) / window_duration_s
            spike_rates_hz.append(rate)
        
        rate_variance = np.var(spike_rates_hz)
        return rate_variance