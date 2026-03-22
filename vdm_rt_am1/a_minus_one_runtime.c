#include "a_minus_one_runtime.h"

void *a_minus_one_bifop(void *aclass_n,
                        const a_minus_one_ops *ops,
                        void *ctx) {
    if (ops->artcap_positive(aclass_n, ctx)) {
        return aclass_n;
    }

    if (ops->bear(aclass_n, ctx) && !ops->discharged(aclass_n, ctx)) {
        return ops->append_orthogonal(
            aclass_n,
            ops->orthogonal_admit(aclass_n, ctx),
            ctx
        );
    }

    return ops->undefined_case(aclass_n, ctx);
}
