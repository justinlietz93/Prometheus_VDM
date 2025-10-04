"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

import numpy as np

# Try to import user's libraries first
try:
    # Import only the elemental deltas from the user's equations.
    # We compose universal_void_dynamics locally to guarantee growth+decay are combined.
    from Void_Equations import delta_re_vgsp, delta_gdsp, get_universal_constants
    HAVE_EXTERNAL = True
except Exception:
    HAVE_EXTERNAL = False
    # Minimal fallback (keeps runtime alive if your file isn't on PYTHONPATH yet)
    ALPHA, BETA, F_REF, PHASE_SENS = 0.25, 0.1, 0.02, 0.5
    def get_universal_constants():
        return {'ALPHA': ALPHA, 'BETA': BETA, 'F_REF': F_REF, 'PHASE_SENS': PHASE_SENS}
    def delta_re_vgsp(W, t, alpha=None, f_ref=None, phase_sens=None, use_time_dynamics=True, domain_modulation=1.0):
        if alpha is None: alpha = ALPHA
        if f_ref is None: f_ref = F_REF
        if phase_sens is None: phase_sens = PHASE_SENS
        eff = alpha * domain_modulation
        noise = np.random.uniform(-0.02, 0.02, size=W.shape)
        base = eff * W * (1 - W) + noise
        if use_time_dynamics:
            phase = np.sin(2 * np.pi * f_ref * t)
            return base * (1 + phase_sens * phase)
        return base
    def delta_gdsp(W, t, beta=None, f_ref=None, phase_sens=None, use_time_dynamics=True, domain_modulation=1.0):
        if beta is None: beta = BETA
        if f_ref is None: f_ref = F_REF
        if phase_sens is None: phase_sens = PHASE_SENS
        eff = beta * domain_modulation
        base = -eff * W
        if use_time_dynamics:
            phase = np.sin(2 * np.pi * f_ref * t)
            return base * (1 + phase_sens * phase)
        return base

# Domain modulation
# Compose universal dynamics locally so growth+decay are always present (avoids saturation).
def universal_void_dynamics(W, t, domain_modulation=1.0, use_time_dynamics=True):
    re = delta_re_vgsp(W, t, use_time_dynamics=use_time_dynamics, domain_modulation=domain_modulation)
    gd = delta_gdsp(W, t, use_time_dynamics=use_time_dynamics, domain_modulation=domain_modulation)
    return re + gd

# Domain modulation
def get_domain_modulation(domain: str):
    # Try user's universal modulation
    try:
        from FUM_Void_Debt_Modulation import VoidDebtModulation
        mod = VoidDebtModulation().get_universal_domain_modulation(domain)
        return float(mod['domain_modulation'])
    except Exception:
        # Fallback to safe default
        targets = {
            'quantum': 0.15, 'standard_model': 0.22, 'dark_matter': 0.27,
            'biology_consciousness': 0.20, 'cosmogenesis': 0.84, 'higgs': 0.80
        }
        ALPHA = get_universal_constants()['ALPHA']
        BETA  = get_universal_constants()['BETA']
        void_debt_ratio = BETA/ALPHA if ALPHA != 0 else 0.4
        s = targets.get(domain, 0.25)
        return 1.0 + (s ** 2) / void_debt_ratio
