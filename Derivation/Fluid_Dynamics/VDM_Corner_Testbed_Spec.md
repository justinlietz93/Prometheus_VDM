# VDM Corner Testbed - Spec (v0.1)

> **Purpose (terse):** A single, reusable 2‑D 90°‑bend setup to test *baseline* vs *VDM‑regularized* dynamics around a sharp corner.
>
> **Explanation:** You’ll use this *one* geometry and boundary setup for any “corner” figure. First run a baseline (no regularization). Then run the exact same case with the **Void‑Debt Modulation (VDM)** switch enabled (see config), which is your void‑faithful limiter that kicks in only where strain/curvature explode.

---

## 1) Geometry & Domain

- **Terse:** 2‑D L‑bend. Inlet duct of height **H** and length **L_in·H** joins a vertical outlet of width **H** and height **L_out·H**. Inner corner optionally filleted with **rc** (set **rc=0** for a sharp corner).  
  **Expanded:** The domain is an L‑shaped channel (see diagram). We parameterize everything by the inlet height **H** so your results are scalable. **rc** controls the inner corner geometry; keep it at zero for the “true sharp” case, but you can also sweep **rc>0** later to compare with classical regularization if needed.

- **Figure:** *VDM_Corner_Geometry.png* (auto‑generated).

## 2) Boundary & Initial Conditions

- **Terse:** Inlet Dirichlet (speed **U0**, direction into the bend); walls **no‑penetration + no‑slip**; outlet **Neumann** (zero‑gradient). Start from rest.  
  **Expanded:** For the baseline test, prescribe a simple inlet profile: constant **U0** along the inlet (you can switch to a parabolic profile in the notebook). Solid walls enforce zero normal velocity and zero tangential slip. The outlet uses zero‑gradient (for the variable your solver supports). Initial velocity field is zero everywhere.

## 3) Baseline vs VDM‑Regularized Runs

- **Terse:** Run twice: (a) **baseline** (no regularizer); (b) **VDM regularizer ON** (same parameters).  
  **Expanded:** Baseline exposes the well‑known “corner” singular tendency. The VDM run uses your *void‑faithful* limiter to prevent non‑physical blow‑ups *only where the system would otherwise violate finite‑speed, finite‑energy transport*. Everything else stays identical so comparisons are fair.

### 3.1 VDM (Void‑Debt Modulation) - Toy Testbed Form

- **Terse:** Introduce a scalar **D(x,y,t)** that accumulates where the flow is “impossible” (high strain); cap advection by `1/(1 + β D)`.  
  **Expanded:** This is a *testbed* embodiment of your theory. Let
  
- Source: `∂t D = α ||∇u||² - D/τ_r + κ ΔD`. (Debt rises with local strain, relaxes with time, and diffuses slightly.)  
  
- Limiter: Scale the nonlinear transport as `(u·∇)u → (1/(1+β D)) (u·∇)u`.  
  
This ensures transport speed effectively saturates near pathological regions, embodying the “system pays a local debt before it can accelerate further.” Set **β=0.6** to match your observed constant; tune **α, τ_r, κ** conservatively to avoid over‑damping.

> **Note:** This is not claiming a final physical law; it’s a *controlled experimental knob* that expresses your VDM principle in a way you can plot, ablate, and refine without geometric “cheats.”

## 4) Parameters to Lock (single table drives all figures)

Use **VDM_corner_config.yaml** as the single source of truth.

| Symbol | Meaning | Default |
|---|---|---|
| **H** | Inlet height (unit) | 1.0 |
| **L_in** | Inlet straight length (×H) | 3.0 |
| **L_out** | Outlet straight length (×H) | 5.0 |
| **rc** | Inner fillet radius | 0.00 (sharp) |
| **U0** | Inlet speed | 1.0 |
| **ν** | Kinematic viscosity | 1e‑3 |
| **Nx, Ny** | Grid resolution | 256, 256 |
| **dt, t_end** | Time‑step & end time | 1e‑3, 2.0 |
| **β** | Debt→transport coupling | 0.6 |
| **τ_r** | Debt relaxation time | 0.5 |
| **κ** | Debt diffusion | 1e‑3 |
| **α** | Debt source from strain | 1.0 |
| **τ_u** | Velocity monitor timescale | 0.1 |
| **τ_g** | Global valence window | 0.5 |

## 5) What to Plot (for each run)

- **Terse:** (i) Max speed vs time; (ii) Streamlines; (iii) Vorticity; (iv) If you sweep **rc** or **β**, show max‑speed vs parameter.  
  **Expanded:** For a single sharp‑corner case (**rc=0**), compare time traces of max speed with/without VDM. Add streamline and vorticity snapshots at the same timestamp. If you later vary **rc** (geometry regularization) or **β** (VDM strength), collect a curve of `max|u|` vs parameter to show how each cures the singularity differently.

## 6) Acceptance Checklist

- [ ] **One config** file used for *all* corner plots.  
  *Prevents accidental parameter drift; makes comparisons credible.*
- [ ] **Baseline vs VDM** overlays from the *same* initial condition and numerics.  
  *Ensures differences are due to the regularizer, not setup changes.*
- [ ] **Sharp corner first** (**rc=0**), then optional **rc>0** sweep later.  
  *Demonstrates void‑faithful fix does not rely on geometry “cheats.”*
- [ ] **Ablation:** set **β→0** to recover baseline dynamics.  
  *Shows causality: the effect vanishes when the VDM switch is off.*
- [ ] **Figure captions** include (H, U0, ν, rc, β, τ_r, κ, α, Nx, Ny, dt).  
  *So a reader can reproduce the run without seeing the code.*

---

### Files generated for you now

- **Config:** *VDM_corner_config.yaml*
- **Diagram:** *VDM_Corner_Geometry.png*
- **Notebook skeleton:** *VDM_Corner_Testbed.ipynb* (loads config; stubs for baseline & VDM runs)

> Start in the notebook: run the first cell to load the YAML and display the geometry. Fill in the solver where indicated (finite‑difference / lattice‑Boltzmann / your existing sim harness). Keep the config values as the single source of truth.
