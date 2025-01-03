from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....config.database import get_db
from ....schemas.report import LaudoCreate, LaudoUpdate, LaudoResponse
from ....services.report import LaudoService
from ....core.security import get_current_user
from ....models.user import User

router = APIRouter()

@router.post('/', response_model=LaudoResponse)
async def create_laudo(
        laudo_data: LaudoCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return LaudoService.create_laudo(db, laudo_data, current_user.id)

@router.get('/', response_model=List[LaudoResponse])
async def list_laudos(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return LaudoService.get_laudo(db, current_user.id)

@router.get('/{laudo_id}', response_model=LaudoResponse)
async def get_laudo(
        laudo_id: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    laudo = LaudoService.get_laudo(db, laudo_id, current_user.id)
    if not laudo:
        raise HTTPException(status_code=404, detail= "Laudo não encontrado")
    return laudo

@router.put('/{laudo_id}', response_model=LaudoResponse)
async def update_laudo(
        laudo_id:str,
        laudo_data: LaudoUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return LaudoUpdate.update_laudo(db, laudo_id, current_user.id, laudo_data.diagnostico)