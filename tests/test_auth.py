"""
test_auth.py - Testes de Integração para Rota de Autenticação (Login e Registro)

Este arquivo valida as regras de segurança e acesso do usuário:
1. Cadastro de novos usuários (com sucesso e impedindo e-mails duplicados).
2. Login com sucesso (emissão de token JWT) e falha com credenciais incorretas.
"""

from app.core.limiter import limiter

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


def test_login_rate_limiting(client):
    limiter.reset()  # Reseta o contador para isolar o teste
    # 1. Faz 5 tentativas rápidas (limite é 5 por minuto)
    for _ in range(5):
        response = client.post(
            "/login",
            data={"username": "fake@example.com", "password": "any"},
        )
        assert response.status_code == 401

    # 2. A 6ª tentativa deve exceder o limite e retornar 429 Too Many Requests
    response = client.post(
        "/login",
        data={"username": "fake@example.com", "password": "any"},
    )
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["error"]
