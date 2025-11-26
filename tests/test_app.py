import os
import sys
import tempfile
import json

import pytest

# Make sure the project root is importable for 'from app import app'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def make_app_with_temp_db():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    os.environ['DB_URL'] = f"sqlite:///{path}"
    # Import app after setting env
    from app import app
    return app, path


def test_health_endpoint():
    app, path = make_app_with_temp_db()
    client = app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_create_and_list_projects():
    app, path = make_app_with_temp_db()
    client = app.test_client()
    # create project
    resp = client.post('/projects', json={'name': 'My Test', 'owner': 'me@example.com'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['id'] == 1
    assert data['name'] == 'My Test'
    assert data['owner'] == 'me@example.com'

    # list
    resp = client.get('/projects')
    assert resp.status_code == 200
    projects = resp.get_json()
    assert any(p['name'] == 'My Test' for p in projects)


def test_create_with_owner_email_alias():
    app, path = make_app_with_temp_db()
    client = app.test_client()
    resp = client.post('/projects', json={'name': 'Alias Test', 'owner_email': 'alias@example.com'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['owner'] == 'alias@example.com'


def test_list_tasks_for_project():
    app, path = make_app_with_temp_db()
    client = app.test_client()
    # create project
    tmp = client.post('/projects', json={'name': 'TaskProj', 'owner': 'u@local'})
    j = tmp.get_json()
    pid = j['id']

    # create a task via the db directly
    from models import db, Task
    with app.app_context():
        t = Task(title='first', status='todo', project_id=pid)
        db.session.add(t)
        db.session.commit()

    resp = client.get(f'/projects/{pid}/tasks')
    assert resp.status_code == 200
    tasks = resp.get_json()
    assert len(tasks) == 1
    assert tasks[0]['title'] == 'first'
