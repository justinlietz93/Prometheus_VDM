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
# --- FUVDM / Void dynamics (optional) ----------------------------------------
import os, importlib.util

universal_void_dynamics = None
VoidDebtModulation = None
VOID_SOURCE = None

def _load_module_by_path(path: str, modname: str):
    if os.path.exists(path):
        spec = importlib.util.spec_from_file_location(modname, path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        return mod
    return None

# 1) Preferred: in-repo Prometheus_FUVDM files (package import)
try:
    from Prometheus_FUVDM.derivation.code.FUM_Void_Equations import universal_void_dynamics as _u
    from Prometheus_FUVDM.derivation.code.FUM_Void_Debt_Modulation import VoidDebtModulation as _V
    universal_void_dynamics, VoidDebtModulation = _u, _V
    VOID_SOURCE = "Prometheus_FUVDM.derivation.code"
except Exception:
    # 2) Fallback: load by file path from derivation/code/ next to this physics folder
    try:
        _ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))  # → Prometheus_FUVDM/derivation/code
        _eq_path = os.path.join(_ROOT, "FUM_Void_Equations.py")
        _mod_path = os.path.join(_ROOT, "FUM_Void_Debt_Modulation.py")
        _eq = _load_module_by_path(_eq_path, "FUM_Void_Equations_local")
        _md = _load_module_by_path(_mod_path, "FUM_Void_Debt_Modulation_local")
        if _eq and hasattr(_eq, "universal_void_dynamics"):
            universal_void_dynamics = getattr(_eq, "universal_void_dynamics")
            VOID_SOURCE = "file:derivation/code/FUM_Void_Equations.py"
        if _md and hasattr(_md, "VoidDebtModulation"):
            VoidDebtModulation = getattr(_md, "VoidDebtModulation")
            if VOID_SOURCE is None:
                VOID_SOURCE = "file:derivation/code/FUM_Void_Debt_Modulation.py"
    except Exception:
        pass
    # 3) fum_rt adapter
    if universal_void_dynamics is None:
        try:
            from fum_rt.core.void_dynamics_adapter import universal_void_dynamics as _u
            from fum_rt.fum_advanced_math.void_dynamics.FUM_Void_Debt_Modulation import VoidDebtModulation as _V
            universal_void_dynamics, VoidDebtModulation = _u, _V
            VOID_SOURCE = "fum_rt"
        except Exception:
            # 4) demo fallback
            try:
                from FUM_Demo_original.FUM_Void_Equations import universal_void_dynamics as _u
                from FUM_Demo_original.FUM_Void_Debt_Modulation import VoidDebtModulation as _V
                universal_void_dynamics, VoidDebtModulation = _u, _V
                VOID_SOURCE = "FUM_Demo_original"
            except Exception:
                pass

# Final fallback: add derivation/code to sys.path and import by name if still missing
if universal_void_dynamics is None:
    try:
        import sys
        _ROOT2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        if _ROOT2 not in sys.path:
            sys.path.insert(0, _ROOT2)
        import FUM_Void_Equations as _eq2
        universal_void_dynamics = getattr(_eq2, "universal_void_dynamics", None)
        if universal_void_dynamics is not None:
            VOID_SOURCE = "sys.path:derivation/code"
        try:
            import FUM_Void_Debt_Modulation as _vdm2
            VoidDebtModulation = getattr(_vdm2, "VoidDebtModulation", None)
        except Exception:
            pass
    except Exception:
        pass
