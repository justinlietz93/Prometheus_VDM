"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Compatibility shim for visualization ring buffer.

Deprecated: import from 'fum_rt.io.visualization.maps_ring' instead.

Kept for transitional period to avoid breaking existing imports:
    from fum_rt.io.maps_ring import MapsRing, MapsFrame
"""

from __future__ import annotations

from fum_rt.io.visualization.maps_ring import MapsRing, MapsFrame

__all__ = ["MapsRing", "MapsFrame"]