from langchain_community.tools import Tool
from app.core.config import get_bigquery_client
import pandas as pd
import json
from datetime import datetime
import fitz  # PyMuPDF
import re
from typing import Dict, List, Optional

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

def extract_bank_statement_from_pdf(pdf_path: str) -> str:
    """
    Extrai texto de um PDF de fatura bancária e retorna dados estruturados em JSON.
    
    Args:
        pdf_path (str): Caminho para o arquivo PDF
        
    Returns:
        str: JSON com as transações extraídas ou mensagem de erro
    """
    try:
        # Abre o PDF
        doc = fitz.open(pdf_path)
        full_text = ""
        
        # Extrai texto de todas as páginas
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            full_text += text + "\n"
        
        doc.close()
        
        # Identifica o banco baseado no texto
        bank_type = identify_bank_type(full_text)
        
        # Extrai transações baseado no tipo de banco
        transactions = extract_transactions_by_bank(full_text, bank_type)
        
        # Retorna como JSON
        result = {
            "bank_type": bank_type,
            "extracted_text_sample": full_text[:500] + "..." if len(full_text) > 500 else full_text,
            "transactions_count": len(transactions),
            "transactions": transactions
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return f"Erro ao processar PDF: {str(e)}"

def identify_bank_type(text: str) -> str:
    """Identifica o tipo de banco baseado no texto extraído"""
    text_lower = text.lower()
    
    if "nubank" in text_lower or "nu pagamentos" in text_lower:
        return "nubank"
    elif "itaú" in text_lower or "itau" in text_lower:
        return "itau"
    elif "bradesco" in text_lower:
        return "bradesco"
    elif "banco do brasil" in text_lower or "bb.com.br" in text_lower:
        return "banco_brasil"
    elif "santander" in text_lower:
        return "santander"
    elif "caixa" in text_lower or "cef" in text_lower:
        return "caixa"
    else:
        return "unknown"

def extract_transactions_by_bank(text: str, bank_type: str) -> List[Dict]:
    """Extrai transações baseado no tipo de banco"""
    transactions = []
    
    if bank_type == "nubank":
        transactions = extract_nubank_transactions(text)
    elif bank_type == "itau":
        transactions = extract_itau_transactions(text)
    elif bank_type == "bradesco":
        transactions = extract_bradesco_transactions(text)
    else:
        # Extração genérica para bancos não identificados
        transactions = extract_generic_transactions(text)
    
    return transactions

def extract_nubank_transactions(text: str) -> List[Dict]:
    """Extrai transações específicas do Nubank"""
    transactions = []
    lines = text.split('\n')
    
    # Padrões comuns do Nubank
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    value_pattern = r'R\$\s*[\d.,]+'
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # Procura por padrões de data
        date_match = re.search(date_pattern, line)
        if date_match:
            # Procura por valor na mesma linha ou próximas
            value_match = re.search(value_pattern, line)
            if not value_match and i + 1 < len(lines):
                value_match = re.search(value_pattern, lines[i + 1])
            
            if value_match:
                # Extrai descrição (remove data e valor)
                description = re.sub(date_pattern, '', line)
                description = re.sub(value_pattern, '', description).strip()
                
                # Limpa descrição
                description = clean_description(description)
                
                if description:  # Só adiciona se tiver descrição válida
                    transaction = {
                        "data": date_match.group(),
                        "descricao": description,
                        "valor": clean_value(value_match.group()),
                        "banco": "nubank"
                    }
                    transactions.append(transaction)
    
    return transactions

def extract_itau_transactions(text: str) -> List[Dict]:
    """Extrai transações específicas do Itaú"""
    transactions = []
    lines = text.split('\n')
    
    date_pattern = r'\d{2}/\d{2}'
    value_pattern = r'[\d.,]+\s*[CD]?'
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Padrão típico do Itaú: data + descrição + valor
        parts = line.split()
        if len(parts) >= 3:
            # Verifica se o primeiro item é uma data
            if re.match(date_pattern, parts[0]):
                date = parts[0]
                # Último item geralmente é o valor
                if re.search(r'[\d,]', parts[-1]):
                    value = parts[-1]
                    # Descrição é o que sobra no meio
                    description = ' '.join(parts[1:-1])
                    description = clean_description(description)
                    
                    if description:
                        transaction = {
                            "data": f"{date}/2025",  # Assume ano atual
                            "descricao": description,
                            "valor": clean_value(value),
                            "banco": "itau"
                        }
                        transactions.append(transaction)
    
    return transactions

def extract_bradesco_transactions(text: str) -> List[Dict]:
    """Extrai transações específicas do Bradesco"""
    transactions = []
    # Implementar padrões específicos do Bradesco
    # Similar aos outros bancos, mas com padrões específicos
    return extract_generic_transactions(text)

def extract_generic_transactions(text: str) -> List[Dict]:
    """Extração genérica para bancos não identificados"""
    transactions = []
    lines = text.split('\n')
    
    # Padrões genéricos
    date_pattern = r'\d{1,2}[/\-\.]\d{1,2}[/\-\.](\d{4}|\d{2})'
    value_pattern = r'R?\$?\s*[\d.,]+'
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:  # Ignora linhas muito pequenas
            continue
            
        date_match = re.search(date_pattern, line)
        value_match = re.search(value_pattern, line)
        
        if date_match and value_match:
            # Remove data e valor para obter descrição
            description = line
            description = re.sub(date_pattern, '', description)
            description = re.sub(value_pattern, '', description)
            description = clean_description(description)
            
            if description:
                transaction = {
                    "data": date_match.group(),
                    "descricao": description,
                    "valor": clean_value(value_match.group()),
                    "banco": "generic"
                }
                transactions.append(transaction)
    
    return transactions

def clean_description(description: str) -> str:
    """Limpa e normaliza a descrição da transação"""
    if not description:
        return ""
    
    # Remove caracteres especiais desnecessários
    description = re.sub(r'[^\w\s\-\.]', ' ', description)
    # Remove espaços múltiplos
    description = re.sub(r'\s+', ' ', description)
    # Remove espaços no início e fim
    description = description.strip()
    
    # Remove palavras muito comuns que não agregam valor
    stop_words = ['em', 'de', 'da', 'do', 'na', 'no', 'para', 'por', 'com']
    words = description.split()
    filtered_words = [word for word in words if word.lower() not in stop_words or len(words) <= 3]
    
    return ' '.join(filtered_words)

def clean_value(value_str: str) -> str:
    """Limpa e normaliza o valor monetário"""
    if not value_str:
        return "0.00"
    
    # Remove símbolos e letras
    cleaned = re.sub(r'[^\d.,\-]', '', value_str)
    
    # Normaliza separadores decimais
    if ',' in cleaned and '.' in cleaned:
        # Se tem ambos, assume que vírgula é decimal
        cleaned = cleaned.replace('.', '').replace(',', '.')
    elif ',' in cleaned:
        # Se só tem vírgula, pode ser decimal ou milhares
        parts = cleaned.split(',')
        if len(parts) == 2 and len(parts[1]) <= 2:
            # Provavelmente decimal
            cleaned = cleaned.replace(',', '.')
    
    try:
        # Tenta converter para garantir formato válido
        float_val = float(cleaned)
        return f"{float_val:.2f}"
    except:
        return "0.00"

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

pdf_extract_tool = Tool(
    name="ExtractBankStatementPDF",
    func=extract_bank_statement_from_pdf,
    description="Extrai dados de transações financeiras de um PDF de fatura bancária. Recebe o caminho do arquivo PDF e retorna um JSON estruturado com as transações extraídas. Suporta múltiplos bancos como Nubank, Itaú, Bradesco, etc."
)

def process_pdf_and_insert_to_db(pdf_path: str) -> str:
    """
    Processa um PDF de fatura bancária e insere as transações diretamente no banco de dados.
    
    Args:
        pdf_path (str): Caminho para o arquivo PDF
        
    Returns:
        str: Resultado da operação
    """
    try:
        # Extrai dados do PDF
        extraction_result = extract_bank_statement_from_pdf(pdf_path)
        
        # Parse do resultado JSON
        data = json.loads(extraction_result)
        
        if "transactions" not in data or not data["transactions"]:
            return "Nenhuma transação encontrada no PDF."
        
        # Insere cada transação no banco
        successful_inserts = 0
        failed_inserts = 0
        errors = []
        
        for transaction in data["transactions"]:
            try:
                # Converte para formato esperado pelo BigQuery
                formatted_transaction = {
                    "data": transaction["data"],
                    "descricao": transaction["descricao"],
                    "valor": float(transaction["valor"]),
                    "banco": transaction.get("banco", "unknown"),
                    "data_insercao": datetime.now().isoformat()
                }
                
                result = insert_data_to_bigquery(json.dumps(formatted_transaction))
                
                if "sucesso" in result.lower():
                    successful_inserts += 1
                else:
                    failed_inserts += 1
                    errors.append(f"Erro na transação {transaction['descricao']}: {result}")
                    
            except Exception as e:
                failed_inserts += 1
                errors.append(f"Erro ao processar transação {transaction.get('descricao', 'N/A')}: {str(e)}")
        
        # Retorna resumo da operação
        summary = f"""
        Processamento concluído:
        - Total de transações encontradas: {len(data['transactions'])}
        - Inserções bem-sucedidas: {successful_inserts}
        - Inserções falharam: {failed_inserts}
        - Banco identificado: {data.get('bank_type', 'unknown')}
        """
        
        if errors:
            summary += f"\n\nErros encontrados:\n" + "\n".join(errors[:5])  # Limita a 5 erros
            
        return summary
        
    except Exception as e:
        return f"Erro ao processar PDF e inserir no banco: {str(e)}"

pdf_process_and_insert_tool = Tool(
    name="ProcessPDFAndInsertToDB",
    func=process_pdf_and_insert_to_db,
    description="Processa um PDF de fatura bancária, extrai as transações e as insere automaticamente no banco de dados BigQuery. Recebe o caminho do arquivo PDF e retorna um resumo da operação."
)