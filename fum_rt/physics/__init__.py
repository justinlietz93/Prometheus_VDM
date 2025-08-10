"""
Physics solvers for the FUM scalar EFT (finite-tube modes and condensation).

References:
- [derivation/finite_tube_mode_analysis.md](derivation/finite_tube_mode_analysis.md:1)
- [derivation/discrete_to_continuum.md](derivation/discrete_to_continuum.md:125-193)
- [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:117-134)
"""

from .cylinder_modes import compute_kappas, mode_functions
from .condense_tube import (
    ModeEntry,
    compute_modes_for_R,
    build_quartic_diagonal,
    find_condensate_diagonal,
    mass_matrix_diagonal,
    energy_scan,
)

__all__ = [
    "compute_kappas",
    "mode_functions",
    "ModeEntry",
    "compute_modes_for_R",
    "build_quartic_diagonal",
    "find_condensate_diagonal",
    "mass_matrix_diagonal",
    "energy_scan",
]