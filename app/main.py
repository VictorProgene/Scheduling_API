from fastapi import FastAPI
from app.api.endpoints import availability

app = FastAPI()

# Incluindo a rota de disponibilidade
app.include_router(availability.router, prefix="/providers", tags=["Availability"])