"""Validation gate helpers (domain-organized).

All numerical PASS/FAIL gate predicates for physics/provenance gates live in this
package (see metriplectic_core, etc.). Runners and instruments must call helpers
from here rather than embedding gate logic or thresholds directly.
"""

from . import metriplectic_core

__all__ = ["metriplectic_core"]
