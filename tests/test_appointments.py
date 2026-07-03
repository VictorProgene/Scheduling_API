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
    assert second_response.json()["detail"] == "Este hor\u00e1rio j\u00e1 est\u00e1 ocupado."
