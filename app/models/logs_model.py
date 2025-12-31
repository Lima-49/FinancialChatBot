from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LogModel(BaseModel):
    """Modelo para registros de log"""
    id: Optional[int] = None
    nivel: str  # ERROR, INFO, WARNING, DEBUG, CRITICAL
    mensagem: str
    modulo: Optional[str] = None
    funcao: Optional[str] = None
    linha: Optional[int] = None
    traceback: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LogCreateModel(BaseModel):
    """Modelo para criar novos logs"""
    nivel: str
    mensagem: str
    modulo: Optional[str] = None
    funcao: Optional[str] = None
    linha: Optional[int] = None
    traceback: Optional[str] = None
