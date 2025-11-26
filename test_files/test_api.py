import os
import importlib
import pytest


@pytest.fixture(scope="session")
def app_module():
    # Ensure the app uses an in-memory SQLite DB for tests
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    import app as app_module
    importlib.reload(app_module)
    return app_module


@pytest.fixture()
def app(app_module):
    app = app_module.app
    with app.app_context():
        app_module.db.drop_all()
        app_module.db.create_all()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_create_project_and_list(client):
    payload = {"name": "Sample Project", "owner_email": "lead@example.com"}
    resp = client.post("/projects", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == payload["name"]
    assert data["owner_email"] == payload["owner_email"]
    project_id = data["id"]

    resp_list = client.get("/projects")
    assert resp_list.status_code == 200
    projects = resp_list.get_json()
    assert len(projects) == 1
    assert projects[0]["id"] == project_id


def test_create_project_accepts_owner_alias(client):
    payload = {"name": "Legacy Project", "owner": "legacy@example.com"}
    resp = client.post("/projects", json=payload)
    assert resp.status_code == 201
    assert resp.get_json()["owner_email"] == payload["owner"]


def test_missing_project_fields(client):
    resp = client.post("/projects", json={"name": "No owner"})
    assert resp.status_code == 400
    assert "owner_email" in resp.get_json()["error"]


def test_tasks_flow(client):
    # Create project
    proj = client.post(
        "/projects",
        json={"name": "Proj", "owner_email": "a@b.com"},
    ).get_json()
    pid = proj["id"]

    resp_empty = client.get(f"/api/projects/{pid}/tasks")
    assert resp_empty.status_code == 200
    assert resp_empty.get_json() == []

    resp_task = client.post(f"/api/projects/{pid}/tasks", json={"title": "T1"})
    assert resp_task.status_code == 201
    task = resp_task.get_json()
    assert task["title"] == "T1"
    assert task["status"] == "todo"

    # List again via both routes
    for path in (f"/api/projects/{pid}/tasks", f"/projects/{pid}/tasks"):
        resp_list = client.get(path)
        assert resp_list.status_code == 200
        tasks = resp_list.get_json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "T1"
