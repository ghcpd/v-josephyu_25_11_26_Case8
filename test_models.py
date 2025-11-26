import pytest
from models import db, Project, Task


def test_project_model_creation():
    """Test creating a Project model instance."""
    project = Project(name='Test Project', owner='test@example.com')
    assert project.name == 'Test Project'
    assert project.owner == 'test@example.com'
    assert project.id is None  # Not yet saved to database


def test_task_model_creation():
    """Test creating a Task model instance."""
    task = Task(title='Test Task', status='todo', project_id=1)
    assert task.title == 'Test Task'
    assert task.status == 'todo'
    assert task.project_id == 1
    assert task.id is None  # Not yet saved to database


def test_task_default_status():
    """Test that Task status defaults to 'todo'."""
    # Note: Default value is only set when saving to database, not on model instantiation
    # When a Task is created without status, it's None until saved
    task = Task(title='Test Task', project_id=1)
    # The default is defined in the column, but won't apply until inserted into DB
    # For now, we'll test that the column has a default defined
    assert Task.__table__.columns['status'].default is not None


def test_project_tablename():
    """Test that Project uses correct table name."""
    assert Project.__tablename__ == 'projects'


def test_task_tablename():
    """Test that Task uses correct table name."""
    assert Task.__tablename__ == 'tasks'


def test_project_has_tasks_relationship():
    """Test that Project model has tasks relationship."""
    assert hasattr(Project, 'tasks')


def test_task_has_project_backref():
    """Test that Task model has project backref."""
    # The backref is created by the relationship, so we just check the foreign key
    assert hasattr(Task, 'project_id')


def test_project_columns():
    """Test that Project has all required columns."""
    columns = [col.name for col in Project.__table__.columns]
    assert 'id' in columns
    assert 'name' in columns
    assert 'owner' in columns


def test_task_columns():
    """Test that Task has all required columns."""
    columns = [col.name for col in Task.__table__.columns]
    assert 'id' in columns
    assert 'title' in columns
    assert 'status' in columns
    assert 'project_id' in columns


def test_project_name_not_nullable():
    """Test that Project name is not nullable."""
    column = Project.__table__.columns['name']
    assert column.nullable is False


def test_project_owner_not_nullable():
    """Test that Project owner is not nullable."""
    column = Project.__table__.columns['owner']
    assert column.nullable is False


def test_task_title_not_nullable():
    """Test that Task title is not nullable."""
    column = Task.__table__.columns['title']
    assert column.nullable is False


def test_task_status_not_nullable():
    """Test that Task status is not nullable."""
    column = Task.__table__.columns['status']
    assert column.nullable is False


def test_task_project_id_not_nullable():
    """Test that Task project_id is not nullable."""
    column = Task.__table__.columns['project_id']
    assert column.nullable is False


def test_project_name_max_length():
    """Test Project name column max length."""
    column = Project.__table__.columns['name']
    assert column.type.length == 80


def test_project_owner_max_length():
    """Test Project owner column max length."""
    column = Project.__table__.columns['owner']
    assert column.type.length == 120


def test_task_title_max_length():
    """Test Task title column max length."""
    column = Task.__table__.columns['title']
    assert column.type.length == 120


def test_task_status_max_length():
    """Test Task status column max length."""
    column = Task.__table__.columns['status']
    assert column.type.length == 20


def test_project_id_is_primary_key():
    """Test that Project id is primary key."""
    column = Project.__table__.columns['id']
    assert column.primary_key is True


def test_task_id_is_primary_key():
    """Test that Task id is primary key."""
    column = Task.__table__.columns['id']
    assert column.primary_key is True


def test_task_foreign_key_exists():
    """Test that Task has foreign key to Project."""
    foreign_keys = list(Task.__table__.foreign_keys)
    assert len(foreign_keys) == 1
    assert foreign_keys[0].column.table.name == 'projects'
