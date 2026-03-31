from app.core.prompts import research_prompt
from app.models.research_model import ResearchResponse
from app.services.opena_ai_service import OpenAIService
from app.tools.tools import confirm_query, datetime_tool, dynamic_query, welcome_tool


def build_research_service() -> OpenAIService:
    tools = [datetime_tool, welcome_tool, dynamic_query, confirm_query]
    return OpenAIService(research_prompt, ResearchResponse, tools=tools)
