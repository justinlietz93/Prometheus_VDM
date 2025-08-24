import numpy as np
# ===== UNIVERSAL PHYSICAL CONSTANTS =====
# These are NOT arbitrary - they come from actual FUM AI learning stability
# requirements, yet they produce realistic physics across all domains
ALPHA = 0.25      # Universal learning rate for RE-VGSP (Resonance-Enhanced dynamics)
BETA = 0.1        # Universal plasticity rate for GDSP (Goal-Directed dynamics)
F_REF = 0.02      # Universal reference frequency for time modulation
PHASE_SENS = 0.5  # Universal phase sensitivity for time modulation

def delta_re_vgsp(W, t, alpha=None, f_ref=None, phase_sens=None, use_time_dynamics=True, domain_modulation=1.0):
    """
    Void Chaos Function: Synchronizes with Void Order Function
    Universal function for FUM Resonance-Enhanced Valence-Gated Synaptic Plasticity.
    Models the fractal energy drain/pull (learning rule).
    
    Args:
        W: Current void state
        t: Time step
        alpha: Learning rate (defaults to universal constant)
        f_ref: Reference frequency (defaults to universal constant)
        phase_sens: Phase sensitivity (defaults to universal constant)
        use_time_dynamics: Enable time modulation
        domain_modulation: Domain-specific scaling factor
    """
    # Use universal constants as defaults
    if alpha is None:
        alpha = ALPHA
    if f_ref is None:
        f_ref = F_REF
    if phase_sens is None:
        phase_sens = PHASE_SENS
    

    
    # Apply domain modulation to alpha
    effective_alpha = alpha * domain_modulation
    
    noise = np.random.uniform(-0.02, 0.02)
    base_delta = effective_alpha * W * (1 - W) + noise
    


    if use_time_dynamics:
        phase = np.sin(2 * np.pi * f_ref * t)
        return base_delta * (1 + phase_sens * phase)
    return base_delta

def delta_gdsp(W, t, beta=None, f_ref=None, phase_sens=None, use_time_dynamics=True, domain_modulation=1.0):
    """
    Void Order Function: Synchronizes with Void Chaos Function
    Universal function for FUM Goal-Directed Structural Plasticity.
    Models the weak closure for persistent voids (structural rule).
    
    Args:
        W: Current void state
        t: Time step
        beta: Plasticity rate (defaults to universal constant)
        f_ref: Reference frequency (defaults to universal constant)
        phase_sens: Phase sensitivity (defaults to universal constant)
        use_time_dynamics: Enable time modulation
        domain_modulation: Domain-specific scaling factor
    """
    # Use universal constants as defaults
    if beta is None:
        beta = BETA
    if f_ref is None:
        f_ref = F_REF
    if phase_sens is None:
        phase_sens = PHASE_SENS
    
    # Apply domain modulation to beta
    effective_beta = beta * domain_modulation
    
    base_delta = -effective_beta * W
    
    if use_time_dynamics:
        phase = np.sin(2 * np.pi * f_ref * t)
        return base_delta * (1 + phase_sens * phase)
    return base_delta
