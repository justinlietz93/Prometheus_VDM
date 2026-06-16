"""
CEG Metriplectic Instrument — self-contained package.

Public API::

    from ceg_instrument import run_ceg, CegSpec

    spec = CegSpec(
        grid={"N": 256, "dx": 1.0},
        params={"c": 1.0, "m": 0.5, "D": 1.0, "r": 0.1, "u": 0.0, "m_lap_operator": "spectral"},
        dt=0.02, steps=200,
        seeds=[1, 2, 3],
        lambdas=[0.0, 0.1, 0.5],
        budget=1e-2,
    )
    results = run_ceg(spec)
    print(results["ceg_summary"])
    print(results["gate_ledger_summary"])
"""
from .assisted_echo import CegSpec, run_ceg
from .echo_gates import gate_noether, gate_h_theorem, gate_energy_match, gate_strang_defect
from .echo_metrics import ceg, h_energy_norm_delta

__all__ = [
    "CegSpec",
    "run_ceg",
    "gate_noether",
    "gate_h_theorem",
    "gate_energy_match",
    "gate_strang_defect",
    "ceg",
    "h_energy_norm_delta",
]
