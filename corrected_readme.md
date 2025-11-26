# Flask Project Manager (Corrected)

This is a minimal project management API built with Flask.

## Onboarding (updated)

1. Create a virtual environment and activate it (Windows Powershell example):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure the database connection (the app accepts `DATABASE_URL` or `DB_URL`):
   ```powershell
   $env:DATABASE_URL = "sqlite:///project_manager.db"
   ```
4. Launch the tutorial server (module is `app`):
   ```powershell
   flask --app app run --debug
   ```

## Tutorial: Creating a Project (updated)

Use this snippet to create your first project (the server expects `owner` key):

```python
import requests

payload = {
    "name": "Sample Project",
    "owner": "lead@example.com"
}
response = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(response.json())
```

You should receive a response like:

```json
{"id": 1, "name": "Sample Project", "owner": "lead@example.com"}
```

## Listing Tasks for a Project (updated)

Use the following endpoint — note there's no `/api` prefix in the current app:

```python
import requests

response = requests.get("http://127.0.0.1:5000/projects/1/tasks")
print(response.json())
```

Notes:
- The app will read `DATABASE_URL` or `DB_URL` when starting. We updated the code to be backward compatible with both env var names.
- Added `Flask-SQLAlchemy` and `requests` to `requirements.txt` for the tutorial and testing.
