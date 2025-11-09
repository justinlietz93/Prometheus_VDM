# Derivation/code/common/instrument_helpers/boundaries/gb_cycle_lyapunov.py
"""
Single-responsibility helper: Monitor GB excess-energy Lyapunov trend over loading cycles.

Purpose
- Certify monotone-decrease behavior (metric-limb Lyapunov) of GB excess energy E_ex over cycles
  under oscillatory loading, per standards in Boundaries_Upgrade_Map.
- Emit JSON/CSV/PNG artifacts and evaluate gates:
  * median per-cycle ΔE_ex <= 0 within tolerance
  * total fractional drop after N cycles ≥ min_drop_frac (e.g., 0.15)

Inputs
- Per call: the cycle index and E_ex for that cycle (units consistent across the dataset).
- Optional: amplitude tag p0 (for provenance), and any meta dict.

Outputs
- JSON summary with gate decisions and configuration
- CSV with (cycle, E_ex, dE_ex)
- Optional PNG plot E_ex vs cycle + ΔE_ex trend

Canon discipline
- Anchors to register: [VDM-E-162](../../../Derivation/EQUATIONS.md#vdm-e-162) (cycle Lyapunov monotonicity for E_ex)
- Reference mapping: [Boundaries_Upgrade_Map.md](../../../docs/misc-standards/Boundaries_Upgrade_Map.md)
- Do not paste closed-form equations; this helper is a meter primitive only.

Usage
- Import into instruments (e.g., materials/gb_relax_ust) to certify the per-cycle Lyapunov gate.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any

import csv
import json
import math
import numpy as np

# Optional plotting (guarded)
try:
    import matplotlib.pyplot as plt  # type: ignore
    _HAVE_MPL = True
except Exception:
    _HAVE_MPL = False

# IO routing per repository policy
try:
    from common.io_paths import (
        figure_path_by_tag,
        log_path_by_tag,
        write_log,
        build_slug,
        ensure_dir,
    )
except Exception:
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[2] / "common"))
    from io_paths import (  # type: ignore
        figure_path_by_tag,
        log_path_by_tag,
        write_log,
        build_slug,
        ensure_dir,
    )


ND = np.ndarray


def _as64(x: Any) -> ND:
    return np.asarray(x, dtype=np.float64)


@dataclass
class LyapunovGateSummary:
    median_delta_ok: bool
    total_drop_ok: bool
    median_delta: float
    min_delta: float
    total_drop_frac: float
    tol: float
    min_drop_frac: float
    notes: str


class GBLyapunovCycleMonitor:
    """
    Monitor and certify Lyapunov-like decrease of GB excess energy over cycles.

    Configuration
    - tol: numerical tolerance for non-increase (default 1e-12)
    - min_drop_frac: required (E_ex[0] - E_ex[-1]) / E_ex[0] ≥ min_drop_frac (default 0.15)

    Methods
    - add(cycle:int, E_ex:float): append a measurement for a cycle
    - gates(): compute gate decisions (median ΔE_ex ≤ tol and total drop fraction ≥ min_drop_frac)
    - write_artifacts(...): write JSON/CSV/PNG artifacts via io_paths
    """

    def __init__(self, *, tol: float = 1e-12, min_drop_frac: float = 0.15) -> None:
        self.cycle: List[int] = []
        self.E: List[float] = []
        self.tol = float(tol)
        self.min_drop_frac = float(min_drop_frac)

    def add(self, cycle: int, E_ex: float) -> None:
        """Record E_ex for given cycle (0-based or 1-based; preserved as provided)."""
        self.cycle.append(int(cycle))
        self.E.append(float(E_ex))

    def _deltas(self) -> ND:
        if len(self.E) < 2:
            return _as64([])
        e = _as64(self.E)
        return e[1:] - e[:-1]

    def snapshot(self) -> Dict[str, Any]:
        d = self._deltas()
        return {
            "n": len(self.E),
            "E0": (self.E[0] if self.E else None),
            "E_last": (self.E[-1] if self.E else None),
            "median_delta": (float(np.median(d)) if d.size else None),
            "min_delta": (float(np.min(d)) if d.size else None),
            "tol": self.tol,
            "min_drop_frac": self.min_drop_frac,
        }

    def gates(self) -> LyapunovGateSummary:
        d = self._deltas()
        if d.size == 0 or len(self.E) < 2:
            # Insufficient data → conservative FAIL on both
            return LyapunovGateSummary(
                median_delta_ok=False,
                total_drop_ok=False,
                median_delta=float("nan"),
                min_delta=float("nan"),
                total_drop_frac=float("nan"),
                tol=self.tol,
                min_drop_frac=self.min_drop_frac,
                notes="insufficient_cycles",
            )
        median_delta = float(np.median(d))
        min_delta = float(np.min(d))
        # Non-increase within tol means median ≤ tol (allow tiny positive numerical drift)
        median_ok = (median_delta <= self.tol)
        E0 = float(self.E[0])
        Elast = float(self.E[-1])
        total_drop = E0 - Elast
        total_drop_frac = (total_drop / E0) if abs(E0) > 1e-300 else float("nan")
        drop_ok = (not math.isnan(total_drop_frac)) and (total_drop_frac >= self.min_drop_frac)
        return LyapunovGateSummary(
            median_delta_ok=bool(median_ok),
            total_drop_ok=bool(drop_ok),
            median_delta=median_delta,
            min_delta=min_delta,
            total_drop_frac=float(total_drop_frac if not math.isnan(total_drop_frac) else -1.0),
            tol=self.tol,
            min_drop_frac=self.min_drop_frac,
            notes="gate-gb-lyapunov",
        )

    def write_artifacts(
        self,
        *,
        domain: str = "materials/gb",
        name: str = "gb_cycle_lyapunov",
        tag: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
        failed: bool = False,
        write_png: bool = True,
    ) -> Dict[str, str]:
        """Emit JSON summary, CSV table, and optional PNG E_ex vs cycle plot."""
        slug = build_slug(name, tag)
        json_path = log_path_by_tag(domain, f"{name}_summary", tag, failed=failed, type="json")
        csv_path = log_path_by_tag(domain, f"{name}_series", tag, failed=failed, type="csv")

        g = self.gates()
        summary = {
            "slug": slug,
            "domain": domain,
            "canon_anchor": "VDM-E-162",
            "n_cycles": len(self.E),
            "gates": asdict(g),
            "meta": meta or {},
            "series_paths": {"csv": str(csv_path)},
        }
        write_log(json_path, summary)

        ensure_dir(Path(csv_path).parent)
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["cycle", "E_ex", "dE_ex"])
            w.writeheader()
            d = self._deltas()
            # Emit aligned rows; first row has no delta
            if self.E:
                w.writerow({"cycle": int(self.cycle[0]), "E_ex": float(self.E[0]), "dE_ex": ""})
            for idx in range(1, len(self.E)):
                w.writerow({"cycle": int(self.cycle[idx]), "E_ex": float(self.E[idx]), "dE_ex": float(d[idx - 1])})

        fig_path_str = ""
        if write_png and _HAVE_MPL and len(self.E) >= 1:
            fig_path = figure_path_by_tag(domain, f"{name}_panel", tag, failed=failed)
            try:
                import matplotlib as mpl  # noqa: F401
                plt.figure(figsize=(6.4, 3.6), dpi=150)
                ax1 = plt.gca()
                ax1.plot(self.cycle, self.E, "o-", color="#1f77b4", label="E_ex(cycle)")
                ax1.set_xlabel("cycle")
                ax1.set_ylabel("E_ex")
                ax1.grid(True, alpha=0.25)
                # Annotate median Δ and total drop
                gsum = self.gates()
                txt = f"median Δ={gsum.median_delta:.3g}, drop={gsum.total_drop_frac:.3g}"
                ax1.set_title(slug + "  [" + txt + "]")
                plt.tight_layout()
                plt.savefig(fig_path, bbox_inches="tight")
                plt.close()
                fig_path_str = str(fig_path)
            except Exception:
                fig_path_str = ""

        return {"json": str(json_path), "csv": str(csv_path), "png": fig_path_str}


__all__ = ["GBLyapunovCycleMonitor", "LyapunovGateSummary"]