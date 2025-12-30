from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConversationMessage(BaseModel):
    """Modelo para uma mensagem individual na conversa"""
    role: str  # 'user' ou 'assistant'
    content: str
    timestamp: Optional[datetime] = None


class ConversationHistory(BaseModel):
    """Modelo para o histórico completo de uma conversa"""
    mensagem_id: Optional[int] = None
    numero_telefone: str
    tipo_mensageiro: str  # 'user' ou 'assistant'
    conteudo_mensagem: str  # Conteúdo criptografado
    data_criacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True
