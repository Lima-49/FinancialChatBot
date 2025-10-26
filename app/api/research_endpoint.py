from fastapi import APIRouter, HTTPException
from app.models.message_models import convert_history
from app.models.research_models import ResearchRequest, ResearchResponse
from app.services.opena_ai_service import OpenAIService
from app.services.ollama_service import OllamaService
from app.core.config import log_error_to_file
from app.core.prompts import research_prompt

router_research = APIRouter()

#PROD
research_service = OpenAIService(research_prompt, ResearchResponse)

#LOCAL
# research_service = OllamaService(research_prompt, ResearchResponse)

@router_research.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    try:
        formatted_history = convert_history(request.chat_history)
        result = research_service.run(request.query, formatted_history)
        return result
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=str(e))