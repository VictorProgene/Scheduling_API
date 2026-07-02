from sqlmodel import SQLModel
from uuid import UUID

class ServiceCreate(SQLModel):
    provider_id: int
    name: str
    duration_minutes: int
    price: float

class ServiceResponse(ServiceCreate):
    id: int