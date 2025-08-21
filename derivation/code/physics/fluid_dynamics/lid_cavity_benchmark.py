#!/usr/bin/env python3
"""
Lid-driven cavity (2-D) incompressibility benchmark for the fluids sector.

CHANGE REASON:
- Relocated into derivation/code/physics/fluid_dynamics per repo rules (no Prometheus_FUVDM/bench/).
- Outputs follow RD harness: derivation/code/outputs/{figures,logs}.
- Ensures JSON uses native Python types to avoid numpy serialization issues.

Outputs (defaults):
- Figures → derivation/code/outputs/figures/<script>_<timestamp>.png
- Logs    → derivation/code/outputs/logs/<script>_<timestamp>.json
"""

import os, json, time, argparse, shutil
import numpy as np
import matplotlib.pyplot as plt
import math

# Ensure repo root on sys.path for absolute import 'Prometheus_FUVDM.*'; else fall back to file import
import sys, pathlib, importlib.util, os
_P = pathlib.Path(__file__).resolve()
for _anc in [_P] + list(_P.parents):
    if _anc.name == "Prometheus_FUVDM":
        _ROOT = str(_anc.parent)
        if _ROOT not in sys.path:
            sys.path.insert(0, _ROOT)
        break

try:
    from Prometheus_FUVDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig, CS2  # noqa: E402
except Exception:
    # Fallback: load lbm2d.py directly by file path (no package/module requirement)
    _lbm_path = os.path.join(os.path.dirname(__file__), "fluids", "lbm2d.py")
    spec = importlib.util.spec_from_file_location("lbm2d_local", _lbm_path)
    _m = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(_m)
    LBM2D = _m.LBM2D
    LBMConfig = _m.LBMConfig
    CS2 = getattr(_m, "CS2", 1.0/3.0)

# Dimensionless helpers (LBM units)
try:
    from Prometheus_FUVDM.derivation.code.common.dimensionless_fuvdm import (
        lbm_viscosity_from_tau, reynolds_lbm, mach_lbm
    )
except Exception:
    lbm_viscosity_from_tau = lambda tau: (float(tau) - 0.5) / 3.0
    def reynolds_lbm(U, L, tau):
        return float(U) * float(L) / (lbm_viscosity_from_tau(tau) + 1e-15)
    def mach_lbm(U):
        return float(U) / (1.0 / np.sqrt(3.0))


class AutoTuner:
    """Adaptive controller for lid cavity (LBM + void dynamics)."""
    def __init__(self, nx, ny, U_init, tau_init, void_gain_init,
                 Ma_max=0.10, Re_target=None, div_target=1e-6):
        self.L = float(max(nx, ny) - 2)          # characteristic length (cells, interior)
        self.U = float(U_init)                    # current lid speed
        self.tau = float(tau_init)                # current tau
        self.g = float(void_gain_init)            # current void gain
        self.Ma_max = float(Ma_max)
        self.Re_target = Re_target
        self.div_target = float(div_target)
        # gentle controller gains (P-like)
        self.k_Ma = 0.50
        self.k_Re = 0.10
        self.k_div_up = 0.50
        self.k_div_dn = 0.02

    def _metrics(self, sim):
        sim.moments()
        speed = np.sqrt(sim.ux**2 + sim.uy**2)
        u_max = float(np.nanmax(speed)) if speed.size else 0.0
        u_rms = float(np.sqrt(np.nanmean(speed**2))) if speed.size else 0.0
        Ma = u_max / math.sqrt(CS2)
        Re_meas = (u_rms * self.L) / (sim.nu + 1e-12)
        div = sim.divergence()
        return {
            "u_max": u_max, "u_rms": u_rms, "Ma": Ma, "Re": Re_meas, "div": div,
            "omega_min": float(getattr(sim, "aggr_omega_min", 0.0)),
            "omega_max": float(getattr(sim, "aggr_omega_max", 0.0)),
            "W_mean": float(getattr(sim, "last_W_mean", 0.0)),
        }

    def step(self, sim):
        """Update U_lid, tau, void gain based on live signals. Report post-clamp Mach (and include pre-clamp for reference)."""
        changed = {}

        # 0) Pre-clamp metrics
        sim.moments()
        speed_pre = np.sqrt(sim.ux**2 + sim.uy**2)
        u_max_pre = float(np.nanmax(speed_pre)) if speed_pre.size else 0.0
        u_rms_pre = float(np.sqrt(np.nanmean(speed_pre**2))) if speed_pre.size else 0.0
        Ma_pre = u_max_pre / math.sqrt(CS2)

        # 1) Mach guard (set clamp first, then measure post-clamp)
        u_cap = self.Ma_max * math.sqrt(CS2)          # target |u|
        sim.cfg.u_clamp = u_cap                       # moments() will enforce this cap

        sim.moments()  # re-compute with clamp enforced
        speed_post = np.sqrt(sim.ux**2 + sim.uy**2)
        u_max_post = float(np.nanmax(speed_post)) if speed_post.size else 0.0
        u_rms_post = float(np.sqrt(np.nanmean(speed_post**2))) if speed_post.size else 0.0
        Ma_post = u_max_post / math.sqrt(CS2)

        # Backoff lid speed based on the pre-clamp Mach (gentle)
        if Ma_pre > 1.05 * self.Ma_max and Ma_pre > 1e-12:
            scale = (self.Ma_max / Ma_pre) ** self.k_Ma
            self.U *= scale
            changed["U_lid"] = self.U

        # 2) Reynolds control through ν (i.e., tau) using post-clamp u_rms
        if self.Re_target:
            nu_target = max(1e-12, (u_rms_post * self.L) / (self.Re_target + 1e-12))
            tau_target = 0.5 + nu_target / CS2
            # relax toward target to avoid oscillation
            self.tau = (1.0 - self.k_Re) * self.tau + self.k_Re * tau_target
            # safe bounds for BGK
            self.tau = min(max(self.tau, 0.51), 1.95)
            sim.tau = self.tau
            sim.omega = 1.0 / self.tau
            changed["tau"] = self.tau

        # 3) Divergence guard through void gain g (evaluate after updates)
        div = sim.divergence()
        if div > self.div_target:
            factor = 1.0 + self.k_div_up * (div / self.div_target - 1.0)
            self.g = min(self.g * factor, 10.0)
            changed["void_gain"] = self.g
        elif div < 0.1 * self.div_target:
            self.g = max(self.g * (1.0 - self.k_div_dn), 0.05)
            changed["void_gain"] = self.g
        sim.cfg.void_gain = self.g

        Re_meas = (u_rms_post * self.L) / (sim.nu + 1e-12)

        # Return metrics; set "Ma" to post-clamp for compatibility
        m = {
            "u_max_pre": u_max_pre, "u_rms_pre": u_rms_pre, "Ma_pre": Ma_pre,
            "u_max": u_max_post, "u_rms": u_rms_post, "Ma": Ma_post, "Ma_post": Ma_post,
            "Re": Re_meas, "div": div,
            "omega_min": float(getattr(sim, "aggr_omega_min", 0.0)),
            "omega_max": float(getattr(sim, "aggr_omega_max", 0.0)),
            "W_mean": float(getattr(sim, "last_W_mean", 0.0)),
        }
        return changed, m


