# PROBLEMS IDENTIFIED:
# UTE Architecture:
# Missing advanced functions

import numpy as np
from scipy.sparse import lil_matrix
from fum_substrate import Substrate

def encode_event(
    substrate: Substrate,
    sensor_data: dict,
    activation_duration_ms: int,
    target_frequency: float,
    refractory_period_ms: int,
    f_ref: float,
    timestep: int,
    scale_factor: float = 1.0
) -> tuple[lil_matrix, dict]:
    """
    The central UTE. Converts a single structured event from a sensor
    into a segment of the Spatio-Temporal-Polarity-Phase Volume.
    This function is called sequentially by the Nexus for each event in a stream.
    """
    neuron_count = substrate.num_neurons
    spike_matrix = lil_matrix((neuron_count, activation_duration_ms), dtype=np.float32)
    spike_phases = {}

    # The group_id is now derived from the symbol itself.
    sensory_event_id = sensor_data['sensory_event_id']
    intensity = sensor_data.get('intensity', 1.0)
    
    # --- FUM Doctrine: The UTE is a Pure Transducer ---
    # The UTE does not use an engineered map. It deterministically assigns a
    # small, consistent block of input neurons based on the hash of the raw
    # sensory group ID. This is a physical reaction, not a conceptual mapping.
    num_input_neurons_per_event = 10 # A small, fixed number
    
    # --- Robust Hashing for Complex Stimuli ---
    # To handle both string-based and array-based stimuli, we ensure the ID is
    # converted to a stable, hashable format before use.
    if isinstance(sensory_event_id, np.ndarray):
        # For numpy arrays, convert the data buffer to bytes for hashing.
        hashable_id = sensory_event_id.tobytes()
    else:
        # For strings and other hashable types, use them directly.
        hashable_id = sensory_event_id
        
    start_index = (hash(hashable_id) % (neuron_count - num_input_neurons_per_event))
    neuron_indices = np.arange(start_index, start_index + num_input_neurons_per_event)

    substrate.neuron_polarities[neuron_indices] = sensor_data.get('polarity', 1)

    prob_per_ms = (target_frequency * intensity * scale_factor) / 1000.0
    current_refractory = substrate.refractory_periods[neuron_indices].copy()

    for t_local in range(activation_duration_ms):
        current_refractory -= 1
        can_fire_mask = (current_refractory <= 0)
        
        eligible_indices = neuron_indices[can_fire_mask]
        if len(eligible_indices) == 0:
            continue
            
        random_values = np.random.rand(len(eligible_indices))
        spiking_mask = random_values < prob_per_ms
        
        global_spiking_indices = eligible_indices[spiking_mask]

        if len(global_spiking_indices) > 0:
            global_time = timestep + t_local
            spike_matrix[global_spiking_indices, t_local] = 1.0
            
            # Map global indices back to their position in the `neuron_indices` array to update refractory periods
            slice_spiking_mask = np.isin(neuron_indices, global_spiking_indices)
            current_refractory[slice_spiking_mask] = refractory_period_ms
            
            # Calculate and store phase for spiking neurons
            phase = np.sin(2 * np.pi * f_ref * (global_time / 1000.0))
            for idx in global_spiking_indices:
                spike_phases[(idx, global_time)] = phase
                
    # Update the master refractory periods in the substrate
    substrate.refractory_periods[neuron_indices] = current_refractory

    return spike_matrix, spike_phases

