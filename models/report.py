from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..config.database import Base
class report(Base):
    __tablename__ = "laudos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    paciente_name = Column(String, nullable=False)
    diagnostico = Column(Text, nullable=False)
    criado_em = Column(Datetime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    atualizado_em = Column(Datetime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    usuario = relationship("User", back_populates="laudos")


