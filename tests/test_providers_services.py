"""
test_providers_services.py - Integration Tests for Providers and Services Registration

This file validates administrative routes created for catalog control:
1. Registration of service providers with data validation and prevention of duplicate emails.
2. Registration of new types of services linked to existing service providers.
3. Database integrity validation (e.g., prevent creating a service for a non-existent provider).
"""

import pytest
from app.models import Provider, Service

def test_create_provider_success(client):
    # 1. Send request to create a provider
    response = client.post(
        "/providers/",
        json={
            "name": "New Provider",
            "email": "new@provider.com",
            "start_work_hour": 8,
            "end_work_hour": 17
        }
    )

    # 2. Validations
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Provider"
    assert data["email"] == "new@provider.com"
    assert "id" in data

def test_create_provider_duplicate_email(client, db):
    # 1. Create a provider in the database
    existing_provider = Provider(
        name="Existing Provider",
        email="duplicate@provider.com",
        start_work_hour=9,
        end_work_hour=18
    )
    db.add(existing_provider)
    db.commit()

    # 2. Try to create another with the same email
    response = client.post(
        "/providers/",
        json={
            "name": "Other Provider",
            "email": "duplicate@provider.com",
            "start_work_hour": 8,
            "end_work_hour": 17
        }
    )

    # 3. Validations (Should return 400 Bad Request)
    assert response.status_code == 400
    assert response.json()["detail"] == "This provider email is already registered."

def test_create_service_success(client, db, sample_provider):
    # 1. Create a service for the test provider
    response = client.post(
        "/services/",
        json={
            "provider_id": sample_provider.id,
            "name": "New Service",
            "description": "Service description",
            "duration_minutes": 45,
            "price": 80.0
        }
    )

    # 2. Validations
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Service"
    assert data["provider_id"] == sample_provider.id
    assert "id" in data

def test_create_service_provider_not_found(client):
    # 1. Try to create a service for a non-existent provider (ID 999)
    response = client.post(
        "/services/",
        json={
            "provider_id": 999,
            "name": "Ghost Service",
            "description": "Does not exist",
            "duration_minutes": 30,
            "price": 40.0
        }
    )

    # 2. Validations (Should return 404 Not Found)
    assert response.status_code == 404
    assert response.json()["detail"] == "Provider (provider_id) not found."
