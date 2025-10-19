# 🔧 AxE Configuration Management Guide

## 📋 Overview

AxE uses **modern YAML configuration files** for better readability, maintainability, and user experience. This guide explains the configuration system and provides comprehensive examples.

### **🚀 Key Benefits of YAML Configuration**

1. **Better Readability**: Hierarchical structure with comments and documentation
2. **Type Safety**: Native support for lists, booleans, numbers
3. **Modern Standard**: Industry-standard format used by Docker, Kubernetes, CI/CD
4. **Rich Comments**: Comprehensive inline documentation and examples
5. **Clean and Simple**: Single configuration format to learn

---

## 📁 **Configuration File Detection**

The system automatically detects and loads YAML configuration files in this priority order:

1. **`config_name.yaml`** (Preferred extension)
2. **`config_name.yml`** (Alternative YAML extension)
3. **`config_name`** (Raw filename)

### **Usage Examples:**
```bash
# All these commands will find the appropriate YAML config file:
python run_mpsoc.py _2x2_main         # Finds _2x2_main.yaml first
python run_mpsoc.py _2x2_main.yaml    # Explicit YAML
python run_mpsoc.py my_experiment     # Finds my_experiment.yaml
```

---

## 🎯 **YAML Configuration Format**

### **Complete Example: `_2x2_main.yaml`**

```yaml
# AxE Configuration - 2x2 Mesh System with Approximate Computing
# Modern YAML format for better readability and maintainability

# Controller Configuration
controller:
  # Controller type selection
  name: thesis_edh  # Options: scheduler, thesis, thesis_edh
  
  # Power management settings
  save_mode_at: 100000000
  start_charging_at: -1  # -1 disables charging simulation
  stop_charging_at: -1   # -1 disables charging simulation

# System Architecture Configuration  
system:
  # System topology selection
  name: 2x2_16_priority_input_approx
  
  # Supported architectures list
  architectures:
    - rv32im  # RISC-V 32-bit with integer multiplication
  
  # Node architecture mapping (determines number of nodes)
  node_architectures:
    - im  # Node 0: Integer + Multiplication

# Execution Configuration
run:
  # Execution mode selection
  mode: prgs  # Options: prgs (programs), tasks (generated tasks)
  
  # Timing configuration
  exec_interval_modifier: 1.0

# Program Configuration (when run.mode = prgs)
programs:
  program_list:
    - mul  # Multiplication benchmark

# Task Generation Configuration (when run.mode = tasks)
tasks:
  count: 3
  loop_count:
    min: 1000
    max: 1000
  multiplication_percentage:
    min: 50
    max: 50

# Simulation Configuration
simulation:
  arguments: []  # Empty for normal simulation
  print_output: true
```

---


---

## 🎛️ **Configuration Options Reference**

### **Controller Section**

| YAML Path | Type | Description | Options |
|-----------|------|-------------|---------|
| `controller.name` | string | Controller algorithm | `scheduler`, `thesis`, `thesis_edh` |
| `controller.save_mode_at` | int | Save mode trigger cycle | Positive integer |
| `controller.start_charging_at` | int | Start energy harvest | Cycle number or -1 to disable |
| `controller.stop_charging_at` | int | Stop energy harvest | Cycle number or -1 to disable |

### **System Section**

