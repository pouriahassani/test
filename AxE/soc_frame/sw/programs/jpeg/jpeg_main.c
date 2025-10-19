#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Debug macro for progress tracking
#ifdef DEBUG_JPEG
#define JPEG_DEBUG(fmt, ...) printf("[JPEG_DEBUG] " fmt "\n", ##__VA_ARGS__)
#else
#define JPEG_DEBUG(fmt, ...) do {} while(0)
#endif

// External main functions from JPEG applications
extern int cjpeg_main(int argc, char **argv);
extern int djpeg_main(int argc, char **argv);

// Test parameters based on runme_small.sh
static char* encode_argv[] = {
    "cjpeg",
    "-dct", "float",
    "-progressive",
    "-opt", 
    "-outfile", "/home/axe/workspace/soc_frame/sw/programs/jpeg/output_small_encode.jpeg",
    "/home/axe/workspace/soc_frame/sw/programs/jpeg/input_small.ppm"
};

static char* decode_argv[] = {
    "djpeg",
    "-dct", "float",
    "-ppm",
    "-outfile", "output_small_decode.ppm", 
    "input_small.jpg"
};

int my_main(void) {
    int result;
    
    printf("AxE JPEG Test Application\n");
    printf("========================\n");
    
    JPEG_DEBUG("Starting AxE JPEG test application");
    JPEG_DEBUG("System initialized, stack pointer configured");
    
    JPEG_DEBUG("Preparing JPEG encoding test");
    JPEG_DEBUG("Encode parameters: %s %s %s %s %s %s %s %s", 
               encode_argv[0], encode_argv[1], encode_argv[2], encode_argv[3],
               encode_argv[4], encode_argv[5], encode_argv[6], encode_argv[7]);
    
    printf("Testing JPEG encoding (cjpeg)...\n");
    JPEG_DEBUG("Calling cjpeg_main with %d arguments", 8);
    
    result = cjpeg_main(8, encode_argv);
    
    JPEG_DEBUG("cjpeg_main returned with code %d", result);
    if (result != 0) {
        printf("JPEG encoding failed with code %d\n", result);
        JPEG_DEBUG("JPEG encoding FAILED - aborting");
        return result;
    }
    printf("JPEG encoding completed successfully\n");
    JPEG_DEBUG("JPEG encoding SUCCESSFUL");
    
    JPEG_DEBUG("Preparing JPEG decoding test");
    JPEG_DEBUG("Decode parameters: %s %s %s %s %s %s", 
               decode_argv[0], decode_argv[1], decode_argv[2], 
               decode_argv[3], decode_argv[4], decode_argv[5]);
    
    printf("\nTesting JPEG decoding (djpeg)...\n");
    JPEG_DEBUG("Calling djpeg_main with %d arguments", 6);
    
    result = djpeg_main(6, decode_argv);
    
    JPEG_DEBUG("djpeg_main returned with code %d", result);
    if (result != 0) {
        printf("JPEG decoding failed with code %d\n", result);
        JPEG_DEBUG("JPEG decoding FAILED - aborting");
        return result;
    }
    printf("JPEG decoding completed successfully\n");
    JPEG_DEBUG("JPEG decoding SUCCESSFUL");
    
    printf("\nAll JPEG tests completed successfully!\n");
    JPEG_DEBUG("All JPEG tests completed successfully - application ending");
    return 0;
}