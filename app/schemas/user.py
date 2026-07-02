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