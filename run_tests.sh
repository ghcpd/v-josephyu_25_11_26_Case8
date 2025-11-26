#!/usr/bin/env bash
set -euo pipefail

echo "Running pytest..."
. .venv/bin/activate || source .venv/Scripts/activate
python -m pytest -q
