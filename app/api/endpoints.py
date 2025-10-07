from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import InsertResponse, ResearchRequest, ResearchResponse, InsertRequest, convert_history
from app.services.opena_ai_service import OpenAIService
from app.services.ollama_service import OllamaService
from app.core.config import log_error_to_file
from app.core.prompts import research_prompt, insert_prompt
from app.tools.tools import extract_bank_statement_from_pdf, process_pdf_and_insert_to_db
import json
import tempfile
import os
from typing import Dict, Any

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

@router.post("/upload-pdf")
async def upload_bank_statement_pdf(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload e processamento de PDF de fatura bancária.
    Extrai as transações e retorna os dados estruturados.
    """
    try:
        # Verifica se é um arquivo PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
        
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Extrai dados do PDF
            result = extract_bank_statement_from_pdf(temp_file_path)
            extracted_data = json.loads(result)
            
            return {
                "success": True,
                "filename": file.filename,
                "bank_type": extracted_data.get("bank_type"),
                "transactions_count": extracted_data.get("transactions_count", 0),
                "transactions": extracted_data.get("transactions", []),
                "message": "PDF processado com sucesso"
            }
            
        finally:
            # Remove o arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

@router.post("/upload-pdf-and-insert")
async def upload_pdf_and_insert_to_db(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload de PDF de fatura bancária, extração de dados e inserção automática no banco.
    """
    try:
        # Verifica se é um arquivo PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
        
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Processa PDF e insere no banco
            result = process_pdf_and_insert_to_db(temp_file_path)
            
            return {
                "success": True,
                "filename": file.filename,
                "result": result,
                "message": "PDF processado e dados inseridos no banco"
            }
            
        finally:
            # Remove o arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF e inserir no banco: {str(e)}")

@router.post("/process-local-pdf")
def process_local_pdf(pdf_path: str, insert_to_db: bool = False) -> Dict[str, Any]:
    """
    Processa um PDF local (útil para desenvolvimento e testes).
    
    Args:
        pdf_path: Caminho para o arquivo PDF local
        insert_to_db: Se True, insere automaticamente no banco de dados
    """
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {pdf_path}")
        
        if insert_to_db:
            # Processa e insere no banco
            result = process_pdf_and_insert_to_db(pdf_path)
            return {
                "success": True,
                "pdf_path": pdf_path,
                "result": result,
                "message": "PDF processado e dados inseridos no banco"
            }
        else:
            # Apenas extrai os dados
            result = extract_bank_statement_from_pdf(pdf_path)
            extracted_data = json.loads(result)
            
            return {
                "success": True,
                "pdf_path": pdf_path,
                "bank_type": extracted_data.get("bank_type"),
                "transactions_count": extracted_data.get("transactions_count", 0),
                "transactions": extracted_data.get("transactions", []),
                "message": "PDF processado com sucesso"
            }
            
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF local: {str(e)}")