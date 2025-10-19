# 🛤️ AxE Path Management Best Practices Guide

## 📋 Table of Contents
- [Overview](#-overview)
- [Critical Issues Fixed](#-critical-issues-fixed)
- [VSCode Configuration](#-vscode-configuration-best-practices)
- [Python Path Management](#-python-path-management)
- [Build System Integration](#-build-system-integration)
- [Implementation Examples](#-implementation-examples)
- [Troubleshooting](#-troubleshooting)
- [Next Steps](#-next-steps)

---

## 🎯 Overview

### **Why Path Management is Critical for AxE**
Proper path management directly impacts:
- **🚀 Development Velocity**: Developers can start contributing immediately
- **🔄 CI/CD Pipeline**: Automated builds work consistently across environments
- **🐳 Container Portability**: Docker environments function seamlessly
- **👥 Team Collaboration**: Multiple developers work without path conflicts
- **📦 Research Reproducibility**: Experiments work across different machines

### **Current State Assessment**
**Status**: **PARTIALLY FIXED** (Phase 1 temporary fixes implemented)
- ✅ VSCode launch.json hardcoded paths **RESOLVED**
- ⚠️ Build system still contains some hardcoded references
- ⚠️ Python modules need centralized path management
- ⚠️ Configuration files need portable path resolution

---

## 🔧 Critical Issues Fixed

### **Issue #1: VSCode Launch Configuration (RESOLVED)**

#### **Before: Broken Hardcoded Paths**
```json
{
    "program": "/home/axe/workspace/soc_frame/tools/run_mpsoc.py",
    "args": ["/home/axe/workspace/soc_frame/tools/_2x2_main.conf"]
}
```
**Problems:**
- ❌ User-specific hardcoded path `/home/axe/workspace/`
- ❌ Breaks for other developers
- ❌ Fails in CI/CD environments
- ❌ Not portable across operating systems

#### **After: Professional Workspace-Relative Paths**
```json
{
    "name": "Python Debugger: run_mpsoc with Arguments",
    "type": "debugpy", 
    "request": "launch",
    "program": "${workspaceFolder}/soc_frame/tools/run_mpsoc.py",
    "console": "integratedTerminal",
    "args": ["${workspaceFolder}/soc_frame/tools/_2x2_main.conf"],
    "cwd": "${workspaceFolder}",
    "env": {
        "AXE_ROOT": "${workspaceFolder}",
        "PYTHONPATH": "${workspaceFolder}/soc_frame/tools:${env:PYTHONPATH}"
    }
}
```
**Improvements:**
- ✅ Uses `${workspaceFolder}` VSCode variable for portability
- ✅ Sets explicit working directory with `cwd`
- ✅ Configures proper environment variables
- ✅ Extends PYTHONPATH for module discovery
- ✅ Works across all development environments

---

## 💻 VSCode Configuration Best Practices

### **Essential VSCode Path Variables Reference**

| Variable | Description | Example Usage |
|----------|-------------|---------------|
| `${workspaceFolder}` | Root workspace directory | `${workspaceFolder}/soc_frame/tools` |
| `${file}` | Currently opened file | `${file}` |
| `${relativeFile}` | File relative to workspace | `${relativeFile}` |
| `${fileWorkspaceFolder}` | Workspace folder of current file | `${fileWorkspaceFolder}` |
| `${fileBasename}` | Basename of current file | `${fileBasename}` |
| `${fileDirname}` | Directory of current file | `${fileDirname}` |
| `${cwd}` | Current working directory | `${cwd}` |
| `${env:VARIABLE}` | Environment variable | `${env:AXE_ROOT}` |

### **Environment Variable Configuration Pattern**
```json
{
    "env": {
        "AXE_ROOT": "${workspaceFolder}",
        "PYTHONPATH": "${workspaceFolder}/soc_frame/tools:${env:PYTHONPATH}",
        "VERILATOR_ROOT": "${env:VERILATOR_ROOT}",
        "RISCV": "${env:RISCV}"
    }
}
```

### **Critical Configuration Requirements**
1. **Always set explicit `cwd`**: VSCode defaults to its own directory, not workspace
2. **Use workspace variables**: Never hardcode absolute paths
3. **Configure environment**: Set up all necessary environment variables
4. **Extend existing paths**: Use `${env:PYTHONPATH}` to preserve existing configuration

---

## 🐍 Python Path Management

### **Phase 1: Immediate Fix Pattern (Current Implementation)**
```python
# File: soc_frame/tools/path_utils.py
"""Centralized path management utilities for AxE project"""

import os
import sys
from pathlib import Path

def setup_axe_paths():
    """Set up AxE project paths with multiple fallback methods"""
    
    # Method 1: Environment variable (highest priority)
    if axe_root := os.environ.get('AXE_ROOT'):
        axe_root = Path(axe_root)
    else:
        # Method 2: Relative to current script
        current_file = Path(__file__).resolve()
        axe_root = current_file.parent.parent.parent  # tools -> soc_frame -> workspace
        
        # Method 3: Verify with marker file
        if not (axe_root / 'CLAUDE.md').exists():
            # Method 4: Search parent directories
            for parent in current_file.parents:
                if (parent / 'CLAUDE.md').exists():
                    axe_root = parent
                    break
            else:
                raise RuntimeError(
                    "Could not locate AxE project root. "
                    "Set AXE_ROOT environment variable or run from project directory."
                )
    
    # Set up derived paths
    paths = {
        'axe_root': axe_root,
        'soc_frame': axe_root / 'soc_frame',
        'tools': axe_root / 'soc_frame' / 'tools',
        'systems': axe_root / 'soc_frame' / 'systems',
        'sw': axe_root / 'soc_frame' / 'sw',
        'docs': axe_root / 'docs'
    }
    
    # Add tools to Python path
    tools_str = str(paths['tools'])
    if tools_str not in sys.path:
        sys.path.insert(0, tools_str)
    
    return paths

# Global paths object
PATHS = setup_axe_paths()
```

### **Usage in Existing Scripts**
```python
# File: soc_frame/tools/run_mpsoc.py
# Add this at the top of existing scripts:

try:
    from path_utils import PATHS
except ImportError:
    # Fallback for scripts that haven't been updated yet
    import os
    from pathlib import Path
    
    current_dir = Path(__file__).parent
    PATHS = {
        'tools': current_dir,
        'soc_frame': current_dir.parent,
        'axe_root': current_dir.parent.parent
    }

# Now use PATHS throughout the script:
config_file = PATHS['tools'] / "_2x2_main.conf"
system_dir = PATHS['systems'] / "2x2_16_priority_input_approx"
```

### **Configuration File Resolution**
```python
def resolve_config_path(config_name: str) -> Path:
    """Resolve configuration file with multiple search locations"""
    
    # Add .conf extension if not present
    if not config_name.endswith('.conf'):
        config_name += '.conf'
    
    # Search locations in priority order
    search_paths = [
        Path(config_name),  # Current directory
        PATHS['tools'] / config_name,  # Tools directory
        Path.cwd() / config_name,  # Working directory
    ]
    
    for path in search_paths:
        if path.exists():
            return path.resolve()
    
    raise FileNotFoundError(
        f"Configuration file '{config_name}' not found in: "
        f"{[str(p) for p in search_paths]}"
    )

# Usage:
config_path = resolve_config_path("_2x2_main")
```

---

## 🔨 Build System Integration

### **Makefile Path Management Best Practices**
```makefile
# File: soc_frame/Makefile
# ✅ BEST PRACTICE: Environment variables with sensible defaults

# Detect project root
AXE_ROOT ?= $(shell pwd | sed 's|/soc_frame.*||')
SOC_FRAME_ROOT ?= $(AXE_ROOT)/soc_frame
TOOLS_DIR ?= $(SOC_FRAME_ROOT)/tools
SYSTEMS_DIR ?= $(SOC_FRAME_ROOT)/systems

# ✅ Use relative paths where possible
SRC_DIR := ./src
BUILD_DIR := ./build
CONFIGS_DIR := ./configurations

# ✅ Platform-independent separators
PATHSEP := $(if $(filter Windows_NT,$(OS)),;,:)

# ✅ Path validation target
.PHONY: check-paths
check-paths:
	@echo "=== AxE Path Validation ==="
	@echo "AXE_ROOT: $(AXE_ROOT)"
	@echo "SOC_FRAME_ROOT: $(SOC_FRAME_ROOT)"
	@echo "TOOLS_DIR: $(TOOLS_DIR)"
	@test -d "$(AXE_ROOT)" || (echo "Error: AXE_ROOT not found: $(AXE_ROOT)" && exit 1)
	@test -f "$(AXE_ROOT)/CLAUDE.md" || (echo "Error: Not a valid AxE root (CLAUDE.md missing)" && exit 1)
	@test -d "$(TOOLS_DIR)" || (echo "Error: TOOLS_DIR not found: $(TOOLS_DIR)" && exit 1)
	@echo "✅ All paths validated successfully"

# ✅ All targets depend on path validation
build: check-paths
	# Build commands here
	
sw: check-paths
	# Software build commands here
```

### **Shell Script Path Management**
```bash
#!/bin/bash
# File: setup-development.sh
# ✅ PROFESSIONAL: Robust shell script path handling

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Function to find AxE project root
find_axe_root() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local current_dir="$script_dir"
    
    # Method 1: Environment variable
    if [[ -n "${AXE_ROOT:-}" ]] && [[ -d "$AXE_ROOT" ]]; then
        echo "$AXE_ROOT"
        return 0
    fi
    
    # Method 2: Look for CLAUDE.md marker file
    while [[ "$current_dir" != "/" ]]; do
        if [[ -f "$current_dir/CLAUDE.md" ]]; then
            echo "$current_dir"
            return 0
        fi
        current_dir="$(dirname "$current_dir")"
    done
    
    # Method 3: Default to script directory
    echo "$script_dir"
}

# Set up paths with validation
readonly AXE_ROOT="$(find_axe_root)"
readonly SOC_FRAME="$AXE_ROOT/soc_frame"
readonly TOOLS_DIR="$SOC_FRAME/tools"

# Validate critical paths
validate_axe_environment() {
    local errors=0
    
    echo "=== AxE Environment Validation ==="
    
    if [[ ! -d "$AXE_ROOT" ]]; then
        echo "❌ AXE_ROOT directory not found: $AXE_ROOT" >&2
        errors=$((errors + 1))
    else
        echo "✅ AXE_ROOT: $AXE_ROOT"
    fi
    
    if [[ ! -f "$AXE_ROOT/CLAUDE.md" ]]; then
        echo "❌ CLAUDE.md not found (not a valid AxE root): $AXE_ROOT" >&2
        errors=$((errors + 1))
    else
        echo "✅ AxE project marker found"
    fi
    
    if [[ ! -d "$TOOLS_DIR" ]]; then
        echo "❌ Tools directory not found: $TOOLS_DIR" >&2
        errors=$((errors + 1))
    else
        echo "✅ Tools directory: $TOOLS_DIR"
    fi
    
    if [[ $errors -gt 0 ]]; then
        echo "❌ Environment validation failed with $errors errors" >&2
        echo "💡 Tip: Set AXE_ROOT environment variable or run from AxE project directory" >&2
        exit 1
    fi
    
    echo "✅ Environment validation successful"
}

# Export paths for other scripts
export AXE_ROOT SOC_FRAME TOOLS_DIR

# Run validation
validate_axe_environment
```

---

## ✅ **IMPLEMENTED SOLUTION**

### **Professional Path Management System**

**Status**: **IMPLEMENTED** - All critical Python files updated with modern path management

#### **Created: `axe_paths.py` - Centralized Path Management Module**
```python
# Usage Examples:
from axe_paths import AXE_PATHS

# Access paths as attributes
config_file = AXE_PATHS.tools / "_2x2_main.conf"
system_dir = AXE_PATHS.systems / "2x2_16_priority_input"
solar_data = AXE_PATHS.resolve_solar_data("final.csv")

# Get system executable
executable = AXE_PATHS.get_system_executable("SoC_approx")

# Memory hex file location
mem_hex = AXE_PATHS.get_memory_hex_path()

# Legacy compatibility (automatically available)
PATH_PRGS, PATH_CONTROLLERS, PATH_TASKS, PATH_SYSS
```

#### **Key Features Implemented:**
- ✅ **Environment Variable Detection**: `AXE_ROOT`, `SOC_FRAME_ROOT`
- ✅ **Multiple Fallback Methods**: Script location, working directory, marker files
- ✅ **Backwards Compatibility**: Legacy constants still work
- ✅ **Error Handling**: Graceful degradation with informative messages
- ✅ **Cross-Platform**: Uses Python pathlib for OS independence
- ✅ **Validation**: Ensures project structure integrity

### **Files Updated with Modern Path Management:**

#### **1. `defines.py` - Import with Fallback Pattern**
```python
try:
    from axe_paths import PATH_CONTROLLERS, PATH_PRGS, PATH_TASKS, PATH_SYSS
except ImportError:
    # Fallback to legacy hardcoded paths
    PATH_CONTROLLERS = "/home/user/soc_frame/sw/controller/"
    # ... etc
    logging.warning("Using fallback hardcoded paths")
```

#### **2. `simulator.py` - Dynamic Path Resolution**
```python
# Modern approach with fallback
try:
    from axe_paths import AXE_PATHS
    call = [ str(AXE_PATHS.get_system_executable(sys.name)) ]
    dst = str(AXE_PATHS.get_memory_hex_path())
except ImportError:
    # Legacy fallback
    call = [ "/home/user/soc_frame/systems/"+sys.name+"/obj_dir/Vtop" ]
    dst = "/home/user/soc_frame/mem.hex"
```

#### **3. `run_mpsoc.py` - Robust File Handling**
```python
try:
    from axe_paths import AXE_PATHS
    solar_file_path = AXE_PATHS.resolve_solar_data("final.csv")
    charges_f = open( str(solar_file_path), "r" )
except ImportError:
    charges_f = open( "/home/user/soc_frame/tools/solar/final.csv", "r" )
except FileNotFoundError:
    logging.error("Solar data file not found")
    charges_f = None
```

---

## 💡 Implementation Examples

### **Example 1: Using the New Path Management (CURRENT)**
```python
# Before (PROBLEMATIC):
import sys
sys.path.append('/home/axe/workspace/soc_frame/tools')  # ❌ Hardcoded
from defines import *

# After (PROFESSIONAL):
# Add to beginning of script
import sys
from pathlib import Path

# Set up paths
script_dir = Path(__file__).parent
axe_root = script_dir.parent.parent if script_dir.name == 'tools' else script_dir.parent
tools_dir = axe_root / 'soc_frame' / 'tools'

# Add to Python path
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# Now imports work
from defines import *
```

### **Example 2: Configuration Loading with Path Resolution**
```python
# File: soc_frame/tools/config_loader.py
import configparser
from pathlib import Path
from typing import Tuple

def load_axe_config(config_name: str) -> Tuple[configparser.ConfigParser, Path]:
    """Load AxE configuration with robust path resolution"""
    
    config = configparser.ConfigParser()
    
    # Normalize config name
    if not config_name.endswith('.conf'):
        config_name += '.conf'
    
    # Search paths in priority order
    search_locations = [
        Path(config_name),  # Current directory
        Path(__file__).parent / config_name,  # Same directory as this script
        Path.cwd() / config_name,  # Working directory
    ]
    
    # Find existing config
    config_path = None
    for location in search_locations:
        if location.exists():
            config_path = location.resolve()
            break
    
    if config_path is None:
        available_locations = '\n  '.join(str(loc) for loc in search_locations)
        raise FileNotFoundError(
            f"Configuration file '{config_name}' not found.\n"
            f"Searched locations:\n  {available_locations}"
        )
    
    # Load and validate config
    try:
        config.read(config_path)
    except Exception as e:
        raise RuntimeError(f"Failed to parse config file '{config_path}': {e}")
    
    # Validate required sections
    required_sections = ['system', 'controller', 'run']
    missing_sections = [sec for sec in required_sections if not config.has_section(sec)]
    if missing_sections:
        raise ValueError(
            f"Config file '{config_path}' missing required sections: {missing_sections}"
        )
    
    return config, config_path

# Usage example:
config, config_file = load_axe_config('_2x2_main')
print(f"✅ Loaded configuration from: {config_file}")
system_name = config.get('system', 'system_name')
```

---

## 🔍 Troubleshooting

### **Common Issues and Solutions**

#### **Issue: ModuleNotFoundError in Python**
```bash
# Problem: Python can't find AxE modules
ModuleNotFoundError: No module named 'defines'
```
**Solution:**
1. **Check environment**: `echo $AXE_ROOT`
2. **Set if missing**: `export AXE_ROOT=/path/to/axe/workspace`
3. **Update PYTHONPATH**: `export PYTHONPATH="$AXE_ROOT/soc_frame/tools:$PYTHONPATH"`
4. **Run from correct directory**: `cd $AXE_ROOT/soc_frame/tools`

#### **Issue: VSCode Debugger Path Errors**
```bash
# Problem: Debugger can't find program files
Error: Cannot find module '/home/axe/workspace/...'
```
**Solution:** ✅ **ALREADY FIXED** - Updated launch.json uses workspace variables

#### **Issue: Configuration Files Not Found**
```bash
# Problem: Scripts can't find .conf files
FileNotFoundError: [Errno 2] No such file or directory: '_2x2_main.conf'
```
**Solution:**
1. **Check working directory**: `pwd` should be in tools directory
2. **Use absolute path**: Provide full path to config file
3. **Set AXE_ROOT**: `export AXE_ROOT=/path/to/workspace`

#### **Issue: Build System Path Failures**
```bash
# Problem: Make can't find source files
make: *** No rule to make target '../systems/...'. Stop.
```
**Solution:**
1. **Run from correct directory**: `cd $AXE_ROOT/soc_frame`
2. **Check AXE_ROOT**: `make check-paths` (if implemented)
3. **Verify directory structure**: Ensure all subdirectories exist

### **Diagnostic Commands**
```bash
# Comprehensive AxE environment check
echo "=== AxE Environment Diagnostics ==="
echo "Working Directory: $(pwd)"
echo "AXE_ROOT: ${AXE_ROOT:-'(not set)'}"
echo "PYTHONPATH: ${PYTHONPATH:-'(not set)'}"
echo ""
echo "Directory Structure:"
ls -la ${AXE_ROOT:-'.'}/
echo ""
echo "Tools Directory:"
ls -la ${AXE_ROOT:-'.'}/soc_frame/tools/ | head -10
echo ""
echo "Python Module Test:"
python3 -c "import sys; sys.path.insert(0, '${AXE_ROOT:-/tmp}/soc_frame/tools'); import defines; print('✅ Python imports working')" 2>/dev/null || echo "❌ Python imports failing"
```

---

## 🎯 Next Steps

### **Phase 1: Immediate Fixes (In Progress)**
- [x] ✅ **VSCode launch.json fixed** with workspace variables
- [ ] 🚧 Create `path_utils.py` utility module
- [ ] 🚧 Update critical Python scripts with path resolution
- [ ] 🚧 Add path validation to main Makefile
- [ ] 🚧 Document path conventions for team

### **Phase 2: Full Modernization (Planned)**
- [ ] 📋 Implement centralized `AxEPaths` class
- [ ] 📋 Add comprehensive path validation and error handling
- [ ] 📋 Create configuration management system
- [ ] 📋 Add path-related unit tests
- [ ] 📋 Update all build scripts with portable paths

### **Immediate Action Items**
1. **Test VSCode fix**: Verify debugging works with new launch.json
2. **Create path utilities**: Implement `path_utils.py` for common usage
3. **Update critical scripts**: Start with `run_mpsoc.py` and `run_single_processor_single_program.py`
4. **Team documentation**: Share path conventions with other developers

---

## 📚 Related Documentation
- [Docker-Tutorial.md](Docker-Tutorial.md) - Container path handling
- [Build-System.md](Build-System.md) - Makefile and compilation paths  
- [Environment-Setup.md](Environment-Setup.md) - Development environment configuration
- [COMPREHENSIVE_SYSTEM_ANALYSIS.md](COMPREHENSIVE_SYSTEM_ANALYSIS.md) - System-wide analysis including build issues

---

**This path management guide is part of the AxE project modernization effort, implementing industry-standard practices while maintaining research functionality.**