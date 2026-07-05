"""
security.py - Security Helpers, Hashing and JWT Cryptography

This file centralizes the cryptographic protection logic of the API, including:
1. User password hashing and verification (using the bcrypt algorithm via passlib).
2. JWT (JSON Web Token) access token generation signed with the defined secret key and expiration time.
"""

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

SECRET_KEY_CORE = settings.secret_key_core
ALGORITHM = "HS256"
SECRET_KEY = settings.secret_key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)