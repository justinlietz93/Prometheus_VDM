#include <stddef.h>

/*
A(-1) runtime kernel
--------------------
This file intentionally implements only the executable operator form:

  B_Inv(A_n) =
    A_n,                                 if Cap(A_n) > 0
    A_n ⊕ A_{n+1}^⊥,                     if Cap(A_n) = 0 and Bear(Inv, A_n) and !Dis(Inv)

Everything else is delegated outward.
The kernel does NOT define:
  - what an articulation class "is"
  - how capacity is computed
  - how bearing is witnessed
  - how discharge is detected
  - what orthogonality means in a concrete representation
  - how ⊕ is realized in storage

Those are representation-level obligations, not primitive-law code.
*/

typedef enum {
    A_MINUS_ONE_ERROR     = -1,
    A_MINUS_ONE_STAY      =  0,
    A_MINUS_ONE_EXTEND    =  1,
    A_MINUS_ONE_UNDEFINED =  2
} a_minus_one_result;

typedef struct a_minus_one_ops {
    /* Return nonzero iff ArtCap(A_n) > 0. */
    int (*artcap_positive)(const void *aclass_n, void *ctx);

    /* Return nonzero iff Bear(Inv, A_n). */
    int (*bear)(const void *aclass_n, void *ctx);

    /* Return nonzero iff Dis(Inv). */
    int (*discharged)(const void *aclass_n, void *ctx);

    /*
    Construct the least admissible orthogonal class A_{n+1}^⊥.
    On success, write the new class handle to *aclass_np1 and return nonzero.
    */
    int (*orthogonal_admit)(const void *aclass_n, void **aclass_np1, void *ctx);

    /*
    Realize A_n ⊕ A_{n+1}^⊥.
    The implementation may mutate *aclass_n in place or replace it.
    Return nonzero on success.
    */
    int (*append_orthogonal)(void **aclass_n, void *aclass_np1, void *ctx);
} a_minus_one_ops;

/*
Execute exactly the primitive operator on an already-admitted class A_n.

Outcomes:
  A_MINUS_ONE_STAY
      The law returns A_n unchanged because same-class articulation capacity remains.

  A_MINUS_ONE_EXTEND
      The law returns A_n ⊕ A_{n+1}^⊥ because capacity is exhausted while bearing remains and discharge is forbidden.

  A_MINUS_ONE_UNDEFINED
      The antecedent for forced orthogonal extension is not satisfied once capacity is exhausted.
      This is not a second law; it simply means the provided state does not license the extension branch.

  A_MINUS_ONE_ERROR
      Null pointers or failed representation-level operations.
*/
a_minus_one_result a_minus_one_bifop(
    void **aclass_n,
    const a_minus_one_ops *ops,
    void *ctx
) {
    void *aclass_np1;

    if (!aclass_n || !*aclass_n || !ops) return A_MINUS_ONE_ERROR;
    if (!ops->artcap_positive || !ops->bear || !ops->discharged ||
        !ops->orthogonal_admit || !ops->append_orthogonal) {
        return A_MINUS_ONE_ERROR;
    }

    /* Branch 1: B_Inv(A_n) = A_n when Cap(A_n) > 0. */
    if (ops->artcap_positive(*aclass_n, ctx)) {
        return A_MINUS_ONE_STAY;
    }

    /* Branch 2 guard: Cap(A_n) = 0 and Bear(Inv, A_n) and !Dis(Inv). */
    if (!ops->bear(*aclass_n, ctx)) {
        return A_MINUS_ONE_UNDEFINED;
    }

    if (ops->discharged(*aclass_n, ctx)) {
        return A_MINUS_ONE_UNDEFINED;
    }

    aclass_np1 = NULL;
    if (!ops->orthogonal_admit(*aclass_n, &aclass_np1, ctx)) {
        return A_MINUS_ONE_ERROR;
    }
    if (!aclass_np1) {
        return A_MINUS_ONE_ERROR;
    }

    if (!ops->append_orthogonal(aclass_n, aclass_np1, ctx)) {
        return A_MINUS_ONE_ERROR;
    }

    return A_MINUS_ONE_EXTEND;
}
