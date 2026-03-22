#include <stdint.h>
#include <stdlib.h>

typedef struct origin_invariant {
    uint64_t seed;
} origin_invariant;

typedef struct origin_class {
    uint64_t id;
    uint64_t depth;
    uint64_t accepted_local;
    uint64_t local_budget;
    struct origin_class *prior;
} origin_class;

typedef struct origin_candidate {
    uint64_t parent_id;
    uint64_t novelty_index;
} origin_candidate;

static uint64_t next_class_id = 1;

static origin_class *as_class(void *p)
{
    return (origin_class *)p;
}

static origin_candidate *as_candidate(void *p)
{
    return (origin_candidate *)p;
}

static uint64_t local_budget_for_depth(uint64_t depth)
{
    return depth + 2;
}

void *InitialInvariant(void)
{
    origin_invariant *inv = (origin_invariant *)malloc(sizeof(*inv));
    if (!inv) exit(1);
    inv->seed = 1;
    return inv;
}

void *InitialClass(void)
{
    origin_class *c = (origin_class *)malloc(sizeof(*c));
    if (!c) exit(1);
    c->id = next_class_id++;
    c->depth = 0;
    c->accepted_local = 0;
    c->local_budget = local_budget_for_depth(c->depth);
    c->prior = NULL;
    return c;
}

void *ArticulateSameClass(void *Inv, void *A_n)
{
    origin_class *c = as_class(A_n);
    origin_candidate *cand;
    (void)Inv;

    if (!c) return NULL;
    if (c->accepted_local >= c->local_budget) return NULL;

    cand = (origin_candidate *)malloc(sizeof(*cand));
    if (!cand) exit(1);
    cand->parent_id = c->id;
    cand->novelty_index = c->accepted_local + 1;
    return cand;
}

int IsGenuinelyNew(void *candidate, void *A_n)
{
    origin_candidate *cand = as_candidate(candidate);
    origin_class *c = as_class(A_n);
    if (!cand || !c) return 0;
    return cand->parent_id == c->id && cand->novelty_index > c->accepted_local;
}

int Bear(void *Inv, void *A_n)
{
    (void)Inv;
    return A_n != NULL;
}

int Dis(void *Inv)
{
    (void)Inv;
    return 0;
}

int Cap_gt_zero(void *A_n)
{
    origin_class *c = as_class(A_n);
    if (!c) return 0;
    return c->accepted_local < c->local_budget;
}

int Cap_eq_zero(void *A_n)
{
    origin_class *c = as_class(A_n);
    if (!c) return 0;
    return c->accepted_local >= c->local_budget;
}

void *OrthogonalAdmit(void *A_n)
{
    origin_class *prior = as_class(A_n);
    origin_class *next = (origin_class *)malloc(sizeof(*next));
    if (!next) exit(1);
    next->id = next_class_id++;
    next->depth = prior ? prior->depth + 1 : 0;
    next->accepted_local = 0;
    next->local_budget = local_budget_for_depth(next->depth);
    next->prior = prior;
    return next;
}

void *IntegrateSameClass(void *A_n, void *candidate)
{
    origin_class *c = as_class(A_n);
    origin_candidate *cand = as_candidate(candidate);
    if (c && cand && cand->novelty_index > c->accepted_local)
        c->accepted_local = cand->novelty_index;
    free(cand);
    return c;
}

void *Append(void *A_n, void *A_n1_perp)
{
    (void)A_n;
    return A_n1_perp;
}
