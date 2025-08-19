from fastapi import APIRouter, HTTPException
from app.models.schemas import ResearchRequest, ResearchResponse, convert_history
from app.services.opena_ai_service import run_research
from app.core.config import log_error_to_file

router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    try:
        formatted_history = convert_history(request.chat_history)
        return run_research(request.query,formatted_history)
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=str(e))