def spatio_temporal_polarity_phase_encoding(
    substrate: Substrate,
    input_data: dict,
    activation_duration_ms: int,
    f_ref: float,
    timestep: int
) -> tuple[lil_matrix, dict]:
    """
    Advanced Blueprint function for full Spatio-Temporal-Polarity-Phase Volume encoding.
    
    Blueprint: "The UTE's output is enriched with a fourth dimension: Phase. This is
    accomplished by leveraging Phase-of-Firing Coding against a virtual reference oscillator."
    - FUM Blueprint, Rule 8.1
    
    This function implements the complete four-dimensional encoding:
    1. Spatial (Which neurons fire)
    2. Temporal (When and for how long)
    3. Polarity (The signal's direction)
    4. Phase (The signal's timing relative to a global clock)
    """
    neuron_count = substrate.num_neurons
    spike_matrix = lil_matrix((neuron_count, activation_duration_ms), dtype=np.float32)
    spike_phases = {}
    
    # Extract encoding parameters
    sensory_event_id = input_data['sensory_event_id']
    intensity = input_data.get('intensity', 1.0)
    polarity = input_data.get('polarity', 1)
    
    # Spatial dimension: deterministic neuron group mapping
    num_input_neurons_per_event = 10
    if isinstance(sensory_event_id, np.ndarray):
        hashable_id = sensory_event_id.tobytes()
    else:
        hashable_id = sensory_event_id
    start_index = (hash(hashable_id) % (neuron_count - num_input_neurons_per_event))
    neuron_indices = np.arange(start_index, start_index + num_input_neurons_per_event)
    
    # Polarity dimension: set neuron polarities
    substrate.neuron_polarities[neuron_indices] = polarity
    
    # Temporal and Phase dimensions: generate spikes with phase encoding
    target_frequency = 50.0  # Hz
    prob_per_ms = (target_frequency * intensity) / 1000.0
    
    for t_local in range(activation_duration_ms):
        global_time = timestep + t_local
        
        # Generate spikes using Poisson process
        random_values = np.random.rand(len(neuron_indices))
        spiking_mask = random_values < prob_per_ms
        spiking_indices = neuron_indices[spiking_mask]
        
        if len(spiking_indices) > 0:
            spike_matrix[spiking_indices, t_local] = 1.0
            
            # Phase dimension: calculate phase relative to virtual reference oscillator
            # Blueprint: "oscillator(t) = sin(2 * π * f_ref * t)"
            phase = np.sin(2 * np.pi * f_ref * (global_time / 1000.0))
            
            for idx in spiking_indices:
                spike_phases[(idx, global_time)] = phase
    
    return spike_matrix, spike_phases

def convert_to_spike_volume(
    spike_matrix: lil_matrix,
    spike_phases: dict,
    polarity_map: dict
) -> dict:
    """
    Converts spike matrix and phases into a complete Spatio-Temporal-Polarity-Phase Volume.
    
    Blueprint: "The output is not a simple spike train, but a 'Spatio-Temporal-Polarity-Phase Volume'
    —a signature of immense informational density."
    """
    volume = {
        'spatial': spike_matrix.nonzero(),  # Which neurons fired
        'temporal': spike_matrix,           # When they fired
        'polarity': polarity_map,          # Signal direction
        'phase': spike_phases              # Phase relative to reference oscillator
    }
    
    return volume

def phase_sensitive_encoding(
    base_spike_pattern: lil_matrix,
    f_ref: float,
    timestep: int,
    phase_sensitivity: float = 1.0
) -> tuple[lil_matrix, dict]:
    """
    Applies phase-sensitive modulation to existing spike patterns.
    
    Blueprint: "This gives the SNN core an extremely fine-grained 'clock' to use for
    pattern discrimination. Two spikes arriving with the same time difference Δt can
    have a different impact depending on whether they were 'in-phase' or 'out-of-phase'."
    """
    enhanced_spikes = base_spike_pattern.copy()
    spike_phases = {}
    
    # Find all spike locations
    spike_rows, spike_cols = base_spike_pattern.nonzero()
    
    for i, (row, col) in enumerate(zip(spike_rows, spike_cols)):
        global_time = timestep + col
        
        # Calculate phase relative to reference oscillator
        phase = np.sin(2 * np.pi * f_ref * (global_time / 1000.0))
        
        # Apply phase-sensitive modulation
        phase_modulation = (1 + np.cos(phase)) / 2  # Normalize to [0, 1]
        enhanced_spikes[row, col] *= (phase_sensitivity * phase_modulation)
        
        spike_phases[(row, global_time)] = phase
    
    return enhanced_spikes, spike_phases
