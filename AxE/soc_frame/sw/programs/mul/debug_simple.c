#include <math.h>
#include <stdio.h>

void debug_atan_simple() {
    printf("Testing atan function step by step\n");
    
    // Test 1: Simple values first
    double zero = 0.0;
    double one = 1.0;
    double two = 2.0;
    
    printf("Constants: zero=%f, one=%f, two=%f\n", zero, one, two);
    
    // Test 2: Test atan with 0 (should be 0)
    double atan_0 = atan(zero);
    printf("atan(0) = %f\n", atan_0);
    
    // Test 3: Test atan with 1 (should be ~0.785)
    double atan_1 = atan(one);
    printf("atan(1) = %f\n", atan_1);
    
    // Test 4: Multiply by 4
    double pi_calc = 4.0 * atan_1;
    printf("4 * atan(1) = %f\n", pi_calc);
    
    // Test 5: Check if values are NaN
    if (atan_0 != atan_0) printf("ERROR: atan(0) is NaN\n");
    if (atan_1 != atan_1) printf("ERROR: atan(1) is NaN\n");
    if (pi_calc != pi_calc) printf("ERROR: pi_calc is NaN\n");
    
    // Test 6: Check ranges
    if (atan_0 < -0.1 || atan_0 > 0.1) printf("ERROR: atan(0) out of range\n");
    if (atan_1 < 0.7 || atan_1 > 0.8) printf("ERROR: atan(1) out of range\n");
}