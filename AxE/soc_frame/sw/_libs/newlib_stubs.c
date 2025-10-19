//----------------------------------------------------------------
// Newlib Syscall Stubs for AxE System
// 
// This file implements the 17 syscall stubs required by newlib
// to provide standard C library functionality (printf, malloc, etc.)
// on the AxE embedded system.
//----------------------------------------------------------------

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/fcntl.h>
#include <sys/times.h>
#include <sys/errno.h>
#include <sys/time.h>
#include <sys/reent.h>
#include <stdio.h>
#include <errno.h>
#include <stdint.h>
#include <stdarg.h>

// AxE system includes
#include "file_io.h"
#include "memmgr.h"

// AxE system constants
#define FINISHED ( 0x00FFFFFC )

// Ensure O_ACCMODE is defined (mask to extract access mode from flags)
#ifndef O_ACCMODE
#define O_ACCMODE 0x0003
#endif

//----------------------------------------------------------------
// Essential AxE Display Functions (imported from util.c)
//----------------------------------------------------------------


__attribute__((noinline))
void checkprint_str(int rs1, int rs2)
{
    asm __volatile__ (".word 0x0EA5850B\n");
}


__attribute__((noinline))
void checkprint_float(int rs1)
{
    asm __volatile__ (".word 0x0EA5950B\n");//0ea5950b
}

__attribute__((noinline))
void checkprint_int(int rs1)
{
    asm __volatile__ (".word 0x0EA5A50B\n");//0ea5a50b
}

void display_print(int is_digit,int value,char* str){
    int rs1 = 0;
    int rs2 = 0;
    if(is_digit == 2){
        checkprint_int(value);
    }
    else if(is_digit == 1){
        checkprint_float((float)value);
    }
    else{
        int i = 0;
        int j = 0;
        while(str[i] != '\0'){
            
            if(j == 0){
                rs1 = str[i];
            }
            else{
                if(j == 8){
                    checkprint_str(rs1,rs2);
                    rs1 = 0;
                    rs2 = 0;
                    j = -1;
                    i-=1;
                }
                else{
                    if(j < 4){
                        rs1 <<= 8;
                        rs1 += str[i];
                        // printf("\n%c",rs1);
                    }
                    else{
                        if(j==4)
                            rs2 = str[i];
                        else{
                            rs2 <<= 8;
                            rs2 += str[i];
                        }
                        // printf("\n%d %d %c",i,j,rs2);
                    }
                }

            }
            j+=1;
            i+=1;
        }
        if(j!=0)
            checkprint_str(rs1,rs2);
    }
}

void display_print_float(float value) {
    asm __volatile__ (".word 0x0EA5950B\n");//0ea5a50b
}

//----------------------------------------------------------------
// Program termination signal
//----------------------------------------------------------------
void signal_fin() {
    *((volatile int*)FINISHED) = FINISHED;
}

//----------------------------------------------------------------
// Newlib Syscall Stubs Implementation
//----------------------------------------------------------------

// Environment pointer (not used in embedded systems)
char *__env[1] = { 0 };
char **environ = __env;

// 1. _exit - Program termination
void _exit(int status) {
    display_print(0, 0, "Program exiting with status: ");
    display_print(2, status, "");
    display_print(0, 0, "\n");
    signal_fin();
    while(1); // Halt execution
}

// 2. _write - Write to file descriptor
int _write(int file, char *ptr, int len) {
    if (file == 1 || file == 2) { // STDOUT or STDERR
        // Console output via AxE display system
        // Write in chunks to avoid stack overflow with large writes
        static char buffer[256];
        int written = 0;
        
        while (written < len) {
            int chunk_size = (len - written) > 255 ? 255 : (len - written);
            memcpy(buffer, ptr + written, chunk_size);
            buffer[chunk_size] = '\0';
            display_print(0, 0, buffer);
            written += chunk_size;
        }
        return len;
    } else if (file >= 3) {
        // File output via AxE file I/O system
        return axe_file_write(file, ptr, len);
    }
    errno = EBADF;
    return -1;
}

// 3. _read - Read from file descriptor
int _read(int file, char *ptr, int len) {
    if (file == 0) { // STDIN
        // For embedded systems, we typically don't support console input
        errno = ENOTSUP;
        return -1;
    } else if (file >= 3) {
        // File input via AxE file I/O system
        return axe_file_read(file, ptr, len);
    }
    errno = EBADF;
    return -1;
}

// 4. _open - Open file
int _open(const char *name, int flags, int mode) {
    // Convert POSIX flags to AxE file modes
    int axe_mode = 0;
    
    // Extract access mode from flags (O_RDONLY=0, O_WRONLY=1, O_RDWR=2)
    int access_mode = flags & O_ACCMODE;
    
    if (access_mode == O_RDONLY) {
        axe_mode = FILE_MODE_READ;
    } else if (access_mode == O_WRONLY) {
        axe_mode = FILE_MODE_WRITE;
    } else if (access_mode == O_RDWR) {
        axe_mode = FILE_MODE_READ | FILE_MODE_WRITE;
    }
    
    if (flags & O_APPEND) {
        axe_mode |= FILE_MODE_APPEND;
    }
    
    return axe_file_open(name, axe_mode);
}

