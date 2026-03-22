#ifndef ORIGIN_RUNNER_H
#define ORIGIN_RUNNER_H

#include <stddef.h>

#include "origin_observer.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct origin_machine {
    void  *Inv;
    void  *A_n;
    size_t step;
} origin_machine;

typedef struct origin_run_config {
    size_t            max_steps;
    origin_event_sink sink;
    void             *sink_user;
} origin_run_config;

void origin_emit(const origin_run_config *cfg, const origin_event *ev);
void origin_run(origin_machine *machine, const origin_run_config *cfg);
void *origin_step_observed(origin_machine *machine, const origin_run_config *cfg);

#ifdef __cplusplus
}
#endif

#endif
