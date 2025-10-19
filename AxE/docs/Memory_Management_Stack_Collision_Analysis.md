# Memory Management: Stack Collision Analysis

## Issue Summary

**Critical Bug Identified**: Stack pointer collision with finish signal address causing premature program termination.

## Problem Description

### Virtual Memory Layout (Per Program View)
```
0x00000000: Program code starts here
    ...
0x00fffffc: Finish signal address (0x1000000 - 4)
0x01000000: Stack pointer start (grows downward)
```

### The Collision
- **Stack grows downward** from `0x1000000` 
- **Finish signal** at `0xfffffc` (only 4 bytes below stack start)
- **Any stack usage** immediately overwrites finish signal address
- **Result**: Program appears to terminate immediately

## Hardware Implementation

### Address Translation System
1. **Programs assume virtual addressing** starting at `0x00000000`
2. **Self-awareness module** adds offset (`axi_offset`) for physical addressing
3. **AXI offset module** (`axi_offset.sv`) performs address translation:
   ```systemverilog
   m_axi.awaddr = s_axi.awaddr + offset;  // Add offset to addresses
   m_axi.araddr = s_axi.araddr + offset;  // For both reads and writes
   ```

### Finish Signal Detection
1. **AXI detector** (`axi_detector.sv`) watches for writes to `0xfffffc`
2. **Detection occurs** at virtual address level (before offset)
3. **Signal flow**: Write to `0xfffffc` → AXI detector → `fin` signal → Self-awareness module

## Software Implementation

### Finish Signal Generation (`start.S` lines 82-86)
```assembly
lui     a5,0x1000        # a5 = 0x1000000
addi    a5,a5,-4         # a5 = 0xfffffc  
lui     a4,0x1000        # a4 = 0x1000000
addi    a4,a4,-4         # a4 = 0xfffffc
sw      a4,0(a5)         # Write 0xfffffc to address 0xfffffc
```

### Stack Pointer Usage
- **Compiled with**: `-DSTACK_POINTER=0x1000000`
- **Stack grows downward** from `0x1000000`
- **First stack access** overwrites finish signal at `0xfffffc`

## Memory Calculations

```
Stack Pointer:     0x01000000 (16,777,216 bytes)
Finish Signal:     0x00fffffc (16,777,212 bytes)
Gap:               4 bytes only
```

**Critical Issue**: Any function call or local variable allocation causes stack collision.

## Current Program Memory Layout

From `prgs.h` analysis:
- **Controller**: Stack pointer `0x2fff8` (196KB)
- **User programs**: Stack pointer `0x1000000` (16MB)  
- **Physical placement**: Programs separated by stack pointer size to prevent interference

## Solutions Implemented

### 1. Reduce Stack Pointer Size
**Change**: Set stack pointer to safe distance from finish signal
```c
// Before: STACK_POINTER=0x1000000 (collision with 0xfffffc)
// After:  STACK_POINTER=0x0f0000   (safe 64KB gap)
```

### 2. Alternative: Move Finish Signal
**Option**: Relocate finish signal to different address range
- Move to I/O mapped region (e.g., `0x10000000`)
- Update both hardware detector and software finish code

## Documentation Updates

### Files Modified
1. **This document**: New analysis of memory management issue
2. **COMPREHENSIVE_SYSTEM_ANALYSIS.md**: Updated memory layout section
3. **Implementation notes**: Added to relevant build documentation

### Hardware Components Affected
- `axi_detector.sv`: Finish signal detection
- `axi_offset.sv`: Address translation
- `self_awareness.sv`: Program lifecycle management

### Software Components Affected  
- `start.S`: Finish signal generation
- `Makefile_nostart`: Stack pointer compilation
- Memory packing system: Stack sizing calculations

## Verification Steps

1. **Compile with reduced stack pointer**
2. **Verify program runs to completion**
3. **Test stack usage doesn't trigger false termination**
4. **Validate address translation still works correctly**

## Best Practices for Memory Management

1. **Stack sizing**: Allow adequate gap between stack and critical addresses
2. **Address layout**: Design memory map with clear separation
3. **Virtual addressing**: Maintain consistent program view across nodes
4. **Testing**: Verify memory usage patterns don't cause collisions

---

**Date**: Current session
**Priority**: Critical - affects program execution reliability
**Status**: Analysis complete, solution implemented