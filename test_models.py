"""
Unit tests for Flask Project Manager models
"""

import pytest
from app import app, db
from models import Project, Task


@pytest.fixture
def app_context():
    """Create application context for model tests"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


class TestProjectModel:
    """Test suite for Project model"""
    
    def test_create_project(self, app_context):
        """Project should be created with correct attributes"""
        project = Project(name='Test Project', owner='owner@example.com')
        db.session.add(project)
        db.session.commit()
        
        assert project.id is not None
        assert project.name == 'Test Project'
        assert project.owner == 'owner@example.com'
    
    def test_project_has_tasks_relationship(self, app_context):
        """Project should have a relationship to tasks"""
        project = Project(name='Test Project', owner='owner@example.com')
        db.session.add(project)
        db.session.commit()
        
        task = Task(title='Test Task', project_id=project.id)
        db.session.add(task)
        db.session.commit()
        
        # Reload project and check relationship
        project = Project.query.get(project.id)
        assert len(project.tasks) == 1
        assert project.tasks[0].title == 'Test Task'
    
    def test_project_query_by_id(self, app_context):
        """Project should be queryable by ID"""
        project = Project(name='Test Project', owner='owner@example.com')
        db.session.add(project)
        db.session.commit()
        
        found_project = Project.query.get(project.id)
        assert found_project is not None
        assert found_project.name == 'Test Project'
    
    def test_project_query_all(self, app_context):
        """All projects should be queryable"""
        project1 = Project(name='Project 1', owner='owner1@example.com')
        project2 = Project(name='Project 2', owner='owner2@example.com')
        db.session.add(project1)
        db.session.add(project2)
        db.session.commit()
        
        projects = Project.query.all()
        assert len(projects) == 2


class TestTaskModel:
    """Test suite for Task model"""
    
    def test_create_task(self, app_context):
        """Task should be created with correct attributes"""
        project = Project(name='Test Project', owner='owner@example.com')
        db.session.add(project)
        db.session.commit()
        
        task = Task(title='Test Task', status='todo', project_id=project.id)
        db.session.add(task)
        db.session.commit()
        
        assert task.id is not None
        assert task.title == 'Test Task'
        assert task.status == 'todo'
        assert task.project_id == project.id
    
    def test_task_default_status(self, app_context):
        """Task should default to 'todo' status"""
        project = Project(name='Test Project', owner='owner@example.com')
        db.session.add(project)
        db.session.commit()
        
        task = Task(title='Test Task', project_id=project.id)
        db.session.add(task)
        db.session.commit()
        
        found_task = Task.query.get(task.id)
        assert found_task.status == 'todo'
    
    def test_task_belongs_to_project(self, app_context):
        """Task should belong to a project"""
        project = Project(name='Test Project', owner='owner@example.com')
        db.session.add(project)
        db.session.commit()
        
        task = Task(title='Test Task', project_id=project.id)
        db.session.add(task)
        db.session.commit()
        
        # Query task and verify project relationship
        found_task = Task.query.get(task.id)
        assert found_task.project is not None
        assert found_task.project.name == 'Test Project'
    
    def test_query_tasks_by_project(self, app_context):
        """Tasks should be queryable by project_id"""
        project1 = Project(name='Project 1', owner='owner1@example.com')
        project2 = Project(name='Project 2', owner='owner2@example.com')
        db.session.add(project1)
        db.session.add(project2)
        db.session.commit()
        
        task1 = Task(title='Task 1', project_id=project1.id)
        task2 = Task(title='Task 2', project_id=project1.id)
        task3 = Task(title='Task 3', project_id=project2.id)
        db.session.add_all([task1, task2, task3])
        db.session.commit()
        
        # Query tasks for project1
        project1_tasks = Task.query.filter_by(project_id=project1.id).all()
        assert len(project1_tasks) == 2
        
        # Query tasks for project2
        project2_tasks = Task.query.filter_by(project_id=project2.id).all()
        assert len(project2_tasks) == 1


class TestModelValidation:
    """Test suite for model validation"""
    
    def test_project_name_not_nullable(self, app_context):
        """Project name should not be nullable"""
        project = Project(name=None, owner='owner@example.com')
        db.session.add(project)
        
        with pytest.raises(Exception):  # Should raise IntegrityError or similar
            db.session.commit()
    
    def test_project_owner_not_nullable(self, app_context):
        """Project owner should not be nullable"""
        project = Project(name='Test Project', owner=None)
        db.session.add(project)
        
        with pytest.raises(Exception):  # Should raise IntegrityError or similar
            db.session.commit()
    
    def test_task_title_not_nullable(self, app_context):
        """Task title should not be nullable"""
        project = Project(name='Test Project', owner='owner@example.com')
        db.session.add(project)
        db.session.commit()
        
        task = Task(title=None, project_id=project.id)
        db.session.add(task)
        
        with pytest.raises(Exception):  # Should raise IntegrityError or similar
            db.session.commit()
    
    def test_task_project_id_not_nullable(self, app_context):
        """Task project_id should not be nullable"""
        task = Task(title='Test Task', project_id=None)
        db.session.add(task)
        
        with pytest.raises(Exception):  # Should raise IntegrityError or similar
            db.session.commit()


class TestTableNames:
    """Test suite for database table names"""
    
    def test_project_table_name(self, app_context):
        """Project table should be named 'projects'"""
        assert Project.__tablename__ == 'projects'
    
    def test_task_table_name(self, app_context):
        """Task table should be named 'tasks'"""
        assert Task.__tablename__ == 'tasks'
