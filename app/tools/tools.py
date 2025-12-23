from langchain_community.tools import Tool
from app.core.config import get_bigquery_client, get_site_config_url
from app.services.postgres_service import PostgresService
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

def first_message_tool(_: str = "") -> str:
    first_mesage = """
        Olá! Sou seu assistente financeiro. Posso ajudar a analisar dados financeiros e inserir novos registros.
    """
    return first_mesage

def _count_rows_for_table(conn, table_name: str) -> int:
    """Tenta contar linhas em uma tabela, tentando nomes não-aspados e aspados.
    Retorna -1 se a tabela não existir em ambos os casos.
    """
    with conn.cursor() as cur:
        # Primeiro tenta sem aspas (tabelas criadas sem aspas viram minúsculas)
        try:
            cur.execute(f"SELECT COUNT(*) AS c FROM {table_name}")
            row = cur.fetchone()
            return int(row["c"]) if isinstance(row, dict) else int(row[0])
        except Exception:
            pass
        # Depois tenta com aspas e nome conforme recebido
        try:
            cur.execute(f'SELECT COUNT(*) AS c FROM "{table_name}"')
            row = cur.fetchone()
            return int(row["c"]) if isinstance(row, dict) else int(row[0])
        except Exception:
            return -1

def _check_required_tables_status() -> dict:
    required_tables = [
        "BANCOS",
        "CARTOES_DE_CREDITO",
        "ENTRADAS",
        "SAIDAS_FREQUENTES",
        "CATEGORIAS_DE_COMPRAS",
        "FATURAS_CARTOES_DE_CREDITO",
    ]
    service = PostgresService()
    status = {}
    try:
        with service.get_connection() as conn:
            for t in required_tables:
                count = _count_rows_for_table(conn, t)
                status[t] = count
    except Exception:
        # Em caso de falha geral de conexão, marque todas como -1 (indefinido/não acessível)
        for t in required_tables:
            status[t] = -1
    return status

def welcome_or_setup(_: str = "") -> str:
    """Retorna mensagem de boas-vindas e link do site.
    Inclui lembrete de configuração se detectar tabelas vazias ou ausentes.
    """
    site_url = get_site_config_url()
    status = _check_required_tables_status()
    needs_setup = any(v <= 0 for v in status.values())

    if needs_setup:
        empty_or_missing = [k for k, v in status.items() if v <= 0]
        tables_list = ", ".join(empty_or_missing)
        return (
            "Bem-vindo(a)! Para começar, é preciso configurar seus dados.\n"
            f"Acesse: {site_url}\n"
            f"Pendências detectadas nas tabelas: {tables_list}.\n"
            "Depois de concluir a configuração, posso analisar seus dados e ajudar no dia a dia."
        )
    else:
        return (
            "Bem-vindo(a)! Estou pronto para ajudar com suas finanças.\n"
            f"Se quiser ajustar suas informações a qualquer momento, acesse: {site_url}"
        )

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

welcome_tool = Tool(
    name="WelcomeOrSetup",
    func=welcome_or_setup,
    description=(
        "Exibe uma mensagem de boas-vindas com o link do site para configurar a conta. "
        "Use quando o usuário pedir o link do site ou mencionar configuração/cadastro, "
        "ou quando for oportuno no início da conversa."
    ),
)