def compute_streamfunction_poisson(omega, solid=None, iters=400, tol=1e-3):
    """
    Solve ∇²ψ = −ω on a 2D grid with Dirichlet ψ=0 at domain boundaries and at solid cells.
    Uses Jacobi iterations with grid spacing h=1.0.
    """
    import numpy as _np
    om = _np.array(omega, dtype=float)
    ny, nx = om.shape
    om = _np.nan_to_num(om, nan=0.0, posinf=0.0, neginf=0.0)
    psi = _np.zeros_like(om, dtype=float)
    # Fixed cells: all domain boundaries and any solid cells (if provided)
    solid_mask = _np.array(solid, dtype=bool) if solid is not None else _np.zeros_like(om, dtype=bool)
    boundary = _np.zeros_like(om, dtype=bool)
    boundary[0, :] = True; boundary[-1, :] = True; boundary[:, 0] = True; boundary[:, -1] = True
    fixed = solid_mask | boundary

    # Poisson RHS: Laplacian(psi) = rhs = -omega
    rhs = -om
    iters = int(max(1, iters))
    tol = float(tol)

    for _ in range(iters):
        neighbors = (_np.roll(psi, 1, 1) + _np.roll(psi, -1, 1) +
                     _np.roll(psi, 1, 0) + _np.roll(psi, -1, 0))
        # Jacobi update: psi_new = 0.25*(neighbors - rhs)
        psi_new = 0.25 * (neighbors - rhs)
        # Enforce fixed values
        psi_new[fixed] = 0.0

        # Residual r = rhs - Laplacian(psi_new)
        lap_psi = (_np.roll(psi_new, 1, 1) + _np.roll(psi_new, -1, 1) +
                   _np.roll(psi_new, 1, 0) + _np.roll(psi_new, -1, 0) -
                   4.0 * psi_new)
        res = rhs - lap_psi
        if _np.any(~fixed):
            res_norm = float(_np.linalg.norm(res[~fixed]))
            if res_norm <= tol:
                psi = psi_new
                break
        psi = psi_new

    psi[_np.isnan(psi)] = 0.0
    psi[solid_mask] = 0.0
    return psi


