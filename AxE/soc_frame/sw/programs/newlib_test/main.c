#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "newlib_stubs.h"
#include "memmgr.h"

int my_main() {
    // Initialize memory manager
    memmgr_init();
    FILE* file = fopen("dummy.txt", "w"); // Dummy call to ensure file I/O is initialized

    fprintf(file, "%s %f","Dummy file to initialize file I/O\n",sin(0.5));
    fclose(file);
    // Test math functions (from newlib)
    float x  = 0.5f;
    printf("\n=== Math Library Test ===\n");
    printf("sin(1.0) = %.4f\n",sin(1.0));
    printf("cos(0.0) = %.4f\n", cos(0.0));
    printf("sqrt(16.0) = %.4f\n", sqrt(16.0));
    // Test printf functionality
    display_print(0,0,"=== AxE Newlib Test ===\n");
    printf("Testing printf with integer: %d\n", 42);
    printf("Testing printf with float: %.2f\n", 3.14159);
    printf("Testing printf with string: %s\n", "Hello AxE!");
    
    // Test string functions
    char test_str[] = "Testing string functions";
    printf("String length: %d\n", strlen(test_str));
    
    char copy_str[50];
    strcpy(copy_str, "Copied string");
    printf("Copied string: %s\n", copy_str);
    
    // Test string comparison
    if (strcmp("test", "test") == 0) {
        printf("String comparison works!\n");
    }
    
    // Test string to number conversion
    int num = atoi("123");
    printf("atoi('123') = %d\n", num);
    
    // Test dynamic memory allocation
    printf("\n=== Memory Allocation Test ===\n");
    int *array = (int*)malloc(10 * sizeof(int));
    if (array != NULL) {
        printf("Successfully allocated array of 10 integers\n");
        
        // Fill array with values
        for (int i = 0; i < 10; i++) {
            array[i] = i * i;
        }
        
        // Print array values
        printf("Array values: ");
        for (int i = 0; i < 10; i++) {
            printf("%d ", array[i]);
        }
        printf("\n");
        
        free(array);
        printf("Array freed successfully\n");
    } else {
        printf("Memory allocation failed!\n");
    }
    
    // Test calloc
    float *float_array = (float*)calloc(5, sizeof(float));
    if (float_array != NULL) {
        printf("Calloc successful, verifying zero initialization: ");
        int all_zero = 1;
        for (int i = 0; i < 5; i++) {
            if (float_array[i] != 0.0f) {
                all_zero = 0;
                break;
            }
        }
        printf("%s\n", all_zero ? "PASS" : "FAIL");
        free(float_array);
    }
    
    // Test random numbers
    printf("\n=== Random Number Test ===\n");
    srand(42);
    printf("Random numbers: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", rand() % 100);
    }
    printf("\n");
    

    
    printf("\n=== All Tests Complete ===\n");
    
    return 0;
}