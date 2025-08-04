from pydantic import BaseModel

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]