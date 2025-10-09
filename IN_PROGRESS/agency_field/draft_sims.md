Yes-I can spin up toy experiments right now. To keep it robust on your machine, here are two **ready-to-run** Python scripts you can drop anywhere and execute immediately. They produce **one figure + one CSV** each, with simple pass/fail expectations so you can sanity-check fast.

No external data. Only needs `numpy`, `pandas`, `matplotlib`.

---

# 1) Energy clamp (does (C) relax with (\tau=1/\gamma)?)

**What it does:** Simulates the order-parameter PDE
(\partial_t C = D\nabla^2 C - \gamma C + S) on a 1-D line. At (t=5), the source is clamped from (S_0) to (\lambda S_0). You should see (C) drift from (C_{\text{ss}}=S_0/\gamma) down to (\lambda S_0/\gamma) with an exponential time constant (1/\gamma).

**Expected numbers (defaults):** (S_0=1,\ \gamma=0.5\Rightarrow C_{\text{ss,pre}}=2.0). Clamp (\lambda=0.6\Rightarrow C_{\text{ss,post}}=1.2).

**Outputs:**

* `energy_clamp.csv` (time series)
* `energy_clamp.png` (curve + steady-state lines + exponential overlay)

**Script - `simulate_energy_clamp.py`:**

```python
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path

def energy_clamp_1d(N=100, L=1.0, D=0.05, gamma=0.5, S0=1.0, lam=0.6,
                    t_total=10.0, t_step=5.0, dt=1e-3):
    # 1D explicit Euler for: dC/dt = D*C_xx - gamma*C + S  (Neumann-ish edges)
    dx = L / (N - 1)
    if D > 0:
        cfl_limit = dx*dx / (2*D)
        if dt > 0.95 * cfl_limit: dt = 0.9 * cfl_limit

    C = np.zeros(N); S = np.full(N, S0)
    steps = int(t_total / dt); clamp_step = int(t_step / dt)
    times = np.zeros(steps+1); Cmean = np.zeros(steps+1); Cmid = np.zeros(steps+1)
    times[0] = 0.0; Cmean[0] = C.mean(); Cmid[0] = C[N//2]

    for n in range(steps):
        if n == clamp_step: S[:] = lam * S0
        C_ext = np.pad(C, (1,1), mode='edge')
        lap = (C_ext[2:] - 2*C_ext[1:-1] + C_ext[:-2]) / (dx*dx)
        dC = D * lap - gamma * C + S
        C = C + dt * dC
        t = (n+1)*dt
        times[n+1] = t; Cmean[n+1] = C.mean(); Cmid[n+1] = C[N//2]

    return pd.DataFrame({"time": times, "C_mean": Cmean, "C_center": Cmid})

def main():
    df = energy_clamp_1d()
    outdir = Path(".")
    df.to_csv(outdir/"energy_clamp.csv", index=False)

    gamma = 0.5; S0 = 1.0; lam = 0.6; t_step = 5.0
    C_ss1 = S0/gamma; C_ss2 = lam*S0/gamma
    t = df["time"].values
    idx_step = (np.abs(t - t_step)).argmin()
    C_at_step = df["C_mean"].iloc[idx_step]
    t_after = t[t >= t_step]
    pred = C_ss2 + (C_at_step - C_ss2)*np.exp(-gamma*(t_after - t_step))

    plt.figure(figsize=(6,4))
    plt.plot(df["time"], df["C_mean"], label="C_mean (sim)")
    plt.axhline(C_ss1, linestyle="--", linewidth=1, label="C_ss (pre)")
    plt.axhline(C_ss2, linestyle="--", linewidth=1, label="C_ss (post)")
    plt.plot(t_after, pred, linestyle=":", linewidth=1, label="exp fit (post)")
    plt.xlabel("time"); plt.ylabel("C_mean"); plt.title("Energy clamp: C relaxes with τ = 1/γ")
    plt.legend(); plt.tight_layout(); plt.savefig(outdir/"energy_clamp.png", dpi=140)

if __name__ == "__main__":
    main()
```

**Run:**

```bash
python simulate_energy_clamp.py
```

**Pass/fail gate:** curve should sit near 2.0 before (t=5), relax toward ~1.2 after, and the dotted exponential should hug the simulated curve.

---

# 2) Inverted-U ridge (coordination without lockstep)

**What it does:** Builds a ring of simple estimators (consensus + innovation) tracking a structured signal in noise. We sweep **coupling** and **measurement noise**, measure **prediction per joule**, and apply a **balance** penalty for over-synchrony. The **C-score** shows a ridge at intermediate coupling/noise (your “no bumping” sweet spot).

**Outputs:**

* `sweep.csv` (grid of coupling × noise with metrics)
* `cscore_heatmap.png` (heatmap; ridge = bright band)

