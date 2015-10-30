CC=gcc
CFLAGS=-shared -O2 -std=gnu99 -Wall -fPIC
LDLIBS=

all: libstats

libstats: statistics.c
	$(CC) $(CFLAGS) $(LDLIBS) $^ -o libstats.so.1

clean:
	rm libstats.so.1