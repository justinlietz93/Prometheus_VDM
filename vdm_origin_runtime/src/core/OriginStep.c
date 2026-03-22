/*
 * OriginStep.c
 *
 * Outer generative driver around BInv.
 *
 * This file does not add a second law.
 * It only operationalizes:
 *
 *   1. same-class articulation attempt
 *   2. same-class integration if the articulation is genuinely new and invariant-bearing
 *   3. otherwise, defer to BInv for forced orthogonal continuation
 *
 * All witness semantics remain external.
 */

extern void *BInv(void *Inv, void *A_n);

extern void *ArticulateSameClass(void *Inv, void *A_n);
extern int   IsGenuinelyNew(void *candidate, void *A_n);
extern int   Bear(void *Inv, void *A_n);
extern void *IntegrateSameClass(void *A_n, void *candidate);

void *OriginStep(void *Inv, void *A_n)
{
    void *candidate = ArticulateSameClass(Inv, A_n);

    if (candidate && IsGenuinelyNew(candidate, A_n) && Bear(Inv, candidate))
        return IntegrateSameClass(A_n, candidate);

    return BInv(Inv, A_n);
}
