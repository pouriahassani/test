# RISC-V Linking Comprehensive Guide

## Executive Summary

This document provides a complete understanding of linking in embedded RISC-V systems, covering fundamental concepts, best practices, and troubleshooting techniques. It addresses the specific challenges encountered in the AxE project's controller linking issues.

## Table of Contents

1. [Introduction to Linking](#introduction-to-linking)
2. [RISC-V Linking Fundamentals](#risc-v-linking-fundamentals)
3. [Linker Scripts and Memory Layout](#linker-scripts-and-memory-layout)
4. [Entry Points and Symbol Resolution](#entry-points-and-symbol-resolution)
5. [Best Practices for Embedded Systems](#best-practices-for-embedded-systems)
6. [Common Linking Problems and Solutions](#common-linking-problems-and-solutions)
7. [AxE Project Specific Analysis](#axe-project-specific-analysis)
8. [Debugging Techniques](#debugging-techniques)
9. [References and Further Reading](#references-and-further-reading)

## Introduction to Linking

### What is Linking?

Linking is the process of combining multiple object files and libraries into a single executable program. The linker resolves symbol references, assigns memory addresses, and creates the final executable format.

### Types of Linking

1. **Static Linking**: All code is combined at compile time
2. **Dynamic Linking**: Code is linked at runtime (not common in embedded systems)
3. **Relocatable Linking**: Creates object files that can be further linked

### Key Concepts

- **Symbol**: A name representing a memory location (function, variable, label)
- **Symbol Table**: Database of all symbols and their properties
- **Relocation**: Process of adjusting addresses in the final executable
- **Entry Point**: First instruction executed when program starts

## RISC-V Linking Fundamentals

### RISC-V Memory Model

```
┌─────────────────┐ ← High Memory (0xFFFFFFFF)
│     Stack       │ ↓ (grows downward)
├─────────────────┤
│       ...       │
├─────────────────┤
│     Heap        │ ↑ (grows upward)
├─────────────────┤
│      BSS        │ (uninitialized data)
├─────────────────┤
│     Data        │ (initialized data)
├─────────────────┤
│     Text        │ (code)
└─────────────────┘ ← Low Memory (0x00000000)
```

### RISC-V ABI (Application Binary Interface)

- **Register Usage**: Standard calling conventions
- **Stack Management**: Frame pointer and stack pointer usage
- **Function Calls**: Parameter passing and return values
- **Symbol Naming**: Standard naming conventions

### Address Spaces in Embedded Systems

```
Physical Memory Layout:
┌─────────────────┐ 0x80000000
│   Main RAM      │
├─────────────────┤ 0x10000000
│   Peripherals   │
├─────────────────┤ 0x02000000
│   Boot ROM      │
└─────────────────┘ 0x00000000
```

## Linker Scripts and Memory Layout

### What are Linker Scripts?

Linker scripts (`.ld` files) define how sections are placed in memory. They control:
- Memory layout
- Section placement
- Symbol definitions
- Entry point specification

### Basic Linker Script Structure

```ld
/* Memory definition */
MEMORY {
    ROM (rx)  : ORIGIN = 0x00000000, LENGTH = 64K
    RAM (rwx) : ORIGIN = 0x20000000, LENGTH = 16K
}

/* Entry point */
ENTRY(_start)

/* Section definitions */
SECTIONS {
    .text : {
        *(.text)
        *(.text.*)
    } > ROM
    
    .data : {
        *(.data)
        *(.data.*)
    } > RAM AT > ROM
    
    .bss : {
        *(.bss)
        *(.bss.*)
    } > RAM
}
```

### Common Linker Script Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| `ENTRY()` | Set entry point | `ENTRY(_start)` |
| `MEMORY` | Define memory regions | `ROM : ORIGIN = 0x0, LENGTH = 64K` |
| `SECTIONS` | Define section layout | `.text : { *(.text) } > ROM` |
| `PROVIDE()` | Provide symbol if undefined | `PROVIDE(__stack_top = 0x20004000)` |
| `ALIGN()` | Align to boundary | `ALIGN(4)` |

## Entry Points and Symbol Resolution

### Entry Point Mechanisms

1. **Linker Entry Point**: Specified with `-e` flag or `ENTRY()` directive
2. **Reset Vector**: Hardware-defined startup address
3. **Boot Sequence**: Chain of startup functions

### Symbol Resolution Process

```
1. Collect all object files and libraries
2. Build symbol table from all sources
3. Resolve undefined symbols
4. Apply relocations
5. Generate final executable
```

### Symbol Types

- **Global Symbols**: Visible across all files
- **Local Symbols**: Visible only within file
- **Weak Symbols**: Can be overridden by strong symbols
- **Common Symbols**: Uninitialized global variables

### Best Practices for Symbol Management

```c
// Good: Clear, descriptive names
extern void hardware_init(void);
void application_main(void);

// Bad: Generic, unclear names
extern void init(void);
void main(void);
```

## Best Practices for Embedded Systems

### 1. Consistent Entry Point Strategy

```assembly
# startup.S
.section .text.start
.global _start
_start:
    # Hardware initialization
    call hardware_init
    # Application entry
    call main
    # Halt on return
1:  j 1b
```

### 2. Proper Section Organization

```c
// Place critical code in specific sections
__attribute__((section(".text.boot")))
void boot_code(void) { /* ... */ }

// Place data in specific sections
__attribute__((section(".data.config")))
const config_t system_config = { /* ... */ };
```

### 3. Memory Layout Planning

```
┌─────────────────┐ 0x00002000
│   Application   │
├─────────────────┤ 0x00001000
│   Libraries     │
├─────────────────┤ 0x00000100
│   Boot Code     │
├─────────────────┤ 0x00000010
│   Vector Table  │
└─────────────────┘ 0x00000000
```

### 4. Stack Pointer Management

```c
// Define stack in linker script
extern uint32_t __stack_top;

// Initialize in startup code
void _start(void) {
    // Set stack pointer
    asm volatile("mv sp, %0" : : "r"(&__stack_top));
    // Continue with initialization
    main();
}
```

## Common Linking Problems and Solutions

### 1. Undefined Symbol Errors

**Problem**: `undefined reference to 'symbol_name'`

**Causes**:
- Missing object file or library
- Misspelled symbol name
- Wrong symbol scope

**Solutions**:
```bash
# Check symbol presence
objdump -t file.o | grep symbol_name

# Check symbol type
readelf -s file.o | grep symbol_name

# Add missing library
gcc ... -lmissing_library
```

### 2. Entry Point Issues

**Problem**: Wrong entry point or execution starts at wrong address

**Causes**:
- Incorrect `-e` flag
- Missing or wrong `ENTRY()` directive
- Hardware reset vector mismatch

**Solutions**:
```bash
# Check entry point
readelf -h executable.elf | grep Entry

# Set correct entry point
gcc -Wl,-e,correct_entry_point ...

# Verify with objdump
objdump -d executable.elf | head -20
```

### 3. Section Placement Problems

**Problem**: Code/data in wrong memory regions

**Causes**:
- Incorrect linker script
- Wrong section attributes
- Memory overflow

**Solutions**:
```bash
# Check section placement
readelf -S executable.elf

# Verify memory usage
size executable.elf

# Check for overlaps
objdump -h executable.elf
```

### 4. Symbol Collision

**Problem**: Multiple definitions of same symbol

**Causes**:
- Duplicate function definitions
- Library conflicts
- Weak symbol issues

**Solutions**:
```bash
# Find duplicate symbols
nm executable.elf | sort | uniq -d

# Check symbol binding
readelf -s executable.elf | grep GLOBAL
```

## AxE Project Specific Analysis

### Current Problem Analysis

Based on our investigation, the AxE project controller has the following linking issues:

#### Issue 1: Entry Point Mismatch
```
Makefile specifies: -Wl,-e,my_start
start.S defines: main (not my_start)
Result: Linker defaults to address 0x0, but wrong function executes
```

#### Issue 2: Symbol Resolution Order
```
Object file order: start.S, memmgr.c, print.c, util.c, main.c, -lm
Library -lm pulls in: exit, _start, register_fini, etc.
Result: Standard library functions placed at low addresses
```

#### Issue 3: Missing Startup Coordination
```
Hardware expects: Execution starts at 0x0
Current layout: exit() function at 0x0, main() at 0xfc
Required: main() or my_start at 0x0
```

### Root Cause Analysis

1. **Historical Mismatch**: Original code expected `my_start` symbol
2. **Library Integration**: Math library adds unwanted startup code
3. **Linker Script Absence**: No explicit memory layout control

### Proposed Solutions

#### Solution 1: Fix Symbol Definitions (RECOMMENDED)
```assembly
# In start.S
.global my_start
my_start:
    # Initialize registers
    # Set stack pointer
    # Call my_main
```

#### Solution 2: Custom Linker Script
```ld
ENTRY(my_start)
SECTIONS {
    .text : {
        *start.o(.text)  /* Place start.S first */
        *(.text)
    }
}
```

#### Solution 3: Object File Ordering
```makefile
# Place startup code first
$(CC) ... start.S main.c $(SRC) -lm
```

### AxE-Specific Analysis (BRAM Systems)

The AxE project uses a unique BRAM-only memory model that simplifies many linking challenges:

#### BRAM vs Traditional Embedded Differences

| Aspect | Traditional (Flash+RAM) | AxE (BRAM Only) |
|--------|------------------------|-----------------|
| **Memory Model** | Separate Flash/RAM | Unified BRAM |
| **Code Storage** | Flash (read-only) | BRAM (read/write) |
| **Data Copying** | Flash→RAM at boot | No copying needed |
| **Entry Point** | Hardware-fixed | Flexible placement |
| **Stack Setup** | Critical for RAM | Simplified |

#### AxE Linking Advantages

1. **Simplified Boot Sequence**: No complex data copying from Flash to RAM
2. **Unified Address Space**: Code and data in same memory region
3. **Fast Access**: Single-cycle access to all memory
4. **Flexible Layout**: Linker has more placement options

#### AxE-Specific Conventions

```assembly
# AxE startup pattern (from sw/_libs/start.S)
.section .text
.global my_start
.global main

my_start:
main:
    # Zero all registers (AxE convention)
    addi x1, zero, 0
    addi x5, zero, 0
    # ... (all registers)
    
    # Set AxE-specific stack address
    lui sp, %hi(131060)      # 0x0001FFE4
    addi sp, sp, %lo(131060)
    
    # Call application entry point
    call my_main
```

#### BRAM Memory Layout Example

```
BRAM Address Space (AxE):
┌─────────────────┐ 0x0199999C
│    (unused)     │
├─────────────────┤ 0x0001FFE4 ← Stack top
│     Stack       │ ↓ grows down
├─────────────────┤ 0x00010000
│   Variables     │ (.data, .bss)
├─────────────────┤ 0x00001000
│   Functions     │ (user code)
├─────────────────┤ 0x00000100
│   Startup       │ (my_start)
└─────────────────┘ 0x00000000 ← Entry point
```

For detailed AxE-specific linking tutorial, see: `docs/AxE_RISC-V_Linking_Tutorial.md`

### Implementation History

| Version | Entry Point | Status | Issues |
|---------|-------------|--------|--------|
| Original | `my_start` | Working | Symbol not found warning |
| Modified | `main` | Broken | Wrong address (0xfc) |
| Fixed | `my_start` | Working | Proper symbol definition |

## Debugging Techniques

### 1. Symbol Table Analysis
```bash
# List all symbols
nm -n executable.elf

# Show symbol types
objdump -t executable.elf

# Check undefined symbols
nm -u executable.elf
```

### 2. Disassembly Examination
```bash
# Disassemble entry point
objdump -d -j .text executable.elf | head -50

# Show specific function
objdump -d executable.elf | grep -A 20 "main>:"

# Display with source
objdump -S executable.elf
```

### 3. Memory Layout Verification
```bash
# Show section headers
readelf -S executable.elf

# Display program headers
readelf -l executable.elf

# Check memory usage
size executable.elf
```

### 4. Linking Process Debugging
```bash
# Verbose linking
gcc -Wl,--verbose ...

# Generate map file
gcc -Wl,-Map=output.map ...

# Cross-reference table
gcc -Wl,--cref ...
```

### 5. Runtime Debugging
```bash
# GDB startup
(gdb) target remote :3333
(gdb) load
(gdb) monitor reset halt
(gdb) info registers
```

## Best Practices Summary

### 1. Project Organization
- Use consistent naming conventions
- Separate startup code from application
- Document memory layout clearly
- Version control linker scripts

### 2. Build System
- Explicit object file ordering
- Conditional library linking
- Automated verification steps
- Clear error messaging

### 3. Documentation
- Document entry point strategy
- Explain memory layout
- Provide debugging guides
- Maintain change history

### 4. Testing
- Verify entry point execution
- Test memory boundaries
- Validate symbol resolution
- Check cross-compilation

## Troubleshooting Checklist

### Entry Point Issues
- [ ] Verify entry point symbol exists
- [ ] Check linker command line flags
- [ ] Confirm hardware reset vector
- [ ] Test with minimal example

### Symbol Resolution
- [ ] Check for undefined symbols
- [ ] Verify library order
- [ ] Look for symbol conflicts
- [ ] Validate weak symbols

### Memory Layout
- [ ] Check section placement
- [ ] Verify stack location
- [ ] Test memory boundaries
- [ ] Validate alignment

### Build Process
- [ ] Check compiler flags
- [ ] Verify object file order
- [ ] Test clean builds
- [ ] Validate dependencies

## References and Further Reading

### Official Documentation
- [RISC-V Assembly Programmer's Handbook](https://github.com/riscv-non-isa/riscv-asm-manual)
- [GNU Binutils Documentation](https://sourceware.org/binutils/docs/)
- [GCC Cross-Compilation Guide](https://gcc.gnu.org/onlinedocs/)

### Technical Standards
- RISC-V ELF psABI Specification
- System V ABI RISC-V Processor Supplement
- IEEE Std 1003.1 (POSIX)

### Best Practice Guides
- Embedded Systems Linker Script Tutorial
- RISC-V Embedded Development Guide
- Cross-Compilation Best Practices

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-18  
**Author**: Claude AI Assistant  
**Project**: AxE (Approximate eXecution) Framework