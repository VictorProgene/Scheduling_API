from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.models import User


class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: datetime
    end_time: datetime
    status: str = Field(default="pending")  # Ex: "pending", "confirmed", "cancelled"

    # Chaves estrangeiras (ligação com o usuário)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="appointments")