"""
appointment.py - Business Rules for Appointment Creation

This file in the Service layer contains the core business logic for creating appointments.
Responsibilities:
1. Execute mathematical validation of time interval intersections to avoid scheduling conflicts.
2. Persist the new appointment atomically in the database.
"""

from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.appointment import Appointment
from datetime import timedelta

def create_appointment(db: Session, appointment_data: Appointment):
    # 1. Check if there is already a conflicting appointment at the same time
    conflict = db.exec(
        select(Appointment).where(
            Appointment.provider_id == appointment_data.provider_id,
            Appointment.start_time < appointment_data.end_time,
            Appointment.end_time > appointment_data.start_time
        )
    ).first()

    if conflict:
        raise HTTPException(status_code=400, detail="This time slot is already booked.")

    # 2. Add the appointment to the database
    db.add(appointment_data)
    db.commit()  # Commit the transaction
    db.refresh(appointment_data)
    return appointment_data