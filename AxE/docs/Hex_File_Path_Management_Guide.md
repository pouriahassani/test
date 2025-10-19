# AxE Hex File Path Management Guide

## Executive Summary

This document provides a comprehensive solution for managing hex file paths in the AxE project. The analysis revealed inconsistent path management across RTL modules, with critical hardcoded paths that break portability. This guide implements a standardized approach using environment variables and centralized configuration.

## Problem Analysis

### Issues Identified

1. **Hardcoded Absolute Paths**: `/home/axe/workspace/test.hex` in bram.sv
2. **Inconsistent Path Resolution**: Mixed approaches between RTL and Python tools
3. **NoC Routing Table Paths**: 80+ hardcoded references in router modules
4. **Environment Variable Mismatches**: Different naming conventions

### Impact

- **Portability**: Code fails when moved to different systems
- **Collaboration**: Each developer needs different paths
- **Docker**: Containers use different directory structures
- **CI/CD**: Automated builds break with hardcoded paths

## Solution Architecture

### 1. Centralized Path Management

**File**: `soc_frame/rtl/defines_paths.vh`
- Centralizes all hex file path definitions
- Uses environment variables with fallback paths
- Supports both absolute and relative path resolution

### 2. Environment Variable Strategy

**Primary Variable**: `AXE_ROOT`
- Points to project root directory
- Passed to Verilator via `-DAXE_ROOT_DEFINE`
- Used by both RTL and Python tools

### 3. Path Categories

```
AXE_ROOT/
├── test.hex                    ← Main program memory
├── soc_frame/
│   ├── tools/
│   │   ├── mesh_*_routing_*.hex ← NoC routing tables
│   │   └── *.hex               ← Generated program files
│   └── systems/*/
│       └── out/                ← Build outputs
```

## Implementation Details

### RTL Path Management

**Updated `soc_frame/rtl/defines_paths.vh`:**
```verilog
`ifndef DEFINES_PATHS_VH
`define DEFINES_PATHS_VH

`ifdef AXE_ROOT_DEFINE
    // Environment variable based paths (preferred)
    `define RTL_ROOT `AXE_ROOT_DEFINE"/soc_frame/rtl"
    `define TOOLS_ROOT `AXE_ROOT_DEFINE"/soc_frame/tools"
    
    // Memory file paths using environment variable
    `define MEMORY_HEX_PATH `AXE_ROOT_DEFINE"/test.hex"
    
    // NoC routing table paths
    `define ROUTING_TABLE_0 `AXE_ROOT_DEFINE"/soc_frame/tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_0.hex"
    // ... (all routing tables)
    
`else
    // Fallback relative paths (from systems directory)
    `define MEMORY_HEX_PATH "../../../test.hex"
    `define ROUTING_TABLE_0 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_0.hex"
    // ... (relative fallbacks)
`endif

`endif // DEFINES_PATHS_VH
```

### Updated BRAM Module

**Fixed `soc_frame/rtl/memory/bram.sv`:**
```verilog
`include "../../rtl/defines_paths.vh"

initial begin
    // Use path management system from defines_paths.vh
    `ifdef MEMORY_HEX_PATH
        $readmemh( `MEMORY_HEX_PATH, mem,  0 );
    `else
        // Fallback for backward compatibility
        $readmemh( "/home/axe/workspace/test.hex", mem,  0 );
    `endif
end
```

### Build System Integration

**Enhanced `soc_frame/Makefile_include`:**
```makefile
# Set environment variables for RTL path management
export AXE_ROOT := $(shell pwd | sed 's|/soc_frame.*||')
export SOC_FRAME_ROOT := $(AXE_ROOT)/soc_frame

# Pass environment variables to Verilator
VERILATOR_FLAGS += -DAXE_ROOT_DEFINE=\"$(AXE_ROOT)\"
```

## Usage Instructions

### 1. Environment Setup

**Option A: Automatic (Recommended)**
```bash
# From any directory in the project
cd /path/to/axe/project/soc_frame/systems/2x2_16_priority_input_approx
make compile  # AXE_ROOT automatically detected
```

**Option B: Manual Override**
```bash
export AXE_ROOT=/path/to/axe/project
cd soc_frame/systems/2x2_16_priority_input_approx
make compile
```

**Option C: Docker Environment**
```bash
# In Dockerfile or docker-compose.yml
ENV AXE_ROOT=/workspace
```

### 2. Hex File Placement

**Main Program Memory:**
```bash
# Place your program hex file at project root
cp my_program.hex $AXE_ROOT/test.hex
```

**NoC Routing Tables:**
```bash
# Place routing tables in tools directory
cp routing_*.hex $AXE_ROOT/soc_frame/tools/
```

### 3. Verification

**Check Path Resolution:**
```bash
cd soc_frame/systems/2x2_16_priority_input_approx
make compile 2>&1 | grep "MEMORY_HEX_PATH"
```

**Verify File Access:**
```bash
# Check if hex file is found
ls -la $AXE_ROOT/test.hex
```

## Python Tool Integration

### Updated axe_paths.py

The Python tools should use the same environment variable:

```python
import os

