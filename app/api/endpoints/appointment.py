from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.connection import get_session
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.models.appointment import Appointment
from app.services.appointment import create_appointment
from app.api.deps import get_current_user
from datetime import timedelta

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
def book_appointment(
    data: AppointmentCreate,
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
    return create_appointment(db, new_appointment)