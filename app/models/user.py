"""
user.py - Modelo ORM físico para a tabela de Usuários

Este arquivo define a estrutura da tabela de dados 'user' no banco de dados.
Campos:
- id: Chave primária autoincremental.
- name: Nome do usuário.
- email: E-mail (usado como login e chave única).
- password: Hash seguro da senha do usuário.
Relacionamentos:
- appointments: Lista de agendamentos realizados pelo usuário.
"""

from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.appointment import Appointment


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    password: str

    # Relação com Appointment
    appointments: list["Appointment"] = Relationship(back_populates="user")
