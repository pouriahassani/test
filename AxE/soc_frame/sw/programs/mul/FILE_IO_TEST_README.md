# File I/O Test in MUL Program

## Overview

This directory contains a comprehensive test of the AxE file I/O system integrated into the existing `mul` program. The test demonstrates all major file operations with practical examples.

## Test Features

### 1. Write Operations
- **File creation**: Creates `results.txt` with multiplication results
- **Data formatting**: Converts integers to strings without library functions
- **Error handling**: Checks for successful file opening

### 2. Read/Write Round-trip
- **Write test data**: Creates `test_data.txt` with formatted content
- **Read verification**: Reads back the written data and displays it
- **Content validation**: Verifies data integrity

### 3. Multi-file Operations
- **Concurrent files**: Opens and writes to `file1.txt` and `file2.txt` simultaneously
- **Resource management**: Proper file handle management and cleanup
- **Multi-node capability**: Demonstrates support for multiple open files

### 4. Integration Testing
- **Memory management**: Uses existing `memmgr` system alongside file I/O
- **Display output**: Shows file operation progress via `display_print`
- **Error reporting**: Comprehensive error checking and user feedback

## Expected Output

When running the program, you should see:

```
=== File I/O Test ===
Opening results.txt for write...
Write file opened successfully!
Bytes written: 14
Write file closed.
Creating test_data.txt...
Test data written successfully.
Reading back test_data.txt...
Read file opened successfully!
Bytes read: 85
File contents:
Multiplication Test Data:
333 * 444 = 147852
Float: 5.9 / 12.9 = 0.457
Memory test passed
Read file closed.
Testing multiple file operations...
Both files opened successfully!
Multi-file test completed!
=== File I/O Test Complete ===
```

## Generated Files

After running the test, the following files will be created in the simulation working directory:
- `results.txt` - Contains multiplication result
- `test_data.txt` - Test data with mathematical results
- `file1.txt` - Multi-file test content
- `file2.txt` - Multi-file test content

## Testing Instructions

### 1. Build the Program
```bash
cd /home/axe/workspace/soc_frame/sw/programs/mul
make clean
make
```

### 2. Run the Simulation
```bash
cd /home/axe/workspace/soc_frame/systems/2x2_16_priority_input_approx
make clean
make
make run
```

### 3. Verify File Creation
After simulation completes, check the simulation directory for created files:
```bash
ls -la *.txt
cat results.txt
cat test_data.txt
```

## Technical Implementation

### File Operations Used
- `axe_file_open()` - Open files for read/write
- `axe_file_read()` - Read data from files
- `axe_file_write()` - Write data to files  
- `axe_file_close()` - Close file handles

### Memory Management
- Uses existing `memmgr_init()` and `malloc()` for dynamic memory
- Demonstrates integration between file I/O and memory systems
- Proper buffer management for read/write operations

### Error Handling
- Checks return values from all file operations
- Graceful degradation on file operation failures
- Comprehensive error reporting via display output

## Performance Characteristics

- **File operations**: Blocking semantics ensure completion
- **Memory usage**: Minimal additional overhead
- **Simulation impact**: Operations only occur during file I/O calls
- **Multi-file support**: Up to 8 concurrent files supported

## Troubleshooting

### Common Issues
1. **File not created**: Check simulation working directory
2. **Operation fails**: Verify memory configuration generation
3. **Build errors**: Ensure `file_io.c` is included in Makefile

### Debug Information
- File operation status is displayed during execution
- Byte counts for read/write operations are shown
- Error messages indicate specific failure points

## Integration Notes

This test demonstrates the file I/O system integration with:
- **Existing programs**: Minimal changes to original `mul` program
- **Memory management**: Coexistence with `memmgr` system
- **Display system**: Progress reporting via `display_print`
- **Build system**: Automatic memory configuration inclusion