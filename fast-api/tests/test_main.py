from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app

from src.models import Token
from src.db_functions import *

createLockableSqliteConnection("../telegram-bot/databases", "test.db")

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

