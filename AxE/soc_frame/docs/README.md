# AxE SoC Framework Documentation

## Overview

This directory contains technical documentation for the AxE (Approximate eXecution) SoC framework implementation.

## Documentation Index

### System Implementation
- **[FILE_IO_IMPLEMENTATION.md](FILE_IO_IMPLEMENTATION.md)** - Complete host-based file I/O system with memory-mapped operations, AXI handshaking, and multi-file support
- **[AXI_COMPLIANCE.md](AXI_COMPLIANCE.md)** - AXI4-Lite protocol compliance analysis, current issues, and recommended fixes

### Architecture Documents  
- **Memory Layout System** - YAML-based configuration with collision detection (see `config/memory_layout.yaml`)
- **Build System Integration** - Automated configuration generation and validation
- **Hardware-Software Interface** - AXI protocol and simulation integration

## Quick Reference

### File I/O System
```c
// Basic usage example
#include "file_io.h"

int fd = axe_file_open("data.txt", AXE_FILE_READ_MODE);
axe_file_read(fd, buffer, size);
axe_file_close(fd);
```

### Memory Configuration
```bash
# Validate and generate memory layout
make generate-memory-config

# Build with updated configuration  
make sw
```

### Key Features Implemented
✅ **Memory-mapped file operations** with blocking semantics  
✅ **Multi-file support** (up to 8 concurrent files)  
✅ **YAML-based memory configuration** with collision detection  
❌ **AXI protocol compliance** - File I/O detector has timing issues (see AXI_COMPLIANCE.md)  
✅ **Build system integration** with automatic generation  
✅ **Multi-node support** for concurrent operations  

## Known Issues

### Critical: AXI Protocol Compliance
**Module**: `file_io_detector.sv`  
**Issue**: Ready signal timing violation during file operations  
**Impact**: Potential system hangs with certain AXI masters  
**Status**: Documented, fix recommended in `AXI_COMPLIANCE.md`  
**Workaround**: Current implementation works with simple masters like PicoRV32

### Investigation Status
**Issue**: File operations trigger twice due to incomplete AXI handshaking  
**Root Cause**: Missing `bready` signal forwarding in `axi_detector.sv`  
**Status**: Fixed - Added proper ready signal connections  
**Verification**: Tested with file I/O operations, no longer triggers twice

## Development Guidelines

### Adding New Documentation
1. Create detailed `.md` files in this directory
2. Update this `README.md` index
3. Reference from main `CLAUDE.md` if system-level
4. Include code examples and usage patterns

### Documentation Standards
- **Clear structure** with overview, implementation, and examples
- **Code snippets** for all APIs and interfaces
- **File references** with exact paths to implementation
- **Performance characteristics** and resource usage
- **Integration instructions** and testing procedures

## Related Files

### Implementation
- `sw/_libs/file_io.h/c` - Software API
- `rtl/file_io_detector/` - Hardware detection  
- `config/memory_layout.yaml` - Memory configuration
- `tools/memory_layout_validator.py` - Validation system

### Build System
- `Makefile_include` - Memory config integration
- `generated/` - Auto-generated headers and constants
- `systems/*/sim_main.cpp` - Simulation handlers

### Documentation  
- `../CLAUDE.md` - Main project context and overview
- `FILE_IO_IMPLEMENTATION.md` - Detailed technical implementation