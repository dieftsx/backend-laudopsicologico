from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LaudoCreate(BaseModel)
    paciente_nome: str
    diagnostico: str

class LaudoUpdate(BaseModel)
    diagnostico: str

class LaudoResponse(BaseModel)
    id: str
    paciente_nome: str
    criado_em: datetime
    atualizado_em: datetime

class Config:
    from_attributes = True

