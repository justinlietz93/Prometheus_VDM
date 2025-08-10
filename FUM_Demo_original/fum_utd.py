import torch
from collections import deque
import hashlib

class UTD:
    """
    Implements the Universal Transduction Decoder (UTD) as specified in the FUM Blueprint.

    Blueprint Rule 8.2: The Universal Transduction Decoder (UTD)
    "The UTD is the FUM's output mechanism, the direct inverse of the UTE. It translates
    the spike patterns from designated output neuron groups into actionable, deterministic
    commands for the various actuator modules. This translation process is a two-stage
    parallel operation, providing the sophisticated control signals required by the
    actuator suite."

    "The SNN's entire learning objective is to discover, via the RE-VGSP/SIE loop,
    the correct internal spike patterns that will, when decoded by the UTD, produce
    goal-achieving actions."

    This class is the final, non-learning translation layer that takes the abstract,
    internal "thoughts" of the SNN (the spike patterns) and turns them into concrete,
    physical actions in the world.
    """

    def __init__(self, config: dict, actuator_map: dict):
        """
        Initializes the UTD.

        Args:
            config (dict): A dictionary containing UTD configuration parameters.
            actuator_map (dict): A dictionary mapping output neuron groups to specific actuators.
        """
        # --- Blueprint Adherence: Key Parameters & State Variables ---
        # "rate_decoding_window_ms: An integer defining the sliding window size for continuous rate decoding."
        self.rate_decoding_window_ms = config['rate_decoding_window_ms']
        
        # "pattern_buffer_ms: An integer defining the time window for capturing a complete spatio-temporal pattern for hierarchical decoding."
        self.pattern_buffer_ms = config['pattern_buffer_ms']
        
        # "pattern_to_macro_map: A static hash map (loaded from config) that maps a unique hash of a spike pattern to a sequence of actuator commands."
        self.pattern_to_macro_map = config['pattern_to_macro_map']
        
        self.actuator_map = actuator_map
        self.output_neuron_groups = self._invert_actuator_map(actuator_map)

        # Buffers for storing recent spikes for both decoding stages
        self.rate_spike_buffer = {group: deque() for group in self.output_neuron_groups}
        self.pattern_spike_buffer = {group: deque() for group in self.output_neuron_groups}
        
    def _invert_actuator_map(self, actuator_map):
        """Helper to create a mapping from group name to neuron indices."""
        groups = {}
        for neuron_idx, mapping in actuator_map.items():
            group_name = mapping.get('group_name')
            if group_name:
                if group_name not in groups:
                    groups[group_name] = []
                groups[group_name].append(neuron_idx)
        return groups

    def process_spikes(self, new_spikes: list[tuple[int, int]], current_time_ms: int) -> list[dict]:
        """
        Processes a new batch of spikes from output neurons and generates actuator commands.

        Args:
            new_spikes (list[tuple[int, int]]): A list of (neuron_idx, spike_time_ms) tuples.
            current_time_ms (int): The current simulation time in milliseconds.

        Returns:
            list[dict]: A list of commands for the actuator modules.
        """
        self._update_buffers(new_spikes, current_time_ms)
        
        commands = []
        
        # --- Stage 1: Rate-Based Continuous Control ---
        rate_commands = self._decode_rate(current_time_ms)
        if rate_commands:
            commands.extend(rate_commands)

        # --- Stage 2: Hierarchical Pattern Expansion ---
        pattern_commands = self._decode_pattern(current_time_ms)
        if pattern_commands:
            commands.extend(pattern_commands)
            
        return commands

    def _update_buffers(self, new_spikes: list[tuple[int, int]], current_time_ms: int):
        """Adds new spikes to the internal buffers and prunes old spikes."""
        # Find which group each spike belongs to and add to buffers
        neuron_to_group = {neuron: group for group, neurons in self.output_neuron_groups.items() for neuron in neurons}
        
        for neuron_idx, spike_time in new_spikes:
            group = neuron_to_group.get(neuron_idx)
            if group:
                self.rate_spike_buffer[group].append(spike_time)
                self.pattern_spike_buffer[group].append((neuron_idx, spike_time))

        # Prune old spikes from buffers
        rate_cutoff = current_time_ms - self.rate_decoding_window_ms
        for group in self.rate_spike_buffer:
            while self.rate_spike_buffer[group] and self.rate_spike_buffer[group][0] < rate_cutoff:
                self.rate_spike_buffer[group].popleft()

        pattern_cutoff = current_time_ms - self.pattern_buffer_ms
        for group in self.pattern_spike_buffer:
            while self.pattern_spike_buffer[group] and self.pattern_spike_buffer[group][0][1] < pattern_cutoff:
                self.pattern_spike_buffer[group].popleft()

    def _decode_rate(self, current_time_ms: int) -> list[dict]:
        """
        --- Blueprint Rule 8.2, Stage 1: Rate-Based Continuous Control ---
        "For actuators requiring smooth, continuous input (e.g., motor velocity, speech
        synthesizer pitch), the UTD calculates a time-averaged firing rate for each
        designated output neuron group over a sliding window. This provides a continuous,
        analog-like signal from the discrete spike trains."
        """
        commands = []
        window_duration_s = self.rate_decoding_window_ms / 1000.0
        
        for group_name, spikes in self.rate_spike_buffer.items():
            # Formula: firing_rate = spike_count(window) / window_duration_s
            spike_count = len(spikes)
            firing_rate = spike_count / window_duration_s if window_duration_s > 0 else 0.0
            
            # This assumes a mapping from group_name to a continuous-control actuator
            # The specific actuator and parameter would be defined in the actuator_map config
            # For simplicity, we create a generic command here.
            commands.append({
                'type': 'continuous',
                'actuator_group': group_name,
                'value': firing_rate
            })
        return commands

    def _decode_pattern(self, current_time_ms: int) -> list[dict]:
        """
        --- Blueprint Rule 8.2, Stage 2: Hierarchical Pattern Expansion ---
        "For actuators requiring symbolic or macro-level commands (e.g., outputting a
        complete word or code block), the UTD uses a deterministic, hash-based lookup.
        A specific, complex spatio-temporal pattern of spikes from a designated group
        acts as a 'key.' The UTD maps this key to a pre-defined sequence of basic
        actuator commands (a 'macro'), which are then executed in order."
        """
        commands = []
        for group_name, pattern_buffer in self.pattern_spike_buffer.items():
            if not pattern_buffer:
                continue

            # This trigger logic is an example; a real implementation might trigger
            # on pattern completion or other cues. Here, we check periodically.
            if current_time_ms % self.pattern_buffer_ms == 0:
                # Normalize spike times relative to the window start
                window_start_time = pattern_buffer[0][1]
                normalized_pattern = sorted([(n, t - window_start_time) for n, t in pattern_buffer])

                # Formula: macro_id = pattern_to_macro_map[hash(spike_pattern_buffer)]
                pattern_str = "".join(f"{n},{t}" for n, t in normalized_pattern)
                pattern_hash = hashlib.sha256(pattern_str.encode()).hexdigest()

                macro_sequence = self.pattern_to_macro_map.get(pattern_hash)
                
                # --- Blueprint Adherence: Edge Case Handling ---
                # "If a spike pattern does not match any key in the pattern_to_macro_map,
                # no action is taken. This is expected behavior, as the SNN must learn
                # to produce valid patterns."
                if macro_sequence:
                    commands.append({
                        'type': 'hierarchical',
                        'actuator_group': group_name,
                        'macro': macro_sequence
                    })
                    # Clear buffer after successful decoding to not re-trigger
                    self.pattern_spike_buffer[group_name].clear()
        
        return commands