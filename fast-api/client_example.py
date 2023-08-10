import time

import requests

url = "http://127.0.0.1:8000"

session = requests.Session()
r = session.post(f"{url}/login", data={"username": "user", "password": "123"})
js = r.json()
session.headers.update({"Authorization": f"Bearer {js['access_token']}", "Accept": "application/json"})

def send_notif(message):
    r = session.get(f"{url}/send_notification_by_id", params={"message": message, "sub_id": 1})
    print(r.status_code)
    print(r.text)

for j in range(10):
    for i in range(10):
        send_notif(f"Test message {i}")
    time.sleep(1)