#!/bin/bash

# Flask Project Manager - Setup Script
# This script automates the environment setup process

set -e  # Exit on any error

echo "=========================================="
echo "Flask Project Manager - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "✓ Found Python: $($PYTHON_CMD --version)"
echo ""

# Step 1: Create virtual environment
echo "Step 1: Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "  ⚠ Virtual environment already exists. Removing old environment..."
    rm -rf .venv
fi

$PYTHON_CMD -m venv .venv
echo "✓ Virtual environment created"
echo ""

# Step 2: Activate virtual environment and install dependencies
echo "Step 2: Installing dependencies..."

# Determine OS for activation
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash)
    source .venv/Scripts/activate
elif [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
    # macOS or Linux
    source .venv/bin/activate
else
    echo "  ⚠ Unknown OS type: $OSTYPE"
    echo "  Please activate the virtual environment manually:"
    echo "    - Windows PowerShell: .\\.venv\\Scripts\\activate"
    echo "    - Windows Git Bash: source .venv/Scripts/activate"
    echo "    - Linux/macOS: source .venv/bin/activate"
    exit 1
fi

pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 3: Verify installation
echo "Step 3: Verifying installation..."
echo "  Checking Flask..."
python -c "import flask; print(f'    ✓ Flask {flask.__version__}')" || exit 1

echo "  Checking Flask-SQLAlchemy..."
python -c "import flask_sqlalchemy; print(f'    ✓ Flask-SQLAlchemy installed')" || exit 1

echo "  Checking pytest..."
python -c "import pytest; print(f'    ✓ pytest {pytest.__version__}')" || exit 1

echo "  Checking requests..."
python -c "import requests; print(f'    ✓ requests {requests.__version__}')" || exit 1

echo ""
echo "✓ All dependencies verified"
echo ""

# Step 4: Database setup information
echo "Step 4: Database configuration..."
echo "  ℹ Database will be created automatically on first run"
echo "  ℹ Database file: project_manager.db"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the Flask application:"
echo ""
echo "  On Windows PowerShell:"
echo "    .\\.venv\\Scripts\\activate"
echo "    \$env:DB_URL = \"sqlite:///project_manager.db\""
echo "    flask --app app run --debug"
echo ""
echo "  On Windows Git Bash:"
echo "    source .venv/Scripts/activate"
echo "    export DB_URL=\"sqlite:///project_manager.db\""
echo "    flask --app app run --debug"
echo ""
echo "  On Linux/macOS:"
echo "    source .venv/bin/activate"
echo "    export DB_URL=\"sqlite:///project_manager.db\""
echo "    flask --app app run --debug"
echo ""
echo "To run tests:"
echo "    bash run_tests.sh"
echo ""
echo "The API will be available at: http://127.0.0.1:5000"
echo ""
