#include <stdio.h>
#include <stdlib.h>

#include "origin_runner.h"
#include "origin_observer.h"

extern void *InitialInvariant(void);
extern void *InitialClass(void);

static size_t parse_steps(const char *s)
{
    char *end = 0;
    unsigned long long v = strtoull(s, &end, 10);
    if (!s || !*s || (end && *end)) return 0;
    return (size_t)v;
}

int main(int argc, char **argv)
{
    origin_machine machine;
    origin_run_config cfg;
    origin_ndjson_writer writer;
    FILE *fp;
    size_t steps;

    if (argc != 3) {
        fprintf(stderr, "usage: %s <steps> <out.ndjson>\n", argv[0]);
        return 1;
    }

    steps = parse_steps(argv[1]);
    if (steps == 0) {
        fprintf(stderr, "invalid step count: %s\n", argv[1]);
        return 1;
    }

    fp = fopen(argv[2], "w");
    if (!fp) {
        perror("fopen");
        return 1;
    }

    writer.fp = fp;

    machine.Inv = InitialInvariant();
    machine.A_n = InitialClass();
    machine.step = 0;

    cfg.max_steps = steps;
    cfg.sink = origin_ndjson_sink;
    cfg.sink_user = &writer;

    origin_run(&machine, &cfg);

    fclose(fp);
    return 0;
}
