"""
test_auth.py - Integration Tests for Authentication Route (Login and Register)

This file validates user security and access rules:
1. Registration of new users (successful and preventing duplicate emails).
2. Successful login (issuing JWT token) and failure with incorrect credentials.
"""

from app.core.limiter import limiter

def test_register_creates_user(client):
    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "user@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "user@example.com"
    assert "id" in data
    assert "password" not in data


def test_register_rejects_duplicate_email(client):
    payload = {
        "name": "Test User",
        "email": "user@example.com",
        "password": "123456",
    }

    first_response = client.post("/register", json=payload)
    second_response = client.post("/register", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email already registered"


def test_login_returns_access_token(client):
    client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "user@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "123456"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_rejects_wrong_password(client):
    client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "user@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_login_rate_limiting(client):
    limiter.reset()  # Reset the counter to isolate the test
    # 1. Make 5 quick attempts (limit is 5 per minute)
    for _ in range(5):
        response = client.post(
            "/login",
            data={"username": "fake@example.com", "password": "any"},
        )
        assert response.status_code == 401

    # 2. The 6th attempt should exceed the limit and return 429 Too Many Requests
    response = client.post(
        "/login",
        data={"username": "fake@example.com", "password": "any"},
    )
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["error"]
