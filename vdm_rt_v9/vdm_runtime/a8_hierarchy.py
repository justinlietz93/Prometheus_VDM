"""
a8_hierarchy.py - A8 Hierarchy and Interface Scaling

CF03 Implementation: A8 Scaling and Hierarchical Interfaces

This module implements the A8 hierarchy verification including:
- Interface counting with logarithmic scaling
- Perimeter reduction principle
- Gamma-convergence to sharp interface limit
- Scale-by-scale boundary census

Key Algorithms:
- VDM-A-041: Interface Counting at Multiple Scales
- VDM-A-042: Perimeter Reduction Verification
- VDM-A-043: Gamma-Convergence Analysis
- VDM-A-044: Hierarchy Depth Computation

Author: VDM Runtime v9
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional, List, Dict, Callable
from dataclasses import dataclass
from scipy.ndimage import label, find_objects
from scipy.spatial.distance import cdist
import warnings

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class InterfaceCount:
    """
    Interface count at a given scale.
    
    CF03 Section 3.2: N(L) = Θ(log(L/ℓ₀))
    
    Attributes:
        scale: Length scale L
        count: Number of interfaces N(L)
        interfaces: List of interface positions/indices
        perimeter: Total perimeter at this scale
    """
    scale: float
    count: int
    interfaces: List[Tuple]
    perimeter: float
    
    def scaling_exponent(self, ell_0: float = 1.0) -> float:
        """
        Compute effective scaling exponent.
        
        N(L) ~ C log(L/ℓ₀) implies scaling with log
        """
        if self.scale <= 0 or self.count <= 0:
            return 0.0
        return self.count / np.log(self.scale / ell_0)


@dataclass(frozen=True)
class HierarchyAnalysis:
    """
    Complete A8 hierarchy analysis.
    
    CF03 Section 3: Hierarchical interface structure.
    
    Attributes:
        scales: List of scales analyzed
        interface_counts: Interface counts at each scale
        log_scaling_verified: Whether N(L) ~ log(L) verified
        perimeter_reduction_verified: Whether perimeter reduction holds
        gamma_convergence_verified: Whether Gamma-convergence verified
    """
    scales: NDArray[np.float64]
    interface_counts: List[InterfaceCount]
    log_scaling_verified: bool
    perimeter_reduction_verified: bool
    gamma_convergence_verified: bool
    
    def get_scaling_coefficient(self) -> float:
        """Extract C from N(L) ≈ C log(L/ℓ₀)"""
        if len(self.interface_counts) < 2:
            return 0.0
        
        # Linear fit to N vs log(L)
        log_scales = np.log([ic.scale for ic in self.interface_counts])
        counts = [ic.count for ic in self.interface_counts]
        
        # Slope gives scaling coefficient
        if len(log_scales) > 1:
            slope = np.polyfit(log_scales, counts, 1)[0]
            return slope
        return 0.0


@dataclass(frozen=True)
class GammaConvergenceResult:
    """
    Gamma-convergence analysis result.
    
    CF03 Section 2.2: E_ε → c₀ Per as ε → 0
    
    Attributes:
        epsilon_values: Values of ε analyzed
        energies: Ginzburg-Landau energies E_ε
        perimeters: Perimeters at each ε
        limit_coefficient: c₀ from limit
        convergence_verified: Whether convergence verified
    """
    epsilon_values: NDArray[np.float64]
    energies: NDArray[np.float64]
    perimeters: NDArray[np.float64]
    limit_coefficient: float
    convergence_verified: bool
    
    def residual(self) -> NDArray[np.float64]:
        """Compute |E_ε - c₀ Per| / E_ε"""
        expected = self.limit_coefficient * self.perimeters
        return np.abs(self.energies - expected) / self.energies


@dataclass(frozen=True)
class PerimeterReduction:
    """
    Perimeter reduction principle verification.
    
    CF03 Section 3.3: Hierarchical < uniform energy.
    
    Attributes:
        hierarchical_energy: Energy with hierarchical interfaces
        uniform_energy: Energy with uniform (non-hierarchical) structure
        reduction_ratio: hierarchical / uniform
        reduction_verified: Whether reduction < 1 verified
    """
    hierarchical_energy: float
    uniform_energy: float
    reduction_ratio: float
    reduction_verified: bool


# ---------------------------------------------------------------------------
# Interface Detection and Counting (CF03 Section 3.2)
# ---------------------------------------------------------------------------

def detect_interfaces(
    phi_field: NDArray[np.float64],
    threshold: float = 0.5,
    connectivity: int = 1
) -> Tuple[NDArray[np.int32], int]:
    """
    Detect interfaces in scalar field.
    
    Interfaces are regions where φ crosses the threshold.
    
    Args:
        phi_field: Scalar order parameter field
        threshold: Interface threshold (typically 0.5 for [0,1] field)
        connectivity: Connectivity for labeling (1=4-conn, 2=8-conn in 2D)
        
    Returns:
        (labeled_array, num_interfaces)
    """
    # Binarize field
    binary = (phi_field > threshold).astype(np.int32)
    
    # Label connected components
    labeled, num_features = label(binary, structure=None)
    
    return labeled, num_features


def count_interfaces_at_scale(
    phi_field: NDArray[np.float64],
    scale: float,
    threshold: float = 0.5,
    ell_0: float = 1.0
) -> InterfaceCount:
    """
    Count interfaces at a given scale.
    
    CF03 Section 3.2: N(L) = Θ(log(L/ℓ₀))
    
    Args:
        phi_field: Scalar field
        scale: Length scale L
        threshold: Interface threshold
        ell_0: Reference length scale
        
    Returns:
        InterfaceCount at scale L
    """
    # Coarsen field to scale L
    if scale > ell_0:
        # Downsample by averaging
        factor = int(scale / ell_0)
        if factor > 1:
            # Simple block averaging
            shape = phi_field.shape
            new_shape = tuple(s // factor for s in shape)
            coarsened = np.zeros(new_shape)
            
            for idx in np.ndindex(*new_shape):
                slices = tuple(
                    slice(i * factor, (i + 1) * factor)
                    for i in idx
                )
                coarsened[idx] = np.mean(phi_field[slices])
        else:
            coarsened = phi_field
    else:
        coarsened = phi_field
    
    # Detect interfaces
    labeled, num_interfaces = detect_interfaces(coarsened, threshold)
    
    # Compute perimeter
    perimeter = compute_perimeter(labeled, num_interfaces)
    
    # Extract interface positions
    interfaces = []
    for i in range(1, num_interfaces + 1):
        coords = np.argwhere(labeled == i)
        if len(coords) > 0:
            interfaces.append(tuple(map(tuple, coords)))
    
    return InterfaceCount(
        scale=scale,
        count=num_interfaces,
        interfaces=interfaces,
        perimeter=perimeter
    )


def compute_perimeter(
    labeled_array: NDArray[np.int32],
    num_labels: int
) -> float:
    """
    Compute total perimeter of all interfaces.
    
    Uses edge counting between different labels.
    
    Args:
        labeled_array: Labeled interface array
        num_labels: Number of distinct labels
        
    Returns:
        Total perimeter
    """
    perimeter = 0.0
    
    # Count edges between different components
    for axis in range(labeled_array.ndim):
        # Roll along axis to compare neighbors
        rolled = np.roll(labeled_array, 1, axis=axis)
        
        # Count edges where labels differ
        edges = (labeled_array != rolled) & (labeled_array > 0) & (rolled > 0)
        perimeter += np.sum(edges)
    
    return float(perimeter)


# ---------------------------------------------------------------------------
# Logarithmic Scaling Verification (CF03 Section 3.2)
# ---------------------------------------------------------------------------

def verify_log_scaling(
    scales: NDArray[np.float64],
    counts: NDArray[np.int32],
    ell_0: float = 1.0,
    tolerance: float = 0.1
) -> Tuple[bool, float]:
    """
    Verify N(L) = Θ(log(L/ℓ₀)) scaling.
    
    CF03 Gate G3: |N(L) - C log(L)|/log(L) < 0.1
    
    Args:
        scales: Length scales L
        counts: Interface counts N(L)
        ell_0: Reference scale
        tolerance: Relative tolerance for verification
        
    Returns:
        (verified, scaling_coefficient C)
    """
    if len(scales) < 2 or len(counts) < 2:
        return False, 0.0
    
    # Remove zeros
    valid = (scales > 0) & (counts > 0)
    scales = scales[valid]
    counts = counts[valid]
    
    if len(scales) < 2:
        return False, 0.0
    
    # Fit N(L) = C log(L/ℓ₀)
    log_scales = np.log(scales / ell_0)
    
    # Linear fit
    coeffs = np.polyfit(log_scales, counts, 1)
    C = coeffs[0]
    
    # Predicted counts
    predicted = C * log_scales
    
    # Check relative error
    relative_error = np.abs(counts - predicted) / np.maximum(counts, 1)
    max_error = np.max(relative_error)
    
    verified = max_error < tolerance
    
    return verified, C


def compute_hierarchy_depth(
    L_max: float,
    ell_0: float,
    C: float
) -> int:
    """
    Compute hierarchy depth N(L_max).
    
    N(L) ≈ C log(L/ℓ₀)
    
    Args:
        L_max: Maximum scale
        ell_0: Minimum scale
        C: Scaling coefficient
        
    Returns:
        Hierarchy depth (number of interface levels)
    """
    if L_max <= ell_0:
        return 0
    return int(np.round(C * np.log(L_max / ell_0)))


# ---------------------------------------------------------------------------
# Perimeter Reduction Principle (CF03 Section 3.3)
# ---------------------------------------------------------------------------

def compute_ginzburg_landau_energy(
    phi_field: NDArray[np.float64],
    epsilon: float,
    lambda_param: float = 1.0,
    dx: float = 1.0
) -> float:
    """
    Compute Ginzburg-Landau energy E_ε[φ].
    
    CF03 Section 2.1: E_ε = ∫ [ε|∇φ|² + (1/ε)V(φ)] dx
    
    Args:
        phi_field: Order parameter field
        epsilon: Interface width parameter
        lambda_param: Quartic coupling
        dx: Grid spacing
        
    Returns:
        Total energy
    """
    # Gradient term: ε|∇φ|²
    gradient_squared = 0.0
    for axis in range(phi_field.ndim):
        grad = np.gradient(phi_field, dx, axis=axis)
        gradient_squared += grad**2
    
    gradient_term = epsilon * gradient_squared
    
    # Potential term: (1/ε)V(φ) = (λ/ε)φ²(1-φ)²
    V = lambda_param * phi_field**2 * (1.0 - phi_field)**2
    potential_term = V / epsilon
    
    # Total energy density
    energy_density = gradient_term + potential_term
    
    # Integrate
    dV = dx**phi_field.ndim
    total_energy = np.sum(energy_density) * dV
    
    return float(total_energy)


def verify_perimeter_reduction(
    phi_hierarchical: NDArray[np.float64],
    phi_uniform: NDArray[np.float64],
    epsilon: float,
    lambda_param: float = 1.0,
    dx: float = 1.0
) -> PerimeterReduction:
    """
    Verify perimeter reduction principle.
    
    CF03 Section 3.3: E_hierarchical < E_uniform
    
    Args:
        phi_hierarchical: Field with hierarchical interfaces
        phi_uniform: Field with uniform (non-hierarchical) structure
        epsilon: Interface width
        lambda_param: Quartic coupling
        dx: Grid spacing
        
    Returns:
        PerimeterReduction analysis
    """
    E_hier = compute_ginzburg_landau_energy(
        phi_hierarchical, epsilon, lambda_param, dx
    )
    E_unif = compute_ginzburg_landandau_energy(
        phi_uniform, epsilon, lambda_param, dx
    )
    
    ratio = E_hier / E_unif if E_unif > 0 else 1.0
    verified = E_hier < E_unif
    
    return PerimeterReduction(
        hierarchical_energy=E_hier,
        uniform_energy=E_unif,
        reduction_ratio=ratio,
        reduction_verified=verified
    )


# Fix typo in function call
def compute_ginzburg_landandau_energy(
    phi_field: NDArray[np.float64],
    epsilon: float,
    lambda_param: float = 1.0,
    dx: float = 1.0
) -> float:
    """Alias for compute_ginzburg_landau_energy"""
    return compute_ginzburg_landau_energy(phi_field, epsilon, lambda_param, dx)


# ---------------------------------------------------------------------------
# Gamma-Convergence (CF03 Section 2.2)
# ---------------------------------------------------------------------------

def analyze_gamma_convergence(
    phi_field: NDArray[np.float64],
    epsilon_values: NDArray[np.float64],
    lambda_param: float = 1.0,
    dx: float = 1.0,
    tolerance: float = 0.1
) -> GammaConvergenceResult:
    """
    Analyze Gamma-convergence E_ε → c₀ Per as ε → 0.
    
    CF03 Section 2.2: Sharp interface limit.
    
    Args:
        phi_field: Order parameter field
        epsilon_values: Array of ε values to analyze
        lambda_param: Quartic coupling
        dx: Grid spacing
        tolerance: Convergence tolerance
        
    Returns:
        GammaConvergenceResult
    """
    energies = []
    perimeters = []
    
    for eps in epsilon_values:
        # Compute energy
        E = compute_ginzburg_landau_energy(phi_field, eps, lambda_param, dx)
        energies.append(E)
        
        # Compute perimeter (interface length)
        labeled, num = detect_interfaces(phi_field)
        perim = compute_perimeter(labeled, num)
        perimeters.append(perim)
    
    energies = np.array(energies)
    perimeters = np.array(perimeters)
    
    # Fit E_ε ≈ c₀ Per for small ε
    # Use smallest ε values for fit
    n_fit = max(3, len(epsilon_values) // 3)
    
    if n_fit >= 2 and np.any(perimeters[-n_fit:] > 0):
        # Linear fit E vs Per for small ε
        valid = perimeters[-n_fit:] > 0
        if np.any(valid):
            c0 = np.mean(energies[-n_fit:][valid] / perimeters[-n_fit:][valid])
        else:
            c0 = 0.0
    else:
        c0 = 0.0
    
    # Verify convergence
    expected = c0 * perimeters
    relative_error = np.abs(energies - expected) / np.maximum(energies, 1e-10)
    convergence_verified = np.all(relative_error < tolerance)
    
    return GammaConvergenceResult(
        epsilon_values=epsilon_values,
        energies=energies,
        perimeters=perimeters,
        limit_coefficient=c0,
        convergence_verified=convergence_verified
    )


def compute_sharp_interface_limit(
    phi_field: NDArray[np.float64],
    threshold: float = 0.5
) -> Tuple[NDArray[np.float64], float]:
    """
    Compute sharp interface limit (ε → 0).
    
    Returns characteristic function and perimeter.
    
    Args:
        phi_field: Order parameter field
        threshold: Interface threshold
        
    Returns:
        (characteristic_function, perimeter)
    """
    # Characteristic function: 1 where φ > threshold, 0 elsewhere
    chi = (phi_field > threshold).astype(np.float64)
    
    # Compute perimeter
    labeled, num = detect_interfaces(chi, threshold=0.5)
    perim = compute_perimeter(labeled, num)
    
    return chi, perim


# ---------------------------------------------------------------------------
# Full Hierarchy Analysis Pipeline
# ---------------------------------------------------------------------------

def analyze_a8_hierarchy(
    phi_field: NDArray[np.float64],
    scales: NDArray[np.float64],
    epsilon_values: Optional[NDArray[np.float64]] = None,
    ell_0: float = 1.0,
    threshold: float = 0.5,
    lambda_param: float = 1.0,
    dx: float = 1.0
) -> HierarchyAnalysis:
    """
    Complete A8 hierarchy analysis.
    
    CF03 Full pipeline: interface counting, perimeter reduction, Gamma-convergence.
    
    Args:
        phi_field: Order parameter field
        scales: Scales L to analyze
        epsilon_values: Epsilon values for Gamma-convergence (optional)
        ell_0: Reference scale
        threshold: Interface threshold
        lambda_param: Quartic coupling
        dx: Grid spacing
        
    Returns:
        Complete HierarchyAnalysis
    """
    # Interface counting at multiple scales
    interface_counts = []
    for scale in scales:
        ic = count_interfaces_at_scale(phi_field, scale, threshold, ell_0)
        interface_counts.append(ic)
    
    # Verify log scaling
    counts = np.array([ic.count for ic in interface_counts])
    log_verified, C = verify_log_scaling(scales, counts, ell_0)
    
    # Perimeter reduction (compare to uniform)
    # Create uniform comparison field
    phi_uniform = np.mean(phi_field) * np.ones_like(phi_field)
    
    if epsilon_values is not None and len(epsilon_values) > 0:
        eps = epsilon_values[len(epsilon_values) // 2]  # Use middle value
        perim_result = verify_perimeter_reduction(
            phi_field, phi_uniform, eps, lambda_param, dx
        )
        perim_verified = perim_result.reduction_verified
    else:
        perim_verified = False
    
    # Gamma-convergence
    if epsilon_values is not None and len(epsilon_values) > 0:
        gamma_result = analyze_gamma_convergence(
            phi_field, epsilon_values, lambda_param, dx
        )
        gamma_verified = gamma_result.convergence_verified
    else:
        gamma_verified = False
    
    return HierarchyAnalysis(
        scales=scales,
        interface_counts=interface_counts,
        log_scaling_verified=log_verified,
        perimeter_reduction_verified=perim_verified,
        gamma_convergence_verified=gamma_verified
    )


# ---------------------------------------------------------------------------
# Validation Functions (CFN Gates)
# ---------------------------------------------------------------------------

def validate_interface_scaling(
    hierarchy: HierarchyAnalysis,
    tolerance: float = 0.1
) -> bool:
    """
    CFN Gate G3: Verify N(L) = Θ(log(L/ℓ₀)) (CF03 Section 3.2)
    """
    return hierarchy.log_scaling_verified


def validate_perimeter_reduction(
    hierarchy: HierarchyAnalysis
) -> bool:
    """
    CFN Gate G29: Verify hierarchical < uniform energy (CF03 Section 3.3)
    """
    return hierarchy.perimeter_reduction_verified


def validate_gamma_convergence(
    gamma_result: GammaConvergenceResult,
    tolerance: float = 0.1
) -> bool:
    """
    CFN Gate G30: Verify E_ε → c₀ Per as ε → 0 (CF03 Section 2.2)
    """
    return gamma_result.convergence_verified
