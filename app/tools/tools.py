import json
import re
from datetime import datetime
from typing import Any, Dict

from langchain_community.tools import Tool

from app.core.config import get_site_config_url
from app.services.cartoes_service import CartoesService
from app.services.categorias_service import CategoriasService
from app.services.compras_cartao_service import ComprasCartaoService
from app.services.postgres_service import PostgresService
from app.services.opena_ai_service import OpenAIService

from app.models.dynamic_query_response_model import DynamicQueryResponse
from app.tools.dynamic_query_context import DynamicQueryContext
from app.core.prompts import dynamic_query_prompt

# Dicionário para armazenar compras pendentes de aprovação
# Estrutura: {phone_number: {compra_data, timestamp}}
pending_purchases: Dict[str, Dict[str, Any]] = {}

query_context = DynamicQueryContext()

def get_current_datetime(_: str = "") -> str:
    """Retorna data e horário atual."""
    now = datetime.now()
    return f"Data atual: {now.strftime('%Y-%m-%d')}\nHorário atual: {now.strftime('%H:%M:%S')}"

def first_message_tool(_: str = "") -> str:
    """Mensagem inicial para o usuário."""
    first_mesage = """
        Olá! Sou seu assistente financeiro. Posso ajudar a analisar dados financeiros e inserir novos registros.
    """
    return first_mesage

def welcome_or_setup(_: str = "") -> str:
    """Retorna mensagem de boas-vindas e link do site.
    Inclui lembrete de configuração se detectar tabelas vazias ou ausentes.
    """
    site_url = get_site_config_url()
    service = PostgresService()
    status = service.check_required_tables_status()
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

def _processar_parcelas(parcelas_input: str) -> str:
    """Processa o campo de parcelas para garantir formato correto.

    Aceita formatos:
    - "1 de 3" -> "1 de 3" (já no formato correto)
    - "3" -> "1 de 3" (apenas número)
    - "3x" -> "1 de 3" (formato com x)
    - "3 vezes" -> "1 de 3" (formato por extenso)
    - None ou vazio -> "1 de 1" (padrão)

    Retorna sempre no formato "1 de N"
    """
    if not parcelas_input or parcelas_input.strip() == "":
        return "1 de 1"

    parcelas_str = str(parcelas_input).strip()

    # Se já está no formato "X de Y", retornar como está
    if " de " in parcelas_str.lower():
        return parcelas_str

    # Tentar extrair apenas o número de parcelas
    # Aceita: "3", "3x", "3 vezes", "parcelado em 3", etc.
    match = re.search(r"(\d+)", parcelas_str)
    if match:
        num_parcelas = match.group(1)
        return f"1 de {num_parcelas}"

    # Se não conseguiu extrair, retornar padrão
    return "1 de 1"

