import pytest
from fastapi.testclient import TestClient

def get_token(client, username="alice", password="secret123"):
    response = client.post("/api/token", data={"username": username, "password": password})
    return response.json()["access_token"]

def create_user(client, username, password):
    client.post("/api/register", json={"username": username, "password": password})

def create_article(client, token, title="Test Article", content="This is a test.", tags=["python"]):
    return client.post(
        "/api/articles",
        json={"title": title, "content": content, "tags": tags},
        headers={"Authorization": f"Bearer {token}"}
    )

def test_create_article_unauthorized(client):
    response = client.post("/api/articles", json={"title": "No Auth", "content": "x"})
    assert response.status_code == 401

def test_create_article_success(client):
    create_user(client, "bob", "password123")
    token = get_token(client, "bob", "password123")
    response = create_article(client, token)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Article"

def test_create_article_missing_title(client):
    create_user(client, "bob", "password123")
    token = get_token(client, "bob", "password123")
    response = client.post(
        "/api/articles",
        json={"content": "No title"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422

def test_list_articles_pagination(client):
    response = client.get("/api/articles?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data and "total" in data

def test_update_article_unauthorized(client):
    # 创建两个用户，第一个用户创建文章，第二个用户尝试修改，应返回403
    create_user(client, "alice", "secret123")
    create_user(client, "bob", "password123")
    alice_token = get_token(client, "alice", "secret123")
    bob_token = get_token(client, "bob", "password123")
    art_resp = create_article(client, alice_token, title="Alice's Article")
    article_id = art_resp.json()["id"]
    response = client.put(
        f"/api/articles/{article_id}",
        json={"title": "Hacked"},
        headers={"Authorization": f"Bearer {bob_token}"}
    )
    assert response.status_code == 403

def test_delete_article_unauthorized(client):
    # 类似越权删除测试
    pass  # 可以补充