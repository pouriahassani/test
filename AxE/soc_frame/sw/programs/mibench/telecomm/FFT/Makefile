SRC = main.c fftmisc.c fourierf.c ../../../../_libs/memmgr.c ../../../../_libs/newlib_stubs.c ../../../../_libs/file_io.c
LINKEDLIBS = -lm -lc
# Force full newlib (not nano) and enable float printf support
CFLAGS += -u _printf_float -Wno-implicit-int -Wno-old-style-definition -Wno-return-type
include ./Makefile_local

clean:
	rm -rf fft output* rv32* *.txt
