/*
 * Primitive Bifurcation Law — exact executable rendering of Equation (10)
 *
 *   B_Inv(A_n) =
 *     A_n,                          if Cap(A_n) > 0
 *     A_n ⊕ A_{n+1}^⊥,              if Cap(A_n)=0 ∧ Bear(Inv,A_n) ∧ ¬Dis(Inv)
 *
 * This file programs only the primitive law.
 * All witness semantics are external.
 */

extern int   Cap_gt_zero(void *A_n);
extern int   Cap_eq_zero(void *A_n);
extern int   Bear(void *Inv, void *A_n);
extern int   Dis(void *Inv);
extern void *OrthogonalAdmit(void *A_n);
extern void *Append(void *A_n, void *A_n1_perp);

void *BInv(void *Inv, void *A_n)
{
    if (Cap_gt_zero(A_n))
        return A_n;

    if (Cap_eq_zero(A_n) && Bear(Inv, A_n) && !Dis(Inv))
        return Append(A_n, OrthogonalAdmit(A_n));

#if defined(__GNUC__) || defined(__clang__)
    __builtin_unreachable();
#endif
}
