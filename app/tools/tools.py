from langchain_community.tools import Tool
from app.core.config import get_site_config_url
from app.services.postgres_service import PostgresService
from datetime import datetime
import json


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


# ==================== CONSULTAS DE BANCOS ====================

def get_bancos_info(_: str = "") -> str:
    """Retorna informações sobre todos os bancos cadastrados."""
    try:
        service = PostgresService()
        bancos = service.get_all_bancos()
        
        if not bancos:
            return "Nenhum banco cadastrado no sistema."
        
        result = "📊 **BANCOS CADASTRADOS**\n\n"
        total_em_conta = 0
        total_investido = 0
        
        for banco in bancos:
            result += f"🏦 {banco['NOME_BANCO']} (ID: {banco['ID_BANCO']})\n"
            result += f"   💰 Em conta: R$ {banco['VALOR_EM_CONTA']:.2f}\n"
            result += f"   📈 Investido: R$ {banco['VALOR_INVESTIDO']:.2f}\n\n"
            total_em_conta += banco['VALOR_EM_CONTA']
            total_investido += banco['VALOR_INVESTIDO']
        
        result += f"**TOTAIS:**\n"
        result += f"Total em conta: R$ {total_em_conta:.2f}\n"
        result += f"Total investido: R$ {total_investido:.2f}\n"
        result += f"**Total geral: R$ {(total_em_conta + total_investido):.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar bancos: {str(e)}"


# ==================== CONSULTAS DE CARTÕES ====================

def get_cartoes_info(_: str = "") -> str:
    """Retorna informações sobre todos os cartões de crédito."""
    try:
        service = PostgresService()
        cartoes = service.get_all_cartoes()
        
        if not cartoes:
            return "Nenhum cartão de crédito cadastrado."
        
        result = "💳 **CARTÕES DE CRÉDITO**\n\n"
        
        for cartao in cartoes:
            tipo_map = {1: "Débito", 2: "Crédito", 3: "Múltiplo"}
            tipo = tipo_map.get(cartao['TIPO_CARTAO'], "Desconhecido")
            
            result += f"💳 {cartao['NOME_CARTAO']} (ID: {cartao['ID_CARTAO']})\n"
            result += f"   Tipo: {tipo}\n"
            result += f"   Banco ID: {cartao['ID_BANCO']}\n"
            result += f"   Vencimento: Dia {cartao['DIA_VENCIMENTO']}\n\n"
        
        return result
    except Exception as e:
        return f"Erro ao consultar cartões: {str(e)}"


# ==================== CONSULTAS DE FATURAS ====================

def get_faturas_pendentes(_: str = "") -> str:
    """Retorna todas as faturas não pagas."""
    try:
        service = PostgresService()
        faturas = service.get_faturas_nao_pagas()
        
        if not faturas:
            return "✅ Não há faturas pendentes! Todas as faturas estão pagas."
        
        result = "⚠️ **FATURAS PENDENTES**\n\n"
        total_pendente = 0
        
        for fatura in faturas:
            result += f"📄 Fatura ID: {fatura['ID_FATURA_CARTAO_CREDITO']}\n"
            result += f"   Cartão ID: {fatura['ID_CARTAO']}\n"
            result += f"   Período: {fatura['MES_FATURA']:02d}/{fatura['ANO_FATURA']}\n"
            result += f"   💰 Valor: R$ {fatura['VALOR_FATURA']:.2f}\n\n"
            total_pendente += fatura['VALOR_FATURA']
        
        result += f"**TOTAL PENDENTE: R$ {total_pendente:.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar faturas: {str(e)}"


def analyze_faturas_por_cartao(_: str = "") -> str:
    """Analisa e compara faturas por cartão, mostrando qual cartão tem maior fatura."""
    try:
        service = PostgresService()
        faturas = service.get_all_faturas()
        cartoes = service.get_all_cartoes()
        
        if not faturas:
            return "Nenhuma fatura cadastrada no sistema."
        
        # Dicionário para armazenar total por cartão
        totais_por_cartao = {}
        cartoes_map = {c['ID_CARTAO']: c['NOME_CARTAO'] for c in cartoes}
        
        for fatura in faturas:
            id_cartao = fatura['ID_CARTAO']
            valor = fatura['VALOR_FATURA']
            
            if id_cartao not in totais_por_cartao:
                totais_por_cartao[id_cartao] = 0
            totais_por_cartao[id_cartao] += valor
        
        # Ordenar por valor (maior para menor)
        cartoes_ordenados = sorted(totais_por_cartao.items(), key=lambda x: x[1], reverse=True)
        
        result = "📊 **ANÁLISE DE FATURAS POR CARTÃO**\n\n"
        
        for i, (id_cartao, total) in enumerate(cartoes_ordenados, 1):
            nome_cartao = cartoes_map.get(id_cartao, f"Cartão {id_cartao}")
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "💳"
            result += f"{emoji} {nome_cartao}\n"
            result += f"   Total: R$ {total:.2f}\n\n"
        
        # Destacar o maior
        if cartoes_ordenados:
            id_maior = cartoes_ordenados[0][0]
            valor_maior = cartoes_ordenados[0][1]
            nome_maior = cartoes_map.get(id_maior, f"Cartão {id_maior}")
            result += f"\n🏆 **MAIOR FATURA:** {nome_maior} com R$ {valor_maior:.2f}"
        
        return result
    except Exception as e:
        return f"Erro ao analisar faturas: {str(e)}"


