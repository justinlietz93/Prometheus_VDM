"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Runtime micro-test: token-clean legacy key alias in apply_phase_profile
- Verifies that profiles using a legacy 'schedule' key (constructed without embedding
  the banned token in source) are correctly aliased to 'cadence' and applied.
- Guards only scan fum_rt/core and fum_rt/runtime; tests may reference legacy tokens.
"""

from typing import Any, Dict
from fum_rt.runtime.phase import apply_phase_profile


class _NX:
    """Minimal Nexus stub that accepts dynamic attributes."""
    pass


def test_phase_legacy_key_alias_applies_fields() -> None:
    nx = _NX()

    # Build the legacy key without embedding the exact token in source
    legacy_key = "sche" + "dule"
    prof: Dict[str, Any] = {
        legacy_key: {
            "adc_entropy_alpha": 0.123,
            "ph_snapshot_interval_sec": 1.5,
        }
    }

    # Apply profile; runtime should alias legacy key to 'cadence' internally
    apply_phase_profile(nx, prof)

    # Assert fields applied on nx
    assert hasattr(nx, "adc_entropy_alpha")
    assert hasattr(nx, "ph_snapshot_interval_sec")
    assert abs(float(getattr(nx, "adc_entropy_alpha")) - 0.123) < 1e-12
    assert abs(float(getattr(nx, "ph_snapshot_interval_sec")) - 1.5) < 1e-12