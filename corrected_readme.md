# Flask Project Manager

A minimal project management API built with Flask.

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

3. Configure the database connection (use `DB_URL`, not `DATABASE_URL`):
   ```powershell
   $env:DB_URL = "sqlite:///project_manager.db"
   ```

4. Launch the tutorial server:
   ```powershell
   flask --app app run --debug
   ```

## Tutorial: Creating a Project

Use this snippet to create your first project. Note: use `owner` field, not `owner_email`:

```python
import requests

payload = {
    "name": "Sample Project",
    "owner": "lead@example.com"
}
response = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(response.json())
```

You should receive a response like (HTTP 201 Created):

```json
{"id": 1, "name": "Sample Project", "owner": "lead@example.com"}
```

## Tutorial: Listing All Projects

```python
import requests

response = requests.get("http://127.0.0.1:5000/projects")
print(response.json())
```

You should receive a response like (HTTP 200 OK):

```json
[
  {"id": 1, "name": "Sample Project", "owner": "lead@example.com"}
]
```

## Tutorial: Listing Tasks for a Project

Use the correct endpoint path `/projects/<id>/tasks` (not `/api/projects/<id>/tasks`):

```python
import requests

response = requests.get("http://127.0.0.1:5000/projects/1/tasks")
print(response.json())
```

You should receive a response like (HTTP 200 OK):

```json
[]
```

(Empty array because no tasks have been created yet)

## Tutorial: Health Check

```python
import requests

response = requests.get("http://127.0.0.1:5000/health")
print(response.json())
```

You should receive a response like (HTTP 200 OK):

```json
{"status": "ok"}
```

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check endpoint |
| GET | `/projects` | List all projects |
| POST | `/projects` | Create a new project |
| GET | `/projects/<id>/tasks` | List tasks for a project |

## API Request/Response Examples

### Create Project
- **Request:** POST `/projects`
  ```json
  {
    "name": "Project Name",
    "owner": "owner@example.com"
  }
  ```
- **Response:** 201 Created
  ```json
  {
    "id": 1,
    "name": "Project Name",
    "owner": "owner@example.com"
  }
  ```

### List Projects
- **Request:** GET `/projects`
- **Response:** 200 OK
  ```json
  [
    {
      "id": 1,
      "name": "Project Name",
      "owner": "owner@example.com"
    }
  ]
  ```

### List Tasks for Project
- **Request:** GET `/projects/1/tasks`
- **Response:** 200 OK
  ```json
  [
    {
      "id": 1,
      "title": "Task Title",
      "status": "todo"
    }
  ]
  ```
