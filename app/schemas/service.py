"""
service.py - Schemas de Validação (Pydantic) para Serviços

Este arquivo define os contratos de dados para criação e resposta de serviços:
1. ServiceCreate: Campos aceitos no payload de criação (entrada).
2. ServiceResponse: Estrutura dos dados retornados para o cliente (saída), incluindo o ID gerado.
"""

from sqlmodel import SQLModel
from uuid import UUID

class ServiceCreate(SQLModel):
    provider_id: int
    name: str
    description: str
    duration_minutes: int
    price: float

class ServiceResponse(ServiceCreate):
    id: int