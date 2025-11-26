"""
Small example script (not a pytest test) to show the tutorial HTTP flow. Requires the server to be running.
"""
import requests


def run_example():
    payload = {"name": "Sample Project", "owner_email": "lead@example.com"}
    r = requests.post("http://127.0.0.1:5000/projects", json=payload)
    print(r.status_code, r.json())


if __name__ == "__main__":
    run_example()
