#!/bin/bash

# AxE Public Development Environment Setup Script
# Creates a professional Docker environment for AxE research platform
# Suitable for public distribution and academic use

set -euo pipefail

# =============================================================================
# COLOR DEFINITIONS
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${PURPLE}===============================================================================${NC}"
    echo -e "${WHITE}$1${NC}"
    echo -e "${PURPLE}===============================================================================${NC}"
    echo ""
}

# =============================================================================
# MAIN SETUP FUNCTIONS
# =============================================================================

create_public_dockerfile() {
    log_section "CREATING PUBLIC DOCKERFILE FOR AxE DEVELOPMENT"
    
    # Backup current Dockerfile if it exists
    if [[ -f "Dockerfile.public" ]]; then
        cp Dockerfile.public Dockerfile.public.backup
        log_info "Backed up Dockerfile.public to Dockerfile.public.backup"
    fi
    
    # Create optimized public Dockerfile
    cat > Dockerfile.public << 'EOF'
# AxE (Approximate eXecution) Research Platform - Development Environment
# Professional Docker container for energy-efficient computing research
# Supports heterogeneous approximate/exact RISC-V processor development
FROM ubuntu:25.04

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Development user configuration
ENV USERNAME=researcher
ENV USER_UID=1001
ENV USER_GID=1001
ENV HOME=/home/researcher
ENV WORKDIR=/home/researcher

# AxE project paths
ENV SOC_FRAME_PATH=${WORKDIR}/soc_frame
ENV RISCV_PATH=/opt/riscv
ENV VERILATOR_PATH=${WORKDIR}/verilator

# =============================================================================
# SYSTEM DEPENDENCIES - OPTIMIZED FOR AxE DEVELOPMENT
# =============================================================================

RUN apt-get update && apt-get install -y \
    # Build essentials for RISC-V and hardware synthesis
    build-essential gcc g++ cmake make \
    # Version control and development tools
    git curl wget unzip vim nano \
    # Python ecosystem for algorithm development
    python3 python3-pip python3-venv python3-dev \
    # RISC-V GNU toolchain dependencies
    autoconf automake autotools-dev \
    libmpc-dev libmpfr-dev libgmp-dev \
    gawk bison flex texinfo gperf libtool \
    patchutils bc zlib1g-dev libexpat-dev \
    # Verilator and hardware simulation dependencies
    ninja-build perl ccache \
    libfl2 libfl-dev zlib1g zlib1g-dev \
    libtcmalloc-minimal4 numactl \
    perl-doc help2man \
    # Development utilities
    htop tree jq sudo \
    lsb-release ca-certificates \
    # VSCode dev container support
    openssh-client procps psmisc \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# USER CREATION FOR DEVELOPMENT
# =============================================================================

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME && \
    usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Create directories and set permissions
RUN mkdir -p $RISCV_PATH && chown $USERNAME:$USERNAME $RISCV_PATH && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME

# Switch to development user
USER $USERNAME
WORKDIR $WORKDIR

# =============================================================================
# PYTHON DEVELOPMENT ENVIRONMENT
# =============================================================================

# Upgrade pip and install scientific computing stack
RUN python3 -m pip install --user --upgrade pip --break-system-packages

# Install Python packages for AxE research and development
RUN pip3 install --user --no-cache-dir --break-system-packages \
    # Scientific computing stack
    numpy>=1.26.0 \
    matplotlib>=3.8.0 \
    pandas>=2.2.0 \
    scipy>=1.12.0 \
    seaborn>=0.13.0 \
    # Development and testing tools
    pytest>=8.0.0 \
    black>=24.0.0 \
    pylint>=3.0.0 \
    mypy>=1.8.0 \
    flake8>=7.0.0 \
    ruff>=0.2.0 \
    # Interactive development
    jupyterlab>=4.1.0 \
    ipykernel \
    # Utility libraries
    click>=8.1.0 \
    pyyaml>=6.0 \
    tqdm>=4.66.0 \
    rich>=13.7.0 \
    typer>=0.9.0

# =============================================================================
# LIGHTWEIGHT RISC-V TOOLCHAIN (PREBUILT)
# =============================================================================

# Download prebuilt RISC-V toolchain for faster container builds
RUN cd /tmp && \
    wget -q https://github.com/stnolting/riscv-gcc-prebuilt/releases/download/rv32i-4.0.0/riscv32-unknown-elf.gcc-12.1.0.tar.gz && \
    tar -xzf riscv32-unknown-elf.gcc-12.1.0.tar.gz -C $RISCV_PATH --strip-components=1 && \
    rm riscv32-unknown-elf.gcc-12.1.0.tar.gz

# =============================================================================
# VERILATOR INSTALLATION (LATEST)
# =============================================================================

# Install Verilator from package manager for faster builds
RUN sudo apt-get update && \
    sudo apt-get install -y verilator && \
    sudo rm -rf /var/lib/apt/lists/*

# =============================================================================
# SHELL ENVIRONMENT CONFIGURATION
# =============================================================================

# Configure development environment
ENV PATH="${RISCV_PATH}/bin:${HOME}/.local/bin:${PATH}"

# Enhanced bash configuration for AxE development
RUN echo '# AxE Research Platform Development Environment' >> ~/.bashrc && \
    echo 'export PS1="\\[\\033[01;32m\\]axe@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\[\\033[01;33m\\]⚡\\[\\033[00m\\]\\$ "' >> ~/.bashrc && \
    echo 'export TERM=xterm-256color' >> ~/.bashrc && \
    echo '' >> ~/.bashrc && \
    echo '# Development aliases' >> ~/.bashrc && \
    echo 'alias ll="ls -la --color=auto"' >> ~/.bashrc && \
    echo 'alias la="ls -A --color=auto"' >> ~/.bashrc && \
    echo 'alias python="python3"' >> ~/.bashrc && \
    echo 'alias pip="pip3"' >> ~/.bashrc && \
    echo '' >> ~/.bashrc && \
    echo '# Git configuration' >> ~/.bashrc && \
    echo 'alias gst="git status"' >> ~/.bashrc && \
    echo 'alias glog="git log --oneline --graph --color=always"' >> ~/.bashrc && \
    echo '' >> ~/.bashrc && \
    echo '# AxE environment variables' >> ~/.bashrc && \
    echo 'export RISCV="'$RISCV_PATH'"' >> ~/.bashrc && \
    echo 'export SOC_FRAME_PATH="'$SOC_FRAME_PATH'"' >> ~/.bashrc && \
    echo 'export PATH="'$RISCV_PATH'/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc

# =============================================================================
# UTILITY SCRIPTS FOR DEVELOPMENT
# =============================================================================

# Create environment verification script
RUN echo '#!/bin/bash' > check_environment.sh && \
    echo 'echo "=== AxE Development Environment Status ==="' >> check_environment.sh && \
    echo 'echo "Ubuntu: $(lsb_release -d | cut -f2)"' >> check_environment.sh && \
    echo 'echo "Python: $(python3 --version)"' >> check_environment.sh && \
    echo 'echo "GCC: $(gcc --version | head -1)"' >> check_environment.sh && \
    echo 'echo ""' >> check_environment.sh && \
    echo 'echo "=== RISC-V Toolchain ==="' >> check_environment.sh && \
    echo 'if command -v riscv32-unknown-elf-gcc &> /dev/null; then' >> check_environment.sh && \
    echo '    echo "RISC-V GCC: $(riscv32-unknown-elf-gcc --version | head -1)"' >> check_environment.sh && \
    echo '    echo "Location: $(which riscv32-unknown-elf-gcc)"' >> check_environment.sh && \
    echo 'else' >> check_environment.sh && \
    echo '    echo "RISC-V GCC: Not found in PATH"' >> check_environment.sh && \
    echo 'fi' >> check_environment.sh && \
    echo 'echo ""' >> check_environment.sh && \
    echo 'echo "=== Hardware Simulation ==="' >> check_environment.sh && \
    echo 'if command -v verilator &> /dev/null; then' >> check_environment.sh && \
    echo '    echo "Verilator: $(verilator --version)"' >> check_environment.sh && \
    echo 'else' >> check_environment.sh && \
    echo '    echo "Verilator: Not found"' >> check_environment.sh && \
    echo 'fi' >> check_environment.sh && \
    echo 'echo ""' >> check_environment.sh && \
    echo 'echo "=== Python Scientific Stack ==="' >> check_environment.sh && \
    echo 'python3 -c "import numpy, matplotlib, pandas; print(f\"NumPy: {numpy.__version__}, Matplotlib: {matplotlib.__version__}, Pandas: {pandas.__version__}\")" 2>/dev/null || echo "Python packages not fully installed"' >> check_environment.sh && \
    echo 'echo ""' >> check_environment.sh && \
    echo 'echo "=== Directory Structure ==="' >> check_environment.sh && \
    echo 'echo "Working Directory: $PWD"' >> check_environment.sh && \
    echo 'echo "User: $(whoami)"' >> check_environment.sh && \
    echo 'echo "RISCV: $RISCV"' >> check_environment.sh && \
    echo 'echo "SOC_FRAME_PATH: $SOC_FRAME_PATH"' >> check_environment.sh && \
    chmod +x check_environment.sh

# Welcome message for development environment
RUN echo 'echo ""' >> ~/.bashrc && \
    echo 'echo -e "\\033[1;36m🚀 AxE Research Platform Development Environment\\033[0m"' >> ~/.bashrc && \
    echo 'echo -e "\\033[0;33m   Energy-Efficient Computing | Approximate Execution | RISC-V\\033[0m"' >> ~/.bashrc && \
    echo 'echo ""' >> ~/.bashrc && \
    echo 'echo -e "\\033[1;32m   💡 Quick Start:\\033[0m"' >> ~/.bashrc && \
    echo 'echo -e "\\033[0;32m   ./check_environment.sh   \\033[0;37m- Verify development tools\\033[0m"' >> ~/.bashrc && \
    echo 'echo -e "\\033[0;32m   cd soc_frame && make      \\033[0;37m- Build hardware simulation\\033[0m"' >> ~/.bashrc && \
    echo 'echo -e "\\033[0;32m   make sw                   \\033[0;37m- Compile software benchmarks\\033[0m"' >> ~/.bashrc && \
    echo 'echo ""' >> ~/.bashrc

# Set default command
CMD ["/bin/bash", "-l"]
EOF

    log_success "Public Dockerfile created (optimized for research use)"
}

create_public_vscode_config() {
    log_section "CREATING PUBLIC VSCODE CONFIGURATION"
    
    # Create public devcontainer directory
    mkdir -p .devcontainer-public
    
    # Create devcontainer.json for public use
    cat > .devcontainer-public/devcontainer.json << 'EOF'
{
    "name": "AxE Research Platform",
    "build": {
        "dockerfile": "../Dockerfile.public",
        "context": ".."
    },
    
    // Workspace configuration
    "workspaceMount": "source=${localWorkspaceFolder},target=/home/researcher,type=bind",
    "workspaceFolder": "/home/researcher",
    
    // Use non-root user for security
    "remoteUser": "researcher",
    
    // VSCode settings optimized for research development
    "settings": {
        "terminal.integrated.defaultProfile.linux": "bash",
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black",
        "python.linting.flake8Enabled": true,
        "files.watcherExclude": {
            "**/obj_dir/**": true,
            "**/build/**": true,
            "**/.git/objects/**": true,
            "**/simulation_results/**": true,
            "**/synthesis_results/**": true
        },
        "files.associations": {
            "*.v": "verilog",
            "*.sv": "systemverilog",
            "*.vh": "verilog"
        }
    },
    
    // Extensions for AxE development
    "extensions": [
        // Python development
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.pylint",
        "ms-python.flake8",
        
        // Hardware development
        "mshr-h.veriloghdl",
        "eirikpre.systemverilog",
        
        // C/C++ for RISC-V development
        "ms-vscode.cpptools",
        
        // General development tools
        "ms-vscode.vscode-json",
        "redhat.vscode-yaml",
        "eamodio.gitlens",
        "yzhang.markdown-all-in-one",
        
        // Documentation and analysis
        "ms-vscode.hexeditor",
        "shd101wyy.markdown-preview-enhanced"
    ],
    
    // Port forwarding for Jupyter and web interfaces
    "forwardPorts": [8888, 8080, 3000],
    
    // Container initialization
    "postCreateCommand": "bash -c 'echo \"🚀 AxE Development Environment Ready!\" && ./check_environment.sh'",
    
    // Git integration (mount host git config if available)
    "mounts": [
        "source=${localEnv:HOME}/.gitconfig,target=/home/researcher/.gitconfig,type=bind,consistency=cached"
    ]
}
EOF

    # Create VSCode tasks for AxE development
    mkdir -p .vscode-public
    cat > .vscode-public/tasks.json << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "AxE: Build Hardware",
            "type": "shell",
            "command": "make",
            "options": {
                "cwd": "${workspaceFolder}/soc_frame"
            },
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "AxE: Build Software",
            "type": "shell",
            "command": "make",
            "args": ["sw"],
            "options": {
                "cwd": "${workspaceFolder}/soc_frame"
            },
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "AxE: Check Environment",
            "type": "shell",
            "command": "./check_environment.sh",
            "options": {
                "cwd": "${workspaceFolder}"
            },
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "AxE: Run Complete Partitioning",
            "type": "shell",
            "command": "python3",
            "args": ["main.py"],
            "options": {
                "cwd": "${workspaceFolder}/Complete_partitioning"
            },
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "AxE: Jupyter Lab",
            "type": "shell",
            "command": "jupyter",
            "args": ["lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"],
            "options": {
                "cwd": "${workspaceFolder}"
            },
            "group": "test",
            "isBackground": true,
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            }
        }
    ]
}
EOF

    # Create launch configuration for debugging
    cat > .vscode-public/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "AxE: Complete Partitioning Analysis",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/Complete_partitioning/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/Complete_partitioning",
            "args": []
        },
        {
            "name": "AxE: Divided Partitioning Analysis",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/Divided_Partitioning/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/Divided_Partitioning",
            "args": []
        }
    ]
}
EOF

    log_success "Public VSCode configuration created"
}

create_public_docker_compose() {
    log_section "CREATING PUBLIC DOCKER COMPOSE"
    
    cat > docker-compose.public.yml << 'EOF'
version: '3.8'

services:
  axe-research:
    build:
      context: .
      dockerfile: Dockerfile.public
    image: axe:research-platform
    container_name: axe-research-environment
    
    # Mount workspace to researcher home directory
    volumes:
      - .:/home/researcher
      - /tmp/.X11-unix:/tmp/.X11-unix:rw  # X11 forwarding for GUI apps
    
    # Interactive terminal
    stdin_open: true
    tty: true
    
    # Port forwarding for research tools
    ports:
      - "8888:8888"  # Jupyter Lab
      - "8080:8080"  # Web interfaces
      - "3000:3000"  # Development servers
    
    # Environment variables
    environment:
      - DISPLAY=${DISPLAY:-:0}
      - WORKSPACE_ROOT=/home/researcher
    
    # Working directory
    working_dir: /home/researcher
    
    # Use researcher user
    user: researcher
    
    # Restart policy
    restart: unless-stopped

# Optional: Add additional services for research workflow
  # jupyter:
  #   image: axe:research-platform
  #   command: jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
  #   ports:
  #     - "8888:8888"
  #   volumes:
  #     - .:/home/researcher
  #   user: researcher

networks:
  default:
    name: axe-research-network
EOF

    log_success "Public Docker Compose created"
}

create_public_documentation() {
    log_section "CREATING PUBLIC DOCUMENTATION"
    
    cat > README-DEVELOPMENT.md << 'EOF'
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
EOF

    log_success "Public documentation created"
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

main() {
    log_section "AxE PUBLIC DEVELOPMENT ENVIRONMENT SETUP"
    log_info "Creating professional Docker environment for public distribution"
    
    create_public_dockerfile
    create_public_vscode_config
    create_public_docker_compose
    create_public_documentation
    
    log_section "🎉 PUBLIC ENVIRONMENT COMPLETE!"
    echo ""
    echo -e "${GREEN}✅ Public Dockerfile created (Dockerfile.public)${NC}"
    echo -e "${GREEN}✅ VSCode dev container configuration (.devcontainer-public/)${NC}"
    echo -e "${GREEN}✅ Docker Compose for public use (docker-compose.public.yml)${NC}"
    echo -e "${GREEN}✅ Comprehensive documentation (README-DEVELOPMENT.md)${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Public Release Ready:${NC}"
    echo -e "${CYAN}1. Build: ${WHITE}docker build -f Dockerfile.public -t axe:research-platform .${NC}"
    echo -e "${CYAN}2. Run: ${WHITE}docker-compose -f docker-compose.public.yml up -d${NC}"
    echo -e "${CYAN}3. Access: ${WHITE}docker exec -it axe-research-environment bash${NC}"
    echo -e "${CYAN}4. VSCode: Copy .devcontainer-public/ to .devcontainer/${NC}"
    echo ""
    echo -e "${PURPLE}📖 Professional documentation ready for public distribution${NC}"
    echo -e "${PURPLE}🔬 Optimized for research and academic use${NC}"
}

main "$@"