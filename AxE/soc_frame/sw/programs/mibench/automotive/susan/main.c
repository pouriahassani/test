#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../../../_libs/newlib_stubs.h"
#include "../../../../_libs/memmgr.h"

// Forward declaration of original SUSAN main function
int susan_main(int argc, char *argv[]);

int my_main() {
    // Initialize memory manager
    memmgr_init();
    
    printf("=== AxE SUSAN Image Processing Test ===\n");
    
    // Hard-coded parameters from runme_small.sh:
    // susan input_small.pgm output_small.smoothing.pgm -s
    // susan input_small.pgm output_small.edges.pgm -e  
    // susan input_small.pgm output_small.corners.pgm -c
    
    // Test 1: Smoothing
    printf("Running SUSAN smoothing...\n");
    char *argv_smooth[] = {"susan", "/home/axe/workspace/soc_frame/sw/programs/mibench/automotive/susan/input_small.pgm", "/home/axe/workspace/soc_frame/sw/programs/mibench/automotive/susan/output_small.smoothing.pgm", "-s"};
    int result1 = susan_main(4, argv_smooth);
    printf("Smoothing result: %d\n", result1);
    
    // Test 2: Edge detection
    printf("Running SUSAN edge detection...\n");
    char *argv_edges[] = {"susan", "/home/axe/workspace/soc_frame/sw/programs/mibench/automotive/susan/input_small.pgm", "/home/axe/workspace/soc_frame/sw/programs/mibench/automotive/susan/output_small.edges.pgm", "-e"};
    int result2 = susan_main(4, argv_edges);
    printf("Edge detection result: %d\n", result2);
    
    // Test 3: Corner detection
    printf("Running SUSAN corner detection...\n");
    char *argv_corners[] = {"susan", "/home/axe/workspace/soc_frame/sw/programs/mibench/automotive/susan/input_small.pgm", "/home/axe/workspace/soc_frame/sw/programs/mibench/automotive/susan/output_small.corners.pgm", "-c"};
    int result3 = susan_main(4, argv_corners);
    printf("Corner detection result: %d\n", result3);
    
    printf("=== SUSAN Tests Complete ===\n");
    
    return 0;
}