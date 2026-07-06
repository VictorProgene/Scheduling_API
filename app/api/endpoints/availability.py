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
from app.models import Provider, User
from app.core.security import get_password_hash
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
    # 1. Check if provider email is already registered in Provider table or User table
    existing_provider = db.exec(select(Provider).where(Provider.email == provider_data.email)).first()
    if existing_provider:
        raise HTTPException(status_code=400, detail="This provider email is already registered.")
    
    existing_user = db.exec(select(User).where(User.email == provider_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="A user with this email is already registered.")
    
    # 2. Create and save corresponding login User
    provider_dict = provider_data.model_dump()
    password = provider_dict.pop("password", None) or "Barber123!"
    hashed_pw = get_password_hash(password)
    
    new_user = User(
        name=provider_data.name,
        email=provider_data.email,
        password=hashed_pw,
        role="provider"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 3. Create and save the provider linked to the new user
    new_provider = Provider(**provider_dict, user_id=new_user.id)
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider