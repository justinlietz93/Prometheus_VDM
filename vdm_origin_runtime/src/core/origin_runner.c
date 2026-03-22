#include "origin_runner.h"

extern void *BInv(void *Inv, void *A_n);

extern void *ArticulateSameClass(void *Inv, void *A_n);
extern int   IsGenuinelyNew(void *candidate, void *A_n);
extern int   Bear(void *Inv, void *A_n);
extern int   Dis(void *Inv);
extern int   Cap_gt_zero(void *A_n);
extern int   Cap_eq_zero(void *A_n);
extern void *OrthogonalAdmit(void *A_n);
extern void *IntegrateSameClass(void *A_n, void *candidate);

void origin_emit(const origin_run_config *cfg, const origin_event *ev)
{
    if (cfg && cfg->sink && ev)
        cfg->sink(ev, cfg->sink_user);
}

void *origin_step_observed(origin_machine *machine, const origin_run_config *cfg)
{
    origin_event ev;
    void *before;
    void *candidate;
    int is_new = 0;
    int bear_candidate = 0;
    int cap_pos;
    int cap_zero;
    int bear_current;
    int dis;
    void *orthogonal = 0;
    void *after;

    before = machine->A_n;

    ev.kind = "step_started";
    ev.step = (uint64_t)machine->step;
    ev.inv = machine->Inv;
    ev.class_before = before;
    ev.class_after = before;
    ev.candidate = 0;
    ev.orthogonal = 0;
    ev.cap_gt_zero = -1;
    ev.cap_eq_zero = -1;
    ev.bear_current = -1;
    ev.bear_candidate = -1;
    ev.is_genuinely_new = -1;
    ev.dis = -1;
    origin_emit(cfg, &ev);

    candidate = ArticulateSameClass(machine->Inv, before);

    ev.kind = "candidate_produced";
    ev.class_before = before;
    ev.class_after = before;
    ev.candidate = candidate;
    origin_emit(cfg, &ev);

    if (candidate) {
        is_new = IsGenuinelyNew(candidate, before);
        bear_candidate = Bear(machine->Inv, candidate);
    }

    if (candidate && is_new && bear_candidate) {
        after = IntegrateSameClass(before, candidate);

        ev.kind = "candidate_accepted";
        ev.class_before = before;
        ev.class_after = after;
        ev.candidate = candidate;
        ev.orthogonal = 0;
        ev.cap_gt_zero = -1;
        ev.cap_eq_zero = -1;
        ev.bear_current = -1;
        ev.bear_candidate = bear_candidate;
        ev.is_genuinely_new = is_new;
        ev.dis = -1;
        origin_emit(cfg, &ev);

        machine->A_n = after;
    } else {
        cap_pos = Cap_gt_zero(before);
        cap_zero = Cap_eq_zero(before);
        bear_current = Bear(machine->Inv, before);
        dis = Dis(machine->Inv);

        if (!cap_pos && cap_zero && bear_current && !dis)
            orthogonal = OrthogonalAdmit(before);

        after = BInv(machine->Inv, before);

        ev.kind = (cap_pos)
            ? "binv_stay"
            : "binv_extend";
        ev.class_before = before;
        ev.class_after = after;
        ev.candidate = candidate;
        ev.orthogonal = orthogonal;
        ev.cap_gt_zero = cap_pos;
        ev.cap_eq_zero = cap_zero;
        ev.bear_current = bear_current;
        ev.bear_candidate = bear_candidate;
        ev.is_genuinely_new = is_new;
        ev.dis = dis;
        origin_emit(cfg, &ev);

        machine->A_n = after;
    }

    ev.kind = "step_finished";
    ev.class_before = before;
    ev.class_after = machine->A_n;
    ev.candidate = candidate;
    ev.orthogonal = orthogonal;
    origin_emit(cfg, &ev);

    machine->step += 1;
    return machine->A_n;
}

void origin_run(origin_machine *machine, const origin_run_config *cfg)
{
    origin_event ev;
    size_t i;

    ev.kind = "run_started";
    ev.step = (uint64_t)machine->step;
    ev.inv = machine->Inv;
    ev.class_before = machine->A_n;
    ev.class_after = machine->A_n;
    ev.candidate = 0;
    ev.orthogonal = 0;
    ev.cap_gt_zero = -1;
    ev.cap_eq_zero = -1;
    ev.bear_current = -1;
    ev.bear_candidate = -1;
    ev.is_genuinely_new = -1;
    ev.dis = -1;
    origin_emit(cfg, &ev);

    for (i = 0; i < cfg->max_steps; ++i)
        origin_step_observed(machine, cfg);

    ev.kind = "run_finished";
    ev.step = (uint64_t)machine->step;
    ev.inv = machine->Inv;
    ev.class_before = machine->A_n;
    ev.class_after = machine->A_n;
    ev.candidate = 0;
    ev.orthogonal = 0;
    ev.cap_gt_zero = -1;
    ev.cap_eq_zero = -1;
    ev.bear_current = -1;
    ev.bear_candidate = -1;
    ev.is_genuinely_new = -1;
    ev.dis = -1;
    origin_emit(cfg, &ev);
}