def prepare_compra_cartao(input_json: str) -> str:
    """Prepara uma compra de cartão para aprovação do usuário.

    Formato esperado (JSON):
    {
        "phone_number": "whatsapp:+5511999999999",  # OBRIGATÓRIO para identificar usuário
        "id_cartao": 1,  # OBRIGATÓRIO
        "id_banco": 1,   # OBRIGATÓRIO
        "data_compra": "YYYY-MM-DD" | "DD/MM/YYYY" | "hoje" | "hj" (opcional, padrão hoje),
        "estabelecimento": "Nome do estabelecimento",  # OBRIGATÓRIO
        "parcelas": "1 de 3" | "3" | "3x" | "3 vezes" (opcional, padrão "1 de 1"),
        "id_categoria": 1 | null (opcional),
        "nome_categoria": "Refeição" (opcional, usado se id não vier),
        "valor_compra": 150.00 | "150,00",  # OBRIGATÓRIO
        "observacoes": "Observação opcional"
    }

    Esta tool NÃO salva a compra no banco. Ela apenas prepara os dados e solicita confirmação.
    """
    try:
        data = json.loads(input_json)
        categorias_service = CategoriasService()
        cartoes_service = CartoesService()

        # Validar campos obrigatórios
        phone_number = data.get("phone_number")
        if not phone_number:
            return "❌ Erro: número de telefone não fornecido. Não é possível armazenar compra para confirmação."

        # Processar data
        data_compra_input = data.get("data_compra", datetime.now().strftime("%Y-%m-%d"))
        if data_compra_input.lower() in ["hoje", "hj"]:
            data_compra = datetime.now().date()
        else:
            try:
                data_compra = datetime.strptime(data_compra_input, "%Y-%m-%d").date()
            except:
                try:
                    data_compra = datetime.strptime(
                        data_compra_input, "%d/%m/%Y"
                    ).date()
                except:
                    data_compra = datetime.now().date()

        # Processar parcelas
        parcelas_input = data.get("parcelas", "1 de 1")
        parcelas = _processar_parcelas(parcelas_input)

        # Processar observações
        observacoes = data.get("observacoes", None)

        # Processar categoria
        id_categoria = data.get("id_categoria")
        nome_categoria_final = ""

        if not id_categoria:
            nome_categoria = data.get("nome_categoria")
            if nome_categoria:
                id_categoria = categorias_service.get_or_create_categoria(
                    nome_categoria
                )
                nome_categoria_final = nome_categoria
            else:
                estabelecimento = data["estabelecimento"]
                id_categoria = categorias_service.get_or_create_categoria(
                    estabelecimento
                )
                nome_categoria_final = estabelecimento
        else:
            categoria = categorias_service.get_categoria_by_id(id_categoria)
            nome_categoria_final = (
                categoria.nome_categoria if categoria else "Não identificada"
            )

        # Obter nome do cartão
        cartao = cartoes_service.get_cartao_by_id(data["id_cartao"])
        nome_cartao = cartao.nome_cartao if cartao else f"Cartão ID {data['id_cartao']}"

        # Armazenar compra pendente
        compra_data = {
            "id_cartao": data["id_cartao"],
            "id_banco": data["id_banco"],
            "data_compra": data_compra.strftime("%Y-%m-%d"),
            "estabelecimento": data["estabelecimento"],
            "parcelas": parcelas,
            "id_categoria": id_categoria,
            "valor_compra": float(data["valor_compra"]),
            "observacoes": observacoes,
            "timestamp": datetime.now().isoformat(),
        }

        pending_purchases[phone_number] = compra_data

        # Retornar resumo para aprovação
        valor_formatado = f"R$ {data['valor_compra']:.2f}".replace(".", ",")
        data_formatada = data_compra.strftime("%d/%m/%Y")

        return (
            f"📝 **CONFIRMAR COMPRA**\n\n"
            f"🏪 Estabelecimento: {data['estabelecimento']}\n"
            f"💳 Cartão: {nome_cartao}\n"
            f"💰 Valor: {valor_formatado}\n"
            f"📅 Data: {data_formatada}\n"
            f"🔢 Parcelas: {parcelas}\n"
            f"📦 Categoria: {nome_categoria_final}\n"
            f"📝 Observações: {observacoes if observacoes else 'Nenhuma'}\n\n"
            f"✅ Digite 'confirmar' ou 'sim' para salvar esta compra.\n"
            f"❌ Digite 'cancelar' ou 'não' para descartar."
        )
    except json.JSONDecodeError:
        return "❌ Erro: JSON inválido. Verifique o formato dos dados."
    except KeyError as e:
        return f"❌ Erro: Campo obrigatório ausente: {str(e)}"
    except Exception as e:
        return f"❌ Erro ao preparar compra: {str(e)}"

