from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools.tools import gcp_tool
from app.models.schemas import ResearchResponse
import json

llm = ChatOpenAI(model="gpt-4.1", temperature=0.1)
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a financial agent that will help with the financial questions and
            Data analysis of data informed.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [gcp_tool]
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

def run_research(query: str, formatted_history: list) -> ResearchResponse:
    raw_response = agent_executor.invoke({"query": query, "chat_history": formatted_history})
    try:
        return parser.parse(raw_response["output"])
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None     