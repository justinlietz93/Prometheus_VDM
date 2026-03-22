CC=gcc
CFLAGS=-std=c11 -O2 -Iinclude

SRC=\
	src/core/BInv.c \
	src/core/OriginStep.c \
	src/core/origin_runner.c \
	src/observe/origin_observer.c \
	src/observe/origin_main.c \
	src/witnesses/origin_witnesses.c

all: origin_run

origin_run:
	$(CC) $(CFLAGS) $(SRC) -o origin_run

clean:
	rm -f origin_run
