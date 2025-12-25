from langchain_community.tools import Tool
from app.core.config import get_site_config_url
from app.services.postgres_service import PostgresService
from app.services.bancos_service import BancosService
from app.services.cartoes_credito_service import CartoesCreditoService
from app.services.faturas_cartoes_de_credito_service import FaturasCartoesDeCreditoService
from app.services.entradas_service import EntradasService
from app.services.saidas_frequentes_service import SaidasFrequentesService
from app.services.compras_cartao_de_credito_service import ComprasCartaoDeCreditoService
from app.services.categorias_service import CategoriasService
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

def get_bancos_info(_: str = "") -> str:
    """Retorna informações sobre todos os bancos cadastrados."""
    try:
        service = BancosService()
        bancos = service.get_all_bancos()
        
        if not bancos:
            return "Nenhum banco cadastrado no sistema."
        
        result = "📊 **BANCOS CADASTRADOS**\n\n"
        total_em_conta = 0
        total_investido = 0
        
        for banco in bancos:
            result += f"🏦 {banco.nome_banco} (ID: {banco.id_banco})\n"
            result += f"   💰 Em conta: R$ {banco.valor_em_conta:.2f}\n"
            result += f"   📈 Investido: R$ {banco.valor_investido:.2f}\n\n"
            total_em_conta += banco.valor_em_conta
            total_investido += banco.valor_investido
        
        result += f"**TOTAIS:**\n"
        result += f"Total em conta: R$ {total_em_conta:.2f}\n"
        result += f"Total investido: R$ {total_investido:.2f}\n"
        result += f"**Total geral: R$ {(total_em_conta + total_investido):.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar bancos: {str(e)}"

def get_cartoes_info(_: str = "") -> str:
    """Retorna informações sobre todos os cartões de crédito."""
    try:
        service = CartoesCreditoService()
        cartoes = service.get_all_cartoes()
        
        if not cartoes:
            return "Nenhum cartão de crédito cadastrado."
        
        result = "💳 **CARTÕES DE CRÉDITO**\n\n"
        
        for cartao in cartoes:
            tipo = cartao.tipo_cartao
            result += f"💳 {cartao.nome_cartao} (ID: {cartao.id_cartao})\n"
            result += f"   Tipo: {tipo}\n"
            result += f"   Banco ID: {cartao.id_banco}\n"
            result += f"   Vencimento: Dia {cartao.dia_vencimento}\n\n"
        
        return result
    except Exception as e:
        return f"Erro ao consultar cartões: {str(e)}"

def get_faturas_pendentes(_: str = "") -> str:
    """Retorna todas as faturas não pagas."""
    try:
        service = FaturasCartoesDeCreditoService()
        faturas = service.get_faturas_nao_pagas()
        
        if not faturas:
            return "✅ Não há faturas pendentes! Todas as faturas estão pagas."
        
        result = "⚠️ **FATURAS PENDENTES**\n\n"
        total_pendente = 0
        
        for fatura in faturas:
            result += f"📄 Fatura ID: {fatura.id_fatura_cartao_credito}\n"
            result += f"   Cartão ID: {fatura.id_cartao}\n"
            result += f"   Período: {fatura.mes_fatura:02d}/{fatura.ano_fatura}\n"
            result += f"   💰 Valor: R$ {fatura.valor_fatura:.2f}\n\n"
            total_pendente += fatura.valor_fatura
        
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

def get_entradas_info(_: str = "") -> str:
    """Retorna informações sobre todas as entradas (receitas)."""
    try:
        service = EntradasService()
        entradas = service.get_all_entradas()
        
        if not entradas:
            return "Nenhuma entrada cadastrada."
        
        result = "💰 **ENTRADAS (RECEITAS)**\n\n"
        total = 0
        
        for entrada in entradas:
            result += f"✅ {entrada.nome_entrada} (ID: {entrada.id_entrada})\n"
            result += f"   Tipo: {entrada.tipo_entrada}\n"
            result += f"   Valor: R$ {entrada.valor_entrada:.2f}\n"
            result += f"   Dia de entrada: {entrada.dia_entrada}\n"
            result += f"   Banco ID: {entrada.id_banco}\n\n"
            total += entrada.valor_entrada
        
        result += f"**TOTAL DE ENTRADAS MENSAIS: R$ {total:.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar entradas: {str(e)}"

def get_saidas_info(_: str = "") -> str:
    """Retorna informações sobre todas as saídas frequentes."""
    try:
        service = SaidasFrequentesService()
        saidas = service.get_all_saidas_frequentes()
        
        if not saidas:
            return "Nenhuma saída frequente cadastrada."
        
        result = "💸 **SAÍDAS FREQUENTES**\n\n"
        total = 0
        
        for saida in saidas:
            result += f"❌ {saida.nome_saida} (ID: {saida.id_saida_frequente})\n"
            result += f"   Tipo: {saida.tipo_saida}\n"
            result += f"   Valor: R$ {saida.valor_saida:.2f}\n"
            result += f"   Dia de saída: {saida.dia_saida}\n\n"
            total += saida.valor_saida
        
        result += f"**TOTAL DE SAÍDAS MENSAIS: R$ {total:.2f}**"
        
        return result
    except Exception as e:
        return f"Erro ao consultar saídas: {str(e)}"

def analyze_balance(_: str = "") -> str:
    """Analisa o balanço financeiro entre entradas e saídas."""
    try:
        entrada_service = EntradasService()
        saida_service = SaidasFrequentesService()
        faturas_service = FaturasCartoesDeCreditoService()
        entradas = entrada_service.get_all_entradas()
        saidas = saida_service.get_all_saidas_frequentes()
        faturas_pendentes = faturas_service.get_faturas_nao_pagas()
        
        total_entradas = sum(e.valor_entrada for e in entradas)
        total_saidas = sum(s.valor_saida for s in saidas)
        total_faturas_pendentes = sum(f.valor_fatura for f in faturas_pendentes)
        
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

def get_compras_por_categoria(_: str = "") -> str:
    """Retorna análise de compras agrupadas por categoria."""
    try:
        compras_service = ComprasCartaoDeCreditoService()
        categorias_service = CategoriasService()
        compras = compras_service.get_all_compras_cartao()
        categorias = categorias_service.get_all_categorias()
        
        if not compras:
            return "Nenhuma compra cadastrada."
        
        # Criar mapa de categorias
        categorias_map = {c.id_categoria: c.nome_categoria for c in categorias}
        
        # Agrupar por categoria
        totais_por_categoria = {}
        for compra in compras:
            id_cat = compra.id_categoria
            nome_cat = categorias_map.get(id_cat, "Sem categoria")
            valor = compra.valor_compra
            
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
        service = ComprasCartaoDeCreditoService()
        
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
        "Pode usar a função get_categories para obter as categorias inseridas pelo usuario, se não se encaixar em nenhuma pode criar uma nova categoria"
    )
)