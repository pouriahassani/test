//----------------------------------------------------------------
// Newlib Stubs Header for AxE System
//
// This header provides declarations for newlib syscall stubs
// and essential system functions for the AxE embedded platform.
//----------------------------------------------------------------

#ifndef NEWLIB_STUBS_H
#define NEWLIB_STUBS_H

#include <stddef.h>
#include <stdint.h>
#include <sys/stat.h>
#include <sys/times.h>
#include <time.h>

//----------------------------------------------------------------
// AxE Display System Functions
//----------------------------------------------------------------

// Low-level display functions (hardware interface)
void checkprint_str(int rs1, int rs2);
void checkprint_float(int rs1);
void checkprint_int(int rs1);

// High-level display functions
void display_print(int is_digit, int value, char* str);
void display_print_float(float value);

//----------------------------------------------------------------
// System Control
//----------------------------------------------------------------

// Program termination
void signal_fin(void);

//----------------------------------------------------------------
// Memory Management 
//----------------------------------------------------------------

// Standard C library memory functions
void *malloc(size_t size);
void free(void *ptr);
void *calloc(size_t num, size_t size);

// Memory utility functions
void *memcpy(void *dest, const void *src, size_t n);
void *memset(void *dest, int c, size_t n);
int memcmp(const void *vl, const void *vr, size_t n);

//----------------------------------------------------------------
// Random Number Generation
//----------------------------------------------------------------

void srand(unsigned int seed);
int rand(void);

//----------------------------------------------------------------
// Newlib Syscall Stubs
// (These are automatically called by newlib - don't call directly)
//----------------------------------------------------------------

// Process management
void _exit(int status);
int _getpid(void);
int _kill(int pid, int sig);
int _fork(void);
int _execve(const char *name, char * const *argv, char * const *env);
int _wait(int *status);

// File operations
int _open(const char *name, int flags, int mode);
int _close(int file);
int _read(int file, char *ptr, int len);
int _write(int file, char *ptr, int len);
int _lseek(int file, int ptr, int dir);

// File status
int _fstat(int file, struct stat *st);
int _stat(const char *file, struct stat *st);
int _isatty(int file);

// File system operations
int _link(const char *old, const char *new);
int _unlink(const char *name);

// Memory management
void *_sbrk(int incr);

// Time functions
clock_t _times(struct tms *buf);

//----------------------------------------------------------------
// Usage Notes
//----------------------------------------------------------------

/*
 * To use this newlib stubs system in your AxE application:
 * 
 * 1. Include this header: #include "newlib_stubs.h"
 * 2. Link with newlib_stubs.c instead of util.c
 * 3. Call memmgr_init() before using malloc/free
 * 4. Use standard C library functions:
 *    - printf() instead of display_print()
 *    - malloc()/free() instead of memmgr_alloc()/memmgr_free()
 *    - Standard string functions: strlen(), strcmp(), etc.
 *    - Math functions: sin(), cos(), sqrt(), etc.
 * 
 * Example:
 *   #include <stdio.h>
 *   #include <stdlib.h>
 *   #include <string.h>
 *   #include <math.h>
 *   #include "newlib_stubs.h"
 *   
 *   int main() {
 *       memmgr_init();
 *       printf("Hello World!\n");
 *       float *data = malloc(100 * sizeof(float));
 *       printf("Allocated %d bytes\n", 100 * sizeof(float));
 *       free(data);
 *       return 0;
 *   }
 */

#endif // NEWLIB_STUBS_H