def confirm_compra_cartao(input_json: str) -> str:
    """Confirma e salva a compra pendente do usuário.

    Formato esperado (JSON):
    {
        "phone_number": "whatsapp:+5511999999999",  # OBRIGATÓRIO
        "confirmed": true | false  # true para salvar, false para cancelar
    }
    """
    try:
        data = json.loads(input_json)
        phone_number = data.get("phone_number")
        confirmed = data.get("confirmed", False)

        if not phone_number:
            return "❌ Erro: número de telefone não fornecido."

        # Verificar se há compra pendente
        if phone_number not in pending_purchases:
            return "⚠️ Não há compra pendente de aprovação. Por favor, adicione uma compra primeiro."

        # Se cancelado
        if not confirmed:
            del pending_purchases[phone_number]
            return "❌ Compra cancelada e descartada."

        # Recuperar compra pendente
        compra_data = pending_purchases[phone_number]

        # Salvar no banco
        compras_service = ComprasCartaoService()
        categorias_service = CategoriasService()

        data_compra = datetime.strptime(compra_data["data_compra"], "%Y-%m-%d").date()

        id_compra = compras_service.insert_compra_cartao(
            id_cartao=compra_data["id_cartao"],
            data_compra=data_compra,
            estabelecimento=compra_data["estabelecimento"],
            id_categoria=compra_data["id_categoria"],
            valor_compra=compra_data["valor_compra"],
            observacoes=compra_data["observacoes"],
            numero_parcelas=(
                compra_data["numero_parcelas"]
                if "numero_parcelas" in compra_data
                else 1
            ),
            parcela_atual=(
                compra_data["parcela_atual"] if "parcela_atual" in compra_data else 1
            ),
        )

        # Limpar compra pendente
        del pending_purchases[phone_number]

        # Obter nome da categoria
        categoria = categorias_service.get_categoria_by_id(compra_data["id_categoria"])
        nome_cat = categoria.nome_categoria if categoria else "Não identificada"

        valor_formatado = f"R$ {compra_data['valor_compra']:.2f}".replace(".", ",")

        return (
            f"✅ **COMPRA SALVA COM SUCESSO!**\n\n"
            f"🆔 ID: {id_compra}\n"
            f"🏪 Estabelecimento: {compra_data['estabelecimento']}\n"
            f"💰 Valor: {valor_formatado}\n"
            f"🔢 Parcelas: {compra_data['parcelas']}\n"
            f"📦 Categoria: {nome_cat}\n"
            f"📝 Observações: {compra_data['observacoes'] if compra_data['observacoes'] else 'Nenhuma'}"
        )
    except json.JSONDecodeError:
        return "❌ Erro: JSON inválido. Verifique o formato dos dados."
    except KeyError as e:
        return f"❌ Erro: Campo obrigatório ausente: {str(e)}"
    except Exception as e:
        return f"❌ Erro ao confirmar compra: {str(e)}"

