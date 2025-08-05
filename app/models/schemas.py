from pydantic import BaseModel
from typing import Optional

class ResearchRequest(BaseModel):
    query: str
    chat_history: Optional[str] = None

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]