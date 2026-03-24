from langchain_community.tools import Tool
from app.core.config import get_site_config_url
from app.services.postgres_service import PostgresService
from app.services.bancos_service import BancosService
from app.services.cartoes_service import CartoesService
from app.services.faturas_cartoes_de_credito_service import FaturasCartoesDeCreditoService
from app.services.entradas_service import EntradasService
from app.services.saidas_realizadas_service import SaidasRealizadasService
from app.services.compras_cartao_service import ComprasCartaoService
from app.services.categorias_service import CategoriasService
from datetime import datetime
import json
import re
from typing import Dict, Any

# Dicionário para armazenar compras pendentes de aprovação
# Estrutura: {phone_number: {compra_data, timestamp}}
pending_purchases: Dict[str, Dict[str, Any]] = {}


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
        service = CartoesService()
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
        faturas_cartoes_service = FaturasCartoesDeCreditoService()
        cartoes_service =  CartoesService()
        faturas = faturas_cartoes_service.get_all_faturas()
        cartoes = cartoes_service.get_all_cartoes()
        
        if not faturas:
            return "Nenhuma fatura cadastrada no sistema."
        
        # Dicionário para armazenar total por cartão
        totais_por_cartao = {}
        cartoes_map = {c.id_cartao: c.nome_cartao for c in cartoes}
        
        for fatura in faturas:
            id_cartao = fatura.id_cartao
            valor = fatura.valor_fatura
            
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
        service = SaidasRealizadasService()
        saidas = service.get_all_saidas_realizadas()
        
        if not saidas:
            return "Nenhuma saída realizada cadastrada."
        
        result = "💸 **SAÍDAS REALIZADAS**\n\n"
        total = 0
        
        for saida in saidas:
            result += f"❌ {saida.descricao} (ID: {saida.id_saida})\n"
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
        saida_service = SaidasRealizadasService()
        faturas_service = FaturasCartoesDeCreditoService()
        entradas = entrada_service.get_all_entradas()
        saidas = saida_service.get_all_saidas_realizadas()
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

def get_categorias_disponiveis(_: str = "") -> str:
    """Retorna lista de todas as categorias disponíveis para classificação de compras."""
    try:
        categorias_service = CategoriasService()
        categorias = categorias_service.get_all_categorias()
        
        if not categorias:
            return "Nenhuma categoria cadastrada no sistema."
        
        result = "📋 **CATEGORIAS DISPONÍVEIS**\n\n"
        
        for cat in categorias:
            result += f"{cat.id_categoria}. {cat.nome_categoria}\n"
        
        result += "\n💡 Para adicionar uma compra, você pode usar o ID ou nome da categoria.\n"
        result += "Se a categoria não existir, será criada automaticamente."
        
        return result
    except Exception as e:
        return f"Erro ao consultar categorias: {str(e)}"
    
