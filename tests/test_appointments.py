"""
test_appointments.py - Integration Tests for Appointment Route (Appointments)

This file validates business rules related to time slot bookings:
1. Route protection (require login token).
2. Creation of valid appointments and validation of busy time slot conflicts.
3. Exclusive listing of appointments belonging to the authenticated client (ownership).
4. Secure cancellation with validation of appointment ownership (blocked for other users).
5. Asynchronous dispatch of confirmation emails in the background (BackgroundTasks).
"""

from datetime import datetime
from app.models import Appointment, User

def test_create_appointment_requires_authentication(client, sample_provider, sample_service):
    response = client.post(
        "/appointments/",
        json={
            "provider_id": sample_provider.id,
            "service_id": sample_service.id,
            "start_time": "2026-07-03T09:00:00",
        },
    )

    assert response.status_code == 401


def test_create_appointment_authenticated(authenticated_client, sample_provider, sample_service):
    response = authenticated_client.post(
        "/appointments/",
        json={
            "provider_id": sample_provider.id,
            "service_id": sample_service.id,
            "start_time": "2026-07-03T09:00:00",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["provider_id"] == sample_provider.id
    assert data["service_id"] == sample_service.id
    assert data["user_id"] == 1
    assert data["status"] == "pending"
    assert data["end_time"] == "2026-07-03T10:00:00"


def test_create_appointment_rejects_conflicting_time(authenticated_client, sample_provider, sample_service):
    payload = {
        "provider_id": sample_provider.id,
        "service_id": sample_service.id,
        "start_time": "2026-07-03T09:00:00",
    }

    first_response = authenticated_client.post("/appointments/", json=payload)
    second_response = authenticated_client.post("/appointments/", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "This time slot is already booked."


def test_get_my_appointments(authenticated_client, sample_provider, sample_service):
    # 1. Create an appointment for the authenticated user (user_id = 1)
    authenticated_client.post(
        "/appointments/",
        json={
            "provider_id": sample_provider.id,
            "service_id": sample_service.id,
            "start_time": "2026-07-03T09:00:00",
        },
    )

    # 2. Call GET /appointments/me
    response = authenticated_client.get("/appointments/me")

    # 3. Validations
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == 1


def test_cancel_appointment_success(authenticated_client, db, sample_provider, sample_service):
    # 1. Insert an appointment directly into the database owned by user 1
    appointment = Appointment(
        provider_id=sample_provider.id,
        service_id=sample_service.id,
        user_id=1,
        start_time=datetime(2026, 7, 3, 9, 0),
        end_time=datetime(2026, 7, 3, 10, 0),
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # 2. Execute DELETE request
    response = authenticated_client.delete(f"/appointments/{appointment.id}")

    # 3. Validations
    assert response.status_code == 200
    assert response.json()["detail"] == "Appointment successfully canceled."

    # Check if it was removed from the database
    appointment_id = appointment.id
    db.expire_all()  # Clear test session cache
    db_appointment = db.get(Appointment, appointment_id)
    assert db_appointment is None


def test_cancel_appointment_forbidden_for_other_user(authenticated_client, db, sample_provider, sample_service):
    # 1. Insert an appointment owned by user 2
    appointment = Appointment(
        provider_id=sample_provider.id,
        service_id=sample_service.id,
        user_id=2,  # Another user
        start_time=datetime(2026, 7, 3, 9, 0),
        end_time=datetime(2026, 7, 3, 10, 0),
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # 2. Try to delete using User 1's session (authenticated_client)
    response = authenticated_client.delete(f"/appointments/{appointment.id}")

    # 3. Validations (Should return 403 Forbidden)
    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to cancel this appointment."

    # Ensure the appointment was NOT deleted from the database
    db_appointment = db.get(Appointment, appointment.id)
    assert db_appointment is not None


def test_create_appointment_triggers_background_email(authenticated_client, db, sample_provider, sample_service, capsys):
    # 1. Create user with ID 1 in the database to match get_current_user mock
    user = User(id=1, name="Test Client", email="client@example.com", password="secure_hash")
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2. Book appointment
    response = authenticated_client.post(
        "/appointments/",
        json={
            "provider_id": sample_provider.id,
            "service_id": sample_service.id,
            "start_time": "2026-07-03T09:00:00",
        },
    )

    assert response.status_code == 200

    # 3. Capture terminal prints (stdout)
    captured = capsys.readouterr()

    # 4. Validate if our simulated email notification was triggered
    assert "SENDING CONFIRMATION EMAIL" in captured.out
    assert "client@example.com" in captured.out
    assert sample_provider.name in captured.out
