"""
FUM Nexus - Universal I/O Interface

The Nexus is FUM's interface with the external world. It handles:
- Input encoding via UTE (Universal Temporal Encoder)
- Output decoding via UTD (Universal Transduction Decoder)  
- Coordination with persistent FUM components
- Pure I/O - NO internal processing or learning logic

This is what gets imported into benchmarks and applications.
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fum_legacy.fum_ute import encode_event
from fum_legacy.fum_utd import UTD

class FUM_Nexus:
    """
    Universal I/O interface for FUM. Pure coordination - no internal logic.
    
    The Nexus maintains references to persistent FUM components but does NOT
    implement their functionality. It only coordinates I/O between the world
    and FUM's internal systems.
    """
    
    def __init__(self, fum_core_system):
        """
        Initialize Nexus with a persistent FUM core system.
        
        Args:
            fum_core_system: Persistent FUM system with Substrate, SIE, etc.
        """
        self.fum_core = fum_core_system
        
        # Default I/O configuration
        self.ute_config = {
            'activation_duration_ms': 50,
            'target_frequency': 50.0,
            'refractory_period_ms': 5,
            'f_ref': 10.0,
            'scale_factor': 1.0
        }
        
        # Default UTD configuration
        utd_config = {
            'rate_decoding_window_ms': 100,
            'pattern_buffer_ms': 200,
            'pattern_to_macro_map': {}
        }
        
        # Default actuator mapping
        num_neurons = self.fum_core.substrate.num_neurons
        default_actuator_map = {
            i: {'group_name': f'output_group_{i//10}', 'actuator_type': 'continuous'}
            for i in range(num_neurons//10, num_neurons//5)
        }
        
        self.utd = UTD(utd_config, default_actuator_map)
        
    def configure_io(self, io_config: dict):
        """
        Configure I/O parameters without affecting persistent FUM state.
        
        Args:
            io_config: Dictionary with 'ute_config', 'utd_config', 'actuator_map'
        """
        if 'ute_config' in io_config:
            self.ute_config.update(io_config['ute_config'])
            
        if 'utd_config' in io_config:
            utd_config = io_config['utd_config']
            actuator_map = io_config.get('actuator_map', {})
            self.utd = UTD(utd_config, actuator_map)
            