from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ResearchRequest, ResearchResponse
from app.services.opena_ai_service import run_research
from app.services.ollama_service import run_ollama_research
from app.core.security import verify_api_key

router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest, x_api_key: str = Depends(verify_api_key)):
    try:
        return run_research(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))