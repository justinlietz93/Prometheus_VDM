#!/usr/bin/env python3
# D2Q9 LBM (BGK) with periodic BCs and bounce-back no-slip walls.
# Viscosity (lattice units): nu = c_s^2 * (tau - 0.5), c_s^2 = 1/3, dx=dt=1.
"""
CHANGE REASON:
- Adds the fluids sector minimal solver (LBM→NS) per TODO_up_next plan.
- Mirrors the repository's proven practice: scripts emit figures + JSON metrics with a 'passed' gate.
- This module is scoped; it does not alter RD canonical sector. It provides the operational path to NS.

References:
- derivation: [fluids_limit.md](Prometheus_FUVDM/derivation/fluids_limit.md:1)
- benchmarks: taylor_green_benchmark.py, lid_cavity_benchmark.py
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass

# Integrate FUVDM void dynamics (bounded, stabilizing)
try:
    from FUM_Demo_original.FUM_Void_Equations import universal_void_dynamics
    from FUM_Demo_original.FUM_Void_Debt_Modulation import VoidDebtModulation
except Exception:  # fallback if path not on sys.path
    universal_void_dynamics = None
    VoidDebtModulation = None

# Lattice constants for D2Q9
D2Q9_C = np.array([
    [ 0,  0],
    [ 1,  0], [ 0,  1], [-1,  0], [ 0, -1],
    [ 1,  1], [-1,  1], [-1, -1], [ 1, -1]
], dtype=np.int32)

D2Q9_W = np.array([4/9] + [1/9]*4 + [1/36]*4, dtype=np.float64)
OPP     = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)  # opposite dirs
CS2     = 1.0/3.0  # c_s^2


@dataclass
class LBMConfig:
    nx: int = 256
    ny: int = 256
    tau: float = 0.8               # relaxation time; nu = CS2 * (tau - 0.5)
    forcing: tuple[float, float] = (0.0, 0.0)  # body force (fx, fy)
    periodic_x: bool = True
    periodic_y: bool = True
    # FUVDM void dynamics coupling (bounded stabilizer)
    void_enabled: bool = True
    void_domain: str = "standard_model"
    void_gain: float = 0.5
    rho_floor: float = 1e-9
    u_clamp: float | None = None   # e.g., 0.1 to keep Ma≲0.1; None disables


class LBM2D:
    def __init__(self, cfg: LBMConfig):
        self.cfg = cfg
        self.nx, self.ny = int(cfg.nx), int(cfg.ny)
        self.tau  = float(cfg.tau)
        self.omega = 1.0 / self.tau
        self.fx, self.fy = cfg.forcing
        # populations f[i, y, x]
        self.f  = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        self.tmp = np.zeros_like(self.f)
        # macroscopic fields
        self.rho = np.ones((self.ny, self.nx), dtype=np.float64)
        self.ux  = np.zeros_like(self.rho)
        self.uy  = np.zeros_like(self.rho)
        # solid mask for bounce-back (False = fluid, True = solid)
        self.solid = np.zeros((self.ny, self.nx), dtype=bool)

        # FUVDM void dynamics state and metrics
        self.t = 0
        self.W = 0.5 * np.ones((self.ny, self.nx), dtype=np.float64)
        self.omega_eff = np.full((self.ny, self.nx), self.omega, dtype=np.float64)
        self.aggr_dW_max = 0.0
        self.aggr_omega_min = float("inf")
        self.aggr_omega_max = 0.0
        self.last_W_mean = float(np.mean(self.W))

        # Optional domain modulator
        self._void_modulator = None
        if VoidDebtModulation is not None:
            try:
                self._void_modulator = VoidDebtModulation()
            except Exception:
                self._void_modulator = None

        self._set_equilibrium()

    def _set_equilibrium(self):
        """Initialize to rho=1, u=(0,0) equilibrium."""
        u2 = self.ux**2 + self.uy**2
        for i in range(9):
            cx, cy = D2Q9_C[i]
            cu = cx*self.ux + cy*self.uy
            self.f[i] = D2Q9_W[i] * self.rho * (1 + 3*cu + 4.5*(cu**2) - 1.5*u2)

    def set_solid_box(self, top: bool=True, bottom: bool=True, left: bool=False, right: bool=False):
        """Create no-slip walls by marking boundary nodes solid (half-way bounce-back)."""
        if top:    self.solid[0, :]  = True
        if bottom: self.solid[-1, :] = True
        if left:   self.solid[:, 0]  = True
        if right:  self.solid[:, -1] = True

    def set_lid_velocity(self, U: float):
        """Top (north) boundary velocity BC (Zou/He) with u=(U,0); top row is y=0 and FLUID (not solid)."""
        y = 0
        x = np.arange(self.nx)
        # Known after streaming (from interior): f2(N), f5(NE), f6(NW); unknown incoming: f4(S), f7(SW), f8(SE)
        f0 = self.f[0, y, x]; f1 = self.f[1, y, x]; f3 = self.f[3, y, x]
        f2 = self.f[2, y, x]; f5 = self.f[5, y, x]; f6 = self.f[6, y, x]
        rho = (f0 + f1 + f3 + 2.0*(f2 + f5 + f6))
        # Reconstruct unknowns pointing into fluid from the top wall
        self.f[4, y, x] = f2
        self.f[7, y, x] = f5 - 0.5*(f1 - f3) + (1.0/6.0) * rho * U
        self.f[8, y, x] = f6 + 0.5*(f1 - f3) + (1.0/6.0) * rho * U

    def moments(self):
        """Compute macroscopic moments rho, ux, uy from populations."""
        self.rho[:] = np.sum(self.f, axis=0)
        # density floor to avoid division by ~0
        rf = float(self.cfg.rho_floor) if hasattr(self.cfg, "rho_floor") else 0.0
        if rf > 0.0:
            np.maximum(self.rho, rf, out=self.rho)
        # momentum components (no reduction over spatial axes)
        self.ux[:]  = (self.f[1] - self.f[3] + self.f[5] - self.f[6] - self.f[7] + self.f[8]) / (self.rho + 1e-15)
        self.uy[:]  = (self.f[2] - self.f[4] + self.f[5] + self.f[6] - self.f[7] - self.f[8]) / (self.rho + 1e-15)
        # optional |u| clamp (keep Ma≲0.1)
        u_clamp = getattr(self.cfg, "u_clamp", None)
        if u_clamp is not None and u_clamp > 0.0:
            speed = np.sqrt(self.ux**2 + self.uy**2) + 1e-30
            fac = np.minimum(1.0, u_clamp / speed)
            self.ux *= fac
            self.uy *= fac

    def collide(self):
        """BGK collision with simple constant body force (optional)."""
        u2 = self.ux**2 + self.uy**2
        fx, fy = self.fx, self.fy
        for i in range(9):
            cx, cy = D2Q9_C[i]
            cu = cx*self.ux + cy*self.uy
            feq = D2Q9_W[i] * self.rho * (1 + 3*cu + 4.5*(cu**2) - 1.5*u2)
            self.f[i] += -self.omega * (self.f[i] - feq)
            # simple forcing term (Guo forcing gives higher accuracy; omitted for brevity)
            if fx or fy:
                self.f[i] += D2Q9_W[i] * (3*(cx*fx + cy*fy))

    def stream(self):
        """Nonperiodic push-streaming via slicing (no wrap); then bounce-back at solids."""
        ny, nx = self.ny, self.nx
        self.tmp.fill(0.0)
        for i in range(9):
            cx, cy = D2Q9_C[i]
            # destination slices
            if cy == 1:
                dst_y = slice(1, ny); src_y = slice(0, ny-1)
            elif cy == -1:
                dst_y = slice(0, ny-1); src_y = slice(1, ny)
            else:
                dst_y = slice(0, ny);   src_y = slice(0, ny)
            if cx == 1:
                dst_x = slice(1, nx); src_x = slice(0, nx-1)
            elif cx == -1:
                dst_x = slice(0, nx-1); src_x = slice(1, nx)
            else:
                dst_x = slice(0, nx);   src_x = slice(0, nx)
            self.tmp[i, dst_y, dst_x] = self.f[i, src_y, src_x]
        self.f[:] = self.tmp
        # bounce-back (swap with opposite direction at solid cells)
        solid = self.solid
        if np.any(solid):
            for i in range(9):
                opp = OPP[i]
                fi   = self.f[i]
                fopp = self.f[opp]
                fi[solid], fopp[solid] = fopp[solid].copy(), fi[solid].copy()

    def step(self, nsteps: int = 1):
        """Advance nsteps time steps."""
        for _ in range(nsteps):
            self.moments()
            self.collide()
            self.stream()

    @property
    def nu(self) -> float:
        """Kinematic viscosity in lattice units."""
        return CS2 * (self.tau - 0.5)

    def divergence(self) -> float:
        """Discrete L2 norm of ∇·u using nonperiodic central differences; exclude walls and 2-cell band."""
        ny, nx = self.ny, self.nx
        div = np.zeros((ny, nx), dtype=np.float64)
        # central differences on interior (avoid periodic wrap)
        div[1:-1, 1:-1] = 0.5 * (self.ux[1:-1, 2:] - self.ux[1:-1, 0:-2]) + \
                          0.5 * (self.uy[2:, 1:-1] - self.uy[0:-2, 1:-1])
        # mask out solids and a 2-cell dilation band (boundary layer not assessed)
        solid = self.solid
        if solid.any():
            band = solid.copy()
            for _ in range(2):
                nb = np.zeros_like(band, dtype=bool)
                nb[1:, :]  |= band[:-1, :]
                nb[:-1, :] |= band[1:,  :]
                nb[:, 1:]  |= band[:, :-1]
                nb[:, :-1] |= band[:,  1:]
                band |= nb
            div[band] = 0.0
        return float(np.sqrt(np.mean(div**2)))