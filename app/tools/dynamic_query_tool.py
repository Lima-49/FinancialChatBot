import json
from typing import Dict, Any
from langchain_community.tools import Tool
from langchain_openai import ChatOpenAI
from app.services.postgres_service import PostgresService
from app.core.prompts import dynamic_query_prompt

class DynamicQueryContext:
    """Classe para gerenciar o contexto das queries dinâmicas."""

    def __init__(self):
        self.phone_number = ""
        self.pending_queries: Dict[str, Dict[str, Any]] = {}

    def set_phone_number(self, phone: str):
        self.phone_number = phone

    def get_phone_number(self) -> str:
        return self.phone_number or "default"

    def get_pending(self, phone: str) -> Dict[str, Any]:
        return self.pending_queries.get(phone, {})

    def set_pending(self, phone: str, data: Dict[str, Any]):
        self.pending_queries[phone] = data

    def pop_pending(self, phone: str) -> Dict[str, Any]:
        return self.pending_queries.pop(phone, {})


# Instância global do contexto
query_context = DynamicQueryContext()


def get_db_schema() -> str:
    """Obtém o esquema dinâmico do banco de dados usando information_schema."""
    service = PostgresService()
    schema_str = "Esquema do Banco de Dados:\n"

    try:
        with service.get_connection() as conn:
            with conn.cursor() as cursor:
                # Obter tabelas
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                """)
                tables = cursor.fetchall()

                for (table_name,) in tables:
                    schema_str += f"- {table_name}: "
                    # Obter colunas para cada tabela
                    cursor.execute("""
                        SELECT column_name, data_type
                        FROM information_schema.columns
                        WHERE table_schema = 'public'
                          AND table_name = %s
                        ORDER BY ordinal_position
                    """, (table_name,))
                    columns = cursor.fetchall()
                    col_str = ", ".join([f"{col} ({dtype})" for col, dtype in columns])
                    schema_str += f"{col_str}\n"
    except Exception as e:
        schema_str += f"Erro ao obter esquema: {str(e)}\n"

    return schema_str


def dynamic_query_tool(user_input: str) -> str:
    """
    Tool dinâmico que interpreta o input do usuário, gera uma query SQL apropriada,
    descreve a ação em linguagem natural e confirma antes de executar modificações.
    """
    phone_number = query_context.get_phone_number()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    db_schema = get_db_schema()
    prompt = dynamic_query_prompt.format(db_schema=db_schema, user_input=user_input)

    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content.strip())

        query_type = result.get("type")
        query = result.get("query")
        description = result.get("description")

        if query_type == "select":
            # Executar query diretamente
            service = PostgresService()
            with service.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    result_data = [dict(zip(columns, row)) for row in rows]

            return f"{description}\n\nResultado:\n{json.dumps(result_data, indent=2, default=str)}"
        else:
            # Armazenar query pendente
            query_context.set_pending(phone_number, {
                'query': query,
                'description': description,
                'type': query_type
            })
            return f"{description}\n\nPara confirmar e executar esta ação, responda com: 'CONFIRMAR QUERY'"

    except Exception as e:
        return f"Erro ao processar a query: {str(e)}"


def confirm_query_tool(confirmation_input: str) -> str:
    """
    Tool para confirmar e executar uma query pendente.
    """
    phone_number = query_context.get_phone_number()

    if not query_context.get_pending(phone_number):
        return "Nenhuma query pendente para confirmar."

    if "CONFIRMAR" in confirmation_input.upper():
        query_data = query_context.pop_pending(phone_number)
        query = query_data['query']
        description = query_data['description']

        try:
            service = PostgresService()
            with service.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
            return f"Ação executada com sucesso: {description}"
        except Exception as e:
            return f"Erro ao executar a query: {str(e)}"
    else:
        query_context.pop_pending(phone_number)
        return "Confirmação cancelada."


# Definir os tools
dynamic_query = Tool(
    name="dynamic_query",
    description="Interpreta input do usuário e gera/executa queries SQL dinâmicas no banco de dados financeiro. Para modificações, pede confirmação antes de executar.",
    func=dynamic_query_tool
)

confirm_query = Tool(
    name="confirm_query",
    description="Confirma e executa uma query pendente de modificação no banco de dados.",
    func=confirm_query_tool
)
dynamic_query = Tool(
    name="dynamic_query",
    description="Interpreta input do usuário e gera/executa queries SQL dinâmicas no banco de dados financeiro. Para modificações, pede confirmação antes de executar.",
    func=dynamic_query_tool
)

confirm_query = Tool(
    name="confirm_query",
    description="Confirma e executa uma query pendente de modificação no banco de dados.",
    func=confirm_query_tool
)