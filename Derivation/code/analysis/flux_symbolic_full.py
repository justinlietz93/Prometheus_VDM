#!/usr/bin/env python3
"""Symbolic CAS: small-N search for discrete flux H_ij.

We use N=2 and the first-order approximation ΔQ ≈ Q'(W) * ΔW (small-step/Taylor).
Ansatz: H_ij = sum_k c_k * W_i^{a_k} * W_j^{b_k} with monomials up to degree 2.
Solve linear equations for coefficients c_k such that ΔQ_i = sum_j (H_ji - H_ij).
"""
from sympy import symbols, diff, log, simplify, expand, collect, Eq, solve_linear_system, Matrix
from sympy import Symbol

def main():
    # symbols
    W1, W2, alpha, beta, r, u = symbols('W1 W2 alpha beta r u')
    t = 0

    # deterministic deltaW: alpha*W*(1-W) - beta*W
    delta1 = alpha * W1 * (1 - W1) - beta * W1
    delta2 = alpha * W2 * (1 - W2) - beta * W2

    # Q(W) = ln(W) - ln(r - u W) - r t
    Q1 = log(W1) - log(r - u * W1) - r * t
    Q2 = log(W2) - log(r - u * W2) - r * t

    # first-order approximation
    dQ1 = simplify(diff(Q1, W1) * delta1)
    dQ2 = simplify(diff(Q2, W2) * delta2)

    # ansatz monomials: (1,0),(0,1),(1,1),(2,0),(0,2)
    monomials = [(1,0),(0,1),(1,1),(2,0),(0,2)]
    coeffs = symbols('c0:5')

    def H_ij(Wi, Wj):
        expr = 0
        for (a,b), c in zip(monomials, coeffs):
            expr += c * (Wi**a) * (Wj**b)
        return expr

    H12 = H_ij(W1, W2)
    H21 = H_ij(W2, W1)

    # equation for node 1: dQ1 - (H21 - H12) == 0
    eq1 = simplify(dQ1 - (H21 - H12))
    # expand and collect by monomials in W1,W2
    eq1s = expand(eq1)

    # build linear system by collecting coefficients of monomials up to total degree 3
    terms = []
    for a in range(0,4):
        for b in range(0,4 - a):
            terms.append(W1**a * W2**b)

    # express eq1s as coefficients over the selected terms
    A_rows = []
    b_vec = []
    # we are solving for coeffs c0..c4
    # collect coefficients of each monomial
    eq_expanded = expand(eq1s)
    # represent as linear combination of coeffs + non-coeff part; move non-coeff to RHS
    # For simplicity, substitute numeric symbols for alpha,beta,r,u? We'll keep symbolic and collect.
    # Collect coefficients multiplying each c_k: these come from -(H21-H12) parts.
    # Compute contribution of each c_k to (H21 - H12):
    contribs = []
    for (a,b) in monomials:
        term = (W2**a * W1**b) - (W1**a * W2**b)
        contribs.append(term)

    # eq1s = dQ1 - sum_k c_k * contribs[k]
    # Rearranged: sum_k c_k * contribs[k] = dQ1
    # We'll collect coefficients of monomials on both sides and equate.
    # Build matrix of coefficients for unknowns c_k by collecting each contribs[k]
    M = []
    RHS = []
    for term in terms:
        row = [simplify(expand(contribs[k].coeff(term))) for k in range(len(coeffs))]
        M.append([r for r in row])
        RHS.append(simplify(expand(dQ1.coeff(term))))

    # Convert to sympy Matrix and attempt solve for coeffs using least squares (if overdetermined)
    Mat = Matrix(M)
    RHSv = Matrix(RHS)
    # Solve linear system Mat * c = RHSv
    # Symbolic solve: use Mat.gauss_jordan_solve when possible, otherwise report underdetermined
    try:
        sol = Mat.gauss_jordan_solve(RHSv)
        print('solution (gauss_jordan_solve):', sol)
    except Exception as e:
        print('gauss_jordan_solve failed:', e)
        # fallback: attempt linear solve numeric by substituting sample numeric parameters
        print('Attempting numeric solve with representative parameters...')
        subs_map = {alpha: 0.25, beta: 0.1, r: 0.15, u: 0.25}
        M_num = Matrix([[m.subs(subs_map) for m in row] for row in M])
        RHS_num = Matrix([r.subs(subs_map) for r in RHS])
        try:
            sol_num = (M_num.T * M_num).inv() * M_num.T * RHS_num
            print('numeric least-squares solution:', [float(x) for x in sol_num])
        except Exception as e2:
            print('numeric solve failed:', e2)

if __name__ == '__main__':
    main()
