"""
provider.py - Schemas de Validação (Pydantic) para Prestadores e Disponibilidade

Este arquivo define os contratos de dados para criação e resposta de prestadores de serviços:
1. ProviderCreate: Estrutura dos dados enviados para cadastrar um prestador.
2. ProviderResponse: Estrutura de retorno dos dados de um prestador contendo o ID gerado.
3. AvailabilityResponse: Formato dos dados de listagem de horários disponíveis.
"""

from sqlmodel import SQLModel
from uuid import UUID
from datetime import time, date, datetime
from typing import List, Optional

class ProviderCreate(SQLModel):
    name: str
    email: str
    start_work_hour: int
    end_work_hour: int
    password: Optional[str] = None

class ProviderResponse(ProviderCreate):
    id: int
    user_id: Optional[int] = None

class AvailabilityResponse(SQLModel):
    provider_id: int
    date: date
    available_slots: List[datetime]