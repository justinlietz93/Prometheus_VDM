#include "a_minus_one_runtime.h"

a_minus_one_result a_minus_one_bifop(void **aclass_n,
                                     const a_minus_one_ops *ops,
                                     void *ctx) {
    void *aclass_np1 = 0;

    if (!aclass_n || !ops) {
        return A_MINUS_ONE_ERROR;
    }

    if (!ops->artcap_positive ||
        !ops->bear ||
        !ops->discharged ||
        !ops->orthogonal_admit ||
        !ops->append_orthogonal) {
        return A_MINUS_ONE_ERROR;
    }

    if (!*aclass_n) {
        return A_MINUS_ONE_UNDEFINED;
    }

    if (ops->artcap_positive(*aclass_n, ctx)) {
        return A_MINUS_ONE_STAY;
    }

    if (!ops->bear(*aclass_n, ctx)) {
        return A_MINUS_ONE_UNDEFINED;
    }

    if (ops->discharged(*aclass_n, ctx)) {
        return A_MINUS_ONE_UNDEFINED;
    }

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
