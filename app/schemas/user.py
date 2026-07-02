from sqlmodel import SQLModel
from uuid import UUID
from pydantic import EmailStr

# Schema para o Cadastro (Input)
class UserCreate(SQLModel):
    email: EmailStr
    password: str
    name: str

# Schema para a Resposta (Output) - Sem a senha!
class UserResponse(SQLModel):
    id: UUID
    email: EmailStr
    name: str