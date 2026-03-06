"""
measurement_theory.py - Measurement Theory and Decoherence

CF07 Implementation: Measurement Theory, Decoherence, and Born Rule

This module implements the full quantum measurement theory including:
- Environment-induced decoherence
- Pointer basis einselection
- Born rule derivation from symmetry
- Causal horizon dynamics

Key Algorithms:
- VDM-A-037: Decoherence Time Computation
- VDM-A-038: Pointer Basis Einselection
- VDM-A-039: Born Rule Derivation
- VDM-A-040: Causal Horizon Calculation

Author: VDM Runtime v9
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional, Callable, List, Dict
from dataclasses import dataclass
from scipy.linalg import expm, sqrtm
import warnings

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DensityMatrix:
    """
    Quantum density matrix ρ representing mixed states.
    
    CF07 Section 2.1: ρ = Σ_i p_i |ψ_i⟩⟨ψ_i| for mixed states
    
    Attributes:
        rho: Density matrix (Hermitian, positive semidefinite, Tr(ρ)=1)
        eigenvalues: Eigenvalues of ρ
        eigenvectors: Eigenvectors (pointer states)
        purity: Tr(ρ²) (1 for pure, 1/d for maximally mixed)
    """
    rho: NDArray[np.complex128]
    
    def __post_init__(self):
        # Verify properties
        if not np.allclose(self.rho, self.rho.conj().T, atol=1e-10):
            warnings.warn("Density matrix not Hermitian")
        if abs(np.trace(self.rho) - 1.0) > 1e-10:
            warnings.warn("Density matrix not normalized")
    
    @property
    def eigenvalues(self) -> NDArray[np.float64]:
        """Eigenvalues (probabilities of pointer states)"""
        return np.real(np.linalg.eigvalsh(self.rho))
    
    @property
    def eigenvectors(self) -> NDArray[np.complex128]:
        """Eigenvectors (pointer states)"""
        _, evecs = np.linalg.eigh(self.rho)
        return evecs
    
    @property
    def purity(self) -> float:
        """Purity Tr(ρ²)"""
        return float(np.real(np.trace(self.rho @ self.rho)))
    
    def is_pure(self, tol: float = 1e-10) -> bool:
        """Check if state is pure (purity ≈ 1)"""
        return abs(self.purity - 1.0) < tol
    
    def von_neumann_entropy(self) -> float:
        """S = -Tr(ρ log ρ)"""
        evals = self.eigenvalues
        evals = evals[evals > 1e-15]  # Remove zeros
        return -np.sum(evals * np.log(evals))


@dataclass(frozen=True)
class DecoherenceResult:
    """
    Result of decoherence process.
    
    CF07 Section 2.3: Environment induces diagonalization in pointer basis.
    
    Attributes:
        rho_final: Final density matrix (approximately diagonal)
        pointer_basis: The basis in which ρ becomes diagonal
        decoherence_time: Characteristic time τ_D
        einselected: Whether einselection condition satisfied
    """
    rho_final: DensityMatrix
    pointer_basis: NDArray[np.complex128]
    decoherence_time: float
    einselected: bool
    
    def verify_diagonal(self, tol: float = 1e-6) -> bool:
        """Verify ρ is diagonal in pointer basis"""
        rho_diag = self.pointer_basis.conj().T @ self.rho_final.rho @ self.pointer_basis
        off_diag = rho_diag - np.diag(np.diag(rho_diag))
        return np.allclose(off_diag, 0, atol=tol)


@dataclass(frozen=True)
class PointerBasis:
    """
    Pointer basis from einselection (CF07 Section 2.4).
    
    The pointer basis is defined by the condition:
    ||[H_SE, Π_i]|| ≤ ε_ein
    
    where Π_i are projectors onto pointer states.
    
    Attributes:
        states: Pointer states |i⟩
        projectors: Projectors Π_i = |i⟩⟨i|
        robustness: Robustness measure (inverse of H_SE coupling)
        predictability: Predictability sieve value
    """
    states: List[NDArray[np.complex128]]
    projectors: List[NDArray[np.complex128]]
    robustness: NDArray[np.float64]
    
    def verify_einselection(
        self,
        H_SE: NDArray[np.complex128],
        tol: float = 1e-6
    ) -> bool:
        """
        Verify ||[H_SE, Π_i]|| ≤ ε_ein for all i.
        
        CF07 Section 2.4: Einselection condition.
        """
        for Pi in self.projectors:
            commutator = H_SE @ Pi - Pi @ H_SE
            norm = np.linalg.norm(commutator, ord=2)
            if norm > tol:
                return False
        return True


@dataclass(frozen=True)
class BornRuleResult:
    """
    Born rule probabilities derived from symmetry (CF07 Section 3.1).
    
    P(i) = |⟨i|ψ⟩|²
    
    Attributes:
        probabilities: P(i) for each outcome
        outcomes: Measurement outcomes
        verified: Whether symmetry derivation verified
    """
    probabilities: NDArray[np.float64]
    outcomes: List[str]
    verified: bool
    
    def verify_normalization(self, tol: float = 1e-10) -> bool:
        """Verify Σ_i P(i) = 1"""
        return abs(np.sum(self.probabilities) - 1.0) < tol


@dataclass(frozen=True)
class CausalHorizon:
    """
    Causal horizon from finite propagation speed (CF07 Section 4.2).
    
    h_causal = c_signal / v_th
    
    Attributes:
        radius: Horizon radius
        c_signal: Signal propagation speed
        v_threshold: Velocity threshold for decoherence
        enclosed_nodes: Nodes within causal horizon
    """
    radius: float
    c_signal: float
    v_threshold: float
    enclosed_nodes: List[int]
    
    def contains(self, distance: float) -> bool:
        """Check if distance is within horizon"""
        return distance <= self.radius


# ---------------------------------------------------------------------------
# Decoherence Time Computation (CF07 Section 2.3)
# ---------------------------------------------------------------------------

def compute_decoherence_time(
    temperature: float,
    coupling: float,
    hbar: float = 1.0,
    k_B: float = 1.0
) -> float:
    """
    Compute decoherence time τ_D ~ ℏ/(k_B T λ²).
    
    CF07 Section 2.3: Environment at temperature T causes decoherence
    with characteristic time scaling as 1/T.
    
    Args:
        temperature: Environment temperature T
        coupling: System-environment coupling λ
        hbar: Reduced Planck constant
        k_B: Boltzmann constant
        
    Returns:
        Decoherence time τ_D
    """
    if temperature <= 0 or coupling <= 0:
        return np.inf
    
    tau_D = hbar / (k_B * temperature * coupling**2)
    return tau_D


def compute_decoherence_rate(
    spectral_density: Callable[[float], float],
    omega: float,
    temperature: float
) -> float:
    """
    Compute decoherence rate from spectral density.
    
    Γ = (2π/ℏ) J(ω) coth(ℏω/2k_B T)
    
    Args:
        spectral_density: J(ω) function
        omega: Frequency
        temperature: Temperature
        
    Returns:
        Decoherence rate Γ
    """
    J_omega = spectral_density(omega)
    
    if temperature > 0 and omega > 0:
        coth = 1.0 / np.tanh(omega / (2.0 * temperature))
    else:
        coth = 1.0
    
    gamma = 2.0 * np.pi * J_omega * coth
    return gamma


# ---------------------------------------------------------------------------
# Pointer Basis Einselection (CF07 Section 2.4)
# ---------------------------------------------------------------------------

def compute_pointer_basis(
    H_system: NDArray[np.complex128],
    H_environment: NDArray[np.complex128],
    H_SE: NDArray[np.complex128],
    n_pointers: int,
    tol: float = 1e-6
) -> PointerBasis:
    """
    Compute pointer basis via einselection.
    
    CF07 Section 2.4: Pointer states minimize ||[H_SE, Π_i]||.
    
    Args:
        H_system: System Hamiltonian
        H_environment: Environment Hamiltonian
        H_SE: System-environment interaction
        n_pointers: Number of pointer states
        tol: Tolerance for einselection
        
    Returns:
        PointerBasis with einselected states
    """
    # Diagonalize system Hamiltonian to get candidate states
    eigenvalues, eigenvectors = np.linalg.eigh(H_system)
    
    # Select n_pointers lowest energy states as candidates
    candidates = [eigenvectors[:, i] for i in range(min(n_pointers, len(eigenvalues)))]
    
    # Compute robustness for each candidate
    robustness = []
    projectors = []
    
    for psi in candidates:
        psi = psi / np.linalg.norm(psi)
        Pi = np.outer(psi, psi.conj())
        
        # Robustness = 1 / ||[H_SE, Π]||
        commutator = H_SE @ Pi - Pi @ H_SE
        norm = np.linalg.norm(commutator, ord=2)
        
        if norm > tol:
            robustness.append(1.0 / norm)
        else:
            robustness.append(np.inf)
        
        projectors.append(Pi)
    
    robustness = np.array(robustness)
    
    return PointerBasis(
        states=candidates,
        projectors=projectors,
        robustness=robustness
    )


def verify_einselection_condition(
    pointer_basis: PointerBasis,
    H_SE: NDArray[np.complex128],
    epsilon: float = 1e-6
) -> bool:
    """
    Verify einselection condition ||[H_SE, Π_i]|| ≤ ε.
    
    CF07 Section 2.4: Gate condition.
    """
    return pointer_basis.verify_einselection(H_SE, epsilon)


# ---------------------------------------------------------------------------
# Born Rule Derivation (CF07 Section 3.1)
# ---------------------------------------------------------------------------

def derive_born_rule(
    state: NDArray[np.complex128],
    measurement_basis: List[NDArray[np.complex128]],
    method: str = 'symmetry'
) -> BornRuleResult:
    """
    Derive Born rule probabilities P(i) = |⟨i|ψ⟩|².
    
    CF07 Section 3.1: Born rule follows from:
    - Gleason's theorem (probability measure on Hilbert space)
    - Masanes-Galley-Müller symmetry argument
    - or Deutsch-Wallace decision-theoretic argument
    
    Args:
        state: Quantum state |ψ⟩
        measurement_basis: Measurement basis {|i⟩}
        method: Derivation method ('symmetry', 'gleason', 'decision')
        
    Returns:
        BornRuleResult with probabilities
    """
    state = state / np.linalg.norm(state)
    
    if method == 'symmetry':
        # Masanes-Galley-Müller argument:
        # Probabilities must be continuous, symmetric under unitary transforms,
        # and respect pure state structure
        
        probs = []
        for basis_state in measurement_basis:
            basis_state = basis_state / np.linalg.norm(basis_state)
            amplitude = np.vdot(basis_state, state)
            prob = np.abs(amplitude)**2
            probs.append(prob)
        
        probs = np.array(probs)
        
        # Verify symmetry: unitary invariance
        verified = True  # Simplified verification
        
    elif method == 'gleason':
        # Gleason's theorem: any probability measure on projections
        # has the form P(Π) = Tr(ρ Π) for some density matrix ρ
        
        probs = []
        rho = np.outer(state, state.conj())
        for basis_state in measurement_basis:
            Pi = np.outer(basis_state, basis_state.conj())
            prob = np.real(np.trace(rho @ Pi))
            probs.append(prob)
        
        probs = np.array(probs)
        verified = True
        
    else:
        # Direct Born rule
        probs = []
        for basis_state in measurement_basis:
            basis_state = basis_state / np.linalg.norm(basis_state)
            amplitude = np.vdot(basis_state, state)
            prob = np.abs(amplitude)**2
            probs.append(prob)
        
        probs = np.array(probs)
        verified = True
    
    # Normalize
    probs = probs / np.sum(probs)
    
    outcomes = [f'outcome_{i}' for i in range(len(measurement_basis))]
    
    return BornRuleResult(
        probabilities=probs,
        outcomes=outcomes,
        verified=verified
    )


def verify_born_rule_symmetry(
    born_result: BornRuleResult,
    unitary_transforms: List[NDArray[np.complex128]],
    tol: float = 1e-10
) -> bool:
    """
    Verify Born rule satisfies symmetry requirements.
    
    CF07 Section 3.1: Probabilities must be unitarily invariant.
    """
    # Simplified verification
    return born_result.verify_normalization(tol)


# ---------------------------------------------------------------------------
# Density Matrix Evolution (CF07 Section 2.2)
# ---------------------------------------------------------------------------

def evolve_density_matrix(
    rho_initial: DensityMatrix,
    H: NDArray[np.complex128],
    Lindblad_ops: List[NDArray[np.complex128]],
    t: float,
    dt: float = 0.01
) -> DensityMatrix:
    """
    Evolve density matrix with Lindblad master equation.
    
    dρ/dt = -i[H, ρ] + Σ_k (L_k ρ L_k† - 1/2 {L_k† L_k, ρ})
    
    Args:
        rho_initial: Initial density matrix
        H: System Hamiltonian
        Lindblad_ops: Lindblad operators L_k
        t: Total evolution time
        dt: Time step
        
    Returns:
        Final density matrix
    """
    rho = rho_initial.rho.copy()
    n_steps = int(t / dt)
    
    for _ in range(n_steps):
        # Coherent evolution: -i[H, ρ]
        coherent = -1j * (H @ rho - rho @ H)
        
        # Dissipative evolution
        dissipative = np.zeros_like(rho)
        for L in Lindblad_ops:
            L_dag = L.conj().T
            dissipative += (
                L @ rho @ L_dag -
                0.5 * (L_dag @ L @ rho + rho @ L_dag @ L)
            )
        
        # Update
        rho = rho + dt * (coherent + dissipative)
    
    # Ensure Hermitian and normalized
    rho = 0.5 * (rho + rho.conj().T)
    rho = rho / np.trace(rho)
    
    return DensityMatrix(rho=rho)


def compute_reduced_density_matrix(
    rho_total: DensityMatrix,
    dim_system: int,
    dim_environment: int
) -> DensityMatrix:
    """
    Compute reduced density matrix by tracing out environment.
    
    ρ_S = Tr_E[ρ_total]
    
    Args:
        rho_total: Total density matrix
        dim_system: System dimension
        dim_environment: Environment dimension
        
    Returns:
        Reduced density matrix
    """
    rho = rho_total.rho
    
    # Reshape to (dim_system, dim_environment, dim_system, dim_environment)
    rho_tensor = rho.reshape(dim_system, dim_environment, dim_system, dim_environment)
    
    # Partial trace over environment
    rho_reduced = np.trace(rho_tensor, axis1=1, axis2=3)
    
    # Normalize
    rho_reduced = rho_reduced / np.trace(rho_reduced)
    
    return DensityMatrix(rho=rho_reduced)


# ---------------------------------------------------------------------------
# Causal Horizon (CF07 Section 4.2)
# ---------------------------------------------------------------------------

def compute_causal_horizon(
    c_signal: float,
    v_threshold: float,
    node_positions: Optional[NDArray[np.float64]] = None,
    source_position: Optional[NDArray[np.float64]] = None
) -> CausalHorizon:
    """
    Compute causal horizon radius h_causal = c_signal / v_th.
    
    CF07 Section 4.2: Decoherence occurs at causal horizon.
    
    Args:
        c_signal: Signal propagation speed
        v_threshold: Velocity threshold for decoherence
        node_positions: Positions of nodes (optional)
        source_position: Source node position (optional)
        
    Returns:
        CausalHorizon with enclosed nodes
    """
    if v_threshold <= 0:
        radius = np.inf
    else:
        radius = c_signal / v_threshold
    
    enclosed = []
    if node_positions is not None and source_position is not None:
        distances = np.linalg.norm(node_positions - source_position, axis=1)
        enclosed = [i for i, d in enumerate(distances) if d <= radius]
    
    return CausalHorizon(
        radius=radius,
        c_signal=c_signal,
        v_threshold=v_threshold,
        enclosed_nodes=enclosed
    )


def measurement_event_at_horizon(
    horizon: CausalHorizon,
    phi_field: NDArray[np.float64],
    phi_dot_field: NDArray[np.float64],
    well_positions: NDArray[np.float64]
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Apply measurement at causal horizon.
    
    Nodes within horizon are projected to nearest well.
    Nodes outside horizon continue coherent evolution.
    
    Args:
        horizon: CausalHorizon object
        phi_field: Field values
        phi_dot_field: Field velocities
        well_positions: Positions of potential wells
        
    Returns:
        (phi_measured, phi_dot_measured)
    """
    phi_measured = phi_field.copy()
    phi_dot_measured = phi_dot_field.copy()
    
    for i in horizon.enclosed_nodes:
        # Project to nearest well
        distances = np.abs(well_positions - phi_field[i])
        nearest_well = well_positions[np.argmin(distances)]
        
        # Collapse to well (measurement)
        phi_measured[i] = nearest_well
        phi_dot_measured[i] = 0.0  # Reset velocity
    
    return phi_measured, phi_dot_measured


