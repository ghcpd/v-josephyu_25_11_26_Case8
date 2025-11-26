import os
import pytest
from app import app, db


@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    # Set up test database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def sample_project(client):
    """Create a sample project for testing."""
    response = client.post('/projects', json={
        'name': 'Test Project',
        'owner': 'test@example.com'
    })
    return response.get_json()


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {'status': 'ok'}


def test_list_projects_empty(client):
    """Test listing projects when database is empty."""
    response = client.get('/projects')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_create_project_success(client):
    """Test creating a project with valid data."""
    payload = {
        'name': 'New Project',
        'owner': 'owner@example.com'
    }
    response = client.post('/projects', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    
    assert 'id' in data
    assert data['name'] == 'New Project'
    assert data['owner'] == 'owner@example.com'
    assert isinstance(data['id'], int)


def test_create_project_missing_name(client):
    """Test creating a project without name field."""
    payload = {
        'owner': 'owner@example.com'
    }
    # The app doesn't validate input, so it raises a 500 error
    with pytest.raises(Exception):
        response = client.post('/projects', json=payload)


def test_create_project_missing_owner(client):
    """Test creating a project without owner field."""
    payload = {
        'name': 'New Project'
    }
    # The app doesn't validate input, so it raises a 500 error
    with pytest.raises(Exception):
        response = client.post('/projects', json=payload)


def test_list_projects_with_data(client, sample_project):
    """Test listing projects when projects exist."""
    response = client.get('/projects')
    assert response.status_code == 200
    data = response.get_json()
    
    assert len(data) == 1
    assert data[0]['name'] == 'Test Project'
    assert data[0]['owner'] == 'test@example.com'
    assert 'id' in data[0]


def test_create_multiple_projects(client):
    """Test creating multiple projects."""
    projects = [
        {'name': 'Project 1', 'owner': 'owner1@example.com'},
        {'name': 'Project 2', 'owner': 'owner2@example.com'},
        {'name': 'Project 3', 'owner': 'owner3@example.com'}
    ]
    
    for project in projects:
        response = client.post('/projects', json=project)
        assert response.status_code == 201
    
    response = client.get('/projects')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 3


def test_list_tasks_empty(client, sample_project):
    """Test listing tasks for a project with no tasks."""
    project_id = sample_project['id']
    response = client.get(f'/projects/{project_id}/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_list_tasks_nonexistent_project(client):
    """Test listing tasks for a project that doesn't exist."""
    response = client.get('/projects/99999/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_project_persistence(client):
    """Test that projects persist correctly."""
    # Create a project
    payload = {'name': 'Persistent Project', 'owner': 'persist@example.com'}
    response1 = client.post('/projects', json=payload)
    project_id = response1.get_json()['id']
    
    # Retrieve it
    response2 = client.get('/projects')
    projects = response2.get_json()
    
    assert any(p['id'] == project_id for p in projects)
    project = next(p for p in projects if p['id'] == project_id)
    assert project['name'] == 'Persistent Project'
    assert project['owner'] == 'persist@example.com'


def test_create_project_empty_json(client):
    """Test creating a project with empty JSON."""
    # The app doesn't validate input, so it raises a 500 error
    with pytest.raises(Exception):
        response = client.post('/projects', json={})


def test_create_project_with_extra_fields(client):
    """Test creating a project with extra fields."""
    payload = {
        'name': 'Extra Fields Project',
        'owner': 'extra@example.com',
        'extra_field': 'should be ignored'
    }
    response = client.post('/projects', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert 'extra_field' not in data
    assert data['name'] == 'Extra Fields Project'
    assert data['owner'] == 'extra@example.com'


def test_endpoint_methods(client):
    """Test that endpoints only accept correct HTTP methods."""
    # Health endpoint should only accept GET
    response = client.post('/health')
    assert response.status_code == 405
    
    # Projects list endpoint accepts GET and POST
    response = client.put('/projects')
    assert response.status_code == 405
    
    response = client.delete('/projects')
    assert response.status_code == 405


def test_project_id_auto_increment(client):
    """Test that project IDs auto-increment correctly."""
    project1 = client.post('/projects', json={
        'name': 'Project 1',
        'owner': 'owner1@example.com'
    }).get_json()
    
    project2 = client.post('/projects', json={
        'name': 'Project 2',
        'owner': 'owner2@example.com'
    }).get_json()
    
    assert project2['id'] > project1['id']
    assert project2['id'] == project1['id'] + 1


def test_project_names_can_be_duplicates(client):
    """Test that project names can be duplicated (no unique constraint)."""
    payload = {'name': 'Duplicate Name', 'owner': 'owner1@example.com'}
    response1 = client.post('/projects', json=payload)
    assert response1.status_code == 201
    
    payload = {'name': 'Duplicate Name', 'owner': 'owner2@example.com'}
    response2 = client.post('/projects', json=payload)
    assert response2.status_code == 201


def test_owner_email_format(client):
    """Test that various email formats are accepted."""
    test_cases = [
        'simple@example.com',
        'user.name@example.com',
        'user+tag@example.co.uk',
        'user@subdomain.example.com'
    ]
    
    for email in test_cases:
        response = client.post('/projects', json={
            'name': f'Project for {email}',
            'owner': email
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['owner'] == email
