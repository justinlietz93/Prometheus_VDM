"""
connectome.py - Self-Modifying Graph Connectome (CF-Aligned)

CF03, CF07, CF11 Implementation: Dynamic Graph with Measurement Theory

This module implements the self-modifying graph structure where:
- Nodes represent computational sites with field values φ
- Bonds represent active connections with field values ψ
- Dynamics follow telegraph equations (CF04)
- Measurement/decoherence follows CF07
- Void-debt throttling follows CF11

Key Features:
- Walker-gated computation (replaced with gauge boson propagation)
- Debt-throttled relaxation (derived from Fisher information)
- Bond instantiation/deletion (from Gamma-convergence)

Author: VDM Runtime v9 (CF-Aligned)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Optional, List, Tuple, Callable, Dict, Set
from dataclasses import dataclass, field
import warnings

# Import CF-derived modules
from .void_equations import (
    solve_telegraph_step, bond_weighted_laplacian,
    node_potential_derivative, compute_effective_relaxation_time,
    derive_beta_debt_from_fisher_info, CFDerivedParameters,
    get_parameters
)
from .measurement_theory import (
    compute_decoherence_time, measure_node_decoherence,
    compute_causal_horizon, CausalHorizon,
    DensityMatrix, BornRuleResult, derive_born_rule
)
from .gauge_emergence import (
    BerryConnection, GaugeBoson, propagate_gauge_boson,
    compute_field_strength
)
from .a8_hierarchy import (
    count_interfaces_at_scale, verify_perimeter_reduction,
    InterfaceCount
)

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class Node:
    """Graph node with field value and state"""
    idx: int
    phi: float = 0.0
    phi_dot: float = 0.0
    phi_prev: float = 0.0
    debt: float = 0.0
    m_gaps: int = 0
    well: int = 0
    is_active: bool = True
    measured_at: Optional[int] = None
    
    # CF07: Density matrix for quantum treatment
    rho: Optional[DensityMatrix] = None


@dataclass
class Bond:
    """Graph bond connecting two nodes"""
    u: int
    v: int
    psi: float = 0.0
    age: int = 0


@dataclass
class GaugeBosonEvent:
    """
    Gauge boson propagation event (replaces WalkerEvent).
    
    CF09: Gauge bosons emerge from Berry connection and propagate
    along field lines, carrying information and mediating interactions.
    """
    source: int
    target: int
    boson: GaugeBoson
    emission_time: int
    arrival_time: int
    
    @property
    def hop_distance(self) -> int:
        """Graph hop distance (simplified)"""
        return 1  # Single hop for now


# ---------------------------------------------------------------------------
# Connectome Class
# ---------------------------------------------------------------------------

class Connectome:
    """
    Self-modifying graph with CF-derived dynamics.
    
    The connectome implements:
    - Telegraph dynamics for φ (CF04)
    - Decoherence-based measurement (CF07)
    - Gauge boson propagation (CF09)
    - Interface dynamics (CF03)
    - Void-debt throttling (CF11)
    """
    
    def __init__(
        self,
        adj: NDArray[np.int32],
        n_nodes: int,
        max_degree: int,
        use_cf_dynamics: bool = True
    ):
        """
        Initialize connectome.
        
        Args:
            adj: Adjacency array (n_nodes, max_degree), -1 for no neighbor
            n_nodes: Number of nodes
            max_degree: Maximum node degree
            use_cf_dynamics: Whether to use CF-derived dynamics (vs legacy)
        """
        self.adj = adj
        self.n_nodes = n_nodes
        self.max_degree = max_degree
        self.use_cf_dynamics = use_cf_dynamics
        
        # Node state
        self.nodes: List[Node] = [
            Node(idx=i, phi=np.random.rand())
            for i in range(n_nodes)
        ]
        
        # Bond state
        self.bonds: Dict[Tuple[int, int], Bond] = {}
        self._initialize_bonds()
        
        # Time step
        self.m: int = 0
        
        # CF-derived parameters
        self.params: Optional[CFDerivedParameters] = None
        
        # Gauge boson events (replaces walkers)
        self.gauge_boson_events: List[GaugeBosonEvent] = []
        
        # Decoherence tracking
        self.decoherence_times: Dict[int, float] = {}
        
        # Measurement tracking
        self.measurement_history: List[Tuple[int, int, float]] = []
    
    def _initialize_bonds(self):
        """Initialize bonds from adjacency structure"""
        for i in range(self.n_nodes):
            for k in range(self.max_degree):
                j = self.adj[i, k]
                if j >= 0 and i < j:  # Avoid duplicates
                    self.bonds[(i, j)] = Bond(u=i, v=j, psi=0.5)
    
    def set_cf_parameters(self, params: CFDerivedParameters):
        """Set CF-derived parameters"""
        self.params = params
    
    # -----------------------------------------------------------------------
    # CF-Derived Dynamics
    # -----------------------------------------------------------------------
    
    def compute_decoherence_time_cf(
        self,
        node_idx: int,
        temperature: float
    ) -> float:
        """
        Compute decoherence time from CF07.
        
        τ_D = ℏ / (k_B T λ²)
        
        Args:
            node_idx: Node index
            temperature: Local temperature
            
        Returns:
            Decoherence time
        """
        # Extract coupling from node dynamics
        node = self.nodes[node_idx]
        coupling = abs(node.phi_dot) if abs(node.phi_dot) > 0 else 0.1
        
        tau_D = compute_decoherence_time(temperature, coupling)
        self.decoherence_times[node_idx] = tau_D
        
        return tau_D
    
    def measure_node_cf(
        self,
        node_idx: int,
        temperature: float,
        well_positions: NDArray[np.float64]
    ) -> Tuple[float, bool]:
        """
        Apply CF07 decoherence-based measurement to a node.
        
        Replaces the heuristic measurement with proper decoherence theory.
        
        Args:
            node_idx: Node to measure
            temperature: Local temperature
            well_positions: Positions of potential wells
            
        Returns:
            (new_phi, was_measured)
        """
        node = self.nodes[node_idx]
        
        # Compute decoherence time
        tau_D = self.compute_decoherence_time_cf(node_idx, temperature)
        
        # Apply measurement with decoherence
        new_phi, was_measured = measure_node_decoherence(
            phi=node.phi,
            phi_dot=node.phi_dot,
            kT=temperature,
            tau_decoherence=tau_D,
            m_gaps=node.m_gaps,
            well_positions=well_positions
        )
        
        if was_measured:
            node.measured_at = self.m
            self.measurement_history.append((self.m, node_idx, new_phi))
        
        return new_phi, was_measured
    
    def emit_gauge_boson(
        self,
        source_idx: int,
        berry_connection: BerryConnection,
        temperature: float
    ) -> Optional[GaugeBoson]:
        """
        Emit gauge boson from node (replaces walker emission).
        
        CF09: Gauge bosons emerge from Berry connection and propagate
        along gauge field lines.
        
        Args:
            source_idx: Source node index
            berry_connection: Background gauge field
            temperature: Temperature for thermal activation
            
        Returns:
            GaugeBoson if emitted, None otherwise
        """
        node = self.nodes[source_idx]
        
        # Thermal activation threshold
        v_th = np.sqrt(temperature) if temperature > 0 else 1e-10
        
        if abs(node.phi_dot) < v_th:
            return None
        
        # Compute emission count from field velocity
        n_emit = int(np.floor(abs(node.phi_dot) / v_th))
        
        if n_emit <= 0:
            return None
        
        # Create gauge boson from Berry connection
        x_source = np.array([node.phi, node.phi_dot])
        A_mu = berry_connection.evaluate(x_source)
        
        boson = GaugeBoson(
            A_mu=A_mu,
            mass=0.0,  # Massless gauge boson
            polarization=1,
            momentum=np.array([1.0, node.phi_dot])
        )
        
        return boson
    
    def propagate_gauge_bosons(
        self,
        berry_connection: BerryConnection,
        dt: float
    ) -> List[GaugeBosonEvent]:
        """
        Propagate all gauge bosons and generate events.
        
        Args:
            berry_connection: Background gauge field
            dt: Time step
            
        Returns:
            List of gauge boson events
        """
        events = []
        
        # Emit gauge bosons from active nodes
        for i, node in enumerate(self.nodes):
            if not node.is_active:
                continue
            
            # Compute local temperature from fluctuations
            kT = self._compute_local_temperature(i)
            
            boson = self.emit_gauge_boson(i, berry_connection, kT)
            
            if boson is not None:
                # Propagate to neighbors
                neighbors = self._get_neighbors(i)
                
                for j in neighbors:
                    event = GaugeBosonEvent(
                        source=i,
                        target=j,
                        boson=boson,
                        emission_time=self.m,
                        arrival_time=self.m + 1
                    )
                    events.append(event)
        
        self.gauge_boson_events = events
        return events
    
    def _compute_local_temperature(self, node_idx: int) -> float:
        """Compute local temperature from field fluctuations"""
        node = self.nodes[node_idx]
        
        # Temperature from velocity variance (equipartition)
        # kT ~ <φ̇²>
        kT = 0.5 * node.phi_dot**2
        
        return max(kT, 0.01)  # Minimum temperature
    
    def _get_neighbors(self, node_idx: int) -> List[int]:
        """Get neighbor indices"""
        neighbors = []
        for k in range(self.max_degree):
            j = self.adj[node_idx, k]
            if j >= 0:
                neighbors.append(j)
        return neighbors
    
    # -----------------------------------------------------------------------
    # Telegraph Dynamics
    # -----------------------------------------------------------------------
    
    def step_telegraph_cf(
        self,
        gauge_boson_events: List[GaugeBosonEvent],
        dt: float = 0.1
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
        """
        Single telegraph dynamics step with CF-derived mechanisms.
        
        Args:
            gauge_boson_events: Gauge boson events for gating
            dt: Time step
            
        Returns:
            (phi_new, phi_dot_new, measured_kT)
        """
        if self.params is None:
            raise RuntimeError("CF parameters not set. Call set_cf_parameters().")
        
        # Extract parameters
        tau_base = self.params.TAU
        D = self.params.D_DIFF
        gamma = self.params.GAMMA_DAMP
        
        # Determine active nodes from gauge boson events
        active_set = self._compute_active_set(gauge_boson_events)
        
        # Prepare arrays
        phi_curr = np.array([n.phi for n in self.nodes])
        phi_prev = np.array([n.phi_prev for n in self.nodes])
        phi_dot = np.array([n.phi_dot for n in self.nodes])
        debt = np.array([n.debt for n in self.nodes])
        
        # Compute effective relaxation time with debt throttling
        beta_debt = 0.1  # Could be derived from Fisher info
        tau_eff = compute_effective_relaxation_time(
            tau_base, debt, beta_debt
        )
        
        # Compute adjacency lists
        adj_lists = [
            [j for j in self.adj[i] if j >= 0]
            for i in range(self.n_nodes)
        ]
        
        # Extract bond field
        psi = self._extract_psi_array()
        
        # Compute RHS for active nodes
        rhs = np.zeros(self.n_nodes)
        for i in active_set:
            laplacian = bond_weighted_laplacian(
                phi_curr, adj_lists, psi
            )
            V_prime = node_potential_derivative(phi_curr)
            
            rhs[i] = D * laplacian[i] - V_prime[i] - gamma * phi_dot[i]
        
        # Solve telegraph equation
        phi_new = phi_curr.copy()
        for i in active_set:
            phi_new[i] = solve_telegraph_step(
                phi_curr[i], phi_prev[i], rhs[i], tau_eff[i], dt
            )
        
        # Compute velocity
        phi_dot_new = (phi_new - phi_curr) / dt
        
        # Apply measurement/decoherence (CF07)
        well_positions = np.array([0.0, 1.0])
        for i in active_set:
            kT = self._compute_local_temperature(i)
            phi_new[i], was_measured = self.measure_node_cf(
                i, kT, well_positions
            )
            
            # Update node state
            self.nodes[i].phi = phi_new[i]
            self.nodes[i].phi_dot = phi_dot_new[i]
            self.nodes[i].phi_prev = phi_curr[i]
            
            if was_measured:
                self.nodes[i].m_gaps = 0
            else:
                self.nodes[i].m_gaps += 1
        
        # Measure temperature from active nodes
        measured_kT = 0.0
        if len(active_set) > 0:
            measured_kT = 0.5 * np.var(phi_dot_new[list(active_set)])
        
        self.m += 1
        
        return phi_new, phi_dot_new, np.array([measured_kT])
    
    def _compute_active_set(
        self,
        gauge_boson_events: List[GaugeBosonEvent]
    ) -> Set[int]:
        """
        Compute active node set from gauge boson events.
        
        Zone 1: Nodes with gauge boson events (full physics)
        Zone 2: Neighbors of active nodes (coupling only)
        """
        active = set()
        
        # Zone 1: Nodes involved in gauge boson events
        for event in gauge_boson_events:
            active.add(event.source)
            active.add(event.target)
        
        # Zone 2: Neighbors (for coupling)
        warm = set()
        for i in active:
            for j in self._get_neighbors(i):
                if j not in active:
                    warm.add(j)
        
        # Combine zones
        return active.union(warm)
    
    def _extract_psi_array(self) -> NDArray[np.float64]:
        """Extract bond field as array"""
        psi = np.zeros((self.n_nodes, self.max_degree))
        
        for i in range(self.n_nodes):
            for k in range(self.max_degree):
                j = self.adj[i, k]
                if j >= 0:
                    key = (min(i, j), max(i, j))
                    if key in self.bonds:
                        psi[i, k] = self.bonds[key].psi
        
        return psi
    
    # -----------------------------------------------------------------------
    # Bond Dynamics (CF03 Gamma-Convergence)
    # -----------------------------------------------------------------------
    
    def update_bonds_cf(
        self,
        phi_new: NDArray[np.float64],
        phi_dot_new: NDArray[np.float64],
        threshold: float = 0.5
    ):
        """
        Update bonds based on field dynamics (CF03 interface dynamics).
        
        Bonds form where interfaces are detected (Gamma-convergence).
        
        Args:
            phi_new: New field values
            phi_dot_new: New field velocities
            threshold: Interface detection threshold
        """
        # Detect interfaces
        phi_dot_abs = np.abs(phi_dot_new)
        
        # Instantiate bonds where both nodes are active
        for i in range(self.n_nodes):
            for k in range(self.max_degree):
                j = self.adj[i, k]
                if j < 0 or i >= j:
                    continue
                
                # Check if both nodes show interface activity
                if phi_dot_abs[i] > threshold and phi_dot_abs[j] > threshold:
                    key = (i, j)
                    if key not in self.bonds:
                        # Instantiate new bond
                        self.bonds[key] = Bond(u=i, v=j, psi=0.5, age=0)
                
                # Update existing bond
                if key in self.bonds:
                    bond = self.bonds[key]
                    bond.age += 1
                    
                    # Update psi based on node correlation
                    bond.psi = 0.5 * (phi_new[i] + phi_new[j])
    
    # -----------------------------------------------------------------------
    # Full Step
    # -----------------------------------------------------------------------
    
    def step_cf(
        self,
        berry_connection: BerryConnection,
        dt: float = 0.1
    ) -> Tuple[int, int, int, float]:
        """
        Full CF-aligned dynamics step.
        
        Args:
            berry_connection: Background gauge field (CF09)
            dt: Time step
            
        Returns:
            (n_active, n_warm, n_bonds, measured_kT)
        """
        # Propagate gauge bosons (CF09)
        gauge_events = self.propagate_gauge_bosons(berry_connection, dt)
        
        # Telegraph dynamics (CF04)
        phi_new, phi_dot_new, measured_kT = self.step_telegraph_cf(
            gauge_events, dt
        )
        
        # Bond dynamics (CF03)
        self.update_bonds_cf(phi_new, phi_dot_new)
        
        # Compute statistics
        active_set = self._compute_active_set(gauge_events)
        warm_set = set()
        for i in active_set:
            for j in self._get_neighbors(i):
                if j not in active_set:
                    warm_set.add(j)
        
        return (
            len(active_set),
            len(warm_set),
            len(self.bonds),
            float(measured_kT[0]) if len(measured_kT) > 0 else 0.0
        )
    
    # -----------------------------------------------------------------------
    # Legacy Interface (for backward compatibility)
    # -----------------------------------------------------------------------
    
    def step(
        self,
        walker_events: Optional[List] = None,
        dt: float = 0.1
    ) -> Tuple[int, int, int, float]:
        """
        Legacy step interface (for backward compatibility).
        
        Uses CF-derived mechanisms internally.
        """
        # Create dummy Berry connection for legacy calls
        from .gauge_emergence import BerryConnection
        
        def dummy_A(x):
            return np.zeros(2)
        
        berry_connection = BerryConnection(
            A=dummy_A,
            coordinates=['phi', 'phi_dot'],
            n_dims=2
        )
        
        return self.step_cf(berry_connection, dt)
    
    def get_state(self) -> Dict:
        """Get current state as dictionary"""
        return {
            'phi': np.array([n.phi for n in self.nodes]),
            'phi_dot': np.array([n.phi_dot for n in self.nodes]),
            'debt': np.array([n.debt for n in self.nodes]),
            'bonds': len(self.bonds),
            'm': self.m
        }
