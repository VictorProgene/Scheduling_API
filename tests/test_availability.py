"""
test_availability.py - Integration Tests for Availability and Providers Routes

This file validates schedule querying and provider listing rules:
1. Schedule query for non-existent provider (expects empty list).
2. Generation of free slots and exclusion of times when the provider is busy.
3. Listing of all registered providers.
4. Validation of request rate limiting (Rate Limiting).
"""

from datetime import date, datetime

from app.models import Appointment
from app.core.limiter import limiter


def test_availability_returns_empty_list_for_missing_provider(client):
    response = client.get("/providers/999/availability", params={"target_date": "2026-07-03"})

    assert response.status_code == 200
    assert response.json() == {
        "provider_id": 999,
        "date": "2026-07-03",
        "available_slots": [],
    }


def test_availability_lists_work_hours_and_skips_busy_slot(client, db, sample_provider, sample_service):
    busy_appointment = Appointment(
        provider_id=sample_provider.id,
        service_id=sample_service.id,
        user_id=1,
        start_time=datetime(2026, 7, 3, 10, 0),
        end_time=datetime(2026, 7, 3, 11, 0),
    )
    db.add(busy_appointment)
    db.commit()

    response = client.get(
        f"/providers/{sample_provider.id}/availability",
        params={"target_date": date(2026, 7, 3).isoformat()},
    )

    assert response.status_code == 200
    assert response.json()["available_slots"] == [
        "2026-07-03T09:00:00",
        "2026-07-03T11:00:00",
    ]


def test_list_providers_returns_all_registered_providers(client, sample_provider):
    # Send GET request to list providers
    response = client.get("/providers/")

    # Validations
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_provider.name
    assert data[0]["id"] == sample_provider.id


def test_availability_rate_limiting(client, sample_provider):
    limiter.reset()  # Reset the counter to isolate the test
    # 1. Make 5 quick requests (limit is 5 per minute)
    for _ in range(5):
        response = client.get(
            f"/providers/{sample_provider.id}/availability",
            params={"target_date": "2026-07-03"},
        )
        assert response.status_code == 200

    # 2. The 6th request should exceed the limit and return 429 Too Many Requests
    response = client.get(
        f"/providers/{sample_provider.id}/availability",
        params={"target_date": "2026-07-03"},
    )
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["error"]
