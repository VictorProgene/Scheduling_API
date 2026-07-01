from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
# from app.models.appointment import Appointment
# from app.models.service import Service


class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)

    # Horário de trabalho básico (ex: 09:00 - 18:00)
    start_work_hour: int = Field(default=9)
    end_work_hour: int = Field(default=18)

    # Relação: Um profissional oferece vários serviços e tem vários agendamentos
    services: List["Service"] = Relationship(back_populates="provider")
    appointments: List["Appointment"] = Relationship(back_populates="provider")