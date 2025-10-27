from fastapi import APIRouter, HTTPException
from app.models.config_account_model import ConfigAccountModelRequest, ConfigAccountModelResponse
from app.core.config import log_error_to_file
from app.services.postgres_service import PostgresService

config_router = APIRouter()

postgres_service = PostgresService()

@config_router.post("/config/addBankAccount", response_model=ConfigAccountModelResponse)
def add_bank_account(request: ConfigAccountModelRequest):
    try:
        result = postgres_service.insert_bank_account(request)
        return result
    except Exception as e:
        log_error_to_file(e)
        raise HTTPException(status_code=500, detail=str(e))