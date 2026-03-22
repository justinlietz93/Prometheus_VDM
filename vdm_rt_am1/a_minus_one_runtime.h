#ifndef A_MINUS_ONE_RUNTIME_H
#define A_MINUS_ONE_RUNTIME_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Literal A(-1) kernel boundary.
 *
 * The kernel does not classify outcomes, validate inputs, define origin policy,
 * assign storage semantics, or decide what happens outside the law's defined
 * branches. All such policy is externalized.
 */

typedef int   (*a_minus_one_artcap_positive_fn)(const void *aclass_n, void *ctx);
typedef int   (*a_minus_one_bear_fn)(const void *aclass_n, void *ctx);
typedef int   (*a_minus_one_discharged_fn)(const void *aclass_n, void *ctx);
typedef void *(*a_minus_one_orthogonal_admit_fn)(const void *aclass_n, void *ctx);
typedef void *(*a_minus_one_append_orthogonal_fn)(void *aclass_n,
                                                   void *aclass_np1_perp,
                                                   void *ctx);
typedef void *(*a_minus_one_undefined_fn)(void *aclass_n, void *ctx);

typedef struct {
    a_minus_one_artcap_positive_fn   artcap_positive;
    a_minus_one_bear_fn              bear;
    a_minus_one_discharged_fn        discharged;
    a_minus_one_orthogonal_admit_fn  orthogonal_admit;
    a_minus_one_append_orthogonal_fn append_orthogonal;
    a_minus_one_undefined_fn         undefined_case;
} a_minus_one_ops;

void *a_minus_one_bifop(void *aclass_n,
                        const a_minus_one_ops *ops,
                        void *ctx);

#ifdef __cplusplus
}
#endif

#endif
