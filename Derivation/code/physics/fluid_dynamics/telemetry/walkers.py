#!/usr/bin/env python3
# Read-only, measurement-only walkers + bus + reducer for fluids telemetry.
# No imports from fum_rt; self-contained.

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple, Iterable, Optional
import numpy as np


@dataclass
class Petition:
    kind: str        # 'div', 'swirl', 'shear'
    value: float
    x: float
    y: float
    t: int


class Bus:
    def __init__(self, cap: int = 20000) -> None:
        self.events: List[Petition] = []
        self.cap = int(max(1, cap))

    def post(self, pet: Petition) -> None:
        if len(self.events) < self.cap:
            self.events.append(pet)

    def clear(self) -> None:
        self.events.clear()


class Reducer:
    """
    Robust quantiles per kind; also track counts.
    """
    def __init__(self) -> None:
        self.stats: Dict[str, float] = {}
        self.counts: Dict[str, int] = {}

    def reduce(self, bus: Bus) -> Dict[str, float]:
        out: Dict[str, float] = {}
        kinds = set(ev.kind for ev in bus.events)
        counts: Dict[str, int] = {}
        for k in kinds:
            vals = np.asarray([ev.value for ev in bus.events if ev.kind == k], dtype=float)
            counts[k] = int(vals.size)
            if vals.size:
                out[f"{k}_p50"] = float(np.quantile(vals, 0.50))
                out[f"{k}_p90"] = float(np.quantile(vals, 0.90))
                out[f"{k}_max"] = float(np.max(vals))
        self.stats = out
        self.counts = counts
        return out


class Walker:
    """
    Read-only walker that:
      - steps using measured velocity field (advection only)
      - senses a local scalar and reports a Petition to a Bus
    """
    __slots__ = ("x", "y", "kind", "rng")

    def __init__(self, x: float, y: float, kind: str, seed: Optional[int] = None) -> None:
        self.x = float(x)
        self.y = float(y)
        self.kind = str(kind)
        self.rng = np.random.default_rng(int(seed) if seed is not None else None)

    @staticmethod
    def _bilinear(F: np.ndarray, x: float, y: float) -> float:
        ny, nx = F.shape
        # Clamp to valid cell square
        x = float(np.clip(x, 0.0, nx - 1.000001))
        y = float(np.clip(y, 0.0, ny - 1.000001))
        j0 = int(np.floor(x)); i0 = int(np.floor(y))
        j1 = min(j0 + 1, nx - 1); i1 = min(i0 + 1, ny - 1)
        fx = x - j0; fy = y - i0
        f00 = F[i0, j0]; f10 = F[i0, j1]; f01 = F[i1, j0]; f11 = F[i1, j1]
        return float((1 - fy) * ((1 - fx) * f00 + fx * f10) + fy * ((1 - fx) * f01 + fx * f11))

    def step(self, sim: object, dt: float = 1.0) -> None:
        """
        Advect by measured velocity (read-only). Keeps inside fluid box; avoids solids.
        Expects sim.ux, sim.uy, sim.solid, sim.nx, sim.ny.
        """
        ux = self._bilinear(sim.ux, self.x, self.y)
        uy = self._bilinear(sim.uy, self.x, self.y)
        x_new = float(self.x + dt * ux)
        y_new = float(self.y + dt * uy)
        # Keep within interior band to avoid index issues
        nx, ny = int(sim.nx), int(sim.ny)
        x_new = float(np.clip(x_new, 0.5, nx - 1.5))
        y_new = float(np.clip(y_new, 0.5, ny - 1.5))
        # Avoid solids by small jitter toward interior if needed
        try:
            if bool(sim.solid[int(round(y_new)), int(round(x_new))]):
                # jitter inward
                x_new = float(np.clip(self.x + 0.25 * np.sign(nx * 0.5 - self.x), 0.5, nx - 1.5))
                y_new = float(np.clip(self.y + 0.25 * np.sign(ny * 0.5 - self.y), 0.5, ny - 1.5))
        except Exception:
            pass
        self.x, self.y = x_new, y_new

    @staticmethod
    def _ddx(F: np.ndarray, x: float, y: float) -> float:
        j = int(np.clip(round(x), 0, F.shape[1] - 1))
        i = int(np.clip(round(y), 0, F.shape[0] - 1))
        jm = max(j - 1, 0); jp = min(j + 1, F.shape[1] - 1)
        return float(0.5 * (F[i, jp] - F[i, jm]))

    @staticmethod
    def _ddy(F: np.ndarray, x: float, y: float) -> float:
        j = int(np.clip(round(x), 0, F.shape[1] - 1))
        i = int(np.clip(round(y), 0, F.shape[0] - 1))
        im = max(i - 1, 0); ip = min(i + 1, F.shape[0] - 1)
        return float(0.5 * (F[ip, j] - F[im, j]))

    def sense(self, sim: object) -> float:
        """
        Sense local scalar based on kind:
          - 'div'   : |∇·u|
          - 'swirl' : |ω| = |∂u/∂y - ∂v/∂x|
          - 'shear' : crude tangential shear near walls
        """
        if self.kind == "div":
            val = self._ddx(sim.ux, self.x, self.y) + self._ddy(sim.uy, self.x, self.y)
            return abs(float(val))
        elif self.kind == "swirl":
            val = self._ddy(sim.ux, self.x, self.y) - self._ddx(sim.uy, self.x, self.y)
            return abs(float(val))
        elif self.kind == "shear":
            # crude proxy near walls: large local gradients if close to solid
            i = int(np.clip(round(self.y), 0, sim.solid.shape[0] - 1))
            j = int(np.clip(round(self.x), 0, sim.solid.shape[1] - 1))
            i0 = max(i - 2, 0); i1 = min(i + 3, sim.solid.shape[0])
            j0 = max(j - 2, 0); j1 = min(j + 3, sim.solid.shape[1])
            near_wall = bool(sim.solid[i0:i1, j0:j1].astype(np.uint8).sum() > 0)
            if near_wall:
                gx = abs(self._ddx(sim.ux, self.x, self.y))
                gy = abs(self._ddy(sim.uy, self.x, self.y))
                return float(max(gx, gy))
            return 0.0
        return 0.0


