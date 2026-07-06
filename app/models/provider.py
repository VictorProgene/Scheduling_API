"""
provider.py - Modelo ORM físico para a tabela de Prestadores de Serviços (Profissionais)

Este arquivo define a estrutura da tabela de dados 'provider' no banco de dados.
Campos:
- id: Chave primária autoincremental.
- name: Nome do profissional.
- email: E-mail de contato do profissional.
- start_work_hour: Hora de início do expediente (inteiro, ex: 9).
- end_work_hour: Hora de término do expediente (inteiro, ex: 18).
Relacionamentos:
- appointments: Lista de agendamentos agendados para este profissional.
- services: Lista de serviços oferecidos por este profissional.
"""

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
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # Relações
    services: list["Service"] = Relationship(back_populates="provider")
    appointments: list["Appointment"] = Relationship(back_populates="provider")
