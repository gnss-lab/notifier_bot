import os.path

import pytest
from fastapi.testclient import TestClient
from fast_api.main import app, db

from lib.db_create import LockableSqliteConnection

@pytest.fixture(scope="session", autouse=True)
def before_tests():
    DB_FOLDER = "../databases"
    DB_NAME = "test.db"

    db_path = os.path.join(os.path.normpath(DB_FOLDER), DB_NAME)
    if os.path.isfile(db_path):
        os.remove(db_path)

    lsc = LockableSqliteConnection(DB_FOLDER, DB_NAME)
    db.set_lsc(lsc)

client = TestClient(app)

def test_root():
    assert client.get("/").status_code == 200


def test_register():
    response = client.post(
        "/register",
        headers={'Content-Type': 'application/json'},
        json={"email": "test@mail.ru", "username": "user", "password": "123"},
    )
    assert response.status_code == 200, response.text
    rj = response.json()
    assert rj["email"] == "test@mail.ru"
    assert rj["username"] == "user"
    assert "id" in rj

def test_success_login():
    response = client.post(
        "/register",
        headers={'Content-Type': 'application/json'},
        json={"email": "test@mail.ru", "username": "user2", "password": "123"},
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "/login",
        headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'username':'user2','password':'123'},
    )

    assert response.status_code == 200, response.text
    rj = response.json()
    assert rj["token_type"] == "bearer"
    assert "access_token" in rj

def test_fail_login():
    response = client.post(
        "/register",
        headers={'Content-Type': 'application/json'},
        json={"email": "test@mail.ru", "username": "user3", "password": "123"},
    )
    assert response.status_code == 200, response.text

    response = client.post(
        "/login",
        headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'username':'user3','password':'1'},
    )

    assert response.status_code == 401, response.text
    rj = response.json()
    assert "detail" in rj

def test_fail_login2():
    response = client.post(
        "/login",
        headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'username':'user3.0','password':'123'},
    )
    assert response.status_code == 401, response.text
    rj = response.json()
    assert "detail" in rj

@pytest.fixture
def token():
    response = client.post(
        "/register",
        headers={'Content-Type': 'application/json'},
        json={"email": "test@mail.ru", "username": "test-user", "password": "111"},
    )

    response = client.post(
        "/login",
        headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={"username": "test-user", "password": "111"},
    )
    return f"Bearer {response.json()['access_token']}"

