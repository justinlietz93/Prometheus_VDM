"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Core Engine package initializer.

Exports CoreEngine from the in-package implementation module to avoid any
cross-file redirects. Implementation resides under this package.
"""

from .core_engine import CoreEngine

__all__ = ["CoreEngine"]