#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/*
A(-1) binary kernel
-------------------
Execution substrate: binary.
Ontology: NOT bits, NOT a lattice, NOT time, NOT a state machine.

The core law is only this:
  - unresolved opposition remains borne,
  - same-class continuation is admitted only while genuinely new bearing
    remains representable in the current class,
  - when same-class bearing is exhausted while non-discharge remains,
    the least new class is forced.

Implementation note:
  - loop count is computational scaffolding only,
  - rank is an admitted articulation class label, not a geometric dimension,
  - Gray order is used only as the least-change executable shadow of
    minimum additional structure once a class has already been admitted.
*/

typedef enum {
    A_MINUS_ONE_INVALID   = 0,
    A_MINUS_ONE_ORIGIN    = 1,
    A_MINUS_ONE_CONTINUE  = 2,
    A_MINUS_ONE_EXTEND    = 3
} a_minus_one_event_kind;

typedef struct {
    uint8_t  kind;      /* origin / same-class continuation / least extension */
    uint8_t  rank;      /* admitted articulation class label (computational only) */
    uint64_t ordinal;   /* position inside current admitted class (computational only) */
    uint64_t word;      /* least-change binary representative of current class */
} a_minus_one_event;

typedef struct {
    /* primitive-law core */
    uint8_t  bearing;      /* unresolved opposition still borne */
    uint8_t  unresolved;   /* non-discharge still active */

    /* admitted-class bookkeeping (execution only, not ontology) */
    uint8_t  has_class;
    uint8_t  rank;
    uint64_t ordinal;
    uint64_t word;

    /* append-only raw trace */
    a_minus_one_event *trace;
    size_t trace_len;
    size_t trace_cap;
} a_minus_one_kernel;

static uint64_t a_minus_one_gray(uint64_t x) {
    return x ^ (x >> 1);
}

static int a_minus_one_trace_push(a_minus_one_kernel *k, uint8_t kind) {
    if (k->trace_len == k->trace_cap) {
        size_t next_cap = (k->trace_cap == 0) ? 64u : (k->trace_cap << 1u);
        a_minus_one_event *next = (a_minus_one_event*)realloc(k->trace, next_cap * sizeof(*next));
        if (!next) return 0;
        k->trace = next;
        k->trace_cap = next_cap;
    }
    a_minus_one_event *e = &k->trace[k->trace_len++];
    e->kind = kind;
    e->rank = k->rank;
    e->ordinal = k->ordinal;
    e->word = k->word;
    return 1;
}

static uint64_t a_minus_one_class_size(uint8_t rank) {
    if (rank >= 63u) return UINT64_MAX;
    return 1ull << rank;
}

static int a_minus_one_bear(const a_minus_one_kernel *k) {
    return k->bearing && k->unresolved;
}

/*
Same-class representability:
A genuinely new same-class articulation exists iff the current admitted class
still has an unseen least-change representative beyond the present ordinal.
This is the executable shadow of "same-class genuinely new continuation".
*/
static int a_minus_one_same_class_rep(const a_minus_one_kernel *k) {
    if (!k->has_class) return 1; /* the first admitted class has not yet been realized */
    const uint64_t size = a_minus_one_class_size(k->rank);
    if (size == UINT64_MAX) return 0;
    return (k->ordinal + 1ull) < size;
}

/*
The one law, executable form.
Return value is an event kind.
*/
uint8_t a_minus_one_force(a_minus_one_kernel *k) {
    if (!a_minus_one_bear(k)) {
        k->bearing = 0u;
        return A_MINUS_ONE_INVALID;
    }

    /* No admitted class yet: the least first admission is rank 1. */
    if (!k->has_class) {
        k->has_class = 1u;
        k->rank = 1u;
        k->ordinal = 0ull;
        k->word = a_minus_one_gray(0ull);
        if (!a_minus_one_trace_push(k, A_MINUS_ONE_ORIGIN)) return A_MINUS_ONE_INVALID;
        return A_MINUS_ONE_ORIGIN;
    }

    /* Same-class continuation remains possible: admit the least-change new representative. */
    if (a_minus_one_same_class_rep(k)) {
        k->ordinal += 1ull;
        k->word = a_minus_one_gray(k->ordinal);
        if (!a_minus_one_trace_push(k, A_MINUS_ONE_CONTINUE)) return A_MINUS_ONE_INVALID;
        return A_MINUS_ONE_CONTINUE;
    }

    /* Same-class saturation under non-discharge: admit the least new class. */
    if (k->rank == UINT8_MAX) {
        k->bearing = 0u;
        return A_MINUS_ONE_INVALID;
    }

    k->rank += 1u;
    k->ordinal = 0ull;
    k->word = a_minus_one_gray(0ull);
    if (!a_minus_one_trace_push(k, A_MINUS_ONE_EXTEND)) return A_MINUS_ONE_INVALID;
    return A_MINUS_ONE_EXTEND;
}

void a_minus_one_init(a_minus_one_kernel *k) {
    memset(k, 0, sizeof(*k));
    k->bearing = 1u;
    k->unresolved = 1u;
}

void a_minus_one_free(a_minus_one_kernel *k) {
    free(k->trace);
    memset(k, 0, sizeof(*k));
}

/* raw accessors: external diagnostics can interpret, core does not */
const a_minus_one_event *a_minus_one_trace_data(const a_minus_one_kernel *k) {
    return k->trace;
}

size_t a_minus_one_trace_size(const a_minus_one_kernel *k) {
    return k->trace_len;
}

#ifdef A_MINUS_ONE_DEMO
static const char *event_name(uint8_t kind) {
    switch (kind) {
        case A_MINUS_ONE_ORIGIN:   return "origin";
        case A_MINUS_ONE_CONTINUE: return "continue";
        case A_MINUS_ONE_EXTEND:   return "extend";
        default:                   return "invalid";
    }
}

static void print_bits(uint64_t word, uint8_t rank) {
    if (rank == 0u) { putchar('0'); return; }
    for (int i = (int)rank - 1; i >= 0; --i) {
        putchar(((word >> i) & 1ull) ? '1' : '0');
    }
}

int main(void) {
    a_minus_one_kernel k;
    a_minus_one_init(&k);

    for (int i = 0; i < 12; ++i) {
        uint8_t kind = a_minus_one_force(&k);
        if (kind == A_MINUS_ONE_INVALID) {
            fprintf(stderr, "kernel invalid at iteration %d\n", i);
            break;
        }
        const a_minus_one_event *e = &k.trace[k.trace_len - 1u];
        printf("%2d  %-8s rank=%u ordinal=%llu word=", i,
               event_name(kind),
               (unsigned)e->rank,
               (unsigned long long)e->ordinal);
        print_bits(e->word, e->rank);
        putchar('\n');
    }

    a_minus_one_free(&k);
    return 0;
}
#endif
