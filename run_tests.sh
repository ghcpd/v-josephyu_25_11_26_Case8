#!/bin/bash

# Flask Project Manager - Test Runner Script
# This script runs all pytest test cases

set -e  # Exit on any error

echo "=========================================="
echo "Flask Project Manager - Test Runner"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run setup.sh first to create the environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash)
    source .venv/Scripts/activate
elif [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu"* ]]; then
    # macOS or Linux
    source .venv/bin/activate
else
    echo "Error: Unknown OS type: $OSTYPE"
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Set environment variable for tests
export DB_URL="sqlite:///:memory:"

# Clean up any existing test databases
echo "Cleaning up test artifacts..."
rm -f test_integration.db project_manager.db
echo "✓ Test artifacts cleaned"
echo ""

# Run pytest with coverage and verbose output
echo "Running tests..."
echo "=========================================="
echo ""

# Run tests with different verbosity levels
pytest -v --tb=short test_api.py test_models.py test_app.py

# Check if basic tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ All basic tests passed!"
    echo "=========================================="
    echo ""
    
    # Optionally run integration tests (commented out by default as they take longer)
    # Uncomment the following lines to run integration tests
    # echo "Running integration tests..."
    # pytest -v --tb=short test_integration.py
    # 
    # if [ $? -eq 0 ]; then
    #     echo ""
    #     echo "=========================================="
    #     echo "✓ All integration tests passed!"
    #     echo "=========================================="
    # else
    #     echo ""
    #     echo "=========================================="
    #     echo "✗ Some integration tests failed"
    #     echo "=========================================="
    #     exit 1
    # fi
    
    echo ""
    echo "Test Summary:"
    echo "  • API endpoint tests: PASSED"
    echo "  • Model tests: PASSED"
    echo "  • Application tests: PASSED"
    echo "  • Integration tests: SKIPPED (uncomment in run_tests.sh to enable)"
    echo ""
    echo "All required tests completed successfully!"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "✗ Some tests failed"
    echo "=========================================="
    echo ""
    echo "Please review the error output above."
    exit 1
fi

# Cleanup
echo "Cleaning up..."
rm -f test_integration.db
echo "✓ Cleanup complete"
echo ""
