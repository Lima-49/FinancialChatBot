from fastapi import APIRouter, HTTPException
from app.models.schemas import InsertResponse, ResearchRequest, ResearchResponse, InsertRequest, convert_history, PDFBankStatementRequest, PDFBankStatementResponse
from app.services.opena_ai_service import OpenAIService
from app.services.ollama_service import OllamaService
from app.core.config import log_error_to_file
from app.core.prompts import research_prompt, insert_prompt
import json

router = APIRouter()

#PROD
research_service = OpenAIService(research_prompt, ResearchResponse)
insert_service = OpenAIService(insert_prompt, InsertResponse)

#LOCAL
# research_service = OllamaService(research_prompt, ResearchResponse)
# insert_service = OllamaService(insert_prompt, InsertResponse)

@router.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    try:
        formatted_history = convert_history(request.chat_history)
        result = research_service.run(request.query, formatted_history)
        return result
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

@router.post("/insertPdf", response_model=PDFBankStatementResponse)
def insert_pdf_bank_statement(request: PDFBankStatementRequest):
    try:
        formatted_history = convert_history(request.chat_history)
        # Assuming the query is a JSON string with the required fields
        query_data = json.loads(request.query)
        result = insert_service.run(json.dumps(query_data), formatted_history)
        return result
    except json.JSONDecodeError:
        log_error_to_file("Invalid JSON format in request query")
        raise HTTPException(status_code=400, detail="Invalid JSON format in request query")
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=str(e))