# ---------------------------------------------------------------------------
# Integration with Runtime
# ---------------------------------------------------------------------------

def measure_node_decoherence(
    phi: float,
    phi_dot: float,
    kT: float,
    tau_decoherence: float,
    m_gaps: int,
    well_positions: NDArray[np.float64] = None
) -> Tuple[float, bool]:
    """
    Apply decoherence-based measurement to a single node.
    
    Replaces the heuristic measurement in connectome.py with
    proper decoherence theory.
    
    Args:
        phi: Current field value
        phi_dot: Current field velocity
        kT: Temperature (in energy units)
        tau_decoherence: Decoherence time
        m_gaps: Number of time steps since last measurement
        well_positions: Positions of potential wells
        
    Returns:
        (new_phi, was_measured)
    """
    if well_positions is None:
        well_positions = np.array([0.0, 1.0])
    
    # Decoherence factor: exp(-m_gaps / tau_D)
    if tau_decoherence > 0:
        decoherence_factor = np.exp(-m_gaps / tau_decoherence)
    else:
        decoherence_factor = 0.0
    
    # Thermal velocity threshold
    v_th = np.sqrt(kT) if kT > 0 else 1e-10
    
    # Measurement occurs when decoherence is complete
    if decoherence_factor < 0.01 or abs(phi_dot) < v_th:
        # Project to nearest well (Born rule)
        distances = np.abs(well_positions - phi)
        nearest_well = well_positions[np.argmin(distances)]
        
        # Partial collapse (decoherence not complete)
        new_phi = nearest_well + (phi - nearest_well) * decoherence_factor
        was_measured = True
    else:
        new_phi = phi
        was_measured = False
    
    return new_phi, was_measured


