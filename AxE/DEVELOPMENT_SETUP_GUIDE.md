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
