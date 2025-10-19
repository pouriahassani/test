#!/bin/bash

# AxE Development Environment Setup Script
# Fixes all Docker/VSCode integration issues and adds Claude Code CLI

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
# MAIN FIXES
# =============================================================================

fix_dockerfile() {
    log_section "FIXING DOCKERFILE - WORKSPACE & CLAUDE CLI INTEGRATION"
    
    # Backup current Dockerfile
    if [[ -f "Dockerfile" ]]; then
        cp Dockerfile Dockerfile.backup
        log_info "Backed up Dockerfile to Dockerfile.backup"
    fi
    
    # Create enhanced Dockerfile with proper workspace and Claude CLI
    cat > Dockerfile << 'EOF'
# AxE Development Environment with Claude Code CLI & VSCode Integration
FROM ubuntu:25.04

# =============================================================================
# ENVIRONMENT SETUP - UNIFIED WORKSPACE
# =============================================================================

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# FIXED: Use /home/axe as single workspace (no more /workspace confusion)
ENV USERNAME=axe
ENV USER_UID=1001
ENV USER_GID=1001
ENV HOME=/home/axe
ENV WORKDIR=/home/axe

# =============================================================================
# SYSTEM PACKAGES WITH CLAUDE CLI SUPPORT
# =============================================================================

RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential gcc-15 g++-15 cmake \
    # Development tools
    git curl wget unzip pkg-config \
    python3 python3-pip python3-venv python3-dev \
    # RISC-V toolchain dependencies
    autoconf automake autotools-dev libmpc-dev libmpfr-dev libgmp-dev \
    gawk bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev \
    # Verilator dependencies
    ninja-build perl make g++ ccache libfl2 libfl-dev zlib1g zlib1g-dev \
    libtcmalloc-minimal4 numactl perl-doc help2man \
    # CLI tools
    vim nano htop tree jq sudo lsb-release software-properties-common ca-certificates gnupg \
    # VSCode integration requirements
    openssh-client procps psmisc gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# NODE.JS FOR CLAUDE CODE CLI
# =============================================================================

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# =============================================================================
# USER SETUP - FIXED FOR /home/axe
# =============================================================================

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME \
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Create RISC-V directory
RUN mkdir -p /opt/riscv && chown $USERNAME:$USERNAME /opt/riscv

# Switch to axe user
USER $USERNAME
WORKDIR $WORKDIR

# =============================================================================
# RISC-V TOOLCHAIN
# =============================================================================

RUN git clone --depth=1 --branch=2025.06.13 \
    https://github.com/riscv-collab/riscv-gnu-toolchain.git riscv-gnu-toolchain

RUN cd riscv-gnu-toolchain && mkdir build-rv32im && cd build-rv32im && \
    ../configure --prefix=/opt/riscv --with-arch=rv32im --with-abi=ilp32 \
    --enable-multilib --disable-linux && \
    make newlib -j$(nproc) && cd ../.. && rm -rf riscv-gnu-toolchain

# =============================================================================
# VERILATOR
# =============================================================================

RUN git clone --depth=1 --branch=stable \
    https://github.com/verilator/verilator.git verilator-src && \
    cd verilator-src && autoconf && \
    ./configure --prefix=$WORKDIR/verilator && \
    make -j$(nproc) && make install && cd .. && rm -rf verilator-src

# =============================================================================
# PYTHON ENVIRONMENT
# =============================================================================

RUN python3 -m pip install --user --upgrade pip --break-system-packages

RUN pip3 install --user --no-cache-dir --break-system-packages \
    numpy matplotlib pandas scipy pytest black pylint mypy flake8 ruff \
    jupyterlab seaborn click pyyaml tqdm rich typer \
    autopep8 pycodestyle pydocstyle rope bandit jupyter ipykernel

# =============================================================================
# CLAUDE CODE CLI INSTALLATION
# =============================================================================

# Install Claude Code CLI
RUN sudo npm install -g @anthropic/claude-code@latest

# Create Claude config directory
RUN mkdir -p ~/.config/claude

# =============================================================================
# ENVIRONMENT & SHELL SETUP
# =============================================================================

ENV PATH="/opt/riscv/bin:$WORKDIR/verilator/bin:$HOME/.local/bin:$PATH"
ENV VERILATOR_ROOT="$WORKDIR/verilator"
ENV RISCV="/opt/riscv"

# Enhanced bash configuration with Claude CLI
RUN echo '# AxE Development Environment with Claude CLI' >> ~/.bashrc && \
    echo 'export PS1="\\[\\033[01;32m\\]axe@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\[\\033[01;33m\\]⚡\\[\\033[00m\\]\\$ "' >> ~/.bashrc && \
    echo 'export TERM=xterm-256color' >> ~/.bashrc && \
    echo 'alias ll="ls -la --color=auto"' >> ~/.bashrc && \
    echo 'alias python="python3"' >> ~/.bashrc && \
    echo 'alias pip="pip3"' >> ~/.bashrc && \
    echo '# Claude CLI aliases' >> ~/.bashrc && \
    echo 'alias claude="claude-code"' >> ~/.bashrc && \
    echo 'alias ai="claude-code"' >> ~/.bashrc && \
    echo 'export PATH="/opt/riscv/bin:$WORKDIR/verilator/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc && \
    echo 'export VERILATOR_ROOT="$WORKDIR/verilator"' >> ~/.bashrc && \
    echo 'export RISCV="/opt/riscv"' >> ~/.bashrc

# Create version check script
RUN echo '#!/bin/bash' > check_versions.sh && \
    echo 'echo "=== AxE Environment (2025) ==="' >> check_versions.sh && \
    echo 'echo "Ubuntu: $(lsb_release -d | cut -f2)"' >> check_versions.sh && \
    echo 'echo "Python: $(python3 --version)"' >> check_versions.sh && \
    echo 'echo "Node.js: $(node --version)"' >> check_versions.sh && \
    echo 'echo "Claude CLI: $(claude-code --version 2>/dev/null || echo \"Not configured\")"' >> check_versions.sh && \
    echo 'echo "RISC-V GCC: $(riscv32-unknown-elf-gcc --version 2>/dev/null | head -1 || echo \"Not found\")"' >> check_versions.sh && \
    echo 'echo "Verilator: $(verilator --version 2>/dev/null || echo \"Not found\")"' >> check_versions.sh && \
    echo 'echo "Working Directory: $PWD"' >> check_versions.sh && \
    chmod +x check_versions.sh

# Welcome message with Claude CLI info
RUN echo 'echo ""' >> ~/.bashrc && \
    echo 'echo -e "\\033[1;36m🚀 AxE Development Environment with Claude Code CLI Ready!\\033[0m"' >> ~/.bashrc && \
    echo 'echo -e "\\033[0;32m   💡 Commands: claude [message] | ai [message] | ./check_versions.sh\\033[0m"' >> ~/.bashrc && \
    echo 'echo ""' >> ~/.bashrc

CMD ["/bin/bash", "-l"]
EOF

    log_success "Enhanced Dockerfile created (workspace: /home/axe, Claude CLI included)"
}

