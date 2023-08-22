from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from src.models import Token

client = TestClient(app)

def test_root():
    assert client.get("/").status_code == 200