// 5. _close - Close file
int _close(int file) {
    if (file <= 2) { // STDIN, STDOUT, STDERR
        return 0; // Always successful for standard streams
    }
    return axe_file_close(file);
}

// 6. _lseek - Seek in file
int _lseek(int file, int ptr, int dir) {
    // AxE file system doesn't support seeking currently
    errno = ENOTSUP;
    return -1;
}

// 7. _fstat - Get file status
int _fstat(int file, struct stat *st) {
    if (file <= 2) { // STDIN, STDOUT, STDERR
        st->st_mode = S_IFCHR; // Character device
        return 0;
    }
    // For files, return minimal stat info
    st->st_mode = S_IFREG; // Regular file
    st->st_size = 0; // Unknown size
    return 0;
}

// 8. _stat - Get file status by name
int _stat(const char *file, struct stat *st) {
    st->st_mode = S_IFREG; // Assume regular file
    st->st_size = 0; // Unknown size
    return 0;
}

// 9. _isatty - Check if file descriptor is a terminal
int _isatty(int file) {
    return (file <= 2) ? 1 : 0; // STDIN, STDOUT, STDERR are terminals
}

// 10. _sbrk - Increase program data space (heap management)
// Newlib needs this for FILE structure allocation
// Use AxE memory manager for consistency with malloc/free
void *_sbrk(int incr) {
    if (incr <= 0) {
        // Invalid request
        display_print(0, 0, "[ERROR] _sbrk called with invalid increment: ");
        display_print(2, incr, "");
        return (void *)-1;
    }
    
    void *result = memmgr_alloc(incr);
    
    if (result == NULL) {
        // Critical _sbrk failure - newlib FILE operations will fail
        display_print(0, 0, "[CRITICAL ERROR] _sbrk() FAILED");
        display_print(0, 0, "Newlib requested: ");
        display_print(2, incr, "");
        display_print(0, 0, " bytes for FILE operations");
        display_print(0, 0, "[CRITICAL] memmgr_alloc returned NULL");
        display_print(0, 0, "[CRITICAL] Newlib cannot allocate FILE structures");
        display_print(0, 0, "[CRITICAL] Check heap size in memory layout");
        display_print(0, 0, "[SYSTEM] HALTING - Newlib memory failure");
        
        // Force immediate halt
        *((volatile uint32_t*)0x0113FFFC) = 1;
        while(1) {
            asm volatile("nop");
        }
    }
    
    // Success
    display_print(0, 0, "[DEBUG] _sbrk: allocated ");
    display_print(2, incr, "");
    display_print(0, 0, " bytes for newlib");
    
    return result;
}

// 11. _getpid - Get process ID
int _getpid(void) {
    return 1; // Single process system
}

// 12. _kill - Send signal to process
int _kill(int pid, int sig) {
    errno = EINVAL;
    return -1;
}

// 13. _link - Create hard link
int _link(const char *old, const char *new) {
    errno = EMLINK;
    return -1;
}

// 14. _unlink - Remove file
int _unlink(const char *name) {
    errno = ENOENT;
    return -1;
}

// 15. _times - Get process times
clock_t _times(struct tms *buf) {
    return -1; // No timing information available
}

// 16. _wait - Wait for child process
int _wait(int *status) {
    errno = ECHILD;
    return -1;
}

// 17. _fork - Create child process
int _fork(void) {
    errno = EAGAIN;
    return -1;
}

// 18. _execve - Execute program
int _execve(const char *name, char * const *argv, char * const *env) {
    errno = ENOMEM;
    return -1;
}

//----------------------------------------------------------------
// Memory allocation using AxE memory manager
//----------------------------------------------------------------

void *malloc(size_t size) {
    void *result = memmgr_alloc(size);
    
    if (result == NULL && size > 0) {
        // Critical malloc failure - immediate halt with detailed error
        display_print(0, 0, "[CRITICAL ERROR] malloc() FAILED");
        display_print(0, 0, "Requested size: ");
        display_print(2, (int)size, "");
        display_print(0, 0, " bytes");
        display_print(0, 0, "[CRITICAL] memmgr_alloc returned NULL - heap exhausted");
        display_print(0, 0, "[CRITICAL] Check memory layout: data region too small");
        display_print(0, 0, "[CRITICAL] Current heap may be insufficient for SUSAN");
        display_print(0, 0, "[SYSTEM] HALTING IMMEDIATELY - NO RECOVERY");
        
        // Force immediate system halt
        *((volatile uint32_t*)0x0113FFFC) = 1;
        while(1) {
            asm volatile("nop");
        }
    }
    
    // Success - show allocation info  
    if (result != NULL) {
        display_print(0, 0, "[DEBUG] malloc: allocated ");
        display_print(2, (int)size, "");
        display_print(0, 0, " bytes");
    }
    
    return result;
}

