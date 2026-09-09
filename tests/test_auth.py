import pytest
from fastapi.testclient import TestClient

def test_register_success(client):
    response = client.post("/api/register", json={"username": "alice", "password": "secret123"})
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

def test_register_duplicate(client):
    # 先注册一个用户，再尝试用相同用户名注册，应返回 400
    client.post("/api/register", json={"username": "alice", "password": "secret123"})
    response = client.post("/api/register", json={"username": "alice", "password": "secret123"})
    assert response.status_code == 400

def test_login_success(client):
    # 先注册，再登录
    client.post("/api/register", json={"username": "alice", "password": "secret123"})
    response = client.post("/api/token", data={"username": "alice", "password": "secret123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    # 先注册，再用错误密码登录
    client.post("/api/register", json={"username": "alice", "password": "secret123"})
    response = client.post("/api/token", data={"username": "alice", "password": "wrongpass"})
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    # 不注册，直接尝试登录不存在用户
    response = client.post("/api/token", data={"username": "ghost", "password": "whatever"})
    assert response.status_code == 401