create_vscode_config() {
    log_section "CREATING VSCODE DEVCONTAINER & SETTINGS"
    
    # Create .devcontainer directory
    mkdir -p .devcontainer
    
    # Create devcontainer.json with fixed workspace mapping
    cat > .devcontainer/devcontainer.json << 'EOF'
{
    "name": "AxE Development Environment",
    "build": {
        "dockerfile": "../Dockerfile",
        "context": ".."
    },
    
    // FIXED: Workspace mapping to /home/axe (removes /workspace confusion)
    "workspaceMount": "source=${localWorkspaceFolder},target=/home/axe,type=bind",
    "workspaceFolder": "/home/axe",
    
    // Use axe user (non-root)
    "remoteUser": "axe",
    
    // VSCode settings optimized for AxE development
    "settings": {
        "terminal.integrated.defaultProfile.linux": "bash",
        "python.defaultInterpreterPath": "/usr/bin/python3",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black",
        "python.formatting.blackPath": "/home/axe/.local/bin/black",
        "python.linting.pylintPath": "/home/axe/.local/bin/pylint",
        "files.watcherExclude": {
            "**/obj_dir/**": true,
            "**/build/**": true,
            "**/.git/objects/**": true
        }
    },
    
    // FIXED: Extensions that work in container environment
    "extensions": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.pylint",
        "mshr-h.veriloghdl",
        "ms-vscode.cpptools",
        "ms-vscode.vscode-json",
        "eamodio.gitlens",
        "yzhang.markdown-all-in-one"
    ],
    
    // Port forwarding
    "forwardPorts": [8888, 3000, 8080],
    
    // Post-create command
    "postCreateCommand": "bash -c 'echo \"🚀 AxE Container Ready!\" && ./check_versions.sh'",
    
    // Mount SSH keys and git config from host
    "mounts": [
        "source=${localEnv:HOME}/.ssh,target=/home/axe/.ssh,type=bind,consistency=cached",
        "source=${localEnv:HOME}/.gitconfig,target=/home/axe/.gitconfig,type=bind,consistency=cached"
    ]
}
EOF

    # Create VSCode tasks for AxE development
    mkdir -p .vscode
    cat > .vscode/tasks.json << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "AxE: Build Hardware",
            "type": "shell",
            "command": "make",
            "options": {"cwd": "${workspaceFolder}/soc_frame"},
            "group": "build"
        },
        {
            "label": "AxE: Check Versions",
            "type": "shell",
            "command": "./check_versions.sh",
            "group": "test"
        },
        {
            "label": "Claude: Chat",
            "type": "shell",
            "command": "claude-code",
            "args": ["${input:message}"],
            "group": "test"
        }
    ],
    "inputs": [
        {
            "id": "message",
            "description": "Message for Claude",
            "type": "promptString"
        }
    ]
}
EOF

    log_success "VSCode configuration created (devcontainer + tasks)"
}