def get_axe_root():
    """Get AxE project root directory."""
    axe_root = os.environ.get('AXE_ROOT')
    if axe_root:
        return axe_root
    
    # Fallback: detect from current working directory
    cwd = os.getcwd()
    if 'soc_frame' in cwd:
        return cwd.split('soc_frame')[0].rstrip('/')
    
    raise RuntimeError("AXE_ROOT not set and cannot auto-detect project root")

def get_memory_hex_path():
    """Get path to main memory hex file."""
    return os.path.join(get_axe_root(), "test.hex")

def get_routing_table_path(router_id):
    """Get path to NoC routing table hex file."""
    tools_dir = os.path.join(get_axe_root(), "soc_frame", "tools")
    filename = f"mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_{router_id}.hex"
    return os.path.join(tools_dir, filename)
```

## Migration Guide

### Step 1: Update RTL Modules

For any RTL module using hardcoded hex file paths:

**Before:**
```verilog
$readmemh("/home/axe/workspace/soc_frame/tools/routing_0.hex", routing_table);
```

**After:**
```verilog
`include "path/to/defines_paths.vh"
$readmemh(`ROUTING_TABLE_0, routing_table);
```

### Step 2: Update Build Scripts

Add environment variable support to Makefiles:

```makefile
# Add to VERILATOR_FLAGS
VERILATOR_FLAGS += -DAXE_ROOT_DEFINE=\"$(AXE_ROOT)\"
```

### Step 3: Update Python Scripts

Replace hardcoded paths with axe_paths.py functions:

**Before:**
```python
hex_file = "/home/axe/workspace/test.hex"
```

**After:**
```python
from soc_frame.tools.axe_paths import get_memory_hex_path
hex_file = get_memory_hex_path()
```

## Testing

### Test Script

Create `test_hex_paths.py`:
```python
#!/usr/bin/env python3
import os
import sys

def test_hex_path_resolution():
    """Test that all hex file paths resolve correctly."""
    
    # Test environment variable
    axe_root = os.environ.get('AXE_ROOT')
    if not axe_root:
        print("WARNING: AXE_ROOT not set, using auto-detection")
        axe_root = os.getcwd().split('soc_frame')[0].rstrip('/')
    
    print(f"AXE_ROOT: {axe_root}")
    
    # Test main memory file
    memory_hex = os.path.join(axe_root, "test.hex")
    print(f"Memory hex: {memory_hex} {'✓' if os.path.exists(memory_hex) else '✗'}")
    
    # Test routing tables
    tools_dir = os.path.join(axe_root, "soc_frame", "tools")
    for i in range(4):
        routing_file = os.path.join(tools_dir, f"mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_{i}.hex")
        exists = os.path.exists(routing_file)
        print(f"Routing {i}: {'✓' if exists else '✗'} {routing_file}")

if __name__ == "__main__":
    test_hex_path_resolution()
```

### Verification Commands

```bash
# Test from different directories
cd $AXE_ROOT && python3 test_hex_paths.py
cd $AXE_ROOT/soc_frame && python3 test_hex_paths.py
cd $AXE_ROOT/soc_frame/systems/2x2_16_priority_input_approx && python3 ../../../test_hex_paths.py
```

## Troubleshooting

### Common Issues

**1. AXE_ROOT not detected**
```bash
# Solution: Set manually
export AXE_ROOT=/path/to/axe/project
```

**2. Hex file not found**
```bash
# Check file exists
ls -la $AXE_ROOT/test.hex

# Check permissions
chmod 644 $AXE_ROOT/test.hex
```

**3. Verilator compilation fails**
```bash
# Check define is passed correctly
cd soc_frame/systems/2x2_16_priority_input_approx
make compile 2>&1 | grep "AXE_ROOT_DEFINE"
```

**4. NoC routing tables missing**
```bash
# Generate routing tables
cd soc_frame/tools
python3 generate_routing_tables.py
```

### Debug Commands

```bash
# Show all environment variables
env | grep AXE

# Check Verilator preprocessor defines
verilator --help | grep -A5 -- '-D'

# Verify hex file format
hexdump -C test.hex | head -10
```

## Best Practices

### 1. File Organization
- Keep `test.hex` at project root for easy access
- Place routing tables in `soc_frame/tools/`
- Use consistent naming for generated hex files

### 2. Development Workflow
- Always check hex file paths before compilation
- Use relative paths in fallback scenarios
- Test path resolution in different directories

### 3. CI/CD Integration
- Set AXE_ROOT in CI environment
- Verify hex files exist before running tests
- Use Docker volumes for hex file persistence

### 4. Documentation
- Document hex file requirements in README
- Provide path verification scripts
- Keep path definitions centralized

## Future Enhancements

### 1. Dynamic Path Configuration
- Support for multiple memory configurations
- Runtime hex file switching
- Configuration file-based paths

### 2. Path Validation
- Compile-time hex file existence checking
- Automatic path correction suggestions
- Integration with IDE path completion

### 3. Tool Integration
- Integration with AxE configuration management
- Automatic hex file generation and placement
- Path synchronization between RTL and Python

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-18  
**Author**: Claude AI Assistant  
**Project**: AxE (Approximate eXecution) Framework