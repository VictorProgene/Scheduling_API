from sqlmodel import SQLModel
from uuid import UUID
from datetime import time

class ProviderCreate(SQLModel):
    name: str
    specialty: str
    start_work_time: time
    end_work_time: time

class ProviderResponse(ProviderCreate):
    id: int