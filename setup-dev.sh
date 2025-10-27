#!/bin/bash

# Development Setup Script for action-repo-maintenance
# This script sets up the development environment

set -e  # Exit on error

echo "================================================"
echo "QuantEcon Repository Maintenance - Dev Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Python 3.9 or higher required. Found: $python_version"
    exit 1
fi
echo "✓ Python version OK: $python_version"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Install dev dependencies
echo "Installing development dependencies..."
pip install pytest pytest-cov pytest-mock black ruff mypy > /dev/null 2>&1
echo "✓ Development dependencies installed"
echo ""

# Create config from example if it doesn't exist
if [ ! -f "config.yml" ]; then
    echo "Creating config.yml from example..."
    cp config.example.yml config.yml
    echo "✓ config.yml created (please customize before running)"
    echo "  Edit config.yml to add your settings"
else
    echo "✓ config.yml already exists"
fi
echo ""

# Check for required environment variables
echo "Checking environment variables..."
missing_vars=()

if [ -z "$GITHUB_TOKEN" ]; then
    missing_vars+=("GITHUB_TOKEN")
fi

if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    missing_vars+=("AWS_ACCESS_KEY_ID")
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    missing_vars+=("AWS_SECRET_ACCESS_KEY")
fi

if [ ${#missing_vars[@]} -eq 0 ]; then
    echo "✓ All required environment variables are set"
else
    echo "⚠️  Missing environment variables:"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "Set them with:"
    echo '  export GITHUB_TOKEN="your_token"'
    echo '  export AWS_ACCESS_KEY_ID="your_key"'
    echo '  export AWS_SECRET_ACCESS_KEY="your_secret"'
fi
echo ""

# Run tests
echo "Running tests..."
if pytest tests/ -v; then
    echo "✓ All tests passed"
else
    echo "⚠️  Some tests failed (this is expected if you haven't configured credentials)"
fi
echo ""

echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Edit config.yml with your settings"
echo "  2. Set required environment variables (if not already set)"
echo "  3. Run: source venv/bin/activate"
echo "  4. Test: python -m src.main --config config.yml --task report"
echo ""
echo "For more information, see QUICKSTART.md"
echo ""
