import jwt
import datetime from datetime, timedelta
import bcrypt

from ..config.settings import settings

def create_access_token(data: dict)
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp:": expire})
    return  jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'),
                          hashed_password.encode('ut-8'))



