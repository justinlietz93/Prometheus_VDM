#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Experiment: Thermodynamic Routing v2 — Prereg Biased Main (full gates)

This script is a dedicated entrypoint that sets its own identity for approvals,
selects the prereg-biased-main spec by default, and delegates to the published runner.
It does not modify the legacy runner.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Preserve provenance: set this script's identity
os.environ.setdefault("VDM_RUN_SCRIPT", Path(__file__).name)

# Default spec path for this prereg experiment
_DEFAULT_SPEC = Path(__file__).with_name("specs").joinpath("tr_v2.prereg_biased_main.json")

# Ensure CODE_ROOT is importable when run as a script
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

# Delegate to the published runner implementation
from physics.thermo_routing.run_thermo_routing import main  # type: ignore

if __name__ == "__main__":
    if not any(arg == "--spec" or arg.startswith("--spec=") for arg in sys.argv[1:]):
        sys.argv.extend(["--spec", str(_DEFAULT_SPEC)])
    sys.exit(main())
