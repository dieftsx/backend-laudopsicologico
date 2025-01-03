from fastapi import APIRouter, Depends, HTTPException
from ....services.ai_assistant import AIAssistant
from ....core.security import get_current_user
from ....models.user import User
from typing import Dict, Any

router = APIRouter()
ai_assistant = AIAssistant()

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_text(
    text: str,
    current_user: User = Depends(get_current_user)
):
    try:
        analysis = await ai_assistant.analyze_text(text)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na análise do texto: {str(e)}"
        )