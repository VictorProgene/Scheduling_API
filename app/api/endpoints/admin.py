"""
admin.py - Administration Control Endpoints

This file exposes private routes restricted to users with 'admin' privileges.
1. 'GET /appointments' ➔ Lists all appointments in the system with full details.
2. 'DELETE /appointments/{appointment_id}' ➔ Allows cancellation of any appointment.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database.connection import get_session
from app.api.deps import get_current_user
from app.models import User, Provider, Appointment, Service
from app.schemas.appointment import AdminAppointmentResponse

router = APIRouter()

def get_current_admin(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    user = db.get(User, user_id)
    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have administrative privileges."
        )
    return user

@router.get("/appointments", response_model=List[AdminAppointmentResponse])
def get_all_appointments(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_session)
):
    # Query all appointments and join User, Provider, and Service
    statement = (
        select(Appointment, User, Provider, Service)
        .join(User, Appointment.user_id == User.id)
        .join(Provider, Appointment.provider_id == Provider.id)
        .join(Service, Appointment.service_id == Service.id)
    )
    results = db.exec(statement).all()
    
    response = []
    for apt, user, provider, service in results:
        response.append(
            AdminAppointmentResponse(
                id=apt.id,
                start_time=apt.start_time,
                end_time=apt.end_time,
                status=apt.status,
                client_name=user.name,
                client_email=user.email,
                provider_name=provider.name,
                service_name=service.name,
                price=service.price
            )
        )
    return response

@router.delete("/appointments/{appointment_id}")
def admin_cancel_appointment(
    appointment_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_session)
):
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found."
        )
    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment successfully canceled by administrator."}
