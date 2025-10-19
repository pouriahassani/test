SRC = jpeg_main.c cjpeg.c djpeg.c cdjpeg.c jcapimin.c jcapistd.c jccoefct.c jccolor.c jcdctmgr.c jchuff.c jcinit.c jcmainct.c jcmarker.c jcmaster.c jcomapi.c jcparam.c jcphuff.c jcprepct.c jcsample.c jctrans.c jdapimin.c jdapistd.c jdatadst.c jdatasrc.c jdcoefct.c jdcolor.c jddctmgr.c jdhuff.c jdinput.c jdmainct.c jdmarker.c jdmaster.c jdmerge.c jdphuff.c jdpostct.c jdsample.c jdtrans.c jerror.c jfdctflt.c jfdctfst.c jfdctint.c jidctflt.c jidctfst.c jidctint.c jidctred.c jmemmgr.c jmemnobs.c jquant1.c jquant2.c jutils.c rdcolmap.c rdppm.c wrppm.c rdgif.c wrgif.c rdtarga.c wrtarga.c rdbmp.c wrbmp.c rdrle.c wrrle.c rdswitch.c ../../_libs/memmgr.c ../../_libs/newlib_stubs.c ../../_libs/file_io.c
LINKEDLIBS = -lm
# Force full newlib and enable float printf support
CFLAGS += -u _printf_float -DJPEG_INTERNALS -DJPEG_CJPEG_DJPEG -DDEBUG_JPEG -Wno-implicit-int -Wno-old-style-definition -Wno-return-type
include ./Makefile_local

clean:
	rm -rf jpeg output* rv32* *.txt