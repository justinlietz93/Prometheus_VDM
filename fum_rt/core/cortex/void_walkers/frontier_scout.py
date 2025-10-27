"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Shim module for naming convention.
Use void-prefixed class from [void_frontier_scout.py](fum_rt/core/cortex/void_walkers/void_frontier_scout.py).
"""

from .void_frontier_scout import FrontierScout

__all__ = ["FrontierScout"]