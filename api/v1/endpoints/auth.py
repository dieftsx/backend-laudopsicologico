from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from main import LoginRequest
from ....config.database import get_db
from ....services import auth
from ....schemas.user import UserCreate, User


router = APIRouter()

@router.post('/register', response_model=User)
async def register(User: UserCreate, db: Session = Depends(get_db)):



@router.post('/login', response_model=User)
async def login(login_data: LoginRequest, db: Session, Depends(get_db)):



