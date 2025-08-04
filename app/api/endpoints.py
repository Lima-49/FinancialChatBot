from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ResearchRequest, ResearchResponse
from app.services.opena_ai_service import run_research
from app.core.security import verify_api_key
from app.core.config import get_env_variable

API_KEY_CREDITS = get_env_variable("API_KEY")

router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest, x_api_key: str = Depends(verify_api_key)):
    try:
        API_KEY_CREDITS[x_api_key] -= 1
        return run_research(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))