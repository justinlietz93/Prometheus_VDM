#!/usr/bin/env python3
from __future__ import annotations

"""
Wave Flux Meter — Phase B (Open-Ports with Absorber/Sponge) v1

Adds a damping sponge (sigma) near the outer boundary and defines two PORTS
at the interior–absorber interfaces (left and right windows). Measures:
 - Power balance: dE_interior/dt + (P_left + P_right) ≈ 0
 - Symmetry null: |P_left - P_right| / (P_left + P_right) small for symmetric IC
 - Absorber efficiency: dissipated power in absorber ≈ total power entering absorber

Artifacts: 1 PNG + 1 CSV + 1 JSON via common.io_paths. Approvals enforced.
"""

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple
from collections import deque

import numpy as np

CODE_ROOT = Path(__file__).resolve().parents[3]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import log_path_by_tag, write_log, figure_path_by_tag
from common.authorization.approval import check_tag_approval
from common.plotting.core import apply_style

DOMAIN = "thermo_routing"


@dataclass
class Spec:
    grid: Dict[str, Any]
    time: Dict[str, Any]
    wave: Dict[str, Any]
    bc: Dict[str, Any]
    absorber: Dict[str, Any]
    ports: Dict[str, Any]
    map: Dict[str, Any]
    seeds: int
    tag: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Wave Flux Meter Phase B (open ports) runner")
    p.add_argument("--spec", required=True, help="Path to spec JSON")
    p.add_argument("--allow-unapproved", action="store_true", help="Allow unapproved run (quarantine artifacts)")
    return p.parse_args()


def _git_hashes(repo_root: Path) -> Tuple[str, str]:
    def _git_short_hash_from_dotgit(repo_root: Path) -> str:
        try:
            dotgit = repo_root / ".git"
            head = (dotgit / "HEAD").read_text().strip()
            if head.startswith("ref:"):
                ref = head.split(":", 1)[1].strip()
                ref_path = dotgit / ref
                if ref_path.exists():
                    full = ref_path.read_text().strip()
                else:
                    full = head
            else:
                full = head
            return full[:7]
        except Exception:
            return "unknown"

    def _git_full_hash(repo_root: Path) -> str:
        try:
            dotgit = repo_root / ".git"
            head = (dotgit / "HEAD").read_text().strip()
            if head.startswith("ref:"):
                ref = head.split(":", 1)[1].strip()
                ref_path = dotgit / ref
                if ref_path.exists():
                    return ref_path.read_text().strip()
                return head
            return head
        except Exception:
            return "unknown"

    return _git_full_hash(repo_root), _git_short_hash_from_dotgit(repo_root)


def sha256_array(arr: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(arr).view(np.uint8)).hexdigest()


