from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools.tools import gcp_tool, insert_gcp_tool, datetime_tool, welcome_tool


class OpenAIService:
    def __init__(self, chat_prompt, parser):
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0.1)
        self.chat_prompt = chat_prompt
        self.parser = PydanticOutputParser(pydantic_object=parser)
        self.tools = [gcp_tool, insert_gcp_tool, datetime_tool, welcome_tool]
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
            print(f"Error parsing response: {e}")
            return None