from __future__ import annotations

import math
import random
import subprocess
import time
from collections import deque
from pathlib import Path

import numpy as np

from vdm_rt.core.sparse_connectome import Connectome
from vdm_rt.core.void_dynamics_adapter import TAU, GAMMA, KT_EFF, EPS_TOPO, ETA_BOND_FLOOR, klein_gordon_rhs


def bfs_dist(adj: list[np.ndarray], src: int, max_depth: int = 10) -> dict[int, int]:
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        du = dist[u]
        if du >= max_depth:
            continue
        for v in adj[u]:
            vv = int(v)
            if vv not in dist:
                dist[vv] = du + 1
                q.append(vv)
    return dist


def gini(vals: np.ndarray) -> float:
    x = np.asarray(vals, dtype=np.float64)
    if x.size == 0:
        return 0.0
    if np.min(x) < 0:
        x = x - np.min(x)
    x = np.sort(x + 1e-12)
    n = x.size
    idx = np.arange(1, n + 1, dtype=np.float64)
    return float((2.0 * np.sum(idx * x) / (n * np.sum(x))) - ((n + 1) / n))


def compute_H(connectome: Connectome) -> float:
    phi = connectome.phi_curr
    lap = 0.0
    for i in range(connectome.N):
        nbrs = connectome.adj[i]
        if nbrs.size:
            lap += float(np.sum((phi[nbrs] - phi[i]) ** 2))
    pot = float(np.sum(connectome.lam * (phi * phi) * ((1.0 - phi) ** 2)))
    return 0.5 * float(connectome.D) * lap + pot


