#!/bin/bash

# Flask Project Manager Test Runner
# This script runs all test cases using pytest

set -e

echo "=========================================="
echo "Flask Project Manager - Test Suite"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo ""
echo "Running pytest..."
echo "=========================================="

# Run all tests
python -m pytest test_api.py test_models.py -v --tb=short

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ All tests passed!"
    echo "=========================================="
    exit 0
else
    echo ""
    echo "=========================================="
    echo "✗ Some tests failed!"
    echo "=========================================="
    exit 1
fi