# ==================== CONSULTAS DE ENTRADAS E SAÍDAS ====================

def get_entradas_info(_: str = "") -> str:
    """Retorna informações sobre todas as entradas (receitas)."""
    try:
        service = PostgresService()
        entradas = service.get_all_entradas()
        
        if not entradas:
            return "Nenhuma entrada cadastrada."
        
        result = "💰 **ENTRADAS (RECEITAS)**\n\n"
        total = 0
        
        for entrada in entradas:
            result += f"✅ {entrada['NOME_ENTRADA']} (ID: {entrada['ID_ENTRADA']})\n"
            result += f"   Tipo: {entrada['TIPO_ENTRADA']}\n"
            result += f"   Valor: R$ {entrada['VALOR_ENTRADA']:.2f}\n"
            result += f"   Dia de entrada: {entrada['DIA_ENTRADA']}\n"
            result += f"   Banco ID: {entrada['ID_BANCO']}\n\n"
            total += entrada['VALOR_ENTRADA']
        
        result += f"**TOTAL DE ENTRADAS MENSAIS: R$ {total:.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar entradas: {str(e)}"


def get_saidas_info(_: str = "") -> str:
    """Retorna informações sobre todas as saídas frequentes."""
    try:
        service = PostgresService()
        saidas = service.get_all_saidas_frequentes()
        
        if not saidas:
            return "Nenhuma saída frequente cadastrada."
        
        result = "💸 **SAÍDAS FREQUENTES**\n\n"
        total = 0
        
        for saida in saidas:
            result += f"❌ {saida['NOME_SAIDA']} (ID: {saida['ID_SAIDA_FREQUENTE']})\n"
            result += f"   Tipo: {saida['TIPO_SAIDA']}\n"
            result += f"   Valor: R$ {saida['VALOR_SAIDA']:.2f}\n"
            result += f"   Dia de saída: {saida['DIA_SAIDA']}\n\n"
            total += saida['VALOR_SAIDA']
        
        result += f"**TOTAL DE SAÍDAS MENSAIS: R$ {total:.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar saídas: {str(e)}"


# ==================== ANÁLISE FINANCEIRA ====================

def analyze_balance(_: str = "") -> str:
    """Analisa o balanço financeiro entre entradas e saídas."""
    try:
        service = PostgresService()
        entradas = service.get_all_entradas()
        saidas = service.get_all_saidas_frequentes()
        faturas_pendentes = service.get_faturas_nao_pagas()
        
        total_entradas = sum(e['VALOR_ENTRADA'] for e in entradas)
        total_saidas = sum(s['VALOR_SAIDA'] for s in saidas)
        total_faturas_pendentes = sum(f['VALOR_FATURA'] for f in faturas_pendentes)
        
        saldo = total_entradas - total_saidas - total_faturas_pendentes
        
        result = "📊 **ANÁLISE FINANCEIRA**\n\n"
        result += f"💰 Entradas mensais: R$ {total_entradas:.2f}\n"
        result += f"💸 Saídas frequentes: R$ {total_saidas:.2f}\n"
        result += f"⚠️ Faturas pendentes: R$ {total_faturas_pendentes:.2f}\n"
        result += f"{'─' * 40}\n"
        
        if saldo >= 0:
            result += f"✅ **Saldo disponível: R$ {saldo:.2f}**\n"
            result += "Status: Positivo! 😊"
        else:
            result += f"❌ **Déficit: R$ {abs(saldo):.2f}**\n"
            result += "Status: Atenção! Gastos excedem receitas. ⚠️"
        
        return result
    except Exception as e:
        return f"Erro ao analisar balanço: {str(e)}"


# ==================== CONSULTAS DE COMPRAS ====================

