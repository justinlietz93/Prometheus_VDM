
"""
vdm_addons.thermo.lit_tools
----------------------------------
Linear Irreversible Thermodynamics (LIT) helpers for VDM A4-splitting.

This module provides production-grade utilities to:
  * build phenomenological (LIT) matrices for isotropic fluids (heat + viscous blocks),
  * enforce/diagnose Curie principle (zeroing forbidden cross couplings),
  * compute Onsager–Casimir reciprocity residuals for a given parity assignment,
  * evaluate local entropy production density and global rate,
  * assemble a compact gate report for A5/H-theorem alignment near equilibrium.

Design notes
------------
* We represent the LIT relation J = L X in a finite-dimensional basis per gridpoint.
  You provide X (forces) and L (phenomenological matrix), we return gates and metrics.
* Parities: +1 for even under time reversal, −1 for odd (e.g., momentum density is odd).
* Curie masks are conservative: for isotropic media they zero couplings between
  forces/fluxes of different tensorial rank (scalar↔vector, vector↔tensor, ...).

No external deps beyond NumPy.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

# IO routing helpers (project policy)
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
    sys.path.append(str(Path(__file__).resolve().parents[1] / "common"))
    from io_paths import (  # type: ignore
        figure_path_by_tag,
        log_path_by_tag,
        write_log,
        build_slug,
        ensure_dir,
    )

# Optional plotting (guarded)
try:
    import matplotlib.pyplot as plt  # type: ignore
    _HAVE_MPL = True
except Exception:
    _HAVE_MPL = False


# ---------- Core LIT primitives ----------

def entropy_production_density(X: np.ndarray, L: np.ndarray) -> float:
    """
    Local entropy production density σ = X^T L X.
    Requires L symmetric positive semidefinite for A5 compliance.
    """
    X = np.asarray(X, dtype=np.float64).reshape(-1, 1)
    L = np.asarray(L, dtype=np.float64)
    return float((X.T @ L @ X)[0, 0])


def entropy_production_rate(X_field: np.ndarray, L: np.ndarray, dV: float) -> float:
    """
    Global entropy production rate: ∑ σ_i * dV for field of forces X_field (N x m).
    dV is the cell volume (or weight). L is m x m (same for all cells; use block-diag externally if needed).
    """
    X_field = np.asarray(X_field, dtype=np.float64)
    L = np.asarray(L, dtype=np.float64)
    sigmas = np.einsum('...i,ij,...j->...', X_field, L, X_field, optimize=True)
    return float(np.sum(sigmas) * dV)


def onsager_casimir_residual(L: np.ndarray, parity: Sequence[int], ord: str = "fro") -> float:
    """
    Residual for Onsager–Casimir: || L - E L^T E ||, E = diag(parity).
    parity[j] = +1 if variable j is even under time reversal, −1 if odd.
    """
    L = np.asarray(L, dtype=np.float64)
    E = np.diag(np.asarray(parity, dtype=np.float64))
    target = E @ L.T @ E
    R = L - target
    if ord == "fro":
        return float(np.linalg.norm(R, ord="fro"))
    elif ord == "linf":
        return float(np.max(np.abs(R)))
    else:
        raise ValueError("ord must be 'fro' or 'linf'")


# ---------- Curie principle (isotropic media) ----------

TensorRank = int  # 0: scalar, 1: vector, 2: (symmetric) tensor, ...

def curie_mask(ranks_forces: Sequence[TensorRank], ranks_fluxes: Sequence[TensorRank]) -> np.ndarray:
    """
    Build a boolean mask M where M[i, j] = True if coupling flux_i <- force_j is allowed
    by Curie's principle for an isotropic medium (same tensor rank), else False.
    For isotropic systems, different tensorial character does not couple.
    """
    rf = np.asarray(ranks_fluxes, dtype=int).reshape(-1, 1)   # rows: fluxes
    rX = np.asarray(ranks_forces, dtype=int).reshape(1, -1)   # cols: forces
    return (rf == rX)


def apply_curie_zeroing(L: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Zero out entries in L that violate Curie's principle (mask=False).
    """
    L = np.array(L, dtype=np.float64, copy=True)
    L[~mask] = 0.0
    return L


# ---------- Reference builder for isotropic single-component fluid ----------

@dataclass(frozen=True)
class IsotropicFluidCoeffs:
    kappa: float   # thermal conductivity
    eta: float     # shear viscosity
    zeta: float    # bulk viscosity


