import os
import importlib


# Ensure the app will initialize with an in-memory database for tests
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")


def _get_app():
    # import app module (which runs init_database at import-time)
    if "app" in globals():
        importlib.reload(globals()["app"])  # rarely needed, but safe
    import app as app_mod
    return app_mod


def test_health():
    app_mod = _get_app()
    client = app_mod.app.test_client()

    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_create_and_list_projects():
    app_mod = _get_app()
    client = app_mod.app.test_client()

    payload = {"name": "Sample Project", "owner_email": "lead@example.com"}
    r = client.post("/projects", json=payload)

    assert r.status_code == 201
    body = r.get_json()
    # id should be a positive integer and returned fields should match
    assert isinstance(body.get("id"), int) and body.get("id") > 0
    assert body["name"] == "Sample Project"
    assert body["owner_email"] == "lead@example.com"

    r = client.get("/projects")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)
    # the created project should appear in the list
    assert any(p["name"] == "Sample Project" and p["owner_email"] == "lead@example.com" for p in data)


def test_list_tasks_empty():
    app_mod = _get_app()
    client = app_mod.app.test_client()

    # create a fresh project then verify its tasks endpoint is empty
    r = client.post("/projects", json={"name": "Another", "owner_email": "x@x.com"})
    pid = r.get_json()["id"]
    r = client.get(f"/projects/{pid}/tasks")
    assert r.status_code == 200
    assert r.get_json() == []
