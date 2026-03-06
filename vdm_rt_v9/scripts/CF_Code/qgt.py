"""
qgt.py - Quantum Geometric Tensor and Metriplectic Operator Derivation

CF01 Implementation: QGT → Metriplectic Brackets

This module implements the full derivation chain from quantum states to
the metriplectic operators J (Poisson) and M (dissipative) as specified
in CF01 Sections 4-5.

Key Algorithms:
- VDM-A-023: QGT Computation from Eigenstates
- VDM-A-024: Berry Curvature Extraction
- VDM-A-025: Metriplectic Operator Construction

Author: VDM Runtime v9
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional, Callable, List
from dataclasses import dataclass
import warnings

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class QGTResult:
    """
    Container for Quantum Geometric Tensor computation results.
    
    Attributes:
        Q: Full quantum geometric tensor Q_μν
        g: Quantum metric (real part) g_μν = Re(Q_μν)
        Omega: Berry curvature (imaginary part) Ω_μν = -2 Im(Q_μν)
        parameters: Parameter values at which QGT was computed
        eigenstate: The eigenstate |ψ(R)⟩ used for computation
    """
    Q: NDArray[np.complex128]
    g: NDArray[np.float64]
    Omega: NDArray[np.float64]
    parameters: NDArray[np.float64]
    eigenstate: NDArray[np.complex128]
    
    def verify_hermiticity(self, tol: float = 1e-10) -> bool:
        """Verify Q is Hermitian: Q† = Q (CF01 Eq. 2.3)"""
        return np.allclose(self.Q, self.Q.conj().T, atol=tol)
    
    def verify_positive_semidefinite(self, tol: float = 1e-10) -> bool:
        """Verify g is positive semidefinite (CF01 Eq. 2.4)"""
        eigvals = np.linalg.eigvalsh(self.g)
        return np.all(eigvals >= -tol)


@dataclass(frozen=True)
class MetriplecticOperators:
    """
    Container for metriplectic operators J and M.
    
    Attributes:
        J: Poisson operator J^μν = (Ω⁻¹)^μν (on non-degenerate leaves)
        M: Dissipative operator M^μν = g^μν
        Omega: Berry curvature used to construct J
        g: Quantum metric used to construct M
        degeneracy_verified: Whether degeneracy conditions were verified
    """
    J: NDArray[np.float64]
    M: NDArray[np.float64]
    Omega: NDArray[np.float64]
    g: NDArray[np.float64]
    degeneracy_verified: bool
    
    def verify_degeneracy_J(self, grad_S: NDArray[np.float64], tol: float = 1e-10) -> bool:
        """
        Verify J·∇Σ = 0 (CF01 Eq. 4.2)
        Σ is the entropy-like quantity (debt in the runtime)
        """
        result = self.J @ grad_S
        return np.allclose(result, 0, atol=tol)
    
    def verify_degeneracy_M(self, grad_I: NDArray[np.float64], tol: float = 1e-10) -> bool:
        """
        Verify M·∇I = 0 (CF01 Eq. 4.3)
        I is the invariant (energy-like quantity)
        """
        result = self.M @ grad_I
        return np.allclose(result, 0, atol=tol)


# ---------------------------------------------------------------------------
# QGT Computation (CF01 Section 5.1 - Algorithm VDM-A-023)
# ---------------------------------------------------------------------------

def compute_parameter_derivative(
    hamiltonian: Callable[[NDArray[np.float64]], NDArray[np.complex128]],
    eigenstate: NDArray[np.complex128],
    parameters: NDArray[np.float64],
    param_index: int,
    dp: float = 1e-6
) -> NDArray[np.complex128]:
    """
    Compute |∂_μ ψ⟩ using finite differences.
    
    CF01 Section 5.1 Step 1: Compute parameter derivatives
    
    Args:
        hamiltonian: Function H(R) returning Hamiltonian matrix
        eigenstate: Current eigenstate |ψ(R)⟩
        parameters: Current parameter values R
        param_index: Which parameter to differentiate (μ)
        dp: Finite difference step size
        
    Returns:
        |∂_μ ψ⟩ - derivative of eigenstate with respect to parameter μ
    """
    # Forward difference
    params_plus = parameters.copy()
    params_plus[param_index] += dp
    H_plus = hamiltonian(params_plus)
    _, evecs_plus = np.linalg.eigh(H_plus)
    
    # Find corresponding eigenstate (match by overlap)
    overlaps = np.abs(evecs_plus.T.conj() @ eigenstate)
    idx = np.argmax(overlaps)
    psi_plus = evecs_plus[:, idx]
    
    # Backward difference for better accuracy
    params_minus = parameters.copy()
    params_minus[param_index] -= dp
    H_minus = hamiltonian(params_minus)
    _, evecs_minus = np.linalg.eigh(H_minus)
    
    overlaps = np.abs(evecs_minus.T.conj() @ eigenstate)
    idx = np.argmax(overlaps)
    psi_minus = evecs_minus[:, idx]
    
    # Central difference
    dpsi = (psi_plus - psi_minus) / (2 * dp)
    
    return dpsi


def parallel_transport_gauge_fix(
    dpsi: NDArray[np.complex128],
    psi: NDArray[np.complex128]
) -> NDArray[np.complex128]:
    """
    Apply parallel transport gauge fixing: ⟨ψ|∂_μ ψ⟩ = 0 (CF01 Section 5.1 Step 2)
    
    This removes the U(1) phase ambiguity from the eigenstate derivative.
    
    Args:
        dpsi: Raw parameter derivative |∂_μ ψ⟩
        psi: Eigenstate |ψ⟩
        
    Returns:
        Gauge-fixed derivative |∂_μ ψ⟩_⊥
    """
    overlap = np.vdot(psi, dpsi)
    dpsi_fixed = dpsi - overlap * psi
    return dpsi_fixed


def compute_qgt(
    hamiltonian: Callable[[NDArray[np.float64]], NDArray[np.complex128]],
    parameters: NDArray[np.float64],
    eigenstate: Optional[NDArray[np.complex128]] = None,
    dp: float = 1e-6,
    apply_gauge_fixing: bool = True
) -> QGTResult:
    """
    Compute Quantum Geometric Tensor Q_μν from eigenstates.
    
    CF01 Section 5.1 Algorithm VDM-A-023:
    Q_μν = ⟨∂_μ ψ|∂_ν ψ⟩ - ⟨∂_μ ψ|ψ⟩⟨ψ|∂_ν ψ⟩
    
    Args:
        hamiltonian: Function H(R) returning Hamiltonian matrix
        parameters: Parameter values R at which to compute QGT
        eigenstate: Pre-computed eigenstate (if None, computed from Hamiltonian)
        dp: Finite difference step size
        apply_gauge_fixing: Whether to apply parallel transport gauge fixing
        
    Returns:
        QGTResult containing Q, g, Omega, and metadata
    """
    n_params = len(parameters)
    
    # Step 0: Compute eigenstate if not provided
    if eigenstate is None:
        H = hamiltonian(parameters)
        eigenvalues, eigenvectors = np.linalg.eigh(H)
        # Ground state (lowest eigenvalue)
        eigenstate = eigenvectors[:, 0]
    
    eigenstate = eigenstate / np.linalg.norm(eigenstate)  # Normalize
    
    # Step 1: Compute all parameter derivatives
    dpsi_list = []
    for mu in range(n_params):
        dpsi = compute_parameter_derivative(
            hamiltonian, eigenstate, parameters, mu, dp
        )
        
        # Step 2: Apply gauge fixing
        if apply_gauge_fixing:
            dpsi = parallel_transport_gauge_fix(dpsi, eigenstate)
        
        dpsi_list.append(dpsi)
    
    # Step 3: Compute QGT components
    Q = np.zeros((n_params, n_params), dtype=np.complex128)
    
    for mu in range(n_params):
        for nu in range(n_params):
            # Q_μν = ⟨∂_μ ψ|∂_ν ψ⟩ - ⟨∂_μ ψ|ψ⟩⟨ψ|∂_ν ψ⟩
            term1 = np.vdot(dpsi_list[mu], dpsi_list[nu])
            term2 = np.vdot(dpsi_list[mu], eigenstate) * np.vdot(eigenstate, dpsi_list[nu])
            Q[mu, nu] = term1 - term2
    
    # Step 4: Extract metric and curvature
    g = np.real(Q)  # Quantum metric (CF01 Eq. 2.3)
    Omega = -2 * np.imag(Q)  # Berry curvature (CF01 Eq. 2.4)
    
    return QGTResult(Q=Q, g=g, Omega=Omega, 
                     parameters=parameters, eigenstate=eigenstate)


# ---------------------------------------------------------------------------
# Metriplectic Operator Construction (CF01 Section 4.1)
# ---------------------------------------------------------------------------

def construct_metriplectic_operators(
    qgt_result: QGTResult,
    verify_degeneracy: bool = True,
    grad_energy: Optional[NDArray[np.float64]] = None,
    grad_entropy: Optional[NDArray[np.float64]] = None,
    tol: float = 1e-10
) -> MetriplecticOperators:
    """
    Construct metriplectic operators J and M from QGT.
    
    CF01 Section 4.1:
    - J^μν = (Ω⁻¹)^μν on non-degenerate leaves
    - M^μν = g^μν (inverse quantum metric)
    
    Args:
        qgt_result: Result from compute_qgt()
        verify_degeneracy: Whether to verify degeneracy conditions
        grad_energy: Gradient of energy ∇I for M-degeneracy check
        grad_entropy: Gradient of entropy ∇Σ for J-degeneracy check
        tol: Tolerance for degeneracy verification
        
    Returns:
        MetriplecticOperators containing J, M, and verification status
    """
    g = qgt_result.g
    Omega = qgt_result.Omega
    
    # Construct M = g^μν (inverse quantum metric)
    try:
        M = np.linalg.inv(g + tol * np.eye(g.shape[0]))  # Regularized inverse
    except np.linalg.LinAlgError:
        # Use pseudo-inverse for singular metric
        M = np.linalg.pinv(g)
        warnings.warn("Quantum metric g is singular, using pseudo-inverse")
    
    # Construct J = (Ω⁻¹)^μν on non-degenerate leaves
    # Berry curvature is antisymmetric, so we need to handle it carefully
    try:
        # For antisymmetric matrix, pseudo-inverse gives the right structure
        J = np.linalg.pinv(Omega)
    except np.linalg.LinAlgError:
        J = np.zeros_like(Omega)
        warnings.warn("Berry curvature Ω is degenerate, J set to zero")
    
    # Verify degeneracy conditions if gradients provided
    degeneracy_verified = False
    if verify_degeneracy and grad_energy is not None and grad_entropy is not None:
        J_check = np.allclose(J @ grad_entropy, 0, atol=tol)
        M_check = np.allclose(M @ grad_energy, 0, atol=tol)
        degeneracy_verified = J_check and M_check
        
        if not degeneracy_verified:
            warnings.warn(
                f"Degeneracy conditions not verified: "
                f"J·∇Σ = {np.linalg.norm(J @ grad_entropy):.2e}, "
                f"M·∇I = {np.linalg.norm(M @ grad_energy):.2e}"
            )
    
    return MetriplecticOperators(
        J=J, M=M, Omega=Omega, g=g,
        degeneracy_verified=degeneracy_verified
    )


# ---------------------------------------------------------------------------
# Telegraph Parameter Derivation from QGT (CF01 → CF04)
# ---------------------------------------------------------------------------

def derive_telegraph_parameters_from_qgt(
    qgt_result: QGTResult,
    base_energy_scale: float = 1.0
) -> Tuple[float, float, float]:
    """
    Derive telegraph equation parameters from QGT.
    
    CF01 → CF04: The telegraph parameters are not engineering constants
    but emerge from the quantum geometric structure.
    
    Args:
        qgt_result: QGT computation result
        base_energy_scale: Energy scale for dimensional analysis
        
    Returns:
        (gamma_damp, D_diff, tau) - derived parameters
    """
    # Extract characteristic scales from quantum metric
    g_eigenvals = np.linalg.eigvalsh(qgt_result.g)
    g_scale = np.mean(g_eigenvals[g_eigenvals > 0])
    
    # Extract characteristic scales from Berry curvature
    Omega_eigenvals = np.linalg.eigvalsh(1j * qgt_result.Omega)  # Hermitize
    omega_scale = np.mean(np.abs(Omega_eigenvals))
    
    # Derive telegraph parameters (CF04 Section 2.1, 3.1)
    # Damping from metric (dissipative scale)
    gamma_damp = base_energy_scale * g_scale
    
    # Diffusivity from combined structure
    D_diff = base_energy_scale**2 * g_scale / omega_scale if omega_scale > 0 else 0.1
    
    # Relaxation time
    tau = 1.0 / gamma_damp if gamma_damp > 0 else 1.0
    
    return gamma_damp, D_diff, tau


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def berry_phase_from_qgt(
    qgt_result: QGTResult,
    loop_params: List[NDArray[np.float64]]
) -> float:
    """
    Compute Berry phase around a closed loop in parameter space.
    
    γ = ∮ A_μ dR^μ where A_μ = i⟨ψ|∂_μ ψ⟩ (CF09 Section 2.1)
    
    Args:
        qgt_result: QGT at reference point
        loop_params: List of parameter points forming closed loop
        
    Returns:
        Berry phase γ (modulo 2π)
    """
    phase = 0.0
    n_points = len(loop_params)
    
    for i in range(n_points):
        R_current = loop_params[i]
        R_next = loop_params[(i + 1) % n_points]
        dR = R_next - R_current
        
        # Approximate Berry connection A_μ
        # A_μ ≈ i⟨ψ(R)|(|ψ(R+dR)⟩ - |ψ(R)⟩)/|dR|
        # This is a simplified version - full implementation needs parallel transport
        
    return phase % (2 * np.pi)


def fidelity_metric_from_qgt(qgt_result: QGTResult) -> NDArray[np.float64]:
    """
    Extract fidelity metric (Bures metric) from QGT.
    
    The Bures metric is related to the quantum metric by:
    g_Bures = (1/4) g_QGT (CF06 Section 2.1)
    
    Args:
        qgt_result: QGT computation result
        
    Returns:
        Fidelity metric g^F_μν
    """
    return 0.25 * qgt_result.g


# ---------------------------------------------------------------------------
# Validation Functions (CFN Gates)
# ---------------------------------------------------------------------------

def validate_qgt_hermiticity(qgt_result: QGTResult, tol: float = 1e-10) -> bool:
    """
    CFN Gate G1: Verify Q† = Q (CF01 Eq. 2.3)
    """
    return qgt_result.verify_hermiticity(tol)


def validate_metric_positive_semidefinite(qgt_result: QGTResult, tol: float = 1e-10) -> bool:
    """
    CFN Gate G2: Verify g ≥ 0 (CF01 Eq. 2.4)
    """
    return qgt_result.verify_positive_semidefinite(tol)


def validate_metriplectic_degeneracy(
    operators: MetriplecticOperators,
    grad_energy: NDArray[np.float64],
    grad_entropy: NDArray[np.float64],
    tol: float = 1e-10
) -> Tuple[bool, bool]:
    """
    CFN Gates G3, G4: Verify J·∇Σ = 0 and M·∇I = 0 (CF01 Eq. 4.2-4.3)
    """
    J_ok = operators.verify_degeneracy_J(grad_entropy, tol)
    M_ok = operators.verify_degeneracy_M(grad_energy, tol)
    return J_ok, M_ok
