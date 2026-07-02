from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.appointment import Appointment
from datetime import timedelta

def create_appointment(db: Session, appointment_data: Appointment):
    # 1. Verifica se já existe um agendamento conflitando no mesmo horário
    conflict = db.exec(
        select(Appointment).where(
            Appointment.provider_id == appointment_data.provider_id,
            Appointment.start_time < appointment_data.end_time,
            Appointment.end_time > appointment_data.start_time
        )
    ).first()

    if conflict:
        raise HTTPException(status_code=400, detail="Este horário já está ocupado.")

    # 2. Adiciona o agendamento ao banco
    db.add(appointment_data)
    db.commit() # Confirma a transação
    db.refresh(appointment_data)
    return appointment_data