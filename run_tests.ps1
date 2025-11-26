#!/usr/bin/env pwsh
$env:DB_URL = "sqlite:///test_run_db.db"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate
pytest -q