def main() -> int:
    out_path = Path("artifacts/migration_v7/validation_report.txt")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    f = out_path.open("w", encoding="utf-8")

    def log(line: str):
        print(line, flush=True)
        f.write(line + "\n")
        f.flush()

    random.seed(0)
    np.random.seed(0)

    connectome = Connectome(N=216, k=6, seed=0)
    connectome.enable_validation_events(True)
    N = connectome.N

    c = math.sqrt(GAMMA / TAU)
    activation_threshold = 5.0 * math.sqrt(2.0 * GAMMA * KT_EFF)

    gate_ok = {i: True for i in range(1, 13)}
    gate_msg: dict[int, str] = {}

    step_times: list[float] = []
    H_samples: list[tuple[int, float]] = []

    inject_tick = 1000
    pairs: list[tuple[int, int, int]] = []
    pair_activated: dict[tuple[int, int], int] = {}

    death_threshold = float(2.0 * EPS_TOPO * KT_EFF)
    life_start: dict[tuple[int, int], int] = {}
    lifetimes: list[int] = []

    for tick in range(1, 50001):
        if tick == inject_tick:
            nodes = list(range(connectome.N))
            random.shuffle(nodes)
            selected: list[tuple[int, int, int]] = []
            for src in nodes:
                dmap = bfs_dist(connectome.adj, src, 10)
                cands = [(j, d) for j, d in dmap.items() if 3 <= d <= 10 and j != src]
                random.shuffle(cands)
                if cands:
                    j, d = cands[0]
                    selected.append((src, j, d))
                if len(selected) >= 10:
                    break
            pairs = selected[:10]
            for s, _, _ in pairs:
                connectome.stimulate_indices([s], amp=1.0)

        t0 = time.perf_counter()
        connectome.step(tick=tick)
        step_times.append(time.perf_counter() - t0)

        phi = connectome.phi_curr

        if gate_ok[1] and bool(np.any(np.isnan(phi))):
            gate_ok[1] = False
            gate_msg[1] = f"NaN at tick={tick}"

        if gate_ok[2]:
            mn = float(np.min(phi))
            mx = float(np.max(phi))
            if mn < 0.0 or mx > 1.0:
                gate_ok[2] = False
                gate_msg[2] = f"bounds violation tick={tick} min={mn:.6f} max={mx:.6f}"

        if gate_ok[12] and bool(np.any(np.isinf(connectome.debt))):
            gate_ok[12] = False
            gate_msg[12] = f"inf debt at tick={tick}"

        # Process event streams incrementally (no full edge scans)
        while connectome._v_psi_up:
            a, b, t_up = connectome._v_psi_up.pop(0)
            life_start[(a, b)] = int(t_up)

        while connectome._v_psi_down:
            a, b, t_dn = connectome._v_psi_down.pop(0)
            key = (a, b)
            if key in life_start:
                lifetimes.append(int(t_dn) - life_start.pop(key))

        while connectome._v_edge_deaths:
            a, b, t_dead = connectome._v_edge_deaths.pop(0)
            key = (a, b)
            if key in life_start:
                lifetimes.append(int(t_dead) - life_start.pop(key))

        # Gate 8 locality from birth events only
        if gate_ok[8]:
            while connectome._v_edge_births:
                a, b, dist2, ra, rb, t_birth = connectome._v_edge_births.pop(0)
                if not (dist2 <= ra * ra and dist2 <= rb * rb):
                    gate_ok[8] = False
                    gate_msg[8] = (
                        f"birth edge=({a},{b}) tick={t_birth} dist2={dist2:.6f} "
                        f"ra={ra:.6f} rb={rb:.6f}"
                    )
                    break

        if pairs and tick >= inject_tick:
            phi_dot = np.abs(connectome.phi_curr - connectome.phi_prev)
            for s, t, d in pairs:
                k = (s, t)
                if k not in pair_activated and float(phi_dot[t]) > activation_threshold:
                    pair_activated[k] = tick

        if tick % 100 == 0:
            H = float(getattr(connectome, "_reward_H", compute_H(connectome)))
            H_samples.append((tick, H))

        if tick % 100 == 0:
            log(f"progress tick={tick}")

    # Gate 3
    count_low = int(np.sum(connectome.phi_curr < 0.2))
    count_high = int(np.sum(connectome.phi_curr > 0.8))
    gate_ok[3] = (count_low > 0.2 * N) and (count_high > 0.2 * N)
    gate_msg[3] = f"count_low={count_low}, count_high={count_high}, N={N}"

    # Gate 4
    g4 = len(pairs) >= 10
    pair_lines = [f"pairs={len(pairs)} c={c:.6f} thresh={activation_threshold:.6f}"]
    for s, t, d in pairs:
        k = (s, t)
        if k not in pair_activated:
            g4 = False
            pair_lines.append(f"({s}->{t}, d={d}) no_activation")
            continue
        delay = pair_activated[k] - inject_tick
        need = d / c
        if delay < need:
            g4 = False
        pair_lines.append(f"({s}->{t}, d={d}) delay={delay} required>={need:.6f}")
    gate_ok[4] = g4
    gate_msg[4] = " | ".join(pair_lines)

    # Gate 5
    g5 = True
    worst = 0.0
    for i in range(0, len(H_samples) - 9):
        win = H_samples[i : i + 10]
        h0 = win[0][1]
        hmax = max(h for _, h in win)
        ratio = hmax / (h0 + 1e-12)
        worst = max(worst, ratio)
        if hmax > 1.05 * h0:
            g5 = False
    gate_ok[5] = g5
    gate_msg[5] = f"worst_ratio={worst:.6f}"

    # Gate 6
    g = gini(connectome.phi_curr)
    gate_ok[6] = g >= 0.45
    gate_msg[6] = f"gini={g:.6f}"

    # Gate 7
    if lifetimes:
        mlt = float(np.mean(lifetimes))
        gate_ok[7] = mlt > 500.0
        gate_msg[7] = f"samples={len(lifetimes)} mean_lifetime={mlt:.6f} death_threshold={death_threshold:.8f}"
    else:
        gate_ok[7] = False
        gate_msg[7] = f"samples=0 death_threshold={death_threshold:.8f}"

    gate_msg.setdefault(8, "all edge births satisfied locality")

    # Gate 9
    grep_checks = [
        (r"F_REF", ["vdm_rt"]),
        (r"PHASE_SENS", ["vdm_rt"]),
        (r"ALPHA\s*=\s*0\.25", ["vdm_rt"]),
        (r"sin\(2 \* np\.pi \* f_ref", ["vdm_rt"]),
        (r"domain_modulation", ["vdm_rt"]),
        (r"get_domain_modulation", ["vdm_rt"]),
        (r"Void_Debt_Modulation", ["vdm_rt"]),
        (r"use_time_dynamics", ["vdm_rt"]),
        (r"time.time_ns\(\)", ["vdm_rt/core", "vdm_rt/io/uted"]),
        (r"np.random.uniform\(-0.02, 0.02", ["vdm_rt"]),
        (r"alpha \* W \* \(1 - W\)|alpha \* W \* \(1.0 - W\)", ["vdm_rt"]),
        (r"-beta \* W", ["vdm_rt"]),
        (r"def delta_re_vgsp", ["vdm_rt"]),
        (r"def delta_gdsp", ["vdm_rt"]),
        (r"def universal_void_dynamics", ["vdm_rt"]),
        (r"neigh_sets: List\[Set\[int\]\] = \[set\(\) for _ in range\(N\)\]", ["vdm_rt"]),
        (r"self._build_alias", ["vdm_rt"]),
        (r"TOPO_PERIOD", ["vdm_rt"]),
        (r"TOPO_THRESHOLD", ["vdm_rt"]),
        (r"TOPO_PATIENCE", ["vdm_rt"]),
        (r"R_NUCLEATION", ["vdm_rt"]),
        (r"tau_e", ["vdm_rt"]),
        (r"DEBT_MAX|debt_max", ["vdm_rt"]),
        (r"dt_physics_us", ["vdm_rt"]),
        (r"PSI_DEATH", ["vdm_rt"]),
        (r"PSI_SEED", ["vdm_rt"]),
        (r"def _maybe_update_topology", ["vdm_rt"]),
        (r"def _compute_eligibility", ["vdm_rt"]),
        (r"eligibility", ["vdm_rt"]),
        (r"last_activation_tick", ["vdm_rt"]),
    ]
    grep_hits = 0
    g9 = True
    for patt, targets in grep_checks:
        cmd = ["grep", "-RIn", "-E", "--", patt] + targets
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = res.stdout.strip()
        if out:
            g9 = False
            grep_hits += len(out.splitlines())
    gate_ok[9] = g9
    gate_msg[9] = f"grep_hits={grep_hits}"

    # Gate 10: one final pass over edges only at end
    psi_vals = []
    for i in range(connectome.N):
        nbrs = connectome.adj[i]
        psi = connectome.psi_curr[i]
        for idx in range(nbrs.size):
            j = int(nbrs[idx])
            if j > i:
                psi_vals.append(float(psi[idx]))
    if psi_vals:
        arr = np.asarray(psi_vals, dtype=np.float64)
        n = arr.size
        hi = int(np.sum(arr > 0.5))
        low = int(np.sum(arr < 0.1))
        frac_hi = hi / n
        gate_ok[10] = (frac_hi > 0.50) and (low > 0)
        gate_msg[10] = f"edges={n} hi_count={hi} frac_hi={frac_hi:.6f} low_count={low}"
    else:
        gate_ok[10] = False
        gate_msg[10] = "edges=0"

    # Gate 11
    mean_step = float(np.mean(step_times))
    reps = 200
    t0 = time.perf_counter()
    for _ in range(reps):
        _ = klein_gordon_rhs(connectome.phi_curr, connectome.adj, connectome.psi_curr)
    mean_rhs = (time.perf_counter() - t0) / reps
    ratio = mean_step / (mean_rhs + 1e-12)
    gate_ok[11] = mean_step <= 3.0 * mean_rhs
    gate_msg[11] = f"mean_step={mean_step:.8f}s mean_rhs={mean_rhs:.8f}s ratio={ratio:.6f}"

    # Gate 12 final
    max_debt = float(np.max(connectome.debt))
    if max_debt >= 500.0:
        gate_ok[12] = False
    gate_msg[12] = f"max_debt={max_debt:.6f}"

    gate_msg.setdefault(1, "no NaN observed")
    gate_msg.setdefault(2, f"phi_in_bounds min={float(np.min(connectome.phi_curr)):.6f} max={float(np.max(connectome.phi_curr)):.6f}")

    for gidx in range(1, 13):
        log(f"Gate {gidx}: {'PASS' if gate_ok[gidx] else 'FAIL'} | {gate_msg[gidx]}")

    overall = all(gate_ok.values())
    log(f"OVERALL: {'PASS' if overall else 'FAIL'}")
    f.close()
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
