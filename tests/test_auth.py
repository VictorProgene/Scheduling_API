def test_register_creates_user(client):
    response = client.post(
        "/register",
        json={
            "name": "Usuario Teste",
            "email": "usuario@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Usuario Teste"
    assert data["email"] == "usuario@example.com"
    assert "id" in data
    assert "password" not in data


def test_register_rejects_duplicate_email(client):
    payload = {
        "name": "Usuario Teste",
        "email": "usuario@example.com",
        "password": "123456",
    }

    first_response = client.post("/register", json=payload)
    second_response = client.post("/register", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "E-mail j\u00e1 cadastrado"


def test_login_returns_access_token(client):
    client.post(
        "/register",
        json={
            "name": "Usuario Teste",
            "email": "usuario@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/login",
        data={"username": "usuario@example.com", "password": "123456"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_rejects_wrong_password(client):
    client.post(
        "/register",
        json={
            "name": "Usuario Teste",
            "email": "usuario@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/login",
        data={"username": "usuario@example.com", "password": "senha-errada"},
    )

    assert response.status_code == 401
