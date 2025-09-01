# app/services/tokenservice.py
import os
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usermodel import User
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

from jose import jwt, JWTError
from app.models.usermodel import User
from sqlalchemy.orm import Session

def get_current_user(token: str, db: Session) -> User:

    # Decode JWT token and return User object from DB. 
    # Raises JWTError if token invalid or expired.

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError("Token missing subject")
    except JWTError as e:
        raise JWTError("Invalid token") from e

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise JWTError("User not found")
    
    return user