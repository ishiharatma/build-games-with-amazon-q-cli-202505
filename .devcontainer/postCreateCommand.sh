#!/bin/bash
set -e

git config --global core.autocrlf false
git config --global core.filemode false

echo "=== Post-create setup starting ==="

# Amazon Q CLIの設定確認
if command -v q &> /dev/null; then
    echo "✅ Amazon Q CLI is available"
    echo "Amazon Q CLI version:"
    q --version || echo "Version check failed but CLI is installed"
else
    echo "❌ Amazon Q CLI not found"
fi

# AWS CLIの設定確認
if command -v aws &> /dev/null; then
    echo "✅ AWS CLI is available"
    echo "AWS CLI version:"
    aws --version
else
    echo "❌ AWS CLI not found"
fi
# Pythonの設定確認
if command -v python3 &> /dev/null; then
    echo "✅ Python3 is available"
    echo "Python version:"
    python3 --version
else
    echo "❌ Python3 not found"
fi

echo "=== Post-create setup completed ==="
echo "You can now use:"
echo "  - q --help          (Amazon Q CLI)"
echo "  - aws --help        (AWS CLI)"
echo "  - python3 --version (Python)"
