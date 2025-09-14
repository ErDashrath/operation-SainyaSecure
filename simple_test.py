import requests
import json

try:
    response = requests.get('http://127.0.0.1:8000/p2p_sync/api/status/', timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")