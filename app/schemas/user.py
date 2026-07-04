"""
user.py - Schemas de Validação (Pydantic) para UsuáriosClientes

Este arquivo define os contratos de dados para criação e retorno de usuários clientes:
1. UserCreate: Dados enviados no registro de novas contas de clientes.
2. UserResponse: Estrutura segura de retorno dos dados cadastrados, sem expor o hash da senha.
"""

from sqlmodel import SQLModel
from pydantic import EmailStr

class UserCreate(SQLModel):
    email: EmailStr
    password: str
    name: str

class UserResponse(SQLModel):
    id: int  # Alterado de UUID para int
    email: EmailStr
    name: str