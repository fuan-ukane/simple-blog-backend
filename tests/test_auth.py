import pytest
from fastapi.testclient import TestClient

def test_register_success(client):
    response = client.post("/api/register", json={"username": "alice", "password": "secret123"})
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

def test_register_duplicate(client):
    response = client.post("/api/register", json={"username": "alice", "password": "secret123"})
    assert response.status_code == 400

def test_login_success(client):
    response = client.post("/api/token", data={"username": "alice", "password": "secret123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    response = client.post("/api/token", data={"username": "alice", "password": "wrong"})
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post("/api/token", data={"username": "ghost", "password": "whatever"})
    assert response.status_code == 401