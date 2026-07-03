from datetime import date, datetime

from app.models import Appointment


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
