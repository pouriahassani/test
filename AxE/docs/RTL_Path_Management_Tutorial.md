# 🔧 RTL Path Management Tutorial

## 📋 Overview

This tutorial teaches you how to fix hardcoded paths in RTL (Register Transfer Level) code to make hardware projects portable across different development environments. We'll use the AxE project as a practical example.

## 🎯 Learning Objectives

By the end of this tutorial, you will understand:
- How to identify hardcoded paths in RTL code
- Different approaches to solve path management in hardware projects
- How to implement portable RTL path solutions
- Best practices for maintaining RTL code across teams

---

## 📚 **Step 1: Understanding the Problem**

### **What Are Hardcoded Paths?**

Hardcoded paths are absolute file system paths written directly into source code. In RTL, these commonly appear in:

1. **Include statements** - Loading other RTL modules
2. **Memory initialization** - Loading data files for simulation
3. **Simulation scripts** - File I/O operations

### **Why Are They Problematic?**

```systemverilog
// ❌ PROBLEMATIC: Only works on specific user's machine
`include "/home/user/soc_frame/rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
$readmemh("/home/user/soc_frame/mem.hex", mem, 0);
```

**Issues:**
- **Environment Dependency**: Only works on systems with exact same directory structure
- **Team Collaboration**: Breaks when different developers use different paths
- **CI/CD Failure**: Automated builds fail in different environments
- **Portability**: Cannot be packaged or deployed easily

---

## 🔍 **Step 2: Identifying Hardcoded Paths**

### **Detection Methods**

**Method 1: grep command**
```bash
# Find all hardcoded paths in SystemVerilog files
find . -name "*.sv" -exec grep -l "/home/user" {} \;
find . -name "*.v" -exec grep -l "/home/user" {} \;
```

**Method 2: Pattern search**
```bash
# Search for common hardcoded path patterns
grep -r "^`include \"/.*/" . --include="*.sv" --include="*.v"
grep -r "\$readmemh.*\"/.*/" . --include="*.sv" --include="*.v"
```

### **AxE Project Analysis**

In our AxE project, we found hardcoded paths in:

1. **`systems/2x2_16_priority_input_approx/top.sv`** - 16 hardcoded include paths
2. **`rtl/memory/bram.sv`** - 1 hardcoded memory file path

```systemverilog
// Example of what we found:
`include "/home/user/soc_frame/rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
`include "/home/user/soc_frame/rtl/clk_gater/clk_gater.sv"
$readmemh("/home/user/soc_frame/mem.hex", mem, 0);
```

---

## 🛠️ **Step 3: SystemVerilog Syntax and Solution Approaches**

### **📚 SystemVerilog Include Syntax Deep Dive**

#### **Basic `include Syntax**

```systemverilog
// Basic include directive syntax
`include "filename.extension"

// Examples of different file types
`include "defines.vh"           // Header files (.vh)
`include "module.sv"            // SystemVerilog modules (.sv)
`include "legacy.v"             // Verilog modules (.v)
```

**Key Syntax Rules:**
- **Backtick prefix**: `include (not include)
- **Quoted filename**: Always use double quotes
- **Preprocessor directive**: Processed before compilation
- **Path resolution**: Relative to including file's directory

#### **How Include Works Internally**

```systemverilog
// File: defines.vh
`define MEMORY_PATH "mem.hex"
`define CLOCK_FREQ 100000000

// File: top.sv  
`include "defines.vh"           // ← Preprocessor copies content here
module top();
    // Now we can use the macros
    initial $readmemh(`MEMORY_PATH, memory);
endmodule

