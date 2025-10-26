from pydantic import BaseModel
from typing import Optional, List
from app.models.message_models import Message

class ResearchRequest(BaseModel):
    query: str
    chat_history: Optional[List[Message]] = None

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]