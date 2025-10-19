#include "file_io.h"
#include <stdio.h>
// #include "util.h"  // Causes trap - avoid full include

// Forward declare only what we need from util.h
extern void display_print(int x, int y, const char* str);
/**
 * @file file_io.c
 * @brief Implementation of host-based file I/O operations
 * 
 * This implementation uses memory-mapped I/O to trigger file operations
 * that are detected by the file_io_detector module and handled by simulation.
 */

/* Memory-mapped I/O addresses from generated configuration */
/* These addresses are automatically generated from memory_layout.yaml */

/* File handle management structure */
typedef struct {
    int in_use;                    /* 1 if this slot is occupied */
    char* buffer;                  /* Pointer to this file's buffer */
    uint32_t buffer_size;            /* Size of allocated buffer */
    uint32_t data_size;              /* Amount of valid data in buffer */
    uint32_t position;               /* Current read/write position */
} file_handle_t;

/* File handle table */
static file_handle_t file_handles[MAX_OPEN_FILES];
static int next_fd = 0;           /* Next available file descriptor */

/* File I/O memory region (reserved for file buffers) */
static char file_io_memory[FILE_IO_MEM_SIZE] __attribute__((section(".file_io_data")));

/* Shared parameter structure for communication with simulation */
static volatile struct {
    int fd;
    const char* filename;
    void* buffer;
    uint32_t size;
    int mode;
    int result;
    uint32_t operation_id;         /* Unique ID for this operation */
} file_params __attribute__((section(".file_io_data")));

/* Initialize file I/O system */
static void init_file_io(void) {
    static int initialized = 0;
    if (initialized) return;
    
    /* Clear file handle table */
    for (int i = 3; i < MAX_OPEN_FILES; i++) {
        file_handles[i].in_use = 0;
        file_handles[i].buffer = &file_io_memory[i * FILE_BUFFER_SIZE];
        file_handles[i].buffer_size = FILE_BUFFER_SIZE;
        file_handles[i].data_size = 0;
        file_handles[i].position = 0;
    }
    
    initialized = 1;
}

/* Allocate a new file descriptor */
static int allocate_fd(void) {
    init_file_io();
    for (int i = 3; i < MAX_OPEN_FILES; i++) {
        if (!file_handles[i].in_use) {
            file_handles[i].in_use = 1;
            file_handles[i].data_size = 0;
            file_handles[i].position = 0;
            return i;
        }
    }
    return FILE_ERROR_NO_SPACE;  /* No free slots */
}

/* Free a file descriptor */
static void free_fd(int fd) {
    if (fd >= 0 && fd < MAX_OPEN_FILES) {
        file_handles[fd].in_use = 0;
        file_handles[fd].data_size = 0;
        file_handles[fd].position = 0;
    }
}

int axe_file_open(const char* filename, int mode) {
    /* Validate input parameters */
    if (!filename) {
        return FILE_ERROR_INVALID_FD;
    }
    
    /* Validate mode combinations */
    if ((mode & FILE_MODE_EXCL) && !(mode & FILE_MODE_CREATE)) {
        /* O_EXCL requires O_CREAT */
        return FILE_ERROR_PERMISSION;
    }
    
    if ((mode & FILE_MODE_READ) && (mode & FILE_MODE_WRITE)) {
        /* Read-write mode: ensure we have both flags properly set */
        if (mode & FILE_MODE_TRUNC) {
            /* Truncate in read-write mode - valid */
        }
    } else if (mode & FILE_MODE_READ) {
        /* Read-only: TRUNC and CREATE don't make sense */
        if (mode & (FILE_MODE_TRUNC | FILE_MODE_CREATE)) {
            display_print(0, 0, "[WARNING] axe_file_open: ignoring TRUNC/CREATE in read-only mode\n");
            mode &= ~(FILE_MODE_TRUNC | FILE_MODE_CREATE);
        }
    }
    
    /* Display mode information for debugging */
    display_print(0, 0, "[DEBUG] axe_file_open: ");
    display_print(0, 0, filename);
    display_print(0, 0, " mode=0x");
    display_print(2, mode, "");
    
    if (mode & FILE_MODE_READ) display_print(0, 0, " READ");
    if (mode & FILE_MODE_WRITE) display_print(0, 0, " WRITE");
    if (mode & FILE_MODE_APPEND) display_print(0, 0, " APPEND");
    if (mode & FILE_MODE_CREATE) display_print(0, 0, " CREATE");
    if (mode & FILE_MODE_EXCL) display_print(0, 0, " EXCL");
    if (mode & FILE_MODE_TRUNC) display_print(0, 0, " TRUNC");
    if (mode & FILE_MODE_BINARY) display_print(0, 0, " BINARY");
    display_print(0, 0, "\n");

    /* Allocate a file descriptor */  
    int fd = allocate_fd();
    if (fd < 0) {
        return fd;  /* Return error */
    }

    /* Set parameters for simulation */
    file_params.fd = fd;
    file_params.filename = filename;
    file_params.mode = mode;
    file_params.buffer = file_handles[fd].buffer;  /* Use allocated buffer */
    file_params.size = file_handles[fd].buffer_size;
    file_params.operation_id = ((uint32_t)filename) ^ (fd << 16);  /* Unique ID */
    file_params.result = -999;  // Initialize to known value
    
    /* Trigger file_open operation */
    *((volatile uint32_t*)FILE_OPEN_TRIGGER) = (uint32_t)&file_params;
    
    /* Wait for simulation to set result */
    int wait_count = 0;                                           
    while (file_params.result != fd ) {                              
        // Wait for simulation to process and set result                                                                     
        wait_count++;                                                 
        __asm__ volatile ("nop");  // Prevent compiler optimization   
    } 
    
    /* Check result */
    if (file_params.result < 0) {
        display_print(0, 0, "[ERROR] axe_file_open failed: ");
        display_print(2, file_params.result, "");
        display_print(0, 0, "\n");
        free_fd(fd);  /* Free on error */
        return file_params.result;
    }
    
    /* Success - return file descriptor */
    display_print(0, 0, "[SUCCESS] axe_file_open: fd=");
    display_print(2, fd, "");
    display_print(0, 0, "\n");
    return fd;
}

