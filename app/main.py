from fastapi import FastAPI
from app.api.endpoints import availability, appointment, auth # Adicione auth
from app import models

app = FastAPI()

# Incluindo a rota de disponibilidade
app.include_router(availability.router, prefix="/providers", tags=["Availability"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])
