from sqlmodel import SQLModel
from uuid import UUID
from datetime import time, date, datetime
from typing import List

class ProviderCreate(SQLModel):
    name: str
    email: str
    start_work_hour: int
    end_work_hour: int

class ProviderResponse(ProviderCreate):
    id: int

class AvailabilityResponse(SQLModel):
    provider_id: int
    date: date
    available_slots: List[datetime]