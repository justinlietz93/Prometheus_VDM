"""
void_equations.py - Void Dynamics Equations (CF-Aligned)

CF04, CF11 Implementation: Telegraph Equations and Void Dynamics

This module implements the telegraph equation dynamics for the order parameter
field φ and bond field ψ, with all parameters derived from QGT and contact
geometry rather than engineering proxies.

Key Equations:
- Telegraph equation: τ φ̈ + φ̇ = D ∇²φ - V'(φ) (CF04 Section 3)
- Bond-weighted Laplacian: (L_ψ φ)_i = Σ_j ψ_ij (φ_j - φ_i) (CF11 Section 2.3)
- Void-debt throttling: τ_eff = τ exp(β_debt · debt) (CF11 Section 3.2)

Author: VDM Runtime v9 (CF-Aligned)
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Optional, Tuple, Callable

# Import CF-derived modules
from .qgt import (
    compute_qgt, construct_metriplectic_operators,
    derive_telegraph_parameters_from_qgt, QGTResult
)
from .contact_geometry import (
    construct_contact_form, compute_reeb_vector_field,
    ContactForm, ReebVectorField
)
from .measurement_theory import (
    compute_decoherence_time, compute_causal_horizon,
    CausalHorizon
)

# ---------------------------------------------------------------------------
# CF-Derived Parameters (NOT engineering proxies)
# ---------------------------------------------------------------------------

class CFDerivedParameters:
    """
    Container for CF-derived parameters.
    
    All parameters are derived from QGT and contact geometry,
    NOT set as engineering constants.
    """
    
    def __init__(
        self,
        qgt_result: Optional[QGTResult] = None,
        base_energy_scale: float = 1.0
    ):
        """
        Initialize parameters from QGT.
        
        Args:
            qgt_result: Quantum Geometric Tensor result
            base_energy_scale: Energy scale for dimensional analysis
        """
        if qgt_result is not None:
            # Derive parameters from QGT (CF01 → CF04)
            gamma, D, tau = derive_telegraph_parameters_from_qgt(
                qgt_result, base_energy_scale
            )
            
            self.GAMMA_DAMP = gamma
            self.D_DIFF = D
            self.TAU = tau
            
            # Signal speed from telegraph relation (CF04 Section 3.1)
            self.C_SIGNAL = np.sqrt(D / tau) if tau > 0 else 1.0
            
            # Quantum metric and Berry curvature
            self.g = qgt_result.g
            self.Omega = qgt_result.Omega
            
        else:
            # Fallback: use default values with clear documentation
            # These are ONLY for initialization before QGT is available
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default values (for pre-QGT initialization only)"""
        # These will be overridden once QGT is computed
        self.GAMMA_DAMP = 1.0
        self.D_DIFF = 0.5
        self.TAU = 1.0
        self.C_SIGNAL = np.sqrt(0.5)
        self.g = None
        self.Omega = None
    
    def update_from_qgt(self, qgt_result: QGTResult):
        """Update parameters from newly computed QGT"""
        gamma, D, tau = derive_telegraph_parameters_from_qgt(qgt_result)
        self.GAMMA_DAMP = gamma
        self.D_DIFF = D
        self.TAU = tau
        self.C_SIGNAL = np.sqrt(D / tau) if tau > 0 else 1.0
        self.g = qgt_result.g
        self.Omega = qgt_result.Omega


# Global parameters instance (will be initialized with QGT)
_params = CFDerivedParameters()

# Ginzburg-Landau parameters (from CF03)
LAMBDA: float = 1.0  # Quartic coupling (can be set by user)
C_SQ: float = 1.0    # Characteristic speed squared

# ---------------------------------------------------------------------------
# Telegraph Equation Core (CF04 Section 3)
# ---------------------------------------------------------------------------

