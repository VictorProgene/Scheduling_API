from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date
from typing import List
from app.database.connection import get_session
from app.services.availability import get_available_slots
from app.schemas.provider import AvailabilityResponse, ProviderResponse
from app.models import Provider

router = APIRouter()


@router.get("/", response_model=List[ProviderResponse])
def list_providers(db: Session = Depends(get_session)):
    # Query para buscar todos os profissionais cadastrados
    providers = db.exec(select(Provider)).all()
    return providers


@router.get("/{provider_id}/availability", response_model=AvailabilityResponse)
def list_availability(
        provider_id: int,
        target_date: date,
        db: Session = Depends(get_session)
):
    slots = get_available_slots(db, provider_id, target_date)

    if not slots:
        return {"provider_id": provider_id, "date": target_date, "available_slots": []}

    return {"provider_id": provider_id, "date": target_date, "available_slots": slots}
