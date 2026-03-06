"""
gauge.py - Gauge Boson Dynamics (CF-Aligned)

CF09 Implementation: Gauge Emergence via Berry Connection

This module implements gauge boson propagation as emergent phenomena from
the Berry connection of quantum states, replacing the heuristic "walkers"
with theoretically-derived gauge bosons.

Key Features:
- Gauge boson emission from Berry connection (CF09 Section 2)
- Propagation along gauge field lines (CF09 Section 3)
- Causal horizon dynamics (CF07 Section 4.2)
- Weinberg-Witten compatibility (CF09 Section 5)

Author: VDM Runtime v9 (CF-Aligned)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Optional, List, Tuple, Callable, Dict
from dataclasses import dataclass
import warnings

# Import CF-derived modules
from .gauge_emergence import (
    BerryConnection, GaugeBoson, FieldStrength,
    compute_berry_connection, compute_field_strength,
    propagate_gauge_boson, verify_weinberg_witten
)
from .measurement_theory import (
    compute_causal_horizon, CausalHorizon,
    measurement_event_at_horizon
)
from .void_equations import get_parameters

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class GaugeBosonEvent:
    """
    Gauge boson propagation event.
    
    CF09: Gauge bosons emerge from Berry connection and propagate
    along field lines, mediating interactions between nodes.
    """
    source: int
    target: int
    boson: GaugeBoson
    emission_time: int
    arrival_time: int
    distance: float = 0.0
    
    @property
    def hop_distance(self) -> int:
        """Graph hop distance"""
        return 1  # Simplified


@dataclass
class CausalHorizonState:
    """
    State of causal horizon for a node.
    
    CF07 Section 4.2: Decoherence occurs at causal horizon.
    """
    node_idx: int
    horizon: CausalHorizon
    enclosed_nodes: List[int]
    decoherence_complete: bool


# ---------------------------------------------------------------------------
# Gauge Boson Emitter
# ---------------------------------------------------------------------------

class GaugeBosonEmitter:
    """
    Emits gauge bosons from field dynamics.
    
    CF09 Section 2: Gauge bosons emerge from Berry connection
    when field velocity exceeds thermal threshold.
    """
    
    def __init__(
        self,
        berry_connection: BerryConnection,
        c_signal: float = 1.0
    ):
        """
        Initialize emitter.
        
        Args:
            berry_connection: Background gauge field
            c_signal: Signal propagation speed
        """
        self.berry_connection = berry_connection
        self.c_signal = c_signal
        self.emission_count = 0
    
    def thermal_velocity(self, kT: float) -> float:
        """
        Compute thermal velocity threshold.
        
        v_th = √(kT) (from equipartition)
        
        Args:
            kT: Temperature (in energy units)
            
        Returns:
            Thermal velocity threshold
        """
        return np.sqrt(max(kT, 1e-10))
    
    def emit_counts(
        self,
        phi_dot: NDArray[np.float64],
        kT: float
    ) -> NDArray[np.int32]:
        """
        Compute gauge boson emission counts from field velocity.
        
        CF09: Emission occurs when |φ̇| > v_th.
        
        Args:
            phi_dot: Field velocities
            kT: Temperature
            
        Returns:
            Emission counts per node
        """
        v_th = self.thermal_velocity(kT)
        counts = np.floor(np.abs(phi_dot) / v_th).astype(np.int32)
        return np.maximum(counts, 0)
    
    def emit_gauge_boson(
        self,
        source_idx: int,
        phi: float,
        phi_dot: float,
        kT: float
    ) -> Optional[GaugeBoson]:
        """
        Emit gauge boson from node.
        
        Args:
            source_idx: Source node index
            phi: Field value
            phi_dot: Field velocity
            kT: Temperature
            
        Returns:
            GaugeBoson if emitted, None otherwise
        """
        v_th = self.thermal_velocity(kT)
        
        if abs(phi_dot) < v_th:
            return None
        
        # Create gauge boson from Berry connection
        x = np.array([phi, phi_dot])
        A_mu = self.berry_connection.evaluate(x)
        
        # Field strength at source
        F = compute_field_strength(self.berry_connection, x)
        
        boson = GaugeBoson(
            A_mu=A_mu,
            mass=0.0,  # Massless (emergent gauge symmetry)
            polarization=self._compute_helicity(F),
            momentum=np.array([self.c_signal, phi_dot])
        )
        
        self.emission_count += 1
        
        return boson
    
    def _compute_helicity(self, field_strength: FieldStrength) -> int:
        """Compute helicity from field strength"""
        # Simplified: use electric field direction
        E = field_strength.electric_field
        if len(E) > 0:
            return 1 if np.sum(E) > 0 else -1
        return 1


# ---------------------------------------------------------------------------
# Gauge Boson Propagator
# ---------------------------------------------------------------------------

class GaugeBosonPropagator:
    """
    Propagates gauge bosons along field lines.
    
    CF09 Section 3: Gauge bosons follow geodesics of the gauge field.
    """
    
    def __init__(
        self,
        berry_connection: BerryConnection,
        node_positions: Optional[NDArray[np.float64]] = None
    ):
        """
        Initialize propagator.
        
        Args:
            berry_connection: Background gauge field
            node_positions: Spatial positions of nodes (optional)
        """
        self.berry_connection = berry_connection
        self.node_positions = node_positions
    
    def propagate(
        self,
        boson: GaugeBoson,
        source_idx: int,
        target_idx: int,
        dt: float
    ) -> GaugeBoson:
        """
        Propagate gauge boson from source to target.
        
        Args:
            boson: Gauge boson to propagate
            source_idx: Source node
            target_idx: Target node
            dt: Time step
            
        Returns:
            Propagated gauge boson
        """
        # Get field strength along path
        if self.node_positions is not None:
            x_mid = (self.node_positions[source_idx] + 
                     self.node_positions[target_idx]) / 2.0
        else:
            x_mid = np.array([0.5, 0.0])  # Default
        
        F = compute_field_strength(self.berry_connection, x_mid)
        
        # Update momentum (Lorentz force)
        # dp/dt = q F^μν p_ν (simplified)
        E = F.electric_field
        if len(E) > 0 and len(boson.momentum) >= len(E):
            force = np.zeros_like(boson.momentum)
            force[1:1+len(E)] = E
            new_momentum = boson.momentum + dt * force
        else:
            new_momentum = boson.momentum
        
        # Create propagated boson
        propagated = GaugeBoson(
            A_mu=boson.A_mu,
            mass=boson.mass,
            polarization=boson.polarization,
            momentum=new_momentum
        )
        
        return propagated
    
    def compute_trajectory(
        self,
        boson: GaugeBoson,
        x0: NDArray[np.float64],
        dt: float,
        n_steps: int
    ) -> List[NDArray[np.float64]]:
        """
        Compute gauge boson trajectory.
        
        Args:
            boson: Initial gauge boson
            x0: Initial position
            dt: Time step
            n_steps: Number of steps
            
        Returns:
            Trajectory points
        """
        trajectory = [x0.copy()]
        x = x0.copy()
        
        for _ in range(n_steps):
            # Follow gauge field line
            A = self.berry_connection.evaluate(x)
            x = x + dt * A[:len(x)]
            trajectory.append(x.copy())
        
        return trajectory


# ---------------------------------------------------------------------------
# Causal Horizon Manager
# ---------------------------------------------------------------------------

class CausalHorizonManager:
    """
    Manages causal horizons for measurement theory.
    
    CF07 Section 4.2: Decoherence occurs at causal horizon.
    """
    
    def __init__(
        self,
        c_signal: float,
        node_positions: Optional[NDArray[np.float64]] = None
    ):
        """
        Initialize horizon manager.
        
        Args:
            c_signal: Signal propagation speed
            node_positions: Node positions for distance computation
        """
        self.c_signal = c_signal
        self.node_positions = node_positions
        self.horizons: Dict[int, CausalHorizonState] = {}
    
    def compute_horizon(
        self,
        source_idx: int,
        v_threshold: float
    ) -> CausalHorizon:
        """
        Compute causal horizon for a node.
        
        h_causal = c_signal / v_th (CF07 Section 4.2)
        
        Args:
            source_idx: Source node index
            v_threshold: Velocity threshold
            
        Returns:
            CausalHorizon
        """
        if self.node_positions is not None:
            source_pos = self.node_positions[source_idx]
        else:
            source_pos = np.array([float(source_idx)])
        
        horizon = compute_causal_horizon(
            c_signal=self.c_signal,
            v_threshold=v_threshold,
            node_positions=self.node_positions,
            source_position=source_pos
        )
        
        return horizon
    
    def update_horizon(
        self,
        node_idx: int,
        kT: float,
        phi_dot: float
    ):
        """
        Update causal horizon for a node.
        
        Args:
            node_idx: Node index
            kT: Temperature
            phi_dot: Field velocity
        """
        v_th = np.sqrt(kT) if kT > 0 else 1e-10
        
        # Adjust threshold based on dynamics
        v_threshold = max(v_th, abs(phi_dot) * 0.1)
        
        horizon = self.compute_horizon(node_idx, v_threshold)
        
        self.horizons[node_idx] = CausalHorizonState(
            node_idx=node_idx,
            horizon=horizon,
            enclosed_nodes=horizon.enclosed_nodes,
            decoherence_complete=False
        )
    
    def get_enclosed_nodes(self, node_idx: int) -> List[int]:
        """Get nodes within causal horizon"""
        if node_idx in self.horizons:
            return self.horizons[node_idx].enclosed_nodes
        return []
    
    def check_decoherence(
        self,
        node_idx: int,
        tau_decoherence: float,
        m_gaps: int
    ) -> bool:
        """
        Check if decoherence is complete.
        
        Args:
            node_idx: Node index
            tau_decoherence: Decoherence time
            m_gaps: Time since last measurement
            
        Returns:
            True if decoherence complete
        """
        if tau_decoherence <= 0:
            return True
        
        decoherence_factor = np.exp(-m_gaps / tau_decoherence)
        return decoherence_factor < 0.01


# ---------------------------------------------------------------------------
# Main Gauge Dynamics Class
# ---------------------------------------------------------------------------

class GaugeDynamics:
    """
    Main class for gauge boson dynamics.
    
    Integrates emission, propagation, and causal horizon management.
    """
    
    def __init__(
        self,
        n_nodes: int,
        c_signal: float = 1.0,
        node_positions: Optional[NDArray[np.float64]] = None,
        eigenstate_func: Optional[Callable] = None
    ):
        """
        Initialize gauge dynamics.
        
        Args:
            n_nodes: Number of nodes
            c_signal: Signal propagation speed
            node_positions: Node positions
            eigenstate_func: Function to compute eigenstates for Berry connection
        """
        self.n_nodes = n_nodes
        self.c_signal = c_signal
        self.node_positions = node_positions
        
        # Create Berry connection from eigenstates if provided
        if eigenstate_func is not None and node_positions is not None:
            self.berry_connection = compute_berry_connection(
                eigenstate_func, node_positions
            )
        else:
            # Create dummy connection
            self.berry_connection = self._create_dummy_connection()
        
        # Sub-components
        self.emitter = GaugeBosonEmitter(self.berry_connection, c_signal)
        self.propagator = GaugeBosonPropagator(
            self.berry_connection, node_positions
        )
        self.horizon_manager = CausalHorizonManager(c_signal, node_positions)
        
        # Event tracking
        self.events: List[GaugeBosonEvent] = []
        self.time_step = 0
    
    def _create_dummy_connection(self) -> BerryConnection:
        """Create dummy Berry connection for initialization"""
        def dummy_A(x):
            return np.zeros(len(x)) if hasattr(x, '__len__') else np.zeros(2)
        
        return BerryConnection(
            A=dummy_A,
            coordinates=['phi', 'phi_dot'],
            n_dims=2
        )
    
    def update_berry_connection(
        self,
        eigenstate_func: Callable,
        coordinates: NDArray[np.float64]
    ):
        """
        Update Berry connection from new eigenstates.
        
        CF09: Gauge field emerges from quantum state geometry.
        
        Args:
            eigenstate_func: Function |ψ(x)⟩
            coordinates: Coordinate points
        """
        self.berry_connection = compute_berry_connection(
            eigenstate_func, coordinates
        )
        
        # Update sub-components
        self.emitter.berry_connection = self.berry_connection
        self.propagator.berry_connection = self.berry_connection
    
    def step(
        self,
        phi: NDArray[np.float64],
        phi_dot: NDArray[np.float64],
        kT: NDArray[np.float64],
        adjacency: List[List[int]],
        dt: float = 0.1
    ) -> List[GaugeBosonEvent]:
        """
        Single step of gauge dynamics.
        
        Args:
            phi: Field values
            phi_dot: Field velocities
            kT: Temperatures per node
            adjacency: Adjacency lists
            dt: Time step
            
        Returns:
            List of gauge boson events
        """
        events = []
        
        for i in range(self.n_nodes):
            # Update causal horizon
            self.horizon_manager.update_horizon(i, kT[i], phi_dot[i])
            
            # Emit gauge boson
            boson = self.emitter.emit_gauge_boson(
                i, phi[i], phi_dot[i], kT[i]
            )
            
            if boson is not None:
                # Propagate to neighbors
                for j in adjacency[i]:
                    propagated = self.propagator.propagate(
                        boson, i, j, dt
                    )
                    
                    event = GaugeBosonEvent(
                        source=i,
                        target=j,
                        boson=propagated,
                        emission_time=self.time_step,
                        arrival_time=self.time_step + 1,
                        distance=1.0  # Simplified
                    )
                    events.append(event)
        
        self.events = events
        self.time_step += 1
        
        return events
    
    def get_active_nodes(self) -> List[int]:
        """Get nodes involved in recent gauge boson events"""
        active = set()
        for event in self.events:
            active.add(event.source)
            active.add(event.target)
        return list(active)
    
    def verify_weinberg_witten(self) -> bool:
        """
        Verify Weinberg-Witten theorem compatibility.
        
        CF09 Section 5.1: Massless gauge bosons must have helicity ±1.
        """
        for event in self.events:
            if not verify_weinberg_witten(
                event.boson, event.boson.polarization
            ):
                return False
        return True
    
    def get_statistics(self) -> Dict:
        """Get statistics about gauge dynamics"""
        return {
            'emission_count': self.emitter.emission_count,
            'event_count': len(self.events),
            'active_nodes': len(self.get_active_nodes()),
            'horizons_defined': len(self.horizon_manager.horizons)
        }


# ---------------------------------------------------------------------------
# Legacy Interface
# ---------------------------------------------------------------------------

class WalkerEmitter:
    """
    Legacy walker emitter (for backward compatibility).
    
    Internally uses GaugeBosonEmitter with translation layer.
    """
    
    def __init__(self, c_signal: float = 1.0):
        self.c_signal = c_signal
        # Create internal gauge emitter
        from .gauge_emergence import BerryConnection
        
        def dummy_A(x):
            return np.zeros(len(x)) if hasattr(x, '__len__') else np.zeros(1)
        
        berry = BerryConnection(A=dummy_A, coordinates=['x'], n_dims=1)
        self._gauge_emitter = GaugeBosonEmitter(berry, c_signal)
    
    def thermal_velocity(self, kT: float) -> float:
        """Legacy interface"""
        return self._gauge_emitter.thermal_velocity(kT)
    
    def emit_counts(self, phi_dot: NDArray[np.float64], kT: float) -> NDArray[np.int32]:
        """Legacy interface"""
        return self._gauge_emitter.emit_counts(phi_dot, kT)


# Convenience function for legacy code
def thermal_velocity(kT: float) -> float:
    """Legacy convenience function"""
    return np.sqrt(max(kT, 1e-10))
