# RISC-V Linking Step-by-Step Example

## Executive Summary

This document provides a concrete, step-by-step walkthrough of the RISC-V linking process using a realistic embedded system example. We'll follow a simple LED blink program from source code to final executable, showing exactly what happens at each stage.

## Table of Contents

1. [Hardware Setup](#hardware-setup)
2. [Program Overview](#program-overview)
3. [Source Code Files](#source-code-files)
4. [Compilation Process](#compilation-process)
5. [Linking Process Detailed](#linking-process-detailed)
6. [Memory Layout Analysis](#memory-layout-analysis)
7. [Execution Flow](#execution-flow)
8. [Troubleshooting Example](#troubleshooting-example)

## Hardware Setup

### Target Hardware: Simple RISC-V Microcontroller

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
│          Memory Map                 │
│                                     │
│ 0x20001000 ├─────────────────┤     │
│            │      Stack      │     │
│ 0x20000800 ├─────────────────┤     │
│            │       RAM       │     │
│ 0x20000000 ├─────────────────┤     │
│            │       ...       │     │
│ 0x10000000 ├─────────────────┤     │
│            │   Peripherals   │     │
│            │   (GPIO, etc.)  │     │
│ 0x00001000 ├─────────────────┤     │
│            │       ...       │     │
│ 0x00000100 ├─────────────────┤     │
│            │   Boot/Reset    │     │
│ 0x00000000 └─────────────────┘     │
└─────────────────────────────────────┘
```

### Hardware Specifications
- **CPU**: 32-bit RISC-V (RV32IM)
- **Flash**: 4KB starting at 0x00000000 
- **RAM**: 2KB starting at 0x20000000
- **GPIO**: Memory-mapped at 0x10000000
- **Reset Vector**: 0x00000000 (hardware jumps here on reset)
- **Stack**: Grows down from 0x20001000

## Program Overview

We'll create a simple LED blink program with these components:

```
Project Structure:
led_blink/
├── startup.S      (assembly startup code)
├── main.c         (main application)
├── gpio.c         (GPIO driver)
├── gpio.h         (GPIO header)
├── Makefile       (build script)
└── linker.ld      (memory layout)
```

**Goal**: Make an LED connected to GPIO pin 5 blink every second.

## Source Code Files

### 1. startup.S (Assembly Startup Code)

```assembly
# startup.S - Hardware initialization and entry point
.section .text.start
.global _start
.global _reset_handler

# This is where hardware jumps on reset
_start:
_reset_handler:
    # Step 1: Initialize stack pointer
    # Hardware spec: Stack at top of RAM (0x20001000)
    lui sp, %hi(0x20001000)    # Load upper immediate
    addi sp, sp, %lo(0x20001000) # Add lower immediate
    
    # Step 2: Zero out BSS section (uninitialized variables)
    la t0, __bss_start         # Load BSS start address
    la t1, __bss_end           # Load BSS end address
    
bss_loop:
    beq t0, t1, bss_done       # If start == end, we're done
    sw zero, 0(t0)             # Store zero at current address
    addi t0, t0, 4             # Move to next word
    j bss_loop                 # Repeat
    
bss_done:
    # Step 3: Copy initialized data from flash to RAM
    la t0, __data_start        # RAM destination
    la t1, __data_end          # RAM end
    la t2, __data_load         # Flash source
    
data_loop:
    beq t0, t1, data_done      # If start == end, we're done
    lw t3, 0(t2)               # Load from flash
    sw t3, 0(t0)               # Store to RAM
    addi t0, t0, 4             # Next RAM address
    addi t2, t2, 4             # Next flash address
    j data_loop                # Repeat
    
data_done:
    # Step 4: Call main function
    call main                  # Jump to main() and save return address
    
    # Step 5: If main returns, halt
halt_loop:
    j halt_loop                # Infinite loop
```

### 2. gpio.h (GPIO Driver Header)

```c
// gpio.h - GPIO driver interface
#ifndef GPIO_H
#define GPIO_H

#include <stdint.h>

// Hardware addresses (from hardware manual)
#define GPIO_BASE_ADDR    0x10000000
#define GPIO_OUTPUT_REG   (GPIO_BASE_ADDR + 0x00)
#define GPIO_DIRECTION_REG (GPIO_BASE_ADDR + 0x04)

// GPIO pin definitions
#define LED_PIN 5

// Function declarations
void gpio_init(void);
void gpio_set_pin(int pin);
void gpio_clear_pin(int pin);

#endif
```

### 3. gpio.c (GPIO Driver Implementation)

```c
// gpio.c - GPIO driver implementation
#include "gpio.h"

// Global variable (goes in .data section)
static uint32_t gpio_state = 0;

void gpio_init(void) {
    // Set LED pin as output
    volatile uint32_t *direction_reg = (uint32_t*)GPIO_DIRECTION_REG;
    *direction_reg |= (1 << LED_PIN);
}

void gpio_set_pin(int pin) {
    volatile uint32_t *output_reg = (uint32_t*)GPIO_OUTPUT_REG;
    *output_reg |= (1 << pin);
    gpio_state |= (1 << pin);  // Update our state
}

void gpio_clear_pin(int pin) {
    volatile uint32_t *output_reg = (uint32_t*)GPIO_OUTPUT_REG;
    *output_reg &= ~(1 << pin);
    gpio_state &= ~(1 << pin);  // Update our state
}
```

### 4. main.c (Main Application)

```c
// main.c - Main application
#include "gpio.h"

// Function to create delay (simple loop)
void delay(int count) {
    volatile int i;
    for (i = 0; i < count; i++) {
        // Just waste time
    }
}

int main(void) {
    // Initialize GPIO system
    gpio_init();
    
    // Main loop
    while (1) {
        gpio_set_pin(LED_PIN);    // Turn LED on
        delay(100000);            // Wait
        gpio_clear_pin(LED_PIN);  // Turn LED off
        delay(100000);            // Wait
    }
    
    return 0;  // Never reached
}
```

### 5. linker.ld (Linker Script)

```ld
/* linker.ld - Memory layout definition */

/* Define memory regions (from hardware manual) */
MEMORY {
    FLASH (rx)  : ORIGIN = 0x00000000, LENGTH = 4K
    RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 2K
}

/* Entry point (where execution starts) */
ENTRY(_start)

/* Define sections */
SECTIONS {
    /* Code section - goes in FLASH */
    .text : {
        KEEP(*(.text.start))    /* Startup code MUST be first */
        *(.text)                /* All other code */
        *(.text.*)              /* Code in named subsections */
    } > FLASH
    
    /* Read-only data - goes in FLASH */
    .rodata : {
        *(.rodata)
        *(.rodata.*)
    } > FLASH
    
    /* Initialized data - stored in FLASH, copied to RAM */
    .data : {
        __data_start = .;       /* Mark start of data in RAM */
        *(.data)
        *(.data.*)
        __data_end = .;         /* Mark end of data in RAM */
    } > RAM AT > FLASH          /* Lives in RAM, stored in FLASH */
    
    /* Store where data is located in FLASH */
    __data_load = LOADADDR(.data);
    
    /* Uninitialized data - goes in RAM */
    .bss : {
        __bss_start = .;        /* Mark start of BSS */
        *(.bss)
        *(.bss.*)
        *(COMMON)
        __bss_end = .;          /* Mark end of BSS */
    } > RAM
    
    /* Stack location */
    PROVIDE(__stack_top = ORIGIN(RAM) + LENGTH(RAM));
}
```

### 6. Makefile (Build Script)

```makefile
# Makefile - Build script
CC = riscv32-unknown-elf-gcc
OBJCOPY = riscv32-unknown-elf-objcopy
OBJDUMP = riscv32-unknown-elf-objdump

CFLAGS = -march=rv32im -mabi=ilp32 -O2 -Wall
LDFLAGS = -T linker.ld -nostartfiles

SOURCES = startup.S main.c gpio.c
OBJECTS = $(SOURCES:.c=.o)
OBJECTS := $(OBJECTS:.S=.o)

TARGET = led_blink

all: $(TARGET).elf $(TARGET).bin $(TARGET).hex

# Link all objects into final executable
$(TARGET).elf: $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $(OBJECTS)

# Convert ELF to binary (for flash programming)
$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

# Convert ELF to hex (for simulation)
$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

# Compile C files
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

# Assemble assembly files
%.o: %.S
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f *.o *.elf *.bin *.hex

.PHONY: all clean
```

## Compilation Process

Let's trace through what happens when we run `make`:

### Step 1: Compile startup.S

```bash
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -Wall -c -o startup.o startup.S
```

**What happens:**
1. **Preprocessing**: Include files processed, macros expanded
2. **Assembly**: Assembly code converted to machine instructions
3. **Object Creation**: `startup.o` created with:
   - Machine code for each instruction
   - Symbol table (`_start`, `_reset_handler`, etc.)
   - Relocation information (addresses to be fixed later)

**startup.o contents:**
```
Symbol Table:
_start          (global, undefined address)
_reset_handler  (global, undefined address)
__bss_start     (undefined - from linker script)
__bss_end       (undefined - from linker script)
main            (undefined - from main.c)

Code Section:
00000000: 200011b7  # lui sp, %hi(0x20001000)
00000004: 00018113  # addi sp, sp, %lo(0x20001000)
...
```

### Step 2: Compile main.c

```bash
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -Wall -c -o main.o main.c
```

**What happens:**
1. **Preprocessing**: `#include "gpio.h"` brings in definitions
2. **Compilation**: C code converted to assembly
3. **Assembly**: Assembly converted to machine code
4. **Object Creation**: `main.o` created

**main.o contents:**
```
Symbol Table:
main            (global, undefined address)
delay           (local, undefined address)
gpio_init       (undefined - from gpio.c)
gpio_set_pin    (undefined - from gpio.c)
gpio_clear_pin  (undefined - from gpio.c)

Code Section:
00000000: ff010113  # addi sp,sp,-16 (function prologue)
00000004: 00112623  # sw ra,12(sp)
...
```

### Step 3: Compile gpio.c

```bash
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -Wall -c -o gpio.o gpio.c
```

**gpio.o contents:**
```
Symbol Table:
gpio_init       (global, undefined address)
gpio_set_pin    (global, undefined address)
gpio_clear_pin  (global, undefined address)
gpio_state      (local, in .data section)

Data Section:
00000000: 00000000  # gpio_state = 0

Code Section:
00000000: ff010113  # gpio_init function start
...
```

## Linking Process Detailed

Now the crucial part - linking! The linker (`ld`) combines all objects:

```bash
riscv32-unknown-elf-gcc -T linker.ld -nostartfiles -o led_blink.elf startup.o main.o gpio.o
```

### Phase 1: Symbol Collection

The linker scans all object files and builds a global symbol table:

```
Global Symbol Table:
┌─────────────────┬─────────┬─────────────┐
│ Symbol Name     │ File    │ Status      │
├─────────────────┼─────────┼─────────────┤
│ _start          │startup.o│ defined     │
│ _reset_handler  │startup.o│ defined     │
│ main            │ main.o  │ defined     │
│ delay           │ main.o  │ defined     │
│ gpio_init       │ gpio.o  │ defined     │
│ gpio_set_pin    │ gpio.o  │ defined     │
│ gpio_clear_pin  │ gpio.o  │ defined     │
│ gpio_state      │ gpio.o  │ defined     │
└─────────────────┴─────────┴─────────────┘
```

### Phase 2: Memory Layout (Using Linker Script)

The linker reads `linker.ld` and creates memory layout:

```
Memory Assignment:
┌─────────────┬──────────────┬───────────────┐
│ Section     │ Address      │ Content       │
├─────────────┼──────────────┼───────────────┤
│ .text       │ 0x00000000   │ Code          │
│   .text.start│ 0x00000000   │ startup.o     │
│   .text     │ 0x00000040   │ main.o, gpio.o│
│ .rodata     │ 0x00000200   │ Constants     │
│ .data       │ 0x20000000   │ Initialized   │
│ .bss        │ 0x20000004   │ Uninitialized │
└─────────────┴──────────────┴───────────────┘
```

### Phase 3: Address Assignment

Now the linker assigns actual addresses to all symbols:

```
Final Symbol Addresses:
┌─────────────────┬──────────────┐
│ Symbol Name     │ Address      │
├─────────────────┼──────────────┤
│ _start          │ 0x00000000   │ ← Entry point!
│ _reset_handler  │ 0x00000000   │ ← Same as _start
│ main            │ 0x00000040   │
│ delay           │ 0x00000080   │
│ gpio_init       │ 0x000000C0   │
│ gpio_set_pin    │ 0x00000100   │
│ gpio_clear_pin  │ 0x00000140   │
│ gpio_state      │ 0x20000000   │
│ __bss_start     │ 0x20000004   │
│ __bss_end       │ 0x20000004   │
│ __data_start    │ 0x20000000   │
│ __data_end      │ 0x20000004   │
│ __data_load     │ 0x00000300   │
└─────────────────┴──────────────┘
```

### Phase 4: Relocation

The linker fixes all address references in the code:

**Before relocation (in startup.o):**
```assembly
call main      # Address unknown - marked for relocation
```

**After relocation (in led_blink.elf):**
```assembly
call main      # Now becomes: call 0x00000040
```

**Example relocation in startup.S:**
```assembly
# Original code:
la t0, __bss_start     # Load address of __bss_start

# Becomes:
lui t0, %hi(0x20000004)    # Load upper 20 bits
addi t0, t0, %lo(0x20000004) # Add lower 12 bits
```

## Memory Layout Analysis

Let's examine the final memory layout:

### Final Memory Map

```
FLASH (0x00000000 - 0x00000FFF):
┌─────────────────┐ 0x00000FFF
│    (unused)     │
├─────────────────┤ 0x00000304
│ gpio_state init │ 0x00000300 ← __data_load
│ value (0x0000)  │
├─────────────────┤ 0x000002FF
│   (padding)     │
├─────────────────┤ 0x00000200
│   .rodata       │ (constants, if any)
├─────────────────┤ 0x00000180
│ gpio_clear_pin  │ 0x00000140
├─────────────────┤ 0x00000140
│ gpio_set_pin    │ 0x00000100
├─────────────────┤ 0x00000100
│ gpio_init       │ 0x000000C0
├─────────────────┤ 0x000000C0
│ delay function  │ 0x00000080
├─────────────────┤ 0x00000080
│ main function   │ 0x00000040
├─────────────────┤ 0x00000040
│ startup code    │ 0x00000000 ← _start (entry point)
└─────────────────┘

RAM (0x20000000 - 0x200007FF):
┌─────────────────┐ 0x20001000 ← __stack_top
│                 │ ↓ Stack grows down
│     Stack       │
│                 │
├─────────────────┤ 0x20000400
│    (unused)     │
├─────────────────┤ 0x20000004
│ .bss (empty)    │ 0x20000004 ← __bss_start = __bss_end
├─────────────────┤ 0x20000004
│ gpio_state      │ 0x20000000 ← Copied from FLASH
└─────────────────┘
```

### Why This Layout?

1. **_start at 0x00000000**: Hardware jumps here on reset
2. **Code in FLASH**: Non-volatile, survives power cycles
3. **Data in RAM**: Fast access, modifiable
4. **Stack at top**: Grows down, won't collide with data

## Execution Flow

Now let's trace what happens when the microcontroller powers on:

### 1. Hardware Reset
```
CPU State:
PC (Program Counter) = 0x00000000
SP (Stack Pointer)   = undefined
All registers        = undefined
```

### 2. Startup Execution

**Step 2a: First Instruction**
```assembly
# At address 0x00000000:
lui sp, %hi(0x20001000)    # SP = 0x20001000 (upper bits)
```

**Step 2b: Complete Stack Setup**
```assembly
# At address 0x00000004:
addi sp, sp, %lo(0x20001000) # SP = 0x20001000 (complete)
```

**Step 2c: Initialize BSS (skipped - empty)**
```assembly
la t0, __bss_start     # t0 = 0x20000004
la t1, __bss_end       # t1 = 0x20000004
beq t0, t1, bss_done   # Equal, so skip loop
```

**Step 2d: Copy Data from FLASH to RAM**
```assembly
la t0, __data_start    # t0 = 0x20000000 (RAM destination)
la t1, __data_end      # t1 = 0x20000004 (RAM end)  
la t2, __data_load     # t2 = 0x00000300 (FLASH source)

# Loop copies gpio_state from FLASH to RAM
lw t3, 0(t2)           # Load 0x00000000 from FLASH
sw t3, 0(t0)           # Store to RAM at 0x20000000
```

**Step 2e: Call Main**
```assembly
call main              # Jump to 0x00000040, save return in ra
```

### 3. Main Function Execution

**Step 3a: GPIO Initialization**
```c
gpio_init();           # Jump to 0x000000C0
```

**Step 3b: Main Loop**
```c
while (1) {
    gpio_set_pin(LED_PIN);    # Jump to 0x00000100
    delay(100000);            # Jump to 0x00000080  
    gpio_clear_pin(LED_PIN);  # Jump to 0x00000140
    delay(100000);            # Jump to 0x00000080
}
```

### 4. GPIO Operations

**gpio_set_pin(5) execution:**
```c
volatile uint32_t *output_reg = (uint32_t*)0x10000000;
*output_reg |= (1 << 5);      # Hardware register write
gpio_state |= (1 << 5);       # Update RAM at 0x20000000
```

## Troubleshooting Example

Let's say our LED doesn't blink. Here's how to debug using linking knowledge:

### Problem: LED Never Turns On

**Step 1: Check if main() is called**
```bash
# Disassemble to see if startup calls main correctly
riscv32-unknown-elf-objdump -d led_blink.elf | grep -A5 "call.*main"
```

Expected output:
```
40: 001000ef    call 40 <main>
```

**Step 2: Check GPIO addresses**
```bash
# Check if GPIO_BASE_ADDR is correct
riscv32-unknown-elf-objdump -d led_blink.elf | grep -A10 "gpio_set_pin"
```

Look for:
```
100: 10000537    lui a0,0x10000    # Should be 0x10000000
```

**Step 3: Check data initialization**
```bash
# Verify gpio_state is in correct section
riscv32-unknown-elf-readelf -S led_blink.elf | grep data
```

**Step 4: Check memory layout**
```bash
# Generate map file to see all symbols
riscv32-unknown-elf-gcc -Wl,-Map=led_blink.map ...
cat led_blink.map | grep gpio_state
```

### Problem: System Doesn't Start

**Symptom**: No activity at all

**Check 1: Entry Point**
```bash
riscv32-unknown-elf-readelf -h led_blink.elf | grep Entry
```
Should show: `Entry point address: 0x0`

**Check 2: First Instruction**
```bash
riscv32-unknown-elf-objdump -d led_blink.elf | head -10
```
Should show code at address 0x00000000

**Check 3: Stack Pointer**
```bash
# Look at first few instructions
riscv32-unknown-elf-objdump -d led_blink.elf | head -5
```
Should show stack pointer setup as first operations.

## Key Takeaways

### Why Linking Order Matters
1. **startup.o must be first**: Ensures _start is at address 0x00000000
2. **Library order**: Last libraries should resolve symbols from earlier objects
3. **Section ordering**: `.text.start` must come before `.text`

### What Linker Scripts Control
1. **Memory layout**: Where each section goes
2. **Symbol definitions**: Creating symbols like `__bss_start`
3. **Entry point**: Which symbol is the program start
4. **Section ordering**: Critical for embedded systems

### Common Mistakes
1. **Wrong entry point**: Hardware jumps to 0x0, but code isn't there
2. **Missing initialization**: BSS not zeroed, data not copied
3. **Stack not set**: Crashes on first function call
4. **Wrong memory regions**: Code in RAM, data in ROM

This example shows exactly how the linker transforms your source code into a working embedded program, and how each piece fits together in memory.