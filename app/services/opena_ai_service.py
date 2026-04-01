from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from app.services.logs_service import log_service
from app.tools.dynamic_query_context import DynamicQueryContext

class OpenAIService:
    def __init__(self, chat_prompt, parser, tools: list[BaseTool] | None = None):
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0.1)
        self.chat_prompt = chat_prompt
        self.parser = PydanticOutputParser(pydantic_object=parser)
        self.current_phone_number = ""  # Para passar para tools
        self.tools = tools or []
        self.prompt = self.init_prompt()
        if self.tools:
            agent = create_tool_calling_agent(
                llm=self.llm, prompt=self.prompt, tools=self.tools
            )
            self.agent_executor = AgentExecutor(
                agent=agent, tools=self.tools, verbose=True, return_intermediate_steps=True
            )
        else:
            self.agent_executor = None
        self.query_context = DynamicQueryContext()

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
        """Run the agent and return the response.

        Args:
            query: User query
            chat_history: Conversation history
            phone_number: User phone number

        Returns:
            ResearchResponse or None in case of error
        """
        self.query_context.set_phone_number(phone_number)
        if self.agent_executor:
            raw_response = self.agent_executor.invoke(
                {"query": query, "chat_history": chat_history, "phone_number": phone_number}
            )
            output_text = raw_response["output"]
        else:
            chain = self.prompt | self.llm
            raw_response = chain.invoke({"query": query, "chat_history": chat_history, "phone_number": phone_number}
            )
            output_text = raw_response.content
        try:
            return self.parser.parse(output_text)
        except Exception as e:
            log_service.error(f"Error parsing OpenAI response: {e}", exc_info=True)
            return None
