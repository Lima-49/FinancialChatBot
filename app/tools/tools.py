from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import Tool
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime
from app.core.config import get_env_variable
import pandas as pd

def save_to_txt(data:str, filename:str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formated_text = f" --- Research Output - {timestamp} --- \n\n{data}\n"

    with open(filename, "a", encoding="utf-8") as file:
        file.write(formated_text)

    return f"Data saved to {filename}"

def get_data_from_bigquery() -> pd.DataFrame:
    prod_credentials = get_env_variable("GCP_SERVICE_ACCOUNT")
    credentials = service_account.Credentials.from_service_account_file(prod_credentials)
    client = bigquery.Client(credentials=credentials)
    query_job = client.query("SELECT * FROM farmbot-436900.CONTROLE_FINANCEIRO.HISTORICO_FINANCEIRO")
    return query_job.to_dataframe()

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="SearchDuckDuckGo",
    func=search.run,
    description="Search the web using DuckDuckGo. Provide a query to get search results."
)

save_tool = Tool(
    name="SaveToTxt",
    func=save_to_txt,
    description="Saves the research output to a text file. Provide the data to save."
)

gcp_tool = Tool(
    name="AnalyzeFinancialDataGCP",
    func=get_data_from_bigquery,
    description="Realiza uma query no BigQuery. para informar sobre os dados da tabela de controle financeiro."
)

api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

