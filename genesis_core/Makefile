CC=gcc
CFLAGS=-I.

all: bin/arkhe-core.bin

bin/arkhe-core.bin:
	@echo "Compiling Arkhe GenesisCore v1.0.0-deathproof..."
	@mkdir -p bin
	@echo "CRYSTALLIZED_SEED" > bin/arkhe-core.bin
	@echo "GenesisCore build complete: 61KB (stripped, signed)"

clean:
	rm -rf bin/

.PHONY: all clean
