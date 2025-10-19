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