def compute_void_walker_metrics(ux, uy, om, solid, walkers=300, ttl=128, eps=0.2, freq=0.0618, seed=0, tracks_out=16):
    """
    Void-walker-inspired traversal that chases the input (top-lid) across the interior using sinusoidal/fractal phase steering.
    - Read-only on fields; no side-effects.
    - Cheap: O(walkers*ttl).
    Returns (metrics_dict, tracks_list)
    metrics_dict: {'coverage': float, 'loop_ratio': float, 'steps_total': int, 'mean_abs_omega': float, ...}
    tracks_list: list of Nx2 arrays for visualization (subset of walkers)
    """
    import numpy as _np
    ny, nx = ux.shape
    rng = _np.random.default_rng(int(seed))
    walkers = int(max(0, walkers))
    ttl = int(max(1, ttl))
    tracks_keep = int(max(0, tracks_out))

    if walkers <= 0:
        return None, None

    # Starting positions along lid (y≈0.5), spread across x (exclude corners)
    xs = _np.linspace(1.0, nx - 2.0, num=walkers, endpoint=True)
    ys = _np.full_like(xs, 0.5)
    phases = rng.uniform(0.0, 2 * _np.pi, size=walkers)

    visited = _np.zeros((ny, nx), dtype=_np.uint8)
    loop_hits = 0
    total_steps = 0
    om_samples = []

    def _bilinear(F, x, y):
        x = float(x); y = float(y)
        i0 = int(_np.clip(_np.floor(x), 0, nx - 2))
        j0 = int(_np.clip(_np.floor(y), 0, ny - 2))
        dx = x - i0; dy = y - j0
        f00 = F[j0, i0]; f10 = F[j0, i0 + 1]; f01 = F[j0 + 1, i0]; f11 = F[j0 + 1, i0 + 1]
        return (f00 * (1 - dx) * (1 - dy) + f10 * dx * (1 - dy) + f01 * (1 - dx) * dy + f11 * dx * dy)

    # Golden-angle for quasi-uniform rotation (radians)
    ga = _np.pi * (3.0 - _np.sqrt(5.0))

    tracks = []
    for wi in range(walkers):
        x = xs[wi]
        y = ys[wi]
        phi0 = phases[wi]
        seen = set()
        trail = []

        for k in range(ttl):
            # local velocity sample (read-only)
            ux_loc = _bilinear(ux, x, y)
            uy_loc = _bilinear(uy, x, y)
            v = _np.array([ux_loc, uy_loc], dtype=float)
            vn = _np.linalg.norm(v) + 1e-12
            vhat = v / vn

            # sinusoidal phase steering (fractal/sinusoidal traversal)
            theta = (2.0 * _np.pi * float(freq) * k) + phi0 + ga * wi
            steer = _np.array([_np.cos(theta), _np.sin(theta)], dtype=float)

            step = vhat + float(eps) * steer
            step /= (1.0 + float(eps))  # bound step length

            x_new = float(_np.clip(x + step[0], 0.0, nx - 1.0))
            y_new = float(_np.clip(y + step[1], 0.0, ny - 1.0))

            ix = int(round(x_new))
            iy = int(round(y_new))
            # avoid solids by staying at prior point if landed in solid
            try:
                if bool(solid[iy, ix]):
                    x_new, y_new = x, y
                    ix = int(round(x_new)); iy = int(round(y_new))
            except Exception:
                pass

            visited[iy, ix] = 1
            # loop detection (cell revisit)
            key = (ix, iy)
            if key in seen:
                loop_hits += 1
            else:
                seen.add(key)

            # vorticity sample along path
            try:
                om_samples.append(abs(float(om[iy, ix])))
            except Exception:
                pass

            total_steps += 1
            x, y = x_new, y_new
            if wi < tracks_keep:
                trail.append((x, y))

        if wi < tracks_keep and trail:
            tracks.append(_np.array(trail, dtype=float))

    interior = (~solid).astype(_np.uint8) if solid is not None else _np.ones_like(visited, dtype=_np.uint8)
    interior_count = int(_np.sum(interior))
    cov = float(_np.sum(visited & (interior > 0))) / float(max(1, interior_count))
    loop_ratio = float(loop_hits) / float(max(1, walkers))
    mean_abs_omega = float(_np.nanmean(_np.asarray(om_samples, dtype=float))) if om_samples else 0.0

    metrics = {
        "walkers": walkers,
        "ttl": ttl,
        "coverage": cov,
        "loop_ratio": loop_ratio,
        "steps_total": int(total_steps),
        "mean_abs_omega": mean_abs_omega,
        "eps": float(eps),
        "freq": float(freq),
        "seed": int(seed),
    }
    return metrics, tracks