def insert_compra_cartao(input_json: str) -> str:
    """Insere uma nova compra de cartão de crédito.

    Formato esperado (JSON):
    {
        "id_cartao": 1,  # OBRIGATÓRIO
        "id_banco": 1,   # OBRIGATÓRIO
        "data_compra": "YYYY-MM-DD" | "DD/MM/YYYY" | "hoje" | "hj" (opcional, padrão hoje),
        "estabelecimento": "Nome do estabelecimento",  # OBRIGATÓRIO
        "parcelas": "1 de 3" | "3" | "3x" | "3 vezes" (opcional, padrão "1 de 1"),
        "id_categoria": 1 | null (opcional),
        "nome_categoria": "Refeição" (opcional, usado se id não vier),
        "valor_compra": 150.00 | "150,00",  # OBRIGATÓRIO
        "observacoes": "Observação opcional"
    }

    IMPORTANTE:
    - Se parcelas não for informado, será definido como "1 de 1"
    - Se informar apenas o número (ex: "3"), será convertido para "1 de 3"
    - Se observacoes não for informado, será None
    - Se id_categoria não for informado, tentará encontrar ou criar categoria baseado em nome_categoria
    - Se nome_categoria também não for informado, tentará inferir do estabelecimento
    """

    try:
        data = json.loads(input_json)
        compras_service = ComprasCartaoService()
        categorias_service = CategoriasService()

        # Processar data
        data_compra = datetime.strptime(data["data_compra"], "%Y-%m-%d").date()

        # Processar parcelas (padrão: "1 de 1")
        parcelas_input = data.get("parcelas", "1 de 1")
        parcelas = _processar_parcelas(parcelas_input)

        # Processar observações (padrão: None)
        observacoes = data.get("observacoes", None)

        # Processar categoria (SEMPRE OBRIGATÓRIO)
        id_categoria = data.get("id_categoria")

        if not id_categoria:
            # Tentar buscar por nome_categoria
            nome_categoria = data.get("nome_categoria")

            if nome_categoria:
                # Buscar ou criar categoria com o nome fornecido
                id_categoria = categorias_service.get_or_create_categoria(
                    nome_categoria
                )
            else:
                # Tentar inferir do estabelecimento
                estabelecimento = data["estabelecimento"]
                # Usar o nome do estabelecimento como categoria
                id_categoria = categorias_service.get_or_create_categoria(
                    estabelecimento
                )

        # Inserir a compra
        id_compra = compras_service.insert_compra_cartao(
            id_cartao=data["id_cartao"],
            data_compra=data_compra,
            estabelecimento=data["estabelecimento"],
            id_categoria=id_categoria,
            valor_compra=data["valor_compra"],
            observacoes=data["observacoes"],
            numero_parcelas=data["numero_parcelas"] if "numero_parcelas" in data else 1,
            parcela_atual=data["parcela_atual"] if "parcela_atual" in data else 1,
        )

        # Obter nome da categoria para mensagem de confirmação
        categoria = categorias_service.get_categoria_by_id(id_categoria)
        nome_cat = categoria.nome_categoria if categoria else "Não identificada"

        return (
            f"✅ Compra inserida com sucesso!\n"
            f"ID: {id_compra}\n"
            f"Estabelecimento: {data['estabelecimento']}\n"
            f"Valor: R$ {data['valor_compra']:.2f}\n"
            f"Parcelas: {parcelas}\n"
            f"Categoria: {nome_cat}\n"
            f"Observações: {observacoes if observacoes else 'Nenhuma'}"
        )
    except json.JSONDecodeError:
        return "❌ Erro: JSON inválido. Verifique o formato dos dados."
    except KeyError as e:
        return f"❌ Erro: Campo obrigatório ausente: {str(e)}"
    except Exception as e:
        return f"❌ Erro ao inserir compra: {str(e)}"

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

                for line in tables:

                    table_name = line['table_name']

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

                    col_str = ", ".join([f"{line['column_name']} ({line['data_type']})" for line in columns])
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

    db_schema = get_db_schema()
    prompt = dynamic_query_prompt.format(db_schema=db_schema, user_input=user_input)
    response_model = DynamicQueryResponse()
    llm = OpenAIService(prompt, response_model)

    try:
        response = llm.run(query=prompt, chat_history=[], phone_number=phone_number)
        query = response.get("query")
        description = response.get("description", "Ação gerada")
        query_type = response.get("type", "select")

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


datetime_tool = Tool(
    name="GetCurrentDateTime",
    func=get_current_datetime,
    description="Retorna a data e o horário atual do sistema.",
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

prepare_compra_tool = Tool(
    name="PrepareCompraCartao",
    func=prepare_compra_cartao,
    description=(
        "SEMPRE use esta tool PRIMEIRO quando o usuário quiser adicionar uma compra. "
        "Esta tool prepara a compra e mostra um resumo para o usuário aprovar. "
        "NÃO salva no banco - apenas prepara e aguarda confirmação. "
        "Formato JSON: {phone_number (obrigatório), id_cartao, id_banco, estabelecimento, valor_compra, "
        "data_compra(opcional), parcelas(opcional), nome_categoria(opcional), observacoes(opcional)}. "
        "Depois de usar esta tool, aguarde o usuário confirmar ou cancelar."
    ),
)

confirm_compra_tool = Tool(
    name="ConfirmCompraCartao",
    func=confirm_compra_cartao,
    description=(
        "Use esta tool quando o usuário confirmar ou cancelar uma compra pendente. "
        "Procure por palavras como 'sim', 'confirmar', 'ok', 'salvar' para confirmed=true. "
        "Procure por palavras como 'não', 'cancelar' para confirmed=false. "
        "Formato JSON: {phone_number (obrigatório), confirmed (boolean)}. "
        "Esta tool salva a compra no banco se confirmed=true, ou descarta se confirmed=false."
    ),
)

insert_compra_tool = Tool(
    name="InsertCompraCartao",
    func=insert_compra_cartao,
    description=(
        "DEPRECATED: Use PrepareCompraCartao + ConfirmCompraCartao ao invés desta. "
        "Esta tool ainda existe para compatibilidade, mas o fluxo correto é: "
        "1) PrepareCompraCartao para mostrar resumo ao usuário "
        "2) ConfirmCompraCartao para salvar após aprovação."
    ),
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