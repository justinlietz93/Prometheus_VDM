Here’s a quick, practical tip for sampling directions on a sphere without bias, plus why it matters.

![Uniform directions on a sphere illustration](attachment://sphere_uniform_sampling.png)

**Problem (the common gotcha):**
If you draw polar angle θ uniformly in ([0,\pi]) and azimuth φ uniformly in ([0,2\pi)), you’ll over‑sample the poles. That’s because equal steps in θ don’t cover equal **solid angle** (d\Omega=\sin\theta,d\theta,d\phi).

**Fix (isotropic prior):**
Sample (u\sim \mathrm{Uniform}(-1,1)) and set (\cos\theta=u) (so (\theta=\arccos u)), and sample (\phi\sim \mathrm{Uniform}(0,2\pi)). This makes (d\Omega) uniform.

**Code (minimal):**

```python
import numpy as np

def sample_unit_vectors(n):
    u = np.random.uniform(-1.0, 1.0, n)      # cos(theta)
    phi = np.random.uniform(0.0, 2*np.pi, n)
    s = np.sqrt(1 - u*u)
    x = s * np.cos(phi)
    y = s * np.sin(phi)
    z = u
    return np.stack([x, y, z], axis=1)
```

**When to use:**

* Random initial spin/momentum directions
* Ray/particle emission, Monte Carlo integration on (S^2)
* Any “isotropic sky‑axis prior” in inference/simulation (no polar bias)

**Quick checks:**

* Histogram of (z) should be flat on ([-1,1]).
* ((x,y)) should look circularly symmetric at any fixed (z).