void free(void *ptr) {
    if (ptr != NULL) {
        display_print(0, 0, "[DEBUG] free: deallocating memory");
    }
    memmgr_free(ptr);
}

void *calloc(size_t num, size_t size) {
    size_t total_size = num * size;
    void *ptr = memmgr_alloc(total_size);
    
    if (ptr == NULL && total_size > 0) {
        // Critical calloc failure
        display_print(0, 0, "[CRITICAL ERROR] calloc() FAILED");
        display_print(0, 0, "Requested: ");
        display_print(2, (int)num, "");
        display_print(0, 0, " x ");
        display_print(2, (int)size, "");
        display_print(0, 0, " = ");
        display_print(2, (int)total_size, "");
        display_print(0, 0, " bytes");
        display_print(0, 0, "[SYSTEM] HALTING IMMEDIATELY");
        
        *((volatile uint32_t*)0x0113FFFC) = 1;
        while(1) {
            asm volatile("nop");
        }
    }
    
    if (ptr) {
        // Zero out memory and show success
        char *p = (char*)ptr;
        for (size_t i = 0; i < total_size; i++) {
            p[i] = 0;
        }
        display_print(0, 0, "[DEBUG] calloc: allocated and zeroed ");
        display_print(2, (int)total_size, "");
        display_print(0, 0, " bytes");
    }
    return ptr;
}

//----------------------------------------------------------------
// Random number generation (imported from util.c)
//----------------------------------------------------------------

static int rng_initialized = 0;
static unsigned long int rng_state = 1;

void srand(unsigned int seed) {
    rng_state = seed;
    rng_initialized = 1;
}

int rand(void) {
    if (!rng_initialized) {
        display_print(0, 0, "ERROR: rng is not initialized, call srand()!\n");
        return 0;
    }
    
    // Linear congruential generator (same as util.c)
    rng_state = rng_state * 1103515245 + 12345;
    return (unsigned int)(rng_state / 65536) % 32768;
}

// Memory functions (memcpy, memset, memcmp) are provided by memmgr.c

//----------------------------------------------------------------
// Non-underscore versions (for newlib compatibility)
// Some newlib configurations call open() instead of _open()
//----------------------------------------------------------------

int open(const char *name, int flags, ...) {
    // Extract mode if provided (variadic argument)
    int mode = 0;
    if (flags & O_CREAT) {
        va_list ap;
        va_start(ap, flags);
        mode = va_arg(ap, int);
        va_end(ap);
    }
    return _open(name, flags, mode);
}

int close(int file) {
    return _close(file);
}

int read(int file, char *ptr, int len) {
    return _read(file, ptr, len);
}

int write(int file, char *ptr, int len) {
    return _write(file, ptr, len);
}

int lseek(int file, int ptr, int dir) {
    return _lseek(file, ptr, dir);
}

int fstat(int file, struct stat *st) {
    return _fstat(file, st);
}

int stat(const char *file, struct stat *st) {
    return _stat(file, st);
}

int isatty(int file) {
    return _isatty(file);
}

//----------------------------------------------------------------
// Reentrant versions (for thread-safe newlib)
// newlib's fopen() calls _fopen_r() which calls these
//----------------------------------------------------------------

int _open_r(struct _reent *ptr, const char *name, int flags, int mode) {
    int ret = _open(name, flags, mode);
    if (ret < 0) {
        ptr->_errno = errno;
    }
    return ret;
}

int _close_r(struct _reent *ptr, int file) {
    int ret = _close(file);
    if (ret < 0) {
        ptr->_errno = errno;
    }
    return ret;
}

int _read_r(struct _reent *ptr, int file, char *buf, int len) {
    int ret = _read(file, buf, len);
    if (ret < 0) {
        ptr->_errno = errno;
    }
    return ret;
}

int _write_r(struct _reent *ptr, int file, char *buf, int len) {
    int ret = _write(file, buf, len);
    if (ret < 0) {
        ptr->_errno = errno;
    }
    return ret;
}

int _lseek_r(struct _reent *ptr, int file, int offset, int whence) {
    int ret = _lseek(file, offset, whence);
    if (ret < 0) {
        ptr->_errno = errno;
    }
    return ret;
}

int _fstat_r(struct _reent *ptr, int file, struct stat *st) {
    int ret = _fstat(file, st);
    if (ret < 0) {
        ptr->_errno = errno;
    }
    return ret;
}

int _stat_r(struct _reent *ptr, const char *file, struct stat *st) {
    int ret = _stat(file, st);
    if (ret < 0) {
        ptr->_errno = errno;
    }
    return ret;
}

void *_sbrk_r(struct _reent *ptr, int incr) {
    void *ret = _sbrk(incr);
    if (ret == (void *)-1) {
        ptr->_errno = errno;
    }
    return ret;
}

int _isatty_r(struct _reent *ptr, int file) {
    return _isatty(file);
}