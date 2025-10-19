# AxE Project Documentation Hub

## 📋 Documentation Structure

This is the central documentation hub for the AxE (Approximate eXecution) project. All documentation is organized here with clear navigation and update instructions.

### 🗂️ Documentation Organization

```
/home/axe/workspace/
├── docs/
│   ├── AxE_PROJECT_DOCUMENTATION.md       # THIS FILE - Central hub
│   ├── IMPLEMENTATION_PROGRESS.md         # Change log and progress tracking
│   ├── RTL_Path_Management_Tutorial.md    # Teaching guide for RTL path management
│   ├── Config-Management-Guide.md         # Configuration system documentation
│   ├── COMPREHENSIVE_SYSTEM_ANALYSIS.md   # System architecture analysis
│   ├── MODULARITY_ASSESSMENT.md           # Code modularity evaluation
│   ├── RTL_ANALYSIS_REPORT.md             # RTL code analysis
│   ├── TRANSFORMATION_ROADMAP.md          # Development roadmap
│   └── Docker-Tutorial.md                 # Container setup guide
└── soc_frame/
    ├── docs/                              # Technical documentation
    └── [project files]
```

---

## 🎯 Quick Navigation

### 📊 **Project Status & Progress**
- **[Implementation Progress Log](IMPLEMENTATION_PROGRESS.md)** - Complete change tracking with learning insights
- **[System Analysis](COMPREHENSIVE_SYSTEM_ANALYSIS.md)** - Complete architecture overview
- **[Modularity Assessment](MODULARITY_ASSESSMENT.md)** - Code organization evaluation
- **[Transformation Roadmap](TRANSFORMATION_ROADMAP.md)** - Development priorities
- **Current Status**: ✅ RTL path management fixed, ✅ File I/O system implemented, ❌ AXI protocol compliance issue identified
- **Last Updated**: August 8, 2025

### 🏗️ **System Architecture**
- **Multi-processor SoC**: 2x2 to 5x5 mesh NoC topologies
- **Heterogeneous Cores**: PicoRV32 (exact) + PiXoRV32 (approximate) RISC-V
- **Energy Harvesting**: Solar panel simulation with battery management
- **Partitioning Algorithms**: Three variants for task-to-core mapping

### 🔧 **Development Guides**
- **[RTL Path Management Tutorial](RTL_Path_Management_Tutorial.md)** - Complete teaching guide
- **[Configuration Management](Config-Management-Guide.md)** - YAML configuration system
- **[Docker Tutorial](Docker-Tutorial.md)** - Development environment setup
- **[File I/O Implementation Analysis](File_IO_Implementation_Analysis.md)** - Host-based file I/O system analysis and implementation
- **[Memory Management Stack Collision Analysis](Memory_Management_Stack_Collision_Analysis.md)** - Critical runtime bug analysis

### 🛠️ **Build System**
- **Hardware**: Verilator simulation and synthesis
- **Software**: RISC-V toolchain with multilib support
- **Commands**: `make` (hardware), `make sw` (software), `python main.py` (algorithms)

---

## 📚 Teaching & Learning Resources

### 🎓 **RTL Path Management - Complete Learning Guide**

#### **Problem**: Hardcoded Absolute Paths in RTL
SystemVerilog files contained hardcoded paths that broke compilation:
```systemverilog
// BROKEN - Environment specific
`include "/home/user/soc_frame/rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
$readmemh("/home/user/soc_frame/mem.hex", mem, 0);
```

#### **Solution**: Centralized Path Management System

**Step 1: Create Central Path Header**
```systemverilog
// File: rtl/defines_paths.vh
`ifndef DEFINES_PATHS_VH
`define DEFINES_PATHS_VH

// Memory file paths - optimized for obj_dir execution
`define MEMORY_HEX_PATH "../../../mem.hex"

// NoC routing table paths
`define ROUTING_TABLE_0 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_0.hex"
`define ROUTING_TABLE_1 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_1.hex"
`define ROUTING_TABLE_2 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_2.hex"
`define ROUTING_TABLE_3 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_3.hex"

`endif
```

**Step 2: Update RTL Files**
```systemverilog
// Memory controller (rtl/memory/bram.sv)
`include "../../rtl/defines_paths.vh"
initial begin
    $readmemh(`MEMORY_HEX_PATH, mem, 0);
end

// NoC router (rtl/noc/noc_connect_2x2_16/mkNetworkSimple.v)
`include "../../defines_paths.vh"
RegFileLoadSyn #(/*file*/ `ROUTING_TABLE_0, // Portable path reference
```

**Step 3: Update Include Statements**
```systemverilog
// System top level (systems/2x2_16_priority_input_approx/top.sv)
`include "../../rtl/defines_paths.vh"        // Path definitions
`include "../../rtl/noc/noc_connect_2x2_16/mkInputQueue.v"  // Relative includes
`include "../../rtl/clk_gater/clk_gater.sv"
```

#### **Teaching: SystemVerilog `include` Behavior**

**Question**: When we include a .sv file, does it copy the content?
**Answer**: Yes, `include` is a preprocessor directive that literally copies file content:

```systemverilog
// Before preprocessing
`include "defines.vh"
module top();
endmodule

// After preprocessing (what the compiler sees)
`define MEMORY_PATH "../../../mem.hex"    // Content from defines.vh
module top();
endmodule
```