def build_L_isotropic_fluid(coeffs: IsotropicFluidCoeffs) -> Tuple[np.ndarray, List[int], List[int]]:
    """
    Construct a minimal phenomenological L for isotropic single-component fluid
    in the (heat, viscous) sector with Curie-consistent block structure.

    Basis choice:
      Forces X = [∇(1/T) components (3), Sym(∇v) invariants (2)]  -> ranks: [1,1,1,2,2]
      Fluxes J = [heat flux q components (3), deviatoric stress invariants (2)] -> ranks: [1,1,1,2,2]

    L then is block diagonal:
      q = κ * ∇(1/T)               (vector-vector, 3x3, κ I)
      τ_dev = 2η * Sym(∇v)_dev     (tensor-tensor, 2x2, 2η I)   (bulk handled via scalar invariant below)

    Notes:
      * Bulk viscosity ζ couples the scalar ∇·v to the scalar pressure correction.
        In this reduced basis we include its effect via an effective invariant in the 2x2 block.
      * Cross couplings (vector↔tensor) are zero by Curie in isotropic media.

    Returns (L, ranks_forces, ranks_fluxes).
    """
    k, e, z = coeffs.kappa, coeffs.eta, coeffs.zeta

    # 3 vector components (heat), 2 tensor invariants (deviatoric + volumetric scalar)
    L = np.zeros((5, 5), dtype=np.float64)

    # Heat block (3x3): κ I
    L[0:3, 0:3] = k * np.eye(3)

    # Viscous block (2x2): [2η, 0; 0, ζ_eff]. Represent deviatoric (2η) and volumetric (ζ).
    L[3, 3] = 2.0 * e       # deviatoric invariant
    L[4, 4] = z             # volumetric invariant (bulk)

    ranks_forces = [1, 1, 1, 2, 2]
    ranks_fluxes = [1, 1, 1, 2, 2]

    # Apply Curie zeroing (no-op for this block structure, but keeps invariant)
    mask = curie_mask(ranks_forces, ranks_fluxes)
    L = apply_curie_zeroing(L, mask)

    return L, ranks_forces, ranks_fluxes


# ---------- Gate report ----------

@dataclass
class LITGateReport:
    sigma_min: float
    sigma_max: float
    sigma_any_negative: bool
    onsager_residual_fro: float
    onsager_residual_linf: float
    curie_violations: int


def gate_report(L: np.ndarray,
                X_field: np.ndarray,
                dV: float,
                parity: Sequence[int],
                mask: Optional[np.ndarray] = None) -> LITGateReport:
    """
    Compute a compact gate report:
      * entropy production density extrema and negativity flag,
      * Onsager–Casimir residuals,
      * count of Curie-prohibited nonzeros (if mask provided).
    """
    L = np.asarray(L, dtype=np.float64)
    X_field = np.asarray(X_field, dtype=np.float64)
    parity = list(parity)

    # Entropy production per cell
    sigmas = np.einsum('...i,ij,...j->...', X_field, L, X_field, optimize=True)
    sigma_min = float(np.min(sigmas))
    sigma_max = float(np.max(sigmas))
    sigma_any_negative = bool(np.any(sigmas < -1e-14))

    # Onsager–Casimir
    r_fro = onsager_casimir_residual(L, parity, ord="fro")
    r_inf = onsager_casimir_residual(L, parity, ord="linf")

    # Curie violations
    curie_violations = 0
    if mask is not None:
        nz = np.nonzero(np.abs(L) > 0)[0].shape[0]
        curie_violations = int(np.sum((~mask) & (np.abs(L) > 0)))

    return LITGateReport(
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        sigma_any_negative=sigma_any_negative,
        onsager_residual_fro=r_fro,
        onsager_residual_linf=r_inf,
        curie_violations=curie_violations,
    )


# ---------- Example parity helpers ----------

def parity_even(n: int) -> List[int]:
    return [1] * n


def parity_momentum_coupled(n_vec: int = 3, n_tensor: int = 2) -> List[int]:
    """
    Example parity assignment for the 5D basis used here.
    Heat sector (vector): even; Viscous sector (tensor): even.
    If you include momentum-related variables directly, assign −1 to odd ones.
    """
    return [1] * (n_vec + n_tensor)


# ---------- Boundary entropy-flux monitor (near-equilibrium walls/corners) ----------

