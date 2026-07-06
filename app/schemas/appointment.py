"""
appointment.py - Schemas de Validação (Pydantic) para Agendamentos

Este arquivo define os contratos de dados para criação e resposta de agendamentos:
1. AppointmentCreate: Dados requeridos ao realizar um agendamento.
2. AppointmentResponse: Dados retornados ao cliente após a criação ou consulta de agendamentos.
"""

from sqlmodel import SQLModel
from datetime import datetime

class AppointmentCreate(SQLModel):
    provider_id: int # Alterado de UUID para int
    service_id: int  # Alterado de UUID para int
    start_time: datetime

class AppointmentResponse(AppointmentCreate):
    id: int
    user_id: int
    end_time: datetime
    status: str

class BarberAppointmentResponse(SQLModel):
    id: int
    provider_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: str
    user_id: int
    client_name: str
    client_email: str

class AdminAppointmentResponse(SQLModel):
    id: int
    start_time: datetime
    end_time: datetime
    status: str
    client_name: str
    client_email: str
    provider_name: str
    service_name: str
    price: float