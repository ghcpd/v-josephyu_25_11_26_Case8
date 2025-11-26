#!/usr/bin/env bash
# Setup script to create a virtual env and install requirements
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Setup complete. Activate the venv using: source .venv/bin/activate" 
