# Flask Project Manager (Corrected)

This document corrects the onboarding and tutorial steps from the project README.

## Onboarding (Windows PowerShell)

1. Create a virtual environment and activate it:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
2. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure the database connection:
   ```powershell
   # The app supports either DB_URL or DATABASE_URL for backwards compatibility
   $env:DB_URL = "sqlite:///project_manager.db"
   ```
4. Launch the server:
   ```powershell
   # The application file is app.py so use `app` here
   flask --app app run --debug
   ```

## Tutorial: Creating a Project

Use this snippet to create your first project (supported keys: `owner` and `owner_email`):

```python
import requests

payload = {
    "name": "Sample Project",
    "owner": "lead@example.com"
}
response = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(response.json())
```

The server also supports `owner_email` as an alias for `owner`, so the original snippet will work too:

```python
payload = {
    "name": "Sample Project",
    "owner_email": "lead@example.com"
}
```

Expected response:

```json
{"id": 1, "name": "Sample Project", "owner": "lead@example.com"}
```

## Listing Tasks for a Project

```python
import requests

response = requests.get("http://127.0.0.1:5000/projects/1/tasks")
print(response.json())
```

Note: The code uses `/projects/<id>/tasks` (no `/api/` prefix) for listing tasks.
