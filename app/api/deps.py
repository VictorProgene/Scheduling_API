"""
deps.py - API Security Dependency Injection

This file contains dependency functions dynamically injected by FastAPI into routes.
The main function is 'get_current_user', which is responsible for:
1. Extracting and validating the JWT token received in the Authorization header.
2. Securing private endpoints (rejecting requests without a valid token).
3. Passing the authenticated user ID to be used in business logic.
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
        return user_id  # Returns the user ID to the route
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")