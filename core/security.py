from dns.dnssecalgs import algorithms
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt import JWTError
from ..config.settings import settings
from ..config.database import get_db
from sqlalchemy.orm import Session
from ..services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
        
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = UserService.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user
        