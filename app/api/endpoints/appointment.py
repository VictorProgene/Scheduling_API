"""
appointment.py - Appointment Management Endpoints

This file exposes private routes (protected by JWT token) for appointment management:
1. 'POST /' ➔ Requests a new appointment. Performs data checks and enqueues asynchronous confirmation email delivery in the background.
2. 'GET /me' ➔ Lists all appointments belonging exclusively to the authenticated caller (ownership).
3. 'DELETE /{appointment_id}' ➔ Allows cancellation of a specific appointment, provided the logged-in user is the owner.
"""

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
    user_id: int = Depends(get_current_user),  # FastAPI blocks access if token is missing
    db: Session = Depends(get_session)
):
    # Here we calculate end_time (simple example)
    # In production, you would fetch duration_minutes from the Service
    new_appointment = Appointment(
        **data.model_dump(),
        end_time=data.start_time + timedelta(hours=1),
        user_id=user_id
    )
    saved_appointment = create_appointment(db, new_appointment)

    # Fetch client and provider info for the notification
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
    # Fetch only appointments belonging to the authenticated user
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
    # 1. Fetch appointment from database
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Appointment not found."
        )

    # 2. Security Validation: Is the logged-in user the owner of this appointment?
    if appointment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to cancel this appointment."
        )

    # 3. Delete from database
    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment successfully canceled."}