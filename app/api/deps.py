"""
deps.py - Dependências de Injeção de Segurança da API

Este arquivo contém as funções de dependência que o FastAPI injeta dinamicamente nas rotas.
A principal função é 'get_current_user', encarregada de:
1. Extrair e validar o Token JWT recebido no Header de Autorização.
2. Garantir o controle de acesso de rotas privadas (barrando requisições sem token válido).
3. Repassar o ID do usuário autenticado para ser usado nas regras de negócio (como criar agendamento).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401)
        return user_id # Retorna o ID do usuário para a rota
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")