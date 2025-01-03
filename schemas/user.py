from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel)
    name: str
    email: EmailStr
    password: str
    crp: str

class User(BaseModel)
    id: str
    name: str
    email: EmailStr
    cpr: str

    class Config:
        from_attributes = True
