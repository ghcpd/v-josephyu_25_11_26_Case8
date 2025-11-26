# Flask Project Manager (Corrected Guide)

Follow these instructions to get the sample API running with the existing source code.

## 1. Set Up the Environment

```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install Flask-SQLAlchemy
```

## 2. Configure the Database URL

The application expects `DB_URL`, not `DATABASE_URL`.

```powershell
$env:DB_URL = "sqlite:///project_manager.db"
```

## 3. Launch the Application

```powershell
flask --app app run --debug
```

## 4. Working Tutorial Examples

### Create a Project

```python
import requests

payload = {
    "name": "Sample Project",
    "owner": "lead@example.com"
}
response = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(response.json())
```

Expected response:

```json
{"id": 1, "name": "Sample Project", "owner": "lead@example.com"}
```

### List Tasks for a Project

```python
import requests

response = requests.get("http://127.0.0.1:5000/projects/1/tasks")
print(response.json())
```

## 5. Run the Tests

```powershell
$env:DB_URL = "sqlite:///:memory:"
pytest
```

Tests should execute without collection errors once the environment variable is present.
