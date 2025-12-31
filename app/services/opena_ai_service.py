from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools.tools import datetime_tool, welcome_tool, bancos_tool, cartoes_tool, faturas_pendentes_tool, analyze_faturas_tool, entradas_tool, saidas_tool, balance_tool, compras_categoria_tool, insert_compra_tool, categorias_tool
from app.services.logs_service import log_service


class OpenAIService:
    def __init__(self, chat_prompt, parser):
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0.1)
        self.chat_prompt = chat_prompt
        self.parser = PydanticOutputParser(pydantic_object=parser)
        self.tools = [datetime_tool, welcome_tool, bancos_tool, cartoes_tool, faturas_pendentes_tool, analyze_faturas_tool, entradas_tool, saidas_tool, balance_tool, categorias_tool, compras_categoria_tool, insert_compra_tool]
        self.prompt = self.init_prompt()
        agent = create_tool_calling_agent(llm=self.llm, prompt=self.prompt, tools=self.tools)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True, return_intermediate_steps=True)

    def init_prompt(self):
        prompt = ChatPromptTemplate.from_messages(
        [
            ("system",self.chat_prompt,),
            ("placeholder", "{chat_history}"),  
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]).partial(format_instructions=self.parser.get_format_instructions())
        
        return prompt

    def run(self, query: str, chat_history: list):
        raw_response = self.agent_executor.invoke({"query": query, "chat_history": chat_history})
        try:
            return self.parser.parse(raw_response["output"])
        except Exception as e:
            log_service.error(f"Erro ao parsear resposta do OpenAI: {e}", exc_info=True)
            return None