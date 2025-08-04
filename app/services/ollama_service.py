import ollama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.models.schemas import ResearchResponse
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools.tools import search_tool, wiki_tool, save_tool

client = ollama.Client()
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(llm=client, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

response = client.generate(model="llama2", prompt=prompt)

def run_research(query: str) -> ResearchResponse:
    raw_response = agent_executor.invoke({"query": query})
    print("DEBUG raw_response:", raw_response)
    try:
        return parser.parse(raw_response["output"][0])
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None     