#!/bin/bash
# install.sh — Market RU Landing skill installer
# Usage: curl -fsSL .../install.sh | bash

set -e

REPO="https://github.com/Valdiss-Valdiss/ai-marketing-ru-landing.git"
SKILL_DIR="market-ru-landing"

echo "Installing Market RU Landing skill..."

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SKILLS_DIR="$HOME/.claude/skills/"
    AGENTS_DIR="$HOME/.claude/agents/"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    SKILLS_DIR="$HOME/.claude/skills/"
    AGENTS_DIR="$HOME/.claude/agents/"
else
    # Windows (Git Bash, WSL)
    SKILLS_DIR="$HOME/.claude/skills/"
    AGENTS_DIR="$HOME/.claude/agents/"
fi

# Clone to temp directory
echo "Downloading..."
git clone --depth 1 "$REPO" "/tmp/$SKILL_DIR" 2>/dev/null || {
    echo "Error: Failed to clone repository"
    exit 1
}

# Create directories
mkdir -p "$SKILLS_DIR"
mkdir -p "$AGENTS_DIR"

# Install skill files
echo "Installing skill..."
cp -r "/tmp/$SKILL_DIR/skills/$SKILL_DIR" "$SKILLS_DIR/"

# Install scripts
if [ -d "/tmp/$SKILL_DIR/scripts" ]; then
    mkdir -p "$SKILLS_DIR/$SKILL_DIR/scripts"
    cp /tmp/$SKILL_DIR/scripts/*.py "$SKILLS_DIR/$SKILL_DIR/scripts/" 2>/dev/null || true
fi

# Install agents (if any)
if [ -d "/tmp/$SKILL_DIR/agents" ]; then
    cp /tmp/$SKILL_DIR/agents/*.md "$AGENTS_DIR/" 2>/dev/null || true
fi

# Cleanup
rm -rf "/tmp/$SKILL_DIR"

echo ""
echo "Installation complete!"
echo "Skill installed to: $SKILLS_DIR$SKILL_DIR"
echo ""
echo "Usage: /market-ru landing <url>"
echo ""
echo "Example:"
echo "  /market-ru landing https://example.com"