print(f"[LBM2D] Loaded. void_module={universal_void_dynamics is not None} source={VOID_SOURCE} file={__file__}")


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
    void_use_modulation: bool = False
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

        # Fail-fast if user requested void but module not available
        if getattr(self.cfg, "void_enabled", False) and universal_void_dynamics is None:
            raise RuntimeError("void_enabled=True but universal_void_dynamics not available; ensure Prometheus_FUVDM/derivation/code/FUM_Void_Equations.py is present or install fum_rt/FUM_Demo_original.")

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
        """Top (north) velocity BC (Zou/He) with u=(U,0); top row is y=0 and FLUID; exclude corners."""
        y = 0
        if self.nx >= 3:
            x = np.arange(1, self.nx - 1)  # exclude corners to avoid conflict with left/right bounce-back
        else:
            x = np.arange(self.nx)
        if x.size == 0:
            return
        # Known after streaming (from interior): f2(N), f5(NE), f6(NW); unknown incoming: f4(S), f7(SW), f8(SE)
        f0 = self.f[0, y, x]; f1 = self.f[1, y, x]; f3 = self.f[3, y, x]
        f2 = self.f[2, y, x]; f5 = self.f[5, y, x]; f6 = self.f[6, y, x]
        rho = (f0 + f1 + f3 + 2.0*(f2 + f5 + f6))  # uy=0 here
        # Reconstruct unknowns pointing into fluid from the top wall
        self.f[4, y, x] = f2
        self.f[7, y, x] = f5 - 0.5*(f1 - f3) - (1.0/6.0) * rho * U  # Zou/He top lid: f7 gets −ρU/6
        self.f[8, y, x] = f6 + 0.5*(f1 - f3) + (1.0/6.0) * rho * U  # Zou/He top lid: f8 gets +ρU/6

    def moments(self):
        """Compute macroscopic moments rho, ux, uy from populations (robust to NaN/Inf)."""
        # sanitize populations to avoid NaN/Inf propagation
        np.nan_to_num(self.f, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
        # density with floor
        self.rho[:] = np.sum(self.f, axis=0)
        np.nan_to_num(self.rho, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
        rf = float(self.cfg.rho_floor) if hasattr(self.cfg, "rho_floor") else 0.0
        if rf > 0.0:
            np.maximum(self.rho, rf, out=self.rho)
        # momentum components
        numx = (self.f[1] - self.f[3] + self.f[5] - self.f[6] - self.f[7] + self.f[8])
        numy = (self.f[2] - self.f[4] + self.f[5] + self.f[6] - self.f[7] - self.f[8])
        np.nan_to_num(numx, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
        np.nan_to_num(numy, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
        den = self.rho + 1e-12
        self.ux[:] = numx / den
        self.uy[:] = numy / den
        # optional |u| clamp (keep Ma≲0.1)
        u_clamp = getattr(self.cfg, "u_clamp", None)
        if u_clamp is not None and u_clamp > 0.0:
            speed = np.sqrt(self.ux**2 + self.uy**2) + 1e-30
            fac = np.minimum(1.0, u_clamp / speed)
            self.ux *= fac
            self.uy *= fac

    def _void_update(self):
        """Update W via universal void dynamics and compute bounded omega_eff."""
        # domain modulation
        s = 1.0
        if getattr(self.cfg, "void_use_modulation", False) and self._void_modulator is not None:
            try:
                info = self._void_modulator.get_universal_domain_modulation(self.cfg.void_domain)
                s = float(info.get("domain_modulation", 1.0))
            except Exception:
                s = 1.0
        # universal delta (vectorized); fallback to zero if import missing
        if universal_void_dynamics is None:
            dW = np.zeros_like(self.W)
            if self.t == 0:
                print("[void] unavailable; dW=0")
        else:
            dW = universal_void_dynamics(self.W, self.t, domain_modulation=s, use_time_dynamics=True)
            if self.t == 0:
                print(f"[void] available from {VOID_SOURCE}; applying update")
        # update and clamp W∈[0,1]
        self.W += dW
        np.clip(self.W, 0.0, 1.0, out=self.W)
        self.last_W_mean = float(np.mean(self.W))
        # bounded relaxation omega field
        g = float(self.cfg.void_gain)
        denom = (1.0 + g * np.abs(dW))
        self.omega_eff = np.clip(self.omega / denom, 1e-3, 1.99)
        # aggregate metrics
        dW_abs_max = float(np.max(np.abs(dW)))
        self.aggr_dW_max = max(self.aggr_dW_max, dW_abs_max)
        self.aggr_omega_min = min(self.aggr_omega_min, float(np.min(self.omega_eff)))
        self.aggr_omega_max = max(self.aggr_omega_max, float(np.max(self.omega_eff)))

    def collide(self):
        """BGK collision with void-stabilized relaxation and optional body force."""
        u2 = self.ux**2 + self.uy**2
        fx, fy = self.fx, self.fy
        # choose omega field (scalar or per-cell)
        omega_field = self.omega_eff if getattr(self.cfg, "void_enabled", False) else self.omega
        for i in range(9):
            cx, cy = D2Q9_C[i]
            cu = cx*self.ux + cy*self.uy
            feq = D2Q9_W[i] * self.rho * (1 + 3*cu + 4.5*(cu**2) - 1.5*u2)
            self.f[i] += -omega_field * (self.f[i] - feq)
            # simple forcing term (Guo forcing gives higher accuracy; omitted for brevity)
            if fx or fy:
                self.f[i] += D2Q9_W[i] * (3*(cx*fx + cy*fy))

    def stream(self):
        """Streaming with nonperiodic slice-shift when any axis is nonperiodic; roll-stream if fully periodic; then bounce-back at solids."""
        px, py = self.cfg.periodic_x, self.cfg.periodic_y
        ny, nx = self.ny, self.nx
        if px and py:
            # fully periodic: use roll
            for i in range(9):
                cx, cy = D2Q9_C[i]
                fi_shift = np.roll(np.roll(self.f[i], shift=cx, axis=1), shift=cy, axis=0)
                self.tmp[i] = fi_shift
        else:
            # nonperiodic: push-stream via slicing (no wrap)
            self.tmp.fill(0.0)
            for i in range(9):
                cx, cy = D2Q9_C[i]
                # NOTE: array axis 0 increases downward; "north" (cy=+1) must move to lower row index
                if cy == 1:
                    dst_y = slice(0, ny-1); src_y = slice(1, ny)   # move up
                elif cy == -1:
                    dst_y = slice(1, ny);   src_y = slice(0, ny-1) # move down
                else:
                    dst_y = slice(0, ny);   src_y = slice(0, ny)
                if cx == 1:
                    dst_x = slice(1, nx);   src_x = slice(0, nx-1)
                elif cx == -1:
                    dst_x = slice(0, nx-1); src_x = slice(1, nx)
                else:
                    dst_x = slice(0, nx);   src_x = slice(0, nx)
                self.tmp[i, dst_y, dst_x] = self.f[i, src_y, src_x]
        self.f[:] = self.tmp
        # bounce-back (swap with opposite direction at solid cells)
        solid = self.solid
        if np.any(solid):
            # swap each opposite pair exactly once to avoid double-reverting
            for i in (1, 2, 5, 6):  # pairs: (1↔3), (2↔4), (5↔7), (6↔8)
                opp = OPP[i]
                fi   = self.f[i]
                fopp = self.f[opp]
                tmp = fi[solid].copy()
                fi[solid] = fopp[solid]
                fopp[solid] = tmp

    def step(self, nsteps: int = 1):
        """Advance nsteps time steps."""
        for _ in range(nsteps):
            self.moments()
            # FUVDM void-stabilized omega update
            if getattr(self.cfg, "void_enabled", False):
                self._void_update()
            else:
                self.omega_eff[...] = self.omega
                # Update aggregator even when void disabled to avoid inf/0 in logs
                self.aggr_omega_min = min(self.aggr_omega_min, float(np.min(self.omega_eff)))
                self.aggr_omega_max = max(self.aggr_omega_max, float(np.max(self.omega_eff)))
            self.collide()
            self.stream()
            self.t += 1

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