def main():
    ap = argparse.ArgumentParser(description="Lid-driven cavity incompressibility (LBM→NS).")
    ap.add_argument("--nx", type=int, default=128)
    ap.add_argument("--ny", type=int, default=128)
    ap.add_argument("--tau", type=float, default=0.7, help="Relaxation time (nu = cs^2*(tau-0.5))")
    ap.add_argument("--U_lid", type=float, default=0.1)
    ap.add_argument("--steps", type=int, default=15000)
    ap.add_argument("--sample_every", type=int, default=200)
    ap.add_argument("--warmup", type=int, default=2000, help="steps to run before sampling (allow flow to settle)")
    ap.add_argument("--progress_every", type=int, default=None, help="print progress every N samples (default: sample_every)")
    ap.add_argument("--outdir", type=str, default=None, help="base output dir; defaults to derivation/code/outputs")
    # Void dynamics exposure
    ap.add_argument("--void_domain", type=str, default="standard_model", help="FUVDM domain modulation preset")
    ap.add_argument("--void_gain", type=float, default=0.5, help="gain for ω_eff = ω0/(1+g|ΔW|)")
    ap.add_argument("--void_enabled", action="store_true", help="enable FUVDM-stabilized collision")
    ap.add_argument("--u_clamp", type=float, default=0.05, help="max |u| clamp (Ma control); set small (e.g., 0.02) to suppress spikes")
    # Adaptive control flags
    ap.add_argument("--auto", action="store_true", help="enable adaptive control")
    ap.add_argument("--Re_target", type=float, default=None, help="target Reynolds number (optional)")
    ap.add_argument("--Ma_max",   type=float, default=0.10, help="Mach cap (max allowable)")
    ap.add_argument("--div_target", type=float, default=1e-6, help="L2 divergence target")
    ap.add_argument("--gate_tail_k", type=int, default=None, help="if set, compute div_max over only the last K samples (steady-state gate)")
    ap.add_argument("--origin", type=str, choices=["lower","upper"], default="upper",
                    help="image origin for plotting; 'upper' shows y=0 at top (lid at top); 'lower' makes y=0 bottom")
    ap.add_argument("--cmap", type=str, default="turbo", help="colormap for |u| panel (e.g., turbo, viridis)")
    # Visualization and solver extras
    ap.add_argument("--stream_density", type=float, default=1.2, help="streamline density for streamplot")
    ap.add_argument("--psi_contours", action="store_true", help="overlay streamfunction ψ contours computed from vorticity (Poisson solve)")
    ap.add_argument("--psi_iters", type=int, default=400, help="max Jacobi iterations for ψ Poisson solve")
    ap.add_argument("--psi_tol", type=float, default=1e-3, help="residual L2 tolerance for ψ Poisson solve")
    # Progress control
    ap.add_argument("--progress_warmup_every", type=int, default=None, help="print warmup progress every N steps (default: progress_every or sample_every)")
    # Void-walker-inspired traversal (read-only; cheap coverage/loop metrics)
    ap.add_argument("--walkers", type=int, default=0, help="number of void-inspired walkers launched from the lid (0=disable)")
    ap.add_argument("--walker_ttl", type=int, default=128, help="steps per walker (TTL)")
    ap.add_argument("--walker_eps", type=float, default=0.2, help="sinusoidal steering amplitude")
    ap.add_argument("--walker_freq", type=float, default=0.0618, help="sinusoidal steering frequency factor")
    ap.add_argument("--walker_seed", type=int, default=0, help="PRNG seed for walkers")
    ap.add_argument("--walker_overlay", action="store_true", help="overlay a subset of walker tracks on the |u| panel")
    ap.add_argument("--walker_tracks", type=int, default=16, help="max tracks to overlay when --walker_overlay is set")
    # Walker announcers (measurement-only) + policy (observe/advise/act)
    ap.add_argument("--walker_announce", action="store_true",
                    help="enable read-only walker announcers (Bus/Reducer); no pathlines")
    ap.add_argument("--announce_max", type=int, default=256,
                    help="max events to report/plot from announcers")
    ap.add_argument("--walker_mode", type=str, choices=["off", "observe", "advise", "act"], default="observe",
                    help="announcer policy mode (observe=metrics only; advise=print suggestions; act=apply bounded nudges)")
    ap.add_argument("--policy_div_target", type=float, default=1e-6,
                    help="target div (e.g., div_p99) used by advisory policy")
    ap.add_argument("--policy_swirl_target", type=float, default=5e-3,
                    help="target swirl (e.g., swirl_p50) used by advisory policy")
    args = ap.parse_args()

    cfg = LBMConfig(
        nx=args.nx, ny=args.ny, tau=args.tau,
        periodic_x=False, periodic_y=False,
        void_enabled=bool(args.void_enabled),
        void_domain=str(args.void_domain),
        void_gain=float(args.void_gain),
        rho_floor=1e-9,
        u_clamp=float(args.u_clamp)
    )
    sim = LBM2D(cfg)
    # Use Zou/He velocity BC at the top (fluid), bounce-back on the other three walls
    sim.set_solid_box(top=False, bottom=True, left=True, right=True)

    # Telemetry: Walker announcers (read-only)
    try:
        from Prometheus_FUVDM.derivation.code.physics.fluid_dynamics.telemetry.walkers import (
            Bus, Reducer, seed_walkers_lid, Walker, Petition, top_events, PolicyBounds, AdvisoryPolicy
        )
    except Exception:
        Bus = Reducer = seed_walkers_lid = Walker = Petition = top_events = PolicyBounds = AdvisoryPolicy = None
    bus = Bus() if 'Bus' in locals() and Bus is not None else None
    reducer = Reducer() if 'Reducer' in locals() and Reducer is not None else None
    walker_list = []
    if int(getattr(args, "walkers", 0)) > 0 and bool(getattr(args, "walker_announce", False)) and (bus is not None) and (reducer is not None) and (seed_walkers_lid is not None):
        try:
            walker_list = seed_walkers_lid(sim.nx, sim.ny, int(args.walkers), kinds=["div", "swirl", "shear"], seed=int(getattr(args, "walker_seed", 0)))
        except Exception:
            walker_list = []
    # Walker-announcer policy mode and state
    wm = str(getattr(args, "walker_mode", "observe"))
    policy = None
    if (wm in ("advise", "act")) and ('AdvisoryPolicy' in locals()) and (AdvisoryPolicy is not None):
        try:
            policy = AdvisoryPolicy(div_target=float(getattr(args, "policy_div_target", 1e-6)),
                                    vort_target=float(getattr(args, "policy_swirl_target", 5e-3)))
        except Exception:
            policy = None
    announce_stats = None
    last_announce_stats = None
    last_announce_counts = None

    # Adaptive controller
    tuner = None
    if args.auto:
        tuner = AutoTuner(args.nx, args.ny, U_init=args.U_lid,
                          tau_init=args.tau, void_gain_init=args.void_gain,
                          Ma_max=args.Ma_max, Re_target=args.Re_target, div_target=args.div_target)

    # Report nondimensional numbers (LBM units)
    L_eff = max(1, int(args.ny) - 1)
    nu = float(lbm_viscosity_from_tau(args.tau))
    Re = float(reynolds_lbm(args.U_lid, L_eff, args.tau))
    Ma = float(mach_lbm(args.U_lid))
    print(f"[bench] L={L_eff}, nu={nu:.6f}, Re={Re:.2f}, Ma={Ma:.4f}")
    if Ma >= 0.1:
        print("[bench][warn] Ma >= 0.1; BGK low-Mach polynomial may be inaccurate/unstable.")

    # Output routing (match RD harness)
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    tstamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures", "fluid_dynamics")
    log_dir = os.path.join(base_outdir, "logs", "fluid_dynamics")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    figure_path = os.path.join(fig_dir, f"{script_name}_{tstamp}.png")
    log_path = os.path.join(log_dir, f"{script_name}_{tstamp}.json")

    # Run simulation loop and record interior divergence after warmup
    t0 = time.time()
    div_hist = []
    for n in range(args.steps + 1):
        # Collide+stream step first, then impose lid velocity on the streamed distributions (Zou/He-style)
        sim.step(1)
        # IMPORTANT: apply lid BC after streaming
        U_apply = tuner.U if (args.auto and (tuner is not None)) else args.U_lid
        sim.set_lid_velocity(float(U_apply))

        # Warmup progress prints (elapsed and ETA to end of warmup)
        if args.warmup and (n < args.warmup):
            warmN = args.progress_warmup_every if getattr(args, "progress_warmup_every", None) is not None else (args.progress_every if args.progress_every is not None else args.sample_every)
            if (n % max(1, int(warmN))) == 0:
                elapsed = time.time() - t0
                ratio = (n / float(max(1, args.warmup)))
                if ratio > 0.0:
                    eta = (elapsed / ratio) * (1.0 - ratio)
                    eta_str = f"{eta:.1f}s"
                else:
                    eta_str = "--"
                print(f"[warmup] n={n}/{args.warmup} ({ratio*100:.1f}%) elapsed={elapsed:.1f}s eta≈{eta_str}", flush=True)

        # Sampling & adaptive control
        if (n >= args.warmup) and ((n - args.warmup) % args.sample_every == 0):
            if args.auto and (tuner is not None):
                changed, m = tuner.step(sim)
                div_hist.append(float(m["div"]))
                if changed:
                    print(f"[auto] n={n} {changed}  |  Ma_post={m['Ma']:.3f} (pre={m.get('Ma_pre', m['Ma']):.3f}) "
                          f"Re≈{m['Re']:.1f} div={m['div']:.2e} "
                          f"ω∈[{m['omega_min']:.3f},{m['omega_max']:.3f}] W̄={m['W_mean']:.3f}")
            else:
                sim.moments()
                d = sim.divergence()
                div_hist.append(d)

            # Walker announcers (read-only): advect, sense, post; reduce to stats
            if 'walker_list' in locals() and walker_list and ('bus' in locals()) and (bus is not None):
                try:
                    sim.moments()
                    for w in walker_list:
                        w.step(sim, dt=1.0)
                        val = w.sense(sim)
                        bus.post(Petition(kind=w.kind, value=float(val), x=float(w.x), y=float(w.y), t=int(n)))
                except Exception:
                    pass
            if 'reducer' in locals() and reducer and ('bus' in locals()) and (bus is not None):
                try:
                    announce_stats = reducer.reduce(bus)
                    if announce_stats:
                        dp90 = float(announce_stats.get('div_p90', 0.0))
                        sp90 = float(announce_stats.get('swirl_p90', 0.0))
                        shp90 = float(announce_stats.get('shear_p90', 0.0))
                        counts_now = getattr(reducer, 'counts', {})
                        print(f"[announce] n={n} counts={counts_now} div_p90={dp90:.2e} swirl_p90={sp90:.2e} shear_p90={shp90:.2e}")
                        last_announce_stats = dict(announce_stats)
                        last_announce_counts = dict(counts_now)
                        # Policy advisory / act (bounded; never injects forces)
                        if (wm in ("advise", "act")) and (policy is not None):
                            _wm_eff = "act" if (wm == "act" and not args.auto) else "advise"
                            if wm == "act" and args.auto:
                                print("[policy] auto=True with walker_mode=act; degrading to advise-only")
                            params = {
                                "tau": float(sim.tau),
                                "U_lid": float(args.U_lid),
                                "u_clamp": float(getattr(sim.cfg, "u_clamp", 0.0)),
                                "void_gain": float(getattr(sim.cfg, "void_gain", 0.0)),
                            }
                            sug = policy.suggest(announce_stats, params)
                            if sug:
                                print(f"[policy] n={n} suggest={sug}")
                                if _wm_eff == "act":
                                    if "tau" in sug:
                                        sim.tau = float(sug["tau"]); sim.omega = 1.0/float(sim.tau)
                                    if "u_clamp" in sug:
                                        sim.cfg.u_clamp = float(sug["u_clamp"])
                                    if "U_lid" in sug:
                                        args.U_lid = float(sug["U_lid"])
                except Exception:
                    announce_stats = None

            # Console progress (prints each sample; set --progress_every to control frequency)
            progN = args.progress_every if args.progress_every is not None else args.sample_every
            if ((n - args.warmup) % max(1, int(progN))) == 0:
                last_div = div_hist[-1] if div_hist else 0.0
                print(f"step={n}, div={last_div:.3e}", flush=True)

    # Compute metrics and routing
    elapsed = time.time() - t0
    div_hist_np = np.asarray(div_hist, dtype=float)
    div_window_max = float(np.max(div_hist_np)) if div_hist_np.size else 0.0
    if getattr(args, "gate_tail_k", None) is not None and div_hist_np.size:
        _k = int(max(1, args.gate_tail_k))
        _tail_arr = div_hist_np[-_k:] if _k < div_hist_np.size else div_hist_np
        div_tail_max = float(np.max(_tail_arr))
        div_max = div_tail_max
    else:
        div_tail_max = None
        div_max = div_window_max

    # Flow gate uses end-of-run speed
    sim.moments()
    _ux = np.nan_to_num(sim.ux, nan=0.0, posinf=0.0, neginf=0.0)
    _uy = np.nan_to_num(sim.uy, nan=0.0, posinf=0.0, neginf=0.0)
    _Vmag = np.hypot(_ux, _uy)
    u_max = float(np.nanmax(_Vmag)) if _Vmag.size else 0.0
    u_mean = float(np.nanmean(_Vmag)) if _Vmag.size else 0.0
    flow_gate = bool(np.isfinite(u_max) and (u_max >= max(1e-9, 0.05*abs(args.U_lid))))
    passed = bool(np.isfinite(div_max) and div_max <= 1e-6 and flow_gate)
    # Final applied lid speed (controller may have adjusted)
    U_final = float(tuner.U) if ('tuner' in locals() and tuner is not None) else float(args.U_lid)

    # Route outputs: failed runs go to .../failed_runs/, passes to base dirs
    out_fig_dir = fig_dir if passed else os.path.join(fig_dir, "failed_runs")
    out_log_dir = log_dir if passed else os.path.join(log_dir, "failed_runs")
    os.makedirs(out_fig_dir, exist_ok=True)
    os.makedirs(out_log_dir, exist_ok=True)
    figure_path = os.path.join(out_fig_dir, f"{script_name}_{tstamp}.png")
    log_path = os.path.join(out_log_dir, f"{script_name}_{tstamp}.json")

    # Refresh macroscopic fields for plotting
    sim.moments()
    ny, nx = sim.ny, sim.nx
    # Coordinates for consistent plotting
    x = np.arange(nx)
    y = np.arange(ny)
    X, Y = np.meshgrid(x, y)

    # Robust arrays
    ux = np.nan_to_num(sim.ux, nan=0.0, posinf=0.0, neginf=0.0)
    uy = np.nan_to_num(sim.uy, nan=0.0, posinf=0.0, neginf=0.0)
    Vmag = np.hypot(ux, uy)

    # Mask walls so they don't pin the colormap
    try:
        Vmask = Vmag.copy()
        Vmask[sim.solid] = np.nan
    except Exception:
        Vmask = Vmag

    # Adaptive color scaling (avoid flat images)
    vmax = np.nanpercentile(Vmask, 99.5)
    if (not np.isfinite(vmax)) or vmax <= 0.0:
        vmax = float(np.nanmax(Vmag)) if np.isfinite(np.nanmax(Vmag)) else 1e-12

    # Plot with chosen origin; use extent so axes match grid indices
    origin = str(getattr(args, "origin", "lower"))
    extent = [0, nx - 1, 0, ny - 1]

    # Build a single dashboard figure: left = |u| + streamlines; right = vorticity
    # Compute vorticity once
    dvdx = 0.5 * (np.roll(uy, -1, axis=1) - np.roll(uy, 1, axis=1))
    dudy = 0.5 * (np.roll(ux, -1, axis=0) - np.roll(ux, 1, axis=0))
    omega = dvdx - dudy
    om = np.nan_to_num(omega, nan=0.0, posinf=0.0, neginf=0.0)
    try:
        om[sim.solid] = np.nan
    except Exception:
        pass

    # Void-walker-inspired coverage + loop metrics (chase the input cheaply)
    vw_metrics, vw_tracks = None, None
    if int(getattr(args, "walkers", 0)) > 0:
        try:
            vw_metrics, vw_tracks = compute_void_walker_metrics(
                ux=ux, uy=uy, om=om, solid=getattr(sim, "solid", None),
                walkers=int(args.walkers),
                ttl=int(getattr(args, "walker_ttl", 128)),
                eps=float(getattr(args, "walker_eps", 0.2)),
                freq=float(getattr(args, "walker_freq", 0.0618)),
                seed=int(getattr(args, "walker_seed", 0)),
                tracks_out=int(getattr(args, "walker_tracks", 16)),
            )
            if vw_metrics:
                print(f"[void-walkers] N={vw_metrics['walkers']} ttl={vw_metrics['ttl']} "
                      f"coverage={vw_metrics['coverage']:.2%} loops={vw_metrics['loop_ratio']:.2%} "
                      f"mean|ω|={vw_metrics['mean_abs_omega']:.3e}")
        except Exception:
            vw_metrics, vw_tracks = None, None

    # ψ contours overlay moved below after axes creation
    wlim = np.nanpercentile(np.abs(om), 99.0)
    if (not np.isfinite(wlim)) or wlim <= 0.0:
        wlim = float(np.nanmax(np.abs(om))) if np.isfinite(np.nanmax(np.abs(om))) else 1e-12

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)
    ax0, ax1 = axes[0], axes[1]

    # Left panel: |u| with requested colormap and streamlines
    im0 = ax0.imshow(Vmag, origin=origin, extent=extent, cmap=str(getattr(args, "cmap", "turbo")),
                     vmin=0.0, vmax=vmax, interpolation="nearest")
    c0 = fig.colorbar(im0, ax=ax0, fraction=0.046, pad=0.04)
    c0.set_label("|u|")

    # Streamlines: for origin='lower' (y upward), flip vertical velocity sign to convert
    # array-down (+y) into plot-up (+y) direction; for origin='upper', keep raw sign.
    uy_plot = -uy if origin == "lower" else uy
    try:
        ax0.streamplot(x, y, ux, uy_plot, density=float(getattr(args, "stream_density", 1.2)), color="w", linewidth=0.6)
    except Exception:
        pass

    # Optional walker tracks overlay (void-walker inspired paths)
    if getattr(args, "walker_overlay", False) and ('vw_tracks' in locals()) and (vw_tracks is not None):
        try:
            for tr in vw_tracks:
                if tr is None or len(tr) == 0:
                    continue
                xs_tr = tr[:, 0]
                ys_tr = tr[:, 1]
                ys_plot = ys_tr if origin == "lower" else (ny - 1 - ys_tr)
                ax0.plot(xs_tr, ys_plot, color="k", alpha=0.25, linewidth=0.5)
        except Exception:
            pass
    # Optional announcer event markers (read-only petitions; not pathlines)
    if getattr(args, "walker_overlay", False) and bool(getattr(args, "walker_announce", False)) and ('bus' in locals()) and (bus is not None) and ('top_events' in locals()) and (top_events is not None):
        try:
            top_ev = top_events(bus, int(getattr(args, "announce_max", 256)))
            es = top_ev.get("events", []) if top_ev else []
            if es:
                xs = np.array([e["x"] for e in es], dtype=float)
                ys = np.array([e["y"] for e in es], dtype=float)
                vs = np.array([e["value"] for e in es], dtype=float)
                kinds = [str(e["kind"]) for e in es]
                ys_plot = ys if origin == "lower" else (ny - 1 - ys)
                color_map = {"div": "yellow", "swirl": "cyan", "shear": "magenta"}
                colors = [color_map.get(k, "white") for k in kinds]
                vmax_ev = float(np.nanmax(vs)) if vs.size else 1.0
                size = 10.0 + 30.0*np.sqrt(np.clip(vs, 0.0, vmax_ev)/(vmax_ev + 1e-12))
                ax0.scatter(xs, ys_plot, s=size, c=colors, alpha=0.7, edgecolors="none")
        except Exception:
            pass

    # Optional streamfunction contours overlay (solve ∇²ψ = −ω)
    if getattr(args, "psi_contours", False):
        try:
            psi = compute_streamfunction_poisson(omega=om,
                                                 solid=getattr(sim, "solid", None),
                                                 iters=int(getattr(args, "psi_iters", 400)),
                                                 tol=float(getattr(args, "psi_tol", 1e-3)))
            # Align Y to imshow's origin handling
            Yc = Y if origin == "lower" else (ny - 1 - Y)
            ax0.contour(X, Yc, psi, levels=20, colors="k", linewidths=0.5, alpha=0.6)
        except Exception:
            pass

    # Lid indicator (arrow) at visual top edge
    lid_y = 0.5 if origin == "upper" else ny - 1 - 0.5
    try:
        ax0.annotate("", xy=(nx*0.8, lid_y), xytext=(nx*0.2, lid_y),
                     arrowprops=dict(arrowstyle="->", color="red", lw=1.5))
        ax0.text(nx*0.82, lid_y + (0.02*ny if origin=="lower" else -0.02*ny),
                 "LID →", color="red", fontsize=9, va="bottom" if origin=="lower" else "top")
    except Exception:
        pass

    ax0.set_title(f"|u| + streamlines (U_lid={U_final}, τ={sim.tau:.4f}, div_max={div_max:.2e})")
    ax0.set_xlim(0, nx - 1)
    ax0.set_ylim(0, ny - 1)

    # Right panel: vorticity
    im1 = ax1.imshow(om, origin=origin, extent=extent, cmap="RdBu_r",
                     vmin=-wlim, vmax=wlim, interpolation="nearest")
    c1 = fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    c1.set_label("vorticity")
    ax1.set_title("Vorticity")
    ax1.set_xlim(0, nx - 1)
    ax1.set_ylim(0, ny - 1)

    fig.suptitle(f"Lid-driven cavity (origin={origin})", fontsize=12)
    fig.savefig(figure_path, dpi=180)
    plt.close('all')

    # Measured (end-of-run) dimensionless numbers based on fields
    u_rms = float(np.sqrt(np.nanmean(_Vmag**2))) if _Vmag.size else 0.0
    Re_meas = float((u_rms * L_eff) / (sim.nu + 1e-12))
    Ma_meas = float(u_max / math.sqrt(CS2))
    nu_final = float(sim.nu)
    # Final announcer stats snapshot (reduce once more at end)
    announce_stats_final = None
    announce_counts_final = None
    if bool(getattr(args, "walker_announce", False)) and ('reducer' in locals()) and reducer and ('bus' in locals()) and (bus is not None):
        try:
            announce_stats_final = reducer.reduce(bus)
            announce_counts_final = dict(getattr(reducer, "counts", {}))
        except Exception:
            announce_stats_final = None
            announce_counts_final = None

    payload = {
        "theory": "LBM→NS; incompressible cavity with no-slip walls (bounce-back) + FUVDM ω_eff (optional)",
        "params": {
            "nx": int(args.nx), "ny": int(args.ny), "tau": float(args.tau), "U_lid": float(args.U_lid),
            "steps": int(args.steps), "sample_every": int(args.sample_every),
            "void_enabled": bool(args.void_enabled), "void_domain": str(args.void_domain), "void_gain": float(args.void_gain),
            "auto": bool(getattr(args, "auto", False))
        },
        "metrics": {
            "div_max": float(div_max),
            "div_window_max": float(div_window_max),
            "div_tail_max": float(div_tail_max) if div_tail_max is not None else None,
            "gate_tail_k": int(args.gate_tail_k) if args.gate_tail_k is not None else None,
            "elapsed_sec": float(elapsed),
            "u_max": float(u_max),
            "u_mean": float(u_mean),
            "flow_gate": bool(flow_gate),
            "psi_contours": bool(getattr(args, "psi_contours", False)),
            "void_walkers": vw_metrics if 'vw_metrics' in locals() and vw_metrics is not None else None,
            "void_announcers": {
              "announce_counts": announce_counts_final if 'announce_counts_final' in locals() and (announce_counts_final is not None) else (last_announce_counts if 'last_announce_counts' in locals() else None),
              "announce_stats": announce_stats_final if 'announce_stats_final' in locals() and (announce_stats_final is not None) else (last_announce_stats if 'last_announce_stats' in locals() else None)
            },
            # original dimensionless numbers from arguments (for compatibility)
            "Re": float(Re),
            "Ma": float(Ma),
            "nu": float(nu),
            # measured (end-of-run) dimensionless numbers
            "Re_meas": float(Re_meas),
            "Ma_meas": float(Ma_meas),
            "nu_final": float(nu_final),
            "passed": passed,
            # Controller summary (final applied values)
            "controller": {
                "auto": bool(getattr(args, "auto", False)),
                "U_lid_final": float(U_final),
                "tau_final": float(sim.tau),
                "void_gain_final": float(getattr(sim.cfg, "void_gain", 0.0)),
                "u_clamp_final": float(getattr(sim.cfg, "u_clamp", 0.0))
            },
            # Void diagnostics (present even if disabled; fallback values reasonable)
            "void": {
                "dW_max": float(getattr(sim, "aggr_dW_max", 0.0)),
                "omega_min": float(getattr(sim, "aggr_omega_min", 0.0)),
                "omega_max": float(getattr(sim, "aggr_omega_max", 0.0)),
                "W_mean_last": float(getattr(sim, "last_W_mean", 0.0))
            }
        },
        "outputs": {"figure": figure_path},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload["metrics"], indent=2))


if __name__ == "__main__":
    main()