from fastapi import APIRouter, HTTPException
from app.models.schemas import InsertResponse, ResearchRequest, ResearchResponse, InsertRequest, convert_history
from app.services.opena_ai_service import OpenAIService
from app.core.config import log_error_to_file
from app.core.prompts import research_prompt, insert_prompt
import json

router = APIRouter()

research_service = OpenAIService(research_prompt, ResearchResponse)
insert_service = OpenAIService(insert_prompt, InsertResponse)

@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    try:
        formatted_history = convert_history(request.chat_history)
        return research_service.run(request.query, formatted_history)
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert", response_model=InsertResponse)
def insert_gasto(request: InsertRequest):
    try:
        formatted_history = convert_history(request.chat_history)
        result = insert_service.run(request.query, formatted_history)
        return result
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=str(e))