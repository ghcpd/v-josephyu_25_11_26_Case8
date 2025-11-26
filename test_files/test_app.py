import os
import json

def setup_module(module):
    # Ensure the DB uses an in-memory SQLite for tests
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"


def test_create_and_list_project():
    # Import app after environment variable is set
    from app import app, db

    client = app.test_client()

    # Create a project
    payload = {"name": "Test Project", "owner": "tester@example.com"}
    response = client.post("/projects", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Project"
    assert data["owner"] == "tester@example.com"

    # List projects
    response = client.get("/projects")
    assert response.status_code == 200
    projects = response.get_json()
    assert any(p["name"] == "Test Project" for p in projects)


def test_list_tasks_empty():
    from app import app, db

    client = app.test_client()
    # Ensure project 1 exists (from previous test)
    response = client.get("/projects/1/tasks")
    assert response.status_code == 200
    tasks = response.get_json()
    assert isinstance(tasks, list)
    assert tasks == []
