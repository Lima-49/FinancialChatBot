from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.message_model import Message


class DynamicQueryRequest(BaseModel):
    query: str
    chat_history: Optional[List[Message]] = None


class DynamicQueryResponse(BaseModel):
    type: str = Field(default="select" | "insert" | "update" | "delete", description="Tipo da query")
    query: str = Field(..., description="the generated SQL query")
    description: str = Field(..., description="description in Portuguese of what the query does")
