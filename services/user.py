from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
import bcrypt
import uuid

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data.senha.encode('utf-8'), salt)

        db_user = User(
            id=str(uuid.uuid4()),
            nome=user_data.nome,
            email=user_data.email,
            password_hash=hashed_password.decode('utf-8'),
            crp=user_data.crp
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_email(db:Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id:str):
        return db.query(User).filter(User.id == user_id).first()