#include <math.h>
#include <stdio.h>

// Test PI as a compile-time constant vs runtime calculation
#define PI_HARDCODED 3.1415926535897932384626433832795

int test_atan_main(void)
{
  printf("=== TESTING ATAN FUNCTION ===\n");
  
  // Test atan with simple values first
  printf("Testing basic atan values:\n");
  double atan_0 = atan(0.0);
  double atan_1 = atan(1.0);
  
  printf("atan(0.0) = %.15f (expected: 0.0)\n", atan_0);
  printf("atan(1.0) = %.15f (expected: 0.785398163397448)\n", atan_1);
  
  // Test PI calculation vs hardcoded
  double pi_runtime = 4.0 * atan(1.0);
  printf("4*atan(1.0) = %.15f\n", pi_runtime);
  printf("PI hardcoded = %.15f\n", PI_HARDCODED);
  printf("Difference = %.15f\n", pi_runtime - PI_HARDCODED);
  
  // Test if the values are reasonable
  if (atan_0 < -0.001 || atan_0 > 0.001) {
    printf("ERROR: atan(0) is wrong: %.15f\n", atan_0);
  }
  if (atan_1 < 0.7 || atan_1 > 0.8) {
    printf("ERROR: atan(1) is wrong: %.15f\n", atan_1);
  }
  if (pi_runtime < 3.0 || pi_runtime > 3.2) {
    printf("ERROR: PI calculation is wrong: %.15f\n", pi_runtime);
  }
  
  // Test NaN detection
  if (atan_1 != atan_1) {
    printf("ERROR: atan(1.0) returned NaN!\n");
  }
  if (pi_runtime != pi_runtime) {
    printf("ERROR: PI calculation returned NaN!\n");
  }
  
  // Test other basic functions for comparison
  printf("\n=== TESTING OTHER MATH FUNCTIONS ===\n");
  double sqrt_4 = sqrt(4.0);
  double cos_0 = cos(0.0);
  
  printf("sqrt(4.0) = %.15f (expected: 2.0)\n", sqrt_4);
  printf("cos(0.0) = %.15f (expected: 1.0)\n", cos_0);
  
  if (sqrt_4 < 1.9 || sqrt_4 > 2.1) {
    printf("ERROR: sqrt(4) is wrong!\n");
  }
  if (cos_0 < 0.9 || cos_0 > 1.1) {
    printf("ERROR: cos(0) is wrong!\n");
  }
  
  return 0;
}