#include "snipmath.h"
#include <math.h>
#include <stdio.h>

/* The printf's may be removed to isolate just the math calculations */

int my_main(void)
{
  double  a1 = 1.0, b1 = -10.5, c1 = 32.0, d1 = -30.0;
  double  a2 = 1.0, b2 = -4.5, c2 = 17.0, d2 = -30.0;
  double  a3 = 1.0, b3 = -3.5, c3 = 22.0, d3 = -31.0;
  double  a4 = 1.0, b4 = -13.7, c4 = 1.0, d4 = -35.0;
  double  x[3];
  double X;
  int     solutions;
  int i;
  unsigned long l = 0x3fed0169L;
  struct int_sqrt q;
  long n = 0;
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
  printf("\nvalude of pi %f\n",PI);
  /* solve soem cubic functions */
  printf("********* CUBIC FUNCTIONS ***********\n");
  printf("Testing first cubic equation (should get 3 solutions: 2, 6 & 2.5)\n");
  printf("Equation: x^3 - 10.5x^2 + 32x - 30 = 0\n");
  
  /* should get 3 solutions: 2, 6 & 2.5   */
  SolveCubic(a1, b1, c1, d1, &solutions, x);  
  printf("Main: Solutions count = %d\n", solutions);
  printf("Main: Solutions (as int*1000):");
  for(i=0;i<solutions;i++)
    printf(" %f",x[i]);
  printf("\n\n");
  
  printf("Testing basic math functions:\n");
  printf("sqrt(4.0) = %.6f\n", sqrt(4.0));
  printf("cos(0.0) = %.6f\n", cos(0.0));
  printf("acos(1.0) = %.6f\n", acos(1.0));
  printf("PI = %.10f\n", PI);
  

  /* Now solve some random equations */
  for(a1=1;a1<10;a1++) {
    for(b1=10;b1>0;b1--) {
      for(c1=5;c1<15;c1+=0.5) {
	for(d1=-1;d1>-11;d1--) {
	  SolveCubic(a1, b1, c1, d1, &solutions, x);  
	  printf("Solutions:");
	  for(i=0;i<solutions;i++)
	    printf(" %f",x[i]);
	  printf("\n");
	}
      }
    }
  }
  
  printf("********* INTEGER SQR ROOTS ***********\n");
  /* perform some integer square roots */
  for (i = 0; i < 1001; ++i)
    {
      usqrt(i, &q);
			// remainder differs on some machines
     // printf("sqrt(%3d) = %2d, remainder = %2d\n",
     printf("sqrt(%3d) = %2d\n",
	     i, q.sqrt);
    }
  usqrt(l, &q);
  //printf("\nsqrt(%lX) = %X, remainder = %X\n", l, q.sqrt, q.frac);
  printf("\nsqrt(%lX) = %X\n", l, q.sqrt);


  printf("********* ANGLE CONVERSION ***********\n");
  /* convert some rads to degrees */
  for (X = 0.0; X <= 360.0; X += 1.0)
    printf("%3.0f degrees = %.12f radians\n", X, deg2rad(X));
  puts("");
  for (X = 0.0; X <= (2 * PI + 1e-6); X += (PI / 180))
    printf("%.12f radians = %3.0f degrees\n", X, rad2deg(X));
  
  
  return 0;
}
