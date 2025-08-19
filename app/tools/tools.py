from langchain_community.tools import Tool
from app.core.config import get_bigquery_client
import pandas as pd
import json
from datetime import datetime


def get_data_from_bigquery(query: str) -> pd.DataFrame:
    client = get_bigquery_client()
    query_job = client.query("SELECT * FROM farmbot-436900.CONTROLE_FINANCEIRO.HISTORICO_FINANCEIRO")
    df = query_job.to_dataframe()
    return df

def insert_data_to_bigquery(data: str) -> str:
    try:

        # Extrai apenas o JSON da resposta do LLM
        if not isinstance(data, dict):
            # Se vier como string, tente extrair o JSON
            start = data.find("{")
            end = data.rfind("}") + 1
            data_json = data[start:end]
            record = json.loads(data_json)
        else:
            record = data

        record = json.loads(data)
        client = get_bigquery_client()
        table_id = "farmbot-436900.CONTROLE_FINANCEIRO.HISTORICO_FINANCEIRO"
        rows_to_insert = [record]
        errors = client.insert_rows_json(table_id, rows_to_insert)
        if errors == []:
            return "Registro inserido com sucesso!"
        else:
            return f"Erro ao inserir: {errors}"
    except Exception as e:
        return f"Erro ao processar/inserir: {e}"

def get_current_datetime(_: str = "") -> str:
    now = datetime.now()
    return f"Data atual: {now.strftime('%Y-%m-%d')}\nHorário atual: {now.strftime('%H:%M:%S')}"

gcp_tool = Tool(
    name="AnalyzeFinancialDataGCP",
    func=get_data_from_bigquery,
    description="Realiza uma query no BigQuery. para informar sobre os dados da tabela de controle financeiro."
)

insert_gcp_tool = Tool(
    name="InsertFinancialDataGCP",
    func=insert_data_to_bigquery,
    description="Insere dados financeiros na tabela do BigQuery. Envie um JSON com os campos: descricao, valor, data."
)

datetime_tool = Tool(
    name="GetCurrentDateTime",
    func=get_current_datetime,
    description="Retorna a data e o horário atual do sistema."
)