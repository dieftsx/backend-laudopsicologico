from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.exceptions import CustomHTTPException
import bcrypt
import uuid


class UserService:
    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        # Verificar se email já existe
        if db.query(User).filter(User.email == user_data.email).first():
            raise CustomHTTPException.credentials_exception()

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data.senha.encode('utf-8'), salt)

        db_user = User(
            id=str(uuid.uuid4()),
            nome=user_data.nome,
            email=user_data.email,
            senha_hash=hashed_password.decode('utf-8'),
            crp=user_data.crp
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdate):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise CustomHTTPException.not_found_exception("Usuário")

        # Atualizar campos se fornecidos
        if user_data.nome:
            user.nome = user_data.nome
        if user_data.email:
            # Verificar se novo email já existe
            existing_user = db.query(User).filter(
                User.email == user_data.email,
                User.id != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email já está em uso"
                )
            user.email = user_data.email
        if user_data.crp:
            user.crp = user_data.crp
        if user_data.senha:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(
                user_data.senha.encode('utf-8'),
                salt
            )
            user.senha_hash = hashed_password.decode('utf-8')

        db.commit()
        db.refresh(user)
        return user
