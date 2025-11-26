"""
Simple client example to create a project as per tutorial.
"""
import requests

payload = {"name": "Sample Project", "owner": "lead@example.com"}
resp = requests.post("http://127.0.0.1:5000/projects", json=payload)
print(resp.status_code)
print(resp.json())
