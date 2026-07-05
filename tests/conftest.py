"""
conftest.py - Pytest Configuration and Global Fixtures

This file centralizes the automated testing environment configuration:
1. Creates a temporary in-memory SQLite engine to run tests isolated from production Postgres.
2. Defines reusable fixtures for tests (db session, HTTP client, sample provider, sample service).
3. Configures mocked dependencies (such as simulating login by returning a test user ID).
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.api.deps import get_current_user
from app.database.connection import get_session
from app.main import app
from app.models import Appointment, Provider, Service, User


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="db")
def db_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine):
    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(client):
    app.dependency_overrides[get_current_user] = lambda: 1
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def sample_provider(db):
    provider = Provider(
        name="Test Provider",
        email="provider@example.com",
        start_work_hour=9,
        end_work_hour=12,
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


@pytest.fixture
def sample_service(db, sample_provider):
    service = Service(
        name="Haircut",
        description="Test service",
        price=50.0,
        duration_minutes=60,
        provider_id=sample_provider.id,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service
