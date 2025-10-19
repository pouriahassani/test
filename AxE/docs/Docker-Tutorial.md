# Docker Fundamentals & AxE Dockerfile Deep Dive

## 📖 Table of Contents
1. [What is Docker?](#what-is-docker)
2. [Basic Docker Concepts](#basic-docker-concepts)
3. [Dockerfile Syntax Tutorial](#dockerfile-syntax-tutorial)
4. [AxE Dockerfile Line-by-Line Analysis](#axe-dockerfile-line-by-line-analysis)
5. [Advanced Docker Concepts Used](#advanced-docker-concepts-used)
6. [Best Practices Explained](#best-practices-explained)
7. [Learning Resources](#learning-resources)

---

## What is Docker?

**Docker** is a **containerization platform** that packages applications and their dependencies into lightweight, portable containers.

### 🤔 Think of it like this:
- **Virtual Machine**: Like renting an entire apartment (OS + apps)
- **Docker Container**: Like renting just a room with shared utilities (shared OS kernel)

### 🎯 Why Docker for AxE?
1. **Consistency**: Same environment on any machine
2. **Isolation**: No conflicts with host system
3. **Portability**: Works on Linux, macOS, Windows
4. **Reproducibility**: Exact same tools and versions every time

---

## Basic Docker Concepts

### 🏗️ Core Components

#### **Docker Image**
```bash
# Think of it as a "template" or "blueprint"
# Like a .iso file for installing an OS
docker images  # List all images on your system
```

#### **Docker Container**  
```bash
# Think of it as a "running instance" of an image
# Like a VM that's currently running
docker ps  # List running containers
```

#### **Dockerfile**
```bash
# Think of it as "installation instructions"
# Step-by-step recipe to create an image
```

### 🔄 Docker Workflow
```
Dockerfile → (docker build) → Image → (docker run) → Container
    ↑                            ↑                      ↑
  Recipe                    Template                Running App
```

---

## Dockerfile Syntax Tutorial

### 📝 Basic Instructions

#### **FROM** - Choose Base Image
```dockerfile
FROM ubuntu:25.04
#    ↑      ↑
#  image   tag(version)
```
**What it does**: Tells Docker "start with Ubuntu 25.04 as foundation"
**Like**: "Start with a fresh Ubuntu installation"

#### **RUN** - Execute Commands
```dockerfile
RUN apt-get update
#   ↑
# Any shell command
```
**What it does**: Executes shell commands during image build
**Like**: Typing commands in terminal during setup

#### **ENV** - Set Environment Variables
```dockerfile
ENV USERNAME=axe
#   ↑        ↑
# variable  value
```
**What it does**: Creates environment variables available in container
**Like**: Setting variables in ~/.bashrc

#### **WORKDIR** - Change Directory
```dockerfile
WORKDIR /workspace
#       ↑
#   directory path
```
**What it does**: Changes current directory (like `cd` command)
**Like**: `cd /workspace`

#### **USER** - Switch User
```dockerfile
USER axe
#    ↑
# username
```
**What it does**: Switch to different user account
**Like**: `su - axe`

#### **COPY/ADD** - Copy Files
```dockerfile
COPY source destination
#    ↑      ↑
#  from     to
```
**What it does**: Copies files from host to container
**Like**: `cp source destination`

---

## AxE Dockerfile Line-by-Line Analysis

Let's analyze our comprehensive AxE Dockerfile with full explanations:

### 🎯 Section 1: Base Image Selection

```dockerfile
# AxE Modern Development Environment
# Using Ubuntu 25.04 "Plucky Puffin" - Latest stable release (April 2025)
FROM ubuntu:25.04
```

**Line-by-Line Breakdown:**

**Line 1-2: Comments**
- `#` creates comments (ignored during build)
- **Purpose**: Documentation for humans reading the file
- **Teaching Point**: Always document WHY you chose something

**Line 3: FROM instruction**
- `FROM ubuntu:25.04`
  - **FROM**: Docker instruction to specify base image
  - **ubuntu**: Image name from Docker Hub registry
  - **25.04**: Tag specifying Ubuntu version (April 2025 release)
  - **Effect**: Downloads Ubuntu 25.04 and uses it as foundation

**🤔 Why Ubuntu 25.04?**
- Latest LTS with modern toolchain
- Better package versions than older Ubuntu
- Security updates and performance improvements

### 🎯 Section 2: Environment Configuration

```dockerfile
# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
```

**Line-by-Line Breakdown:**

**Lines 1-3: Section Header**
- Visual separator using `=` characters
- Makes Dockerfile easier to read and navigate
- **Teaching Point**: Organization improves maintainability

**Line 5-6: Environment Variables**
- `ENV DEBIAN_FRONTEND=noninteractive`
  - **ENV**: Docker instruction to set environment variable
  - **DEBIAN_FRONTEND**: Controls how Debian/Ubuntu packages interact
  - **noninteractive**: Prevents packages from asking questions during install
  - **Why needed**: Automated builds can't answer interactive prompts

- `ENV TZ=UTC`
  - **TZ**: System timezone variable
  - **UTC**: Coordinated Universal Time
  - **Why UTC**: Consistent timestamps regardless of host location

### 🎯 Section 3: User Configuration

```dockerfile
# User configuration - creates consistent development environment
ENV USERNAME=axe
ENV USER_UID=1001
ENV USER_GID=1001
ENV WORKDIR=/workspace
ENV SOC_FRAME_PATH=${WORKDIR}/soc_frame
```

**Line-by-Line Breakdown:**

**ENV USERNAME=axe**
- Creates variable containing username
- **Why variable**: Used multiple times in file, easier to change

**ENV USER_UID=1001**
- **UID**: User ID number in Linux
- **1001**: Chosen to avoid conflicts with existing users
- **Why not 1000**: Ubuntu 25.04 has default user with UID 1000

**ENV USER_GID=1001**
- **GID**: Group ID number in Linux
- **Same as UID**: Common practice for primary user group

**ENV WORKDIR=/workspace**
- Sets main working directory path
- **Why /workspace**: Clear, descriptive name for development area

**ENV SOC_FRAME_PATH=${WORKDIR}/soc_frame**
- **${WORKDIR}**: Variable substitution (expands to /workspace)
- **Result**: /workspace/soc_frame
- **Purpose**: AxE-specific path for hardware framework

### 🎯 Section 4: Package Installation

```dockerfile
# Update package list and install all required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc-15 \
    g++-15 \
    cmake \
    git \
    curl \
    wget \
    unzip \
    pkg-config \
    # ... more packages
    && rm -rf /var/lib/apt/lists/*
```

**Line-by-Line Breakdown:**

**RUN apt-get update && apt-get install -y \\**
- **RUN**: Execute shell commands during build
- **apt-get update**: Downloads latest package lists
- **&&**: Logical AND - only run second command if first succeeds
- **apt-get install -y**: Install packages without prompting
- **-y**: Automatically answer "yes" to prompts
- **\\**: Line continuation character (command continues on next line)

**Package Categories Explained:**

**build-essential**
- **What**: Meta-package including GCC, make, libc-dev
- **Why**: Essential tools for compiling C/C++ programs
- **Like**: Installing "Developer Tools" on macOS

**gcc-15 / g++-15**
- **What**: GNU Compiler Collection version 15
- **gcc**: C compiler
- **g++**: C++ compiler  
- **Why version 15**: Latest stable with modern C++ features

**cmake**
- **What**: Cross-platform build system generator
- **Why**: Many projects use CMake instead of plain Makefiles
- **Like**: Visual Studio project files but cross-platform

**git**
- **What**: Version control system
- **Why**: Download source code from repositories

**curl / wget**
- **What**: Command-line download tools
- **curl**: More features, API-friendly
- **wget**: Simpler, good for file downloads

**&& rm -rf /var/lib/apt/lists/***
- **Purpose**: Clean up package cache files
- **Why**: Reduces final image size
- **/var/lib/apt/lists/**: Where apt stores package information
- **Teaching Point**: Always clean up in same RUN command

### 🎯 Section 5: GCC Configuration

```dockerfile
# Set GCC 15 as default (optional - for cutting edge features)
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-14 14 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-15 15 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-14 14 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-15 15
```

**Line-by-Line Breakdown:**

**update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-14 14**
- **update-alternatives**: Ubuntu system for managing multiple versions
- **--install**: Register a new alternative
- **Parameters breakdown**:
  - `/usr/bin/gcc`: Link location (what users type)
  - `gcc`: Alternative name (internal reference)
  - `/usr/bin/gcc-14`: Actual executable path
  - `14`: Priority number (higher = preferred)

**Why This Matters:**
- Ubuntu installs both GCC 14 and GCC 15
- By default, `gcc` might point to older version
- This ensures `gcc` command uses GCC 15
- **Like**: Setting default browser in Windows

### 🎯 Section 6: User Creation (Security)

```dockerfile
# Create non-root user with passwordless sudo for development convenience
RUN if ! getent group $USER_GID; then groupadd --gid $USER_GID $USERNAME; fi \
    && if ! getent passwd $USER_UID; then useradd --uid $USER_UID --gid $USER_GID -m $USERNAME; fi \
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
```

**Line-by-Line Breakdown:**

**if ! getent group $USER_GID; then groupadd --gid $USER_GID $USERNAME; fi**
- **getent group $USER_GID**: Check if group with GID 1001 exists
- **!**: NOT operator (if group does NOT exist)
- **groupadd --gid $USER_GID $USERNAME**: Create group "axe" with GID 1001
- **Why conditional**: Avoid error if group already exists

**if ! getent passwd $USER_UID; then useradd ...; fi**
- **getent passwd $USER_UID**: Check if user with UID 1001 exists
- **useradd parameters**:
  - `--uid $USER_UID`: Set user ID to 1001
  - `--gid $USER_GID`: Set primary group ID to 1001
  - `-m`: Create home directory
  - `$USERNAME`: Username "axe"

**usermod -aG sudo $USERNAME**
- **usermod**: Modify user account
- **-aG**: Add to group (append, don't replace)
- **sudo**: Group that can use sudo command
- **Effect**: User "axe" can use sudo

**echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers**
- **echo**: Print text
- **$USERNAME ALL=(ALL) NOPASSWD:ALL**: Sudoers rule meaning:
  - `$USERNAME`: User "axe"
  - `ALL`: On all hosts
  - `(ALL)`: Can run as any user
  - `NOPASSWD:ALL`: Without password for any command
- **>>**: Append to file (don't overwrite)
- **/etc/sudoers**: File controlling sudo permissions

**🚨 Security Note**: NOPASSWD is convenient for development but NOT for production!

### 🎯 Section 7: Directory Setup

```dockerfile
# Create and set ownership of workspace directory
RUN mkdir -p $WORKDIR && chown $USERNAME:$USERNAME $WORKDIR

# Switch to non-root user for all subsequent operations
USER $USERNAME

# Set working directory for all following commands
WORKDIR $WORKDIR
```

**Line-by-Line Breakdown:**

**mkdir -p $WORKDIR**
- **mkdir**: Create directory
- **-p**: Create parent directories if needed (no error if exists)
- **$WORKDIR**: Expands to /workspace

**chown $USERNAME:$USERNAME $WORKDIR**
- **chown**: Change ownership
- **$USERNAME:$USERNAME**: User:Group format (axe:axe)
- **Effect**: User "axe" owns /workspace directory

**USER $USERNAME**
- **USER**: Docker instruction to switch user
- **Effect**: All subsequent commands run as "axe" user
- **Security**: Don't run as root unless necessary

**WORKDIR $WORKDIR**
- **WORKDIR**: Docker instruction to change directory
- **Effect**: Like running `cd /workspace`
- **All future commands**: Execute in /workspace

### 🎯 Section 8: RISC-V Toolchain (AxE-Optimized Build)

```dockerfile
# Clone latest stable RISC-V GNU Toolchain (2025.06.13 - latest nightly)
RUN git clone --depth=1 --branch=2025.06.13 \
    https://github.com/riscv-collab/riscv-gnu-toolchain.git riscv-gnu-toolchain
```

**Line-by-Line Breakdown:**

**git clone --depth=1 --branch=2025.06.13 \\**
- **git clone**: Downloads a Git repository from remote server
- **--depth=1**: Shallow clone - downloads only the latest commit, not full history
  - **Benefit**: Saves ~90% download time and disk space
  - **Trade-off**: Can't access commit history, but we don't need it for building
- **--branch=2025.06.13**: Specific version tag/branch to checkout
  - **Why specific version**: Ensures reproducible builds across all environments
  - **Version choice**: Latest stable release with known working configuration
- **\\**: Line continuation character in Dockerfile (command continues on next line)

**Repository URL**: https://github.com/riscv-collab/riscv-gnu-toolchain.git
- **riscv-collab**: Official RISC-V International collaboration organization
- **Contains**: Complete toolchain including:
  - **GCC**: GNU Compiler Collection for RISC-V
  - **binutils**: Binary utilities (assembler, linker, objdump, etc.)
  - **newlib**: Embedded C library for bare-metal development
  - **gdb**: GNU Debugger with RISC-V support
- **Purpose**: Enables cross-compilation from x86/ARM hosts to RISC-V targets

```dockerfile
# Build RV32IM toolchain (32-bit RISC-V with integer + multiplication)  
# Only IM needed for AxE project (approximate multiplication focus)
# Skip explicit submodule init - modern toolchain fetches on-demand (avoids dejagnu issues)
RUN cd riscv-gnu-toolchain && \
    mkdir build-rv32im && cd build-rv32im && \
    ../configure \
        --prefix=/opt/riscv \
        --with-arch=rv32im \
        --with-abi=ilp32 \
        --enable-multilib \
        --disable-linux && \
    make newlib -j$(nproc)
```

**AxE-Specific Build Decisions:**

**Why Only RV32IM (Not RV32I):**
- **AxE Focus**: Research on approximate **multiplication** algorithms
- **Hardware**: PicoRV32 vs PiXoRV32 (approximate **multipliers**)
- **M Extension**: Provides hardware multiplication/division instructions
- **Efficiency**: Only build what's actually needed

**Modern On-Demand Submodule Fetching (No Manual `git submodule` Commands)**
- **Traditional approach**: `git submodule update --init --recursive` downloads everything
  - **Problem**: Tries to clone ALL submodules including dejagnu (testing framework)
  - **Issue**: dejagnu hosted on unreliable git.savannah.gnu.org server
  - **Result**: Build fails with connection timeouts
- **Modern approach**: Let build system fetch only what it needs
  - **How it works**: `make newlib` automatically clones required submodules (gcc, binutils, newlib)
  - **Smart fetching**: Build system knows dependencies and fetches them on-demand
  - **Avoids problems**: Skips unnecessary submodules like dejagnu completely
- **Benefits for AxE**:
  - **Faster builds**: Downloads only essential components (~60% less data)
  - **More reliable**: No dependency on problematic servers
  - **Focused**: Perfect for embedded/bare-metal development (our use case)

**../configure (Build Configuration Parameters Explained Line-by-Line):**

**--prefix=/opt/riscv**
- **What it does**: Sets installation directory for all toolchain components
- **Why /opt/**: Standard Linux location for optional software packages
- **Why /riscv**: Clear identification of RISC-V specific tools
- **Official standard**: Matches RISC-V GNU toolchain documentation examples
- **Result**: All tools installed to `/opt/riscv/bin/`, libraries to `/opt/riscv/riscv32-unknown-elf/lib/`

**--with-arch=rv32im**
- **rv32**: 32-bit RISC-V architecture (vs rv64 for 64-bit)
- **i**: Base integer instruction set (mandatory)
- **m**: Multiplication and division extension
- **Why IM for AxE**: Project focuses on approximate **multiplication** algorithms
- **Multilib impact**: This becomes the default architecture, but multilib enables others too

**--with-abi=ilp32**
- **i**: int = 32 bits
- **l**: long = 32 bits  
- **p**: pointer = 32 bits
- **Why ilp32**: Matches our 32-bit architecture choice
- **Alternative**: ilp32f (with floating-point), but AxE is integer-focused

**--enable-multilib**
- **What it enables**: Single toolchain supporting multiple architectures
- **How it works**: Builds separate library sets for rv32i, rv32im, rv32imc, etc.
- **AxE benefit**: One installation supports both exact cores (RV32I) and approximate cores (RV32IM)
- **Directory structure**: Creates `/opt/riscv/riscv32-unknown-elf/lib/rv32i/` and `/opt/riscv/riscv32-unknown-elf/lib/rv32im/`

**--disable-linux**
- **What it disables**: Linux-specific components (glibc, Linux headers, userspace tools)
- **What we keep**: Bare-metal components (newlib, standalone runtime)
- **Why disable**: AxE is embedded/SoC system, no Linux operating system
- **Result**: Smaller build, faster compilation, focused on our use case

**GDB Enabled (No --disable-gdb flag)**
- **What's included**: Full GNU Debugger with RISC-V support
- **Why essential**: Debug both exact and approximate computation algorithms
- **Capabilities**: Hardware breakpoints, register inspection, memory analysis
- **AxE usage**: Compare execution between PicoRV32 and PiXoRV32 cores

**Why /opt/riscv/ (Following Official Recommendation):**
- **Official Standard**: RISC-V GNU toolchain repo recommends `/opt/riscv`
- **Consistency**: Matches examples in official documentation
- **Community Practice**: Standard path used by RISC-V community
- **Tool Compatibility**: Scripts and tutorials expect tools in `/opt/riscv`

**make newlib -j$(nproc)**
- **make newlib**: Build only the newlib C library and essential tools (not full Linux toolchain)
- **newlib target**: Embedded C library perfect for bare-metal RISC-V development
- **-j$(nproc)**: Use all CPU cores for parallel compilation
- **$(nproc)**: Shell command returning number of CPU cores
- **Why newlib only**: AxE is embedded/bare-metal focused, doesn't need Linux userspace tools
- **Faster build**: Skips glibc, Linux headers, and other unnecessary components

### 📚 Understanding Multilib in RISC-V Toolchain

**Multilib** = **Multiple Libraries** - A crucial feature that allows a single toolchain installation to build code for **multiple target architectures**.

#### 🔧 **What Multilib Does**

**Without Multilib (Traditional Approach):**
```bash
# You'd need separate toolchain installations:
/opt/riscv32i/     # For RV32I (base integer only)
/opt/riscv32im/    # For RV32IM (integer + multiplication)
/opt/riscv32imc/   # For RV32IMC (+ compressed instructions)
/opt/riscv32imf/   # For RV32IMF (+ single-precision float)
```

**With Multilib (Our Unified Approach):**
```bash
# Single installation supports all architectures:
/opt/riscv/        # One toolchain, multiple targets!
```

#### 🎯 **RISC-V Architecture Extensions**

RISC-V uses a modular architecture system where each letter adds functionality:

- **RV32I**: Base 32-bit integer instruction set
- **RV32IM**: Base + **M**ultiplication/division extension  
- **RV32IMC**: + **C**ompressed instructions (16-bit for code density)
- **RV32IMF**: + **F**loating-point (single precision)
- **RV32IMFD**: + **D**ouble-precision floating-point

#### 🛠️ **How to Use Multilib**

With our unified toolchain, compile for different architectures using the `-march` flag:

```bash
# Compile for RV32I (base integer only - exact cores)
riscv32-unknown-elf-gcc -march=rv32i -mabi=ilp32 program.c

# Compile for RV32IM (with multiplication - approximate cores)  
riscv32-unknown-elf-gcc -march=rv32im -mabi=ilp32 program.c

# Compile for RV32IMC (with compression)
riscv32-unknown-elf-gcc -march=rv32imc -mabi=ilp32 program.c
```

#### 🔬 **Why Multilib Matters for AxE**

**AxE's Heterogeneous Architecture:**
- **PicoRV32**: Exact cores (RV32I - no hardware multiplication)
- **PiXoRV32**: Approximate cores (RV32IM - with approximate multiplication)

**With Multilib Support:**
```bash
# AxE Makefile targets use different architectures:
make rv32i     # Compiles with -march=rv32i for exact cores
make rv32im    # Compiles with -march=rv32im for approximate cores
```

#### 📚 **Technical Implementation**

**Library Directory Structure:**
```bash
/opt/riscv/riscv32-unknown-elf/lib/
├── rv32i/          # Libraries optimized for RV32I
├── rv32im/         # Libraries optimized for RV32IM  
├── rv32imc/        # Libraries optimized for RV32IMC
└── rv32imf/        # Libraries optimized for RV32IMF
```

**Automatic Library Selection:**
The compiler **automatically** selects the correct library variant based on your `-march` flag, ensuring optimal code generation for each target architecture.

#### 🚀 **Benefits for AxE Development**

1. **Single Installation**: One toolchain for all AxE core types
2. **Correct Optimization**: Each library variant optimized for its target architecture
3. **Easy Architecture Switching**: Just change the `-march` flag
4. **Space Efficient**: Shared components, separate only what differs
5. **Future-Proof**: Easy to add support for new RISC-V extensions

#### 💡 **Example in AxE Makefiles**

```makefile
# From AxE software Makefiles:
SMALL = rv32i      # Architecture for exact cores (PicoRV32)
BIG = rv32im       # Architecture for approximate cores (PiXoRV32)

rv32i: ARCH=$(SMALL)   # Uses rv32i libraries (no multiplication)
rv32im: ARCH=$(BIG)    # Uses rv32im libraries (with multiplication)

$(ARCH)_main.elf:
    $(CC) -march=$(ARCH) $(CFLAGS) -o ./$(ARCH)_main.elf $(SRC)
```

This multilib approach is what enables our single `/opt/riscv` toolchain to properly support both AxE's exact and approximate computing cores with optimal code generation for each! 🎯

**💡 For Complete Multilib Details:** See our comprehensive [RISC-V Toolchain Guide](RISCV-Toolchain.md#multilib-support) which covers:
- Technical implementation details
- Directory structure and library organization  
- Advanced compilation examples
- Troubleshooting multilib issues

### 🎯 Section 9: Python Environment

```dockerfile
# Install Python packages for AxE development and analysis
RUN pip3 install --user --no-cache-dir \
    numpy>=1.26.0 \
    matplotlib>=3.8.0 \
    pandas>=2.2.0 \
    # ... more packages
```

**Line-by-Line Breakdown:**

**pip3 install parameters:**
- **--user**: Install in user directory (~/.local) not system-wide
- **--no-cache-dir**: Don't save downloaded packages (saves space)
- **--break-system-packages**: Override PEP 668 externally managed environment protection
  - **PEP 668**: Python enhancement preventing pip conflicts with OS package manager
  - **Why needed**: Ubuntu 25.04 implements strict package management
  - **Docker safety**: Safe in containers since they're isolated from host system
- **Why --user**: Don't need root permissions, cleaner installation

**Package Version Specifications:**
- **numpy>=1.26.0**: Minimum version 1.26.0
- **Why minimum versions**: Ensure compatibility with modern features
- **>=**: "Greater than or equal" version constraint

**Scientific Computing Stack:**
- **numpy**: Numerical computing (arrays, math)
- **matplotlib**: Plotting and visualization  
- **pandas**: Data analysis (spreadsheet-like operations)
- **scipy**: Scientific computing (statistics, optimization)

---

## Advanced Docker Concepts Used

### 🔗 Multi-Stage Builds (Not used here, but good to know)
```dockerfile
# Example of multi-stage build
FROM ubuntu:25.04 AS builder
RUN # ... build steps

FROM ubuntu:25.04 AS runtime  
COPY --from=builder /app/binary /usr/local/bin/
```

### 📦 Layer Optimization
- Each RUN/COPY/ADD creates a new layer
- Combining commands with && reduces layers
- Smaller images = faster downloads

### 🧹 Cache Busting
```dockerfile
# This will always rebuild from here if file changes
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /app/  # Put this AFTER pip install
```

---

## Best Practices Explained

### ✅ DO's

**1. Use specific tags**
```dockerfile
FROM ubuntu:25.04  # ✅ Good
FROM ubuntu:latest # ❌ Bad (unpredictable)
```

**2. Minimize layers**
```dockerfile
# ✅ Good - single layer
RUN apt-get update && apt-get install -y package && rm -rf /var/lib/apt/lists/*

# ❌ Bad - three layers  
RUN apt-get update
RUN apt-get install -y package
RUN rm -rf /var/lib/apt/lists/*
```

**3. Use non-root user**
```dockerfile
USER $USERNAME  # ✅ Security best practice
```

**4. Clean up in same layer**
```dockerfile
RUN command && cleanup  # ✅ Smaller image
```

### ❌ DON'Ts

**1. Don't use ADD for local files**
```dockerfile
COPY file.txt /app/    # ✅ Use COPY
ADD file.txt /app/     # ❌ ADD has side effects
```

**2. Don't install unnecessary packages**
```dockerfile
RUN apt-get install -y --no-install-recommends package  # ✅ Minimal
```

**3. Don't hardcode values**
```dockerfile
ENV USERNAME=axe       # ✅ Use variables
RUN useradd axe        # ❌ Hardcoded
```

---

## 🎓 Learning Exercises

### Exercise 1: Modify User
Try changing the username from "axe" to your name. What variables need to change?

### Exercise 2: Add Package
Add `htop` package to the installation list. Where should it go?

### Exercise 3: Environment Variable
Create an environment variable for the Python version. Use it in pip commands.

### Exercise 4: Customize Terminal Colors
Modify the PS1 prompt to use your preferred colors. Check ANSI color codes online!

---

## 🌈 Colorful Development Experience

### **Enhanced Terminal Features**

Our Docker environment includes a **colorful, developer-friendly terminal**:

#### **🎨 Custom AxE-Branded Prompt**
```bash
axe@hostname:/workspace⚡$ 
```
- **Green username**: Easy identification  
- **Blue path**: Clear directory context
- **Yellow lightning bolt**: AxE energy theme ⚡
- **Consistent formatting**: Professional appearance

#### **🌈 Colorful Command Output**
- **File listings**: `ls`, `ll`, `la` with colored file types
- **Search results**: `grep` with highlighted matches
- **Git commands**: `gst`, `glog`, `gdiff` with syntax highlighting
- **Directory navigation**: Colored file permissions and sizes

#### **🚀 Smart Color Detection**
- **Auto-detection**: Colors only appear when terminal supports them
- **256-color support**: Full color palette for modern terminals
- **Universal compatibility**: Works with all major terminal emulators

#### **💡 Development-Focused Aliases**
```bash
# Navigation
ll          # Detailed colored file listing
la          # All files with colors  
..          # Quick parent directory
cls         # Clear screen

# Git workflow  
gst         # Colorful git status
glog        # Beautiful commit graph
gdiff       # Syntax-highlighted diffs

# Development
python      # Points to python3
pip         # Points to pip3
```

This creates a **pleasant, productive development environment** that makes working with AxE more enjoyable! 🎯

---

## 📚 Additional Learning Resources

For comprehensive learning resources including RISC-V toolchain guides, Docker fundamentals, and AxE project documentation, visit our main [Documentation Wiki](README.md).

**Quick Links:**
- **[RISC-V Toolchain Guide](RISCV-Toolchain.md)** - Complete cross-compilation reference
- **[Docker Concepts](Docker-Concepts.md)** - Docker theory and best practices  
- **[AxE Project Overview](AxE-Overview.md)** - Project architecture and research context

---

This tutorial covers Docker from basics to advanced concepts used in our AxE project. Each line serves a specific purpose in creating a robust, reproducible development environment!