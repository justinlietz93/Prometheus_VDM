# Derivation/code/common/instrument_helpers/boundaries/gb_moire_contrast.py
"""
Single-responsibility helper: Compute a Moiré-contrast index from a 2D field/image and emit artifacts.

Context
- Nazarov & Murzaev (2018) visualize long-range internal stress via Moiré overlays.
- This helper quantifies that visual diagnostic as a reproducible observable for GB meters.

Scope (no heavy deps; NumPy + optional Matplotlib)
- Input: 2D array F[y,x] (e.g., per-atom potential energy, grayscale overlay, or lattice indicator)
- Compute 2D power spectrum and its radial average (PSD(k))
- Detect strongest non-DC peak k_peak and report contrast metrics:
  * moire_contrast = PSD(k_peak) / median(PSD over k>0)
  * ring_energy_frac = (sum PSD in an annulus around k_peak) / (sum PSD over k>0)
- Emit artifacts:
  - JSON summary with metrics and detection parameters
  - CSV table (k_radius, PSD_radial)
  - Optional PNG plot of radial PSD with marked k_peak and band

Canon discipline
- EQUATIONS anchor to register: [VDM-E-163](../../../Derivation/EQUATIONS.md#vdm-e-163) (Moiré-contrast observable)
- Do not duplicate equations; this helper is a meter primitive for import by instruments.

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


def _radial_bins(ny: int, nx: int) -> Tuple[ND, ND]:
    """Return (r, r_indices) where r is the radius for each pixel in frequency space (centered)."""
    cy = (ny - 1) / 2.0
    cx = (nx - 1) / 2.0
    y = np.arange(ny) - cy
    x = np.arange(nx) - cx
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X * X + Y * Y)
    return R, np.rint(R).astype(np.int64)


def _radial_average(psd2d: ND) -> Tuple[ND, ND]:
    """Compute radial average of a 2D PSD (fftshift-aligned). Returns (k, psd_radial)."""
    ny, nx = psd2d.shape
    R, Ri = _radial_bins(ny, nx)
    r_max = int(np.max(Ri))
    psd_rad = np.zeros(r_max + 1, dtype=np.float64)
    counts = np.zeros(r_max + 1, dtype=np.int64)
    # Accumulate
    for r in range(r_max + 1):
        mask = (Ri == r)
        c = int(np.count_nonzero(mask))
        if c > 0:
            psd_rad[r] = float(np.sum(psd2d[mask]) / c)
            counts[r] = c
        else:
            psd_rad[r] = 0.0
            counts[r] = 0
    k = np.arange(r_max + 1, dtype=np.float64)
    return k, psd_rad


@dataclass
class MoireContrastResult:
    k_peak: float
    moire_contrast: float
    ring_energy_frac: float
    k_band: Tuple[float, float]
    dc_power: float
    total_power_nz: float
    meta: Dict[str, Any]


class GBMoireContrast:
    """
    Compute Moiré-contrast metrics from a 2D field.

    Configuration
    - detrend: if True, subtract mean before PSD (default True)
    - band_rel_width: relative band half-width around k_peak for ring energy (default 0.20 → ±20%)
    - kmin_exclude: exclude first k bins up to this value from peak search (default 1 to skip DC lobe)
    """

    def __init__(
        self,
        *,
        detrend: bool = True,
        band_rel_width: float = 0.20,
        kmin_exclude: int = 1,
    ) -> None:
        self.detrend = bool(detrend)
        self.band_rel_width = float(band_rel_width)
        self.kmin_exclude = int(kmin_exclude)

    def compute(self, F: Any) -> MoireContrastResult:
        """Compute contrast metrics (no artifacts)."""
        img = _as64(F)
        if img.ndim != 2:
            raise ValueError("F must be a 2D array")
        ny, nx = img.shape

        # Detrend by mean to reduce DC dominance
        A = img - float(np.mean(img)) if self.detrend else img.copy()

        # 2D FFT power spectrum (centered)
        P = np.abs(np.fft.fftshift(np.fft.fft2(A))) ** 2

        # Radial average
        k, psd_rad = _radial_average(P)
        if k.size < 3:
            raise ValueError("radial spectrum too small to analyze")

        # Exclude k<=kmin from peak search (skip DC and immediate neighbors)
        start = min(self.kmin_exclude + 1, psd_rad.size - 1)
        k_search = k[start:]
        psd_search = psd_rad[start:]
        if psd_search.size == 0:
            raise ValueError("no non-DC spectrum available for peak detection")

        # Peak detection: largest bin
        idx_rel = int(np.argmax(psd_search))
        idx_peak = start + idx_rel
        k_peak = float(k[idx_peak])

        # Contrast metric relative to non-DC median
        nz_slice = psd_rad[1:] if psd_rad.size > 1 else psd_rad
        nz_median = float(np.median(nz_slice)) if nz_slice.size else 1.0
        nz_median = nz_median if nz_median > 0.0 else 1.0
        moire_contrast = float(psd_rad[idx_peak] / nz_median)

        # Ring energy fraction in ±(band_rel_width * k_peak)
        if k_peak <= 0.0:
            k_lo, k_hi = 0.0, 0.0
            ring_energy = 0.0
        else:
            dk = max(1.0, self.band_rel_width * k_peak)
            k_lo = max(1.0, k_peak - dk)
            k_hi = min(float(k[-1]), k_peak + dk)
            # Discrete bins: include indices with k in [k_lo, k_hi]
            mask_ring = (k >= k_lo) & (k <= k_hi)
            mask_nz = (k >= 1.0)  # exclude DC bin only
            ring_energy = float(np.sum(psd_rad[mask_ring]))
        total_power_nz = float(np.sum(psd_rad[k >= 1.0]))
        ring_energy_frac = float(ring_energy / total_power_nz) if total_power_nz > 0 else 0.0

        # DC power
        dc_power = float(psd_rad[0]) if psd_rad.size > 0 else 0.0

        return MoireContrastResult(
            k_peak=k_peak,
            moire_contrast=moire_contrast,
            ring_energy_frac=ring_energy_frac,
            k_band=(float(k_lo), float(k_hi)),
            dc_power=dc_power,
            total_power_nz=total_power_nz,
            meta={
                "detrend": self.detrend,
                "band_rel_width": self.band_rel_width,
                "kmin_exclude": self.kmin_exclude,
                "canon_anchor": "VDM-E-163",
            },
        )

    def write_artifacts(
        self,
        F: Any,
        *,
        domain: str = "materials/gb",
        name: str = "gb_moire_contrast",
        tag: Optional[str] = None,
        failed: bool = False,
        write_png: bool = True,
    ) -> Dict[str, str]:
        """Compute metrics and emit JSON/CSV/PNG artifacts via io_paths."""
        img = _as64(F)
        if img.ndim != 2:
            raise ValueError("F must be a 2D array")
        ny, nx = img.shape

        # Compute PSD and radial spectrum (reuse internal pipeline)
        A = img - float(np.mean(img)) if self.detrend else img.copy()
        P = np.abs(np.fft.fftshift(np.fft.fft2(A))) ** 2
        k, psd_rad = _radial_average(P)

        res = self.compute(F)

        slug = build_slug(name, tag)
        json_path = log_path_by_tag(domain, f"{name}_summary", tag, failed=failed, type="json")
        csv_path = log_path_by_tag(domain, f"{name}_radial_psd", tag, failed=failed, type="csv")

        summary = {
            "slug": slug,
            "domain": domain,
            "canon_anchor": "VDM-E-163",
            "metrics": {
                "k_peak": res.k_peak,
                "moire_contrast": res.moire_contrast,
                "ring_energy_frac": res.ring_energy_frac,
                "k_band": list(res.k_band),
                "dc_power": res.dc_power,
                "total_power_nz": res.total_power_nz,
            },
            "meta": res.meta,
            "series_paths": {"csv": str(csv_path)},
        }
        write_log(json_path, summary)

        # CSV for radial PSD
        ensure_dir(Path(csv_path).parent)
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["k_radius", "PSD_radial"])
            w.writeheader()
            for ki, pi in zip(k, psd_rad):
                w.writerow({"k_radius": float(ki), "PSD_radial": float(pi)})

        fig_path_str = ""
        if write_png and _HAVE_MPL and k.size > 1:
            fig_path = figure_path_by_tag(domain, f"{name}_panel", tag, failed=failed)
            try:
                plt.figure(figsize=(6.4, 3.6), dpi=150)
                plt.plot(k[1:], psd_rad[1:], "-", color="#1f77b4", lw=1.5, label="PSD_radial (k>0)")
                # Mark peak and band
                kpk = res.k_peak
                klo, khi = res.k_band
                if kpk > 0.0:
                    plt.axvline(kpk, color="#d62728", lw=1.5, ls="--", label=f"k_peak≈{kpk:.3g}")
                    plt.axvspan(klo, khi, color="#ffbb78", alpha=0.25, label="ring band")
                plt.xlabel("k radius (pixels)")
                plt.ylabel("PSD (arb.)")
                txt = f"contrast={res.moire_contrast:.3g}, ring_frac={res.ring_energy_frac:.3g}"
                plt.title(slug + "  [" + txt + "]")
                plt.grid(True, alpha=0.25)
                plt.legend()
                plt.tight_layout()
                plt.savefig(fig_path, bbox_inches="tight")
                plt.close()
                fig_path_str = str(fig_path)
            except Exception:
                fig_path_str = ""

        return {"json": str(json_path), "csv": str(csv_path), "png": fig_path_str}


__all__ = ["GBMoireContrast", "MoireContrastResult"]