# Derivation/code/common/instrument_helpers/boundaries/gb_emission_threshold.py
"""
Single-responsibility helper: Estimate the asymmetric dislocation-emission threshold p0* under
oscillating load and emit certification artifacts.

Scope
- Input (per run at a fixed amplitude p0):
  * emission_counts: list/array of ints per cycle (emitted partials count)
  * delta_E_ex: list/array of floats per cycle (net GB excess-energy change for that cycle)
  * p0: scalar amplitude (units consistent across runs, e.g., MPa)
- Aggregation across runs at multiple p0:
  * Compute per-run event fraction f_event = mean( (emission_count>=1) AND (delta_E_ex<0) )
  * Determine p0_star = smallest p0 with f_event >= f_req (default 0.5)
- Outputs:
  - JSON summary with per-run stats, estimated p0_star, and optional gate decision
  - CSV table of {p0, n_cycles, f_event, n_event, event_criterion}
  - Optional PNG plot of f_event vs p0 with criterion line

Gating (no hard-coded claims; thresholds configurable):
- If target_p0 and rel_tol are provided, compute |p0_star/target_p0 - 1| <= rel_tol.
- Default criterion fraction f_req=0.5 matches the standards note for asymmetric emission.

Canon discipline
- Relates to EQUATIONS anchor to register: [VDM-E-161](../../../Derivation/EQUATIONS.md#vdm-e-161)
- Validation gate lives in: [Derivation/VALIDATION_METRICS.md](../../../Derivation/VALIDATION_METRICS.md)
- Do not duplicate source equations; this is a meter primitive for boundary instruments.

References
- Source extraction: [Nonequilibrium-grain-boundaries.md](../../../Derivation/References/Boundaries/Nonequilibrium-grain-boundaries.md)
- Standards map: [Boundaries_Upgrade_Map.md](../../../docs/misc-standards/Boundaries_Upgrade_Map.md)
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import csv
import json
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
class EmissionRunStats:
    p0: float
    n_cycles: int
    n_event: int
    f_event: float
    criterion: str  # description of the event condition used
    meta: Dict[str, Any]


@dataclass
class ThresholdEstimate:
    p0_star: Optional[float]
    f_req: float
    found: bool
    idx: Optional[int]  # index in sorted runs if found


@dataclass
class ThresholdGate:
    threshold_ok: Optional[bool]
    target_p0: Optional[float]
    rel_tol: Optional[float]
    rel_err: Optional[float]
    notes: str


class GBEmissionThresholdEstimator:
    """
    Aggregate per-amplitude runs and estimate the minimal amplitude p0* producing asymmetric
    emission events at or above the required fraction of cycles.

    Configuration
    - f_req: required fraction of cycles with (emission_count>=1) AND (delta_E_ex<0), default 0.5
    - target_p0: optional expected threshold for a baseline geometry (for gate evaluation)
    - rel_tol: optional relative tolerance for |p0_star/target_p0 - 1|, e.g. 0.25
    - event_condition: "emit_and_drop" (default) or "emit_only"
        * "emit_and_drop": event if (emission>=1) AND (ΔE_ex<0)
        * "emit_only": event if (emission>=1) (diagnostic variant)
    """

    def __init__(
        self,
        *,
        f_req: float = 0.5,
        target_p0: Optional[float] = None,
        rel_tol: Optional[float] = 0.25,
        event_condition: str = "emit_and_drop",
    ) -> None:
        self.f_req = float(f_req)
        self.target_p0 = float(target_p0) if target_p0 is not None else None
        self.rel_tol = float(rel_tol) if rel_tol is not None else None
        if event_condition not in ("emit_and_drop", "emit_only"):
            raise ValueError("event_condition must be 'emit_and_drop' or 'emit_only'")
        self.event_condition = event_condition

        self._runs: List[EmissionRunStats] = []

    @staticmethod
    def _run_stats(
        p0: float,
        emission_counts: Any,
        delta_E_ex: Any,
        event_condition: str,
    ) -> EmissionRunStats:
        ec = np.asarray(emission_counts, dtype=np.int64).reshape(-1)
        dE = _as64(delta_E_ex).reshape(-1)
        if ec.size != dE.size or ec.size == 0:
            raise ValueError("emission_counts and delta_E_ex must have the same non-zero length")

        if event_condition == "emit_and_drop":
            mask_event = (ec >= 1) & (dE < 0.0)
            crit = "(emission>=1) AND (ΔE_ex<0)"
        else:
            mask_event = (ec >= 1)
            crit = "(emission>=1)"

        n_cycles = int(ec.size)
        n_event = int(np.count_nonzero(mask_event))
        f_event = float(n_event / max(1, n_cycles))

        return EmissionRunStats(
            p0=float(p0),
            n_cycles=n_cycles,
            n_event=n_event,
            f_event=f_event,
            criterion=crit,
            meta={},
        )

    def add_run(self, p0: float, emission_counts: Any, delta_E_ex: Any) -> EmissionRunStats:
        """Add a single-amplitude run and return its statistics."""
        stats = self._run_stats(p0, emission_counts, delta_E_ex, self.event_condition)
        self._runs.append(stats)
        return stats

    def runs(self) -> List[EmissionRunStats]:
        """Access accumulated per-run stats (unsorted)."""
        return list(self._runs)

    def estimate_threshold(self) -> ThresholdEstimate:
        """Estimate p0_star as smallest p0 with f_event >= f_req. Returns not found if criterion is unmet."""
        if not self._runs:
            return ThresholdEstimate(p0_star=None, f_req=self.f_req, found=False, idx=None)

        # Sort by p0 ascending
        runs_sorted = sorted(self._runs, key=lambda r: r.p0)
        for i, r in enumerate(runs_sorted):
            if r.f_event >= self.f_req:
                return ThresholdEstimate(p0_star=r.p0, f_req=self.f_req, found=True, idx=i)
        return ThresholdEstimate(p0_star=None, f_req=self.f_req, found=False, idx=None)

    def gate(self, est: ThresholdEstimate) -> ThresholdGate:
        """Evaluate threshold gate if a target is configured; otherwise return None-like fields."""
        if not est.found or self.target_p0 is None or self.rel_tol is None:
            return ThresholdGate(
                threshold_ok=None, target_p0=self.target_p0, rel_tol=self.rel_tol, rel_err=None, notes="no_gate"
            )
        if self.target_p0 == 0.0:
            return ThresholdGate(
                threshold_ok=False, target_p0=self.target_p0, rel_tol=self.rel_tol, rel_err=None, notes="invalid_target"
            )
        rel_err = abs(float(est.p0_star) / self.target_p0 - 1.0) if est.p0_star is not None else None
        ok = (rel_err is not None) and (rel_err <= self.rel_tol)
        return ThresholdGate(
            threshold_ok=bool(ok),
            target_p0=self.target_p0,
            rel_tol=self.rel_tol,
            rel_err=None if rel_err is None else float(rel_err),
            notes="gate-gb-asym-threshold",
        )

    def write_artifacts(
        self,
        *,
        domain: str = "materials/gb",
        name: str = "gb_emission_threshold",
        tag: Optional[str] = None,
        failed: bool = False,
        write_png: bool = True,
    ) -> Dict[str, str]:
        """Emit JSON summary, CSV table, and optional PNG plot of f_event vs p0."""
        # Prepare data (sorted by p0)
        runs_sorted = sorted(self._runs, key=lambda r: r.p0)
        p0_vals = [r.p0 for r in runs_sorted]
        f_vals = [r.f_event for r in runs_sorted]

        est = self.estimate_threshold()
        gate_summary = self.gate(est)

        slug = build_slug(name, tag)
        json_path = log_path_by_tag(domain, f"{name}_summary", tag, failed=failed, type="json")
        csv_path = log_path_by_tag(domain, f"{name}_table", tag, failed=failed, type="csv")

        summary = {
            "slug": slug,
            "domain": domain,
            "canon_anchor": "VDM-E-161",
            "f_req": self.f_req,
            "threshold_estimate": asdict(est),
            "gate": asdict(gate_summary),
            "runs": [asdict(r) for r in runs_sorted],
            "series_paths": {"csv": str(csv_path)},
        }
        write_log(json_path, summary)

        ensure_dir(Path(csv_path).parent)
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["p0", "n_cycles", "n_event", "f_event", "criterion"])
            w.writeheader()
            for r in runs_sorted:
                w.writerow(
                    {
                        "p0": float(r.p0),
                        "n_cycles": int(r.n_cycles),
                        "n_event": int(r.n_event),
                        "f_event": float(r.f_event),
                        "criterion": r.criterion,
                    }
                )

        fig_path_str = ""
        if write_png and _HAVE_MPL and len(p0_vals) > 0:
            fig_path = figure_path_by_tag(domain, f"{name}_plot", tag, failed=failed)
            try:
                import numpy as _np  # local alias to avoid shadowing
                plt.figure(figsize=(6.0, 4.0), dpi=150)
                plt.plot(p0_vals, f_vals, "o-", color="#1f77b4", label="f_event")
                plt.axhline(self.f_req, color="#d62728", lw=1.5, ls="--", label=f"f_req={self.f_req:.2f}")
                if est.found and est.p0_star is not None:
                    plt.axvline(est.p0_star, color="#2ca02c", lw=1.5, ls=":", label=f"p0*≈{est.p0_star:.3g}")
                if gate_summary.threshold_ok is not None and gate_summary.target_p0 is not None:
                    t = gate_summary.target_p0
                    if self.rel_tol is not None:
                        plt.axvspan(t * (1 - self.rel_tol), t * (1 + self.rel_tol), color="#ffbb78", alpha=0.25, label="tolerance")
                        plt.axvline(t, color="#ff7f0e", lw=1.2, ls="-.", label=f"target={t:.3g}")
                plt.xlabel("p0 (units as provided)")
                plt.ylabel("f_event (fraction)")
                plt.grid(True, alpha=0.25)
                plt.title(slug)
                plt.legend()
                plt.tight_layout()
                plt.savefig(fig_path, bbox_inches="tight")
                plt.close()
                fig_path_str = str(fig_path)
            except Exception:
                fig_path_str = ""

        return {"json": str(json_path), "csv": str(csv_path), "png": fig_path_str}


__all__ = [
    "GBEmissionThresholdEstimator",
    "EmissionRunStats",
    "ThresholdEstimate",
    "ThresholdGate",
]