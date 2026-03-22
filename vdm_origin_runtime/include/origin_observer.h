#ifndef ORIGIN_OBSERVER_H
#define ORIGIN_OBSERVER_H

#include <stdio.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct origin_event {
    const char *kind;
    uint64_t    step;
    void       *inv;
    void       *class_before;
    void       *class_after;
    void       *candidate;
    void       *orthogonal;
    int         cap_gt_zero;
    int         cap_eq_zero;
    int         bear_current;
    int         bear_candidate;
    int         is_genuinely_new;
    int         dis;
} origin_event;

typedef void (*origin_event_sink)(const origin_event *ev, void *user);

typedef struct origin_ndjson_writer {
    FILE *fp;
} origin_ndjson_writer;

void origin_ndjson_sink(const origin_event *ev, void *user);

#ifdef __cplusplus
}
#endif

#endif
