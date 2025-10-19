
#include "util.h"
#include "print.h"
void thomas(const int X, float x[restrict X],
            const float a[restrict X], const float b[restrict X],
            const float c[restrict X], float scratch[restrict X]) {
    /*
     solves Ax = d, where A is a tridiagonal matrix consisting of vectors a, b, c
     X = number of equations
     x[] = initially contains the input, d, and returns x. indexed from [0, ..., X - 1]
     a[] = subdiagonal, indexed from [1, ..., X - 1]
     b[] = main diagonal, indexed from [0, ..., X - 1]
     c[] = superdiagonal, indexed from [0, ..., X - 2]
     scratch[] = scratch space of length X, provided by caller, allowing a, b, c to be const
     not performed in this example: manual expensive common subexpression elimination
     */
    scratch[0] = c[0] / b[0];
    x[0] = x[0] / b[0];

    /* loop from 1 to X - 1 inclusive */
    for (int ix = 1; ix < X; ix++) {
        if (ix < X-1){
        scratch[ix] = c[ix] / (b[ix] - a[ix] * scratch[ix - 1]);
        }
        x[ix] = (x[ix] - a[ix] * x[ix - 1]) / (b[ix] - a[ix] * scratch[ix - 1]);
    }

    /* loop from X - 2 to 0 inclusive */
    for (int ix = X - 2; ix >= 0; ix--)
        x[ix] -= scratch[ix] * x[ix + 1];
}

float rand_float(float min, float max) {
    int val = rand();
    float d_val = (float)val;
    return min + (max - min) * (val / RAND_MAX);
}

void my_main(){
      const int X = 10;
    // float a[X], b[X], c[X], d[X], x[X], scratch[X];

    float x[X], scratch[X];


    srand(1); // Seed random number generator
// float a[10] = {
//     0.0f, 58145.5f, 20384.5f, 6758.5f, 96394.0f,
//     90634.0f, 68066.5f, 84395.5f, 42485.5f, 38864.5f
// };

//  float b[10] = {
//     1.0f, 109078.0f, 123130.0f, 80593.0f, 16714.0f,
//     99790.0f, 109504.0f, 19462.0f, 119200.0f, 86209.0f
// };

//  float c[10] = {
//     67829.5f, 37199.5f, 33434.5f, 86507.5f, 89224.0f,
//     85750.0f, 35576.5f, 86219.5f, 91210.0f, 0.0f
// };

//  float d[10] = {
//     662470.0f, 337810.0f, 1106070.0f, 418750.0f, 134350.0f,
//     436810.0f, 41910.0f, 588850.0f, 870690.0f, 854750.0f
// };
float a[10] = {0.5,     -0.8,    -0.8,    -1.1,    -0.6,    -1.1,    -0.8,    -1.8,    -0.7,    -1.2};
float b[10] ={ 3.5 ,    3.7,     1.8,     2.1,     2.9,     1.0,     1.5,     4.0,     2.8     ,2.5};
float c[10] = { -1.4 ,   -1.7,    -1.2,    -1.2,    -0.9,    -1.6,    -1.4,    -1.7,    -1.6,    0.5};
float d[10]={ 5.7   ,  -3.3 ,   -0.5 ,   9.0    , -7.2   , -7.3  ,  -7.4   , 0.3     ,2.8     ,9.5};
    // Generate random a, b, c, d
    for (int i = 0; i < X; i++) {
        // if (i > 0) {
        //     a[i] = rand_float(-2.0, -0.5);  // Subdiagonal (usually negative)
        // } else {
        //     a[i] = 0.0; // No subdiagonal for first element
        // }

        // b[i] = rand_float(1.0, 4.0); // Main diagonal (positive)

        // if (i < X - 1) {
        //     c[i] = rand_float(-2.0, -0.5);  // Superdiagonal (usually negative)
        // } else {
        //     c[i] = 0.0; // No superdiagonal for last element
        // }

        // d[i] = rand_float(-10.0, 10.0);  // Right-hand side (RHS)
        x[i] = d[i]; // Initialize x with RHS for thomas()
    }

    // Print the generated system
    display_print(0,0,"Generated system:\n");
    display_print(0,0,"a:\t");
    for (int i = 0; i < X; i++)     {display_print(0,0,"\n"); display_print_float(a[i]);}
    display_print(0,0,"\nb:\t");
    for (int i = 0; i < X; i++) {display_print(0,0,"\n"); display_print_float(b[i]);}
    display_print(0,0,"\nc:\t");
    for (int i = 0; i < X; i++) {display_print(0,0,"\n"); display_print_float(c[i]);}
    display_print(0,0,"\nd:\t");
    for (int i = 0; i < X; i++) {display_print(0,0,"\n"); display_print_float(d[i]);}
    display_print(0,0,"\n\n");

    // Solve the system
    thomas(X, x, a, b, c, scratch);

    // Print the solution
    display_print(0,0,"Solution x:\n");
    for (int i = 0; i < X; i++) {
        display_print(0,0,"\nx[");
        display_print(2,i,"");
        display_print(0,0,"] = ");
        display_print_float(x[i]);
    }  
        display_print(0,0,"\n");

}