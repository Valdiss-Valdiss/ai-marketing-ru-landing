#!/bin/bash
# uninstall.sh — Market RU Landing skill uninstaller
# Usage: ./uninstall.sh

set -e

SKILL_DIR="market-ru-landing"

echo "Uninstalling Market RU Landing skill..."

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    SKILLS_DIR="$HOME/.claude/skills/"
    AGENTS_DIR="$HOME/.claude/agents/"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SKILLS_DIR="$HOME/.claude/skills/"
    AGENTS_DIR="$HOME/.claude/agents/"
else
    SKILLS_DIR="$HOME/.claude/skills/"
    AGENTS_DIR="$HOME/.claude/agents/"
fi

# Remove skill
if [ -d "$SKILLS_DIR/$SKILL_DIR" ]; then
    rm -rf "$SKILLS_DIR/$SKILL_DIR"
    echo "Removed: $SKILLS_DIR$SKILL_DIR"
else
    echo "Skill not found in $SKILLS_DIR"
fi

# Remove agent (if exists)
if [ -f "$AGENTS_DIR/market-ru-landing.md" ]; then
    rm -f "$AGENTS_DIR/market-ru-landing.md"
    echo "Removed: $AGENTS_DIR/market-ru-landing.md"
fi

# Note about npm uninstall for OpenCode
echo ""
echo "Note: If you installed via npm (OpenCode), also run:"
echo "  npm uninstall -g market-ru-landing"
echo ""

echo "Uninstallation complete!"