// After preprocessing (what compiler sees):
`define MEMORY_PATH "mem.hex"   // ← Content from defines.vh
`define CLOCK_FREQ 100000000    // ← Content from defines.vh
module top();
    initial $readmemh(`MEMORY_PATH, memory);
endmodule
```

**Critical Understanding:**
- **Text Substitution**: Include literally copies file content
- **Order Matters**: Includes processed top-to-bottom
- **Scope**: Macros available after include point
- **No Duplication Protection**: Same file can be included multiple times

#### **Advanced Include Guard Syntax**

```systemverilog
// File: defines_paths.vh - Professional include guard
`ifndef DEFINES_PATHS_VH        // If not defined
`define DEFINES_PATHS_VH        // Define guard macro

// Your actual definitions here
`define MEMORY_HEX_PATH "../../../mem.hex"
`define ROUTING_TABLE_0 "../../../tools/routing_0.hex"

`endif                          // End guard
```

**Why Include Guards:**
- **Prevent Redefinition**: Avoid macro redefinition errors
- **Performance**: Skip re-processing if already included
- **Safety**: Standard practice in professional code

### **🔧 SystemVerilog Macro Definition Syntax**

#### **Basic Macro Syntax**

```systemverilog
// Simple text replacement macro
`define MACRO_NAME replacement_text

// Examples
`define CLK_FREQ 100_000_000
`define RESET_ACTIVE 1'b0
`define MEMORY_SIZE 1024
```

#### **String Macros for Paths**

```systemverilog
// String macros (note the quotes)
`define MEMORY_FILE "memory.hex"
`define LOG_FILE "simulation.log"

// Path macros with directory structure
`define TOOLS_DIR "../../../tools"
`define MEMORY_PATH `TOOLS_DIR"/mem.hex"    // Concatenation

// Usage in code
initial begin
    $readmemh(`MEMORY_FILE, mem_array);     // Expands to "memory.hex"
    $readmemh(`MEMORY_PATH, mem_array);     // Expands to "../../../tools/mem.hex"
end
```

#### **Parameterized Macros (Advanced)**

```systemverilog
// Macro with parameters
`define CREATE_MEMORY(name, size, init_file) \
    reg [7:0] name [0:size-1]; \
    initial $readmemh(init_file, name);

// Usage
`CREATE_MEMORY(program_mem, 1024, "program.hex")
`CREATE_MEMORY(data_mem, 2048, "data.hex")
```

### **💡 File Reading Syntax in SystemVerilog**

#### **$readmemh Syntax**

```systemverilog
// Basic syntax
$readmemh("filename", memory_array);

// With start/end addresses
$readmemh("filename", memory_array, start_addr);
$readmemh("filename", memory_array, start_addr, end_addr);

// Real examples from our project
initial begin
    // Simple filename - searches in working directory
    $readmemh("mem.hex", mem, 0);
    
    // Relative path from execution directory
    $readmemh("../../../mem.hex", mem, 0);
    
    // Using macro (recommended)
    $readmemh(`MEMORY_HEX_PATH, mem, 0);
end
```

#### **File Format for $readmemh**

```
// mem.hex - Example hexadecimal memory file
@00000000    // Address (optional)
12345678     // 32-bit hex value
ABCDEF01     // Another value
@00000010    // Jump to address 0x10
DEADBEEF     // Value at 0x10
CAFEBABE     // Value at 0x11
```

**Key Points:**
- **Hexadecimal format**: Values in hex (no 0x prefix)
- **Address directives**: @address sets current location
- **No commas**: Just whitespace between values
- **Comments**: // supported

### **🏗️ Solution Approaches for Path Management**

### **Approach 1: Relative Paths (Our Implementation)**

**Concept**: Use paths relative to execution directory

```systemverilog
// ✅ CURRENT IMPLEMENTATION: Relative paths optimized for obj_dir
`include "../../rtl/noc/noc_connect_2x2_16/mkInputQueue.v"

// Memory files relative to obj_dir execution
$readmemh("../../../mem.hex", mem, 0);
```

**Directory Context Understanding:**
```
soc_frame/
├── systems/2x2_16_priority_input_approx/
│   ├── obj_dir/           ← Verilator runs here
│   │   └── Vtop           ← Generated executable
│   └── top.sv             ← Source files here
├── rtl/                   ← Target modules
└── tools/
    └── mem.hex            ← Memory files
```

**Path Calculation from obj_dir:**
```
../../../mem.hex           → soc_frame/mem.hex
../../rtl/module.sv        → soc_frame/rtl/module.sv
../../../tools/file.hex    → soc_frame/tools/file.hex
```

### **Approach 2: Centralized Macro System (Recommended)**

**Implementation**: Central header with all path definitions

```systemverilog
// File: rtl/defines_paths.vh
`ifndef DEFINES_PATHS_VH
`define DEFINES_PATHS_VH

// Memory file paths - optimized for obj_dir execution
`define MEMORY_HEX_PATH "../../../mem.hex"

// NoC routing table paths (real examples from our project)
`define ROUTING_TABLE_0 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_0.hex"
`define ROUTING_TABLE_1 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_1.hex"
`define ROUTING_TABLE_2 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_2.hex"
`define ROUTING_TABLE_3 "../../../tools/mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_3.hex"

`endif
```

**Usage in RTL Files:**

```systemverilog
// Include the path definitions
`include "../../rtl/defines_paths.vh"

// Use in memory initialization
initial begin
    $readmemh(`MEMORY_HEX_PATH, mem, 0);
end

// Use in module instantiation (RegFileLoadSyn example)
RegFileLoadSyn #(
    .file(`ROUTING_TABLE_0),    // ← Macro expands to full path
    .width(width),
    .depth(depth)
) routing_table_0 (
    // port connections
);
```

### **Approach 3: Environment Variables (Advanced)**

**Concept**: Use environment variables for maximum flexibility

```systemverilog
// This approach has limitations in SystemVerilog
// Environment variables are not directly supported in preprocessor
`include "$SOC_FRAME_ROOT/rtl/module.sv"  // ← Does NOT work

// Would require external preprocessing or tool support
```

**Why Environment Variables Don't Work Well:**
- **Preprocessor Limitation**: SystemVerilog preprocessor doesn't expand environment variables
- **Tool Dependency**: Would need external tools to substitute variables
- **Synthesis Issues**: Many synthesis tools don't support dynamic paths

**Better Alternative - Makefile Variables:**
```makefile
# In Makefile
SOC_FRAME_ROOT = /path/to/soc_frame
VERILATOR_FLAGS += -DSOC_FRAME_ROOT=\"$(SOC_FRAME_ROOT)\"

# In SystemVerilog
`include `SOC_FRAME_ROOT"/rtl/module.sv"
```

---

## 🔧 **Step 4: Implementation Guide**

### **Implementation: Relative Path Solution**

This is the approach we used for the AxE project.

#### **Step 4.1: Analyze Directory Structure**

```
soc_frame/
├── systems/
│   └── 2x2_16_priority_input_approx/
│       └── top.sv                          # Working directory
├── rtl/
│   ├── noc/
│   │   └── noc_connect_2x2_16/
│   │       └── mkInputQueue.v              # Target file
│   └── memory/
│       └── bram.sv
└── tools/
    └── mem.hex
```

#### **Step 4.2: Calculate Relative Paths**

From `systems/2x2_16_priority_input_approx/top.sv` to `rtl/noc/noc_connect_2x2_16/mkInputQueue.v`:

```
Path: ../.. → soc_frame/
      /rtl  → rtl/
      /noc/noc_connect_2x2_16/mkInputQueue.v
Final: "../../rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
```

#### **Step 4.3: Apply the Fix**

**Before:**
```systemverilog
`include "/home/user/soc_frame/rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
`include "/home/user/soc_frame/rtl/clk_gater/clk_gater.sv"
$readmemh("/home/user/soc_frame/mem.hex", mem, 0);
```

**After:**
```systemverilog
`include "../../rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
`include "../../rtl/clk_gater/clk_gater.sv"
$readmemh("mem.hex", mem, 0);
```

#### **Step 4.4: Systematic Replacement**

We replaced all 16 hardcoded paths in `top.sv`:

```systemverilog
// Network-on-Chip includes
`include "../../rtl/noc/noc_connect_2x2_16/mkInputQueue.v"
`include "../../rtl/noc/noc_connect_2x2_16/mkIQRouterCoreSimple.v"
`include "../../rtl/noc/noc_connect_2x2_16/mkNetworkSimple.v"
`include "../../rtl/noc/noc_connect_2x2_16/mkOutPortFIFO.v"
`include "../../rtl/noc/noc_connect_2x2_16/mkRouterInputArbitersRoundRobin.v"
`include "../../rtl/noc/noc_connect_2x2_16/mkRouterOutputArbitersRoundRobin.v"
`include "../../rtl/noc/noc_connect_2x2_16/mkSepRouterAllocator.v"
`include "../../rtl/noc/noc_connect_2x2_16/module_gen_grant_carry.v"
`include "../../rtl/noc/noc_connect_2x2_16/module_outport_encoder.v"
`include "../../rtl/noc/noc_connect_2x2_16/RegFile_1port.v"
`include "../../rtl/noc/noc_connect_2x2_16/RegFileLoadSyn.v"

// Core system includes
`include "../../rtl/clk_gater/clk_gater.sv"
`include "../../rtl/node_clk_gating.sv"
`include "../../rtl/controller_axi.sv"
`include "../../rtl/memory_controller_priority_input.sv"

// Conditional includes (synthesis only)
`ifdef SYNTHESIS
    `include "../../rtl/uart/uart.sv"
    `include "../../rtl/uart/uart_clk.sv"
    `include "../../rtl/uart/uart_tx.sv"
`endif
```

---

## 🧪 **Step 5: Testing and Validation**

### **Validation Process**

1. **Clean Build**: Remove all generated files
2. **Compilation Test**: Run Verilator compilation
3. **Simulation Test**: Execute generated simulation
4. **Error Analysis**: Check for any remaining path issues

### **AxE Project Test Results**

**Before Fix:**
```
%Error: top.sv:72:10: Cannot find include file: '/home/user/soc_frame/rtl/noc/noc_connect_2x2_16/mkInputQueue.v'
[15+ similar errors]
```

**After Fix:**
```
%Warning-SHORTREAL: ../../rtl/PiXo/picorv32_extended.v:3945:19: Unsupported: shortreal being promoted to real
[Only warnings, no path errors]
--------------------
starting 2x2_16
--------------------
```

✅ **SUCCESS**: System compiles and runs successfully!

---

## 🔧 **Step 6: Additional Fixes**

### **Verilator Timing Issue**

During testing, we encountered:
```
%Error-NEEDTIMINGOPT: Use --timing or --no-timing to specify how delays should be handled
```

**Solution**: Added `--no-timing` flag to Verilator options in `Makefile_include`:

```makefile
VERILATOR_FLAGS += -cc --exe --no-timing
```

### **File Working Directory**

For memory files, we simplified the path to work from the execution directory:

```systemverilog
// Simple filename - looks in current working directory
$readmemh("mem.hex", mem, 0);
```

---

## 📊 **Step 7: Best Practices**

### **1. Path Management Strategy**

**Choose the Right Approach:**
- **Simple projects**: Use relative paths
- **Complex projects**: Use environment variables
- **Team projects**: Use preprocessor macros with centralized headers

### **2. Directory Structure Guidelines**

```
project/
├── rtl/               # All RTL source files
│   ├── common/        # Shared modules
│   ├── cores/         # Processor cores
│   └── interfaces/    # Interface definitions
├── systems/           # Top-level system configurations
│   └── system_name/   # Individual system directories
├── tools/             # Build and simulation tools
└── docs/              # Documentation
```

### **3. Documentation Requirements**

Always document:
- **Path conventions** used in the project
- **Directory structure** and its purpose
- **Build requirements** and environment setup
- **Testing procedures** for path validation

### **4. Code Review Checklist**

Before merging RTL code:
- [ ] No hardcoded absolute paths
- [ ] Consistent relative path usage
- [ ] Environment variables properly used
- [ ] Paths work from expected execution directory
- [ ] Documentation updated

---

## 🎓 **Learning Summary**

### **Key Concepts Mastered**

1. **Path Management**: Understanding different approaches to handle file paths in RTL
2. **Relative Paths**: Using paths relative to execution directory
3. **Environment Variables**: Leveraging system environment for configuration
4. **Preprocessor Macros**: Using SystemVerilog preprocessor for path management

### **Problem-Solving Methodology**

1. **Identify**: Use grep and find commands to locate hardcoded paths
2. **Analyze**: Understand directory structure and path relationships
3. **Design**: Choose appropriate solution approach
4. **Implement**: Apply systematic path replacement
5. **Test**: Validate through compilation and simulation
6. **Document**: Record changes and best practices

### **Tools and Techniques**

- **grep/find**: For path detection
- **Relative path calculation**: Understanding directory navigation
- **SystemVerilog preprocessor**: For advanced path management
- **Verilator**: For RTL compilation and simulation
- **Makefiles**: For build system integration

---

## 🔍 **Troubleshooting Guide**

### **Common Issues**

**Issue 1: "Cannot find include file"**
```
%Error: Cannot find include file: 'path/to/file.v'
```
**Solution**: Check path is correct relative to working directory

**Issue 2: "File not found" during simulation**
```
%Warning: mem.hex:0: $readmem file not found
```
**Solution**: Ensure file exists in expected directory or adjust path

**Issue 3: "Multiple top level modules"**
```
%Warning-MULTITOP: Multiple top level modules
```
**Solution**: Use `--top-module` flag in Verilator or fix module hierarchy

### **Debugging Steps**

1. **Verify working directory**: `pwd` during build
2. **Check file existence**: `ls -la path/to/file`
3. **Trace path resolution**: Use verbose compilation flags
4. **Test incremental**: Fix one path at a time

---

## 📚 **Additional Resources**

### **SystemVerilog Path Management**
- SystemVerilog LRM: File I/O and path handling
- Verilator documentation: Include path resolution
- Industry standards: RTL project organization

### **Build System Integration**
- Makefile path management
- Environment variable best practices
- CI/CD pipeline considerations

### **Team Collaboration**
- Code review guidelines for path management
- Documentation standards
- Testing procedures for portable code

---

**This tutorial provides a comprehensive foundation for managing paths in RTL projects. The methodology can be applied to any hardware project requiring portable, maintainable code.**