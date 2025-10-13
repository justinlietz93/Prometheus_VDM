#!/usr/bin/env python3
"""
Experiment: Thermodynamic Routing v2 — Prereg Biased Geometry (full gates)

Creates a dedicated entrypoint for the preregistered biased-geometry run.
This does not modify the legacy runner. It sets this script's identity for
script-scoped approvals and delegates to the existing implementation.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Preserve provenance: optionally set this script name for script-scoped approvals.
# Note: the delegated runner may override this to its own stem for approval matching.
os.environ.setdefault("VDM_RUN_SCRIPT", Path(__file__).name)

# Default spec path for this experiment (can be overridden via --spec)
_DEFAULT_SPEC = Path(__file__).with_name("specs").joinpath("tr_v2.prereg_biased.json")

# Ensure common helpers are importable when running as a script
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

# Delegate to the existing runner implementation (absolute import)
from physics.thermo_routing.run_thermo_routing import main  # type: ignore

if __name__ == "__main__":
    # If caller didn't supply --spec, use the experiment's default spec
    if not any(arg == "--spec" or arg.startswith("--spec=") for arg in sys.argv[1:]):
        sys.argv.extend(["--spec", str(_DEFAULT_SPEC)])
    sys.exit(main())
