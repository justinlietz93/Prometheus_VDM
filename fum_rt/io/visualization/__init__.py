"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Visualization transport primitives.

- maps_ring: bounded, drop-oldest ring buffer for maps/frame payloads
- websocket_server: bounded WebSocket forwarder for maps frames
"""
from .maps_ring import MapsRing, MapsFrame  # re-export
from .websocket_server import MapsWebSocketServer  # re-export