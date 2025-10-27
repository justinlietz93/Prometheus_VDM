"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt

def make_grid(n=21, obstacle_density=0.15, seed=0):
    rng = np.random.default_rng(seed)
    grid = np.zeros((n,n), dtype=np.int8)
    mask = rng.random((n,n)) < obstacle_density
    grid[mask] = 1
    c = n//2
    grid[c, c] = 0
    goal = np.zeros_like(grid, dtype=np.int8)
    goal[n-5:n-1, n-5:n-1] = 1
    grid[n-5:n-1, n-5:n-1] = 0
    return grid, goal

def moves_for_actuators(kind="4"):
    if kind == "2": return [(-1,0),(1,0)]
    if kind == "4": return [(-1,0),(1,0),(0,-1),(0,1)]
    if kind == "8": return [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    raise ValueError("kind must be '2','4','8'")

def neighbors(pos, moves, n, grid):
    r,c = pos
    for dr,dc in moves:
        rr,cc = r+dr, c+dc
        if 0 <= rr < n and 0 <= cc < n and grid[rr,cc]==0:
            yield (rr,cc)

def reachable_states(grid, start, moves, steps):
    n = grid.shape[0]
    reached = set([start])
    frontier = set([start])
    for _ in range(steps):
        newf = set()
        for s in frontier:
            for nb in neighbors(s, moves, n, grid):
                newf.add(nb)
        frontier = newf - reached
        if not frontier: break
        reached |= frontier
    return reached

def useful_fraction(grid, goal, reached, slip=0.0):
    goal_cells = np.argwhere(goal==1)
    if goal_cells.size == 0: return 0.0
    def manhattan(p,q): return abs(p[0]-q[0]) + abs(p[1]-q[1])
    ds = []
    for (r,c) in reached:
        d = int(np.min([manhattan((r,c),(gr,gc)) for (gr,gc) in goal_cells]))
        ds.append(d)
    ds = np.array(ds, dtype=float)
    probs = (1.0 - slip)**ds
    return float(np.clip(probs.mean(), 0.0, 1.0))

def run_options_probe(n=21, obstacle_density=0.15, budgets=(2,4,6,8,10),
                      slips=(0.0,0.1,0.2,0.3), actuator_kinds=("2","4","8"), seed=0):
    grid, goal = make_grid(n=n, obstacle_density=obstacle_density, seed=seed)
    start = (n//2, n//2)
    rows = []
    for kind in actuator_kinds:
        moves = moves_for_actuators(kind)
        for E in budgets:
            reached = reachable_states(grid, start, moves, steps=E)
            R = len(reached); V_bits = np.log2(max(R,1))
            for slip in slips:
                useful_frac = useful_fraction(grid, goal, reached, slip=slip)
                useful_count = int(np.round(useful_frac * R))
                V_use_bits = np.log2(max(useful_count,1))
                rows.append(dict(actuators=kind, budget=E, slip=slip,
                                 grid_n=n, obstacles=obstacle_density,
                                 reachable=R, useful=useful_count,
                                 V_bits=V_bits, V_useful_bits=V_use_bits))
    return pd.DataFrame(rows)

def main():
    df = run_options_probe()
    df.to_csv("options.csv", index=False)
    df4 = df[df["actuators"]=="4"].copy()
    pv = df4.pivot_table(index="slip", columns="budget", values="V_useful_bits")
    plt.figure(figsize=(6,4))
    plt.imshow(pv.values, aspect="auto", origin="lower",
               extent=[pv.columns.min(), pv.columns.max(), pv.index.min(), pv.index.max()])
    plt.colorbar(label="V_useful_bits")
    plt.xlabel("energy budget (steps)"); plt.ylabel("slip probability")
    plt.title("Options probe (4 actuators): useful reachable entropy")
    plt.tight_layout(); plt.savefig("options_heatmap.png", dpi=140)

if __name__ == "__main__":
    main()