def seed_walkers_lid(nx: int, ny: int, count: int, kinds: Iterable[str], seed: int = 0) -> List[Walker]:
    """
    Seed walkers along the top-lid interior line (y≈0.5), excluding corners.
    kinds: iterable of kind labels; will be cycled to match count.
    """
    rng = np.random.default_rng(int(seed))
    count = int(max(0, count))
    if count <= 0:
        return []
    xs = np.linspace(1.0, nx - 2.0, num=count, endpoint=True)
    ys = np.full_like(xs, 0.5)
    kinds_list = list(kinds) if kinds else ["div", "swirl", "shear"]
    if not kinds_list:
        kinds_list = ["div", "swirl", "shear"]
    walkers: List[Walker] = []
    for idx in range(count):
        k = kinds_list[idx % len(kinds_list)]
        # small jitter in x for diversity
        x = float(np.clip(xs[idx] + rng.uniform(-0.15, 0.15), 0.5, nx - 1.5))
        y = float(ys[idx])
        walkers.append(Walker(x, y, k, seed=seed + idx))
    return walkers


def top_events(bus: Bus, max_n: int = 512) -> Dict[str, object]:
    """
    Extract top events overall by value (bounded by max_n) and per-kind counts.
    Returns:
      {
        "counts": {"div": int, "swirl": int, "shear": int},
        "events": [{"kind": str, "value": float, "x": float, "y": float, "t": int}, ...]
      }
    """
    max_n = int(max(0, max_n))
    counts: Dict[str, int] = {}
    for ev in bus.events:
        counts[ev.kind] = counts.get(ev.kind, 0) + 1
    if max_n == 0 or not bus.events:
        return {"counts": counts, "events": []}
    # overall top by value
    arr = np.asarray([(ev.value, ev.kind, ev.x, ev.y, ev.t) for ev in bus.events], dtype=object)
    # argsort descending by value
    idx = np.argsort(arr[:, 0].astype(float))[::-1][:max_n]
    out_events = []
    for k in idx:
        v, kind, x, y, t = arr[k]
        out_events.append({"kind": str(kind), "value": float(v), "x": float(x), "y": float(y), "t": int(t)})
    return {"counts": counts, "events": out_events}
    
    

# --- Advisory Policy (bounded, numeric-parameters only; no forcing) ---
@dataclass
class PolicyBounds:
    tau_min: float = 0.51
    tau_max: float = 1.95
    U_min: float = 1e-8
    U_max: float = 0.2
    uclamp_min: float = 1e-6
    uclamp_max: float = 0.1

class AdvisoryPolicy:
    """
    Map petition summaries -> suggested small nudges to numerical parameters.
    Never injects forces; caller decides whether to apply.
    """
    def __init__(self, div_target: float = 1e-6, vort_target: float = 5e-3, bounds: Optional[PolicyBounds] = None):
        self.div_target = float(div_target)
        self.vort_target = float(vort_target)
        self.bounds = bounds if bounds is not None else PolicyBounds()

    def suggest(self, stats_summary: Dict[str, float], params: Dict[str, float]) -> Dict[str, float]:
        # robust extraction with fallbacks
        div_p99 = float(stats_summary.get("div_p99", stats_summary.get("div_p90", 0.0) * 1.2))
        vort_p50 = float(stats_summary.get("swirl_p50", 0.0))
        s: Dict[str, float] = {}
        # 1) Compressibility guard: high divergence -> tighten u_clamp, raise tau slightly
        if div_p99 > self.div_target:
            ucl = max(self.bounds.uclamp_min,
                      min(self.bounds.uclamp_max, float(params.get("u_clamp", self.bounds.uclamp_max)) * 0.9))
            tau = min(self.bounds.tau_max,
                      max(self.bounds.tau_min, float(params.get("tau", 0.7)) + 0.02))
            s["u_clamp"] = float(ucl)
            s["tau"] = float(tau)
        # 2) Swirl encouragement when divergence acceptable -> lower tau a touch, allow slightly larger U
        elif vort_p50 < self.vort_target and div_p99 < 2.0 * self.div_target:
            tau = max(self.bounds.tau_min,
                      min(self.bounds.tau_max, float(params.get("tau", 0.7)) - 0.02))
            U = min(self.bounds.U_max,
                    max(self.bounds.U_min, float(params.get("U_lid", 0.1)) * 1.05))
            s["tau"] = float(tau)
            s["U_lid"] = float(U)
        else:
            # keep within safe bounds; no strong opinion
            tau = float(np.clip(float(params.get("tau", 0.7)), self.bounds.tau_min, self.bounds.tau_max))
            s["tau"] = float(tau)
        return s