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
    assert second_response.json()["detail"] == "Este horário já está ocupado."


def test_get_my_appointments(authenticated_client, sample_provider, sample_service):
    # 1. Cria um agendamento para o usuário autenticado (user_id = 1)
    authenticated_client.post(
        "/appointments/",
        json={
            "provider_id": sample_provider.id,
            "service_id": sample_service.id,
            "start_time": "2026-07-03T09:00:00",
        },
    )

    # 2. Chama o GET /appointments/me
    response = authenticated_client.get("/appointments/me")

    # 3. Validações
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == 1


def test_cancel_appointment_success(authenticated_client, db, sample_provider, sample_service):
    # 1. Insere um agendamento diretamente no banco pertencente ao usuário 1
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

    # 2. Executa a requisição de DELETE
    response = authenticated_client.delete(f"/appointments/{appointment.id}")

    # 3. Validações
    assert response.status_code == 200
    assert response.json()["detail"] == "Agendamento cancelado com sucesso."

    # Verifica se foi removido do banco
    appointment_id = appointment.id
    db.expire_all() # Limpa o cache da sessão de teste
    db_appointment = db.get(Appointment, appointment_id)
    assert db_appointment is None


def test_cancel_appointment_forbidden_for_other_user(authenticated_client, db, sample_provider, sample_service):
    # 1. Insere um agendamento pertencente ao usuário 2
    appointment = Appointment(
        provider_id=sample_provider.id,
        service_id=sample_service.id,
        user_id=2, # Outro usuário
        start_time=datetime(2026, 7, 3, 9, 0),
        end_time=datetime(2026, 7, 3, 10, 0),
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # 2. Tenta deletar usando a sessão do Usuário 1 (authenticated_client)
    response = authenticated_client.delete(f"/appointments/{appointment.id}")

    # 3. Validações (Deve retornar 403 Forbidden)
    assert response.status_code == 403
    assert response.json()["detail"] == "Você não tem permissão para cancelar este agendamento."

    # Garante que o agendamento NÃO foi excluído do banco
    db_appointment = db.get(Appointment, appointment.id)
    assert db_appointment is not None


def test_create_appointment_triggers_background_email(authenticated_client, db, sample_provider, sample_service, capsys):
    # 1. Cria o usuário com ID 1 no banco para bater com o mock do get_current_user
    user = User(id=1, name="Cliente Teste", email="cliente@example.com", password="hash_seguro")
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2. Faz o agendamento
    response = authenticated_client.post(
        "/appointments/",
        json={
            "provider_id": sample_provider.id,
            "service_id": sample_service.id,
            "start_time": "2026-07-03T09:00:00",
        },
    )

    assert response.status_code == 200

    # 3. Captura o que foi impresso (print) no terminal
    captured = capsys.readouterr()

    # 4. Valida se a nossa simulação de e-mail foi disparada
    assert "ENVIANDO E-MAIL DE CONFIRMAÇÃO" in captured.out
    assert "cliente@example.com" in captured.out
    assert sample_provider.name in captured.out
