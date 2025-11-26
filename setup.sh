#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

# Default database (override by exporting DATABASE_URL before running)
export DATABASE_URL="${DATABASE_URL:-sqlite:///project_manager.db}"

echo "Environment ready. To run the server:"
echo "  flask --app project_manager run --debug"
