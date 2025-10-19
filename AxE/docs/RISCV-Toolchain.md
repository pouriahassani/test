# RISC-V Toolchain Guide for AxE Development

## 📖 Table of Contents
1. [Overview](#overview)
2. [Understanding RISC-V Architecture](#understanding-risc-v-architecture)
3. [Cross-Compilation Fundamentals](#cross-compilation-fundamentals)
4. [Multilib Support](#multilib-support)
5. [Compilation Examples](#compilation-examples)
6. [Debugging with GDB](#debugging-with-gdb)
7. [AxE-Specific Development](#axe-specific-development)
8. [Build System Integration](#build-system-integration)
9. [Troubleshooting](#troubleshooting)
10. [External Resources](#external-resources)

---

## Overview

This guide provides comprehensive coverage of the RISC-V GNU toolchain specifically configured for AxE (Approximate eXecution) project development. The AxE project uses a unified toolchain approach with multilib support to handle both exact and approximate computing cores efficiently.

**🔗 Related Documentation:**
- **[Docker Tutorial](Docker-Tutorial.md#risc-v-toolchain-axe-optimized-build)** - How this toolchain is built in our Docker environment
- **[Build System Guide](Build-System.md)** - Integration with AxE's Makefile system
- **[AxE Overview](AxE-Overview.md)** - Project context and research background

### 🎯 **What You'll Learn**
- How to use the unified RISC-V toolchain installed at `/opt/riscv`
- Cross-compilation for embedded RISC-V targets
- Architecture-specific compilation for AxE's heterogeneous cores
- Debugging techniques for bare-metal RISC-V programs
- Integration with AxE's build system

---

## Understanding RISC-V Architecture

### 🔧 **Modular Architecture System**

RISC-V uses a modular approach where each letter represents an extension:

- **RV32I**: Base 32-bit integer instruction set (mandatory)
- **RV32IM**: Base + **M**ultiplication/division extension  
- **RV32IMC**: + **C**ompressed instructions (16-bit for code density)
- **RV32IMF**: + **F**loating-point (single precision)
- **RV32IMFD**: + **D**ouble-precision floating-point

### 🎯 **AxE Architecture Context**

**AxE's Heterogeneous Design:**
- **PicoRV32**: Exact cores (RV32I - no hardware multiplication)
- **PiXoRV32**: Approximate cores (RV32IM - with approximate multiplication)

**Why This Matters:**
- Different cores need different instruction sets
- Exact cores: Software multiplication (smaller, lower power)
- Approximate cores: Hardware multiplication (faster, energy-accuracy trade-offs)

---

## Cross-Compilation Fundamentals

### 🔍 **Key Concepts**

**Target Triple:** `riscv32-unknown-elf`
- **riscv32**: 32-bit RISC-V architecture
- **unknown**: No specific vendor
- **elf**: Executable and Linkable Format (bare-metal)

**ABI (Application Binary Interface):** `ilp32`
- **i**: int = 32-bit
- **l**: long = 32-bit  
- **p**: pointer = 32-bit

**Sysroot:** `/opt/riscv/riscv32-unknown-elf/`
- Root directory for target system libraries and headers

### 🛠️ **Toolchain Components**

```bash
# Core compilation tools
riscv32-unknown-elf-gcc      # C/C++ compiler
riscv32-unknown-elf-g++      # C++ compiler  
riscv32-unknown-elf-as       # Assembler
riscv32-unknown-elf-ld       # Linker

# Binary utilities
riscv32-unknown-elf-objdump  # Disassembler
riscv32-unknown-elf-objcopy  # Binary format converter
riscv32-unknown-elf-readelf  # ELF file analyzer
riscv32-unknown-elf-nm       # Symbol table viewer
riscv32-unknown-elf-strip    # Symbol remover

# Debugging tools
riscv32-unknown-elf-gdb      # GNU Debugger
riscv32-unknown-elf-run      # Simulator interface
```

---

## Multilib Support

### 📚 **What is Multilib?**

**Multilib** = **Multiple Libraries** - A single toolchain installation that supports multiple target architectures with optimized libraries for each.

### 🔧 **Traditional vs Unified Approach**

**Without Multilib (Old AxE Setup):**
```bash
/opt/riscv32i/     # Separate installation for RV32I
/opt/riscv32im/    # Separate installation for RV32IM
```

**With Multilib (New AxE Setup):**
```bash
/opt/riscv/        # Single installation supporting both!
├── bin/           # Shared tools
└── riscv32-unknown-elf/lib/
    ├── rv32i/     # Libraries optimized for RV32I
    └── rv32im/    # Libraries optimized for RV32IM
```

### 🎯 **How Multilib Works**

1. **Compiler detects** the `-march` flag
2. **Automatically selects** the appropriate library directory
3. **Links against** optimized libraries for that architecture
4. **Generates code** specific to the target instruction set

### 🚀 **Benefits for AxE**

1. **Single Installation**: One toolchain for all core types
2. **Correct Optimization**: Each library variant optimized for its architecture
3. **Easy Switching**: Just change the `-march` flag
4. **Space Efficient**: Shared tools, separate only what differs
5. **Future-Proof**: Easy to add new RISC-V extensions

---

## Compilation Examples

### 🔨 **Basic Compilation**

```bash
# Compile for exact cores (RV32I - no multiplication)
riscv32-unknown-elf-gcc -march=rv32i -mabi=ilp32 -o program program.c

# Compile for approximate cores (RV32IM - with multiplication)  
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -o program program.c

# With compressed instructions (smaller code size)
riscv32-unknown-elf-gcc -march=rv32imc -mabi=ilp32 -o program program.c
```

### 🐛 **Development Builds**

```bash
# Debug build with symbols and no optimization
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -g -O0 -o program program.c

# Release build with optimization
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O2 -o program program.c

# Size-optimized build (important for embedded)
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -Os -o program program.c
```

### 📋 **Analysis & Inspection**

```bash
# Generate assembly listing
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -S -o program.s program.c

# Create mixed source/assembly disassembly
riscv32-unknown-elf-objdump -S program.elf > program.disasm

# Show symbol table
riscv32-unknown-elf-nm program.elf

# Display ELF header information
riscv32-unknown-elf-readelf -h program.elf

# Convert to binary format (for hardware loading)
riscv32-unknown-elf-objcopy -O binary program.elf program.bin
```

### 🎯 **AxE-Specific Flags**

```bash
# Common flags used in AxE Makefiles
CFLAGS = -march=$(ARCH) -mabi=ilp32 -O0 -g -Wall -pedantic -ffreestanding -fstack-usage

# Bare-metal linking (no OS)
LDFLAGS = -Ttext 0 -nostartfiles -Wl,-e,my_start

# Complete AxE compilation command
riscv32-unknown-elf-gcc $(CFLAGS) $(LDFLAGS) -o program.elf start.S program.c -lm
```

---

## Debugging with GDB

### 🐛 **Starting GDB Session**

```bash
# Start GDB with RISC-V binary
riscv32-unknown-elf-gdb program.elf

# Or with additional symbol file
riscv32-unknown-elf-gdb -s symbols.elf program.elf
```

### 🎯 **Essential GDB Commands for RISC-V**

```bash
# Target setup
(gdb) target sim                    # Use built-in simulator
(gdb) target remote localhost:1234  # Connect to Verilator/QEMU

# Program loading
(gdb) load                          # Load program into target
(gdb) file program.elf              # Load symbol information

# Execution control
(gdb) break main                    # Set breakpoint at main
(gdb) break *0x1000                 # Set breakpoint at address
(gdb) run                           # Start execution
(gdb) continue                      # Continue execution
(gdb) step                          # Step one source line
(gdb) stepi                         # Step one instruction

# Inspection
(gdb) disas                         # Show disassembly
(gdb) disas main                    # Disassemble function
(gdb) info registers                # Show all RISC-V registers
(gdb) print $pc                     # Show program counter
(gdb) print $sp                     # Show stack pointer
(gdb) x/10i $pc                     # Show 10 instructions at PC

# Memory examination
(gdb) x/10w 0x1000                  # Show 10 words at address
(gdb) x/s 0x2000                    # Show string at address
(gdb) info mem                      # Show memory regions
```

### 🔧 **RISC-V Register Names**

```bash
# General purpose registers
x0 (zero)    # Always zero
x1 (ra)      # Return address
x2 (sp)      # Stack pointer
x3 (gp)      # Global pointer
x4 (tp)      # Thread pointer
x5-x7 (t0-t2) # Temporary registers
x8 (s0/fp)   # Saved register / Frame pointer
x9 (s1)      # Saved register
x10-x11 (a0-a1) # Function arguments/return values
x12-x17 (a2-a7) # Function arguments
x18-x27 (s2-s11) # Saved registers
x28-x31 (t3-t6) # Temporary registers
```

---

## AxE-Specific Development

### 🏗️ **AxE Project Context**

**Research Focus:**
- **Approximate Computing**: Energy-accuracy trade-offs
- **Heterogeneous Architecture**: Mixed exact/approximate cores
- **Energy Harvesting**: Battery-powered system optimization
- **Multi-Processor SoC**: NoC-based communication

**Core Types:**
- **PicoRV32**: Exact computation cores (RV32I)
- **PiXoRV32**: Approximate computation cores (RV32IM)

### 🎯 **Compilation Strategy**

**For Exact Cores (PicoRV32):**
```bash
# No hardware multiplication - smaller, lower power
make rv32i ARCH=rv32i
```

**For Approximate Cores (PiXoRV32):**
```bash
# Hardware multiplication with approximation
make rv32im ARCH=rv32im
```

### 🔬 **Analysis Workflow**

```bash
# 1. Compile for both architectures
make rv32i rv32im

# 2. Compare instruction counts
riscv32-unknown-elf-objdump -S rv32i_main.elf | wc -l
riscv32-unknown-elf-objdump -S rv32im_main.elf | wc -l

# 3. Analyze multiplication usage
riscv32-unknown-elf-objdump -S rv32im_main.elf | grep -E "(mul|div)"

# 4. Check code size
ls -la *.elf *.bin

# 5. Generate hex files for hardware simulation
python3 ../../../tools/freedom-bin2hex.py --bit-width 32 rv32im_main.bin > rv32im_main.hex
```

---

## Build System Integration

### 📁 **AxE Makefile Structure**

```makefile
# Standard AxE Makefile pattern
CC = /opt/riscv/bin/riscv32-unknown-elf-gcc
OBJDUMP = /opt/riscv/bin/riscv32-unknown-elf-objdump
OBJCOPY = /opt/riscv/bin/riscv32-unknown-elf-objcopy

# Architecture definitions
SMALL = rv32i      # For exact cores
BIG = rv32im       # For approximate cores

# Compilation flags
CFLAGS = -Wall -O0 -pedantic -ffreestanding -fstack-usage
INC = -I../../_libs
LINK = -Ttext 0 -Wl,-e,my_start

# Phony targets
.PHONY: clean rv32i rv32im

# Architecture-specific builds
rv32i: ARCH=$(SMALL)
rv32i: $(ARCH)_main.hex $(ARCH)_code

rv32im: ARCH=$(BIG)  
rv32im: $(ARCH)_main.hex $(ARCH)_code

# Build rules
$(ARCH)_main.elf:
	$(CC) -march=$(ARCH) -mabi=ilp32 $(CFLAGS) $(INC) -nostartfiles \
	-o ./$(ARCH)_main.elf $(LINK) ../start.S ./main.c -lm

$(ARCH)_main.bin: $(ARCH)_main.elf
	$(OBJCOPY) -O binary ./$(ARCH)_main.elf ./$(ARCH)_main.bin

$(ARCH)_main.hex: $(ARCH)_main.bin
	python3 ../../../tools/freedom-bin2hex.py --bit-width 32 \
	./$(ARCH)_main.bin > $(ARCH)_main.hex

$(ARCH)_code: $(ARCH)_main.elf
	$(OBJDUMP) -S ./$(ARCH)_main.elf > $(ARCH)_main.objdump
	$(OBJDUMP) -t ./$(ARCH)_main.elf > $(ARCH)_main.objdump_table
```

### 🚀 **Common Build Commands**

```bash
# Build for exact cores
make rv32i

# Build for approximate cores
make rv32im

# Build both architectures
make rv32i rv32im

# Clean build artifacts
make clean

# View generated assembly
less rv32im_main.objdump

# Check symbol table
less rv32im_main.objdump_table
```

---

## Troubleshooting

### ❌ **Common Issues**

#### **1. Toolchain Not Found**
```bash
# Error: command not found
bash: riscv32-unknown-elf-gcc: command not found

# Solution: Check PATH
echo $PATH | grep riscv
export PATH="/opt/riscv/bin:$PATH"
```

#### **2. Wrong Architecture Libraries**
```bash
# Error: no multilib for architecture
riscv32-unknown-elf-gcc: error: no multilib match for rv32imc/ilp32

# Solution: Check supported architectures
riscv32-unknown-elf-gcc -print-multi-lib
```

#### **3. Missing Headers**
```bash
# Error: newlib headers not found
fatal error: stdio.h: No such file or directory

# Solution: Verify installation
ls /opt/riscv/riscv32-unknown-elf/include/
```

#### **4. Linking Errors**
```bash
# Error: undefined reference to '__start'
ld: undefined reference to `__start'

# Solution: Check entry point
objdump -f program.elf | grep "start address"
```

### 🔧 **Verification Commands**

```bash
# Check toolchain installation
which riscv32-unknown-elf-gcc
riscv32-unknown-elf-gcc --version

# Verify multilib support  
riscv32-unknown-elf-gcc -print-multi-lib

# Check available libraries
ls /opt/riscv/riscv32-unknown-elf/lib/

# Test basic compilation
echo 'int main(){return 0;}' | riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 -x c - -o test
```

---

## External Resources

### 📚 **Official Documentation**
- **[RISC-V GNU Toolchain Repository](https://github.com/riscv-collab/riscv-gnu-toolchain)** - Official toolchain source and documentation
- **[RISC-V Specifications](https://riscv.org/technical/specifications/)** - Complete ISA specifications including extensions
- **[RISC-V Assembly Programming Guide](https://github.com/riscv-non-isa/riscv-asm-manual)** - Assembly language reference

### 🎓 **Learning Materials**
- **[RISC-V Reference Card](https://www.cl.cam.ac.uk/teaching/1617/ECAD+Arch/files/docs/RISCVGreenCardv8-20151013.pdf)** - Quick instruction reference
- **[RISC-V Online Assembler](https://riscvasm.lucasteske.dev/)** - Web-based assembly testing
- **[Spike RISC-V Simulator](https://github.com/riscv-software-src/riscv-isa-sim)** - Functional simulator for testing

### 🔬 **AxE Research Context**
- **IEEE ISLPED**: Low Power Electronics and Design conference
- **IEEE DATE**: Design, Automation & Test in Europe conference  
- **ACM CODES+ISSS**: Hardware/Software Codesign conference
- **ACM ASPLOS**: Architectural Support for Programming Languages and Operating Systems

### 🛠️ **Development Tools**
- **[PicoRV32 GitHub](https://github.com/cliffordwolf/picorv32)** - Base exact processor core
- **[Verilator Documentation](https://verilator.org/guide/latest/)** - Hardware simulation
- **[GTKWave](http://gtkwave.sourceforge.net/)** - Waveform viewer for debugging

---

This guide provides the foundation for effective RISC-V development within the AxE project. For questions specific to AxE's approximate computing research, consult the project's research publications and documentation.