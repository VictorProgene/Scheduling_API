from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import date
from typing import List
from app.database.connection import get_session
from app.services.availability import get_available_slots

router = APIRouter()


@router.get("/{provider_id}/availability")
def list_availability(
        provider_id: int,
        target_date: date,
        db: Session = Depends(get_session)
):
    slots = get_available_slots(db, provider_id, target_date)

    if not slots:
        return {"provider_id": provider_id, "date": target_date, "available_slots": []}

    return {"provider_id": provider_id, "date": target_date, "available_slots": slots}