SRC = ./../../_libs/memmgr.c  ./../../_libs/newlib_stubs.c ./../../_libs/file_io.c
LINKEDLIBS = -lm -lc
# Force full newlib (not nano) and enable float printf support
CFLAGS +=  -u _printf_float
LINKEDLIBS += 
include ../Makefile_nostart
