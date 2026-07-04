"""
connection.py - Conexão e Sessão com o Banco de Dados

Este arquivo estabelece e gerencia o ciclo de vida da conexão com o banco de dados via SQLModel.
Responsabilidades:
1. Instanciar a engine de comunicação usando a URL lida das configurações.
2. Disponibilizar o gerador de sessões 'get_session' injetado como dependência nos endpoints para operações no banco (CRUD).
"""

from sqlmodel import create_engine, Session
from app.core.config import settings

# Agora ele lê dinamicamente o que está no seu .env (porta 5432)
engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session