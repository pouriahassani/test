#include "snipmath.h"
#include <math.h>
#include <stdio.h>

/* Debug version to test cubic solver step by step */

int debug_main(void)
{
  double  a1 = 1.0, b1 = -10.5, c1 = 32.0, d1 = -30.0;
  double  x[3];
  int     solutions;
  
  printf("=== DEBUG CUBIC SOLVER ===\n");
  printf("Input: a=%.6f, b=%.6f, c=%.6f, d=%.6f\n", a1, b1, c1, d1);
  
  // Test PI calculation first
  printf("Testing PI calculation:\n");
  printf("atan(1) = %.10f\n", atan(1.0));
  printf("4*atan(1) = %.10f\n", 4.0*atan(1.0));
  printf("PI from header = %.10f\n", PI);
  
  // Manual cubic calculation step by step
  long double    a1_norm = b1/a1, a2_norm = c1/a1, a3_norm = d1/a1;
  printf("Normalized coefficients: a1=%.6Lf, a2=%.6Lf, a3=%.6Lf\n", a1_norm, a2_norm, a3_norm);
  
  long double    Q = (a1_norm*a1_norm - 3.0*a2_norm)/9.0;
  long double    R = (2.0*a1_norm*a1_norm*a1_norm - 9.0*a1_norm*a2_norm + 27.0*a3_norm)/54.0;
  printf("Q = %.10Lf\n", Q);
  printf("R = %.10Lf\n", R);
  
  double    R2_Q3 = R*R - Q*Q*Q;
  printf("R^2 - Q^3 = %.10f\n", R2_Q3);
  
  if (R2_Q3 <= 0) {
    printf("Taking 3-solution path\n");
    double Q_cubed = Q*Q*Q;
    printf("Q^3 = %.10f\n", Q_cubed);
    
    if (Q_cubed <= 0) {
      printf("ERROR: Q^3 <= 0, cannot take sqrt\n");
      return -1;
    }
    
    double sqrt_Q3 = sqrt(Q_cubed);
    printf("sqrt(Q^3) = %.10f\n", sqrt_Q3);
    
    if (sqrt_Q3 == 0.0) {
      printf("ERROR: sqrt(Q^3) == 0, division by zero in acos\n");
      return -1;
    }
    
    double acos_arg = R/sqrt_Q3;
    printf("acos argument = R/sqrt(Q^3) = %.10f\n", acos_arg);
    
    if (acos_arg < -1.0 || acos_arg > 1.0) {
      printf("ERROR: acos argument out of range [-1,1]\n");
      return -1;
    }
    
    double theta = acos(acos_arg);
    printf("theta = acos(%.10f) = %.10f\n", acos_arg, theta);
    
    // Calculate solutions
    solutions = 3;
    double sqrt_Q = sqrt(Q);
    printf("sqrt(Q) = %.10f\n", sqrt_Q);
    
    x[0] = -2.0*sqrt_Q*cos(theta/3.0) - a1_norm/3.0;
    x[1] = -2.0*sqrt_Q*cos((theta+2.0*PI)/3.0) - a1_norm/3.0;
    x[2] = -2.0*sqrt_Q*cos((theta+4.0*PI)/3.0) - a1_norm/3.0;
    
    printf("Solutions (manual calc):\n");
    printf("  x[0] = %.10f\n", x[0]);
    printf("  x[1] = %.10f\n", x[1]); 
    printf("  x[2] = %.10f\n", x[2]);
  } else {
    printf("Taking 1-solution path\n");
    solutions = 1;
    // Calculate the single solution...
  }
  
  // Now test original function
  printf("\n=== TESTING ORIGINAL FUNCTION ===\n");
  SolveCubic(a1, b1, c1, d1, &solutions, x);
  printf("Original function results:\n");
  printf("Solutions: %d\n", solutions);
  for(int i=0; i<solutions; i++) {
    printf("  x[%d] = %.10f\n", i, x[i]);
  }
  
  return 0;
}