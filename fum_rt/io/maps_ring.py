"""
Compatibility shim for visualization ring buffer.

Deprecated: import from 'fum_rt.io.visualization.maps_ring' instead.

Kept for transitional period to avoid breaking existing imports:
    from fum_rt.io.maps_ring import MapsRing, MapsFrame
"""

from __future__ import annotations

from fum_rt.io.visualization.maps_ring import MapsRing, MapsFrame

__all__ = ["MapsRing", "MapsFrame"]