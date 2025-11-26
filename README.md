# Flask Project Manager

A minimal project management API built with Flask.

NOTE: If you are following this project's tutorial, please see `corrected_readme.md` for working onboarding instructions and examples (it fixes a few inconsistencies in this original README). 

## Onboarding

1. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure the database connection:
   ```powershell
   $env:DATABASE_URL = "sqlite:///project_manager.db"
   ```
4. Launch the tutorial server:
   ```powershell
   flask --app project_manager run --debug
   ```

## Tutorial: Creating a Project

Use this snippet to create your first project:

```python
import requests

payload = {
    "name": "Sample Project",
    "owner_email": "lead@example.com"
}
response = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(response.json())
```

You should receive a response like:

```json
{"id": 1, "name": "Sample Project", "owner_email": "lead@example.com"}
```

## Listing Tasks for a Project

```python
import requests

response = requests.get("http://127.0.0.1:5000/api/projects/1/tasks")
print(response.json())
```

