"""
main.py - Ponto de Entrada da Aplicação

Este arquivo é o inicializador (bootstrapper) do servidor FastAPI. Ele é encarregado de:
1. Instanciar o aplicativo FastAPI.
2. Reunir e incluir os roteadores (APIRouter) de todas as rotas do sistema (Auth, Providers, Appointments).
3. Configurar os prefixos de URL e tags de organização para a documentação interativa (Swagger).
"""

from fastapi import FastAPI
from app.api.endpoints import availability, appointment, auth, service
from app import models

app = FastAPI()

app.include_router(availability.router, prefix="/providers", tags=["Availability"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])
app.include_router(service.router, prefix="/services", tags=["Services"])
