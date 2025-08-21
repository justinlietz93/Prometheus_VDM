# dimensionless.py
import math

CS2 = 1.0/3.0
CS  = CS2**0.5

def lbm_numbers(U_char, tau, L_char):
    nu = CS2*(tau - 0.5)
    Re = (U_char*L_char)/nu if nu > 0 else float('inf')
    Ma = U_char/CS
    C_lb = U_char  # Δx=Δt=1
    return dict(nu=nu, Re=Re, Ma=Ma, C_lb=C_lb)

def rd_numbers(D, r, L):
    Pi_Dr = D/(r*L*L) if r>0 else float('inf')
    return dict(Pi_Dr=Pi_Dr)

def fuvdm_numbers(theta=None, Lambda=None, Gamma=None, D_a=None, kappa=None, L=None, void_gain=None):
    out = {}
    if theta is not None: out['Theta'] = theta
    if Lambda is not None: out['Lambda'] = Lambda
    if Gamma  is not None: out['Gamma']  = Gamma
    if D_a    is not None: out['D_a']    = D_a
    if kappa is not None and L is not None: out['kappaL'] = kappa*L
    if void_gain is not None: out['g'] = void_gain
    return out
