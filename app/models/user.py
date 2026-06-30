from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models import Appointment


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    password: str  # Lembre-se: em um sistema real, você sempre deve salvar o hash da senha!

    # Relação: Um usuário pode ter vários agendamentos
    appointments: List["Appointment"] = Relationship(back_populates="user")