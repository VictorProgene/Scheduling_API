"""
main.py - Application Entry Point

This file is the bootstrapper for the FastAPI server. It is responsible for:
1. Instantiating the FastAPI application.
2. Gathering and including routers (APIRouter) for all system endpoints (Auth, Providers, Appointments).
3. Configuring URL prefixes and tags for interactive documentation (Swagger).
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter
from app.api.endpoints import availability, appointment, auth, service, admin
from app import models

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS middleware to allow requests from frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(availability.router, prefix="/providers", tags=["Availability"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])
app.include_router(service.router, prefix="/services", tags=["Services"])
app.include_router(admin.router, prefix="/admin", tags=["Administration"])