def test_fake_token():
    response = client.get(
        "/fastapi-users/me/",
        headers={'Content-Type': 'application/json',
                 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmb29sMTIzIiwiZXhwIjoxNjk0NTk0NDg4fQ.FNKH8yE6Y-MyhZ3ihaKnXcUrvJLMooB3s-aO9x2QrsM'},
    )
    assert response.status_code == 401, response.text

def test_read_users_me_success(token):
    response = client.get(
        "/fastapi-users/me/",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
    )
    assert response.status_code == 200, response.text

def test_add_user_success(token):
    params = {"user_id": 1234567}
    response = client.get(
        "/user/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert response.json()["user_id"] == params["user_id"]

def test_add_user_fail(token):
    response = client.get(
        "/user/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params={"user_id": "22"}
    )
    assert response.status_code == 200, response.text

    response = client.get(
        "/user/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params={"user_id": "22"}
    )
    assert response.status_code == 400, response.text

def test_add_subscription_success(token):
    params = {"sub_name": "Test_sub1",
              "sub_description": "Test_description"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert "sub_id" in response.json()

def test_subscribe_success(token):
    response = client.get(
        "/fastapi-users/me/",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "id" in j
    user_id = j["id"]

    params = {"sub_name": "Test_sub2",
              "sub_description": "Test_description2"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"sub_id": sub_id,
              "user_id": user_id}
    response = client.get(
        "/subscribe",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert "usub_id" in response.json()

def test_unsubscribe(token):
    response = client.get(
        "/fastapi-users/me/",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "id" in j
    user_id = j["id"]

    params = {"sub_name": "Test_sub2.1",
              "sub_description": "Test_description2.1"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"sub_id": sub_id,
              "user_id": user_id}
    response = client.get(
        "/subscribe",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert "usub_id" in response.json()

    response = client.get(
        "/subscribe",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "usub_id" in j
    usub_id = j["usub_id"]

    response = client.get(
        "/unsubscribe",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert "sub_id" in response.json()

    response = client.get(
        "/users_subscriptions/get",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
    )
    assert response.status_code == 200, response.text
    ids = set(map(lambda x:x[0],response.json()))
    assert usub_id not in ids

def test_send_notification_by_id(token):
    params = {"sub_name": "Test_sub3",
              "sub_description": "Test_description3"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"sub_id": sub_id,
              "message": "Test notification1"}
    response = client.get(
        "/send_notification_by_id",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert "notif_id" in response.json()

def test_send_notification_by_id_fail(token):
    params = {"sub_id": 242424,
              "message": "Test notification1"}
    response = client.get(
        "/send_notification_by_id",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 400, response.text

def test_send_notification_by_name(token):
    params = {"sub_name": "Test_sub3",
              "sub_description": "Test_description3"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j

    params = {"sub_name": params["sub_name"],
              "message": "Test notification2"}
    response = client.get(
        "/send_notification_by_name",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert "notif_id" in response.json()

def test_send_notification_by_name_fail(token):

    params = {"sub_name": "foo_bar_baz_bad_name",
              "message": "f"}
    response = client.get(
        "/send_notification_by_name",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 400, response.text

def test_monitored_service_add_success(token):
    params = {"sub_name": "Test_sub4",
              "sub_description": "Test_description4"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"error_message": "Something went wrong",
              "sub_id": sub_id,
              "url": "https://ya.ru",
              "crontab": "* * * * *"}
    response = client.get(
        "/monitored_service/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert "ser_id" in response.json()

def test_monitored_service_add_fail(token):
    params = {"sub_name": "Test_sub5",
              "sub_description": "Test_description5"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"error_message": "Something went wrong",
              "sub_id": sub_id,
              "url": "https://ya.ru",
              "crontab": "30 0 0 2-1"}
    response = client.get(
        "/monitored_service/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 400, response.text
    assert "detail" in response.json()

def test_monitored_service_delete(token):
    params = {"sub_name": "Test_sub6",
              "sub_description": "Test_description6"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"error_message": "Something went wrong",
              "sub_id": sub_id,
              "url": "https://ya.ru",
              "crontab": "* * * * 2"}
    response = client.get(
        "/monitored_service/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "ser_id" in j
    ser_id = j["ser_id"]

    params = {"service_id": ser_id}
    response = client.get(
        "/monitored_service/delete",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text

    response = client.get(
            "/monitored_services/get",
            headers={
                'Content-Type': 'application/json',
                'Authorization': token}
    )
    assert response.status_code == 200, response.text
    for service in response.json():
        if service[0] == ser_id:
            assert service[8] == 1
            break

def test_monitored_service_update(token):
    params = {"sub_name": "Test_sub7",
              "sub_description": "Test_description7"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"error_message": "Something went wrong24",
              "sub_id": sub_id,
              "url": "https://ya.ru",
              "crontab": "* * * 2 2"}
    response = client.get(
        "/monitored_service/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "ser_id" in j
    ser_id = j["ser_id"]

    params = {"service_id": ser_id,
              "crontab": "* * 3 3 3"}
    response = client.get(
        "/monitored_service/update",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    assert response.json()["ser_id"] == ser_id

    response = client.get(
            "/monitored_service/get",
            headers={
                'Content-Type': 'application/json',
                'Authorization': token},
            params={"ser_id": ser_id}
    )
    assert response.status_code == 200, response.text
    service = response.json()
    assert service[0] == ser_id
    assert service[7] == 0
    assert service[5] == params["crontab"]

def test_monitored_service_update_fail(token):
    params = {"service_id": 242424,
              "crontab": "123 3 5-6 1 *"}
    response = client.get(
        "/monitored_service/update",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 400, response.text

def test_users_get(token):
    response = client.get(
        "/users/get",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token}
    )
    assert response.status_code == 200, response.text

def test_subscriptions_get(token):
    response = client.get(
        "/subscriptions/get",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token}
    )
    assert response.status_code == 200, response.text

def test_users_subscriptions_get(token):
    response = client.get(
        "/users_subscriptions/get",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token}
    )
    assert response.status_code == 200, response.text

def test_notifications_get(token):
    response = client.get(
        "/notifications/get",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token}
    )
    assert response.status_code == 200, response.text

def test_monitored_services_get(token):
    response = client.get(
        "/monitored_services/get",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token}
    )
    assert response.status_code == 200, response.text

def test_get_monitored_service_by_id(token):
    params = {"sub_name": "Test_sub8",
              "sub_description": "Test_description8"}
    response = client.get(
        "/subscription/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "sub_id" in j
    sub_id = j["sub_id"]

    params = {"error_message": "Something went wrong24",
              "sub_id": sub_id,
              "url": "https://ya.ru",
              "crontab": "* * * 2 2"}
    response = client.get(
        "/monitored_service/add",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params=params
    )
    assert response.status_code == 200, response.text
    j = response.json()
    assert "ser_id" in j
    ser_id = j["ser_id"]

    response = client.get(
        "/monitored_service/get",
        headers={
            'Content-Type': 'application/json',
            'Authorization': token},
        params={"ser_id": ser_id}
    )
    assert response.status_code == 200, response.text
    service = response.json()
    assert service[0] == ser_id