**Why This Matters:**
- **Compilation**: Preprocessor runs before synthesis
- **Path Resolution**: Relative to the file doing the include
- **Scope**: Macros defined in included files are available
- **Order**: Include order matters for macro definitions

#### **Teaching: Path Resolution Strategy**

**Directory Structure:**
```
workspace/soc_frame/
├── systems/2x2_16_priority_input_approx/
│   ├── obj_dir/           ← Verilator execution directory
│   └── top.sv
├── rtl/
│   ├── defines_paths.vh
│   └── memory/bram.sv
├── tools/                 ← routing tables
└── mem.hex               ← program memory
```

**Path Calculation (from obj_dir):**
```
../../../mem.hex          → /workspace/soc_frame/mem.hex
../../../tools/routing.hex → /workspace/soc_frame/tools/routing.hex
```

**Why This Works:**
- **Verilator Execution**: Binary runs from obj_dir subdirectory
- **Relative Paths**: Always resolve correctly regardless of user/system
- **Portability**: No environment variables or hardcoded paths needed

#### **Teaching: Makefile Integration**

```makefile
# Verilator configuration (Makefile_include)
VERILATOR_FLAGS += -cc --exe --no-timing
VERILATOR_FLAGS += -Wno-fatal
VERILATOR_FLAGS += -y ../../rtl/noc/noc_connect_2x2_16  # Module directory
VERILATOR_FLAGS += -I../../rtl                        # Include directory

# Build and run
obj_dir/Vtop:
	$(VERILATOR) $(VERILATOR_FLAGS) top.sv sim_main.cpp
	$(MAKE) -j 32 -C obj_dir -f Vtop.mk

run: obj_dir/Vtop
	cd obj_dir && ./Vtop
```

**Teaching Points:**
- **`-I` flag**: Adds include search directory
- **`-y` flag**: Adds module search directory  
- **Working directory**: `cd obj_dir` ensures correct execution context
- **`--no-timing`**: Disables timing analysis for functional simulation

---

## 🔧 Current System Status

### ✅ **Successfully Implemented**
- **RTL Path Management**: All 73+ hardcoded paths fixed
- **Centralized Headers**: Single point of path configuration
- **Build System**: Makefile updated with proper flags
- **Compilation**: System compiles successfully with Verilator 5.038
- **Runtime**: System starts and initializes (warnings are for large files, not path errors)

### 📁 **Files Modified**
| File | Purpose | Changes |
|------|---------|---------|
| `rtl/defines_paths.vh` | **NEW** - Path definitions | Central macro definitions |
| `rtl/memory/bram.sv` | Memory initialization | Uses `MEMORY_HEX_PATH` macro |
| `rtl/noc/noc_connect_2x2_16/mkNetworkSimple.v` | NoC routing | Uses `ROUTING_TABLE_*` macros |
| `systems/2x2_16_priority_input_approx/top.sv` | System top level | Includes path header, relative includes |
| `Makefile_include` | Build configuration | Added include paths and flags |

### 🏃 **How to Use**
```bash
# Clean build
make clean

# Compile hardware
make compile

# Run system  
make run

# Expected output:
# --------------------
# starting 2x2_16
# --------------------
# [System initializes successfully]
```

---

## 📖 **Documentation Maintenance**

### ✏️ **How to Add New Documentation**

1. **Determine Category**: 
   - **System changes** → Update `docs/IMPLEMENTATION_PROGRESS.md`
   - **Teaching guides** → Create new file in `docs/` directory
   - **Quick reference** → Add to this central hub

2. **Update This Hub**: 
   - Add new documentation to navigation section
   - Update "Last Updated" date
   - Link to new files with clear descriptions

3. **Cross-Reference**: 
   - Link related documentation together
   - Update progress log with implementation details
   - Maintain consistent formatting

### 📝 **Documentation Standards**

- **Clear Headers**: Use descriptive section titles
- **Code Examples**: Always include before/after comparisons
- **Teaching Focus**: Explain why, not just what
- **Practical Examples**: Real code snippets from the project
- **Cross-References**: Link to related documentation

### 🔄 **Update Procedures**

**When making system changes:**
1. Implement the change
2. Test thoroughly
3. Update relevant documentation
4. Update progress log with learning insights
5. Update this central hub if needed

**When creating new features:**
1. Design the feature
2. Document the approach
3. Implement with teaching examples
4. Create usage documentation
5. Update central navigation

---

## 🎯 **Next Development Priorities**

### 🔨 **Phase 1: Core System Stabilization**
- [ ] Complete software build system validation
- [ ] Add comprehensive testing framework
- [ ] Create development environment setup scripts

### 🏗️ **Phase 2: Advanced Features**
- [ ] Implement synthesis tool compatibility
- [ ] Add automated regression testing
- [ ] Create performance benchmarking suite

### 📚 **Phase 3: Documentation Enhancement**
- [ ] Video tutorials for complex procedures
- [ ] Interactive examples and demos
- [ ] API documentation generation

---

## 📞 **Support & Contributing**

### 🆘 **Getting Help**
- **Documentation Issues**: Check this hub for navigation
- **Build Problems**: See troubleshooting in implementation progress
- **Path Issues**: Refer to RTL path management tutorial

### 🤝 **Contributing Guidelines**
- **Code Changes**: Always update progress documentation
- **New Features**: Include teaching examples and explanations
- **Bug Fixes**: Document the problem and solution approach

---

**Last Updated**: July 15, 2025  
**Status**: ✅ RTL path management system successfully implemented and documented  
**Next Update**: When new system changes are implemented