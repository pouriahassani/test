# AxE Research Platform - Development Environment

## Overview

The AxE (Approximate eXecution) Research Platform provides a comprehensive development environment for energy-efficient computing research. This Docker-based setup includes all necessary tools for developing and analyzing heterogeneous approximate/exact RISC-V processor systems.

## Features

### 🔬 Research-Focused Environment
- **Heterogeneous Computing**: Support for both exact and approximate RISC-V processors
- **Energy Analysis**: Tools for power consumption and energy efficiency research
- **NoC Simulation**: Network-on-Chip modeling and analysis
- **Algorithm Development**: Python-based partitioning and optimization algorithms

### 🛠️ Development Tools
- **RISC-V Toolchain**: Cross-compilation for RV32I/RV32IM architectures
- **Verilator**: Hardware simulation and synthesis
- **Python Scientific Stack**: NumPy, Matplotlib, Pandas, SciPy
- **Jupyter Lab**: Interactive research and analysis environment
- **VSCode Integration**: Full IDE support with extensions

### 📊 Analysis Capabilities
- **Partitioning Algorithms**: Complete and divided partitioning strategies
- **Energy Modeling**: Battery-powered system simulation
- **Quality Analysis**: Approximation error and trade-off evaluation
- **Performance Metrics**: Timing analysis and optimization

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the AxE repository
git clone <repository-url>
cd AxE

# Start the research environment
docker-compose -f docker-compose.public.yml up -d

# Access the container
docker exec -it axe-research-environment bash

# Verify the environment
./check_environment.sh
```

### Option 2: Direct Docker Commands

```bash
# Build the research environment
docker build -f Dockerfile.public -t axe:research-platform .

# Run with workspace mounted
docker run -it -v $(pwd):/home/researcher axe:research-platform

# Run with port forwarding for Jupyter
docker run -it -p 8888:8888 -v $(pwd):/home/researcher axe:research-platform
```

### Option 3: VSCode Dev Containers

1. Install the "Dev Containers" extension in VSCode
2. Copy `.devcontainer-public/` to `.devcontainer/`
3. Copy `.vscode-public/` to `.vscode/`
4. Press `Ctrl+Shift+P` and select "Dev Containers: Reopen in Container"
5. VSCode will build and open the container automatically

## Development Workflow

### 1. Environment Verification

```bash
# Check all development tools
./check_environment.sh

# Verify RISC-V toolchain
riscv32-unknown-elf-gcc --version

# Test Python environment
python3 -c "import numpy, matplotlib, pandas; print('Scientific stack ready!')"
```

### 2. Hardware Development

```bash
# Navigate to hardware framework
cd soc_frame

# Build hardware simulation
make

# Build software components
make sw

# Run specific simulations
make simulate CONFIG=2x2_exact
```

### 3. Algorithm Research

```bash
# Complete partitioning analysis
cd Complete_partitioning
python3 main.py

# Divided partitioning with different parameters
cd ../Divided_Partitioning
python3 main.py --deadline-pressure 5

# Comparative analysis
cd ../Divided_Partitioning_3SYS_2_ALGO
python3 main.py --systems AXE,EXE,FULL
```

### 4. Interactive Research

```bash
# Start Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Access via browser: http://localhost:8888
# Default password: (none, token-based authentication)
```

## VSCode Development

### Available Tasks (Ctrl+Shift+P → "Tasks: Run Task")

- **AxE: Build Hardware** - Compile RTL and generate simulation
- **AxE: Build Software** - Cross-compile RISC-V applications
- **AxE: Check Environment** - Verify development setup
- **AxE: Run Complete Partitioning** - Execute partitioning analysis
- **AxE: Jupyter Lab** - Start interactive research environment

### Pre-configured Extensions

- **Python Development**: pylint, black, flake8 for code quality
- **Hardware Description**: Verilog/SystemVerilog syntax support
- **C/C++ Tools**: RISC-V cross-development support
- **Documentation**: Markdown preview and editing
- **Version Control**: Enhanced Git integration

## Research Applications

### Energy-Efficient Computing
- Battery-powered IoT device optimization
- Mobile system energy analysis
- Edge computing power management

### Approximate Computing
- Quality vs. energy trade-off analysis
- Application-specific approximation strategies
- Heterogeneous processing optimization

### RISC-V Development
- Custom instruction set exploration
- Cross-compilation and optimization
- Embedded system development

## Project Structure

```
/home/researcher/                 # Your workspace
├── soc_frame/                   # Hardware framework
│   ├── rtl/                     # Verilog/SystemVerilog sources
│   ├── sw/                      # Software benchmarks
│   └── Makefile                 # Build system
├── Complete_partitioning/       # Exhaustive optimization
├── Divided_Partitioning/        # Parametric analysis
├── Divided_Partitioning_3SYS_2_ALGO/  # Comparative study
├── docs/                        # Documentation
└── README-DEVELOPMENT.md        # This guide
```

## Troubleshooting

### Container Issues

```bash
# Rebuild container
docker-compose -f docker-compose.public.yml build --no-cache

# Check container logs
docker logs axe-research-environment

# Reset environment
docker-compose -f docker-compose.public.yml down
docker system prune -f
```

### Tool Problems

```bash
# Reinstall Python packages
pip3 install --user --upgrade --force-reinstall numpy matplotlib pandas

# Check RISC-V toolchain
which riscv32-unknown-elf-gcc
ls -la /opt/riscv/bin/

# Verify Verilator
verilator --version
which verilator
```

### VSCode Integration

```bash
# Reload VSCode window
Ctrl+Shift+P → "Developer: Reload Window"

# Rebuild dev container
Ctrl+Shift+P → "Dev Containers: Rebuild Container"

# Check extension status
Ctrl+Shift+P → "Extensions: Show Installed Extensions"
```

## Research Workflow Examples

### Energy Analysis

```python
# Example: Analyze energy consumption
import numpy as np
import matplotlib.pyplot as plt
from soc_frame.analysis import EnergyModel

# Load experimental data
results = EnergyModel.load_results('partition_results.csv')

# Plot energy vs quality trade-offs
plt.figure(figsize=(10, 6))
plt.scatter(results['quality'], results['energy'])
plt.xlabel('Approximation Quality')
plt.ylabel('Energy Consumption (mJ)')
plt.title('Energy-Quality Trade-off Analysis')
plt.show()
```

### Hardware Simulation

```bash
# Simulate 2x2 NoC with approximate cores
cd soc_frame
make simulate CONFIG=noc_2x2_approx BENCHMARK=fft

# Generate synthesis reports
make synthesize TARGET=fpga CONFIG=4x4_mixed

# Analyze timing results
python3 scripts/analyze_timing.py results/timing_report.json
```

## Contributing

This research platform is designed for academic and research use. Contributions are welcome for:

- New approximation algorithms
- Hardware optimizations
- Analysis tools and visualizations
- Documentation improvements
- Bug fixes and performance enhancements

## License

This project is released under an academic research license. Please cite our work if you use this platform in your research.

## Support

For technical issues and research collaboration:
- Check the troubleshooting section above
- Review the comprehensive documentation in `docs/`
- Contact the research team for collaboration opportunities

---

**The AxE Research Platform - Advancing Energy-Efficient Computing Through Approximate Execution**
