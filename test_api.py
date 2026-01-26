"""
Test suite for Flask Project Manager API
Tests all endpoints and error cases
"""

import pytest
from app import app, db
from models import Project, Task


@pytest.fixture
def client():
    """Create a test client and initialize the test database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


class TestHealthEndpoint:
    """Test suite for health check endpoint"""
    
    def test_health_check_returns_ok(self, client):
        """Health check should return status OK"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json == {'status': 'ok'}


class TestProjectEndpoints:
    """Test suite for project-related endpoints"""
    
    def test_list_projects_empty(self, client):
        """GET /projects should return empty list when no projects exist"""
        response = client.get('/projects')
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_project_success(self, client):
        """POST /projects should create a new project and return 201"""
        payload = {
            'name': 'Test Project',
            'owner': 'test@example.com'
        }
        response = client.post('/projects', json=payload)
        
        assert response.status_code == 201
        data = response.json
        assert data['id'] == 1
        assert data['name'] == 'Test Project'
        assert data['owner'] == 'test@example.com'
    
    def test_create_project_missing_name(self, client):
        """POST /projects without name should fail"""
        payload = {'owner': 'test@example.com'}
        response = client.post('/projects', json=payload)
        
        assert response.status_code == 400
    
    def test_create_project_missing_owner(self, client):
        """POST /projects without owner should fail"""
        payload = {'name': 'Test Project'}
        response = client.post('/projects', json=payload)
        
        assert response.status_code == 400
    
    def test_list_projects_with_data(self, client):
        """GET /projects should return list of created projects"""
        # Create a project
        payload = {'name': 'Project 1', 'owner': 'owner1@example.com'}
        client.post('/projects', json=payload)
        
        # Create another project
        payload = {'name': 'Project 2', 'owner': 'owner2@example.com'}
        client.post('/projects', json=payload)
        
        # List projects
        response = client.get('/projects')
        assert response.status_code == 200
        projects = response.json
        assert len(projects) == 2
        assert projects[0]['name'] == 'Project 1'
        assert projects[1]['name'] == 'Project 2'
    
    def test_create_multiple_projects_increment_id(self, client):
        """IDs should increment correctly when creating multiple projects"""
        payload1 = {'name': 'Project 1', 'owner': 'owner1@example.com'}
        response1 = client.post('/projects', json=payload1)
        project1_id = response1.json['id']
        
        payload2 = {'name': 'Project 2', 'owner': 'owner2@example.com'}
        response2 = client.post('/projects', json=payload2)
        project2_id = response2.json['id']
        
        assert project2_id == project1_id + 1


class TestTaskEndpoints:
    """Test suite for task-related endpoints"""
    
    def test_list_tasks_for_nonexistent_project(self, client):
        """GET /projects/999/tasks should return empty list (no error)"""
        response = client.get('/projects/999/tasks')
        assert response.status_code == 200
        assert response.json == []
    
    def test_list_tasks_for_existing_project(self, client):
        """GET /projects/<id>/tasks should return list of tasks"""
        # Create a project
        project_payload = {'name': 'Test Project', 'owner': 'test@example.com'}
        project_response = client.post('/projects', json=project_payload)
        project_id = project_response.json['id']
        
        # List tasks for project (should be empty)
        response = client.get(f'/projects/{project_id}/tasks')
        assert response.status_code == 200
        assert response.json == []
    
    def test_list_tasks_endpoint_format(self, client):
        """Verify correct endpoint format /projects/<id>/tasks exists"""
        response = client.get('/projects/1/tasks')
        assert response.status_code == 200  # Should work without the /api prefix
    
    def test_incorrect_endpoint_api_prefix_returns_404(self, client):
        """Old endpoint /api/projects/<id>/tasks should return 404"""
        response = client.get('/api/projects/1/tasks')
        assert response.status_code == 404


class TestResponseFormats:
    """Test suite for response format compliance"""
    
    def test_create_project_response_format(self, client):
        """Verify create project response contains correct fields"""
        payload = {'name': 'Test', 'owner': 'test@example.com'}
        response = client.post('/projects', json=payload)
        
        data = response.json
        assert 'id' in data
        assert 'name' in data
        assert 'owner' in data
        # Ensure response does NOT have owner_email
        assert 'owner_email' not in data
    
    def test_list_projects_response_format(self, client):
        """Verify list projects response contains correct fields"""
        payload = {'name': 'Test', 'owner': 'test@example.com'}
        client.post('/projects', json=payload)
        
        response = client.get('/projects')
        projects = response.json
        assert len(projects) > 0
        
        for project in projects:
            assert 'id' in project
            assert 'name' in project
            assert 'owner' in project
            assert 'owner_email' not in project
    
    def test_list_tasks_response_format(self, client):
        """Verify list tasks response contains correct fields"""
        # Create a project
        project_payload = {'name': 'Test', 'owner': 'test@example.com'}
        project_response = client.post('/projects', json=project_payload)
        project_id = project_response.json['id']
        
        # List tasks
        response = client.get(f'/projects/{project_id}/tasks')
        tasks = response.json
        
        # Even if empty, response should be a list
        assert isinstance(tasks, list)


class TestStatusCodes:
    """Test suite for HTTP status codes"""
    
    def test_create_project_returns_201_created(self, client):
        """Create project should return 201 Created status"""
        payload = {'name': 'Test', 'owner': 'test@example.com'}
        response = client.post('/projects', json=payload)
        assert response.status_code == 201
    
    def test_list_projects_returns_200_ok(self, client):
        """List projects should return 200 OK status"""
        response = client.get('/projects')
        assert response.status_code == 200
    
    def test_list_tasks_returns_200_ok(self, client):
        """List tasks should return 200 OK status"""
        response = client.get('/projects/1/tasks')
        assert response.status_code == 200
    
    def test_health_check_returns_200_ok(self, client):
        """Health check should return 200 OK status"""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_invalid_endpoint_returns_404(self, client):
        """Invalid endpoint should return 404 Not Found"""
        response = client.get('/invalid/endpoint')
        assert response.status_code == 404


class TestDataPersistence:
    """Test suite for data persistence across requests"""
    
    def test_project_persists_after_creation(self, client):
        """Created project should persist in database"""
        # Create project
        payload = {'name': 'Persistent Project', 'owner': 'test@example.com'}
        create_response = client.post('/projects', json=payload)
        project_id = create_response.json['id']
        
        # List projects and verify it exists
        list_response = client.get('/projects')
        projects = list_response.json
        
        project_ids = [p['id'] for p in projects]
        assert project_id in project_ids
    
    def test_project_data_correctness(self, client):
        """Project data should be returned correctly after creation"""
        payload = {'name': 'Test Project', 'owner': 'owner@example.com'}
        create_response = client.post('/projects', json=payload)
        created_id = create_response.json['id']
        
        list_response = client.get('/projects')
        projects = list_response.json
        
        found_project = next((p for p in projects if p['id'] == created_id), None)
        assert found_project is not None
        assert found_project['name'] == 'Test Project'
        assert found_project['owner'] == 'owner@example.com'
