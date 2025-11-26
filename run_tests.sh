#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

pip install -r requirements.txt

# Use in-memory DB for pytest (handled by fixtures via DATABASE_URL)
pytest test_files "$@"
