"""
appointment.py - Modelo ORM físico para a tabela de Agendamentos (Compromissos)

Este arquivo define a estrutura da tabela de dados 'appointment' no banco de dados.
Campos:
- id: Chave primária autoincremental.
- start_time: Horário de início do agendamento (datetime).
- end_time: Horário estimado de encerramento do agendamento (datetime).
- status: Estado do agendamento (ex: "pending", "confirmed").
- user_id: ID do cliente dono do agendamento (chave estrangeira vinculada ao user).
- provider_id: ID do profissional prestador (chave estrangeira vinculada ao provider).
- service_id: ID do tipo de serviço contratado (chave estrangeira vinculada ao service).
Relacionamentos:
- user: Objeto do cliente associado.
- provider: Objeto do profissional prestador associado.
"""

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
    service_id: int = Field(foreign_key="service.id")

    # Relações que fecham o ciclo com User e Provider
    user: "User" = Relationship(back_populates="appointments")
    provider: "Provider" = Relationship(back_populates="appointments")
