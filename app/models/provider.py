from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.appointment import Appointment
    from app.models.service import Service


class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    start_work_hour: int = Field(default=9)
    end_work_hour: int = Field(default=18)

    # Relações
    services: list["Service"] = Relationship(back_populates="provider")
    appointments: list["Appointment"] = Relationship(back_populates="provider")
