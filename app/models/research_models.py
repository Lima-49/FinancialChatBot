from pydantic import BaseModel, Field
from typing import Optional, List
from app.models.message_models import Message

class ResearchRequest(BaseModel):
    query: str
    chat_history: Optional[List[Message]] = None

class ResearchResponse(BaseModel):
    topic: str = Field(default="Resposta Financeira", description="Tópico da resposta")
    summary: str = Field(..., description="Resumo da resposta para o usuário")
    sources: List[str] = Field(default_factory=list, description="Lista de fontes utilizadas")
    tools_used: List[str] = Field(default_factory=list, description="Lista de ferramentas utilizadas")