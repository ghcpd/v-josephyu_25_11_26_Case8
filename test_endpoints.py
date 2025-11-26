import requests
import time

# Give the server a moment to start if just launched
time.sleep(1)

print("=" * 60)
print("TEST 1: Create project with README payload (owner_email)")
print("=" * 60)
payload = {
    "name": "Sample Project",
    "owner_email": "lead@example.com"
}
try:
    response = requests.post("http://127.0.0.1:5000/projects", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("TEST 2: Create project with correct payload (owner)")
print("=" * 60)
payload = {
    "name": "Sample Project",
    "owner": "lead@example.com"
}
try:
    response = requests.post("http://127.0.0.1:5000/projects", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("TEST 3: List projects")
print("=" * 60)
try:
    response = requests.get("http://127.0.0.1:5000/projects")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("TEST 4: List tasks for project 1 (README endpoint /api/projects/1/tasks)")
print("=" * 60)
try:
    response = requests.get("http://127.0.0.1:5000/api/projects/1/tasks")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("TEST 5: List tasks for project 1 (correct endpoint /projects/1/tasks)")
print("=" * 60)
try:
    response = requests.get("http://127.0.0.1:5000/projects/1/tasks")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("TEST 6: Health check")
print("=" * 60)
try:
    response = requests.get("http://127.0.0.1:5000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
