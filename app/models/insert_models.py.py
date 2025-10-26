from app.models.message_models import Message
from pydantic import BaseModel
from typing import Optional, List

class InsertRequest(BaseModel):
    query: str
    chat_history: Optional[List[Message]] = None

class InsertResponse(BaseModel):
    data: str
    categoria: str
    descricao: str
    banco: int
    metodo: int
    valor: float
    summary: str