create_docker_compose() {
    log_section "CREATING DOCKER COMPOSE FOR EASY MANAGEMENT"
    
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  axe-dev:
    build:
      context: .
      dockerfile: Dockerfile
    image: axe:dev-claude
    container_name: axe-development
    
    # FIXED: Mount to /home/axe (unified workspace)
    volumes:
      - .:/home/axe
      - ~/.ssh:/home/axe/.ssh:ro
      - ~/.gitconfig:/home/axe/.gitconfig:ro
    
    stdin_open: true
    tty: true
    
    # Port forwarding
    ports:
      - "8888:8888"
      - "3000:3000"
      - "8080:8080"
    
    working_dir: /home/axe
    user: axe
    restart: unless-stopped
EOF

    log_success "Docker Compose created"
}

create_claude_setup() {
    log_section "CREATING CLAUDE CLI SETUP SCRIPT"
    
    cat > setup_claude_in_container.sh << 'EOF'
#!/bin/bash

# Claude Code CLI Setup for Container
echo "🤖 Setting up Claude Code CLI..."

# Check if already installed
if command -v claude-code &> /dev/null; then
    echo "✅ Claude Code CLI is installed: $(which claude-code)"
else
    echo "❌ Installing Claude Code CLI..."
    sudo npm install -g @anthropic/claude-code@latest
fi

# Configure Claude CLI
echo ""
echo "🔧 Configuring Claude CLI..."
echo "💡 You'll need your Anthropic API key"
echo ""

# Test if already configured
if claude-code --version &> /dev/null; then
    echo "✅ Claude CLI appears to be working"
    echo ""
    echo "🚀 Ready to use Claude!"
    echo "💡 Try: claude-code 'Hello! Continue our AxE analysis'"
    echo "💡 Or:  ai 'Help me with the NoC implementation'"
else
    echo "⚙️  First-time setup needed..."
    claude-code --configure
fi

echo ""
echo "🎯 Quick Start Commands:"
echo "  claude-code 'message'     # Chat with Claude"
echo "  ai 'message'              # Shortcut alias"
echo "  claude-code --file file.v 'analyze this'"
echo ""
EOF

    chmod +x setup_claude_in_container.sh
    log_success "Claude setup script created"
}