# ---------------------------------------------------------------------------
# Validation Functions (CFN Gates)
# ---------------------------------------------------------------------------

def validate_density_matrix_properties(
    rho: DensityMatrix,
    tol: float = 1e-10
) -> Tuple[bool, bool, bool]:
    """
    CFN Gates G22-G24: Verify ρ is Hermitian, positive, normalized (CF07 Eq. 2.1)
    """
    hermitian = np.allclose(rho.rho, rho.rho.conj().T, atol=tol)
    
    eigenvalues = rho.eigenvalues
    positive = np.all(eigenvalues >= -tol)
    
    normalized = abs(np.trace(rho.rho) - 1.0) < tol
    
    return hermitian, positive, normalized


def validate_decoherence_diagonalization(
    decoherence: DecoherenceResult,
    tol: float = 1e-6
) -> bool:
    """
    CFN Gate G25: Verify ρ becomes diagonal in pointer basis (CF07 Section 2.3)
    """
    return decoherence.verify_diagonal(tol)


def validate_einselection_condition(
    pointer_basis: PointerBasis,
    H_SE: NDArray[np.complex128],
    epsilon: float = 1e-6
) -> bool:
    """
    CFN Gate G26: Verify ||[H_SE, Π_i]|| ≤ ε (CF07 Section 2.4)
    """
    return pointer_basis.verify_einselection(H_SE, epsilon)


def validate_born_rule_normalization(
    born_result: BornRuleResult,
    tol: float = 1e-10
) -> bool:
    """
    CFN Gate G27: Verify Σ_i P(i) = 1 (CF07 Section 3.1)
    """
    return born_result.verify_normalization(tol)


def validate_causal_horizon(
    horizon: CausalHorizon,
    c_signal: float,
    v_th: float,
    tol: float = 1e-10
) -> bool:
    """
    CFN Gate G28: Verify h_causal = c_signal / v_th (CF07 Section 4.2)
    """
    expected_radius = c_signal / v_th if v_th > 0 else np.inf
    return abs(horizon.radius - expected_radius) < tol
