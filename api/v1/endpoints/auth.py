from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any
from ....config.database import get_db
from ....schemas.user import UserCreate, User, Token, LoginRequest
from ....services.auth import AuthService
from ....services.user import UserService
from ....core.security import get_current_user


router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if UserService.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email já está registrado"
        )
    return UserService.create_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = AuthService.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return AuthService.create_token(user)

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


