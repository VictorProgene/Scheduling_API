"""
availability.py - Providers and Availability Query Endpoints

This file maps routes associated with the '/providers' prefix for professional management:
1. 'GET /' ➔ Lists all registered service providers in the database.
2. 'GET /{provider_id}/availability' ➔ Calculates and lists available time slots for a specific provider on a given date.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from datetime import date
from typing import List
from app.database.connection import get_session
from app.services.availability import get_available_slots
from app.schemas.provider import AvailabilityResponse, ProviderResponse, ProviderCreate
from app.models import Provider
from app.core.limiter import limiter

router = APIRouter()


@router.get("/", response_model=List[ProviderResponse])
def list_providers(db: Session = Depends(get_session)):
    # Query to fetch all registered providers
    providers = db.exec(select(Provider)).all()
    return providers


@router.get("/{provider_id}/availability", response_model=AvailabilityResponse)
@limiter.limit("5/minute")
def list_availability(
        provider_id: int,
        target_date: date,
        request: Request,
        db: Session = Depends(get_session)
):
    slots = get_available_slots(db, provider_id, target_date)

    if not slots:
        return {"provider_id": provider_id, "date": target_date, "available_slots": []}

    return {"provider_id": provider_id, "date": target_date, "available_slots": slots}


@router.post("/", response_model=ProviderResponse)
def create_provider(provider_data: ProviderCreate, db: Session = Depends(get_session)):
    # 1. Check if provider email is already registered
    existing = db.exec(select(Provider).where(Provider.email == provider_data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="This provider email is already registered.")
    
    # 2. Create and save the provider
    new_provider = Provider(**provider_data.model_dump())
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider