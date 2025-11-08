#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OQ-021 LIT gates: Curie mask, Onsager–Casimir residuals, entropy production.
Inputs: snapshots from a lid-cavity/corner run (T(x,y), v(x,y)), material coeffs.
Outputs: JSON/CSV/PNG artifacts + exit code gates.

Assumes availability:
- instrument_helpers.lit_tools: IsotropicFluidCoeffs, build_L_isotropic_fluid, curie_mask, gate_report, parity_even, BoundaryEntropyFluxMonitor, write_lit_gate_artifacts
- instrument_helpers.generic_helpers (optional): EntropyMonitor

References:
- de Groot & Mazur, Ch. III–IV: entropy balance; linear laws J = L X; Curie principle; Onsager reciprocity.
- Öttinger, §1.2, §2: GENERIC split, degeneracy, hydrodynamics blocks.
"""

import argparse, json, os, sys
from dataclasses import asdict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt  # optional; safe import

# Configure import path for in-repo instrument helpers
sys.path.append(str(Path(__file__).resolve().parents[2] / "common"))

from instrument_helpers.lit_tools import (
    IsotropicFluidCoeffs, build_L_isotropic_fluid, curie_mask, gate_report,
    parity_even, BoundaryEntropyFluxMonitor, write_lit_gate_artifacts
)

# ---------- helpers ----------

def grad_centered(f, dx, dy):
    """Return ∇f with second-order centered differences, Neumann at boundary."""
    gx = np.zeros_like(f); gy = np.zeros_like(f)
    gx[:,1:-1] = (f[:,2:] - f[:,:-2])/(2*dx); gx[:,0] = gx[:,1]; gx[:,-1]=gx[:,-2]
    gy[1:-1,:] = (f[2:,:] - f[:-2,:])/(2*dy); gy[0,:] = gy[1,:]; gy[-1,:]=gy[-2,:]
    return gx, gy

def sym_grad(vx, vy, dx, dy):
    """Return Sym(∇v): deviatoric invariant and volumetric scalar invariant."""
    dvx_dx, dvx_dy = grad_centered(vx, dx, dy)
    dvy_dx, dvy_dy = grad_centered(vy, dx, dy)
    # symmetric part
    Dxx = dvx_dx
    Dyy = dvy_dy
    Dxy = 0.5*(dvx_dy + dvy_dx)
    # deviatoric magnitude (2nd invariant) and volumetric divergence
    div = Dxx + Dyy
    dev2 = 2*(Dxx - Dyy)**2/4 + 2*(Dxy**2)  # simple proxy of |dev(D)|^2
    return dev2, div

def build_X_field(T, vx, vy, dx, dy, inv_T=True):
    """
    Assemble LIT forces per cell:
    X = [∇(1/T) components (3 slots but we have 2D -> pad third with zeros),
         Sym(∇v) invariants: deviatoric (scalar proxy), volumetric (scalar)]
    Returns array with shape (Ny, Nx, 5)
    """
    if inv_T:
        gT_x, gT_y = grad_centered(1.0/np.clip(T, 1e-12, np.inf), dx, dy)
    else:
        gT_x, gT_y = grad_centered(T, dx, dy)
    dev2, div = sym_grad(vx, vy, dx, dy)
    Ny, Nx = T.shape
    X = np.zeros((Ny, Nx, 5), dtype=np.float64)
    X[...,0] = gT_x
    X[...,1] = gT_y
    X[...,2] = 0.0  # 2D padding for heat sector third component
    X[...,3] = np.sqrt(np.clip(dev2,0, np.inf))  # use magnitude as scalar force proxy
    X[...,4] = div
    return X

def write_csv(path, sigmas):
    Ny, Nx = sigmas.shape
    with open(path, "w", encoding="utf-8") as f:
        f.write("i,j,sigma\n")
        for j in range(Ny):
            for i in range(Nx):
                f.write(f"{i},{j},{sigmas[j,i]:.12e}\n")

def plot_sigma(path, sigmas):
    plt.figure(figsize=(6,5), dpi=120)
    plt.imshow(sigmas, origin="lower", aspect="auto")
    plt.colorbar(label=r"$\sigma = X^T L X$")
    plt.title("Entropy production density")
    plt.tight_layout()
    plt.savefig(path); plt.close()

def accumulate_boundary_entropy_flux(T: np.ndarray, kappa: float, dx: float, dy: float) -> float:
    """
    Compute total boundary entropy flux rate J_s = ∮ (q/T)·n dA for Fourier heat flux q = -kappa ∇T.
    Uses one-sided differences at walls; outward normals on domain boundary.
    """
    Ny, Nx = T.shape
    Js_total = 0.0

    # Left boundary (normal = (-1,0)), area element = dy
    dTdx_left = (T[:, 1] - T[:, 0]) / dx
    qx_left = -kappa * dTdx_left
    Js_total += float(np.sum((qx_left * (-1.0)) * dy / np.clip(T[:, 0], 1e-300, np.inf)))

    # Right boundary (normal = (+1,0)), area element = dy
    dTdx_right = (T[:, -1] - T[:, -2]) / dx
    qx_right = -kappa * dTdx_right
    Js_total += float(np.sum((qx_right * (+1.0)) * dy / np.clip(T[:, -1], 1e-300, np.inf)))

    # Bottom boundary (normal = (0,-1)), area element = dx
    dTdy_bottom = (T[1, :] - T[0, :]) / dy
    qy_bottom = -kappa * dTdy_bottom
    Js_total += float(np.sum((qy_bottom * (-1.0)) * dx / np.clip(T[0, :], 1e-300, np.inf)))

    # Top boundary (normal = (0,+1)), area element = dx
    dTdy_top = (T[-1, :] - T[-2, :]) / dy
    qy_top = -kappa * dTdy_top
    Js_total += float(np.sum((qy_top * (+1.0)) * dx / np.clip(T[-1, :], 1e-300, np.inf)))

    return Js_total


# ---------- main gate runner ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T-npy", required=True, help="Path to T(x,y) npy")
    ap.add_argument("--vx-npy", required=True, help="Path to vx(x,y) npy")
    ap.add_argument("--vy-npy", required=True, help="Path to vy(x,y) npy")
    ap.add_argument("--dx", type=float, required=True)
    ap.add_argument("--dy", type=float, required=True)
    ap.add_argument("--kappa", type=float, required=True)
    ap.add_argument("--eta", type=float, required=True)
    ap.add_argument("--zeta", type=float, required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--onsager_tol_fro", type=float, default=1e-12)
    ap.add_argument("--sigma_tol", type=float, default=0.0)  # nonnegativity floor
    args = ap.parse_args()

    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    T  = np.load(args.T_npy).astype(np.float64, copy=False)
    vx = np.load(args.vx_npy).astype(np.float64, copy=False)
    vy = np.load(args.vy_npy).astype(np.float64, copy=False)

    # Build L, mask and forces
    coeffs = IsotropicFluidCoeffs(kappa=args.kappa, eta=args.eta, zeta=args.zeta)
    L, r_forces, r_fluxes = build_L_isotropic_fluid(coeffs)
    mask = curie_mask(r_forces, r_fluxes)
    X = build_X_field(T, vx, vy, args.dx, args.dy)

    # Compute gate report
    # Flatten cells to (Ncells, m); m=5
    X_field = X.reshape(-1, X.shape[-1])
    # Entropy production per cell
    sigmas = np.einsum("ij,nj->ni", L, X_field)  # J = L X
    sigmas = np.einsum("ni,ni->n", X_field, sigmas).reshape(T.shape)
    # Prepare parity (even for both blocks here; set odd values if adding B-field etc.)
    parity = parity_even(L.shape[0])
    rep = gate_report(L=L, X_field=X_field, dV=args.dx*args.dy, parity=parity, mask=mask)

    # Boundary entropy-flux accounting (near-equilibrium; de Groot & Mazur Ch. III–IV)
    bem = BoundaryEntropyFluxMonitor(tol=1e-12)
    Js_rate = accumulate_boundary_entropy_flux(T, args.kappa, args.dx, args.dy)
    # Single snapshot update; for time series, call per step in main loop
    bem.update_from_heat_flux(q_dot_n=Js_rate, T_face=float(np.mean(T)), area=1.0, dt=1.0)

    # Gates
    pass_sigma = (rep.sigma_min >= -abs(args.sigma_tol))
    pass_onsager = (rep.onsager_residual_fro <= args.onsager_tol_fro)
    pass_curie = (rep.curie_violations == 0)

    # Write artifacts
    js = {
        "tag": args.tag,
        "dims": {"Ny": int(T.shape[0]), "Nx": int(T.shape[1])},
        "coeffs": asdict(coeffs),
        "sigma": {
            "min": rep.sigma_min, "max": rep.sigma_max,
            "any_negative": rep.sigma_any_negative
        },
        "onsager": {
            "residual_fro": rep.onsager_residual_fro,
            "residual_linf": rep.onsager_residual_linf,
            "tolerance_fro": args.onsager_tol_fro
        },
        "curie": {"violations": rep.curie_violations},
        "gates": {
            "sigma_nonnegative": pass_sigma,
            "onsager_within_tol": pass_onsager,
            "curie_zero_cross": pass_curie,
            "PASS": bool(pass_sigma and pass_onsager and pass_curie)
        }
    }

    # Canonical KPI artifact routed via io_paths (logs/fluids)
    write_lit_gate_artifacts(
        domain="fluids", name="oq021_lit", tag=args.tag,
        L=L, X_field=X_field, dV=args.dx*args.dy, parity=parity, mask=mask,
        meta={"coeffs": asdict(coeffs), "dims": {"Ny": int(T.shape[0]), "Nx": int(T.shape[1])}}
    )

    json_path = out / f"{args.tag}__lit_gates.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(js, f, indent=2, sort_keys=True)

    csv_path = out / f"{args.tag}__sigma.csv"
    write_csv(csv_path, sigmas)
    png_path = out / f"{args.tag}__sigma.png"
    try:
        plot_sigma(png_path, sigmas)
    except Exception:
        pass

    # Append boundary-entropy-flux summary to JSON for convenience
    js["boundary_entropy_flux"] = bem.gates()
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(js, f, indent=2, sort_keys=True)

    # Exit code for CI
    sys.exit(0 if js["gates"]["PASS"] else 2)

if __name__ == "__main__":
    main()
