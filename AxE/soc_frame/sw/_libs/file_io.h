#ifndef FILE_IO_H
#define FILE_IO_H

#include <stdint.h>
// #include <stddef.h>

/**
 * @file file_io.h
 * @brief Host-based file I/O API for AxE SoC platform
 * 
 * This module provides POSIX-like file operations that work during simulation
 * by communicating with the host system through custom RISC-V instructions.
 * File operations are handled by the Verilator simulation environment.
 */

/* File operation modes - Enhanced POSIX support */
#define FILE_MODE_READ     0x01   /* Read access */
#define FILE_MODE_WRITE    0x02   /* Write access */
#define FILE_MODE_APPEND   0x04   /* Append mode - write at end */
#define FILE_MODE_CREATE   0x08   /* O_CREAT - create if doesn't exist */
#define FILE_MODE_EXCL     0x10   /* O_EXCL - fail if file exists with O_CREAT */
#define FILE_MODE_TRUNC    0x20   /* O_TRUNC - truncate existing file to zero */
#define FILE_MODE_BINARY   0x40   /* Binary mode (no text conversion) */

/* Convenience combinations for common patterns */
#define FILE_MODE_READ_ONLY    (FILE_MODE_READ | FILE_MODE_BINARY)
#define FILE_MODE_WRITE_NEW    (FILE_MODE_WRITE | FILE_MODE_CREATE | FILE_MODE_TRUNC | FILE_MODE_BINARY)
#define FILE_MODE_WRITE_APPEND (FILE_MODE_WRITE | FILE_MODE_APPEND | FILE_MODE_CREATE | FILE_MODE_BINARY)
#define FILE_MODE_READ_WRITE   (FILE_MODE_READ | FILE_MODE_WRITE | FILE_MODE_BINARY)

/* Error codes - Enhanced for comprehensive file operations */
#define FILE_SUCCESS              0
#define FILE_ERROR_INVALID_FD     -1   /* Invalid file descriptor */
#define FILE_ERROR_FILE_NOT_FOUND -2   /* File doesn't exist (and CREATE not set) */
#define FILE_ERROR_PERMISSION     -3   /* Permission denied or invalid mode combination */
#define FILE_ERROR_NO_SPACE       -4   /* No free file descriptors or disk space */
#define FILE_ERROR_FILE_EXISTS    -5   /* File exists (with EXCL flag) */
#define FILE_ERROR_INVALID_MODE   -6   /* Invalid mode combination */
#define FILE_ERROR_IO_ERROR       -7   /* General I/O error */
#define FILE_ERROR_TRUNCATE_FAIL  -8   /* Failed to truncate file */

/* Include generated memory layout configuration */
#include "axe_memory_layout.h"

/* File I/O configuration from memory layout */
#define MAX_OPEN_FILES    FILE_IO_MAX_FILES
#define FILE_BUFFER_SIZE  FILE_IO_BUFFER_SIZE
#define FILE_IO_MEM_BASE  FILE_IO_BASE_ADDR
#define FILE_IO_MEM_SIZE  (MAX_OPEN_FILES * FILE_BUFFER_SIZE)

/**
 * @brief Open a file for reading or writing
 * 
 * Opens a file on the host system and returns a file descriptor for subsequent
 * operations. The file path is relative to the simulation working directory.
 * 
 * @param filename Path to the file (null-terminated string)
 * @param mode File access mode (FILE_MODE_READ, FILE_MODE_WRITE, FILE_MODE_APPEND)
 * @return File descriptor (>= 0) on success, negative error code on failure
 */
int axe_file_open(const char* filename, int mode);

/**
 * @brief Read data from an open file
 * 
 * Reads up to 'size' bytes from the file into the provided buffer.
 * The data is transferred from the host system to AxE memory.
 * 
 * @param fd File descriptor returned by axe_file_open()
 * @param buffer Pointer to buffer where data will be stored
 * @param size Maximum number of bytes to read
 * @return Number of bytes actually read, or negative error code
 */
int axe_file_read(int fd, void* buffer, uint32_t size);

/**
 * @brief Write data to an open file
 * 
 * Writes 'size' bytes from the buffer to the file on the host system.
 * The data is transferred from AxE memory to the host filesystem.
 * 
 * @param fd File descriptor returned by axe_file_open()
 * @param buffer Pointer to data to be written
 * @param size Number of bytes to write
 * @return Number of bytes actually written, or negative error code
 */
int axe_file_write(int fd, const void* buffer, uint32_t size);

/**
 * @brief Close an open file
 * 
 * Closes the file and releases associated resources on the host system.
 * The file descriptor becomes invalid after this operation.
 * 
 * @param fd File descriptor to close
 * @return FILE_SUCCESS on success, negative error code on failure
 */
int axe_file_close(int fd);

/**
 * @brief Get the size of a file
 * 
 * Returns the size of the specified file in bytes.
 * 
 * @param filename Path to the file
 * @return File size in bytes, or negative error code
 */
int axe_file_size(const char* filename);

/* Internal custom instruction opcodes - do not use directly */
#define _FILE_OPEN_INSTR   0x0EA5F00B
#define _FILE_READ_INSTR   0x0EA5F10B  
#define _FILE_WRITE_INSTR  0x0EA5F20B
#define _FILE_CLOSE_INSTR  0x0EA5F30B
#define _FILE_SIZE_INSTR   0x0EA5F40B

#endif /* FILE_IO_H */