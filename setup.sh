#!/usr/bin/env bash
# Setup script to prepare environment (bash / *nix)
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. To run locally (bash):"
echo "  export DATABASE_URL='sqlite:///project_manager.db'"
echo "  flask --app app run --debug"
