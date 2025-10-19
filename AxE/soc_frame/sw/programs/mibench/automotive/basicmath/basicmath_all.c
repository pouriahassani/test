#include <math.h>
#include <stdlib.h>
#include <stdio.h>

/* PI constant */
#define PI (4*atan(1))

/* Helper macros for integer square root */
#define HIWORD(x)  ((unsigned short)((x) >> 16))
#define LOWORD(x)  ((unsigned short)(x))

/* Integer square root structures and functions */
struct int_sqrt
{
      unsigned short sqrt;
      unsigned short frac;
};

/* Cubic solver */
void SolveCubic(double  a,
                double  b,
                double  c,
                double  d,
                int    *solutions,
                double *x)
{
      double    a1 = b/a, a2 = c/a, a3 = d/a;
      double    Q = (a1*a1 - 3.0*a2)/9.0;
      double    R = (2.0*a1*a1*a1 - 9.0*a1*a2 + 27.0*a3)/54.0;
      double    R2_Q3 = R*R - Q*Q*Q;

      double    theta;

      if (R2_Q3 <= 0)
      {
            *solutions = 3;
            theta = acos(R/sqrt(Q*Q*Q));
            x[0] = -2.0*sqrt(Q)*cos(theta/3.0) - a1/3.0;
            x[1] = -2.0*sqrt(Q)*cos((theta+2.0*PI)/3.0) - a1/3.0;
            x[2] = -2.0*sqrt(Q)*cos((theta+4.0*PI)/3.0) - a1/3.0;
      }
      else
      {
            *solutions = 1;
            x[0] = pow(sqrt(R2_Q3)+fabs(R), 1/3.0);
            x[0] += Q/x[0];
            x[0] *= (R < 0.0) ? 1 : -1;
            x[0] -= a1/3.0;
      }
}

/* Degree to radian conversion */
double deg2rad(double deg)
{
      return (deg * PI / 180.0);
}

/* Radian to degree conversion */
double rad2deg(double rad)
{
      return (rad * 180.0 / PI);
}

/* Integer square root */
void usqrt(unsigned long x, struct int_sqrt *q)
{
      unsigned long a = 0L;                   /* Accumulator      */
      unsigned long r = 0L;                   /* Remainder        */
      unsigned long e = 0L;                   /* Trial product    */

      int i;

      for (i = 0; i < 16; i++)   /* NOTE 1 */
      {
            r = (r << 2) + HIWORD(x); x <<= 2; /* NOTE 2 */
            a <<= 1;                            /* NOTE 3 */
            e = (a << 1) + 1;
            if (r >= e)
            {
                  r -= e;
                  a++;
            }
      }
      for (i = 0; i < 16; i++)   /* NOTE 1 */
      {
            r = (r << 2) + HIWORD(x); x <<= 2; /* NOTE 2 */
            a <<= 1;                            /* NOTE 3 */
            e = (a << 1) + 1;
            if (r >= e)
            {
                  r -= e;
                  a++;
            }
      }
      q->sqrt = (unsigned short)a;
      q->frac = (unsigned short)r;
}

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

  /* solve some cubic functions */
  printf("********* CUBIC FUNCTIONS ***********\n");
  printf("Testing first cubic equation (should get 3 solutions: 2, 6 & 2.5)\n");
  printf("Equation: x^3 - 10.5x^2 + 32x - 30 = 0\n");
  
  /* should get 3 solutions: 2, 6 & 2.5   */
  SolveCubic(a1, b1, c1, d1, &solutions, x);  
  printf("Main: Solutions count = %d\n", solutions);
  printf("Main: Solutions (as int*1000):");
  for(i=0;i<solutions;i++)
    printf(" %d",(int)(x[i]*1000));
  printf("\n\n");
  
  printf("Testing basic math functions (as int*1000):\n");
  printf("sqrt(4.0) = %d\n", (int)(sqrt(4.0)*1000));
  printf("cos(0.0) = %d\n", (int)(cos(0.0)*1000));
  printf("acos(1.0) = %d\n", (int)(acos(1.0)*1000));
  printf("PI = %d\n", (int)(PI*1000));
  
  return 0;
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
    printf("%3.0f degrees = %d milliradians\n", X, (int)(deg2rad(X)*1000));
  puts("");
  for (X = 0.0; X <= (2 * PI + 1e-6); X += (PI / 180))
    printf("%d milliradians = %3.0f degrees\n", (int)(X*1000), rad2deg(X));
  
  
  return 0;
}