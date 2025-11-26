"""
Simple client example to list tasks for a project.
"""
import requests

resp = requests.get("http://127.0.0.1:5000/projects/1/tasks")
print(resp.status_code)
print(resp.json())