class BoundaryEntropyFluxMonitor:
    """
    Track boundary entropy flux time series: J_s = ∮ (q/T)·n dA (plus optional extra terms).
    This is a near-equilibrium LIT helper for wall/corner tests (e.g., OQ-021).
    Units must be consistent with UNITS_NORMALIZATION canon.
    """
    def __init__(self, tol: float = 1e-12) -> None:
        self.t: list[float] = []
        self.Js: list[float] = []
        self._time: float = 0.0
        self.tol = float(tol)

    def update_from_heat_flux(
        self,
        q_dot_n: float,
        T_face: float,
        area: float,
        dt: float,
        sign: float = +1.0,
    ) -> Dict[str, float]:
        """
        Increment from a boundary face contribution.
        Arguments:
          - q_dot_n: heat flux dot outward normal (power per area)
          - T_face: face temperature
          - area: face area contribution
          - dt: timestep
          - sign: +1 for outward normal as defined; use -1 to accumulate inward flux
        Entropy flux rate across boundary face: sign * (q·n)/(T) * area
        """
        qn = float(q_dot_n)
        T = float(T_face)
        A = float(area)
        dt = float(dt)

        # Guard T to avoid divide-by-zero; units and scaling follow canon
        Js_inst = sign * (qn / max(T, 1e-300)) * A
        self._time += dt
        self.t.append(self._time)
        self.Js.append(Js_inst)
        return {"t": self._time, "Js": Js_inst}

    def snapshot(self) -> Dict[str, float]:
        return {
            "t": self.t[-1] if self.t else 0.0,
            "Js": self.Js[-1] if self.Js else 0.0,
            "n": float(len(self.t)),
            "tol": self.tol,
        }

    def gates(self) -> Dict[str, float]:
        # No fixed sign gate in general; report descriptive stats
        if self.Js:
            js_min = float(np.min(self.Js))
            js_max = float(np.max(self.Js))
            js_mean = float(np.mean(self.Js))
        else:
            js_min = js_max = js_mean = 0.0
        return {"Js_min": js_min, "Js_max": js_max, "Js_mean": js_mean}

    def write_artifacts(
        self,
        domain: str,
        name: str,
        tag: Optional[str],
        meta: Optional[Dict[str, any]] = None,
        failed: bool = False,
        write_png: bool = True,
    ) -> Dict[str, str]:
        """
        Write JSON summary + CSV time series and optional PNG.
        Uses repository io_paths routing and standards.
        """
        slug = build_slug(name, tag)
        json_path = log_path_by_tag(domain, f"{name}_summary", tag, failed=failed, type="json")
        csv_path = log_path_by_tag(domain, f"{name}_series", tag, failed=failed, type="csv")

        summary = {
            "slug": slug,
            "domain": domain,
            "n": len(self.t),
            "tol": self.tol,
            "gates": self.gates(),
            "meta": meta or {},
            "series_paths": {"csv": str(csv_path)},
        }
        write_log(json_path, summary)

        # CSV time series
        ensure_dir(Path(csv_path).parent)
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            import csv
            writer = csv.DictWriter(f, fieldnames=["t", "Js"])
            writer.writeheader()
            for ti, ji in zip(self.t, self.Js):
                writer.writerow({"t": ti, "Js": ji})

        fig_path_str = ""
        if write_png and _HAVE_MPL and self.t:
            fig_path = figure_path_by_tag(domain, f"{name}_panel", tag, failed=failed)
            try:
                plt.figure(figsize=(6.4, 3.0), dpi=150)
                plt.plot(self.t, self.Js, label="Boundary entropy flux rate J_s")
                plt.xlabel("t")
                plt.ylabel("J_s")
                plt.grid(True, alpha=0.25)
                plt.title(slug)
                plt.tight_layout()
                plt.savefig(fig_path, bbox_inches="tight")
                plt.close()
                fig_path_str = str(fig_path)
            except Exception:
                fig_path_str = ""

        return {"json": str(json_path), "csv": str(csv_path), "png": fig_path_str}


# ---------- Artifact writer for LIT gate report ----------

def write_lit_gate_artifacts(
    domain: str,
    name: str,
    tag: Optional[str],
    L: np.ndarray,
    X_field: np.ndarray,
    dV: float,
    parity: Sequence[int],
    mask: Optional[np.ndarray] = None,
    meta: Optional[Dict[str, any]] = None,
    failed: bool = False,
) -> Dict[str, str]:
    """
    Convenience writer: compute LIT gate report and write JSON with KPI-aligned keys.
    KPIs follow VALIDATION_METRICS canon names:
      - kpi-onsager-resid-fro
      - kpi-onsager-resid-linf
      - kpi-curie-violations
    """
    rep = gate_report(L, X_field, dV, parity, mask)

    payload = {
        "slug": build_slug(name, tag),
        "domain": domain,
        "kpi-onsager-resid-fro": rep.onsager_residual_fro,
        "kpi-onsager-resid-linf": rep.onsager_residual_linf,
        "kpi-curie-violations": rep.curie_violations,
        "sigma_min": rep.sigma_min,
        "sigma_max": rep.sigma_max,
        "sigma_any_negative": rep.sigma_any_negative,
        "meta": meta or {},
    }
    json_path = log_path_by_tag(domain, f"{name}_lit_gate", tag, failed=failed, type="json")
    write_log(json_path, payload)
    return {"json": str(json_path)}


__all__ = [
    "entropy_production_density",
    "entropy_production_rate",
    "onsager_casimir_residual",
    "curie_mask",
    "apply_curie_zeroing",
    "IsotropicFluidCoeffs",
    "build_L_isotropic_fluid",
    "LITGateReport",
    "gate_report",
    "parity_even",
    "parity_momentum_coupled",
    "BoundaryEntropyFluxMonitor",
    "write_lit_gate_artifacts",
]
