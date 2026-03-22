#include "origin_observer.h"

#include <inttypes.h>

static const char *pstr(void *p)
{
    /* JSON string-safe pointer rendering with no heap allocation.
       fprintf handles %p formatting directly, so this helper is unused. */
    (void)p;
    return "";
}

void origin_ndjson_sink(const origin_event *ev, void *user)
{
    origin_ndjson_writer *w = (origin_ndjson_writer *)user;
    if (!w || !w->fp || !ev) return;

    fprintf(
        w->fp,
        "{"
        "\"kind\":\"%s\","
        "\"step\":%" PRIu64 ","
        "\"inv\":\"%p\","
        "\"class_before\":\"%p\","
        "\"class_after\":\"%p\","
        "\"candidate\":\"%p\","
        "\"orthogonal\":\"%p\","
        "\"cap_gt_zero\":%d,"
        "\"cap_eq_zero\":%d,"
        "\"bear_current\":%d,"
        "\"bear_candidate\":%d,"
        "\"is_genuinely_new\":%d,"
        "\"dis\":%d"
        "}\n",
        ev->kind ? ev->kind : "",
        ev->step,
        ev->inv,
        ev->class_before,
        ev->class_after,
        ev->candidate,
        ev->orthogonal,
        ev->cap_gt_zero,
        ev->cap_eq_zero,
        ev->bear_current,
        ev->bear_candidate,
        ev->is_genuinely_new,
        ev->dis
    );

    fflush(w->fp);
}
