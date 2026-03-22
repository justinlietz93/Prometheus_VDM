# Origin runner / witness shell

This layer sits **outside** `BInv.c`.

It does three things only:

1. run for a predetermined number of steps
2. emit sparse append-only events as NDJSON
3. let a later renderer replay those events without touching the law

## Files

- `origin_observer.h/.c` — append-only NDJSON sink
- `origin_runner.h/.c` — observed outer driver around `BInv`
- `origin_main.c` — CLI entrypoint

## What the runner observes

Each step emits sparse events such as:

- `run_started`
- `step_started`
- `candidate_produced`
- `candidate_accepted`
- `binv_stay`
- `binv_extend`
- `step_finished`
- `run_finished`

## Required external symbols

You still need to provide the witness semantics and initial conditions somewhere else:

```c
void *InitialInvariant(void);
void *InitialClass(void);

void *BInv(void *Inv, void *A_n);

void *ArticulateSameClass(void *Inv, void *A_n);
int   IsGenuinelyNew(void *candidate, void *A_n);
int   Bear(void *Inv, void *A_n);
int   Dis(void *Inv);
int   Cap_gt_zero(void *A_n);
int   Cap_eq_zero(void *A_n);
void *OrthogonalAdmit(void *A_n);
void *IntegrateSameClass(void *A_n, void *candidate);
```

## Build shape

A typical compile would look like:

```bash
gcc -std=c11 -O2 \
  BInv.c \
  origin_observer.c \
  origin_runner.c \
  origin_main.c \
  your_witnesses.c \
  -o origin_run
```

## Run shape

```bash
./origin_run 100000 out.ndjson
```

That gives you an append-only event log you can later replay in any renderer.
