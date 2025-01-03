from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid
from ..config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    pass_hash = Column(String, nullable=False)
    crp = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)