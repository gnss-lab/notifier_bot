import os.path

import pytest
from fastapi.testclient import TestClient
from fast_api.main import app, db

from fast_api.src.models import Token
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

def test_read_users_me_fail():
    response = client.get(
        "/fastapi-users/me/",
        headers={'Content-Type': 'application/json'},
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