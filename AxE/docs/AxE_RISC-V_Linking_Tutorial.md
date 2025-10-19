# AxE RISC-V Linking Tutorial: BRAM-Only Memory Model

## Executive Summary

This document provides a comprehensive tutorial on RISC-V linking specifically for the AxE (Approximate eXecution) framework. Unlike traditional embedded systems with separate Flash and RAM, AxE uses a unified BRAM (Block RAM) memory model. We'll walk through a simple addition function example to demonstrate every aspect of the linking process.

## Table of Contents

1. [AxE Memory Architecture](#axe-memory-architecture)
2. [BRAM vs Flash+RAM Differences](#bram-vs-flashram-differences)
3. [Simple Addition Example](#simple-addition-example)
4. [Source Code Files](#source-code-files)
5. [Assembly Syntax Deep Dive](#assembly-syntax-deep-dive)
6. [Linking Process Detailed](#linking-process-detailed)
7. [Memory Layout Analysis](#memory-layout-analysis)
8. [Execution Flow](#execution-flow)
9. [AxE-Specific Debugging](#axe-specific-debugging)

## AxE Memory Architecture

### Hardware Overview: AxE SoC with BRAM

```
┌─────────────────────────────────────┐
│         RISC-V CPU Core             │
│  ┌─────────────┐ ┌─────────────┐   │
│  │     PC      │ │  Registers  │   │
│  │ 0x00000000  │ │   x0-x31    │   │
│  └─────────────┘ └─────────────┘   │
└─────────────────────────────────────┘
           │
           │ Address/Data Bus
           │
┌─────────────────────────────────────┐
│          BRAM Memory                │
│                                     │
│ 0x00020000 ├─────────────────┤     │
│            │      Stack      │     │ ↓ grows down
│ 0x00010000 ├─────────────────┤     │
│            │   Data/BSS      │     │
│ 0x00008000 ├─────────────────┤     │
│            │   Application   │     │
│ 0x00004000 ├─────────────────┤     │
│            │   Functions     │     │
│ 0x00001000 ├─────────────────┤     │
│            │  Boot/Startup   │     │
│ 0x00000000 └─────────────────┘     │ ← Reset vector
└─────────────────────────────────────┘
```

### AxE Memory Specifications
- **Memory Type**: Unified BRAM (Block RAM)
- **Total Size**: ~26MB (configurable via `MEM_SIZE`)
- **Address Range**: 0x00000000 - 0x0199999C
- **Reset Vector**: 0x00000000 (CPU starts here)
- **Stack Location**: 131060 (0x0001FFE4) - grows downward
- **Memory Access**: Single-cycle read/write
- **Initialization**: Via $readmemh from .hex files

## BRAM vs Flash+RAM Differences

### Traditional Embedded System (Flash + RAM)
```
┌─────────────────┬─────────────────┐
│      Flash      │       RAM       │
│   (Read-Only)   │  (Read/Write)   │
├─────────────────┼─────────────────┤
│ Code Storage    │ Variable Storage│
│ Constant Data   │ Stack Space     │
│ Initial Values  │ Runtime Data    │
└─────────────────┴─────────────────┘
  Separate buses      Fast access
  Non-volatile        Volatile
```

### AxE System (Unified BRAM)
```
┌─────────────────────────────────────┐
│             BRAM                    │
│         (Read/Write)                │
├─────────────────────────────────────┤
│ Code Execution (can be modified!)  │
│ Variable Storage                    │
│ Stack Space                         │
│ All in same address space          │
└─────────────────────────────────────┘
  Single address space
  Fast access everywhere
  Volatile (loaded at startup)
```

### Key Implications for Linking

| Aspect | Traditional | AxE BRAM |
|--------|-------------|----------|
| **Code Location** | Flash (fixed) | BRAM (can be anywhere) |
| **Data Copying** | Flash→RAM required | No copying needed |
| **Startup Code** | Complex initialization | Simplified setup |
| **Memory Sections** | Strict separation | Flexible placement |
| **Entry Point** | Must be at Flash start | Flexible placement |

## Simple Addition Example

### Project Goal
Create a simple program that:
1. Defines two integers (a=5, b=3)
2. Calls an addition function
3. Stores the result
4. Returns the sum

### Project Structure
```
axe_addition/
├── start.S        (AxE startup code)
├── main.c         (main function)
├── add.c          (addition function)
├── add.h          (addition header)
└── Makefile       (build script)
```

## Source Code Files

### 1. start.S (AxE Startup Code)

```assembly
# start.S - AxE startup code (BRAM-specific)
# Based on AxE framework sw/_libs/start.S

    .section .text           # Standard text section (no .text.start needed)
    .global my_start         # AxE uses my_start as entry point
    .global main             # Also export main for compatibility

# Entry point - where CPU jumps on reset
my_start:
main:
    # Step 1: Zero-initialize all registers (AxE convention)
    # This ensures clean state regardless of previous execution
    
    addi x1, zero, 0         # x1 = ra (return address) = 0
    # Note: x2 (sp) will be set explicitly below
    # Note: x3, x4 often skipped in AxE (performance optimization)
    
    addi x5, zero, 0         # x5 = t0 (temporary register) = 0
    addi x6, zero, 0         # x6 = t1 = 0
    addi x7, zero, 0         # x7 = t2 = 0
    addi x8, zero, 0         # x8 = s0/fp (frame pointer) = 0
    addi x9, zero, 0         # x9 = s1 = 0
    addi x10, zero, 0        # x10 = a0 (arg 0) = 0
    addi x11, zero, 0        # x11 = a1 (arg 1) = 0
    addi x12, zero, 0        # x12 = a2 (arg 2) = 0
    addi x13, zero, 0        # x13 = a3 (arg 3) = 0
    addi x14, zero, 0        # x14 = a4 (arg 4) = 0
    addi x15, zero, 0        # x15 = a5 (arg 5) = 0
    addi x16, zero, 0        # x16 = a6 (arg 6) = 0
    addi x17, zero, 0        # x17 = a7 (arg 7) = 0
    addi x18, zero, 0        # x18 = s2 (saved register) = 0
    addi x19, zero, 0        # x19 = s3 = 0
    addi x20, zero, 0        # x20 = s4 = 0
    addi x21, zero, 0        # x21 = s5 = 0
    addi x22, zero, 0        # x22 = s6 = 0
    addi x23, zero, 0        # x23 = s7 = 0
    addi x24, zero, 0        # x24 = s8 = 0
    addi x25, zero, 0        # x25 = s9 = 0
    addi x26, zero, 0        # x26 = s10 = 0
    addi x27, zero, 0        # x27 = s11 = 0
    addi x28, zero, 0        # x28 = t3 = 0
    addi x29, zero, 0        # x29 = t4 = 0
    addi x30, zero, 0        # x30 = t5 = 0
    addi x31, zero, 0        # x31 = t6 = 0
    
    # Step 2: Set up stack pointer (AxE-specific value)
    # AxE uses 131060 decimal = 0x0001FFE4 hex
    lui sp, %hi(131060)      # Load upper 20 bits of 131060 into sp
    addi sp, sp, %lo(131060) # Add lower 12 bits to complete address
    
    # Step 3: Call main application function
    # AxE convention: application logic goes in my_main
    call my_main             # Jump to my_main, save return in ra (x1)
    
    # Step 4: Infinite loop if main returns
    # In BRAM system, no OS to return to
loop:
    j loop                   # Jump to self = infinite loop
```

### 2. add.h (Addition Function Header)

```c
// add.h - Addition function interface
#ifndef ADD_H
#define ADD_H

#include <stdint.h>

// Function declaration
// Parameters: two 32-bit integers
// Returns: 32-bit integer sum
int32_t add_numbers(int32_t a, int32_t b);

// Global variable for storing result
// This will go in .data section in BRAM
extern int32_t result;

#endif
```

### 3. add.c (Addition Function Implementation)

```c
// add.c - Addition function implementation
#include "add.h"

// Global variable with initial value
// In BRAM: stored directly where it will be used (no copying needed)
int32_t result = 0;

// Addition function
// RISC-V ABI: a0=first param, a1=second param, a0=return value
int32_t add_numbers(int32_t a, int32_t b) {
    // Simple addition
    int32_t sum = a + b;
    
    // Store in global variable
    result = sum;
    
    // Return the sum
    return sum;
}
```

### 4. main.c (Main Application)

```c
// main.c - Main application function
#include "add.h"

// AxE convention: main logic goes in my_main function
int my_main(void) {
    // Define two numbers to add
    int32_t first_number = 5;
    int32_t second_number = 3;
    
    // Call addition function
    int32_t sum = add_numbers(first_number, second_number);
    
    // Verify result is stored correctly
    if (result == sum && sum == 8) {
        return 0;  // Success
    } else {
        return 1;  // Error
    }
}
```

### 5. Makefile (Build Script)

```makefile
# Makefile - AxE addition example build script

# RISC-V toolchain
CC = riscv32-unknown-elf-gcc
OBJCOPY = riscv32-unknown-elf-objcopy
OBJDUMP = riscv32-unknown-elf-objdump
READELF = riscv32-unknown-elf-readelf

# Compiler flags for AxE
CFLAGS = -march=rv32im -mabi=ilp32 -O2 -Wall -fno-builtin
LDFLAGS = -nostartfiles -Wl,-e,my_start

# Source files
ASM_SOURCES = start.S
C_SOURCES = main.c add.c
OBJECTS = $(ASM_SOURCES:.S=.o) $(C_SOURCES:.c=.o)

# Target names
TARGET = axe_addition

# Build targets
all: $(TARGET).elf $(TARGET).hex $(TARGET).dump

# Link all objects into final executable
$(TARGET).elf: $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $(OBJECTS)

# Convert ELF to hex (for AxE BRAM loading)
$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O verilog $< $@

# Create disassembly for debugging
$(TARGET).dump: $(TARGET).elf
	$(OBJDUMP) -d $< > $@

# Compile C files
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

# Assemble assembly files
%.o: %.S
	$(CC) $(CFLAGS) -c -o $@ $<

# Debug targets
debug: $(TARGET).elf
	$(OBJDUMP) -d $(TARGET).elf
	$(READELF) -a $(TARGET).elf
	$(READELF) -S $(TARGET).elf

clean:
	rm -f *.o *.elf *.hex *.dump

.PHONY: all debug clean
```

## Assembly Syntax Deep Dive

### RISC-V Register Naming and ABI

```assembly
# RISC-V has 32 registers (x0-x31) with ABI names:

# x0  = zero    # Hardwired to 0 (cannot be changed)
# x1  = ra      # Return address (where function returns to)
# x2  = sp      # Stack pointer (top of stack)
# x3  = gp      # Global pointer (often unused in embedded)
# x4  = tp      # Thread pointer (often unused in embedded)
# x5  = t0      # Temporary register (caller-saved)
# x6  = t1      # Temporary register (caller-saved)
# x7  = t2      # Temporary register (caller-saved)
# x8  = s0/fp   # Saved register/Frame pointer (callee-saved)
# x9  = s1      # Saved register (callee-saved)
# x10 = a0      # Argument 0 / Return value (caller-saved)
# x11 = a1      # Argument 1 (caller-saved)
# x12 = a2      # Argument 2 (caller-saved)
# x13 = a3      # Argument 3 (caller-saved)
# x14 = a4      # Argument 4 (caller-saved)
# x15 = a5      # Argument 5 (caller-saved)
# x16 = a6      # Argument 6 (caller-saved)
# x17 = a7      # Argument 7 (caller-saved)
# x18 = s2      # Saved register (callee-saved)
# x19 = s3      # Saved register (callee-saved)
# x20 = s4      # Saved register (callee-saved)
# x21 = s5      # Saved register (callee-saved)
# x22 = s6      # Saved register (callee-saved)
# x23 = s7      # Saved register (callee-saved)
# x24 = s8      # Saved register (callee-saved)
# x25 = s9      # Saved register (callee-saved)
# x26 = s10     # Saved register (callee-saved)
# x27 = s11     # Saved register (callee-saved)
# x28 = t3      # Temporary register (caller-saved)
# x29 = t4      # Temporary register (caller-saved)
# x30 = t5      # Temporary register (caller-saved)
# x31 = t6      # Temporary register (caller-saved)
```

### Assembly Directive Syntax

```assembly
# .section directive - defines which section this code belongs to
.section .text          # Put following code in .text section
.section .data          # Put following data in .data section
.section .bss           # Put following uninitialized data in .bss section

# .global directive - makes symbol visible to linker
.global my_start        # Export my_start symbol
.global main            # Export main symbol

# Label syntax - creates a symbol at current location
my_start:               # Symbol my_start points to next instruction
main:                   # Symbol main points to same location
loop:                   # Symbol loop for jump target
```

### RISC-V Instruction Syntax Deep Dive

#### 1. ADD Immediate (addi)
```assembly
addi x5, zero, 0        # x5 = zero + 0 = 0
addi sp, sp, %lo(131060) # sp = sp + lower_12_bits(131060)

# Syntax: addi destination, source, immediate
# Constraints: immediate must be 12-bit signed (-2048 to +2047)
```

#### 2. Load Upper Immediate (lui)
```assembly
lui sp, %hi(131060)     # sp = upper_20_bits(131060) << 12

# Syntax: lui destination, immediate
# Purpose: Load upper 20 bits, zero lower 12 bits
# Example: 131060 = 0x0001FFE4
#   %hi(131060) = 0x00001 (upper 20 bits)
#   Result: sp = 0x00001000 (lower 12 bits zero)
```

#### 3. Address Calculation with %hi and %lo
```assembly
# To load full 32-bit address 131060 (0x0001FFE4):
lui sp, %hi(131060)      # sp = 0x00001000
addi sp, sp, %lo(131060) # sp = 0x00001000 + 0xFE4 = 0x0001FFE4

# %hi() extracts bits [31:12] and handles 2's complement correction
# %lo() extracts bits [11:0] as signed 12-bit value
```

#### 4. Function Call (call)
```assembly
call my_main            # Pseudo-instruction that expands to:
                        # auipc ra, %hi(my_main)
                        # jalr ra, %lo(my_main)(ra)

# Effect: 
#   1. ra = current_pc + 4 (return address)
#   2. pc = address_of_my_main (jump to function)
```

#### 5. Unconditional Jump (j)
```assembly
j loop                  # Pseudo-instruction that expands to:
                        # jal zero, loop

# Effect: pc = address_of_loop (jump without saving return address)
```

### AxE-Specific Assembly Patterns

#### Register Initialization Pattern
```assembly
# AxE convention: Zero all registers for clean state
addi x1, zero, 0        # x1 = 0 + 0 = 0
addi x5, zero, 0        # x5 = 0 + 0 = 0
# ... repeat for all registers

# Why not use "mv x1, zero"?
# mv is pseudo-instruction for "addi x1, zero, 0"
# Using addi directly is more explicit
```

#### Stack Setup Pattern
```assembly
# AxE uses specific stack address: 131060
lui sp, %hi(131060)     # sp gets upper bits
addi sp, sp, %lo(131060) # sp gets complete address

# Converting 131060 to hex: 131060 = 0x0001FFE4
# Binary: 00000000000000011111111111100100
#         |---- 20 bits ----||-- 12 bits --|
# %hi(131060) = 0x00001 (bits 31:12)
# %lo(131060) = 0xFE4 (bits 11:0) = -28 in signed 12-bit
```

## Linking Process Detailed

Now the crucial part - linking in the AxE BRAM environment! The linker combines all objects:

```bash
riscv32-unknown-elf-gcc -nostartfiles -Wl,-e,my_start -o axe_addition.elf start.o main.o add.o
```

### Phase 1: Symbol Collection

The linker scans all object files and builds a global symbol table:

```
Global Symbol Table (AxE Addition Example):
┌─────────────────┬─────────┬─────────────┬─────────────┐
│ Symbol Name     │ File    │ Status      │ Section     │
├─────────────────┼─────────┼─────────────┼─────────────┤
│ my_start        │start.o  │ defined     │ .text       │
│ main            │start.o  │ defined     │ .text       │
│ my_main         │ main.o  │ defined     │ .text       │
│ add_numbers     │ add.o   │ defined     │ .text       │
│ result          │ add.o   │ defined     │ .data       │
└─────────────────┴─────────┴─────────────┴─────────────┘
```

### Phase 2: Memory Layout (BRAM-Specific)

Unlike Flash+RAM systems, AxE uses unified BRAM layout:

```
BRAM Memory Assignment (No Linker Script):
┌─────────────┬──────────────┬─────────────────┐
│ Section     │ Address      │ Content         │
├─────────────┼──────────────┼─────────────────┤
│ .text       │ 0x00000000   │ All code        │
│   my_start  │ 0x00000000   │ Entry point     │
│   my_main   │ 0x00000080   │ Main function   │
│   add_numbers│ 0x000000C0   │ Add function    │
│ .rodata     │ 0x00000200   │ Constants       │
│ .data       │ 0x00000300   │ Initialized vars│
│   result    │ 0x00000300   │ Global int      │
│ .bss        │ 0x00000304   │ Uninit vars     │
└─────────────┴──────────────┴─────────────────┘
```

### Phase 3: Address Assignment (AxE BRAM Model)

The linker assigns actual addresses to all symbols:

```
Final Symbol Addresses (BRAM Layout):
┌─────────────────┬──────────────┬─────────────────┐
│ Symbol Name     │ Address      │ Notes           │
├─────────────────┼──────────────┼─────────────────┤
│ my_start        │ 0x00000000   │ ← Entry point!  │
│ main            │ 0x00000000   │ ← Same as start │
│ my_main         │ 0x00000080   │ App entry       │
│ add_numbers     │ 0x000000C0   │ Addition func   │
│ result          │ 0x00000300   │ Global variable │
└─────────────────┴──────────────┴─────────────────┘
```

### Phase 4: Relocation (Simplified in BRAM)

The linker fixes all address references in the code:

**Before relocation (in start.o):**
```assembly
call my_main       # Address unknown - marked for relocation
```

**After relocation (in axe_addition.elf):**
```assembly
call my_main       # Now becomes: call 0x00000080
```

**Example relocation in add.c:**
```c
// Original C code:
result = sum;

// Becomes assembly:
lui t0, %hi(0x00000300)    # Load upper bits of result address
sw a0, %lo(0x00000300)(t0) # Store sum to result variable
```

### BRAM vs Flash+RAM Relocation Differences

#### Traditional Flash+RAM System
```assembly
# Complex data section handling required
la t0, __data_start       # RAM address for runtime
la t1, __data_load        # Flash address for initial value
lw t2, 0(t1)             # Load from Flash
sw t2, 0(t0)             # Store to RAM
```

#### AxE BRAM System
```assembly
# Simplified - data lives where it executes
lui t0, %hi(result_addr)  # Load address directly
sw a0, %lo(result_addr)(t0) # Store directly - no copying
```

## Memory Layout Analysis

### Final BRAM Memory Map

```
BRAM (0x00000000 - 0x0199999C):
┌─────────────────┐ 0x0199999C
│    (unused)     │
├─────────────────┤ 0x00020000
│     Stack       │ ↓ grows down from 0x0001FFE4
│                 │
├─────────────────┤ 0x00010000
│   (free space)  │
├─────────────────┤ 0x00000304
│ .bss (if any)   │ 0x00000304
├─────────────────┤ 0x00000304
│ result = 0      │ 0x00000300 ← .data section
├─────────────────┤ 0x00000300
│  (padding)      │
├─────────────────┤ 0x00000200
│ .rodata         │ (constants, if any)
├─────────────────┤ 0x00000200
│ add_numbers()   │ 0x000000C0
├─────────────────┤ 0x000000C0
│ my_main()       │ 0x00000080
├─────────────────┤ 0x00000080
│ startup code    │ 0x00000000 ← my_start entry point
└─────────────────┘
```

### Why This Layout Works in BRAM

1. **Unified Address Space**: Code and data in same memory
2. **No Copying Required**: Variables stored where they execute
3. **Flexible Placement**: Linker can optimize layout
4. **Fast Access**: Single-cycle access to all memory

## Execution Flow

### 1. AxE Hardware Reset
```
CPU State on Reset:
PC (Program Counter) = 0x00000000
SP (Stack Pointer)   = undefined
All registers        = undefined
BRAM contents        = loaded from .hex file
```

### 2. Startup Execution (start.S)

**Step 2a: Register Initialization**
```assembly
# At address 0x00000000:
addi x1, zero, 0        # ra = 0 (return address)
addi x5, zero, 0        # t0 = 0 (temporary)
# ... (all 31 registers zeroed)
```

**Step 2b: Stack Setup**
```assembly
lui sp, %hi(131060)     # sp = 0x00001000 (upper bits)
addi sp, sp, %lo(131060) # sp = 0x0001FFE4 (complete)
```

**Step 2c: Call Application**
```assembly
call my_main            # Jump to 0x00000080, save return to ra
```

### 3. Application Execution (my_main)

**Step 3a: Local Variables**
```c
int32_t first_number = 5;   # Stored on stack
int32_t second_number = 3;  # Stored on stack
```

**Assembly equivalent:**
```assembly
# Function prologue
addi sp, sp, -16        # Allocate stack space
sw ra, 12(sp)           # Save return address

# Initialize local variables
addi t0, zero, 5        # t0 = 5 (first_number)
sw t0, 8(sp)            # Store on stack
addi t1, zero, 3        # t1 = 3 (second_number)
sw t1, 4(sp)            # Store on stack
```

**Step 3b: Function Call**
```c
int32_t sum = add_numbers(first_number, second_number);
```

**Assembly equivalent:**
```assembly
lw a0, 8(sp)            # Load first_number into a0 (arg 0)
lw a1, 4(sp)            # Load second_number into a1 (arg 1)
call add_numbers        # Jump to 0x000000C0
sw a0, 0(sp)            # Store return value (sum) on stack
```

### 4. Addition Function Execution

**Step 4a: Function Entry**
```assembly
# add_numbers prologue
addi sp, sp, -16        # Allocate stack space
sw ra, 12(sp)           # Save return address
sw s0, 8(sp)            # Save frame pointer
addi s0, sp, 16         # Set frame pointer
```

**Step 4b: Computation**
```c
int32_t sum = a + b;    # a is in a0, b is in a1
```

**Assembly equivalent:**
```assembly
add t0, a0, a1          # t0 = a0 + a1 (sum = a + b)
```

**Step 4c: Global Variable Update**
```c
result = sum;           # Update global variable
```

**Assembly equivalent:**
```assembly
lui t1, %hi(0x00000300) # Load upper bits of result address
sw t0, %lo(0x00000300)(t1) # Store sum to result variable
```

**Step 4d: Return Value**
```c
return sum;
```

**Assembly equivalent:**
```assembly
mv a0, t0               # Move sum to return register a0
lw ra, 12(sp)           # Restore return address
lw s0, 8(sp)            # Restore frame pointer
addi sp, sp, 16         # Deallocate stack space
ret                     # Return to caller
```

## AxE-Specific Debugging

### 1. BRAM Content Verification

**Check .hex file loading:**
```bash
# View generated hex file
hexdump -C axe_addition.hex | head -20

# Expected format (Verilog memory format):
@00000000
00000593  # addi x5, zero, 0
00000613  # addi x6, zero, 0
...
```

**Verify BRAM initialization:**
```verilog
// In bram.sv - check initialization
$readmemh("/path/to/axe_addition.hex", mem, 0);
```

### 2. Symbol Table Analysis for AxE

```bash
# List all symbols with addresses
riscv32-unknown-elf-nm -n axe_addition.elf

# Expected output:
00000000 T my_start
00000000 T main
00000080 T my_main
000000c0 T add_numbers
00000300 D result
```

### 3. Disassembly Examination

```bash
# Disassemble entry point
riscv32-unknown-elf-objdump -d axe_addition.elf | head -50

# Check for correct function calls
riscv32-unknown-elf-objdump -d axe_addition.elf | grep "call"
```

### 4. BRAM-Specific Memory Debugging

**Check data section placement:**
```bash
# Show section headers
riscv32-unknown-elf-readelf -S axe_addition.elf

# Look for .data section address
```

**Expected output:**
```
[Nr] Name      Type     Address  Off    Size   ES Flg Lk Inf Al
[ 1] .text     PROGBITS 00000000 001000 000200 00  AX  0   0  4
[ 2] .data     PROGBITS 00000300 001300 000004 00  WA  0   0  4
```

### 5. Runtime Debugging with Verilator

**Trace execution:**
```cpp
// In sim_main.cpp - add debug output
if (main_time % 100 == 0) {
    printf("PC: 0x%08x, Instruction: 0x%08x\n", 
           top->top__DOT__cpu__DOT__pc,
           top->top__DOT__cpu__DOT__instruction);
}
```

**Monitor memory writes:**
```cpp
// Watch writes to result variable (0x00000300)
if (top->top__DOT__memory_write && 
    top->top__DOT__memory_addr == 0x00000300) {
    printf("Writing to result: 0x%08x\n", 
           top->top__DOT__memory_wdata);
}
```

## Key Takeaways for AxE BRAM Systems

### Advantages of BRAM Model
1. **Simplified Boot**: No Flash→RAM copying required
2. **Unified Memory**: Code and data in same address space
3. **Fast Access**: Single-cycle read/write everywhere
4. **Flexible Layout**: Linker has more placement freedom

### AxE-Specific Considerations
1. **Entry Point**: Must be `my_start` (AxE convention)
2. **Stack Address**: Fixed at 131060 (0x0001FFE4)
3. **Register Init**: Zero all registers for clean state
4. **Memory Loading**: Via $readmemh from .hex files

### Debugging Best Practices
1. **Verify .hex**: Check generated memory file format
2. **Symbol Check**: Ensure my_start at address 0x0
3. **Memory Map**: Verify no section overlaps
4. **Runtime Trace**: Monitor PC and memory access

This completes the comprehensive AxE RISC-V linking tutorial demonstrating every aspect of linking in a BRAM-only system!

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-18  
**Author**: Claude AI Assistant  
**Project**: AxE (Approximate eXecution) Framework
