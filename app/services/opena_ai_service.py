from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.services.logs_service import log_service
from app.tools.tools import welcome_tool, datetime_tool

from app.tools.dynamic_query_context import dynamic_query, confirm_query, query_context


class OpenAIService:
    def __init__(self, chat_prompt, parser):
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0.1)
        self.chat_prompt = chat_prompt
        self.parser = PydanticOutputParser(pydantic_object=parser)
        self.current_phone_number = ""  # Para passar para tools
        self.tools = [
            datetime_tool,
            welcome_tool,
            dynamic_query,
            confirm_query,
        ]
        self.prompt = self.init_prompt()
        agent = create_tool_calling_agent(
            llm=self.llm, prompt=self.prompt, tools=self.tools
        )
        self.agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, verbose=True, return_intermediate_steps=True
        )

    def init_prompt(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.chat_prompt,
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions())

        return prompt

    def run(self, query: str, chat_history: list, phone_number: str = ""):
        """Executa o agente e retorna a resposta.

        Args:
            query: Query do usuário
            chat_history: Histórico de conversa
            phone_number: Número de telefone do usuário

        Returns:
            ResearchResponse ou None em caso de erro
        """
        query_context.set_phone_number(phone_number)
        raw_response = self.agent_executor.invoke(
            {"query": query, "chat_history": chat_history, "phone_number": phone_number}
        )
        try:
            return self.parser.parse(raw_response["output"])
        except Exception as e:
            log_service.error(f"Erro ao parsear resposta do OpenAI: {e}", exc_info=True)
            return None
