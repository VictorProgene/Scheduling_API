import pytest
from app.models import Provider, Service

def test_create_provider_success(client):
    # 1. Envia requisição para criar um profissional
    response = client.post(
        "/providers/",
        json={
            "name": "Professional Novo",
            "email": "novo@provider.com",
            "start_work_hour": 8,
            "end_work_hour": 17
        }
    )

    # 2. Validações
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Professional Novo"
    assert data["email"] == "novo@provider.com"
    assert "id" in data

def test_create_provider_duplicate_email(client, db):
    # 1. Cria um profissional no banco
    existing_provider = Provider(
        name="Existente",
        email="duplicado@provider.com",
        start_work_hour=9,
        end_work_hour=18
    )
    db.add(existing_provider)
    db.commit()

    # 2. Tenta criar outro com o mesmo e-mail
    response = client.post(
        "/providers/",
        json={
            "name": "Outro",
            "email": "duplicado@provider.com",
            "start_work_hour": 8,
            "end_work_hour": 17
        }
    )

    # 3. Validações (Deve retornar 400 Bad Request)
    assert response.status_code == 400
    assert response.json()["detail"] == "Este e-mail de profissional já está cadastrado."

def test_create_service_success(client, db, sample_provider):
    # 1. Cria um serviço para o provider de teste
    response = client.post(
        "/services/",
        json={
            "provider_id": sample_provider.id,
            "name": "Servico Novo",
            "description": "Descricao do servico",
            "duration_minutes": 45,
            "price": 80.0
        }
    )

    # 2. Validações
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Servico Novo"
    assert data["provider_id"] == sample_provider.id
    assert "id" in data

def test_create_service_provider_not_found(client):
    # 1. Tenta criar um serviço para um provider inexistente (ID 999)
    response = client.post(
        "/services/",
        json={
            "provider_id": 999,
            "name": "Servico Fantasma",
            "description": "Nao existe",
            "duration_minutes": 30,
            "price": 40.0
        }
    )

    # 2. Validações (Deve retornar 404 Not Found)
    assert response.status_code == 404
    assert response.json()["detail"] == "Profissional (provider_id) não encontrado."