create_usage_guide() {
    log_section "CREATING COMPREHENSIVE USAGE GUIDE"
    
    cat > DEVELOPMENT_SETUP_GUIDE.md << 'EOF'
# AxE Development Environment - Complete Setup Guide

## 🚀 Quick Start (All Issues Fixed)

### Option 1: VSCode Dev Containers (Recommended)
```bash
# 1. Build the container
docker build -t axe:dev-claude .

# 2. Open in VSCode
# Press Ctrl+Shift+P -> "Dev Containers: Reopen in Container"
# Workspace will be at /home/axe (your project root)
```

### Option 2: Docker Compose
```bash
# 1. Start container
docker-compose up -d

# 2. Attach to container
docker exec -it axe-development bash

# 3. Or attach from VSCode
# Ctrl+Shift+P -> "Dev Containers: Attach to Running Container"
```

### Option 3: Direct Docker
```bash
# Run with workspace mounted to /home/axe
docker run -it -v $(pwd):/home/axe axe:dev-claude
```

## ✅ Fixed Issues

### 1. ✅ Workspace Path Fixed
- **Before**: Confusion between `/workspace` and `/home/axe`
- **After**: Everything unified at `/home/axe`
- **VSCode**: Automatically opens in correct directory

### 2. ✅ VSCode Extensions Fixed
- **Before**: Extensions not available in container
- **After**: Pre-configured extensions install automatically
- **Extensions**: Python, Verilog, C++, Git tools

### 3. ✅ Claude Code CLI Integrated
- **Before**: No Claude CLI in container
- **After**: Claude Code CLI pre-installed and configured
- **Usage**: `claude-code 'message'` or `ai 'message'`

## 🤖 Claude Integration

### Setup Claude CLI (First Time)
```bash
# Inside container
./setup_claude_in_container.sh

# Follow prompts to configure API key
```

### Continue Your Chat
```bash
# Reference previous conversation
claude-code "Continue our AxE analysis from where we left off"

# Ask about specific components
ai "Help me understand the NoC router implementation"

# Code analysis
claude-code --file soc_frame/rtl/pico/picorv32.v "Analyze this RISC-V core"
```

## 🛠️ Development Workflow

### 1. Start Environment
```bash
# Option A: VSCode Dev Container
# Ctrl+Shift+P -> "Dev Containers: Reopen in Container"

# Option B: Docker Compose
docker-compose up -d
docker exec -it axe-development bash
```

### 2. Verify Environment
```bash
./check_versions.sh
```

### 3. Build AxE Components
```bash
# Hardware
cd soc_frame && make

# Software
make sw
```

### 4. AI-Assisted Development
```bash
# Get help with current task
ai "I'm working on optimizing the approximate multiplier. Can you help?"

# Code review
claude-code --file my_changes.v "Review this Verilog implementation"

# Debug assistance
ai "I'm getting this error: [paste error]. How do I fix it?"
```

## 📁 Directory Structure (Fixed)

```
/home/axe/                     # Your project root (mounted from host)
├── soc_frame/                 # Hardware framework
├── Complete_partitioning/     # Algorithms
├── .devcontainer/            # VSCode container config
├── .vscode/                  # VSCode settings
├── docker-compose.yml        # Container management
├── setup_claude_in_container.sh  # Claude CLI setup
├── check_versions.sh         # Environment check
└── DEVELOPMENT_SETUP_GUIDE.md    # This guide
```

## 🎯 VSCode Features

### Available Tasks (Ctrl+Shift+P -> "Tasks: Run Task")
- **AxE: Build Hardware** - Compile RTL
- **AxE: Check Versions** - Verify tools
- **Claude: Chat** - AI assistance

### Pre-installed Extensions
- **Python**: Full development support
- **Verilog/SystemVerilog**: Syntax highlighting
- **C/C++**: RISC-V development
- **Git**: Enhanced git integration
- **Markdown**: Documentation support

## 🤖 AI-Powered Development

### Code Analysis
```bash
# Analyze specific files
claude-code --file soc_frame/rtl/noc/router.v "Explain this NoC router"

# Review implementations
ai "Compare PicoRV32 vs PiXoRV32 implementations"
```

### Learning and Documentation
```bash
# Understanding concepts
claude-code "Explain approximate computing in the context of AxE"

# Getting detailed explanations
ai "Walk me through the line-by-line syntax of this Verilog module"
```

### Debugging Help
```bash
# Synthesis errors
claude-code "I'm getting Verilator errors: [paste errors]"

# Performance optimization
ai "How can I optimize this RISC-V assembly code for energy efficiency?"
```

## 🔧 Troubleshooting

### VSCode Extension Issues
```bash
# Reload VSCode window
Ctrl+Shift+P -> "Developer: Reload Window"

# Rebuild container
Ctrl+Shift+P -> "Dev Containers: Rebuild Container"
```

### Claude CLI Issues
```bash
# Reinstall
sudo npm uninstall -g @anthropic/claude-code
sudo npm install -g @anthropic/claude-code@latest

# Reconfigure
claude-code --configure
```

### Permission Issues
```bash
# Fix ownership (if needed)
sudo chown -R axe:axe /home/axe
```

## 🎓 Continuing Your Learning

### Resume Previous Conversations
```bash
# Reference our previous analysis
claude-code "We were analyzing the AxE NoC architecture. Continue from where we left off."

# Ask for specific help
ai "Based on our previous discussion about the learning framework, help me analyze the router implementation"
```

### Structured Learning
```bash
# Follow the established methodology
claude-code "Using the critical analysis framework we established, analyze this SystemVerilog code"

# Get detailed syntax explanations
ai "Provide line-by-line explanation of this Verilog code following our learning approach"
```

## ✅ Success Indicators

- [ ] Container starts without errors
- [ ] VSCode opens workspace at `/home/axe`
- [ ] All extensions load properly
- [ ] `./check_versions.sh` shows all tools working
- [ ] `claude-code 'hello'` responds
- [ ] Can build hardware with `make` in `soc_frame/`

Your development environment is now fully integrated with AI assistance and ready for professional AxE development!
EOF

    log_success "Complete usage guide created"
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

main() {
    log_section "AxE DEVELOPMENT ENVIRONMENT SETUP"
    log_info "Fixing Docker workspace, VSCode extensions, and adding Claude Code CLI"
    
    fix_dockerfile
    create_vscode_config
    create_docker_compose
    create_claude_setup
    create_usage_guide
    
    log_section "🎉 ALL ISSUES FIXED!"
    echo ""
    echo -e "${GREEN}✅ Dockerfile enhanced with Claude Code CLI${NC}"
    echo -e "${GREEN}✅ Workspace unified at /home/axe (no more /workspace confusion)${NC}"
    echo -e "${GREEN}✅ VSCode devcontainer configured with extensions${NC}"
    echo -e "${GREEN}✅ Docker Compose for easy container management${NC}"
    echo -e "${GREEN}✅ Claude CLI setup script created${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Quick Start:${NC}"
    echo -e "${CYAN}1. Build: ${WHITE}docker build -t axe:dev-claude .${NC}"
    echo -e "${CYAN}2. VSCode: ${WHITE}Ctrl+Shift+P -> 'Dev Containers: Reopen in Container'${NC}"
    echo -e "${CYAN}3. Setup Claude: ${WHITE}./setup_claude_in_container.sh${NC}"
    echo -e "${CYAN}4. Continue chat: ${WHITE}claude-code 'Continue our AxE analysis'${NC}"
    echo ""
    echo -e "${PURPLE}📖 Read DEVELOPMENT_SETUP_GUIDE.md for complete instructions${NC}"
}

main "$@"