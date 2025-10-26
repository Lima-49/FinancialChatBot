from fastapi import APIRouter, HTTPException
from app.models.schemas import InsertResponse, InsertRequest, convert_history
from app.services.opena_ai_service import OpenAIService
from app.services.ollama_service import OllamaService
from app.core.config import log_error_to_file
from app.core.prompts import research_prompt, insert_prompt
import json

insert_router = APIRouter()

#PROD
insert_service = OpenAIService(insert_prompt, InsertResponse)

#LOCAL
# insert_service = OllamaService(insert_prompt, InsertResponse)

@insert_router.post("/insert", response_model=InsertResponse)
def insert_gasto(request: InsertRequest):
    try:
        formatted_history = convert_history(request.chat_history)
        result = insert_service.run(request.query, formatted_history)
        return result
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=str(e))