Here’s a simple, high‑signal recipe to make your echo results instantly readable without walls of text: show the **final state image** and, right beneath it, a **per‑pixel |q − q₀| difference map** with one shared colorbar. Annotate each frame with energy tags so people can compare at a glance.

---

# Minimal, repeatable visualization pattern for echoes

**What it shows (at a glance):**

* Top: final state (q(x,y,t_{\mathrm{echo}})) (either baseline or assisted).
* Bottom: per‑pixel absolute error (|q-q_0|) vs the ground‑truth or rewind target (q_0).
* One consistent colormap & scale across experiments.
* In‑frame labels: `E_baseline` vs `E_assisted` in the top‑right corner of the top image.

**Why it works:**

* Humans instantly spot structure in the **difference map** (where improvement happens).
* The **colorbar** quantifies that improvement without hunting for numbers.
* Consistent **colormaps** and **ranges** prevent “chart‑junk” comparisons.

---

## File/figure spec (drop‑in)

* **Inputs:**
  `q0.npy`, `q_final_baseline.npy`, `q_final_assisted.npy`  (float32/64 arrays, shape H×W or H×W×C)
  Optional masks: `domain_mask.npy` (bool) for irregular domains.

* **Plotting defaults:**

  * Colormap: `viridis` (keep it the same for all runs).
  * Intensity range: fix per campaign (e.g., `vmin=global_min`, `vmax=global_max`).
  * Difference map range: fix once (e.g., `dmax = 99th percentile of |q−q0|` over your whole suite).
  * Resolution: 180–300 DPI; figure size 6″×7.5″ (journal‑friendly).
  * Titles: top-left small caps `BASELINE` / `ASSISTED`.
  * Corner tag: `E=…` (mean |q−q0| or energy you prefer), same font, same location.

* **Metrics to print in caption/log:**
  `MAE`, `RMSE`, `PSNR` (if images), and `% pixels below τ` (robust threshold like τ = 1e−3 units).

---

## Python snippet (ready to paste)

```python
import numpy as np, matplotlib.pyplot as plt

def load(path): 
    a = np.load(path)
    return a.astype(np.float32)

def norm_range(arrs, pct=1.0):
    lo = min(np.nanpercentile(a, pct) for a in arrs)
    hi = max(np.nanpercentile(a, 100-pct) for a in arrs)
    return float(lo), float(hi)

def mae(a,b): return float(np.nanmean(np.abs(a-b)))
def rmse(a,b): return float(np.sqrt(np.nanmean((a-b)**2)))

# --- inputs ---
q0 = load("q0.npy")
qb = load("q_final_baseline.npy")
qa = load("q_final_assisted.npy")

# choose a single channel if 3D
if q0.ndim == 3: 
    q0, qb, qa = q0[...,0], qb[...,0], qa[...,0]

# global ranges
vmin, vmax = norm_range([q0, qb, qa], pct=1.0)
db = np.abs(qb - q0); da = np.abs(qa - q0)
dmax = np.nanpercentile(np.concatenate([db.ravel(), da.ravel()]), 99.0)

# metrics
Eb = mae(qb, q0); Rb = rmse(qb, q0)
Ea = mae(qa, q0); Ra = rmse(qa, q0)

def panel(ax_img, ax_diff, q, d, tag):
    im = ax_img.imshow(q, vmin=vmin, vmax=vmax, cmap="viridis")
    ax_img.set_xticks([]); ax_img.set_yticks([])
    ax_img.text(0.02, 0.06, tag, color="white", fontsize=9, transform=ax_img.transAxes,
                bbox=dict(fc=(0,0,0,0.35), ec="none", pad=2))
    dm = ax_diff.imshow(d, vmin=0, vmax=dmax, cmap="magma")
    ax_diff.set_xticks([]); ax_diff.set_yticks([])
    return im, dm

fig = plt.figure(figsize=(6,7.5), dpi=240)
gs = fig.add_gridspec(2, 2, height_ratios=[1,1], hspace=0.15, wspace=0.08)

ax_b_img = fig.add_subplot(gs[0,0]); ax_a_img = fig.add_subplot(gs[0,1])
ax_b_dif = fig.add_subplot(gs[1,0]); ax_a_dif = fig.add_subplot(gs[1,1])

im_b, dm_b = panel(ax_b_img, ax_b_dif, qb, db, f"BASELINE  E={Eb:.3e}, RMSE={Rb:.3e}")
im_a, dm_a = panel(ax_a_img, ax_a_dif, qa, da, f"ASSISTED  E={Ea:.3e}, RMSE={Ra:.3e}")

# shared colorbars
cbar1 = fig.colorbar(im_b, ax=[ax_b_img, ax_a_img], fraction=0.025, pad=0.02)
cbar1.set_label("q intensity")
cbar2 = fig.colorbar(dm_b, ax=[ax_b_dif, ax_a_dif], fraction=0.025, pad=0.02)
cbar2.set_label("|q - q₀|")

ax_b_img.set_title("Final state"); ax_a_img.set_title("Final state")
ax_b_dif.set_title("Difference vs q₀"); ax_a_dif.set_title("Difference vs q₀")
fig.suptitle("Echo comparison: Baseline vs Assisted (shared scales)", y=0.995, fontsize=11)

plt.tight_layout()
plt.savefig("echo_comparison.png")
plt.close(fig)
```

---

## Usage notes

* Keep **the same colormap and ranges** across a whole paper/section to prevent unintentional cheating.
* If domains vary, overlay a faint boundary/mesh so readers see geometry.
* For time‑series, stack frames horizontally (t₁…tₖ) with the same colorbars.
* Report both **pixel metrics** (MAE/RMSE) and a **functional metric** (e.g., refocused signal at probe ROI).

---

If you want, I can adapt this into your repo style (paths, logging, gate tags like T2/T3), or convert it into a small CLI (`vdm-echo-viz`) that scans a run directory and batch‑renders these figures.
