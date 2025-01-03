from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
import jwt
import bcrypt
from ..config.settings import settings
from ..models.user import User
from ..schemas.user import Token

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not AuthService.verify_password(password, user.senha_hash):
            return None
        return user

    @staticmethod
    def create_token(user: User) -> Token:
        access_token = AuthService.create_access_token(
            data={"sub": str(user.id)}
        )
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )