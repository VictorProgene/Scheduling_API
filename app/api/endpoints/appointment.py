from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session, select
from app.database.connection import get_session
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.models.appointment import Appointment
from app.models import User, Provider
from app.services.appointment import create_appointment
from app.services.notification import send_appointment_email
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
def book_appointment(
    data: AppointmentCreate,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(get_current_user), # O FastAPI bloqueia o acesso se não houver token
    db: Session = Depends(get_session)
):
    # Aqui calculamos o end_time (simples exemplo)
    # Em produção, você buscaria a duration_minutes do Service
    new_appointment = Appointment(
        **data.model_dump(),
        end_time=data.start_time + timedelta(hours=1),
        user_id=user_id
    )
    saved_appointment = create_appointment(db, new_appointment)

    # Busca as informações do cliente e profissional para a notificação
    user = db.get(User, user_id)
    provider = db.get(Provider, data.provider_id)

    if user and provider:
        background_tasks.add_task(
            send_appointment_email,
            email_to=user.email,
            provider_name=provider.name,
            start_time=saved_appointment.start_time
        )

    return saved_appointment


@router.get("/me", response_model=List[AppointmentResponse])
def get_my_appointments(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    # Busca apenas os agendamentos pertencentes ao usuário autenticado
    appointments = db.exec(
        select(Appointment).where(Appointment.user_id == user_id)
    ).all()
    return appointments


@router.delete("/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    # 1. Busca o agendamento no banco
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Agendamento não encontrado."
        )

    # 2. Validação de Segurança: O usuário logado é dono deste agendamento?
    if appointment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para cancelar este agendamento."
        )

    # 3. Deleta do banco
    db.delete(appointment)
    db.commit()
    return {"detail": "Agendamento cancelado com sucesso."}