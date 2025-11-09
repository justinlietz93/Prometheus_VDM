# Derivation/code/common/instrument_helpers/boundaries/gb_energy_gamma2_fitter.py
"""
Single-responsibility helper: Fit the GB excess-energy law E_ex ≈ A * gamma^2,
emit artifacts, and evaluate gates.

Scope
- Input: arrays gamma (dimensionless shear), E_ex (J/m^2 per-GB-area or normalized)
- Model: E_ex = A * (gamma^2) (optionally allow intercept for diagnostics)
- Outputs:
  - JSON fit summary and gate decisions via io_paths
  - CSV table with {gamma, gamma2, E_ex, E_hat}
  - Optional PNG overlay (scatter vs fit line)

Canon discipline
- Equations anchor to register: [VDM-E-160](../../../Derivation/EQUATIONS.md#vdm-e-160)
- Validation gates live in: [Derivation/VALIDATION_METRICS.md](../../../Derivation/VALIDATION_METRICS.md)
- Do not duplicate source equations in this helper; this is a meter instrument primitive.

Intended usage
- Imported by instruments (e.g., materials/gb_relax_ust) to certify γ^2 scaling.
- Not a standalone runner.

References
- Source extraction: [Nonequilibrium-grain-boundaries.md](../../../Derivation/References/Boundaries/Nonequilibrium-grain-boundaries.md)
- Standards map: [Boundaries_Upgrade_Map.md](../../../docs/misc-standards/Boundaries_Upgrade_Map.md)
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional, Any, Tuple

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
class Gamma2FitResult:
    n: int
    use_origin: bool
    A_hat: float
    intercept_hat: float
    R2: float
    sse: float
    sst: float
    slope_CI95: Optional[Tuple[float, float]]
    intercept_CI95: Optional[Tuple[float, float]]
    meta: Dict[str, Any]


@dataclass
class Gamma2GateSummary:
    r2_ok: bool
    slope_ok: Optional[bool]
    R2: float
    A_hat: float
    slope_target: Optional[float]
    slope_rel_tol: Optional[float]
    notes: str


class GBExcessEnergyGamma2Fitter:
    """
    Fit E_ex ≈ A * gamma^2 and emit artifacts + gate decisions.

    Parameters
    - tol_R2: minimum R^2 for acceptance (default 0.98)
    - slope_target: expected A (unit-consistent) for a baseline material (optional)
    - slope_rel_tol: relative tolerance band for A_hat vs slope_target (e.g. 0.20 for ±20%)
    - enforce_origin: if True, fit through origin (intercept=0); else include intercept for diagnostics
    - material_tag: optional label for logs

    Anchors
    - VDM-E-160: GB excess energy γ² law
    - See VALIDATION_METRICS gates: gate-gb-gamma2-law
    """

    def __init__(
        self,
        *,
        tol_R2: float = 0.98,
        slope_target: Optional[float] = None,
        slope_rel_tol: Optional[float] = 0.20,
        enforce_origin: bool = True,
        material_tag: Optional[str] = None,
    ) -> None:
        self.tol_R2 = float(tol_R2)
        self.slope_target = float(slope_target) if slope_target is not None else None
        self.slope_rel_tol = float(slope_rel_tol) if slope_rel_tol is not None else None
        self.enforce_origin = bool(enforce_origin)
        self.material_tag = material_tag or ""

    def fit(self, gamma: Any, E_ex: Any) -> Gamma2FitResult:
        """Fit E_ex vs gamma^2 under the configured model."""
        g = _as64(gamma).reshape(-1)
        y = _as64(E_ex).reshape(-1)
        if g.size != y.size or g.size < 2:
            raise ValueError("gamma and E_ex must have the same length ≥ 2")

        x = g ** 2
        n = int(x.size)

        if self.enforce_origin:
            # OLS through origin: slope = (x^T y)/(x^T x), intercept = 0
            denom = float(np.dot(x, x))
            if denom <= 0.0:
                raise ValueError("Degenerate gamma^2 data (sum x^2 == 0)")
            A_hat = float(np.dot(x, y) / denom)
            b_hat = 0.0
            yhat = A_hat * x
            # Residuals and variance estimate
            resid = y - yhat
            sse = float(np.dot(resid, resid))
            # Use conventional SST about mean of y
            ybar = float(np.mean(y))
            sst = float(np.dot(y - ybar, y - ybar))
            R2 = 0.0 if sst <= 0.0 else max(0.0, 1.0 - sse / sst)

            # Approximate 95% CI for slope with intercept fixed at 0:
            # Var(A) ≈ sigma^2 / (x^T x), with sigma^2 = sse/(n-1) in this model
            slope_CI = None
            intercept_CI = None
            dof = max(1, n - 1)
            sigma2 = sse / dof
            if denom > 0.0 and n >= 3:
                se = math.sqrt(max(0.0, sigma2 / denom))
                z = 1.96  # normal approx
                slope_CI = (A_hat - z * se, A_hat + z * se)

        else:
            # Full OLS with intercept
            X = np.column_stack([x, np.ones_like(x)])
            # Normal equations: beta = (X^T X)^(-1) X^T y
            XtX = X.T @ X
            try:
                beta = np.linalg.solve(XtX, X.T @ y)
            except np.linalg.LinAlgError:
                beta = np.linalg.pinv(XtX) @ (X.T @ y)
            A_hat = float(beta[0])
            b_hat = float(beta[1])
            yhat = X @ beta
            resid = y - yhat
            sse = float(np.dot(resid, resid))
            ybar = float(np.mean(y))
            sst = float(np.dot(y - ybar, y - ybar))
            R2 = 0.0 if sst <= 0.0 else max(0.0, 1.0 - sse / sst)

            # Approximate 95% CI for slope/intercept
            dof = max(1, n - 2)
            sigma2 = sse / dof
            XtX_inv = np.linalg.pinv(XtX)
            var_beta = sigma2 * XtX_inv
            z = 1.96
            se_slope = math.sqrt(max(0.0, float(var_beta[0, 0])))
            se_intercept = math.sqrt(max(0.0, float(var_beta[1, 1])))
            slope_CI = (A_hat - z * se_slope, A_hat + z * se_slope)
            intercept_CI = (b_hat - z * se_intercept, b_hat + z * se_intercept)

        meta = {
            "enforce_origin": self.enforce_origin,
            "material_tag": self.material_tag,
            "canon_anchor": "VDM-E-160",
            "notes": "Fit performed in double precision; CI via normal approximation.",
        }
        return Gamma2FitResult(
            n=n,
            use_origin=self.enforce_origin,
            A_hat=A_hat,
            intercept_hat=b_hat,
            R2=R2,
            sse=sse,
            sst=sst,
            slope_CI95=None if slope_CI is None else (float(slope_CI[0]), float(slope_CI[1])),
            intercept_CI95=None if intercept_CI is None else (float(intercept_CI[0]), float(intercept_CI[1])),
            meta=meta,
        )

    def gates(self, fit: Gamma2FitResult) -> Gamma2GateSummary:
        """Evaluate acceptance gates against configured thresholds."""
        r2_ok = bool(fit.R2 >= self.tol_R2)
        slope_ok = None
        notes = ""
        if self.slope_target is not None and self.slope_rel_tol is not None:
            if self.slope_target == 0.0:
                slope_ok = False
                notes = "slope_target=0 invalid"
            else:
                rel_err = abs(fit.A_hat / self.slope_target - 1.0)
                slope_ok = bool(rel_err <= self.slope_rel_tol)
                notes = f"rel_err={rel_err:.3g}"
        return Gamma2GateSummary(
            r2_ok=r2_ok,
            slope_ok=slope_ok,
            R2=float(fit.R2),
            A_hat=float(fit.A_hat),
            slope_target=self.slope_target,
            slope_rel_tol=self.slope_rel_tol,
            notes=notes,
        )

    def write_artifacts(
        self,
        gamma: Any,
        E_ex: Any,
        fit: Gamma2FitResult,
        gates: Gamma2GateSummary,
        *,
        domain: str = "materials/gb",
        name: str = "gb_gamma2_fit",
        tag: Optional[str] = None,
        failed: bool = False,
        write_png: bool = True,
    ) -> Dict[str, str]:
        """Emit JSON summary, CSV table, and optional PNG overlay."""
        g = _as64(gamma).reshape(-1)
        y = _as64(E_ex).reshape(-1)
        x = g ** 2
        if fit.use_origin:
            yhat = fit.A_hat * x
        else:
            yhat = fit.A_hat * x + fit.intercept_hat

        slug = build_slug(name, tag)
        json_path = log_path_by_tag(domain, f"{name}_summary", tag, failed=failed, type="json")
        csv_path = log_path_by_tag(domain, f"{name}_table", tag, failed=failed, type="csv")

        summary = {
            "slug": slug,
            "domain": domain,
            "model": "E_ex = A * gamma^2" + ("" if fit.use_origin else " + b"),
            "fit": asdict(fit),
            "gates": asdict(gates),
            "series_paths": {"csv": str(csv_path)},
        }
        write_log(json_path, summary)

        ensure_dir(Path(csv_path).parent)
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["gamma", "gamma2", "E_ex", "E_hat"])
            w.writeheader()
            for gi, xi, yi, yh in zip(g, x, y, yhat):
                w.writerow({"gamma": float(gi), "gamma2": float(xi), "E_ex": float(yi), "E_hat": float(yh)})

        fig_path_str = ""
        if write_png and _HAVE_MPL:
            fig_path = figure_path_by_tag(domain, f"{name}_overlay", tag, failed=failed)
            try:
                plt.figure(figsize=(6.0, 4.0), dpi=150)
                plt.scatter(x, y, s=20, c="#1f77b4", alpha=0.9, label="data")
                x_line = np.linspace(float(np.min(x)), float(np.max(x)), 200) if x.size else np.linspace(0.0, 1.0, 2)
                y_line = fit.A_hat * x_line + (0.0 if fit.use_origin else fit.intercept_hat)
                plt.plot(x_line, y_line, c="#d62728", lw=2.0, label="fit")
                plt.xlabel("gamma^2 (-)")
                plt.ylabel("E_ex (J/m^2 or normalized)")
                gate_txt = f"R^2={fit.R2:.4f}"
                if gates.slope_ok is not None and self.slope_target is not None:
                    gate_txt += f", A={fit.A_hat:.3g} vs {self.slope_target:.3g}"
                plt.title(slug + "  [" + gate_txt + "]")
                plt.grid(True, alpha=0.25)
                plt.legend()
                plt.tight_layout()
                plt.savefig(fig_path, bbox_inches="tight")
                plt.close()
                fig_path_str = str(fig_path)
            except Exception:
                fig_path_str = ""

        return {"json": str(json_path), "csv": str(csv_path), "png": fig_path_str}


__all__ = ["GBExcessEnergyGamma2Fitter", "Gamma2FitResult", "Gamma2GateSummary"]