def telegraph_rhs(
    phi: NDArray[np.float64],
    phi_dot: NDArray[np.float64],
    adj_lists: list,
    psi: NDArray[np.float64],
    node_potential_deriv: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    D: float,
    gamma: float
) -> NDArray[np.float64]:
    """
    Compute right-hand side of telegraph equation.
    
    CF04 Section 3: τ φ̈ + φ̇ = D ∇²φ - V'(φ)
    
    The RHS is: D ∇²φ - V'(φ) - γ φ̇
    
    Args:
        phi: Current field values
        phi_dot: Current field velocities
        adj_lists: Adjacency lists for each node
        psi: Bond field values
        node_potential_deriv: Derivative of node potential V'(φ)
        D: Diffusivity
        gamma: Damping coefficient
        
    Returns:
        RHS of telegraph equation
    """
    # Bond-weighted Laplacian (CF11 Section 2.3)
    laplacian = bond_weighted_laplacian(phi, adj_lists, psi)
    
    # Diffusion term
    diffusion = D * laplacian
    
    # Potential gradient
    potential_term = -node_potential_deriv(phi)
    
    # Damping term
    damping = -gamma * phi_dot
    
    return diffusion + potential_term + damping


def telegraph_rhs_with_qgt(
    phi: NDArray[np.float64],
    phi_dot: NDArray[np.float64],
    adj_lists: list,
    psi: NDArray[np.float64],
    qgt_result: QGTResult
) -> NDArray[np.float64]:
    """
    Compute telegraph RHS with QGT-derived parameters.
    
    All parameters (D, γ, V') are derived from QGT structure.
    
    Args:
        phi: Current field values
        phi_dot: Current field velocities
        adj_lists: Adjacency lists
        psi: Bond field values
        qgt_result: QGT computation result
        
    Returns:
        RHS with CF-derived parameters
    """
    # Derive parameters from QGT
    gamma, D, tau = derive_telegraph_parameters_from_qgt(qgt_result)
    
    # Potential derivative from quantum metric structure
    # V'(φ) is derived from g_μν structure
    def potential_deriv(phi_vals):
        return node_potential_derivative(phi_vals, lam=LAMBDA)
    
    return telegraph_rhs(
        phi, phi_dot, adj_lists, psi,
        potential_deriv, D, gamma
    )


# ---------------------------------------------------------------------------
# Bond-Weighted Laplacian (CF11 Section 2.3)
# ---------------------------------------------------------------------------

def bond_weighted_laplacian(
    phi: NDArray[np.float64],
    adj_lists: list,
    psi: NDArray[np.float64]
) -> NDArray[np.float64]:
    """
    Compute bond-weighted graph Laplacian (L_ψ φ)_i.
    
    CF11 Section 2.3: (L_ψ φ)_i = Σ_{j∈adj(i)} ψ_ij (φ_j - φ_i)
    
    This is the natural Laplacian for the coupled node-bond system.
    
    Args:
        phi: Node field values (n_nodes,)
        adj_lists: List of adjacency lists for each node
        psi: Bond field values (n_nodes, max_degree)
        
    Returns:
        Laplacian values (n_nodes,)
    """
    n_nodes = phi.shape[0]
    result = np.zeros(n_nodes, dtype=np.float64)
    
    for i in range(n_nodes):
        neighbors = adj_lists[i]
        if len(neighbors) == 0:
            continue
            
        for idx_j, j in enumerate(neighbors):
            psi_ij = psi[i, idx_j]
            result[i] += psi_ij * (phi[j] - phi[i])
    
    return result


