import requests

url = "http://127.0.0.1:8000"

session = requests.Session()
r = session.post(f"{url}/login", data={"username": "user", "password": "123"})
js = r.json()
session.headers.update({"Authorization": f"Bearer {js['access_token']}", "Accept": "application/json"})

r = session.get(f"{url}/send_notification_by_id", params={"message": "Test message", "sub_id": 3})

print(r.status_code)
print(r.text)