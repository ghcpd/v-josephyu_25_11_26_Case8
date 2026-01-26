import pytest
import requests
import time
import subprocess
import os
import signal
import sys


@pytest.fixture(scope='module')
def live_server():
    """Start a live Flask server for integration testing."""
    # Set environment variable
    env = os.environ.copy()
    env['DB_URL'] = 'sqlite:///test_integration.db'
    
    # Determine Python executable
    if sys.platform == 'win32':
        python_exe = os.path.join('.venv', 'Scripts', 'python.exe')
    else:
        python_exe = os.path.join('.venv', 'bin', 'python')
    
    if not os.path.exists(python_exe):
        python_exe = 'python'
    
    # Start Flask server
    process = subprocess.Popen(
        [python_exe, '-m', 'flask', '--app', 'app', 'run', '--port', '5001'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    yield 'http://127.0.0.1:5001'
    
    # Cleanup: stop server and remove test database
    if sys.platform == 'win32':
        process.terminate()
    else:
        os.kill(process.pid, signal.SIGTERM)
    
    process.wait(timeout=5)
    
    if os.path.exists('test_integration.db'):
        os.remove('test_integration.db')


def test_integration_health_check(live_server):
    """Test health check endpoint in live server."""
    response = requests.get(f'{live_server}/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_integration_create_and_list_projects(live_server):
    """Test creating and listing projects in live server."""
    # Create first project
    payload1 = {
        'name': 'Integration Project 1',
        'owner': 'int1@example.com'
    }
    response1 = requests.post(f'{live_server}/projects', json=payload1)
    assert response1.status_code == 201
    project1 = response1.json()
    assert project1['name'] == 'Integration Project 1'
    assert 'id' in project1
    
    # Create second project
    payload2 = {
        'name': 'Integration Project 2',
        'owner': 'int2@example.com'
    }
    response2 = requests.post(f'{live_server}/projects', json=payload2)
    assert response2.status_code == 201
    project2 = response2.json()
    
    # List all projects
    response3 = requests.get(f'{live_server}/projects')
    assert response3.status_code == 200
    projects = response3.json()
    assert len(projects) >= 2
    assert any(p['name'] == 'Integration Project 1' for p in projects)
    assert any(p['name'] == 'Integration Project 2' for p in projects)


def test_integration_list_tasks_for_project(live_server):
    """Test listing tasks for a project in live server."""
    # Create a project
    payload = {
        'name': 'Project with Tasks',
        'owner': 'tasks@example.com'
    }
    response1 = requests.post(f'{live_server}/projects', json=payload)
    project = response1.json()
    project_id = project['id']
    
    # List tasks (should be empty)
    response2 = requests.get(f'{live_server}/projects/{project_id}/tasks')
    assert response2.status_code == 200
    tasks = response2.json()
    assert tasks == []


def test_integration_workflow(live_server):
    """Test a complete workflow in live server."""
    # Step 1: Verify server is healthy
    health_response = requests.get(f'{live_server}/health')
    assert health_response.status_code == 200
    
    # Step 2: Create a new project
    project_payload = {
        'name': 'Workflow Test Project',
        'owner': 'workflow@example.com'
    }
    create_response = requests.post(f'{live_server}/projects', json=project_payload)
    assert create_response.status_code == 201
    project = create_response.json()
    project_id = project['id']
    
    # Step 3: Verify project appears in list
    list_response = requests.get(f'{live_server}/projects')
    assert list_response.status_code == 200
    projects = list_response.json()
    assert any(p['id'] == project_id for p in projects)
    
    # Step 4: Check tasks for the project
    tasks_response = requests.get(f'{live_server}/projects/{project_id}/tasks')
    assert tasks_response.status_code == 200
    tasks = tasks_response.json()
    assert isinstance(tasks, list)


def test_integration_invalid_project_creation(live_server):
    """Test creating project with invalid data in live server."""
    # Missing owner field
    payload = {
        'name': 'Invalid Project'
    }
    response = requests.post(f'{live_server}/projects', json=payload)
    assert response.status_code in [400, 500]


def test_integration_tasks_for_nonexistent_project(live_server):
    """Test listing tasks for nonexistent project in live server."""
    response = requests.get(f'{live_server}/projects/999999/tasks')
    assert response.status_code == 200
    tasks = response.json()
    assert tasks == []
