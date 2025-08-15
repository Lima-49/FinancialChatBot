from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import Tool
from google.cloud import bigquery
from google.oauth2 import service_account
from app.core.config import get_env_variable
import pandas as pd


def get_data_from_bigquery(query: str) -> pd.DataFrame:

    prod_credentials = get_env_variable("GCP_SERVICE_ACCOUNT")
    credentials = service_account.Credentials.from_service_account_file(prod_credentials)
    client = bigquery.Client(credentials=credentials)
    query_job = client.query("SELECT * FROM farmbot-436900.CONTROLE_FINANCEIRO.HISTORICO_FINANCEIRO")
    df = query_job.to_dataframe()

    return df

gcp_tool = Tool(
    name="AnalyzeFinancialDataGCP",
    func=get_data_from_bigquery,
    description="Realiza uma query no BigQuery. para informar sobre os dados da tabela de controle financeiro."
)

api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

