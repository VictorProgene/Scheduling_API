"""
auth.py - Authentication Endpoints (Login and Register)

This route file (APIRouter) exposes public API security endpoints:
1. 'POST /register' ➔ Allows client registration, hashing the password securely with bcrypt.
2. 'POST /login' ➔ Validates credentials (email and password) and issues the corresponding JWT access token for future calls.
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
    # 1. Find user by email
    statement = select(User).where(User.email == form_data.username)
    user = db.exec(statement).first()

    # 2. Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # 3. Generate JWT Token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
@limiter.limit("5/minute")
def register(
        request: Request,
        user_data: UserCreate,
        db: Session = Depends(get_session)
):
    # 1. Check if email is already registered
    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Create user with hashed password
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
