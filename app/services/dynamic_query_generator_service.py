from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.models.dynamic_query_response_model import DynamicQueryResponse
from app.services.logs_service import log_service


class DynamicQueryGeneratorService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0.0)
        self.parser = PydanticOutputParser(pydantic_object=DynamicQueryResponse)

    def generate(self, prompt_text: str) -> DynamicQueryResponse | None:
        prompt = ChatPromptTemplate.from_messages(
            [("system", "{prompt_text}\n\n{format_instructions}")]
        ).partial(format_instructions=self.parser.get_format_instructions())

        chain = prompt | self.llm

        try:
            response = chain.invoke({"prompt_text": prompt_text})
            return self.parser.parse(response.content)
        except Exception as e:
            log_service.error(f"Error generating dynamic query response: {e}", exc_info=True)
            return None
