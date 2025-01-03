import uuid

from sqlalchemy.orm import Session
from ..models.report import report
from ..schemas.report import LaudoCreate

from fastapi import HTTPException
from uuid


class Laudo:
    pass


class LaudoService:
    @staticmethod

    def create_laudo(db:Session, laudo_data: LaudoCreate, usuario_id: str):
        db_laudo = Laudo(
            id=str(uuid.uuid4()),
        usuario_id=usuario_id,
        paciente_nome=laudo_data.paciente_nome,
        diagnostico=laudo_data.diagnostico
        )
        db.add(db_laudo)
        db.commit()
        db.refresh(db_laudo)
        return db_laudo

    @staticmethod
    def get_laudo(db: Session, laudo_id: str, usuario_id: str):
        return db.query(Laudo).filter(
     Laudo.id == laudo_id,
            Laudo.usuario_id == usuario_id
        ).first()

    @staticmethod
    def update_laudo(db:Session, laudo_id:str, usuario_id: str, diagnostico: str):
        laudo = db.query(Laudo).filter(
            Laudo.id == laudo_id,
            Laudo.usuario.id == usuario_id
        ).first()
        
    if not laudo:
        raise HTTPException(status_code=404, detail="Laudo não encontrado")
    
    laudo.diagnostico = diagnostico
    db.commit()
    db.refresh(laudo)
    return laudo






