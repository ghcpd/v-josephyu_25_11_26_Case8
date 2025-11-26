#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
echo "Activating virtual environment..."
if [ -f .venv/bin/activate ]; then
  . .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  . .venv/Scripts/activate
fi
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Environment setup complete. You can run:"
echo "  $ env DATABASE_URL=\"sqlite:///project_manager.db\" flask --app app run --debug"
