#ifndef A_MINUS_ONE_RUNTIME_H
#define A_MINUS_ONE_RUNTIME_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    A_MINUS_ONE_ERROR     = -1,
    A_MINUS_ONE_STAY      =  0,
    A_MINUS_ONE_EXTEND    =  1,
    A_MINUS_ONE_UNDEFINED =  2
} a_minus_one_result;

typedef int (*a_minus_one_artcap_positive_fn)(const void *aclass_n, void *ctx);
typedef int (*a_minus_one_bear_fn)(const void *aclass_n, void *ctx);
typedef int (*a_minus_one_discharged_fn)(const void *aclass_n, void *ctx);
typedef int (*a_minus_one_orthogonal_admit_fn)(const void *aclass_n,
                                                void **aclass_np1,
                                                void *ctx);
typedef int (*a_minus_one_append_orthogonal_fn)(void **aclass_n,
                                                 void *aclass_np1,
                                                 void *ctx);

typedef struct {
    a_minus_one_artcap_positive_fn     artcap_positive;
    a_minus_one_bear_fn                bear;
    a_minus_one_discharged_fn          discharged;
    a_minus_one_orthogonal_admit_fn    orthogonal_admit;
    a_minus_one_append_orthogonal_fn   append_orthogonal;
} a_minus_one_ops;

a_minus_one_result a_minus_one_bifop(void **aclass_n,
                                     const a_minus_one_ops *ops,
                                     void *ctx);

#ifdef __cplusplus
}
#endif

#endif
