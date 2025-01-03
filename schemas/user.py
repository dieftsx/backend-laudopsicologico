from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    nome: str
    email: EmailStr
    crp: str

class UserCreate(UserBase):
    senha: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    crp: Optional[str] = None
    senha: Optional[str] = None

class User(UserBase):
    id: str
    created_at: datetime
    is_admin: bool = False

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    exp: int