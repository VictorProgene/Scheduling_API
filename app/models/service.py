from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models import Provider


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    duration_minutes: int  # Importante para calcular o end_time no agendamento

    # Chave estrangeira ligando ao profissional
    provider_id: int = Field(foreign_key="provider.id")
    provider: Provider = Relationship(back_populates="services")