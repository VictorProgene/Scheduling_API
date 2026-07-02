from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID

class AppointmentCreate(SQLModel):
    provider_id: UUID
    service_id: UUID
    start_time: datetime

class AppointmentResponse(AppointmentCreate):
    id: UUID
    user_id: UUID
    end_time: datetime
    status: str