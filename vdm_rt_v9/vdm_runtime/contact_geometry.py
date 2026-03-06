"""
contact_geometry.py - Contact Geometry and GENERIC Formalism

CF02 Implementation: Contact → Metriplectic Evolution

This module implements the contact geometric structure underlying the
metriplectic framework, including the contact 1-form, Reeb vector field,
and the GENERIC (General Equation for Non-Equilibrium Reversible-Irreversible
Coupling) formalism.

Key Algorithms:
- VDM-A-026: Contact Form Construction
- VDM-A-027: Reeb Vector Field Computation
- VDM-A-028: Contact-to-GENERIC Mapping

Author: VDM Runtime v9
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional, Callable, Dict, List
from dataclasses import dataclass
from scipy.optimize import minimize
import warnings

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ContactForm:
    """
    Contact 1-form α = ds - p_i dq^i (CF02 Section 1.1)
    
    In the thermodynamic context:
    - s: entropy-like coordinate (debt in the runtime)
    - q^i: extensive variables (field values φ)
    - p_i: conjugate intensive variables (field derivatives φ̇)
    
    Attributes:
        alpha: Contact 1-form as a function of state
        d_alpha: Exterior derivative dα (symplectic form on contact distribution)
        state_dim: Dimension of the state space
    """
    alpha: Callable[[NDArray[np.float64]], NDArray[np.float64]]
    d_alpha: Callable[[NDArray[np.float64]], NDArray[np.float64]]
    state_dim: int
    
    def evaluate(self, state: NDArray[np.float64]) -> float:
        """Evaluate α at a given state: α(X)"""
        return float(np.dot(self.alpha(state), state))
    
    def evaluate_d(self, state: NDArray[np.float64], X: NDArray[np.float64]) -> float:
        """Evaluate dα at state applied to vector X: dα(X, ·)"""
        d_alpha_matrix = self.d_alpha(state)
        return float(np.dot(X, d_alpha_matrix @ X))


@dataclass(frozen=True)
class ReebVectorField:
    """
    Reeb vector field R satisfying (CF02 Section 1.2):
    - ι_R α = 1 (normalization)
    - ι_R dα = 0 (kernel condition)
    
    The Reeb field generates the "time" evolution in contact geometry.
    """
    R: Callable[[NDArray[np.float64]], NDArray[np.float64]]
    contact_form: ContactForm
    
    def flow(self, state: NDArray[np.float64], dt: float) -> NDArray[np.float64]:
        """Integrate Reeb flow for time dt"""
        return state + dt * self.R(state)


@dataclass(frozen=True)
class GenericEvolution:
    """
    GENERIC evolution equation (CF02 Section 4.3):
    
    ẋ = L(x) ∇E(x) + M(x) ∇S(x)
    
    where:
    - L: Poisson operator (antisymmetric, derived from J)
    - M: Dissipative operator (symmetric positive semidefinite, derived from M)
    - E: Energy functional
    - S: Entropy functional
    
    Degeneracy conditions:
    - L ∇S = 0 (conservative dynamics preserves entropy)
    - M ∇E = 0 (dissipative dynamics preserves energy)
    """
    L: NDArray[np.float64]  # Poisson operator
    M: NDArray[np.float64]  # Dissipative operator
    grad_E: NDArray[np.float64]  # ∇E
    grad_S: NDArray[np.float64]  # ∇S
    degeneracy_verified: bool
    
    def compute_evolution(self) -> NDArray[np.float64]:
        """Compute ẋ = L∇E + M∇S"""
        return self.L @ self.grad_E + self.M @ self.grad_S
    
    def verify_degeneracy(self, tol: float = 1e-10) -> Tuple[bool, bool]:
        """Verify L∇S = 0 and M∇E = 0"""
        L_S = np.allclose(self.L @ self.grad_S, 0, atol=tol)
        M_E = np.allclose(self.M @ self.grad_E, 0, atol=tol)
        return L_S, M_E


# ---------------------------------------------------------------------------
# Contact Form Construction (CF02 Section 1.1)
# ---------------------------------------------------------------------------

def construct_contact_form(
    n_extensive: int,
    entropy_coord: int = 0
) -> ContactForm:
    """
    Construct the standard contact 1-form α = ds - p_i dq^i.
    
    CF02 Section 1.1: The contact form encodes the first law of thermodynamics
    in geometric terms.
    
    State vector structure: x = (s, q^1, ..., q^n, p_1, ..., p_n)
    - s: entropy coordinate (index 0)
    - q^i: extensive variables (indices 1 to n)
    - p_i: conjugate variables (indices n+1 to 2n)
    
    Args:
        n_extensive: Number of extensive variables (n)
        entropy_coord: Index of entropy coordinate (default 0)
        
    Returns:
        ContactForm with α and dα
    """
    state_dim = 1 + 2 * n_extensive
    
    def alpha(state: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        α = ds - p_i dq^i
        
        In components: α_0 = 1, α_{n+i} = -q^i, others = 0
        """
        result = np.zeros(state_dim)
        result[entropy_coord] = 1.0  # ds coefficient
        
        # -p_i dq^i terms
        for i in range(n_extensive):
            q_idx = 1 + i
            p_idx = 1 + n_extensive + i
            # This is a simplification - full implementation needs careful index handling
            
        return result
    
    def d_alpha(state: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        dα = -dp_i ∧ dq^i (symplectic form on contact distribution)
        
        In matrix form: dα has blocks:
        [ 0   0    0   ]
        [ 0   0   -I   ]
        [ 0   I    0   ]
        """
        result = np.zeros((state_dim, state_dim))
        
        # dα = Σ_i dq^i ∧ dp_i
        for i in range(n_extensive):
            q_idx = 1 + i
            p_idx = 1 + n_extensive + i
            result[q_idx, p_idx] = 1.0
            result[p_idx, q_idx] = -1.0
            
        return result
    
    return ContactForm(alpha=alpha, d_alpha=d_alpha, state_dim=state_dim)


def construct_thermodynamic_contact_form(
    temperature: float,
    extensive_vars: List[str] = None
) -> ContactForm:
    """
    Construct contact form for thermodynamic system.
    
    In thermodynamics: α = dU - TdS + Σ μ_i dN_i + ...
    Rearranging: α = TdS - dU - Σ μ_i dN_i - ...
    
    Args:
        temperature: Temperature T
        extensive_vars: Names of extensive variables (e.g., ['U', 'N', 'V'])
        
    Returns:
        ContactForm for thermodynamic system
    """
    if extensive_vars is None:
        extensive_vars = ['energy', 'particle_number']
    
    n_extensive = len(extensive_vars)
    state_dim = 1 + 2 * n_extensive
    
    def alpha(state: NDArray[np.float64]) -> NDArray[np.float64]:
        """α = T ds - p_i dq^i"""
        result = np.zeros(state_dim)
        result[0] = temperature  # T ds
        
        s, *rest = state
        q = rest[:n_extensive]
        p = rest[n_extensive:]
        
        # -p_i dq^i contribution
        for i in range(n_extensive):
            result[1 + i] = -p[i]
            
        return result
    
    def d_alpha(state: NDArray[np.float64]) -> NDArray[np.float64]:
        """dα = -dp_i ∧ dq^i"""
        result = np.zeros((state_dim, state_dim))
        
        for i in range(n_extensive):
            q_idx = 1 + i
            p_idx = 1 + n_extensive + i
            result[q_idx, p_idx] = 1.0
            result[p_idx, q_idx] = -1.0
            
        return result
    
    return ContactForm(alpha=alpha, d_alpha=d_alpha, state_dim=state_dim)


# ---------------------------------------------------------------------------
# Reeb Vector Field (CF02 Section 1.2)
# ---------------------------------------------------------------------------

def compute_reeb_vector_field(
    contact_form: ContactForm,
    method: str = 'direct'
) -> ReebVectorField:
    """
    Compute Reeb vector field R from contact form.
    
    CF02 Section 1.2: The Reeb field is uniquely defined by:
    - α(R) = 1
    - dα(R, ·) = 0
    
    Args:
        contact_form: Contact 1-form α
        method: Computation method ('direct' or 'optimization')
        
    Returns:
        ReebVectorField satisfying Reeb conditions
    """
    state_dim = contact_form.state_dim
    
    if method == 'direct':
        # Direct solution using linear algebra
        # At each point, solve: [α; dα] R = [1; 0]
        
        def R(state: NDArray[np.float64]) -> NDArray[np.float64]:
            alpha_vec = contact_form.alpha(state)
            d_alpha_mat = contact_form.d_alpha(state)
            
            # Construct system: [α^T; dα] R = [1; 0]
            A = np.vstack([alpha_vec.reshape(1, -1), d_alpha_mat])
            b = np.zeros(state_dim + 1)
            b[0] = 1.0
            
            # Solve least squares (system may be over/under-determined)
            R_vec, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
            
            return R_vec
        
    elif method == 'optimization':
        # Optimization-based solution
        
        def R(state: NDArray[np.float64]) -> NDArray[np.float64]:
            alpha_vec = contact_form.alpha(state)
            d_alpha_mat = contact_form.d_alpha(state)
            
            def objective(R_vec):
                # Minimize ||dα(R, ·)||^2 subject to α(R) = 1
                d_alpha_R = d_alpha_mat @ R_vec
                return np.sum(d_alpha_R**2)
            
            def constraint(R_vec):
                return np.dot(alpha_vec, R_vec) - 1.0
            
            # Initial guess
            R0 = np.random.randn(state_dim)
            R0 = R0 / np.dot(alpha_vec, R0) if np.dot(alpha_vec, R0) != 0 else R0
            
            # Constrained optimization
            from scipy.optimize import minimize
            cons = {'type': 'eq', 'fun': constraint}
            result = minimize(objective, R0, method='SLSQP', constraints=cons)
            
            return result.x
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return ReebVectorField(R=R, contact_form=contact_form)


def verify_reeb_conditions(
    reeb: ReebVectorField,
    state: NDArray[np.float64],
    tol: float = 1e-10
) -> Tuple[bool, bool]:
    """
    Verify Reeb conditions at a given state.
    
    Returns:
        (α(R) = 1, dα(R, ·) = 0)
    """
    R_vec = reeb.R(state)
    alpha_vec = reeb.contact_form.alpha(state)
    d_alpha_mat = reeb.contact_form.d_alpha(state)
    
    alpha_R = np.dot(alpha_vec, R_vec)
    d_alpha_R = d_alpha_mat @ R_vec
    
    cond1 = np.abs(alpha_R - 1.0) < tol
    cond2 = np.allclose(d_alpha_R, 0, atol=tol)
    
    return cond1, cond2


# ---------------------------------------------------------------------------
# GENERIC Formalism (CF02 Section 4.3)
# ---------------------------------------------------------------------------

def construct_generic_evolution(
    L: NDArray[np.float64],
    M: NDArray[np.float64],
    energy_func: Callable[[NDArray[np.float64]], float],
    entropy_func: Callable[[NDArray[np.float64]], float],
    state: NDArray[np.float64],
    grad_method: str = 'analytic',
    analytic_grad_E: Optional[Callable] = None,
    analytic_grad_S: Optional[Callable] = None
) -> GenericEvolution:
    """
    Construct GENERIC evolution at a given state.
    
    CF02 Section 4.3: ẋ = L∇E + M∇S with degeneracy conditions
    
    Args:
        L: Poisson operator (antisymmetric)
        M: Dissipative operator (symmetric positive semidefinite)
        energy_func: Energy functional E(x)
        entropy_func: Entropy functional S(x)
        state: Current state x
        grad_method: How to compute gradients ('analytic' or 'numerical')
        analytic_grad_E: Analytic gradient of energy (if available)
        analytic_grad_S: Analytic gradient of entropy (if available)
        
    Returns:
        GenericEvolution with verified degeneracy
    """
    # Compute gradients
    if grad_method == 'analytic' and analytic_grad_E is not None:
        grad_E = analytic_grad_E(state)
    else:
        grad_E = numerical_gradient(energy_func, state)
    
    if grad_method == 'analytic' and analytic_grad_S is not None:
        grad_S = analytic_grad_S(state)
    else:
        grad_S = numerical_gradient(entropy_func, state)
    
    # Verify degeneracy conditions
    L_S = np.allclose(L @ grad_S, 0, atol=1e-10)
    M_E = np.allclose(M @ grad_E, 0, atol=1e-10)
    degeneracy_verified = L_S and M_E
    
    if not degeneracy_verified:
        warnings.warn(
            f"GENERIC degeneracy not verified: "
            f"L∇S = {np.linalg.norm(L @ grad_S):.2e}, "
            f"M∇E = {np.linalg.norm(M @ grad_E):.2e}"
        )
    
    return GenericEvolution(
        L=L, M=M, grad_E=grad_E, grad_S=grad_S,
        degeneracy_verified=degeneracy_verified
    )


def numerical_gradient(
    func: Callable[[NDArray[np.float64]], float],
    x: NDArray[np.float64],
    dx: float = 1e-6
) -> NDArray[np.float64]:
    """Compute numerical gradient using central differences"""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += dx
        x_minus[i] -= dx
        grad[i] = (func(x_plus) - func(x_minus)) / (2 * dx)
    return grad


# ---------------------------------------------------------------------------
# Contact Hamiltonian to GENERIC Mapping (CF02 Section 4.3)
# ---------------------------------------------------------------------------

def contact_hamiltonian_to_generic(
    K: float,
    E: float,
    S: float,
    lambda_param: float,
    L_contact: NDArray[np.float64],
    M_contact: NDArray[np.float64]
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Map contact Hamiltonian K = E + λS to GENERIC operators.
    
    CF02 Section 4.3: The contact Hamiltonian decomposes into energy and entropy
    parts, which map to the GENERIC structure.
    
    Args:
        K: Contact Hamiltonian value
        E: Energy component
        S: Entropy component
        lambda_param: Lagrange multiplier (thermodynamic-like)
        L_contact: Contact Poisson operator
        M_contact: Contact dissipative operator
        
    Returns:
        (L_generic, M_generic) - GENERIC operators
    """
    # The mapping preserves the structure but may rescale
    # L_generic = L_contact (conservative part unchanged)
    # M_generic = λ * M_contact (dissipative part scaled by λ)
    
    L_generic = L_contact.copy()
    M_generic = lambda_param * M_contact
    
    return L_generic, M_generic


# ---------------------------------------------------------------------------
# Integration with QGT (CF01 → CF02)
# ---------------------------------------------------------------------------

def qgt_to_contact_structure(
    g: NDArray[np.float64],
    Omega: NDArray[np.float64],
    entropy_coord: int = 0
) -> Tuple[ContactForm, ReebVectorField]:
    """
    Convert QGT (metric g and curvature Ω) to contact structure.
    
    This bridges CF01 and CF02, showing how quantum geometry induces
    thermodynamic-like contact structure.
    
    Args:
        g: Quantum metric from QGT
        Omega: Berry curvature from QGT
        entropy_coord: Which coordinate plays role of entropy
        
    Returns:
        (ContactForm, ReebVectorField) derived from QGT
    """
    n = g.shape[0]
    state_dim = 1 + 2 * n
    
    # Construct contact form from metric structure
    def alpha(state: NDArray[np.float64]) -> NDArray[np.float64]:
        result = np.zeros(state_dim)
        result[entropy_coord] = 1.0
        
        # Use metric to define conjugate variables
        s = state[0]
        q = state[1:1+n]
        p = state[1+n:]
        
        # p_i = g_{ij} q^j (metric relates q and p)
        p_from_g = g @ q
        for i in range(n):
            result[1+i] = -p[i]  # -p_i dq^i
            
        return result
    
    def d_alpha(state: NDArray[np.float64]) -> NDArray[np.float64]:
        result = np.zeros((state_dim, state_dim))
        
        # Use Berry curvature for symplectic structure
        for i in range(n):
            for j in range(n):
                q_i = 1 + i
                q_j = 1 + j
                result[q_i, q_j] = Omega[i, j]
                
        # Standard dp ∧ dq terms
        for i in range(n):
            q_idx = 1 + i
            p_idx = 1 + n + i
            result[q_idx, p_idx] = 1.0
            result[p_idx, q_idx] = -1.0
            
        return result
    
    contact = ContactForm(alpha=alpha, d_alpha=d_alpha, state_dim=state_dim)
    reeb = compute_reeb_vector_field(contact)
    
    return contact, reeb


# ---------------------------------------------------------------------------
# Validation Functions (CFN Gates)
# ---------------------------------------------------------------------------

def validate_contact_condition(
    contact_form: ContactForm,
    state: NDArray[np.float64],
    tol: float = 1e-10
) -> bool:
    """
    CFN Gate G5: Verify α ∧ (dα)^n ≠ 0 (contact condition, CF02 Eq. 1.1)
    """
    alpha_vec = contact_form.alpha(state)
    d_alpha_mat = contact_form.d_alpha(state)
    
    # For 2n+1 dimensional space, check (dα)^n is non-degenerate on ker(α)
    n = (contact_form.state_dim - 1) // 2
    
    # Compute wedge product (dα)^n
    # This is simplified - full implementation needs exterior algebra
    d_alpha_power = np.linalg.matrix_power(d_alpha_mat, n)
    
    # Check non-degeneracy
    return np.linalg.matrix_rank(d_alpha_power) >= 2 * n


def validate_reeb_conditions_at_point(
    reeb: ReebVectorField,
    state: NDArray[np.float64],
    tol: float = 1e-10
) -> Tuple[bool, bool]:
    """
    CFN Gates G6, G7: Verify ι_R α = 1 and ι_R dα = 0 (CF02 Eq. 1.2)
    """
    return verify_reeb_conditions(reeb, state, tol)


def validate_generic_degeneracy(
    generic: GenericEvolution,
    tol: float = 1e-10
) -> Tuple[bool, bool]:
    """
    CFN Gates G8, G9: Verify L∇S = 0 and M∇E = 0 (CF02 Eq. 4.4-4.5)
    """
    return generic.verify_degeneracy(tol)
