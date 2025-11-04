Here’s a quick, practical sanity‑check for **Rayleigh–Bénard convection (RBC)** that you can drop into any fluid/heat sim to tell if you *should* see convection rolls or just plain conduction.

---

### What’s the core idea?

Convection in a horizontal fluid layer heated from below turns on only after buoyancy beats viscosity + thermal diffusion. The on/off switch is the **Rayleigh number**:
[
\mathrm{Ra}=\frac{g,\alpha,\Delta T,H^{3}}{\nu,\kappa}
]

* (g): gravity
* (\alpha): thermal expansion coefficient
* (\Delta T): temperature drop across the layer
* (H): layer depth
* (\nu): kinematic viscosity
* (\kappa): thermal diffusivity

---

### Pass/Fail gate (rigid plates)

* **Critical threshold:** (\boxed{\mathrm{Ra}_c \approx 1708}) (no‑slip top & bottom).
* **Below (1708):** conduction only (no rolls).
* **Above (1708):** steady convection rolls should appear.

Near onset, this (\mathrm{Ra}_c) is effectively **independent of Prandtl number** (so you don’t need to tune ( \mathrm{Pr}=\nu/\kappa ) to use this gate).

---

### What pattern to expect at onset?

* **Critical wavenumber:** (\boxed{k_c \approx 3.117})
* **Roll wavelength:** (\displaystyle \lambda_c=\frac{2\pi}{k_c}\approx 2.015,H ;;(\approx 2\times \text{depth}))

So, first rolls have a spacing about **twice the layer depth**.

---

### Minimal checklist for your sim

1. Compute ( \mathrm{Ra} ) from your parameters.
2. If ( \mathrm{Ra}<1708) → expect flat temperature profile + zero mean flow (conduction).
3. If ( \mathrm{Ra}\gtrsim1708) → expect roll pattern with wavelength (\approx 2H).
4. Validate wave number via FFT along the horizontal; peak should sit near (k_c).
5. Vary (\Delta T) (or (H)) to cross the threshold and confirm the bifurcation.

---

### Fast mapping to your M‑limb parameters

* Treat **depth (H)** as the control knob: doubling (H) multiplies (\mathrm{Ra}) by **(8)** and the onset roll spacing by **(\approx 2)**.
* If you see rolls when (\mathrm{Ra}<1708) (or no rolls when (\mathrm{Ra}>1708)), that flags a boundary condition or nondimensionalization bug (e.g., slip BCs, wrong (\nu,\kappa), or effective gravity).

Want me to wrap this into a tiny “RBC gate” function (given (g,\alpha,\Delta T,H,\nu,\kappa) → returns PASS/FAIL + predicted (\lambda_c))?
