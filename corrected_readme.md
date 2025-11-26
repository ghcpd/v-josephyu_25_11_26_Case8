# Flask Project Manager (Corrected)

A minimal project management API built with Flask.

---

## 🧰 Onboarding

### PowerShell (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Optional – override database
$env:DATABASE_URL = "sqlite:///project_manager.db"  # default if unset
# Run the server
flask --app project_manager run --debug
```

### Bash (macOS/Linux/WSL)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Optional – override database
export DATABASE_URL="sqlite:///project_manager.db"
# Run the server
flask --app project_manager run --debug
```

> **Note:** The app prefers `DATABASE_URL`, falls back to `DB_URL`, and otherwise uses `sqlite:///project_manager.db`.

---

## 🚀 Tutorials

Assuming the server is running at `http://127.0.0.1:5000`.

### 1) Create a project
```python
import requests
payload = {"name": "Sample Project", "owner_email": "lead@example.com"}
resp = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(resp.status_code)
print(resp.json())
# → {"id": 1, "name": "Sample Project", "owner_email": "lead@example.com"}
```

### 2) List projects
```python
import requests
resp = requests.get("http://127.0.0.1:5000/projects")
print(resp.json())
```

### 3) Create a task for a project
```python
import requests
payload = {"title": "First task", "status": "todo"}
resp = requests.post("http://127.0.0.1:5000/api/projects/1/tasks", json=payload)
print(resp.json())  # → {"id": 1, "title": "First task", "status": "todo"}
```

### 4) List tasks for a project
```python
import requests
resp = requests.get("http://127.0.0.1:5000/api/projects/1/tasks")
print(resp.json())  # → [{"id": 1, "title": "First task", "status": "todo"}]
```

---

## 🔌 API Reference

| Method | Path                                 | Description                |
|--------|--------------------------------------|----------------------------|
| GET    | `/health`                            | Health check               |
| GET    | `/projects` or `/api/projects`       | List projects              |
| POST   | `/projects` or `/api/projects`       | Create project             |
| GET    | `/projects/<id>/tasks` or `/api/projects/<id>/tasks` | List tasks for project |
| POST   | `/projects/<id>/tasks` or `/api/projects/<id>/tasks` | Create task for project |

Payloads:
- **Create project:** `{ "name": str, "owner_email": str }` (`owner` also accepted)
- **Create task:** `{ "title": str, "status": str = "todo" }

---

## 🧪 Tests

Run the automated tests:
```bash
./run_tests.sh        # bash
# or
pytest                # inside activated venv
```

---

## ⚙️ Troubleshooting
- **Module not found (`project_manager`)**: Ensure you’re in the repo root and using the venv (`.venv`).
- **`flask_sqlalchemy` missing**: `pip install -r requirements.txt` inside the venv.
- **Schema changes**: Delete `project_manager.db` and restart to recreate tables.
