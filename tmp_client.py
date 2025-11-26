import requests
import json
payload={'name':'X_ve','owner_email':'unique@example.com'}
print('Sending', json.dumps(payload))
resp=requests.post('http://127.0.0.1:5000/projects', json=payload)
print('Status', resp.status_code)
print('Response', resp.text)
