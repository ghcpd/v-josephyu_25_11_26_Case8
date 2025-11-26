# Flask Project Manager — corrected onboarding and tutorial

This file contains the corrected onboarding steps and working examples verified against the repository.

Onboarding (PowerShell)
------------------------
1. Create a virtual environment and activate it:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure the database connection (match the app's env var):
   ```powershell
   $env:DATABASE_URL = "sqlite:///project_manager.db"
   ```
4. Launch the tutorial server (use the actual module `app`):
   ```powershell
   flask --app app run --debug
   ```

Onboarding (bash / macOS / Linux)
--------------------------------
1. Create & activate venv:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set DB env var and run server:
   ```bash
   export DATABASE_URL="sqlite:///project_manager.db"
   flask --app app run --debug
   ```

Tutorial: Creating a Project (working example)
--------------------------------------------
Use requests to create a new project (this example matches the app’s JSON format exactly):

```python
import requests

payload = {
    "name": "Sample Project",
    "owner_email": "lead@example.com"
}

resp = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(resp.status_code, resp.json())
```

Expected response body:

```json
{"id": 1, "name": "Sample Project", "owner_email": "lead@example.com"}
```

Listing tasks for a project (working example)
--------------------------------------------
```python
import requests

resp = requests.get("http://127.0.0.1:5000/projects/1/tasks")
print(resp.json())  # e.g. [] when no tasks exist
```

Notes
-----
- The app reads the `DATABASE_URL` environment variable. Update your environment accordingly when running locally or in CI.
- Tests are included in `tests/test_app.py` and were validated with an in-memory SQLite database.
