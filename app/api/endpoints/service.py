"""
service.py - Endpoints de Gerenciamento de Serviços

Este arquivo expõe as rotas para o gerenciamento de serviços oferecidos:
1. 'POST /' ➔ Cadastra um novo tipo de serviço associado a um profissional (provider_id) específico.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.connection import get_session
from app.schemas.service import ServiceCreate, ServiceResponse
from app.models.service import Service
from app.models.provider import Provider

router = APIRouter()

@router.post("/", response_model=ServiceResponse)
def create_service(service_data: ServiceCreate, db: Session = Depends(get_session)):
    # 1. Verifica se o profissional informado existe
    provider = db.get(Provider, service_data.provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Profissional (provider_id) não encontrado.")
    
    # 2. Cria e salva o serviço
    new_service = Service(**service_data.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@router.get("/", response_model=List[ServiceResponse])
def list_services(db: Session = Depends(get_session)):
    services = db.exec(select(Service)).all()
    return services