def get_compras_por_categoria(_: str = "") -> str:
    """Retorna análise de compras agrupadas por categoria."""
    try:
        compras_service = ComprasCartaoService()
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
    if not parcelas_input or parcelas_input.strip() == '':
        return '1 de 1'
    
    parcelas_str = str(parcelas_input).strip()
    
    # Se já está no formato "X de Y", retornar como está
    if ' de ' in parcelas_str.lower():
        return parcelas_str
    
    # Tentar extrair apenas o número de parcelas
    # Aceita: "3", "3x", "3 vezes", "parcelado em 3", etc.
    match = re.search(r'(\d+)', parcelas_str)
    if match:
        num_parcelas = match.group(1)
        return f"1 de {num_parcelas}"
    
    # Se não conseguiu extrair, retornar padrão
    return '1 de 1'


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
        phone_number = data.get('phone_number')
        if not phone_number:
            return "❌ Erro: número de telefone não fornecido. Não é possível armazenar compra para confirmação."
        
        # Processar data
        data_compra_input = data.get('data_compra', datetime.now().strftime('%Y-%m-%d'))
        if data_compra_input.lower() in ['hoje', 'hj']:
            data_compra = datetime.now().date()
        else:
            try:
                data_compra = datetime.strptime(data_compra_input, '%Y-%m-%d').date()
            except:
                try:
                    data_compra = datetime.strptime(data_compra_input, '%d/%m/%Y').date()
                except:
                    data_compra = datetime.now().date()
        
        # Processar parcelas
        parcelas_input = data.get('parcelas', '1 de 1')
        parcelas = _processar_parcelas(parcelas_input)
        
        # Processar observações
        observacoes = data.get('observacoes', None)
        
        # Processar categoria
        id_categoria = data.get('id_categoria')
        nome_categoria_final = ""
        
        if not id_categoria:
            nome_categoria = data.get('nome_categoria')
            if nome_categoria:
                id_categoria = categorias_service.get_or_create_categoria(nome_categoria)
                nome_categoria_final = nome_categoria
            else:
                estabelecimento = data['estabelecimento']
                id_categoria = categorias_service.get_or_create_categoria(estabelecimento)
                nome_categoria_final = estabelecimento
        else:
            categoria = categorias_service.get_categoria_by_id(id_categoria)
            nome_categoria_final = categoria.nome_categoria if categoria else "Não identificada"
        
        # Obter nome do cartão
        cartao = cartoes_service.get_cartao_by_id(data['id_cartao'])
        nome_cartao = cartao.nome_cartao if cartao else f"Cartão ID {data['id_cartao']}"
        
        # Armazenar compra pendente
        compra_data = {
            'id_cartao': data['id_cartao'],
            'id_banco': data['id_banco'],
            'data_compra': data_compra.strftime('%Y-%m-%d'),
            'estabelecimento': data['estabelecimento'],
            'parcelas': parcelas,
            'id_categoria': id_categoria,
            'valor_compra': float(data['valor_compra']),
            'observacoes': observacoes,
            'timestamp': datetime.now().isoformat()
        }
        
        pending_purchases[phone_number] = compra_data
        
        # Retornar resumo para aprovação
        valor_formatado = f"R$ {data['valor_compra']:.2f}".replace('.', ',')
        data_formatada = data_compra.strftime('%d/%m/%Y')
        
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
        phone_number = data.get('phone_number')
        confirmed = data.get('confirmed', False)
        
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
        
        data_compra = datetime.strptime(compra_data['data_compra'], '%Y-%m-%d').date()
        
        id_compra = compras_service.insert_compra_cartao(
            id_cartao=compra_data['id_cartao'],
            data_compra=data_compra,
            estabelecimento=compra_data['estabelecimento'],
            id_categoria=compra_data['id_categoria'],
            valor_compra=compra_data['valor_compra'],
            observacoes=compra_data['observacoes'],
            numero_parcelas=compra_data['numero_parcelas'] if 'numero_parcelas' in compra_data else 1,
            parcela_atual=compra_data['parcela_atual'] if 'parcela_atual' in compra_data else 1
        )
        
        # Limpar compra pendente
        del pending_purchases[phone_number]
        
        # Obter nome da categoria
        categoria = categorias_service.get_categoria_by_id(compra_data['id_categoria'])
        nome_cat = categoria.nome_categoria if categoria else "Não identificada"
        
        valor_formatado = f"R$ {compra_data['valor_compra']:.2f}".replace('.', ',')
        
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
        data_compra = datetime.strptime(data['data_compra'], '%Y-%m-%d').date()
        
        # Processar parcelas (padrão: "1 de 1")
        parcelas_input = data.get('parcelas', '1 de 1')
        parcelas = _processar_parcelas(parcelas_input)
        
        # Processar observações (padrão: None)
        observacoes = data.get('observacoes', None)
        
        # Processar categoria (SEMPRE OBRIGATÓRIO)
        id_categoria = data.get('id_categoria')
        
        if not id_categoria:
            # Tentar buscar por nome_categoria
            nome_categoria = data.get('nome_categoria')
            
            if nome_categoria:
                # Buscar ou criar categoria com o nome fornecido
                id_categoria = categorias_service.get_or_create_categoria(nome_categoria)
            else:
                # Tentar inferir do estabelecimento
                estabelecimento = data['estabelecimento']
                # Usar o nome do estabelecimento como categoria
                id_categoria = categorias_service.get_or_create_categoria(estabelecimento)
        
        # Inserir a compra
        id_compra = compras_service.insert_compra_cartao(
                id_cartao=data['id_cartao'],
                data_compra=data_compra,
                estabelecimento=data['estabelecimento'],
                id_categoria=id_categoria,
                valor_compra=data['valor_compra'],
                observacoes=data['observacoes'],
                numero_parcelas=data['numero_parcelas'] if 'numero_parcelas' in data else 1,
                parcela_atual=data['parcela_atual'] if 'parcela_atual' in data else 1
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

categorias_tool = Tool(
    name="GetCategoriasDisponiveis",
    func=get_categorias_disponiveis,
    description=(
        "Lista todas as categorias disponíveis no sistema para classificação de compras. "
        "Use esta tool quando o usuário perguntar sobre categorias ou quando precisar saber quais categorias existem."
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
    )
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
    )
)

insert_compra_tool = Tool(
    name="InsertCompraCartao",
    func=insert_compra_cartao,
    description=(
        "DEPRECATED: Use PrepareCompraCartao + ConfirmCompraCartao ao invés desta. "
        "Esta tool ainda existe para compatibilidade, mas o fluxo correto é: "
        "1) PrepareCompraCartao para mostrar resumo ao usuário "
        "2) ConfirmCompraCartao para salvar após aprovação."
    )
)