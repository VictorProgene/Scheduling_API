"""
auth.py - Endpoints de Autenticação (Login e Registro)

Este arquivo de rotas (APIRouter) expõe os endpoints públicos de segurança da API:
1. 'POST /register' ➔ Permite o cadastro de novos usuários clientes, salvando a senha de forma segura com hash bcrypt.
2. 'POST /login' ➔ Valida as credenciais (e-mail e senha) e emite o token de acesso JWT correspondente para chamadas futuras.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.database.connection import get_session
from app.models import User
from app.core.security import verify_password, create_access_token, get_password_hash
from app.schemas.user import UserCreate, UserResponse
from app.core.limiter import limiter

router = APIRouter()


@router.post("/login")
@limiter.limit("5/minute")
def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_session)
):
    # 1. Busca o usuário pelo e-mail
    statement = select(User).where(User.email == form_data.username)
    user = db.exec(statement).first()

    # 2. Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )

    # 3. Gera o Token JWT
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
@limiter.limit("5/minute")
def register(
        request: Request,
        user_data: UserCreate,
        db: Session = Depends(get_session)
):
    # 1. Verifica se o e-mail já existe
    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    # 2. Cria o usuário com a senha hasheada
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
