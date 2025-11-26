"""
Tutorial verification script
This script follows the corrected_readme.md tutorial exactly to verify all steps work
"""

import requests
import time
import subprocess
import os
import signal
import sys

def test_tutorial():
    """Run the tutorial steps from corrected_readme.md"""
    
    print("=" * 70)
    print("TUTORIAL VERIFICATION - Flask Project Manager")
    print("=" * 70)
    
    # Give server a moment if it's already running
    time.sleep(1)
    
    # Test 1: Create a project
    print("\n[Tutorial Step 1] Creating a project...")
    payload = {
        "name": "Sample Project",
        "owner": "lead@example.com"
    }
    try:
        response = requests.post("http://127.0.0.1:5000/projects", json=payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        project_data = response.json()
        assert project_data['id'] == 1
        assert project_data['name'] == 'Sample Project'
        assert project_data['owner'] == 'lead@example.com'
        print("✓ Successfully created project")
        print(f"  Response: {project_data}")
        project_id = project_data['id']
    except Exception as e:
        print(f"✗ Failed to create project: {e}")
        return False
    
    # Test 2: List all projects
    print("\n[Tutorial Step 2] Listing all projects...")
    try:
        response = requests.get("http://127.0.0.1:5000/projects")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        projects = response.json()
        assert len(projects) >= 1, "Expected at least 1 project"
        print("✓ Successfully listed projects")
        print(f"  Response: {projects}")
    except Exception as e:
        print(f"✗ Failed to list projects: {e}")
        return False
    
    # Test 3: List tasks for a project
    print(f"\n[Tutorial Step 3] Listing tasks for project {project_id}...")
    try:
        response = requests.get(f"http://127.0.0.1:5000/projects/{project_id}/tasks")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        tasks = response.json()
        assert isinstance(tasks, list), "Expected response to be a list"
        print("✓ Successfully listed tasks")
        print(f"  Response: {tasks}")
    except Exception as e:
        print(f"✗ Failed to list tasks: {e}")
        return False
    
    # Test 4: Health check
    print("\n[Tutorial Step 4] Checking health endpoint...")
    try:
        response = requests.get("http://127.0.0.1:5000/health")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        health = response.json()
        assert health['status'] == 'ok'
        print("✓ Health check passed")
        print(f"  Response: {health}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False
    
    # Test 5: Verify incorrect endpoint returns 404
    print("\n[Tutorial Step 5] Verifying old endpoint returns 404...")
    try:
        response = requests.get(f"http://127.0.0.1:5000/api/projects/{project_id}/tasks")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        print("✓ Old endpoint correctly returns 404")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✓ ALL TUTORIAL STEPS PASSED!")
    print("=" * 70)
    return True

if __name__ == '__main__':
    success = test_tutorial()
    sys.exit(0 if success else 1)