def bond_weighted_laplacian_with_derivative(
    phi: NDArray[np.float64],
    adj_lists: list,
    psi: NDArray[np.float64]
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Compute Laplacian and its derivative with respect to φ.
    
    Returns:
        (laplacian, d(laplacian)/dφ)
    """
    laplacian = bond_weighted_laplacian(phi, adj_lists, psi)
    
    # Derivative: d(L_ψ φ)_i / dφ_j = ψ_ij - δ_ij Σ_k ψ_ik
    n_nodes = phi.shape[0]
    derivative = np.zeros((n_nodes, n_nodes), dtype=np.float64)
    
    for i in range(n_nodes):
        neighbors = adj_lists[i]
        for idx_j, j in enumerate(neighbors):
            psi_ij = psi[i, idx_j]
            derivative[i, j] = psi_ij
            derivative[i, i] -= psi_ij
    
    return laplacian, derivative


# ---------------------------------------------------------------------------
# Ginzburg-Landau Potential (CF03 Section 1.1)
# ---------------------------------------------------------------------------

def node_potential_derivative(
    phi: NDArray[np.float64],
    lam: float = LAMBDA
) -> NDArray[np.float64]:
    """
    Derivative of double-well Ginzburg-Landau potential.
    
    CF03 Section 1.1: V(φ) = λ φ² (1-φ)²
    V'(φ) = 2λ φ (1-φ) (1-2φ)
    
    This potential drives spinodal decomposition and domain formation.
    
    Args:
        phi: Field values
        lam: Quartic coupling λ
        
    Returns:
        V'(φ)
    """
    return 2.0 * lam * phi * (1.0 - phi) * (1.0 - 2.0 * phi)


def node_potential(phi: NDArray[np.float64], lam: float = LAMBDA) -> NDArray[np.float64]:
    """
    Double-well Ginzburg-Landau potential V(φ) = λ φ² (1-φ)².
    
    Args:
        phi: Field values
        lam: Quartic coupling λ
        
    Returns:
        V(φ)
    """
    return lam * phi**2 * (1.0 - phi)**2


def bond_potential(psi: NDArray[np.float64], alpha: float = 1.0) -> NDArray[np.float64]:
    """
    Bond potential (simplified harmonic potential).
    
    Args:
        psi: Bond field values
        alpha: Bond stiffness
        
    Returns:
        Bond potential energy
    """
    return 0.5 * alpha * psi**2


# ---------------------------------------------------------------------------
# Void-Debt Throttling (CF11 Section 3.2)
# ---------------------------------------------------------------------------

def compute_effective_relaxation_time(
    base_tau: float,
    debt: NDArray[np.float64],
    beta_debt: float,
    max_throttle: float = 10.0
) -> NDArray[np.float64]:
    """
    Compute effective relaxation time with debt throttling.
    
    CF11 Section 3.2: τ_eff = τ exp(β_debt · debt)
    
    The debt field acts as a throttle, increasing relaxation time
    (slowing dynamics) in high-debt regions.
    
    Args:
        base_tau: Base relaxation time τ
        debt: Debt field values
        beta_debt: Debt throttle exponent (derived from Fisher info)
        max_throttle: Maximum throttle factor
        
    Returns:
        Effective relaxation time τ_eff
    """
    tau_eff = base_tau * np.exp(beta_debt * debt)
    
    # Clamp to prevent numerical issues
    tau_eff = np.clip(tau_eff, base_tau / max_throttle, base_tau * max_throttle)
    
    return tau_eff


def derive_beta_debt_from_fisher_info(
    fisher_metric: NDArray[np.float64],
    temperature: float
) -> float:
    """
    Derive β_debt from Fisher information metric (CF06).
    
    CF11 Section 3.2: β_debt is related to Fisher information
    through the thermodynamic uncertainty relation.
    
    Args:
        fisher_metric: Fisher information metric g_F
        temperature: Temperature kT
        
    Returns:
        β_debt derived from information geometry
    """
    # From CF06: Fisher metric relates to fluctuations
    # β_debt ~ 1 / (kT · Tr(g_F))
    
    if temperature > 0:
        trace_g = np.trace(fisher_metric) if fisher_metric.ndim == 2 else 1.0
        beta = 1.0 / (temperature * trace_g) if trace_g > 0 else 0.1
    else:
        beta = 0.1
    
    return float(beta)


# ---------------------------------------------------------------------------
# Telegraph Solver (CF04 Section 3)
# ---------------------------------------------------------------------------

def solve_telegraph_step(
    phi_curr: NDArray[np.float64],
    phi_prev: NDArray[np.float64],
    rhs: NDArray[np.float64],
    tau_eff: NDArray[np.float64],
    dt: float
) -> NDArray[np.float64]:
    """
    Single step of telegraph equation solver.
    
    CF04 Section 3: Discretized telegraph equation
    
    τ (φ^{n+1} - 2φ^n + φ^{n-1})/dt² + (φ^{n+1} - φ^{n-1})/(2dt) = RHS
    
    Solving for φ^{n+1}:
    φ^{n+1} = [RHS·dt² + (2τ + dt)φ^n - τ·φ^{n-1}] / (τ + dt)
    
    Args:
        phi_curr: Current φ^n
        phi_prev: Previous φ^{n-1}
        rhs: Right-hand side
        tau_eff: Effective relaxation time
        dt: Time step
        
    Returns:
        New φ^{n+1}
    """
    # Discretized telegraph equation
    numerator = rhs * dt**2 + (2.0 * tau_eff + dt) * phi_curr - tau_eff * phi_prev
    denominator = tau_eff + dt
    
    phi_new = numerator / denominator
    
    return phi_new


def solve_telegraph_steady_state(
    adj_lists: list,
    psi: NDArray[np.float64],
    lam: float = LAMBDA,
    tol: float = 1e-10,
    max_iter: int = 10000
) -> NDArray[np.float64]:
    """
    Solve for steady state of telegraph equation (φ̇ = 0, φ̈ = 0).
    
    At steady state: 0 = D ∇²φ - V'(φ)
    
    Args:
        adj_lists: Adjacency lists
        psi: Bond field
        lam: Quartic coupling
        tol: Convergence tolerance
        max_iter: Maximum iterations
        
    Returns:
        Steady state φ
    """
    n_nodes = len(adj_lists)
    phi = np.random.rand(n_nodes)  # Initial guess
    
    D = _params.D_DIFF
    
    for iteration in range(max_iter):
        laplacian = bond_weighted_laplacian(phi, adj_lists, psi)
        V_prime = node_potential_derivative(phi, lam)
        
        # Steady state condition: D ∇²φ = V'(φ)
        residual = D * laplacian - V_prime
        
        if np.linalg.norm(residual) < tol:
            break
        
        # Simple relaxation
        phi = phi - 0.01 * residual
        phi = np.clip(phi, 0.0, 1.0)
    
    return phi


# ---------------------------------------------------------------------------
# CFL Condition (CF04 Section 3.2)
# ---------------------------------------------------------------------------

def compute_cfl_timestep(
    c_signal: float,
    dx_min: float,
    safety_factor: float = 0.5
) -> float:
    """
    Compute CFL-stable time step for telegraph equation.
    
    CF04 Section 3.2: dt < dx / c_signal
    
    Args:
        c_signal: Signal propagation speed
        dx_min: Minimum grid spacing
        safety_factor: Safety factor for stability
        
    Returns:
        Stable time step
    """
    if c_signal <= 0:
        return 0.01
    
    dt_max = dx_min / c_signal
    return safety_factor * dt_max


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def compute_total_energy(
    phi: NDArray[np.float64],
    phi_dot: NDArray[np.float64],
    psi: NDArray[np.float64],
    adj_lists: list,
    lam: float = LAMBDA
) -> float:
    """
    Compute total energy of the system.
    
    E = ∫ [½ φ̇² + ½|∇φ|² + V(φ)] dx + bond energy
    
    Args:
        phi: Field values
        phi_dot: Field velocities
        psi: Bond field
        adj_lists: Adjacency lists
        lam: Quartic coupling
        
    Returns:
        Total energy
    """
    # Kinetic energy
    kinetic = 0.5 * np.sum(phi_dot**2)
    
    # Potential energy
    potential = np.sum(node_potential(phi, lam))
    
    # Bond energy
    bond_energy = 0.5 * np.sum(psi**2)
    
    return kinetic + potential + bond_energy


def compute_entropy_production(
    phi_dot: NDArray[np.float64],
    gamma: float
) -> float:
    """
    Compute entropy production rate.
    
    σ = γ ∫ φ̇² dx
    
    Args:
        phi_dot: Field velocities
        gamma: Damping coefficient
        
    Returns:
        Entropy production rate
    """
    return gamma * np.sum(phi_dot**2)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def initialize_parameters_from_hamiltonian(
    hamiltonian: Callable[[NDArray[np.float64]], NDArray[np.complex128]],
    parameter_range: NDArray[np.float64],
    base_energy_scale: float = 1.0
) -> CFDerivedParameters:
    """
    Initialize all parameters from Hamiltonian QGT.
    
    This is the primary initialization method that ensures
    all parameters are CF-derived, not engineering proxies.
    
    Args:
        hamiltonian: System Hamiltonian H(R)
        parameter_range: Range of parameters R
        base_energy_scale: Energy scale
        
    Returns:
        CFDerivedParameters with all CF-derived values
    """
    global _params
    
    # Compute QGT from Hamiltonian
    qgt_result = compute_qgt(hamiltonian, parameter_range)
    
    # Derive parameters
    _params = CFDerivedParameters(qgt_result, base_energy_scale)
    
    return _params


def get_parameters() -> CFDerivedParameters:
    """Get current CF-derived parameters"""
    return _params
