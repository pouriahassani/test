SRC = basicmath_small.c rad2deg.c  cubic.c   isqrt.c ../../../../_libs/memmgr.c ../../../../_libs/newlib_stubs.c ../../../../_libs/file_io.c
LINKEDLIBS = -lm
# Force full newlib (not nano) and enable float printf support
CFLAGS += -u _printf_float -Wno-implicit-int -Wno-old-style-definition -Wno-return-type
include ./Makefile_local

clean:
	rm -rf basicmath output* rv32* *.txt
