"""
Core Engine package initializer.

Exports CoreEngine from the in-package implementation module to avoid any
cross-file redirects. Implementation resides under this package.
"""

from .core_engine import CoreEngine

__all__ = ["CoreEngine"]