| YAML Path | Type | Description | Options |
|-----------|------|-------------|---------|
| `system.name` | string | System topology | See [System Configurations](#system-configurations) |
| `system.architectures` | list | Supported ISA | `["rv32i"]`, `["rv32im"]`, `["rv32i", "rv32im"]` |
| `system.node_architectures` | list | Per-node ISA | `["i"]`, `["im"]`, `["i", "im"]` |

### **Run Section**

| YAML Path | Type | Description | Options |
|-----------|------|-------------|---------|
| `run.mode` | string | Execution mode | `prgs`, `tasks` |
| `run.exec_interval_modifier` | float | Timing multiplier | Positive float |

### **Programs Section (when run.mode = prgs)**

| YAML Path | Type | Description | Options |
|-----------|------|-------------|---------|
| `programs.program_list` | list | Programs to run | See [Available Programs](#available-programs) |

### **Tasks Section (when run.mode = tasks)**

| YAML Path | Type | Description | Range |
|-----------|------|-------------|-------|
| `tasks.count` | int | Number of tasks | 1-100 |
| `tasks.loop_count.min` | int | Min loop iterations | 1-10000 |
| `tasks.loop_count.max` | int | Max loop iterations | 1-10000 |
| `tasks.multiplication_percentage.min` | int | Min multiplication % | 0-100 |
| `tasks.multiplication_percentage.max` | int | Max multiplication % | 0-100 |

### **Simulation Section**

| YAML Path | Type | Description | Options |
|-----------|------|-------------|---------|
| `simulation.arguments` | list | Simulator flags | `[]`, `["+trace"]` |
| `simulation.print_output` | bool | Output control | `true`, `false` |

---

## 🏗️ **System Configurations**

### **Available System Topologies**

```yaml
system:
  name: 2x2_16_priority_input          # 2x2 mesh, exact cores only
  # name: 2x2_16_priority_input_approx  # 2x2 mesh, approximate cores
  # name: 3x3_16_priority_input         # 3x3 mesh
  # name: 4x4_16_priority_input         # 4x4 mesh  
  # name: 4x5_16_priority_input         # 4x5 mesh
  # name: mult_noc_interface            # Single core with NoC
  # name: mult_noc_interface_vivado     # Vivado-optimized single core
```

### **Architecture Combinations**

```yaml
system:
  # Integer-only configuration
  architectures: [rv32i]
  node_architectures: [i, i, i, i]  # 4 nodes, all integer-only
  
  # Mixed configuration
  architectures: [rv32i, rv32im]
  node_architectures: [i, i, im, im]  # 2 exact + 2 approximate
  
  # Multiplication-enabled configuration  
  architectures: [rv32im]
  node_architectures: [im]  # Single node with multiplication
```

---

## 📚 **Available Programs**

### **Computational Benchmarks**
```yaml
programs:
  program_list:
    - mul                 # Multiplication benchmark
    - tridiagonal         # Tridiagonal matrix solver
    - fft                 # Fast Fourier Transform
    - matrix_multiply     # Matrix multiplication
    - square_mmult        # Square matrix multiplication
```

### **Algorithm Benchmarks**
```yaml
programs:
  program_list:
    - qsort              # Quick sort algorithm
    - msort              # Merge sort algorithm
    - shortest_path      # Graph shortest path
    - max_subseq         # Maximum subsequence
```

### **Cryptography & Security**
```yaml
programs:
  program_list:
    - aes                # Advanced Encryption Standard
    - blowfish           # Blowfish encryption
    - sha                # SHA hash algorithm
    - sha256             # SHA-256 hash algorithm
```

### **Image & Signal Processing**
```yaml
programs:
  program_list:
    - sharpen            # Image sharpening filter
    - grayscale          # RGB to grayscale conversion
    - audio_codec        # Audio compression/decompression
```

---

## 🛠️ **Configuration Templates**

### **Template 1: Single Core Testing**
```yaml
# File: single_core_test.yaml
controller:
  name: thesis_edh
  save_mode_at: 100000000
  start_charging_at: -1
  stop_charging_at: -1

system:
  name: 2x2_16_priority_input_approx
  architectures: [rv32im]
  node_architectures: [im]

run:
  mode: prgs
  exec_interval_modifier: 1.0

programs:
  program_list: [mul]

simulation:
  arguments: []
  print_output: true
```

### **Template 2: Multi-Core Performance Study**
```yaml
# File: multicore_performance.yaml
controller:
  name: thesis_edh
  save_mode_at: 100000000
  start_charging_at: -1
  stop_charging_at: -1

system:
  name: 4x4_16_priority_input
  architectures: [rv32i, rv32im]
  node_architectures: [i, i, i, i, i, i, i, i, im, im, im, im, im, im, im, im]

run:
  mode: prgs
  exec_interval_modifier: 1.0

programs:
  program_list: [fft, matrix_multiply, qsort, aes]

simulation:
  arguments: []
  print_output: true
```

### **Template 3: Energy Harvesting Study**
```yaml
# File: energy_harvesting.yaml
controller:
  name: thesis_edh
  save_mode_at: 50000000
  start_charging_at: 3218725    # Start harvesting
  stop_charging_at: 4218725     # Stop harvesting

system:
  name: 2x2_16_priority_input_approx
  architectures: [rv32i, rv32im]
  node_architectures: [i, im]

run:
  mode: tasks
  exec_interval_modifier: 2.0   # Slower execution for energy study

tasks:
  count: 10
  loop_count:
    min: 500
    max: 2000
  multiplication_percentage:
    min: 30
    max: 70

simulation:
  arguments: []
  print_output: true
```

### **Template 4: Debug Configuration**
```yaml
# File: debug_trace.yaml
controller:
  name: scheduler
  save_mode_at: 1000000        # Early save for debugging
  start_charging_at: -1
  stop_charging_at: -1

system:
  name: 2x2_16_priority_input
  architectures: [rv32i]
  node_architectures: [i]

run:
  mode: prgs
  exec_interval_modifier: 1.0

programs:
  program_list: [add]          # Simple program for debugging

simulation:
  arguments: ["+trace"]        # Enable waveform tracing
  print_output: true
```

---


---

## 🔍 **Troubleshooting**

### **Common Issues and Solutions**

#### **Issue: "PyYAML not installed"**
```bash
# Solution: Install PyYAML
pip install PyYAML
# or
apt install python3-yaml
```

#### **Issue: "YAML parsing error"**
```yaml
# Problem: Incorrect YAML syntax
controller:
name: thesis_edh  # ❌ Missing indentation

# Solution: Proper indentation
controller:
  name: thesis_edh  # ✅ Correct indentation
```

#### **Issue: "Configuration section missing"**
```bash
# Error: YAML config missing required sections: ['simulation']
# Solution: Check section names match exactly
simulation:  # ✅ Not 'sim'
  print_output: true
```


---

## 📈 **Best Practices**

### **1. Configuration Naming Convention**
```
experiment_name.yaml          # Main config
experiment_name_debug.yaml    # Debug variant
experiment_name_energy.yaml   # Energy study variant
experiment_name_single.yaml   # Single core variant
```

### **2. Comment Documentation**
```yaml
controller:
  name: thesis_edh  # Energy-aware heterogeneous controller
  
  # Power management (cycles)
  save_mode_at: 100000000      # Enter low-power mode
  start_charging_at: 3218725   # Begin energy harvesting simulation
  stop_charging_at: 4218725    # End energy harvesting simulation
```

### **3. Environment-Specific Configs**
```yaml
# development.yaml - Fast debugging
simulation:
  arguments: ["+trace"]
  print_output: true

# production.yaml - Performance measurement  
simulation:
  arguments: []
  print_output: false

# research.yaml - Comprehensive analysis
simulation:
  arguments: ["+trace", "+coverage"]
  print_output: true
```

---

**The YAML configuration system brings AxE into the modern era with clean, readable, and maintainable configuration files!** 🎉