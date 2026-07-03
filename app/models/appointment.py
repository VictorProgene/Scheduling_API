from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.provider import Provider
    from app.models.user import User


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: datetime
    end_time: datetime
    status: str = Field(default="pending")

    user_id: int = Field(foreign_key="user.id")
    provider_id: int = Field(foreign_key="provider.id")

    # Relações que fecham o ciclo com User e Provider
    user: "User" = Relationship(back_populates="appointments")
    provider: "Provider" = Relationship(back_populates="appointments")