def _build_face_mu(mu_cell: np.ndarray | None, Ny: int, Nx: int) -> Tuple[np.ndarray, np.ndarray]:
    """Construct face-based mu on x-faces (Ny x (Nx-1)) and y-faces ((Ny-1) x Nx).
    If mu_cell is None, return ones.
    Use harmonic mean for conductivity-like weighting; fall back to arithmetic if needed.
    """
    if mu_cell is None:
        mux = np.ones((Ny, Nx - 1), dtype=float)
        muy = np.ones((Ny - 1, Nx), dtype=float)
        return mux, muy
    mu = np.asarray(mu_cell, dtype=float)
    # x-faces between i and i+1
    left = mu[:, :-1]
    right = mu[:, 1:]
    with np.errstate(divide='ignore', invalid='ignore'):
        mux = 2.0 / (1.0 / np.maximum(left, 1e-12) + 1.0 / np.maximum(right, 1e-12))
    mux[~np.isfinite(mux)] = 0.5 * (left[~np.isfinite(mux)] + right[~np.isfinite(mux)]) if np.any(~np.isfinite(mux)) else mux[~np.isfinite(mux)]
    # y-faces between j and j+1
    down = mu[:-1, :]
    up = mu[1:, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        muy = 2.0 / (1.0 / np.maximum(down, 1e-12) + 1.0 / np.maximum(up, 1e-12))
    muy[~np.isfinite(muy)] = 0.5 * (down[~np.isfinite(muy)] + up[~np.isfinite(muy)]) if np.any(~np.isfinite(muy)) else muy[~np.isfinite(muy)]
    return mux, muy


def _grad_faces(phi: np.ndarray, a: float) -> Tuple[np.ndarray, np.ndarray]:
    """Face gradients using centered (forward) differences at faces.
    Returns (dx_phi on x-faces Ny x (Nx-1), dy_phi on y-faces (Ny-1) x Nx).
    """
    dx_face = (phi[:, 1:] - phi[:, :-1]) / a  # Ny x (Nx-1)
    dy_face = (phi[1:, :] - phi[:-1, :]) / a  # (Ny-1) x Nx
    return dy_face, dx_face  # maintain (gy_face, gx_face) ordering for compatibility


def _div_mu_grad(phi: np.ndarray, a: float, c2: float, mux: np.ndarray, muy: np.ndarray) -> np.ndarray:
    """Discrete operator: c^2 [D_x(mux D_x phi) + D_y(muy D_y phi)] on cell centers.
    mux shape Ny x (Nx-1), muy shape (Ny-1) x Nx.
    """
    Ny, Nx = phi.shape
    # face gradients
    gy_face, gx_face = _grad_faces(phi, a)
    # x-fluxes on faces: Fx = mux * D_x phi
    Fx = mux * gx_face  # Ny x (Nx-1)
    # y-fluxes on faces: Fy = muy * D_y phi
    Fy = muy * gy_face  # (Ny-1) x Nx
    # divergence back to cells (zero-Neumann mirrors at domain edges)
    div = np.zeros_like(phi)
    # x-part: (Fx[i+1/2] - Fx[i-1/2]) / a
    div[:, 1:-1] += (Fx[:, 1:] - Fx[:, :-1]) / a
    # boundaries: copy one-sided (Neumann-like)
    div[:, 0] += (Fx[:, 0] - 0.0) / a
    div[:, -1] += (0.0 - Fx[:, -1]) / a
    # y-part
    div[1:-1, :] += (Fy[1:, :] - Fy[:-1, :]) / a
    div[0, :] += (Fy[0, :] - 0.0) / a
    div[-1, :] += (0.0 - Fy[-1, :]) / a
    return c2 * div


def _energy_density_face_split(phi: np.ndarray, pi_half: np.ndarray, c2: float, mux: np.ndarray, muy: np.ndarray, a: float, V: np.ndarray) -> np.ndarray:
    """Per-cell energy using symmetric face split (conservation-matching).
    e_ij = 0.5*pi^2 + 0.5*V*phi^2 + (1/4)*c^2*sum_{faces adj to cell} mu_face (D phi on face)^2
    Each face contributes half of its 0.5*c^2*mu*(grad)^2 to each adjacent cell.
    """
    Ny, Nx = phi.shape
    e = 0.5 * (pi_half * pi_half) + 0.5 * V * (phi * phi)
    gy_face, gx_face = _grad_faces(phi, a)
    # x-faces: contribution 0.25*c2*mux*(Dx phi)^2 to left and right cells
    ex = 0.25 * c2 * (mux * (gx_face * gx_face))  # Ny x (Nx-1)
    e[:, :-1] += ex
    e[:, 1:] += ex
    # y-faces: contribution 0.25*c2*muy*(Dy phi)^2 to bottom and top cells
    ey = 0.25 * c2 * (muy * (gy_face * gy_face))  # (Ny-1) x Nx
    e[:-1, :] += ey
    e[1:, :] += ey
    return e


def _poynting_faces(pi_n: np.ndarray, phi: np.ndarray, c2: float, mux: np.ndarray, muy: np.ndarray, a: float) -> Tuple[np.ndarray, np.ndarray]:
    """Face-based Poynting-like flux components on faces using mid-time pi.
    s_x on x-faces Ny x (Nx-1), s_y on y-faces (Ny-1) x Nx.
    s_x = -c^2 * mux * (D_x phi) * (pi at face), where pi(face) is average of adjacent cells.
    """
    Ny, Nx = pi_n.shape
    gy_face, gx_face = _grad_faces(phi, a)
    # pi averaged to faces
    pi_x_face = 0.5 * (pi_n[:, 1:] + pi_n[:, :-1])
    pi_y_face = 0.5 * (pi_n[1:, :] + pi_n[:-1, :])
    s_x = -c2 * mux * gx_face * pi_x_face
    s_y = -c2 * muy * gy_face * pi_y_face
    return s_y, s_x  # keep (sy, sx) ordering


def main() -> int:
    args = parse_args()
    os.environ["VDM_RUN_SCRIPT"] = Path(__file__).stem
    code_root = Path(__file__).resolve().parents[3]

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    S = Spec(**spec)

    # Approvals
    approved, engineering_only, proposal = check_tag_approval(DOMAIN, S.tag, args.allow_unapproved, code_root)
    quarantine = bool((not approved) or engineering_only)

    # Grid/time
    Nx, Ny = int(S.grid.get("Nx", 128)), int(S.grid.get("Ny", 64))
    Lx, Ly = float(S.grid.get("Lx", 8.0)), float(S.grid.get("Ly", 4.0))
    a = Lx / max(1, Nx)
    dy = Ly / max(1, Ny)
    dt = float(S.time.get("dt", 2.0e-4))
    T = float(S.time.get("T", 2.0))
    steps = int(round(T / dt))
    c = float(S.wave.get("c", 1.0))
    c2 = c * c
    bc_kind = str(S.bc.get("kind", "periodic")).lower()
    # CFL guard (explicit leapfrog)
    CFL = float(S.time.get("CFL", 0.35))
    dt_max = CFL * min(a, dy) / max(c, 1e-12)
    if dt > dt_max:
        # shrink dt and recompute steps to respect T
        dt = dt_max
        steps = int(max(1, np.floor(T / dt)))
        T = steps * dt
        print(f"[wave_flux_meter] dt reduced by CFL guard to {dt:.6g} (steps={steps})")
    warmup_frac = float(S.time.get("warmup_frac", 0.10))

    # Absorber/sponge profile (sigma)
    n_abs = int(S.absorber.get("thickness", 8))
    sigma_max = float(S.absorber.get("sigma_max", 5.0))
    sigma_pow = float(S.absorber.get("power", 2.0))

    # Ports geometry: default vertical windows on left/right interior boundary
    port_frac = float(S.ports.get("height_frac", 0.5))  # fraction of Ny
    port_center = float(S.ports.get("center_frac", 0.5))
    j_half = Ny * port_frac * 0.5
    j_mid = int(round(Ny * port_center))
    j0 = max(0, int(round(j_mid - j_half)))
    j1 = min(Ny, int(round(j_mid + j_half)))
    i_left = n_abs  # interior boundary index (left)
    i_right = Nx - n_abs - 1  # interior boundary index (right)
    port_segments_left = [(j0, j1)]
    port_segments_right = [(j0, j1)]

    # Potential V (frozen). Priority: explicit array -> external mu map -> generated channels -> zeros.
    V_in = S.map.get("V", [])
    mu_loaded = None
    mu_corridor = None  # normalized corridor strength in [0,1]
    if isinstance(V_in, list) and len(V_in) > 0:
        V = np.array(V_in, dtype=float).reshape(Ny, Nx)
    elif S.map.get("mu_path"):
        mu_path = str(S.map.get("mu_path"))
        try:
            mu = np.load(mu_path)
            # Resize to (Ny, Nx) if needed via nearest-neighbor to avoid new deps
            if mu.shape != (Ny, Nx):
                yy = np.linspace(0, mu.shape[0] - 1, Ny)
                xx = np.linspace(0, mu.shape[1] - 1, Nx)
                yi = np.clip(np.round(yy).astype(int), 0, mu.shape[0] - 1)
                xi = np.clip(np.round(xx).astype(int), 0, mu.shape[1] - 1)
                mu = mu[np.ix_(yi, xi)]
            mu_loaded = mu.astype(float)
            # Normalize to [0,1]
            mmin, mmax = float(np.min(mu_loaded)), float(np.max(mu_loaded))
            denom = (mmax - mmin) if (mmax - mmin) > 1e-12 else 1.0
            mu01 = (mu_loaded - mmin) / denom
            # Optionally invert: corridors = high mu -> low V; default aligns with FTMC (high mu = easy flow)
            invert = bool(S.map.get("mu_invert", False))
            mu_eff = (1.0 - mu01) if invert else mu01
            mu_corridor = mu_eff  # corridor strength: larger -> easier path
            walls_V = float(S.map.get("walls_V", 3.0))
            V = walls_V * (1.0 - mu_eff)
            # Zero-out V in absorber region to avoid double-counting impedance and damping
            V[:n_abs, :] = 0.0; V[-n_abs:, :] = 0.0; V[:, :n_abs] = 0.0; V[:, -n_abs:] = 0.0
        except Exception as e:
            print(f"[wave_flux_meter] Failed to load mu map '{mu_path}': {e}. Falling back to generated channels or zeros.")
            V = np.zeros((Ny, Nx), dtype=float)
    else:
        # Generate from 'walls_V' and optional 'channels' list of rectangles.
        walls_V = float(S.map.get("walls_V", 0.0))
        V = np.zeros((Ny, Nx), dtype=float)
        if walls_V > 0.0:
            # Start with walls everywhere in the interior box, then carve zero-V channels.
            V[n_abs:Ny - n_abs, n_abs:Nx - n_abs] = walls_V
            chans = S.map.get("channels", []) or [{}]
            for ch in chans:
                # Defaults: span full interior in x, and port window in y.
                x0 = int(ch.get("x0", n_abs))
                x1 = int(ch.get("x1", Nx - n_abs))
                y0 = int(ch.get("y0", 0))
                y1 = int(ch.get("y1", 0))
                # If y not provided, use port window [j0:j1)
                if (y1 <= y0):
                    y0 = j0
                    y1 = j1
                x0 = max(n_abs, min(x0, Nx - n_abs))
                x1 = max(x0 + 1, min(x1, Nx - n_abs))
                y0 = max(n_abs, min(y0, Ny - n_abs))
                y1 = max(y0 + 1, min(y1, Ny - n_abs))
                V[y0:y1, x0:x1] = 0.0
    map_hash_start = sha256_array(V)

    # Damping sigma(x,y)
    sigma = np.zeros((Ny, Nx), dtype=float)
    # distance (in cells) to interior box
    # interior indices: [n_abs, Nx-n_abs-1] x [n_abs, Ny-n_abs-1]
    X = np.arange(Nx)[None, :]
    Y = np.arange(Ny)[:, None]
    di = np.maximum(0, np.maximum(n_abs - X, X - (Nx - n_abs - 1)))
    dj = np.maximum(0, np.maximum(n_abs - Y, Y - (Ny - n_abs - 1)))
    d = np.maximum(di, dj).astype(float)
    with np.errstate(divide='ignore', invalid='ignore'):
        prof = (d / max(1, n_abs)) ** sigma_pow
    sigma = sigma_max * prof
    sigma[d <= 0] = 0.0  # zero inside interior

    # Initial conditions: symmetric central Gaussian pulse (phi) with outward momentum (pi)
    x = (np.arange(Nx) + 0.5) * a
    y = (np.arange(Ny) + 0.5) * (Ly / max(1, Ny))
    XX, YY = np.meshgrid(x, y)
    x0, y0 = 0.5 * Lx, 0.5 * Ly
    w = 0.2 * Lx
    phi = np.exp(-(((XX - x0) ** 2 + (YY - y0) ** 2) / (2 * (w ** 2))))
    # radial outward pi via gradient of Gaussian
    # gradient for initializing outward momentum
    gy0 = 0.5 * (np.roll(phi, -1, axis=0) - np.roll(phi, 1, axis=0)) / a
    gx0 = 0.5 * (np.roll(phi, -1, axis=1) - np.roll(phi, 1, axis=1)) / a
    pi0 = -(gx0 * (XX - x0) + gy0 * (YY - y0))
    pi = np.copy(pi0)

    # Build face-based mu (toggle μ-weighting via spec: wave.use_mu_weighting)
    use_mu_faces = bool(S.wave.get("use_mu_weighting", False))
    mux, muy = _build_face_mu(mu_corridor if use_mu_faces else None, Ny, Nx)

    # Start leapfrog with damping (explicit sigma term) using divergence form
    Lphi = _div_mu_grad(phi, a, c2, mux, muy) - V * phi
    pi_half = pi + 0.5 * dt * (Lphi - sigma * pi)
    pi_half_prev = np.copy(pi_half)

    # Helpers
    def energy_density(phi_, pi_half_):
        return _energy_density_face_split(phi_, pi_half_, c2, mux, muy, a, V)

    def poynting(pi_n_, phi_):
        return _poynting_faces(pi_n_, phi_, c2, mux, muy, a)

    def interior_mask() -> np.ndarray:
        mask = np.zeros((Ny, Nx), dtype=bool)
        mask[n_abs:Ny - n_abs, n_abs:Nx - n_abs] = True
        return mask

    M_in = interior_mask()
    M_abs = ~M_in

    # If a mobility map is available, auto-detect port segments aligned to channels that actually connect across.
    if mu_corridor is not None and bool(S.ports.get("auto_from_mu", True)):
        # Threshold corridor mask using interior quantile
        mu_int = mu_corridor[n_abs:Ny - n_abs, n_abs:Nx - n_abs]
        q = float(S.ports.get("mu_thresh_quantile", 0.8))
        thresh = float(np.quantile(mu_int, q))
        corridor = (mu_corridor >= thresh) & M_in

        def contiguous_segments(mask_1d: np.ndarray, offset: int, min_len: int) -> list[tuple[int, int]]:
            segs = []
            start = None
            for k in range(mask_1d.size):
                if mask_1d[k] and start is None:
                    start = k
                if ((not mask_1d[k]) or k == mask_1d.size - 1) and start is not None:
                    end = k if not mask_1d[k] else (k + 1)
                    if (end - start) >= min_len:
                        segs.append((offset + start, offset + end))
                    start = None
            return segs

        def bfs_from_left_to_right(corr: np.ndarray) -> Tuple[list[tuple[int,int]], list[tuple[int,int]]]:
            # Restrict BFS to port window rows [j0:j1)
            rows = range(j0, j1)
            cols = range(i_left, i_right + 1)
            visited = np.zeros_like(corr, dtype=bool)
            dq = deque()
            # Seed with left boundary cells within corridor and port window
            for j in rows:
                if corr[j, i_left]:
                    visited[j, i_left] = True
                    dq.append((j, i_left))
            # BFS
            while dq:
                j, i = dq.popleft()
                for dj, di in ((1,0),(-1,0),(0,1),(0,-1)):
                    jj, ii = j + dj, i + di
                    if (jj >= j0 and jj < j1) and (ii >= i_left and ii <= i_right):
                        if corr[jj, ii] and not visited[jj, ii]:
                            visited[jj, ii] = True
                            dq.append((jj, ii))
            # Extract contiguous segments at left and right boundaries where visited True
            min_len = int(S.ports.get("min_band_cells", max(2, Ny // 64)))
            left_mask = visited[j0:j1, i_left]
            right_mask = visited[j0:j1, i_right]
            left_segs = contiguous_segments(left_mask, j0, min_len)
            right_segs = contiguous_segments(right_mask, j0, min_len)
            # Fallback if nothing detected: use full port window
            if not left_segs:
                left_segs = [(j0, j1)]
            if not right_segs:
                right_segs = [(j0, j1)]
            return left_segs, right_segs

        port_segments_left, port_segments_right = bfs_from_left_to_right(corridor)

        # Optional: geodesic-style single-path across the window to place one narrow band at each boundary
        if bool(S.ports.get("geodesic_path", True)):
            rows = np.arange(j0, j1)
            cols = np.arange(i_left, i_right + 1)
            H = rows.size
            W = cols.size
            if H > 0 and W > 1:
                sub_mu = mu_corridor[rows[:, None], cols[None, :]]
                # cost prefers high mobility (corridor): minimize 1 - mu
                cost = 1.0 - sub_mu
                C = np.full((H, W), np.inf, dtype=float)
                Pidx = np.full((H, W), -1, dtype=int)
                C[:, 0] = cost[:, 0]
                for k in range(1, W):
                    for r in range(H):
                        best_prev = C[r, k - 1]
                        best_r = r
                        if r - 1 >= 0 and C[r - 1, k - 1] < best_prev:
                            best_prev = C[r - 1, k - 1]; best_r = r - 1
                        if r + 1 < H and C[r + 1, k - 1] < best_prev:
                            best_prev = C[r + 1, k - 1]; best_r = r + 1
                        C[r, k] = cost[r, k] + best_prev
                        Pidx[r, k] = best_r
                # Backtrack best terminal
                r_end = int(np.argmin(C[:, -1]))
                path_rows = [r_end]
                for k in range(W - 1, 0, -1):
                    r_prev = Pidx[path_rows[-1], k]
                    if r_prev < 0:
                        r_prev = path_rows[-1]
                    path_rows.append(r_prev)
                path_rows = list(reversed(path_rows))
                j_left_center = rows[path_rows[0]]
                j_right_center = rows[path_rows[-1]]
                hw = int(S.ports.get("band_halfwidth", max(2, Ny // 128)))
                ls = max(j0, int(j_left_center - hw)); le = min(j1, int(j_left_center + hw))
                rs = max(j0, int(j_right_center - hw)); re = min(j1, int(j_right_center + hw))
                if le > ls and re > rs:
                    port_segments_left = [(ls, le)]
                    port_segments_right = [(rs, re)]

        # Optionally snap to top-K peak rows of mobility at each boundary to avoid overly broad segments
        if bool(S.ports.get("snap_peaks", True)):
            K = int(S.ports.get("num_bands", 2))
            hw = int(S.ports.get("band_halfwidth", max(2, Ny // 128)))
            profL = mu_corridor[j0:j1, i_left]
            profR = mu_corridor[j0:j1, i_right]
            # top-K indices (without duplicates) sorted by value descending
            idxL = np.argpartition(-profL, range(min(K, profL.size)))[:K]
            idxR = np.argpartition(-profR, range(min(K, profR.size)))[:K]
            idxL = idxL[np.argsort(-profL[idxL])]
            idxR = idxR[np.argsort(-profR[idxR])]
            def bands_from_peaks(idx_arr: np.ndarray) -> list[tuple[int,int]]:
                used = []
                bands = []
                for idx in idx_arr:
                    # skip if overlaps an existing band
                    j_center = j0 + int(idx)
                    j_start = max(j0, j_center - hw)
                    j_end = min(j1, j_center + hw)
                    if any(not (j_end <= s or j_start >= e) for (s,e) in bands):
                        continue
                    bands.append((j_start, j_end))
                return bands or [(j0, j1)]
            port_segments_left = bands_from_peaks(idxL)
            port_segments_right = bands_from_peaks(idxR)

    # Time series
    E_interior = []
    P_left = []           # port-only over detected segments
    P_right = []          # port-only over detected segments
    P_out_full_series = []  # full boundary flux (all four sides)
    balance_resid = []  # |dE_in/dt + P_out|
    dE_dt_series = []   # centered dE/dt values
    P_out_centered = [] # P_out aligned with centered derivative
    Q_abs_series = []  # instantaneous absorber dissipation

    # Initialize energies
    e_curr = energy_density(phi, pi_half)
    e_prev = None

    for n in range(steps):
        # compute pi at integer time for flux and dissipation
        pi_n = 0.5 * (pi_half + pi_half_prev)
        sy, sx = poynting(pi_n, phi)
        # sample flux on interior rectangle faces for ports
        # Face indices for interior rectangle
        j_min, j_max = n_abs, Ny - n_abs  # rows in interior (cells)
        i_min, i_max = n_abs, Nx - n_abs  # cols in interior (cells)
        i_face_left = i_min - 1    # x-face index for left boundary (between i_min-1 and i_min)
        i_face_right = i_max - 1   # x-face index for right boundary (between i_max-1 and i_max)
        j_face_bottom = j_min - 1  # y-face index for bottom boundary
        j_face_top = j_max - 1     # y-face index for top boundary
        # Line integrals across port windows: multiply by edge length dy
        # Sum flux across possibly multiple vertical segments aligned to channels
        P_L = 0.0
        for (jj0, jj1) in port_segments_left:
            # clamp to interior window
            j0c = max(jj0, j_min)
            j1c = min(jj1, j_max)
            if j1c > j0c and (i_face_left >= 0):
                # outward normal at left is -x => flux = -s_x
                P_L += float(np.sum((-1.0) * sx[j0c:j1c, i_face_left]) * dy)
        P_R = 0.0
        for (jj0, jj1) in port_segments_right:
            j0c = max(jj0, j_min)
            j1c = min(jj1, j_max)
            if j1c > j0c and (i_face_right < sx.shape[1]):
                # outward normal at right is +x => flux = +s_x
                P_R += float(np.sum((+1.0) * sx[j0c:j1c, i_face_right]) * dy)
        P_left.append(P_L)
        P_right.append(P_R)

        # Full boundary flux across entire interior boundary (four sides)
        # Left side outward normal -x
        if i_face_left >= 0:
            P_left_full = float(np.sum((-1.0) * sx[j_min:j_max, i_face_left]) * dy)
        else:
            P_left_full = 0.0
        # Right side outward normal +x
        if i_face_right < sx.shape[1]:
            P_right_full = float(np.sum((+1.0) * sx[j_min:j_max, i_face_right]) * dy)
        else:
            P_right_full = 0.0
        # Bottom side outward normal -y (note: sy shape (Ny-1) x Nx, sum over i in [i_min:i_max))
        if j_face_bottom >= 0:
            P_bottom_full = float(np.sum((-1.0) * sy[j_face_bottom, i_min:i_max]) * a)
        else:
            P_bottom_full = 0.0
        # Top side outward normal +y
        if j_face_top < sy.shape[0]:
            P_top_full = float(np.sum((+1.0) * sy[j_face_top, i_min:i_max]) * a)
        else:
            P_top_full = 0.0
        P_out_full = P_left_full + P_right_full + P_bottom_full + P_top_full
        P_out_full_series.append(P_out_full)

        # absorber dissipation: Q = ∫_{absorber} sigma * pi^2 dA (per unit time)
        # Volume integral in absorber: multiply by cell area a^2
        Q_abs = float(np.sum(sigma * (pi_n * pi_n) * M_abs) * (a * a))
        Q_abs_series.append(Q_abs)

        # total interior energy at t=n
        # Interior energy integral: sum(e) * cell area
        E_interior.append(float(np.sum(e_curr[M_in]) * (a * a)))

        # advance one step (explicit damping)
        Lphi = _div_mu_grad(phi, a, c2, mux, muy) - V * phi
        pi_half_new = pi_half + dt * (Lphi - sigma * pi_half)
        phi_new = phi + dt * pi_half_new
        # energy at n+1
        e_next = energy_density(phi_new, pi_half_new)

        # balance residual using first-difference dE/dt aligned to time n (matches P_out computed with pi_n)
        if e_prev is not None:
            dE_dt = float(((np.sum(e_curr[M_in]) - np.sum(e_prev[M_in])) * (a * a)) / dt)
            P_out = P_out_full
            balance_resid.append(abs(dE_dt + P_out))
            dE_dt_series.append(dE_dt)
            P_out_centered.append(P_out)
        else:
            balance_resid.append(float('nan'))

        # rotate state
        e_prev = e_curr
        e_curr = e_next
        pi_half_prev = pi_half
        pi_half = pi_half_new
        phi = phi_new

    # drop first NaN
    balance_vals = [v for v in balance_resid if (v == v)]

    # KPIs (exclude warm-up window)
    P_left_arr = np.array(P_left, dtype=float)
    P_right_arr = np.array(P_right, dtype=float)
    P_tot = P_left_arr + P_right_arr
    P_out_full_arr = np.array(P_out_full_series, dtype=float)
    # centered arrays have length steps-1; compute warm-up cutoff index for centered series
    n_center = len(dE_dt_series)
    k0 = int(max(0, min(n_center, np.floor(warmup_frac * max(n_center, 1)))))
    dE_dt_c = np.array(dE_dt_series[k0:], dtype=float)
    P_out_c = np.array(P_out_centered[k0:], dtype=float)
    bal_c = np.array(balance_vals[k0:], dtype=float)
    mean_P = float(np.mean(np.abs(P_out_c)) + 1e-12)
    mean_balance_err = float(np.mean(bal_c)) if bal_c.size else float('inf')
    rel_balance_err = float(mean_balance_err / mean_P)
    # symmetry computed on same window length as P series (skip first sample count equivalent to warmup_frac)
    k0_ports = int(max(0, min(len(P_left_arr), np.floor(warmup_frac * max(len(P_left_arr), 1)))))
    P_left_c = P_left_arr[k0_ports:]
    P_right_c = P_right_arr[k0_ports:]
    P_tot_c = P_left_c + P_right_c
    symmetry_diff = float(np.mean(np.abs(P_left_c - P_right_c)) / (np.mean(np.abs(P_tot_c)) + 1e-12)) if P_left_c.size else float('inf')
    # R^2 diagnostics
    def _safe_r2(x: np.ndarray, y: np.ndarray) -> float:
        if len(x) < 3 or np.allclose(np.std(x), 0.0) or np.allclose(np.std(y), 0.0):
            return 0.0
        r = np.corrcoef(x, y)[0, 1]
        if not (r == r):
            return 0.0
        return float(r * r)
    balance_r2 = _safe_r2(-dE_dt_c, P_out_c)
    sym_mask = (np.abs(P_tot_c) > 1e-12)
    if np.count_nonzero(sym_mask) >= 3:
        symmetry_r2 = _safe_r2(P_left_c[sym_mask], P_right_c[sym_mask])
    else:
        symmetry_r2 = 0.0
    # absorber efficiency via time integral comparison
    dt_arr = dt
    # Trapezoidal time integration for energies
    if P_out_full_arr.size >= 2:
        E_inflow_to_abs = float(np.trapezoid(P_out_full_arr, dx=dt_arr))
    else:
        E_inflow_to_abs = float(np.sum(P_out_full_arr) * dt_arr)
    q_abs_arr = np.array(Q_abs_series, dtype=float)
    if q_abs_arr.size >= 2:
        E_diss_abs = float(np.trapezoid(q_abs_arr, dx=dt_arr))
    else:
        E_diss_abs = float(np.sum(q_abs_arr) * dt_arr)
    absorber_eff = float(0.0 if E_inflow_to_abs == 0.0 else E_diss_abs / E_inflow_to_abs)

    # Gates (tight Phase B acceptance)
    gate_r2 = balance_r2 >= float(S.ports.get("gate_balance_r2", 0.9995))
    gate_imbalance = rel_balance_err <= float(S.ports.get("gate_imbalance_rel", 0.005))  # ≤0.5%
    # Back-compat balance gate at 10%
    gate_balance_rel_legacy = rel_balance_err <= float(S.ports.get("gate_balance_rel", 0.1))
    # Symmetry gate applicability: disable by default when using an external mu map (asym geometry)
    symmetry_applicable = bool(S.ports.get("symmetry_applicable", S.map.get("mu_path") is None))
    gate_symmetry = True if (not symmetry_applicable) else (symmetry_diff <= float(S.ports.get("gate_symmetry_rel", 0.005)))
    gate_absorber = absorber_eff >= float(S.absorber.get("gate_efficiency", 0.9))   # ≥90%
    passed = bool(gate_r2 and gate_imbalance and gate_symmetry and gate_absorber)

    # Artifacts
    import matplotlib.pyplot as plt
    apply_style("light")
    # Build a time axis in seconds for readability
    t = np.arange(len(E_interior), dtype=float) * dt
    # Balance residual series aligned to steps (prepend NaN for first point)
    bal_series = [float('nan')] + balance_vals
    if len(bal_series) < len(E_interior):
        bal_series += [bal_series[-1]] * (len(E_interior) - len(bal_series))

    fig, (ax0, ax1) = plt.subplots(2, 1, sharex=True, figsize=(8.5, 5.2))
    fig.suptitle(f"Wave Flux Meter — Phase B (open ports) — tag: {S.tag}")

    # Top: interior energy
    ax0.plot(t, E_interior, label="E_interior", color="#1f77b4")
    ax0.set_ylabel("Energy E_interior [J]")
    ax0.grid(True, alpha=0.3)
    ax0.legend(loc="best")

    # Bottom: port powers and balance
    ax1.plot(t, P_left, label="P_left [J/s]", color="#2ca02c")
    ax1.plot(t, P_right, label="P_right [J/s]", color="#d62728")
    ax1.plot(t, bal_series, label="|dE/dt + P_out| [J/s]", color="#9467bd")
    ax1.set_xlabel("Time t [s]")
    ax1.set_ylabel("Power [J/s]")
    ax1.grid(True, alpha=0.3)
    # Shade warm-up window
    if warmup_frac > 0:
        ax0.axvspan(0.0, warmup_frac * T, color="#ffcc00", alpha=0.12, label="warm-up")
        ax1.axvspan(0.0, warmup_frac * T, color="#ffcc00", alpha=0.12)
    # Annotate accuracy metrics (R^2 and relative error)
    sym_applicable = bool(S.ports.get("symmetry_applicable", S.map.get("mu_path") is None))
    annot_lines = [
        f"balance: R^2(-dE/dt, P_out)={balance_r2:.4f}; rel_err={rel_balance_err:.4f}",
        (f"symmetry: R^2(P_L,P_R)={symmetry_r2:.3f}" if sym_applicable else "symmetry: N/A (asymmetric μ)")
    ]
    ax1.text(0.99, 0.98, "\n".join(annot_lines), transform=ax1.transAxes,
             va='top', ha='right', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.75, edgecolor='#cccccc'))
    ax1.legend(loc="upper left", framealpha=0.85)
    failed = bool((not approved) or passed is False or engineering_only)
    fig_path = figure_path_by_tag(DOMAIN, "wave_flux_meter_openports_timeseries", S.tag, failed=failed)
    fig.savefig(fig_path, bbox_inches="tight")

    # Optional channel map figure (if V was generated or provided)
    fig_map_path = None
    try:
        fig_map, axm = plt.subplots(1, 1, figsize=(6.5, 3.0))
        # Prefer showing mu if provided; else show V
        if mu_loaded is not None:
            im = axm.imshow(mu_loaded, origin="lower", cmap="magma",
                            extent=(0, Lx, 0, Ly), aspect="auto")
            cb_label = "mu (mobility) [arb]"
        else:
            im = axm.imshow(V, origin="lower", cmap="viridis",
                        extent=(0, Lx, 0, Ly), aspect="auto")
            cb_label = "V [arb]"
        axm.set_title("Channel map: loaded map with ports and interior")
        axm.set_xlabel("x [arb]")
        axm.set_ylabel("y [arb]")
        cb = fig_map.colorbar(im, ax=axm, shrink=0.9)
        cb.set_label(cb_label)
        # Draw interior rectangle
        xL = n_abs * a
        xR = (Nx - n_abs) * a
        yB = n_abs * dy
        yT = (Ny - n_abs) * dy
        axm.plot([xL, xR, xR, xL, xL], [yB, yB, yT, yT, yB], color="w", lw=1.2, label="interior")
        # Ports as vertical segments at interior boundary (could be multiple bands)
        xpL = (i_left + 0.5) * a
        xpR = (i_right + 0.5) * a
        for idx, (jj0, jj1) in enumerate(port_segments_left):
            axm.plot([xpL, xpL], [jj0 * dy, jj1 * dy], color="#2ca02c", lw=3.0, solid_capstyle='butt', label="left port" if idx == 0 else None)
        for idx, (jj0, jj1) in enumerate(port_segments_right):
            axm.plot([xpR, xpR], [jj0 * dy, jj1 * dy], color="#d62728", lw=3.0, solid_capstyle='butt', label="right port" if idx == 0 else None)
        # If channels were defined, draw their rectangles
        chans = S.map.get("channels", []) if isinstance(S.map.get("channels", []), list) else []
        for ch in chans:
            cx0 = int(ch.get("x0", n_abs)); cx1 = int(ch.get("x1", Nx - n_abs))
            cy0 = ch.get("y0"); cy1 = ch.get("y1")
            if cy0 is None or cy1 is None or cy1 <= cy0:
                cy0 = j0; cy1 = j1
            cx0 = max(n_abs, min(cx0, Nx - n_abs)); cx1 = max(cx0 + 1, min(cx1, Nx - n_abs))
            cy0 = max(n_abs, min(int(cy0), Ny - n_abs)); cy1 = max(cy0 + 1, min(int(cy1), Ny - n_abs))
            xr = np.array([cx0, cx1, cx1, cx0, cx0], dtype=float) * a
            yr = np.array([cy0, cy0, cy1, cy1, cy0], dtype=float) * dy
            axm.plot(xr, yr, color="w", lw=1.0, ls=":", label="channel" if ch is chans[0] else None)
        axm.legend(loc="upper right", framealpha=0.6)
        fig_map_path = figure_path_by_tag(DOMAIN, "wave_flux_meter_channel_map", S.tag, failed=failed)
        fig_map.savefig(fig_map_path, bbox_inches="tight")
    except Exception as e:
        # Non-fatal: map figure is optional. Print once to stdout for traceability.
        print(f"[wave_flux_meter] map-figure generation skipped: {e}")

    # Dashboard: combine map + energy + powers in one figure
    fig_dash_path = None
    try:
        from matplotlib import gridspec
        figd = plt.figure(figsize=(14.5, 6.0))
        gs = figd.add_gridspec(2, 2, height_ratios=[1, 1], wspace=0.28, hspace=0.35)
        axm2 = figd.add_subplot(gs[0, :])
        axe = figd.add_subplot(gs[1, 0])
        axp = figd.add_subplot(gs[1, 1])

        # Map panel
        if mu_loaded is not None:
            im2 = axm2.imshow(mu_loaded, origin="lower", cmap="magma", extent=(0, Lx, 0, Ly), aspect="auto")
            cbl = "mu (mobility) [arb]"
        else:
            im2 = axm2.imshow(V, origin="lower", cmap="viridis", extent=(0, Lx, 0, Ly), aspect="auto")
            cbl = "V [arb]"
        cb2 = figd.colorbar(im2, ax=axm2, shrink=0.9)
        cb2.set_label(cbl)
        axm2.set_title("Channel map with interior and ports")
        axm2.set_xlabel("x [arb]")
        axm2.set_ylabel("y [arb]")
        # Interior box
        xL = n_abs * a; xR = (Nx - n_abs) * a; yB = n_abs * dy; yT = (Ny - n_abs) * dy
        axm2.plot([xL, xR, xR, xL, xL], [yB, yB, yT, yT, yB], color="w", lw=1.2, label="interior")
        # Ports
        xpL = (i_left + 0.5) * a; xpR = (i_right + 0.5) * a
        for idx, (jj0, jj1) in enumerate(port_segments_left):
            axm2.plot([xpL, xpL], [jj0 * dy, jj1 * dy], color="#2ca02c", lw=3.0, solid_capstyle='butt', label="left port" if idx == 0 else None)
        for idx, (jj0, jj1) in enumerate(port_segments_right):
            axm2.plot([xpR, xpR], [jj0 * dy, jj1 * dy], color="#d62728", lw=3.0, solid_capstyle='butt', label="right port" if idx == 0 else None)
        axm2.legend(loc="upper right", framealpha=0.6)

        # Energy panel
        axe.plot(t, E_interior, color="#1f77b4")
        axe.set_title("Interior energy vs time")
        axe.set_xlabel("t [s]")
        axe.set_ylabel("E_int [J]")
        axe.grid(True, alpha=0.3)

        # Power panel
        axp.plot(t, P_left, label="P_left [J/s]", color="#2ca02c")
        axp.plot(t, P_right, label="P_right [J/s]", color="#d62728")
        axp.plot(t, bal_series, label="|dE/dt + P_out| [J/s]", color="#9467bd")
        axp.set_title("Port powers and balance")
        axp.set_xlabel("t [s]")
        axp.set_ylabel("Power [J/s]")
        axp.grid(True, alpha=0.3)
        sym_applicable = bool(S.ports.get("symmetry_applicable", S.map.get("mu_path") is None))
        annot = [
            f"balance R^2={balance_r2:.4f}, rel_err={rel_balance_err:.4f}",
            (f"sym R^2={symmetry_r2:.3f}" if sym_applicable else "sym: N/A (asymmetric μ)")
        ]
        axp.text(0.99, 0.98, "\n".join(annot), transform=axp.transAxes, va='top', ha='right', fontsize=9,
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.75, edgecolor='#cccccc'))
        axp.legend(loc="upper left", framealpha=0.85)

        figd.suptitle(f"Wave Flux Meter — Open Ports — {S.tag}")
        fig_dash_path = figure_path_by_tag(DOMAIN, "wave_flux_meter_openports_dashboard", S.tag, failed=failed)
        figd.savefig(fig_dash_path, bbox_inches="tight")
    except Exception as e:
        print(f"[wave_flux_meter] dashboard generation skipped: {e}")

    # CSV
    commit_full, commit_short = _git_hashes(code_root)
    csv_metrics = {
        "timestamp": datetime.now().isoformat(),
        "domain": DOMAIN,
        "tag": S.tag,
    "approved": bool(approved),
        "quarantined": bool(failed),
        "passed": bool(passed),
        "Nx": int(Nx),
        "Ny": int(Ny),
        "dt": float(dt),
        "steps": int(steps),
    "rel_balance_err": float(rel_balance_err),
    "balance_r2": float(balance_r2),
        "symmetry_diff": float(symmetry_diff),
        "symmetry_r2": float(symmetry_r2),
        "absorber_efficiency": float(absorber_eff),
        "port_j0": int(j0),
        "port_j1": int(j1),
        "n_abs": int(n_abs),
        "sigma_max": float(sigma_max),
        "commit": commit_short,
    }
    csv_path = log_path_by_tag(DOMAIN, "wave_flux_meter_openports_v1_metrics", S.tag, failed=failed, type="csv")
    write_log(csv_path, csv_metrics)

    # JSON summary
    json_path = log_path_by_tag(DOMAIN, "wave_flux_meter_openports_v1_summary", S.tag, failed=failed, type="json")
    summary = {
        "tag": S.tag,
        "domain": DOMAIN,
        "provenance": {"commit_full": commit_full, "commit": commit_short},
        "env": {"threads": int(os.getenv("OMP_NUM_THREADS", "1")), "blas": "openblas", "fft": "numpy.pocketfft"},
        "passed": passed,
        "gates": {
            "power_balance_rel": bool(gate_balance_rel_legacy),
            "power_balance_r2": bool(gate_r2),
            "power_imbalance_rel": bool(gate_imbalance),
            "symmetry_null_rel": bool(gate_symmetry),
            "absorber_efficiency": bool(gate_absorber)
        },
        "kpi": {
            "power_balance_rel": {"mean_abs": float(rel_balance_err), "tol": float(S.ports.get("gate_balance_rel", 0.1))},
            "power_balance_r2": {"value": float(balance_r2), "tol": float(S.ports.get("gate_balance_r2", 0.9995))},
            "power_imbalance_rel": {"mean_abs": float(rel_balance_err), "tol": float(S.ports.get("gate_imbalance_rel", 0.005))},
            "symmetry_null_rel": {"mean_abs": float(symmetry_diff), "tol": float(S.ports.get("gate_symmetry_rel", 0.05)), "applicable": bool(symmetry_applicable)},
            "absorber_efficiency": {"value": float(absorber_eff), "tol": float(S.absorber.get("gate_efficiency", 0.9))}
        },
        "geometry": {
            "Nx": int(Nx), "Ny": int(Ny), "Lx": float(Lx), "Ly": float(Ly),
            "n_abs": int(n_abs), "port_y": [int(j0), int(j1)], "i_left": int(i_left), "i_right": int(i_right),
            "port_segments": {"left": [[int(a), int(b)] for (a,b) in port_segments_left], "right": [[int(a), int(b)] for (a,b) in port_segments_right]},
            "ports_auto_from_mu": bool(mu_corridor is not None and bool(S.ports.get("auto_from_mu", True)))
        },
        "compliance": {
            "map_immutable": bool(sha256_array(V) == map_hash_start),
            "probe_limit": True,
            "absorber_static": True
        },
    "artifacts": {"figures": [str(p) for p in [fig_path, fig_map_path, fig_dash_path] if p], "logs": [str(csv_path), str(json_path)]},
        "policy": {"approved": bool(approved), "engineering_only": bool(engineering_only), "quarantined": bool(failed)}
    }
    summary["numerics"] = {"use_mu_weighting": bool(S.wave.get("use_mu_weighting", False)), "CFL": float(S.time.get("CFL", 0.35)), "warmup_frac": float(warmup_frac)}
    write_log(json_path, summary)
    print(json.dumps({"summary_path": str(json_path), "approved": approved}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
