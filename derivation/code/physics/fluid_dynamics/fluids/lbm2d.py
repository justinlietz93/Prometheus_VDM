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
        """Impose a moving lid at top boundary via a simple Zou/He-like BC (approx)."""
        y = 0
        x = np.arange(self.nx)
        rho = (self.f[0,y,x] + self.f[2,y,x] + self.f[4,y,x] + 2*(self.f[3,y,x] + self.f[6,y,x] + self.f[7,y,x])) / (1 - U + 1e-15)
        self.f[1,y,x] = self.f[3,y,x] + (2/3.)*rho*U
        self.f[5,y,x] = self.f[7,y,x] + (1/6.)*rho*U + (1/2.)*(self.f[4,y,x] - self.f[2,y,x])
        self.f[8,y,x] = self.f[6,y,x] + (1/6.)*rho*U + (1/2.)*(self.f[2,y,x] - self.f[4,y,x])

    def moments(self):
        """Compute macroscopic moments rho, ux, uy from populations."""
        self.rho[:] = np.sum(self.f, axis=0)
        # momentum components (no reduction over spatial axes)
        self.ux[:]  = (self.f[1] - self.f[3] + self.f[5] - self.f[6] - self.f[7] + self.f[8]) / (self.rho + 1e-15)
        self.uy[:]  = (self.f[2] - self.f[4] + self.f[5] + self.f[6] - self.f[7] - self.f[8]) / (self.rho + 1e-15)

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
        """Periodic streaming in x/y, then bounce-back at solid nodes."""
        # stream (with periodic wraps)
        for i in range(9):
            cx, cy = D2Q9_C[i]
            self.tmp[i] = np.roll(np.roll(self.f[i], shift=cx, axis=1), shift=cy, axis=0)
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
        """Discrete L2 norm of divergence of velocity (periodic interior; walls ignored)."""
        dudx = (np.roll(self.ux, -1, axis=1) - np.roll(self.ux, 1, axis=1)) * 0.5
        dvdy = (np.roll(self.uy, -1, axis=0) - np.roll(self.uy, 1, axis=0)) * 0.5
        div  = dudx + dvdy
        div[self.solid] = 0.0
        return float(np.sqrt(np.mean(div**2)))