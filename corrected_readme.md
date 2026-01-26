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

3. Configure the database connection:
   ```powershell
   $env:DB_URL = "sqlite:///project_manager.db"
   ```

4. Launch the tutorial server:
   ```powershell
   flask --app app run --debug
   ```

   Alternatively, you can run steps 3 and 4 in a single command:
   ```powershell
   $env:DB_URL = "sqlite:///project_manager.db"; flask --app app run --debug
   ```

## API Endpoints

### Health Check
```http
GET /health
```
Returns the health status of the API.

**Response:**
```json
{"status": "ok"}
```

### List All Projects
```http
GET /projects
```
Returns a list of all projects.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Sample Project",
    "owner": "lead@example.com"
  }
]
```

### Create a Project
```http
POST /projects
Content-Type: application/json

{
  "name": "Project Name",
  "owner": "email@example.com"
}
```

**Response:** (201 Created)
```json
{
  "id": 1,
  "name": "Project Name",
  "owner": "email@example.com"
}
```

### List Tasks for a Project
```http
GET /projects/{project_id}/tasks
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Task Title",
    "status": "todo"
  }
]
```

## Tutorial: Creating a Project

Use this snippet to create your first project:

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

## Tutorial: Listing All Projects

```python
import requests

response = requests.get("http://127.0.0.1:5000/projects")
print(response.json())
```

## Tutorial: Listing Tasks for a Project

```python
import requests

response = requests.get("http://127.0.0.1:5000/projects/1/tasks")
print(response.json())
```

This will return an empty list `[]` if no tasks have been added to the project yet.

## Tutorial: Creating a Task

To add tasks to a project, you would need to create a POST endpoint for tasks. Currently, the API only supports listing tasks.

## Running Tests

To run the automated test suite:

```powershell
pytest
```

Or use the provided test runner script:

```bash
bash run_tests.sh
```

## Quick Setup with Setup Script

You can use the provided setup script to automate the environment setup:

```bash
bash setup.sh
```

This will:
- Create the virtual environment
- Install all dependencies
- Set up the database
- Verify the installation

## Troubleshooting

### Issue: "RuntimeError: Missing DB_URL environment variable"
**Solution:** Make sure you set the `DB_URL` environment variable before starting the Flask server:
```powershell
$env:DB_URL = "sqlite:///project_manager.db"
```

### Issue: "Could not import 'project_manager'"
**Solution:** The app module is named `app`, not `project_manager`. Use:
```powershell
flask --app app run --debug
```

### Issue: "ModuleNotFoundError: No module named 'flask_sqlalchemy'"
**Solution:** Install all dependencies from requirements.txt:
```powershell
pip install -r requirements.txt
```

### Issue: 404 errors when accessing endpoints
**Solution:** Make sure you're using the correct endpoint paths:
- ✅ Correct: `/projects/1/tasks`
- ❌ Incorrect: `/api/projects/1/tasks`

## Database

The application uses SQLite by default. The database file (`project_manager.db`) will be created automatically in the project root directory when you first run the application.

## Models

### Project
- `id` (Integer, Primary Key)
- `name` (String, required)
- `owner` (String, required) - Email address of the project owner
- `tasks` (Relationship to Task model)

### Task
- `id` (Integer, Primary Key)
- `title` (String, required)
- `status` (String, default: "todo")
- `project_id` (Integer, Foreign Key to Project)

## Development

The application runs in debug mode by default, which provides:
- Automatic reloading when code changes
- Detailed error messages
- Interactive debugger

**Note:** Debug mode should not be used in production environments.

## Next Steps

To extend this application, you might want to add:
- POST endpoint for creating tasks
- PUT/PATCH endpoints for updating projects and tasks
- DELETE endpoints for removing projects and tasks
- Query parameters for filtering and sorting
- Authentication and authorization
- Input validation and error handling
- API documentation (e.g., with Swagger/OpenAPI)