def get_compras_por_categoria(_: str = "") -> str:
    """Retorna análise de compras agrupadas por categoria."""
    try:
        service = PostgresService()
        compras = service.get_all_compras_cartao()
        categorias = service.get_all_categorias()
        
        if not compras:
            return "Nenhuma compra cadastrada."
        
        # Criar mapa de categorias
        categorias_map = {c['ID_CATEGORIA']: c['NOME_CATEGORIA'] for c in categorias}
        
        # Agrupar por categoria
        totais_por_categoria = {}
        for compra in compras:
            id_cat = compra['ID_CATEGORIA']
            nome_cat = categorias_map.get(id_cat, "Sem categoria")
            valor = compra['VALOR_COMPRA']
            
            if nome_cat not in totais_por_categoria:
                totais_por_categoria[nome_cat] = 0
            totais_por_categoria[nome_cat] += valor
        
        # Ordenar por valor
        categorias_ordenadas = sorted(totais_por_categoria.items(), key=lambda x: x[1], reverse=True)
        
        result = "🛒 **COMPRAS POR CATEGORIA**\n\n"
        total_geral = 0
        
        for categoria, total in categorias_ordenadas:
            result += f"📦 {categoria}: R$ {total:.2f}\n"
            total_geral += total
        
        result += f"\n{'─' * 40}\n"
        result += f"**TOTAL GERAL: R$ {total_geral:.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar compras por categoria: {str(e)}"


# ==================== INSERÇÃO DE DADOS ====================

def insert_compra_cartao(input_json: str) -> str:
    """Insere uma nova compra de cartão de crédito.
    
    Formato esperado (JSON):
    {
        "id_cartao": 1,
        "id_banco": 1,
        "data_compra": "2024-12-23",
        "estabelecimento": "Nome do estabelecimento",
        "parcelas": "1 de 1" ou "3 de 4",
        "id_categoria": 1,
        "valor_compra": 150.00,
        "observacoes": "Observação opcional"
    }
    """
    try:
        data = json.loads(input_json)
        service = PostgresService()
        
        # Converter data string para date object
        from datetime import datetime
        data_compra = datetime.strptime(data['data_compra'], '%Y-%m-%d').date()
        
        id_compra = service.insert_compra_cartao(
            id_cartao=data['id_cartao'],
            id_banco=data['id_banco'],
            data_compra=data_compra,
            estabelecimento=data['estabelecimento'],
            parcelas=data['parcelas'],
            id_categoria=data['id_categoria'],
            valor_compra=data['valor_compra'],
            observacoes=data.get('observacoes')
        )
        
        return f"✅ Compra inserida com sucesso! ID: {id_compra}"
    except json.JSONDecodeError:
        return "❌ Erro: JSON inválido. Verifique o formato dos dados."
    except Exception as e:
        return f"❌ Erro ao inserir compra: {str(e)}"



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

bancos_tool = Tool(
    name="GetBancosInfo",
    func=get_bancos_info,
    description="Retorna informações sobre todos os bancos cadastrados, incluindo valores em conta e investidos."
)

cartoes_tool = Tool(
    name="GetCartoesInfo",
    func=get_cartoes_info,
    description="Retorna informações sobre todos os cartões de crédito cadastrados."
)

faturas_pendentes_tool = Tool(
    name="GetFaturasPendentes",
    func=get_faturas_pendentes,
    description="Retorna todas as faturas de cartão de crédito que ainda não foram pagas."
)

analyze_faturas_tool = Tool(
    name="AnalyzeFaturasPorCartao",
    func=analyze_faturas_por_cartao,
    description=(
        "Analisa e compara todas as faturas por cartão de crédito. "
        "Mostra qual cartão tem o maior valor total de faturas. "
        "Use quando o usuário perguntar sobre qual cartão tem mais gastos ou maior fatura."
    )
)

entradas_tool = Tool(
    name="GetEntradasInfo",
    func=get_entradas_info,
    description="Retorna informações sobre todas as entradas (receitas) cadastradas."
)

saidas_tool = Tool(
    name="GetSaidasInfo",
    func=get_saidas_info,
    description="Retorna informações sobre todas as saídas frequentes (despesas recorrentes)."
)

balance_tool = Tool(
    name="AnalyzeFinancialBalance",
    func=analyze_balance,
    description=(
        "Analisa o balanço financeiro completo, comparando entradas, saídas e faturas pendentes. "
        "Use quando o usuário perguntar sobre sua situação financeira geral ou saldo disponível."
    )
)

compras_categoria_tool = Tool(
    name="GetComprasPorCategoria",
    func=get_compras_por_categoria,
    description=(
        "Retorna análise de todas as compras agrupadas por categoria. "
        "Mostra quanto foi gasto em cada categoria."
    )
)

insert_compra_tool = Tool(
    name="InsertCompraCartao",
    func=insert_compra_cartao,
    description=(
        "Insere uma nova compra de cartão de crédito. "
        "Requer JSON com: id_cartao, id_banco, data_compra, estabelecimento, parcelas, id_categoria, valor_compra, observacoes (opcional)."
    )
)