from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.tools.tools import gcp_tool, insert_gcp_tool, datetime_tool
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

            When the user asks for add a new financial record, generate a JSON with the following fields:
            {{
              "Data": "YYYY-MM-DD",
              "Categoria": "Alimentação",
              "Descricao": "Agua com gás no mercado do bairro",
              "Banco": "Nubank",
              "Metodo": 1,
              "Valor": 2.00
            }}
            - Data: formato YYYY-MM-DD (actual date when the user send the message)
            - Categoria: ex: Alimentação, Transporte, you can choose accordingly
            - Descricao: (string, texto curto)
            - Banco: ex: (integer, Alimentação=0, Nubank=1, Itau=2)
            - Metodo: (Integer, Crédito=0, Débito=1, Pix=2, Transferência=3)
            - Valor: (float, ex: 2.00)

            dont include any other text or explanation, just the json.
            For others questions, respond normally. Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [gcp_tool, insert_gcp_tool, datetime_tool]
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

def run_research(query: str, formatted_history: list) -> ResearchResponse:
    raw_response = agent_executor.invoke({"query": query, "chat_history": formatted_history})
    try:
        return parser.parse(raw_response["output"])
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None     