int axe_file_read(int fd, void* buffer, uint32_t size) {
    /* Validate file descriptor */
    if (fd < 0 || fd >= MAX_OPEN_FILES || !file_handles[fd].in_use) {
        return FILE_ERROR_INVALID_FD;
    }
    
    /* Use the file's dedicated buffer for data transfer */
    file_handle_t* fh = &file_handles[fd];
    
    /* Set parameters for simulation */
    file_params.fd = fd;
    file_params.buffer = fh->buffer;  /* Use file's own buffer */
    file_params.size = (size > fh->buffer_size) ? fh->buffer_size : size;
    file_params.operation_id = fd | (0x01 << 24);  /* Read operation ID */
    
    /* Trigger file_read operation */
    *((volatile uint32_t*)FILE_READ_TRIGGER) = (uint32_t)&file_params;
    
    /* Check result */
    if (file_params.result > 0) {
        /* Copy data from file buffer to user buffer */
        uint32_t bytes_to_copy = (file_params.result > size) ? size : file_params.result;
        for (uint32_t i = 0; i < bytes_to_copy; i++) {
            ((char*)buffer)[i] = fh->buffer[i];
        }
        fh->data_size = file_params.result;
        return bytes_to_copy;
    }
    
    return file_params.result;
}

int axe_file_write(int fd, const void* buffer, uint32_t size) {
    /* Validate file descriptor */
    if (fd < 0 || fd >= MAX_OPEN_FILES || !file_handles[fd].in_use) {
        return FILE_ERROR_INVALID_FD;
    }

    
    /* Use the file's dedicated buffer for data transfer */
    file_handle_t* fh = &file_handles[fd];
    
    /* Copy user data to file buffer */
    uint32_t bytes_to_copy = (size > fh->buffer_size) ? fh->buffer_size : size;
    for (uint32_t i = 0; i < bytes_to_copy; i++) {
        fh->buffer[i] = ((const char*)buffer)[i];
    }
    
    /* Set parameters for simulation */
    file_params.fd = fd;
    file_params.buffer = fh->buffer;  /* Use file's own buffer */
    file_params.size = bytes_to_copy;
    file_params.operation_id = fd | (0x02 << 24);  /* Write operation ID */
    
    /* Trigger file_write operation */
    *((volatile uint32_t*)FILE_WRITE_TRIGGER) = (uint32_t)&file_params;
    
    return file_params.result;
}

int axe_file_close(int fd) {
    /* Validate file descriptor */
    if (fd < 0 || fd >= MAX_OPEN_FILES || !file_handles[fd].in_use) {
        return FILE_ERROR_INVALID_FD;
    }
    
    /* Set parameters for simulation */
    file_params.fd = fd;
    file_params.operation_id = fd | (0x03 << 24);  /* Close operation ID */
    
    /* Trigger file_close operation */
    *((volatile uint32_t*)FILE_CLOSE_TRIGGER) = (uint32_t)&file_params;
    
    /* Free the file descriptor */
    free_fd(fd);
    
    return file_params.result;
}

int axe_file_size(const char* filename) {
    /* Set parameters */
    file_params.filename = filename;
    
    /* Trigger file_size operation */
    *((volatile uint32_t*)FILE_SIZE_TRIGGER) = (uint32_t)&file_params;
    
    /* Return result set by simulation */
    return file_params.result;
}