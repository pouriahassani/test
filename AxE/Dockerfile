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
RUN mkdir -p /opt/riscv 



# =============================================================================
# RISC-V TOOLCHAIN
# =============================================================================

RUN git clone --depth=1 --branch=2025.06.13 \
    https://github.com/riscv-collab/riscv-gnu-toolchain.git riscv-gnu-toolchain

RUN cd riscv-gnu-toolchain && mkdir build-rv32im && cd build-rv32im && \
    ../configure --prefix=/opt/riscv --with-arch=rv32im --with-abi=ilp32 \
    --enable-multilib --disable-linux \
    --enable-newlib-io-float \
    --enable-newlib-io-long-long && \

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
RUN npm install -g @anthropic-ai/claude-code && chown $USERNAME:$USERNAME /opt/riscv

# Create Claude config directory
RUN mkdir -p ~/.config/claude && chown -R $USERNAME:$USERNAME /home/axe

# =============================================================================
# ENVIRONMENT & SHELL SETUP
# =============================================================================

# Switch to axe user
USER $USERNAME
WORKDIR $WORKDIR
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