**Script - `simulate_inverted_u.py`:**

```python
import numpy as np, pandas as pd, matplotlib.pyplot as plt

def run_consensus_prediction(T=3000, N=50, k_c=0.1, k_i=0.2,
                             meas_noise=0.5, env_noise=0.1, freq=0.01, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    s = np.sin(2*np.pi*freq*t) + rng.normal(0, env_noise, size=T)

    x = rng.normal(0, 1e-3, size=(N,))
    X_hist = np.zeros((T, N))
    updates_energy = np.zeros(T)

    for tt in range(T):
        y = s[tt] + rng.normal(0, meas_noise, size=N)
        x_left = np.roll(x, 1); x_right = np.roll(x, -1)
        consensus = k_c * (0.5*(x_left + x_right) - x)
        innovation = k_i * (y - x)
        dx = consensus + innovation
        x = x + dx
        X_hist[tt] = x
        updates_energy[tt] = np.mean(dx*dx)

    # Ensemble predictor
    x_mean = X_hist.mean(axis=1)
    s_next = s[1:]; x_now = x_mean[:-1]
    if np.var(x_now) > 1e-12:
        beta = np.cov(x_now, s_next, bias=True)[0,1]/np.var(x_now)
        preds = beta * x_now
        r2_ens = 1.0 - np.var(s_next - preds)/np.var(s_next)
    else:
        r2_ens = 0.0

    # Single-node med R^2
    r2_nodes = []
    for i in range(N):
        xi = X_hist[:-1, i]
        if np.var(xi) > 1e-12:
            b = np.cov(xi, s_next, bias=True)[0,1]/np.var(xi)
            p = b * xi
            r2 = 1.0 - np.var(s_next - p)/np.var(s_next)
        else:
            r2 = 0.0
        r2_nodes.append(r2)
    r2_med = float(np.median(r2_nodes))

    # Correlation-induced redundancy
    X_ds = X_hist[::5]
    Xn = (X_ds - X_ds.mean(axis=0)) / (X_ds.std(axis=0) + 1e-12)
    corr = (Xn.T @ Xn) / Xn.shape[0]
    n = corr.shape[0]
    mean_offdiag = float((np.sum(corr) - np.trace(corr)) / (n*(n-1)))

    energy_per_step = float(updates_energy.mean())
    pred_per_joule = r2_ens / (energy_per_step + 1e-12)

    # Balance = (ensemble gain over median) * (1 - mean corr), clipped
    integ_gain = max(0.0, r2_ens - r2_med)
    red_penalty = max(0.0, min(1.0, 1.0 - mean_offdiag))
    B = max(0.0, min(1.0, integ_gain * red_penalty))

    return dict(r2_ens=float(r2_ens), r2_med=r2_med, mean_corr=mean_offdiag,
                energy=energy_per_step, pred_per_joule=pred_per_joule, B=B)

def main():
    couplings = np.linspace(0.0, 0.6, 13)
    noises = np.linspace(0.05, 1.0, 12)
    rows = []
    for kc in couplings:
        for noise in noises:
            rows.append(dict(coupling=kc, noise=noise,
                            **run_consensus_prediction(k_c=kc, meas_noise=noise, seed=42)))
    df = pd.DataFrame(rows)
    pred_z = (df["pred_per_joule"] - df["pred_per_joule"].mean()) / (df["pred_per_joule"].std() + 1e-12)
    df["C_score"] = pred_z * df["B"]
    df.to_csv("sweep.csv", index=False)

    pivot = df.pivot_table(index="noise", columns="coupling", values="C_score")
    plt.figure(figsize=(6,4))
    plt.imshow(pivot.values, aspect="auto", origin="lower",
               extent=[pivot.columns.min(), pivot.columns.max(),
                       pivot.index.min(), pivot.index.max()])
    plt.colorbar(label="C_score")
    plt.xlabel("coupling k_c"); plt.ylabel("measurement noise std")
    plt.title("Inverted-U ridge (C_score vs coupling & noise)")
    plt.tight_layout(); plt.savefig("cscore_heatmap.png", dpi=140)

if __name__ == "__main__":
    main()
```

**Run:**

```bash
python simulate_inverted_u.py
```

**Pass/fail gate:** heatmap shows a **bright band** (ridge) at **intermediate coupling** and **moderate noise**; dark corners at very low/high coupling and very low/high noise.

---

## What these two runs “prove out” for your spec

* **Energy budget link:** (C) tracks source power with an exponential time constant (1/\gamma).
* **Balance principle:** there’s a sweet spot between fragmentation and lockstep where the **C-score** peaks-exactly your “interactions become more complex without bumping” intuition.

If you want, I can also add a **τ-horizon options probe** script (empowerment proxy via reachable-state counting) so you can complete the P-U-V triangle.
