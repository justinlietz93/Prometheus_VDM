"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
# Runtime package initializer for modularized orchestrator components.
# Exposes submodules for clarity; keep lightweight to avoid side effects.
# Note: Nexus remains the external façade; internals live under runtime/*
__all__ = [
    "phase",
    "loop",
    "telemetry",
    "retention",
    "events_adapter",
    "runtime_helpers",
    "emitters",
    "orchestrator",
    "state",
]