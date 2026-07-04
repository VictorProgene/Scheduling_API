"""
service.py - Modelo ORM físico para a tabela de Serviços Oferecidos

Este arquivo define a estrutura da tabela de dados 'service' no banco de dados.
Campos:
- id: Chave primária autoincremental.
- name: Nome do serviço (ex: "Corte de Cabelo").
- description: Breve descrição informativa sobre o serviço.
- price: Valor monetário cobrado pelo serviço (float).
- duration_minutes: Duração estimada do serviço em minutos (inteiro).
- provider_id: ID do profissional que oferece este serviço (chave estrangeira vinculada ao provider).
Relacionamentos:
- provider: Instância do profissional dono deste serviço.
"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.provider import Provider


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    duration_minutes: int

    provider_id: int = Field(foreign_key="provider.id")
    provider: "Provider" = Relationship(back_populates="services")
