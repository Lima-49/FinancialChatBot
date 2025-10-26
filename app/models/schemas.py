from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel
from typing import Optional, List

def convert_history(history):
    messages = []
    for m in history or []:
        if m.role == "user":
            messages.append(HumanMessage(content=m.content))
        elif m.role == "bot":
            messages.append(AIMessage(content=m.content))
    return messages

class Message(BaseModel):
    role: str
    content: str

class ResearchRequest(BaseModel):
    query: str
    chat_history: Optional[List[Message]] = None

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

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

class PDFBankStatementRequest(BaseModel):
    file_name: str
    file_content: str
    chat_history: Optional[List[Message]] = None
    query: Optional[str] = None

class PDFBankStatementResponse(BaseModel):
    data: str
    categoria: str
    descricao: str
    banco: int
    metodo: int
    valor: float
    summary: str