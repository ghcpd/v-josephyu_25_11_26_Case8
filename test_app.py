import os
import pytest
from app import app, init_database


def test_init_database_missing_env_var():
    """Test that init_database raises error when DB_URL is not set."""
    # Save current env var if it exists
    original_db_url = os.environ.get('DB_URL')
    
    try:
        # Remove the env var
        if 'DB_URL' in os.environ:
            del os.environ['DB_URL']
        
        # Try to initialize a new app
        with pytest.raises(RuntimeError) as exc_info:
            from flask import Flask
            test_app = Flask(__name__)
            init_database(test_app)
        
        assert 'Missing DB_URL environment variable' in str(exc_info.value)
    
    finally:
        # Restore original env var
        if original_db_url:
            os.environ['DB_URL'] = original_db_url


def test_init_database_sets_config():
    """Test that init_database sets correct configuration."""
    original_db_url = os.environ.get('DB_URL')
    
    try:
        os.environ['DB_URL'] = 'sqlite:///:memory:'
        
        from flask import Flask
        test_app = Flask(__name__)
        init_database(test_app)
        
        assert test_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
        assert test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
    
    finally:
        if original_db_url:
            os.environ['DB_URL'] = original_db_url


def test_app_has_routes():
    """Test that app has all expected routes."""
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    
    assert '/health' in routes
    assert '/projects' in routes
    assert '/projects/<int:project_id>/tasks' in routes


def test_health_route_methods():
    """Test health route accepts only GET method."""
    rules = [rule for rule in app.url_map.iter_rules() if rule.rule == '/health']
    assert len(rules) == 1
    assert 'GET' in rules[0].methods


def test_projects_route_methods():
    """Test projects route accepts GET and POST methods."""
    rules = [rule for rule in app.url_map.iter_rules() if rule.rule == '/projects']
    # Flask creates separate rules for GET and POST when they have different handlers
    assert len(rules) >= 1
    methods = set()
    for rule in rules:
        methods.update(rule.methods)
    assert 'GET' in methods
    assert 'POST' in methods


def test_tasks_route_methods():
    """Test tasks route accepts only GET method."""
    rules = [rule for rule in app.url_map.iter_rules() 
             if '/tasks' in rule.rule]
    assert len(rules) == 1
    assert 'GET' in rules[0].methods


def test_app_name():
    """Test that app name is correct."""
    assert app.name == 'app'


def test_sqlalchemy_config():
    """Test SQLAlchemy configuration."""
    assert 'SQLALCHEMY_DATABASE_URI' in app.config
    assert 'SQLALCHEMY_TRACK_MODIFICATIONS' in app.config
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
